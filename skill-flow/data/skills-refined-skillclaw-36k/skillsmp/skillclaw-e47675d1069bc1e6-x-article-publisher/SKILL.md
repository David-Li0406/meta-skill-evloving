---
name: x-article-publisher
description: Use this skill to publish Markdown articles to X (Twitter) Articles editor with proper formatting, especially when you want to share content on X or need assistance with X Premium article publishing.
---

# X Article Publisher

Publish Markdown content to X (Twitter) Articles editor, preserving formatting with rich text conversion.

## Prerequisites

- X Premium Plus subscription
- Python 3.9+ with dependencies:
  - macOS: `pip install Pillow pyobjc-framework-Cocoa patchright`
  - Windows: `pip install Pillow pywin32 clip-util`

## 🎉 First Use: One-Time Authentication

**X Article Publisher now supports persistent authentication, eliminating the need for repeated logins!**

### 🔧 Initialize Authentication (One-Time Setup)

Before first use, run the authentication setup:

```bash
cd ~/.claude/skills/x-article-publisher/scripts
python auth_manager.py setup
```

**Process:**
1. ✅ A browser window will automatically open to the X login page.
2. 🔐 Manually log in to your X account (Premium+ subscription required).
3. ✅ Complete 2FA verification (if enabled).
4. 🏠 After successful login, you will be redirected to your Home timeline.
5. 💾 Authentication status is automatically saved (valid for 7 days).

### 📋 Authentication Management Commands

```bash
# Check authentication status
python auth_manager.py status

# Validate if authentication is still valid
python auth_manager.py validate

# Clear authentication data (requires re-login)
python auth_manager.py clear

# Re-authenticate (clear + setup)
python auth_manager.py reauth
```

### 🚀 Automated Workflow

Once authentication is set up, the skill will automatically:
1. ✅ Check authentication status.
2. 🔓 If authenticated, use the saved browser state (no login required).
3. ⚠️ If not authenticated, prompt to run `auth_manager.py setup`.

**Note**: Authentication data is stored in `~/.claude/skills/x-article-publisher/data/browser_state/`, excluded from Git via .gitignore.

## Scripts

Located in `~/.claude/skills/x-article-publisher/scripts/`:

### publish_article.py (Main Script - One-Click Publish)
**Recommended Use** - Automatically completes all publishing steps:
```bash
# Basic usage (default shows browser)
python publish_article.py --file article.md

# Hide browser (run in background)
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

## Workflow (Simplified)

**Prerequisite**: Authentication setup completed (`python auth_manager.py setup`).

### 🚀 One-Click Publish (Recommended)

Run `publish_article.py` directly to automatically complete all steps:

```bash
cd ~/.claude/skills/x-article-publisher/scripts
python publish_article.py --file article.md
```