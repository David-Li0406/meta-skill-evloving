# ReentrantLock 与 AQS 详解

## 一、ReentrantLock 简介

`ReentrantLock`（可重入锁）是 JDK 5 引入的，位于 `java.util.concurrent.locks` 包下。
它是一种互斥锁，功能类似于 `synchronized`，但提供了更高级的功能。

**主要特性**：
1. **可重入**：线程可以重复获取已持有的锁。
2. **可中断**：支持 `lockInterruptibly()`，在等待锁时可被中断。
3. **超时获取**：支持 `tryLock(time, unit)`，超时放弃。
4. **公平锁**：支持公平锁（FairSync）和非公平锁（NonFairSync）。
5. **多条件变量**：支持多个 `Condition`，实现精确唤醒。

---

## 二、使用示例

### 2.1 基本用法

```java
public class LockDemo {
    private final Lock lock = new ReentrantLock();

    public void method() {
        lock.lock(); // 获取锁
        try {
            // 业务逻辑
        } finally {
            lock.unlock(); // 必须在 finally 块中释放锁
        }
    }
}
```

### 2.2 公平锁 vs 非公平锁

```java
// 默认是非公平锁 (性能更高)
Lock nonFairLock = new ReentrantLock();

// 创建公平锁 (按请求顺序获取锁)
Lock fairLock = new ReentrantLock(true);
```

### 2.3 Condition 实现等待/通知

```java
public class ConditionDemo {
    private final Lock lock = new ReentrantLock();
    private final Condition condition = lock.newCondition();

    public void await() throws InterruptedException {
        lock.lock();
        try {
            condition.await(); // 释放锁并等待，类似 Object.wait()
        } finally {
            lock.unlock();
        }
    }

    public void signal() {
        lock.lock();
        try {
            condition.signal(); // 唤醒等待线程，类似 Object.notify()
        } finally {
            lock.unlock();
        }
    }
}
```

---

## 三、AQS (AbstractQueuedSynchronizer) 原理

`AQS` 是 Java 并发包的核心基础框架，`ReentrantLock`、`Semaphore`、`CountDownLatch` 都基于它实现。

### 3.1 核心结构

AQS 内部维护了：
1. **state**：volatile int 类型的同步状态。
   - 0 表示无锁
   - >0 表示有锁（重入次数）
2. **CLH 队列**：双向链表，存储等待锁的线程。
   - Head：当前持有锁的节点（或虚节点）
   - Tail：等待队列的尾节点

```java
// AQS 伪代码结构
public abstract class AbstractQueuedSynchronizer {
    private volatile int state;
    private transient volatile Node head;
    private transient volatile Node tail;
    
    // 内部类 Node
    static final class Node {
        volatile Thread thread;
        volatile Node prev;
        volatile Node next;
        volatile int waitStatus; // 节点状态
    }
}
```

### 3.2 ReentrantLock 加锁过程（非公平锁）

1. **CAS 尝试**：尝试将 `state` 从 0 改为 1。
   - 成功：设置当前线程为 ExclusiveOwnerThread。
   - 失败：进入 `acquire(1)`。
2. **acquire(1) 流程**：
   - `tryAcquire(1)`：再次尝试获取锁（包括重入判断）。
   - `addWaiter(Node.EXCLUSIVE)`：封装成 Node 加入队列尾部。
   - `acquireQueued(node, 1)`：自旋等待。
     - 检查前驱节点是否为 Head。
     - 如果是 Head，再次 `tryAcquire`。
     - 如果失败，挂起当前线程 (`LockSupport.park()`)。

### 3.3 释放锁过程

1. `tryRelease(1)`：`state` 减 1。
   - 如果 `state` 变为 0，清空 ExclusiveOwnerThread，返回 true。
2. `unparkSuccessor(h)`：唤醒后继节点。
   - 找到 Head 的下一个有效节点。
   - 调用 `LockSupport.unpark(s.thread)` 唤醒线程。

---

## 四、ReentrantReadWriteLock

`ReentrantReadWriteLock` 维护了一对锁：
- **读锁**（共享锁）：多个线程可以同时获取，适合读多写少。
- **写锁**（独占锁）：同一时刻只能有一个线程获取。

**互斥规则**：
- 读-读：不互斥
- 读-写：互斥
- 写-写：互斥

**锁降级**：
- 写锁可以降级为读锁（持有写锁时获取读锁，然后释放写锁）。
- 读锁**不能**升级为写锁（必须先释放读锁，存在死锁风险）。

```java
public class Cache {
    private final Map<String, Object> map = new HashMap<>();
    private final ReentrantReadWriteLock rwl = new ReentrantReadWriteLock();
    private final Lock r = rwl.readLock();
    private final Lock w = rwl.writeLock();

    public Object get(String key) {
        r.lock();
        try {
            return map.get(key);
        } finally {
            r.unlock();
        }
    }

    public void put(String key, Object value) {
        w.lock();
        try {
            map.put(key, value);
        } finally {
            w.unlock();
        }
    }
}
```

---

## 五、常见面试题

### 1. ReentrantLock 与 synchronized 的区别？
**答**：
- **实现**：synchronized 是 JVM 层面（Monitor），ReentrantLock 是 JDK API 层面（AQS）。
- **功能**：ReentrantLock 功能更丰富（超时、中断、公平锁、Condition）。
- **性能**：JDK 6 以后，synchronized 做了大量优化（偏向/轻量级），两者性能差别不大。
- **释放**：synchronized 自动释放，ReentrantLock 必须手动释放。

### 2. 什么是 AQS？
**答**：
AQS（AbstractQueuedSynchronizer）是一个构建锁和同步器的框架。
它使用一个 volatile int 变量 `state` 表示同步状态，通过 CAS 操作修改 state。
内部维护一个 FIFO 的双向链表（CLH 队列）来管理等待线程。
核心方法是 `acquire`（获取资源）和 `release`（释放资源）。

### 3. 公平锁是如何实现的？
**答**：
在 `tryAcquire` 时，公平锁会先判断队列中是否有前驱节点 (`hasQueuedPredecessors()`)。
如果有线程在排队，当前线程必须加入队列尾部，不能插队。
非公平锁则不检查，直接尝试 CAS 获取锁。

### 4. 读写锁适用什么场景？
**答**：
适用于**读多写少**的并发场景，如缓存系统。
读写锁通过分离读锁和写锁，提高了并发性。
注意：如果写操作过于频繁，可能导致读线程饥饿。
