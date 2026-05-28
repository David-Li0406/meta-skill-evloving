# Go Services - Sharp Edges

## Goroutine Leak

### **Id**
goroutine-leak
### **Summary**
Goroutines that never terminate consume memory forever
### **Severity**
critical
### **Situation**
  You spawn goroutines in a loop or for each request, but they block on
  a channel or network call that never completes. Memory grows until OOM.
  
### **Why**
  Goroutines are cheap to create but never garbage collected until they exit.
  A goroutine blocked on a channel read forever will live forever. At scale,
  this means thousands of leaked goroutines per hour. We've seen services
  with 500k+ goroutines that should have 100.
  
### **Solution**
  # ALWAYS have an exit path for goroutines
  
  // WRONG: Goroutine blocks forever if channel is abandoned
  go func() {
      result := <-resultChan  // Blocked forever if sender dies
      process(result)
  }()
  
  // RIGHT: Context cancellation provides exit path
  go func() {
      select {
      case result := <-resultChan:
          process(result)
      case <-ctx.Done():
          return  // Exit when context cancelled
      }
  }()
  
  // RIGHT: Timeout ensures eventual exit
  go func() {
      select {
      case result := <-resultChan:
          process(result)
      case <-time.After(30 * time.Second):
          log.Warn("timed out waiting for result")
          return
      }
  }()
  
### **Symptoms**
  - Memory usage growing over time
  - runtime.NumGoroutine() increasing without bound
  - OOM kills after hours/days of runtime
  - pprof goroutine dump shows thousands blocked on same line
### **Detection Pattern**
go\s+func\s*\([^)]*\)\s*\{[^}]*<-[^}]*\}(?!.*select)

## Nil Channel Block

### **Id**
nil-channel-block
### **Summary**
Sending or receiving on nil channel blocks forever
### **Severity**
high
### **Situation**
  You have a channel variable that might be nil (uninitialized or set to nil
  conditionally), and you try to send or receive on it.
  
### **Why**
  Unlike nil maps (panic on write) or nil slices (work fine), nil channels
  block forever on both send and receive. This is by design for select
  statements but a footgun for regular use.
  
### **Solution**
  # NIL CHANNEL BEHAVIOR
  
  var ch chan int  // ch is nil
  
  ch <- 1   // BLOCKS FOREVER (not panic!)
  <-ch      // BLOCKS FOREVER (not panic!)
  
  // RIGHT: Initialize channels before use
  ch := make(chan int)
  
  // Using nil channel in select (intentionally disable a case)
  var enabled chan int
  if shouldEnable {
      enabled = make(chan int, 1)
  }
  
  select {
  case v := <-enabled:  // Disabled if enabled is nil
      process(v)
  case <-ctx.Done():
      return
  }
  
### **Symptoms**
  - Goroutine appears to hang
  - pprof shows goroutine blocked on channel operation
  - Code after channel operation never executes
### **Detection Pattern**
var\s+\w+\s+chan\s+\w+

## Defer In Loop

### **Id**
defer-in-loop
### **Summary**
Deferred calls in loops execute at function end, not iteration end
### **Severity**
high
### **Situation**
  You use defer inside a for loop expecting cleanup after each iteration,
  but all defers stack up and execute when the function returns.
  
### **Why**
  Defer is function-scoped, not block-scoped. In a loop processing 10,000
  files, you'll have 10,000 open file handles until the function returns.
  This causes "too many open files" errors and resource exhaustion.
  
### **Solution**
  # DEFER IN LOOPS
  
  // WRONG: All files stay open until function returns
  for _, path := range paths {
      f, err := os.Open(path)
      if err != nil {
          continue
      }
      defer f.Close()  // Won't close until function ends!
      process(f)
  }
  
  // RIGHT: Extract to function for per-iteration defer
  for _, path := range paths {
      if err := processFile(path); err != nil {
          log.Error(err)
      }
  }
  
  func processFile(path string) error {
      f, err := os.Open(path)
      if err != nil {
          return err
      }
      defer f.Close()  // Closes when this function returns
      return process(f)
  }
  
  // RIGHT: Explicit close without defer
  for _, path := range paths {
      f, err := os.Open(path)
      if err != nil {
          continue
      }
      process(f)
      f.Close()  // Immediate close
  }
  
### **Symptoms**
  - "too many open files" errors
  - Memory usage spikes during loops
  - Resources not released as expected
### **Detection Pattern**
for\s+[^{]*\{[^}]*defer\s+

## Range Variable Capture

### **Id**
range-variable-capture
### **Summary**
Loop variable captured by reference in goroutines
### **Severity**
critical
### **Situation**
  You spawn goroutines inside a range loop, and they all see the same
  (final) value of the loop variable.
  
### **Why**
  Prior to Go 1.22, the loop variable was reused each iteration. Goroutines
  capture by reference, so they all see the final value. Go 1.22+ fixed this
  by default, but legacy code and older versions still have the bug.
  
### **Solution**
  # LOOP VARIABLE CAPTURE (Pre Go 1.22)
  
  // WRONG: All goroutines see the last item
  for _, item := range items {
      go func() {
          process(item)  // item is the same (last) for all goroutines!
      }()
  }
  
  // RIGHT: Pass as parameter (works in all Go versions)
  for _, item := range items {
      go func(item Item) {
          process(item)
      }(item)  // Pass by value
  }
  
  // RIGHT: Shadow the variable (pre-1.22 idiom)
  for _, item := range items {
      item := item  // Shadow with new variable
      go func() {
          process(item)
      }()
  }
  
  // Go 1.22+: Fixed by default with GOEXPERIMENT=loopvar
  // But still good practice to be explicit
  
### **Symptoms**
  - All goroutines process the same (last) item
  - Race condition warnings from race detector
  - Intermittent wrong results
### **Detection Pattern**
for\s+\w*,?\s*(\w+)\s*:?=\s*range[^{]*\{[^}]*go\s+func\s*\([^)]*\)\s*\{[^}]*\1

## Sync Mutex Copy

### **Id**
sync-mutex-copy
### **Summary**
Copying a mutex copies its lock state
### **Severity**
critical
### **Situation**
  You pass a struct containing a mutex by value, or embed a mutex in
  a struct that gets copied.
  
### **Why**
  Copying a locked mutex creates a new locked mutex. Copying an unlocked
  mutex is a data race waiting to happen. The go vet tool catches this
  but many codebases don't run vet in CI.
  
### **Solution**
  # MUTEX COPY
  
  type Cache struct {
      mu    sync.Mutex  // Embedded mutex
      items map[string]string
  }
  
  // WRONG: Passing by value copies the mutex
  func processCache(c Cache) {
      c.mu.Lock()  // Operating on a COPY of the mutex!
      // ...
  }
  
  // RIGHT: Pass by pointer
  func processCache(c *Cache) {
      c.mu.Lock()
      defer c.mu.Unlock()
      // ...
  }
  
  // Run go vet to catch these
  // go vet ./...
  
### **Symptoms**
  - Data races detected by -race flag
  - Deadlocks that seem impossible
  - go vet warnings about copying locks
### **Detection Pattern**
func\s+\w+\([^)]*\w+\s+\w*sync\.(Mutex|RWMutex|WaitGroup)

## Empty Select Block

### **Id**
empty-select-block
### **Summary**
Empty select{} blocks forever and is hard to debug
### **Severity**
medium
### **Situation**
  You use `select {}` to block a main goroutine or as a placeholder,
  making debugging difficult when things hang.
  
### **Why**
  An empty select blocks forever and gives no indication why. When
  your service hangs, the stack trace just shows "blocked in select".
  Use explicit channel waits or signal handling instead.
  
### **Solution**
  # BLOCKING PATTERNS
  
  // BAD: Empty select blocks with no explanation
  func main() {
      go startServer()
      select {}  // Blocks forever, but why?
  }
  
  // GOOD: Signal handling makes intent clear
  func main() {
      go startServer()
  
      quit := make(chan os.Signal, 1)
      signal.Notify(quit, syscall.SIGINT, syscall.SIGTERM)
      <-quit  // Clear: waiting for shutdown signal
  
      log.Println("Shutting down...")
  }
  
  // GOOD: Use sync.WaitGroup for waiting on goroutines
  var wg sync.WaitGroup
  wg.Add(1)
  go func() {
      defer wg.Done()
      startServer()
  }()
  wg.Wait()
  
### **Symptoms**
  - Service hangs with no clear cause
  - Stack trace shows "select (no cases)"
  - Can't gracefully shut down
### **Detection Pattern**
select\s*\{\s*\}

## Http Body Not Closed

### **Id**
http-body-not-closed
### **Summary**
HTTP response body not closed causes connection leak
### **Severity**
high
### **Situation**
  You make HTTP requests but don't read and close the response body,
  or you return early after error checking the response.
  
### **Why**
  HTTP/1.1 connections can be reused, but only if the body is fully read
  and closed. Unclosed bodies leak connections until the connection pool
  is exhausted, then requests start failing.
  
### **Solution**
  # HTTP BODY HANDLING
  
  // WRONG: Body never closed on success
  resp, err := http.Get(url)
  if err != nil {
      return err
  }
  // Body never closed!
  
  // WRONG: Body never closed on status error
  resp, err := http.Get(url)
  if err != nil {
      return err
  }
  if resp.StatusCode != 200 {
      return errors.New("bad status")  // Body never closed!
  }
  
  // RIGHT: Always close body
  resp, err := http.Get(url)
  if err != nil {
      return err
  }
  defer resp.Body.Close()
  
  if resp.StatusCode != 200 {
      io.Copy(io.Discard, resp.Body)  // Drain to allow reuse
      return fmt.Errorf("bad status: %d", resp.StatusCode)
  }
  
  // Read body
  data, err := io.ReadAll(resp.Body)
  
### **Symptoms**
  - "connection reset by peer" errors
  - Requests timing out after running fine initially
  - Connection pool exhaustion
### **Detection Pattern**
http\.(Get|Post|Do)\([^)]*\)[^}]*(return|continue|break)[^}]*(?!defer\s+\w*\.Body\.Close)

## Json Time Format

### **Id**
json-time-format
### **Summary**
time.Time JSON marshaling defaults to RFC3339 with nanoseconds
### **Severity**
medium
### **Situation**
  You expect a specific time format in JSON (ISO 8601, Unix timestamp) but
  time.Time marshals to RFC3339Nano format by default.
  
### **Why**
  Frontend JavaScript or external APIs often expect specific formats.
  The default format works but may not match expectations. Worse, parsing
  inconsistent formats causes silent data corruption.
  
### **Solution**
  # TIME FORMAT HANDLING
  
  type Event struct {
      Name      string    `json:"name"`
      CreatedAt time.Time `json:"created_at"`  // RFC3339Nano default
  }
  
  // Default output: "2024-01-15T10:30:00.123456789Z"
  
  // For custom format, use custom type:
  type UnixTime time.Time
  
  func (t UnixTime) MarshalJSON() ([]byte, error) {
      return json.Marshal(time.Time(t).Unix())
  }
  
  func (t *UnixTime) UnmarshalJSON(data []byte) error {
      var unix int64
      if err := json.Unmarshal(data, &unix); err != nil {
          return err
      }
      *t = UnixTime(time.Unix(unix, 0))
      return nil
  }
  
  type Event struct {
      Name      string   `json:"name"`
      CreatedAt UnixTime `json:"created_at"`  // Unix timestamp
  }
  
### **Symptoms**
  - Frontend can't parse dates
  - API clients complain about format
  - Time zone confusion
### **Detection Pattern**


## Unbuffered Channel Deadlock

### **Id**
unbuffered-channel-deadlock
### **Summary**
Send and receive on unbuffered channel in same goroutine deadlocks
### **Severity**
high
### **Situation**
  You try to send on an unbuffered channel and then receive from it
  (or vice versa) in the same goroutine.
  
### **Why**
  Unbuffered channels block until both sender and receiver are ready.
  A single goroutine can't be both simultaneously. The code deadlocks
  instantly but silently if there's no other goroutine to detect it.
  
### **Solution**
  # UNBUFFERED CHANNEL DEADLOCK
  
  ch := make(chan int)  // Unbuffered
  
  // DEADLOCK: Blocks on send, never reaches receive
  ch <- 1
  <-ch
  
  // RIGHT: Use goroutine for one side
  ch := make(chan int)
  go func() {
      ch <- 1
  }()
  value := <-ch
  
  // RIGHT: Use buffered channel for send-then-receive
  ch := make(chan int, 1)  // Buffer of 1
  ch <- 1
  value := <-ch
  
### **Symptoms**
  - Program hangs immediately
  - fatal error: all goroutines are asleep - deadlock!
### **Detection Pattern**
make\(chan\s+\w+\)[^,)]