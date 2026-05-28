---
name: vectorize-ollama
description: Create embeddings with gpt-oss:120b-cloud or other models via Ollama. Use this skill to turn text into vector representations for semantic search or comparison.
---

# Vectorize with Ollama

## Overview

This skill generates vector embeddings for text using a local Ollama instance. Default model is `nomic-embed-text`, but can be configured.

## Prerequisites

*   Local Ollama instance running (default `http://127.0.0.1:11434`).
*   The embedding model pulled (e.g., `ollama pull nomic-embed-text`).
*   `requests` library (`pip install requests`).

## Usage

### Embed Script

**Syntax:**

```bash
python3 .agent/skills/vectorize-ollama/scripts/embed.py "Your text here" [--model model_name] [--url base_url]
```

**Output:**
JSON array of floats (e.g., `[0.1, -0.2, ...]`).

**Example:**

```bash
# Basic usage
python3 .agent/skills/vectorize-ollama/scripts/embed.py "Software Engineer" > vector.json

# Specify model
python3 .agent/skills/vectorize-ollama/scripts/embed.py "Product Manager" --model llama3.2
```
