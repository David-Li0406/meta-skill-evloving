---
name: sc-create-slide-template
description: Use this skill when you need to extract visual styling from screenshots to create reusable ScriptCast slide templates, ensuring all templates are validated for correctness.
---

# ScriptCast Template Creation Workflow

## Purpose

Enable users to create slide templates by:
1. Uploading screenshots/mockups of desired visual style.
2. Extracting colors, fonts, spacing, and layout from images.
3. Generating a complete template covering all ScriptCast features.
4. Storing templates for reuse via CLI `--template <name>` option.
5. Validating all bundled templates work correctly.

## Template Scope

A complete ScriptCast template must define styling for ALL visual elements:

### Slide Styling (`SlideStyle`)
| Property | Description | Extracted From |
|----------|-------------|----------------|
| `background_color` | Default slide background | Dominant background color |
| `gradient_start`/`gradient_end` | Optional gradient | Gradient detection |
| `title_color`, `title_size` | Title typography | Header text analysis |
| `text_color`, `text_size` | Body text styling | Body text analysis |
| `bullet_color`, `bullet_size`, `bullet_char` | Bullet point styling | List detection |
| `margin`, `line_spacing` | Layout spacing | Edge/padding analysis |
| `vertical_align`, `title_align`, `text_align` | Alignment | Content positioning |

### Carbon Code Block Styling (`CarbonConfig`)
| Property | Description | Default |
|----------|-------------|---------|
| `gradient` | Background gradient preset | From GRADIENTS dict |
| `theme` | Pygments syntax theme | monokai, dracula, etc. |
| `window_bg` | Editor window background | Dark color from palette |
| `show_titlebar` | macOS-style titlebar | true |
| `corner_radius` | Window corner rounding | 16 |

### Transition Defaults (`TransitionConfig`)
| Property | Description | Default |
|----------|-------------|---------|
| `type` | Default transition type | fade, crossfade, etc. |
| `duration` | Transition duration | 0.5s |
| `color` | Fade color | black |

### Video Settings
| Property | Description | Options |
|----------|-------------|---------|
| `resolution` | Default resolution | 4K (3840x2160), 1080p (1920x1080) |
| `frame_rate` | Video frame rate | 30, 60 |

## Template Storage

### Location
```
src/scriptcast/assets/templates/
├── __init__.py          # Template registry
```