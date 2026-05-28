---
name: w0x7ce-post-to-tencent-docs
description: Post content to Tencent Docs (腾讯文档). Supports creating new documents with title and content. Uses Chrome CDP automation. Supports Simplified Chinese, Traditional Chinese, English.
---

# Post to Tencent Docs (腾讯文档)

Post content and create new documents on Tencent Docs using Chrome CDP automation.

## Script Directory

**Important**: All scripts are located in the `scripts/` subdirectory of this skill.

**Agent Execution Instructions**:
1. Determine this SKILL.md file's directory path as `SKILL_DIR`
2. Script path = `${SKILL_DIR}/scripts/<script-name>.ts`
3. Replace all `${SKILL_DIR}` in this document with the actual path

**Script Reference**:
| Script | Purpose |
|--------|---------|
| `scripts/tencent-docs-browser.ts` | Create and publish documents |
| `scripts/cdp.ts` | Chrome CDP utilities |

## Prerequisites

- Google Chrome installed
- `bun` installed (for running scripts)
- Tencent account (first run requires login)

## Usage

### Create New Document

```bash
# Preview mode (doesn't publish)
npx -y bun ${SKILL_DIR}/scripts/tencent-docs-browser.ts --title "文档标题" --content "文档内容"

# Actually publish/share
npx -y bun ${SKILL_DIR}/scripts/tencent-docs-browser.ts --title "文档标题" --content "文档内容" --submit
```

### From Markdown File

```bash
# Create document from markdown
npx -y bun ${SKILL_DIR}/scripts/tencent-docs-browser.ts --markdown article.md --submit
```

### From File Content

```bash
# Create document with content from file
npx -y bun ${SKILL_DIR}/scripts/tencent-docs-browser.ts --title "标题" --file content.txt --submit
```

## Parameters

| Parameter | Description |
|-----------|-------------|
| `--title <text>` | Document title (required) |
| `--content <text>` | Document content (required) |
| `--markdown <path>` | Create from Markdown file |
| `--file <path>` | Read content from text file |
| `--submit` | Publish/share document (default: preview only) |
| `--profile <dir>` | Custom Chrome profile directory |
| `--type <type>` | Document type: `doc` (Word), `sheet` (Excel), `slide` (PPT). Default: `doc` |

## Document Types

Tencent Docs supports multiple document types:

| Type | Name | URL | Status |
|------|------|-----|--------|
| `doc` | Word Document | `doc.weixin.qq.com` | ✅ **Implemented** |
| `sheet` | Excel Spreadsheet | `doc.weixin.qq.com` | ⏳ TODO |
| `slide` | PowerPoint Presentation | `doc.weixin.qq.com` | ⏳ TODO |

### Word Documents (doc) ✅

**Fully Implemented**

- Rich text content
- Multi-line support
- Auto-publishing/sharing

```bash
npx -y bun ${SKILL_DIR}/scripts/tencent-docs-browser.ts \
  --title "项目文档" \
  --content "这是文档内容

支持多行文本。" \
  --submit
```

## Posting Workflow

1. **Launch Chrome**: Opens Chrome with Tencent Docs home page (`https://doc.weixin.qq.com/home/recent`)
2. **Login**: First run requires QR code scan (session saved)
3. **Click "新建" (New)**: Clicks the new document button
4. **Click "文档" (Document)**: Selects document type from menu
5. **New Tab Opens**: A new tab opens with the blank document
6. **Fill Title**: Types title into the title field
7. **Fill Content**: Types content into the document body
8. **Preview or Submit**: Either preview or leave open for sharing

## Markdown Format

When using `--markdown`, the script extracts:

```markdown
# Title (becomes document title)

Content description here...

## Subsections (optional)

More content...

### Lists (optional)

- Item 1
- Item 2

**Bold** and *italic* text supported.
```

## Content Tips

### Title (标题)
- Keep it descriptive but concise
- Use keywords for easy searching

### Content (内容)
- Detailed description
- Use line breaks for readability
- Supports basic formatting

### Example

```bash
npx -y bun ${SKILL_DIR}/scripts/tencent-docs-browser.ts \
  --title "会议记录 - 2024年项目规划" \
  --content "会议时间：2024年1月15日
参会人员：产品团队、开发团队

主要议题：
1. 产品功能规划
2. 技术架构讨论
3. 时间线安排

决议事项：
- 确定Q1发布计划
- 启动技术重构" \
  --submit
```

## Multi-language Support

The skill supports Tencent Docs' multiple interface languages:

- Simplified Chinese (简体中文)
- Traditional Chinese (繁體中文)
- English

## Troubleshooting

- **Not logged in**: First run opens browser - scan QR code to log in
- **Chrome not found**: Set `TENCENT_DOCS_CHROME_PATH` environment variable
- **Title too long**: Tencent Docs may have title length limits
- **Session expired**: Delete profile directory and login again

## Extension Support

Custom configurations via EXTEND.md.

**Check paths** (priority order):
1. `.w0x7ce-skills/w0x7ce-post-to-tencent-docs/EXTEND.md` (project)
2. `~/.w0x7ce-skills/w0x7ce-post-to-tencent-docs/EXTEND.md` (user)

If found, load before workflow. Extension content overrides defaults.
