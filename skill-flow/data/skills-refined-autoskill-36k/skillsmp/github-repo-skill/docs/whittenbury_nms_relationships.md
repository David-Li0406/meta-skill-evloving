# Relationships among BacMedia J1221, TogoMedium M511, JCM GRMD 510, ATCC 1306, and Whittenbury et al. (1970)

## Executive summary
These resources are all describing (or derived from) the same *family* of media used for methane/methanol-utilizing bacteria:

- **Whittenbury et al. (1970)** introduces **NMS** (nitrate mineral salts) and **AMS** (ammonium mineral salts) basal media for enrichment/isolation of methane utilizers.
- **JCM GRMD=510** is explicitly **“NMS MEDIUM”** and closely matches the Whittenbury NMS concept, expressed as a modern, fully specified recipe (with a 20× phosphate solution + trace elements).
- **ATCC Medium 1306** is also **“Nitrate mineral salts medium (NMS)”** and its per‑liter phosphate amounts match JCM’s 20× phosphate solution dilution.
- **BacMedia J1221** is **“MODIFIED NITRATE MINERAL SALTS MEDIUM‑2”** (source: JCM) — i.e., a *modified NMS* variant (adds HEPES, vitamins, different trace element recipe/iron handling, and explicit methane vs methanol cultivation steps).
- **TogoMedium M511** is very likely the RDF/aggregated representation of this same “NMS” medium, often with cross‑references to contributing repositories (JCM/DSMZ/ATCC), but you should confirm via the TogoMedium SPARQList API.

## What Whittenbury et al. (1970) actually specifies (NMS/AMS)
Whittenbury et al. describe two basal media, differing only by nitrogen source, and name **NMS** explicitly as nitrate mineral salts:

- Base salts (%, w/v): MgSO4·7H2O (0.1), CaCl2 (0.02), sequestrene iron complex (0.0004), and **KNOW3** (0.1) for **NMS**; agar if added (1.25).  
- They add a **trace element solution** (Pfennig, 1962) and, after cooling, add a sterile **phosphate buffer** made from KH2PO4 and Na2HPO4·12H2O (pH 6.8).

## JCM GRMD 510 vs ATCC 1306: essentially the same NMS “core”
JCM 510 lists (per liter): MgSO4·7H2O 1.0 g, CaCl2·2H2O 0.13 g, ferric citrate 4 mg, KNOW3 1.0 g, trace element solution 0.5 mL, plus **50 mL of a 20× phosphate solution** (KH2PO4 5.44 g/L and Na2HPO4·12H2O 14.3 g/L). pH 6.8.

ATCC 1306 lists (per liter): MgSO4·7H2O 1.0 g, CaCl2·6H2O 0.20 g, KNOW3 1.0 g, trace element solution 0.5 mL, KH2PO4 0.272 g, Na2HPO4·12H2O 0.717 g, plus a chelated iron solution.

Notably: **(5.44 g/L × 50 mL / 1000 mL) = 0.272 g/L** and **(14.3 g/L × 50 mL / 1000 mL) = 0.715 g/L**, matching ATCC’s phosphate amounts.

So: **JCM 510 and ATCC 1306 are two “encodings” of the same NMS recipe** (differences are mostly in iron handling and CaCl2 hydration state).

## BacMedia J1221: a “modified NMS” recipe, not the base NMS
BacMedia J1221’s main solution includes MgSO4·7H2O (1.0 g), CaCl2·2H2O (0.2 g), KNOW3 (0.25 g), FeCl2 solution (1 mL), trace element solution (1 mL), HEPES (2 mL of 1 M), ammonium ferric citrate (4 mg), then separately adds phosphate buffer (2 mL/ L) and vitamin solution (10 mL/L). It also gives explicit methane headspace conditions and a methanol supplementation procedure.

This is best treated as:
- **derived-from / variant-of**: “NMS medium”
- with extra solution-components and cultivation metadata.

## How your ingredient list fits (and where it’s likely “off”)
Your list:

- Agar
- Calcium chloride dihydrate
- Dipotassium phosphate
- Ferrous sulfate heptahydrate
- Magnesium sulfate heptahydrate
- Methanol
- Potassium dihydrogen phosphate
- Potassium nitrate

This resembles “NMS agar” plus a methanol condition — but:
- In the Whittenbury and JCM/ATCC formulations, the **phosphate partner is sodium phosphate (Na2HPO4·12H2O)**, not K2HPO4.
- Iron is typically specified as **chelated iron / sequestrene / ferric citrate / ammonium ferric citrate**, while FeSO4·7H2O appears as part of **trace element solution**, not the sole iron source.
- Methanol is not part of the core NMS recipe; it’s a *substrate condition* (Whittenbury notes methanol toxicity and growth under methanol vapor for many strains).

So this ingredient list looks like it may be:
- a simplified/flattened merge of **base medium + trace elements + cultivation condition**, with some substitutions/mixups.

## Practical next steps for your KG
1. **Ground the “base medium” entity first** (NMS):
   - `https://www.jcm.riken.jp/cgi-bin/jcm/jcm_grmd?GRMD=510` (JCM canonical view)
   - ATCC 1306 PDF URL
   - TogoMedium `M511` (confirm via API)
2. Represent **variants** like BacMedia J1221 as:
   - `variant_of` (or `skos:closeMatch`) the base NMS medium
   - plus explicit `has_ingredient` edges and `has_preparation_step`/`cultivation_condition` edges (e.g., methane headspace; methanol supplementation)
3. Treat **methanol** primarily as a **growth substrate condition**, not a base ingredient, unless a recipe explicitly includes it as an added component with units.
4. Build a small deterministic QA report:
   - compare each asserted medium’s ingredient set against the grounded recipe
   - flag “unexpected” items (e.g., K2HPO4 vs Na2HPO4) and “missing critical” items (e.g., trace element solution).

## Useful TogoMedium automation hook
TogoMedium exposes a SPARQList REST API (see https://togomedium.org/api). The endpoint family includes:
- `/sparqlist/api/gmdb_medium_by_gmid?gmid=...` (medium detail by GMID)

Use that to programmatically retrieve the authoritative component list (and any cross references) for `M511`.
