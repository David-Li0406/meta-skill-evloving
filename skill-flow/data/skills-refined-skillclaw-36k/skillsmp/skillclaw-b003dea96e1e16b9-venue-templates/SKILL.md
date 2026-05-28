---
name: venue-templates
description: Use this skill when preparing manuscripts for journal submission, conference papers, research posters, or grant proposals and need venue-specific formatting requirements and templates.
---

# Venue Templates

## Overview

Access comprehensive LaTeX templates, formatting requirements, and submission guidelines for major scientific publication venues, academic conferences, research posters, and grant proposals. This skill provides ready-to-use templates and detailed specifications for successful academic submissions across disciplines.

## When to Use This Skill

This skill should be used when:
- Preparing a manuscript for submission to a specific journal (Nature, Science, PLOS, IEEE, etc.)
- Writing a conference paper with specific formatting requirements (NeurIPS, ICML, CHI, etc.)
- Creating an academic research poster for conferences
- Drafting grant proposals for federal agencies (NSF, NIH, DOE, DARPA) or private foundations
- Checking formatting requirements and page limits for target venues
- Customizing templates with author information and project details
- Verifying document compliance with venue specifications

## Visual Enhancement with Scientific Schematics

When creating documents with this skill, always consider adding scientific diagrams and schematics to enhance visual communication. If your document does not already contain schematics or diagrams:
- Use the **scientific-schematics** skill to generate AI-powered publication-quality diagrams by describing your desired diagram in natural language.
- The AI will automatically generate, review, and refine the schematic.

## How to Generate Schematics

```bash
python scripts/generate_schematic.py "your diagram description" -o figures/output.png
```