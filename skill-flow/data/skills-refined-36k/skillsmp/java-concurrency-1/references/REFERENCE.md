# Java Concurrency References

## References

- [**Executor Patterns**](executor-patterns.md) - Thread pool sizing, configuration, graceful shutdown
- [**CompletableFuture**](completable-future.md) - Async composition, error handling, timeouts
- [**Virtual Threads**](virtual-threads.md) - Java 21+ patterns, when to use, pitfalls

## Quick Checks

- [ ] Use ExecutorService over raw Thread creation
- [ ] Size thread pools appropriately (CPU-bound: cores, I/O-bound: higher)
- [ ] Always shutdown executors in finally/try-with-resources
- [ ] Handle InterruptedException - restore interrupt status
- [ ] Use virtual threads for I/O-bound tasks (Java 21+)
- [ ] Prefer immutability over synchronization
- [ ] Use AtomicXxx for simple counters, Lock for complex critical sections
