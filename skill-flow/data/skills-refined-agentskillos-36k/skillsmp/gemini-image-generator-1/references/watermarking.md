# Watermarking Guidance

## Workflow

1. Generate a watermark image with transparent background (text-only PNG).
2. Overlay the watermark image onto the base image.

## Positions

- `bottom-right` (default)
- `bottom-left`
- `top-right`
- `top-left`
- `center`

## Prompt Snippets

### Create a watermark (transparent background)

```
Create a clean watermark with the text "[TEXT]". Use a transparent background.
Keep the typography crisp and legible at small sizes.
```

### Overlay watermark at a position

```
Add the watermark from the second image to the [POSITION] of the first image.
Blend it naturally with the lighting and texture. Preserve the original image.
```
