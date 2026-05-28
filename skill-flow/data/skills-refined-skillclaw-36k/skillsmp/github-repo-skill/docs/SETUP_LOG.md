# Setup Log: cmm-ai-automation

This document records the setup process and design decisions for the `cmm-ai-automation` repository.

**Date:** 2024-12-09
**Author:** Mark Miller (with Claude Code assistance)
**Repository:** https://github.com/turbomam/cmm-ai-automation

---

## 1. Project Goals

Create a GitHub repository for AI-assisted automation of Critical Mineral Metabolism (CMM) data curation with:
- Python-based tools using LinkML and OBO Foundry ecosystem
- Integration with private Google Sheets (specifically "BER CMM Data for AI - for editing")
- AI/LLM automation via GitHub Actions (Claude Code)

### Collaboration with CultureBotAI/CMM-AI

This repository is developed in collaboration with [CultureBotAI/CMM-AI](https://github.com/CultureBotAI/CMM-AI). The division of responsibilities:

| Repository | Focus |
|------------|-------|
| [CultureBotAI/CMM-AI](https://github.com/CultureBotAI/CMM-AI) | AI-driven biological discovery, microorganism identification, analysis workflows |
| [turbomam/cmm-ai-automation](https://github.com/turbomam/cmm-ai-automation) | Data modeling (LinkML), Google Sheets integration, OBO Foundry ontology tooling |

The AI automation workflows in this repository were adapted from those used in CMM-AI, which in turn came from the [ai4curation/github-ai-integrations](https://github.com/ai4curation/github-ai-integrations) template maintained by the Monarch Initiative.

---

## 2. Template Selection

### Evaluated Options

| Template | Tool | Pros | Cons |
|----------|------|------|------|
| [linkml-project-cookiecutter](https://github.com/linkml/linkml-project-cookiecutter) | cruft | Official LinkML, well-maintained | Uses Poetry, older approach |
| [linkml-project-copier](https://github.com/dalito/linkml-project-copier) | copier | Uses `uv`, modern, based on cookiecutter | Newer, fewer users |
| [ontology-development-kit (ODK)](https://github.com/INCATools/ontology-development-kit) | Docker/Make | Full ontology lifecycle | Overkill for this use case |
| [ai4curation/github-ai-integrations](https://github.com/ai4curation/github-ai-integrations) | copier | Claude GitHub Actions, MCP servers | AI-only, no schema support |

### Decision

Use **linkml-project-copier** as the base template, then layer on **ai4curation/github-ai-integrations** for AI automation.

**Rationale:**
- `uv` is faster and simpler than Poetry for dependency management
- LinkML provides schema-driven data modeling appropriate for structured CMM data
- The ai4curation template provides battle-tested Claude GitHub Actions with MCP server integration (OLS for ontology lookup)

---

## 3. Repository Creation

### 3.1 Create Empty GitHub Repo

```bash
gh repo create turbomam/cmm-ai-automation --public \
  --description "AI-assisted automation for Critical Mineral Metabolism data curation using LinkML, OBO tools, and Google Sheets integration"
```

**Result:** https://github.com/turbomam/cmm-ai-automation

### 3.2 Clone Locally

```bash
cd /home/mark/gitrepos
gh repo clone turbomam/cmm-ai-automation
# Warning: empty repository
```

---

## 4. Initialize with LinkML Template

### 4.1 Install Dependencies

```bash
pip install copier jinja2-time
```

Note: `jinja2-time` was required as an additional dependency for the copier template.

### 4.2 Run Copier

```bash
copier copy --trust --defaults gh:dalito/linkml-project-copier cmm-ai-automation \
  --data project_name="cmm-ai-automation" \
  --data project_description="AI-assisted automation for Critical Mineral Metabolism data curation" \
  --data full_name="Mark Miller" \
  --data email="MAM@lbl.gov" \
  --data github_org="turbomam" \
  --data main_schema_class="CmmDataset" \
  --data license="MIT"
```

### 4.3 Template Output Structure

```
cmm-ai-automation/
├── .github/
│   ├── dependabot.yml
│   └── workflows/
│       ├── deploy-docs.yaml
│       ├── main.yaml
│       ├── pypi-publish.yaml
│       └── test_pages_build.yaml
├── docs/
├── examples/
├── project/
├── src/cmm_ai_automation/
│   ├── schema/cmm_ai_automation.yaml  # LinkML schema
│   └── datamodel/                      # Generated Python classes
├── tests/
├── pyproject.toml
├── justfile
└── mkdocs.yml
```

### 4.4 Initial Commit

```bash
cd /home/mark/gitrepos/cmm-ai-automation
git init
git add -A
git commit -m "Initialize from linkml-project-copier template"
git branch -m main
git remote add origin git@github.com:turbomam/cmm-ai-automation.git
```

---

## 5. Add AI Automation (Claude GitHub Actions)

### 5.1 Source Analysis

Examined [CultureBotAI/CMM-AI](https://github.com/CultureBotAI/CMM-AI) `.github/` directory, which uses the [ai4curation/github-ai-integrations](https://github.com/ai4curation/github-ai-integrations) copier template.

**Files identified:**
- `workflows/claude.yml` - Main Claude Code action
- `workflows/claude-issue-triage.yml` - Auto-triage issues
- `workflows/claude-issue-summarize.yml` - Auto-summarize issues
- `copilot-setup-steps.yml` - GitHub Copilot workspace setup
- `ai-controllers.json` - List of GitHub users who can control Claude
- `actions/` - Custom composite actions

### 5.2 Download Workflow Files

```bash
# Create directories
mkdir -p .github/actions

# Download workflows
gh api repos/ai4curation/github-ai-integrations/contents/template/.github/workflows/claude.yml | \
  jq -r '.content' | base64 -d > .github/workflows/claude.yml

gh api repos/ai4curation/github-ai-integrations/contents/template/.github/workflows/claude-issue-triage.yml | \
  jq -r '.content' | base64 -d > .github/workflows/claude-issue-triage.yml

gh api repos/ai4curation/github-ai-integrations/contents/template/.github/workflows/claude-issue-summarize.yml | \
  jq -r '.content' | base64 -d > .github/workflows/claude-issue-summarize.yml

gh api repos/ai4curation/github-ai-integrations/contents/template/.github/copilot-setup-steps.yml | \
  jq -r '.content' | base64 -d > .github/copilot-setup-steps.yml
```

### 5.3 Download Custom Actions

```bash
mkdir -p .github/actions/claude-code-action \
         .github/actions/claude-issue-summarize-action \
         .github/actions/claude-issue-triage-action

# Download action.yml for each
curl -sL "https://raw.githubusercontent.com/ai4curation/github-ai-integrations/main/template/.github/actions/claude-code-action/action.yml" \
  -o ".github/actions/claude-code-action/action.yml"

curl -sL "https://raw.githubusercontent.com/ai4curation/github-ai-integrations/main/template/.github/actions/claude-issue-summarize-action/action.yml" \
  -o ".github/actions/claude-issue-summarize-action/action.yml"

curl -sL "https://raw.githubusercontent.com/ai4curation/github-ai-integrations/main/template/.github/actions/claude-issue-triage-action/action.yml" \
  -o ".github/actions/claude-issue-triage-action/action.yml"
```

### 5.4 Create AI Controllers Config

```bash
echo '["turbomam"]' > .github/ai-controllers.json
```

This restricts Claude action triggers to the `turbomam` GitHub user.

### 5.5 Claude Workflow Features

The `claude.yml` workflow includes:

```yaml
# Triggers on @claude mentions in:
# - Issue comments
# - PR review comments
# - PR reviews
# - New issues (title or body)

# MCP Servers configured:
mcp_config: |
  {
    "mcpServers": {
      "ols": {
        "command": "uvx",
        "args": ["ols-mcp"]
      },
      "sequential-thinking": {
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-sequential-thinking"]
      }
    }
  }

# Allowed tools:
allowed_tools: "Bash(*),FileEdit,Edit,MultiEdit,WebSearch,WebFetch,mcp__ols_mcp__search_all_ontologies,mcp__ols_mcp__get_terms_from_ontology"
```

---

## 6. Add Google Sheets Integration

### 6.1 Design Decision: gspread vs google-api-python-client

| Library | Pros | Cons |
|---------|------|------|
| `gspread` | Simple API, pandas integration | Less control |
| `google-api-python-client` | Full API access | More verbose |

**Decision:** Use `gspread` for simplicity, with `google-auth` for authentication.

### 6.2 Add Dependencies

Updated `pyproject.toml`:

```toml
dependencies = [
  "linkml-runtime >=1.9.4",
  "gspread >=6.0.0",
  "google-auth >=2.0.0",
  "google-auth-oauthlib >=1.0.0",
  "pandas >=2.0.0",
]
```

### 6.3 Create gsheets Module

Created `src/cmm_ai_automation/gsheets.py` with:

- `get_gspread_client()` - Authenticate with service account
- `get_spreadsheet()` - Open spreadsheet by name or ID
- `list_worksheets()` - List all tabs in a spreadsheet
- `get_sheet_data()` - Read worksheet to DataFrame
- `update_sheet_data()` - Write DataFrame to worksheet

**Known Spreadsheet IDs:**
```python
KNOWN_SHEETS = {
    "BER CMM Data for AI - for editing": "1h-kOdyvVb1EJPqgTiklTN9Z8br_8bP8KGmxA19clo7Q",
}
```

### 6.4 Authentication Strategy

The module supports three credential locations (in order of precedence):
1. Explicit path passed to functions
2. `GOOGLE_APPLICATION_CREDENTIALS` environment variable
3. Default gspread location: `~/.config/gspread/service_account.json`

---

## 7. Documentation Updates

Updated `README.md` with:
- Feature list
- Quick start guide
- Google Sheets usage examples
- AI integration documentation

---

## 8. Final Commit and Push

```bash
git add -A
git commit -m "Add AI automation and Google Sheets integration

- Add Claude Code GitHub Action workflows from ai4curation/github-ai-integrations
  - claude.yml: Main Claude Code action for @claude mentions
  - claude-issue-triage.yml: Auto-triage new issues
  - claude-issue-summarize.yml: Auto-summarize issues
- Add custom actions for Claude integrations
- Add copilot-setup-steps.yml for GitHub Copilot workspace
- Add gsheets.py module for Google Sheets API access
- Add gspread, google-auth, pandas dependencies
- Update README with features, quick start, and usage examples"

git push -u origin main
```

---

## 9. Post-Setup Configuration Required

### 9.1 GitHub Repository Secrets

| Secret | Purpose |
|--------|---------|
| `CLAUDE_CODE_OAUTH_TOKEN` | Authentication for Claude GitHub Action |
| `GOOGLE_CREDENTIALS_JSON` | (Optional) Service account JSON for CI/CD |

### 9.2 Google Cloud Setup

1. Create a Google Cloud project
2. Enable Google Sheets API and Google Drive API
3. Create a service account
4. Download JSON key file
5. Share the "BER CMM Data for AI - for editing" spreadsheet with the service account email

### 9.3 Local Development

```bash
cd /home/mark/gitrepos/cmm-ai-automation

# Initialize project
just setup

# Set credentials
export GOOGLE_APPLICATION_CREDENTIALS=/path/to/service_account.json

# Or copy to default location
cp /path/to/service_account.json ~/.config/gspread/service_account.json
```

---

## 10. Planned Integrations

### Knowledge Graph and Ontology Resources

| Project | Purpose | Integration Status |
|---------|---------|-------------------|
| [kg-microbe](https://github.com/Knowledge-Graph-Hub/kg-microbe) | Microbial knowledge graph with strain/function data | Planned - CMM strains link via `kg_node_ids` column |
| [kgx](https://github.com/biolink/kgx) | Knowledge Graph Exchange for Biolink Model graphs | Planned - Import/export KG data |
| [biolink-model](https://github.com/biolink/biolink-model) | Schema and upper ontology for biological KGs | Planned - Data modeling alignment |
| [biolink-model-toolkit](https://github.com/biolink/biolink-model-toolkit) | Python utilities for Biolink Model | Planned - Model validation |
| [metpo](https://github.com/berkeleybop/metpo) | Microbial Phenotype Ontology | Planned - Phenotype annotation |

See also:
- [biolink organization](https://github.com/orgs/biolink/repositories) for additional tools (ontobio, etc.)
- [biopragmatics organization](https://github.com/biopragmatics) for identifier and ontology tools (bioregistry, curies, pyobo, etc.)

### OLS Embeddings Database

A local copy of OLS text embeddings is available for semantic search and term mapping:

| Property | Value |
|----------|-------|
| Location | `/home/mark/work/large/ontologies/embeddings.db` |
| Size | 288 GB |
| Total embeddings | ~9.5 million |
| Model | OpenAI `text-embedding-3-small` (1536 dimensions) |
| Source | [cthoyt.com/2025/08/04/ontology-text-embeddings.html](https://cthoyt.com/2025/08/04/ontology-text-embeddings.html) |

**Database schema:**
```sql
CREATE TABLE embeddings (
    ontologyId TEXT,
    entityType TEXT,
    iri TEXT,
    document TEXT,
    model TEXT,
    hash TEXT,
    embeddings TEXT,  -- JSON-encoded float array
    PRIMARY KEY (ontologyId, entityType, iri)
);
```

**Top ontologies by embedding count:**
| Ontology | Count |
|----------|-------|
| ncbitaxon | 2,650,614 |
| slm | 1,001,034 |
| dron | 756,397 |
| gaz | 678,436 |
| pr | 364,392 |
| snomed | 352,573 |
| chebi | 221,776 |
| go | 84,737 |

**Planned CMM subset ontologies:** chebi, go, obi, envo, ncbitaxon (subset), micro, metpo

**Reference implementation:** See `search_pcr_embeddings.py` and `chromadb_semantic_mapper.py` in [berkeleybop/metpo](https://github.com/berkeleybop/metpo).

### Data Flow

```
Google Sheets (BER CMM Data)
    ↓
cmm-ai-automation (this repo)
    ↓ LinkML schema validation
    ↓ Ontology term lookup (OLS)
    ↓
kg-microbe (knowledge graph)
    ↓ kgx export
    ↓
Biolink Model-compliant KG
```

---

## 11. Project Initialization with `just setup`

### 11.1 Installing just

The `just` command runner was installed via pip:

```bash
pip install just-bin
just --version  # 1.43.1
```

Note: Attempted `cargo install just` first but the system Rust version was too old. The `just-bin` package provides pre-compiled binaries.

### 11.2 Running `just setup`

```bash
cd /home/mark/gitrepos/cmm-ai-automation
just setup
```

This command executes:

1. **`uv sync --group dev`** - Install all dependencies including dev tools
   - Installed 187 packages
   - Created `.venv/` virtual environment
   - Generated `uv.lock` lockfile

2. **`uv run gen-project`** - Generate project artifacts from LinkML schema
   - Input: `src/cmm_ai_automation/schema/cmm_ai_automation.yaml`
   - Output directory: `project/`
   - Generated formats: Java, TypeScript, JSON Schema, OWL, SHACL, ShEx, etc.

3. **`uv run gen-doc`** - Generate schema documentation
   - Output: `docs/schema/` and `docs/elements/`

### 11.3 Generated Files

After `just setup`, the following were generated:

**Schema-generated Python datamodel** (DO NOT EDIT):
- `src/cmm_ai_automation/datamodel/cmm_ai_automation.py` - Python dataclasses
- `src/cmm_ai_automation/datamodel/cmm_ai_automation_pydantic.py` - Pydantic models

**Project artifacts** (in `project/`):
- `java/` - Java classes
- `typescript/` - TypeScript definitions
- `jsonschema/` - JSON Schema
- `owl/` - OWL ontology
- `shacl/` - SHACL shapes
- `shex/` - ShEx expressions

**Documentation** (in `docs/`):
- `schema/` - Schema documentation
- `elements/` - Element documentation

---

## 12. Code Organization

### Directory Structure

```
src/cmm_ai_automation/
├── __init__.py           # Package init (template-generated)
├── _version.py           # Auto-versioning (template-generated)
├── datamodel/            # GENERATED from LinkML schema
│   ├── __init__.py       # DO NOT EDIT - regenerated by `just gen-py`
│   ├── cmm_ai_automation.py
│   └── cmm_ai_automation_pydantic.py
├── schema/               # LinkML YAML schema (HAND-AUTHORED)
│   └── cmm_ai_automation.yaml
├── gsheets.py            # Google Sheets module (HAND-AUTHORED)
└── scripts/              # CLI tools with Click (HAND-AUTHORED)
    └── __init__.py
```

### Code Classification

| Location | Type | Edit Policy |
|----------|------|-------------|
| `schema/*.yaml` | LinkML schema | HAND-AUTHORED - edit freely |
| `datamodel/*.py` | Python from schema | GENERATED - do not edit |
| `gsheets.py` | Utility module | HAND-AUTHORED - edit freely |
| `scripts/*.py` | CLI tools | HAND-AUTHORED - edit freely |
| `project/*` | Multi-format exports | GENERATED - do not edit |
| `docs/schema/*` | Documentation | GENERATED - do not edit |

### Script Development Standards

Following [metpo conventions](https://github.com/berkeleybop/metpo):

1. **Use Click CLI interfaces** - proper named option parsing
2. **Register in pyproject.toml** - `[project.scripts]` entries
3. **Integrate with Makefile** - use `$<` and `$@` patterns
4. **Production quality** - reusable tools, not one-off scripts

Example script template:
```python
#!/usr/bin/env python3
"""Brief description of what this script does."""
import click

@click.command()
@click.option('--input', '-i', required=True, help='Input file path')
@click.option('--output', '-o', required=True, help='Output file path')
def main(input: str, output: str):
    """Detailed description of the command."""
    pass

if __name__ == '__main__':
    main()
```

---

## 13. Code Quality Assurance

### Python Version

Python 3.12+ is required (`requires-python = ">=3.12"`).

**Rationale:**
- Modern type hint syntax (`X | Y` unions, built-in generics)
- Better error messages
- Performance improvements
- `uv` handles Python version management automatically (no pyenv needed)

### QA Tools Configured

| Tool | Purpose | Command |
|------|---------|---------|
| **ruff** | Linting and formatting | `uv run ruff check src/` |
| **mypy** | Static type checking | `uv run mypy src/cmm_ai_automation/` |
| **deptry** | Dependency checking | `uv run deptry src/` |
| **pytest** | Unit testing | `uv run pytest` |
| **pytest-cov** | Coverage reporting | `uv run pytest --cov` |
| **pre-commit** | Git hooks | `uv run pre-commit run --all-files` |

### Installing QA Dependencies

```bash
uv sync --group dev --group qa
```

### Pre-commit Setup

```bash
uv run pre-commit install
```

### Ruff Configuration

Ruff is configured with these rule sets:
- `E`, `W` - pycodestyle
- `F` - Pyflakes
- `I` - isort
- `B` - flake8-bugbear
- `C4` - flake8-comprehensions
- `UP` - pyupgrade
- `ARG` - unused arguments
- `SIM` - simplify
- `TCH` - type checking imports
- `PTH` - pathlib
- `RUF` - Ruff-specific

Generated files (datamodel/, project/) are excluded from linting.

### Coverage Requirements

- Minimum coverage: 80%
- Branch coverage enabled
- Generated code excluded from coverage

---

## 14. GitHub Repository Configuration

### Branch Protection (main)

Configured via GitHub API on 2024-12-09:

| Setting | Value | Rationale |
|---------|-------|-----------|
| Require PR reviews | 1 approval | Ensures code review before merge |
| Dismiss stale reviews | Yes | Re-review after changes |
| Require conversation resolution | Yes | All comments must be addressed |
| Enforce admins | **No** | Owner (turbomam) can bypass for urgent fixes |
| Allow force pushes | No | Preserve history |
| Allow deletions | No | Protect main branch |

**Key point:** `enforce_admins: false` allows the repository owner to push directly or merge without approval when needed, while still requiring reviews for other contributors.

### Merge Settings

| Setting | Value |
|---------|-------|
| Allow squash merge | Yes (preferred) |
| Allow merge commit | No |
| Allow rebase merge | Yes |
| Delete branch on merge | Yes |
| Allow auto-merge | Yes |

### Other Settings

| Setting | Value |
|---------|-------|
| Issues | Enabled |
| Projects | Enabled |
| Wiki | Disabled (use docs/ instead) |

### Workflow for Contributors

1. Create a feature branch: `git checkout -b feature/my-feature`
2. Make changes and commit
3. Push branch: `git push -u origin feature/my-feature`
4. Create PR via `gh pr create` or GitHub web UI
5. Request review (or owner can self-merge with bypass)
6. Squash merge after approval
7. Branch auto-deleted

### Commands Used

```bash
# Set branch protection
gh api repos/turbomam/cmm-ai-automation/branches/main/protection -X PUT \
  --input - << 'EOF'
{
  "required_status_checks": null,
  "enforce_admins": false,
  "required_pull_request_reviews": {
    "dismiss_stale_reviews": true,
    "require_code_owner_reviews": false,
    "required_approving_review_count": 1
  },
  "restrictions": null,
  "required_conversation_resolution": true
}
EOF

# Configure merge settings
gh api repos/turbomam/cmm-ai-automation -X PATCH --input - << 'EOF'
{
  "has_wiki": false,
  "allow_squash_merge": true,
  "allow_merge_commit": false,
  "allow_rebase_merge": true,
  "delete_branch_on_merge": true,
  "allow_auto_merge": true
}
EOF
```

---

## 15. Google Sheets Authentication Setup

**Date:** 2024-12-09

### Google Cloud Project

Used existing project `mam-gdrive-mcp-server` (already had Google Drive API enabled).

### Steps Performed

**1. Set active project:**
```bash
gcloud config set project mam-gdrive-mcp-server
```

**2. Enable Google Sheets API:**
```bash
gcloud services enable sheets.googleapis.com --project=mam-gdrive-mcp-server
```

**3. Create service account:**
```bash
gcloud iam service-accounts create cmm-sheets-access \
  --display-name="CMM Sheets Access" \
  --description="Service account for cmm-ai-automation Google Sheets access" \
  --project=mam-gdrive-mcp-server
```

**4. Download credentials:**
```bash
mkdir -p ~/.config/gspread
gcloud iam service-accounts keys create ~/.config/gspread/service_account.json \
  --iam-account=cmm-sheets-access@mam-gdrive-mcp-server.iam.gserviceaccount.com \
  --project=mam-gdrive-mcp-server
```

**5. Share spreadsheet with service account:**
- Open "BER CMM Data for AI - for editing" in Google Sheets
- Click Share → Add `cmm-sheets-access@mam-gdrive-mcp-server.iam.gserviceaccount.com`
- Set permission: **Viewer** (read-only)
- Uncheck "Notify people"

### Service Account Details

| Property | Value |
|----------|-------|
| Email | `cmm-sheets-access@mam-gdrive-mcp-server.iam.gserviceaccount.com` |
| Project | `mam-gdrive-mcp-server` |
| Access Level | Viewer (read-only) |
| Credentials Location | `~/.config/gspread/service_account.json` |

### Available Worksheets

Verified access to "BER CMM Data for AI - for editing":

| Tab Name | Records |
|----------|---------|
| taxa_and_genomes | 215 |
| strains | - |
| growth_media | - |
| media_ingredients | 76 |
| growth_preferences | - |
| transcriptomics | - |
| biosamples | - |
| macromolecular_structures | - |
| genes_and_proteins | - |
| pathways | - |
| protocols | - |
| assays | - |
| chemicals | - |
| bioprocesses | - |
| datasets | - |
| publications | - |
| screening_results | - |

### Usage Example

```python
from cmm_ai_automation.gsheets import list_worksheets, get_sheet_records, get_sheet_data

# List all tabs
tabs = list_worksheets("BER CMM Data for AI - for editing")

# Get data as list of dicts
records = get_sheet_records("BER CMM Data for AI - for editing", "media_ingredients")

# Get data as pandas DataFrame
df = get_sheet_data("BER CMM Data for AI - for editing", "taxa_and_genomes")
```

### Security Notes

- Credentials stored outside repository (`~/.config/gspread/`)
- `.gitignore` updated to block `**/service_account.json` and similar patterns
- Service account has read-only access
- No credentials committed to git

---

## 16. References

- [linkml-project-copier](https://github.com/dalito/linkml-project-copier) - Base template
- [ai4curation/github-ai-integrations](https://github.com/ai4curation/github-ai-integrations) - AI automation template
- [CultureBotAI/CMM-AI](https://github.com/CultureBotAI/CMM-AI) - Collaborating project for CMM discovery
- [kg-microbe](https://github.com/Knowledge-Graph-Hub/kg-microbe) - Microbial knowledge graph
- [biolink organization](https://github.com/orgs/biolink/repositories) - Biolink Model ecosystem
  - [kgx](https://github.com/biolink/kgx) - Knowledge Graph Exchange tools
  - [biolink-model](https://github.com/biolink/biolink-model) - Schema and upper ontology
  - [biolink-model-toolkit](https://github.com/biolink/biolink-model-toolkit) - Python utilities
- [metpo](https://github.com/berkeleybop/metpo) - Microbial Phenotype Ontology
- [biopragmatics organization](https://github.com/biopragmatics) - Identifier and ontology tools
  - [bioregistry](https://github.com/biopragmatics/bioregistry) - Integrative registry
  - [curies](https://github.com/biopragmatics/curies) - CURIE/URI conversion
  - [pyobo](https://github.com/biopragmatics/pyobo) - Python ontology tools
- [gspread documentation](https://docs.gspread.org/)
- [LinkML documentation](https://linkml.io/)
- [Claude Code GitHub Action](https://github.com/anthropics/claude-code-action)
