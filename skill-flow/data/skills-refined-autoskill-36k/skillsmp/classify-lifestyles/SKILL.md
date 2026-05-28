---
name: classify-lifestyles
description: Classify lifestyle categories for all biographical stories. Use when asked to classify or reclassify lifestyles.
---

# Lifestyle Classification Workflow

You are classifying the economic lifestyle of all people in `_lives/` and `_lives_pending/` to improve filtering and visualization on the website.

## Categories

Use exactly these five categories:

1. **Hunter-Gatherer** - foraging societies (no agriculture)
2. **Pastoralist** - primarily livestock herding (mobile/semi-nomadic)
3. **Farmer** - agricultural cultivation (peasants, smallholders, agricultural laborers, farm household workers)
4. **Rural Non-Farm** - non-agricultural rural work (village craftspeople, rural servants, rural laborers, rural traders)
5. **Urban** - town/city dwellers (regardless of occupation)

## How to Classify

For each person:

1. **Read the occupation field** in the YAML debug comments (`# occupation:`)
2. **Check the narrative context** for clues about settlement type
3. **Consider these markers**:
   - **Urban indicators**: references to "town," "city," "plaza," "market," "street," "workshop," officials/priests present, multiple named establishments
   - **Rural indicators**: "village," "hamlet," dispersed settlement, primarily household-based work
   - **Grid cell limitations**: The `urban_area percentage` can be misleading since HYDE grid cells are ~10km x 10km - a small town can exist in a 0.03% urban cell

4. **Apply decision tree**:
   - If narrative clearly describes town/city life → **Urban**
   - Else if occupation is hunter/gatherer/forager → **Hunter-Gatherer**
   - Else if occupation is herder/pastoralist → **Pastoralist**
   - Else if occupation is cultivation/farming/agricultural labor → **Farmer**
   - Else if rural setting with non-agricultural work → **Rural Non-Farm**
   - Else (ambiguous/uncertain) → **Add "FLAG: " prefix to lifestyle** (e.g., `lifestyle: "FLAG: Urban"`) so you can grep for it later

## Edge Cases

- **Migrant workers who move to cities**: Classify by where they spend their adult life (e.g., construction worker living in cities = Urban)
- **District capitals**: Small district capitals count as Urban even if grid cell is mostly rural
- **Infants who die**: Classify by parents' occupation and setting
- **Mixed occupations**: Choose primary occupation (e.g., "farmer + occasional craft" = Farmer)

## FLAG System

Add "FLAG: " prefix to the lifestyle field when ANY of these occur:

1. **Classification uncertain** - occupation is ambiguous or mixed
2. **Urban location mismatch** - classified as Urban but:
   - `urban_area percentage` is very low (<0.5%)
   - Narrative doesn't clearly describe town/city
3. **Missing key data** - no occupation field found
4. **Contradictory information** - occupation and narrative don't match

Examples:
- `lifestyle: "FLAG: Urban"` - classified as Urban but uncertain
- `lifestyle: "FLAG: Farmer"` - mixed agro-pastoral occupation, chose Farmer
- `lifestyle: "FLAG: Rural Non-Farm"` - mining settlement, urban_area% very low but might be small town

## Process

**CRITICAL: Process ONE file at a time. NO batch processing.**

Work through files systematically:

1. Read ONE file's occupation and narrative context
2. Determine the correct category for THIS file
3. If uncertain, add "FLAG: " prefix to the lifestyle value
4. **BEFORE updating**: Record the old classification value
5. Add a new `old_lifestyle:` field in frontmatter with the original value
6. Update the `lifestyle:` field in frontmatter with new classification (with FLAG prefix if uncertain)
7. Move to the NEXT file and repeat steps 1-6
8. Track progress (report every 25 stories)

## Example Classifications

- **Construction laborer living in cities** → Urban
- **Peasant farmer on family land** → Farmer
- **Agricultural day laborer** → Farmer
- **Village weaver/blacksmith** → Rural Non-Farm
- **Maasai herder** → Pastoralist
- **Atlantic Forest forager** → Hunter-Gatherer
- **Small-town artisan with workshop** → Urban (even if urban_area = 0.03%)
- **Domestic worker in urban household** → Urban
- **Household farm worker** → Farmer

## Output Format

For each file, add the old value and update the current value:
```yaml
old_lifestyle: "Rural"
lifestyle: "Urban"
```

The `lifestyle:` value should be one of: `"Hunter-Gatherer"`, `"Pastoralist"`, `"Farmer"`, `"Rural Non-Farm"`, or `"Urban"`.

The `old_lifestyle:` field preserves the original automatic classification for comparison.
