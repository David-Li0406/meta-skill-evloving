package com.example.designpatterns.singleton;

/**
 * 静态内部类单例 (推荐使用)
 * 
 * 特点：
 * 1. 延迟加载 - 只有调用 getInstance() 时才会加载内部类
 * 2. 线程安全 - 利用 JVM 类加载机制保证
 * 3. 代码简洁 - 不需要 synchronized 或 volatile
 * 
 * 原理：
 * - 外部类加载时，静态内部类不会被加载
 * - 调用 getInstance() 触发 SingletonHolder 类加载
 * - JVM 保证类加载过程是线程安全的
 * 
 * @author java_learn
 */
public class Singleton03_StaticInnerClass {
    
    private Singleton03_StaticInnerClass() {
        System.out.println("Singleton03_StaticInnerClass 实例被创建");
    }
    
    /**
     * 静态内部类
     * - 外部类加载时不会加载
     * - 只有第一次调用 getInstance() 时才会加载
     * - JVM 保证类加载的线程安全性
     */
    private static class SingletonHolder {
        private static final Singleton03_StaticInnerClass INSTANCE = 
            new Singleton03_StaticInnerClass();
        
        static {
            System.out.println("SingletonHolder 静态内部类被加载");
        }
    }
    
    public static Singleton03_StaticInnerClass getInstance() {
        return SingletonHolder.INSTANCE;
    }
    
    public void showMessage() {
        System.out.println("Hello from Singleton03_StaticInnerClass!");
    }
    
    // 测试
    public static void main(String[] args) {
        System.out.println("=== 静态内部类单例测试 ===\n");
        
        System.out.println("外部类已加载，但实例未创建");
        System.out.println("准备调用 getInstance()...\n");
        
        // 此时才会触发 SingletonHolder 类加载，创建实例
        Singleton03_StaticInnerClass s1 = Singleton03_StaticInnerClass.getInstance();
        
        System.out.println("\n再次调用 getInstance()...");
        Singleton03_StaticInnerClass s2 = Singleton03_StaticInnerClass.getInstance();
        
        System.out.println("\n验证: s1 == s2: " + (s1 == s2));
        s1.showMessage();
    }
}
