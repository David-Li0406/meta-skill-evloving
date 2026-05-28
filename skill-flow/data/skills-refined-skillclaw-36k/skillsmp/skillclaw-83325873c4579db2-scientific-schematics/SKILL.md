---
name: scientific-schematics
description: Use this skill when you need to create publication-quality scientific diagrams quickly and efficiently using AI, ensuring high standards through iterative quality review.
---

# Skill body

## Overview

This skill allows you to generate publication-quality scientific diagrams using Nano Banana Pro AI, which incorporates smart iterative refinement and quality review through Gemini 3 Pro. It is specialized in creating various types of diagrams, including neural network architectures, system diagrams, flowcharts, biological pathways, and other complex scientific visualizations.

## How it Works
1. **Describe Your Diagram**: Provide a natural language description of the diagram you need.
2. **Automatic Generation**: Nano Banana Pro generates the diagram automatically.
3. **Quality Review**: Gemini 3 Pro reviews the generated diagram against predefined quality thresholds based on the document type.
4. **Smart Iteration**: The diagram is only regenerated if the quality falls below the specified threshold.
5. **Publication-Ready Output**: Diagrams are ready for publication in minutes, with no coding or manual drawing required.

## Quality Thresholds by Document Type
| Document Type | Threshold | Description |
|---------------|-----------|-------------|
| journal       | 8.5/10    | Nature, Science, peer-reviewed journals |
| conference     | 8.0/10    | Conference papers |
| thesis        | 8.0/10    | Dissertations, theses |
| grant         | 8.0/10    | Grant proposals |
| preprint      | 7.5/10    | arXiv, bioRxiv, etc. |
| report        | 7.5/10    | Technical reports |
| poster        | 7.0/10    | Academic posters |
| presentation   | 6.5/10    | Slides, talks |
| default       | 7.5/10    | General purpose |

## Quick Start: Generate Any Diagram
To create a scientific diagram, simply describe it. Here are some examples:

```bash
# Generate for journal paper (highest quality threshold: 8.5/10)
python scripts/generate_schematic.py "CONSORT participant flow diagram with 500 screened, 150 excluded, 350 randomized" -o figures/consort.png --doc-type journal

# Generate for presentation (lower threshold: 6.5/10 - faster)
python scripts/generate_schematic.py "Transformer encoder-decoder architecture showing multi-head attention" -o figures/transformer.png --doc-type presentation

# Generate for poster (moderate threshold: 7.0/10)
python scripts/generate_schematic.py "MAPK signaling pathway from EGFR to gene transcription" -o figures/mapk.png --doc-type poster
```

All generated diagrams are stored in the `figures/` subfolder and can be referenced in your papers or posters.