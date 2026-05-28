# Decision Maker - Validations

## Technology Choice Without Comment

### **Id**
undocumented-technology-choice
### **Severity**
info
### **Type**
regex
### **Pattern**
  - new\s+(?:Redis|Postgres|Mongo|Kafka|RabbitMQ|Elasticsearch)\s*\(
  - createClient\s*\(\s*\{[^}]*\}\s*\)
  - (?:prisma|drizzle|mongoose|sequelize)\.\$connect
### **Message**
Technology initialization without documenting why this choice was made. Consider adding ADR or inline comment.
### **Fix Action**
Add comment explaining why this technology was chosen over alternatives, or link to ADR.
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx

## Configuration Value Without Explanation

### **Id**
magic-configuration
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - maxRetries:\s*\d+
  - timeout:\s*\d{4,}
  - poolSize:\s*\d+
  - batchSize:\s*\d+
  - limit:\s*\d{3,}
### **Message**
Configuration value without explaining why this specific value was chosen.
### **Fix Action**
Add comment explaining the rationale: 'maxRetries: 3 // Balances reliability vs latency, based on P99 response times'
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx
  - **/*.yaml
  - **/*.yml
  - **/*.json

## Deferred Decision Marker

### **Id**
todo-decision-needed
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - //\s*TODO.*decide
  - //\s*TODO.*choice
  - //\s*FIXME.*which
  - //\s*TBD
  - #\s*TODO.*decide
### **Message**
Decision explicitly deferred. Track in decision log with deadline.
### **Fix Action**
Either make the decision now, or document: what, deadline, default-if-not-decided.
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx
  - **/*.py

## Temporary Solution Missing Deadline

### **Id**
temporary-solution-permanent
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - //\s*(?:temporary|temp|hack)(?!.*(?:until|by|deadline|date))
  - //\s*(?:workaround|stopgap)(?!.*(?:until|by|deadline|date))
  - #\s*(?:temporary|temp|hack)(?!.*(?:until|by|deadline|date))
### **Message**
Temporary solution without expiration date. Will become permanent.
### **Fix Action**
Add deadline: '// TEMPORARY until 2024-Q2 - replace with proper caching layer'
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx
  - **/*.py

## Hardcoded Value That Should Be Configurable

### **Id**
hardcoded-decision
### **Severity**
info
### **Type**
regex
### **Pattern**
  - const\s+(?:MAX|MIN|DEFAULT|LIMIT)_[A-Z_]+\s*=\s*\d+
  - (?:maxConnections|poolSize|cacheSize)\s*=\s*\d+
### **Message**
Hardcoded limit that may need adjustment. Document why this value was chosen.
### **Fix Action**
Add comment with rationale or make configurable: 'const MAX_CONNECTIONS = 10; // Based on DB connection limits'
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx

## Assumption Without Documentation

### **Id**
assumption-not-documented
### **Severity**
info
### **Type**
regex
### **Pattern**
  - //\s*(?:assume|assuming)
  - //\s*(?:should be|must be|always)
  - #\s*(?:assume|assuming)
### **Message**
Assumption should be validated or documented as known constraint.
### **Fix Action**
Either add runtime validation or document in design doc/ADR why assumption is safe.
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx
  - **/*.py

## Commented-Out Alternative Approach

### **Id**
commented-alternative
### **Severity**
info
### **Type**
regex
### **Pattern**
  - //\s*Alternative:
  - //\s*Could also
  - //\s*Option \d:
  - //\s*or we could
### **Message**
Alternative approach documented in code. Consider moving to ADR.
### **Fix Action**
If the alternative was considered, document in ADR. If obsolete, remove.
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx

## Breaking Change Without Migration Note

### **Id**
breaking-change-undocumented
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - //\s*BREAKING
  - //\s*breaking change
  - @deprecated(?!.*migration|alternative)
### **Message**
Breaking change mentioned but migration path not documented.
### **Fix Action**
Document: what's breaking, who's affected, migration steps, timeline.
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx

## Revisit Marker Without Trigger

### **Id**
revisit-marker
### **Severity**
info
### **Type**
regex
### **Pattern**
  - //\s*TODO.*revisit(?!.*(?:if|when|at))
  - //\s*(?:review|reconsider)\s+later
  - #\s*TODO.*revisit(?!.*(?:if|when|at))
### **Message**
Revisit marker without specifying trigger condition.
### **Fix Action**
Add trigger: '// REVISIT when user count > 10k or latency > 500ms'
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx
  - **/*.py

## Vendor-Specific Code Without Abstraction

### **Id**
vendor-lock-in
### **Severity**
info
### **Type**
regex
### **Pattern**
  - import.*from\s+['"]@aws-sdk
  - import.*from\s+['"]@azure/
  - import.*from\s+['"]@google-cloud/
  - import.*from\s+['"]firebase
### **Message**
Direct vendor SDK import. Document if vendor lock-in is an accepted trade-off.
### **Fix Action**
Either abstract behind interface for portability, or document in ADR why lock-in is acceptable.
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx

## Scale Assumption Not Documented

### **Id**
scale-assumption
### **Severity**
info
### **Type**
regex
### **Pattern**
  - //\s*(?:should|will)\s+(?:scale|handle)
  - //\s*(?:works for|up to)\s+\d+[kKmM]?
  - //\s*(?:sufficient|enough)\s+for
### **Message**
Scale assumption stated but not validated or documented with limits.
### **Fix Action**
Document expected limits and what happens when exceeded.
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx

## Framework Decision Discussed in Code

### **Id**
framework-choice-inline
### **Severity**
info
### **Type**
regex
### **Pattern**
  - //\s*(?:chose|using|picked)\s+(?:React|Vue|Next|Svelte|Angular)
  - //\s*(?:instead of|over|rather than)\s+(?:React|Vue|Next|Svelte|Angular)
### **Message**
Framework decision discussed in code comments. Should be in ADR.
### **Fix Action**
Move rationale to docs/adr/NNNN-framework-choice.md for better discoverability.
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx

## Team Consensus Referenced

### **Id**
consensus-comment
### **Severity**
info
### **Type**
regex
### **Pattern**
  - //\s*(?:team|we)\s+(?:decided|agreed)
  - //\s*(?:per|as per)\s+(?:discussion|meeting)
### **Message**
Team decision referenced but not formally documented.
### **Fix Action**
Document in ADR with date, participants, and rationale so future team knows context.
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
  - **/*.jsx