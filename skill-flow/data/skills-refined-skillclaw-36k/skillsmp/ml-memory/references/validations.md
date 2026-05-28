# Ml Memory - Validations

## Memory Without Temporal Level

### **Id**
memory-no-temporal-level
### **Severity**
error
### **Type**
regex
### **Pattern**
  - class Memory.*:(?!.*temporal_level)
  - Memory\\((?!.*level|.*temporal)
### **Message**
Memory created without temporal level. Always assign a hierarchy level.
### **Fix Action**
Add temporal_level field to Memory class and set on creation
### **Applies To**
  - **/memory/**/*.py
  - **/*memory*.py

## Memory Without Temporal Validity

### **Id**
memory-no-valid-from
### **Severity**
error
### **Type**
regex
### **Pattern**
  - class.*Fact.*:(?!.*valid_from)
  - class.*Memory.*:(?!.*created_at|.*valid_from)
### **Message**
Memory/Fact without temporal validity. Track when facts became true.
### **Fix Action**
Add valid_from and valid_until fields for temporal validity
### **Applies To**
  - **/memory/**/*.py
  - **/*memory*.py

## Entity Created Without Resolution Check

### **Id**
entity-no-resolution
### **Severity**
error
### **Type**
regex
### **Pattern**
  - Entity\\(.*name.*=|create.*entity(?!.*resolv)
  - new.*Entity(?!.*resolution|.*dedupe|.*match)
### **Message**
Entity created without resolution check. May create duplicates.
### **Fix Action**
Check for existing entity match before creating new one
### **Applies To**
  - **/entity/**/*.py
  - **/memory/**/*.py

## Salience Only Increases Never Decreases

### **Id**
salience-only-increase
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - salience.*\\+.*=(?!.*-)
  - salience.*=.*salience.*\\+(?!.*outcome|.*decay)
### **Message**
Salience only increases. Implement decay or outcome-based decrease.
### **Fix Action**
Add decay mechanism and negative outcome handling
### **Applies To**
  - **/memory/**/*.py
  - **/*salience*.py

## Memory System Without Decay

### **Id**
memory-no-decay
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - class.*Memory.*System.*:(?!.*decay|.*forget)
### **Message**
Memory system without decay/forgetting. Will grow unbounded.
### **Fix Action**
Implement decay based on time and access patterns
### **Applies To**
  - **/memory/**/*.py

## Consolidation Without Locking

### **Id**
consolidation-no-lock
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - async.*def.*consolidat.*:(?!.*lock|.*mutex)
  - consolidat.*(?!.*lock|.*for_update|.*atomic)
### **Message**
Consolidation without locking. Concurrent runs may corrupt data.
### **Fix Action**
Add distributed lock or database-level locking
### **Applies To**
  - **/consolidation/**/*.py
  - **/*consolidat*.py

## Hardcoded Memory Thresholds

### **Id**
memory-hardcoded-thresholds
### **Severity**
info
### **Type**
regex
### **Pattern**
  - promotion_threshold.*=.*\\d+
  - decay.*=.*0\\.\\d+
  - MAX_SALIENCE.*=.*1\\.0
### **Message**
Hardcoded memory thresholds. Consider configuration or learning.
### **Fix Action**
Move thresholds to configuration or make them learnable
### **Applies To**
  - **/memory/**/*.py

## Memory Retrieval Without Outcome Tracking

### **Id**
memory-no-outcome-tracking
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - retrieve.*memor.*(?!.*trace|.*log|.*track)
  - search.*memor.*return(?!.*trace)
### **Message**
Memory retrieval without outcome tracking. Can't learn from usage.
### **Fix Action**
Implement decision trace to track retrieval and outcome
### **Applies To**
  - **/memory/**/*.py
  - **/retrieval/**/*.py

## Memory Deletion Without Reference Cleanup

### **Id**
forget-no-cascade
### **Severity**
error
### **Type**
regex
### **Pattern**
  - delete.*memory(?!.*cascade|.*reference|.*edge)
  - remove.*memory(?!.*graph|.*relationship)
### **Message**
Memory deletion without reference cleanup. May leave dangling refs.
### **Fix Action**
Clean up graph edges and references before deletion
### **Applies To**
  - **/memory/**/*.py

## Embedding Without Model Version

### **Id**
embedding-no-model-version
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - embedding.*:.*List\\[float\\](?!.*model)
  - embed\\(.*\\)(?!.*model=)
### **Message**
Embedding stored without model version. Migration will be hard.
### **Fix Action**
Store embedding_model alongside embedding vector
### **Applies To**
  - **/memory/**/*.py
  - **/embedding/**/*.py

## Memory Query Without User Scope

### **Id**
memory-no-user-scope
### **Severity**
error
### **Type**
regex
### **Pattern**
  - SELECT.*FROM.*memor(?!.*user_id|.*WHERE.*user)
  - get.*memor.*(?!.*user_id)
### **Message**
Memory query without user scope. May leak cross-user data.
### **Fix Action**
Always filter memories by user_id
### **Applies To**
  - **/memory/**/*.py
  - **/db/**/*.py

## Memory Update Without Contradiction Check

### **Id**
contradiction-no-handling
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - update.*fact(?!.*contradict|.*conflict)
  - store.*fact(?!.*existing|.*check)
### **Message**
Fact stored without contradiction check. May have conflicting facts.
### **Fix Action**
Check for existing contradictory facts and resolve
### **Applies To**
  - **/memory/**/*.py
  - **/fact/**/*.py