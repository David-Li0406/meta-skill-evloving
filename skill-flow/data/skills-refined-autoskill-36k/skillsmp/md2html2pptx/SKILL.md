---
name: md2html2pptx
description: Markdown to HTML to PowerPoint presentation converter using html2pptx library. Use when creating slide presentations from markdown content, generating HTML slides with strict layout constraints for PPTX conversion, or building PowerPoint files from HTML templates. Triggers on requests to create presentations, slides, PPTX files, or convert markdown to slides.
---

# md2html2pptx

Convert Markdown content to HTML slides, then to PowerPoint presentations.

## Project Setup

`/md2html2pptx setup` を実行する。詳細は [setup.md](scripts/setup.md) を参照。

## Workflow

1. **Markdown → HTML**: Generate HTML slides from markdown in `1_mds/`
2. **Preview**: View slides in browser to verify layout
3. **HTML → PPTX**: Convert HTML slides to PowerPoint

## Slash Commands

| Command | Description |
|---------|-------------|
| `/md2html2pptx setup` | Initial project setup (see [setup.md](scripts/setup.md)) |
| `/md2html2pptx to_html <file>` | Generate HTML slides from markdown (see [to_html.md](scripts/to_html.md)) |
| `/md2html2pptx preview` | Preview slides in browser with validation (see [preview.md](scripts/preview.md)) |
| `/md2html2pptx to_pptx [filter]` | Build PPTX from HTML slides (see [to_pptx.md](scripts/to_pptx.md)) |

## Directory Structure

```
project/
├── package.json              # npm dependencies
├── 1_mds/                    # Markdown source files
├── 2_htmls/                  # HTML slide templates
└── 3_pptxs/                  # Generated PPTX files
```

## Build Commands

```bash
npm run to_html -- 1_mds/sample.md   # Markdown → HTML
npm run preview                       # Browser preview with validation
npm run preview -- part1              # Preview filtered slides
npm run to_pptx                       # HTML → PowerPoint (all)
npm run to_pptx -- part1              # HTML → PowerPoint (filtered)
```

## html2pptx Function

```javascript
const { slide, placeholders } = await html2pptx("slides/example.html", pptx);
```

Returns slide object and placeholder positions for PptxGenJS charts/tables.

## Critical Rules

- **Slide size**: 960px × 540px (16:9)
- **Text wrapping**: All text must be in `<p>`, `<h1>`-`<h6>`, `<ul>`, `<ol>`
- **No bullets in p**: Never start `<p>` with `-`, `•`, `*`
- **Flex widths**: Use fixed width (e.g., `width: 380px`) for flex children

## Troubleshooting

```bash
npm install
npx playwright install chromium
```
