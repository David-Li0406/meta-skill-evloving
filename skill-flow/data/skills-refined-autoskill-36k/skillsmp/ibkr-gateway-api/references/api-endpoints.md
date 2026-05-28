# API Endpoints (Market Data, Account, Orders)

Use this as a quick index. For full request/response examples and error codes, read `api/API.md`.

## Health

- `GET /health`

## Market Data

- `POST /market-data/quote`
- `POST /market-data/historical`

## Account

- `GET /account/summary` (optional `account_id` query)
- `GET /account/positions` (optional `account_id` query)
- `GET /account/pnl` (optional `account_id` query)

## Orders

- `POST /orders/preview`
- `POST /orders`
- `GET /orders/{order_id}/status`
- `POST /orders/{order_id}/cancel`
- `GET /orders/open`

## Authentication

If `API_KEY` is set, include `X-API-Key: <key>` on every request.

## Order Request Shape (OrderSpec)

Required fields:
- `instrument`: `SymbolSpec` with `symbol` and `securityType` (optional `exchange`, `currency`, `expiry`, `strike`, `right`, `multiplier`)
- `side`: `BUY` or `SELL`
- `quantity`: number > 0
- `orderType`: `MKT`, `LMT`, `STP`, `STP_LMT`, `TRAIL`, `TRAIL_LIMIT`, `BRACKET`, `MOC`, `OPG`

Common optional fields:
- `limitPrice`, `stopPrice`
- `trailingAmount` or `trailingPercent` (for `TRAIL`)
- `takeProfitPrice`, `stopLossPrice`, `stopLossLimitPrice` (for `BRACKET`)
- `tif`, `outsideRth`, `clientOrderId`, `transmit`

Read `docs/SCHEMAS.md` for full validation rules.

## Market Data Request Shape

Quote request fields:
- `symbol`, `securityType` (required)
- `exchange`, `currency` (optional)

Historical request fields:
- `symbol`, `securityType` (required)
- `exchange`, `currency` (optional)
- `barSize` (e.g., `1m`, `5m`, `1d`)
- `duration` (e.g., `1d`, `1w`, `1mo`, `1y`)
- `whatToShow` (e.g., `TRADES`, `MIDPOINT`, `BID`, `ASK`)
- `rthOnly` (boolean)

## Example (Preview Order)

```bash
curl -X POST http://localhost:8000/orders/preview \
  -H "Content-Type: application/json" \
  -d '{
    "instrument": {"symbol": "AAPL", "securityType": "STK"},
    "side": "BUY",
    "quantity": 10,
    "orderType": "LMT",
    "limitPrice": 150.00
  }'
```
