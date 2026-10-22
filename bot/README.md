# BTC/ETH multi-timeframe Futures bot — paper prototype

Python 3.10+; standard library only. Run from this directory:

```bash
python3 -m unittest -v
python3 futures_bot.py --once
python3 futures_bot.py
```

Uses public Binance USD-M Futures Testnet data at `demo-fapi.binance.com`. No API key is needed. This prototype **does not submit exchange orders**; all positions are simulated and persisted in `/workspace/.fx-bot/paper.json`. Stop with Ctrl-C. Use a separate `--state` file to start an independent paper account; `--equity 1000` only applies when that file does not exist.

Strategy: closed 4h and 1h candles must agree (price above EMA20 above EMA50 for Long; reverse for Short). The last closed 15m candle must break the previous twenty highs/lows. Stop distance is twice the mean true range of fourteen candles; target is twice the stop distance. Entry uses the current observed mark price, not a historical candle close. Each closed 15m candle is considered only once.

Risk: 0.5% current paper equity per entry including estimated costs, maximum two positions, total entry exposure capped at 2x equity. Pause new entries at a 2% UTC daily equity drawdown; continue monitoring existing positions. Existing exposure can exceed 2x after adverse price movement; this is an entry cap, not a liquidation engine. Fee assumption 0.04% per fill, adverse slippage 0.02% per fill. Real fees vary.

Limitations: stops/targets are evaluated at observed prices every polling cycle, not exchange-hosted orders. Intracycle touches can be missed, outages prevent exits, and gaps can exceed intended loss. Balance includes realized PnL and fees; reported equity includes unrealized PnL. No funding, liquidation, isolated-margin accounting, exchange quantity filters, or backtest engine yet. Paper results do not establish profitability. Adding actual Testnet order execution requires quantity rounding, isolated-margin/leverage configuration, exchange-native protective orders, reconciliation and idempotency first. Real-money execution is not implemented.

After publication, the cloud proxy permits the Testnet hostname. The endpoint now returns HTTP 451 with Binance’s explicit restricted-location eligibility message. Live market-data validation remains blocked by Binance location restrictions; an API key does not resolve this. Use an eligible deployment location and account in accordance with Binance terms, or continue development with offline historical data. No live orders have been sent. Six unit tests pass; live integration is not validated.

## Local web dashboard (Windows / macOS / Linux)

Requires Python 3.10 or later; no pip dependencies. From the extracted `bot` directory:

```bash
python web.py
```

On macOS/Linux use `python3 web.py` if necessary. Open your browser at host `127.0.0.1`, port `8765`. The server binds only to your own machine by default. Do not expose this development server to the public Internet.

Click **Chạy demo** to simulate BTC/ETH trades, **Dừng demo** to pause, and **Đặt lại vốn** to reset while stopped. Prices/candles are synthetic and accelerated, not live Binance data. The dashboard uses the same signal/risk engine but an independent in-memory paper account; it does not read or modify the CLI account. Restarting the server loses demo state. **Kiểm tra kết nối** calls the actual public Testnet time endpoint from whichever machine runs the server; success does not enable trading or validate account eligibility. No API keys or exchange orders are used.

The CLI `futures_bot.py` currently uses POSIX file locking and is intended for Linux/macOS. The web demo does not use that lock and can run on Windows.
