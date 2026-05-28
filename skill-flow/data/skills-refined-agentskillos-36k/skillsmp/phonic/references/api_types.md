# Phonic API Types Reference

Comprehensive request and response data types for the Phonic Python SDK.

## Table of Contents

- [OutboundCallConfig](#outboundcallconfig-request)
- [Conversation](#conversation-response)
- [ConversationItem](#conversationitem)
- [ConversationEndedBy](#conversationendedby)
- [ConversationAnalysis](#conversationanalysis)
- [ConversationCallInfo](#conversationcallinfo)
- [Tool Types](#tool-types)

---

## OutboundCallConfig (Request)

Configuration for `client.conversations.outbound_call()`. All fields are optional and override any pre-configured agent settings.

| Field | Type | Description |
|-------|------|-------------|
| `agent` | `str` | Agent name to use for the call |
| `project` | `str` | Project name (default: "main") |
| `system_prompt` | `str` | Instructions for agent behavior; supports `{{variable}}` templates |
| `welcome_message` | `str` | Opening message; supports templates. Only specify if custom greeting needed |
| `template_variables` | `dict[str, str]` | Values for `{{placeholder}}` substitution in prompts |
| `voice_id` | `str` | Voice selection (default: "virginia") |
| `languages` | `list[str]` | ISO 639-1 codes for speech recognition ("en" always included) |
| `boosted_keywords` | `list[str]` | Words/phrases for improved recognition accuracy |
| `tools` | `list[str]` | Tool names to enable ("keypad_input" always included) |
| `no_input_poke_sec` | `int` | Seconds of silence before sending poke message; `None` disables |
| `no_input_poke_text` | `str` | Message sent after silence period (default: "Are you still there?") |
| `no_input_end_conversation_sec` | `int` | Seconds of silence before ending conversation |

### Example

```python
config = {
    "system_prompt": "You are calling to confirm an appointment for {{name}}.",
    "voice_id": "virginia",
    "template_variables": {"name": "John Smith"},
    "languages": ["es"],  # "en" is always included automatically
    "boosted_keywords": ["appointment", "reschedule"],
    "tools": ["transfer_to_agent"],  # "keypad_input" is always included automatically
    "no_input_poke_sec": 30,
}
```

---

## Conversation (Response)

Returned by `client.conversations.get(id)` and `client.conversations.outbound_call()`.

| Field | Type | Description |
|-------|------|-------------|
| `id` | `str` | Unique conversation identifier |
| `workspace` | `str` | Organization/workspace name |
| `external_id` | `str \| None` | External tracking reference |
| `agent` | `ConversationAgent \| None` | Associated agent information |
| `project` | `ConversationProject` | Project details |
| `model` | `str` | Speech-to-text model used |
| `started_at` | `datetime` | When the call started |
| `ended_at` | `datetime \| None` | When the call ended (`None` if still active) |
| `ended_by` | `ConversationEndedBy \| None` | How the call was terminated |
| `duration_ms` | `float` | Call length in milliseconds |
| `live_transcript` | `str` | Real-time transcript (full text) |
| `post_call_transcript` | `str \| None` | Refined transcript after processing (preferred) |
| `items` | `list[ConversationItem]` | Individual conversation turns |
| `analysis` | `ConversationAnalysis` | Latency and interruption metrics |
| `call_info` | `ConversationCallInfo \| None` | Phone number details |
| `audio_url` | `str \| None` | Presigned URL for audio recording |
| `task_results` | `dict` | Results from extractions/evaluations |
| `template_variables` | `dict[str, str]` | Template values used in the call |
| `welcome_message` | `str \| None` | Opening message used |
| `generate_welcome_message` | `bool` | Whether greeting was auto-generated |
| `languages` | `list[str] \| None` | Language codes used |
| `boosted_keywords` | `list[str] \| None` | Boosted keywords used |
| `input_format` | `str` | Audio input format |
| `output_format` | `str` | Audio output format |
| `background_noise_level` | `float` | Background noise level setting |
| `background_noise` | `str \| None` | Background noise type |
| `no_input_poke_sec` | `int \| None` | Silence poke threshold |
| `no_input_poke_text` | `str \| None` | Silence poke message |
| `no_input_end_conversation_sec` | `int \| None` | Silence end threshold |

### Checking Call Status

```python
conversation = client.conversations.get(conversation_id)

# Check if call is still active
if conversation.ended_at is None:
    print("Call still in progress")
else:
    print(f"Call ended: {conversation.ended_by}")
```

---

## ConversationItem

Individual turn in a conversation (from `conversation.items`).

| Field | Type | Description |
|-------|------|-------------|
| `item_idx` | `int` | Turn index in conversation (0-based) |
| `role` | `"user" \| "assistant"` | Who spoke in this turn |
| `live_transcript` | `str` | Real-time transcript of this turn |
| `post_call_transcript` | `str \| None` | Refined transcript of this turn |
| `duration_ms` | `float` | Duration of this turn in milliseconds |
| `started_at` | `datetime` | When this turn started |
| `voice_id` | `str \| None` | Voice used (assistant turns only) |
| `audio_speed` | `float \| None` | Audio speed (assistant turns only) |
| `system_prompt` | `str \| None` | System prompt for this turn |
| `tool_calls` | `list[ToolCall] \| None` | Tools invoked by assistant |

### Iterating Through Turns

```python
for item in conversation.items:
    speaker = "Agent" if item.role == "assistant" else "User"
    text = item.post_call_transcript or item.live_transcript
    print(f"{speaker}: {text}")
```

---

## ConversationEndedBy

Enum indicating how the call was terminated. Access via `conversation.ended_by`.

| Value | Description |
|-------|-------------|
| `"user"` | User (callee) hung up |
| `"user_canceled"` | User canceled the call |
| `"user_validation_failed"` | Validation failure on user side |
| `"assistant"` | AI agent ended the call |
| `"error"` | Error occurred during call |

### Handling Different Endings

```python
match conversation.ended_by:
    case "user":
        print("Caller hung up")
    case "assistant":
        print("Agent completed the call")
    case "error":
        print("Call failed due to error")
    case _:
        print(f"Call ended: {conversation.ended_by}")
```

---

## ConversationAnalysis

Call quality metrics. Access via `conversation.analysis`.

| Field | Type | Description |
|-------|------|-------------|
| `latencies_ms` | `list[float]` | Response latencies between turns (milliseconds) |
| `interruptions_count` | `int` | Number of times speakers interrupted each other |

### Checking Call Quality

```python
analysis = conversation.analysis
avg_latency = sum(analysis.latencies_ms) / len(analysis.latencies_ms) if analysis.latencies_ms else 0
print(f"Average latency: {avg_latency:.0f}ms")
print(f"Interruptions: {analysis.interruptions_count}")
```

---

## ConversationCallInfo

Phone call metadata. Access via `conversation.call_info`.

| Field | Type | Description |
|-------|------|-------------|
| `from_phone_number` | `str` | Caller phone number (E.164 format) |
| `to_phone_number` | `str` | Callee phone number (E.164 format) |
| `twilio_call_sid` | `str \| None` | Twilio Call SID (SIP trunking only) |

---

## Tool Types

Available tool types for custom tools created via `client.tools.create()`.

| Type | Description |
|------|-------------|
| `custom_context` | Returns contextual information without external calls |
| `custom_webhook` | Calls external HTTP endpoint (GET or POST) |
| `custom_websocket` | Real-time WebSocket connection for async responses |
| `built_in_transfer_to_phone_number` | Transfer call to specified phone number |
| `built_in_transfer_to_agent` | Transfer call to another Phonic agent |

### Tool Parameter Types

When defining tool parameters:

| Type | Description |
|------|-------------|
| `string` | Text value |
| `integer` | Whole number |
| `number` | Decimal number |
| `boolean` | True/false |
| `array` | List (requires `item_type`) |

---

## Additional Resources

- [Phonic Python SDK](https://github.com/Phonic-Co/phonic-python)
- [Phonic Documentation](https://docs.phonic.co)
