---
name: product_alchemist
description: Enhances product data using local LLMs (LM Studio) to generate SEO-optimized titles and descriptions.
---

# Product Alchemist Skill

This skill transforms raw product data into marketing-ready content using a local LLM.

## Capabilities

- Generate SEO optimized titles.
- Create sales-oriented product descriptions (HTML).
- Extract relevant tags.

## Usage

```python
from src.skills.product_alchemist.alchemist import mejorar_producto

result = mejorar_producto("Raw Title", "Specs", 100)
```

## Configuration

- `LM_STUDIO_URL`: Endpoint for local LLM (default: http://localhost:1234/v1/chat/completions)
- `MODELO_LOCAL`: Model identifier.
