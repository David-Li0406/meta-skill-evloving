---
name: pdf-translation
description: PDF 遊戲規則轉換與翻譯流程。Use when processing PDF files, extracting content, splitting chapters, or translating game documentation.
---

# PDF Translation Workflow

## Phase 1: Extract PDF

```bash
cd scripts
uv run python extract_pdf.py ../data/pdfs/<filename>.pdf
```

**Outputs** (in `data/markdown/`):
| File | Purpose |
|------|---------|
| `<name>.md` | Clean text (markitdown) |
| `<name>_pages.md` | With `<!-- PAGE N -->` markers |
| `images/<name>/` | Extracted images |

## Phase 2: Configure Chapters

1. Generate template: `uv run python split_chapters.py --init`
2. Edit `chapters.json`:

```json
{
  "source": "data/markdown/<name>_pages.md",
  "output_dir": "docs/src/content/docs",
  "clean_patterns": ["\\(Order #\\d+\\)"],
  "chapters": {
    "section-slug": {
      "title": "章節標題",
      "order": 1,
      "files": {
        "filename": {
          "title": "頁面標題",
          "description": "SEO 描述",
          "pages": [1, 10],
          "order": 0
        }
      }
    }
  }
}
```

3. Split: `uv run python split_chapters.py`

## Phase 3: Translation

For each markdown file in `docs/src/content/docs/`:

1. **Identify terms** - Extract English game terms
2. **Check glossary** - Lookup in `glossary.json`
3. **Translate** - Apply consistent terminology
4. **Preserve structure** - Keep frontmatter, headings, lists intact

### Translation Rules

- Maintain original meaning, avoid over-localization
- Game mechanics terms: use established translations
- Proper nouns: keep original or use accepted translations
- Format: preserve markdown syntax exactly

## Phase 4: Quality Check

| Check | Action |
|-------|--------|
| Terminology | Verify against `glossary.json` |
| Completeness | Compare page count with original |
| Format | Validate frontmatter, links |
| Preview | `cd docs && bun dev` |

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Garbled text | PDF may have non-standard encoding; try different extraction |
| Missing pages | Check `_pages.md` for page markers |
| Broken images | Verify image paths in `images/` folder |
| Format issues | Use `clean_patterns` to remove artifacts |
