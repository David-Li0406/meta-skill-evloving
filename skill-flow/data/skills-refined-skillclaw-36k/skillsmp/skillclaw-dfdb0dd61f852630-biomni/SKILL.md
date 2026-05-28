---
name: biomni
description: Use this skill when conducting multi-step biomedical research tasks across genomics, drug discovery, molecular biology, and clinical analysis, leveraging LLM reasoning and integrated biomedical databases.
---

# Biomni

## Overview

Biomni is an open-source biomedical AI agent framework that autonomously executes complex research tasks across various biomedical domains. It is designed for multi-step biological reasoning, data analysis, and research spanning genomics, drug discovery, molecular biology, and clinical analysis.

## Core Capabilities

Biomni excels at:

1. **Multi-step biological reasoning** - Autonomous task decomposition and planning for complex biomedical queries.
2. **Code generation and execution** - Dynamic analysis pipeline creation for data processing.
3. **Knowledge retrieval** - Access to integrated biomedical databases and literature.
4. **Cross-domain problem solving** - Unified interface for genomics, proteomics, drug discovery, and clinical tasks.

## When to Use This Skill

Use Biomni for:
- **CRISPR screening** - Design screens, prioritize genes, analyze knockout effects.
- **Single-cell RNA-seq** - Cell type annotation, differential expression, trajectory analysis.
- **Drug discovery** - ADMET prediction, target identification, compound optimization.
- **GWAS analysis** - Variant interpretation, causal gene identification, pathway enrichment.
- **Clinical genomics** - Rare disease diagnosis, variant pathogenicity, phenotype-genotype mapping.
- **Lab protocols** - Protocol optimization, literature synthesis, experimental design.

## Quick Start

### Installation and Setup

Install Biomni and configure API keys for LLM providers:

```bash
pip install biomni --upgrade
```

Configure API keys (store in `.env` file or environment variables):
```bash
export ANTHROPIC_API_KEY="your-key-here"
# Optional: OpenAI, Azure, Google, Groq, AWS Bedrock keys
```

Use `scripts/setup_environment.py` for interactive setup assistance.

### Basic Usage Pattern

```python
from biomni.agent import A1

# Initialize agent with data path and LLM choice
agent = A1(path='./data', llm='claude-sonnet-4-20250514')

# Execute biomedical tasks
```