# SEO Article Optimizer

A Claude Code skill for optimizing single articles or landing pages for SEO.

## Features

- **Keyword Analysis** — Placement, density, LSI variations with visual indicators (✅❌⚠️)
- **Readability Metrics** — Flesch score, grade level, sentence length, passive voice, transition words
- **Content Structure** — Heading hierarchy, scanability, paragraph optimization
- **Publishing Assets** — Meta title/description, URL slug, image alt text
- **Internal Linking** — Content-length based formula with anchor text suggestions
- **E-E-A-T Signals** — Trust signals, author bio, citations, schema markup recommendations
- **Featured Snippets** — Definition, list, table, and FAQ snippet opportunities

## Usage

The skill activates when you mention:
- "Help me optimize this article for SEO"
- "Generate meta tags for this page"
- "Improve readability and structure"
- "Target featured snippets"

## Outputs

1. **Structured Report** — 100-point scoring with priority fixes
2. **Optimized Draft** — Markdown preserving original voice
3. **Publishing Assets** — Ready-to-paste meta, slug, alt text
4. **Implementation Checklist** — For editors or engineering

## Files

```
seo-article-optimizer/
├── SKILL.md                              # Main skill definition
├── workflow.md                           # Detailed 7-step workflow
├── reference.md                          # SEO rules and templates
└── templates/
    ├── article-report-template.md        # Report output format
    ├── publish-checklist.md              # Pre-publish checklist
    └── snippet-blocks.md                 # Featured snippet templates
```

## Acknowledgments

This skill was inspired by and incorporates ideas from:
- [OneWave-AI/claude-skills/seo-optimizer](https://github.com/OneWave-AI/claude-skills/tree/main/seo-optimizer)
