# Chapter 3: Data Quality Issues

[<- Back to Index](00_index.md) | [Previous: Data Model Analysis](02_data_model_analysis.md) | [Next: Code Analysis ->](04_code_analysis.md)

---

## UTF-8 Encoding Corruption (Mojibake)

Present in Google Sheet-derived TSV files:

| Corrupted | Should Be |
|-----------|-----------|
| `..` | `*` (middle dot for hydrates) |
| `..` | micro sign |
| `...` | subscript 2 |
| `...` | subscript 4 |

**Examples:**
- `MgSO4..7H2O` -> should be `MgSO4*7H2O`
- `20 ..M` -> should be `20 uM`
- `K..HPO..` -> should be `K2HPO4`

**Root cause**: UTF-8 encoded text interpreted as Latin-1 or Windows-1252 during Google Sheets -> XLSX -> TSV conversion.

**Fix options**:
1. Fix in Google Sheets source (preferred)
2. Add post-processing step in `convert_sheets.py` to detect and correct mojibake
3. Use Python `ftfy` library for automated fix

---

## Inconsistent Units

Media ingredients use multiple unit systems without conversion:
- Mass concentration: `g/L`
- Volume ratio: `mL/L`, `% (v/v)`
- Molar concentration: `mM`, `uM`

---

## Undefined Vocabularies

### Role values (not in schema or docs):
- mineral
- nitrogen source
- buffer
- trace element
- carbon source
- solidifying agent
- vitamin source
- protein source
- amino acid source
- salt

### kg_microbe_nodes prefixes (not documented):
| Prefix | Meaning |
|--------|---------|
| `CHEBI:` | ChEBI ontology ID |
| `solution:` | KG-Microbe internal - stock solution node |
| `ingredient:` | KG-Microbe internal - ingredient entity |
| `CAS-RN:` | Chemical Abstracts Service Registry Number |
| `medium:` | KG-Microbe internal - complete medium formulation |

**Issue**: Multiple values concatenated with semicolons have unclear semantics (are they equivalent? alternatives? related?)

---

## FAKE Publications (Critical Data Quality Issue)

**File**: `src/publication_search.py` lines 172-205

**These DOIs/URLs DO NOT EXIST:**

```python
# From search_arxiv_preprints() - lines 170-187
{"url": "https://arxiv.org/abs/2309.12345", ...},  # FAKE
{"url": "https://arxiv.org/abs/2308.54321", ...},  # FAKE

# From search_biorxiv_preprints() - lines 190-213
{"url": "https://www.biorxiv.org/content/10.1101/2023.09.15.557123v1", ...},  # FAKE
{"url": "https://www.biorxiv.org/content/10.1101/2023.08.22.554321v1", ...},  # FAKE
```

**This is classic LLM hallucination** - generating plausible-looking but non-existent URLs.

**Impact**: If these functions are called, fabricated data will contaminate the database.

**Required action**: DELETE these fake entries from the codebase.

---

## Missing Provenance

### What We Cannot Determine

For hardcoded data structures (media, assays, genes, publications), we cannot determine:

1. **Who** created the data?
2. **When** was it created?
3. **What source** was used (if any)?
4. **Has it been validated** against authoritative sources?
5. **Is it complete** or just a sample?

### Ingredient Roles - No References

The roles in `media_search.py` (carbon source, nitrogen source, buffer, mineral, trace element, etc.) are:
- Generic/reasonable but not authoritative
- No citations or references
- Consistent with LLM knowledge of microbiology basics
- **Not validated against any database**

All ingredient roles in `CURATED_MEDIA` were hardcoded with **NO reference sources** cited.

---

## Assay Protocol Concerns

**File**: `src/assay_search.py` lines 26-132

7 complete assay protocols are hardcoded with potential issues:

- Protocol URLs like `protocols.io/view/lanthanide-trl-htp-screening` may not exist
- References like `Protocol_TRL_HTP_v1` are internal names with no source
- No provenance for detection limits, equipment specs, etc.

---

## Gene Database Issues

**File**: `src/gene_search.py` lines 25-120

15+ lanthanide-related genes are hardcoded with:

- Mix of real KEGG IDs (K23995) and custom IDs (custom_mxbD)
- Custom IDs have no documentation
- GO/CHEBI terms manually assigned without references

---

## Documentation Gaps

### What IS Documented

| Topic | Location | Quality |
|-------|----------|---------|
| Make commands | CLAUDE.md, README.md | Good |
| Python module purposes | CLAUDE.md | Good |
| LinkML schema | CLAUDE.md, schema/*.yaml | Good |
| Code style | AGENTS.md | Good (but outdated paths) |
| API integrations | README.md | Good |

### What is NOT Documented

| Missing | Impact |
|---------|--------|
| Google Sheet -> XLSX -> TSV workflow | Cannot understand data entry process |
| Who enters what data where | No roles/responsibilities |
| Manual vs LLM-generated data | Cannot distinguish sources |
| When/how XLSX is downloaded | No versioning or triggers |
| Relationship between TSV and extended/ | Which is authoritative? |
| Role vocabulary for ingredients | Values undefined |
| kg_microbe_nodes ID prefixes | What do solution:, ingredient: mean? |

### AGENTS.md is Outdated

The file references things that don't exist:
- `src/cmm_ai/` -> actual path is `src/`
- `docs/` -> directory doesn't exist
- `mkdocs.yml` -> file doesn't exist
- `just --list` -> no justfile (only `ai.just`)
- `tests/input` -> no tests/ directory

---

## Reproducibility Issues

### Reproducible

| Step | Command | Output |
|------|---------|--------|
| XLSX -> TSV conversion | `make convert-excel` | `data/txt/sheet/*.tsv` |
| Generate extended tables | `make update-all` | `data/txt/sheet/extended/*_extended.tsv` |
| Generate media from Python dict | `make update-media` | growth_media_extended.tsv, media_ingredients_extended.tsv |
| Validate schema | `make validate-schema` | Validation report |
| Validate consistency | `make validate-consistency` | Consistency report |

### NOT Reproducible

| Data | Why Not |
|------|---------|
| Google Sheet content | No version history in repo |
| MP medium data | Not in Python code, origin unknown |
| Manual entries | No record of who/when/what |
| LLM-generated content | No prompts or outputs saved |
| kg_microbe_nodes in Google Sheet | Different from what extend scripts generate |

---

## Questions Requiring Human Answers

1. **Who is responsible for Google Sheet data entry?**
   - Names/roles of collaborators
   - What data they're expected to enter

2. **What is the download/conversion cadence?**
   - How often is XLSX downloaded?
   - What triggers a download?

3. **Which version is authoritative?**
   - Google Sheet TSV (`data/txt/sheet/`)
   - Extended TSV (`data/txt/sheet/extended/`)
   - Or are they meant to be merged?

4. **Where did MP medium data come from?**
   - Manual entry?
   - LLM generation?
   - Literature extraction?

5. **Are LLMs being used to generate data?**
   - If yes, which LLM?
   - What prompts?
   - Where are outputs reviewed?

6. **What is the intended merge strategy?**
   - Does extended data flow back to Google Sheets?
   - Does Google Sheet data override extended?

---

[<- Back to Index](00_index.md) | [Previous: Data Model Analysis](02_data_model_analysis.md) | [Next: Code Analysis ->](04_code_analysis.md)
