package com.example.designpatterns.singleton;

/**
 * 枚举单例 (最安全的实现方式)
 * 
 * 特点：
 * 1. 线程安全 - JVM 保证枚举实例的唯一性
 * 2. 防止反射攻击 - JVM 禁止通过反射创建枚举实例
 * 3. 防止序列化破坏 - 枚举序列化机制保证不会创建新实例
 * 4. 代码最简洁
 * 
 * Effective Java 作者 Joshua Bloch 推荐的单例实现方式
 * 
 * @author java_learn
 */
public enum Singleton04_Enum {
    
    INSTANCE;
    
    // 可以添加实例变量
    private String config;
    private int counter = 0;
    
    // 枚举构造函数（隐式 private）
    Singleton04_Enum() {
        System.out.println("Singleton04_Enum 实例被创建");
        this.config = "Default Config";
    }
    
    // 可以添加实例方法
    public void doSomething() {
        counter++;
        System.out.println("执行业务逻辑，第 " + counter + " 次调用");
    }
    
    public String getConfig() {
        return config;
    }
    
    public void setConfig(String config) {
        this.config = config;
    }
    
    public int getCounter() {
        return counter;
    }
    
    // 测试
    public static void main(String[] args) {
        System.out.println("=== 枚举单例测试 ===\n");
        
        // 获取实例
        Singleton04_Enum s1 = Singleton04_Enum.INSTANCE;
        Singleton04_Enum s2 = Singleton04_Enum.INSTANCE;
        
        // 验证单例
        System.out.println("s1 == s2: " + (s1 == s2));
        
        // 使用实例方法
        s1.doSomething();
        s1.doSomething();
        
        // 修改配置
        s1.setConfig("New Config");
        System.out.println("s2 获取配置: " + s2.getConfig()); // 同一个实例，所以能看到修改
        System.out.println("s2 获取计数: " + s2.getCounter());
        
        // 演示反射无法破坏枚举单例
        System.out.println("\n=== 尝试通过反射创建新实例 ===");
        try {
            java.lang.reflect.Constructor<Singleton04_Enum> constructor = 
                Singleton04_Enum.class.getDeclaredConstructor();
            constructor.setAccessible(true);
            constructor.newInstance();
        } catch (Exception e) {
            System.out.println("反射创建失败: " + e.getClass().getSimpleName());
            System.out.println("原因: 枚举类型不能通过反射创建实例");
        }
    }
}
