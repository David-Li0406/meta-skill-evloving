# Codebase Optimization - Validations

## Unbounded Cache

### **Id**
opt-unbounded-cache
### **Severity**
warning
### **Type**
regex
### **Pattern**
new Map\\(\\)(?![\\s\\S]*\\.delete|[\\s\\S]*\\.clear|[\\s\\S]*LRU)|cache\\s*=\\s*\\{\\}(?![\\s\\S]*delete\\s+cache)|new Set\\(\\)(?![\\s\\S]*\\.delete|[\\s\\S]*\\.clear)
### **Message**
Unbounded cache without cleanup. Can cause memory leaks.
### **Fix Action**
Use LRU cache with max size or add TTL/cleanup
### **Applies To**
  - *.ts
  - *.js

## Nested Loop (O(n²) Potential)

### **Id**
opt-nested-loop
### **Severity**
warning
### **Type**
regex
### **Pattern**
\\.forEach\\([^)]*\\)[^}]*\\.forEach\\(|\\.map\\([^)]*\\)[^}]*\\.map\\(|for\\s*\\([^)]*\\)[^}]*for\\s*\\(
### **Message**
Nested loops detected. O(n²) complexity. Consider optimization if n is large.
### **Fix Action**
Use Map/Set for lookups or reconsider algorithm
### **Applies To**
  - *.ts
  - *.js
  - *.tsx
  - *.jsx

## Synchronous File Operation

### **Id**
opt-sync-file-op
### **Severity**
warning
### **Type**
regex
### **Pattern**
readFileSync|writeFileSync|existsSync(?![\\s\\S]*startup|[\\s\\S]*init)|readdirSync
### **Message**
Synchronous file operation blocks event loop.
### **Fix Action**
Use async version: readFile, writeFile, etc.
### **Applies To**
  - *.ts
  - *.js

## Event Listener Without Cleanup

### **Id**
opt-event-listener-leak
### **Severity**
warning
### **Type**
regex
### **Pattern**
addEventListener\\([^)]*\\)(?![\\s\\S]{0,200}removeEventListener)|window\\.on[a-z]+\\s*=(?![\\s\\S]{0,100}null)|\\.subscribe\\((?![\\s\\S]{0,200}\\.unsubscribe)
### **Message**
Event listener added without visible cleanup. Potential memory leak.
### **Fix Action**
Add cleanup in useEffect return or componentWillUnmount
### **Applies To**
  - *.ts
  - *.js
  - *.tsx
  - *.jsx

## String Concatenation in Loop

### **Id**
opt-string-concat-loop
### **Severity**
warning
### **Type**
regex
### **Pattern**
for.*\\+=\\s*["']|\\.forEach.*\\+=\\s*["']|while.*\\+=\\s*["']
### **Message**
String concatenation in loop is O(n²). Use array.join() instead.
### **Fix Action**
Collect strings in array, then join: parts.push(str); parts.join('')
### **Applies To**
  - *.ts
  - *.js

## Regex Creation in Loop

### **Id**
opt-regex-in-loop
### **Severity**
warning
### **Type**
regex
### **Pattern**
for.*new RegExp\\(|\\.forEach.*new RegExp\\(|\\.map.*new RegExp\\(
### **Message**
Regex created inside loop. Create once outside loop.
### **Fix Action**
Hoist regex creation outside the loop
### **Applies To**
  - *.ts
  - *.js

## JSON Parse in Hot Path

### **Id**
opt-json-parse-loop
### **Severity**
warning
### **Type**
regex
### **Pattern**
\\.map.*JSON\\.parse|\\.forEach.*JSON\\.parse|for.*JSON\\.parse
### **Message**
JSON.parse in loop can be expensive. Consider caching or batch processing.
### **Fix Action**
Parse once if possible, or use streaming JSON parser for large data
### **Applies To**
  - *.ts
  - *.js

## Sequential Await in Loop

### **Id**
opt-await-in-loop
### **Severity**
warning
### **Type**
regex
### **Pattern**
for\\s*\\([^)]*\\)\\s*\\{[^}]*await\\s+|\\.forEach\\(async[^}]*await\\s+
### **Message**
Sequential await in loop. Consider Promise.all for parallel execution.
### **Fix Action**
Use Promise.all(items.map(async item => ...))
### **Applies To**
  - *.ts
  - *.js

## Query Without Index Hint

### **Id**
opt-no-index-query
### **Severity**
warning
### **Type**
regex
### **Pattern**
\\.find\\(\\{[^}]*\\$regex|\\.find\\(\\{[^}]*\\$where|SELECT.*WHERE(?!.*INDEX)
### **Message**
Query pattern may not use indexes efficiently.
### **Fix Action**
Ensure indexed fields are queried, add EXPLAIN to verify
### **Applies To**
  - *.ts
  - *.js

## Large Library Full Import

### **Id**
opt-large-bundle-import
### **Severity**
warning
### **Type**
regex
### **Pattern**
import\s+\*\s+as\s+\w+\s+from\s+['"]lodash['"]|import\s+\w+\s+from\s+['"]lodash['"]|import\s+\*\s+as\s+\w+\s+from\s+['"]moment['"]|require\(['"]lodash['"]\)
### **Message**
Full library import increases bundle size. Use specific imports.
### **Fix Action**
Import specific: import { debounce } from 'lodash/debounce'
### **Applies To**
  - *.ts
  - *.js
  - *.tsx
  - *.jsx

## Inefficient Array Existence Check

### **Id**
opt-inefficient-array-check
### **Severity**
warning
### **Type**
regex
### **Pattern**
\\.indexOf\\([^)]*\\)\\s*[!=]==?\\s*-1|\\.indexOf\\([^)]*\\)\\s*>=?\\s*0
### **Message**
Use .includes() instead of .indexOf() !== -1 for clarity.
### **Fix Action**
Replace with array.includes(item)
### **Applies To**
  - *.ts
  - *.js
  - *.tsx
  - *.jsx

## DOM Query in Loop

### **Id**
opt-document-query-loop
### **Severity**
warning
### **Type**
regex
### **Pattern**
for.*document\\.querySelector|\\.forEach.*document\\.getElementById|\\.map.*document\\.querySelector
### **Message**
DOM query inside loop. Query once and cache the result.
### **Fix Action**
Hoist DOM query outside loop: const el = document.querySelector(...)
### **Applies To**
  - *.ts
  - *.js
  - *.tsx
  - *.jsx

## Potential Main Thread Block

### **Id**
opt-blocking-main-thread
### **Severity**
warning
### **Type**
regex
### **Pattern**
while\\s*\\(true\\)|while\\s*\\(1\\)|\\.sort\\(.*\\.sort\\(
### **Message**
Pattern may block main thread. Consider Web Workers or chunking.
### **Fix Action**
Use requestIdleCallback, Web Workers, or chunk processing
### **Applies To**
  - *.ts
  - *.js
  - *.tsx
  - *.jsx

## Console Log in Production Path

### **Id**
opt-console-in-prod
### **Severity**
warning
### **Type**
regex
### **Pattern**
console\\.log\\([^)]*\\$\\{.*\\}[^)]*\\)|console\\.log\\([^)]*\\+[^)]*\\)
### **Message**
Console with string interpolation in production code. Use structured logging.
### **Fix Action**
Use structured logger: logger.info({ data }, 'message')
### **Applies To**
  - src/**/*.ts
  - src/**/*.js