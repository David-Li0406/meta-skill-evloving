# CMM-AI Data Workflow Analysis

**Date:** 2025-12-05
**Analyst:** Claude Code
**Purpose:** Document the actual data flow, sources, and gaps in the CMM-AI pipeline

---

## Navigation

| Chapter | Description |
|---------|-------------|
| [01 - Project Context](01_project_context.md) | DOE BER proposal, funding, KG-CMREE goals, data table mapping |
| [02 - Data Model Analysis](02_data_model_analysis.md) | Two data systems, foreign keys, media/ingredients model, schema relationships |
| [03 - Data Quality Issues](03_data_quality_issues.md) | UTF-8 corruption, undefined vocabularies, fake publications, missing provenance |
| [04 - Code Analysis](04_code_analysis.md) | Makefile targets (including 7 broken), orphaned scripts, hardcoded data inventory |
| [05 - API and LLM](05_api_and_llm.md) | External APIs, LLM-generated code evidence, GitHub Actions workflows |
| [06 - Setup Guide](06_setup_guide.md) | Barriers to running scripts, missing KG databases, NCBI email bug, quick start |
| [07 - Recommendations](07_recommendations.md) | Prioritized fixes: immediate, short-term, medium-term, long-term |
| [08 - Appendices](08_appendices.md) | File inventory, key file locations, prefix registry proposal |

---

## Executive Summary

The CMM-AI project has **two parallel data systems** that are not well integrated or documented:

1. **Google Sheets** (collaborative manual entry) -> XLSX download -> TSV conversion
2. **Python extend scripts** (deterministic/API-based) -> Extended TSV files

There is no documentation explaining how these systems relate, which is authoritative, or how to reproduce the current state of the data.

### Critical Issues Found

| Issue | Impact | Chapter |
|-------|--------|---------|
| 7 Makefile targets with wrong paths | Commands fail | [04](04_code_analysis.md) |
| 4 files with NCBI email placeholder | API calls fail | [06](06_setup_guide.md) |
| 4 fake publications with non-existent DOIs | Data contamination | [03](03_data_quality_issues.md) |
| Missing KG databases (~44GB) | KG features unavailable | [06](06_setup_guide.md) |
| Hardcoded data with NO citations | Unknown provenance | [05](05_api_and_llm.md) |
| UTF-8 mojibake in Google Sheet data | Display corruption | [03](03_data_quality_issues.md) |

### Questions Requiring Human Answers

1. Who is responsible for Google Sheet data entry?
2. What is the download/conversion cadence?
3. Which TSV version is authoritative (base or extended)?
4. Where did MP medium data come from?
5. What is the intended merge strategy?

---

*This analysis was split from a single 2,323-line file to improve navigation and reduce redundancy.*
