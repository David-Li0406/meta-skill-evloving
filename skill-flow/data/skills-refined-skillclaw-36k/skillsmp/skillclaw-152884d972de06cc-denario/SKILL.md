---
name: denario
description: Use this skill when you need to automate scientific research workflows, from data analysis to publication-ready manuscripts, including generating research ideas, developing methodologies, and executing computational experiments.
---

# Denario

## Overview

Denario is a multiagent AI system designed to automate scientific research workflows from initial data analysis through publication-ready manuscripts. Built on AG2 and LangGraph frameworks, it orchestrates multiple specialized agents to handle hypothesis generation, methodology development, computational analysis, and paper writing.

## When to Use This Skill

Use this skill when:
- Analyzing datasets to generate novel research hypotheses
- Developing structured research methodologies
- Executing computational experiments and generating visualizations
- Conducting literature searches for research context
- Writing journal-formatted LaTeX papers from research results
- Automating the complete research pipeline from data to publication

## Installation

Install Denario using uv (recommended):

```bash
uv init
uv add "denario[app]"
```

Or using pip:

```bash
uv pip install "denario[app]"
```

For Docker deployment or building from source, see the installation documentation.

## LLM API Configuration

Denario requires API keys from supported LLM providers. Supported providers include:
- Google Vertex AI
- OpenAI
- Other LLM services compatible with AG2/LangGraph

Store API keys securely using environment variables or `.env` files. For detailed configuration instructions, refer to the LLM configuration documentation.

## Core Research Workflow

Denario follows a structured four-stage research pipeline:

### 1. Data Description

Define the research context by specifying available data and tools:

```python
from denario import Denario

den = Denario(project_dir="./my_research")
den.set_data_description("""
Available datasets: time-series data on X and Y
Tools: pandas, sklearn, matplotlib
Research domain: [specify domain]
""")
```

### 2. Idea Generation

Generate research hypotheses from the data description:

```python
den.get_idea()
```

This produces a research question or hypothesis based on the described data.