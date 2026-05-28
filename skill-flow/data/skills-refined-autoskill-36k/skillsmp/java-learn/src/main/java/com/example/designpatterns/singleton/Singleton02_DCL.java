package com.example.designpatterns.singleton;

/**
 * 双重检查锁定 (Double-Checked Locking) 单例
 * 
 * 特点：
 * 1. 延迟加载 - 第一次调用时才创建实例
 * 2. 线程安全 - 通过双重检查 + synchronized 保证
 * 3. 高效 - 只有第一次创建时需要同步
 * 4. 必须使用 volatile 防止指令重排序
 * 
 * @author java_learn
 */
public class Singleton02_DCL {
    
    /**
     * volatile 关键字的作用：
     * 1. 保证可见性 - 一个线程修改后，其他线程立即可见
     * 2. 禁止指令重排序 - 保证 new 操作的正确顺序
     * 
     * new Singleton02_DCL() 实际上分为三步：
     * 1. 分配内存空间
     * 2. 初始化对象
     * 3. 将引用指向分配的内存
     * 
     * 如果没有 volatile，JVM 可能会将步骤重排序为 1 -> 3 -> 2
     * 导致其他线程获取到未初始化完成的对象
     */
    private static volatile Singleton02_DCL instance;
    
    private Singleton02_DCL() {
        System.out.println("Singleton02_DCL 实例被创建，线程: " + Thread.currentThread().getName());
    }
    
    public static Singleton02_DCL getInstance() {
        // 第一次检查：避免不必要的同步开销
        if (instance == null) {
            // 同步块
            synchronized (Singleton02_DCL.class) {
                // 第二次检查：防止多个线程同时通过第一次检查后创建多个实例
                if (instance == null) {
                    instance = new Singleton02_DCL();
                }
            }
        }
        return instance;
    }
    
    public void showMessage() {
        System.out.println("Hello from Singleton02_DCL!");
    }
    
    // 多线程测试
    public static void main(String[] args) throws InterruptedException {
        System.out.println("=== 双重检查锁定单例 - 多线程测试 ===\n");
        
        // 创建多个线程同时获取单例
        int threadCount = 10;
        Thread[] threads = new Thread[threadCount];
        Singleton02_DCL[] instances = new Singleton02_DCL[threadCount];
        
        for (int i = 0; i < threadCount; i++) {
            final int index = i;
            threads[i] = new Thread(() -> {
                instances[index] = Singleton02_DCL.getInstance();
                System.out.println("线程 " + Thread.currentThread().getName() 
                    + " 获取实例: " + instances[index].hashCode());
            }, "Thread-" + i);
        }
        
        // 启动所有线程
        for (Thread thread : threads) {
            thread.start();
        }
        
        // 等待所有线程完成
        for (Thread thread : threads) {
            thread.join();
        }
        
        // 验证所有线程获取的是否是同一个实例
        System.out.println("\n=== 验证结果 ===");
        boolean allSame = true;
        for (int i = 1; i < threadCount; i++) {
            if (instances[i] != instances[0]) {
                allSame = false;
                break;
            }
        }
        System.out.println("所有线程获取的是同一个实例: " + allSame);
    }
}
