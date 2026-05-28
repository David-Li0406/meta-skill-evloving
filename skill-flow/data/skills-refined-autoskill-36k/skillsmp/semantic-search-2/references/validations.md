# Semantic Search - Validations

## Hardcoded Embedding Model

### **Id**
hardcoded-embedding-model
### **Severity**
warning
### **Description**
Embedding model should be configurable
### **Pattern**
  model:\s*["']text-embedding-(?:3-small|ada-002)["'](?!.*config|env|EMBED)
  
### **Message**
Hardcoded embedding model. Use config/env for easier migration.
### **Autofix**


## Missing Dimensions Parameter

### **Id**
missing-dimensions-param
### **Severity**
info
### **Description**
text-embedding-3 models support dimension reduction
### **Pattern**
  text-embedding-3.*(?!.*dimensions)
  
### **Message**
Consider using dimensions parameter to reduce vector size and costs.
### **Autofix**


## Missing Model Version in Metadata

### **Id**
no-model-version-tracking
### **Severity**
warning
### **Description**
Track embedding model version for migrations
### **Pattern**
  metadata.*(?!.*embeddingModel|model_version|embedding_version)
  
### **Message**
Store embedding model version in metadata for future migrations.
### **Autofix**


## Missing Reranking Stage

### **Id**
no-reranking
### **Severity**
info
### **Description**
Consider reranking for precision-critical applications
### **Pattern**
  vector.*search.*return(?!.*rerank|second.*stage)
  
### **Message**
Consider adding Cohere/Jina reranking for better precision.
### **Autofix**


## Vector-Only Search

### **Id**
no-hybrid-search
### **Severity**
warning
### **Description**
Hybrid search handles exact matches better
### **Pattern**
  embed.*query.*results(?!.*keyword|bm25|hybrid|full.*text)
  
### **Message**
Pure vector search misses exact matches. Consider hybrid search.
### **Autofix**


## No Metadata Filtering

### **Id**
no-metadata-filter
### **Severity**
info
### **Description**
Filtering before search improves relevance
### **Pattern**
  query.*topK(?!.*filter|where|must)
  
### **Message**
Consider adding metadata filters to narrow search scope.
### **Autofix**


## Fixed-Size Chunking Without Overlap

### **Id**
fixed-size-chunking
### **Severity**
warning
### **Description**
Fixed chunks break semantic context
### **Pattern**
  slice\(\d+,\s*\d+\)|substring\(\d+,\s*\d+\)|split.*join.*slice
  
### **Message**
Fixed-size chunking breaks sentences. Use semantic chunking.
### **Autofix**


## No Chunk Overlap

### **Id**
no-chunk-overlap
### **Severity**
warning
### **Description**
Overlapping chunks preserve context
### **Pattern**
  chunk.*size(?!.*overlap)
  
### **Message**
Add chunk overlap (10-20%) to preserve context at boundaries.
### **Autofix**


## Very Small Chunk Size

### **Id**
tiny-chunks
### **Severity**
warning
### **Description**
Chunks under 100 tokens lose context
### **Pattern**
  chunk.*size.*[<:].*(?:[1-9]|[1-9]\d)(?!\d)
  
### **Message**
Chunks under 100 tokens may lack sufficient context.
### **Autofix**


## Sequential Embedding Calls

### **Id**
no-batch-embedding
### **Severity**
warning
### **Description**
Batch embeddings to reduce API calls
### **Pattern**
  for.*await.*embed\(|\.map\(.*embed\)
  
### **Message**
Use batch embedding API to reduce calls and costs.
### **Autofix**


## No Query Embedding Cache

### **Id**
no-embedding-cache
### **Severity**
info
### **Description**
Cache query embeddings for repeated searches
### **Pattern**
  async.*search.*embed.*query(?!.*cache)
  
### **Message**
Consider caching query embeddings for common searches.
### **Autofix**


## Full Reindex Without Change Detection

### **Id**
no-change-detection
### **Severity**
warning
### **Description**
Only re-embed changed documents
### **Pattern**
  reindex.*all|embed.*all.*documents(?!.*hash|changed|diff)
  
### **Message**
Use content hashing to avoid re-embedding unchanged docs.
### **Autofix**


## No Rate Limit Handling

### **Id**
no-rate-limit-handling
### **Severity**
warning
### **Description**
Embedding APIs have rate limits
### **Pattern**
  embed\((?!.*retry|limit|queue)
  
### **Message**
Add rate limiting and retry logic for embedding calls.
### **Autofix**


## No Empty Result Handling

### **Id**
no-empty-result-handling
### **Severity**
warning
### **Description**
Handle empty search results gracefully
### **Pattern**
  results\[0\](?!.*\?|length|if)
  
### **Message**
Handle case when search returns no results.
### **Autofix**


## No Dimension Validation

### **Id**
no-dimension-validation
### **Severity**
error
### **Description**
Validate vector dimensions match index
### **Pattern**
  upsert.*vector(?!.*length.*===|dimensions|validate)
  
### **Message**
Validate embedding dimensions match index configuration.
### **Autofix**


## API Key in Code

### **Id**
exposed-api-key
### **Severity**
error
### **Description**
Vector DB API keys should be in environment
### **Pattern**
  apiKey:\s*["'][a-zA-Z0-9_-]{20,}["']
  
### **Message**
API key in code. Use environment variables.
### **Autofix**


## No Query Input Validation

### **Id**
no-input-validation
### **Severity**
warning
### **Description**
Validate and sanitize search queries
### **Pattern**
  search\(.*req\.(?:query|body)(?!.*validate|sanitize|z\.)
  
### **Message**
Validate and sanitize user search queries.
### **Autofix**
