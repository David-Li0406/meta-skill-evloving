---
name: vertex-agent-builder
description: Build and deploy production-ready generative AI agents using Vertex AI, Gemini models, and Google Cloud infrastructure with RAG, function calling, and multi-modal capabilities.
---

# Vertex AI Agent Builder

This skill provides production-ready scaffolding and deployment for generative AI agents using Google Cloud's Vertex AI platform. It includes capabilities for retrieval-augmented generation (RAG), function calling, and multi-modal processing.

## Overview

- Produces an agent scaffold aligned with Vertex AI Agent Engine deployment patterns.
- Helps choose models/regions, design tool/function interfaces, and wire up retrieval.
- Includes an evaluation + smoke-test checklist to ensure deployments don’t regress.

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
6. Add ops: logs/metrics, alerting, quota/cost guardrails, and rollback steps.

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
from vertexai.preview import agents
from vertexai.preview.generative_models import Tool, FunctionDeclaration
import functions_framework

class ProductionAgent:
    def __init__(self, project_id: str, location: str = "us-central1"):
        self.project_id = project_id
        self.location = location
        self.agent = agents.Agent.create(
            project=project_id,
            location=location,
            display_name="production-agent",
            description="Production-ready agent with tools and RAG",
            model="gemini-1.5-pro-002",
            tools=self._create_tools(),
            system_instruction=self._get_system_instruction()
        )

    def _create_tools(self):
        return [
            Tool(function_declarations=[
                FunctionDeclaration(
                    name="search_knowledge_base",
                    description="Search internal knowledge base",
                    parameters={"type": "object", "properties": {"query": {"type": "string"}, "top_k": {"type": "integer", "default": 5}}}
                ),
                FunctionDeclaration(
                    name="execute_sql",
                    description="Execute SQL query on BigQuery",
                    parameters={"type": "object", "properties": {"query": {"type": "string"}, "dataset": {"type": "string"}}}
                ),
                FunctionDeclaration(
                    name="send_email",
                    description="Send email notification",
                    parameters={"type": "object", "properties": {"to": {"type": "string"}, "subject": {"type": "string"}, "body": {"type": "string"}}}
                )
            ])
        ]

    def _get_system_instruction(self):
        return """You are a production AI agent that helps users with:
        1. Information retrieval from knowledge bases
        2. Data analysis using BigQuery
        3. Automated communications
        Always verify user intent before executing critical operations.
        Provide clear explanations of what you're doing and why.
        """

    async def process_request(self, user_input: str):
        session = self.agent.start_session()
        response = await session.send_message(user_input)
        if response.function_calls:
            for func_call in response.function_calls:
                result = await self._execute_function(func_call.name, func_call.args)
                response = await session.send_message(content=None, function_responses=[{"name": func_call.name, "response": result}])
        return response.text

    async def _execute_function(self, name: str, args: dict):
        if name == "search_knowledge_base":
            return await self._search_kb(args["query"], args.get("top_k", 5))
        elif name == "execute_sql":
            return await self._execute_bigquery(args["query"], args["dataset"])
        elif name == "send_email":
            return await self._send_email(args["to"], args["subject"], args["body"])
```

### 2. RAG-Enhanced Agent

```python
from vertexai.language_models import TextEmbeddingModel
from vertexai.preview import rag

class RAGAgent:
    def __init__(self, project_id: str, corpus_name: str):
        self.project_id = project_id
        self.corpus = rag.create_corpus(display_name=corpus_name, description="Knowledge base for RAG")
        self.embedding_model = TextEmbeddingModel.from_pretrained("text-embedding-004")
        self.model = GenerativeModel("gemini-1.5-pro-002")

    async def import_documents(self, gcs_uris: list):
        import_job = rag.import_files(corpus_name=self.corpus.name, gcs_uris=gcs_uris, chunk_size=512, chunk_overlap=100)
        import_job.wait()
        return import_job

    async def query_with_rag(self, query: str, similarity_top_k: int = 5):
        retrieval_response = rag.retrieval_query(rag_resources=[rag.RagResource(rag_corpus=self.corpus.name, similarity_top_k=similarity_top_k)], query=query)
        context = "\n\n".join([f"Source: {chunk.source}\nContent: {chunk.text}" for chunk in retrieval_response.contexts])
        prompt = f"""Based on the following context, answer the question.
        Context:
        {context}
        Question: {query}
        Answer:"""
        response = self.model.generate_content(prompt, generation_config={"temperature": 0.2, "max_output_tokens": 1024})
        return {"answer": response.text, "sources": [chunk.source for chunk in retrieval_response.contexts], "confidence": retrieval_response.attribution_score}
```

### 3. Multi-Modal Agent

```python
from vertexai.generative_models import GenerativeModel, Part

class MultiModalAgent:
    def __init__(self):
        self.model = GenerativeModel("gemini-1.5-flash-002")

    async def analyze_image(self, image_path: str, prompt: str):
        image = Part.from_uri(uri=f"gs://your-bucket/{image_path}", mime_type="image/jpeg")
        response = self.model.generate_content([prompt, image])
        return response.text

    async def analyze_video(self, video_path: str, prompt: str):
        video = Part.from_uri(uri=f"gs://your-bucket/{video_path}", mime_type="video/mp4")
        response = self.model.generate_content([prompt, video], generation_config={"temperature": 0.4, "max_output_tokens": 2048})
        return response.text

    async def analyze_document(self, pdf_path: str):
        document = Part.from_uri(uri=f"gs://your-bucket/{pdf_path}", mime_type="application/pdf")
        prompt = """Extract all key information from this document:
        1. Main topics covered
        2. Key findings or conclusions
        3. Important data or statistics
        4. Actionable recommendations
        """
        response = self.model.generate_content([prompt, document])
        return response.text
```

## Deployment Patterns

### 1. Cloud Run Deployment

```yaml
# cloudbuild.yaml
steps:
  - name: 'gcr.io/cloud-builders/docker'
    args: ['build', '-t', 'gcr.io/$PROJECT_ID/vertex-agent:$COMMIT_SHA', '.']
  - name: 'gcr.io/cloud-builders/docker'
    args: ['push', 'gcr.io/$PROJECT_ID/vertex-agent:$COMMIT_SHA']
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
    aiplatform.init(project="your-project", location="us-central1")
    model = aiplatform.Model.upload(display_name="vertex-agent-model", artifact_uri="gs://your-bucket/model", serving_container_image_uri="us-docker.pkg.dev/vertex-ai/prediction/sklearn-cpu.1-3:latest")
    endpoint = aiplatform.Endpoint.create(display_name="vertex-agent-endpoint")
    endpoint.deploy(model=model, deployed_model_display_name="vertex-agent-v1", machine_type="n1-standard-4", min_replica_count=1, max_replica_count=5, accelerator_type="NVIDIA_TESLA_T4", accelerator_count=1)
    return endpoint
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