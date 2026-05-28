---
name: now-writer
description: Create new "now" page entries showing what you're currently focused on. Use when the user says "create a now post", "update my now page", "write about what I'm doing now", or mentions wanting to document their current focus or activities.
allowed-tools:
  - Write
  - Read
  - Bash
---

# Now Page Writer

This skill creates new entries for the `/now` page - a "what I'm doing now" page inspired by [nownownow.com](https://nownownow.com/about).

## File Location

Create new entries in: `src/content/now/`

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

## Content Format

Use markdown with `##` headings to organize different areas of focus:

```markdown
## Section Title

Your content here. Write in a conversational, direct voice. Be authentic and show what's genuinely on your mind.
```

## Style Guidelines

- **Conversational tone**: Write as if talking to a friend
- **Multiple sections**: Use `##` headings for different topics (work, personal, learning, etc.)
- **Authentic voice**: Share real thoughts, uncertainties, and reflections
- **Present tense**: Focus on what's happening NOW, not past achievements
- **Brief updates**: Each section should be 1-3 paragraphs

## Example Entry

```markdown
---
date: 2025-10-30
---

## Academic Year Begins

The academic year has started and I'm diving into teaching new subjects. Introduction to Software Engineering and Science Programming - both with heavy AI bias. The students are skeptical about AI usage, which is fascinating.

## AI Infrastructure Ruminations

Thinking a lot about AI infrastructure futures, Agent Labs, and where Steel.dev fits. The agentic guardrails question keeps surfacing.

## PhD Direction Reconsideration

Rapid AI evolution has me reconsidering my PhD direction. What seemed relevant a year ago might not be the most impactful research focus now.
```

## How It Works

1. The `/now` page automatically shows the **most recent** entry (sorted by date)
2. Old entries remain in the directory but aren't displayed on the main page
3. The page renders with "What I'm Currently Focused On" header and "Last updated" timestamp

## When to Create a New Entry

Create a new now entry when:
- Your major focus areas have shifted significantly
- It's been 2-4 weeks since your last entry
- You're starting a new chapter (job, project, life change)
- You want to capture a snapshot of your current state

## Process

1. Determine today's date for the filename (YYMMDD.md) and frontmatter (YYYY-MM-DD)
2. Ask the user what they'd like to share about their current focus
3. Draft the content with appropriate sections
4. Create the file in `src/content/now/`
5. Confirm creation with the user
