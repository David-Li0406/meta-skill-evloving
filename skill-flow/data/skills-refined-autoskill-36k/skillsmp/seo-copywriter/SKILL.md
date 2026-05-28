---
name: seo-copywriter
description: SEO-optimized copywriting for web content. Use when writing or improving landing pages, blog posts, product descriptions, meta tags, or any web copy. Includes text analysis script for keyword density, readability, power words, and SEO metrics. Trigger on requests for "SEO copy", "web content", "landing page copy", "meta description", or when analyzing existing copy for SEO.
---

# SEO Copywriter

Write conversion-focused, search-optimized web content.

## Workflow

1. **Clarify** - target keyword, audience, content type, tone
2. **Write** - apply SEO principles below
3. **Analyze** - run `scripts/analyze.py` on draft
4. **Refine** - address recommendations, re-analyze

## SEO Writing Principles

### Keywords
- Primary keyword in: first 100 words, H1, 1-2 subheadings, conclusion
- Keyword density: 1-2% (script checks this)
- Use LSI (related) keywords naturally
- Never stuff - write for humans first

### Structure
- H1: one per page, include primary keyword
- H2/H3: logical hierarchy, keywords where natural
- Paragraphs: 2-4 sentences max for web
- Sentences: avg 15-20 words, vary length
- Bullet points for scannable content

### Readability
- Target Flesch-Kincaid grade 6-8 for general audience
- Use active voice (aim <15% passive)
- Simple words over complex alternatives
- Break long sentences

### Engagement
- Questions engage readers
- Power words trigger emotion (see `references/power-words.md`)
- Address reader directly ("you", "your")
- Include CTAs

### Meta Content
| Element | Length | Notes |
|---------|--------|-------|
| Title tag | 50-60 chars | Primary keyword near start |
| Meta description | 150-160 chars | Include keyword, CTA |
| URL slug | 3-5 words | Hyphenated, keyword |
| H1 | 20-70 chars | Match/relate to title |

## Analysis Script

Run after writing to check metrics:

```bash
# From file
python3 scripts/analyze.py content.txt

# From clipboard (macOS)
pbpaste | python3 scripts/analyze.py -

# Pipe text
echo "Your content here" | python3 scripts/analyze.py -
```

**Script checks:**
- Word count, frequency, percentages
- Character count (with/without spaces)
- Word pairs & triples (find repeated phrases)
- Sentence/paragraph length stats
- Flesch-Kincaid readability
- Passive voice percentage
- Power word density
- Question count
- Automated recommendations

## Content-Type Guidelines

### Landing Pages
- Lead with benefit, not feature
- One primary CTA above fold
- Social proof near CTA
- Address objections
- Urgency without being pushy

### Blog Posts
- Hook in first sentence
- Deliver value promised in title
- Internal linking to related content
- End with CTA or next step

### Product Descriptions
- Benefits > features (but include both)
- Sensory language
- Overcome objections
- Include specs for SEO

## References

- `references/power-words.md` - Categorized power words for emotional triggers
