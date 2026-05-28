---
name: AI Architecture Patterns
description: Enterprise AI design patterns for production systems - RAG, Multi-Agent, AI Gateway, LLMOps, and more
version: 1.0.0
category: technical
command: /ai-architecture-patterns
triggers: ["ai pattern", "architecture pattern", "rag pattern", "agent pattern", "ai gateway"]
type: reference
---

# AI Architecture Patterns Skill

## Purpose

Provide expert guidance on selecting and implementing enterprise AI architecture patterns for production systems. This skill contains battle-tested patterns from real-world deployments and the AI Architect Academy.

## When to Use

- Designing new AI systems
- Evaluating architecture options
- Selecting patterns for specific use cases
- Understanding tradeoffs between approaches
- Getting implementation guidance

## Core Patterns Library

### 1. AI Gateway Pattern

**Problem**: Multiple AI services with inconsistent interfaces, no centralized security, and limited observability create management complexity and security risks.

**Solution**: Deploy a centralized AI gateway that provides unified authentication, rate limiting, request/response logging, and model routing for all AI services.

**Key Components**:
- API Gateway (Kong, AWS API Gateway, OCI API Gateway)
- Authentication Service (OAuth2, API Keys)
- Rate Limiter (Redis-based)
- Request Logger (OpenTelemetry)
- Model Router

**When to Use**:
- Multiple AI providers in your stack
- Need centralized security controls
- Want unified logging and monitoring
- Cost allocation across teams

**When NOT to Use**:
- Single AI provider with simple use case
- Ultra-low latency requirements (<10ms)
- Early prototyping

---

### 2. RAG Production Pattern

**Problem**: LLMs hallucinate and lack access to enterprise-specific knowledge, making them unreliable for business-critical applications.

**Solution**: Implement a RAG pipeline with document ingestion, chunking, embedding, vector storage, retrieval, and augmented generation with source citations.

**Key Components**:
- Document Ingestion Pipeline
- Text Chunking Service (semantic, fixed, hybrid)
- Embedding Model (OpenAI, Cohere, Local)
- Vector Database (Pinecone, Weaviate, pgvector)
- Retrieval Service with Reranking
- LLM with RAG prompt template

**When to Use**:
- Customer support knowledge base
- Internal document Q&A
- Legal/compliance document analysis
- Technical documentation assistants

**When NOT to Use**:
- General creative writing
- Real-time frequently changing data
- Very small document corpus (<100 docs)

**Implementation Tips**:
- Start with fixed-size chunks (512-1024 tokens)
- Add metadata extraction for filtering
- Implement hybrid search (keyword + semantic)
- Use reranking for improved precision

---

### 3. Multi-Agent Orchestration Pattern

**Problem**: Complex tasks require multiple specialized capabilities that exceed what a single LLM prompt can handle reliably.

**Solution**: Decompose complex workflows into specialized agents with an orchestrator that coordinates task distribution, handoffs, and result aggregation.

**Key Components**:
- Orchestrator Agent (workflow coordinator)
- Specialized Worker Agents (domain experts)
- Task Queue (for async processing)
- State Management (context preservation)
- Handoff Protocol (agent-to-agent communication)
- Result Aggregator

**When to Use**:
- Complex workflows with 5+ distinct steps
- Tasks requiring different expertise
- Autonomous systems
- Workflows with branching logic

**When NOT to Use**:
- Simple single-step tasks
- When cost is primary constraint
- High-volume, low-complexity operations

**Frameworks**:
- LangGraph (graph-based orchestration)
- Claude Agent SDK
- AutoGen / CrewAI

---

### 4. MCP Server Architecture

**Problem**: N agents x M tools = N*M integrations. Each AI agent needs custom code to integrate with each tool.

**Solution**: Implement MCP (Model Context Protocol) servers that provide standardized interfaces for tools, resources, and prompts.

**Key Components**:
- MCP Server (Node.js or Python)
- Tool Definitions (JSON Schema)
- Resource Providers
- Prompt Templates
- Transport Layer (stdio, SSE)

**When to Use**:
- Building tools for multiple AI agents
- Creating reusable integrations
- Claude Code environments
- Enterprise tool standardization

**Implementation**:
```typescript
import { Server } from '@modelcontextprotocol/sdk/server';

const server = new Server({
  name: 'my-mcp-server',
  version: '1.0.0'
});

server.tool('search', {
  description: 'Search documents',
  inputSchema: {
    type: 'object',
    properties: {
      query: { type: 'string' }
    }
  },
  handler: async ({ query }) => {
    // Implementation
  }
});
```

---

### 5. LLMOps Pipeline Pattern

**Problem**: LLM applications lack mature DevOps practices, leading to unpredictable quality and difficult rollbacks.

**Solution**: Implement prompt versioning, automated evaluation, staged deployments, and continuous monitoring.

**Key Components**:
- Prompt Version Control (Git, Promptfoo)
- Evaluation Dataset
- Automated Eval Pipeline
- Deployment Orchestrator
- Monitoring Dashboard
- Rollback Mechanism

**When to Use**:
- Production LLM applications
- Teams with multiple prompt engineers
- Regulated industries
- High-stakes AI applications

**Evaluation Metrics**:
- Accuracy (vs golden answers)
- Latency (p50, p95, p99)
- Cost per request
- User satisfaction scores

---

### 6. Vector Database Selection Framework

**Problem**: Many vector database options with different tradeoffs. Wrong choice leads to expensive migrations.

**Solution**: Structured decision framework evaluating scale, features, operations, and cost.

**Selection Matrix**:

| Scale | Recommendation |
|-------|----------------|
| <1M vectors | pgvector (simple), Chroma (prototyping) |
| 1-100M vectors | Weaviate, Qdrant (self-hosted) |
| 100M+ vectors | Pinecone, Milvus (managed) |

**Key Considerations**:
- Hybrid search support
- Metadata filtering
- Multi-tenancy
- Backup/restore
- Managed vs self-hosted

---

### 7. AI Center of Excellence Framework

**Problem**: Scattered AI initiatives across organization lead to duplicated effort, inconsistent quality, and security gaps.

**Solution**: Establish centralized governance with standardized patterns, reusable components, and shared infrastructure.

**Key Components**:
- Pattern Library (this skill!)
- Governance Framework
- Shared Infrastructure
- Training Program
- Review Board
- Metrics Dashboard

**Governance Areas**:
- Model selection criteria
- Security standards
- Cost controls
- Ethical guidelines
- Incident response

---

### 8. Security & Governance Pattern

**Problem**: AI introduces new security vectors: prompt injection, data leakage, model manipulation.

**Solution**: Implement AI-specific security controls including guardrails, PII handling, and audit logging.

**Key Controls**:
- Input Guardrails (prompt injection detection)
- Output Guardrails (content filtering)
- PII Detection & Redaction
- Audit Logging
- Access Control
- Compliance Reporting

**Guardrails Implementation**:
```python
from guardrails import Guard

guard = Guard.from_pydantic(output_class=SafeResponse)

response = guard(
    llm.invoke,
    prompt=user_input,
    on_fail="reask"
)
```

---

## Pattern Selection Decision Tree

```
START: What type of AI system?
│
├── Document/Knowledge Q&A
│   └── → RAG Production Pattern
│       ├── Need multiple models? → + AI Gateway
│       └── Sensitive data? → + Security & Governance
│
├── Autonomous Agents
│   └── → Multi-Agent Orchestration
│       ├── Many tools? → + MCP Servers
│       └── Production deployment? → + LLMOps
│
├── Enterprise AI Platform
│   └── → AI Gateway + AI CoE Framework
│       ├── Cost concerns? → + Cost Optimization
│       └── Compliance? → + Security & Governance
│
└── Content Generation
    └── → AI Gateway + LLMOps
        └── Quality critical? → + Evaluation Pipeline
```

## Pattern Combinations Matrix

| Use Case | Primary | Secondary | Tertiary |
|----------|---------|-----------|----------|
| Customer Support Bot | RAG | AI Gateway | Security |
| Code Assistant | Multi-Agent | MCP Servers | LLMOps |
| Document Intelligence | RAG | Vector DB | AI Gateway |
| Enterprise AI Platform | AI Gateway | AI CoE | Security |
| Research Assistant | RAG | Multi-Agent | LLMOps |

## Cloud Provider Mapping

### AWS
- AI Gateway: API Gateway + Lambda
- RAG: Bedrock + OpenSearch
- Vector DB: OpenSearch, Aurora pgvector

### GCP
- AI Gateway: Cloud Endpoints + Cloud Functions
- RAG: Vertex AI + Matching Engine
- Vector DB: Matching Engine, AlloyDB

### Azure
- AI Gateway: API Management + Functions
- RAG: Azure OpenAI + AI Search
- Vector DB: AI Search, Cosmos DB

### OCI
- AI Gateway: API Gateway + Functions
- RAG: OCI GenAI + OpenSearch
- Vector DB: OpenSearch, PostgreSQL

## Resources

- **GitHub**: https://github.com/frankxai/ai-architect-academy
- **Patterns Library**: /01-design-patterns
- **Learning Paths**: /02-learning-paths
- **Templates**: /AI CoE Templates

## Related Skills

- `mcp-architecture` - MCP server development
- `claude-sdk` - Agent development with Claude
- `langgraph-patterns` - Graph-based agent workflows
- `oci-services-expert` - Oracle Cloud guidance

---

*Part of the AI Architect Academy by FrankX.AI*
