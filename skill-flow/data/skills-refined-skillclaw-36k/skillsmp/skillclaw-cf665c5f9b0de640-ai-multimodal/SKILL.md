---
name: ai-multimodal
description: Use this skill to process and generate multimedia content using the Google Gemini API, including audio, images, videos, and documents.
---

# Skill body

## Overview
This skill allows you to analyze and generate multimedia content using the Google Gemini API. It supports various tasks such as audio transcription, image understanding, video analysis, document extraction, and content generation.

## Core Capabilities

### Audio Processing
- Transcription with timestamps (up to 9.5 hours)
- Audio summarization and analysis
- Speech understanding and speaker identification
- Music and environmental sound analysis

### Image Understanding
- Image captioning and description
- Object detection and segmentation
- Visual question answering
- Optical character recognition (OCR)

### Video Analysis
- Scene detection and summarization
- Video Q&A with temporal understanding
- Long video processing (up to 6 hours)
- YouTube URL support

### Document Extraction
- PDF processing (up to 1,000 pages)
- Table and form extraction
- Multi-page document understanding

### Content Generation
- Text-to-image generation and editing
- Text-to-video generation (up to 8-second clips)
- Iterative refinement of generated content

## Setup

```bash
export GEMINI_API_KEY="your-key"  # Get from https://aistudio.google.com/apikey
pip install google-genai python-dotenv pillow
```

## Quick Start

1. **Verify setup**: `python scripts/check_setup.py`
2. **Analyze media**: 
   ```bash
   python scripts/gemini_batch_process.py --files <file> --task <analyze|transcribe|extract>
   ```
3. **Generate content**: 
   ```bash
   python scripts/gemini_batch_process.py --task <generate|generate-video> --prompt "description"
   ```

## Notes
- Supports multiple models (Gemini 3/2.5, Imagen 4, Veo 3) with context windows up to 2M tokens.
- For high-volume usage, consider API key rotation to manage rate limits.