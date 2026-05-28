---
name: organize-transcript
description: File a VTT transcript into the correct project folder. Use when the user provides a .vtt file, mentions a meeting transcript, or says they have a recording to process.
---

# Organize Meeting Transcript

File the provided .vtt transcript into the correct project folder structure.

## Instructions

1. Read the transcript content provided by the user (either pasted or from a file path)
2. Ask which project this belongs to if not specified (or detect from context)
3. Determine the meeting date from:
   - The filename if provided
   - The transcript timestamps
   - Or ask the user
4. Create the project folder structure if it doesn't exist:
   ```
   projects/{project-name}/transcripts/
   projects/{project-name}/dashboards/
   projects/{project-name}/analysis/
   ```
5. Save the transcript to `projects/{project-name}/transcripts/{YYYY-MM-DD}.vtt`
6. Confirm the saved location

## Conventions

- Project names use kebab-case: `my-project-name`
- Dates use ISO format: `YYYY-MM-DD`

## Example

User provides: "standup.vtt for project alpha"
→ Save to: `projects/project-alpha/transcripts/2026-01-12.vtt`
