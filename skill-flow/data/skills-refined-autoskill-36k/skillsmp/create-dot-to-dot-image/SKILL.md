---
name: create_dot_to_dot_image
description: Generate a high-quality Dot-to-Dot puzzle image for a given subject.
---

# Create Dot-to-Dot Image

This skill generates a clear, solvable Dot-to-Dot puzzle image using the `generate_image` tool.

## Usage

When the user asks for a dot-to-dot puzzle of a specific subject (e.g., "cat", "car", "castle"), use the following prompt structure.

## Prompt Template

Use the `generate_image` tool with the following prompt, replacing `[SUBJECT]` with the requested object:

```text
A simple, black and white line art illustration of a [SUBJECT] designed as a connect-the-dots puzzle. The [SUBJECT] outline is formed by numbered dots (1, 2, 3...) in a sequence. White background. Suitable for children. Clear lines and distinct dots.
```

## Best Practices

1.  **Simplicity**: Keep the subject simple. Complex overlapping lines make the puzzle confusing.
2.  **Contrast**: Ensure the prompt specifies "black and white" and "white background" for maximum visibility.
3.  **Audience**: The "Suitable for children" keyword helps the model generate cleaner, less cluttered lines.
4.  **Note on Interactivity**: Remind the user that the generated image is a *raster* (pixel) image. To make it interactive (clicking dots), they will need to manually map the coordinates or use the image as a printable asset.
