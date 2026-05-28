---
name: supabase
description: Expert guidance on Supabase/PostgreSQL implementation for RAG, including pgvector semantic search and full-text search.
---

# Supabase & PostgreSQL Expert Skill

This skill provides patterns for implementing RAG logic with Supabase and the pgvector extension.

## 📂 Storage Pattern (Postgres)

- **Tables**:
  - `documents`: Stores source document text and global metadata.
  - `chunks`: Stores text fragments, `embedding` (vector), and a foreign key `document_id` (UUID).
- **Relationships**: Ensure a foreign key relationship with `ON DELETE CASCADE` from `chunks` to `documents` for clean deletions.

## 🔍 Search Patterns

- **Semantic Search (pgvector)**:

  - Assumes a stored procedure `match_chunks` exists in the database.
  - Parameters: `query_embedding` (vector), `match_threshold` (float), `match_count` (int).
  - Use `self.client.rpc("match_chunks", rpc_params).execute()`.

- **Text Search (WFTS)**:
  - Use Postgres full-text search capabilities.
  - Pattern: `self.client.table("chunks").select("...").filter("content", "wfts", query).range(0, limit - 1).execute()`.

## 🛠️ Code Standards

- **Client**: Use the `supabase` Python library (`create_client`).
- **UUIDs**: PostgreSQL IDs are typically UUIDs (strings in Python).
- **Error Handling**: Verify that the `match_chunks` RPC is properly defined in the database schema before use.
- **Config**: The `threshold` for semantic matches is usually configurable in the repository's `__init__`.
