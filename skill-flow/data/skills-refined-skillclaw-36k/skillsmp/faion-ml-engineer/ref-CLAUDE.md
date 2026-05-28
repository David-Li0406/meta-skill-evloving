# ML Engineer References

## Overview

Technical documentation for AI/ML engineering. Contains API guides, framework documentation, and best practices for LLM integration, embeddings, RAG systems, fine-tuning, and vector databases.

**Total:** 10 files, ~11,000 lines

---

## Files

### LLM APIs

| File | Description | Lines |
|------|-------------|-------|
| [openai-api.md](openai-api.md) | OpenAI API guide: Chat Completions, GPT-4o, Vision, Function Calling, DALL-E, Whisper, TTS, Embeddings, Assistants, Batch API, Realtime, Fine-tuning. Includes authentication, models, parameters, streaming, error handling. | ~1310 |
| [claude-api.md](claude-api.md) | Anthropic Claude API: Messages API, Claude Opus 4.5/Sonnet 4/Haiku 3.5, Tool Use, Vision, Extended Thinking, Computer Use, Batch API, Prompt Caching. Includes authentication, model selection, parameters. | ~1420 |
| [gemini-api.md](gemini-api.md) | Google Gemini API: Gemini 2.0 Flash, 1.5 Pro (2M context), multimodal (text/images/video/audio), function calling, code execution, grounding with Google Search, context caching, safety settings. | ~1150 |

### Embeddings and Vector Search

| File | Description | Lines |
|------|-------------|-------|
| [embeddings.md](embeddings.md) | Text embeddings guide: model comparison (OpenAI, Cohere, local models), batch processing, Matryoshka embeddings (dimension reduction), chunking strategies, similarity metrics, cost optimization. | ~900 |
| [vector-databases.md](vector-databases.md) | Vector database guide: Qdrant (recommended), Weaviate, pgvector, Chroma, Pinecone, Milvus. Covers installation, collection management, CRUD operations, filtering, indexing (HNSW), performance tuning. | ~1390 |

### RAG and Frameworks

| File | Description | Lines |
|------|-------------|-------|
| [rag.md](rag.md) | RAG pipeline reference: BUILD mode (document ingestion, chunking, indexing), QUERY mode (semantic search with citations), EVALUATE mode (retrieval quality metrics: MRR, recall, faithfulness). | ~500 |
| [langchain.md](langchain.md) | LangChain/LangGraph guide: chain patterns (sequential, router, parallel), LangGraph agents, memory systems, tool integration, structured output, multi-agent orchestration, LangSmith tracing. | ~1440 |
| [llamaindex.md](llamaindex.md) | LlamaIndex RAG framework: data connectors, node parsers, index types (VectorStore, Keyword, KnowledgeGraph), query engines, retrievers, response synthesizers, agents, evaluation. | ~1210 |

### Fine-tuning and Best Practices

| File | Description | Lines |
|------|-------------|-------|
| [finetuning.md](finetuning.md) | LLM fine-tuning guide: techniques (Full FT, LoRA, QLoRA, DoRA), frameworks (LLaMA-Factory, Unsloth, Axolotl), dataset formats, alignment (SFT, RLHF, DPO), evaluation, deployment (GGUF, vLLM). | ~990 |
| [best-practices-2026.md](best-practices-2026.md) | Current AI/ML best practices: Agentic RAG (RAG 2.0 with multi-hop retrieval), AI Agent patterns (CoT, ReAct, Plan-and-Execute), MCP (Model Context Protocol), LLM observability. | ~300 |

---

## Usage Guide

### For LLM Integration

1. Choose provider: `openai-api.md`, `claude-api.md`, or `gemini-api.md`
2. Review authentication and model selection
3. Implement streaming and error handling

### For RAG Systems

1. Start with `rag.md` for pipeline overview
2. Choose framework: `langchain.md` or `llamaindex.md`
3. Select vector DB from `vector-databases.md`
4. Configure embeddings from `embeddings.md`

### For Fine-tuning

1. Review `finetuning.md` for technique selection
2. Choose LoRA/QLoRA for most use cases
3. Prepare dataset in appropriate format

### For Agents

1. Review patterns in `best-practices-2026.md`
2. Implement with `langchain.md` (LangGraph)
3. Use Agentic RAG for complex retrieval tasks
