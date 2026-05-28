---
name: openrouter-gemini-image-generation
description: |
  Fix for OpenRouter image generation with Gemini/Nano Banana models returning 404 or 400 errors.
  Use when: (1) OpenRouter API returns 404 Not Found for image generation, (2) getting 400 Bad Request
  with "Invalid option" for aspect_ratio, (3) response parsing fails with "error decoding response body",
  (4) using /images/generations endpoint with Nano Banana or Gemini image models. The fix is to use
  /chat/completions endpoint with modalities parameter instead of the images endpoint.
author: Claude Code
version: 1.0.0
date: 2026-01-21
---

# OpenRouter Gemini Image Generation

## Problem
OpenRouter's Gemini image models (Nano Banana, Nano Banana Pro) don't work with the standard
`/images/generations` endpoint. Using this endpoint returns 404 errors, and even when the
endpoint seems correct, aspect ratio validation and response parsing can fail.

## Context / Trigger Conditions
- Error: `OpenRouter API error 404 Not Found` when calling `/api/v1/images/generations`
- Error: `400 Bad Request` with message about invalid aspect_ratio values
- Error: `Failed to parse response: error decoding response body`
- Using models: `google/gemini-3-pro-image-preview` (Nano Banana Pro) or `google/gemini-2.5-flash-image` (Nano Banana)

## Solution

### 1. Use Chat Completions Endpoint
Instead of `/api/v1/images/generations`, use `/api/v1/chat/completions`:

```rust
let response = client
    .post("https://openrouter.ai/api/v1/chat/completions")
    .header("Authorization", format!("Bearer {}", api_key))
    .header("Content-Type", "application/json")
    .json(&request)
    .send()
    .await?;
```

### 2. Include Modalities Parameter
The request must include `modalities: ["image", "text"]`:

```json
{
  "model": "google/gemini-3-pro-image-preview",
  "messages": [
    {"role": "user", "content": "Create a professional blog header image..."}
  ],
  "modalities": ["image", "text"],
  "image_config": {
    "aspect_ratio": "16:9"
  }
}
```

### 3. Use Valid Aspect Ratios Only
Valid values: `1:1`, `2:3`, `3:2`, `3:4`, `4:3`, `4:5`, `5:4`, `9:16`, `16:9`, `21:9`

**Invalid values that will cause 400 errors:**
- `1.91:1` (use `16:9` instead for social media images)
- Custom ratios like `1200x630` format

### 4. Parse Nested Response Structure
Images are nested in the response:

```json
{
  "choices": [{
    "message": {
      "role": "assistant",
      "content": "I've generated the image.",
      "images": [{
        "type": "image_url",
        "image_url": {
          "url": "data:image/png;base64,iVBORw0KGgo..."
        }
      }]
    }
  }]
}
```

Extract image bytes from: `choices[0].message.images[0].image_url.url`

## Verification
- API returns 200 status
- Response contains `choices[0].message.images` array with at least one image
- Image URL starts with `data:image/png;base64,` (or similar)
- After base64 decoding, bytes represent valid image data

## Example

```rust
// Request structure
#[derive(Serialize)]
struct ChatCompletionsRequest {
    model: String,
    messages: Vec<ChatMessage>,
    modalities: Vec<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    image_config: Option<ImageConfig>,
}

#[derive(Serialize)]
struct ImageConfig {
    aspect_ratio: String,
}

// Response structure
#[derive(Deserialize)]
struct ChatCompletionsResponse {
    choices: Vec<ChatChoice>,
}

#[derive(Deserialize)]
struct ChatChoice {
    message: AssistantMessage,
}

#[derive(Deserialize)]
struct AssistantMessage {
    #[serde(default)]
    images: Vec<ImageObject>,
}

#[derive(Deserialize)]
struct ImageObject {
    image_url: ImageUrlData,
}

#[derive(Deserialize)]
struct ImageUrlData {
    url: String,  // "data:image/png;base64,..."
}

// Usage
let request = ChatCompletionsRequest {
    model: "google/gemini-3-pro-image-preview".to_string(),
    messages: vec![ChatMessage {
        role: "user".to_string(),
        content: prompt.to_string(),
    }],
    modalities: vec!["image".to_string(), "text".to_string()],
    image_config: Some(ImageConfig {
        aspect_ratio: "16:9".to_string(),
    }),
};
```

## Notes
- Nano Banana Pro (`google/gemini-3-pro-image-preview`) is paid ($2/M input, $12/M output tokens)
- Nano Banana (`google/gemini-2.5-flash-image`) is cheaper ($0.30/M input, $2.50/M output tokens)
- Image generation can take 20-30+ seconds
- The `content` field in the response may contain descriptive text about the generated image

## References
- [OpenRouter Image Generation Docs](https://openrouter.ai/docs/guides/overview/multimodal/image-generation)
- [Nano Banana Pro Model Page](https://openrouter.ai/google/gemini-3-pro-image-preview)
- [Nano Banana Model Page](https://openrouter.ai/google/gemini-2.5-flash-image)
