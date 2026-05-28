# Relationship between BacMedia J1221, TogoMedium M511, and JCM GRMD=510 — and how they relate to ATCC Medium 1306

## What we can say with high confidence (directly supported by the sites)

### 1) **BacMedia `J1221` is the same recipe as JCM `GRMD=1221` (not GRMD=510)**
BacMedia explicitly states the source is **JCM** and links to **JCM GRMD=1221**:
- BacMedia JSON has `"source":"JCM"` and `"link":"https://www.jcm.riken.jp/cgi-bin/jcm/jcm_grmd?GRMD=1221"` and the composition matches JCM 1221 ingredient-for-ingredient.

So:
- `https://bacmedia.dsmz.de/medium/J1221`  **≡**  `https://www.jcm.riken.jp/cgi-bin/jcm/jcm_grmd?GRMD=1221`

### 2) **JCM `GRMD=510` is a related “NMS medium”, but it is a *different* recipe than JCM 1221 / BacMedia J1221**
JCM `GRMD=510` is labeled **“NMS MEDIUM”** and includes (among other items):
- MgSO4·7H2O, CaCl2·2H2O, ferric citrate, KNOW3
- plus **20× phosphate solution** and **trace element solution**
- and cultivation guidance for methane (methane–air gas mixture)

By contrast, JCM `GRMD=1221` (“MODIFIED NITRATE MINERAL SALTS MEDIUM-2”) includes:
- MgSO4·7H2O, CaCl2·2H2O, KNOW3
- **FeCl2 solution**, **trace element solution**, **HEPES**, ammonium ferric citrate
- plus **phosphate buffer solution** and **vitamin solution**
- and explicitly allows **methane or methanol** (methanol added after sterilization)

So: `GRMD=510` and `GRMD=1221` share a family resemblance (both are NMS-type mineral salts media used for methanotroph/methylotroph cultivation), but they are *not identical*.

---

## The uncertain part: where TogoMedium `M511` fits
TogoMedium provides a REST API (via SPARQList) and its media IDs look like `M####`, while also storing a “source ID” field like `JCM_M####` for JCM-derived records.

However, in this environment I could not retrieve the *details page* or the `gmdb_medium_by_gmid` API response specifically for `M511`, so I cannot prove whether:
- `M511` corresponds to **JCM GRMD=510**, or
- it corresponds to some other source record.

**Working hypothesis (to verify):** `M511` is very likely TogoMedium’s normalized record for **JCM GRMD=510** because of the close number match and the way TogoMedium ingests JCM medium records.

### Quick verification procedure (manual / interactive)
1. Use the TogoMedium API to fetch the medium:
   - Try `gmdb_medium_by_gmid` for `M511` (via the TogoMedium API docs: https://togomedium.org/api)
2. Confirm whether `original_media_id` equals something like `JCM_M510` / `JCM_510` / similar.
3. Compare the component list in that response to the JCM GRMD=510 page.

---

## How the ATCC Medium 1306 PDF relates
From the uploaded **ATCC Medium 1306** PDF (page 1), the “Nitrate mineral salts medium (NMS)” recipe includes (among other items):
- **MgSO4·7H2O**
- **CaCl2 (a hydrate form)**
- **KNOW3**
- **KH2PO4** and a second phosphate salt (a sodium phosphate hydrate)
- **chel(ated) iron solution**
- **trace element solution**
- **agar** (so this is explicitly a solid medium recipe)

This makes ATCC 1306 clearly part of the same **NMS / nitrate mineral salts** family as the JCM 510 / JCM 1221 recipes, but:
- ATCC 1306 is not identical to JCM 510 (different iron, explicit agar, etc.)
- ATCC 1306 is not identical to JCM 1221 (JCM 1221 uses HEPES and separate FeCl2 solution; no agar in the base recipe)

---

## How your ingredient list relates
Your list:

- Agar  
- Calcium chloride dihydrate  
- Dipotassium phosphate  
- Ferrous sulfate heptahydrate  
- Magnesium sulfate heptahydrate  
- Methanol  
- Potassium dihydrogen phosphate  
- Potassium nitrate  

### Most likely explanation
This looks like **a simplified / partially “mutated” NMS recipe** that mixes elements from:
- **ATCC 1306** (because of *agar* plus the “classic” mineral salts backbone), and
- **JCM 1221 / BacMedia J1221** (because *methanol* is explicitly used as a substrate there).

And it appears to contain **substitutions** that are *not* in the authoritative recipes above, such as:
- using **K2HPO4** (dipotassium phosphate) instead of the **Na2HPO4 hydrate** used in the JCM/ATCC phosphate buffers,
- using **FeSO4·7H2O** instead of the chelated iron solution / ferric citrate / FeCl2 solution patterns found in the referenced recipes.

So your list is “in the right neighborhood”, but as a grounding target it should be treated as **suspect until you can tie it to a known source recipe** (ATCC/DSMZ/JCM/etc.), ideally by:
- matching **hydration state** (e.g., CaCl2·2H2O vs CaCl2·6H2O),
- matching **which phosphate pair** is used (K/Na vs K/K), and
- matching **iron formulation** (FeCl2 vs ferric citrate vs chelated iron vs FeSO4).

---

## Suggested debugging move (high leverage)
For each “medium name” in your sheet, store **one of these as provenance**:
- a stable medium ID (ATCC, DSMZ, JCM GRMD, BacMedia, TogoMedium), plus
- the URL of the canonical recipe page/PDF, plus
- a hash (or normalized component list signature) of the ingredient composition you believe is canonical.

Then, treat any row that *lacks* a canonical ID+URL as “un-grounded” and don’t propagate it into KGX until reviewed.
