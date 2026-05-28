# Rust Craftsman - Sharp Edges

## Async Block Sync Code

### **Id**
async-block-sync-code
### **Summary**
Blocking sync code in async context freezes executor
### **Severity**
critical
### **Situation**
Mixing sync and async code
### **Why**
  Tokio uses cooperative multitasking. If you call std::fs::read_to_string()
  in an async function, you block the entire executor thread. All other
  tasks on that thread stall. Under load, the whole server appears frozen.
  
### **Solution**
  1. Use async versions of I/O:
     // BAD - blocks executor
     let content = std::fs::read_to_string("file.txt")?;
  
     // GOOD - async I/O
     let content = tokio::fs::read_to_string("file.txt").await?;
  
  2. For CPU-bound work, use spawn_blocking:
     let result = tokio::task::spawn_blocking(|| {
         expensive_cpu_computation()
     }).await?;
  
  3. For libraries without async, use block_in_place:
     let result = tokio::task::block_in_place(|| {
         sync_library_call()
     });
  
### **Symptoms**
  - Server becomes unresponsive under load
  - Requests timeout randomly
  - Single slow request affects all others
### **Detection Pattern**
std::fs::|std::io::|std::net::|thread::sleep

## Unbounded Channels

### **Id**
unbounded-channels
### **Summary**
Unbounded channels cause OOM under pressure
### **Severity**
high
### **Situation**
Using mpsc channels without backpressure
### **Why**
  mpsc::unbounded_channel() has no limit. If producer is faster than
  consumer, memory grows unbounded. Under spike traffic, you OOM.
  This can happen suddenly after running fine for months.
  
### **Solution**
  1. Always use bounded channels:
     // BAD - unbounded
     let (tx, rx) = mpsc::unbounded_channel();
  
     // GOOD - bounded with backpressure
     let (tx, rx) = mpsc::channel(1000);
  
  2. Handle send failures:
     // Blocks when buffer full
     tx.send(msg).await?;
  
     // Or try_send for non-blocking with feedback
     match tx.try_send(msg) {
         Ok(_) => {}
         Err(TrySendError::Full(_)) => {
             // Apply backpressure - reject, retry, etc.
         }
         Err(TrySendError::Closed(_)) => {
             // Channel closed
         }
     }
  
  3. Monitor queue depth in production
  
### **Symptoms**
  - Memory grows over time
  - OOM under traffic spikes
  - Works in testing, fails in production
### **Detection Pattern**
unbounded_channel|crossbeam.*unbounded

## Arc Mutex Deadlock

### **Id**
arc-mutex-deadlock
### **Summary**
Arc<Mutex<T>> across await points causes deadlock
### **Severity**
critical
### **Situation**
Holding mutex guard across .await
### **Why**
  MutexGuard is not Send. If you hold it across .await, the task might
  resume on a different thread. Even with tokio::sync::Mutex, holding
  across .await blocks other tasks needing the lock, causing priority
  inversion and deadlocks.
  
### **Solution**
  1. Never hold locks across await:
     // BAD - lock held across await
     let guard = mutex.lock().await;
     do_async_thing().await;  // Still holding lock!
     drop(guard);
  
     // GOOD - release before await
     let data = {
         let guard = mutex.lock().await;
         guard.clone()  // Clone what you need
     };  // Lock released here
     do_async_thing().await;
  
  2. Use interior mutability patterns:
     // RwLock for read-heavy workloads
     let data = RwLock::new(State::default());
  
     // Or redesign with channels (actor pattern)
     let (tx, rx) = mpsc::channel(100);
     // Actor owns state, receives messages
  
  3. Consider parking_lot for sync contexts
  
### **Symptoms**
  - Tasks hang indefinitely
  - Deadlock under concurrent access
  - Works with single request, fails with concurrent
### **Detection Pattern**
lock\(\)\.await.*\.await|Mutex.*await.*await

## Iterator Vs Collect

### **Id**
iterator-vs-collect
### **Summary**
Collecting iterators when you don't need to
### **Severity**
medium
### **Situation**
Processing collections
### **Why**
  .collect::<Vec<_>>() allocates a new vector. If you're just iterating
  to find one item or compute a sum, you allocated for nothing. Iterators
  are lazy and zero-cost - collect is not.
  
### **Solution**
  1. Use iterator methods directly:
     // BAD - collects then searches
     let found = items.iter()
         .filter(|x| x.active)
         .collect::<Vec<_>>()
         .iter()
         .find(|x| x.name == "target");
  
     // GOOD - lazy, stops at first match
     let found = items.iter()
         .filter(|x| x.active)
         .find(|x| x.name == "target");
  
  2. Use fold/reduce for aggregation:
     // BAD
     let sum: i32 = items.iter()
         .map(|x| x.value)
         .collect::<Vec<_>>()
         .iter()
         .sum();
  
     // GOOD
     let sum: i32 = items.iter().map(|x| x.value).sum();
  
  3. Collect only when you need the Vec as output
  
### **Symptoms**
  - High memory usage in data processing
  - Slow iteration over large datasets
  - Unnecessary allocations in hot paths
### **Detection Pattern**
collect.*iter|collect.*find|collect.*sum

## String Formatting Allocation

### **Id**
string-formatting-allocation
### **Summary**
Format strings allocate, even when unused
### **Severity**
medium
### **Situation**
Logging or debug strings in hot paths
### **Why**
  format!() and to_string() always allocate. In hot paths, this adds
  up. Debug logging with format! runs even at info level if not gated.
  
### **Solution**
  1. Use log macros (lazy evaluation):
     // BAD - always formats
     let msg = format!("Processing {:?}", data);
     log::debug!("{}", msg);
  
     // GOOD - only formats if debug enabled
     log::debug!("Processing {:?}", data);
  
  2. Avoid format! in hot paths:
     // BAD
     for item in millions_of_items {
         let key = format!("prefix_{}", item.id);
         cache.get(&key);
     }
  
     // GOOD - reuse buffer
     let mut key = String::with_capacity(20);
     for item in millions_of_items {
         key.clear();
         write!(&mut key, "prefix_{}", item.id).unwrap();
         cache.get(&key);
     }
  
  3. Use Cow<str> for conditional allocation
  
### **Symptoms**
  - High allocation rate in profiler
  - String formatting dominates CPU profile
  - Memory fragmentation over time
### **Detection Pattern**
format!\(.*\).*for|loop.*format!

## Drop Order Matters

### **Id**
drop-order-matters
### **Summary**
Drop order causes use-after-free in unsafe or FFI
### **Severity**
critical
### **Situation**
Structs with multiple fields that reference each other
### **Why**
  Rust drops struct fields in declaration order. If field A borrows from
  field B, and A is declared first, A drops first while B is still valid.
  But if B drops first, A has dangling reference. Safe Rust prevents this,
  but FFI and unsafe can expose it.
  
### **Solution**
  1. Order fields correctly:
     // BAD - buffer drops before reader
     struct Parser {
         reader: BufReader<&'a [u8]>,  // References buffer
         buffer: Vec<u8>,              // Drops second - too late!
     }
  
     // GOOD - buffer drops after reader
     struct Parser {
         buffer: Vec<u8>,              // Drops second
         reader: BufReader<&'a [u8]>,  // Drops first
     }
  
  2. Use ManuallyDrop for explicit control:
     use std::mem::ManuallyDrop;
  
     struct Careful {
         handle: ManuallyDrop<Handle>,
         resource: Resource,
     }
  
     impl Drop for Careful {
         fn drop(&mut self) {
             // Explicit order
             unsafe { ManuallyDrop::drop(&mut self.handle); }
             // resource drops automatically after
         }
     }
  
  3. In FFI, always explicitly manage drop order
  
### **Symptoms**
  - Segfaults in destructors
  - Use-after-free in FFI code
  - ASAN violations on shutdown
### **Detection Pattern**
ManuallyDrop|Drop.*impl|unsafe.*drop

## Send Sync Bounds

### **Id**
send-sync-bounds
### **Summary**
Missing Send/Sync bounds cause compile errors far from source
### **Severity**
medium
### **Situation**
Generic code with async or threading
### **Why**
  Async runtimes require futures to be Send. If your generic type isn't
  Send, users get confusing errors deep in framework code. The fix is
  in your library, but the error appears in user code.
  
### **Solution**
  1. Add bounds on public APIs:
     // BAD - no Send bound, users hit errors
     pub async fn process<T>(item: T) { ... }
  
     // GOOD - explicit bounds
     pub async fn process<T: Send + 'static>(item: T) { ... }
  
  2. Propagate bounds in traits:
     pub trait Handler: Send + Sync {
         type Output: Send;
         async fn handle(&self, req: Request) -> Self::Output;
     }
  
  3. Document non-Send types clearly:
     /// NOTE: This type is !Send due to internal Rc.
     /// Use in single-threaded context only.
     pub struct LocalCache { ... }
  
  4. Consider using #[derive(Debug)] - it helps debugging
  
### **Symptoms**
  - Compile errors mentioning "Send" in user code
  - Errors appear in tokio/async-std internals
  - Works in tests, fails when users try to spawn
### **Detection Pattern**
impl.*Future|async fn.*<T>

## Orphan Tasks

### **Id**
orphan-tasks
### **Summary**
Spawned tasks outlive expected scope, leak or panic
### **Severity**
high
### **Situation**
Spawning background tasks
### **Why**
  tokio::spawn() detaches the task. If you don't await the JoinHandle,
  the task runs independently. It might panic (silently ignored) or
  outlive the main task, accessing dropped resources.
  
### **Solution**
  1. Always track JoinHandles:
     // BAD - fire and forget
     tokio::spawn(async { do_work().await });
  
     // GOOD - track handle
     let handle = tokio::spawn(async { do_work().await });
     // ... later
     handle.await??;  // Propagate panics and errors
  
  2. Use TaskTracker for groups:
     use tokio_util::task::TaskTracker;
  
     let tracker = TaskTracker::new();
     for i in 0..10 {
         tracker.spawn(async move { work(i).await });
     }
     tracker.close();
     tracker.wait().await;  // Wait for all
  
  3. Use structured concurrency patterns:
     // Tasks tied to scope
     async fn scoped_work() {
         let (a, b) = tokio::join!(
             async { work_a().await },
             async { work_b().await }
         );
     }
  
### **Symptoms**
  - Tasks silently fail
  - Resources accessed after drop
  - Shutdown hangs waiting for tasks
### **Detection Pattern**
tokio::spawn\([^)]+\);|spawn\([^)]+\)(?!\.await)

## Refcell Runtime Borrow

### **Id**
refcell-runtime-borrow
### **Summary**
RefCell borrows panic at runtime, defeating borrow checker
### **Severity**
medium
### **Situation**
Using RefCell for interior mutability
### **Why**
  RefCell moves borrow checking to runtime. If you borrow_mut() while
  a borrow() is active, it panics. This defeats the purpose of Rust's
  compile-time safety.
  
### **Solution**
  1. Prefer compile-time alternatives:
     // Instead of RefCell, consider:
     // - Restructure to avoid shared mutable state
     // - Use Cell for Copy types
     // - Use Mutex/RwLock for multi-threaded
  
  2. If RefCell is necessary, use try_borrow:
     // BAD - panics on conflict
     let val = cell.borrow();
     let mut val2 = cell.borrow_mut();  // PANIC!
  
     // BETTER - handle gracefully
     match cell.try_borrow_mut() {
         Ok(mut val) => { /* use val */ }
         Err(_) => { /* handle conflict */ }
     }
  
  3. Keep borrow scopes minimal:
     // BAD - long borrow
     let borrowed = cell.borrow();
     do_lots_of_work(&borrowed);  // Blocks others
  
     // GOOD - short borrow
     let value = cell.borrow().clone();
     do_lots_of_work(&value);
  
### **Symptoms**
  - Runtime panics on borrow
  - "Already borrowed" errors
  - Panics only under specific call patterns
### **Detection Pattern**
RefCell|borrow_mut.*borrow|borrow.*borrow_mut