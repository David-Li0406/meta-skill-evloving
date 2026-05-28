---
name: thin-adapters
description: Thin adapters pattern - connectors contain zero business logic. Use when adding platform integrations or refactoring boundaries.
allowed-tools: Read Write Edit Grep
---

# Thin Adapters Architecture

Adapters translate. Core decides.

## The Rule

```
┌─────────────────────────────────────────────────────┐
│                    ADAPTER                          │
│  • Parse platform format                            │
│  • Translate to/from canonical models               │
│  • Handle platform-specific quirks                  │
│  • NO business logic                                │
│  • NO decisions about what to do                    │
└─────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────┐
│                     CORE                            │
│  • All business rules                               │
│  • All decisions                                    │
│  • Platform-agnostic                                │
│  • Testable without adapters                        │
└─────────────────────────────────────────────────────┘
```

## Inbound Adapter

ONLY translates external → canonical:

```python
# src/connectors/telegram/inbound.py

async def normalize_inbound(payload: dict) -> NormalizedEvent | None:
    """
    Translate Telegram payload to NormalizedEvent.

    Returns None if payload is not a user message.
    Does NOT decide whether to respond.
    Does NOT check for time mentions.
    Does NOT look up user timezone.
    """
    message = payload.get("message")
    if not message or "text" not in message:
        return None  # Not a text message

    return NormalizedEvent(
        platform=Platform.TELEGRAM,
        platform_event_id=f"{message['chat']['id']}_{message['message_id']}",
        chat_id=str(message["chat"]["id"]),
        user_id=str(message["from"]["id"]),
        text=message["text"],
        timestamp=datetime.fromtimestamp(message["date"]),
        raw_payload=payload
    )
```

## Outbound Adapter

ONLY translates canonical → external:

```python
# src/connectors/telegram/outbound.py

async def send_outbound(msg: OutboundMessage) -> bool:
    """
    Send OutboundMessage via Telegram API.

    Does NOT decide what to send.
    Does NOT format the message.
    Does NOT handle retries (that's infrastructure).
    """
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
            json={
                "chat_id": msg.chat_id,
                "text": msg.text,
                "parse_mode": "HTML"
            }
        )
        return response.status_code == 200
```

## What Goes in Core

Everything else:

```python
# src/core/handler.py

async def handle_message(event: NormalizedEvent) -> OutboundMessage | None:
    """
    Core business logic. Platform-agnostic.

    THIS is where decisions happen:
    - Should we respond?
    - Is this a duplicate?
    - Does it contain time?
    - What timezone to use?
    - How to format response?
    """
    # Dedupe check
    if await is_duplicate(event):
        return None

    # Time detection
    parsed_time = await parse_time(event.text)
    if not parsed_time:
        return None

    # Timezone resolution
    user_tz = await get_user_timezone(event.user_id, event.platform)
    if user_tz.confidence < THRESHOLD:
        return prompt_verification(event)

    # Conversion
    conversions = convert_to_team_zones(parsed_time, user_tz)

    # Format response
    return OutboundMessage(
        platform=event.platform,
        chat_id=event.chat_id,
        text=format_conversions(conversions)
    )
```

## Testing Benefits

Core tests don't need adapters:

```python
async def test_handler_skips_duplicate():
    event = NormalizedEvent(...)  # No Telegram needed
    # Mock only dedupe, not platform
    with patch("is_duplicate", return_value=True):
        result = await handle_message(event)
    assert result is None
```

Adapter tests don't need core:

```python
async def test_telegram_normalize():
    payload = TELEGRAM_FIXTURE
    event = await normalize_inbound(payload)
    assert event.platform == Platform.TELEGRAM
    # No business logic tested here
```

## Anti-Patterns

### DON'T: Business logic in adapter

```python
# BAD: Adapter making decisions
async def normalize_inbound(payload: dict) -> NormalizedEvent | None:
    message = payload.get("message")
    if not message:
        return None

    # NO! This is business logic
    if "time" not in message["text"].lower():
        return None  # Don't process non-time messages

    # NO! This is business logic
    if await is_user_banned(message["from"]["id"]):
        return None
```

### DON'T: Platform-specific code in core

```python
# BAD: Core knows about Telegram
async def handle_message(event: NormalizedEvent):
    if event.platform == Platform.TELEGRAM:
        # NO! Platform-specific handling
        await telegram_specific_thing()
```

### DON'T: Formatting in adapter

```python
# BAD: Adapter formatting response
async def send_outbound(msg: OutboundMessage) -> bool:
    # NO! Core should format
    text = f"🕐 {msg.time} in your timezone"
```

## Directory Structure

```
src/
├── core/                    # Platform-agnostic
│   ├── handler.py          # Business logic
│   ├── models.py           # Canonical models
│   └── ...
└── connectors/             # Platform-specific
    ├── telegram/
    │   ├── inbound.py      # Telegram → NormalizedEvent
    │   └── outbound.py     # OutboundMessage → Telegram
    ├── discord/
    │   ├── inbound.py
    │   └── outbound.py
    └── whatsapp/
        ├── inbound.py
        └── outbound.py
```

## The Test

If you can swap adapters without touching core, you did it right.

Discord, WhatsApp, Slack, email - core doesn't care.
