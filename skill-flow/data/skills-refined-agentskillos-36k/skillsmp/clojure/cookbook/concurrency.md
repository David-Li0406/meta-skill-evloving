# Concurrency & State Management Cookbook

A guide to Clojure's concurrency primitives and state management patterns.

## Reference Types Overview

| Type | Use Case | Coordination | Sync/Async |
|------|----------|--------------|------------|
| Atom | Independent state | None | Sync |
| Ref | Coordinated state | STM | Sync |
| Agent | Async updates | None | Async |
| Var | Thread-local | None | Sync |

---

## Managing Independent State with Atoms

**Problem**: You need thread-safe synchronous updates to independent state without coordination.

**Solution**:
```clojure
;; Create
(def counter (atom 0))
(def users (atom {}))

;; Read
@counter          ; => 0
(deref counter)   ; => 0

;; Update with swap! (fn applied to current value)
(swap! counter inc)           ; => 1
(swap! counter + 5)           ; => 6
(swap! users assoc :alice {:name "Alice"})

;; Replace with reset! (use sparingly)
(reset! counter 0)

;; Compare-and-set (low-level)
(compare-and-set! counter 0 1) ; true if was 0
```

**Tip**: Use `swap!` for updates based on current value. Only use `reset!` when you truly need to replace the value regardless of current state.

---

## Conditional Updates with Atoms

**Problem**: You need to update an atom only when certain conditions are met.

**Solution**:
```clojure
;; Conditional update
(swap! state
  (fn [s]
    (if (valid? s)
      (transform s)
      s)))

;; Update and return old value
(let [old @counter]
  (swap! counter inc)
  old)
```

**Tip**: The function passed to `swap!` may be called multiple times due to retries, so keep it pure and free of side effects.

---

## Validating and Watching Atom Changes

**Problem**: You need to enforce constraints on atom values or react to changes.

**Solution**:
```clojure
;; With validators
(def positive (atom 0 :validator pos?))
(reset! positive -1) ; throws

;; With watchers
(add-watch counter :logger
  (fn [key ref old new]
    (println "Changed from" old "to" new)))

(remove-watch counter :logger)
```

**Tip**: Validators throw exceptions on invalid updates. Use watchers for logging or triggering side effects after state changes.

---

## Building a Thread-Safe Cache

**Problem**: You need a simple thread-safe cache that computes values on-demand.

**Solution**:
```clojure
(def cache (atom {}))

(defn cached [key compute-fn]
  (if-let [v (get @cache key)]
    v
    (let [v (compute-fn)]
      (swap! cache assoc key v)
      v)))

;; Or use swap! with update-if-absent pattern
(defn memoized-get [cache key compute-fn]
  (or (get @cache key)
      (get (swap! cache
             (fn [m]
               (if (contains? m key)
                 m
                 (assoc m key (compute-fn)))))
           key)))
```

**Tip**: The second approach ensures the compute function is only called once even under contention, preventing duplicate work.

---

## Coordinated Updates with Refs and STM

**Problem**: You need to update multiple pieces of state atomically (all-or-nothing).

**Solution**:
```clojure
;; Create refs
(def account-a (ref {:balance 1000}))
(def account-b (ref {:balance 500}))

;; Transaction: all-or-nothing
(dosync
  (alter account-a update :balance - 100)
  (alter account-b update :balance + 100))

;; Read inside transaction
(dosync
  (let [total (+ (:balance @account-a)
                 (:balance @account-b))]
    (println "Total:" total)))
```

**Tip**: Use refs when you need coordinated updates to multiple pieces of state. STM ensures all changes happen atomically or not at all.

---

## Ref Operations for Different Use Cases

**Problem**: You need to choose the right ref operation for your use case.

**Solution**:
```clojure
;; alter: apply fn (retries on conflict)
(dosync (alter counter inc))

;; commute: apply fn (no retry for commutative ops)
(dosync (commute counter inc))

;; ref-set: replace value
(dosync (ref-set counter 0))

;; ensure: read consistency without modify
(dosync
  (ensure account-a)
  (if (> (:balance @account-a) 100)
    (alter account-b update :balance + 50)))
```

**Tip**: Use `commute` for commutative operations (like `inc`) to reduce retries. Use `ensure` when you need consistent reads without modification.

---

## Avoiding Side Effects in Transactions

**Problem**: You need to perform side effects based on transactional state changes.

**Solution**:
```clojure
;; DON'T: Side effects in transactions (may retry!)
(dosync
  (alter state transform)
  (send-email!))  ; BAD: may send multiple times

;; DO: Perform side effects after
(let [result (dosync (alter state transform))]
  (send-email! result))

;; DO: Use for coordinated state
(dosync
  (alter inventory update item dec)
  (alter orders conj new-order))
```

**Tip**: Transactions may retry, so never put side effects inside `dosync`. Extract the result and perform side effects afterward.

---

## Async State Updates with Agents

**Problem**: You need to update state asynchronously without blocking the caller.

**Solution**:
```clojure
;; Create
(def log-agent (agent []))

;; send: for CPU-bound work (fixed thread pool)
(send log-agent conj {:event :login :time (now)})

;; send-off: for blocking I/O (cached thread pool)
(send-off log-agent
  (fn [logs]
    (write-to-file! logs)
    []))

;; Read (current value, may have pending actions)
@log-agent

;; Wait for completion
(await log-agent)              ; Wait for this agent
(await-for 1000 agent1 agent2) ; Timeout ms
```

**Tip**: Use `send` for CPU-bound work and `send-off` for blocking I/O. Actions are executed in order, one at a time per agent.

---

## Handling Agent Errors

**Problem**: You need to detect and recover from errors in agent actions.

**Solution**:
```clojure
;; Check for errors
(agent-error log-agent)

;; Restart failed agent
(restart-agent log-agent []
  :clear-actions true)

;; Set error handler
(set-error-handler! log-agent
  (fn [ag ex]
    (println "Agent error:" (.getMessage ex))))

;; Set error mode
(set-error-mode! log-agent :continue) ; or :fail
```

**Tip**: Agents enter a failed state on errors. Set error handlers and modes proactively to handle failures gracefully.

---

## Serializing I/O with Agents

**Problem**: You need to serialize writes to a file or resource without explicit locking.

**Solution**:
```clojure
(def file-writer (agent nil))

(defn write-line [filename line]
  (send-off file-writer
    (fn [_]
      (spit filename (str line "\n") :append true))))

;; All writes serialized, no locks needed
(write-line "log.txt" "Event 1")
(write-line "log.txt" "Event 2")
```

**Tip**: Agents naturally serialize operations, making them perfect for coordinating I/O without explicit locks.

---

## Thread-Local State with Dynamic Vars

**Problem**: You need context-specific state that's isolated per thread (like database connections or request data).

**Solution**:
```clojure
;; Define with earmuffs
(def ^:dynamic *db-conn* nil)
(def ^:dynamic *request* nil)

;; Bind for scope
(binding [*db-conn* (connect!)
          *request* {:user "alice"}]
  (do-work))

;; Access
(defn current-user []
  (:user *request*))

;; Nested bindings shadow outer
(binding [*db-conn* conn1]
  (query)  ; uses conn1
  (binding [*db-conn* conn2]
    (query)))  ; uses conn2
```

**Tip**: Dynamic vars provide thread-local scope without passing parameters explicitly. Use earmuffs `*var-name*` by convention.

---

## Preserving Bindings Across Threads

**Problem**: You need thread-local bindings to be available in newly spawned threads.

**Solution**:
```clojure
;; bound-fn preserves bindings for new threads
(binding [*x* 10]
  (future (bound-fn [] (println *x*))))  ; prints 10

;; Without bound-fn, future sees root binding
(binding [*x* 10]
  (future (println *x*)))  ; prints root value
```

**Tip**: Use `bound-fn` to capture current bindings for use in futures or other threads. Without it, new threads see only root bindings.

---

## Creating and Using Channels

**Problem**: You need to communicate between concurrent processes using CSP-style channels.

**Solution**:
```clojure
(require '[clojure.core.async :as a
           :refer [go go-loop chan <! >! <!! >!!
                   close! timeout alts! alts!!]])

;; Create channels
(def ch (chan))           ; Unbuffered
(def ch (chan 10))        ; Buffered (10 items)
(def ch (chan (a/sliding-buffer 10)))  ; Drops oldest
(def ch (chan (a/dropping-buffer 10))) ; Drops newest

;; With transducer
(def ch (chan 10 (map inc)))

;; Close
(close! ch)
```

**Tip**: Unbuffered channels block until both producer and consumer are ready. Use buffered channels when you need decoupling.

---

## Producing and Consuming with Go Blocks

**Problem**: You need lightweight threads for concurrent operations without blocking OS threads.

**Solution**:
```clojure
;; Produce
(go
  (>! ch 1)
  (>! ch 2)
  (close! ch))

;; Consume
(go-loop []
  (when-let [v (<! ch)]
    (println "Got:" v)
    (recur)))

;; Blocking (outside go blocks)
(>!! ch value)  ; Block until taken
(<!! ch)        ; Block until available
```

**Tip**: Use `<!` and `>!` inside go blocks, `<!!` and `>!!` outside. Go blocks are lightweight and can be parked efficiently.

---

## Selecting from Multiple Channels

**Problem**: You need to wait on multiple channels simultaneously with timeout support.

**Solution**:
```clojure
(go
  (let [[v port] (alts! [ch1 ch2 (timeout 1000)])]
    (cond
      (= port ch1) (println "From ch1:" v)
      (= port ch2) (println "From ch2:" v)
      :else (println "Timeout!"))))

;; With priority
(alts! [ch1 ch2] :priority true)  ; Prefer ch1

;; With default
(alts! [ch1 ch2] :default :none)  ; Don't block
```

**Tip**: Use `timeout` channels for timeouts, `:priority true` for deterministic ordering, and `:default` for non-blocking operations.

---

## Parallel Processing with Pipelines

**Problem**: You need to process channel data in parallel with a specified level of concurrency.

**Solution**:
```clojure
;; Parallel processing
(a/pipeline 4       ; parallelism
  out-ch            ; output
  (map process)     ; transducer
  in-ch)            ; input

;; Async pipeline (for async operations)
(a/pipeline-async 4
  out-ch
  (fn [v out-ch]
    (go
      (>! out-ch (async-process v))
      (close! out-ch)))
  in-ch)

;; Blocking pipeline (for blocking I/O)
(a/pipeline-blocking 4
  out-ch
  (map blocking-process)
  in-ch)
```

**Tip**: Use `pipeline` for CPU-bound work, `pipeline-async` for async operations, and `pipeline-blocking` for blocking I/O.

---

## Fan-Out Pattern

**Problem**: You need multiple workers consuming from a single channel.

**Solution**:
```clojure
;; Fan-out: one producer, multiple consumers
(let [ch (chan)]
  (dotimes [i 3]
    (go-loop []
      (when-let [v (<! ch)]
        (println "Worker" i "got" v)
        (recur)))))
```

**Tip**: Multiple consumers automatically compete for values from the channel, distributing work naturally.

---

## Fan-In Pattern

**Problem**: You need to merge multiple producer channels into a single consumer channel.

**Solution**:
```clojure
;; Fan-in: multiple producers, one consumer
(defn fan-in [chs]
  (let [out (chan)]
    (doseq [ch chs]
      (go-loop []
        (when-let [v (<! ch)]
          (>! out v)
          (recur))))
    out))
```

**Tip**: Fan-in merges multiple channels into one, useful for consolidating results from parallel operations.

---

## Publish-Subscribe Pattern

**Problem**: You need to route messages to multiple subscribers based on topics.

**Solution**:
```clojure
;; Pub/sub
(def publisher (chan))
(def publication (a/pub publisher :topic))

(let [sub-ch (chan)]
  (a/sub publication :news sub-ch)
  (go-loop []
    (when-let [msg (<! sub-ch)]
      (println "News:" msg)
      (recur))))

(go (>! publisher {:topic :news :content "Hello"}))
```

**Tip**: Publications automatically route messages to subscribers based on a topic function. Supports multiple subscribers per topic.

---

## Async Computations with Futures

**Problem**: You need to run a computation asynchronously on a thread pool and retrieve the result later.

**Solution**:
```clojure
;; Start async computation
(def result (future
              (Thread/sleep 1000)
              42))

;; Check if done
(realized? result)  ; => false/true

;; Get result (blocks)
@result             ; => 42
(deref result 500 :timeout)  ; With timeout
```

**Tip**: Futures start executing immediately on creation. Use `realized?` to check completion without blocking.

---

## One-Time Value Delivery with Promises

**Problem**: You need a container for a value that will be delivered exactly once, possibly from another thread.

**Solution**:
```clojure
;; Create empty promise
(def p (promise))

;; Deliver value (once only)
(deliver p 42)

;; Get value (blocks until delivered)
@p  ; => 42

;; Check if delivered
(realized? p)
```

**Tip**: Promises can only be delivered once. Subsequent `deliver` calls have no effect. Great for one-time signaling between threads.

---

## Lazy Evaluation with Delays

**Problem**: You need to defer an expensive computation until it's actually needed, and cache the result.

**Solution**:
```clojure
;; Deferred computation (runs once when dereferenced)
(def expensive (delay
                 (println "Computing...")
                 (reduce + (range 1000000))))

;; Force evaluation
@expensive  ; prints "Computing...", returns result
@expensive  ; returns cached result, no recomputation
```

**Tip**: Delays compute their value only once, on first dereference. Subsequent derefs return the cached value. Perfect for lazy initialization.

---
