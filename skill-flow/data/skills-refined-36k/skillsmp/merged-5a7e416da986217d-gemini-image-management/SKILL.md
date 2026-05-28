---
name: gemini-image-management
description: Use this skill when you need to generate or edit images based on text prompts using fal.ai Gemini 3 Pro.
---

# Gemini Image Management

Generate high-quality images or edit existing images using text prompts with Google's Gemini 3 Pro model via fal.ai.

## Prerequisites

- `FAL_KEY` environment variable must be set (typically in `~/.zshrc`)

## API Endpoints

- **Image Generation**: `POST https://fal.run/fal-ai/gemini-3-pro-image-preview`
- **Image Editing**: `POST https://fal.run/fal-ai/gemini-3-pro-image-preview/edit`

## Image Generation Parameters

### Required
- `prompt` (string): The text description of the image to generate

### Optional
| Parameter | Type | Default | Options |
|-----------|------|---------|---------|
| `num_images` | integer | 1 | 1-4 |
| `aspect_ratio` | string | "1:1" | "21:9", "16:9", "3:2", "4:3", "5:4", "1:1", "4:5", "3:4", "2:3", "9:16" |
| `output_format` | string | "png" | "jpeg", "png", "webp" |
| `resolution` | string | "1K" | "1K", "2K", "4K" |
| `sync_mode` | boolean | false | Returns data URI when true |
| `enable_web_search` | boolean | false | Uses current web data for generation |
| `limit_generations` | boolean | false | Restricts to 1 image per prompt round |

## Image Editing Parameters

### Required
- `prompt` (string): The editing instruction describing what changes to make
- `image_urls` (array of strings): URLs of the images to edit

### Optional
| Parameter | Type | Default | Options |
|-----------|------|---------|---------|
| `num_images` | integer | 1 | 1-4 |
| `aspect_ratio` | string | "auto" | "auto", "21:9", "16:9", "3:2", "4:3", "5:4", "1:1", "4:5", "3:4", "2:3", "9:16" |
| `output_format` | string | "png" | "jpeg", "png", "webp" |
| `resolution` | string | "1K" | "1K", "2K", "4K" |
| `sync_mode` | boolean | false | Returns data URI when true |
| `enable_web_search` | boolean | false | Uses current web data for generation |
| `limit_generations` | boolean | false | Restricts to 1 image per prompt round |

## Usage

### Image Generation Example

#### cURL
```bash
curl --request POST \
  --url https://fal.run/fal-ai/gemini-3-pro-image-preview \
  --header "Authorization: Key $FAL_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "prompt": "A serene mountain landscape at sunset with golden light",
    "num_images": 1,
    "aspect_ratio": "16:9",
    "resolution": "2K",
    "output_format": "png"
  }'
```

### Image Editing Example

#### cURL
```bash
curl --request POST \
  --url https://fal.run/fal-ai/gemini-3-pro-image-preview/edit \
  --header "Authorization: Key $FAL_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "prompt": "Add snow to this mountain scene and make it winter",
    "image_urls": ["https://example.com/mountain.jpg"],
    "num_images": 1,
    "output_format": "png"
  }'
```

## Response Format

Both image generation and editing return a similar response format:

```json
{
  "images": [
    {
      "file_name": "generated_image.png",
      "content_type": "image/png",
      "url": "https://storage.googleapis.com/..."
    }
  ],
  "description": "A description of the generated or edited image"
}
```

## Examples

### Image Generation
1. **Simple image generation**:
   - Prompt: "Generate an image of a futuristic city at night"

2. **Specific aspect ratio**:
   - Prompt: "Create a portrait-oriented image of a forest path" with `aspect_ratio: "9:16"`

3. **High resolution**:
   - Prompt: "Generate a detailed 4K image of a coral reef" with `resolution: "4K"`

### Image Editing
1. **Style transformation**:
   - Prompt: "Convert this photo to a watercolor painting style"

2. **Object addition**:
   - Prompt: "Add a rainbow in the sky"

3. **Scene modification**:
   - Prompt: "Change the time of day to sunset with golden hour lighting"

4. **Multiple reference images**:
   - Prompt: "Combine elements from these images into a cohesive scene" with multiple URLs in `image_urls` array

## Tips

- Be specific in your prompts for better results.
- Include lighting, mood, and style descriptors.
- Use appropriate aspect ratios for your use case (16:9 for landscapes, 9:16 for portraits).
- Higher resolution takes longer to generate.
- For editing, be descriptive about what changes you want and provide multiple images for context if needed.

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| `401 Unauthorized` | Invalid FAL_KEY | Verify key at fal.ai dashboard |
| `429 Too Many Requests` | Rate limit exceeded | Wait 60 seconds, retry |
| `400 Bad Request` | Invalid parameters or image URLs | Check aspect_ratio, resolution values, and ensure image URLs are accessible |
| `500 Server Error` | API temporary issue | Retry after 30 seconds |
| `Timeout` | Generation taking too long | Reduce resolution or simplify prompt |