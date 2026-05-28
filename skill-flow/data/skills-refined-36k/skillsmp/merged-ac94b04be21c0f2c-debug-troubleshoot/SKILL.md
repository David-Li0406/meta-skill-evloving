---
name: debug-troubleshoot
description: Use this skill when diagnosing runtime issues, performance problems, async deadlocks, database connection issues, or panics in Rust async code with Tokio, Turso, and redb.
---

# Debug and Troubleshoot

Systematic debugging approach for Rust async code with Tokio, Turso, and redb.

## Quick Reference

- **[Logging](logging.md)** - Tracing and log configuration
- **[Tokio Console](tokio-console.md)** - Async task debugging
- **[Common Issues](issues.md)** - Common problems and fixes
- **[Techniques](techniques.md)** - Debugging techniques

## When to Use

- Diagnosing runtime issues
- Performance problems
- Async deadlocks
- Database connection issues
- Panics and crashes

## Debugging Tools

1. **Logging** - Tracing with RUST_LOG levels
   - Setup logging with tracing:
   ```rust
   use tracing::{debug, info, warn, error, instrument};

   #[instrument]
   async fn problematic_function(id: &str) -> Result<Data> {
       debug!("Starting operation for id: {}", id);
       // Function implementation...
   }
   ```
   - Run with different logging levels:
   ```bash
   RUST_LOG=info cargo run
   RUST_LOG=debug cargo run
   RUST_LOG=trace cargo run
   ```

2. **Console Debugging** - Use Tokio Console for async task inspection.
   - Enable console subscriber in `Cargo.toml`:
   ```toml
   [dependencies]
   tokio = { version = "1", features = ["full", "tracing"] }
   console-subscriber = "0.1"
   ```
   - Run the application and console in separate terminals.

3. **LLDB/GDB Debugger** - Use for step-by-step debugging.
   ```bash
   cargo build
   rust-lldb target/debug/memory-core
   ```

## Common Issues

### 1. Async Deadlocks
- Symptoms: Program hangs, high CPU usage.
- Diagnosis: Use timeouts to detect hangs.
  
### 2. Database Connection Issues
- Check Turso connection health and handle redb lock issues.

### 3. Memory Leaks
- Detect with Valgrind and avoid circular references.

### 4. Performance Issues
- Profile with Flamegraph and identify common bottlenecks.

### 5. Panic Debugging
- Get full backtrace and add panic hooks for better error handling.

## Debugging Workflow

1. **Reproduce the Issue** - Create a minimal reproduction.
2. **Add Instrumentation** - Use logging to trace execution.
3. **Run with Logging** - Capture logs for analysis.
4. **Analyze Logs** - Look for patterns and timing issues.
5. **Form Hypothesis** - Identify potential causes.
6. **Test Hypothesis** - Add specific logging and assertions.
7. **Fix and Verify** - Implement fixes and ensure no new issues arise.

## Troubleshooting Checklist

- [ ] Can you reproduce the issue?
- [ ] Is it in production, test, or both?
- [ ] Recent changes related to the issue?
- [ ] Error messages or panics?
- [ ] Logs show expected flow?
- [ ] Performance degradation?
- [ ] Resource usage (CPU, memory, connections)?
- [ ] External dependencies healthy?
- [ ] Database connections working?
- [ ] Locks or deadlocks?
- [ ] Async tasks completing?