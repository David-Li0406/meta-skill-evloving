package com.example.designpatterns.singleton;

/**
 * 饿汉式单例 - 静态常量
 * 
 * 特点：
 * 1. 类加载时就创建实例，线程安全
 * 2. 不支持延迟加载
 * 3. 实现简单，推荐用于实例创建开销小的场景
 * 
 * @author java_learn
 */
public class Singleton01_Eager {
    
    // 类加载时就创建实例
    private static final Singleton01_Eager INSTANCE = new Singleton01_Eager();
    
    // 私有构造函数，防止外部实例化
    private Singleton01_Eager() {
        // 防止反射破坏单例
        if (INSTANCE != null) {
            throw new RuntimeException("单例已存在，禁止通过反射创建");
        }
        System.out.println("Singleton01_Eager 实例被创建");
    }
    
    public static Singleton01_Eager getInstance() {
        return INSTANCE;
    }
    
    public void showMessage() {
        System.out.println("Hello from Singleton01_Eager!");
    }
    
    // 测试
    public static void main(String[] args) {
        System.out.println("=== 饿汉式单例测试 ===");
        
        // 获取两次实例
        Singleton01_Eager s1 = Singleton01_Eager.getInstance();
        Singleton01_Eager s2 = Singleton01_Eager.getInstance();
        
        // 验证是否为同一实例
        System.out.println("s1 == s2: " + (s1 == s2));
        System.out.println("s1.hashCode(): " + s1.hashCode());
        System.out.println("s2.hashCode(): " + s2.hashCode());
        
        s1.showMessage();
    }
}
