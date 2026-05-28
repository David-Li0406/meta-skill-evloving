---
name: w0x7ce-post-to-linkedin
description: Post content to LinkedIn. Supports text posts and images. Uses Chrome CDP automation. Supports English, Simplified Chinese, Traditional Chinese.
---

# Post to LinkedIn

Post content and images to LinkedIn using Chrome CDP automation.

## Script Directory

**Important**: All scripts are located in the `scripts/` subdirectory of this skill.

**Agent Execution Instructions**:
1. Determine this SKILL.md file's directory path as `SKILL_DIR`
2. Script path = `${SKILL_DIR}/scripts/<script-name>.ts`
3. Replace all `${SKILL_DIR}` in this document with the actual path

**Script Reference**:
| Script | Purpose |
|--------|---------|
| `scripts/linkedin-browser.ts` | Create and publish posts |

## Prerequisites

- Google Chrome installed
- `bun` installed (for running scripts)
- LinkedIn account (first run requires login)

## Usage

### Create Text Post

```bash
# Preview mode (doesn't publish)
npx -y bun ${SKILL_DIR}/scripts/linkedin-browser.ts "Hello LinkedIn!"

# Actually publish
npx -y bun ${SKILL_DIR}/scripts/linkedin-browser.ts "Excited to share!" --submit
```

### Create Post with Images

```bash
# Post with single image
npx -y bun ${SKILL_DIR}/scripts/linkedin-browser.ts "Check this out" --image ./photo.jpg --submit

# Post with multiple images
npx -y bun ${SKILL_DIR}/scripts/linkedin-browser.ts "Multiple photos" --image ./a.jpg --image ./b.jpg --submit
```

## Parameters

| Parameter | Description |
|-----------|-------------|
| `<text>` | Post content (positional argument) |
| `--image <path>` | Image file path (can be repeated) |
| `--submit` | Publish post (default: preview only) |
| `--profile <dir>` | Custom Chrome profile directory |

## Posting Workflow

1. **Launch Chrome**: Opens Chrome with LinkedIn feed page (`https://www.linkedin.com/feed/`)
2. **Login**: First run requires manual login (session saved)
3. **Click "Start a post"**: Clicks the post creation button
4. **Fill Content**: Types text content into the editor
5. **Add Images**: Uploads images if specified
6. **Preview or Submit**: Either preview or publish

## Content Tips

### Text Content
- LinkedIn posts can be up to 3,000 characters
- Use line breaks for readability
- Include relevant hashtags

### Example

```bash
npx -y bun ${SKILL_DIR}/scripts/linkedin-browser.ts "Just finished an amazing project!

We successfully launched our new product after months of hard work. 🚀

#productlaunch #teamwork #innovation" --submit
```

### Images
- Supported formats: JPG, PNG, GIF
- Recommended size: 1200x627 pixels
- Max file size: 5MB per image

## Multi-language Support

The skill supports LinkedIn's multiple interface languages:

- English
- Simplified Chinese (简体中文)
- Traditional Chinese (繁體中文)

## Troubleshooting

- **Not logged in**: First run opens browser - log in manually
- **Chrome not found**: Set `LINKEDIN_BROWSER_CHROME_PATH` environment variable
- **Post button not found**: Make sure you're on the feed page
- **Session expired**: Delete profile directory and login again

## Extension Support

Custom configurations via EXTEND.md.

**Check paths** (priority order):
1. `.w0x7ce-skills/w0x7ce-post-to-linkedin/EXTEND.md` (project)
2. `~/.w0x7ce-skills/w0x7ce-post-to-linkedin/EXTEND.md` (user)

If found, load before workflow. Extension content overrides defaults.
