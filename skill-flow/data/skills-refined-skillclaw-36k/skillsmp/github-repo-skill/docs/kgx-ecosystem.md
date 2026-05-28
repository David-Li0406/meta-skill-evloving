# KGX Ecosystem: GitHub Organizations and Repositories

This document maps the GitHub ecosystem relevant to KGX compliance, kg-microbe, METPO, and CMM/PFAS research.

## Organization Overview

| Org | Focus | Access |
|-----|-------|--------|
| **[biolink](https://github.com/biolink)** | Biolink Model, KGX tooling | Public |
| **[Knowledge-Graph-Hub](https://github.com/Knowledge-Graph-Hub)** | kg-microbe, kg-phenio, KG infrastructure | Public |
| **[berkeleybop](https://github.com/berkeleybop)** | METPO, BBOP tooling | Public |
| **[CultureBotAI](https://github.com/CultureBotAI)** | CMM-AI, PFAS-AI, assay-metadata | Mixed |
| **[turbomam](https://github.com/turbomam)** | cmm-ai-automation | Public |

---

## Core Repositories

### biolink/biolink-model

- **URL**: https://github.com/biolink/biolink-model
- **Purpose**: Canonical Biolink Model schema - defines categories, predicates, domain/range constraints
- **Local clone**: `/home/mark/gitrepos/biolink-model`
- **Relevance**: Source of truth for KGX compliance
- **Key changes**:
  - v4.3.3 (Nov 2024): `biolink:assesses` DEPRECATED
  - v4.3.6 (current): `biolink:assesses` REMOVED completely
- **Note**: Marcin observed "biolink may not give the detail we need" - hence METPO predicates

### biolink/kgx

- **URL**: https://github.com/biolink/kgx
- **Purpose**: Knowledge Graph Exchange library - validation, transformation, serialization
- **Local clone**: `/home/mark/gitrepos/kgx`
- **Key feature**: `kgx validate` command for checking KGX compliance
- **Limitation**: Marcin noted "there is no actual compliance tool" - validation is incomplete
- **Note**: cmm-ai-automation monkey-patches KGX to allow slashes in CURIEs (for DOIs)

### Knowledge-Graph-Hub/kg-microbe

- **URL**: https://github.com/Knowledge-Graph-Hub/kg-microbe
- **Purpose**: Main microbial knowledge graph - integrates BacDive, MediaDive, KEGG, Rhea, etc.
- **Local clone**: `/home/mark/gitrepos/kg-microbe`
- **Active work**: PR #485 - Major KGX compliance refactoring
- **Data sources**:
  - BacDive (strain metadata, phenotypes)
  - MediaDive (growth media, ingredients)
  - KEGG (pathways, enzymes)
  - Rhea (reactions)
  - TrEMBL (proteins)
  - Bakta (genome annotations)

### berkeleybop/metpo

- **URL**: https://github.com/berkeleybop/metpo
- **Purpose**: Microbial Ecophysiological Trait and Phenotype Ontology
- **Local clone**: `/home/mark/gitrepos/metpo`
- **Role**: Provides predicates that Biolink lacks
- **Key predicates**:
  - `METPO:2000103` - capable_of (organism capabilities)
  - `METPO:2000202` - produces (production edges)
  - `METPO:2000002`, `METPO:2000003` - chemical interactions
- **Features**:
  - Literature mining pipeline (OntoGPT + METPO grounding)
  - BactoTraits/Madin database reconciliation
  - Biolink class mappings via `skos:closeMatch`

### turbomam/cmm-ai-automation (this repo)

- **URL**: https://github.com/turbomam/cmm-ai-automation
- **Purpose**: KGX-compliant CMM data curation with AI automation
- **Key features**:
  - `KGXNode`/`KGXEdge` pydantic classes with PROV-O fields
  - Custom KGX validator (monkey-patched for DOI CURIEs)
  - CURIE-based export scripts for strains/chemicals
  - Google Sheets integration for private CMM data
  - Rigorous Biolink 3.x compliance (knowledge_level, agent_type)

---

## CultureBotAI Repositories (Marcin's Org)

| Repo | Access | Purpose | URL |
|------|--------|---------|-----|
| **CMM-AI** | Private | Critical Mineral Metabolism AI research | https://github.com/CultureBotAI/CMM-AI |
| **PFAS-AI** | Public | PFAS degradation literature/data | https://github.com/CultureBotAI/PFAS-AI |
| **PFASCommunityAgents** | Private | Agentic framework for PFAS microbial community research | https://github.com/CultureBotAI/PFASCommunityAgents |
| **assay-metadata** | Public | Assay labels and chemical mappings | https://github.com/CultureBotAI/assay-metadata |
| **kg-microbe-projects** | Private | KG-Microbe project management | https://github.com/CultureBotAI/kg-microbe-projects |
| **MicroGrowLink** | Private | Growth media linking | https://github.com/CultureBotAI/MicroGrowLink |
| **MicroGrowAgents** | Public | Agentic microbe growth tools | https://github.com/CultureBotAI/MicroGrowAgents |
| **kg-ai-prep** | Private | Preparing KGs for AI training | https://github.com/CultureBotAI/kg-ai-prep |
| **MicroMediaParam** | Public | Media parameterization | https://github.com/CultureBotAI/MicroMediaParam |
| **auto-term-catalog** | Public | Extract AUTO terms from OntoGPT output | https://github.com/CultureBotAI/auto-term-catalog |
| **microbe-rules** | Public | Microbial rule systems | https://github.com/CultureBotAI/microbe-rules |

---

## Knowledge-Graph-Hub Repositories

| Repo | Purpose | URL |
|------|---------|-----|
| **kg-microbe** | Main microbial KG | https://github.com/Knowledge-Graph-Hub/kg-microbe |
| **kg-microbe-merge** | Merged KG outputs | https://github.com/Knowledge-Graph-Hub/kg-microbe-merge |
| **kg-phenio** | Phenotype KG | https://github.com/Knowledge-Graph-Hub/kg-phenio |
| **kg-registry** | KG registry | https://github.com/Knowledge-Graph-Hub/kg-registry |
| **microbe-traits-ingest** | Trait data ingestion | https://github.com/Knowledge-Graph-Hub/microbe-traits-ingest |
| **universalizer** | ID normalization | https://github.com/Knowledge-Graph-Hub/universalizer |
| **kg-cookiecutter** | KG project template | https://github.com/Knowledge-Graph-Hub/kg-cookiecutter |

---

## berkeleybop Repositories (METPO-related)

| Repo | Purpose | URL |
|------|---------|-----|
| **metpo** | METPO ontology | https://github.com/berkeleybop/metpo |
| **metpo-kgm-studio** | METPO/KG-Microbe studio | https://github.com/berkeleybop/metpo-kgm-studio |
| **metpo-kgm-copier** | Copier template for METPO/KGM workflow | https://github.com/berkeleybop/metpo-kgm-copier |

---

## Repository Relationships

```
                    biolink-model
                         │
                    (defines schema)
                         │
                         ▼
    ┌────────────────── kgx ──────────────────┐
    │              (validation)                │
    │                    │                     │
    ▼                    ▼                     ▼
kg-microbe ◄──────── METPO ──────────► cmm-ai-automation
    │           (predicates/classes)           │
    │                    │                     │
    │                    ▼                     │
    │           literature_mining              │
    │           (OntoGPT extraction)           │
    │                    │                     │
    ▼                    ▼                     ▼
┌─────────────── CultureBotAI ─────────────────┐
│  CMM-AI  │  PFAS-AI  │  PFASCommunityAgents  │
│         (AI/ML applications)                 │
└──────────────────────────────────────────────┘
```

### Data Flow

1. **METPO** defines predicates/classes for microbial traits
2. **kg-microbe** ingests BacDive/MediaDive/KEGG using METPO + Biolink
3. **cmm-ai-automation** produces KGX-compliant CMM strain data
4. **CultureBotAI repos** consume KG outputs for AI/ML applications
5. **biolink-model** and **kgx** enforce compliance standards

---

## Key Integration Points

### METPO → kg-microbe
- METPO predicates used in kg-microbe edges (e.g., `METPO:2000103`, `METPO:2000202`)
- METPO classes for phenotypes mapped via `skos:closeMatch` to Biolink
- Literature mining extracts traits grounded to METPO

### cmm-ai-automation → kg-microbe
- Shared data sources (BacDive, MediaDive)
- Compatible KGX output format
- cmm-ai-automation has stricter validation (Biolink 3.x columns)

### Biolink Model versions
- kg-microbe was using older Biolink (pre-4.3.3)
- `biolink:assesses` was removed in 4.3.6
- Need METPO predicates to fill gaps (e.g., `assesses`, `is_assessed_by`)

---

## Local Clone Locations

```
/home/mark/gitrepos/
├── biolink-model/          # biolink/biolink-model
├── kgx/                    # biolink/kgx
├── kg-microbe/             # Knowledge-Graph-Hub/kg-microbe
├── metpo/                  # berkeleybop/metpo
├── cmm-ai-automation/      # turbomam/cmm-ai-automation (this repo)
├── CMM-AI/                 # CultureBotAI/CMM-AI
└── ... (80+ other repos)
```

---

## Related Documentation

- [kg-microbe Technical Debt](./kg-microbe-technical-debt.md) - Compliance issues and fixes
- [PFAS Community Modeling](./pfas-community-modeling.md) - PFAS degradation role modeling
- [KGX Compliance](./delaney_kgx_compliance.md) - This repo's compliance approach

---

*Last updated: 2026-01-14*
