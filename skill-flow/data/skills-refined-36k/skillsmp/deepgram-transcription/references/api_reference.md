# Deepgram API Reference

## Overview

Deepgram provides speech-to-text transcription via a RESTful API. This reference covers the key features and parameters used in this skill.

## API Endpoint

```
POST https://api.deepgram.com/v1/listen
```

## Authentication

Use token-based authentication in the header:

```
Authorization: Token YOUR_API_KEY
```

## Common Query Parameters

### model

Specifies which Deepgram model to use:

- `nova-2` (Recommended) - Latest and most accurate model
- `nova` - Previous generation
- `whisper-large` - OpenAI Whisper model
- `whisper-medium` - Faster Whisper variant
- `base` - Fastest, less accurate

Example: `?model=nova-2`

### smart_format

Enables automatic formatting:

- `true` (Recommended) - Adds punctuation, capitalization, number formatting
- `false` - Raw text output

Example: `?smart_format=true`

### language

Specify source language (auto-detection if omitted):

- `en` - English
- `es` - Spanish
- `fr` - French
- etc.

Example: `?language=en`

### punctuate

Add punctuation to transcript:

- `true` - Add punctuation
- `false` - No punctuation

Note: Included in `smart_format`

Example: `?punctuate=true`

### diarize

Speaker separation:

- `true` - Separate different speakers
- `false` - No speaker separation

Example: `?diarize=true`

### utterances

Split transcript by speaker turns:

- `true` - Split by utterances
- `false` - Continuous transcript

Example: `?utterances=true`

## Request Headers

### Content-Type

Must match the file format:

- `audio/mp4` - M4A files
- `audio/mpeg` - MP3 files
- `audio/wav` - WAV files
- `video/mp4` - MP4 videos
- `video/quicktime` - MOV videos
- `application/octet-stream` - Generic binary

## Response Format

### Successful Response

```json
{
  "metadata": {
    "transaction_key": "...",
    "request_id": "...",
    "sha256": "...",
    "created": "2025-11-08T12:00:00.000Z",
    "duration": 120.5,
    "channels": 1,
    "models": ["model-id"]
  },
  "results": {
    "channels": [
      {
        "alternatives": [
          {
            "transcript": "Full transcript text here...",
            "confidence": 0.998,
            "words": [
              {
                "word": "hello",
                "start": 0.5,
                "end": 0.9,
                "confidence": 0.99,
                "punctuated_word": "Hello."
              }
            ]
          }
        ]
      }
    ]
  }
}
```

### Key Response Fields

**metadata.duration** - Audio duration in seconds

**results.channels[0].alternatives[0].transcript** - Full transcript text

**results.channels[0].alternatives[0].confidence** - Overall confidence score (0-1)

**results.channels[0].alternatives[0].words** - Array of word-level details with timestamps

**words[].word** - Raw word

**words[].punctuated_word** - Word with punctuation

**words[].start** - Start time in seconds

**words[].end** - End time in seconds

**words[].confidence** - Word-level confidence (0-1)

## Error Responses

### 400 Bad Request

Invalid parameters or file format

### 401 Unauthorized

Invalid or missing API key

### 413 Payload Too Large

File exceeds size limit (solution: extract audio first)

### 429 Too Many Requests

Rate limit exceeded

### 500 Internal Server Error

Deepgram service issue

## Best Practices

### File Size Optimization

1. **Video files**: Always extract audio first for files >50MB
2. **Audio bitrate**: 128kbps is optimal for speech (balances quality and size)
3. **Format**: M4A/AAC provides good compression

### Model Selection

1. **nova-2**: Best for accuracy, supports most languages
2. **whisper-large**: Alternative high-accuracy option
3. **base**: Use only when speed is critical over accuracy

### Smart Formatting

Always enable `smart_format=true` for production use:
- Better readability
- Proper punctuation and capitalization
- Number and date formatting
- No additional cost

### Timeout Settings

- Short audio (<5 min): 30-60 seconds
- Medium audio (5-15 min): 1-2 minutes
- Long audio (15+ min): 3-5 minutes
- Very long/poor quality: 5-10 minutes

## Rate Limits

Varies by plan:
- Free tier: Limited requests per month
- Paid tier: Higher limits based on subscription

Check your account dashboard for current limits.

## Supported Audio Formats

- MP3, MP4/M4A, WAV, FLAC, OGG, WebM
- AAC, AMR, Opus
- Most common audio codecs

## Supported Video Formats

- MP4, MOV, AVI, MKV, FLV, WMV
- Must contain audio track
- Recommendation: Extract audio first for better performance

## Example Curl Commands

### Basic Transcription

```bash
curl -X POST "https://api.deepgram.com/v1/listen?model=nova-2&smart_format=true" \
  -H "Authorization: Token YOUR_API_KEY" \
  -H "Content-Type: audio/mp4" \
  --data-binary @audio.m4a
```

### With Speaker Diarization

```bash
curl -X POST "https://api.deepgram.com/v1/listen?model=nova-2&smart_format=true&diarize=true" \
  -H "Authorization: Token YOUR_API_KEY" \
  -H "Content-Type: audio/mp4" \
  --data-binary @meeting.m4a
```

### With Language Specification

```bash
curl -X POST "https://api.deepgram.com/v1/listen?model=nova-2&language=es" \
  -H "Authorization: Token YOUR_API_KEY" \
  -H "Content-Type: audio/mpeg" \
  --data-binary @spanish_audio.mp3
```
