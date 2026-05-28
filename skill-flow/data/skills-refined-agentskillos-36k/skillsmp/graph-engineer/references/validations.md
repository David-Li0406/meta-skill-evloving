# Graph Engineer - Validations

## Cypher Query Without Index Hint

### **Id**
cypher-no-index
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - MATCH\\s*\\(\\w+\\)\\s*WHERE
  - MATCH\\s*\\(\\w+:\\w+\\)\\s*WHERE\\s*\\w+\\.\\w+\\s*=
### **Message**
Query may not use index. Consider using indexed property in pattern match.
### **Fix Action**
Move filter to pattern: MATCH (n:Label {prop: $val}) instead of WHERE
### **Applies To**
  - *.py
  - *.cypher
  - **/graph/*.py

## Unbounded Path Traversal

### **Id**
cypher-unbounded-traversal
### **Severity**
error
### **Type**
regex
### **Pattern**
  - \\[:\\w+\\*\\]
  - \\[r\\*\\]
  - -\\[\\*\\]-
### **Message**
Unbounded path traversal (*) is exponential. Add depth limit like *1..5
### **Fix Action**
Change [*] to [*1..5] or appropriate bounded range
### **Applies To**
  - *.py
  - *.cypher

## Potential Cartesian Product in Query

### **Id**
cypher-cartesian-product
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - MATCH\\s*\\([^)]+\\)\\s*\\n\\s*MATCH\\s*\\([^)]+\\)(?!.*WITH)
### **Message**
Multiple MATCH without WITH may create Cartesian product. Use connected patterns.
### **Fix Action**
Connect patterns or use WITH between MATCH clauses
### **Applies To**
  - *.py
  - *.cypher

## Edge Creation Without Temporal Validity

### **Id**
graph-edge-no-temporal
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - CREATE.*\\[r:.*\\{(?!.*valid_from)
  - MERGE.*\\[r:.*\\{(?!.*valid_from)
### **Message**
Edge created without valid_from. Add temporal validity for history tracking.
### **Fix Action**
Add valid_from: datetime() and valid_until: null to edge properties
### **Applies To**
  - *.py
  - *.cypher
  - **/graph/*.py

## Cypher Query String Concatenation

### **Id**
graph-query-not-parameterized
### **Severity**
error
### **Type**
regex
### **Pattern**
  - f".*MATCH.*\\{.*\\}"
  - f'.*MATCH.*\{.*\}'
  - \\.format\\(.*MATCH
### **Message**
String formatting in Cypher query. Use parameters to enable plan caching.
### **Fix Action**
Use query parameters: query($param) instead of f-string
### **Applies To**
  - *.py

## Direct Node Deletion

### **Id**
graph-node-delete
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - DELETE\\s+\\w+\\s*$
  - DETACH DELETE
### **Message**
Deleting nodes loses history. Consider setting deleted_at timestamp instead.
### **Fix Action**
Use soft delete: SET n.deleted_at = datetime() instead of DELETE
### **Applies To**
  - *.py
  - *.cypher

## MERGE Without ON CREATE/ON MATCH

### **Id**
graph-merge-without-on-create
### **Severity**
info
### **Type**
regex
### **Pattern**
  - MERGE\\s*\\([^)]+\\)(?!.*ON\\s*(CREATE|MATCH))
### **Message**
MERGE without ON CREATE/ON MATCH. Consider specifying behavior for each case.
### **Fix Action**
Add ON CREATE SET and ON MATCH SET clauses for clarity
### **Applies To**
  - *.py
  - *.cypher

## Large Embedding in Graph Property

### **Id**
graph-embedding-property
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - embedding:\\s*\\$
  - embedding:\\s*\\[.*\\]
  - \\.embedding\\s*=
### **Message**
Storing embeddings in graph properties is slow. Use external vector store.
### **Fix Action**
Store embedding_id reference, keep vectors in Qdrant/pgvector
### **Applies To**
  - *.py
  - **/graph/*.py

## Missing Index for Frequent Query Pattern

### **Id**
graph-no-index-creation
### **Severity**
info
### **Type**
regex
### **Pattern**
  - WHERE\\s+\\w+\\.user_id\\s*=(?!.*CREATE INDEX)
  - WHERE\\s+\\w+\\.\\w+_id\\s*=(?!.*CREATE INDEX)
### **Message**
Query filters on ID field. Ensure index exists for this property.
### **Fix Action**
CREATE INDEX idx FOR (n:Label) ON (n.property)
### **Applies To**
  - *.py
  - *.cypher

## Causal Edge Without Cycle Detection

### **Id**
graph-causal-no-cycle-check
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - CREATE.*:CAUSES(?!.*cycle|.*acyclic)
  - MERGE.*:CAUSES(?!.*cycle|.*acyclic)
### **Message**
Creating causal edge without cycle check. Causal graphs must be DAGs.
### **Fix Action**
Validate that adding edge doesn't create cycle before insertion
### **Applies To**
  - *.py
  - **/graph/*.py

## Counting All Edges on Node

### **Id**
graph-count-all-edges
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - MATCH.*-\\[r\\]-.*RETURN count\\(r\\)
  - SIZE\\(\\(.*\\)-\\[\\]-
### **Message**
Counting all edges on a node can be slow for god nodes. Consider caching count.
### **Fix Action**
Store edge count as node property, update incrementally
### **Applies To**
  - *.py
  - *.cypher

## OPTIONAL MATCH Without Limit

### **Id**
graph-optional-match-unbounded
### **Severity**
info
### **Type**
regex
### **Pattern**
  - OPTIONAL MATCH(?!.*LIMIT)
### **Message**
OPTIONAL MATCH without LIMIT can return many rows. Consider adding LIMIT.
### **Fix Action**
Add LIMIT or use collect() with slice to bound results
### **Applies To**
  - *.py
  - *.cypher