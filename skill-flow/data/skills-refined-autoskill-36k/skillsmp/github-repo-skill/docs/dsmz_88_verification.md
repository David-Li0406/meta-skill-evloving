# Medium ID Verification Report: DSMZ 88

**Date:** 2026-01-06  
**Status:** Discrepancy Found

## Objective
To verify if the medium labeled as `DSMZ:88` ("SM medium for Paracoccus") in the CMM growth media spreadsheet matches the authoritative definition of "DSMZ Medium 88".

## Data Sources
1.  **Input:** `BER-CMM-data-for-AI-normalized - growth_media.tsv` (Row: `DSMZ Medium 88`) & `media_ingredients.tsv`
2.  **Reference 1:** MediaDive Database ID `88` (Verified local MongoDB).
3.  **Reference 2:** Official DSMZ PDF: `https://www.dsmz.de/microorganisms/medium/pdf/DSMZ_Medium88.pdf`

## Comparison Results

The comparison revealed a total mismatch in identity, chemistry, and target organism.

| Feature | Input Sheet (`DSMZ:88`) | Official DSMZ 88 | Mismatch Type |
| :--- | :--- | :--- | :--- |
| **Name** | "SM medium for Paracoccus" | "SULFOLOBUS MEDIUM" | ❌ **Identity** |
| **Target Organism** | *Paracoccus* (Proteobacteria) | *Sulfolobus* (Archaea) | ❌ **Biology** |
| **Key Ingredient** | Disodium Succinate (2.7 g/L) | (NH₄)₂SO₄ (1.3 g/L) | ❌ **Chemistry** |
| **pH** | Neutral (implicit for *Paracoccus*) | 2.0 (Acidic) | ❌ **Condition** |

## Diagnosis
The CMM spreadsheet entry `DSMZ:88` is **incorrect**.
*   The acronym "SM" likely stands for "Succinate Medium" or "Standard Medium" in the lab's context.
*   It was likely mismapped to DSMZ 88 because DSMZ 88 is the first result for "SM" (Sulfolobus Medium) in some searches, or due to a simple data entry error (perhaps DSMZ 576 "Nutrient Agar" or similar was intended?).

## Action Taken
1.  **Grounding:** The medium has been grounded to a stable local identifier: `BER-CMM-MEDIUM:0000006`.
2.  **Decoupling:** The link to `dsmz:88` has been removed/suppressed to prevent false assertions in the Knowledge Graph.
3.  **Graph Integrity:** This prevents the absurd biological assertion that a neutrophilic *Paracoccus* grows in a pH 2.0 Sulfolobus medium.
