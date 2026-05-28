# Rag Engineer - Validations

## Fixed Chunk Size

### **Id**
fixed-chunk-size
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - chunk_size\s*=\s*\d{3,4}
  - split_by_tokens\(\d+
  - textwrap\.wrap
### **Message**
Fixed-size chunking may split sentences and context.
### **Fix Action**
Use semantic or sentence-aware chunking
### **Applies To**
  - **/*.py
  - **/*.ts
  - **/*.js

## Chunks Without Overlap

### **Id**
no-overlap
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - overlap\s*=\s*0
  - chunk_overlap\s*=\s*0
  - split(?!.*overlap)
### **Message**
Chunks without overlap may lose context at boundaries.
### **Fix Action**
Add 10-20% overlap between chunks
### **Applies To**
  - **/*.py
  - **/*.ts
  - **/*.js

## Naive Top-K Without Reranking

### **Id**
naive-top-k
### **Severity**
info
### **Type**
regex
### **Pattern**
  - top_k\s*=\s*[1-9](?!.*rerank)
  - \.similarity_search\([^)]*\)(?!.*rerank)
  - limit\s*=\s*\d+(?!.*cross_encoder)
### **Message**
Using top-K without reranking may miss relevant results.
### **Fix Action**
Add cross-encoder reranking for better precision
### **Applies To**
  - **/*.py
  - **/*.ts
  - **/*.js

## No Metadata Filtering

### **Id**
no-metadata-filter
### **Severity**
info
### **Type**
regex
### **Pattern**
  - \.search\(\s*query\s*\)
  - similarity_search\([^,]+\)$
  - vector_search(?!.*filter)
### **Message**
Pure semantic search without metadata filtering.
### **Fix Action**
Add metadata filters for date, source, or category
### **Applies To**
  - **/*.py
  - **/*.ts
  - **/*.js

## Context Stuffing

### **Id**
context-stuffing
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - context\s*=\s*["']\\s*["']\\.join
  - \\n\\.join\(.*chunks\)
  - all_chunks|all_documents
### **Message**
Stuffing all context may exceed window or confuse LLM.
### **Fix Action**
Use relevance threshold or compression
### **Applies To**
  - **/*.py
  - **/*.ts
  - **/*.js

## Hardcoded Embedding Model

### **Id**
hardcoded-embedding
### **Severity**
info
### **Type**
regex
### **Pattern**
  - text-embedding-ada-002
  - all-MiniLM-L6-v2
  - embedding_model\s*=\s*["'][^"']+["']
### **Message**
Hardcoded embedding model - consider making configurable.
### **Fix Action**
Make embedding model configurable for evaluation
### **Applies To**
  - **/*.py
  - **/*.ts
  - **/*.js
### **Excludes**
  - **/config.*
  - **/.env*

## No Similarity Threshold

### **Id**
no-similarity-threshold
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - search\([^)]*\)(?!.*threshold|.*score)
  - retrieve(?!.*min_score)
### **Message**
No minimum similarity threshold - may return irrelevant results.
### **Fix Action**
Add minimum similarity score cutoff
### **Applies To**
  - **/*.py
  - **/*.ts
  - **/*.js

## Synchronous Embedding

### **Id**
sync-embedding
### **Severity**
info
### **Type**
regex
### **Pattern**
  - for.*in.*documents.*embed\(
  - embed_query\([^)]+\)\s*$
### **Message**
Synchronous embedding may be slow for large batches.
### **Fix Action**
Use batch embedding or async for performance
### **Applies To**
  - **/*.py
  - **/*.ts
  - **/*.js

## Missing Retrieval Evaluation

### **Id**
missing-retrieval-eval
### **Severity**
info
### **Type**
regex
### **Pattern**
  - def test_rag|test_retrieval(?!.*recall|.*mrr|.*ndcg)
  - assert.*response(?!.*retrieved)
### **Message**
Testing RAG without separate retrieval evaluation.
### **Fix Action**
Add retrieval-specific metrics (MRR, NDCG, Recall@K)
### **Applies To**
  - **/test*.py
  - **/*.test.ts
  - **/*.spec.ts