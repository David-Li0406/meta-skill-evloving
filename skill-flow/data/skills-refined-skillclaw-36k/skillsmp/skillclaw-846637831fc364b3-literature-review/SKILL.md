---
name: literature-review
description: Use this skill when conducting systematic literature reviews, meta-analyses, or comprehensive literature searches across biomedical, scientific, and technical domains to create professionally formatted documents with verified citations.
---

# Literature Review

## Overview

Conduct comprehensive, systematic literature reviews following rigorous academic methodology. This skill allows you to search multiple literature databases (e.g., PubMed, arXiv, bioRxiv, Semantic Scholar), synthesize findings thematically, verify citations for accuracy, and generate professional output documents in markdown and PDF formats.

## When to Use This Skill

Use this skill when:
- Conducting a systematic literature review for research or publication
- Synthesizing current knowledge on a specific topic across multiple sources
- Performing meta-analysis or scoping reviews
- Writing the literature review section of a research paper or thesis
- Investigating the state of the art in a research domain
- Identifying research gaps and future directions
- Requiring verified citations and professional formatting

## Visual Enhancement with Scientific Schematics

**⚠️ MANDATORY: Every literature review MUST include at least 1-2 AI-generated figures using the scientific-schematics skill.**

Before finalizing any document:
1. Generate at minimum ONE schematic or diagram (e.g., PRISMA flow diagram for systematic reviews).
2. Prefer 2-3 figures for comprehensive reviews (search strategy flowchart, thematic synthesis diagram, conceptual framework).

**How to generate figures:**
- Use the **scientific-schematics** skill to generate AI-powered publication-quality diagrams by describing your desired diagram in natural language.
- The system will automatically generate, review, and refine the schematic.

**How to generate schematics:**
```bash
python scripts/generate_schematic.py "your diagram description" -o figures/output.png
```