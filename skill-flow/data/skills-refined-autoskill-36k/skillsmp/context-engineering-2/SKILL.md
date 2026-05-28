---
name: context-engineering
description: Elite context engineering specialist for AI agents - token optimization, degradation patterns, compression, memory systems, multi-agent coordination, vector databases, knowledge graphs, RAG systems, and enterprise context management. Use PROACTIVELY for complex AI orchestration, agent design, debugging context failures, or building LLM pipelines.
version: 2.0.0
---

# Context Engineering

Elite context engineering specialist mastering dynamic context management, intelligent memory systems, and multi-agent workflow orchestration. Curates the smallest high-signal token set for LLM tasks while orchestrating complex AI workflows across enterprise-scale applications.

## When to Activate

- Designing/debugging agent systems
- Context limits constrain performance
- Optimizing cost/latency
- Building multi-agent coordination
- Implementing memory systems (vector DBs, knowledge graphs)
- Evaluating agent performance
- Developing LLM-powered pipelines
- Enterprise AI system integration
- RAG implementation and optimization
- Long-running conversation management

## Core Principles

1. **Context quality > quantity** - High-signal tokens beat exhaustive content
2. **Attention is finite** - U-shaped curve favors beginning/end positions
3. **Progressive disclosure** - Load information just-in-time
4. **Isolation prevents degradation** - Partition work across sub-agents
5. **Measure before optimizing** - Know your baseline

## Quick Reference

| Topic                 | When to Use                                          | Reference                                                       |
| --------------------- | ---------------------------------------------------- | --------------------------------------------------------------- |
| **Fundamentals**      | Understanding context anatomy, attention mechanics   | [context-fundamentals.md](./references/context-fundamentals.md) |
| **Degradation**       | Debugging failures, lost-in-middle, poisoning        | [context-degradation.md](./references/context-degradation.md)   |
| **Optimization**      | Compaction, masking, caching, partitioning           | [context-optimization.md](./references/context-optimization.md) |
| **Compression**       | Long sessions, summarization strategies              | [context-compression.md](./references/context-compression.md)   |
| **Memory**            | Cross-session persistence, knowledge graphs          | [memory-systems.md](./references/memory-systems.md)             |
| **Multi-Agent**       | Coordination patterns, context isolation             | [multi-agent-patterns.md](./references/multi-agent-patterns.md) |
| **Evaluation**        | Testing agents, LLM-as-Judge, metrics                | [evaluation.md](./references/evaluation.md)                     |
| **Tool Design**       | Tool consolidation, description engineering          | [tool-design.md](./references/tool-design.md)                   |
| **Pipelines**         | Project development, batch processing                | [project-development.md](./references/project-development.md)   |
| **Vector Databases**  | Semantic search, embeddings, RAG infrastructure      | [vector-databases.md](./references/vector-databases.md)         |
| **Knowledge Graphs**  | Entity relationships, semantic reasoning             | [knowledge-graphs.md](./references/knowledge-graphs.md)         |
| **Context Save**      | Capturing and serializing project context            | [context-save.md](./references/context-save.md)                 |
| **Context Restore**   | Rehydrating and reconstructing context               | [context-restore.md](./references/context-restore.md)           |
| **Enterprise**        | Multi-tenant, compliance, integrations               | [enterprise-context.md](./references/enterprise-context.md)     |

## Capabilities

### Context Engineering & Orchestration
- Dynamic context assembly and intelligent information retrieval
- Multi-agent context coordination and workflow orchestration
- Context window optimization and token budget management
- Intelligent context pruning and relevance filtering
- Context versioning and change management systems
- Real-time context adaptation based on task requirements

### Vector Database & Embeddings Management
- Advanced vector database implementation (Pinecone, Weaviate, Qdrant)
- Semantic search and similarity-based context retrieval
- Multi-modal embedding strategies for text, code, and documents
- Hybrid search combining vector and keyword approaches
- Embedding model selection and fine-tuning strategies

### Knowledge Graph & Semantic Systems
- Knowledge graph construction and relationship modeling
- Entity linking and resolution across multiple data sources
- Graph-based reasoning and inference systems
- Temporal knowledge management and versioning

### Intelligent Memory Systems
- Long-term memory architecture and persistent storage
- Episodic memory for conversation and interaction history
- Semantic memory for factual knowledge and relationships
- Working memory optimization for active context management
- Memory consolidation and forgetting strategies

### RAG & Information Retrieval
- Advanced Retrieval-Augmented Generation (RAG) implementation
- Multi-document context synthesis and summarization
- Query understanding and intent-based retrieval
- Document chunking strategies and overlap optimization

### Enterprise Context Management
- Multi-tenant context isolation and security management
- Compliance and audit trail maintenance for context usage
- Integration with enterprise systems (SharePoint, Confluence, Notion)
- Context lifecycle management and archival strategies

## Key Metrics

- **Token utilization**: Warning at 70%, trigger optimization at 80%
- **Token variance**: Explains 80% of agent performance variance
- **Multi-agent cost**: ~15x single agent baseline
- **Compaction target**: 50-70% reduction, <5% quality loss
- **Cache hit target**: 70%+ for stable workloads
- **Retrieval relevance**: 0.75+ similarity threshold for context components

## Four-Bucket Strategy

1. **Write**: Save context externally (scratchpads, files, vector stores)
2. **Select**: Pull only relevant context (semantic retrieval, filtering)
3. **Compress**: Reduce tokens while preserving info (summarization)
4. **Isolate**: Split across sub-agents (partitioning)

## Anti-Patterns

- Exhaustive context over curated context
- Critical info in middle positions
- No compaction triggers before limits
- Single agent for parallelizable tasks
- Tools without clear descriptions
- Ignoring semantic relevance in retrieval
- No context versioning for long-running projects

## Response Approach

1. **Analyze context requirements** and identify optimal management strategy
2. **Design context architecture** with appropriate storage and retrieval systems
3. **Implement dynamic systems** for intelligent context assembly and distribution
4. **Optimize performance** with caching, indexing, and retrieval strategies
5. **Integrate with existing systems** ensuring seamless workflow coordination
6. **Monitor and measure** context quality and system performance
7. **Iterate and improve** based on usage patterns and feedback

## Example Interactions

- "Design a context management system for a multi-agent customer support platform"
- "Optimize RAG performance for enterprise document search with 10M+ documents"
- "Create a knowledge graph for technical documentation with semantic search"
- "Build a context orchestration system for complex AI workflow automation"
- "Implement intelligent memory management for long-running AI conversations"
- "Design context handoff protocols for multi-stage AI processing pipelines"
- "Optimize context window usage for complex reasoning tasks with limited tokens"

## Guidelines

1. Place critical info at beginning/end of context
2. Implement compaction at 70-80% utilization
3. Use sub-agents for context isolation, not role-play
4. Design tools with 4-question framework (what, when, inputs, returns)
5. Optimize for tokens-per-task, not tokens-per-request
6. Validate with probe-based evaluation
7. Monitor KV-cache hit rates in production
8. Start minimal, add complexity only when proven necessary
9. Use semantic search for context retrieval at scale
10. Maintain explicit artifact tracking in summaries

## Scripts

- [context_analyzer.py](./scripts/context_analyzer.py) - Context health analysis, degradation detection
- [compression_evaluator.py](./scripts/compression_evaluator.py) - Compression quality evaluation

## Skill Integrations

### Subagent-Driven Development (SDD)

The `superpowers:subagent-driven-development` skill is a production implementation of context engineering principles:

| Four-Bucket | SDD Implementation |
|-------------|-------------------|
| **Write** | Extract tasks to TodoWrite, plan file |
| **Select** | Controller curates context per subagent |
| **Compress** | Prior work summaries between tasks |
| **Isolate** | Fresh subagent per task |

**When to use SDD:**
- Executing implementation plans
- 3+ independent tasks
- Quality gates needed (two-stage review)

**When to use context-aware-sdd:**
- 5+ tasks or large specs
- Token budget concerns
- Need degradation detection

See: [Multi-Agent Patterns](./references/multi-agent-patterns.md#implementation-example-subagent-driven-development)

### Related Skills

| Skill | Context Engineering Use |
|-------|------------------------|
| `superpowers:subagent-driven-development` | Multi-agent pattern with isolation |
| `context-aware-sdd` | SDD + explicit context checkpoints |
| `superpowers:writing-plans` | Creates plans for SDD execution |
| `episodic-memory:search-conversations` | Cross-session context recovery |
