---
name: thought-writer
description: Create new "thought" entries - quick insights, observations, or reflections. Use when the user says "add a thought", "new thought", "write a thought", or mentions wanting to capture a quick insight or observation.
allowed-tools:
  - Write
  - Read
  - Bash
---

# Thought Writer

This skill creates new "thought" entries - short-form insights, observations, or philosophical reflections. Thoughts are the minimal content type on the site: just a date and a few sentences.

## File Location

Create new thoughts in: `src/content/thoughts/`

## Filename Format

Use the format `YYMMDD.md` where:
- `YY` = 2-digit year (e.g., `25` for 2025)
- `MM` = 2-digit month (e.g., `01`, `12`)
- `DD` = 2-digit day (e.g., `05`, `31`)

Example: `260114.md` for January 14, 2026

## Frontmatter Schema

```yaml
---
date: YYYY-MM-DD
draft: false  # optional, defaults to false
author: Nikola Balić  # optional, defaults to Nikola Balić
---
```

The `date` field is **required** and must be in ISO format (YYYY-MM-DD).

**Note**: Thoughts have minimal frontmatter - no title, description, tags, or topics. Just the date.

## Content Style Guidelines

Thoughts are short-form, blockquote-style content:

- **Length**: Single sentence to a few paragraphs
- **Tone**: Philosophical, observational, reflective
- **Style**: No section headings (unlike now entries)
- **Format**: Can include simple ASCII art or diagrams if relevant
- **Rendering**: Thoughts appear as blockquotes on the site

Think of thoughts as filling the gap between tweets (too short/ephemeral) and blog articles (too structured/long).

## Examples

**Single sentence:**
```markdown
---
date: 2025-05-26
---

The only way you're going to figure this out is by getting your hands dirty and seeing what works.
```

**Philosophical observation:**
```markdown
---
date: 2025-05-23
---

Human requests are binary: fix this thing, answer this question. But agents operate in probabilistic space, spawning subprocess after subprocess, each one justified by some internal logic tree I never asked for. The billing model assumes perfect alignment between what I want and what the machine thinks I need. Spoiler: there isn't any.
```

**With ASCII diagram:**
```markdown
---
date: 2025-06-07
---

Hear me out: "Adversarial Pair Coding with AI Agents" -- feels nice, keeps me in the flow and velocity is immense!

<pre>
+----------------------------+
|        Coder Agent        |
| - Generates Code          |
| - Learns patterns         |
| - Optimizes logic         |
+----------------------------+
             |
+----------------------------+
|   Shared Understanding     |
| - Language rules           |
| - Functional goals         |
| - Iterative improvement    |
+----------------------------+
             |
+----------------------------+
|     Adversary Agent       |
| - Finds bugs              |
| - Suggests attacks        |
| - Tests edge cases        |
+----------------------------+
</pre>
```

**Quote with reflection:**
```markdown
---
date: 2025-07-28
---

"Play long-term games with long-term people." — Naval Ravikant

This hits different when someone extracts value from you, then actively works to devalue you.

Long-term games compound. Trust compounds. Reputation compounds.
```

## When to Use Thoughts vs Other Content Types

| Type | When to use | Format |
|------|-------------|--------|
| **Thought** | Quick insight, observation, philosophical reflection | 1 paragraph, minimal frontmatter |
| **Now Entry** | Life update with multiple focus areas | ## sections, YYMMDD.md |
| **Article** | Full blog post with narrative/technical depth | Complete frontmatter (title, tags, etc.), kebab-case filename |

## Process

When the user wants to add a thought:

1. **Determine today's date** for the filename (YYMMDD.md) and frontmatter (YYYY-MM-DD)
2. **Ask what insight or observation** they want to capture
3. **Draft the content** keeping it short and focused
4. **Create the file** in `src/content/thoughts/`
5. **Confirm creation** with the user

## How It Works

- Thoughts appear on the homepage (`/`) in the main feed
- Integrated with search at `/search`
- Displayed as blockquotes with date and "Thought" label
- Sorted chronologically (newest first)
