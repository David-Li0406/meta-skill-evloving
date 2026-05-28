---
name: linkedin-feed-brief
description: Collect and summarize LinkedIn home feed posts using the Playwright MCP. Use when you need to (1) open linkedin.com/feed, (2) extract N feed posts while scrolling, (3) exclude ads/"Promoted" and non-post modules (jobs, in-app promotions), and (4) produce a grouped brief with keywords, per-post core title + insight, and a source link (prefer permalink; fallback to URN-based feed/update URL).
---

# LinkedIn Feed Brief (Playwright MCP)

## Goal

Collect up to N LinkedIn feed posts reliably (collection is primary), filter out ads/modules, and output a brief in the user’s format:
`<Overall Title>` then `(Category(Keywords + (Title + Author + Posted Date + Summary + Link)*N))*M`.

Title guidance:
- Create a witty, feed-wide umbrella title, **or** pick one hooky theme that would make people stop scrolling on SNS.
- Keep it short (ideally 1 line) and specific (hint at a tension/tradeoff/trend).
- Avoid the word `AI` in the title (too obvious); use concrete nouns (e.g., agents, automation, governance, workflow) instead.

## Workflow

### 1) Navigate

- Use Playwright MCP to navigate to `https://www.linkedin.com/feed/`.
- If redirected to login, stop and ask the user to log in first.

### 2) Validate you are on the feed

- Confirm URL contains `/feed/` and the page shows the main nav + feed layout.
- If unsure, take a Playwright snapshot and verify the center column is the infinite scroll feed.

### 3) Collect posts (primary)

- Run the JS snippet in `scripts/extract_feed_posts.browser_run_code.js` via Playwright `browser_run_code`.
- Default: collect `N=20` unique posts by `data-urn`.
- Prefer DOM permalink (`/feed/update/...`); fallback to URN link if missing.

If collection returns 0 or times out:
- Avoid reading full `innerText` for large containers.
- Increase waits between scrolls (LinkedIn lazy-loads heavily).
- Click “New posts” if present, then retry.

### 4) Filter (required)

- Exclude “Promoted” posts.
- Exclude non-post modules like job cards and in-app promotions.
- Exclude Employment / job-change posts and **do not count them toward N**.
- Apply rules in `references/api_reference.md`.

### 5) Normalize links (required)

- **Preferred:** DOM permalink extracted from the post.
- **Fallback:** `https://www.linkedin.com/feed/update/{URN}/`

### 6) Write the brief (secondary)

- Categorize posts using the fixed taxonomy in `references/api_reference.md`.
- Choose the output language based on the dominant language of the collected posts:
  - If the majority of posts are written in Korean, write the brief in Korean.
  - Otherwise, write the brief in English.
- Save the final brief to a `.txt` file (in addition to printing it in chat).
- For each category:
  - `Keywords`: 3–5 items, **plain text only** (no emojis inside the keyword list). Use ` · ` as the separator.
  - Emoji rule: Put **one** emoji before the `Keywords:` label (e.g. `🧠 Keywords:`) and **do not reuse** that emoji across categories within the same brief.
    - Example: `🧠 Keywords: k1 · k2 · k3`, `🧰 Keywords: k1 · k2 · k3`, `📈 Keywords: k1 · k2 · k3`
  - Category naming rule:
    - If the category is `ETC`, include a best-guess candidate label in parentheses.
  - Post numbering rule:
    - Number posts **within each category** as `1)`, `2)`, `3)`... and restart numbering at `1)` for each new category.
  - For each post: `Title` + `Author` + `Posted Date` + `1~2 sentence summary` + `Link`
    - Posted Date rule:
      - If the feed only provides relative times (e.g. `18h`, `4 days ago`), convert it to an **absolute local timestamp** by comparing against the script execution time, using the **system timezone** by default (unless the user specifies otherwise).
      - Output `Posted Date` as absolute when possible (e.g. `2026-01-15 09:42`); otherwise fall back to relative (e.g. `4 days ago`).
  - Post formatting rules:
    - Write the `Title (Author, Posted Date)` line, then put the summary on the **next line** (no extra blank line between title and summary).
    - Put **one blank line between posts** within the same category.
- Use `assets/example_asset.txt` as the output shape.

## Output format (must match)

```
<Overall Title>

🧩 Category Name

🧠 Keywords: k1 · k2 · k3 · ...
1) Title (Author, Posted Date)
- 1~2 sentence summary
(link)

2) Title (Author, Posted Date)
- 1~2 sentence summary
(link)
...
```

## Notes / Guardrails

- Only collect what is visible on the page.
- If LinkedIn UI changes, update selectors and the extraction snippet first.
