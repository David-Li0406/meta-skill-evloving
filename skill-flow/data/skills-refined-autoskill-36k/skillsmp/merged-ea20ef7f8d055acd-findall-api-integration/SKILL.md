---
name: findall-api-integration
description: Use this skill when building applications with the Parallel FindAll API to discover and evaluate entities based on complex criteria from natural language objectives.
---

# FindAll API - Complete Reference

The FindAll API discovers and evaluates entities that match complex criteria from natural language objectives. Submit a high-level goal and the service automatically generates structured match conditions, discovers relevant candidates, and evaluates each against the criteria. Returns comprehensive results with detailed reasoning, citations, and confidence scores for each match decision.

## Table of Contents

- [Quickstart](#quickstart)
- [Core Concepts](#core-concepts)
  - [Candidates](#candidates)
  - [Lifecycle](#lifecycle)
  - [Generators & Pricing](#generators--pricing)
- [API Operations](#api-operations)
  - [Create & Ingest](#create--ingest)
  - [Retrieve & Monitor](#retrieve--monitor)
  - [Modify & Control](#modify--control)
- [Advanced Features](#advanced-features)
  - [Streaming Events](#streaming-events)
  - [Enrichments](#enrichments)
  - [Webhooks](#webhooks)
  - [Preview & Refresh](#preview--refresh)
- [Migration Guide](#migration-guide)
- [Best Practices](#best-practices)
- [Error Handling](#error-handling)
- [Complete Example: Company Research Pipeline](#complete-example-company-research-pipeline)
- [API Reference Summary](#api-reference-summary)
- [Additional Resources](#additional-resources)

---

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
print(f"Entity type: {schema.entity_type}")
print(f"Match conditions: {schema.match_conditions}")

# Create run with the generated schema
run = client.findall.runs.create(
    objective=schema.objective,
    entity_type=schema.entity_type,
    match_conditions=schema.match_conditions,
    generator="core",
    match_limit=50
)
```

---

## Core Concepts

### Candidates

A **candidate** represents a potential match for your FindAll objective. Candidates progress through different states during evaluation:

#### Match Statuses

- **`generated`**: Candidate has been discovered but not yet evaluated
- **`matched`**: Candidate satisfies all match conditions
- **`unmatched`**: Candidate fails to satisfy one or more match conditions
- **`discarded`**: Candidate was determined to be irrelevant or duplicate

#### Candidate Structure

```json
{
  "candidate_id": "candidate_7594eb7c-4f4a-487f-9d0c-9d1e63ec240c",
  "name": "Cognition AI",
  "url": "cognition.ai",
  "description": "AI software engineering company",
  "match_status": "matched",
  "output": {
    "developing_ai_products_check": "yes",
    "raised_series_a_2024_check": "yes"
  },
  "basis": [
    {
      "field": "developing_ai_products_check",
      "citations": [
        {
          "title": "Cognition - Devin and Cognition AI",
          "url": "https://cognition.ai/",
          "excerpts": ["We're the makers of Devin..."]
        }
      ],
      "reasoning": "The search results repeatedly state that Cognition AI is an 'applied AI lab building the future of software engineering'...",
      "confidence": "high"
    }
  ]
}
```

### Lifecycle

FindAll runs progress through several states:

```
queued → running → completed
              ↓
         action_required (if needed)
              ↓
         cancelling → cancelled
              ↓
           failed
```

#### Status Descriptions

- **`queued`**: Run is waiting to start
- **`action_required`**: Run needs user input (rare)
- **`running`**: Actively discovering and evaluating candidates
- **`completed`**: Run finished successfully
- **`failed`**: Run encountered an error
- **`cancelling`**: Cancellation in progress
- **`cancelled`**: Run was cancelled by user

### Generators & Pricing

Generators control the quality, speed, and cost of FindAll runs:

| Generator   | Quality      | Speed    | Price per Match |
| ----------- | ------------ | -------- | --------------- |
| **base**    | Good         | Fast     | $0.30           |
| **core**    | Better       | Moderate | $1.50           |
| **pro**     | Best         | Slower   | $3.00           |
| **preview** | Experimental | Varies   | $1.50           |

---

## API Operations

### Create & Ingest

#### Ingest FindAll Run

Transforms a natural language objective into a structured FindAll specification.

**Note**: Requires `parallel-beta` header.

**Endpoint**: `POST /v1beta/findall/ingest`

**Request**:

```json
{
  "objective": "Find all AI companies that raised Series A funding in 2024"
}
```

**Response**:

```json
{
  "objective": "Find all AI companies that raised Series A funding in 2024",
  "entity_type": "companies",
  "match_conditions": [
    {
      "name": "developing_ai_products_check",
      "description": "Company must be developing artificial intelligence (AI) products"
    },
    {
      "name": "raised_series_a_2024_check",
      "description": "Company must have raised Series A funding in 2024"
    }
  ],
  "generator": "core"
}
```

### Create FindAll Run

Starts a FindAll run that discovers and evaluates entities.

**Endpoint**: `POST /v1beta/findall/runs`

**Request**:

```json
{
  "objective": "Find all AI companies that raised Series A funding in 2024",
  "entity_type": "companies",
  "match_conditions": [
    {
      "name": "developing_ai_products_check",
      "description": "Company must be developing artificial intelligence (AI) products"
    },
    {
      "name": "raised_series_a_2024_check",
      "description": "Company must have raised Series A funding in 2024"
    }
  ],
  "generator": "core",
  "match_limit": 50,
  "exclude_list": [
    {
      "name": "OpenAI",
      "url": "openai.com"
    }
  ],
  "metadata": {
    "project": "Q1 research"
  },
  "webhook": {
    "url": "https://example.com/webhook",
    "event_types": ["task_run.status"]
  }
}
```

### Retrieve & Monitor

#### Retrieve FindAll Run Status

Get the current status of a FindAll run.

**Endpoint**: `GET /v1beta/findall/runs/{findall_id}`

#### Get FindAll Run Result

Retrieve the complete result snapshot including all evaluated candidates.

**Endpoint**: `GET /v1beta/findall/runs/{findall_id}/result`

### Modify & Control

#### Extend FindAll Run

Add more matches to an existing run by increasing the match limit.

**Endpoint**: `POST /v1beta/findall/runs/{findall_id}/extend`

**Request**:

```json
{
  "additional_match_limit": 25
}
```

#### Add Enrichment to FindAll Run

Add structured data extraction to matched candidates.

**Endpoint**: `POST /v1beta/findall/runs/{findall_id}/enrich`

**Request**:

```json
{
  "processor": "core",
  "output_schema": {
    "json_schema": {
      "type": "object",
      "properties": {
        "ceo_name": {
          "type": "string",
          "description": "Name of the current CEO"
        },
        "funding_amount": {
          "type": "string",
          "description": "Total funding amount in USD"
        }
      },
      "required": ["ceo_name"]
    },
    "type": "json"
  },
  "mcp_servers": [
    {
      "type": "url",
      "url": "https://api.example.com/mcp",
      "name": "company_data",
      "headers": {
        "Authorization": "Bearer token"
      },
      "allowed_tools": ["get_company_info"]
    }
  ]
}
```

#### Cancel FindAll Run

Stop an active FindAll run.

**Endpoint**: `POST /v1beta/findall/runs/{findall_id}/cancel`

---

## Advanced Features

### Streaming Events

Monitor FindAll runs in real-time using Server-Sent Events (SSE).

**Endpoint**: `GET /v1beta/findall/runs/{findall_id}/events`

**Query Parameters**:

- `last_event_id` (optional): Resume from specific event
- `timeout` (optional): Connection timeout in seconds

### Enrichments

Add structured data fields to matched candidates after initial matching.

### Webhooks

Receive HTTP notifications when FindAll events occur.

### Preview & Refresh

#### Preview Mode

Test your FindAll configuration before committing to a full run.

#### Refresh Results

Re-evaluate candidates with updated web data or revised match conditions.

---

## Migration Guide

### From Tasks API to FindAll API

The FindAll API is purpose-built for discovering multiple entities, replacing the pattern of running many parallel Task API calls.

---

## Best Practices

### Writing Match Conditions

**Be Specific**:

```python
# ❌ Too vague
"Company must be successful"

# ✅ Specific and verifiable
"Company must have raised Series A funding of at least $10M in 2024"
```

### Cost Optimization

1. **Start with preview**: Test with `generator="preview"` first
2. **Use base for scale**: Use `base` generator for large searches (100+ matches)

---

## Error Handling

### Common Errors

**422 Validation Error**:

```python
try:
    run = client.findall.runs.create(
        match_limit=5000  # Over max of 1000
    )
except Exception as e:
    print(f"Invalid parameters: {e}")
```

---

## Complete Example: Company Research Pipeline

```python
from parallel import Parallel
import time

client = Parallel(api_key="your_api_key")

# Step 1: Ingest objective
print("Generating FindAll schema...")
schema = client.findall.ingest.create(
    objective="Find YC-backed AI companies founded in 2023 with active products"
)

# Step 2: Start FindAll run
print("\nStarting FindAll run...")
run = client.findall.runs.create(
    objective=schema.objective,
    entity_type=schema.entity_type,
    match_conditions=schema.match_conditions,
    generator="core",
    match_limit=50,
    metadata={"project": "Q1_2025_research"}
)

# Step 3: Monitor with SSE
print(f"\nMonitoring run {run.findall_id}...")
matched_count = 0

for event in client.findall.runs.events(run.findall_id):
    if event.type == "findall.candidate.matched":
        matched_count += 1
        candidate = event.data
        print(f"✓ Match #{matched_count}: {candidate.name}")

# Step 4: Add enrichments for matched companies
print("\nAdding enrichments...")
client.findall.runs.enrich(
    findall_id=run.findall_id,
    processor="core",
    output_schema={
        "json_schema": {
            "type": "object",
            "properties": {
                "ceo_name": {"type": "string"},
                "employee_count": {"type": "integer"},
                "total_funding": {"type": "string"}
            }
        },
        "type": "json"
    }
)

# Step 5: Get final results
print("\nFinal results:")
result = client.findall.runs.result(run.findall_id)

for candidate in result.candidates:
    if candidate.match_status == "matched":
        output = candidate.output
        print(f"\n{candidate.name} ({candidate.url})")
        print(f"  CEO: {output.get('ceo_name', 'N/A')}")
        print(f"  Employees: {output.get('employee_count', 'N/A')}")
        print(f"  Funding: {output.get('total_funding', 'N/A')}")

print(f"\n✓ Found {matched_count} companies matching criteria")
```

---

## API Reference Summary

| Endpoint                           | Method | Purpose                                |
| ---------------------------------- | ------ | -------------------------------------- |
| `/v1beta/findall/ingest`           | POST   | Generate FindAll schema from objective |
| `/v1beta/findall/runs`             | POST   | Create FindAll run                     |
| `/v1beta/findall/runs/{id}`        | GET    | Get run status                         |
| `/v1beta/findall/runs/{id}/result` | GET    | Get complete results                   |
| `/v1beta/findall/runs/{id}/schema` | GET    | Get run schema                         |
| `/v1beta/findall/runs/{id}/events` | GET    | Stream events (SSE)                    |
| `/v1beta/findall/runs/{id}/extend` | POST   | Increase match limit                   |
| `/v1beta/findall/runs/{id}/enrich` | POST   | Add enrichments                        |
| `/v1beta/findall/runs/{id}/cancel` | POST   | Cancel run                             |

---

## Additional Resources

- **API Reference**: https://docs.parallel.ai/api-reference/findall-api-beta/
- **Python SDK**: https://github.com/parallelinc/parallel-python
- **Support**: support@parallel.ai
- **Status Page**: https://status.parallel.ai

---

_Last Updated: January 2025_
_API Version: 0.1.2_