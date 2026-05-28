---
name: Metadata Mapping RCO to RI
description: Procedures and logic for mapping Carif-Oref (RCO) XML data to Réfugiés.info (RI) structured metadata. Use when processing new RCO fiches to generate the technical frontmatter and mapping table.
---

# Metadata Mapping RCO to RI

This skill provides the logic and tools to transform metadata from a Carif-Oref XML (Lhéo) into the Réfugiés.info format.

## 📋 Workflow

1. **Extract**: Read the RCO XML and identify relevant tags.
2. **Map**: Apply business logic and conversion tables (from `ressources_metadatas/base-connaissance.md`).
3. **Generate**: Produce the `metadata_ri` YAML frontmatter and the mapping traceability table.

## 🔧 Business Rules

### Price Logic
- **Gratuit**: If `conventionnement = 1` AND `code-financeur` is in [2, 3, 8, 9, 11, 12, 13, 15, 19].
- **Payant**: Otherwise.

### Duration & Frequency
- **Commitment**: Extract total hours from `duree-indicative`.
- **Frequency**: Calculate hours/week from `contenu-formation` (e.g., "2h x 2 days" = 4h/week).

### Conversions
- **Public**: Map `code-public-vise` using the conversion table.
- **French Level**: Extract from `contenu-formation` (alpha, A1, A2, B1, B2, C1, C2).
- **Dates**: Convert YYYYMMDD to ISO 8601.

## 🛠️ Tools

A TypeScript script is available to automate the extraction and mapping:

```bash
pnpm tsx .skills/metadata/scripts/map-metadata.ts <path_to_xml>
```

## 📝 Output Format

The output must follow the standard RI frontmatter structure and include a markdown table for traceability.

| Metadata | Value | RCO Source |
|----------|-------|------------|
| Title    | ...   | tag : value|
