# Executor Patterns

## Thread Pool Sizing

```java
// CPU-bound tasks: cores or cores + 1
int cpuBound = Runtime.getRuntime().availableProcessors();

// I/O-bound tasks: cores * (1 + wait/compute ratio)
// If tasks spend 80% waiting: cores * 5
int ioBound = cpuBound * 5;

// Mixed workloads: separate pools
ExecutorService cpuPool = Executors.newFixedThreadPool(cpuBound);
ExecutorService ioPool = Executors.newFixedThreadPool(ioBound);
```

## Custom Thread Pool

```java
// Production-ready configuration
ThreadPoolExecutor executor = new ThreadPoolExecutor(
    4,                              // corePoolSize
    16,                             // maximumPoolSize
    60L, TimeUnit.SECONDS,          // keepAliveTime
    new LinkedBlockingQueue<>(1000), // workQueue with bounded capacity
    new ThreadFactoryBuilder()
        .setNameFormat("worker-%d")
        .setUncaughtExceptionHandler((t, e) -> log.error("Thread {} failed", t, e))
        .build(),
    new ThreadPoolExecutor.CallerRunsPolicy()  // backpressure
);

// Allow core threads to timeout (saves resources when idle)
executor.allowCoreThreadTimeOut(true);

// Pre-start core threads (faster initial response)
executor.prestartAllCoreThreads();
```

## Rejection Policies

```java
// AbortPolicy (default) - throws RejectedExecutionException
new ThreadPoolExecutor.AbortPolicy()

// CallerRunsPolicy - caller thread executes the task (backpressure)
new ThreadPoolExecutor.CallerRunsPolicy()

// DiscardPolicy - silently discards
new ThreadPoolExecutor.DiscardPolicy()

// DiscardOldestPolicy - discards oldest waiting task
new ThreadPoolExecutor.DiscardOldestPolicy()

// Custom policy
RejectedExecutionHandler custom = (r, executor) -> {
    log.warn("Task rejected, queue full: {}", executor.getQueue().size());
    // Maybe save to database for later processing
    taskRepository.save(r);
};
```

## Graceful Shutdown

```java
public void shutdown(ExecutorService executor) {
    executor.shutdown();  // No new tasks accepted

    try {
        // Wait for existing tasks to complete
        if (!executor.awaitTermination(30, TimeUnit.SECONDS)) {
            log.warn("Executor did not terminate in time, forcing shutdown");
            List<Runnable> pending = executor.shutdownNow();
            log.warn("{} tasks were cancelled", pending.size());

            // Wait again for tasks to respond to interrupt
            if (!executor.awaitTermination(10, TimeUnit.SECONDS)) {
                log.error("Executor did not terminate");
            }
        }
    } catch (InterruptedException e) {
        executor.shutdownNow();
        Thread.currentThread().interrupt();
    }
}

// With lifecycle hook (Spring)
@PreDestroy
public void cleanup() {
    shutdown(executor);
}
```

## Scheduled Executor

```java
ScheduledExecutorService scheduler = Executors.newScheduledThreadPool(2);

// One-time delay
scheduler.schedule(() -> sendReminder(), 1, TimeUnit.HOURS);

// Fixed rate (starts every N seconds, regardless of duration)
scheduler.scheduleAtFixedRate(
    () -> collectMetrics(),
    0,                    // initial delay
    30, TimeUnit.SECONDS  // period
);

// Fixed delay (N seconds after previous completion)
scheduler.scheduleWithFixedDelay(
    () -> processQueue(),
    0,                    // initial delay
    5, TimeUnit.SECONDS   // delay between end and next start
);

// Handle exceptions in scheduled tasks
scheduler.scheduleAtFixedRate(() -> {
    try {
        riskyOperation();
    } catch (Exception e) {
        log.error("Scheduled task failed", e);
        // Don't rethrow - task would stop repeating
    }
}, 0, 1, TimeUnit.MINUTES);
```

## Fork/Join Pool

```java
// For recursive divide-and-conquer tasks
ForkJoinPool forkJoinPool = new ForkJoinPool(
    Runtime.getRuntime().availableProcessors()
);

class SumTask extends RecursiveTask<Long> {
    private final long[] array;
    private final int start, end;
    private static final int THRESHOLD = 10_000;

    @Override
    protected Long compute() {
        if (end - start <= THRESHOLD) {
            return computeDirectly();
        }

        int mid = (start + end) / 2;
        SumTask left = new SumTask(array, start, mid);
        SumTask right = new SumTask(array, mid, end);

        left.fork();  // async
        long rightResult = right.compute();  // sync
        long leftResult = left.join();  // wait

        return leftResult + rightResult;
    }
}

Long result = forkJoinPool.invoke(new SumTask(array, 0, array.length));
```

## Monitoring

```java
// Get metrics from ThreadPoolExecutor
ThreadPoolExecutor executor = (ThreadPoolExecutor) Executors.newFixedThreadPool(4);

int activeCount = executor.getActiveCount();
long completedTasks = executor.getCompletedTaskCount();
int queueSize = executor.getQueue().size();
int poolSize = executor.getPoolSize();

// Expose via metrics library
meterRegistry.gauge("executor.active", executor, ThreadPoolExecutor::getActiveCount);
meterRegistry.gauge("executor.queue.size", executor, e -> e.getQueue().size());
```
