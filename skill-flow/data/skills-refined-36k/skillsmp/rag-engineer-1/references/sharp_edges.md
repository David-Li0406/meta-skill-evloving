# Rag Engineer - Sharp Edges

## Naive Chunking

### **Id**
naive-chunking
### **Summary**
Fixed-size chunking breaks sentences and context
### **Severity**
high
### **Situation**
Using fixed token/character limits for chunking
### **Why**
  Fixed-size chunks split mid-sentence, mid-paragraph, or mid-idea.
  The resulting embeddings represent incomplete thoughts, leading to
  poor retrieval quality. Users search for concepts but get fragments.
  
### **Solution**
  Use semantic chunking that respects document structure:
  - Split on sentence/paragraph boundaries
  - Use embedding similarity to detect topic shifts
  - Include overlap for context continuity
  - Preserve headers and document structure as metadata
  
### **Symptoms**
  - Retrieved chunks feel incomplete or cut off
  - Answer quality varies wildly
  - High recall but low precision
### **Detection Pattern**
  #### **Language**
generic
  #### **Pattern**
chunk_size.*=.*\d{3,4}|split.*\[:.*\]|textwrap

## No Metadata Filtering

### **Id**
no-metadata-filtering
### **Summary**
Pure semantic search without metadata pre-filtering
### **Severity**
medium
### **Situation**
Only using vector similarity, ignoring metadata
### **Why**
  Semantic search finds semantically similar content, but not necessarily
  relevant content. Without metadata filtering, you return old docs when
  user wants recent, wrong categories, or inapplicable content.
  
### **Solution**
  Implement hybrid filtering:
  - Pre-filter by metadata (date, source, category) before vector search
  - Post-filter results by relevance criteria
  - Include metadata in the retrieval API
  - Allow users to specify filters
  
### **Symptoms**
  - Returns outdated information
  - Mixes content from wrong sources
  - Users can't scope their searches
### **Detection Pattern**
  #### **Language**
generic
  #### **Pattern**
similarity_search\(query\)|search\(embedding\)|query.*without.*filter

## Embedding Mismatch

### **Id**
embedding-mismatch
### **Summary**
Using same embedding model for different content types
### **Severity**
medium
### **Situation**
One embedding model for code, docs, and structured data
### **Why**
  Embedding models are trained on specific content types. Using a text
  embedding model for code, or a general model for domain-specific
  content, produces poor similarity matches.
  
### **Solution**
  Evaluate embeddings per content type:
  - Use code-specific embeddings for code (e.g., CodeBERT)
  - Consider domain-specific or fine-tuned embeddings
  - Benchmark retrieval quality before choosing
  - Separate indices for different content types if needed
  
### **Symptoms**
  - Code search returns irrelevant results
  - Domain terms not matched properly
  - Similar concepts not clustered
### **Detection Pattern**
  #### **Language**
generic
  #### **Pattern**
all-MiniLM.*code|text-embedding.*code|single.*embedding.*model

## No Reranking

### **Id**
no-reranking
### **Summary**
Using first-stage retrieval results directly
### **Severity**
medium
### **Situation**
Taking top-K from vector search without reranking
### **Why**
  First-stage retrieval (vector search) optimizes for recall, not precision.
  The top results by embedding similarity may not be the most relevant
  for the specific query. Cross-encoder reranking dramatically improves
  precision for the final results.
  
### **Solution**
  Add reranking step:
  - Retrieve larger candidate set (e.g., top 20-50)
  - Rerank with cross-encoder (query-document pairs)
  - Return reranked top-K (e.g., top 5)
  - Cache reranker for performance
  
### **Symptoms**
  - Clearly relevant docs not in top results
  - Results order seems arbitrary
  - Adding more results helps quality
### **Detection Pattern**
  #### **Language**
generic
  #### **Pattern**
top_k.*=.*[1-9](?!.*rerank)|similarity_search.*limit.*\d+$

## Context Stuffing

### **Id**
context-stuffing
### **Summary**
Cramming maximum context into LLM prompt
### **Severity**
medium
### **Situation**
Using all retrieved context regardless of relevance
### **Why**
  More context isn't always better. Irrelevant context confuses the LLM,
  increases latency and cost, and can cause the model to ignore the
  most relevant information. Models have attention limits.
  
### **Solution**
  Use relevance thresholds:
  - Set minimum similarity score cutoff
  - Limit context to truly relevant chunks
  - Summarize or compress if needed
  - Order context by relevance
  
### **Symptoms**
  - Answers drift with more context
  - LLM ignores key information
  - High token costs
### **Detection Pattern**
  #### **Language**
generic
  #### **Pattern**
context.*=.*"\s*"\.join|retrieved.*join|all.*chunks

## No Retrieval Evaluation

### **Id**
no-retrieval-evaluation
### **Summary**
Not measuring retrieval quality separately from generation
### **Severity**
high
### **Situation**
Only evaluating end-to-end RAG quality
### **Why**
  If answers are wrong, you can't tell if retrieval failed or generation
  failed. This makes debugging impossible and leads to wrong fixes
  (tuning prompts when retrieval is the problem).
  
### **Solution**
  Separate retrieval evaluation:
  - Create retrieval test set with relevant docs labeled
  - Measure MRR, NDCG, Recall@K for retrieval
  - Evaluate generation only on correct retrievals
  - Track metrics over time
  
### **Symptoms**
  - Can't diagnose poor RAG performance
  - Prompt changes don't help
  - Random quality variations
### **Detection Pattern**
  #### **Language**
generic
  #### **Pattern**
evaluate.*rag|test.*answer|assert.*response

## Stale Embeddings

### **Id**
stale-embeddings
### **Summary**
Not updating embeddings when source documents change
### **Severity**
medium
### **Situation**
Embeddings generated once, never refreshed
### **Why**
  Documents change but embeddings don't. Users retrieve outdated content
  or, worse, content that no longer exists. This erodes trust in the
  system.
  
### **Solution**
  Implement embedding refresh:
  - Track document versions/hashes
  - Re-embed on document change
  - Handle deleted documents
  - Consider TTL for embeddings
  
### **Symptoms**
  - Returns outdated information
  - References deleted content
  - Inconsistent with source
### **Detection Pattern**
  #### **Language**
generic
  #### **Pattern**
embed_once|created_at(?!.*updated)|static.*embeddings

## Ignoring Query Type

### **Id**
ignoring-query-type
### **Summary**
Same retrieval strategy for all query types
### **Severity**
medium
### **Situation**
Using pure semantic search for keyword-heavy queries
### **Why**
  Some queries are keyword-oriented (looking for specific terms) while
  others are semantic (looking for concepts). Pure semantic search fails
  on exact matches; pure keyword search fails on paraphrases.
  
### **Solution**
  Implement hybrid search:
  - BM25/TF-IDF for keyword matching
  - Vector similarity for semantic matching
  - Reciprocal Rank Fusion to combine
  - Tune weights based on query patterns
  
### **Symptoms**
  - Exact term searches miss results
  - Concept searches too literal
  - Users frustrated with both
### **Detection Pattern**
  #### **Language**
generic
  #### **Pattern**
similarity_search\(|vector_search\((?!.*bm25|.*keyword)