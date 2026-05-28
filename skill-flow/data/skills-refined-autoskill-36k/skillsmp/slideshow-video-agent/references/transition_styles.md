# Transition Styles

The Kling 2.6 Pro model generates animated transitions between slides. Available styles:

| Style | Description | Effect |
|-------|-------------|--------|
| **cinematic** | Elegant dissolve with subtle particles | Particles flow across frame with light streaks |
| **zoom_blur** | Dynamic zoom blur | Content rushes toward camera with motion blur |
| **swipe** | Horizontal swipe | Smooth 3D parallax depth effect |
| **shatter** | Breaking apart | Elements gracefully break into floating pieces |
| **morph** | Organic transformation | Shapes smoothly flow and transform |
| **particles** | Particle dissolve | Content dissolves into swirling glowing particles |
| **flip** | 3D card flip | Realistic card flip with depth and shadow |
| **wave** | Ripple effect | Wave spreads across frame |
| **slide_left** | Slide out | Content slides left revealing darkness |
| **fade_blur** | Soft fade | Gentle blur with fade effect |

## Default Style

The default style is **cinematic**, which provides an elegant, professional look.

## Duration

Transitions are generated as 5-second videos and trimmed to 2.5 seconds by default. You can adjust:

```python
config = PresentationConfig(
    slides=[...],
    transition_style="swipe",
    transition_duration=3.0,  # 3 seconds instead of 2.5
    ...
)
```

## Style Recommendations

| Presentation Type | Recommended Styles |
|-------------------|-------------------|
| Corporate/Formal | cinematic, fade_blur |
| Tech/Product | zoom_blur, swipe |
| Creative/Artistic | particles, morph, shatter |
| Training/Education | cinematic, slide_left |
| Marketing | zoom_blur, particles |

## Usage

In Python:
```python
config = PresentationConfig(
    slides=[...],
    transition_style="particles",
    ...
)
```

In JSON:
```json
{
    "transition_style": "particles",
    "slides": [...]
}
```
