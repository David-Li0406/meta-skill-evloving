# Java 线程基础详解

## 一、线程基本概念

### 1.1 进程与线程的区别

| 特性 | 进程 | 线程 |
|------|------|------|
| 定义 | 资源分配的最小单位 | CPU调度的最小单位 |
| 内存空间 | 独立的地址空间 | 共享进程的地址空间 |
| 资源拥有 | 拥有独立的系统资源 | 共享进程的资源，仅拥有一点必不可少的资源（PC、栈、寄存器） |
| 开销 | 创建/切换开销大 | 创建/切换开销小 |
| 通信 | 进程间通信（IPC）复杂 | 线程间通信简单（共享内存） |
| 健壮性 | 进程间互不影响，更健壮 | 一个线程崩溃可能导致整个进程崩溃 |

### 1.2 并行与并发

- **并发（Concurrency）**：指两个或多个事件在**同一个时间段内**发生。在单核CPU中，通过时间片轮转实现。
- **并行（Parallelism）**：指两个或多个事件在**同一时刻**发生。需要多核CPU支持。

---

## 二、创建线程的四种方式

### 2.1 继承 Thread 类

```java
public class MyThread extends Thread {
    @Override
    public void run() {
        System.out.println("继承Thread类创建线程: " + Thread.currentThread().getName());
    }

    public static void main(String[] args) {
        new MyThread().start();
    }
}
```
**特点**：
- 简单直接
- 无法继承其他类（Java单继承限制）
- 每个任务需要一个对象，不适合资源共享

### 2.2 实现 Runnable 接口

```java
public class MyRunnable implements Runnable {
    @Override
    public void run() {
        System.out.println("实现Runnable接口创建线程: " + Thread.currentThread().getName());
    }

    public static void main(String[] args) {
        // 可以被多个线程共享
        MyRunnable task = new MyRunnable();
        new Thread(task).start();
        new Thread(task).start();
    }
}
```
**特点**：
- 避免了单继承限制
- 适合资源共享（多个线程处理同一个任务）
- 代码与线程控制解耦

### 2.3 实现 Callable 接口

```java
public class MyCallable implements Callable<String> {
    @Override
    public String call() throws Exception {
        System.out.println("实现Callable接口创建线程: " + Thread.currentThread().getName());
        return "Success";
    }

    public static void main(String[] args) throws ExecutionException, InterruptedException {
        FutureTask<String> futureTask = new FutureTask<>(new MyCallable());
        new Thread(futureTask).start();
        
        // 获取返回值（会阻塞直到完成）
        String result = futureTask.get();
        System.out.println("返回值: " + result);
    }
}
```
**特点**：
- 可以有返回值
- 可以抛出检查异常
- 需要配合 FutureTask 使用

### 2.4 使用线程池

```java
public class ThreadPoolDemo {
    public static void main(String[] args) {
        ExecutorService executor = Executors.newFixedThreadPool(2);
        
        executor.execute(() -> {
            System.out.println("线程池创建线程: " + Thread.currentThread().getName());
        });
        
        executor.shutdown();
    }
}
```
**特点**：
- 复用线程，降低资源消耗
- 提高响应速度
- 统一管理线程

---

## 三、线程生命周期

### 3.1 六种状态（Java）

```java
public enum State {
    NEW,            // 新建
    RUNNABLE,       // 可运行（包括运行中和就绪）
    BLOCKED,        // 阻塞（等待锁）
    WAITING,        // 无限等待（wait/join/park）
    TIMED_WAITING,  // 限时等待（sleep/wait(t)/join(t)）
    TERMINATED      // 终止
}
```

### 3.2 状态转换图

```
      new Thread()           start()
[NEW] ───────────────> [RUNNABLE] <──────────────────┐
                          │  │                       │
           获取到锁        │  │ yield() / CPU时间片耗尽 │
       ┌──────────────────┘  │                       │
       │                     │ notify() / notifyAll()│
       │        synchronized │                       │
       ▼                     ▼                       │
   [BLOCKED] <───────── [WAITING] ───────────────────┘
       │     wait()          │
       │                     │ sleep(t) / wait(t)
       │                     ▼
       └─────────── [TIMED_WAITING] 
                     RUNNABLE 执行完毕 / 异常
[TERMINATED] <────────────────┘
```

---

## 四、线程常用方法

### 4.1 sleep() vs wait()

| 特性 | sleep() | wait() |
|------|---------|--------|
| 所属类 | Thread | Object |
| 锁释放 | **不释放锁** | **释放锁** |
| 使用场景 | 任何地方 | 同步代码块/同步方法 |
| 唤醒方式 | 时间到自动唤醒 | notify()/notifyAll() 或时间到 |
| 异常 | InterruptedException | InterruptedException |

### 4.2 start() vs run()

- **start()**：启动新线程，JVM 调用该线程的 run() 方法。
- **run()**：普通方法调用，不会启动新线程，在当前线程执行。

### 4.3 join()

等待该线程终止。
```java
Thread t1 = new Thread(() -> System.out.println("t1 done"));
t1.start();
t1.join(); // 主线程等待t1执行完才继续
System.out.println("main done");
```
**原理**：内部调用 wait() 方法等待。

### 4.4 yield()

提示调度器当前线程愿意放弃 CPU 使用权，但调度器可以忽略。
状态从 Running 变为 Runnable（就绪）。

### 4.5 interrupt()

中断线程。
- 如果线程阻塞（sleep/wait/join），会抛出 `InterruptedException` 并清除中断状态。
- 如果线程正常运行，只设置中断标志位，线程需手动检查 `isInterrupted()`。

---

## 五、线程安全与通信

### 5.1 线程通信方式
1. **volatile**：保证内存可见性
2. **synchronized + wait/notify**：等待通知机制
3. **Lock + Condition**：更灵活的等待通知
4. **CountDownLatch / CyclicBarrier**：并发工具类
5. **BlockingQueue**：阻塞队列
6. **Pipe**：管道流

### 5.2 守护线程 (Daemon Thread)

- **用户线程**：主要的工作线程。
- **守护线程**：服务于用户线程（如 GC 线程）。
- **特点**：当所有用户线程结束，JVM 退出，不管守护线程是否结束。

```java
Thread t = new Thread();
t.setDaemon(true); // 必须在 start() 之前设置
t.start();
```

---

## 六、常见面试题

### 1. 为什么不建议使用 stop() 方法停止线程？
**答**：`stop()` 方法是废弃的（Deprecated）。它会强制终止线程，导致：
- 立即释放所有锁，可能导致数据不一致（数据破坏）。
- 无法完成清理工作（如关闭资源）。
**正确做法**：使用中断机制 `interrupt()` 配合标志位停止线程。

### 2. run() 方法可以抛出异常吗？
**答**：`run()` 方法不支持 `throws` 检查异常，必须在方法内部 `try-catch` 处理。
但可以抛出运行时异常（RuntimeException），这会导致线程终止。
可以使用 `UncaughtExceptionHandler` 捕获未处理异常。

### 3. wait() 为什么要放在循环中？
**答**：防止**虚假唤醒**（Spurious Wakeup）。
在多线程环境下，线程可能在没有收到 notify 的情况下醒来，或者条件在唤醒后被其他线程改变。使用 while 循环可以再次检查条件。
```java
synchronized (obj) {
    while (condition) {
        obj.wait();
    }
    // do logic
}
```

### 4. Java 中 notify() 和 notifyAll() 有什么区别？
**答**：
- `notify()`：随机唤醒一个等待该锁的线程。
- `notifyAll()`：唤醒所有等待该锁的线程。
通常建议使用 `notifyAll()` 防止信号丢失（即唤醒了错误的线程，而正确的线程还在等待）。

### 5. Thread.sleep(0) 有什么用？
**答**：触发操作系统重新进行一次 CPU 竞争。可以让优先级较低的线程有机会执行，或者作为一种让出 CPU 的手段（类似 yield）。
