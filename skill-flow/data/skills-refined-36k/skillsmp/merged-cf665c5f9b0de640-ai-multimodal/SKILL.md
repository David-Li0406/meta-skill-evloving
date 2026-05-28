---
name: ai-multimodal
description: Use this skill to process and generate multimedia content using the Google Gemini API, including audio, images, videos, and documents.
---

# AI Multimodal Processing Skill

Process audio, images, videos, documents, and generate images/videos using Google Gemini's multimodal API. This skill provides a unified interface for all multimedia content understanding and generation.

## Core Capabilities

### Audio Processing
- Transcription with timestamps (up to 9.5 hours)
- Audio summarization and analysis
- Speech understanding and speaker identification
- Music and environmental sound analysis
- Text-to-speech generation with controllable voice

### Image Understanding
- Image captioning and description
- Object detection with bounding boxes
- Pixel-level segmentation
- Visual question answering
- Multi-image comparison
- OCR and text extraction

### Video Analysis
- Scene detection and summarization
- Video Q&A with temporal understanding
- Transcription with visual descriptions
- YouTube URL support
- Long video processing (up to 6 hours)
- Frame-level analysis

### Document Extraction
- Native PDF vision processing (up to 1,000 pages)
- Table and form extraction
- Chart and diagram analysis
- Multi-page document understanding
- Structured data output (JSON schema)
- Format conversion (PDF to HTML/JSON)

### Image and Video Generation
- Text-to-image generation and editing
- Multi-image composition
- Text-to-video generation (8-second clips with native audio)

## Setup

### Prerequisites
**API Key Setup**: Supports both Google AI Studio and Vertex AI.

```bash
export GEMINI_API_KEY="your-key"  # Get from https://aistudio.google.com/apikey
pip install google-genai python-dotenv pillow
```

### Quick Start
- **Verify setup**: `python scripts/check_setup.py`
- **Analyze media**: `python scripts/gemini_batch_process.py --files <file> --task <analyze|transcribe|extract>`
- **Generate content**: `python scripts/gemini_batch_process.py --task <generate|generate-video> --prompt "description"`

## Supported Formats
- **Audio**: WAV, MP3, AAC, FLAC, OGG Vorbis, AIFF (Max 9.5 hours)
- **Images**: PNG, JPEG, WEBP, HEIC, HEIF (Max 3,600 images)
- **Video**: MP4, MPEG, MOV, AVI, FLV, WebM (Max 6 hours)
- **Documents**: PDF only for vision processing (Max 1,000 pages)

## Scripts Overview
- **`gemini_batch_process.py`**: Batch process multiple media files.
- **`media_optimizer.py`**: Prepare media for Gemini API.
- **`document_converter.py`**: Convert documents to PDF and extract data.
- **`check_setup.py`**: Verify environment setup and API key availability.

## References
For detailed implementation guidance, see:
- Audio Processing
- Image Understanding
- Video Analysis
- Document Extraction
- Image and Video Generation

## Limits
- **Size**: 20MB inline, 2GB via File API
- **Rate Limits**: Free tier: 10-15 requests per minute

## Error Handling
Common errors and solutions:
- **400**: Invalid format/size - validate before upload
- **401**: Invalid API key - check configuration
- **429**: Rate limit exceeded - implement exponential backoff

## Resources
- [API Docs](https://ai.google.dev/gemini-api/docs/)
- [Pricing](https://ai.google.dev/pricing)