# Ingredient Recipe Verification Report

**Date:** 2026-01-06  
**Status:** Discrepancy Found

## Objective
To verify if the chemical recipe for `ATCC:1306` provided in the `media_ingredients.tsv` file matches the authoritative definition of "ATCC Medium 1306" (Nitrate Mineral Salts / NMS) obtained from the ATCC datasheet and MediaDive database.

## Data Sources
1.  **Input:** `BER-CMM-data-for-AI-normalized - media_ingredients.tsv` (Row: `ATCC:1306`)
2.  **Reference:** MediaDive Database ID `632` (NMS Medium), verified against ATCC PDF.

## Comparison Results

The comparison revealed significant quantitative and qualitative differences.

| Component | Input TSV (`ATCC:1306`) | Reference (MediaDive 632 / ATCC PDF) | Mismatch Type |
| :--- | :--- | :--- | :--- |
| **Magnesium Sulfate** | 0.2 g/L | 1.0 g/L | ❌ **Concentration (5x difference)** |
| **Calcium Chloride** | 0.02 g/L | 0.2 g/L | ❌ **Concentration (10x difference)** |
| **Potassium Nitrate** | 2.0 g/L | 1.0 g/L | ❌ **Concentration (2x difference)** |
| **Trace Elements** | Not listed / distinct | Detailed list (Zn, Mn, Co, etc.) | ❌ **Missing/Different** |

## Conclusion

The recipe labeled `ATCC:1306` in the provided `media_ingredients.tsv` **does NOT match** the standard ATCC 1306 / NMS formulation.

**Implications:**
1.  The TSV likely describes a **modified variant** or contains data entry errors.
2.  The `ATCC:1306` identifier in the CMM dataset is unreliable for chemical definitions.
3.  Grounding decisions should rely on the **local registry** (based on name/DOI) rather than assuming chemical equivalence to the ATCC catalog number based on this ingredients file.

## Action Taken
We have prioritized the **Local Registry** and **DOI-based grounding** for the Knowledge Graph, decoupling the "PIPES minimal medium" and other local variants from standard ATCC/DSMZ identifiers where chemical equivalence cannot be proven.
