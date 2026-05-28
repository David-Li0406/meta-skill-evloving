---
name: voice-call
description: Use this skill to start and manage voice calls via supported plugins.
---

# Voice Call

Utilize the voice-call plugin to initiate or inspect calls through various providers (Twilio, Telnyx, Plivo, or mock).

## CLI

```bash
<plugin_name> voicecall call --to "<phone_number>" --message "<message>"
<plugin_name> voicecall status --call-id <id>
```

Replace `<plugin_name>` with either `rampage` or `clawdbot`, `<phone_number>` with the recipient's number, and `<message>` with your desired message.

## Tool

Use `voice_call` for agent-initiated calls.

Actions:
- `initiate_call` (message, to?, mode?)
- `continue_call` (callId, message)
- `speak_to_user` (callId, message)
- `end_call` (callId)
- `get_status` (callId)

## Notes
- Requires the voice-call plugin to be enabled.
- Plugin configuration is located under `plugins.entries.voice-call.config`.
- Twilio configuration: `provider: "twilio"` + `twilio.accountSid/authToken` + `fromNumber`.
- Telnyx configuration: `provider: "telnyx"` + `telnyx.apiKey/connectionId` + `fromNumber`.
- Plivo configuration: `provider: "plivo"` + `plivo.authId/authToken` + `fromNumber`.
- Development fallback: `provider: "mock"` (no network).