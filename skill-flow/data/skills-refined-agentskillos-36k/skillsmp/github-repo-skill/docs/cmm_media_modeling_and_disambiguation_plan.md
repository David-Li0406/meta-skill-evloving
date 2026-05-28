# CMM Microbes: Modeling + disambiguation plan for growth media (KGX-first, mapping-driven)

_Date generated: 2026-01-07_

This document codifies a practical pattern for representing **(a) web-resolvable media records**, **(b) literature-described media**, and **(c) your local sheet entities** (which may be novel, corrupted, or incomplete), and for automating the **disambiguation / grounding** process that we just prototyped with “NMS”.

The core idea: **don’t force one node to do everything.** Separate *records*, *recipes*, and *mentions*, then connect them with explicit mapping/provenance.

---

## 0) Why the “NMS” exercise is a template, not a one-off

In the NMS case, you saw:

- A **canonical “family concept”** (NMS / nitrate mineral salts) introduced in literature (Whittenbury et al. 1970).
- Multiple **repository encodings** of essentially the same medium:
  - JCM “NMS MEDIUM” (GRMD=510)
  - ATCC “NMS” (Medium 1306 PDF)
  - TogoMedium “M511” likely representing the same concept in an RDF KB
- A **modified variant** (BacMedia/JCM 1221 “modified NMS-2”) that is clearly related but not identical.

This is the norm for growth media: same basal concept, multiple encodings, plus countless variants.

---

## 1) Modeling pattern: separate *records*, *recipes*, and *mentions*

### 1.1 MediumRecord (web-resolvable catalog entries)
**What it is:** a resolvable entry in an external database (MediaDive, TogoMedium, JCM GRMD, DSMZ medium PDFs, etc.).

- **IDs:** prefer stable CURIEs where available. MediaDive has registered prefixes like `mediadive.medium` and `mediadive.ingredient` with resolvable providers.  
  - Example provider patterns include `https://mediadive.dsmz.de/medium/<id>` and `https://mediadive.dsmz.de/ingredients/<id>`.  
  Sources: Bioregistry entries for MediaDive Medium and Ingredient.  
  - https://bioregistry.io/mediadive.medium  
  - https://bioregistry.io/mediadive.ingredient

- **TogoMedium:** designed as an RDF KB for media recipes, implemented on Virtuoso and exposed via SPARQList API; ingredients are normalized using Growth Medium Ontology (GMO).  
  Source: https://dev.togomedium.org/about/

### 1.2 MediumRecipe (your canonical, machine-comparable “recipe object”)
**What it is:** a normalized representation of the recipe *independent* of any one source encoding.

- Expanded stock solutions → per-liter “molecular composition” where possible
- Normalized ingredient identifiers
- Normalized units (and hydration state where necessary)
- Structured sub-solutions (trace element solution, phosphate buffer, vitamin solution)
- Explicit split of basal vs supplements vs cultivation conditions

This is exactly the kind of “standardized database of recipes and compositions” that MediaDive was built to support. MediaDive also provides per-medium “molecular composition” and download links (CSV/JSON) for compositions.  
Sources:
- MediaDive publication: programmatic access via REST service at `https://mediadive.dsmz.de/rest` and “complete media recipes and compositions”.  
  https://pmc.ncbi.nlm.nih.gov/articles/PMC9825534/
- Example medium page showing “Molecular composition” plus CSV/JSON:  
  https://bacmedia.dsmz.de/medium/215

### 1.3 MediumMention (strings/claims in papers and in your sheets)
**What it is:** a literal string in a source artifact that purports to identify a medium, but may be incomplete, ambiguous, or wrong.

- “NMS”
- “Modified NMS”
- “Methanol mineral salts”
- “ATCC Medium 1306 (Methanol mineral salts)” (often not a faithful name)

A MediumMention should always keep:
- `mention_text` (the literal)
- `source` (paper / sheet / lab notebook)
- `location` (page, table row, DOI, spreadsheet row id)
- `confidence` and/or `status` (unreviewed / suggested / confirmed)

---

## 2) Relationship vocabulary that actually matches the data

### 2.1 Record-to-record mappings (cross-scheme)
Use SKOS mapping properties for cross-repository alignments:

- `skos:exactMatch` for “same thing” links that you consider safe to chain across multiple schemes.
- `skos:closeMatch` for “very similar / likely interchangeable” links that you **do not** want to assume are transitive.

SKOS explicitly declares `skos:exactMatch` transitive and `skos:closeMatch` non-transitive to avoid “compound errors”.  
Source: SKOS mapping properties documentation  
- https://www.w3.org/TR/skos-reference/ (see mapping properties and transitivity discussion)

### 2.2 Recipe-to-recipe relationships (variants)
Treat recipe variation as first-class:

- `cmm:variant_of` (or `biolink:has_variant` / a local predicate if you prefer)
- `cmm:derived_from_recipe`
- `cmm:has_stock_solution`
- `cmm:has_basal_ingredient`
- `cmm:has_supplement` (post-autoclave additions like methanol, vitamins, metals)
- `cmm:has_cultivation_condition` (gas phase, headspace composition, incubation)

This is what NMS taught: methanol is often a **condition/supplement**, not part of the basal medium.

### 2.3 Mention-to-thing (grounding)
For each MediumMention, store grounding candidates:

- `cmm:grounding_candidate` → MediumRecord
- `cmm:grounded_to` → MediumRecord (only after review)

And store the “why” as structured justification (below).

---

## 3) Put provenance on every assertion (this is your main anti-corruption layer)

Use W3C PROV-O to represent transformations and responsible agents:

- `prov:Entity` for input/output artifacts (raw sheets, cleaned exports, intermediate tables, KGX files)
- `prov:Activity` for operations (LLM enrichment run, deterministic normalization, a “partial sort”, a merge, an export)
- `prov:Agent` for people and software agents

Key relations include: `prov:used`, `prov:wasGeneratedBy`, `prov:wasAssociatedWith`, `prov:wasDerivedFrom`.  
Source: PROV-O spec  
- https://www.w3.org/TR/prov-o/

This is what lets you answer “who caused this row to look this way?” *without guessing*.

---

## 4) Use SSSOM for mappings (keep KGX clean, make grounding auditable)

Your KG is going to evolve. Don’t bake all equivalences into the KG immediately.

Instead:

- Keep your “facts” graph in KGX (nodes/edges).
- Keep your “alignments” in SSSOM mapping sets.

SSSOM supports fields like:
- `mapping_justification` (using SEMAPV terms like lexical matching)
- `author_id`
- `reviewer_id`
…which is exactly what you need to track “LLM suggestion vs human confirmation”.  
Source: SSSOM docs  
- https://mapping-commons.github.io/sssom/

---

## 5) How to represent this in KGX

KGX TSV convention is “nodes.tsv + edges.tsv” with Biolink categories/predicates.

- Nodes have an `id` and `category` (Biolink class CURIEs).
- Edges have `subject`, `predicate`, `object` (and optionally `category`, `provided_by`, etc.).

Reference examples:
- KG Hub quick start shows `edges.tsv` columns like `subject`, `edge_label`, `object`, `relation` and Biolink category usage.  
  https://kghub.org/kg-idg/getting_started.html
- Biolink docs show KGX edge layout (`subject predicate object ... category`).  
  https://biolink.github.io/biolink-model/working-with-the-model/

**Practical suggestion:** keep a small internal “CMM vocabulary” (your own `cmm:` CURIE space) for the medium-specific distinctions (mention vs recipe vs record) and map outward as needed.

---

## 6) Automation plan for disambiguation (deterministic first; LLM only as a proposer)

### Step A — build canonical “recipe signatures”
Create normalized recipe objects and compute signatures:

1. **Exact signature**: (ingredient_id, amount, unit, hydration-state) + stock-solution expansions  
2. **Ingredient-bag signature**: ingredient_id set only (ignore amounts)  
3. **Condition signature**: gas phase + substrate additions + timing (post-autoclave vs in base)

This lets you compare:
- JCM “phosphate stock solution” vs ATCC “per-liter phosphate salts”
- recipes with missing quantities (papers) vs fully specified catalog recipes

### Step B — candidate retrieval per source
Use each source the way it’s strongest:

- **MediaDive**
  - RESTful service exists at `https://mediadive.dsmz.de/rest` and includes endpoints for ingredients, solutions, strains, recipes, and compositions.  
    Source: https://pmc.ncbi.nlm.nih.gov/articles/PMC9825534/
  - Per-medium pages include “Molecular composition” and downloadable CSV/JSON.  
    Example: https://bacmedia.dsmz.de/medium/215

- **TogoMedium**
  - Ingredient normalization to GMO and explicit goal of similarity measures across media.  
    Source: https://dev.togomedium.org/about/
  - Retrieve candidate media using their component search UI and SPARQList API.

- **JCM GRMD**
  - Treat GRMD pages as authoritative “recipe pages” for JCM-numbered media.
  - Use catalog search to resolve medium names to GRMD IDs, then parse `jcm_grmd?GRMD=<id>`.

- **BacMedia**
  - Media pages expose structured tables and JSON exports that are straightforward to parse.

### Step C — matching ladder
1. **Direct ID match** in mention: “GRMD=510”, “DSMZ Medium 88”, “ATCC 1306” → strong grounding
2. **Exact signature match** → `skos:exactMatch`
3. **High overlap with explainable diffs** → `skos:closeMatch` + `variant_of` at recipe level
4. **Only name/partial list** → keep as MediumMention; ground to a family concept node until resolved

### Step D — outputs
- **KGX graph**: everything instantiated, including uncertain MediumMentions and local variants
- **SSSOM mapping sets**: your evolving grounding decisions with justification and review state

This separation is what makes the system maintainable.

---

## 7) One high-leverage rule to adopt immediately
**No growth assertion should point only to a raw medium string.**

Every growth assertion (strain → grows_in → medium) must point to either:
- a grounded external MediumRecord, or
- a normalized MediumRecipe node (with explicit provenance),
and any raw strings must be captured as MediumMentions linked to those nodes.

That single rule will stop most silent “spreadsheet drift” from contaminating the KG.

---

## 8) Minimal file artifacts to maintain in-repo
I’d recommend committing these (regeneratable) artifacts to your repo:

- `kgx/nodes.tsv` and `kgx/edges.tsv` (facts graph)
- `mappings/mediummention_to_record.sssom.tsv`
- `mappings/recipe_to_record.sssom.tsv`
- `mappings/ingredient_to_gmo_or_mediadive.sssom.tsv`
- `provenance/activities.tsv` (or RDF) describing pipeline steps using PROV-O terms

---

## Appendix: Quick reference links
- PROV-O (provenance): https://www.w3.org/TR/prov-o/
- SKOS mapping properties: https://www.w3.org/TR/skos-reference/
- SSSOM: https://mapping-commons.github.io/sssom/
- MediaDive REST access described here: https://pmc.ncbi.nlm.nih.gov/articles/PMC9825534/
- MediaDive medium composition example (CSV/JSON): https://bacmedia.dsmz.de/medium/215
- TogoMedium design & GMO usage: https://dev.togomedium.org/about/
- KGX TSV overview via KG Hub example: https://kghub.org/kg-idg/getting_started.html
- Biolink KGX edge layout example: https://biolink.github.io/biolink-model/working-with-the-model/
- Bioregistry prefixes:
  - MediaDive Medium: https://bioregistry.io/mediadive.medium
  - MediaDive Ingredient: https://bioregistry.io/mediadive.ingredient
