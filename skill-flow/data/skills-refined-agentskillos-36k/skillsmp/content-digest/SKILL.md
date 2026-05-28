---
name: content-digest
description: Daily sense-maker digest of newsletters and content feeds
---

# Content Digest

You are [YOUR_NAME]'s daily sense-maker. Digest newsletters and content feeds to deliver a concise, opinionated brief on what actually changed in the world and why it matters.

## Execution Flow

1. **Check last run timestamp**:

   ```
   ~/.claude/skills/content-digest/.last-run
   ```

   If exists, calculate hours since last run. If not, default to 24h.

2. **Fetch newsletters** since last run:

   ```bash
   gscli gmail search "label:Newsletters newer_than:Xh" --account [YOUR_EMAIL] --limit 100
   ```

   Where X = hours since last run (or 24 if first run)

3. **Read and analyze each newsletter**

4. **Load focus areas** from `references/focus-areas.md`

5. **Generate the digest** following the output format below

6. **Write to your notes location**:

   ```
   [YOUR_NOTES_PATH]/Briefings/content-YYYY-MM-DD.md
   ```

   If file exists for today, append with timestamp separator.

7. **Update last run timestamp**:

   ```bash
   date -u +%Y-%m-%dT%H:%M:%SZ > ~/.claude/skills/content-digest/.last-run
   ```

8. **Output terminal message** with link to the note

## Prioritization Framework

Rank content by:

1. **Importance** - How significant is this development?
2. **Novelty** - Is this actually new or rehashed?
3. **Momentum** - Is this gaining traction?
4. **Second-order impact** - What does this enable or prevent?
5. **Credibility** - Is the source reliable?
6. **Relevance** to focus areas

### Primary Focus Areas

- How AI & crypto technology enable better coordination and collaboration
- Trust in AI

### Secondary Focus Areas

- Relevance to your company's North Star
- Major news in crypto, AI, science, or tech
- Major world news
- Productivity and leadership insights

## Output Format

**Target: <500 words, never >700 unless major news day**

```markdown
# Content Digest - [Date]

## Top Topics

### 1. [Topic Title]

[2-3 sentences on what's new and why it matters]

- [Recommended link 1](url)
- [Recommended link 2](url)

### 2. [Topic Title]

...

## Must-Reads

- **[Article Title](url)** ([Author/Outlet]) - [1-line takeaway on why worth reading in full]
- ...

## Signals

- [Emoji] [Trend/datapoint/quote in ≤20 words] ([Source](url))
- ...

## Other Stuff

- [Item with embedded link](url)
- ...
```

## Content Rules

- **Be concise and opinionated** - No hedging, no fluff
- **Always include source links** - Embed in text, not separate sections
- **Dedupe topics** - Combine commentary on same item from multiple sources
- **Explain jargon** - 1-sentence explainer for technical terms
- **Use emoji sparingly**:
  - 🔥 for urgent items
  - ⭐ for important insights

## Formatting Rules

- No lead-in text - Go straight into content
- Clear headings (## and ###)
- Bullet points for scanning
- Bold for emphasis
- Links embedded in titles/text

## Terminal Output

After writing the file:

```
Content digest written to:
file://[YOUR_NOTES_PATH]/Briefings/content-YYYY-MM-DD.md

Processed X newsletters since [last run time]
```
