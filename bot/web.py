"""Local paper dashboard; no exchange orders or credentials."""
import argparse
import datetime as dt
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import math
from pathlib import Path
import threading
import time
from urllib.error import HTTPError

from futures_bot import initial, step, signal, equity, get

LOCK = threading.Lock()
STATE = initial(1000)
RUNNING = False
TICK = 0
EVENTS = []
PRICES = {'BTCUSDT': 60000., 'ETHUSDT': 3000.}
HISTORY = []
CONNECTION = 'Chưa kiểm tra Binance Testnet'


def advance():
    global TICK, PRICES
    TICK += 1
    frames = {}
    for symbol, base in [('BTCUSDT',60000),('ETHUSDT',3000)]:
        frames[symbol] = {}
        for tf in ('4h','1h','15m'):
            rows=[]
            for i in range(TICK,TICK+100):
                price=base*(1+.0008*i+.006*math.sin(i/12))
                rows.append([i,price,price+base*.00015,price-base*.00015,price,0,i])
            frames[symbol][tf]=rows
        PRICES[symbol]=frames[symbol]['15m'][-1][4]
    events=step(STATE,PRICES,{s:signal(f) for s,f in frames.items()},dt.datetime.now(dt.timezone.utc))
    EVENTS.extend(events)
    del EVENTS[:-100]
    HISTORY.append({'tick':TICK,'equity':equity(STATE,PRICES)})
    del HISTORY[:-120]


def worker():
    while True:
        with LOCK:
            if RUNNING: advance()
        time.sleep(2)


class Handler(BaseHTTPRequestHandler):
    def reply(self, data, status=200):
        body=json.dumps(data,allow_nan=False).encode()
        self.send_response(status)
        self.send_header('Content-Type','application/json; charset=utf-8')
        self.send_header('Cache-Control','no-store')
        self.send_header('Content-Length',str(len(body)))
        self.end_headers();self.wfile.write(body)

    def do_GET(self):
        if self.path=='/':
            body=Path(__file__).with_name('index.html').read_bytes()
            self.send_response(200);self.send_header('Content-Type','text/html; charset=utf-8')
            self.send_header('Content-Length',str(len(body)));self.end_headers();self.wfile.write(body)
        elif self.path=='/api/status':
            with LOCK:
                self.reply(dict(mode='DEMO',running=RUNNING,equity=equity(STATE,PRICES),balance=STATE['balance'],
                                prices=PRICES,positions=STATE['positions'],events=EVENTS,history=HISTORY,connection=CONNECTION))
        else:self.reply({'error':'Not found'},404)

    def do_POST(self):
        global RUNNING, STATE, TICK, CONNECTION
        # Reject cross-origin mutations; no CORS access is granted.
        origin=self.headers.get('Origin')
        if origin and origin != 'http://'+self.headers.get('Host',''):
            return self.reply({'error':'Origin rejected'},403)
        if self.path=='/api/connection':
            try:
                get('/fapi/v1/time')
                message='Kết nối Testnet thành công; bot vẫn chỉ chạy DEMO.'
            except HTTPError as exc:
                message=f'Binance HTTP {exc.code}: '+('khu vực máy chủ bị hạn chế.' if exc.code==451 else 'không thể lấy dữ liệu.')
            except Exception:
                message='Không kết nối được Testnet; kiểm tra mạng máy chủ.'
            with LOCK:CONNECTION=message
            return self.reply({'connection':message})
        with LOCK:
            if self.path=='/api/start':RUNNING=True
            elif self.path=='/api/stop':RUNNING=False
            elif self.path=='/api/reset':
                if RUNNING:return self.reply({'error':'Dừng demo trước khi đặt lại.'},409)
                STATE=initial(1000);TICK=0;EVENTS.clear();HISTORY.clear()
                PRICES.update(BTCUSDT=60000.,ETHUSDT=3000.)
            else:return self.reply({'error':'Not found'},404)
        self.reply({'ok':True})


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--host',default='127.0.0.1')
    parser.add_argument('--port',type=int,default=8765)
    args=parser.parse_args()
    threading.Thread(target=worker,daemon=True).start()
    print(f'Dashboard listening on {args.host}:{args.port}; DEMO only',flush=True)
    ThreadingHTTPServer((args.host,args.port),Handler).serve_forever()
