---
name: java-thread
description: Java 并发与线程池学习（JMM/AQS/实践）
---

# Java 并发学习资料（总纲）

> 目标：能写出线程安全代码、能解释 JMM/锁/线程池原理、能定位死锁/CPU 飙高/内存泄漏（ThreadLocal）。

## 0. 学习路径（对应 java-thread/01~06）
1. `java-thread/01-ThreadBasics.md`：线程基础
2. `java-thread/02-Synchronized.md`：synchronized/volatile/happens-before
3. `java-thread/03-ThreadLocal.md`：ThreadLocal/内存泄漏/线程池场景
4. `java-thread/04-ReentrantLock.md`：AQS/Condition/公平与非公平
5. `java-thread/05-ConcurrentHashMap.md`：并发容器（JDK8）
6. `java-thread/06-ThreadPool.md`：线程池参数/执行流程/治理

---

## 1. 并发基础（01-ThreadBasics）
### 1.1 线程与进程
- 线程是调度单位，进程是资源单位

### 1.2 线程创建方式
- 继承 Thread / 实现 Runnable / Callable+Future
- 线程池（生产推荐）

### 1.3 线程状态（要会画状态图）
- NEW / RUNNABLE / BLOCKED / WAITING / TIMED_WAITING / TERMINATED

### 1.4 线程通信
- `wait/notify/notifyAll`
- `join`
- `LockSupport.park/unpark`

---

## 2. synchronized/volatile/JMM（02-Synchronized）
### 2.1 synchronized 解决什么
- 原子性 + 可见性 + 有序性（互斥带来的）

### 2.2 锁升级（了解思路）
- 偏向锁（JDK8 默认曾开启，后续版本变化）
- 轻量级锁
- 重量级锁

### 2.3 volatile 解决什么
- 可见性 + 禁止指令重排（不保证复合操作原子性）

### 2.4 happens-before
- 程序顺序规则、volatile 规则、监视器锁规则、线程启动/结束规则等

---

## 3. ThreadLocal（03-ThreadLocal）
### 3.1 适用场景
- 线程隔离上下文：traceId、用户上下文（注意线程池）

### 3.2 关键实现
- ThreadLocalMap：key 是弱引用，value 是强引用

### 3.3 内存泄漏与正确姿势
- 线程池复用线程 → value 可能长期存活
- 最佳实践：`try { set } finally { remove }`

---

## 4. ReentrantLock & AQS（04-ReentrantLock）
### 4.1 为什么需要
- 可中断锁、可限时、可公平、Condition 多队列

### 4.2 AQS 核心
- state + CLH 队列（FIFO）
- 独占/共享

### 4.3 Condition
- await/signal 的条件队列

---

## 5. 并发容器（05-ConcurrentHashMap）
### 5.1 JDK8 CHM 思路
- CAS + synchronized（桶级别），Node/TreeBin

### 5.2 size 统计
- baseCount + CounterCell（分片累加）

---

## 6. 线程池（06-ThreadPool）
### 6.1 为什么建议用线程池
- 复用线程、控制并发、统一治理

### 6.2 核心参数
- corePoolSize / maximumPoolSize / keepAliveTime
- workQueue
- threadFactory
- rejectedExecutionHandler

### 6.3 执行流程（面试必会）
- 先 core → 再 queue → 再 max → 最后 reject

### 6.4 常见问题
- OOM：无界队列 + 提交过快
- 线程打满：慢任务/下游抖动
- 拒绝策略：CallerRuns vs Abort 等选型

---

## 7. 生产排错速查
- CPU 飙高：`top`/任务管理器 → `jstack` 找热点线程
- 死锁：`jstack` 直接提示 deadlock
- 频繁 Full GC：结合 `jstat` + GC log
- ThreadLocal 泄漏：线程池 + 忘记 remove

---

## 8. 可运行示例代码索引（对应 src/main/java）
- 线程池示例：`src/main/java/com/example/thread/ThreadPoolDemo.java`
- ThreadLocal 示例：`src/main/java/com/example/thread/ThreadLocalDemo.java`
- ReentrantLock 示例：`src/main/java/com/example/thread/ReentrantLockDemo.java`

---

## 9. 高频面试题
1. 线程状态有哪些？WAITING 与 BLOCKED 区别？
2. synchronized 与 ReentrantLock 区别？公平锁是否一定更好？
3. volatile 能不能保证 i++ 线程安全？为什么？
4. ThreadLocal 为什么 key 用弱引用？value 为什么会泄漏？
5. 线程池的执行流程？为什么不建议 Executors.newFixedThreadPool？
