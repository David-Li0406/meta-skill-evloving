# Bat Ratings Instructions (bats.yaml)

You will create or update **only** the `ratings:` section for the bat(s) requested by the user in:

`data/bats.yaml`

---

## General Rules

- Only edit the bats the user asked for (no drive-by cleanup).
- When adding ratings for a new bat, first try to **seed ratings** from a similar existing bat (same model/league/drop; usually prior year).
- If you copy ratings from a similar bat, tell the user which bat you used as the seed and why.

---

## 1st Step Seed Ratings From Similar Bat

Use this script to find the closest matching *rated* bat and print copy/paste seed ratings:

`./BAT_RATINGS_SCRIPTS/suggest_similar_bat_ratings.py`

It requires you input the year, brand, model and league. It will return a result that may include a "no matches found".

Report the results to the user and let them decide what ratings they would like to use to complete the following YAML STRUCTURE for the bat.

## Bat YAML Structure (ratings fields)

```yaml
[id]:
  .
  .
  .
  ratings:
    swing_weight:
    performance:
    player_rating:
    tech_specs:
    durability:
    resell:
    relevance:
    demand:
    stiffness:
    profile_size:

```

## STEP 2: Calculated Ratings.

The following ratings are calculated by using the ____.py file.

```yaml
[id]:
  ratings:
    grade:
    performance_score:
    performance_grade:
    control_score:
    control_grade:
    quality_score:
    quality_grade:
    value_score:
    value_grade:
    overall_score:
    overall_grade:
```

---

## Notes and Constraints

- Prefer using the seed ratings output as a baseline, then adjust only if the user provides guidance.
- Do not invent performance claims; ratings should reflect the user’s direction or the closest comparable in the dataset.
- If the bat is already added to `bats.yaml` with `sizes`, you can compute a YAML-based relevance score with:
  `./venv/bin/python AGENTS/Content_Creation/BAT_LISTINGS_Agent/BAT_RATINGS_SCRIPTS/calculate_relevance_score.py [BAT_ID]`

