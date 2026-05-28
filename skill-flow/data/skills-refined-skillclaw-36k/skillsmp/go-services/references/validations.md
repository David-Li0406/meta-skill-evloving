# Go Services - Validations

## Error return value ignored

### **Id**
error-ignored
### **Severity**
error
### **Type**
regex
### **Pattern**
  - ^\s*\w+\([^)]*\)\s*$
  - _\s*,?\s*=\s*\w+\([^)]*\)(?!\s*//)
### **Message**
Error return value ignored - errors should be handled explicitly
### **Fix Action**
Handle the error: if err != nil { return err }
### **Applies To**
  - *.go

## Naked panic without recovery

### **Id**
naked-panic
### **Severity**
error
### **Type**
regex
### **Pattern**
  - panic\([^)]+\)
### **Message**
Panic in production code - use error returns instead
### **Fix Action**
Return an error instead of panicking: return fmt.Errorf(...)
### **Applies To**
  - *.go

## HTTP client with no timeout

### **Id**
hardcoded-timeout
### **Severity**
error
### **Type**
regex
### **Pattern**
  - http\.DefaultClient
  - &http\.Client\{\s*\}
### **Message**
HTTP client without timeout will block forever on slow responses
### **Fix Action**
Set explicit timeout: &http.Client{Timeout: 30*time.Second}
### **Applies To**
  - *.go

## Hardcoded credentials in code

### **Id**
hardcoded-credentials
### **Severity**
error
### **Type**
regex
### **Pattern**
  - password\s*:?=\s*"[^"]+"
  - apiKey\s*:?=\s*"[^"]+"
  - secret\s*:?=\s*"[^"]+"
### **Message**
Hardcoded credentials - use environment variables
### **Fix Action**
Use os.Getenv() or a secrets manager
### **Applies To**
  - *.go

## fmt.Print used instead of logging

### **Id**
fmt-print-in-production
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - fmt\.Print(ln|f)?\(
### **Message**
fmt.Print lacks timestamps and levels - use structured logging
### **Fix Action**
Use slog, log/slog, or zerolog for structured logging
### **Applies To**
  - *.go

## context.Background() in HTTP handler

### **Id**
context-background-in-handler
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - context\.Background\(\)
### **Message**
Use r.Context() in HTTP handlers, not context.Background()
### **Fix Action**
Pass the request context: ctx := r.Context()
### **Applies To**
  - *.go

## Goroutine without panic recovery

### **Id**
goroutine-without-recovery
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - go\s+func\s*\([^)]*\)\s*\{(?![\s\S]*defer[\s\S]*recover)
### **Message**
Goroutine without recover() - uncaught panic will crash service
### **Fix Action**
Add defer with recover: defer func() { if r := recover(); r != nil { log.Error(...) } }()
### **Applies To**
  - *.go

## Mutex unlock not deferred

### **Id**
mutex-not-deferred
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - \.Lock\(\)[^}]*\.Unlock\(\)(?!\s*defer)
### **Message**
Mutex unlock not deferred - may not unlock on panic
### **Fix Action**
Use defer: mu.Lock(); defer mu.Unlock()
### **Applies To**
  - *.go

## Overuse of interface{}

### **Id**
empty-interface
### **Severity**
info
### **Type**
regex
### **Pattern**
  - interface\{\}
  - \bany\b
### **Message**
interface{}/any loses type safety - consider generics or specific types
### **Fix Action**
Use generics [T any] or define a specific interface
### **Applies To**
  - *.go

## time.Sleep used for timing

### **Id**
time-sleep-in-production
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - time\.Sleep\(
### **Message**
time.Sleep blocks goroutine - use time.After with select for cancellation
### **Fix Action**
Use select with time.After and context.Done()
### **Applies To**
  - *.go

## fmt.Sprintf for simple conversions

### **Id**
strconv-instead-of-fmt
### **Severity**
info
### **Type**
regex
### **Pattern**
  - fmt\.Sprintf\("%d",\s*\w+\)
  - fmt\.Sprintf\("%s",\s*\w+\)
### **Message**
Use strconv for simple conversions - faster than fmt
### **Fix Action**
Use strconv.Itoa() or strconv.FormatInt()
### **Applies To**
  - *.go

## SQL query with string concatenation

### **Id**
sql-string-concat
### **Severity**
error
### **Type**
regex
### **Pattern**
  - (Query|Exec)\s*\([^,]*\+\s*\w+
  - (Query|Exec)\s*\(\s*fmt\.Sprintf
### **Message**
SQL injection vulnerability - use parameterized queries
### **Fix Action**
Use $1, $2 placeholders: db.Query("SELECT * FROM users WHERE id = $1", id)
### **Applies To**
  - *.go