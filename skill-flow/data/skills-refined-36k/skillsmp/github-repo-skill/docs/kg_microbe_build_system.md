# kg-microbe Build System Reference

**Date:** 2026-01-08
**Based on:** kg-microbe commit `cddcd79`
**Purpose:** Document build commands, available transforms, and architecture for CMM team use

---

## Quick Reference

```bash
cd ~/gitrepos/kg-microbe

# Full pipeline
poetry run kg download -y download.yaml -o data/raw
poetry run kg transform
poetry run kg merge

# Selective transform for CMM work (CORRECT ORDER - ontologies first!)
poetry run kg transform -s ontologies && poetry run kg transform -s bacdive -s bactotraits -s madin_etal -s mediadive

# Selective merge
poetry run kg merge -y merge.cmm.yaml  # (create custom config first)
```

**⚠️ Transform order matters!** See [Transform Dependencies](#transform-dependencies) below.

---

## CLI Commands

### Download

```bash
poetry run kg download [OPTIONS]

Options:
  -y PATH    YAML config file (required, e.g., download.yaml)
  -o TEXT    Output directory (required, e.g., data/raw)
  -x         Download only first 5 kB (for testing)
  -i         Ignore cache, force re-download
```

**Re-running is safe:** Existing files are cached. Only use `-i` if you need fresh copies.

### Transform

```bash
poetry run kg transform [OPTIONS]

Options:
  -i PATH    Input directory (default: data/raw)
  -o TEXT    Output directory (default: data/transformed)
  -s SOURCE  Specific source(s) to transform (repeatable)
  --show-status / --no-show-status
```

**Available sources:**
```
-s [ontologies|bacdive|bakta|cog|kegg|mediadive|madin_etal|rhea_mappings|bactotraits]
```

### Merge

```bash
poetry run kg merge [OPTIONS]

Options:
  -y PATH      YAML merge config (default: merge.yaml)
  -p INTEGER   Number of processes
```

---

## Available Transforms

| Transform | Description | Input Data | Notes |
|-----------|-------------|------------|-------|
| `bacdive` | Microbial strain traits | `bacdive_strains.json` (Google Drive) | Core CMM source |
| `bactotraits` | Microbial traits database | `BactoTraits_databaseV2_Jun2022.csv` | Core CMM source |
| `madin_etal` | Condensed traits (bacteria-archaea-traits) | `madin_etal.csv` (GitHub) | Core CMM source |
| `mediadive` | Growth media, solutions, ingredients | MediaDive API + cached JSON | **New from Marcin** |
| `ontologies` | NCBITaxon, ChEBI, ENVO, GO, EC, METPO, UPA | OBO PURLs | Expensive (large ontologies) |
| `bakta` | Gene annotations | CMM-specific Bakta files | New in 2026-01 |
| `cog` | Clusters of Orthologous Groups | NCBI FTP (`cog-24.def.tab`) | New in 2026-01 |
| `kegg` | KEGG orthologs | KEGG REST API | New in 2026-01 |
| `rhea_mappings` | Rhea reaction → GO/EC mappings | Expasy FTP | Supporting data |

### CMM-Relevant Subset

For CMM work, you need ontologies plus the trait sources:
```bash
poetry run kg transform -s ontologies && poetry run kg transform -s bacdive -s bactotraits -s madin_etal -s mediadive
```

---

## Transform Dependencies

**Critical:** Some transforms depend on outputs from other transforms. Running them out of order causes failures or slow fallbacks.

### The `ontologies` → `bacdive` Dependency

The `bacdive` transform needs `data/transformed/ontologies/ncbitaxon_nodes.tsv` for fast taxon label lookups. If this file doesn't exist:

```
Warning: NCBITaxon nodes file not found at data/transformed/ontologies/ncbitaxon_nodes.tsv
  Will fall back to OakLib queries (slower)
```

**The OakLib fallback is ~3x slower and should be avoided.**

### Correct Order

```bash
# Step 1: Run ontologies first (creates ncbitaxon_nodes.tsv)
poetry run kg transform -s ontologies

# Step 2: Run other transforms (can read ncbitaxon_nodes.tsv)
poetry run kg transform -s bacdive -s bactotraits -s madin_etal -s mediadive
```

Or as a single command:
```bash
poetry run kg transform -s ontologies && poetry run kg transform -s bacdive -s bactotraits -s madin_etal -s mediadive
```

### Ontologies is Faster (When Cached)

The expensive part of ontologies transform is ROBOT processing of `ncbitaxon.owl` (~1.6GB). However, if you have the cached JSON file, ROBOT is skipped:

| File | Size | What It Means |
|------|------|---------------|
| `data/raw/ncbitaxon_removed_subset.json` | ~623MB | ROBOT already ran, will be reused |
| `data/raw/chebi.json` | ~482MB | ROBOT already ran, will be reused |

**Check if you have the cache:**
```bash
ls -lh data/raw/ncbitaxon_removed_subset.json data/raw/chebi.json
```

If these exist, the ontologies transform skips ROBOT processing (still takes time, but not hours).

### Filename Case Issue (Fixed in #475)

There was a bug where `bacdive.py` looked for `NCBITaxon_nodes.tsv` (mixed case) but ontologies creates `ncbitaxon_nodes.tsv` (lowercase). This was fixed in commit `26c029b` (PR #477).

If you're on an older version, update:
```bash
git pull origin main
```

### Safe Files During Interrupted Transforms

If you ctrl-C during a transform, your **raw files are safe**:

| Directory | Safe? | Why |
|-----------|-------|-----|
| `data/raw/` | ✅ Yes | Transforms only READ from here |
| `data/transformed/` | ⚠️ May be partial | Transforms WRITE here - may need to re-run |

Expensive cached files that survive interruption:
- `data/raw/ncbitaxon_removed_subset.json` (623MB)
- `data/raw/chebi.json` (482MB)
- `data/raw/bacdive_strains.json` (748MB)
- `data/raw/mediadive/` (42MB total)

---

## Merge Configurations

Three merge configs exist:

| File | Contents | Use Case |
|------|----------|----------|
| `merge.yaml` | Full KG (all active sources) | Production releases |
| `merge.minimal.yaml` | bacdive + madin_etal only | Quick testing |
| `merge.current.yaml` | bacdive + madin_etal + bactotraits | Development |

### Creating a CMM-Specific Merge Config

```bash
cp merge.current.yaml merge.cmm.yaml
# Edit to add mediadive source, then:
poetry run kg merge -y merge.cmm.yaml
```

Example addition for `merge.cmm.yaml`:
```yaml
    mediadive:
      name: "mediadive"
      input:
        format: tsv
        filename:
          - data/transformed/mediadive/nodes.tsv
          - data/transformed/mediadive/edges.tsv
```

---

## Directory Structure

```
kg-microbe/
├── data/
│   ├── raw/              # Downloaded source files (cached)
│   │   ├── bacdive_strains.json
│   │   ├── mediadive.json
│   │   ├── mediadive/    # Cached MediaDive API responses
│   │   └── ...
│   ├── transformed/      # Transform outputs (nodes.tsv, edges.tsv per source)
│   │   ├── bacdive/
│   │   ├── bactotraits/
│   │   ├── mediadive/
│   │   ├── ontologies/
│   │   └── ...
│   └── merged/           # Final merged KG
│       └── merged-kg/
├── download.yaml         # Download configuration
├── merge.yaml            # Full merge configuration
├── merge.minimal.yaml    # Minimal merge configuration
├── merge.current.yaml    # Development merge configuration
└── kg_microbe/
    ├── transform.py      # Transform dispatcher
    └── transform_utils/  # Per-source transform code
        ├── bacdive/
        ├── mediadive/
        └── ...
```

---

## Architecture: Standard Tools vs Custom Code

| Component | Standard BBOP/KGX Tool | Custom kg-microbe Code |
|-----------|------------------------|------------------------|
| **Download** | `kghub-downloader` | Config only (`download.yaml`) |
| **Merge** | KGX merge library | Config only (`merge.yaml`) |
| **Transform** | **None** | Custom Python per source |
| **Node/Edge schema** | **None** | Hardcoded in `Transform` base class |

### The Transform Framework

kg-microbe uses a custom `Transform` base class (`kg_microbe/transform_utils/transform.py`) rather than KGX instantiators:

```python
# From transform_utils/transform.py lines 53-75
self.node_header = [
    ID_COLUMN,
    CATEGORY_COLUMN,
    NAME_COLUMN,
    DESCRIPTION_COLUMN,
    XREF_COLUMN,
    PROVIDED_BY_COLUMN,
    SYNONYM_COLUMN,
    IRI_COLUMN,
    OBJECT_COLUMN,      # ← Edge column in node header
    PREDICATE_COLUMN,   # ← Edge column in node header
    RELATION_COLUMN,    # ← Edge column in node header (deprecated in Biolink 3.x)
    SAME_AS_COLUMN,
    SUBJECT_COLUMN,     # ← Edge column in node header
    SUBSETS_COLUMN,
]
self.edge_header = [
    SUBJECT_COLUMN,
    PREDICATE_COLUMN,
    OBJECT_COLUMN,
    RELATION_COLUMN,
    PRIMARY_KNOWLEDGE_SOURCE_COLUMN,
]
```

**This explains why:**
- Node files have edge-specific columns (`subject`, `predicate`, `object`, `relation`) - baked into base class
- Edge files have only 5 columns (missing Biolink 3.x `knowledge_level`, `agent_type`)
- The `relation` column persists despite being deprecated

Each source has its own transform class that inherits from this base:
- `kg_microbe/transform_utils/bacdive/bacdive.py` → `BacDiveTransform`
- `kg_microbe/transform_utils/mediadive/mediadive.py` → `MediaDiveTransform`
- etc.

---

## Cleaning and Rebuilding

### Backup Current Outputs

```bash
cd ~/gitrepos/kg-microbe

# Backup transformed data
tar -czvf backup_transformed_$(date +%Y%m%d).tar.gz data/transformed/

# Backup merged data
tar -czvf backup_merged_$(date +%Y%m%d).tar.gz data/merged/
```

### Clean Intermediate Files

```bash
# Clean transformed data (cheap to regenerate)
rm -rf data/transformed/*

# Clean merged data (cheap to regenerate)
rm -rf data/merged/*

# Keep data/raw/ - expensive to re-download, and download is cached anyway
```

### Rebuild

```bash
# If you kept data/raw/ (remember: ontologies FIRST!)
poetry run kg transform -s ontologies && poetry run kg transform -s bacdive -s bactotraits -s madin_etal -s mediadive
poetry run kg merge -y merge.cmm.yaml

# Full rebuild from scratch:
poetry run kg download -y download.yaml -o data/raw
poetry run kg transform -s ontologies && poetry run kg transform -s bacdive -s bactotraits -s madin_etal -s mediadive
poetry run kg merge
```

---

## Anti-patterns and Reproducibility Concerns

### Pre-processed Files from Google Drive

**Problem:** Some "raw" downloads are actually pre-processed files hosted on Google Drive rather than fetched directly from authoritative sources.

From `download.yaml`:
```yaml
# BacDive - pre-processed JSON from Google Drive, not BacDive API
-
  url: gdrive:1b_UWdIvsIM81V5WdFedNoxN3R4UUf4F2
  local_name: bacdive_strains.json

# UniProt - pre-processed tarballs from Google Drive
-
  url: https://drive.google.com/file/d/1-aFVHE54t8HvcV4Z32hyTkmlXci07Y9g/view?usp=drive_link
  local_name: uniprot_proteomes.tar.gz
-
  url: https://drive.google.com/file/d/1PkqAp5v0IKs9qwu9mbK7gVeNaO-p3HsI/view?usp=drive_link
  local_name: uniprot_human.tar.gz
```

**Why this is problematic:**

| Issue | Impact |
|-------|--------|
| **Broken provenance chain** | Cannot trace data back to authoritative source |
| **Unknown processing** | What transformations were applied before upload? |
| **Version ambiguity** | Which version of the source data was used? |
| **Not reproducible** | Cannot regenerate from scratch without the Google Drive files |
| **Single point of failure** | If Google Drive link breaks, pipeline fails |
| **No update path** | How do you get fresh data from the actual source? |

**Best practice:** Download raw data directly from authoritative APIs/endpoints, then apply all transformations in documented, versioned code.

**Contrast with good examples in the same file:**
```yaml
# Good: Direct from authoritative source
-
  url: http://purl.obolibrary.org/obo/chebi.owl.gz
  local_name: chebi.owl.gz

# Good: Direct from source API
-
  url: https://mediadive.dsmz.de/rest/media
  local_name: mediadive.json

# Good: Direct from source repository
-
  url: https://github.com/bacteria-archaea-traits/bacteria-archaea-traits/blob/master/output/condensed_traits_NCBI.csv?raw=true
  local_name: madin_etal.csv
```

**Recommendation:** For any source using `gdrive:` or Google Drive URLs, document:
1. What the original authoritative source is
2. What processing was applied before upload
3. When the file was created and from what version of source data
4. How to regenerate the file from scratch

---

## Resource Requirements

From the README:

> The KG construction process, particularly the transform step involving trimming of NCBI Taxonomy for any KG and the steps involving the microbial UniProt dataset for KG-Microbe-Function and KG-Microbe-Biomedical-Function, is computationally intensive. Successful execution on a local machine may require significant memory resources (e.g., >500 GB of RAM).

**For CMM work:** The bacdive, bactotraits, madin_etal, and mediadive transforms are reasonable on a standard machine. The `ontologies` transform is **required first** (see [Transform Dependencies](#transform-dependencies)). It's faster when you have the cached JSON files (`ncbitaxon_removed_subset.json`, `chebi.json`), but still takes significant time.

---

## Documentation Status

| Aspect | Documented? | Location |
|--------|-------------|----------|
| Basic usage | ✅ Brief | README.md |
| CLI options | ✅ Via `--help` | CLI |
| Transform sources | ❌ Not listed | (this document) |
| Merge configs | ❌ Not explained | (this document) |
| Architecture | ❌ Not documented | (this document) |
| Custom schema issues | ❌ Not documented | See `kg_microbe_verification_2026-01-08.md` |

---

## Software Engineering Practices

### Test Coverage

**Current state:** Minimal test coverage, focused on newest transforms only.

| Test File | Lines | Covers |
|-----------|-------|--------|
| `demo_test.py` | 250 bytes | Demo/smoke test only |
| `test_bakta.py` | 7.1 KB | Bakta transform |
| `test_cog.py` | 11.4 KB | COG transform |
| `test_kegg.py` | 11.8 KB | KEGG transform |

**Untested transforms (core CMM sources):**
- ❌ `bacdive` - No tests
- ❌ `bactotraits` - No tests
- ❌ `madin_etal` - No tests
- ❌ `mediadive` - No tests
- ❌ `ontologies` - No tests
- ❌ `rhea_mappings` - No tests

**Concern:** The 3 tested transforms (bakta, cog, kegg) are the newest additions from 2026-01. The 5+ original/core transforms have zero test coverage.

### CI/CD Pipeline

GitHub Actions workflow (`.github/workflows/qc.yml`):

```yaml
# Runs on push/PR to master, Python 3.10-3.12
- poetry run tox -e codespell  # Spell checking
- poetry run tox -e lint       # Ruff linting
- poetry run tox -e py         # Pytest
```

**Present:**
- Multi-version Python testing (3.10, 3.11, 3.12)
- Spell checking (codespell)
- Linting (ruff)
- Unit tests (pytest)

**Absent:**
- Pre-commit hooks (no `.pre-commit-config.yaml`)
- Type checking (mypy)
- Integration tests with actual transform outputs
- Schema validation tests (Biolink compliance)

### AI/LLM Configuration

| File | Status | Contents |
|------|--------|----------|
| `AGENTS.md` | ❌ Missing | - |
| `CLAUDE.md` | ❌ Missing | - |
| `SKILLS/` | ❌ Missing | - |
| `.claude/settings.local.json` | ✅ Present | Permission settings only (no project context) |

The `.claude/settings.local.json` contains Bash permissions and MCP server configs but no project-specific context or instructions.

### Recommendations

1. **Testing:** Add tests for core transforms (bacdive, bactotraits, madin_etal, mediadive)
2. **Pre-commit:** Add pre-commit hooks for consistent formatting/linting
3. **Schema validation:** Add tests that verify output conforms to Biolink/KGX schemas
4. **AI context:** Add CLAUDE.md with project conventions (especially custom schema decisions)

---

## Analyzing Build Output

### Extracting the Merged Archive

The merge step produces a compressed archive in `data/merged/merged-kg.tar.gz`. To analyze the KGX files, extract them first:

```bash
cd ~/gitrepos/kg-microbe

# Extract without deleting the archive
tar -xzf data/merged/merged-kg.tar.gz -C data/merged/
```

**Flags explained:**
- `-x` = extract
- `-z` = decompress gzip
- `-f` = file to extract
- `-C` = directory to extract into

The `tar` command extracts by default without removing the original archive.

After extraction, you'll have:
```
data/merged/
├── merged-kg.tar.gz              # Original archive (preserved)
└── merged-kg/                    # Extracted directory
    ├── merged-kg_nodes.tsv       # All nodes
    └── merged-kg_edges.tsv       # All edges
```

### Analyzing Edge Patterns

Two scripts are available for analyzing edge patterns. The key difference is **which source files contribute to each pattern**.

**Quick usage with just targets:**
```bash
just edge-patterns-merged      # → output/edge_patterns/edge_patterns_merged.tsv
just edge-patterns-by-source   # → output/edge_patterns/edge_patterns_by_source.tsv
just clean-edge-patterns       # Clean outputs
```

**Direct script usage** (for custom paths):

#### Option 1: Analyze Merged Data (Source Information Lost)

Use `edge_patterns_merged.py` on the merged output. This shows aggregate patterns across all sources but **doesn't show which source contributed each pattern**:

```bash
cd ~/gitrepos/cmm-ai-automation

# Analyze merged data (all patterns labeled "merged-kg")
uv run python src/cmm_ai_automation/scripts/edge_patterns_merged.py ../kg-microbe/data/merged/

# Save to timestamped file
uv run python src/cmm_ai_automation/scripts/edge_patterns_merged.py ../kg-microbe/data/merged/ > edge_patterns_merged_$(date +%Y-%m-%d).tsv
```

**Output format:**
```tsv
source     subject_category              subject_prefix      predicate              object_category              object_prefix    count
merged-kg  biolink:OrganismTaxon         NCBITaxon           biolink:subclass_of    biolink:OrganismTaxon        NCBITaxon        882437
merged-kg  biolink:OrganismTaxon         kgmicrobe.strain    METPO:2000028          biolink:ChemicalEntity       CHEBI            321601
merged-kg  biolink:ChemicalSubstance     CHEBI               biolink:subclass_of    biolink:ChemicalSubstance    CHEBI            275776
```

**Limitation:** All patterns show `merged-kg` as the source. You cannot tell if a pattern came from bacdive, mediadive, ontologies, etc.

#### Option 2: Analyze Transformed Data (Preserves Source Information)

Use `edge_patterns_by_source.py` on the **transformed** directory before merging. This shows **which source directory contributes each pattern**:

```bash
cd ~/gitrepos/cmm-ai-automation

# Analyze transformed data (source breakdown preserved)
uv run python src/cmm_ai_automation/scripts/edge_patterns_by_source.py ../kg-microbe/data/transformed/

# Save to timestamped file
uv run python src/cmm_ai_automation/scripts/edge_patterns_by_source.py ../kg-microbe/data/transformed/ > edge_patterns_by_source_$(date +%Y-%m-%d).tsv
```

**Output format:**
```tsv
source       subject_category              subject_prefix      predicate              object_category              object_prefix    count
bacdive      biolink:OrganismTaxon         kgmicrobe.strain    METPO:2000028          biolink:ChemicalEntity       CHEBI            321601
mediadive    biolink:ChemicalEntity        mediadive.solution  biolink:has_part       biolink:ChemicalEntity       CHEBI            38531
bactotraits  biolink:OrganismTaxon         NCBITaxon           METPO:2000006          biolink:ChemicalEntity       CHEBI            36816
ontologies   biolink:OrganismTaxon         NCBITaxon           biolink:subclass_of    biolink:OrganismTaxon        NCBITaxon        882437
```

**Advantage:** You can see exactly which source (bacdive, mediadive, bactotraits, ontologies, etc.) contributes each pattern.

#### Which Script to Use?

| Use Case | Script | Data Location |
|----------|--------|---------------|
| Want to see which source contributes patterns | `edge_patterns_by_source.py` | `data/transformed/` |
| Already merged and don't need source breakdown | `edge_patterns_merged.py` | `data/merged/` |
| Debugging transform-specific issues | `edge_patterns_by_source.py` | `data/transformed/` |
| Quick aggregate statistics | `edge_patterns_merged.py` | `data/merged/` |

#### What the Output Shows

Both scripts produce the same TSV format with these columns:

- **source**: Which file/directory the pattern came from
- **subject_category**: Biolink category of the subject node (e.g., `biolink:OrganismTaxon`)
- **subject_prefix**: ID prefix of the subject (e.g., `NCBITaxon`, `kgmicrobe.strain`)
- **predicate**: Relationship type (e.g., `biolink:subclass_of`, `METPO:2000028`)
- **object_category**: Biolink category of the object node
- **object_prefix**: ID prefix of the object
- **count**: Number of edges with this exact pattern

#### Use Cases

- **Quality checking:** Are the expected relationships present?
- **Data exploration:** What kinds of connections exist?
- **Source auditing:** Which transform contributes specific patterns?
- **Integration planning:** Which prefixes/categories need mapping?
- **Bug detection:** Unexpected patterns may indicate transform issues
- **Performance analysis:** Which sources create the most edges?

---

## Related Documentation

- [kg_microbe_verification_2026-01-08.md](kg_microbe_verification_2026-01-08.md) - Data quality verification
- [kg_microbe_risks.md](kg_microbe_risks.md) - Risk assessment for CMM
- [cmm_vs_kg_microbe.md](cmm_vs_kg_microbe.md) - Comparison of approaches
- [curie_prefix_strategy.md](curie_prefix_strategy.md) - CURIE/prefix planning

---

## See Also

- [KGX documentation](https://github.com/biolink/kgx)
- [kghub-downloader](https://github.com/monarch-initiative/kghub-downloader)
- [kg-microbe repository](https://github.com/Knowledge-Graph-Hub/kg-microbe)
