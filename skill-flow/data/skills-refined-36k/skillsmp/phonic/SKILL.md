---
name: phonic
description: "AI telephone agent for outbound calls including sales, appointments, surveys, reminders, and data collection. Initiates calls with inline agent configuration (system_prompt, voice), monitors completion via polling, and retrieves transcripts. Use with Claude skill for structured data extraction from transcripts. Environment variable PHONIC_API_KEY must be set."
license: "© 2025 Daisyloop Technologies Inc. See LICENSE.txt"
---

# Phonic AI Telephone Agent

## Overview

Phonic provides AI-powered voice agents for telephone calls with sub-500ms latency. This skill enables outbound calls with automatic transcript retrieval using a polling-based approach (webhooks not available in sandbox environments).

**Call flow**: Initiate call -> Poll for completion -> Retrieve transcript

## Quick Start

```python
from phonic import Phonic

client = Phonic()  # Uses PHONIC_API_KEY from environment

# Start an outbound call
result = client.conversations.outbound_call(
    to_phone_number="+1234567890",
    config={
        "system_prompt": "You are a friendly dental office assistant calling to confirm an appointment for tomorrow at 2pm. Be polite and concise.",
        "voice_id": "virginia",
    }
)

conversation_id = result.conversation_id
```

Or use the provided script for complete call handling with polling:

```bash
uv run skills/phonic/scripts/make_call.py "+1234567890" \
    --system-prompt "You are a friendly survey assistant collecting feedback." \
    --voice virginia
```

## Dispatching Calls

**Always dispatch an `external_ref` immediately after initiating an outbound call.** This enables the timeline to track the conversation and potentially display transcripts/audio later.

```python
from phonic import Phonic
from fulcrum_sdk._internal.dispatch import get_dispatch_client

client = Phonic()
result = client.conversations.outbound_call(
    to_phone_number="+1234567890",
    config={
        "system_prompt": "You are a friendly dental office assistant calling to confirm an appointment.",
        "voice_id": "virginia",
    }
)

# Dispatch immediately after call initiation
dispatch = get_dispatch_client()
dispatch.dispatch_external_ref(
    summary="Outbound call started",
    provider="phonic",
    ref_type="conversation",
    ref_id=result.conversation_id,
)

# Then poll for completion...
conversation_id = result.conversation_id
```

**Key points:**
- Dispatch **immediately** after `outbound_call` returns (before polling)
- Use `result.conversation_id` which is available right after call initiation
- Provider is `"phonic"`, ref_type is `"conversation"`
- This enables future display of transcripts and audio replay in the timeline

## Call Configuration

Configure calls inline with `system_prompt` and `voice_id`. All config options override any pre-configured agent settings.

### Required Options

| Option | Description |
|--------|-------------|
| `system_prompt` | Instructions for the AI agent's behavior and goals |
| `voice_id` | Voice selection (default: "virginia") |

**Note:** The following are always enabled by default:
- `keypad_input` is always included in tools
- `en` (English) is always included in languages

### Optional Options

| Option | Description |
|--------|-------------|
| `welcome_message` | Custom opening line. Only specify if you need a specific greeting; otherwise the agent generates one from system_prompt |
| `template_variables` | Dict of variables for `{{variable}}` placeholders in prompts |
| `languages` | Additional ISO 639-1 codes for speech recognition ("en" always included, e.g., ["es"] adds Spanish) |
| `boosted_keywords` | Words/phrases for improved recognition accuracy |
| `tools` | Additional tool names to enable ("keypad_input" always included) |
| `no_input_poke_sec` | Seconds of silence before reminder message (default: 180) |
| `no_input_poke_text` | Reminder message (default: "Are you still there?") |
| `no_input_end_conversation_sec` | Seconds of silence before ending call |

### Example with Options

```python
result = client.conversations.outbound_call(
    to_phone_number="+1234567890",
    config={
        "system_prompt": "You are conducting a customer satisfaction survey for {{company}}. Ask about their recent experience.",
        "voice_id": "virginia",
        "template_variables": {"company": "Acme Corp"},
        "languages": ["es"],  # "en" is always included automatically
        "boosted_keywords": ["satisfaction", "rating", "feedback"],
        "no_input_poke_sec": 30,
    }
)
```

## Call Flow and Polling

After initiating a call, poll for completion by checking `ended_at`:

```python
import time

conversation_id = result.conversation_id

while True:
    response = client.conversations.get(conversation_id)
    conversation = response.conversation
    if conversation.ended_at is not None:
        break
    time.sleep(5)  # Poll every 5 seconds

# Call completed
print(f"Ended by: {conversation.ended_by}")
print(f"Duration: {conversation.duration_ms / 1000:.1f}s")
```

The `make_call.py` script handles this automatically with progress output.

## Transcript Handling

Two transcript types are available:

| Type | Field | Description |
|------|-------|-------------|
| Live | `live_transcript` | Real-time transcription during call |
| Post-call | `post_call_transcript` | Refined transcript after processing (preferred) |

Access transcripts after call completion:

```python
# Prefer post-call transcript for accuracy
transcript = conversation.post_call_transcript or conversation.live_transcript

# Or access individual turns
for item in conversation.items:
    speaker = "Agent" if item.role == "assistant" else "User"
    text = item.post_call_transcript or item.live_transcript
    print(f"{speaker}: {text}")
```

## Retrieving Past Calls

Retrieve transcript and audio for any conversation by ID:

```python
from phonic import Phonic

client = Phonic()
response = client.conversations.get("conv_abc123")
conversation = response.conversation

# Transcript (prefer post-call for accuracy)
transcript = conversation.post_call_transcript or conversation.live_transcript

# Audio URL (presigned, may be .gz or .zip compressed)
audio_url = conversation.audio_url
```

### Downloading Audio

The `audio_url` may return compressed files (.gz or .zip). Use the `download_audio` helper from `make_call.py` or handle extraction manually:

```python
import gzip
import urllib.request

urllib.request.urlretrieve(audio_url, "recording.gz")
with gzip.open("recording.gz", "rb") as f_in:
    with open("recording.wav", "wb") as f_out:
        f_out.write(f_in.read())
```

**Note:** Audio URLs are presigned and expire. Download promptly or re-fetch the conversation.

## Data Extraction with Claude

For structured data extraction from transcripts, use the Claude skill:

```python
from anthropic import Anthropic

claude = Anthropic()

# Extract appointment details
message = claude.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    temperature=0,
    system="""Extract appointment details from this call transcript.
Return JSON: {"confirmed": bool, "date": string|null, "time": string|null, "notes": string}""",
    messages=[{"role": "user", "content": transcript}]
)

import json
appointment = json.loads(message.content[0].text)
```

## Error Handling

### Call Termination

Check `ended_by` to understand how the call ended:

| Value | Meaning |
|-------|---------|
| `"user"` | Caller hung up |
| `"user_canceled"` | Caller canceled |
| `"assistant"` | Agent ended the call |
| `"error"` | Error occurred |

### Common Errors

```python
from phonic import Phonic, APIError

try:
    result = client.conversations.outbound_call(...)
except APIError as e:
    if e.status_code == 400:
        print("Invalid phone number format")
    elif e.status_code == 402:
        print("Insufficient credits")
    else:
        print(f"API error: {e}")
```

### Timeout Handling

```bash
# Increase timeout for long calls
uv run skills/phonic/scripts/make_call.py "+1234567890" \
    --system-prompt "..." \
    --max-wait 900  # 15 minutes
```

## Scripts

### make_call.py

Complete outbound call workflow with polling, transcript output, and optional audio download.

```bash
uv run skills/phonic/scripts/make_call.py "+1234567890" \
    --system-prompt "You are a friendly assistant..." \
    --voice virginia \
    --max-wait 600 \
    --poll-interval 5 \
    --output-dir ./recordings \
    --json  # Output as JSON
```

| Option | Default | Description |
|--------|---------|-------------|
| `--system-prompt` | Required | Agent instructions |
| `--voice` | virginia | Voice ID |
| `--welcome-message` | None | Custom opening (optional) |
| `--languages` | None | Additional language codes ("en" always included) |
| `--tools` | None | Additional tools ("keypad_input" always included) |
| `--max-wait` | 600 | Max seconds to wait |
| `--poll-interval` | 5 | Seconds between polls |
| `--output-dir` | None | Directory to save audio recording (auto-extracts zip files) |
| `--json` | False | Output JSON instead of text |

## Use Cases

### Appointment Confirmation

```bash
uv run skills/phonic/scripts/make_call.py "+1234567890" \
    --system-prompt "You are calling to confirm a dental appointment for tomorrow at 2pm. Ask if they can make it, and if not, offer to reschedule. Be friendly and professional."
```

### Survey Collection

```bash
uv run skills/phonic/scripts/make_call.py "+1234567890" \
    --system-prompt "You are conducting a brief customer satisfaction survey. Ask: 1) How satisfied were they with their recent purchase (1-5)? 2) Would they recommend us? 3) Any feedback to share? Thank them when done."
```

### Payment Reminder

```bash
uv run skills/phonic/scripts/make_call.py "+1234567890" \
    --system-prompt "You are calling about an outstanding balance of $150. Politely remind them of the payment due, ask if they need payment options, and offer to transfer to billing if needed."
```

## References

For detailed API type definitions, see [references/api_types.md](references/api_types.md).
