---
name: clean-models
description: Clean data modeling with Pydantic, strict typing, and database hygiene. Use when designing data structures or working with storage.
allowed-tools: Read Write Edit Grep
---

# Clean Models & Data Hygiene

Data flows through the system. Keep it clean at every point.

## Pydantic as the Contract

Every data boundary has a Pydantic model:

```python
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum

class Platform(str, Enum):
    TELEGRAM = "telegram"
    DISCORD = "discord"
    WHATSAPP = "whatsapp"

class NormalizedEvent(BaseModel):
    """Canonical representation of any platform message."""
    platform: Platform
    platform_event_id: str
    chat_id: str
    user_id: str
    text: str
    timestamp: datetime
    raw_payload: dict = Field(exclude=True)  # Don't serialize back

    model_config = {"frozen": True}  # Immutable
```

## Why Frozen Models?

Immutability prevents bugs:

```python
# BAD: Mutable state causes surprises
event.text = "modified"  # Who changed this? When?

# GOOD: Frozen model - create new if needed
new_event = event.model_copy(update={"text": "modified"})
```

## Validation at Boundaries

Validate ONCE at the edge, then trust internal data:

```python
# EDGE: External input - validate strictly
async def normalize_inbound(payload: dict) -> NormalizedEvent:
    # Pydantic validates here
    return NormalizedEvent(
        platform=Platform.TELEGRAM,
        platform_event_id=str(payload["message"]["message_id"]),
        chat_id=str(payload["message"]["chat"]["id"]),
        user_id=str(payload["message"]["from"]["id"]),
        text=payload["message"].get("text", ""),
        timestamp=datetime.fromtimestamp(payload["message"]["date"]),
        raw_payload=payload
    )

# INTERNAL: Trust the model
async def handle_message(event: NormalizedEvent) -> OutboundMessage | None:
    # No need to re-validate - NormalizedEvent guarantees structure
    ...
```

## Database Hygiene

### Don't Bloat Collections

```python
# BAD: Store everything "just in case"
{
    "user_id": "123",
    "full_payload": {...},  # 10KB of junk
    "all_messages": [...],  # Growing forever
    "debug_info": {...}     # Temporary data made permanent
}

# GOOD: Store only what you need
{
    "user_id": "123",
    "platform": "telegram",
    "tz_iana": "America/New_York",
    "confidence": 1.0,
    "verified_at": ISODate()
}
```

### Use TTL for Temporary Data

```python
# Dedupe events expire automatically
await db.dedupe_events.create_index(
    "created_at",
    expireAfterSeconds=7 * 24 * 60 * 60  # 7 days
)
```

### Indexes Are Part of the Schema

```python
async def ensure_indexes(db):
    """Run on startup - indexes are contracts."""
    # Users: one timezone per user per platform
    await db.users.create_index(
        [("platform", 1), ("user_id", 1)],
        unique=True
    )

    # Dedupe: fast lookup, auto-cleanup
    await db.dedupe_events.create_index(
        [("platform", 1), ("event_id", 1)],
        unique=True
    )
    await db.dedupe_events.create_index(
        "created_at",
        expireAfterSeconds=604800
    )
```

## Type Everything

Pyright strict mode catches bugs at compile time:

```python
# BAD: Any type hides bugs
def process(data):  # What is data?
    return data["key"]  # KeyError at runtime

# GOOD: Types make intent clear
def process(data: NormalizedEvent) -> ParsedTime | None:
    ...  # Pyright validates usage
```

## Config as Models

Even configuration should be typed:

```python
class TimezoneConfig(BaseModel):
    team_timezones: list[str] = ["UTC"]
    default_tz: str = "UTC"

class ConfidenceConfig(BaseModel):
    threshold: float = Field(ge=0.0, le=1.0, default=0.7)
    verified: float = Field(ge=0.0, le=1.0, default=1.0)

class Settings(BaseModel):
    timezone: TimezoneConfig
    confidence: ConfidenceConfig
    # Pydantic validates on load
```

## Model Evolution

When schema changes:

1. **Add optional fields** with defaults (backwards compatible)
2. **Never remove fields** from stored data without migration
3. **Version your models** if breaking changes needed

```python
class UserTzState(BaseModel):
    user_id: str
    tz_iana: str | None
    confidence: float
    # New field - optional with default
    source: str = "unknown"  # Added in v2
```

## Checklist

Before adding any data structure:
- [ ] Is it a Pydantic model?
- [ ] Is it frozen/immutable?
- [ ] Are all fields typed?
- [ ] Does it validate at the boundary?
- [ ] Does stored data have TTL if temporary?
- [ ] Are indexes defined?
- [ ] Is it the minimal required data?
