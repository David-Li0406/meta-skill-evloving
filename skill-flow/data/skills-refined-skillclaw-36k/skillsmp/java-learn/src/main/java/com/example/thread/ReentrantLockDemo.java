package com.example.thread;

import java.util.concurrent.locks.ReentrantLock;
import java.util.concurrent.locks.Condition;
import java.util.concurrent.locks.ReentrantReadWriteLock;
import java.util.concurrent.TimeUnit;
import java.util.LinkedList;
import java.util.Queue;

/**
 * ReentrantLock 与 AQS 使用示例
 * 
 * ReentrantLock 是基于 AQS (AbstractQueuedSynchronizer) 实现的可重入锁。
 * 
 * 核心知识点：
 * 1. ReentrantLock 基本使用
 * 2. 公平锁 vs 非公平锁
 * 3. Condition 条件变量
 * 4. ReentrantReadWriteLock 读写锁
 * 5. 锁的可中断、超时获取
 * 
 * @author java_learn
 */
public class ReentrantLockDemo {

    private static String repeat(String s, int count) {
        StringBuilder sb = new StringBuilder(s.length() * count);
        for (int i = 0; i < count; i++) {
            sb.append(s);
        }
        return sb.toString();
    }
    
    // ==================== 1. 基本使用 ====================
    
    /**
     * ReentrantLock 基本使用
     */
    public static class BasicUsage {
        private final ReentrantLock lock = new ReentrantLock();
        private int count = 0;
        
        public void increment() {
            lock.lock();  // 获取锁
            try {
                count++;
                System.out.println(Thread.currentThread().getName() + 
                    " 增加后: " + count);
            } finally {
                lock.unlock();  // 必须在 finally 中释放锁
            }
        }
        
        public int getCount() {
            lock.lock();
            try {
                return count;
            } finally {
                lock.unlock();
            }
        }
        
        public static void demo() throws InterruptedException {
            System.out.println("【1. ReentrantLock 基本使用】");
            System.out.println(repeat("-", 50));
            
            BasicUsage counter = new BasicUsage();
            
            Thread t1 = new Thread(() -> {
                for (int i = 0; i < 3; i++) {
                    counter.increment();
                }
            }, "Thread-A");
            
            Thread t2 = new Thread(() -> {
                for (int i = 0; i < 3; i++) {
                    counter.increment();
                }
            }, "Thread-B");
            
            t1.start();
            t2.start();
            t1.join();
            t2.join();
            
            System.out.println("最终计数: " + counter.getCount());
            System.out.println();
        }
    }
    
    // ==================== 2. 可重入性演示 ====================
    
    /**
     * 可重入性演示
     */
    public static class ReentrantDemo {
        private final ReentrantLock lock = new ReentrantLock();
        
        public void outer() {
            lock.lock();
            try {
                System.out.println("外层方法获取锁，持有次数: " + lock.getHoldCount());
                inner();  // 调用内层方法，再次获取同一把锁
            } finally {
                lock.unlock();
            }
        }
        
        public void inner() {
            lock.lock();  // 同一线程可以再次获取锁
            try {
                System.out.println("内层方法获取锁，持有次数: " + lock.getHoldCount());
            } finally {
                lock.unlock();
            }
        }
        
        public static void demo() {
            System.out.println("【2. 可重入性演示】");
            System.out.println(repeat("-", 50));
            
            ReentrantDemo demo = new ReentrantDemo();
            demo.outer();
            
            System.out.println("释放后持有次数: " + demo.lock.getHoldCount());
            System.out.println();
        }
    }
    
    // ==================== 3. 公平锁 vs 非公平锁 ====================
    
    /**
     * 公平锁与非公平锁对比
     */
    public static class FairLockDemo {
        
        public static void demo() throws InterruptedException {
            System.out.println("【3. 公平锁 vs 非公平锁】");
            System.out.println(repeat("-", 50));
            
            // 非公平锁（默认）
            System.out.println("非公平锁测试：");
            testLock(new ReentrantLock(false));
            
            Thread.sleep(100);
            
            // 公平锁
            System.out.println("\n公平锁测试：");
            testLock(new ReentrantLock(true));
            
            System.out.println("\n公平锁 vs 非公平锁：");
            System.out.println("  非公平锁：新线程可能抢占等待队列中线程的锁，吞吐量高");
            System.out.println("  公平锁：严格按等待顺序获取锁，避免饥饿，但性能较低");
            System.out.println();
        }
        
        private static void testLock(ReentrantLock lock) throws InterruptedException {
            Runnable task = () -> {
                for (int i = 0; i < 2; i++) {
                    lock.lock();
                    try {
                        System.out.println("  " + Thread.currentThread().getName() + " 获取锁");
                        Thread.sleep(10);
                    } catch (InterruptedException e) {
                        e.printStackTrace();
                    } finally {
                        lock.unlock();
                    }
                }
            };
            
            Thread t1 = new Thread(task, "T1");
            Thread t2 = new Thread(task, "T2");
            Thread t3 = new Thread(task, "T3");
            
            t1.start();
            t2.start();
            t3.start();
            
            t1.join();
            t2.join();
            t3.join();
        }
    }
    
    // ==================== 4. Condition 条件变量 ====================
    
    /**
     * 使用 Condition 实现生产者-消费者模式
     */
    public static class ProducerConsumer {
        private final ReentrantLock lock = new ReentrantLock();
        private final Condition notFull = lock.newCondition();   // 队列不满条件
        private final Condition notEmpty = lock.newCondition();  // 队列不空条件
        
        private final Queue<Integer> queue = new LinkedList<>();
        private final int capacity = 5;
        
        public void produce(int value) throws InterruptedException {
            lock.lock();
            try {
                // 队列满，等待消费者消费
                while (queue.size() == capacity) {
                    System.out.println("[生产者] 队列已满，等待...");
                    notFull.await();
                }
                
                queue.offer(value);
                System.out.println("[生产者] 生产: " + value + ", 队列大小: " + queue.size());
                
                // 通知消费者
                notEmpty.signal();
                
            } finally {
                lock.unlock();
            }
        }
        
        public int consume() throws InterruptedException {
            lock.lock();
            try {
                // 队列空，等待生产者生产
                while (queue.isEmpty()) {
                    System.out.println("[消费者] 队列为空，等待...");
                    notEmpty.await();
                }
                
                int value = queue.poll();
                System.out.println("[消费者] 消费: " + value + ", 队列大小: " + queue.size());
                
                // 通知生产者
                notFull.signal();
                
                return value;
                
            } finally {
                lock.unlock();
            }
        }
        
        public static void demo() throws InterruptedException {
            System.out.println("【4. Condition 条件变量 - 生产者消费者】");
            System.out.println(repeat("-", 50));
            
            ProducerConsumer pc = new ProducerConsumer();
            
            // 生产者线程
            Thread producer = new Thread(() -> {
                try {
                    for (int i = 1; i <= 8; i++) {
                        pc.produce(i);
                        Thread.sleep(100);
                    }
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }, "Producer");
            
            // 消费者线程
            Thread consumer = new Thread(() -> {
                try {
                    for (int i = 1; i <= 8; i++) {
                        pc.consume();
                        Thread.sleep(200);
                    }
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }, "Consumer");
            
            producer.start();
            consumer.start();
            producer.join();
            consumer.join();
            
            System.out.println();
        }
    }
    
    // ==================== 5. 可中断锁 ====================
    
    /**
     * 可中断锁获取
     */
    public static class InterruptibleLock {
        private final ReentrantLock lock = new ReentrantLock();
        
        public static void demo() throws InterruptedException {
            System.out.println("【5. 可中断锁获取】");
            System.out.println(repeat("-", 50));
            
            ReentrantLock lock = new ReentrantLock();
            
            // 线程1持有锁
            Thread t1 = new Thread(() -> {
                lock.lock();
                try {
                    System.out.println("T1 获取到锁，持有 3 秒...");
                    Thread.sleep(3000);
                } catch (InterruptedException e) {
                    System.out.println("T1 被中断");
                } finally {
                    lock.unlock();
                    System.out.println("T1 释放锁");
                }
            }, "T1");
            
            // 线程2尝试获取锁，可被中断
            Thread t2 = new Thread(() -> {
                try {
                    System.out.println("T2 尝试获取锁 (可中断)...");
                    lock.lockInterruptibly();  // 可中断的锁获取
                    try {
                        System.out.println("T2 获取到锁");
                    } finally {
                        lock.unlock();
                    }
                } catch (InterruptedException e) {
                    System.out.println("T2 等待锁时被中断！");
                }
            }, "T2");
            
            t1.start();
            Thread.sleep(100);  // 确保 T1 先获取锁
            t2.start();
            Thread.sleep(500);
            
            // 中断 T2
            System.out.println("主线程中断 T2...");
            t2.interrupt();
            
            t1.join();
            t2.join();
            System.out.println();
        }
    }
    
    // ==================== 6. 超时获取锁 ====================
    
    /**
     * 超时获取锁
     */
    public static class TryLockDemo {
        
        public static void demo() throws InterruptedException {
            System.out.println("【6. 超时获取锁】");
            System.out.println(repeat("-", 50));
            
            ReentrantLock lock = new ReentrantLock();
            
            // 线程1持有锁
            Thread t1 = new Thread(() -> {
                lock.lock();
                try {
                    System.out.println("T1 获取到锁，持有 2 秒...");
                    Thread.sleep(2000);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                } finally {
                    lock.unlock();
                    System.out.println("T1 释放锁");
                }
            }, "T1");
            
            // 线程2 超时获取锁
            Thread t2 = new Thread(() -> {
                try {
                    System.out.println("T2 尝试获取锁，超时时间 1 秒...");
                    // tryLock 返回是否成功获取锁
                    if (lock.tryLock(1, TimeUnit.SECONDS)) {
                        try {
                            System.out.println("T2 获取到锁");
                        } finally {
                            lock.unlock();
                        }
                    } else {
                        System.out.println("T2 获取锁超时，执行其他逻辑...");
                    }
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }, "T2");
            
            t1.start();
            Thread.sleep(100);
            t2.start();
            
            t1.join();
            t2.join();
            System.out.println();
        }
    }
    
    // ==================== 7. 读写锁 ====================
    
    /**
     * ReentrantReadWriteLock 读写锁
     */
    public static class ReadWriteLockDemo {
        private final ReentrantReadWriteLock rwLock = new ReentrantReadWriteLock();
        private final ReentrantReadWriteLock.ReadLock readLock = rwLock.readLock();
        private final ReentrantReadWriteLock.WriteLock writeLock = rwLock.writeLock();
        
        private int data = 0;
        
        public int read() {
            readLock.lock();
            try {
                System.out.println(Thread.currentThread().getName() + 
                    " 读取数据: " + data);
                Thread.sleep(100);
                return data;
            } catch (InterruptedException e) {
                throw new RuntimeException(e);
            } finally {
                readLock.unlock();
            }
        }
        
        public void write(int value) {
            writeLock.lock();
            try {
                System.out.println(Thread.currentThread().getName() + 
                    " 写入数据: " + value);
                data = value;
                Thread.sleep(100);
            } catch (InterruptedException e) {
                throw new RuntimeException(e);
            } finally {
                writeLock.unlock();
            }
        }
        
        public static void demo() throws InterruptedException {
            System.out.println("【7. 读写锁 ReentrantReadWriteLock】");
            System.out.println(repeat("-", 50));
            System.out.println("特点：读读共享，读写互斥，写写互斥");
            System.out.println();
            
            ReadWriteLockDemo demo = new ReadWriteLockDemo();
            
            // 多个读线程可以同时读
            Thread r1 = new Thread(() -> demo.read(), "Reader-1");
            Thread r2 = new Thread(() -> demo.read(), "Reader-2");
            Thread w1 = new Thread(() -> demo.write(100), "Writer-1");
            Thread r3 = new Thread(() -> demo.read(), "Reader-3");
            
            r1.start();
            r2.start();  // r1 和 r2 可以同时读
            Thread.sleep(50);
            w1.start();  // 写操作会等待读完成
            Thread.sleep(50);
            r3.start();  // r3 会等待写完成
            
            r1.join();
            r2.join();
            w1.join();
            r3.join();
            
            System.out.println();
        }
    }
    
    // ==================== 8. ReentrantLock vs synchronized ====================
    
    public static void comparison() {
        System.out.println("【8. ReentrantLock vs synchronized】");
        System.out.println(repeat("-", 50));
        System.out.println();
        System.out.println("| 特性           | synchronized      | ReentrantLock      |");
        System.out.println("|----------------|-------------------|--------------------|");
        System.out.println("| 锁的获取/释放   | 自动              | 手动(try-finally)   |");
        System.out.println("| 可中断         | 不支持            | 支持                |");
        System.out.println("| 超时获取       | 不支持            | 支持                |");
        System.out.println("| 公平锁         | 不支持            | 支持                |");
        System.out.println("| 条件变量       | 单一(wait/notify) | 多个(Condition)     |");
        System.out.println("| 锁状态查询     | 不支持            | 支持                |");
        System.out.println("| 性能           | JDK6后优化接近    | 高并发略优           |");
        System.out.println();
    }
    
    // ==================== 主方法 ====================
    
    public static void main(String[] args) throws InterruptedException {
        System.out.println("=== ReentrantLock 与 AQS 使用示例 ===\n");
        
        BasicUsage.demo();
        ReentrantDemo.demo();
        FairLockDemo.demo();
        ProducerConsumer.demo();
        InterruptibleLock.demo();
        TryLockDemo.demo();
        ReadWriteLockDemo.demo();
        comparison();
    }
}
