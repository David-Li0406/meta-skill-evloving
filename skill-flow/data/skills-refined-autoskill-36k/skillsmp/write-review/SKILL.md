---
name: write-review
description: Create or update BatDigest review summary YAML files in data/reviews/summaries for bat review pages. Use when asked to write, draft, or update a bat review, generate a review summary YAML, update review content from a review YAML file, or associate bats to a review (slug/associated_bat_ids).
---

# Write Review

## Overview

Create or update bat review summary YAML files for BatDigest review pages, including slug selection, associated bat IDs, and timestamps.

## Quick Start

1. Open the BatDigest repo at `C:\Users\bduryea\OneDrive - Davis School District\Desktop\14_Dev_Projects\batdigest-flask`.
2. Use the helper script to generate a skeleton review file (see "Helper Script").
3. Fill in review fields in BatDigest voice and update timestamps.

## Workflow

1. **Confirm required inputs** before editing:
   - year, brand, model, sport (Baseball or Fastpitch), bat_type
   - Optional but helpful: league focus, preferred slug, associated bat IDs, YouTube link
2. **Check for an existing review** in `data/reviews/summaries/`:
   - Default slug: `{year}-{brand}-{model}-review`
   - If multiple variants are needed, append a league token (example: `2025-easton-hype-fire-usssa-review`).
3. **Find associated bat IDs** in `data/bats.yaml` (match year/brand/model/league).
4. **Create or update the YAML file** at `data/reviews/summaries/<slug>.yaml` using the schema in `references/BAT_REVIEW_Agent.md`.
5. **Timestamps**:
   - New review: set `published_at` (ISO).
   - Always update `updated_at`.
6. **Quality checks**:
   - Keep language direct and practical (no hype).
   - Do not invent specs or claims without evidence.
   - Confirm associated_bat_ids if uncertain.

## Helper Script

Run this from the repo root to generate a skeleton review summary:

```bash
python3 AGENTS/Content_Creation/BAT_REVIEW_SCRIPTS/create_review_summary.py \
  --year 2025 \
  --brand "Easton" \
  --model "Hype Fire" \
  --sport Baseball \
  --bat-type "Two Piece Composite"
```

## References

- `references/BAT_REVIEW_Agent.md` for schema, field notes, and constraints.
