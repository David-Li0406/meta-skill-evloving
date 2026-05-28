---
name: world-labs-image-generation
description: Use this skill to generate immersive 3D worlds from one or multiple reference images, with options for directional control or automatic layout.
---

# Skill body

## Overview

Generate 3D worlds from one or multiple reference images. This skill allows for precise directional control of image placement or automatic layout for reconstructing existing spaces.

## Modes

### 1. Single Image Input

Use this mode when you have a single reference image. The model extrapolates the scene to create an immersive 360° environment.

#### Requirements

| Requirement            | Specification                      |
| ---------------------- | ---------------------------------- |
| Recommended resolution | 1024px on long side                |
| Maximum file size      | 20 MB                              |
| Formats                | PNG (recommended), JPG, WebP       |
| Aspect ratio           | 16:9, 9:16, or anything in between |

#### Best Practices

**DO:**
- Use clear spatial definitions with depth and perspective.
- Provide wide shots showing foreground, midground, and background.
- Ensure visible ground/floor for world orientation.
- Maintain consistent lighting in well-lit scenes.

**DON'T:**
- Avoid close-up shots, people or animals as main subjects, abstract images, and blurry or low-contrast images.

#### API Usage

```json
{
  "model": "Marble 0.1-plus",
  "world_prompt": {
    "type": "single-image",
    "image": {
      "source": "media_asset",
      "media_asset_id": "image_id"
    }
  }
}
```

### 2. Multi-Image Input

Use this mode when you have multiple reference images. This allows for explicit control over image placement or automatic layout.

#### Direction Control Mode

Use when you want explicit control over image placement. Non-overlapping images are preferred.

#### Azimuth Angles

| Azimuth | Direction | Description                         |
| ------- | --------- | ----------------------------------- |
| `0`     | Front     | Primary view, camera facing forward |
| `90`    | Right     | View from right side                |
| `180`   | Back      | Opposite of front view              |
| `270`   | Left      | View from left side                 |

#### API Usage

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
          "media_asset_id": "front_image_id"
        }
      },
      {
        "azimuth": 90,
        "content": {
          "source": "media_asset",
          "media_asset_id": "right_image_id"
        }
      },
      {
        "azimuth": 180,
        "content": {
          "source": "media_asset",
          "media_asset_id": "back_image_id"
        }
      },
      {
        "azimuth": 270,
        "content": {
          "source": "media_asset",
          "media_asset_id": "left_image_id"
        }
      }
    ],
    "text_prompt": "A grand Victorian mansion interior"
  }
}
```

## Credits

| Model           | Credits |
| --------------- | ------- |
| Marble 0.1-plus | 1,600   |
| Marble 0.1-mini | 250     |