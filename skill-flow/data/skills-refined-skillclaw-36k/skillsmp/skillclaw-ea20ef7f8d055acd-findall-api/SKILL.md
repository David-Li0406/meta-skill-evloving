---
name: findall-api
description: Use this skill when building applications with the Parallel FindAll API to discover and evaluate entities based on complex criteria from natural language objectives.
---

# Skill body

## Overview

The FindAll API discovers and evaluates entities that match complex criteria from natural language objectives. Submit a high-level goal, and the service automatically generates structured match conditions, discovers relevant candidates, and evaluates each against the criteria. It returns comprehensive results with detailed reasoning, citations, and confidence scores for each match decision.

## Core Concepts

### FindAll Lifecycle

A FindAll run progresses through several statuses:

1. **queued** - Run has been created and is waiting to start.
2. **action_required** - User input needed (e.g., schema review).
3. **running** - Actively discovering and evaluating candidates.
4. **completed** - Successfully finished with all results available.
5. **failed** - Encountered an error during execution.
6. **cancelling** - Cancel request received, shutting down.
7. **cancelled** - Successfully cancelled by user.

**Active statuses**: queued, action_required, running, cancelling  
**Terminal statuses**: completed, failed, cancelled

### FindAll Candidates

Candidates represent entities being evaluated against match conditions. Each candidate has:

- **candidate_id** - Unique identifier.
- **name** - Entity name.
- **url** - Context URL for disambiguation.
- **description** - Brief description (optional).
- **match_status** - One of: generated, matched, unmatched, discarded.
- **output** - Structured results of match condition evaluations.
- **basis** - Citations, reasoning, and confidence for each field.

A candidate is considered a **match** only if ALL match conditions are satisfied.

## Quickstart

### Basic FindAll Run

```python
from parallel import Parallel
import time

client = Parallel(api_key="your_api_key")

# Create a FindAll run
run = client.findall.runs.create(
    objective="Find all AI companies that raised Series A funding in 2024",
    entity_type="companies",
    match_conditions=[
        {
            "name": "developing_ai_products_check",
            "description": "Company must be developing artificial intelligence (AI) products"
        },
        {
            "name": "raised_series_a_2024_check",
            "description": "Company must have raised Series A funding in 2024"
        }
    ],
    generator="core",
    match_limit=50
)

# Poll for results
while run.status.is_active:
    run = client.findall.runs.retrieve(run.findall_id)
    time.sleep(5)

# Get final results
result = client.findall.runs.result(run.findall_id)
for candidate in result.candidates:
    if candidate.match_status == "matched":
        print(f"Match: {candidate.name} - {candidate.url}")
```

### Using Ingest for Auto-Generation

```python
# Let the API generate match conditions from your objective
schema = client.findall.ingest.create(
    objective="Find all AI companies that raised Series A funding in 2024"
)

# Review and customize the generated schema
print(f"Generated schema: {schema}")
```