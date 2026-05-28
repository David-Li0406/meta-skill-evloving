---
name: vertex-ai-agent-builder
description: Build and deploy production-ready generative AI agents using Vertex AI, Gemini models, and Google Cloud infrastructure with RAG, function calling, and multi-modal capabilities.
---

# Vertex AI Agent Builder

This skill provides a comprehensive framework for building and deploying production-ready agents on Vertex AI, leveraging Gemini models, retrieval-augmented generation (RAG), function calling, and multi-modal capabilities.

## Overview

- Produces an agent scaffold aligned with Vertex AI Agent Engine deployment patterns.
- Helps choose models/regions, design tool/function interfaces, and wire up retrieval.
- Includes an evaluation and smoke-test checklist to ensure deployments don’t regress.

## Prerequisites

- Google Cloud project with Vertex AI API enabled.
- Permissions to deploy/operate Agent Engine runtimes (or a local-only build target).
- If using RAG: a document source (GCS/BigQuery/Firestore/etc.) and an embeddings/index strategy.
- Secrets handled via environment variables or Secret Manager (never committed).

## Instructions

1. Clarify the agent’s job (user intents, inputs/outputs, latency, and cost constraints).
2. Choose model + region and define tool/function interfaces (schemas, error contracts).
3. Implement retrieval (if needed): chunking, embeddings, index, and a “citation-first” response format.
4. Add evaluation: golden prompts, offline checks, and a minimal online smoke test.
5. Deploy (optional): provide the exact deployment command/config and verify endpoints + permissions.
6. Add operations: logs/metrics, alerting, quota/cost guardrails, and rollback steps.

## Output

- A Vertex AI agent scaffold (code/config) with clear extension points.
- A retrieval plan (when applicable) and a validation/evaluation checklist.
- Optional: deployment commands and post-deploy health checks.

## Error Handling

- Quota/region issues: detect the failing service/quota and propose a scoped fix.
- Auth failures: identify the principal and missing role; prefer least-privilege remediation.
- Retrieval failures: validate indexing/embedding dimensions and add fallback behavior.
- Tool/function errors: enforce structured error responses and add regression tests.

## Agent Patterns

### 1. Production Agent with Agent Builder

```python
# Example code for creating a production agent
from vertexai.preview import agents
from vertexai.preview.generative_models import Tool, FunctionDeclaration
import functions_framework

class ProductionAgent:
    # Implementation details...
```

### 2. RAG-Enhanced Agent

```python
# Example code for RAG agent
from vertexai.language_models import TextEmbeddingModel
from vertexai.preview import rag

class RAGAgent:
    # Implementation details...
```

### 3. Multi-Modal Agent

```python
# Example code for multi-modal agent
from vertexai.generative_models import GenerativeModel, Part

class MultiModalAgent:
    # Implementation details...
```

## Deployment Patterns

### 1. Cloud Run Deployment

```yaml
# cloudbuild.yaml
steps:
  # Build container
  - name: 'gcr.io/cloud-builders/docker'
    args: ['build', '-t', 'gcr.io/$PROJECT_ID/vertex-agent:$COMMIT_SHA', '.']
  # Push to Container Registry
  - name: 'gcr.io/cloud-builders/docker'
    args: ['push', 'gcr.io/$PROJECT_ID/vertex-agent:$COMMIT_SHA']
  # Deploy to Cloud Run
  - name: 'gcr.io/google.com/cloudsdktool/cloud-sdk'
    entrypoint: gcloud
    args:
      - 'run'
      - 'deploy'
      - 'vertex-agent'
      - '--image'
      - 'gcr.io/$PROJECT_ID/vertex-agent:$COMMIT_SHA'
      - '--region'
      - 'us-central1'
      - '--platform'
      - 'managed'
      - '--allow-unauthenticated'
      - '--set-env-vars'
      - 'GCP_PROJECT=$PROJECT_ID'
```

### 2. Vertex AI Endpoint Deployment

```python
from google.cloud import aiplatform

def deploy_to_vertex_endpoint():
    # Implementation details...
```

## Evaluation Framework

```python
from vertexai.preview.evaluation import EvalTask

class AgentEvaluator:
    # Implementation details...
```

## Monitoring & Observability

```python
from google.cloud import monitoring_v3
from google.cloud import logging

class AgentMonitor:
    # Implementation details...
```

## Cost Optimization

```python
class CostOptimizedAgent:
    # Implementation details...
```

## Integration with Google Cloud Services

### BigQuery Integration

```python
from google.cloud import bigquery

class BigQueryAgent:
    # Implementation details...
```

### Cloud Storage Integration

```python
from google.cloud import storage

class StorageAgent:
    # Implementation details...
```

## Best Practices

### 1. Security

```python
from google.cloud import secretmanager

class SecureAgent:
    # Implementation details...
```

### 2. Error Handling

```python
from tenacity import retry

class ResilientAgent:
    # Implementation details...
```

## Resources

- [Vertex AI Documentation](https://cloud.google.com/vertex-ai/docs)
- [Gemini API Reference](https://cloud.google.com/vertex-ai/generative-ai/docs/model-reference/gemini)
- [Agent Builder Guide](https://cloud.google.com/generative-ai-app-builder/docs/agent-builder)
- [GitHub: GoogleCloudPlatform/generative-ai](https://github.com/GoogleCloudPlatform/generative-ai)
- [GitHub: GoogleCloudPlatform/agent-starter-pack](https://github.com/GoogleCloudPlatform/agent-starter-pack)

---

**Version:** 1.0.0  
**Last Updated:** October 2025  
**Author:** Jeremy Longshore  
**License:** MIT