# Agent Memory Systems - Validations

## In-Memory Store in Production Code

### **Id**
in-memory-store-production
### **Severity**
error
### **Description**
In-memory stores lose data on restart
### **Pattern**
  (MemorySaver|InMemoryStore|chromadb\.Client\(\))
  
### **Anti Pattern**
  (test|spec|mock|dev|development)
  
### **Message**
In-memory store detected. Use persistent storage (Postgres, Qdrant, Pinecone) for production.
### **Autofix**


## Vector Upsert Without Metadata

### **Id**
no-metadata-on-upsert
### **Severity**
warning
### **Description**
Vectors should have metadata for filtering
### **Pattern**
  (upsert|insert|add)\s*\([^)]*vector
  
### **Anti Pattern**
  metadata|user_id|type|timestamp
  
### **Message**
Vector upsert without metadata. Add user_id, type, timestamp for proper filtering.
### **Autofix**


## Query Without User Filtering

### **Id**
no-user-isolation
### **Severity**
error
### **Description**
Queries should filter by user to prevent data leakage
### **Pattern**
  (query|search)\s*\([^)]*vector
  
### **Anti Pattern**
  filter.*user_id|where.*user
  
### **Message**
Vector query without user filtering. Always filter by user_id to prevent data leakage.
### **Autofix**


## Hardcoded Chunk Size Without Justification

### **Id**
hardcoded-chunk-size
### **Severity**
info
### **Description**
Chunk size should be tested and justified
### **Pattern**
  chunk_size\s*=\s*\d{3,4}
  
### **Message**
Hardcoded chunk size. Test different sizes for your content type and measure retrieval accuracy.
### **Autofix**


## Chunking Without Overlap

### **Id**
no-chunk-overlap
### **Severity**
warning
### **Description**
Chunk overlap prevents boundary issues
### **Pattern**
  (RecursiveCharacterTextSplitter|TextSplitter)
  
### **Anti Pattern**
  overlap|chunk_overlap
  
### **Message**
Text splitting without overlap. Add chunk_overlap (10-20%) to prevent boundary issues.
### **Autofix**


## Semantic Search Without Filters

### **Id**
semantic-only-retrieval
### **Severity**
warning
### **Description**
Pure semantic search often returns irrelevant results
### **Pattern**
  (query|search)\s*\(\s*vector
  
### **Anti Pattern**
  filter|where|metadata
  
### **Message**
Pure semantic search. Add metadata filters (user, type, time) for better relevance.
### **Autofix**


## Retrieval Without Result Limit

### **Id**
no-retrieval-limit
### **Severity**
warning
### **Description**
Unbounded retrieval can overflow context
### **Pattern**
  (query|search|retrieve)
  
### **Anti Pattern**
  (limit|top_k|k=|max_results)
  
### **Message**
Retrieval without limit. Set top_k to prevent context overflow.
### **Autofix**


## Embeddings Without Model Version Tracking

### **Id**
no-model-versioning
### **Severity**
warning
### **Description**
Track embedding model to handle migrations
### **Pattern**
  (embed|embedding).*upsert
  
### **Anti Pattern**
  (model|version|embedding_model).*metadata
  
### **Message**
Store embedding model version in metadata to handle model migrations.
### **Autofix**


## Different Models for Document and Query Embedding

### **Id**
different-embed-query-model
### **Severity**
error
### **Description**
Documents and queries must use same embedding model
### **Pattern**
  # Manual check - ensure same model for index and query
  
### **Message**
Ensure same embedding model for indexing and querying.
### **Autofix**
