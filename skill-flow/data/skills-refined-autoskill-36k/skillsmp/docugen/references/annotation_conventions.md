# Annotation Conventions for DocuGen

This guide defines visual annotation standards for screenshot markup.

## Highlight Boxes

### Purpose
Highlight boxes draw attention to the specific UI element referenced in the step.

### Style
- **Color**: Orange-red (#FF5733) with 70% opacity
- **Border**: 3px solid line
- **Shape**: Rectangle matching element bounds + 4px padding

### Placement Rules
1. Box should surround the entire clickable element
2. Include a small margin (4px) around the element
3. For dropdown menus, highlight the trigger element, not the entire menu

### Multiple Elements
When a step involves multiple elements:
1. Use numbered callouts instead of multiple boxes
2. Number in order of interaction
3. Connect with arrows if sequence matters

## Arrows

### Purpose
Arrows indicate direction or flow, connecting callouts to their targets.

### Style
- **Color**: Orange-red (#FF5733), solid
- **Line width**: 3px
- **Head style**: Filled triangle, 15px length

### Placement Rules
1. Arrow should not obscure the target element
2. Approach from a clear direction (usually top-left or left)
3. Keep arrow length consistent (75-150px)
4. Avoid crossing other annotations

## Numbered Callouts

### Purpose
Callouts mark multiple interaction points in a single screenshot.

### Style
- **Shape**: Circle, 24px diameter
- **Background**: Orange-red (#FF5733)
- **Text**: White (#FFFFFF), bold, centered
- **Font size**: 16px

### Placement Rules
1. Position callout near but not overlapping the element
2. Numbers follow interaction sequence (1, 2, 3...)
3. Place consistently (prefer top-left of element)
4. Maximum 5 callouts per screenshot

### Numbering Scheme
- Single screenshot: 1, 2, 3...
- Multi-step: Match step numbers (Step 1 = callout 1)

## Blur Regions

### Purpose
Blur protects sensitive information while maintaining context.

### Style
- **Type**: Gaussian blur
- **Strength**: 15px radius
- **Coverage**: Full region, no visible edges

### Auto-Detection Patterns
Automatically blur:
- Password fields (type="password")
- Fields labeled: SSN, Credit Card, API Key
- Email addresses in forms
- User avatars/profile pictures (optional)

### Manual Override
Users can specify additional blur regions or disable auto-detection.

## Color Scheme

### Primary Annotation Color
- **Hex**: #FF5733
- **RGB**: (255, 87, 51)
- **Purpose**: High visibility against most backgrounds

### Alternative Colors (for complex annotations)
| Color | Hex | Use Case |
|-------|-----|----------|
| Blue | #3498DB | Secondary highlights |
| Green | #2ECC71 | Success/completion states |
| Yellow | #F1C40F | Warnings/caution areas |

### Contrast Guidelines
- Test annotations against the screenshot background
- Use alternative colors if primary doesn't contrast well
- Never use red on red UI elements

## Annotation Order (Layering)

From bottom to top:
1. Blur regions
2. Highlight boxes
3. Arrows
4. Numbered callouts

## Quality Standards

### Resolution
- Source screenshots: Native resolution
- Annotated output: Same as source
- Minimum width: 800px

### File Format
- **PNG**: Default, lossless quality
- **Maximum size**: 200KB per image
- **Optimization**: Compress after annotation

### Accessibility
- Alt text must describe the annotation purpose
- Don't rely solely on color to convey meaning
- Include text descriptions in documentation

## Examples

### Simple Step (Single Element)
```
+------------------+
|  [Button]        | <-- Orange highlight box
+------------------+
```

### Multi-Action Step
```
    ①           ②
+--------+  +--------+
| First  |  | Second |
+--------+  +--------+
     |          |
     └----→-----┘ <-- Arrow showing sequence
```

### Sensitive Data
```
+------------------+
| Email: ████████  | <-- Blurred region
| Password: ██████ |
+------------------+
```
