---
name: nano-banana-image-generation
description: Use this skill to generate, edit, and restore high-quality images using the Gemini API with the Nano Banana extension. Ideal for creating visuals from text prompts, modifying existing images, or generating graphics with text.
---

# Skill body

## Overview

Utilize the Gemini API with the Nano Banana extension to generate and edit images through command-line instructions. Outputs are saved for review or delivery.

## Prerequisites

- Ensure Gemini CLI is installed: `gemini --version`
- Install the Nano Banana extension: 
  ```bash
  gemini extensions install https://github.com/gemini-cli-extensions/nanobanana
  ```
- Set your API key as an environment variable: 
  ```bash
  export GEMINI_API_KEY=your_api_key_here
  ```
- Optional: Set `NANOBANANA_MODEL=gemini-3-pro-image-preview` for enhanced capabilities.

## Workflow

1. **Identify Request Type**: Determine if the user wants to generate, edit, restore, create icons, patterns, or diagrams.
2. **Prepare Input**: Ensure any input images are accessible in the current directory.
3. **Start Gemini CLI**: Launch the CLI in the working directory:
   ```bash
   gemini
   ```
4. **Execute Commands**: Use the appropriate command based on the request:
   - **Generate**: 
     ```bash
     /generate "your prompt" --count=3 --styles="style1,style2"
     ```
   - **Edit**: 
     ```bash
     /edit input.png "editing instructions" --preview
     ```
   - **Restore**: 
     ```bash
     /restore old_photo.jpg "restoration instructions"
     ```
   - **Create Icon**: 
     ```bash
     /icon "icon prompt" --sizes="64,128,256"
     ```
   - **Generate Pattern**: 
     ```bash
     /pattern "pattern prompt" --type="seamless"
     ```
   - **Create Story**: 
     ```bash
     /story "story prompt" --steps=4
     ```
   - **Custom Command**: 
     ```bash
     /nanobanana "freeform instruction"
     ```
5. **Collect Outputs**: Retrieve generated files from `./nanobanana-output/` and share the paths with the user.

## Troubleshooting

- If you encounter permission issues, run with approval mode:
  ```bash
  gemini --approval-mode yolo -p "..."
  ```
- If no valid API key is found, ensure `GEMINI_API_KEY` is set correctly.

## Prompting Guidance

- Provide detailed prompts specifying subject, style, medium, and any constraints.
- For consistent series, maintain style and specify variation goals.
- Use options like `--count`, `--styles`, and `--variations` for systematic exploration.

## Additional Notes

- For iterative refinement, consider using lower resolutions initially (1K) and move to higher resolutions (4K) once the prompt is finalized.
- Always save outputs in the user's current working directory to avoid confusion.