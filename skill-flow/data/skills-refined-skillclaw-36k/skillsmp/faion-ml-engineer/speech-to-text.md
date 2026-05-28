---
id: speech-to-text
name: "Speech-to-Text"
domain: ML
skill: faion-ml-engineer
category: "ml-engineering"
---

# Speech-to-Text

## Overview

Speech-to-Text (STT) converts audio recordings into text transcriptions. Modern AI-powered STT systems like Whisper provide high accuracy across many languages with features like speaker diarization, timestamps, and translation.

## When to Use

- Meeting transcription
- Voice note processing
- Podcast/video transcription
- Voice command recognition
- Call center analysis
- Accessibility features
- Content indexing

## Key Concepts

### STT Services Comparison

| Service | Languages | Features | Cost |
|---------|-----------|----------|------|
| OpenAI Whisper | 99+ | Translation, timestamps | $0.006/min |
| Whisper Local | 99+ | Offline, customizable | Free |
| Google Speech | 125+ | Streaming, diarization | $0.004-0.016/min |
| AssemblyAI | 100+ | Diarization, summaries | $0.002-0.04/min |
| Deepgram | 30+ | Real-time, custom vocab | $0.0043/min |

### Audio Formats

| Format | Quality | Size | Supported |
|--------|---------|------|-----------|
| WAV | Lossless | Large | Yes |
| MP3 | Good | Medium | Yes |
| M4A | Good | Medium | Yes |
| FLAC | Lossless | Medium | Yes |
| WebM | Variable | Small | Yes |

## Implementation

### OpenAI Whisper API

```python
from openai import OpenAI
from pathlib import Path

client = OpenAI()

def transcribe_audio(
    audio_path: str,
    language: str = None,
    response_format: str = "text",
    prompt: str = None
) -> str:
    """
    Transcribe audio using Whisper API.

    response_format: "text", "json", "verbose_json", "srt", "vtt"
    """
    with open(audio_path, "rb") as audio_file:
        response = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
            language=language,  # ISO-639-1 code (e.g., "en", "es", "uk")
            response_format=response_format,
            prompt=prompt  # Guide transcription with context
        )

    if response_format == "text":
        return response
    return response

def transcribe_with_timestamps(audio_path: str) -> dict:
    """Get transcription with word-level timestamps."""
    with open(audio_path, "rb") as audio_file:
        response = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
            response_format="verbose_json",
            timestamp_granularities=["word", "segment"]
        )

    return {
        "text": response.text,
        "segments": response.segments,
        "words": response.words,
        "duration": response.duration
    }

def translate_audio(audio_path: str) -> str:
    """Translate audio to English."""
    with open(audio_path, "rb") as audio_file:
        response = client.audio.translations.create(
            model="whisper-1",
            file=audio_file
        )
    return response.text
```

### Local Whisper

```python
import whisper
import torch

class LocalWhisper:
    """Local Whisper transcription."""

    def __init__(
        self,
        model_size: str = "base",
        device: str = None
    ):
        """
        model_size: "tiny", "base", "small", "medium", "large", "large-v3"
        """
        if device is None:
            device = "cuda" if torch.cuda.is_available() else "cpu"
        self.device = device
        self.model = whisper.load_model(model_size, device=device)

    def transcribe(
        self,
        audio_path: str,
        language: str = None,
        task: str = "transcribe",  # or "translate"
        word_timestamps: bool = False
    ) -> dict:
        """Transcribe audio file."""
        result = self.model.transcribe(
            audio_path,
            language=language,
            task=task,
            word_timestamps=word_timestamps
        )

        return {
            "text": result["text"],
            "segments": result["segments"],
            "language": result["language"]
        }

    def transcribe_with_vad(
        self,
        audio_path: str,
        vad_threshold: float = 0.5
    ) -> dict:
        """Transcribe with voice activity detection."""
        # Use faster-whisper for better VAD support
        from faster_whisper import WhisperModel

        model = WhisperModel(
            "base",
            device=self.device,
            compute_type="float16" if self.device == "cuda" else "int8"
        )

        segments, info = model.transcribe(
            audio_path,
            vad_filter=True,
            vad_parameters={"threshold": vad_threshold}
        )

        return {
            "segments": list(segments),
            "language": info.language,
            "language_probability": info.language_probability
        }
```

### Faster Whisper (Optimized)

```python
from faster_whisper import WhisperModel
from typing import Generator, Dict

class FasterWhisperTranscriber:
    """Optimized Whisper using CTranslate2."""

    def __init__(
        self,
        model_size: str = "base",
        device: str = "auto",
        compute_type: str = "auto"
    ):
        self.model = WhisperModel(
            model_size,
            device=device,
            compute_type=compute_type
        )

    def transcribe(
        self,
        audio_path: str,
        language: str = None,
        beam_size: int = 5,
        word_timestamps: bool = False,
        vad_filter: bool = True
    ) -> Dict:
        """Transcribe audio with optimized performance."""
        segments, info = self.model.transcribe(
            audio_path,
            language=language,
            beam_size=beam_size,
            word_timestamps=word_timestamps,
            vad_filter=vad_filter
        )

        # Collect segments
        all_segments = []
        full_text = ""

        for segment in segments:
            all_segments.append({
                "start": segment.start,
                "end": segment.end,
                "text": segment.text,
                "words": [
                    {"word": w.word, "start": w.start, "end": w.end, "probability": w.probability}
                    for w in (segment.words or [])
                ]
            })
            full_text += segment.text

        return {
            "text": full_text.strip(),
            "segments": all_segments,
            "language": info.language,
            "language_probability": info.language_probability,
            "duration": info.duration
        }

    def transcribe_stream(
        self,
        audio_path: str,
        **kwargs
    ) -> Generator[Dict, None, None]:
        """Stream transcription segments."""
        segments, info = self.model.transcribe(audio_path, **kwargs)

        for segment in segments:
            yield {
                "start": segment.start,
                "end": segment.end,
                "text": segment.text
            }
```

### Long Audio Processing

```python
from pydub import AudioSegment
from pathlib import Path
import tempfile
from typing import List, Dict

class LongAudioTranscriber:
    """Handle long audio files by chunking."""

    def __init__(
        self,
        chunk_duration_ms: int = 300000,  # 5 minutes
        overlap_ms: int = 5000  # 5 seconds
    ):
        self.chunk_duration = chunk_duration_ms
        self.overlap = overlap_ms
        self.client = OpenAI()

    def transcribe(self, audio_path: str) -> Dict:
        """Transcribe long audio file."""
        # Load audio
        audio = AudioSegment.from_file(audio_path)
        duration_ms = len(audio)

        # Check if chunking needed (Whisper limit is 25MB)
        if duration_ms <= self.chunk_duration:
            return self._transcribe_chunk(audio_path)

        # Chunk and transcribe
        chunks = self._split_audio(audio)
        results = []

        for i, chunk in enumerate(chunks):
            print(f"Processing chunk {i + 1}/{len(chunks)}")

            # Save chunk to temp file
            with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as f:
                chunk["audio"].export(f.name, format="mp3")
                result = self._transcribe_chunk(f.name)

                results.append({
                    "start_ms": chunk["start"],
                    "end_ms": chunk["end"],
                    "text": result
                })

                Path(f.name).unlink()

        # Merge results
        return self._merge_results(results)

    def _split_audio(self, audio: AudioSegment) -> List[Dict]:
        """Split audio into overlapping chunks."""
        chunks = []
        duration_ms = len(audio)
        start = 0

        while start < duration_ms:
            end = min(start + self.chunk_duration, duration_ms)
            chunk = audio[start:end]

            chunks.append({
                "audio": chunk,
                "start": start,
                "end": end
            })

            start = end - self.overlap

        return chunks

    def _transcribe_chunk(self, audio_path: str) -> str:
        """Transcribe single chunk."""
        with open(audio_path, "rb") as f:
            response = self.client.audio.transcriptions.create(
                model="whisper-1",
                file=f
            )
        return response

    def _merge_results(self, results: List[Dict]) -> Dict:
        """Merge chunk results, handling overlap."""
        full_text = results[0]["text"]

        for i in range(1, len(results)):
            # Simple merge (more sophisticated would handle overlap)
            full_text += " " + results[i]["text"]

        return {
            "text": full_text,
            "chunks": results
        }
```

### Speaker Diarization

```python
# Using pyannote for speaker diarization
# pip install pyannote.audio

from pyannote.audio import Pipeline
from typing import Dict, List
import torch

class SpeakerDiarizer:
    """Add speaker labels to transcription."""

    def __init__(self, hf_token: str):
        """
        Requires HuggingFace token with pyannote access.
        """
        self.pipeline = Pipeline.from_pretrained(
            "pyannote/speaker-diarization-3.1",
            use_auth_token=hf_token
        )

        if torch.cuda.is_available():
            self.pipeline.to(torch.device("cuda"))

    def diarize(self, audio_path: str) -> List[Dict]:
        """Get speaker segments."""
        diarization = self.pipeline(audio_path)

        segments = []
        for turn, _, speaker in diarization.itertracks(yield_label=True):
            segments.append({
                "speaker": speaker,
                "start": turn.start,
                "end": turn.end
            })

        return segments

    def align_with_transcript(
        self,
        audio_path: str,
        transcript_segments: List[Dict]
    ) -> List[Dict]:
        """Align speaker labels with transcript."""
        speaker_segments = self.diarize(audio_path)

        # Assign speakers to transcript segments
        for segment in transcript_segments:
            segment_mid = (segment["start"] + segment["end"]) / 2

            # Find overlapping speaker
            for speaker_seg in speaker_segments:
                if speaker_seg["start"] <= segment_mid <= speaker_seg["end"]:
                    segment["speaker"] = speaker_seg["speaker"]
                    break
            else:
                segment["speaker"] = "UNKNOWN"

        return transcript_segments
```

### Production Transcription Service

```python
from dataclasses import dataclass
from typing import Optional, List, Dict, Any, Union
from pathlib import Path
from enum import Enum
import logging
import os

class TranscriptionProvider(Enum):
    OPENAI = "openai"
    LOCAL = "local"
    FASTER_WHISPER = "faster_whisper"

@dataclass
class TranscriptionConfig:
    provider: TranscriptionProvider = TranscriptionProvider.OPENAI
    model_size: str = "base"  # For local models
    language: Optional[str] = None
    word_timestamps: bool = False
    speaker_diarization: bool = False
    max_file_size_mb: int = 25
    supported_formats: List[str] = None

    def __post_init__(self):
        if self.supported_formats is None:
            self.supported_formats = [".mp3", ".wav", ".m4a", ".flac", ".webm", ".mp4"]

class TranscriptionService:
    """Production speech-to-text service."""

    def __init__(self, config: Optional[TranscriptionConfig] = None):
        self.config = config or TranscriptionConfig()
        self.logger = logging.getLogger(__name__)
        self._init_provider()

    def _init_provider(self):
        """Initialize transcription provider."""
        if self.config.provider == TranscriptionProvider.OPENAI:
            self.client = OpenAI()
        elif self.config.provider == TranscriptionProvider.FASTER_WHISPER:
            self.transcriber = FasterWhisperTranscriber(
                model_size=self.config.model_size
            )
        elif self.config.provider == TranscriptionProvider.LOCAL:
            self.transcriber = LocalWhisper(
                model_size=self.config.model_size
            )

    def transcribe(
        self,
        audio_path: Union[str, Path],
        **kwargs
    ) -> Dict[str, Any]:
        """Transcribe audio file."""
        audio_path = Path(audio_path)

        # Validate file
        if not audio_path.exists():
            raise FileNotFoundError(f"Audio file not found: {audio_path}")

        if audio_path.suffix.lower() not in self.config.supported_formats:
            raise ValueError(f"Unsupported format: {audio_path.suffix}")

        # Check file size
        size_mb = audio_path.stat().st_size / (1024 * 1024)
        if size_mb > self.config.max_file_size_mb:
            self.logger.info(f"Large file ({size_mb:.1f}MB), using chunked processing")
            return self._transcribe_large(audio_path, **kwargs)

        # Transcribe
        try:
            if self.config.provider == TranscriptionProvider.OPENAI:
                result = self._transcribe_openai(audio_path, **kwargs)
            else:
                result = self._transcribe_local(audio_path, **kwargs)

            # Add speaker diarization if enabled
            if self.config.speaker_diarization and "segments" in result:
                result = self._add_speakers(audio_path, result)

            return {
                "success": True,
                **result
            }

        except Exception as e:
            self.logger.error(f"Transcription failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }

    def _transcribe_openai(self, audio_path: Path, **kwargs) -> Dict:
        """Transcribe using OpenAI Whisper API."""
        response_format = "verbose_json" if self.config.word_timestamps else "json"

        with open(audio_path, "rb") as f:
            response = self.client.audio.transcriptions.create(
                model="whisper-1",
                file=f,
                language=self.config.language,
                response_format=response_format,
                timestamp_granularities=["word", "segment"] if self.config.word_timestamps else None
            )

        if response_format == "verbose_json":
            return {
                "text": response.text,
                "segments": response.segments,
                "words": getattr(response, "words", None),
                "duration": response.duration
            }
        return {"text": response.text}

    def _transcribe_local(self, audio_path: Path, **kwargs) -> Dict:
        """Transcribe using local model."""
        return self.transcriber.transcribe(
            str(audio_path),
            language=self.config.language,
            word_timestamps=self.config.word_timestamps
        )

    def _transcribe_large(self, audio_path: Path, **kwargs) -> Dict:
        """Handle large files."""
        processor = LongAudioTranscriber()
        return processor.transcribe(str(audio_path))

    def _add_speakers(self, audio_path: Path, result: Dict) -> Dict:
        """Add speaker diarization."""
        # Would need pyannote token
        # diarizer = SpeakerDiarizer(hf_token=os.environ.get("HF_TOKEN"))
        # result["segments"] = diarizer.align_with_transcript(
        #     str(audio_path),
        #     result["segments"]
        # )
        return result
```

## Best Practices

1. **Audio Quality**
   - Use clear recordings
   - Minimize background noise
   - Prefer lossless formats for quality

2. **Performance**
   - Use faster-whisper for speed
   - Chunk long audio files
   - Use appropriate model size

3. **Accuracy**
   - Provide language hint
   - Use prompts for domain terms
   - Post-process results

4. **Cost Optimization**
   - Use local models for high volume
   - Compress audio before sending
   - Cache transcriptions

5. **Production**
   - Implement retries
   - Handle rate limits
   - Monitor transcription quality

## Common Pitfalls

1. **File Size Limits** - Not chunking large files
2. **Wrong Language** - Not specifying language code
3. **Poor Audio** - Low quality inputs
4. **No Timestamps** - Missing timing information
5. **Speaker Confusion** - Not using diarization
6. **Slow Processing** - Using large models unnecessarily

## References

- [OpenAI Whisper API](https://platform.openai.com/docs/guides/speech-to-text)
- [Whisper GitHub](https://github.com/openai/whisper)
- [faster-whisper](https://github.com/guillaumekln/faster-whisper)
- [pyannote-audio](https://github.com/pyannote/pyannote-audio)
