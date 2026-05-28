---
name: notebook
description: Work with Jupyter notebooks in the wc_simd project. Use this skill to run, convert, or explore notebooks. Invoke with /notebook.
---

# Jupyter Notebooks

This skill helps work with Jupyter notebooks in the wc_simd project.

## Notebook Categories

### Data Ingestion & Processing
- `wellcome_dataset.ipynb` - Load works/images into Hive (738K works, 128K images)
- `download_iiif_manifests.ipynb` - Batch download IIIF manifests (340K files)
- `iiif_manifests.ipynb` - Process manifests for text renderings (226K works)
- `iiif_manifest_pages.ipynb` - Estimate collection size (~42M pages)

### Text Analysis & NLP
- `alto_text.ipynb` - OCR text analysis (9.8B words, 78.9% English)
- `alto_text_chunking.ipynb` - Text chunking (74M chunks) + Elasticsearch indexing
- `alto_text_analysis.ipynb` - Comprehensive NLP: NER, sentiment, topic modeling

### Labels & Metadata
- `dn_labels.ipynb` - Combined labels DataFrame (646K labels)
- `works_labels.ipynb` - Genre/subject/concept exploration

### VLM Embeddings
- `vlm_embed.ipynb` - VLM embedding analysis (537K attempted, 150K failed)
- `vlm_embed_train_data.ipynb` - AE3D latent visualization, UMAP plots

### Name Reconciliation
- `name_rec_poc.ipynb` - Name reconciliation POC with Qwen3-Embedding
- `narese_evaluation.ipynb` - NARESE evaluation (81.7% accuracy)

### LLM & Agents
- `llm.ipynb` - Test VLLM/VLM models (Qwen3-30B, Qwen2.5-VL)
- `chat_simple.ipynb` - LangGraph chat with memory
- `agent_spark_sql_toolkit.ipynb` - Spark SQL agent
- `describe_works.ipynb` - LLM-driven SQL generation

## Run Notebook

### Interactive (Jupyter)
```bash
jupyter notebook notebooks/
```

### Non-Interactive (papermill)
```bash
papermill notebooks/alto_text.ipynb output.ipynb
```

### Convert to Script
```bash
jupyter nbconvert --to script notebooks/alto_text.ipynb
```

### Convert to HTML
```bash
jupyter nbconvert --to html notebooks/alto_text.ipynb
```

## Start Jupyter Server

```bash
# Standard
jupyter notebook

# With specific port
jupyter notebook --port 8889

# Lab interface
jupyter lab
```

## Clear Outputs

```bash
jupyter nbconvert --clear-output --inplace notebooks/*.ipynb
```

## Prerequisites

Ensure Spark is running for notebooks that use Hive tables:
```bash
cd spark_docker_s3 && docker compose up -d --build
```

Load environment variables:
```python
from dotenv import load_dotenv
load_dotenv()
```
