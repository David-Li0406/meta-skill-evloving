---
name: format-for-x
description: Convert markdown articles to X/Twitter-compatible format. Removes markdown syntax, converts tables to em-dash format, and provides formatting instructions for the X editor.
---

# Format for X (Twitter)

Convert markdown content to X article editor format. The X editor is a rich text editor that does NOT support markdown syntax - formatting must be applied manually using keyboard shortcuts or toolbar buttons.

## What This Skill Does

1. **Removes all markdown syntax** that X doesn't render
2. **Converts content** to plain text with clear section breaks
3. **Provides formatting instructions** so you know what to select and format after pasting

## X Editor Capabilities

**Supported:**

- Bold (Cmd+B after selecting text)
- Italic (Cmd+I after selecting text)
- Strikethrough (Cmd+Shift+X)
- Headings (via "Body" dropdown → "Heading")
- Subheadings (via "Body" dropdown → "Subheading")
- Links (inline hyperlinks)
- Line breaks and paragraph spacing

**NOT Supported:**

- Markdown tables (| syntax)
- Code blocks or inline backticks
- Blockquotes (> syntax)
- Markdown bold/italic markers (**text**, _text_)
- Markdown headings (# syntax)
- Lists with automatic styling
- Horizontal rules

---

## Conversion Process

When the user provides markdown content, apply these transformations:

### 1. Headings

**Before:**

```
# Main Heading
## Section Heading
### Subsection
```

**After:**

```
Main Heading
[HEADING]

Section Heading
[SUBHEADING]

Subsection
[SUBHEADING]
```

Remove `#` characters. Add `[HEADING]` marker for top-level headings, `[SUBHEADING]` for all others.

### 2. Bold and Italic

**Before:**

```
This has **bold text** and *italic text* and ***both***.
```

**After:**

```
This has bold text and italic text and both.
```

Track formatting locations for the instructions section:

- "bold text" → BOLD
- "italic text" → ITALIC
- "both" → BOLD + ITALIC

### 3. Tables

**Before:**

```
| Column 1 | Column 2 | Column 3 |
| -------- | -------- | -------- |
| Value A  | Value B  | Value C  |
| Value D  | Value E  | Value F  |
```

**After:**

```
Column 1 — Column 2 — Column 3
Value A — Value B — Value C
Value D — Value E — Value F
```

Remove pipe characters and separator rows. Use em-dashes (—) as separators.

### 4. Code

**Inline code:**

```
Use `npm install` to install dependencies.
```

→

```
Use npm install to install dependencies.
```

**Code blocks:**

````
```javascript
const x = 1;
```
````

→

```
const x = 1;
```

Remove all backticks. Code will appear as plain text - context makes it clear what's code.

### 5. Blockquotes

**Before:**

```
> This is an important quote that spans
> multiple lines.
```

**After:**

```
"This is an important quote that spans multiple lines."
```

Remove `>` characters, wrap in quotes, and note for italic formatting.

### 6. Lists

**Before:**

```
- Item one
- Item two
- Item three

1. First
2. Second
3. Third
```

**After:**

```
• Item one
• Item two
• Item three

1. First
2. Second
3. Third
```

Convert `-` or `*` bullets to `•`. Keep numbered lists as-is.

### 7. Horizontal Rules

**Before:**

```
---
```

**After:**

```

⸻

```

Replace with a visual separator or extra blank line.

### 8. Links

**Before:**

```
Check out [this article](https://example.com) for more.
```

**After:**

```
Check out this article (https://example.com) for more.
```

Or if link text is descriptive enough:

```
Check out this article for more.
[LINK: "this article" → https://example.com]
```

---

## Output Format

Produce two sections:

### Section 1: Formatted Content

The clean, paste-ready text with:

- All markdown syntax removed
- Tables converted to em-dash format
- Proper paragraph spacing (blank lines between sections)
- `[HEADING]` and `[SUBHEADING]` markers on their own lines after headings
- Quotes wrapped in quotation marks

### Section 2: Formatting Instructions

A numbered list of manual formatting to apply after pasting:

```
## Formatting Instructions

After pasting into X, apply these formats:

1. Line 1: Select "Main Heading" → Set style to Heading
2. Line 5: Select "Section Title" → Set style to Subheading
3. Line 7: Select "bold text" → Apply Bold (Cmd+B)
4. Line 9: Select "italic phrase" → Apply Italic (Cmd+I)
5. Line 12: Select "link text" → Add link to https://example.com
6. Lines 15-17: Select entire quote → Apply Italic (Cmd+I)
```

---

## Example Transformation

### Input:

```markdown
# Getting Started with AI Agents

This is a paragraph with **bold text** and _italic text_.

## Configuration

| Setting | Value |
| ------- | ----- |
| theme   | dark  |
| version | 1.0   |

Here's some code: `npm install`

> **Important**: This step is critical for success.

### Next Steps

1. Read the docs
2. Try the examples
3. Build something
```

### Output:

```
Getting Started with AI Agents
[HEADING]

This is a paragraph with bold text and italic text.

Configuration
[SUBHEADING]

Setting — Value
theme — dark
version — 1.0

Here's some code: npm install

"Important: This step is critical for success."

Next Steps
[SUBHEADING]

1. Read the docs
2. Try the examples
3. Build something
```

**Formatting Instructions:**

After pasting into X, apply these formats:

1. Select "Getting Started with AI Agents" → Set style to Heading (dropdown)
2. Select "Configuration" → Set style to Subheading (dropdown)
3. Select "bold text" → Apply Bold (Cmd+B)
4. Select "italic text" → Apply Italic (Cmd+I)
5. Select "Next Steps" → Set style to Subheading (dropdown)
6. Select "Important:" → Apply Bold (Cmd+B)
7. Select entire quote line → Apply Italic (Cmd+I)

---

## Tips for Best Results

**Spacing:**

- Add blank lines before and after headings
- Add blank lines between sections
- Keep paragraphs under 150 words for readability

**Character encoding:**

- Use proper em-dashes (—) not double-hyphens (--)
- Smart quotes ("") work but straight quotes are fine too

**Editor quirks:**

- Avoid keyboard selection across multiple lines (can cause jumps)
- Triple-click to select entire lines
- Edit small sections at a time

---

## Invocation

User says: "Format this for X" or "/format-for-x" followed by markdown content.

**Response:** Provide the cleaned content and formatting instructions. Do not add commentary - just the two output sections.
