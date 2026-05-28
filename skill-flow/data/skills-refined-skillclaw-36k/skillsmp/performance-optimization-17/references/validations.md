# Performance Optimization - Validations

## Heavy library import

### **Id**
heavy-import
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - from ["']moment["']
  - from ["']lodash["']$
  - import _ from ["']lodash["']
  - require\(["']moment["']\)
### **Message**
Heavy library import - consider lighter alternatives
### **Fix Action**
Use date-fns instead of moment, lodash-es with specific imports
### **Applies To**
  - *.js
  - *.ts
  - *.jsx
  - *.tsx

## Large component without lazy loading

### **Id**
no-lazy-loading
### **Severity**
info
### **Type**
regex
### **Pattern**
  - import.*from ["']\./.*Chart["']
  - import.*from ["']\./.*Editor["']
  - import.*from ["']\./.*Modal["']
  - import.*from ["']@monaco-editor
### **Message**
Consider lazy loading heavy components
### **Fix Action**
Use dynamic(() => import('./Component')) or lazy()
### **Applies To**
  - *.jsx
  - *.tsx

## Inline object/array in JSX props

### **Id**
inline-object-props
### **Severity**
info
### **Type**
regex
### **Pattern**
  - style=\\{\\{
  - className=\\{\\[.*\\]\\.join
### **Message**
Inline objects/arrays cause re-renders
### **Fix Action**
Move to useMemo or define outside component
### **Applies To**
  - *.jsx
  - *.tsx

## Anonymous function in render

### **Id**
anonymous-callback-props
### **Severity**
info
### **Type**
regex
### **Pattern**
  - onClick=\\{\\(\\)\\s*=>
  - onChange=\\{\\(e\\)\\s*=>
  - onSubmit=\\{\\(\\)\\s*=>
### **Message**
Anonymous callbacks may cause re-renders in memoized children
### **Fix Action**
Use useCallback if passed to memoized components
### **Applies To**
  - *.jsx
  - *.tsx

## Potentially heavy synchronous operation

### **Id**
sync-heavy-operation
### **Severity**
info
### **Type**
regex
### **Pattern**
  - \\.sort\\(.*\\)\\.filter\\(
  - \\.filter\\(.*\\)\\.map\\(.*\\)\\.reduce\\(
  - JSON\\.parse\\(.*JSON\\.stringify
### **Message**
Chain of array operations may be expensive
### **Fix Action**
Consider single-pass loop or memoization
### **Applies To**
  - *.js
  - *.ts
  - *.jsx
  - *.tsx

## Blocking synchronous API

### **Id**
blocking-sync-api
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - readFileSync
  - writeFileSync
  - execSync
  - localStorage\\.getItem.*localStorage\\.getItem
### **Message**
Synchronous API blocks the event loop
### **Fix Action**
Use async versions or move to worker
### **Applies To**
  - *.js
  - *.ts

## Query without index consideration

### **Id**
no-index-hint
### **Severity**
info
### **Type**
regex
### **Pattern**
  - findMany\\(\\{[^}]*where:\\s*\\{[^}]*\\}[^}]*\\}\\)
  - SELECT.*WHERE(?!.*(?:id|_id)\\s*=)
### **Message**
Verify this query uses an index
### **Fix Action**
Check query plan, add index if needed
### **Applies To**
  - *.ts
  - *.js
  - *.sql

## Query without LIMIT

### **Id**
missing-limit
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - findMany\\(\\{(?![^}]*take:)
  - SELECT(?!.*LIMIT).*FROM
### **Message**
Query may return unbounded results
### **Fix Action**
Add take/LIMIT to prevent loading too much data
### **Applies To**
  - *.ts
  - *.js
  - *.sql

## Event listener without cleanup

### **Id**
missing-cleanup
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - useEffect\\([^]*addEventListener[^]*(?!removeEventListener)
### **Message**
Event listener may not be cleaned up
### **Fix Action**
Return cleanup function from useEffect
### **Applies To**
  - *.jsx
  - *.tsx

## setInterval without cleanup

### **Id**
uncontrolled-interval
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - setInterval\\([^;]*\\);(?!.*clearInterval)
### **Message**
Interval may not be cleared
### **Fix Action**
Store interval ID and clear in cleanup
### **Applies To**
  - *.js
  - *.ts
  - *.jsx
  - *.tsx