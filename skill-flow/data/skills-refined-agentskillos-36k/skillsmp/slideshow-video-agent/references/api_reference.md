# fal.ai API Reference

All services are accessed through a single fal.ai API key.

## Authentication

Set your API key in the environment:
```python
import os
os.environ["FAL_KEY"] = "your-api-key"
```

Or in `.env` file:
```
FAL_KEY=your-api-key
```

## Services

### Nano Banana Pro (Text-to-Image)

**Model ID:** `fal-ai/nano-banana-pro`

Generates slide images from text prompts only.

```python
import fal_client

result = fal_client.subscribe(
    "fal-ai/nano-banana-pro",
    arguments={
        "prompt": "Professional presentation slide titled 'Welcome'",
        "num_images": 1,
        "aspect_ratio": "16:9",
        "output_format": "png"
    }
)

image_url = result["images"][0]["url"]
```

**Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| prompt | string | Text description of desired image |
| num_images | int | Number of images to generate (default: 1) |
| aspect_ratio | string | "16:9", "1:1", "9:16", etc. |
| output_format | string | "png" or "jpeg" |

### Nano Banana Pro Edit (Image + Text)

**Model ID:** `fal-ai/nano-banana-pro/edit`

Generates images using reference images for style/brand consistency.

```python
result = fal_client.subscribe(
    "fal-ai/nano-banana-pro/edit",
    arguments={
        "prompt": "Professional slide matching brand style",
        "image_urls": [
            "https://fal.ai/uploaded/logo.png",
            "https://fal.ai/uploaded/colors.png"
        ],
        "num_images": 1,
        "aspect_ratio": "16:9",
        "output_format": "png"
    }
)
```

**Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| prompt | string | Text description |
| image_urls | list[string] | URLs of reference images |
| num_images | int | Number of images to generate |
| aspect_ratio | string | Output aspect ratio |
| output_format | string | "png" or "jpeg" |

### Eleven Labs v3 (Text-to-Speech)

**Model ID:** `fal-ai/elevenlabs/tts/eleven-v3`

Generates voiceover audio from text.

```python
result = fal_client.subscribe(
    "fal-ai/elevenlabs/tts/eleven-v3",
    arguments={
        "text": "Welcome to our presentation.",
        "voice": "George",
        "speed": 1.0,
        "output_format": "mp3_44100_128"
    }
)

audio_url = result["audio"]["url"]
```

**Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| text | string | Text to convert to speech |
| voice | string | Voice name (George, Aria, Rachel, Sam, Charlie, Emily) |
| speed | float | Speech speed (default: 1.0) |
| output_format | string | "mp3_44100_128" recommended |

### Kling 2.6 Pro (Image-to-Video)

**Model ID:** `fal-ai/kling-video/v2.6/pro/image-to-video`

Generates animated video from a static image.

```python
# First upload the image
image_url = fal_client.upload(image_bytes, "image/png")

result = fal_client.subscribe(
    "fal-ai/kling-video/v2.6/pro/image-to-video",
    arguments={
        "prompt": "Cinematic dissolve with particles",
        "image_url": image_url,
        "duration": "5",
        "aspect_ratio": "16:9",
        "cfg_scale": 0.5,
        "generate_audio": False,
        "negative_prompt": "static, frozen, still image"
    }
)

video_url = result["video"]["url"]
```

**Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| prompt | string | Description of motion/animation |
| image_url | string | URL of source image |
| duration | string | "5" or "10" seconds |
| aspect_ratio | string | "16:9", "1:1", "9:16" |
| cfg_scale | float | Guidance scale (0.0-1.0) |
| generate_audio | bool | Whether to generate audio |
| negative_prompt | string | What to avoid |

## Uploading Files

Use `fal_client.upload()` to upload local files:

```python
with open("image.png", "rb") as f:
    url = fal_client.upload(f.read(), "image/png")
```

MIME types:
- `image/png` - PNG images
- `image/jpeg` - JPEG images
- `image/webp` - WebP images

## Error Handling

API calls may fail due to rate limits or server issues. Use retry logic:

```python
from scripts.utils import api_call_with_retry

def my_api_call():
    return fal_client.subscribe(...)

result = api_call_with_retry(my_api_call, max_retries=3)
```

## Pricing

| Service | Cost |
|---------|------|
| Nano Banana Pro | $0.15/image |
| Nano Banana Pro Edit | $0.15/image |
| Eleven Labs v3 | ~$0.30/1000 chars |
| Kling 2.6 Pro | $0.35/5s video |

Get your API key at: https://fal.ai/dashboard/keys
