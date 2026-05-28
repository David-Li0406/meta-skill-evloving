# Models reference

LiveKit Inference is the recommended way to use AI models with LiveKit Agents. It provides access to leading models without managing individual provider API keys. LiveKit Cloud handles authentication, billing, and optimal provider selection automatically.

## LiveKit Inference (recommended)

Use model strings to configure STT, LLM, and TTS in your AgentSession.

### STT (speech-to-text)

```typescript
const session = new voice.AgentSession({
  stt: "deepgram/nova-3:en",
});
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

```typescript
const session = new voice.AgentSession({
  stt: "auto:en",  // Best available English STT
});
```

### LLM (large language model)

```typescript
const session = new voice.AgentSession({
  llm: "openai/gpt-4.1-mini",
});
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

```typescript
const session = new voice.AgentSession({
  tts: "cartesia/sonic-3:9626c31c-bec5-4cca-baa8-f8ba9e84c8bc",
});
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

```typescript
import * as openai from '@livekit/agents-plugin-openai';

const session = new voice.AgentSession({
  llm: new openai.realtime.RealtimeModel({
    voice: 'coral',
    model: 'gpt-4o-realtime-preview',
  }),
});
```

### Gemini Live

```typescript
import * as google from '@livekit/agents-plugin-google';

const session = new voice.AgentSession({
  llm: new google.realtime.RealtimeModel({
    voice: 'Puck',
  }),
});
```

## Advanced configuration

Use the `inference` module when you need additional parameters while still using LiveKit Inference:

```typescript
import { voice, inference } from '@livekit/agents';

const session = new voice.AgentSession({
  llm: new inference.LLM({
    model: "openai/gpt-5-mini",
    provider: "openai",
    modelOptions: { reasoning_effort: "low" }
  }),
  stt: new inference.STT({
    model: "deepgram/nova-3",
    language: "en",
  }),
  tts: new inference.TTS({
    model: "cartesia/sonic-3",
    voice: "9626c31c-bec5-4cca-baa8-f8ba9e84c8bc",
    language: "en",
    modelOptions: { speed: 1.2, emotion: "cheerful" }
  }),
});
```

## VAD and turn detection

These components are configured separately from model providers:

```typescript
import * as silero from '@livekit/agents-plugin-silero';
import * as livekit from '@livekit/agents-plugin-livekit';

// In prewarm
proc.userData.vad = await silero.VAD.load();

// In entry
const session = new voice.AgentSession({
  vad: ctx.proc.userData.vad as silero.VAD,
  turnDetection: new livekit.turnDetector.MultilingualModel(),
});
```

**Turn detection options:**
- `new livekit.turnDetector.MultilingualModel()` - Recommended for natural conversation flow
- `"vad"` - VAD-only turn detection
- `"stt"` - STT endpointing (works with Deepgram Flux)
- `"manual"` - Manual control with `session.commitUserTurn()`

## Noise cancellation

```typescript
import { BackgroundVoiceCancellation } from '@livekit/noise-cancellation-node';

await session.start({
  agent: assistant,
  room: ctx.room,
  inputOptions: {
    noiseCancellation: BackgroundVoiceCancellation(),
  },
});
```

---

## Using plugins (when needed)

Use plugins directly only when you need features not available in LiveKit Inference:

- **Custom or fine-tuned models** not available in LiveKit Inference
- **Voice cloning** with your own provider account
- **Self-hosted models** via Ollama
- **Provider-specific features** not exposed through inference module

### OpenAI (direct)

```typescript
import * as openai from '@livekit/agents-plugin-openai';

const session = new voice.AgentSession({
  llm: new openai.LLM({ model: 'gpt-4o' }),
  stt: new openai.STT(),
  tts: new openai.TTS({ voice: 'alloy' }),
});
```

Requires: `OPENAI_API_KEY`

### Deepgram (direct)

```typescript
import * as deepgram from '@livekit/agents-plugin-deepgram';

const session = new voice.AgentSession({
  stt: new deepgram.STT({ model: 'nova-2' }),
  tts: new deepgram.TTS({ model: 'aura-asteria-en' }),
});
```

Requires: `DEEPGRAM_API_KEY`

### ElevenLabs (direct)

```typescript
import * as elevenlabs from '@livekit/agents-plugin-elevenlabs';

const session = new voice.AgentSession({
  tts: new elevenlabs.TTS({
    voiceId: '21m00Tcm4TlvDq8ikWAM',
    model: 'eleven_turbo_v2_5',
  }),
});
```

Requires: `ELEVENLABS_API_KEY`

### Groq (direct)

```typescript
import * as groq from '@livekit/agents-plugin-groq';

const session = new voice.AgentSession({
  llm: new groq.LLM({ model: 'llama-3.3-70b-versatile' }),
  stt: new groq.STT(),
  tts: new groq.TTS(),
});
```

Requires: `GROQ_API_KEY`

### Other plugins

Additional plugins are available for: Gemini, Ollama, and more. Each requires its own API key and account setup.

See the [LiveKit Agents documentation](https://docs.livekit.io/agents/models) for the full list.

## Package installation

```bash
# Core
pnpm add @livekit/agents@1.x

# Plugins (only install if needed)
pnpm add @livekit/agents-plugin-openai@1.x
pnpm add @livekit/agents-plugin-deepgram@1.x
pnpm add @livekit/agents-plugin-elevenlabs@1.x
pnpm add @livekit/agents-plugin-silero@1.x
pnpm add @livekit/agents-plugin-livekit@1.x
pnpm add @livekit/agents-plugin-gemini@1.x
pnpm add @livekit/agents-plugin-groq@1.x

# Noise cancellation
pnpm add @livekit/noise-cancellation-node@0.x
```
