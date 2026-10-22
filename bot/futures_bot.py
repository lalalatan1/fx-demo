"""Multi-timeframe Binance USD-M testnet market-data bot; paper execution only."""
import argparse
import datetime as dt
import json
import math
import os
from pathlib import Path
import time
import urllib.parse
import urllib.request

BASE = 'https://demo-fapi.binance.com'
SYMBOLS = ('BTCUSDT', 'ETHUSDT')


def get(path, params=None):
    url = BASE + path + '?' + urllib.parse.urlencode(params or {})
    with urllib.request.urlopen(url, timeout=15) as response:
        return json.load(response)


def closed(rows, now_ms):
    return [r for r in rows if int(r[6]) < now_ms]


def ema(values, period):
    if len(values) < period:
        raise ValueError('Insufficient candles')
    value = sum(values[:period]) / period
    for price in values[period:]:
        value += 2 / (period + 1) * (price - value)
    return value


def signal(frames):
    """4h trend, 1h trend agreement, 15m twenty-bar breakout; ATR stop."""
    if any(len(frames[t]) < 60 for t in ('4h', '1h', '15m')):
        raise ValueError('Need at least 60 closed candles per timeframe')
    trends = []
    for tf in ('4h', '1h'):
        prices = [float(r[4]) for r in frames[tf]]
        fast, slow = ema(prices, 20), ema(prices, 50)
        trends.append(1 if prices[-1] > fast > slow else -1 if prices[-1] < fast < slow else 0)
    rows = frames['15m']
    price = float(rows[-1][4])
    previous = rows[-21:-1]
    side = 'LONG' if trends == [1, 1] and price > max(float(r[2]) for r in previous) else (
        'SHORT' if trends == [-1, -1] and price < min(float(r[3]) for r in previous) else None)
    ranges = [max(float(rows[i][2])-float(rows[i][3]),
                  abs(float(rows[i][2])-float(rows[i-1][4])),
                  abs(float(rows[i][3])-float(rows[i-1][4]))) for i in range(len(rows)-14, len(rows))]
    return side, 2 * sum(ranges) / 14, int(rows[-1][6])


def initial(equity):
    if not math.isfinite(equity) or equity <= 0:
        raise ValueError('Equity must be positive and finite')
    return dict(balance=equity, day='', day_equity=equity, positions={}, seen={}, trades=[])


def equity(state, prices):
    return state['balance'] + sum((prices[s]-p['entry'])*p['qty']*p['direction']
                                  for s, p in state['positions'].items())


def size(state, prices, symbol, distance):
    eq = equity(state, prices)
    if distance <= 0 or not math.isfinite(distance) or eq <= 0:
        return 0
    used = sum(p['qty']*prices[s] for s, p in state['positions'].items())
    # Risk includes estimated round-trip fees and adverse execution allowance.
    return max(0, min(eq*.005/(distance + prices[symbol]*.0012),
                      max(0, eq*2-used)/prices[symbol]))


def step(state, prices, candidates, now):
    if set(prices) != set(SYMBOLS) or any(not math.isfinite(p) or p <= 0 for p in prices.values()):
        raise ValueError('Invalid market snapshot')
    day = now.date().isoformat()
    if day != state['day']:
        state['day'], state['day_equity'] = day, equity(state, prices)
    events = []
    # Paper stop/target fills use observed prices: gaps can exceed intended risk.
    for symbol, p in list(state['positions'].items()):
        price = prices[symbol]
        if (price-p['stop'])*p['direction'] <= 0 or (price-p['target'])*p['direction'] >= 0:
            fill = price*(1-.0002*p['direction'])
            pnl = (fill-p['entry'])*p['qty']*p['direction'] - fill*p['qty']*.0004
            state['balance'] += pnl
            event = dict(symbol=symbol, action='CLOSE', price=fill, pnl=pnl, time=now.isoformat())
            state['trades'].append(event); events.append(event)
            del state['positions'][symbol]
    halted = equity(state, prices) <= state['day_equity']*.98
    for symbol, (side, distance, candle) in candidates.items():
        if state['seen'].get(symbol, -1) >= candle:
            continue
        state['seen'][symbol] = candle
        if halted or not side or symbol in state['positions'] or len(state['positions']) >= 2:
            continue
        qty = size(state, prices, symbol, distance)
        if qty <= 0:
            continue
        direction = 1 if side == 'LONG' else -1
        entry = prices[symbol]*(1+.0002*direction)
        state['balance'] -= entry*qty*.0004
        state['positions'][symbol] = dict(entry=entry, qty=qty, direction=direction,
                                         stop=entry-direction*distance, target=entry+direction*distance*2)
        events.append(dict(symbol=symbol, action=side, price=entry, qty=qty, time=now.isoformat()))
    return events


def save(path, state):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix('.tmp')
    tmp.write_text(json.dumps(state, indent=2, allow_nan=False))
    os.replace(tmp, path)


def run(args):
    # Exclusive local lock prevents two processes from trading the same paper account.
    import fcntl
    path = Path(args.state)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.with_suffix('.lock').open('w') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        state = json.loads(path.read_text()) if path.exists() else initial(args.equity)
        while True:
            try:
                now_ms = int(get('/fapi/v1/time')['serverTime'])
                frames = {s: {tf: closed(get('/fapi/v1/klines', dict(symbol=s, interval=tf, limit=150)), now_ms)
                              for tf in ('4h', '1h', '15m')} for s in SYMBOLS}
                prices = {s: float(get('/fapi/v1/premiumIndex', dict(symbol=s))['markPrice']) for s in SYMBOLS}
                now = dt.datetime.fromtimestamp(now_ms/1000, dt.timezone.utc)
                # Reject stale data rather than trading on an outdated signal.
                if any(now_ms-int(frames[s]['15m'][-1][6]) > 16*60*1000 for s in SYMBOLS):
                    raise ValueError('Stale market data')
                events = step(state, prices, {s: signal(frames[s]) for s in SYMBOLS}, now)
                save(path, state)
                print(json.dumps(dict(mode='PAPER', time=now.isoformat(), equity=equity(state, prices),
                                      positions=state['positions'], events=events)), flush=True)
            except Exception as exc:
                print(json.dumps(dict(mode='PAPER', error=str(exc))), flush=True)
                if args.once:
                    raise
            if args.once:
                return
            time.sleep(15)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--once', action='store_true')
    parser.add_argument('--state', default='/workspace/.fx-bot/paper.json')
    parser.add_argument('--equity', type=float, default=1000)
    run(parser.parse_args())
