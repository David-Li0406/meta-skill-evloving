# Webhooks

## TradingView Integration

### Webhook URL
```
POST http://localhost:5001/webhook/tradingview
Authorization: Bearer YOUR_SECRET_TOKEN
```

### Payload Format
```json
{
    "action": "buy",
    "ticker": "BINANCE:BTCUSDT",
    "price": 50000,
    "time": "2024-01-15T10:30:00Z",
    "strategy": "RSI_Strategy"
}
```

### Handler Implementation
```python
@webhook.register_handler("/tradingview")
async def handle_tradingview(payload):
    action = payload["action"]
    symbol = payload["ticker"].split(":")[1]
    
    if action == "buy":
        await trading_api.create_market_order(
            symbol=symbol,
            side="buy",
            amount=0.001
        )
    elif action == "sell":
        await trading_api.create_market_order(
            symbol=symbol,
            side="sell",
            amount=0.001
        )
```

## Custom Webhooks

### Define Custom Endpoint
```python
@webhook.register_handler("/custom/signal")
async def custom_signal(payload):
    if payload["confidence"] > 0.8:
        await execute_trade(payload)
```

### Authentication
```python
def verify_webhook(request):
    token = request.headers.get("Authorization")
    if not token or token != f"Bearer {SECRET_TOKEN}":
        raise Unauthorized()
```

## Testing Webhooks

```bash
# Test with curl
curl -X POST http://localhost:5001/webhook/tradingview \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"action": "buy", "ticker": "BINANCE:BTCUSDT"}'
```
