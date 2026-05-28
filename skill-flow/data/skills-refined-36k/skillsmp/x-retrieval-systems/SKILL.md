---
name: x-retrieval-systems
description: Use this skill when analyzing how the system narrows down 500 million daily tweets to a candidate pool of ~1,500. This is the "top-of-funnel" engineering that determines what is even eligible to be ranked.
version: 1.0.0
license: MIT
---

# X Retrieval Systems

Expertise in X's multi-stage retrieval architecture, including Earlybird search indexing and Phoenix-based ANN similarity search.

## Context
Retrieval at X is split between **In-Network** (content from people you follow) and **Out-of-Network** (discovery). In-Network retrieval relies on **Earlybird** (Lucene-based search), while Out-of-Network retrieval uses **Phoenix** (Two-Tower embeddings) and **ANN** (Approximate Nearest Neighbor) algorithms like HNSW.

- [Earlybird Search Index](./references/earlybird-search-index.md)
- [ANN & Embedding Retrieval](./references/ann-retrieval.md)

## What it does

* **Decodes In-Network Sourcing:** Explains how Earlybird shards the index into Realtime, Protected, and Archive clusters.
* **Explains Discovery Logic:** Details how Two-Tower models enable "semantic" search for content you don't follow.
* **Analyzes Latency:** Breaks down the single-writer/multi-reader concurrency model that allows for sub-second global retrieval.

## Example Trigger Prompts

* "/find-candidates how Earlybird shards real-time index"
* "/find-candidates retrieving 1,500 candidates from 500M tweets"
* "Role of HNSW in embedding-based discovery"
* "In-Network (Thunder) vs Out-of-Network (Phoenix) retrieval"
* "Trace 'Discovery' request: User Embedding → Candidate Source"
