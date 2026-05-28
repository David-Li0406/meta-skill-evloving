---
name: add-a-bat
description: Add a new bat listing to BatDigest by creating a new entry in `data/bats.yaml`, researching missing specs (JustBats/manufacturer), and generating affiliate links; then optionally proceed to add ratings and bat images (R2 upload + `data/images.yaml`). Use when asked to "add a bat", "create a bat listing", "add to bats.yaml", "add ratings", or "attach bat images".
---

# Add A Bat

## Overview

Add a bat to the BatDigest dataset in a safe, repeatable way: confirm the exact variant, check for duplicates, fill missing specs via reputable sources, append a correct `data/bats.yaml` entry, then pause and ask whether to proceed to ratings and images.

## Assumptions

- Repo root: `~/Coding_Projects/batdigest-flask`
- Data files:
  - `data/bats.yaml`
  - `data/images.yaml`
- Image staging folder: `AGENTS/Content_Creation/BAT_LISTINGS_Agent/Image_Processing/`
- You can use the network to look up missing specs (prefer user-provided retailer/manufacturer URLs).

## Workflow (Gated: Entry → Ratings → Images)

### 0) Confirm the exact bat(s)

If any of these are missing, ask before editing anything:
- year
- brand
- model
- league (`BBCOR`, `USSSA`, `USA`, `Fastpitch`)
- drop (e.g. `-3`, `-5`, `-8`, `-10`, etc.)

Strongly prefer at least one source URL (JustBats/manufacturer) for specs.

### 1) De-dupe (make sure it’s actually new)

- Search `data/bats.yaml` for same year/brand/model and league/drop variants.
- If something close exists (paint job vs new model vs different league/drop), confirm with the user whether to:
  - add a new bat entry (new variant), or
  - update an existing entry (not the default for this skill).

### 2) Gather missing specs (use the internet, but don’t guess)

Fill (when possible) using JustBats/manufacturer pages:
- `serial`
- `diameter`
- `sizes`
- `price` (MSRP/original)
- `release_date`

Use the existing helper to generate affiliate links (and often find a JustBats product page):

```bash
cd ~/Coding_Projects/batdigest-flask
python3 AGENTS/Content_Creation/BAT_LISTINGS_Agent/affiliate_link_generator.py <YEAR> "<BRAND>" "<MODEL>"
```

If a spec cannot be confirmed from reputable sources, ask the user; do not invent it.

### 3) Add the bat entry to `data/bats.yaml`

- Append to the end of `data/bats.yaml` using the next sequential numeric id.
- Match existing file conventions (important):
  - `review_status` is typically `in_review` (underscore).
  - Affiliate links are stored as top-level keys (`amazon`, `justbats`, `dicks`, `sideline`, `ebay`, `closeout`, `brand_link`), not under an `affiliate:` block.
  - Use `null`/blank values for unknown fields (don’t fabricate).
- Set `created_at` and `updated_at` to the current timestamp (same formatting as existing entries).
- Leave ratings fields blank unless the user explicitly wants to proceed to the ratings step.

### 4) Gate: ask before ratings

After writing the new `data/bats.yaml` entry, ask:
- “Do you want to add ratings now (seed from a similar bat)?”

If **no**, stop.

### 5) Ratings (optional, only if user says yes)

- Follow the ratings-only workflow (edit only `ratings:` for the requested bat id).
- Seed from similar bats first:
  ```bash
  cd ~/Coding_Projects/batdigest-flask/AGENTS/Content_Creation/BAT_LISTINGS_Agent
  python3 BAT_RATINGS_SCRIPTS/suggest_similar_bat_ratings.py
  ```
- Report the suggested seed to the user and confirm what to apply.

Then ask:
- “Do you want to attach/upload images now?”

### 6) Images (optional, only if user says yes)

- Require a **long** cutout image staged in `AGENTS/Content_Creation/BAT_LISTINGS_Agent/Image_Processing/`.
- Generate a **feature** image if missing.
- Run the R2 uploader script to generate variants + upload.
- Update `data/images.yaml` under `images: <BAT_ID>:` with the script’s `static_paths` output (do not hand-write URLs).

## References

Use these as the canonical “agent prompt” details:
- `references/BAT_LISTINGS_Agent.md`
- `references/Bat_Entry_Agent.md`
- `references/Bat_Ratings_Agent.md`
- `references/Bat_Image_Attach_Agent.md`
