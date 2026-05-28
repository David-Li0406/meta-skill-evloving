---
name: image-generation-and-editing
description: Use this skill when you need to generate or edit high-quality images, create graphics, or visualize concepts using the Gemini API.
---

# Image Generation and Editing

Generate and edit images using Google's Gemini API (Nano Banana Pro). This skill supports text-to-image generation, image editing, and multi-turn refinement.

## When to Use

Invoke this skill when the user:
- Requests to "generate an image" or "create a picture"
- Wants to "edit this photo" or "modify this image"
- Needs graphics with text (logos, infographics, diagrams)
- Asks for "consistent characters" across multiple images
- Says "visualize this" or "make me a [visual thing]"

## Workflow Overview

1. **Gather Design Direction**: Ask clarifying questions to understand the user's intent.
   - **Purpose**: What is the image for? (banner, logo, social media, etc.)
   - **Style preference**: Any specific art style or aesthetic?
   - **Color palette**: Any brand colors or mood?
   - **Composition constraints**: Aspect ratio, text overlay space?
   - **Key elements**: What must be included or avoided?

2. **Prompt Rewriting**: Transform user prompts into detailed descriptions.
   - Include subject details, environment, lighting, composition, style, mood, and technical specs.

3. **Generate Images**: Use the Gemini API to create images based on the refined prompts.
   - **Text-to-Image**: Generate new images from text prompts.
   - **Edit Existing Images**: Modify images with specific instructions.

4. **Iterate and Refine**: Use a draft → iterate → final approach.
   - Start with quick drafts (1K resolution) for feedback.
   - Refine prompts and generate higher resolution images (2K or 4K) once satisfied.

## Image Generation Commands

### Generate New Image
```bash
python scripts/generate_image.py "A description of the image" output.png --resolution 4K
```

### Edit Existing Image
```bash
python scripts/edit_image.py input.png "Editing instructions" output.png --resolution 2K
```

## Image Configuration Options

- **Resolution**: Choose from 1K, 2K, or 4K based on user needs.
- **Aspect Ratio**: Specify aspect ratios like 16:9, 1:1, etc., depending on the use case.

## Advanced Features

- **Multi-Image Composition**: Combine up to 14 reference images for complex scenes.
- **Character Consistency**: Maintain the same character across multiple images by referencing previous generations.
- **Google Search Grounding**: Generate images based on real-time data.

## Prompting Best Practices

- **Be Specific**: Include details about colors, materials, lighting, and mood.
- **Specify Style**: Indicate the desired artistic style (e.g., photorealistic, watercolor).
- **Use Negative Prompts**: Specify what to avoid for better results (e.g., "Avoid: text, logos, blurry images").

## Example Prompts

### Basic Image Generation
```bash
python scripts/generate_image.py "A futuristic cityscape at sunset" output.png --resolution 4K
```

### Photo Editing
```bash
python scripts/edit_image.py input.png "Make it look like winter" output.png --resolution 2K
```

### Iterative Refinement
```bash
python scripts/edit_image.py input.png "Adjust lighting to warmer tones" output.png --resolution 2K
```

## Output Management

Images are saved in the current working directory with a timestamped naming format for easy organization.

## Security Notes

- Ensure the `GEMINI_API_KEY` is set in your environment for API access.
- Images are processed locally and not stored on external servers.

## References

- For detailed prompting techniques, refer to `references/prompting-guide.md`.
- For examples of prompts by category, see `references/examples.md`.