# Scrutiny of Growth Media Assertions for Lanthanide-Utilizing Microbes

## 1. “ATCC Medium 1306 (Methanol mineral salts)” and `ATCC:1306`

### Is there really a medium called that?

- **ATCC Medium 1306** is a real ATCC-defined medium, officially named **“Nitrate mineral salts (NMS)”**.
- Your sheet labels it “Methanol mineral salts”, which is **incorrect**.
- ATCC Medium **1354** is “NMS + 0.1% methanol”—this is the closest match to a methanol‑mineral medium within ATCC’s numbering system.
- General “Methanol mineral salts (MMS)” recipes exist in methylotroph literature but **are not ATCC Medium 1306**.

### What system is `ATCC:1306` from?

- This is **not** a formally maintained CURIE or ontology prefix.
- It is almost certainly a **local identifier scheme** meaning “ATCC medium #1306”.
- If retained, document it as an internal CURIE rather than an externally resolvable identifier.

---

## 2. Are “minimal” vs “complex” distinctions rigorous?

Your assignments are largely correct:

| Medium | Classification | Notes |
|-------|----------------|-------|
| AMS | Minimal / Defined | Derived from NMS, NH₄⁺ replaces NO₃⁻ |
| ATCC 1306 / NMS | Minimal / Defined | Salt + trace medium, no organics |
| NMS (generic) | Minimal / Defined | Standard methanotroph medium |
| MP (PIPES medium) | Minimal / Defined | Chemically defined |
| MPYG | Complex | Peptone + YE = complex |
| DSMZ 88 | Complex | Contains yeast extract |
| LB | Complex | Tryptone + YE |
| R2A | Complex | Multiple hydrolysates |

The only conceptual caution: DSMZ 88 as “Succinate medium” is incorrect—it is formally “Sulfolobus medium”.

---

## 3. Alternative names & descriptions — accuracy issues

### Good / consistent:
- **AMS** names & description: correct relative to published AMS/NMS modifications.
- **MP**: matches Delaney et al.’s “Methylobacterium PIPES (MP) medium”.
- **NMS**: consistent across ATCC, NITE/JCM, cultivation literature.
- **R2A**: canonical and accurate.

### Problems:
- **ATCC:1306** row incorrectly conflates NMS with methanol media.
- **DSMZ 88** alt-name “Succinate medium” has no support in DSMZ or BacDive documentation.
- **MPYG** appears to be a synthesized name with an uncertain reference (“Green and Bousfield 1983”) that cannot be validated as a medium recipe.
- **LB** alt‑names are broadly correct but historically inconsistent (e.g., “Lysogeny broth” is a backronym).

---

## 4. pH & sterilization methods

These values in your sheet look **reasonable**:

- NMS/AMS: pH ~6.8, autoclave base, add methanol/vitamins aseptically.
- MP: pH 6.75, autoclaved salts + sterile methanol supplementation.
- DSMZ 88: pH 2.0 (very acidic), autoclave.
- LB: pH 7.0, autoclave.
- R2A: pH ~7.2, autoclave.

No glaring mistakes—only the media naming is problematic.

---

## 5. Validating `target_organisms`

Your current column uses very broad organism groups. To validate rigorously:

### Recommended workflow
1. **Collect canonical strains** associated with each medium:
   - NMS/AMS: *Methylosinus trichosporium* OB3b, *Methylococcus capsulatus* Bath, etc.
   - MP: *Methylobacterium extorquens* AM1.
   - DSMZ 88: *Sulfolobus acidocaldarius*, *S. solfataricus*, *Metallosphaera sedula*.

2. **Cross-check with authoritative sources**:
   - ATCC medium recommendations per strain.
   - DSMZ / BacDive media usage and strain growth‑media metadata.
   - Methods sections of lanthanide-utilization papers.

3. **Normalize organism identifiers**:
   - Map each group to NCBI Taxon IDs.
   - Validate at least one literature-supported strain grows on the medium.

Currently, your sheet’s organism claims are *plausible but unverified*.

---

## 6. “Whittenbury et al. (1970)” — provenance

The citation refers to:

**Whittenbury, Phillips & Wilkinson (1970). _Enrichment, isolation and some properties of methane-utilizing bacteria_. J. Gen. Microbiol. 61:205–218.**

This paper is the original source of many NMS-like mineral salts medium recipes.

### Relationship to your publications sheet
- This citation **does not appear** in your uploaded publications.tsv.
- If you want a self-contained data package, you should add this DOI.

---

## 7. Are other medium references in `publications.tsv`?

Your growth_media file references:

- Whittenbury 1970 — **missing**
- Bertani 1951 (LB origin) — **missing**
- Green & Bousfield 1983 — **missing**
- Reasoner & Geldreich 1985 (R2A origin) — **missing**
- Delaney et al. 2013 (MP medium) — **missing**

Thus, most references in the media TSV need to be added to the publications dataset.

---

## 8. Recommended validation & cleanup plan

### Step 1 — Correct media identity & naming
- Separate NMS (ATCC 1306) from MMS.
- Add ATCC 1354 (“NMS + methanol”) if relevant.
- Replace “Succinate medium” with “Sulfolobus medium (DSMZ 88)”.

### Step 2 — Add explicit provenance columns
- `primary_reference_doi`
- `canonical_source_url`
- `evidence_code` (ATCC, DSMZ, primary literature, inferred)

### Step 3 — Validate organism usage
Produce a table linking:
- medium_id  
- strain_id  
- ncbi_taxon_id  
- publication_id  
- lanthanide_condition (Y/N)

### Step 4 — Align with publications.tsv
Ensure each cited reference is present with DOI, authors, year, and title.

### Step 5 — Add confidence ratings
Useful categories:
- **high** (ATCC/DSMZ canonical)
- **medium** (well-cited literature)
- **low** (inferred; unclear reference)

---

## 9. Offer to generate a corrected TSV

If you want, I can generate:
- A **cleaned growth_media.tsv** with corrected names, provenance, DOIs, and confidence scores.
- A **cross-link table** (`medium_usage.tsv`) connecting media ↔ organisms ↔ publications.

Just say the word.
