# Growth media grounding & retrieval notes (JCM / DSMZ / MediaDive / TogoMedium / ATCC)

_Date generated: 2026-01-07 (America/New_York)_

This note captures **web-discovered retrieval options** for grounding growth-media records (medium ↔ ingredients ↔ strains) to **stable, web-resolvable IDs**, with an emphasis on **search interfaces and bulk-ish access** (not “guessing a numeric ID from a base URL”).

---

## Context and immediate goal

You have a set of sheets describing:
- **ingredients**
- **media**
- **strain ↔ medium** growth assertions
- **medium ↔ ingredient** assertions

The top priority is **grounding “media” to stable IDs** in external, resolvable repositories (MediaDive / TogoMedium / JCM / DSMZ / ATCC, etc.), so that:
1) you can compare and debug asserted recipes,
2) you can automate enrichment and QA, and
3) you can publish a KGX knowledge graph with resolvable identifiers.

---

## What we already produced from your uploaded sheets (local artifacts)

These were generated earlier from your TSVs (and are meant to help you jump straight into debugging + grounding):

- `medium_grounding_candidates.tsv` — normalized “best-effort” grounding candidates per medium name (string- and pattern-based).
- `component_lists.tsv` — per-medium canonicalized ingredient lists (good for ingredient-based “finder” UIs).
- `mediadive_finder_inputs.tsv` — rows you can copy/paste toward MediaDive’s **Medium Finder** style queries.
- `ingredient_nodes.tsv` and `kgx_medium_has_ingredient_edges.tsv` — KGX-ready node/edge extracts (for incremental QC).

(These exist in this sandbox environment; if you want them checked in to a repo, I’d recommend copying them out and versioning them.)

---

## Key web findings: where you can *search* and how you can retrieve recipes

### 1) JCM (RIKEN) culture media: searchable + direct “medium data” pages

#### A. Direct recipe page by medium number
Example (your prompt): **JCM medium 510 (NMS MEDIUM)**  
- https://www.jcm.riken.jp/cgi-bin/jcm/jcm_grmd?GRMD=510

This page is a human-readable recipe and is structured enough to scrape:
- has a stable “GRMD” numeric identifier
- includes ingredients + amounts
- often includes sub-solutions (e.g., “Trace element solution”, “Phosphate solution”)

#### B. Search interface that includes “Culture medium”
JCM’s **On-line Catalogue of Strains** page includes a “Culture medium” search block with:
- **JCM Medium No.** (exact match)
- **Name of Medium** (substring match)

Entry point:
- https://jcm.brc.riken.jp/en/catalogue_e

This matters because it gives you a **name→number lookup** path (so you don’t need to already know GRMD IDs).

**Practical use:** for each “un-grounded” medium name in your sheet:
1) try searching by “Name of Medium” to find candidate medium numbers,
2) then open `jcm_grmd?GRMD=<num>` to retrieve the recipe for validation and ingredient extraction.

---

### 2) DSMZ “List of Media for Microorganisms” is an indexable listing (with links)

DSMZ maintains a **large HTML table** listing medium numbers + names and (in practice) links out to the recipe PDFs and/or MediaDive pages.

Entry point:
- https://www.dsmz.de/collection/catalogue/microorganisms/culture-technology/list-of-media-for-microorganisms

Notes:
- The page explicitly points users to MediaDive as the “novel database” for >3,200 cultivation media and offers tools like the Medium Finder and Medium Builder (so DSMZ is steering usage toward MediaDive for programmatic + normalized access).
- The table is long; but it’s machine-indexable and (in many cases) provides direct navigation to each medium’s detail/download.

**Practical use:** treat this DSMZ page as the “search interface” you wanted:
- It can seed a **bulk crawl** of DSMZ medium numbers/names.
- It provides a sanity-check index for mediums claimed in your sheet as “DSMZ Medium <N>”.

---

### 3) MediaDive (DSMZ) is the best “ground truth” hub for DSMZ + a lot of JCM media

#### A. MediaDive website tools
MediaDive’s manual describes:
- **Medium finder** (ingredient-based)
- **Medium builder**
- **Compare media**
- **Download content** (including text, CSV/JSON for compositions, etc.)
- **SPARQL endpoint** link from the manual navigation

Manual entry point:
- https://mediadive.dsmz.de/docs/website

The paper describing MediaDive states that data can be retrieved via a **RESTful web service** for large-scale analyses, and that the dataset includes large numbers of DSMZ and JCM media.

Reference (NAR / PMC):
- https://pmc.ncbi.nlm.nih.gov/articles/PMC9825534/

#### B. “Download content” and API-ish access
The manual notes multiple download options (PDF/text for recipes; CSV/JSON for solution & composition tables; plus “URL-based API” mentioned in the manual).

**Practical use:** since you already have MediaDive data cloned into local MongoDB, you can:
- use MediaDive **as the canonical ID space** for recipes, and
- treat ingredient-based matching as a second-pass QA check when names/IDs don’t match.

---

### 4) TogoMedium: aggregated media knowledge base + component search + RDF/ontology ecosystem

TogoMedium provides a **Find media by components** interface:
- https://togomedium.org/find-media-by-components

TogoMedium is positioned as a comprehensive media knowledge base aggregated from multiple resources:
- https://togomedium.org/about

A “dev/about” page explicitly states (as of March 2023) the breakdown of media sources, including a large slice from **JCM**:
- https://dev.togomedium.org/about/

A Japanese article describing TogoMedium discusses the broader approach (RDF for media, and development of a “Growth Medium Ontology (GMO)”):
- https://www.jstage.jst.go.jp/article/jsb/78/1/78_15/_pdf/-char/ja

**Practical use:** TogoMedium can act as:
- an additional stable ID namespace for media recipes,
- a crosswalk target when JCM/DSMZ representations diverge,
- a source of curated component terms / ontology organization (GMO).

---

### 5) ATCC media: accessible PDFs exist, but “search/bulk” is the hard part

You already have examples of ATCC media preparation PDFs (e.g., “ATCC Medium 1306”, “ATCC Medium 2099”).

The key issue (as you noted) is that **knowing the base PDF URL is not enough**; you need:
- a searchable catalog or listing, or
- a dataset export, or
- a consistent robot-accessible endpoint that returns medium metadata.

**Practical strategy (until ATCC exposes better bulk access):**
1) Prioritize grounding to **MediaDive / DSMZ / JCM / TogoMedium** first (since they’re clearly indexable and provide programmatic affordances).
2) For ATCC:
   - treat the medium PDFs as **secondary evidence** (to validate or correct recipes),
   - keep ATCC IDs as literals or “secondary identifiers” until a reliable search/bulk path is found.
3) Where possible, use MediaDive/TogoMedium to find equivalent media that correspond to ATCC formulations (when a medium has a known synonym like “NMS”, “MMS”, “R2A”, etc.).

---

## “Can we search this site?”: JCM medium 510 page and broader search

Yes:
- The specific medium page is accessible at: https://www.jcm.riken.jp/cgi-bin/jcm/jcm_grmd?GRMD=510
- The JCM catalogue search supports “JCM Medium No.” and “Name of Medium” searches (via the strain catalogue page): https://jcm.brc.riken.jp/en/catalogue_e

So you can automate:
- name → candidate medium number(s) via the catalogue search,
- medium number → recipe via `jcm_grmd?GRMD=<num>`.

---

## Suggested next steps for interactive retrieval & early automation

### A) Establish a “grounding ladder” (highest-trust → lowest-trust)

1. **MediaDive IDs** (if present or matchable)  
   - Most useful for normalized recipes + downstream computation.
2. **TogoMedium IDs** (especially if it clearly maps to JCM/NBRC or literature-derived media)
3. **JCM GRMD IDs** (when you can match the medium name/number)
4. **DSMZ Medium numbers / PDF links** (as evidence; often you’ll also find a MediaDive page)
5. **ATCC** (PDF evidence; keep as secondary identifier until a better bulk/search approach is found)

### B) Build “retrieval adapters” (lightweight, deterministic)

**Adapter 1: JCM recipe retrieval**
- Input: GRMD number
- Output: parsed list of ingredient rows + sub-solutions + pH + sterilization notes (where present)
- Source: `https://www.jcm.riken.jp/cgi-bin/jcm/jcm_grmd?GRMD=<num>`

**Adapter 2: DSMZ index**
- Input: medium name token(s) or medium number
- Output: candidate links to DSMZ PDF and/or MediaDive page
- Source: DSMZ “List of Media for Microorganisms” table page

**Adapter 3: MediaDive lookups**
- Input: medium name token(s) and/or ingredient set
- Output: candidate MediaDive medium IDs + normalized recipe components
- Source: MediaDive website & API capabilities (plus your local MongoDB clone)

**Adapter 4: TogoMedium component search**
- Input: ingredient set (strings)
- Output: candidate TogoMedium media IDs

### C) Add QA hooks that catch “sheet corruption” early

Given the risk profile you described (partial sorts, LLM edits, drift, etc.), add cheap QC checks:
- **Row identity checks:** stable row IDs (UUIDs) per asserted relation.
- **Foreign key checks:** every edge refers to an existing node ID.
- **Ingredient normalization checks:** unit parsing, casing, whitespace, Unicode normalization.
- **Duplicate detection:** same strain+medium+predicate duplicated with conflicting evidence.
- **“Round-trip” checks:** export → import → export should be stable.

---

## Concrete experiments to run next (interactive)

1) Pick ~10 “highest-impact” media from your KG (most strains, or most heavy-metal/lanthanide-related assertions).
2) For each:
   - Try MediaDive name match (and check if it has a stable medium ID).
   - If it looks like a JCM medium, search JCM catalogue by medium name → retrieve GRMD recipe.
   - Run ingredient-set queries against:
     - MediaDive finder: https://mediadive.dsmz.de/finder
     - TogoMedium components: https://togomedium.org/find-media-by-components
3) Compare:
   - sheet ingredients vs retrieved recipe ingredients
   - sheet naming vs canonical names
   - “base medium” vs “supplement” components (trace elements/vitamins, metals, etc.)

---

## Source links (for quick reference)

- JCM medium recipe page pattern (example GRMD=510): https://www.jcm.riken.jp/cgi-bin/jcm/jcm_grmd?GRMD=510  
- JCM on-line catalogue (includes Culture medium search): https://jcm.brc.riken.jp/en/catalogue_e  
- DSMZ list of media table: https://www.dsmz.de/collection/catalogue/microorganisms/culture-technology/list-of-media-for-microorganisms  
- MediaDive manual (website/tools/downloads; includes SPARQL endpoint link): https://mediadive.dsmz.de/docs/website  
- MediaDive publication (describes RESTful retrieval and dataset scope): https://pmc.ncbi.nlm.nih.gov/articles/PMC9825534/  
- TogoMedium “find by components”: https://togomedium.org/find-media-by-components  
- TogoMedium about: https://togomedium.org/about  
- TogoMedium dev about (explicit source breakdown including JCM counts): https://dev.togomedium.org/about/  
- J-Stage article mentioning TogoMedium + Growth Medium Ontology (GMO): https://www.jstage.jst.go.jp/article/jsb/78/1/78_15/_pdf/-char/ja  

---

## If you want, I can also generate a “retrieval plan” YAML

If you want to move toward automation, the next useful artifact is a small config (YAML) that declares:
- identifier patterns (DSMZ Medium <N>, JCM Medium <N>, ATCC Medium <N>, etc.)
- per-source retrieval adapters (base URLs, query params, throttling)
- parsing rules (tables vs PDFs vs HTML)
- output schema (KGX nodes/edges; evidence/provenance; version stamps)

But the above should be enough to start: **JCM & DSMZ are searchable/indexable; MediaDive/TogoMedium are the best grounding hubs; ATCC is “evidence first” until a better bulk/search approach is found.**
