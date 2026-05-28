package com.example.designpatterns.proxy;

import java.lang.reflect.InvocationHandler;
import java.lang.reflect.Method;
import java.lang.reflect.Proxy;

/**
 * 代理模式示例
 * 
 * 代理模式为其他对象提供一种代理以控制对这个对象的访问。
 * 
 * 本示例包含：
 * 1. 静态代理
 * 2. JDK 动态代理
 * 3. CGLIB 动态代理（模拟）
 * 
 * @author java_learn
 */
public class ProxyPatternDemo {
    
    // ==================== 接口定义 ====================
    
    /**
     * 用户服务接口
     */
    public interface UserService {
        void addUser(String username);
        String getUser(int id);
        void deleteUser(int id);
    }
    
    // ==================== 真实对象 ====================
    
    /**
     * 用户服务实现
     */
    public static class UserServiceImpl implements UserService {
        @Override
        public void addUser(String username) {
            System.out.println("  [Real] 添加用户: " + username);
        }
        
        @Override
        public String getUser(int id) {
            System.out.println("  [Real] 查询用户: " + id);
            return "User-" + id;
        }
        
        @Override
        public void deleteUser(int id) {
            System.out.println("  [Real] 删除用户: " + id);
        }
    }
    
    // ==================== 1. 静态代理 ====================
    
    /**
     * 静态代理类 - 手动编写代理类
     * 
     * 特点：
     * - 代理类在编译时就确定
     * - 代理类需要实现与目标类相同的接口
     * - 缺点：每个接口都需要编写代理类，不灵活
     */
    public static class UserServiceStaticProxy implements UserService {
        private UserService target;
        
        public UserServiceStaticProxy(UserService target) {
            this.target = target;
        }
        
        @Override
        public void addUser(String username) {
            System.out.println("[Static Proxy] 开始添加用户...");
            long start = System.currentTimeMillis();
            
            target.addUser(username);
            
            long end = System.currentTimeMillis();
            System.out.println("[Static Proxy] 添加用户完成，耗时: " + (end - start) + "ms");
        }
        
        @Override
        public String getUser(int id) {
            System.out.println("[Static Proxy] 开始查询用户...");
            System.out.println("[Static Proxy] 检查缓存...");
            
            String result = target.getUser(id);
            
            System.out.println("[Static Proxy] 查询完成");
            return result;
        }
        
        @Override
        public void deleteUser(int id) {
            System.out.println("[Static Proxy] 权限检查...");
            System.out.println("[Static Proxy] 开始删除用户...");
            
            target.deleteUser(id);
            
            System.out.println("[Static Proxy] 删除完成，记录日志");
        }
    }
    
    // ==================== 2. JDK 动态代理 ====================
    
    /**
     * JDK 动态代理处理器
     * 
     * 特点：
     * - 代理类在运行时动态生成
     * - 只能代理实现了接口的类
     * - 通过 InvocationHandler 统一处理所有方法调用
     */
    public static class JdkProxyHandler implements InvocationHandler {
        private Object target;
        
        public JdkProxyHandler(Object target) {
            this.target = target;
        }
        
        @Override
        public Object invoke(Object proxy, Method method, Object[] args) throws Throwable {
            String methodName = method.getName();
            
            // 前置处理
            System.out.println("[JDK Proxy] 调用方法: " + methodName);
            System.out.println("[JDK Proxy] 参数: " + argsToString(args));
            long start = System.currentTimeMillis();
            
            // 调用目标方法
            Object result = method.invoke(target, args);
            
            // 后置处理
            long end = System.currentTimeMillis();
            System.out.println("[JDK Proxy] 返回值: " + result);
            System.out.println("[JDK Proxy] 耗时: " + (end - start) + "ms");
            
            return result;
        }
        
        private String argsToString(Object[] args) {
            if (args == null || args.length == 0) {
                return "无";
            }
            StringBuilder sb = new StringBuilder();
            for (Object arg : args) {
                sb.append(arg).append(", ");
            }
            return sb.substring(0, sb.length() - 2);
        }
        
        /**
         * 创建代理对象
         */
        @SuppressWarnings("unchecked")
        public static <T> T createProxy(T target) {
            return (T) Proxy.newProxyInstance(
                target.getClass().getClassLoader(),
                target.getClass().getInterfaces(),
                new JdkProxyHandler(target)
            );
        }
    }
    
    // ==================== 3. CGLIB 动态代理（模拟）====================
    
    /**
     * CGLIB 代理模拟类
     * 
     * 注意：真正的 CGLIB 需要引入 cglib 库
     * 这里只是模拟其行为
     * 
     * 特点：
     * - 通过继承目标类创建代理
     * - 可以代理没有实现接口的类
     * - 不能代理 final 类和 final 方法
     */
    public static class CglibProxySimulator {
        
        /**
         * 方法拦截器接口
         */
        public interface MethodInterceptor {
            Object intercept(Object obj, String methodName, Object[] args, 
                           Runnable superMethod) throws Exception;
        }
        
        /**
         * 创建代理（模拟）
         * 实际 CGLIB 使用字节码技术，这里简化处理
         */
        public static UserService createProxy(UserServiceImpl target, MethodInterceptor interceptor) {
            // 这是一个简化的模拟，真正的 CGLIB 会动态生成子类
            return new UserService() {
                @Override
                public void addUser(String username) {
                    try {
                        interceptor.intercept(target, "addUser", new Object[]{username}, 
                            () -> target.addUser(username));
                    } catch (Exception e) {
                        e.printStackTrace();
                    }
                }
                
                @Override
                public String getUser(int id) {
                    try {
                        return (String) interceptor.intercept(target, "getUser", new Object[]{id}, 
                            () -> { /* 返回值在拦截器中处理 */ });
                    } catch (Exception e) {
                        e.printStackTrace();
                        return null;
                    }
                }
                
                @Override
                public void deleteUser(int id) {
                    try {
                        interceptor.intercept(target, "deleteUser", new Object[]{id}, 
                            () -> target.deleteUser(id));
                    } catch (Exception e) {
                        e.printStackTrace();
                    }
                }
            };
        }
    }
    
    // ==================== 测试 ====================
    
    public static void main(String[] args) {
        System.out.println("=== 代理模式示例 ===\n");
        
        // 创建真实对象
        UserService realService = new UserServiceImpl();
        
        // ========== 1. 静态代理测试 ==========
        System.out.println("【1. 静态代理】");
        System.out.println("-".repeat(50));
        UserService staticProxy = new UserServiceStaticProxy(realService);
        staticProxy.addUser("Alice");
        System.out.println();
        staticProxy.getUser(1);
        System.out.println();
        staticProxy.deleteUser(1);
        
        // ========== 2. JDK 动态代理测试 ==========
        System.out.println("\n\n【2. JDK 动态代理】");
        System.out.println("-".repeat(50));
        UserService jdkProxy = JdkProxyHandler.createProxy(realService);
        jdkProxy.addUser("Bob");
        System.out.println();
        String user = jdkProxy.getUser(2);
        System.out.println("获取到的用户: " + user);
        
        // ========== 3. CGLIB 代理测试（模拟）==========
        System.out.println("\n\n【3. CGLIB 动态代理（模拟）】");
        System.out.println("-".repeat(50));
        
        CglibProxySimulator.MethodInterceptor interceptor = (obj, methodName, argsArray, superMethod) -> {
            System.out.println("[CGLIB] 拦截方法: " + methodName);
            System.out.println("[CGLIB] 执行前置逻辑...");
            
            // 调用父类方法
            if (methodName.equals("getUser") && argsArray.length > 0) {
                String result = ((UserServiceImpl) obj).getUser((Integer) argsArray[0]);
                System.out.println("[CGLIB] 执行后置逻辑...");
                return result;
            } else {
                superMethod.run();
                System.out.println("[CGLIB] 执行后置逻辑...");
                return null;
            }
        };
        
        UserService cglibProxy = CglibProxySimulator.createProxy(
            (UserServiceImpl) realService, interceptor);
        cglibProxy.addUser("Charlie");
        
        // ========== 代理模式对比 ==========
        System.out.println("\n\n【代理模式对比】");
        System.out.println("=".repeat(60));
        System.out.println("| 类型       | 实现方式           | 优点                 | 缺点                 |");
        System.out.println("|------------|-------------------|---------------------|---------------------|");
        System.out.println("| 静态代理    | 手动编写代理类     | 简单直观             | 每个类都需要代理类    |");
        System.out.println("| JDK 动态代理| Proxy.newInstance | 动态生成，灵活        | 只能代理接口         |");
        System.out.println("| CGLIB      | 字节码增强         | 可代理普通类          | 不能代理 final 类    |");
        System.out.println("=".repeat(60));
    }
}
