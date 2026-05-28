---
name: openai-whisper-transcription
description: Use this skill to transcribe audio files to text using OpenAI's Whisper model or API.
---

# OpenAI Whisper Audio Transcription Skill

Transcribe audio files to text using OpenAI's Whisper model or API.

## Capabilities

- Transcribe audio files (MP3, WAV, M4A, FLAC, OGG, etc.) to text
- Support for 90+ languages with auto-detection
- Optional timestamp generation
- Multiple model sizes (tiny/base/small/medium/large)
- Output in plain text or JSON format
- Use OpenAI's API for transcription

## Usage

### Local Transcription with Whisper

#### Basic Transcription

```bash
python3 scripts/transcribe.py <audio_file> <output_file>
```

#### With Options

```bash
# Specify model size (default: base)
python3 scripts/transcribe.py audio.mp3 transcript.txt --model medium

# Specify language (improves accuracy)
python3 scripts/transcribe.py audio.mp3 transcript.txt --language zh

# Include timestamps
python3 scripts/transcribe.py audio.mp3 transcript.txt --timestamps

# JSON output with metadata
python3 scripts/transcribe.py audio.mp3 output.json --format json
```

### Transcription via OpenAI API

#### Quick Start

```bash
{baseDir}/scripts/transcribe.sh /path/to/audio.m4a
```

#### Useful Flags

```bash
{baseDir}/scripts/transcribe.sh /path/to/audio.ogg --model whisper-1 --out /tmp/transcript.txt
{baseDir}/scripts/transcribe.sh /path/to/audio.m4a --language en
{baseDir}/scripts/transcribe.sh /path/to/audio.m4a --prompt "Speaker names: Peter, Daniel"
{baseDir}/scripts/transcribe.sh /path/to/audio.m4a --json --out /tmp/transcript.json
```

## Parameters

- `audio_file` (required): Path to input audio file
- `output_file` (required): Path to output text/JSON file
- `--model`: Whisper model size (tiny/base/small/medium/large, default: base)
- `--language`: Language code (e.g., en, zh, es, fr, auto for detection)
- `--timestamps`: Include word-level timestamps in output
- `--format`: Output format (text/json, default: text)

## Model Sizes

| Model  | Parameters | Speed | Accuracy | Memory |
|--------|------------|-------|----------|--------|
| tiny   | 39M        | ~32x  | Good     | ~1GB   |
| base   | 74M        | ~16x  | Better   | ~1GB   |
| small  | 244M       | ~6x   | Great    | ~2GB   |
| medium | 769M       | ~2x   | Excellent| ~5GB   |
| large  | 1.5B       | 1x    | Best     | ~10GB  |

## Supported Audio Formats

MP3, WAV, M4A, FLAC, OGG, AAC, WMA, and more (via FFmpeg)

## Dependencies

- Python 3.8+
- openai-whisper
- ffmpeg
- curl (for API usage)

## Installation

```bash
pip install openai-whisper
sudo apt-get install ffmpeg  # Ubuntu/Debian
```

## API Key

Set `OPENAI_API_KEY`, or configure it in `~/.rampage/rampage.json`:

```json5
{
  skills: {
    "openai-whisper-api": {
      apiKey: "OPENAI_KEY_HERE"
    }
  }
}
```