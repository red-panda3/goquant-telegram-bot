Assumptions about GoMarket  
--------------------------  
- The real GoMarket endpoints are not publicly reachable; therefore the  
  system runs against a mock layer that produces synthetically generated,  
  self-consistent L1 order-book data.  
- Payload format assumed:  
  REST /api/symbols/{exchange}/{kind} → [{"symbol":"BTC-USDT","base":"BTC","quote":"USDT"}, …]  
  WS subscribe frame → {"op":"subscribe","topic":"l1","symbols":["BTC-USDT"]}  
  WS data frame → {"symbol":"BTC-USDT","exchange":"binance","bid":60000,"ask":60001,"ts":1699123456789}

  1. What was built
A production-ready trading-information Telegram bot that:
Arbitrage Signal Service
/monitor_arb <symbol> <threshold>%
Watches real-time L1 order-book data (OKX, Binance, Bybit, Deribit) and alerts when a two-leg spread ≥ threshold appears.
Consolidated Market View & Venue Signalling
/view_market <symbol>
Continuously shows the cross-exchange best bid/offer (CBBO) and which venue currently offers it.
Symbol Discovery
/list_symbols <exchange> spot

┌-------------┐     WebSocket / REST      ┌----------------┐
│ GoMarket    │ ------>  L1 snapshots ---> │  Data layer    │ (client + models)
│  feed       │                            └------┬---------┘
└-------------┘                                   │
                                                  ▼
┌-------------┐     Async generators       ┌-------------┐
│ Telegram    │ <------  CBBO / Arb ------ │  Engine     │ (CbboCalculator, SpreadCalculator)
│   Bot       │                             └------┬------┘
└-------------┘                                   │
                                   Command handlers

| Command         | Arguments               | Description                                                 |
| --------------- | ----------------------- | ----------------------------------------------------------- |
| `/start`        | —                       | Health check                                                |
| `/list_symbols` | `<exchange> spot`       | Returns 20 symbols available on that exchange               |
| `/view_market`  | `<symbol>`              | Live CBBO message that updates every 2 s until `/stop_view` |
| `/monitor_arb`  | `<symbol> <threshold>%` | Live arbitrage alerts; threshold e.g. `0.3%`                |
| `/stop_view`    | —                       | Stops the CBBO stream for current chat                      |
| `/stop_arb`     | —                       | Stops the arbitrage monitor for current chat                |

 //env
 TELEGRAM_BOT_TOKEN=7000...<your-token>
GOMARKET_API_KEY=GQM...<real-or-dummy>
MOCK=true
LOG_LEVEL=INFO
