package com.example.thread;

import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.TimeUnit;

/**
 * ThreadLocal 使用示例
 * 
 * ThreadLocal 为每个线程提供独立的变量副本，实现线程隔离。
 * 
 * 核心知识点：
 * 1. ThreadLocal 内存模型
 * 2. 内存泄漏问题及解决方案
 * 3. InheritableThreadLocal
 * 4. 线程池中的注意事项
 * 
 * @author java_learn
 */
public class ThreadLocalDemo {

    private static String repeat(String s, int count) {
        StringBuilder sb = new StringBuilder(s.length() * count);
        for (int i = 0; i < count; i++) {
            sb.append(s);
        }
        return sb.toString();
    }
    
    // ==================== 1. 基本使用 ====================
    
    /**
     * 基本的 ThreadLocal 使用
     */
    public static class BasicUsage {
        // 为每个线程存储用户 ID
        private static final ThreadLocal<String> USER_ID = new ThreadLocal<>();
        
        // 使用 withInitial 设置初始值
        private static final ThreadLocal<Integer> COUNTER = 
            ThreadLocal.withInitial(() -> 0);
        
        public static void demo() {
            System.out.println("【1. ThreadLocal 基本使用】");
            System.out.println(repeat("-", 50));
            
            // 线程1
            Thread t1 = new Thread(() -> {
                USER_ID.set("user-001");
                COUNTER.set(COUNTER.get() + 1);
                
                System.out.println(Thread.currentThread().getName() + 
                    " - USER_ID: " + USER_ID.get() + 
                    ", COUNTER: " + COUNTER.get());
                
                // 必须在使用完后清理
                USER_ID.remove();
                COUNTER.remove();
            }, "Thread-1");
            
            // 线程2
            Thread t2 = new Thread(() -> {
                USER_ID.set("user-002");
                COUNTER.set(COUNTER.get() + 10);
                
                System.out.println(Thread.currentThread().getName() + 
                    " - USER_ID: " + USER_ID.get() + 
                    ", COUNTER: " + COUNTER.get());
                
                USER_ID.remove();
                COUNTER.remove();
            }, "Thread-2");
            
            t1.start();
            t2.start();
            
            try {
                t1.join();
                t2.join();
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
            
            // 主线程的值是独立的
            System.out.println("Main - USER_ID: " + USER_ID.get() + 
                ", COUNTER: " + COUNTER.get());
            System.out.println();
        }
    }
    
    // ==================== 2. 解决 SimpleDateFormat 线程安全问题 ====================
    
    /**
     * SimpleDateFormat 线程安全问题及解决方案
     */
    public static class DateFormatSafety {
        // 错误做法：共享 SimpleDateFormat 会导致线程安全问题
        // private static final SimpleDateFormat UNSAFE_FORMAT = 
        //     new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
        
        // 正确做法：使用 ThreadLocal 为每个线程创建独立的实例
        private static final ThreadLocal<SimpleDateFormat> DATE_FORMAT = 
            ThreadLocal.withInitial(() -> new SimpleDateFormat("yyyy-MM-dd HH:mm:ss"));
        
        public static void demo() throws InterruptedException {
            System.out.println("【2. SimpleDateFormat 线程安全】");
            System.out.println(repeat("-", 50));
            
            ExecutorService executor = Executors.newFixedThreadPool(3);
            
            for (int i = 0; i < 5; i++) {
                final int taskId = i;
                executor.submit(() -> {
                    try {
                        // 安全地使用 SimpleDateFormat
                        SimpleDateFormat sdf = DATE_FORMAT.get();
                        String formatted = sdf.format(new Date());
                        System.out.println("Task-" + taskId + " 格式化时间: " + formatted);
                    } finally {
                        // 线程池中必须清理
                        DATE_FORMAT.remove();
                    }
                });
            }
            
            executor.shutdown();
            executor.awaitTermination(5, TimeUnit.SECONDS);
            System.out.println();
        }
    }
    
    // ==================== 3. 请求上下文传递 ====================
    
    /**
     * 模拟 Web 请求上下文
     */
    public static class RequestContext {
        private String requestId;
        private String userId;
        private long startTime;
        
        public RequestContext(String requestId, String userId) {
            this.requestId = requestId;
            this.userId = userId;
            this.startTime = System.currentTimeMillis();
        }
        
        public String getRequestId() { return requestId; }
        public String getUserId() { return userId; }
        public long getStartTime() { return startTime; }
        
        @Override
        public String toString() {
            return "RequestContext{requestId='" + requestId + "', userId='" + userId + "'}";
        }
    }
    
    /**
     * 请求上下文持有者
     */
    public static class RequestContextHolder {
        private static final ThreadLocal<RequestContext> CONTEXT = new ThreadLocal<>();
        
        public static void setContext(RequestContext context) {
            CONTEXT.set(context);
        }
        
        public static RequestContext getContext() {
            return CONTEXT.get();
        }
        
        public static void clear() {
            CONTEXT.remove();
        }
        
        public static void demo() {
            System.out.println("【3. 请求上下文传递】");
            System.out.println(repeat("-", 50));
            
            // 模拟处理多个请求
            Thread request1 = new Thread(() -> {
                try {
                    // 设置请求上下文
                    setContext(new RequestContext("REQ-001", "USER-A"));
                    System.out.println(Thread.currentThread().getName() + 
                        " 开始处理请求: " + getContext());
                    
                    // 模拟调用 Service 层
                    processService();
                    
                } finally {
                    clear(); // 清理
                }
            }, "Request-1");
            
            Thread request2 = new Thread(() -> {
                try {
                    setContext(new RequestContext("REQ-002", "USER-B"));
                    System.out.println(Thread.currentThread().getName() + 
                        " 开始处理请求: " + getContext());
                    
                    processService();
                    
                } finally {
                    clear();
                }
            }, "Request-2");
            
            request1.start();
            request2.start();
            
            try {
                request1.join();
                request2.join();
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
            System.out.println();
        }
        
        private static void processService() {
            // Service 层可以直接获取上下文，无需方法参数传递
            RequestContext ctx = getContext();
            System.out.println("  [Service] 处理请求: " + ctx.getRequestId() + 
                ", 用户: " + ctx.getUserId());
            
            processDao();
        }
        
        private static void processDao() {
            // DAO 层同样可以获取上下文
            RequestContext ctx = getContext();
            System.out.println("  [DAO] 执行数据库操作, 请求: " + ctx.getRequestId());
        }
    }
    
    // ==================== 4. InheritableThreadLocal ====================
    
    /**
     * InheritableThreadLocal 演示
     * 子线程可以继承父线程的 ThreadLocal 值
     */
    public static class InheritableDemo {
        private static final ThreadLocal<String> NORMAL_TL = new ThreadLocal<>();
        private static final InheritableThreadLocal<String> INHERITABLE_TL = 
            new InheritableThreadLocal<>();
        
        public static void demo() throws InterruptedException {
            System.out.println("【4. InheritableThreadLocal】");
            System.out.println(repeat("-", 50));
            
            // 父线程设置值
            NORMAL_TL.set("普通值");
            INHERITABLE_TL.set("可继承值");
            
            System.out.println("父线程设置完毕");
            System.out.println("父线程 - NORMAL_TL: " + NORMAL_TL.get());
            System.out.println("父线程 - INHERITABLE_TL: " + INHERITABLE_TL.get());
            
            // 创建子线程
            Thread child = new Thread(() -> {
                // 普通 ThreadLocal 无法继承
                System.out.println("子线程 - NORMAL_TL: " + NORMAL_TL.get());
                // InheritableThreadLocal 可以继承
                System.out.println("子线程 - INHERITABLE_TL: " + INHERITABLE_TL.get());
            }, "Child");
            
            child.start();
            child.join();
            
            // 清理
            NORMAL_TL.remove();
            INHERITABLE_TL.remove();
            System.out.println();
        }
    }
    
    // ==================== 5. 线程池中的问题 ====================
    
    /**
     * 线程池中 InheritableThreadLocal 的问题
     */
    public static class ThreadPoolProblem {
        private static final InheritableThreadLocal<String> TRACE_ID = 
            new InheritableThreadLocal<>();
        
        public static void demo() throws InterruptedException {
            System.out.println("【5. 线程池中的问题】");
            System.out.println(repeat("-", 50));
            System.out.println("问题：线程池中线程是复用的，InheritableThreadLocal 只在创建子线程时复制一次");
            System.out.println();
            
            // 创建只有1个线程的线程池，确保线程复用
            ExecutorService executor = Executors.newFixedThreadPool(1);
            
            // 第一次提交任务
            TRACE_ID.set("TRACE-001");
            System.out.println("主线程设置 TRACE_ID: " + TRACE_ID.get());
            
            executor.submit(() -> {
                System.out.println("任务1 - 线程: " + Thread.currentThread().getName() + 
                    ", TRACE_ID: " + TRACE_ID.get());
            });
            
            Thread.sleep(100); // 等待任务1完成
            
            // 修改主线程的值
            TRACE_ID.set("TRACE-002");
            System.out.println("主线程修改 TRACE_ID: " + TRACE_ID.get());
            
            executor.submit(() -> {
                // 这里获取到的还是 TRACE-001，因为线程是复用的，不会重新继承
                System.out.println("任务2 - 线程: " + Thread.currentThread().getName() + 
                    ", TRACE_ID: " + TRACE_ID.get());
                System.out.println("  问题：期望 TRACE-002，实际是 TRACE-001！");
            });
            
            executor.shutdown();
            executor.awaitTermination(5, TimeUnit.SECONDS);
            
            System.out.println("\n解决方案：使用阿里巴巴的 TransmittableThreadLocal (TTL)");
            System.out.println("  - 包装线程池：TtlExecutors.getTtlExecutorService(executor)");
            System.out.println("  - 每次提交任务时自动传递上下文");
            
            TRACE_ID.remove();
            System.out.println();
        }
    }
    
    // ==================== 6. 内存泄漏分析 ====================
    
    /**
     * ThreadLocal 内存泄漏分析
     */
    public static class MemoryLeakAnalysis {
        public static void demo() {
            System.out.println("【6. 内存泄漏分析】");
            System.out.println(repeat("-", 50));
            System.out.println();
            System.out.println("ThreadLocalMap 的 Entry 结构：");
            System.out.println("  Entry extends WeakReference<ThreadLocal<?>> {");
            System.out.println("      Object value;  // 强引用");
            System.out.println("  }");
            System.out.println();
            System.out.println("引用链：");
            System.out.println("  Thread -> ThreadLocalMap -> Entry[] -> Entry");
            System.out.println("                                          ├─ key (WeakReference -> ThreadLocal)");
            System.out.println("                                          └─ value (强引用 -> 实际数据)");
            System.out.println();
            System.out.println("泄漏场景：");
            System.out.println("  1. ThreadLocal 对象被回收（弱引用）");
            System.out.println("  2. Entry.key = null");
            System.out.println("  3. 但 Entry.value 仍然是强引用");
            System.out.println("  4. 如果线程一直存活（线程池），value 永远不会被回收");
            System.out.println();
            System.out.println("解决方案：");
            System.out.println("  try {");
            System.out.println("      threadLocal.set(value);");
            System.out.println("      // 使用 value...");
            System.out.println("  } finally {");
            System.out.println("      threadLocal.remove();  // 必须清理！");
            System.out.println("  }");
            System.out.println();
        }
    }
    
    // ==================== 主方法 ====================
    
    public static void main(String[] args) throws InterruptedException {
        System.out.println("=== ThreadLocal 使用示例 ===\n");
        
        BasicUsage.demo();
        DateFormatSafety.demo();
        RequestContextHolder.demo();
        InheritableDemo.demo();
        ThreadPoolProblem.demo();
        MemoryLeakAnalysis.demo();
    }
}
