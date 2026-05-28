# Cascading Selects Reference

Cascading selects (or dependent selects) show choice options that depend on a previous selection. Example: Select country, then province options change based on country.

## Basic Pattern

Use the `choice_filter` column in the survey worksheet.

### Example: Country → Province

**Survey:**
```
| type | name | label | choice_filter |
| select_one country | country | Country | |
| select_one province | province | Province | province in ${country} |
```

**Choices:**
```
| list_name | name | label | country |
| country | ke | Kenya | |
| country | ug | Uganda | |
| province | nairobi | Nairobi | ke |
| province | mombasa | Mombasa | ke |
| province | kampala | Kampala | ug |
| province | jinja | Jinja | ug |
```

**How it works:**
1. User selects "Kenya" from country
2. Province list filters to show only provinces where country = "ke"
3. User sees: Nairobi, Mombasa
4. User selects "Uganda" from country
5. Province list updates: Kampala, Jinja

---

## Syntax Explained

```
choice_filter: province in ${country}
```

- `province` - Column name in choices worksheet that filters
- `in` - Operator (filter to this value)
- `${country}` - The selected country question

The `country` column in choices worksheet must match the selected value:
```
| list_name | name | label | country |
| province | nairobi | Nairobi | ke |
```

When user selects `ke` in country question, province list shows rows where country = "ke".

---

## Advanced Filtering

### Multiple-Level Cascading

**Survey:**
```
| type | name | label | choice_filter |
| select_one country | country | Country | |
| select_one region | region | Region | region in ${country} |
| select_one district | district | District | district in ${region} |
| select_one ward | ward | Ward | ward in ${district} |
```

**Choices:**
```
| list_name | name | label | country | region |
| region | central | Central | ke | |
| region | coast | Coast | ke | |
| region | rift | Rift Valley | ug | |

| list_name | name | label | region | district |
| district | nairobi | Nairobi | central | |
| district | kiambu | Kiambu | central | |
| district | mombasa | Mombasa | coast | |

| list_name | name | label | district | ward |
| ward | embakasi | Embakasi | nairobi | |
| ward | westlands | Westlands | nairobi | |
| ward | kilifi | Kilifi | mombasa | |
```

**Flow:**
1. Select country
2. Region options filter by country
3. District options filter by selected region
4. Ward options filter by selected district

---

### Filtering on Multiple Columns

```
choice_filter: (district in ${region}) and (district in ${country})
```

Filters on both region AND country.

---

## Building Cascading Choices

### Step 1: Plan the Hierarchy
```
Country
  └─ Province
       └─ District
            └─ Ward
```

### Step 2: Create Survey Questions
```
| type | name | label | choice_filter |
| select_one country | country | Country | |
| select_one province | province | Province | province in ${country} |
| select_one district | district | District | district in ${province} |
```

### Step 3: Create Choices Rows
For each level, create a choices worksheet row with filtering column:

```
| list_name | name | label | country |
| province | nairobi | Nairobi | ke |
```

The `country` column contains the country code to filter on.

### Step 4: Test
1. Select first option (country)
2. Verify second option (province) updates
3. Verify only matching choices show
4. Test all branches

---

## Real-World Examples

### Healthcare Facility Hierarchy

**Form Structure:**
```
Country → Region → District → Health Facility
```

**Survey:**
```
| type | name | label | choice_filter |
| select_one country | country | Country |
| select_one region | region | Region | region in ${country} |
| select_one district | district | District | district in ${region} |
| select_one facility | facility | Health facility | facility in ${district} |
```

**Choices (partial):**
```
| list_name | name | label | country |
| country | ke | Kenya |
| country | ug | Uganda |

| list_name | name | label | region | country |
| region | nairobi | Nairobi | nairobi | ke |
| region | kampala | Kampala | kampala | ug |

| list_name | name | label | district | region |
| district | nbi_west | Nairobi West | nairobi |
| district | kpl_south | Kampala South | kampala |

| list_name | name | label | facility | district |
| facility | f001 | City Hospital | nbi_west |
| facility | f002 | District Hospital | nbi_west |
| facility | f003 | Kampala General | kpl_south |
```

### Education Cascading

**Form:**
```
Country → State/Province → District → School
```

### Organization Cascading

**Form:**
```
Organization → Department → Team → Project
```

### Address Cascading

**Form:**
```
Country → Region → City → Neighborhood → Street
```

---

## Best Practices

### Do's
✓ Make filtering column names match perfectly (case-sensitive)
✓ Test all branches before deployment
✓ Use meaningful names (not option_1, option_2)
✓ Verify filtering column contains actual values
✓ Combine with `relevant` for complex logic

### Don'ts
✗ Don't create circular cascades (A filters B, B filters A)
✗ Don't use too many levels (3-4 is practical limit)
✗ Don't make filtering value ambiguous
✗ Don't mix cascading levels (skip levels)

---

## Common Mistakes

| Mistake | Problem | Fix |
|---------|---------|-----|
| Column name typo | Cascading doesn't work | Verify column name matches exactly |
| Case mismatch | Filtering fails | Use exact case: `region in ${country}` |
| Missing value in filtering column | Some options hidden | Ensure all choices have filtering value |
| Filtering circular | Unpredictable behavior | Don't create dependent loops |
| Too many levels | Complex/slow | Limit to 3-4 cascading levels |
| Filtering column empty | Cascading fails | All choices need filtering value |

---

## Troubleshooting

### Cascading Not Working

1. **Check survey column name** - Matches spelling exactly?
   ```
   choice_filter: district in ${region}
   (${region} must match the survey field name)
   ```

2. **Check choices filtering column** - Exists in choices worksheet?
   ```
   | list_name | name | label | region |
   | district | item1 | ... | regional_value |
   ```

3. **Check filtering values** - Do choices have matching values?
   ```
   If ${region} = "north", choices must have region = "north"
   ```

4. **Test step by step:**
   - Select first option
   - Does second list update? No? Check column name.
   - Does second list show empty? Check values match.
   - Does cascade work but slowly? Performance issue, consider file-based.

### Large Choice Lists

If cascading lists have 1000+ items, use `select_one_from_file` instead. See [external-data.md](external-data.md).

---

## Alternative: External Data

For very large cascading lists, use external CSV files:

```
| type | name | label |
| select_one_from_file hospitals | hospital | Hospital |
```

With hospitals.csv containing thousands of hospitals filtered by district. See [external-data.md](external-data.md) for details.

---

## Performance Notes

- Cascading with <100 choices per list: fast
- Cascading with 100-1000 choices: acceptable
- Cascading with 1000+ choices: consider external file
- Multiple cascading levels (3+): slightly slower but workable

Test on actual device before deployment, especially with large lists.

---

## See Also

- [choices-sheet.md](choices-sheet.md) - Choices worksheet structure
- [external-data.md](external-data.md) - Using external CSV files
- [examples.md](../examples.md) - Example form with cascading selects
