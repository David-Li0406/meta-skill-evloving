---
name: gemini
description: Use Google Gemini API for text generation, multimodal analysis, image generation (Nano Banana), function calling, and search grounding. Invoke when user wants to use Gemini, ask Gemini, generate images with Gemini, or analyze content with Gemini.
trigger_keywords:
  - use gemini
  - ask gemini
  - gemini chat
  - gemini generate
  - gemini analyze
  - gemini image
  - nano banana
  - gemini function
  - gemini search
---

# Gemini API

Use Google Gemini API via REST for text generation, multimodal analysis, image generation, and more.

## Prerequisites

- Environment variable `GOOGLE_API_KEY` must be set
- API endpoint: `https://generativelanguage.googleapis.com/v1beta`

## Available Models

| Model | Use Case |
|-------|----------|
| `gemini-2.5-flash` | Fast text generation (default) |
| `gemini-2.5-pro` | High quality text generation |
| `gemini-3-flash-preview` | Latest flash model |
| `gemini-3-pro-preview` | Latest pro model |
| `gemini-2.5-flash-image` | Image generation (Nano Banana) |
| `gemini-3-pro-image-preview` | Advanced image generation with thinking & search |

## Workflow

### Phase 1: Determine Task Type

Based on user request, identify which capability to use:
- **Text Generation**: Basic prompts, chat, Q&A
- **Multimodal Analysis**: Analyze images, videos, or audio
- **Image Generation**: Create or edit images (Nano Banana)
- **Function Calling**: Execute custom functions
- **Search Grounding**: Real-time web search integration

### Phase 2: Execute API Call

Use the appropriate curl command based on task type.

---

## 1. Text Generation

### Basic Prompt

```bash
curl "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=$GOOGLE_API_KEY" \
    -H 'Content-Type: application/json' \
    -X POST \
    -d '{
      "contents": [{
        "parts": [{"text": "Your prompt here"}]
      }]
    }'
```

### With Configuration

```bash
curl "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=$GOOGLE_API_KEY" \
    -H 'Content-Type: application/json' \
    -X POST \
    -d '{
      "contents": [{
        "parts": [{"text": "Your prompt here"}]
      }],
      "generationConfig": {
        "temperature": 0.9,
        "maxOutputTokens": 2000,
        "stopSequences": ["END"]
      }
    }'
```

### Multi-turn Chat

```bash
curl "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=$GOOGLE_API_KEY" \
    -H 'Content-Type: application/json' \
    -X POST \
    -d '{
      "contents": [
        {"role": "user", "parts": [{"text": "First message"}]},
        {"role": "model", "parts": [{"text": "Model response"}]},
        {"role": "user", "parts": [{"text": "Follow-up question"}]}
      ]
    }'
```

### System Instructions

```bash
curl "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=$GOOGLE_API_KEY" \
    -H 'Content-Type: application/json' \
    -X POST \
    -d '{
      "system_instruction": {
        "parts": [{"text": "You are a helpful assistant that speaks like a pirate."}]
      },
      "contents": [{
        "parts": [{"text": "Hello!"}]
      }]
    }'
```

### JSON Mode Output

```bash
curl "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=$GOOGLE_API_KEY" \
    -H 'Content-Type: application/json' \
    -X POST \
    -d '{
      "contents": [{
        "parts": [{"text": "List 3 colors as JSON array"}]
      }],
      "generationConfig": {
        "response_mime_type": "application/json"
      }
    }'
```

### Streaming Response

```bash
curl "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:streamGenerateContent?alt=sse&key=$GOOGLE_API_KEY" \
    -H 'Content-Type: application/json' \
    -X POST \
    -d '{
      "contents": [{
        "parts": [{"text": "Write a long story"}]
      }]
    }'
```

### Safety Settings

```bash
curl "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=$GOOGLE_API_KEY" \
    -H 'Content-Type: application/json' \
    -X POST \
    -d '{
      "contents": [{
        "parts": [{"text": "Your prompt"}]
      }],
      "safetySettings": [
        {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_ONLY_HIGH"},
        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_ONLY_HIGH"}
      ]
    }'
```

---

## 2. Multimodal Analysis

### Image Analysis (Base64 Inline)

```bash
# First encode image to base64
BASE64_IMAGE=$(base64 -w0 image.jpg)

curl "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=$GOOGLE_API_KEY" \
    -H 'Content-Type: application/json' \
    -X POST \
    -d '{
      "contents": [{
        "parts": [
          {"text": "Describe this image in detail"},
          {"inline_data": {"mime_type": "image/jpeg", "data": "'$BASE64_IMAGE'"}}
        ]
      }]
    }'
```

### Video Analysis (File API)

#### Step 1: Upload Video

```bash
# Get upload URL
UPLOAD_URL=$(curl -s "https://generativelanguage.googleapis.com/upload/v1beta/files?key=$GOOGLE_API_KEY" \
    -H "X-Goog-Upload-Protocol: resumable" \
    -H "X-Goog-Upload-Command: start" \
    -H "X-Goog-Upload-Header-Content-Length: $(stat -f%z video.mp4)" \
    -H "X-Goog-Upload-Header-Content-Type: video/mp4" \
    -H "Content-Type: application/json" \
    -d '{"file": {"display_name": "video.mp4"}}' \
    -D - | grep -i "x-goog-upload-url" | cut -d' ' -f2 | tr -d '\r')

# Upload file
curl "$UPLOAD_URL" \
    -H "X-Goog-Upload-Offset: 0" \
    -H "X-Goog-Upload-Command: upload, finalize" \
    -H "Content-Type: video/mp4" \
    --data-binary @video.mp4
```

#### Step 2: Query with Video

```bash
curl "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=$GOOGLE_API_KEY" \
    -H 'Content-Type: application/json' \
    -X POST \
    -d '{
      "contents": [{
        "parts": [
          {"text": "Describe what happens in this video"},
          {"file_data": {"mime_type": "video/mp4", "file_uri": "FILE_URI_FROM_UPLOAD"}}
        ]
      }]
    }'
```

### Audio Analysis

Similar to video, upload via File API then query:

```bash
curl "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=$GOOGLE_API_KEY" \
    -H 'Content-Type: application/json' \
    -X POST \
    -d '{
      "contents": [{
        "parts": [
          {"text": "Transcribe and summarize this audio"},
          {"file_data": {"mime_type": "audio/mp3", "file_uri": "FILE_URI_FROM_UPLOAD"}}
        ]
      }]
    }'
```

---

## 3. Image Generation (Nano Banana)

### Basic Image Generation

```bash
curl "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-image:generateContent?key=$GOOGLE_API_KEY" \
    -H 'Content-Type: application/json' \
    -X POST \
    -d '{
      "contents": [{"parts": [{"text": "Create a photorealistic image of a cat wearing a hat"}]}],
      "generationConfig": {
        "responseModalities": ["TEXT", "IMAGE"]
      }
    }'
```

### With Aspect Ratio Control

Supported ratios: `1:1`, `2:3`, `3:2`, `3:4`, `4:3`, `4:5`, `5:4`, `9:16`, `16:9`, `21:9`

```bash
curl "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-image:generateContent?key=$GOOGLE_API_KEY" \
    -H 'Content-Type: application/json' \
    -X POST \
    -d '{
      "contents": [{"parts": [{"text": "Create a landscape scene"}]}],
      "generationConfig": {
        "responseModalities": ["IMAGE"],
        "imageConfig": {
          "aspectRatio": "16:9"
        }
      }
    }'
```

### Image Editing (Character Consistency)

```bash
BASE64_IMAGE=$(base64 -w0 original.jpg)

curl "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-image:generateContent?key=$GOOGLE_API_KEY" \
    -H 'Content-Type: application/json' \
    -X POST \
    -d '{
      "contents": [{
        "parts": [
          {"text": "Put this character in a tropical forest"},
          {"inline_data": {"mime_type": "image/jpeg", "data": "'$BASE64_IMAGE'"}}
        ]
      }],
      "generationConfig": {
        "responseModalities": ["TEXT", "IMAGE"]
      }
    }'
```

### High Resolution (Pro Model - 2K/4K)

```bash
curl "https://generativelanguage.googleapis.com/v1beta/models/gemini-3-pro-image-preview:generateContent?key=$GOOGLE_API_KEY" \
    -H 'Content-Type: application/json' \
    -X POST \
    -d '{
      "contents": [{"parts": [{"text": "A photo of an oak tree in all four seasons"}]}],
      "generationConfig": {
        "responseModalities": ["TEXT", "IMAGE"],
        "imageConfig": {
          "aspectRatio": "1:1",
          "imageSize": "4K"
        }
      }
    }'
```

### Image Generation with Search Grounding (Pro)

```bash
curl "https://generativelanguage.googleapis.com/v1beta/models/gemini-3-pro-image-preview:generateContent?key=$GOOGLE_API_KEY" \
    -H 'Content-Type: application/json' \
    -X POST \
    -d '{
      "contents": [{"parts": [{"text": "Visualize the current weather forecast for Tokyo as a chart"}]}],
      "generationConfig": {
        "responseModalities": ["TEXT", "IMAGE"],
        "imageConfig": {
          "aspectRatio": "16:9"
        }
      },
      "tools": [{"google_search": {}}]
    }'
```

### Multi-Image Fusion

```bash
BASE64_IMG1=$(base64 -w0 image1.jpg)
BASE64_IMG2=$(base64 -w0 image2.jpg)

curl "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-image:generateContent?key=$GOOGLE_API_KEY" \
    -H 'Content-Type: application/json' \
    -X POST \
    -d '{
      "contents": [{
        "parts": [
          {"text": "Combine these two characters in a fantasy world"},
          {"inline_data": {"mime_type": "image/jpeg", "data": "'$BASE64_IMG1'"}},
          {"inline_data": {"mime_type": "image/jpeg", "data": "'$BASE64_IMG2'"}}
        ]
      }],
      "generationConfig": {
        "responseModalities": ["TEXT", "IMAGE"]
      }
    }'
```

---

## 4. Function Calling

### Define and Call Functions

```bash
curl "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=$GOOGLE_API_KEY" \
    -H 'Content-Type: application/json' \
    -X POST \
    -d '{
      "contents": [{
        "role": "user",
        "parts": [{"text": "What movies are playing in Mountain View?"}]
      }],
      "tools": [{
        "function_declarations": [{
          "name": "find_movies",
          "description": "Find movies playing in theaters",
          "parameters": {
            "type": "object",
            "properties": {
              "location": {"type": "string", "description": "City and state"},
              "genre": {"type": "string", "description": "Movie genre"}
            },
            "required": ["location"]
          }
        }]
      }]
    }'
```

### Provide Function Response

```bash
curl "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=$GOOGLE_API_KEY" \
    -H 'Content-Type: application/json' \
    -X POST \
    -d '{
      "contents": [
        {"role": "user", "parts": [{"text": "What movies are playing in Mountain View?"}]},
        {"role": "model", "parts": [{"functionCall": {"name": "find_movies", "args": {"location": "Mountain View, CA"}}}]},
        {"role": "function", "parts": [{"functionResponse": {"name": "find_movies", "response": {"movies": ["Barbie", "Oppenheimer"]}}}]}
      ],
      "tools": [{
        "function_declarations": [{
          "name": "find_movies",
          "description": "Find movies playing in theaters",
          "parameters": {
            "type": "object",
            "properties": {
              "location": {"type": "string"},
              "genre": {"type": "string"}
            },
            "required": ["location"]
          }
        }]
      }]
    }'
```

---

## 5. Search Grounding

Real-time web search integration:

```bash
curl "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=$GOOGLE_API_KEY" \
    -H 'Content-Type: application/json' \
    -X POST \
    -d '{
      "contents": [{"parts": [{"text": "What is the current Google stock price?"}]}],
      "tools": [{"google_search": {}}]
    }'
```

Response includes `groundingMetadata` with sources.

---

## 6. Context Caching

For repeated queries on the same large content:

### Create Cache

```bash
curl "https://generativelanguage.googleapis.com/v1beta/cachedContents?key=$GOOGLE_API_KEY" \
    -H 'Content-Type: application/json' \
    -X POST \
    -d '{
      "model": "models/gemini-2.5-flash",
      "contents": [{"parts": [{"text": "LARGE_DOCUMENT_TEXT_HERE"}]}],
      "ttl": "3600s"
    }'
```

### Use Cache

```bash
curl "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=$GOOGLE_API_KEY" \
    -H 'Content-Type: application/json' \
    -X POST \
    -d '{
      "cachedContent": "cachedContents/CACHE_ID",
      "contents": [{"parts": [{"text": "Summarize the document"}]}]
    }'
```

---

## 7. Model Information

### List All Models

```bash
curl "https://generativelanguage.googleapis.com/v1beta/models?key=$GOOGLE_API_KEY"
```

### Get Specific Model

```bash
curl "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash?key=$GOOGLE_API_KEY"
```

---

## Response Handling

### Text Response Structure

```json
{
  "candidates": [{
    "content": {
      "parts": [{"text": "Response text here"}],
      "role": "model"
    },
    "finishReason": "STOP"
  }],
  "usageMetadata": {
    "promptTokenCount": 10,
    "candidatesTokenCount": 50,
    "totalTokenCount": 60
  }
}
```

### Image Response Structure

When using image generation, response includes base64-encoded images:

```json
{
  "candidates": [{
    "content": {
      "parts": [
        {"text": "Here is your image:"},
        {"inlineData": {"mimeType": "image/png", "data": "BASE64_IMAGE_DATA"}}
      ]
    }
  }]
}
```

To save the image:

```bash
# Extract and decode image from response
echo "BASE64_DATA" | base64 -d > output.png
```

---

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| 400 | Invalid request | Check JSON syntax |
| 401 | Invalid API key | Verify GOOGLE_API_KEY |
| 429 | Rate limit | Wait and retry |
| 500 | Server error | Retry with exponential backoff |

---

## Best Practices

1. **Use appropriate model**: Flash for speed, Pro for quality
2. **Set temperature**: Lower (0.1-0.3) for factual, higher (0.7-1.0) for creative
3. **Limit output tokens**: Set `maxOutputTokens` to avoid excessive responses
4. **Use caching**: For repeated queries on large documents
5. **Handle streaming**: For long responses, use `streamGenerateContent`
6. **Image generation tips**: Use detailed, descriptive prompts for best results
