---
name: peer-review
description: Use this skill when you need to systematically evaluate scientific manuscripts or grant proposals, focusing on methodology, statistics, design, and compliance with reporting standards.
---

# Scientific Critical Evaluation and Peer Review

## Overview

Peer review is a systematic process for evaluating scientific manuscripts and grant proposals. This skill helps assess methodology, statistics, design, reproducibility, ethics, and reporting standards across disciplines, providing constructive and rigorous evaluations.

## When to Use This Skill

Use this skill when:
- Conducting peer reviews of scientific manuscripts for journals
- Evaluating grant proposals and research applications
- Assessing methodology and experimental design rigor
- Reviewing statistical analyses and reporting standards
- Evaluating reproducibility and data availability
- Checking compliance with reporting guidelines (e.g., CONSORT, STROBE, PRISMA)
- Providing constructive feedback on scientific writing

## Visual Enhancement with Scientific Schematics

To enhance visual communication in your documents, consider adding scientific diagrams and schematics. If your document lacks these elements:
- Use the **scientific-schematics** skill to generate AI-powered publication-quality diagrams by describing your desired diagram in natural language.
- The AI will automatically create, review, and refine the schematic.

### How to Generate Schematics
```bash
python scripts/generate_schematic.py "your diagram description" -o figures/output.png
```

The AI will:
- Create publication-quality images with proper formatting
- Review and refine through multiple iterations
- Ensure accessibility (colorblind-friendly, high contrast)
- Save outputs in the figures/ directory

### When to Add Schematics
- Peer review workflow diagrams
- Evaluation criteria decision trees
- Review process flowcharts
- Methodology assessment frameworks
- Quality assessment visualizations
- Reporting guidelines compliance diagrams
- Any complex concept that benefits from visualization

For detailed guidance on creating schematics, refer to the scientific-schematics skill documentation.