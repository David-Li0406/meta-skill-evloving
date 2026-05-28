---
name: nanobanana
description: Use this skill to generate or edit images using Google's latest AI models.
---

# Nano Banana Skill

This skill allows you to generate and edit images using Google's Gemini models via the `nanobanana.js` script. It supports text-to-image and multimodal (image + text) prompts.

## Prerequisites

Ensure the `GEMINI_API_KEY` environment variable is set.

## Usage

```bash
node nanobanana.js [options] <prompt> [image_path] ...
```

## Options

- **`--model <name>`**: Specifies the Gemini model to use. (Default: `gemini-2.5-flash-image`)
- **`--output`, `-o <path>`**: Output filename or directory. (Default: `./nanobanana-outputs`)
- **`--aspectRatio`, `--ar <ratio>`**: Sets the aspect ratio of the generated image (e.g., `16:9`, `1:1`, `4:3`, `3:4`).
- **`--count <number>`**: Number of images to generate.
- **`--seed <number>`**: Integer seed for reproducible results.
- **`--imageSize <size>`**: **Requires `gemini-3-pro-image-preview`**. Sets specific image dimensions (e.g., `1024x1024`).
- **`--googleSearch`**: **Requires `gemini-3-pro-image-preview`**. Enables Google Search grounding for generation. (Default: `false`)

## Constraints

- **Model Capabilities**: The `--imageSize` and `--googleSearch` flags are **only** compatible with the `gemini-3-pro-image-preview` model. Using them with other models may result in errors or them being ignored.

## Examples

### 1. Basic Text-to-Image

Generate a landscape using the default model (`gemini-2.5-flash-image`).

```bash
node nanobanana.js "A futuristic city at sunset, synthwave style"
```

### 2. Image Variation (Image-to-Image)

Generate a variation of an existing image.

```bash
node nanobanana.js "A watercolor painting of this scene" ./images/01_Evan_Plays_Drums.png
```

### 3. Intermixed Text & Images (Virtual Try-On)

Provide multiple text and image inputs in sequence to guide the generation.

```bash
node nanobanana.js "Show this person:" ./person.jpeg "wearing this shirt:" ./shirt.png
```

### 4. Advanced Generation with Preview Model

Use advanced features like `imageSize` and `googleSearch` with the preview model.

```bash
node nanobanana.js --model gemini-3-pro-image-preview --imageSize 1024x1024 --googleSearch "A realistic image of the latest electric car model"
```

### 5. Specific Aspect Ratio, Count and Output

Generate 3 portraits with a 9:16 aspect ratio and save them to a specific directory.

```bash
node nanobanana.js --ar 9:16 --count 3 --output ./my-portraits/ "Portrait of a cypherpunk character"
```

## Output

Generated images are saved to the `./nanobanana-outputs` directory with unique filenames (e.g., `image-uuid.png`).
