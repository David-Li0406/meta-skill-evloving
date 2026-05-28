# Bat Review Creation Instructions (YAML summaries)

You will create or update **individual bat review summaries** in:

```
../batdigest-flask/data/reviews/summaries/
```

These files are the source of truth for `/reviews/<slug>/` pages. This is YAML-only (no DB).

---

## Required User Inputs

If any of the following are missing, **ask the user before proceeding**:

- year
- brand
- model
- sport (Baseball or Fastpitch)
- bat_type

Optional but helpful:
- league focus (BBCOR, USSSA, USA, Fastpitch)
- preferred slug (if not standard)
- known associated bat IDs
- YouTube link

---

## Workflow

1. **Confirm slug and check for an existing review**
   - Default slug pattern: `{year}-{brand}-{model}-review`
   - If multiple reviews for the same model/year are needed, append a league token
     (e.g., `2025-easton-hype-fire-usssa-review`).
   - Search `data/reviews/summaries/` for an existing file before creating a new one.

2. **Find associated bat IDs**
   - Match bats in `data/bats.yaml` by year + brand + model (and league if specified).
   - Include all matching bat IDs in `associated_bat_ids`.
   - Use the helper script below to list matches.

3. **Write the review YAML file**
   - Create `data/reviews/summaries/<slug>.yaml`.
   - Follow the schema exactly.
   - Use Bat Digest voice: direct, practical, no marketing hype.

4. **Update timestamps**
   - Set `published_at` for new reviews (ISO format).
   - Always update `updated_at` when editing.

---

## Helper Script

```
python3 AGENTS/Content_Creation/BAT_REVIEW_SCRIPTS/create_review_summary.py \
  --year 2025 \
  --brand "Easton" \
  --model "Hype Fire" \
  --sport Baseball \
  --bat-type "Two Piece Composite"
```

This script:
- Finds matching bat IDs in `data/bats.yaml`
- Builds a correctly structured YAML file
- Writes it to `data/reviews/summaries/`

---

## Review YAML Structure

```yaml
slug: 2025-easton-hype-fire-review
review:
  slug: 2025-easton-hype-fire-review
  brand: Easton
  model: Hype Fire
  year: 2025
  sport: Baseball
  bat_type: Two Piece Composite
  opening_review: ""
  models_overview: ""
  construction: ""
  vs_last_years: ""
  comparable: ""
  recommendations: ""
  conclusions: ""
  youtube: ""
  published_at: "2025-01-01T00:00:00"
  updated_at: "2025-01-01T00:00:00.000000"
  associated_bat_ids: "100,101,102"
  verdict: ""
  takeaways: {}
  watchouts: []
  comparables: []
```

### Field Notes
- `opening_review` should be the short hook and thesis.
- `models_overview` should explain drop/league variants.
- `construction` is materials + build details.
- `vs_last_years` summarizes deltas vs prior year.
- `comparable` is a short paragraph list of similar bats.
- `comparables` is a list of link objects:
  ```yaml
  comparables:
  - label: 2025 Rawlings Icon
    url: /reviews/2025-rawlings-icon-review/
  ```
- `takeaways` is a short map of key facts:
  ```yaml
  takeaways:
    Overall grade: A
    Construction: Two Piece Composite
    Drop options: "-11 to -5"
    Price: "$350 - $430"
  ```

---

## Constraints

- Do not use the database.
- Do not invent specs or claims without evidence.
- Confirm the matched bat IDs with the user when uncertain.
- Keep language clean, specific, and consistent with existing Bat Digest reviews.
