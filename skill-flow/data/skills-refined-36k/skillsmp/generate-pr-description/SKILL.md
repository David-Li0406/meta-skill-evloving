---
name: generate-pr-description
description: Generates a professional PR description by analyzing git diff between current branch and main. Use when the user wants to prepare a pull request, write a description, or summarize their changes for a PR.
---

# Generate PR Description

## Instructions

When this skill is activated, follow these steps strictly:

1. **Get the Diff**:
   - Run `git diff main...HEAD` to identify changes in the current branch relative to the `main` branch.
   - If the user specifies a different base branch, use that instead of `main`.

2. **Generate Content (Strictly English)**:
   - Create a PR description in **English** with the following sections:
     - **Summary**: A high-level overview of the purpose of this PR.
     - **Changes**: A detailed bulleted list of technical changes.
     - **Test**: A description of how these changes were verified.

3. **Output to File**:
   - **Do NOT** use any tools to actually create or push a PR to GitHub/GitLab.
   - Save the generated content into a file named `PR_DESCRIPTION.md` in the root directory of the current project.
   - If the file already exists, overwrite it.

4. **Completion**:
   - Inform the user: "PR description has been generated and saved to `PR_DESCRIPTION.md`."
   - Provide a brief summary of what was written in the terminal for immediate feedback.

## Examples

- "Generate a PR description for my current changes."
- "幫我寫 PR description 並存成檔案。"
