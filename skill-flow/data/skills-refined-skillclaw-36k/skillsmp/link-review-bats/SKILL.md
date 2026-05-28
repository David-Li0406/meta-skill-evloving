---
name: link-review-bats
description: Link bat entries in data/bats.yaml to review summary files by updating review.associated_bat_ids in data/reviews/summaries/*.yaml. Use when asked to associate bat ids with reviews, add new variants/colorways to a review, or keep review associations in sync after adding bats.
---

# Link Review Bats

## Overview

Find bats that are not linked to any review and walk through interactive, suggested
connections that update `associated_bat_ids` after confirmation.

## Quick Start

Run the interactive helper:

```bash
python3 /Users/brianduryea/.codex/skills/link-review-bats/scripts/link_review_bats.py \
  --repo ~/Coding_Projects/batdigest-flask
```

For non-interactive runs, use auto mode to apply high-confidence matches:

```bash
python3 /Users/brianduryea/.codex/skills/link-review-bats/scripts/link_review_bats.py \
  --repo ~/Coding_Projects/batdigest-flask \
  --auto --auto-gap 0.5 --min-score 2.5
```

The script:
- Loads `data/bats.yaml` and all review summaries in `data/reviews/summaries/`.
- Finds bat ids not present in any `associated_bat_ids`.
- Suggests likely review matches and prompts in the terminal to confirm.
- Preserves the original `associated_bat_ids` formatting (quoted/unquoted, delimiter).
- In `--auto` mode, applies strong matches and skips ambiguous ones.
- Matches only when review year and brand match exactly (with small brand aliases like "Slugger" -> "Louisville Slugger").
- Matches only within the same sport: Fastpitch stays with Fastpitch; BBCOR/USSSA/USA map to Baseball.

## Options

- `--dry-run` preview changes without writing.
- `--year`, `--brand`, `--model` filter bats to a subset.
- `--limit` stop after N bats.
- `--top` number of suggestions shown (default 5).
- `--min-score` threshold for a “strong” suggestion (default 2.5).
- `--auto` apply high-confidence matches without prompting.
- `--auto-gap` minimum score gap between the top and runner-up for auto mode (default 0.5).
- `--auto-min-score` override the score threshold used by auto mode.

## Notes

- The script appends new ids at the end and skips duplicates.
- If the `pyyaml` import fails, install it with `python3 -m pip install pyyaml`.
