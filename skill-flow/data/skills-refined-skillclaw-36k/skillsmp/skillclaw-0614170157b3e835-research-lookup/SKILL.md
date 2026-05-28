---
name: research-lookup
description: Use this skill when you need to look up current research information, including academic papers, recent studies, and technical documentation, utilizing Perplexity's Sonar models through OpenRouter.
---

# Research Information Lookup

## Overview

This skill enables real-time research information lookup using Perplexity's Sonar models through OpenRouter. It intelligently selects between **Sonar Pro Search** (fast, efficient lookup) and **Sonar Reasoning Pro** (deep analytical reasoning) based on query complexity. The skill provides access to current academic literature, recent studies, technical documentation, and general research information with proper citations and source attribution.

## When to Use This Skill

Use this skill when you need:

- **Current Research Information**: Latest studies, papers, and findings in a specific field.
- **Literature Verification**: Check facts, statistics, or claims against current research.
- **Background Research**: Gather context and supporting evidence for scientific writing.
- **Citation Sources**: Find relevant papers and studies to cite in manuscripts.
- **Technical Documentation**: Look up specifications, protocols, or methodologies.
- **Recent Developments**: Stay current with emerging trends and breakthroughs.
- **Statistical Data**: Find recent statistics, survey results, or research findings.
- **Expert Opinions**: Access insights from recent interviews, reviews, or commentary.

## Visual Enhancement with Scientific Schematics

When creating documents with this skill, always consider adding scientific diagrams and schematics to enhance visual communication. If your document does not already contain schematics or diagrams:

- Use the **scientific-schematics** skill to generate AI-powered publication-quality diagrams.
- Simply describe your desired diagram in natural language, and the AI will automatically generate, review, and refine the schematic.

**How to generate schematics:**
```bash
python scripts/generate_schematic.py "your diagram description" -o figures/output.png
```