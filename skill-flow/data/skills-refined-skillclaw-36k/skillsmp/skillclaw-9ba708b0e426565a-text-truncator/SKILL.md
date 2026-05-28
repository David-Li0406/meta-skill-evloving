---
name: text-truncator
description: Use this skill when you need to intelligently truncate text while preserving content integrity and semantic coherence, ensuring it does not exceed specified length limits.
---

# Skill body

## Functionality

Intelligently truncate text while maintaining content integrity and semantic coherence, limiting text to a specified length.

## Usage Scenarios

- Preprocess text that exceeds length limits to meet agent input requirements.
- Extract key sections for text previews or summary generation to improve efficiency and readability.
- Assist content creation by intelligently trimming generated long text to avoid redundancy.

## Core Capabilities

- **Semantic-Priority Truncation**: Prioritize truncation at natural semantic boundaries (periods, question marks, exclamation points) to maximize sentence integrity.
- **Paragraph Integrity**: When semantic boundaries are insufficient, prioritize truncation at paragraph ends or line breaks to avoid breaking paragraph structure.
- **Precise Length Control**: Strictly adhere to user-specified maximum length limits, ensuring output text does not exceed limits.
- **Truncation Marker Insertion** (optional): Automatically add custom truncation markers (such as "...") at the end of truncated text to indicate content omission.

## Input Requirements

- **Text Content**: Original text to be truncated (string).
- **Maximum Length Limit**: Target maximum character count for text (integer).
- **Truncation Marker** (optional): String to identify text truncation location, such as "[...]".

## Output Format

```
[Text Truncation Report]

Original Length: [character count]
Truncated Length: [character count]
Truncation Position: [position description, such as: at period in sentence X]

Truncated Text:
[truncated text]
```