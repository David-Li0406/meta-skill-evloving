---
name: world-labs-image-generation
description: Use this skill to generate 3D worlds from single or multiple images, with options for direction control and auto layout.
---

# World Labs Image Generation

Generate immersive 3D worlds from single or multiple reference images. This skill supports both single image inputs and multi-image configurations with precise directional control or automatic layout.

## Quick Reference

| Input Type         | Max Images | Overlap                   | Best For                           |
| ------------------ | ---------- | ------------------------- | ---------------------------------- |
| **Single Image**   | 1          | N/A                       | Extrapolating a scene from one image |
| **Multi-Image**    | Up to 8    | Required (Auto Layout)    | Creative connections or reconstructing spaces |

### Credits

| Model           | Credits |
| --------------- | ------- |
| Marble 0.1-plus | 1,600   |
| Marble 0.1-mini | 250     |

## Single Image Input

### Requirements

- **Recommended resolution**: 1024px on the long side
- **Maximum file size**: 20 MB
- **Formats**: PNG (recommended), JPG, WebP
- **Aspect ratio**: 16:9, 9:16, or anything in between

### Best Practices

#### DO

✅ **Clear spatial definition**: Images with obvious depth and perspective  
✅ **Wide shots**: Show foreground, midground, and background  
✅ **Visible ground/floor**: Helps establish world orientation  
✅ **Consistent lighting**: Clear, well-lit scenes  
✅ **Environmental scenes**: Landscapes, interiors, architectural spaces  

#### DON'T

❌ **Close-up shots**: Lack spatial context for 3D reconstruction  
❌ **People or animals**: As main subjects (may cause artifacts)  
❌ **Abstract images**: Non-representational art  
❌ **Borders or frames**: Decorative edges, watermarks  
❌ **Heavy text overlays**: Text doesn't render clearly  
❌ **Flat graphics**: 2D illustrations without depth  
❌ **Blurry or low-contrast images**: Reduces detail inference  

## Multi-Image Input

### Direction Control Mode

Use when you want explicit control over image placement. **Non-overlapping images** are preferred—the model creatively fills spaces between views.

#### Azimuth Angles

| Azimuth | Direction | Description                         |
| ------- | --------- | ----------------------------------- |
| `0`     | Front     | Primary view, camera facing forward |
| `90`    | Right     | View from right side                |
| `180`   | Back      | Opposite of front view              |
| `270`   | Left      | View from left side                 |

### Auto Layout Mode

Use when you have multiple overlapping images from the same space. The model automatically positions images.

#### Requirements for Auto Layout

| Requirement  | Details                                         |
| ------------ | ----------------------------------------------- |
| Aspect ratio | **All images MUST have identical aspect ratio** |
| Resolution   | **All images MUST have identical resolution**   |
| Location     | All images from the same space                  |
| Overlap      | Visual overlap between images required          |
| Lighting     | Consistent lighting and color temperature       |

## API Usage

### Single Image

```json
{
  "model": "Marble 0.1-plus",
  "world_prompt": {
    "type": "image",
    "image_prompt": {
      "source": "media_asset",
      "media_asset_id": "<media_asset_id>"
    },
    "text_prompt": "<optional_description>"
  }
}
```

### Multi-Image (Direction Control)

```json
{
  "model": "Marble 0.1-plus",
  "world_prompt": {
    "type": "multi-image",
    "multi_image_prompt": [
      {
        "azimuth": 0,
        "content": {
          "source": "media_asset",
          "media_asset_id": "<front_image_id>"
        }
      },
      {
        "azimuth": 90,
        "content": {
          "source": "media_asset",
          "media_asset_id": "<right_image_id>"
        }
      },
      {
        "azimuth": 180,
        "content": {
          "source": "media_asset",
          "media_asset_id": "<back_image_id>"
        }
      },
      {
        "azimuth": 270,
        "content": {
          "source": "media_asset",
          "media_asset_id": "<left_image_id>"
        }
      }
    ],
    "text_prompt": "<scene_description>"
  }
}
```

### Multi-Image (Auto Layout)

```json
{
  "model": "Marble 0.1-plus",
  "world_prompt": {
    "type": "multi-image",
    "multi_image_prompt": [
      {
        "content": {
          "source": "media_asset",
          "media_asset_id": "<image_1_id>"
        }
      },
      {
        "content": {
          "source": "media_asset",
          "media_asset_id": "<image_2_id>"
        }
      },
      {
        "content": {
          "source": "media_asset",
          "media_asset_id": "<image_3_id>"
        }
      }
    ],
    "text_prompt": "<scene_description>"
  }
}
```

## Python Example

```python
import requests

def generate_world(api_key: str, images: list[dict], prompt: str = None, is_pano: bool = False):
    base_url = "https://api.worldlabs.ai/marble/v1"
    headers = {"WLT-Api-Key": api_key, "Content-Type": "application/json"}

    # Prepare multi-image prompt
    multi_image_prompt = []
    for img in images:
        image_entry = {
            "content": {
                "source": "media_asset",
                "media_asset_id": img["media_asset_id"]
            }
        }
        if "azimuth" in img:
            image_entry["azimuth"] = img["azimuth"]
        multi_image_prompt.append(image_entry)

    # Build world prompt
    world_prompt = {
        "type": "multi-image",
        "multi_image_prompt": multi_image_prompt
    }
    if prompt:
        world_prompt["text_prompt"] = prompt

    # Generate world
    response = requests.post(
        f"{base_url}/worlds:generate",
        headers=headers,
        json={"model": "Marble 0.1-plus", "world_prompt": world_prompt}
    )

    return response.json()["operation_id"]
```

## Troubleshooting

| Issue               | Cause                   | Solution                                    |
| ------------------- | ----------------------- | ------------------------------------------- |
| Seams between views | Inconsistent lighting   | Match exposure and white balance            |
| Floating objects    | Conflicting depth info  | Use more consistent reference images        |
| Distorted geometry  | Images too different    | Use more similar reference images           |
| Auto layout fails   | Different aspect ratios | Ensure all images have identical dimensions |

## Related Skills

- `world-labs-api` - API integration details
- `world-labs-text-prompt` - Text prompting best practices
- `world-labs-pano-video` - Panorama and video input