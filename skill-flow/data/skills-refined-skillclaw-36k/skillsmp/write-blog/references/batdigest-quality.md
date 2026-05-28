# BatDigest Blog: Quality + SEO Checklist

Use this as a “final pass” checklist after drafting (or when auditing an older post).

## Voice / Standards

- Be direct, practical, and data-first (avoid fluff).
- Make claims only when you can support them (internal data, reputable sources, or clear reasoning).
- Prefer specific, testable statements over hype (“X tends to feel stiffer than Y” + why).
- Keep the reader’s decision in mind: what should they do next?

## Structure Blueprint

- Open with a clear promise (what the reader will learn/decide).
- Use scannable H2/H3 sections; each section should answer one question.
- Include at least one of: table, checklist, decision tree, or “if/then” rules.
- Close with a short recommendation summary + CTA.

## “BatDigest-Level” Differentiators (Ideas)

- A simple decision framework (who should buy/avoid, based on constraints).
- Comparisons that match intent (price, swing feel, durability, legality, availability).
- Data hooks: exit velocity by age, year-over-year changes, league rules, or test notes.
- Internal links that keep users moving (1–3 highly relevant links, not a link dump).

## SEO / UX Pass

- One primary query/intent per post; don’t split into multiple unrelated posts in one.
- Title: specific + benefit + (year) if it matters.
- Meta description: 140–160 chars, matches intent, no clickbait.
- Headings: include intent language (“Best…”, “Is it legal…”, “How to choose…”).
- Add an FAQ section if it’s natural (3–6 short Q/A blocks).
- Images: use descriptive alt text; avoid huge inline styles.

## Refresh Pass (Existing Posts)

- Identify what changed: rules, product lineups, bans/approvals, pricing, availability.
- Update “year” references (and ensure the content still matches the title).
- Replace weak sections with: clearer comparisons, updated data, or a better framework.
- Fix broken/outdated links; improve internal linking to current pillar pages.
- Update `blog_summary` + `key_takeaways` to reflect the new state of the article.

## BatDigest `blog.yaml` Notes

- `content` should be an HTML fragment (no full-page `<html>` wrappers).
- Avoid embedding extra JSON-LD inside `content` (templates add schema automatically).
- Use `class="img-fluid"` on images when embedding in the article body.
