# Bat Entry Creation Instructions (bats.yaml)

You will create one or more **bat entries** in:

```
../batdigest-flask/data/bats.yaml
```

---

## Required User Inputs

If any of the following are missing, **ask the user before proceeding**:

* year
* brand
* model
* league
* drop

You may be asked to create **multiple bats in one request**.

---

## General Rules

* Do a search on the yaml file and make sure this is a new bat to our list, if confusing exists, confirm with user before proceeding.
* Append each new bat to the **end of `bats.yaml`**.
* Use the **next sequential `id`**.
* Follow the YAML structure **exactly**.
* Comments in the structure below describe how each field should be populated.
* Ensure spelling and casing match official product names.
* Use the Python script below to generate affiliate links.

---

## Python Files Needed

* `affiliate_link_generator.py`

---

## Data Sources

* **JustBats.com**

  * serial
  * diameter
  * sizes
  * original price
  * product specs
* **Google / manufacturer pages**

  * release date
  * missing specifications
* **User input always overrides scraped data**

---

## Bat YAML Structure

```yaml
[id]:
  year:            # YYYY (user provided)
  brand:           # user provided, exact spelling
  model:           # user provided, exact spelling
  drop:            # examples: -3, -5, -8, -9, -10, -11, -12, -13
  league:          # BBCOR, USSSA, USA, Fastpitch
  serial:          # scrape from justbats.com if not provided
  type:            # Single Piece Alloy, Single Piece Composite, Composite, Hybrid, Wood
  diameter:        # scrape from justbats.com: 2 5/8, 2 3/4, or 2 1/4
  sizes:           # one size per line, no blank lines
    - 29
    - 30
    - 31
  price:           # original MSRP from justbats.com
  created_at:      # current timestamp: 'YYYY-MM-DD HH:MM:SS.ffffff'
  updated_at:      # current timestamp: 'YYYY-MM-DD HH:MM:SS.ffffff'
  release_date:    # 'YYYY-MM-DD 00:00:00.000000'
  review_status:   # default: in-review; use Tested if specified
  rank_in_class:   # populated AFTER all new bats are added
  description:     # 1–2 sentences in BatDigest voice, based on research
  ratings:         # placeholder values only
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
  affiliate:
    amazon:
    justbats:
    dicks:
    sideline:
    ebay:
    closeout:
    brand_link:
  is_active: true  # unless explicitly told otherwise
```

---

## Notes and Constraints

* Do **not** invent specifications when reliable data is unavailable.
* Validate **sizes**, **diameter**, and **serial** against JustBats whenever possible.
* Leave all rating fields blank as placeholders until scoring is applied later.

