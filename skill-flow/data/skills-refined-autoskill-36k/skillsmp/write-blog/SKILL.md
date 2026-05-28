---
name: write-blog
description: 'Guided blog writing and updates: topic ideation/research, outlining, drafting, rewriting, SEO/quality improvements, and (optionally) BatDigest `data/blog.yaml` integration for new posts or refreshes. Use for "write a blog", "draft a blog post", "refresh/update an old blog post", "find a blog topic", or creating an SEO content brief.'
---

# Write Blog

## Overview

Run a structured blog workflow: pick (or discover) a topic, build a brief + outline, draft content, and iterate with improvements. Supports BatDigest publishing prep as an optional final step.

## Workflow Decision Tree

1. Prompt for a workflow number unless the user already made it clear:
   - Ask: `Which blog workflow would you like to run?`
   - `0` - Topic discovery + content brief (no draft)
   - `1` - Draft a new post (outline → draft → SEO pack)
   - `2` - Refresh an existing post (audit → improvements → revised content)
   - `3` - BatDigest publish prep (update `batdigest-flask/data/blog.yaml` + optional local build)
2. If the user asks for “internet research” but network isn’t available, ask them to paste 3–10 source URLs (or excerpts) and proceed from those.

## Common Intake (Ask First)

- Topic (or “suggest topics”)
- Audience (players / parents / coaches)
- Goal + CTA (inform, compare, buy intent, email signup, etc.)
- Must-include facts + sources (links or pasted excerpts)
- Target keyword(s) + what should rank (one page, one intent)
- Constraints (length, tone, publish vs draft, deadline)

## Workflow 0: Topic Discovery + Brief

1. If the user gave a topic: refine it into 2–5 better angles (clear promise, audience, and differentiation).
2. If the user did not give a topic: propose 5 topics with:
   - Working title
   - Target reader + intent
   - Why it’s timely (seasonality, rules, releases, controversy, data update)
   - What BatDigest can add that others won’t (data, testing, clear opinions, tools)
3. Ask the user to pick 1 topic, then produce a content brief:
   - One-sentence thesis
   - H2/H3 outline
   - Data/graphics to include (tables, charts, calculators, checklists)
   - Internal link targets (1–3)
   - SEO pack: title options, slug, meta description, FAQ ideas

## Workflow 1: Draft a New Post

1. Create a brief + outline (Workflow 0 output).
2. Draft the post (Markdown or HTML—ask which), then iterate:
   - Improve clarity, structure, and “so what?”
   - Add concrete examples, comparisons, and decision rules
   - Add a “quick take” (1–2 sentences) and 3–6 key takeaways
   - Run the final-pass checklist in `references/batdigest-quality.md`
3. Deliver a publishable bundle:
   - Final title + slug
   - `blog_summary` (1–2 sentences) + `key_takeaways` list
   - Body content
   - Suggested hero image concept + alt text
   - Internal links list and suggested anchor text

## Workflow 2: Refresh an Existing Post

1. Ask for the URL/slug (or run the helper script below to suggest candidates).
2. Audit the post and propose upgrades:
   - What changed since publish (rules, products, pricing, availability)
   - Where it’s thin (missing comparisons, missing data, unclear CTA)
   - Structure upgrades (better headings, FAQs, tables, internal links)
   - Run the final-pass checklist in `references/batdigest-quality.md`
3. Produce:
   - A short “refresh plan” (what to change and why)
   - Updated `blog_summary` + `key_takeaways`
   - Revised sections (or full rewritten post if requested)

## Workflow 3: BatDigest Publish Prep (blog.yaml)

Assumes repos at `~/Coding_Projects/batdigest-flask` and `~/Coding_Projects/batdigest-static`.

- Source of truth: `~/Coding_Projects/batdigest-flask/data/blog.yaml`
- Blog template renders `post.content` directly (HTML fragment); schema/meta are handled in templates, so avoid embedding extra JSON-LD in `content`.

**Create a new post (preferred):**
- Use BatDigest’s existing script: `~/Coding_Projects/batdigest-flask/scripts/active/blog_yaml_add.py` (writes minimal, append-only changes).

**Refresh an existing post (recommended helpers):**
- List candidates: `scripts/batdigest_blog_candidates.py`
- Extract a post for editing: `scripts/batdigest_blog_extract.py`
- Update a post in-place (minimal diff): `scripts/batdigest_blog_update.py` (dry-run by default)

**Optional local build (no deploy):**
- `cd ~/Coding_Projects/batdigest-flask && source venv/bin/activate && python scripts/active/static_site_generator.py`

## Resources

- `scripts/batdigest_blog_candidates.py`: list/sort refresh candidates from `data/blog.yaml`
- `scripts/batdigest_blog_extract.py`: extract one post’s content/meta for editing
- `scripts/batdigest_blog_update.py`: update one post in-place (minimal diff; dry-run default)
- `references/batdigest-quality.md`: BatDigest voice, SEO, and refresh checklist
