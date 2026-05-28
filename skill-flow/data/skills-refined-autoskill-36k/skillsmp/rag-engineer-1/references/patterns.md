# RAG Engineer

## Patterns


---
  #### **Name**
Semantic Chunking
  #### **Description**
Chunk by meaning, not arbitrary token counts
  #### **When**
Processing documents with natural sections
  #### **Implementation**
    - Use sentence boundaries, not token limits
    - Detect topic shifts with embedding similarity
    - Preserve document structure (headers, paragraphs)
    - Include overlap for context continuity
    - Add metadata for filtering
    

---
  #### **Name**
Hierarchical Retrieval
  #### **Description**
Multi-level retrieval for better precision
  #### **When**
Large document collections with varied granularity
  #### **Implementation**
    - Index at multiple chunk sizes (paragraph, section, document)
    - First pass: coarse retrieval for candidates
    - Second pass: fine-grained retrieval for precision
    - Use parent-child relationships for context
    

---
  #### **Name**
Hybrid Search
  #### **Description**
Combine semantic and keyword search
  #### **When**
Queries may be keyword-heavy or semantic
  #### **Implementation**
    - BM25/TF-IDF for keyword matching
    - Vector similarity for semantic matching
    - Reciprocal Rank Fusion for combining scores
    - Weight tuning based on query type
    

---
  #### **Name**
Query Expansion
  #### **Description**
Expand queries to improve recall
  #### **When**
User queries are short or ambiguous
  #### **Implementation**
    - Use LLM to generate query variations
    - Add synonyms and related terms
    - Hypothetical Document Embedding (HyDE)
    - Multi-query retrieval with deduplication
    

---
  #### **Name**
Contextual Compression
  #### **Description**
Compress retrieved context to fit window
  #### **When**
Retrieved chunks exceed context limits
  #### **Implementation**
    - Extract relevant sentences only
    - Use LLM to summarize chunks
    - Remove redundant information
    - Prioritize by relevance score
    

---
  #### **Name**
Metadata Filtering
  #### **Description**
Pre-filter by metadata before semantic search
  #### **When**
Documents have structured metadata
  #### **Implementation**
    - Filter by date, source, category first
    - Reduce search space before vector similarity
    - Combine metadata filters with semantic scores
    - Index metadata for fast filtering
    

## Anti-Patterns


---
  #### **Name**
Fixed Chunk Size
  #### **Description**
Using fixed token counts regardless of content
  #### **Problem**
Splits sentences, breaks context, loses meaning
  #### **Solution**
Use semantic or structure-aware chunking

---
  #### **Name**
Embedding Everything
  #### **Description**
Embedding raw documents without preprocessing
  #### **Problem**
Noise, boilerplate, and irrelevant content pollute retrieval
  #### **Solution**
Clean, preprocess, and filter before embedding

---
  #### **Name**
Ignoring Evaluation
  #### **Description**
Not measuring retrieval quality separately
  #### **Problem**
Can't distinguish retrieval failures from generation failures
  #### **Solution**
Use retrieval-specific metrics (MRR, NDCG, Recall@K)

---
  #### **Name**
One Embedding Model
  #### **Description**
Using same embedding for all content types
  #### **Problem**
Different content needs different embeddings
  #### **Solution**
Evaluate embeddings per domain, consider fine-tuning

---
  #### **Name**
Naive Top-K
  #### **Description**
Just taking top K results without reranking
  #### **Problem**
First-stage retrieval is optimized for recall, not precision
  #### **Solution**
Use cross-encoder reranking for final selection

---
  #### **Name**
Context Stuffing
  #### **Description**
Cramming maximum context into prompt
  #### **Problem**
More context can confuse LLM, increases cost
  #### **Solution**
Quality over quantity - use relevance thresholds