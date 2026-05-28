# Self-Assessment Checklists

Check what you can do without looking it up.

Use this on low-energy days: reviewing what you know is still progress.

---

## Phase 0: Go Philosophy

### I understand...

- [ ] Why Go has no inheritance (composition only)
- [ ] Why Go interfaces are small (often 1-2 methods)
- [ ] Why errors are values, not exceptions
- [ ] Why "explicit is better than implicit"
- [ ] The "accept interfaces, return structs" principle

### I can explain to someone...

- [ ] How Go's implicit interface satisfaction works
- [ ] Why YAGNI matters more in Go than Java

---

## Phase 1: Syntax Survival

### I can write...

- [ ] A Chi router with GET and POST handlers
- [ ] A struct with JSON tags
- [ ] A function that returns (result, error)
- [ ] Error handling with errors.Is/errors.As
- [ ] A constructor function (NewXxx pattern)

### I understand...

- [ ] The difference between value and pointer receivers
- [ ] Why capitalization controls visibility
- [ ] How defer works for cleanup
- [ ] The difference between slices and arrays
- [ ] How to initialize maps (and why it matters)

### I can explain to someone...

- [ ] Why Go doesn't have exceptions
- [ ] How package structure works in Go

---

## Phase 2: Building APIs

### I can write...

- [ ] A complete CRUD handler with Chi
- [ ] JSON request parsing and response encoding
- [ ] Validation using go-playground/validator
- [ ] Custom error types and error handling
- [ ] A unit test with httptest

### I understand...

- [ ] How Chi URL params work (chi.URLParam)
- [ ] How to return proper HTTP status codes
- [ ] Table-driven tests and t.Run
- [ ] How to structure handlers, services, and repos
- [ ] The difference between unit and integration tests

### I can explain to someone...

- [ ] How Go's error handling flows through layers
- [ ] Why interface mocking is simple in Go

---

## Phase 3: Data & Concurrency

### I can write...

- [ ] Database queries with database/sql or sqlx
- [ ] A repository with interface
- [ ] Goroutines with sync.WaitGroup
- [ ] Channel-based communication
- [ ] A simple worker pool
- [ ] Context with timeout/cancellation

### I understand...

- [ ] Why maps are not thread-safe
- [ ] When to use buffered vs unbuffered channels
- [ ] How context propagates through call stack
- [ ] The difference between pointer and value receivers
- [ ] How to avoid goroutine leaks

### I can explain to someone...

- [ ] "Don't communicate by sharing memory; share memory by communicating"
- [ ] How Go's channels compare to Java's BlockingQueue

---

## Phase 4: Production Patterns

### I can write...

- [ ] Structured logging with slog
- [ ] Prometheus metrics endpoints
- [ ] Graceful shutdown with signal handling
- [ ] Integration tests with testcontainers
- [ ] Proper project structure (cmd/, internal/, pkg/)

### I understand...

- [ ] How to use build tags
- [ ] Why /internal restricts imports
- [ ] How environment variables work in Go
- [ ] When to use third-party packages vs stdlib

### I can explain to someone...

- [ ] How to structure a production Go service
- [ ] The trade-offs between frameworks and stdlib

---

## Final: Javer No More

### Mindset shifts

- [ ] I return errors instead of trying to simulate exceptions
- [ ] I write explicit code instead of relying on framework magic
- [ ] I create interfaces when I need them, not anticipating future needs
- [ ] I access struct fields directly instead of using getters/setters
- [ ] I wire dependencies manually in main()

### Practical proof

- [ ] I can write an HTTP handler without thinking about Spring
- [ ] I can debug a Go stack trace without confusion
- [ ] I know where code belongs in Go's package structure
- [ ] I can read someone else's Go code and understand it

### Emotional state

- [ ] I feel neutral (not frustrated) toward Go
- [ ] I can appreciate what Go does well
- [ ] I accept that this is a skill worth having
- [ ] I don't mentally translate from Java anymore when writing Go

---

## How to Use This

**On a full-energy day:**
- Work through exercises
- Come back here to check off what you learned

**On a low-energy day:**
- Scan through and check boxes for things you already know
- Notice progress since last time
- Pick ONE unchecked item to review (not learn, just review)

**When frustrated:**
- Count your checkmarks
- Remember: every check is evidence of progress
- Close this file and do something else

---

Checking boxes is progress. You don't have to do exercises to move forward.
