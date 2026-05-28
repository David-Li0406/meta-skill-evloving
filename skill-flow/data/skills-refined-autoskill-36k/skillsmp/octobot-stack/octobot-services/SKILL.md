---
name: OctoBot-Services
description: External service integrations for OctoBot (webhooks, notifications, cloud sync)
version: 1.0.0
license: GPL-3.0
---

# OctoBot-Services Development

## Overview

OctoBot-Services provides integration with external services including webhooks, notifications (Telegram, Discord, Twitter), cloud synchronization, and third-party APIs.

## References

- **[Service Tentacles](references/service-tentacles.md)**: Notification, webhook, and cloud service implementations
- **[Webhooks](references/webhooks.md)**: TradingView signals, custom webhooks, payload handling
- **[Notifications](references/notifications.md)**: Telegram, Discord, Twitter bot configuration

## Key Concepts

### Service Tentacles
Plugin-based services as tentacles, configurable via web interface.

### Service Instances
Each service runs as independent async task.

### Service Factory
Creates and manages service instances.

## Common Tasks

### Enable Telegram Notifications
```python
from octobot_services.services import TelegramService

telegram = TelegramService()
telegram.set_bot_token("YOUR_TOKEN")
telegram.set_chat_id("YOUR_CHAT_ID")
await telegram.start()
await telegram.send_message("Bot started")
```

### Handle TradingView Webhook
```python
from octobot_services.services import WebhookService

webhook = WebhookService()

@webhook.register_handler("/tradingview")
async def handle_tradingview(payload):
    action = payload["action"]  # buy/sell
    symbol = payload["ticker"]
    if action == "buy":
        await place_order(symbol, "buy")
```

### Configure Discord Bot
```python
from octobot_services.services import DiscordService

discord = DiscordService()
discord.set_token("BOT_TOKEN")
discord.set_channel_id("CHANNEL_ID")
await discord.start()
```

## Integration Points

- **OctoBot Core**: Services notify on trading events
- **OctoBot-Trading**: Services trigger orders via webhooks
- **Web Interface**: Configure services via dashboard
- **External APIs**: Twitter, Telegram, Discord, TradingView

## Quick Reference

### Service Configuration
```json
{
    "telegram": {
        "enabled": true,
        "token": "YOUR_TOKEN",
        "chat_id": "YOUR_CHAT_ID"
    },
    "webhook": {
        "enabled": true,
        "port": 5001,
        "auth_token": "SECRET"
    }
}
```

### Common Service Events
- `on_trade`: Trade executed
- `on_order`: Order placed
- `on_evaluation`: Evaluator signal
- `on_profitability`: Portfolio update

## Checklist

- [ ] Configure at least one notification service (Telegram/Discord)
- [ ] Test webhook endpoint with curl/Postman
- [ ] Secure webhook with authentication token
- [ ] Subscribe services to relevant channels (Async-Channel)
- [ ] Handle service errors gracefully
- [ ] Test notification delivery
- [ ] Document webhook payload format
