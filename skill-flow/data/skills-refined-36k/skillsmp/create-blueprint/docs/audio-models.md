# Audio Model Selection Guide

This guide helps you choose the right audio generation model for speech and music.

## Table of Contents

- [Speech/TTS Models](#speechtts-models)
- [Music Models](#music-models)
- [Model by Producer](#model-by-producer)

---

## Speech/TTS Models

### Quick Comparison

| Model | Provider | Voice Cloning | Emotion | Pitch | Languages |
|-------|----------|---------------|---------|-------|-----------|
| **ElevenLabs v3** | fal-ai | No | No | No | Yes |
| **MiniMax Speech 02 HD** | fal-ai/replicate | No | Yes | Yes | Yes |
| **MiniMax Speech 2.6 HD** | fal-ai/replicate | No | Yes | Yes | Yes |
| **MiniMax Speech Turbo** | replicate | No | Yes | Yes | Yes |
| **Chatterbox** | fal-ai | Yes | No | No | No |
| **Resemble Chatterbox Turbo** | replicate | Yes | No | No | No |

---

### ElevenLabs v3

**Provider:** fal-ai
**ID:** `elevenlabs/tts/eleven-v3`

**Strengths:**
- High-quality voice synthesis
- Multi-language support
- Speed control
- Well-known voice library

**Best for:**
- Professional narration
- Multi-language content
- When quality is paramount

**Key inputs:**
- `Text` → `text`
- `VoiceId` → `voice` (model-specific voice IDs)
- `Speed` → `speed` (0.5-2.0)
- `LanguageCode` → `language_code`

---

### MiniMax Speech (02 HD, 2.6 HD, Turbo)

**Provider:** fal-ai, replicate
**Versions:**
- `minimax/speech-02-hd` - High definition
- `minimax/speech-2.6-hd` - Latest HD version
- `minimax/speech-02-turbo` - Faster (replicate)
- `minimax/speech-2.6-turbo` - Latest turbo (replicate)

**Strengths:**
- Full emotional control
- Pitch adjustment (-12 to +12 semitones)
- Volume control
- Channel selection (mono/stereo)
- Comprehensive audio settings

**Best for:**
- Expressive narration
- When emotion matters
- Fine-tuned audio output
- Characters with distinct voices

**Key inputs (fal-ai - nested structure):**
- `VoiceId` → `voice_setting.voice_id`
- `Speed` → `voice_setting.speed`
- `Pitch` → `voice_setting.pitch`
- `Volume` → `voice_setting.vol`
- `Emotion` → `voice_setting.emotion`
- `OutputFormat` → `audio_setting.format`
- `SampleRate` → `audio_setting.sample_rate`
- `Bitrate` → `audio_setting.bitrate`
- `Channel` → `audio_setting.channel` (1 for mono, 2 for stereo)
- `LanguageCode` → `language_boost`

**Key inputs (replicate - flat structure):**
- `VoiceId` → `voice_id`
- `Speed`, `Pitch`, `Volume`, `Emotion` → direct mapping
- `Channel` → `channel` (string: "mono"/"stereo")

**Emotion options:**
- `happy`, `sad`, `angry`, `neutral`, `surprised`, `fearful`, `disgusted`

---

### Chatterbox

**Provider:** fal-ai, replicate
**ID:** `chatterbox/text-to-speech`, `resemble-ai/chatterbox-turbo`

**Strengths:**
- Voice cloning from reference audio
- Temperature control for variation
- Seed for reproducibility

**Best for:**
- Cloning a specific voice
- When you have reference audio
- Varied generation with temperature

**Key inputs (fal-ai):**
- `Text` → `text`
- `ReferenceAudioUrl` → `audio_url`
- `Temperature` → `temperature`
- `Seed` → `seed`

**Key inputs (replicate):**
- `VoiceId` → `voice`
- `ReferenceAudioUrl` → `reference_audio`
- `Temperature` → `temperature`
- `Seed` → `seed`

---

## Music Models

### Quick Comparison

| Model | Provider | Lyrics | Duration | Key Features |
|-------|----------|--------|----------|--------------|
| **MiniMax Music 1.5** | replicate | Yes | Via lyrics | Song sections |
| **Stable Audio 2.5** | replicate | No | Yes | Diffusion steps |

---

### MiniMax Music 1.5

**Provider:** replicate
**ID:** `minimax/music-1.5`

**Strengths:**
- Lyrics support with section tags
- Song structure control
- Audio format options

**Best for:**
- Songs with vocals
- Structured music (intro, verse, chorus)
- When lyrics matter

**Key inputs:**
- `Prompt` → `prompt` (style/mood description)
- `Lyrics` → `lyrics` (with section tags)
- `OutputFormat` → `audio_format`
- `SampleRate` → `sample_rate`
- `Bitrate` → `bitrate`

**Lyrics format:**
```
[intro]
(Musical intro)

[verse]
First verse lyrics here
More lyrics on this line

[chorus]
Catchy chorus here
Repeat the hook

[outro]
Fade out lyrics
```

---

### Stable Audio 2.5 (Stability AI)

**Provider:** replicate
**ID:** `stability-ai/stable-audio-2.5`

**Strengths:**
- Duration control in seconds
- Diffusion steps for quality
- Guidance scale control
- Good for instrumental

**Best for:**
- Instrumental music
- Background tracks
- When duration control is needed

**Key inputs:**
- `Prompt` → `prompt` (style/mood description)
- `Duration` → `duration` (seconds)
- `Steps` → `steps` (diffusion steps)
- `GuidanceScale` → `cfg_scale`
- `Seed` → `seed`

---

## Model by Producer

### text-to-speech.yaml

| Model | Provider | Voice Cloning | Emotion |
|-------|----------|---------------|---------|
| `elevenlabs/tts/eleven-v3` | fal-ai | No | No |
| `minimax/speech-02-hd` | fal-ai | No | Yes |
| `minimax/speech-2.6-hd` | fal-ai | No | Yes |
| `chatterbox/text-to-speech` | fal-ai | Yes | No |
| `minimax/speech-02-hd` | replicate | No | Yes |
| `minimax/speech-02-turbo` | replicate | No | Yes |
| `minimax/speech-2.6-hd` | replicate | No | Yes |
| `minimax/speech-2.6-turbo` | replicate | No | Yes |
| `resemble-ai/chatterbox-turbo` | replicate | Yes | No |

### text-to-music.yaml

| Model | Provider | Lyrics | Duration Control |
|-------|----------|--------|------------------|
| `minimax/music-1.5` | replicate | Yes | Via lyrics |
| `stability-ai/stable-audio-2.5` | replicate | No | Yes |

---

## Audio Output Settings

### Sample Rates
- `8000` - Phone quality
- `16000` - Broadcast quality
- `22050` - FM radio quality
- `24000` - Standard quality
- `32000` - Higher quality
- `44100` - CD quality

### Bitrates
- `32000` - Low quality, small file
- `64000` - Acceptable quality
- `128000` - Good quality (recommended)
- `256000` - High quality

### Output Formats
- `mp3` - Compressed, universal
- `wav` - Uncompressed, high quality
- `flac` - Lossless compression
- `pcm` - Raw audio data

---

## Voice Selection Tips

### ElevenLabs
Voice IDs are specific to ElevenLabs library. Check their documentation for available voices.

### MiniMax Speech
Voice IDs are model-specific. Use the MiniMax voice library for available options.

### Chatterbox
Provide a `ReferenceAudioUrl` to clone any voice. The reference audio should:
- Be clear and noise-free
- Be 10-30 seconds long
- Contain only the target voice
- Be representative of the desired tone
