---
name: dev
description: Maintainer guide for docpack_confluence development. Use when understanding project architecture, implementing features, or learning the codebase.
---

# docpack_confluence Maintainer Guide

This skill provides guidance for developing and maintaining the docpack_confluence library.

## Available Topics

Read the specific document when you need detailed information:

| Topic | Document | When to Read |
|-------|----------|--------------|
| **Project Overview** | [01-About-This-Project](docs/source/02-Maintainer-Guide/01-About-This-Project/index.rst) | Understanding project vision, pain points solved, and use cases |
| **Filter Language** | [02-Filter-Language](docs/source/02-Maintainer-Guide/02-Filter-Language/index.rst) | When working with include/exclude patterns, wildcards (`/*`, `/**`), URL-based matching, page selection logic, or gitignore-style filters |
| **Data Fetching Strategy** | [03-Data-Fetching-Strategy](docs/source/02-Maintainer-Guide/03-Data-Fetching-Strategy/index.rst) | When working with hierarchy fetching, understanding API depth=5 limitation, Parent Clustering Algorithm, crawler optimization, or caching strategy |
| **Testing Strategy and Workflow** | [04-Testing-Strategy-and-Workflow](docs/source/02-Maintainer-Guide/04-Testing-Strategy-and-Workflow/index.rst) | When writing tests, creating/deleting test data, understanding hierarchy_specs format, running manual tests, or validating crawler behavior |
| **Export and Pack Module** | [05-Export-and-Pack-Module](docs/source/02-Maintainer-Guide/05-Export-and-Pack-Module/index.rst) | When working with exporter.py, pack.py, SpaceExportConfig, ExportSpec, XML export, all-in-one file generation, or running test_pack.py |

## Quick Reference

- **Understand the project**: Read "Project Overview" first
- **Learn filter syntax**: Read "Filter Language" for include/exclude patterns
- **Understand hierarchy fetching**: Read "Data Fetching Strategy" for Parent Clustering Algorithm
- **Write tests**: Read "Testing Strategy and Workflow" for test data and workflow
- **Export pages to XML**: Read "Export and Pack Module" for exporter.py and pack.py

## Core Concepts

### The Three Pain Points

1. **Precise Batch Selection**: gitignore-style `include`/`exclude` patterns with `/*` wildcards
2. **Rich Metadata Output**: XML-wrapped Markdown with source URLs and hierarchical metadata
3. **Single-File Packaging**: Consolidate all pages into one file for easy AI platform sync

### Key Components

- `Entity`: Data model for Confluence nodes with lineage (hierarchy path)
- `crawl_descendants`: Parent Clustering Algorithm for fetching complete hierarchies
- `crawl_descendants_with_cache`: Cached version for repeated access
- `Selector`: Pattern matcher for include/exclude filtering
- `filter_pages`: Pure filtering function for cached entities
- `select_pages`: Convenience API combining crawl + filter
- `SpaceExportConfig`: Configuration for exporting pages from a single space
- `ExportSpec`: High-level API for multi-space export with all-in-one merge

## Related Skills

(Add related skills here as needed)
