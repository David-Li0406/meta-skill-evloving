---
name: similarity-cosine
description: Compute cosine similarity between two embeddings. Use this to determine how similar two pieces of text are based on their vector representations.
---

# Cosine Similarity

## Overview

Calculates the cosine similarity between two vectors provided as JSON files. Result is a score between -1.0 and 1.0 (usually 0.0 to 1.0 for embeddings).

## Usage

### Similarity Script

**Syntax:**

```bash
python3 .agent/skills/similarity-cosine/scripts/cosine_sim.py <vector1.json> <vector2.json>
```

**Arguments:**
*   `vector1.json`: JSON file containing a list of floats.
*   `vector2.json`: JSON file containing a list of floats.

**Example:**

```bash
python3 .agent/skills/similarity-cosine/scripts/cosine_sim.py resume_vec.json job_vec.json
# Output: 0.854321
```
