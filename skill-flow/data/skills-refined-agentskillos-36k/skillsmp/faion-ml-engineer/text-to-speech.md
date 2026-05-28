---
id: text-to-speech
name: "Text-to-Speech"
domain: ML
skill: faion-ml-engineer
category: "ml-engineering"
---

# Text-to-Speech

## Overview

Text-to-Speech (TTS) converts written text into natural-sounding audio. Modern AI-powered TTS systems offer human-like voices, emotional expression, and multiple language support for applications like audiobooks, voice assistants, and accessibility tools.

## When to Use

- Voice assistants and chatbots
- Audiobook generation
- Video narration
- Accessibility features
- Podcast production
- Interactive voice response (IVR)
- E-learning content

## Key Concepts

### TTS Services Comparison

| Service | Voices | Languages | Real-time | Cost |
|---------|--------|-----------|-----------|------|
| OpenAI TTS | 6 | 50+ | Yes | $0.015-0.030/1K chars |
| ElevenLabs | 120+ | 29 | Yes | $0.18-0.30/1K chars |
| Google TTS | 400+ | 50+ | Yes | $0.004-0.016/1K chars |
| Azure TTS | 500+ | 140+ | Yes | $0.004-0.016/1K chars |
| Coqui | Many | 50+ | Local | Free |

### Voice Characteristics

| Attribute | Description |
|-----------|-------------|
| Pitch | High/low voice frequency |
| Speed | Words per minute |
| Tone | Emotional quality |
| Accent | Regional pronunciation |
| Gender | Voice gender perception |

## Implementation

### OpenAI TTS

```python
from openai import OpenAI
from pathlib import Path

client = OpenAI()

def text_to_speech(
    text: str,
    output_path: str,
    voice: str = "alloy",
    model: str = "tts-1",
    speed: float = 1.0,
    response_format: str = "mp3"
) -> str:
    """
    Convert text to speech using OpenAI TTS.

    voice: "alloy", "echo", "fable", "onyx", "nova", "shimmer"
    model: "tts-1" (faster), "tts-1-hd" (higher quality)
    speed: 0.25 to 4.0
    response_format: "mp3", "opus", "aac", "flac", "wav", "pcm"
    """
    response = client.audio.speech.create(
        model=model,
        voice=voice,
        input=text,
        speed=speed,
        response_format=response_format
    )

    # Save to file
    response.stream_to_file(output_path)
    return output_path

def text_to_speech_stream(
    text: str,
    voice: str = "alloy"
):
    """Stream audio for real-time playback."""
    response = client.audio.speech.create(
        model="tts-1",
        voice=voice,
        input=text
    )

    # Iterate over chunks
    for chunk in response.iter_bytes():
        yield chunk

# Usage
text_to_speech(
    "Hello, this is a test of text to speech.",
    "output.mp3",
    voice="nova",
    model="tts-1-hd"
)
```

### ElevenLabs Integration

```python
from elevenlabs import ElevenLabs
from elevenlabs.client import generate, Voice, VoiceSettings

def elevenlabs_tts(
    text: str,
    output_path: str,
    voice_id: str = "21m00Tcm4TlvDq8ikWAM",  # Rachel
    model: str = "eleven_multilingual_v2",
    stability: float = 0.5,
    similarity_boost: float = 0.75
) -> str:
    """Generate speech using ElevenLabs."""
    client = ElevenLabs()

    audio = client.generate(
        text=text,
        voice=Voice(
            voice_id=voice_id,
            settings=VoiceSettings(
                stability=stability,
                similarity_boost=similarity_boost,
                style=0.5,
                use_speaker_boost=True
            )
        ),
        model=model
    )

    # Save audio
    with open(output_path, "wb") as f:
        for chunk in audio:
            f.write(chunk)

    return output_path

def clone_voice(
    audio_samples: list[str],
    name: str,
    description: str = ""
) -> str:
    """Clone a voice from audio samples."""
    client = ElevenLabs()

    voice = client.clone(
        name=name,
        description=description,
        files=audio_samples
    )

    return voice.voice_id

def list_voices():
    """List available ElevenLabs voices."""
    client = ElevenLabs()
    return client.voices.get_all()
```

### Google Cloud TTS

```python
from google.cloud import texttospeech

def google_tts(
    text: str,
    output_path: str,
    language_code: str = "en-US",
    voice_name: str = "en-US-Neural2-D",
    speaking_rate: float = 1.0,
    pitch: float = 0.0
) -> str:
    """Generate speech using Google Cloud TTS."""
    client = texttospeech.TextToSpeechClient()

    # Build input
    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Voice configuration
    voice = texttospeech.VoiceSelectionParams(
        language_code=language_code,
        name=voice_name
    )

    # Audio configuration
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3,
        speaking_rate=speaking_rate,
        pitch=pitch
    )

    # Generate
    response = client.synthesize_speech(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config
    )

    # Save
    with open(output_path, "wb") as f:
        f.write(response.audio_content)

    return output_path

def google_tts_ssml(
    ssml: str,
    output_path: str,
    language_code: str = "en-US",
    voice_name: str = "en-US-Neural2-D"
) -> str:
    """Generate speech from SSML markup."""
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(ssml=ssml)

    voice = texttospeech.VoiceSelectionParams(
        language_code=language_code,
        name=voice_name
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config
    )

    with open(output_path, "wb") as f:
        f.write(response.audio_content)

    return output_path
```

### SSML Support

```python
class SSMLBuilder:
    """Build SSML markup for speech synthesis."""

    def __init__(self):
        self.content = []

    def say(self, text: str):
        """Add plain text."""
        self.content.append(text)
        return self

    def pause(self, duration_ms: int):
        """Add a pause."""
        self.content.append(f'<break time="{duration_ms}ms"/>')
        return self

    def emphasis(self, text: str, level: str = "moderate"):
        """Add emphasis (strong, moderate, reduced)."""
        self.content.append(f'<emphasis level="{level}">{text}</emphasis>')
        return self

    def say_as(self, text: str, interpret_as: str):
        """Interpret text as specific type (date, cardinal, characters, etc.)."""
        self.content.append(f'<say-as interpret-as="{interpret_as}">{text}</say-as>')
        return self

    def prosody(
        self,
        text: str,
        rate: str = None,
        pitch: str = None,
        volume: str = None
    ):
        """Modify prosody (rate: slow/medium/fast, pitch: low/medium/high)."""
        attrs = []
        if rate:
            attrs.append(f'rate="{rate}"')
        if pitch:
            attrs.append(f'pitch="{pitch}"')
        if volume:
            attrs.append(f'volume="{volume}"')

        attr_str = " ".join(attrs)
        self.content.append(f'<prosody {attr_str}>{text}</prosody>')
        return self

    def sub(self, text: str, alias: str):
        """Substitute pronunciation."""
        self.content.append(f'<sub alias="{alias}">{text}</sub>')
        return self

    def phoneme(self, text: str, phonetic: str, alphabet: str = "ipa"):
        """Specify phonetic pronunciation."""
        self.content.append(
            f'<phoneme alphabet="{alphabet}" ph="{phonetic}">{text}</phoneme>'
        )
        return self

    def build(self) -> str:
        """Build final SSML."""
        content_str = "".join(self.content)
        return f'<speak>{content_str}</speak>'

# Usage
ssml = (
    SSMLBuilder()
    .say("Welcome to our service.")
    .pause(500)
    .prosody("This is important!", pitch="high", rate="slow")
    .pause(300)
    .say("Your order number is ")
    .say_as("12345", "cardinal")
    .say(".")
    .build()
)
```

### Long Text Processing

```python
from typing import List
import re

class LongTextTTS:
    """Handle long text for TTS with chunking."""

    def __init__(
        self,
        max_chars: int = 4096,
        overlap_chars: int = 50
    ):
        self.max_chars = max_chars
        self.overlap_chars = overlap_chars
        self.client = OpenAI()

    def synthesize(
        self,
        text: str,
        output_path: str,
        voice: str = "alloy"
    ) -> str:
        """Synthesize long text with automatic chunking."""
        from pydub import AudioSegment

        # Split into chunks
        chunks = self._split_text(text)

        # Generate audio for each chunk
        audio_segments = []
        for i, chunk in enumerate(chunks):
            print(f"Processing chunk {i + 1}/{len(chunks)}")

            response = self.client.audio.speech.create(
                model="tts-1",
                voice=voice,
                input=chunk
            )

            # Save temp file
            temp_path = f"/tmp/chunk_{i}.mp3"
            response.stream_to_file(temp_path)

            audio_segments.append(AudioSegment.from_mp3(temp_path))

        # Combine audio
        combined = audio_segments[0]
        for segment in audio_segments[1:]:
            combined += segment

        # Export
        combined.export(output_path, format="mp3")

        # Cleanup temp files
        import os
        for i in range(len(chunks)):
            os.remove(f"/tmp/chunk_{i}.mp3")

        return output_path

    def _split_text(self, text: str) -> List[str]:
        """Split text at sentence boundaries."""
        chunks = []
        current_chunk = ""

        # Split into sentences
        sentences = re.split(r'(?<=[.!?])\s+', text)

        for sentence in sentences:
            if len(current_chunk) + len(sentence) <= self.max_chars:
                current_chunk += sentence + " "
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = sentence + " "

        if current_chunk:
            chunks.append(current_chunk.strip())

        return chunks
```

### Real-time Streaming

```python
import asyncio
from typing import AsyncGenerator

async def stream_tts(
    text: str,
    voice: str = "alloy"
) -> AsyncGenerator[bytes, None]:
    """Stream TTS audio in real-time."""
    client = OpenAI()

    async with client.audio.speech.with_streaming_response.create(
        model="tts-1",
        voice=voice,
        input=text,
        response_format="pcm"  # Raw PCM for low latency
    ) as response:
        async for chunk in response.iter_bytes():
            yield chunk

async def stream_to_speaker(text: str):
    """Stream directly to speakers using pyaudio."""
    import pyaudio

    p = pyaudio.PyAudio()
    stream = p.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=24000,  # OpenAI TTS sample rate
        output=True
    )

    async for chunk in stream_tts(text):
        stream.write(chunk)

    stream.stop_stream()
    stream.close()
    p.terminate()
```

### Production TTS Service

```python
from dataclasses import dataclass
from typing import Optional, List, Dict, Any, Union
from pathlib import Path
from enum import Enum
import logging
import hashlib

class TTSProvider(Enum):
    OPENAI = "openai"
    ELEVENLABS = "elevenlabs"
    GOOGLE = "google"

@dataclass
class Voice:
    id: str
    name: str
    provider: TTSProvider
    language: str = "en"
    gender: str = "neutral"

@dataclass
class TTSConfig:
    provider: TTSProvider = TTSProvider.OPENAI
    default_voice: str = "alloy"
    default_speed: float = 1.0
    output_format: str = "mp3"
    cache_enabled: bool = True
    cache_dir: str = "./tts_cache"
    max_text_length: int = 4096

class TTSService:
    """Production text-to-speech service."""

    def __init__(self, config: Optional[TTSConfig] = None):
        self.config = config or TTSConfig()
        self.logger = logging.getLogger(__name__)

        if self.config.cache_enabled:
            Path(self.config.cache_dir).mkdir(exist_ok=True)

        self._init_provider()

    def _init_provider(self):
        """Initialize TTS provider."""
        if self.config.provider == TTSProvider.OPENAI:
            self.client = OpenAI()

    def synthesize(
        self,
        text: str,
        output_path: Optional[str] = None,
        voice: Optional[str] = None,
        speed: Optional[float] = None,
        use_cache: bool = True
    ) -> Dict[str, Any]:
        """Synthesize speech from text."""
        voice = voice or self.config.default_voice
        speed = speed or self.config.default_speed

        # Check cache
        if use_cache and self.config.cache_enabled:
            cached_path = self._get_cached(text, voice, speed)
            if cached_path:
                self.logger.info("Cache hit")
                return {"success": True, "path": cached_path, "cached": True}

        # Validate text length
        if len(text) > self.config.max_text_length:
            return self._synthesize_long(text, output_path, voice, speed)

        try:
            # Generate audio
            if self.config.provider == TTSProvider.OPENAI:
                audio_path = self._synthesize_openai(text, output_path, voice, speed)
            else:
                raise ValueError(f"Unsupported provider: {self.config.provider}")

            # Cache if enabled
            if self.config.cache_enabled:
                self._cache_audio(text, voice, speed, audio_path)

            return {
                "success": True,
                "path": audio_path,
                "cached": False,
                "duration": self._get_duration(audio_path)
            }

        except Exception as e:
            self.logger.error(f"TTS failed: {e}")
            return {"success": False, "error": str(e)}

    def _synthesize_openai(
        self,
        text: str,
        output_path: Optional[str],
        voice: str,
        speed: float
    ) -> str:
        """Synthesize using OpenAI TTS."""
        response = self.client.audio.speech.create(
            model="tts-1-hd",
            voice=voice,
            input=text,
            speed=speed,
            response_format=self.config.output_format
        )

        output_path = output_path or f"/tmp/tts_{hash(text)}.{self.config.output_format}"
        response.stream_to_file(output_path)

        return output_path

    def _synthesize_long(
        self,
        text: str,
        output_path: Optional[str],
        voice: str,
        speed: float
    ) -> Dict:
        """Handle long text."""
        processor = LongTextTTS(max_chars=self.config.max_text_length)
        output_path = output_path or f"/tmp/tts_long_{hash(text)}.mp3"
        result_path = processor.synthesize(text, output_path, voice)

        return {
            "success": True,
            "path": result_path,
            "cached": False
        }

    def _get_cache_key(self, text: str, voice: str, speed: float) -> str:
        """Generate cache key."""
        content = f"{text}|{voice}|{speed}|{self.config.provider.value}"
        return hashlib.sha256(content.encode()).hexdigest()

    def _get_cached(self, text: str, voice: str, speed: float) -> Optional[str]:
        """Get cached audio file."""
        key = self._get_cache_key(text, voice, speed)
        cache_path = Path(self.config.cache_dir) / f"{key}.{self.config.output_format}"

        if cache_path.exists():
            return str(cache_path)
        return None

    def _cache_audio(self, text: str, voice: str, speed: float, audio_path: str):
        """Cache audio file."""
        import shutil
        key = self._get_cache_key(text, voice, speed)
        cache_path = Path(self.config.cache_dir) / f"{key}.{self.config.output_format}"
        shutil.copy(audio_path, cache_path)

    def _get_duration(self, audio_path: str) -> float:
        """Get audio duration in seconds."""
        try:
            from pydub import AudioSegment
            audio = AudioSegment.from_file(audio_path)
            return len(audio) / 1000.0
        except:
            return 0.0

    def get_available_voices(self) -> List[Voice]:
        """Get available voices for current provider."""
        if self.config.provider == TTSProvider.OPENAI:
            return [
                Voice("alloy", "Alloy", TTSProvider.OPENAI, "en", "neutral"),
                Voice("echo", "Echo", TTSProvider.OPENAI, "en", "male"),
                Voice("fable", "Fable", TTSProvider.OPENAI, "en", "neutral"),
                Voice("onyx", "Onyx", TTSProvider.OPENAI, "en", "male"),
                Voice("nova", "Nova", TTSProvider.OPENAI, "en", "female"),
                Voice("shimmer", "Shimmer", TTSProvider.OPENAI, "en", "female"),
            ]
        return []
```

## Best Practices

1. **Voice Selection**
   - Match voice to content type
   - Consider audience preferences
   - Test multiple voices

2. **Text Preparation**
   - Clean and normalize text
   - Use SSML for control
   - Handle abbreviations

3. **Quality vs. Speed**
   - Use HD for final content
   - Use standard for real-time
   - Consider streaming for latency

4. **Caching**
   - Cache repeated phrases
   - Use content-based keys
   - Set appropriate TTLs

5. **Cost Management**
   - Batch similar requests
   - Use local models for development
   - Monitor character usage

## Common Pitfalls

1. **No SSML** - Missing control over pronunciation
2. **Wrong Voice** - Mismatch with content
3. **Long Text** - Exceeding API limits
4. **No Caching** - Regenerating same audio
5. **Ignoring Latency** - Not streaming for real-time
6. **Poor Text** - Abbreviations read literally

## References

- [OpenAI TTS](https://platform.openai.com/docs/guides/text-to-speech)
- [ElevenLabs](https://elevenlabs.io/docs)
- [Google Cloud TTS](https://cloud.google.com/text-to-speech/docs)
- [SSML Reference](https://cloud.google.com/text-to-speech/docs/ssml)
