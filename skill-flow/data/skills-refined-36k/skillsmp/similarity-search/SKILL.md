---
name: similarity-search
description: Retrieves 10 similar historical cases from AgentDB vector store for RAG-based diagnosis support
license: MIT
compatibility: opencode
metadata:
  audience: developers
  workflow: clinical-pipeline
---

## What I do

I perform RAG (Retrieval-Augmented Generation) by querying the AgentDB vector store for similar historical cases. I retrieve the 10 most relevant past cases to inform risk assessment and recommendations.

## When to use me

Use this when:

- Lesion detection is complete and you need historical context
- You need similar cases for differential diagnosis
- You're building a risk profile based on historical patterns

## Key Concepts

- **AgentDB**: Local vector database for case storage
- **Vector Store**: Embedding-based similarity search
- **RAG Retrieval**: Find top-k similar historical cases
- **similarity_searched**: State flag after search complete

## Source Files

- `services/agentDB.ts`: Vector database operations
- `types.ts`: ReasoningPattern interface

## Code Patterns

- Use AgentDB for vector similarity search
- Retrieve diverse historical cases (demographic diversity)
- Return cases sorted by similarity score

## Operational Constraints

- Must return diverse cases across demographics
- Vector store initialized via `npm run agentdb:init`
- Maximum 10 cases retrieved for performance
