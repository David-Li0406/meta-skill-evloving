---
name: synthesize-inbox-entry
description: Synthesize raw notes or conversations into a compliant `planning/inbox/` entry using the repo template. Use when turning unstructured input into a new inbox file without modifying existing entries.
---

# Skill: synthesize-inbox-entry

## Purpose
Turn raw notes or conversation text into a compliant inbox entry in `planning/inbox/`
using the template at `planning/templates/inbox_synthesis.md`.

## When to use
- The user asks to synthesize research or chat logs into a planning inbox entry.
- The user provides unstructured notes that should be preserved as a curated input.

## Inputs
- Raw text (notes, chat transcript, bullets).
- Optional: source context, author, date, related links.

## Steps
1. Open `planning/templates/inbox_synthesis.md` and follow its section order.
2. Ask clarifying questions if any required section is ambiguous or missing.
3. Produce a new file in `planning/inbox/` using the repo's naming convention.
4. Keep content precise and testable where possible; avoid adding new scope.
5. Do not edit existing inbox files.

## Output
- A new inbox entry file path plus the synthesized content.

## Constraints
- Inbox files are immutable once created; create a new file instead of editing.
- Treat exploratory sections as non-requirements.
