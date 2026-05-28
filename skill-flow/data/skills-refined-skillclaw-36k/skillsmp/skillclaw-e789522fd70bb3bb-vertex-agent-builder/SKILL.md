---
name: vertex-agent-builder
description: Use this skill when you need to build and deploy production-ready generative AI agents on Google Cloud's Vertex AI platform, leveraging Gemini models and advanced capabilities like RAG and function calling.
---

# Vertex AI Agent Builder Skill

## Overview

This skill provides production-ready scaffolding and deployment for generative AI agents using Google Cloud's Vertex AI platform. It integrates Gemini models and supports multi-modal capabilities, retrieval-augmented generation (RAG), and function calling.

## Prerequisites

- Google Cloud project with Vertex AI API enabled
- Permissions to deploy/operate Agent Engine runtimes
- If using RAG: a document source (GCS/BigQuery/Firestore/etc) and an embeddings/index strategy
- Secrets handled via environment variables or Secret Manager

## Instructions

1. **Clarify the Agent’s Job**: Define user intents, inputs/outputs, latency, and cost constraints.
2. **Choose Model and Region**: Select the appropriate Gemini model and region, and define tool/function interfaces (schemas, error contracts).
3. **Implement Retrieval (if needed)**: Set up chunking, embeddings, indexing, and a “citation-first” response format.
4. **Add Evaluation**: Create golden prompts, perform offline checks, and conduct a minimal online smoke test.
5. **Deploy**: Provide the deployment command/config and verify endpoints and permissions.
6. **Add Operations**: Implement logs/metrics, alerting, quota/cost guardrails, and rollback steps.

## Output

- A Vertex AI agent scaffold (code/config) with clear extension points
- A retrieval plan (when applicable) and a validation/evaluation checklist
- Optional: deployment commands and post-deploy health checks

## Error Handling

- **Quota/Region Issues**: Detect the failing service/quota and propose a scoped fix.
- **Auth Failures**: Identify the principal and missing role; prefer least-privilege remediation.
- **Retrieval Failures**: Validate indexing/embedding dimensions and add fallback behavior.
- **Tool/Function Errors**: Enforce structured error responses and add regression tests.

## Installation

```bash
# Install Google Cloud SDK
curl https://sdk.cloud.google.com | bash
exec -l $SHELL
gcloud init

# Install Python SDK
pip install google-cloud-aiplatform>=1.38.0
pip install vertexai>=1.46.0
pip install google-generativeai>=0.3.2

# Clone source repositories
git clone https://github.com/GoogleCloudPlatform/generative-ai.git
git clone https://github.com/GoogleCloudPlatform/agent-starter-pack.git
git clone https://github.com/GoogleCloudPlatform/vertex-ai-samples.git

# Install this plugin
/plugin install jeremy-vertex-ai@jeremylongshore
```

## Quick Start

### Create Your First Vertex AI Agent

```python
import vertexai
from vertexai.generative_models import GenerativeModel

# Initialize Vertex AI
vertexai.init(project="your-project-id", location="us-central1")

# Create Gemini model
model = GenerativeModel(
    "gemini-1.5-pro-002",
    system_instruction="""You are a helpful AI assistant that can:
    - Search the web for information
    - Analyze documents and images
    - Execute Python code
    - Call external APIs
    """
)
```