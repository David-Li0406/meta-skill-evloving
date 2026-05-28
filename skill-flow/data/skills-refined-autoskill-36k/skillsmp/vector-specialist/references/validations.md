# Vector Specialist - Validations

## Vector Search Without Reranking

### **Id**
vector-search-no-rerank
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - return.*search\\(.*\\)(?!.*rerank)
  - \\.search\\([^)]+\\)\\s*$
### **Message**
Vector search without reranking. Consider adding cross-encoder reranking for quality.
### **Fix Action**
Add reranking step before returning results
### **Applies To**
  - *.py
  - **/retrieval/*.py

## Embedding Call Without Caching

### **Id**
embedding-no-cache
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - await.*embed\\((?!.*cache)
  - openai.*embed(?!.*cache)
### **Message**
Embedding without caching. Same content may be re-embedded, wasting API costs.
### **Fix Action**
Add caching layer with content hash as key
### **Applies To**
  - *.py
  - **/embeddings/*.py

## Single Embedding Calls in Loop

### **Id**
embedding-no-batch
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - for.*in.*:\\s*\\n.*await.*embed\\(
  - for.*:\\s*embed\\(
### **Message**
Embedding one at a time in loop. Batch for efficiency and cost savings.
### **Fix Action**
Collect texts and use batch embedding API
### **Applies To**
  - *.py

## Vector-Only Retrieval Without Hybrid

### **Id**
vector-only-retrieval
### **Severity**
info
### **Type**
regex
### **Pattern**
  - async def search[^:]*:[\\s\\S]*?vector.*search(?!.*bm25|.*keyword|.*hybrid)
### **Message**
Vector-only retrieval. Consider hybrid (vector + BM25) for better recall.
### **Fix Action**
Combine vector search with keyword/BM25 search using RRF
### **Applies To**
  - *.py
  - **/retrieval/*.py

## Large Document Chunk Size

### **Id**
large-chunk-size
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - chunk_size.*(?:1000|1500|2000)
  - max_tokens.*(?:1000|1500|2000)
### **Message**
Large chunk size (>1000) dilutes specific information. Use 256-512 tokens.
### **Fix Action**
Reduce chunk size to 256-512 tokens with 10-20% overlap
### **Applies To**
  - *.py
  - **/chunking/*.py

## Hardcoded Embedding Model Name

### **Id**
hardcoded-embedding-model
### **Severity**
info
### **Type**
regex
### **Pattern**
  - model.*=.*['"]text-embedding
  - model.*=.*['"]ada
### **Message**
Hardcoded embedding model. Use config/env variable for easier upgrades.
### **Fix Action**
Move model name to configuration: EMBEDDING_MODEL = os.getenv(...)
### **Applies To**
  - *.py

## Missing Embedding Dimension Validation

### **Id**
no-embedding-dimension-check
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - def.*embed[^:]*:[\\s\\S]*?return(?!.*len|.*dimension|.*shape)
### **Message**
No dimension validation on embeddings. Model mismatch could cause silent failures.
### **Fix Action**
Validate embedding dimension matches expected value
### **Applies To**
  - *.py
  - **/embeddings/*.py

## Quantization Enabled Without Recall Testing

### **Id**
quantization-no-recall-test
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - ScalarQuantization|BinaryQuantization(?!.*recall|.*measure|.*test)
### **Message**
Quantization enabled without recall measurement. Measure recall before/after.
### **Fix Action**
Measure recall@k before and after enabling quantization
### **Applies To**
  - *.py
  - **/vector_db/*.py

## Qdrant Search With Payload Filter But No Index

### **Id**
qdrant-no-payload-index
### **Severity**
info
### **Type**
regex
### **Pattern**
  - Filter.*FieldCondition(?!.*create_payload_index)
### **Message**
Filtering on payload field. Consider creating payload index for performance.
### **Fix Action**
Create payload index for frequently filtered fields
### **Applies To**
  - *.py
  - **/qdrant/*.py

## pgvector Table Without Vector Index

### **Id**
pgvector-no-index
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - CREATE TABLE.*vector\\([\\s\\S]*?(?!CREATE INDEX.*USING)
### **Message**
pgvector table without index. Queries will be slow O(n) scans.
### **Fix Action**
CREATE INDEX USING ivfflat or hnsw on vector column
### **Applies To**
  - *.sql
  - **/migrations/*.py

## Uniform Cache TTL for Embeddings

### **Id**
uniform-cache-ttl
### **Severity**
info
### **Type**
regex
### **Pattern**
  - setex.*(?:3600|86400)\\)
  - expire.*(?:3600|86400)\\)
### **Message**
Uniform cache TTL can cause thundering herd. Add jitter.
### **Fix Action**
Add random jitter (±10%) to TTL to spread cache expiry
### **Applies To**
  - *.py
  - **/cache/*.py

## Embedding Call in Request Handler

### **Id**
embedding-in-request-handler
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - @app\\.(?:get|post)[\\s\\S]*?await.*embed\\(
  - async def.*handler[\\s\\S]*?embed\\(
### **Message**
Embedding in request handler adds latency. Consider pre-computing or async.
### **Fix Action**
Pre-compute embeddings or move to background task
### **Applies To**
  - *.py
  - **/api/*.py