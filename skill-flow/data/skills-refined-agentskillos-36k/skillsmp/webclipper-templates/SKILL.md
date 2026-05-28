---
name: webclipper-templates
description: Web Clipper template management for ADHD-friendly capture workflow. Single universal template with zero-decision capture, automatic classification, and deferred organization. Use for template installation, understanding the capture pipeline, or troubleshooting Web Clipper issues.
---

# Web Clipper Templates

**ADHD-friendly web clipping: Capture now, organize later.**

---

## Philosophy

Traditional web clippers require decisions at capture time:
- Which template to use?
- Is this a recipe or an article?
- Should I tag it now?

This cognitive load fights against ADHD brains. Our approach: **capture everything with zero decisions, classify automatically during review.**

---

## The Single Template Approach

One template (`capture.json`) captures everything to `00 Inbox/` with minimal metadata:

```yaml
type: clipping
source: <url>
clipped: <date>
domain: <domain>
distill_status: raw
```

No decisions required. No analysis paralysis. Just capture.

---

## Classification Pipeline

```
Capture          →    para scan     →   para enrich   →   para execute
(Web Clipper)         (classify)        (transcripts)     (templates)
```

### 1. Capture (Web Clipper)
- Use single Capture template
- Zero decisions required
- All clips go to `00 Inbox/`

### 2. Classify (para scan)
Automatic detection from URL patterns and content:

| Type | Detected From |
|------|---------------|
| 🎬 youtube | youtube.com, youtu.be |
| 🐙 github | github.com |
| 💬 social | twitter.com, reddit.com |
| 📚 documentation | docs.*, developer.* |
| 🍳 recipe | Recipe sites, ingredients |
| 🛍️ product | amazon, ebay, prices |
| 🎧 podcast | spotify episodes, apple podcasts |
| 📖 book | goodreads |
| 📰 article | Default for articles |
| ✂️ generic | Fallback |

### 3. Review Prompt
During interactive review, you're asked:
> "Why did you save this? (Enter to skip)"

Optional - stored in frontmatter as `capture_reason`.

### 4. Enrich (para enrich)
- YouTube clips get transcripts (via Firecrawl)
- Bookmark clips get full page content
- Other enrichments as needed

### 5. Execute (para execute)
- Apply vault templates
- Add emoji prefixes
- Move to final location

---

## Installing the Template

1. Open Obsidian Web Clipper settings
2. Go to Templates section
3. Import `capture.json`
4. Set as default template

---

## Template Location

```
plugins/para-obsidian/templates/webclipper/capture.json
```

---

## Archived Templates

Previous 15 specialized templates are in `archived/` for reference.
They were replaced to reduce decision fatigue at capture time.

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| Template won't import | Check JSON syntax with `jq` |
| Clippings not in inbox | Verify path is set to `00 Inbox` |
| Missing metadata | Re-import template (Web Clipper caches) |

---

## Technical Notes

### JSON Template Structure

```json
{
  "schemaVersion": "0.1.0",
  "name": "Capture",
  "behavior": "create",
  "noteNameFormat": "{{domain|safe_name|trim}} {{date:YYYY-MM-DD-HHmmss}}",
  "path": "00 Inbox",
  "noteContentFormat": "# {{title}}\n\nContent here...",
  "properties": [
    {
      "name": "type",
      "value": "clipping",
      "type": "text"
    }
  ]
}
```

### Filter Syntax Quick Reference

```
{{variable|filter}}
{{variable|filter1|filter2}}              # Chained filters
{{variable|filter:"arg"}}                 # Filter with argument
{{variable|replace:"search":"replace"}}   # Simple replacement
{{variable|replace:"/regex/":"replace"}}  # Regex replacement
```

### Common Filters

- `safe_name` - Convert to safe filename
- `trim` - Remove leading/trailing whitespace
- `date:"YYYY-MM-DD"` - Format date
- `replace:"search":"replace"` - Replace text

**CRITICAL:** Always add `|trim` after `|safe_name` in noteNameFormat to prevent trailing whitespace.

---

## References

For advanced usage and troubleshooting:

- **Filter syntax**: `./references/filter-syntax.md` - Complete filter reference
- **Export script**: `./references/export-script.cjs` - Template export utility
- **Troubleshooting**: `./references/troubleshooting.md` - Detailed debugging guide

---

## Official Documentation

- Templates: https://help.obsidian.md/web-clipper/templates
- Variables: https://help.obsidian.md/web-clipper/variables
- Filters: https://help.obsidian.md/web-clipper/filters
