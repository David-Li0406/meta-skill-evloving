---
name: code-review-skill
description: 指定されたコードファイルを読み取り、要約と「TODO/FIXME」の有無を確認してフィードバックします。
---

# Code Summary and Feedback Skill

## Purpose
This skill is designed to provide a concise summary of a given code file and offer specific feedback based on its content. It checks for common patterns or required elements.

## Usage
When activated, you must provide the path to a code file. I will then:
1. **Read** the content of the specified code file using the `read` tool.
2. Generate a 2-3 sentence summary of the file's main purpose and structure.
3. Check if the file contains the string "TODO" (case-insensitive).
4. Check if the file contains the string "FIXME" (case-insensitive).
5. Report the summary and the findings regarding "TODO" and "FIXME".

## Output Format
📝 Code Summary for [FILENAME]: [Summary text]

🔍 Feedback:

Contains TODO: [Yes/No]

Contains FIXME: [Yes/No]

--- Skill Executed (code-review-skill) ---


## Example Prompt
"Apply code-review-skill to src/app.tsx"
