# Rag Implementation - Validations

## Chunks Without Overlap

### **Id**
rag-no-overlap
### **Severity**
warning
### **Type**
regex
### **Pattern**
split|chunk
### **Negative Pattern**
overlap|Overlap|sliding
### **Message**
Chunking without overlap. Context at boundaries may be lost.
### **Fix Action**
Add 10-20% overlap between chunks
### **Applies To**
  - *.ts
  - *.js
  - *.py

## Fixed Chunk Size

### **Id**
rag-fixed-chunk-size
### **Severity**
info
### **Type**
regex
### **Pattern**
chunk.*size\s*=\s*\d{3,}|split.*\d{3,}
### **Negative Pattern**
semantic|recursive|paragraph
### **Message**
Fixed-size chunking may break context. Consider semantic chunking.
### **Fix Action**
Use semantic or recursive chunking that respects document structure
### **Applies To**
  - *.ts
  - *.js
  - *.py

## No Reranking

### **Id**
rag-no-reranking
### **Severity**
info
### **Type**
regex
### **Pattern**
search|retrieve|query
### **Negative Pattern**
rerank|Rerank|score|sort.*relevance
### **Message**
Retrieval without reranking. Top-k may not be most relevant.
### **Fix Action**
Add reranking step to improve retrieval precision
### **Applies To**
  - *.ts
  - *.js
  - *.py

## Single Retrieval Strategy

### **Id**
rag-single-retrieval
### **Severity**
info
### **Type**
regex
### **Pattern**
vectorStore\.search|similarity_search
### **Negative Pattern**
hybrid|bm25|keyword|sparse
### **Message**
Only using vector search. Hybrid search often performs better.
### **Fix Action**
Combine dense (vector) and sparse (keyword) retrieval
### **Applies To**
  - *.ts
  - *.js
  - *.py