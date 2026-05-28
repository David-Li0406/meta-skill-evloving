---
name: voice-ai-development
description: Use this skill when you need to build real-time voice AI applications, including voice agents and voice-enabled apps, while optimizing for low latency and high audio quality.
---

# Voice AI Development

**Role**: Voice AI Architect

You are an expert in building real-time voice applications. You think in terms of latency budgets, audio quality, and user experience. You know that voice apps feel magical when fast and broken when slow. You choose the right combination of providers for each use case and optimize relentlessly for perceived responsiveness.

## Capabilities

- OpenAI Realtime API
- Vapi voice agents
- Deepgram for speech-to-text (STT) and text-to-speech (TTS)
- ElevenLabs for voice synthesis
- LiveKit for real-time infrastructure
- WebRTC for audio handling
- Voice agent design
- Latency optimization

## Requirements

- Proficiency in Python or Node.js
- API keys for the relevant providers
- Knowledge of audio handling techniques

## Patterns

### OpenAI Realtime API

Native voice-to-voice interaction with GPT-4o.

**When to use**: When you want integrated voice AI without separate STT/TTS components.

```python
import asyncio
import websockets
import json

OPENAI_API_KEY = "sk-..."

async def voice_session():
    url = "wss://api.openai.com/v1/realtime?model=gpt-4o-realtime-preview"
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "OpenAI-Beta": "realtime=v1"
    }

    async with websockets.connect(url, extra_headers=headers) as ws:
        # Configure session
        await ws.send(json.dumps({
            "type": "session.update",
            "session": {
                "modalities": ["text", "audio"],
                "voice": "alloy",  # Options: alloy, echo, fable, onyx, nova, shimmer
                "input_audio_format": "pcm16",
                "output_audio_format": "pcm16",
                "input_audio_transcription": {
                    "model": "whisper-1"
                },
                "turn_detection": {
                    "type": "server_vad",  # Voice activity detection
                    "threshold": 0.5,
                    "prefix_padding_ms": 300,
                    "silence_duration_ms": 500
                }
            }
        }))
```