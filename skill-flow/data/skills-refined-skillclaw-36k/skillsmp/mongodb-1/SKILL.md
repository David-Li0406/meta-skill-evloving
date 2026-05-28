---
name: mongodb
description: Expert guidance on MongoDB implementation for RAG, including aggregation pipelines and search patterns.
---

# MongoDB Expert Skill

This skill provides patterns for implementing RAG logic with MongoDB Atlas.

## 📂 Storage Pattern

- **Two-Collection Pattern**:
  - `documents`: Stores source document text and global metadata.
  - `chunks`: Stores text fragments, embeddings (list[float]), and a foreign key (`document_id`) to the source document.
- **Score Meta**: Use `{"$meta": "vectorSearchScore"}` for semantic scores and `{"$meta": "searchScore"}` for text scores.

## 🔍 Search Patterns

- **Semantic Search**: Use `$vectorSearch` aggregation. Default `numCandidates`: 100.
- **Text Search**: Use `$search` (Atlas Search) in `chunks` collection.
- **Hybrid Search**: Currently implemented via manual **Reciprocal Rank Fusion (RRF)** in `RAGService` by merging results from semantic and text search.
- **Joins**: Always use `$lookup` to fetch document metadata (`title`, `source`) when returning search results.

## 🛠️ Code Standards

- **Async First**: Use `motor` (AsyncIOMotorClient) for all database operations.
- **List Embeddings**: Embeddings MUST be stored and queried as Python lists of floats (e.g., 1536 dims for OpenAI).
- **ID Handling**: Convert string IDs to `bson.ObjectId` where necessary.
- **Graceful Failure**: Handle missing search indexes (code 291) with clear error messages.
