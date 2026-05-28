# Verification of ATCC 1306 vs. NMS Medium

**Date:** 2026-01-06  
**Status:** Verified

## Objective
To determine if "ATCC Medium 1306" is equivalent to "Nitrate Mineral Salts (NMS) Medium" and to resolve a discrepancy in the CMM growth media spreadsheet where `ATCC:1306` was associated with a "PIPES minimal medium".

## Methodology

1.  **Source Extraction (PDF):**
    *   Extracted text from the official `ATCC Medium 1306.pdf` using `pdftotext`.
    *   **Result:** The PDF explicitly titles the medium "ATCC medium: 1306 Nitrate mineral salts medium (NMS)".

2.  **Database Retrieval (MongoDB):**
    *   Queried the local **MediaDive** database (`mediadive.media_details`) for the known NMS ID (`_id: 632`, corresponding to DSMZ 632).
    *   **Command:** `db.media_details.findOne({'_id': 632})`

3.  **Ingredient Comparison:**
    *   Compared the extracted PDF text against the structured JSON recipe from MediaDive.

## Results

| Component | ATCC 1306 (PDF) | DSMZ 632 (MediaDive) | Match? |
| :--- | :--- | :--- | :--- |
| **MgSO4 . 7H2O** | 1.0 g | 1 g | ✅ |
| **CaCl2 . 6H2O** | 0.20 g | 0.2 g | ✅ |
| **KNOW3** | 1.0 g | 1 g | ✅ |
| **KH2PO4** | 0.272 g | 0.272 g | ✅ |
| **Na2HPO4 . 12H2O** | 0.717 g | 0.717 g | ✅ |
| **Trace Elements** | 0.5 ml | 0.5 ml | ✅ |

## Conclusion

1.  **Identity Confirmed:** **ATCC 1306 IS chemically equivalent to DSMZ 632 (NMS Medium).**
2.  **Spreadsheet Error:** The entry in the CMM spreadsheet associating `ATCC:1306` with "PIPES minimal medium" is **incorrect**. The PIPES medium described in the sheet (Delaney et al.) is a distinct, lab-specific formulation.
3.  **Action Taken:** The local media registry has been updated to decouple the "PIPES minimal medium" node from `ATCC:1306` to prevent provenance errors in the knowledge graph.
