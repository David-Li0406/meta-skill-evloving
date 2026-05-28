# Rust Craftsman - Validations

## Unwrap/Expect in Production Code

### **Id**
unwrap-in-production
### **Severity**
error
### **Type**
regex
### **Pattern**
  - \.unwrap\(\)
  - \.expect\(
### **Message**
Using unwrap/expect in production code. Will panic on None/Err.
### **Fix Action**
Use ? operator or match/if-let for proper error handling
### **Applies To**
  - **/*.rs
### **Excludes**
  - **/tests/**
  - **/test_*.rs
  - **/benches/**

## Sync I/O in Async Context

### **Id**
sync-io-in-async
### **Severity**
error
### **Type**
regex
### **Pattern**
  - std::fs::
  - std::io::BufReader
  - std::net::
  - thread::sleep
### **Message**
Sync I/O in async context blocks the executor.
### **Fix Action**
Use tokio::fs, tokio::io, tokio::net, or tokio::time::sleep
### **Applies To**
  - **/*.rs

## Unbounded Channel

### **Id**
unbounded-channel
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - unbounded_channel
  - crossbeam.*unbounded
### **Message**
Unbounded channels can cause OOM under load.
### **Fix Action**
Use bounded channel with explicit capacity
### **Applies To**
  - **/*.rs

## Lock Held Across Await

### **Id**
lock-across-await
### **Severity**
error
### **Type**
regex
### **Pattern**
  - lock\(\)\.await[^;]*\.await
  - read\(\)\.await[^;]*\.await
  - write\(\)\.await[^;]*\.await
### **Message**
Holding lock across await point can cause deadlock.
### **Fix Action**
Clone data from lock, release lock, then await
### **Applies To**
  - **/*.rs

## Clone in Hot Loop

### **Id**
clone-in-loop
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - for.*\.clone\(\)
  - loop.*\.clone\(\)
  - while.*\.clone\(\)
### **Message**
Cloning in loop may cause unnecessary allocations.
### **Fix Action**
Consider borrowing or moving data instead
### **Applies To**
  - **/*.rs

## Format String in Loop

### **Id**
format-in-loop
### **Severity**
info
### **Type**
regex
### **Pattern**
  - for.*format!
  - loop.*format!
  - while.*format!
### **Message**
format! allocates on each iteration. Consider reusing buffer.
### **Fix Action**
Use write! with reusable String buffer
### **Applies To**
  - **/*.rs

## Panic in Library Code

### **Id**
panic-in-library
### **Severity**
error
### **Type**
regex
### **Pattern**
  - panic!\(
  - todo!\(
  - unimplemented!\(
### **Message**
Library code should not panic. Return Result instead.
### **Fix Action**
Replace with Result<T, Error> return type
### **Applies To**
  - **/lib.rs
  - **/lib/**/*.rs
### **Excludes**
  - **/tests/**

## Box<dyn Error> Return Type

### **Id**
box-dyn-error
### **Severity**
info
### **Type**
regex
### **Pattern**
  - Box<dyn.*Error>
  - Box<dyn.*std::error::Error>
### **Message**
Box<dyn Error> loses type information. Consider custom error type.
### **Fix Action**
Use thiserror for custom error types with proper variants
### **Applies To**
  - **/*.rs

## Async Function Without Send Bound

### **Id**
missing-send-bound
### **Severity**
info
### **Type**
regex
### **Pattern**
  - pub async fn.*<T>(?!.*Send)
  - async fn.*<T>(?!.*Send).*\{
### **Message**
Generic async function may need Send bound for spawn compatibility.
### **Fix Action**
Add T: Send + 'static bound if function will be spawned
### **Applies To**
  - **/*.rs

## Spawned Task Not Awaited

### **Id**
spawn-without-await
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - tokio::spawn\([^)]+\);$
  - spawn\([^)]+\);$
### **Message**
Spawned task JoinHandle is ignored. Errors/panics will be lost.
### **Fix Action**
Store and await JoinHandle, or use TaskTracker
### **Applies To**
  - **/*.rs

## RefCell Borrow Pattern

### **Id**
refcell-borrow-mut
### **Severity**
info
### **Type**
regex
### **Pattern**
  - RefCell.*borrow_mut
### **Message**
RefCell borrow_mut panics if already borrowed. Use try_borrow_mut.
### **Fix Action**
Consider try_borrow_mut or redesign to avoid RefCell
### **Applies To**
  - **/*.rs

## Unsafe Block Without Safety Comment

### **Id**
unsafe-without-comment
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - unsafe\s*\{(?!/)
### **Message**
Unsafe block without SAFETY comment explaining invariants.
### **Fix Action**
Add // SAFETY: comment explaining why this is safe
### **Applies To**
  - **/*.rs

## String in Public API

### **Id**
string-allocation-api
### **Severity**
info
### **Type**
regex
### **Pattern**
  - pub fn.*\(.*: String\)
  - pub async fn.*\(.*: String\)
### **Message**
Taking String forces callers to allocate. Consider &str or impl Into<String>.
### **Fix Action**
Use &str for read-only, impl Into<String> for flexibility
### **Applies To**
  - **/*.rs

## Collect Then Iterate

### **Id**
collect-then-iterate
### **Severity**
info
### **Type**
regex
### **Pattern**
  - collect::<Vec<.*>>.*\.iter\(\)
  - collect::<Vec<.*>>.*\.find\(
  - collect::<Vec<.*>>.*\.filter\(
### **Message**
Collecting then iterating wastes allocation. Use iterator directly.
### **Fix Action**
Remove .collect() and use iterator methods directly
### **Applies To**
  - **/*.rs

## Arc Clone Pattern in Closure

### **Id**
arc-clone-in-closure
### **Severity**
info
### **Type**
regex
### **Pattern**
  - let.*= Arc::clone\(&
### **Message**
Arc::clone in closure - ensure this is intentional for sharing.
### **Fix Action**
Verify Arc is needed, consider borrowing for short-lived uses
### **Applies To**
  - **/*.rs