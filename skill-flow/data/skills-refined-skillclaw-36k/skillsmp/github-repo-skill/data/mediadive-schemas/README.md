# MediaDive MongoDB Collection Schemas

## Source

These schemas were inferred from MongoDB collections using **MongoDB Compass's "Infer Schema" tool**.

## Date Created

December 11, 2025

## Collections

- `ingredient_details.json` - Detailed ingredient information
- `ingredients.json` - Ingredient collection schema
- `media.json` - Growth media collection schema
- `media_details.json` - Detailed media information (largest file: 5.9 MB)
- `medium_composition.json` - Medium composition relationships
- `medium_strains.json` - Strain-medium associations
- `solution_details.json` - Detailed solution information
- `solutions.json` - Solution collection schema
- `stats.json` - Statistical summary of collections
- `strains.json` - Strain collection schema

## Purpose

These inferred schemas document the structure of MediaDive MongoDB collections for:
- Understanding data models
- Planning data transformations
- Documenting field types and distributions
- Identifying data quality issues

## Regeneration

To regenerate these schemas:

1. Open MongoDB Compass
2. Connect to the MediaDive database
3. Select a collection
4. Click "Schema" tab
5. Click "Analyze Schema" button
6. Export the schema JSON

## Notes

- These are **inferred** schemas based on sampling, not authoritative schemas
- Field presence and types may vary across documents
- Probability values indicate how often a field appears in the sample
