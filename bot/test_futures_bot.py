import datetime as dt
import unittest
from futures_bot import closed, initial, signal, size, step

NOW = dt.datetime(2026, 10, 22, tzinfo=dt.timezone.utc)


def candles(up=True):
    rows=[]
    for i in range(100):
        p=100+i if up else 300-i
        rows.append([i, str(p), str(p+.4), str(p-.4), str(p), 0, i+1])
    return rows


class BotTests(unittest.TestCase):
    def test_closed_only(self):
        self.assertEqual(len(closed(candles(), 50)),49)

    def test_both_directions_and_disagreement(self):
        for up, expected in [(True,'LONG'),(False,'SHORT')]:
            frames={tf:candles(up) for tf in ('4h','1h','15m')}
            self.assertEqual(signal(frames)[0],expected)
            frames['1h']=candles(not up)
            self.assertIsNone(signal(frames)[0])

    def test_risk_budget_and_exposure(self):
        state=initial(1000); prices={'BTCUSDT':100,'ETHUSDT':100}
        qty=size(state, prices, 'BTCUSDT', 2)
        self.assertLessEqual(qty*(2+100*.0012), 5.000001)
        self.assertLessEqual(qty*100,2000)

    def test_close_costs_and_duplicate_candle(self):
        state=initial(1000); prices={'BTCUSDT':100,'ETHUSDT':100}
        candidate={'BTCUSDT':('LONG',2,1)}
        self.assertEqual(step(state,prices,candidate,NOW)[0]['action'],'LONG')
        self.assertEqual(step(state,prices,candidate,NOW),[])
        prices['BTCUSDT']=97
        events=step(state,prices,candidate,NOW)
        self.assertEqual(events[0]['action'],'CLOSE')
        self.assertLess(state['balance'],1000)
        self.assertFalse(state['positions'])

    def test_daily_halt_and_two_positions(self):
        state=initial(1000); prices={'BTCUSDT':100,'ETHUSDT':100}
        step(state,prices,{},NOW)
        state['balance']=979
        self.assertEqual(step(state,prices,{'BTCUSDT':('LONG',2,1)},NOW),[])
        self.assertFalse(state['positions'])
        tomorrow=NOW+dt.timedelta(days=1)
        step(state,prices,{s:('LONG',2,2) for s in prices},tomorrow)
        self.assertEqual(len(state['positions']),2)

    def test_short_stop_and_invalid_market(self):
        state=initial(1000); prices={'BTCUSDT':100,'ETHUSDT':100}
        step(state,prices,{'BTCUSDT':('SHORT',2,1)},NOW)
        prices['BTCUSDT']=103
        self.assertEqual(step(state,prices,{},NOW)[0]['action'],'CLOSE')
        with self.assertRaises(ValueError):step(state,{'BTCUSDT':float('nan'),'ETHUSDT':100},{},NOW)


if __name__=='__main__':unittest.main()
