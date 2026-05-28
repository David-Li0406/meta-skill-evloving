package com.example.thread;

import java.util.concurrent.*;
import java.util.concurrent.atomic.AtomicInteger;

/**
 * 线程池使用示例
 * 
 * 线程池是 Java 并发编程中最重要的组件之一。
 * 
 * 核心知识点：
 * 1. ThreadPoolExecutor 核心参数
 * 2. 四种拒绝策略
 * 3. 线程池工作流程
 * 4. 常见线程池类型
 * 5. 线程池监控
 * 6. 最佳实践
 * 
 * @author java_learn
 */
public class ThreadPoolDemo {

    private static String repeat(String s, int count) {
        StringBuilder sb = new StringBuilder(s.length() * count);
        for (int i = 0; i < count; i++) {
            sb.append(s);
        }
        return sb.toString();
    }
    
    // ==================== 1. ThreadPoolExecutor 核心参数 ====================
    
    /**
     * 演示 ThreadPoolExecutor 的七大参数
     */
    public static class CoreParameters {
        
        public static void demo() {
            System.out.println("【1. ThreadPoolExecutor 七大参数】");
            System.out.println(repeat("-", 50));
            
            /*
             * 参数说明：
             * 1. corePoolSize: 核心线程数（常驻线程）
             * 2. maximumPoolSize: 最大线程数
             * 3. keepAliveTime: 空闲线程存活时间
             * 4. unit: 时间单位
             * 5. workQueue: 工作队列
             * 6. threadFactory: 线程工厂
             * 7. handler: 拒绝策略
             */
            
            ThreadPoolExecutor executor = new ThreadPoolExecutor(
                2,                      // corePoolSize: 核心线程数
                5,                      // maximumPoolSize: 最大线程数
                60,                     // keepAliveTime: 空闲线程存活时间
                TimeUnit.SECONDS,       // unit: 时间单位
                new LinkedBlockingQueue<>(10),  // workQueue: 容量为10的阻塞队列
                new CustomThreadFactory("MyPool"),  // threadFactory: 自定义线程工厂
                new ThreadPoolExecutor.CallerRunsPolicy()  // handler: 调用者运行策略
            );
            
            System.out.println("线程池创建成功！");
            System.out.println("  核心线程数: " + executor.getCorePoolSize());
            System.out.println("  最大线程数: " + executor.getMaximumPoolSize());
            System.out.println("  空闲存活时间: " + executor.getKeepAliveTime(TimeUnit.SECONDS) + "秒");
            System.out.println("  队列类型: " + executor.getQueue().getClass().getSimpleName());
            
            executor.shutdown();
            System.out.println();
        }
    }
    
    /**
     * 自定义线程工厂
     */
    public static class CustomThreadFactory implements ThreadFactory {
        private final String namePrefix;
        private final AtomicInteger threadNumber = new AtomicInteger(1);
        
        public CustomThreadFactory(String namePrefix) {
            this.namePrefix = namePrefix;
        }
        
        @Override
        public Thread newThread(Runnable r) {
            Thread thread = new Thread(r, namePrefix + "-thread-" + threadNumber.getAndIncrement());
            thread.setDaemon(false);
            thread.setPriority(Thread.NORM_PRIORITY);
            return thread;
        }
    }
    
    // ==================== 2. 线程池工作流程 ====================
    
    /**
     * 演示线程池工作流程
     */
    public static class WorkflowDemo {
        
        public static void demo() throws InterruptedException {
            System.out.println("【2. 线程池工作流程】");
            System.out.println(repeat("-", 50));
            
            System.out.println("执行流程：");
            System.out.println("  1. 提交任务");
            System.out.println("  2. 当前线程数 < corePoolSize ? 创建核心线程执行");
            System.out.println("  3. 核心线程满，任务加入队列");
            System.out.println("  4. 队列满 && 当前线程数 < maximumPoolSize ? 创建非核心线程");
            System.out.println("  5. 队列满 && 当前线程数 = maximumPoolSize ? 执行拒绝策略");
            System.out.println();
            
            // 创建线程池：核心2，最大4，队列容量3
            ThreadPoolExecutor executor = new ThreadPoolExecutor(
                2, 4, 60, TimeUnit.SECONDS,
                new ArrayBlockingQueue<>(3),
                new CustomThreadFactory("Demo"),
                new ThreadPoolExecutor.AbortPolicy()
            );
            
            System.out.println("线程池配置：core=2, max=4, queue=3");
            System.out.println("提交 8 个任务观察执行流程：\n");
            
            for (int i = 1; i <= 8; i++) {
                final int taskId = i;
                try {
                    executor.execute(() -> {
                        System.out.println("任务" + taskId + " 开始执行 - " + 
                            Thread.currentThread().getName());
                        try {
                            Thread.sleep(1000);
                        } catch (InterruptedException e) {
                            e.printStackTrace();
                        }
                        System.out.println("任务" + taskId + " 执行完成");
                    });
                    System.out.println("提交任务" + taskId + " - 活动线程: " + 
                        executor.getActiveCount() + ", 队列大小: " + executor.getQueue().size());
                } catch (RejectedExecutionException e) {
                    System.out.println("任务" + taskId + " 被拒绝！");
                }
                Thread.sleep(100);
            }
            
            executor.shutdown();
            executor.awaitTermination(10, TimeUnit.SECONDS);
            System.out.println();
        }
    }
    
    // ==================== 3. 四种拒绝策略 ====================
    
    /**
     * 四种拒绝策略演示
     */
    public static class RejectionPolicyDemo {
        
        public static void demo() {
            System.out.println("【3. 四种拒绝策略】");
            System.out.println(repeat("-", 50));
            
            System.out.println("1. AbortPolicy（默认）");
            System.out.println("   抛出 RejectedExecutionException 异常");
            testPolicy(new ThreadPoolExecutor.AbortPolicy(), "AbortPolicy");
            
            System.out.println("\n2. CallerRunsPolicy");
            System.out.println("   由提交任务的线程执行该任务");
            testPolicy(new ThreadPoolExecutor.CallerRunsPolicy(), "CallerRunsPolicy");
            
            System.out.println("\n3. DiscardPolicy");
            System.out.println("   静默丢弃任务，不抛异常");
            testPolicy(new ThreadPoolExecutor.DiscardPolicy(), "DiscardPolicy");
            
            System.out.println("\n4. DiscardOldestPolicy");
            System.out.println("   丢弃队列中最老的任务，然后重新提交");
            testPolicy(new ThreadPoolExecutor.DiscardOldestPolicy(), "DiscardOldestPolicy");
            
            System.out.println();
        }
        
        private static void testPolicy(RejectedExecutionHandler policy, String policyName) {
            ThreadPoolExecutor executor = new ThreadPoolExecutor(
                1, 1, 0, TimeUnit.SECONDS,
                new ArrayBlockingQueue<>(1),
                policy
            );
            
            try {
                // 第1个任务：核心线程执行
                executor.execute(() -> {
                    try { Thread.sleep(100); } catch (Exception e) {}
                });
                // 第2个任务：进入队列
                executor.execute(() -> {});
                // 第3个任务：触发拒绝策略
                executor.execute(() -> 
                    System.out.println("   任务3执行于: " + Thread.currentThread().getName()));
                System.out.println("   [" + policyName + "] 任务提交成功");
            } catch (RejectedExecutionException e) {
                System.out.println("   [" + policyName + "] 任务被拒绝: " + e.getClass().getSimpleName());
            } finally {
                executor.shutdownNow();
            }
        }
    }
    
    // ==================== 4. 常见线程池类型 ====================
    
    /**
     * Executors 工具类创建的线程池
     */
    public static class CommonPoolTypes {
        
        public static void demo() {
            System.out.println("【4. 常见线程池类型】");
            System.out.println(repeat("-", 50));
            
            System.out.println("1. FixedThreadPool - 固定大小线程池");
            System.out.println("   new ThreadPoolExecutor(n, n, 0L, LinkedBlockingQueue)");
            System.out.println("   问题：队列无界，可能OOM");
            
            System.out.println("\n2. CachedThreadPool - 缓存线程池");
            System.out.println("   new ThreadPoolExecutor(0, Integer.MAX_VALUE, 60s, SynchronousQueue)");
            System.out.println("   问题：线程数无上限，可能OOM");
            
            System.out.println("\n3. SingleThreadExecutor - 单线程池");
            System.out.println("   new ThreadPoolExecutor(1, 1, 0L, LinkedBlockingQueue)");
            System.out.println("   问题：队列无界，可能OOM");
            
            System.out.println("\n4. ScheduledThreadPool - 定时线程池");
            System.out.println("   用于延迟执行和周期执行");
            
            System.out.println("\n5. WorkStealingPool (JDK8+) - 工作窃取线程池");
            System.out.println("   基于 ForkJoinPool，适合任务可拆分场景");
            
            System.out.println("\n【阿里巴巴开发规范】");
            System.out.println("  不推荐使用 Executors 创建线程池！");
            System.out.println("  应使用 ThreadPoolExecutor 自定义参数，避免 OOM");
            System.out.println();
        }
    }
    
    // ==================== 5. 线程池监控 ====================
    
    /**
     * 线程池监控
     */
    public static class MonitoringDemo {
        
        public static void demo() throws InterruptedException {
            System.out.println("【5. 线程池监控】");
            System.out.println(repeat("-", 50));
            
            ThreadPoolExecutor executor = new ThreadPoolExecutor(
                2, 5, 60, TimeUnit.SECONDS,
                new LinkedBlockingQueue<>(10),
                new CustomThreadFactory("Monitor")
            );
            
            // 提交任务
            for (int i = 0; i < 15; i++) {
                executor.execute(() -> {
                    try { Thread.sleep(500); } catch (Exception e) {}
                });
            }
            
            // 监控线程池状态
            System.out.println("线程池状态监控：");
            for (int i = 0; i < 5; i++) {
                System.out.println("  -------------------------");
                System.out.println("  池大小(PoolSize): " + executor.getPoolSize());
                System.out.println("  活动线程(ActiveCount): " + executor.getActiveCount());
                System.out.println("  已完成任务(CompletedTasks): " + executor.getCompletedTaskCount());
                System.out.println("  总任务数(TaskCount): " + executor.getTaskCount());
                System.out.println("  队列大小(QueueSize): " + executor.getQueue().size());
                System.out.println("  最大池大小(LargestPoolSize): " + executor.getLargestPoolSize());
                Thread.sleep(600);
            }
            
            executor.shutdown();
            executor.awaitTermination(10, TimeUnit.SECONDS);
            System.out.println();
        }
    }
    
    // ==================== 6. 最佳实践 ====================
    
    /**
     * 线程池最佳实践
     */
    public static class BestPractices {
        
        public static void demo() {
            System.out.println("【6. 线程池最佳实践】");
            System.out.println(repeat("-", 50));
            
            System.out.println("1. 线程池大小设置：");
            int cpuCores = Runtime.getRuntime().availableProcessors();
            System.out.println("   CPU 核心数: " + cpuCores);
            System.out.println("   CPU 密集型: 核心数 + 1 = " + (cpuCores + 1));
            System.out.println("   IO 密集型:  核心数 * 2 = " + (cpuCores * 2));
            System.out.println("   混合型:     根据 IO 等待时间/计算时间 比例调整");
            
            System.out.println("\n2. 队列选择：");
            System.out.println("   ArrayBlockingQueue: 有界队列，推荐");
            System.out.println("   LinkedBlockingQueue: 可选有界，默认无界");
            System.out.println("   SynchronousQueue: 直接传递，不存储任务");
            System.out.println("   PriorityBlockingQueue: 优先级队列");
            
            System.out.println("\n3. 异常处理：");
            System.out.println("   - submit() 方法的异常会被 Future 吞掉");
            System.out.println("   - 建议在任务内部 try-catch");
            System.out.println("   - 或使用 afterExecute() 钩子方法");
            
            System.out.println("\n4. 优雅关闭：");
            System.out.println("   executor.shutdown();  // 不接受新任务，等待已提交任务完成");
            System.out.println("   executor.awaitTermination(timeout, unit);  // 等待终止");
            System.out.println("   executor.shutdownNow();  // 尝试停止所有任务");
            
            System.out.println("\n5. 命名线程：");
            System.out.println("   使用自定义 ThreadFactory 给线程命名");
            System.out.println("   便于问题排查和监控");
            
            System.out.println();
        }
    }
    
    // ==================== 7. 自定义线程池示例 ====================
    
    /**
     * 生产环境推荐的线程池配置
     */
    public static class ProductionPool {
        
        public static ThreadPoolExecutor createPool(String poolName, int coreSize, int maxSize, int queueSize) {
            return new ThreadPoolExecutor(
                coreSize,
                maxSize,
                60L,
                TimeUnit.SECONDS,
                new ArrayBlockingQueue<>(queueSize),
                new CustomThreadFactory(poolName),
                new ThreadPoolExecutor.CallerRunsPolicy()  // 或自定义拒绝策略
            ) {
                @Override
                protected void beforeExecute(Thread t, Runnable r) {
                    // 任务执行前的钩子
                    super.beforeExecute(t, r);
                }
                
                @Override
                protected void afterExecute(Runnable r, Throwable t) {
                    // 任务执行后的钩子，可处理异常
                    super.afterExecute(r, t);
                    if (t != null) {
                        System.err.println("任务执行异常: " + t.getMessage());
                    }
                }
                
                @Override
                protected void terminated() {
                    // 线程池终止时的钩子
                    super.terminated();
                    System.out.println("线程池已终止");
                }
            };
        }
        
        public static void demo() throws InterruptedException {
            System.out.println("【7. 生产环境线程池示例】");
            System.out.println(repeat("-", 50));
            
            ThreadPoolExecutor pool = createPool("BizPool", 4, 8, 100);
            
            System.out.println("生产环境线程池已创建：");
            System.out.println("  名称前缀: BizPool");
            System.out.println("  核心线程: 4");
            System.out.println("  最大线程: 8");
            System.out.println("  队列容量: 100");
            System.out.println("  拒绝策略: CallerRunsPolicy");
            
            // 模拟业务
            for (int i = 0; i < 5; i++) {
                final int taskId = i;
                pool.execute(() -> {
                    System.out.println("  执行业务任务 " + taskId);
                });
            }
            
            pool.shutdown();
            pool.awaitTermination(5, TimeUnit.SECONDS);
            System.out.println();
        }
    }
    
    // ==================== 主方法 ====================
    
    public static void main(String[] args) throws InterruptedException {
        System.out.println("=== 线程池使用示例 ===\n");
        
        CoreParameters.demo();
        WorkflowDemo.demo();
        RejectionPolicyDemo.demo();
        CommonPoolTypes.demo();
        MonitoringDemo.demo();
        BestPractices.demo();
        ProductionPool.demo();
    }
}
