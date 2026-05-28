---
name: document-illustrator
description: >
  AI-powered document illustration generator that analyzes document content and creates professional images.
  Use this skill when users need to generate illustrations for documents, articles, or notes.
  Supports three styles: gradient-glass (tech/modern), ticket (infographic/data), and vector-illustration (storytelling/education).
  Triggers: "generate illustrations", "create images for document", "配图", "插图", "document images"
---

# Document Illustrator

Generate professional illustrations for documents using AI. Claude analyzes the content, summarizes key points, and generates images via Gemini API.

## Workflow

### Step 1: Read and Analyze Document

Read the document with Read tool, then intelligently identify core themes and key points. No specific format required - works with Markdown, plain text, or any readable format.

### Step 2: Gather User Preferences

Ask the user three questions using AskUserQuestion:

1. **Aspect ratio**: 16:9 (landscape) or 3:4 (portrait)
2. **Cover image**: Generate a cover image summarizing the entire document?
3. **Number of images**: How many content images? (recommended: 3-10)

### Step 3: Summarize and Confirm

Based on the requested number, intelligently group document content into themes. Present the summary to the user:

```
Content Summary Complete

Cover Image (if selected):
"[Document Title]"
- Core concept 1
- Core concept 2

Content Images (N total):
1. [Theme 1 Title]
   Includes: point A, point B, point C

2. [Theme 2 Title]
   Includes: point D, point E

...

Confirm to start generating? (Y/N)
```

### Step 4: Generate Images

After user confirmation, call the Python script for each image:

```bash
python3 scripts/generate_single_image.py \
  --title "Image Title" \
  --content "Content description..." \
  --style-file references/styles/gradient-glass.md \
  --output /path/to/images/illustration-01.png \
  --ratio 16:9 \
  --resolution 2K
```

For cover images, add `--cover` flag.

**Output location**: `images/` folder in the document's directory.

## Style Reference

Three styles available in `references/styles/`:

| Style | File | Best For |
|-------|------|----------|
| Gradient Glass | `gradient-glass.md` | Tech products, data reports, modern presentations |
| Ticket | `ticket.md` | Infographics, statistics, timelines, summaries |
| Vector Illustration | `vector-illustration.md` | Storytelling, tutorials, educational content |

## Image Specifications

| Ratio | 2K Resolution | 4K Resolution |
|-------|---------------|---------------|
| 16:9 | 2560x1440 | 3840x2160 |
| 3:4 | 1920x2560 | 2880x3840 |

## Environment Requirements

**Python dependencies**:
```bash
pip install google-genai pillow python-dotenv
```

**API key**: Set `GEMINI_API_KEY` in environment or create `.env` file in skill directory.

## Content Grouping Principles

When summarizing document content:
- **Completeness**: Include all important information
- **Logical flow**: Group related content together
- **Balance**: Similar information density per image
- **User control**: Show summary for user confirmation before generating
