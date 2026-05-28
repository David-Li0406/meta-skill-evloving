---
name: gemini-image
description: Use this skill when you want to generate new images from text prompts or edit existing images based on text descriptions using fal.ai Gemini 3 Pro.
---

# Gemini Image Generation and Editing

Generate high-quality images from text prompts or edit existing images using Google's Gemini 3 Pro model via fal.ai.

## Prerequisites

- `FAL_KEY` environment variable must be set (typically in `~/.zshrc`)

## API Endpoints

- **Image Generation**: `POST https://fal.run/fal-ai/gemini-3-pro-image-preview`
- **Image Editing**: `POST https://fal.run/fal-ai/gemini-3-pro-image-preview/edit`

## Parameters

### For Image Generation
#### Required
- `prompt` (string): The text description of the image to generate

#### Optional
| Parameter | Type | Default | Options |
|-----------|------|---------|---------|
| `num_images` | integer | 1 | 1-4 |
| `aspect_ratio` | string | "1:1" | "21:9", "16:9", "3:2", "4:3", "5:4", "1:1", "4:5", "3:4", "2:3", "9:16" |
| `output_format` | string | "png" | "jpeg", "png", "webp" |
| `resolution` | string | "1K" | "1K", "2K", "4K" |
| `sync_mode` | boolean | false | Returns data URI when true |
| `enable_web_search` | boolean | false | Uses current web data for generation |
| `limit_generations` | boolean | false | Restricts to 1 image per prompt round |

### For Image Editing
#### Required
- `prompt` (string): The editing instruction describing what changes to make
- `image_urls` (array of strings): URLs of the images to edit

#### Optional
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

#### Python
```python
import fal_client

result = fal_client.subscribe(
    "fal-ai/gemini-3-pro-image-preview",
    arguments={
        "prompt": "A serene mountain landscape at sunset with golden light",
        "num_images": 1,
        "aspect_ratio": "16:9",
        "resolution": "2K"
    }
)

# Access the generated image URL
image_url = result["images"][0]["url"]
print(f"Generated image: {image_url}")
```

#### JavaScript
```javascript
import { fal } from "@fal-ai/client";

const result = await fal.subscribe("fal-ai/gemini-3-pro-image-preview", {
  input: {
    prompt: "A serene mountain landscape at sunset with golden light",
    num_images: 1,
    aspect_ratio: "16:9",
    resolution: "2K"
  }
});

console.log("Generated image:", result.images[0].url);
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

#### Python
```python
import fal_client

result = fal_client.subscribe(
    "fal-ai/gemini-3-pro-image-preview/edit",
    arguments={
        "prompt": "Add snow to this mountain scene and make it winter",
        "image_urls": ["https://example.com/mountain.jpg"],
        "num_images": 1
    }
)

# Access the edited image URL
edited_url = result["images"][0]["url"]
print(f"Edited image: {edited_url}")
```

#### JavaScript
```javascript
import { fal } from "@fal-ai/client";

const result = await fal.subscribe("fal-ai/gemini-3-pro-image-preview/edit", {
  input: {
    prompt: "Add snow to this mountain scene and make it winter",
    image_urls: ["https://example.com/mountain.jpg"],
    num_images: 1
  }
});

console.log("Edited image:", result.images[0].url);
```

## Response Format

For both image generation and editing, the response will be in the following format:
```json
{
  "images": [
    {
      "file_name": "generated_image.png",
      "url": "https://example.com/generated_image.png"
    }
  ]
}
```