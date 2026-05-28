# Notifications

## Telegram Setup

### Create Bot
1. Message @BotFather on Telegram
2. Run `/newbot` command
3. Get bot token

### Configure
```json
{
    "telegram": {
        "enabled": true,
        "token": "123456789:ABCdefGHIjklMNOpqrsTUVwxyz",
        "chat_id": "987654321"
    }
}
```

### Send Notifications
```python
await telegram.send_message("🚀 Trade executed: BUY BTC/USDT @ $50000")
```

## Discord Setup

### Create Bot
1. Go to Discord Developer Portal
2. Create Application → Bot
3. Copy token
4. Invite bot to server
5. Get channel ID

### Configure
```json
{
    "discord": {
        "enabled": true,
        "token": "YOUR_BOT_TOKEN",
        "channel_id": "123456789012345678"
    }
}
```

### Send Notifications
```python
await discord.send_message(
    embed={
        "title": "Trade Alert",
        "description": "BUY BTC/USDT",
        "color": 0x00ff00
    }
)
```

## Twitter Integration

### Setup OAuth
```python
twitter = TwitterService()
twitter.set_credentials(
    api_key="...",
    api_secret="...",
    access_token="...",
    access_secret="..."
)
```

### Tweet Updates
```python
await twitter.post_tweet("Bot made profitable trade! #crypto #trading")
```
