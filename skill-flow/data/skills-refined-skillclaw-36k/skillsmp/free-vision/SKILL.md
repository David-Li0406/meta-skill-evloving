---
name: free-vision
description: Handle vision/image tasks (read, describe, analyze images) by calling Gemini CLI or Qwen Code CLI from the shell. Use for requests to interpret or describe images, extract visible text, or summarize visual content; prefer Gemini and fall back to Qwen if Gemini fails or is too generic.
---

# Free Vision

## Quick workflow

1. Identify the image path(s). Prefer absolute paths; confirm the file exists before calling a CLI.
2. Run Gemini first with a specific, structured prompt. Use the CLI's file-include syntax if supported (commonly `@/path/to/image`).
   ```bash
   gemini "Analyze the image: (1) 1-sentence summary, (2) key objects, (3) visible text verbatim, (4) notable details. @/absolute/path/to/image"
   ```
3. If Gemini errors, produces empty output, or responds too generically, run Qwen with the same prompt structure and image reference.
   ```bash
   qwen "Analyze the image: (1) 1-sentence summary, (2) key objects, (3) visible text verbatim, (4) notable details. @/absolute/path/to/image"
   ```

## Prompting tips

- Be explicit about the required fields and verbosity.
- Ask for verbatim text extraction when relevant.
- If the output is vague, re-run with stricter instructions: “Be specific; avoid generic phrases; list exact items and locations.”

## Failure handling

- If the CLI rejects `@/path` syntax, retry in interactive mode and include the image path in the prompt as supported by the CLI.
- If both tools fail to load the image, report the failure and ask the user for guidance on the expected image input format.
