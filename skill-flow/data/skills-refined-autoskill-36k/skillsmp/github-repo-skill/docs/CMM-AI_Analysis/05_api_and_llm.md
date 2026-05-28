# Chapter 5: API and LLM Automation

[<- Back to Index](00_index.md) | [Previous: Code Analysis](04_code_analysis.md) | [Next: Setup Guide ->](06_setup_guide.md)

---

## External APIs Used

The codebase integrates with the following external APIs:

### 1. NCBI APIs (via Bio.Entrez)

**Files**: `ncbi_search.py`, `publication_search.py`, `transcriptomics_search.py`, `strain_search.py`, `add_missing_organisms.py`

**Endpoints**:
- `Entrez.esearch()` - Search databases
- `Entrez.efetch()` - Retrieve records
- `Entrez.esummary()` - Get record summaries
- `Entrez.read()` - Parse XML responses

**Databases Queried**:
- Assembly (genome assemblies)
- BioSample (biological samples)
- PubMed (publications)
- SRA (sequence read archive)
- GEO (gene expression)
- Taxonomy

**Note**: NCBI email configuration is broken - see [Chapter 6](06_setup_guide.md).

### 2. KEGG REST API

**File**: `pathway_search.py` (line 36)
**Endpoint**: `http://rest.kegg.jp/find/pathway/{keyword}`
**Usage**: Pathway name/ID searches

### 3. PubChem REST API

**File**: `chemical_search.py` (lines 31, 70, 102)
**Base URL**: `https://pubchem.ncbi.nlm.nih.gov/rest/pug`
**Endpoints**:
- `/compound/name/{name}/property/...` - Search by name
- `/compound/cid/{cid}/property/...` - Get compound properties

### 4. ArrayExpress API

**File**: `transcriptomics_search.py` (line 306, 319)
**Endpoint**: `https://www.ebi.ac.uk/arrayexpress/json/v3/experiments`
**Usage**: RNA-seq dataset search

### 5. NCBI ID Converter

**File**: `publication_search.py` (line 67)
**Endpoint**: `https://www.ncbi.nlm.nih.gov/pmc/utils/idconv/v1.0/?ids={pmid}&format=json`
**Usage**: Convert PMID to PMC IDs

### 6. UniProt API

**Files**: `gene_search.py`, `uniprot_functions.py`, `apis/uniprot_client.py` (if exists)
**Usage**: Protein search and ID mapping

### 7. Planned but NOT Implemented

- **BacDive API**: `strain_search.py` line 330: `# TODO: Implement BacDive API once credentials available`
- **protocols.io API**: `assay_search.py` line 156: `# GET https://www.protocols.io/api/v3/protocols?key={key}&filter=lanthanide`

---

## Files Using `requests` Library (Direct HTTP Calls)

12 files import requests:
1. `publication_search.py` - PMC ID conversion
2. `pathway_search.py` - KEGG searches
3. `download_pdfs_from_publications.py` - PDF downloads
4. `chemical_search.py` - PubChem queries (2 calls)
5. `structure_search.py` - (imported but may not be used)
6. `ncbi_search.py` - (imported but may not be used - uses Entrez)
7. `strain_search.py` - (imported but may not be used)
8. `gene_search.py` - (imported but may not be used)
9. `test_annotation_urls.py` - URL validation
10. `transcriptomics_search.py` - ArrayExpress queries
11. `media_search.py` - (imported but may not be used)
12. `dataset_search.py` - (imported but may not be used)

---

## URL Generation (No API Calls)

Many files generate URLs without making API calls - these are template-based:
- RCSB PDB: `https://www.rcsb.org/structure/{pdb_id}`
- AlphaFold: `https://alphafold.ebi.ac.uk/`
- KEGG Entry: `https://www.kegg.jp/entry/{id}`
- MetaCyc: `https://metacyc.org/META/NEW-IMAGE?type=PATHWAY&object={id}`
- Culture Collections: ATCC, DSM, JCM, NCIMB, NBRC, CCM, CECT
- DOI resolver: `https://doi.org/{doi}`
- PubMed: `https://pubmed.ncbi.nlm.nih.gov/{pmid}/`

---

## Summary of External Integrations

| API/Service | Status | Rate Limited | Auth Required |
|-------------|--------|--------------|---------------|
| NCBI Entrez | **BROKEN** (placeholder email) | Yes (0.5s delay) | Email only |
| KEGG REST | Working | Unknown | No |
| PubChem REST | Working | Unknown | No |
| ArrayExpress | Working | Unknown | No |
| UniProt | Likely working | Unknown | No |
| BacDive | NOT IMPLEMENTED | N/A | Yes (TODO) |
| protocols.io | NOT IMPLEMENTED | N/A | Yes (TODO) |

---

## LLM/AI Automation

### GitHub Workflows Using Claude/LLMs

**FIVE (5) different LLM integration workflows exist**:

#### 1. dragon-ai.yml - Dragon AI Agent
- **Trigger**: `@dragon-ai-agent please` mentions
- **Uses**: Claude Code via CBORG API (LBL proxy)
- **DANGEROUS**: `--dangerously-skip-permissions` flag
- **Auth**: `CBORG_API_KEY` secret
- **Can**: Create branches, submit PRs, modify files

#### 2. claude.yml - Claude Code Action
- **Trigger**: `@claude` mentions in issues/PRs
- **Uses**: `anthropics/claude-code-action@beta`
- **Auth**: `CLAUDE_CODE_OAUTH_TOKEN` secret
- **MCP Servers**: OLS (Ontology Lookup Service), sequential-thinking
- **Can**: Write files, create PRs, run bash commands

#### 3. claude-issue-triage.yml - Automatic Issue Triage
- **Trigger**: Issue opened
- **Uses**: Custom action `.github/actions/claude-issue-triage-action`
- **Auth**: `ANTHROPIC_API_KEY` or `CBORG_API_KEY`

#### 4. claude-issue-summarize.yml - Automatic Issue Summarization
- **Trigger**: Issue opened
- **Uses**: Custom action `.github/actions/claude-issue-summarize-action`
- **Auth**: `ANTHROPIC_API_KEY` or `CBORG_API_KEY`
- **Includes**: `artl-mcp` installation

#### 5. copilot-setup-steps.yml - GitHub Copilot Configuration
- Not a workflow per se, but Copilot integration config

### LLM API Endpoints Configured

| Workflow | API Endpoint | Notes |
|----------|--------------|-------|
| dragon-ai | `api.cborg.lbl.gov` | LBL's Claude proxy |
| claude | Anthropic direct | OAuth token |
| issue-triage | Either | Falls back to CBORG |
| issue-summarize | Either | Falls back to CBORG |

---

## Evidence of LLM-Generated Code

### Clarification: Source of LLM-Generated Code

**IMPORTANT DISTINCTION**: The LLM-generated code in this repository did NOT come from the GitHub Actions workflows.

**Actual workflow**:
1. Marcin used the **Claude Code CLI** (interactive terminal sessions, like `claude` command)
2. Claude generated Python code including "curated" data structures
3. Marcin committed the output under his own name
4. The GitHub Actions (dragon-ai, claude-code-action, etc.) were set up separately and recently (December 2025)

**Why this matters**:
- Git history shows human commits, but the actual author of much code content was Claude
- The provenance is invisible - git only records the committer, not the LLM that generated the content
- This is a common pattern with Claude Code / Cursor / Copilot workflows
- The hardcoded "curated" data represents **Claude's training knowledge**, not literature-sourced curation

### Indicators of LLM-Generated Code

1. **Code Style Patterns**:
   - Extremely verbose docstrings with full type hints
   - Comprehensive error handling that's often unused
   - Overly detailed comments explaining obvious operations
   - Consistent formatting across all files (suggests single author or generated)

2. **Hardcoded "Curated" Data**:
   - `CURATED_MEDIA` in `media_search.py` (7 media, ~50 ingredients)
   - `curated_assays` in `assay_search.py` (7 protocols)
   - `lanthanide_genes` in `gene_search.py` (15+ genes)
   - `curated_publications` in `publication_search.py` (8 real + 4 FAKE)

   These have **NO citations or references** - exactly what you'd expect if an LLM generated them from training data.

3. **FAKE Data Created by LLM**:
   `publication_search.py` lines 172-205 contain fabricated publications:
   ```python
   {"url": "https://arxiv.org/abs/2309.12345", ...},  # DOES NOT EXIST
   {"url": "https://arxiv.org/abs/2308.54321", ...},  # DOES NOT EXIST
   ```
   This is classic LLM hallucination - generating plausible-looking but non-existent URLs.

4. **Ingredient Roles**:
   The roles in `media_search.py` (carbon source, nitrogen source, buffer, mineral, trace element, etc.) are:
   - Generic/reasonable but not authoritative
   - No citations or references
   - Consistent with LLM knowledge of microbiology basics
   - **Not validated against any database**

5. **Git History**:
   - All commits from "marcin p. joachimiak"
   - No Dragon-AI or Claude commits in main code (only one `.gitignore` from Dragon-AI)
   - Consistent with human prompting LLM -> copying output to files -> committing

### What Claude Generates vs. What Needs Validation

| Data Type | Claude's Knowledge | Validation Needed |
|-----------|-------------------|-------------------|
| Standard media recipes (LB, R2A) | Generally accurate | Low priority |
| CHEBI IDs for common chemicals | Usually correct | Spot-check |
| Ingredient roles | Reasonable guesses | **HIGH PRIORITY** - no citations |
| Assay detection limits | May be fabricated | **HIGH PRIORITY** - verify in literature |
| KEGG IDs (K#####) | Real IDs | Low priority |
| Custom gene IDs (custom_*) | Fabricated placeholders | Replace with real IDs |
| Preprint URLs | **HALLUCINATED** | Delete fake entries |

### Implications for Data Quality

If the ingredient roles, assay protocols, gene annotations, and media formulations were generated by Claude:

| Data Type | Reliability | Recommendation |
|-----------|-------------|----------------|
| CHEBI IDs | **Medium** - Likely correct, LLMs know these | Validate against CHEBI API |
| Ingredient roles | **LOW** - No provenance | Cross-reference with MediaDive |
| Detection limits | **UNKNOWN** - May be plausible but fabricated | Verify in literature |
| Assay protocols | **LOW** - URLs may not exist | Test all URLs |
| Media formulations | **Medium** - Standard recipes known | Verify against ATCC/DSMZ |
| Gene annotations | **Medium** - KEGG IDs real, custom_ IDs fabricated | Validate against UniProt |
| Fake preprints | **ZERO** - Confirmed fabrications | DELETE from codebase |

---

[<- Back to Index](00_index.md) | [Previous: Code Analysis](04_code_analysis.md) | [Next: Setup Guide ->](06_setup_guide.md)
