# Nano Banana API Reference

Complete API reference for Nano Banana (Gemini 2.5 Flash Image) and Nano Banana PRO (Gemini 3 Pro Image).

## Endpoints

| Model | Endpoint |
|-------|----------|
| Nano Banana PRO | `https://generativelanguage.googleapis.com/v1beta/models/gemini-3-pro-image-preview:generateContent` |
| Nano Banana | `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-image:generateContent` |

## Authentication

Set the API key in the `x-goog-api-key` header:
```bash
-H "x-goog-api-key: $GEMINI_API_KEY"
```

## Request Format

### Basic Text-to-Image

```bash
curl -s -X POST \
  "https://generativelanguage.googleapis.com/v1beta/models/gemini-3-pro-image-preview:generateContent" \
  -H "x-goog-api-key: $GEMINI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "contents": [{
      "parts": [{"text": "A serene mountain landscape at sunset"}]
    }]
  }'
```

### With Image Configuration

```bash
curl -s -X POST \
  "https://generativelanguage.googleapis.com/v1beta/models/gemini-3-pro-image-preview:generateContent" \
  -H "x-goog-api-key: $GEMINI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "contents": [{
      "parts": [{"text": "Your prompt here"}]
    }],
    "generationConfig": {
      "responseModalities": ["TEXT", "IMAGE"],
      "imageConfig": {
        "aspectRatio": "16:9",
        "imageSize": "2K"
      }
    }
  }'
```

### Image Editing (with Input Image)

```bash
# First, encode your image to base64
BASE64_IMAGE=$(base64 -w 0 input.png)

curl -s -X POST \
  "https://generativelanguage.googleapis.com/v1beta/models/gemini-3-pro-image-preview:generateContent" \
  -H "x-goog-api-key: $GEMINI_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{
    \"contents\": [{
      \"parts\": [
        {\"text\": \"Add a wizard hat to this cat\"},
        {\"inline_data\": {\"mime_type\": \"image/png\", \"data\": \"$BASE64_IMAGE\"}}
      ]
    }],
    \"generationConfig\": {
      \"responseModalities\": [\"TEXT\", \"IMAGE\"]
    }
  }"
```

### Multiple Reference Images (Character Consistency)

PRO supports up to 14 reference images (6 high-fidelity objects, 5 humans).

```bash
curl -s -X POST \
  "https://generativelanguage.googleapis.com/v1beta/models/gemini-3-pro-image-preview:generateContent" \
  -H "x-goog-api-key: $GEMINI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "contents": [{
      "parts": [
        {"text": "Create a group photo of these people in an office setting"},
        {"inline_data": {"mime_type": "image/png", "data": "BASE64_PERSON1"}},
        {"inline_data": {"mime_type": "image/png", "data": "BASE64_PERSON2"}},
        {"inline_data": {"mime_type": "image/png", "data": "BASE64_PERSON3"}}
      ]
    }],
    "generationConfig": {
      "responseModalities": ["TEXT", "IMAGE"],
      "imageConfig": {
        "aspectRatio": "16:9",
        "imageSize": "2K"
      }
    }
  }'
```

### Google Search Grounding (Real-Time Data)

```bash
curl -s -X POST \
  "https://generativelanguage.googleapis.com/v1beta/models/gemini-3-pro-image-preview:generateContent" \
  -H "x-goog-api-key: $GEMINI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "contents": [{
      "parts": [{"text": "Create an infographic of current S&P 500 performance"}]
    }],
    "tools": [{"google_search": {}}],
    "generationConfig": {
      "responseModalities": ["TEXT", "IMAGE"],
      "imageConfig": {"aspectRatio": "16:9"}
    }
  }'
```

### Multi-Turn Conversation (Iterative Editing)

```bash
curl -s -X POST \
  "https://generativelanguage.googleapis.com/v1beta/models/gemini-3-pro-image-preview:generateContent" \
  -H "x-goog-api-key: $GEMINI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "contents": [
      {
        "role": "user",
        "parts": [{"text": "Create an infographic about photosynthesis"}]
      },
      {
        "role": "model",
        "parts": [{"inline_data": {"mime_type": "image/png", "data": "PREVIOUS_IMAGE_BASE64"}}]
      },
      {
        "role": "user",
        "parts": [{"text": "Now translate all text to Spanish"}]
      }
    ],
    "generationConfig": {
      "responseModalities": ["TEXT", "IMAGE"]
    }
  }'
```

## Configuration Options

### imageConfig Parameters

| Parameter | Values | Default | Notes |
|-----------|--------|---------|-------|
| `aspectRatio` | `1:1`, `2:3`, `3:2`, `3:4`, `4:3`, `4:5`, `5:4`, `9:16`, `16:9`, `21:9` | `1:1` | Match your use case |
| `imageSize` | `1K`, `2K`, `4K` | `1K` | **Use uppercase K**. 4K only on PRO |

### responseModalities

Always include both for image generation:
```json
"responseModalities": ["TEXT", "IMAGE"]
```

### Supported MIME Types for Input

- `image/png`
- `image/jpeg`
- `image/gif`
- `image/webp`

## Response Format

### Success Response

```json
{
  "candidates": [{
    "content": {
      "parts": [
        {
          "text": "Here's the generated image..."
        },
        {
          "inlineData": {
            "mimeType": "image/png",
            "data": "BASE64_ENCODED_IMAGE_DATA"
          }
        }
      ]
    }
  }]
}
```

### With Search Grounding

Response includes `groundingMetadata`:
```json
{
  "candidates": [{
    "content": {...},
    "groundingMetadata": {
      "searchEntryPoint": {
        "renderedContent": "<html>...</html>"
      },
      "groundingChunks": [
        {"web": {"uri": "https://...", "title": "..."}}
      ]
    }
  }]
}
```

### Error Response

```json
{
  "error": {
    "code": 400,
    "message": "Invalid request",
    "status": "INVALID_ARGUMENT"
  }
}
```

## Extracting Image Data

### Using jq

```bash
# Extract base64 image data
cat response.json | jq -r '.candidates[0].content.parts[] | select(.inlineData) | .inlineData.data' | base64 -d > output.png

# Extract text response
cat response.json | jq -r '.candidates[0].content.parts[] | select(.text) | .text'
```

### One-liner Generation

```bash
curl -s -X POST "https://generativelanguage.googleapis.com/v1beta/models/gemini-3-pro-image-preview:generateContent" \
  -H "x-goog-api-key: $GEMINI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"contents":[{"parts":[{"text":"A cute robot reading a book"}]}],"generationConfig":{"responseModalities":["TEXT","IMAGE"]}}' \
  | jq -r '.candidates[0].content.parts[] | select(.inlineData) | .inlineData.data' \
  | base64 -d > robot.png
```

## Thinking Mode (PRO Only)

PRO uses reasoning for complex prompts. Thought images are generated internally (not charged) to refine composition.

Access thoughts in response:
```bash
# Check for thought parts
jq '.candidates[0].content.parts[] | select(.thought == true)' response.json
```

Thought signatures may be included for multi-turn context preservation. If present, pass them back in subsequent requests.

## Rate Limits & Pricing

- Check current limits at https://ai.google.dev/gemini-api/docs/rate-limits
- PRO costs more than Flash due to higher compute requirements
- Implement exponential backoff for retries
- Cache common prompts when possible

## Common Issues

### "model not found"
Use exact identifier: `gemini-3-pro-image-preview` or `gemini-2.5-flash-image`

### "invalid imageSize"
Use uppercase: `1K`, `2K`, `4K` (not `1k`, `2k`, `4k`)

### No image in response
- Check `responseModalities` includes `"IMAGE"`
- Verify prompt doesn't violate content policies
- Check for error in response

### Authentication failure
- Verify `GEMINI_API_KEY` is set correctly
- Check for trailing spaces in key
- Regenerate key if needed

## SynthID Watermark

All generated images include an invisible SynthID watermark for provenance tracking. This is embedded automatically and cannot be disabled.
