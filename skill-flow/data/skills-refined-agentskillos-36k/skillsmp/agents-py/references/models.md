# Models reference

LiveKit Inference is the recommended way to use AI models with LiveKit Agents. It provides access to leading models without managing individual provider API keys. LiveKit Cloud handles authentication, billing, and optimal provider selection automatically.

## LiveKit Inference (recommended)

Use model strings to configure STT, LLM, and TTS in your AgentSession.

### STT (speech-to-text)

```python
session = AgentSession(
    stt="deepgram/nova-3:en",
)
```

| Provider | Model | String |
|----------|-------|--------|
| AssemblyAI | Universal Streaming | `"assemblyai/universal-streaming:en"` |
| AssemblyAI | Universal Multilingual | `"assemblyai/universal-streaming-multilingual:en"` |
| Cartesia | Ink Whisper | `"cartesia/ink"` |
| Deepgram | Flux | `"deepgram/flux-general:en"` |
| Deepgram | Nova 3 | `"deepgram/nova-3:en"` |
| Deepgram | Nova 3 (multilingual) | `"deepgram/nova-3:multi"` |
| Deepgram | Nova 2 | `"deepgram/nova-2:en"` |
| ElevenLabs | Scribe V2 | `"elevenlabs/scribe_v1:en"` |

**Automatic model selection:** Use `"auto:language"` to let LiveKit choose the best STT model for a language:

```python
session = AgentSession(
    stt="auto:en",  # Best available English STT
    stt="auto:es",  # Best available Spanish STT
)
```

### LLM (large language model)

```python
session = AgentSession(
    llm="openai/gpt-4.1-mini",
)
```

| Provider | Model | String |
|----------|-------|--------|
| OpenAI | GPT-4.1 mini | `"openai/gpt-4.1-mini"` |
| OpenAI | GPT-4.1 | `"openai/gpt-4.1"` |
| OpenAI | GPT-4.1 nano | `"openai/gpt-4.1-nano"` |
| OpenAI | GPT-5 | `"openai/gpt-5"` |
| OpenAI | GPT-5 mini | `"openai/gpt-5-mini"` |
| OpenAI | GPT-5 nano | `"openai/gpt-5-nano"` |
| OpenAI | GPT-5.1 | `"openai/gpt-5.1"` |
| OpenAI | GPT-5.2 | `"openai/gpt-5.2"` |
| OpenAI | GPT OSS 120B | `"openai/gpt-oss-120b"` |
| Google | Gemini 3 Pro | `"gemini/gemini-3-pro"` |
| Google | Gemini 3 Flash | `"gemini/gemini-3-flash"` |
| Google | Gemini 2.5 Pro | `"gemini/gemini-2.5-pro"` |
| Google | Gemini 2.5 Flash | `"gemini/gemini-2.5-flash"` |
| Google | Gemini 2.0 Flash | `"gemini/gemini-2.0-flash"` |
| DeepSeek | DeepSeek V3 | `"deepseek/deepseek-v3"` |
| DeepSeek | DeepSeek V3.2 | `"deepseek/deepseek-v3.2"` |

### TTS (text-to-speech)

```python
session = AgentSession(
    tts="cartesia/sonic-3:9626c31c-bec5-4cca-baa8-f8ba9e84c8bc",
)
```

| Provider | Model | String format |
|----------|-------|---------------|
| Cartesia | Sonic 3 | `"cartesia/sonic-3:{voice_id}"` |
| Cartesia | Sonic 2 | `"cartesia/sonic-2:{voice_id}"` |
| Deepgram | Aura 2 | `"deepgram/aura-2:{voice}"` |
| ElevenLabs | Turbo v2.5 | `"elevenlabs/eleven_turbo_v2_5:{voice_id}"` |
| Inworld | Inworld TTS | `"inworld/inworld-tts-1:{voice_name}"` |
| Rime | Arcana | `"rime/arcana:{voice}"` |
| Rime | Mist | `"rime/mist:{voice}"` |

**Popular voices:**

| Provider | Voice | String |
|----------|-------|--------|
| Cartesia | Jacqueline (American female) | `"cartesia/sonic-3:9626c31c-bec5-4cca-baa8-f8ba9e84c8bc"` |
| Cartesia | Blake (American male) | `"cartesia/sonic-3:a167e0f3-df7e-4d52-a9c3-f949145efdab"` |
| Deepgram | Apollo (casual male) | `"deepgram/aura-2:apollo"` |
| Deepgram | Athena (professional female) | `"deepgram/aura-2:athena"` |
| ElevenLabs | Jessica (playful female) | `"elevenlabs/eleven_turbo_v2_5:cgSgspJ2msm6clMCkdW9"` |
| Rime | Luna (excitable female) | `"rime/arcana:luna"` |

## Realtime models

For speech-to-speech without separate STT/TTS pipelines:

### OpenAI Realtime

```python
from livekit.plugins import openai

session = AgentSession(
    llm=openai.realtime.RealtimeModel(
        voice="coral",
        model="gpt-4o-realtime-preview",
    ),
)
```

### Gemini Live

```python
from livekit.plugins import google

session = AgentSession(
    llm=google.realtime.RealtimeModel(
        voice="Puck",
    ),
)
```

### xAI Grok

```python
from livekit.plugins import xai

session = AgentSession(
    llm=xai.realtime.RealtimeModel(
        voice="aurora",
    ),
)
```

## Advanced configuration

Use the `inference` module when you need additional parameters while still using LiveKit Inference:

```python
from livekit.agents import AgentSession, inference

session = AgentSession(
    llm=inference.LLM(
        model="openai/gpt-5-mini",
        provider="openai",
        extra_kwargs={"reasoning_effort": "low"}
    ),
    stt=inference.STT(
        model="deepgram/nova-3",
        language="en",
    ),
    tts=inference.TTS(
        model="cartesia/sonic-3",
        voice="9626c31c-bec5-4cca-baa8-f8ba9e84c8bc",
        language="en",
        extra_kwargs={"speed": 1.2, "emotion": "cheerful"}
    ),
)
```

## VAD and turn detection

These components are configured separately from model providers:

```python
from livekit.plugins import silero
from livekit.plugins.turn_detector.multilingual import MultilingualModel

session = AgentSession(
    vad=silero.VAD.load(),
    turn_detection=MultilingualModel(),  # Recommended
)
```

**Turn detection options:**
- `MultilingualModel()` - Recommended for natural conversation flow
- `"vad"` - VAD-only turn detection
- `"stt"` - STT endpointing (works with Deepgram Flux)
- `"manual"` - Manual control with `session.commit_user_turn()`

## Noise cancellation

```python
from livekit.plugins import noise_cancellation
from livekit.agents import room_io

await session.start(
    room=ctx.room,
    agent=agent,
    room_options=room_io.RoomOptions(
        audio_input=room_io.AudioInputOptions(
            noise_cancellation=noise_cancellation.BVC(),
        ),
    ),
)
```

---

## Using plugins (when needed)

Use plugins directly only when you need features not available in LiveKit Inference:

- **Custom or fine-tuned models** not available in LiveKit Inference
- **Voice cloning** with your own provider account
- **Anthropic Claude models** (not available in LiveKit Inference)
- **Self-hosted models** via Ollama
- **Provider-specific features** not exposed through inference module

### Anthropic

```python
from livekit.plugins import anthropic

session = AgentSession(
    llm=anthropic.LLM(model="claude-sonnet-4-20250514"),
)
```

Requires: `ANTHROPIC_API_KEY`

### OpenAI (direct)

```python
from livekit.plugins import openai

session = AgentSession(
    llm=openai.LLM(model="gpt-4o"),
    stt=openai.STT(),
    tts=openai.TTS(voice="alloy"),
)
```

Requires: `OPENAI_API_KEY`

### Ollama (self-hosted)

```python
from livekit.plugins import ollama

session = AgentSession(
    llm=ollama.LLM(model="llama3.2"),
)
```

### Other plugins

Additional plugins are available for: AWS Bedrock, Azure, Baseten, Cerebras, Deepgram, ElevenLabs, Fireworks, Google Cloud, Groq, Mistral AI, and more. Each requires its own API key and account setup.

See the [LiveKit Agents documentation](https://docs.livekit.io/agents/models) for the full list.
