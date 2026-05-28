# References Folder

## Overview

Contains templates, detailed workflow instructions, and research compilations for Specification-Driven Development.

## File Summary

| File | Description |
|------|-------------|
| **templates.md** | All SDD document templates (constitution, spec, design, impl-plan, task, roadmap, etc.) |
| **workflows.md** | Detailed step-by-step instructions for all 13 SDD sections |
| ai-assisted-specification-writing.md | Using LLMs for spec generation, human-AI collaboration workflow |
| living-documentation-docs-as-code.md | Treating docs like code, CI/CD integration, auto-generation |
| architecture-decision-records.md | Nygard format, ADR lifecycle, status types, co-location with code |
| api-first-development.md | OpenAPI 3.1, contract testing, mock servers, SDK generation |
| design-docs-patterns-big-tech.md | Google Design Docs, Uber ERD/RFC, Amazon 6-pager approaches |
| key-trends-summary.md | Summary of 2025-2026 trends and all sources |
| yaml-frontmatter.md | YAML frontmatter conventions for SDD files |

## Primary Files

### templates.md

All SDD document templates in one place:
- Constitution template
- Specification template
- Design document template
- Implementation plan template
- Task file template
- Roadmap template
- Backlog item template
- Confidence check template
- Pattern/mistake record templates (JSON)
- Token estimation guide

### workflows.md

Detailed step-by-step instructions for all 13 sections of the SDD workflow:

1. Writing Constitutions (Modes: existing/new project)
2. Writing Specifications (Brainstorm -> Research -> Clarify -> Draft -> Review)
3. Writing Design Documents (Read -> Research -> Decisions -> Approach)
4. Writing Implementation Plans (100k rule, dependencies, waves)
5. Task Creation (faion-task-creator-agent)
6. Task Execution (faion-task-executor-agent)
7. Batch Execution (all tasks with continue/stop rules)
8. Parallelization Analysis (wave pattern, speedup)
9. Backlog Grooming (Definition of Ready)
10. Roadmapping (Now/Next/Later structure)
11. Quality Gates (L1-L6, code/SDD review)
12. Confidence Checks (thresholds, phase-specific)
13. Reflexion Learning (PDCA, memory storage)

## Research Files

### ai-assisted-specification-writing.md

AI-assisted specification writing methodology:
- SDD-AI workflow: Intent -> Spec -> Plan -> Execution -> Review
- Human-AI collaboration process
- Tools: AWS Kiro, Claude Code, Cursor, Windsurf
- Templates for spec generation and review

### living-documentation-docs-as-code.md

Living documentation (Docs-as-Code) approach:
- Docs-as-Code principles
- CI/CD pipeline for documentation
- LLM-ready documentation structure
- Tools: Doxygen, Sphinx, Mintlify, GitBook

### architecture-decision-records.md

Architecture Decision Records (ADR):
- Nygard format structure
- ADR lifecycle and status types
- Templates for ADR and review meetings
- Best practices for co-location with code

### api-first-development.md

API-First development approach:
- API-First principles and workflow
- OpenAPI 3.1 specification template
- CI/CD pipeline for contract testing
- Tools: Spectral, Prism, Pact, Dredd

### design-docs-patterns-big-tech.md

Design document patterns from Big Tech:
- Google Design Doc template
- Uber RFC/ERD template
- Amazon 6-pager approach
- Best practices for silent reading and reviews

### key-trends-summary.md

Summary of key trends 2025-2026:
- SDD trends: AI as specification partner, bottleneck shift
- Living documentation: Docs-as-Code mainstream
- ADRs: Standard practice across AWS, Google, Microsoft
- API development: API-First mandatory, contract testing
- Complete sources list

## Sources

Research drawn from:

- **Thoughtworks** - SDD engineering practices
- **Martin Fowler** - SDD tools analysis
- **AWS** - ADR best practices
- **Google Cloud** - Architecture documentation
- **Microsoft** - Spec-driven development, Azure ADR
- **Red Hat** - AI coding quality
- **Pragmatic Engineer** - RFCs and design docs
- **Uber** - H3 RFC template
- **JetBrains** - Spec-driven approach for AI

## Usage

1. **Need a template?** Start with `templates.md`
2. **Need workflow details?** Check `workflows.md`
3. **Need best practices?** See research files
4. **Need trends/sources?** See `key-trends-summary.md`
