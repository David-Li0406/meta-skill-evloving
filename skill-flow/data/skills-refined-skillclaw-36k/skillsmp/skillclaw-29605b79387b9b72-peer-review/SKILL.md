---
name: peer-review
description: Use this skill when conducting structured evaluations of scientific manuscripts or grant proposals, providing constructive feedback based on specific criteria and reporting standards.
---

# Scientific Critical Evaluation and Peer Review

## Overview

Peer review is a systematic process for evaluating scientific manuscripts and grant proposals. This skill helps assess methodology, statistics, design, reproducibility, ethics, and compliance with reporting standards (e.g., CONSORT, STROBE). 

## When to Use This Skill

This skill should be used when:
- Conducting peer reviews of scientific manuscripts for journals
- Evaluating grant proposals and research applications
- Assessing methodology and experimental design rigor
- Reviewing statistical analyses and reporting standards
- Evaluating reproducibility and data availability
- Checking compliance with reporting guidelines (CONSORT, STROBE, PRISMA)
- Providing constructive feedback on scientific writing

## Visual Enhancement with Scientific Schematics

When creating documents with this skill, consider adding scientific diagrams and schematics to enhance visual communication. If your document does not already contain schematics or diagrams:
- Use the **scientific-schematics** skill to generate AI-powered publication-quality diagrams by describing your desired diagram in natural language.
- The AI will automatically generate, review, and refine the schematic.

**How to generate schematics:**
```bash
python scripts/generate_schematic.py "your diagram description" -o figures/output.png
```

The AI will automatically:
- Create publication-quality images with proper formatting
- Review and refine through multiple iterations
- Ensure accessibility (colorblind-friendly, high contrast)
- Save outputs in the figures/ directory