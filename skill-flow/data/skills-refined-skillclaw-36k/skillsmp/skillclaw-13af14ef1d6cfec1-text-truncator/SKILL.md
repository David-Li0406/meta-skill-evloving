---
name: text-truncator
description: Use this skill when you need to intelligently truncate text while maintaining its integrity and coherence, ensuring it does not exceed a specified length limit.
---

# Skill body

## Functionality

This tool intelligently truncates text while preserving its integrity and coherence, adhering to a specified maximum length.

## Use Cases

- Preprocess long texts to meet input requirements for various applications.
- Extract key portions of text for previews or summaries to enhance efficiency and readability.
- Assist in content creation by intelligently trimming generated long texts to avoid redundancy.

## Core Capabilities

- **Semantic Priority Truncation**: Prioritizes truncation at natural semantic boundaries (e.g., periods, question marks, exclamation points) to maintain sentence integrity.
- **Paragraph Integrity**: When semantic boundaries are insufficient, truncation occurs at paragraph ends or line breaks to avoid disrupting paragraph structure.
- **Precise Length Control**: Strictly adheres to the user-specified maximum length limit, ensuring the output text does not exceed it.
- **Truncation Marker Insertion** (optional): Automatically adds a custom truncation marker (e.g., "...") at the end of truncated text to indicate content has been shortened.

## Input Requirements

- **Text Content**: The original text to be truncated (string).
- **Maximum Length Limit**: The maximum length for the truncated text (integer, e.g., character count or token count).
- **Truncation Marker** (optional): A custom truncation marker, such as "..." or "[content truncated]".

## Output Format

```
【Text Truncation Report】

- Original Text Length: [integer] characters/tokens
- Truncated Length: [integer] characters/tokens
- Truncation Position: [description of position, e.g., "at the end of sentence X"] or "not truncated"

### Truncated Text
[truncated text content]
```

## Constraints

- The length of the truncated text must strictly comply with the maximum length limit.
- Ensure the truncated text is as coherent and complete as possible.
- If the text does not reach the maximum length, return the original text without truncation.
- The output format must be structured, clearly displaying the length information before and after truncation and the content of the truncated text.

## Examples

Refer to `{baseDir}/references/examples.md` for more detailed examples:
- `examples.md` - Contains truncation examples with varying lengths, truncation markers, and complex text structures.

## Detailed Documentation

Refer to `{baseDir}/references/examples.md` for comprehensive guidance and case studies on the text truncation tool.