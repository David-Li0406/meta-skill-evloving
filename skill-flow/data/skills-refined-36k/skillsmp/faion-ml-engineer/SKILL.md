---
name: faion-ml-engineer
description: "ML Engineer role: LLM APIs (OpenAI, Claude, Gemini), embeddings, RAG pipelines, fine-tuning, LangChain, LlamaIndex, vector databases (Pinecone, Chroma, Weaviate), prompt engineering, model evaluation, cost optimization, Agentic RAG, AI Agents, MCP, LLM observability. 42 methodologies."
user-invocable: false
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Task, AskUserQuestion, TodoWrite
---

# ML Engineer Domain Skill

**Communication: User's language. Code: English.**

## Purpose

Orchestrates AI/ML engineering activities. Covers LLM APIs, embeddings, RAG systems, fine-tuning, and AI frameworks.

---

## Agents

| Agent | Purpose |
|-------|---------|
| faion-ml-agent | AI/ML implementation and integration |

---

## References

Detailed technical context for each area:

| Reference | Content | Lines |
|-----------|---------|-------|
| [openai-api.md](openai-api.md) | GPT-4, DALL-E, Whisper, Assistants | ~1310 |
| [claude-api.md](claude-api.md) | Claude models, tool use, extended thinking | ~1420 |
| [gemini-api.md](gemini-api.md) | Gemini models, multimodal, grounding | ~1150 |
| [embeddings.md](embeddings.md) | Text embeddings, similarity, chunking | ~900 |
| [finetuning.md](finetuning.md) | Model fine-tuning, datasets, evaluation | ~990 |
| [langchain.md](langchain.md) | Chains, agents, memory, tools | ~1440 |
| [llamaindex.md](llamaindex.md) | Document indexing, query engines | ~1210 |
| [vector-databases.md](vector-databases.md) | Pinecone, Weaviate, Chroma, pgvector | ~1390 |
| [ref-agentic-rag.md](ref-agentic-rag.md) | Agentic RAG, AI Agents, LLM Management, MCP | ~300 |

**Total:** ~10,110 lines of technical reference

---

## Quick Reference

### LLM Provider Selection

| Provider | Best For | Context | Cost |
|----------|----------|---------|------|
| **OpenAI** | General purpose, vision, tools | 128K | $$$ |
| **Claude** | Long context, reasoning, safety | 200K | $$$ |
| **Gemini** | Multimodal, grounding, 2M context | 2M | $$ |
| **Local (Ollama)** | Privacy, no API costs | Varies | Free |

### Model Selection

| Task | Recommended Model |
|------|-------------------|
| Complex reasoning | Claude Opus 4.5, GPT-4o |
| Fast responses | Claude Sonnet 4, GPT-4o-mini |
| Code generation | Claude Sonnet 4, GPT-4o |
| Vision/Images | GPT-4o, Gemini Pro Vision |
| Embeddings | text-embedding-3-large, voyage-3 |
| Fine-tuning | GPT-4o-mini, Claude (coming) |

### Framework Selection

| Framework | Use Case |
|-----------|----------|
| **LangChain** | Complex chains, agents, many integrations |
| **LlamaIndex** | Document indexing, RAG, structured data |
| **Haystack** | Production RAG, enterprise |
| **Vercel AI SDK** | Streaming UI, React integration |

### Vector Database Selection

| Database | Best For |
|----------|----------|
| **Pinecone** | Managed, serverless, enterprise |
| **Weaviate** | Hybrid search, GraphQL |
| **Chroma** | Local dev, lightweight |
| **pgvector** | PostgreSQL integration |
| **Qdrant** | Performance, filtering |

---

## Methodologies (24)

### LLM APIs

| Name | Purpose |
|------|---------|
| prompt-engineering | Effective prompts, few-shot |
| structured-output | JSON mode, function calling |
| streaming (in api refs) | Real-time output |
| cost-optimization | Context management, caching |
| error-handling (in api refs) | Retries, fallbacks |
| rate-limiting (in api refs) | Throttling, queuing |

### Embeddings

| Name | Purpose |
|------|---------|
| chunking-strategies | Size, overlap, semantic |
| embedding-generation | Cosine, dot product, similarity search |
| hybrid-search | Vector + keyword |
| reranking | Cross-encoder, Cohere |

### RAG

| Name | Purpose |
|------|---------|
| rag-pipeline-design | Document processing, parsing, extraction |
| graph-rag-advanced-retrieval | Index design, hierarchical, knowledge graphs |
| query-processing (in rag) | Expansion, routing |
| context-assembly (in rag) | Ranking, filtering |
| response-generation (in rag) | Grounding, citations |
| rag-evaluation | Relevance, faithfulness |

### Fine-tuning

| Name | Purpose |
|------|---------|
| fine-tuning-openai | Dataset preparation, format, quality, size |
| fine-tuning-lora | Training configuration, hyperparameters |
| model-evaluation | Loss, task-specific metrics |
| deployment (in devops) | Model serving, A/B testing |

### Agents

| Name | Purpose |
|------|---------|
| tool-use-function-calling | Function definitions, tool design |
| autonomous-agents | Agent loop, ReAct, plan-and-execute |
| ai-agent-patterns | Memory management, short/long-term |
| multi-agent-systems | Orchestration, coordination |

---

## Workflows

### RAG System Development

```
1. Document ingestion
   - Parse documents
   - Split into chunks
   - Generate embeddings

2. Index creation
   - Store in vector DB
   - Add metadata

3. Query pipeline
   - Embed query
   - Retrieve relevant chunks
   - Rerank results

4. Response generation
   - Assemble context
   - Generate response
   - Add citations
```

### Fine-tuning Pipeline

```
1. Data preparation
   - Collect examples
   - Format for model
   - Split train/eval

2. Training
   - Upload dataset
   - Configure hyperparameters
   - Start job

3. Evaluation
   - Run on eval set
   - Compare to base model
   - Check for regressions

4. Deployment
   - Deploy model
   - Monitor performance
   - Iterate
```

---

## Code Patterns

### OpenAI Chat Completion

```python
from openai import OpenAI

client = OpenAI()

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello!"}
    ],
    temperature=0.7,
    max_tokens=1000
)

print(response.choices[0].message.content)
```

### Claude Messages

```python
import anthropic

client = anthropic.Anthropic()

message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Hello!"}
    ]
)

print(message.content[0].text)
```

### Embeddings + Vector Search

```python
from openai import OpenAI
import chromadb

# Create embeddings
client = OpenAI()
embedding = client.embeddings.create(
    model="text-embedding-3-small",
    input="Search query"
)

# Store and search
chroma = chromadb.Client()
collection = chroma.create_collection("docs")

collection.add(
    embeddings=[embedding.data[0].embedding],
    documents=["Document text"],
    ids=["doc1"]
)

results = collection.query(
    query_embeddings=[query_embedding],
    n_results=5
)
```

### LangChain RAG

```python
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain.chains import RetrievalQA

# Setup
llm = ChatOpenAI(model="gpt-4o")
embeddings = OpenAIEmbeddings()
vectorstore = Chroma(embedding_function=embeddings)

# RAG chain
qa = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=vectorstore.as_retriever(),
    return_source_documents=True
)

result = qa.invoke({"query": "What is RAG?"})
```

---

## Cost Optimization

### Token Usage

| Strategy | Savings |
|----------|---------|
| Prompt caching | 90% on cached |
| Batch API | 50% on batch |
| Smaller models | 80%+ vs large |
| Context pruning | Variable |

### Caching

```python
# OpenAI caching example
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {
            "role": "system",
            "content": long_system_prompt,  # Cached after first call
        },
        {"role": "user", "content": user_query}
    ]
)
```

---

## Evaluation

### RAG Metrics

| Metric | Measures |
|--------|----------|
| **Relevance** | Retrieved docs match query |
| **Faithfulness** | Response grounded in context |
| **Answer correctness** | Response matches ground truth |

### LLM Evaluation

| Method | Use Case |
|--------|----------|
| Human evaluation | Gold standard, expensive |
| LLM-as-judge | Scalable, needs calibration |
| Automated metrics | Fast, limited |

---

## Related Skills

| Skill | Relationship |
|-------|--------------|
| faion-software-developer | Application integration |
| faion-devops-engineer | Model deployment |

---

## Error Handling

| Issue | Action |
|-------|--------|
| Unknown provider | Ask user or check env vars |
| Rate limits | Implement exponential backoff |
| Token limits | Chunk and summarize |
| Context overflow | Use RAG or summarization |

---

*ML Engineer Domain Skill v1.0*
*8 Reference Files | 24 Methodologies*
*Aggregated from: openai-api, claude-api, gemini-api, embeddings, finetuning, langchain, llamaindex, vector-databases*
