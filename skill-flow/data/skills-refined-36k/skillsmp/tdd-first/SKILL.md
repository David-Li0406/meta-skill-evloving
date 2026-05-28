---
name: tdd-first
description: Test-Driven Development approach. Use this skill when writing any new functionality - tests and contracts come BEFORE implementation.
allowed-tools: Read Write Edit Bash Grep
---

# TDD-First Development

Every feature starts with a failing test. No exceptions.

## The Cycle

```
RED → GREEN → REFACTOR
 ↑_______________↓
```

1. **RED**: Write a test that fails (because code doesn't exist yet)
2. **GREEN**: Write minimal code to make test pass
3. **REFACTOR**: Clean up while keeping tests green

## Contract-First Thinking

Before writing ANY code, define the contract:

```python
# FIRST: Define what you expect
async def test_parse_time_extracts_hour_and_minute():
    result = await parse_time("let's meet at 3:30pm")

    assert result is not None
    assert result.hour == 15
    assert result.minute == 30

# THEN: Implement to satisfy the contract
async def parse_time(text: str) -> ParsedTime | None:
    ...
```

## Fixtures Over Mocks

Use real data structures, not magic mocks:

```python
# BAD: Magic mock hides contract violations
mock_event = MagicMock()
mock_event.text = "3pm"

# GOOD: Real fixture enforces contract
TELEGRAM_MESSAGE_FIXTURE = {
    "message_id": 42,
    "chat": {"id": -100123, "type": "group"},
    "from": {"id": 789, "first_name": "Test"},
    "text": "let's meet at 3pm PST",
    "date": 1705849200
}

async def test_normalize_telegram_message():
    event = await normalize_inbound(TELEGRAM_MESSAGE_FIXTURE)

    assert event.platform == Platform.TELEGRAM
    assert event.text == "let's meet at 3pm PST"
```

## Test Categories

### 1. Contract Tests
Verify input/output boundaries:
```python
async def test_inbound_returns_normalized_event():
    """Contract: inbound adapter produces NormalizedEvent"""

async def test_outbound_accepts_outbound_message():
    """Contract: outbound adapter consumes OutboundMessage"""
```

### 2. Behavior Tests
Verify business logic:
```python
async def test_unknown_timezone_triggers_verification():
    """When user timezone unknown, bot asks to verify"""

async def test_duplicate_message_is_skipped():
    """Same message_id within TTL is not processed twice"""
```

### 3. Edge Case Tests
Verify boundaries:
```python
async def test_empty_message_returns_none():
async def test_malformed_payload_does_not_crash():
async def test_timezone_near_midnight_handles_date_change():
```

## Offline Tests Only

Tests MUST NOT make network calls:

```python
# BAD: Hits real API
async def test_send_message():
    await send_telegram_message(chat_id, text)  # NO!

# GOOD: Mock HTTP layer
async def test_send_message(httpx_mock):
    httpx_mock.add_response(json={"ok": True})
    result = await send_telegram_message(chat_id, text)
    assert result is True
```

## Test File Structure

```
tests/
├── test_<module>_contract.py    # Contract tests
├── test_<module>_behavior.py    # Behavior tests
├── fixtures/
│   ├── telegram_payloads.py     # Real payload samples
│   └── discord_payloads.py
└── conftest.py                  # Shared fixtures
```

## Before You Write Code

Ask yourself:
1. What test would prove this works?
2. What's the contract (input → output)?
3. What edge cases exist?
4. How do I test this offline?

Write those tests FIRST. Then implement.

## Commands

- `/test` - run all tests
- `/test -k handler` - run by keyword
- `/check` - run all quality gates (lint + types + tests)

For coverage: `pytest --cov=src --cov-report=term-missing`
