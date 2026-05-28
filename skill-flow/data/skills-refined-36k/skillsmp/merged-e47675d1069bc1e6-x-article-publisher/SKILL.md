---
name: x-article-publisher
description: Use this skill to publish Markdown articles to X (Twitter) Articles editor with proper formatting, including cover image upload and rich text conversion. Ideal for users looking to publish Markdown files or URLs to X Articles.
---

# X Article Publisher

Publish Markdown content to X (Twitter) Articles editor, preserving formatting with rich text conversion.

## Prerequisites

- X Premium Plus subscription
- Python 3.9+ with dependencies:
  - macOS: `pip install Pillow pyobjc-framework-Cocoa`
  - Windows: `pip install Pillow pywin32 clip-util`
- Playwright MCP for browser automation

## 🎉 Initial Setup: Persistent Authentication

**X Article Publisher now supports persistent authentication, eliminating the need for repeated logins!**

### 🔧 Initialize Authentication (One-time Setup)

Before first use, run the authentication setup:

```bash
cd ~/.claude/skills/x-article-publisher/scripts
python auth_manager.py setup
```

**Process:**
1. ✅ A browser window opens for X login.
2. 🔐 Manually log into your X account (Premium+ required).
3. ✅ Complete 2FA verification (if enabled).
4. 🏠 Successful login redirects to Home timeline.
5. 💾 Authentication status is saved (valid for 7 days).

### 📋 Authentication Management Commands

```bash
# Check authentication status
python auth_manager.py status

# Validate authentication
python auth_manager.py validate

# Clear authentication data (requires re-login)
python auth_manager.py clear

# Re-authenticate (clear + setup)
python auth_manager.py reauth
```

### 🚀 Automated Workflow

Once authentication is set up, the skill will automatically:
1. ✅ Check authentication status.
2. 🔓 If authenticated, use saved browser state (no login required).
3. ⚠️ If not authenticated, prompt to run `auth_manager.py setup`.

**Note**: Authentication data is stored in `~/.claude/skills/x-article-publisher/data/browser_state/`, excluded from Git via .gitignore.

---

## Scripts

Located in `~/.claude/skills/x-article-publisher/scripts/`:

### publish_article.py (Main Script - One-click Publish)
**Recommended** - Automatically completes all publishing steps:
```bash
# Basic usage (default shows browser)
python publish_article.py --file article.md

# Hide browser (run headless)
python publish_article.py --file article.md --headless

# Custom title
python publish_article.py --file article.md --title "Custom Title"
```

### parse_markdown.py
Parse Markdown and extract structured data:
```bash
python parse_markdown.py <markdown_file> [--output json|html] [--html-only]
```
Returns JSON with: title, cover_image, content_images (with block_index for positioning), html, total_blocks.

### copy_to_clipboard.py
Copy image or HTML to system clipboard:
```bash
# Copy image (with optional compression)
python copy_to_clipboard.py image /path/to/image.jpg [--quality 80]

# Copy HTML for rich text paste
python copy_to_clipboard.py html --file /path/to/content.html
```

## Workflow Overview

**Prerequisite**: Complete authentication setup (`python auth_manager.py setup`).

### 🚀 One-click Publish (Recommended)

Run `publish_article.py` to automatically complete all steps:

```bash
cd ~/.claude/skills/x-article-publisher/scripts
python publish_article.py --file /path/to/article.md
```

The script will automatically:
1. ✅ Check authentication status.
2. 📄 Parse the Markdown file.
3. 🌐 Launch the authenticated browser.
4. 📍 Navigate to X Articles editor.
5. 🔘 Click the create button.
6. 🖼️ Upload cover image (if any).
7. 📝 Fill in the title.
8. 📋 Paste HTML content.
9. ✅ Save as draft (**will not auto-publish**).

### Manual Workflow (Advanced Users)

For finer control, execute steps individually:
1. Parse Markdown: `python parse_markdown.py article.md`
2. Manually operate the browser to publish.

---

## 🧠 Intelligent Enhancements

### Smart Title Generation

If the article lacks an H1 title, `parse_markdown.py` will return `needs_title_generation: true`.

**Claude should automatically:**
1. Read the article content to understand the core message.
2. Generate an engaging title (15-25 characters recommended).
3. Use `--title "Generated Title"` parameter to publish.

### Smart Cover Image Generation

If the article lacks a cover image, `parse_markdown.py` will return `needs_cover_generation: true`.

**Claude should automatically:**
1. Read the article to extract core concepts (1-3 keywords).
2. Call an image generation skill to create a cover image.
3. Insert the generated image path at the beginning of the article as the cover.

---

## Technical Details

### parse_markdown.py Output Format

```json
{
  "title": "Article Title",
  "title_source": "h1",           // "h1", "h2", "first_line", or "none"
  "needs_title_generation": false, // true if no H1 title
  "cover_image": "/path/to/first-image.jpg",
  "needs_cover_generation": false, // true if no cover image
  "content_images": [
    {"path": "/path/to/img2.jpg", "block_index": 5}
  ],
  "html": "<p>Content...</p><h2>Section</h2>...",
  "total_blocks": 45
}
```

**Field Descriptions:**
- `title_source`: Source of the title.
- `needs_title_generation`: Indicates if a better title is needed.
- `needs_cover_generation`: Indicates if a cover image is needed.

## Critical Rules

1. **NEVER auto-publish** - Only save as draft.
2. **NO automatic cover images** - User adds cover manually, never insert the first image as cover.
3. **Clean placeholders** - Remove all remaining `@@@IMG_X@@@` markers after image insertion.
4. **H1 title handling** - H1 is used as title only, not included in body.

## Supported Formatting

- H2 headers (## )
- Blockquotes (> )
- Code blocks (converted to blockquotes)
- Bold text (**)
- Hyperlinks ([text](url))
- Ordered/Unordered lists
- Paragraphs

## Example

User: "Publish /path/to/article.md to X"

```bash
cd ~/.claude/skills/x-article-publisher/scripts
python publish_article.py --file /path/to/article.md
```

Output:
```
📄 Parsing file: /path/to/article.md
  📝 Title: Article Title
  🖼️  Cover Image: /path/to/cover.jpg
  📷 Content Images: 2

🌐 Launching browser...
  📍 Navigating to X Articles...
  🔘 Clicking create button...
  📝 Filling in title...
  📋 Pasting content...

✅ Draft created!
  💡 Please check in the browser and publish manually.
  🖥️ Browser remains open for review...
```

**Technical Reference**: For browser automation debugging tips, see [skill-development-guide](../skill-development-guide/technical-lessons.md).