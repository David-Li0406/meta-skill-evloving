# Java 线程池详解

## 一、为什么使用线程池

1. **降低资源消耗**：通过重复利用已创建的线程，降低线程创建和销毁造成的消耗。
2. **提高响应速度**：当任务到达时，任务可以不需要等待线程创建就能立即执行。
3. **提高线程的可管理性**：线程是稀缺资源，如果无限制地创建，不仅会消耗系统资源，还会降低系统的稳定性，使用线程池可以进行统一分配、调优和监控。

---

## 二、ThreadPoolExecutor 核心参数

```java
public ThreadPoolExecutor(int corePoolSize,
                          int maximumPoolSize,
                          long keepAliveTime,
                          TimeUnit unit,
                          BlockingQueue<Runnable> workQueue,
                          ThreadFactory threadFactory,
                          RejectedExecutionHandler handler)
```

| 参数名 | 含义 |
|--------|------|
| **corePoolSize** | 核心线程数（即使空闲也不会被销毁） |
| **maximumPoolSize** | 最大线程数（核心线程 + 非核心线程） |
| **keepAliveTime** | 非核心线程空闲存活时间 |
| **unit** | 时间单位 |
| **workQueue** | 任务队列（当核心线程满了，新任务放入队列） |
| **threadFactory** | 线程工厂（用于创建线程，设置线程名等） |
| **handler** | 拒绝策略（当队列和最大线程数都满了，如何处理新任务） |

---

## 三、线程池工作流程

1. **提交任务**：执行 `execute()`。
2. **核心线程判断**：
   - 如果当前运行的线程数 < `corePoolSize`，则创建新线程执行任务。
   - 否则，进入下一步。
3. **队列判断**：
   - 如果队列未满，将任务加入 `workQueue`。
   - 否则，进入下一步。
4. **最大线程判断**：
   - 如果当前运行的线程数 < `maximumPoolSize`，则创建非核心线程执行任务。
   - 否则，执行拒绝策略。

```
     Submit Task
          │
          ▼
   Running < CoreSize? ──YES──> Create Thread
          │
          NO
          ▼
    Queue Full? ──────NO──────> Add to Queue
          │
          YES
          ▼
   Running < MaxSize? ──YES──> Create Thread
          │
          NO
          ▼
    Reject Strategy
```

---

## 四、常见阻塞队列

| 队列名称 | 特性 |
|----------|------|
| **ArrayBlockingQueue** | 基于数组的有界阻塞队列，FIFO。 |
| **LinkedBlockingQueue** | 基于链表的阻塞队列，默认无界（Integer.MAX_VALUE），FIFO。 |
| **SynchronousQueue** | 不存储元素的阻塞队列，每个插入操作必须等待另一个线程的移除操作。 |
| **PriorityBlockingQueue** | 支持优先级的无界阻塞队列。 |
| **DelayQueue** | 使用优先级队列实现的无界阻塞队列，只有在延迟期满时才能从中提取元素。 |

---

## 五、四种拒绝策略

1. **AbortPolicy** (默认)：直接抛出 `RejectedExecutionException` 异常。
2. **CallerRunsPolicy**：用调用者所在的线程来执行任务。
3. **DiscardOldestPolicy**：丢弃队列中最老的一个任务，并执行当前任务。
4. **DiscardPolicy**：不处理，直接丢弃任务。

---

## 六、Executors 工具类（不推荐生产使用）

虽然 `Executors` 提供了便捷的方法创建线程池，但《阿里巴巴Java开发手册》**禁止**在生产环境使用，原因如下：

1. **FixedThreadPool** 和 **SingleThreadPool**：
   - 允许的请求队列长度为 `Integer.MAX_VALUE`，可能会堆积大量请求，导致 OOM。
2. **CachedThreadPool**：
   - 允许的创建线程数量为 `Integer.MAX_VALUE`，可能会创建大量线程，导致 OOM。

**推荐方式**：手动创建 `ThreadPoolExecutor`。

```java
// 生产环境推荐写法
ThreadPoolExecutor executor = new ThreadPoolExecutor(
    5, // corePoolSize
    10, // maximumPoolSize
    60L, TimeUnit.SECONDS, // keepAliveTime
    new ArrayBlockingQueue<>(100), // workQueue
    new ThreadFactoryBuilder().setNameFormat("demo-pool-%d").build(), // threadFactory (Guava)
    new ThreadPoolExecutor.CallerRunsPolicy() // handler
);
```

---

## 七、线程池状态

1. **RUNNING**：能接受新任务，也能处理队列中的任务。
2. **SHUTDOWN**：不接受新任务，但处理队列中的任务（调用 `shutdown()`）。
3. **STOP**：不接受新任务，也不处理队列中的任务，中断正在执行的任务（调用 `shutdownNow()`）。
4. **TIDYING**：所有任务都已终止，workerCount 为 0。
5. **TERMINATED**：`terminated()` 方法执行完。

---

## 八、常见面试题

### 1. 线程池参数如何设置？
**答**：
- **CPU 密集型任务**（加密、计算）：
  - 线程数 = CPU 核数 + 1
- **IO 密集型任务**（数据库、网络请求）：
  - 线程数 = CPU 核数 * 2
  - 或者：线程数 = CPU 核数 / (1 - 阻塞系数)  (阻塞系数通常 0.8~0.9)

### 2. 线程池是如何复用线程的？
**答**：
线程执行完任务后，不会销毁，而是去队列中获取下一个任务 (`task = workQueue.take()`)。
如果队列为空，核心线程会阻塞等待，非核心线程等待超时后销毁。
核心逻辑在 `runWorker()` 方法的 `while` 循环中。

### 3. submit() 和 execute() 的区别？
**答**：
- **execute()**：提交 Runnable 任务，无返回值。
- **submit()**：提交 Callable 或 Runnable 任务，返回 Future 对象，可以获取执行结果或捕获异常。

### 4. 线程池中线程发生异常怎么处理？
**答**：
- 如果使用 `execute()`，异常会打印到控制台，线程终止，线程池会创建一个新线程代替它。
- 如果使用 `submit()`，异常会被封装在 Future 中，调用 `future.get()` 时才会抛出。
- 建议在任务内部 try-catch 处理异常。
