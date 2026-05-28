---
name: w0x7ce-post-to-rednote
description: Post content to Xiaohongshu (Little Red Book / RED). Supports posting images with title and content. Uses Chrome CDP automation. Supports Traditional Chinese.
---

# Post to Xiaohongshu (Little Red Book / RED)

Post content with images to Xiaohongshu using Chrome CDP automation.

## Script Directory

**Important**: All scripts are located in the `scripts/` subdirectory of this skill.

**Agent Execution Instructions**:
1. Determine this SKILL.md file's directory path as `SKILL_DIR`
2. Script path = `${SKILL_DIR}/scripts/<script-name>.ts`
3. Replace all `${SKILL_DIR}` in this document with the actual path

**Script Reference**:
| Script | Purpose |
|--------|---------|
| `scripts/rednote-browser.ts` | Main posting script (images + text) |
| `scripts/cdp.ts` | Chrome CDP utilities |
| `scripts/copy-to-clipboard.ts` | Copy images to clipboard |

## Prerequisites

- Google Chrome installed
- `bun` installed (for running scripts)
- Xiaohongshu account (first run requires login)

## Usage

### Basic Post

```bash
# Preview mode (doesn't post)
npx -y bun ${SKILL_DIR}/scripts/rednote-browser.ts --title "标题" --content "内容描述" --image ./photo1.png --image ./photo2.png

# Actually post
npx -y bun ${SKILL_DIR}/scripts/rednote-browser.ts --title "标题" --content "内容描述" --image ./photo1.png --image ./photo2.png --submit
```

### From Markdown File

```bash
# Post images with extracted title and content
npx -y bun ${SKILL_DIR}/scripts/rednote-browser.ts --markdown article.md --images ./photos/ --submit
```

### With Hashtags

```bash
# Add hashtags to content
npx -y bun ${SKILL_DIR}/scripts/rednote-browser.ts --title "标题" --content "内容描述 #标签1 #标签2" --image ./photo.png --submit
```

## Parameters

| Parameter | Description |
|-----------|-------------|
| `--title <text>` | Post title (required) |
| `--content <text>` | Post content/description (required) |
| `--markdown <path>` | Markdown file to extract title/content |
| `--image <path>` | Image file path (can repeat, min 1) |
| `--images <dir>` | Directory containing images |
| `--submit` | Actually post (default: preview only) |
| `--profile <dir>` | Custom Chrome profile directory |
| `--topic <text>` | Topic/Category (optional) |

## Posting Workflow

1. **Launch Chrome**: Opens Chrome with Xiaohongshu creator platform
2. **Login**: First run requires QR code scan (session saved)
3. **Navigate to Post**: Opens the content creation page
4. **Fill Title**: Types title character by character
5. **Upload Images**: Uploads all provided images
6. **Fill Content**: Types content/description
7. **Preview or Submit**: Either preview or submit for publishing

## Image Guidelines

Xiaohongshu image requirements:
- **Format**: JPG, PNG
- **Ratio**: 3:4 recommended (portrait)
- **Count**: 1-9 images per post
- **Size**: Under 10MB per image

## Content Tips

### Title (标题)
- Keep it concise (under 20 characters recommended)
- Use emojis to attract attention
- Include keywords for search

### Content (内容)
- Detailed description (500-1000 characters)
- Use line breaks for readability
- Add relevant hashtags (#标签)
- Call to action at the end

### Example

```bash
npx -y bun ${SKILL_DIR}/scripts/rednote-browser.ts \
  --title "今日穿搭分享 👗" \
  --content "今天分享一套超级好看的春日穿搭！

#OOTD #春日穿搭 #时尚分享" \
  --image ./outfit1.png \
  --image ./outfit2.png \
  --image ./outfit3.png \
  --submit
```

## Markdown Format

When using `--markdown`, the script extracts:

```markdown
# Title (becomes post title)

Content description here...

## Subsections (optional)

More content...

#hashtag1 #hashtag2
```

## Post Types

Xiaohongshu supports three different post types:

| Type | Status | URL |
|------|--------|-----|
| **图文** (Image/Text) | ✅ **Implemented** | `?target=image` |
| **视频** (Video) | ⏳ TODO | `?target=video` |
| **文章** (Article) | ⏳ TODO | `?target=article` |

### Image/Text Posts (图文) ✅

**Fully Implemented**

- Supports 1-9 images per post
- Title + content/description
- Hashtags support
- Auto-publishing

```bash
npx -y bun ${SKILL_DIR}/scripts/rednote-browser.ts \
  --title "标题" \
  --content "内容描述" \
  --image ./photo.png \
  --submit
```

### Video Posts (视频) ⏳ TODO

**Not yet implemented**

Will support:
- Video file upload (MP4, MOV, etc.)
- Title + description
- Cover image selection
- Duration limits (60 min for regular users)

Target URL: `https://creator.xiaohongshu.com/publish/publish?from=tab_switch&target=video`

### Article Posts (文章) ⏳ TODO

**Not yet implemented**

Will support:
- Long-form content (markdown to HTML)
- Multiple inline images
- Rich formatting
- Cover image

Target URL: `https://creator.xiaohongshu.com/publish/publish?from=tab_switch&target=article`

## Multi-language Support

The skill supports Xiaohongshu's multiple interface languages:

- Simplified Chinese (简体中文)
- Traditional Chinese (繁體中文)
- English

## Troubleshooting

- **Not logged in**: First run opens browser - scan QR code to log in
- **Chrome not found**: Set `REDNOTE_BROWSER_CHROME_PATH` environment variable
- **Image upload fails**: Check image format and size requirements
- **Title too long**: Xiaohongshu limits title to ~20 characters
- **Session expired**: Delete profile directory and login again

## Extension Support

Custom configurations via EXTEND.md.

**Check paths** (priority order):
1. `.w0x7ce-skills/w0x7ce-post-to-rednote/EXTEND.md` (project)
2. `~/.w0x7ce-skills/w0x7ce-post-to-rednote/EXTEND.md` (user)

If found, load before workflow. Extension content overrides defaults.
