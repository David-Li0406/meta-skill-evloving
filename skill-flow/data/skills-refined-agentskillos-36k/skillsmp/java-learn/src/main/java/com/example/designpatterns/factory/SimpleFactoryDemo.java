package com.example.designpatterns.factory;

/**
 * 简单工厂模式示例
 * 
 * 场景：根据不同的支付方式创建对应的支付处理器
 * 
 * 特点：
 * 1. 一个工厂类负责创建所有产品
 * 2. 客户端不需要知道具体产品类
 * 3. 新增产品需要修改工厂类（违反开闭原则）
 * 
 * @author java_learn
 */
public class SimpleFactoryDemo {
    
    // ==================== 产品接口 ====================
    
    /**
     * 支付接口
     */
    public interface Payment {
        void pay(double amount);
        String getName();
    }
    
    // ==================== 具体产品 ====================
    
    /**
     * 支付宝支付
     */
    public static class AlipayPayment implements Payment {
        @Override
        public void pay(double amount) {
            System.out.println("[支付宝] 支付 " + amount + " 元");
        }
        
        @Override
        public String getName() {
            return "支付宝";
        }
    }
    
    /**
     * 微信支付
     */
    public static class WechatPayment implements Payment {
        @Override
        public void pay(double amount) {
            System.out.println("[微信支付] 支付 " + amount + " 元");
        }
        
        @Override
        public String getName() {
            return "微信支付";
        }
    }
    
    /**
     * 银联支付
     */
    public static class UnionPayPayment implements Payment {
        @Override
        public void pay(double amount) {
            System.out.println("[银联] 支付 " + amount + " 元");
        }
        
        @Override
        public String getName() {
            return "银联支付";
        }
    }
    
    // ==================== 简单工厂 ====================
    
    /**
     * 支付工厂 - 根据类型创建对应的支付方式
     */
    public static class PaymentFactory {
        
        public static Payment createPayment(String type) {
            if (type == null) {
                throw new IllegalArgumentException("支付类型不能为空");
            }
            
            switch (type.toLowerCase()) {
                case "alipay":
                    return new AlipayPayment();
                case "wechat":
                    return new WechatPayment();
                case "unionpay":
                    return new UnionPayPayment();
                default:
                    throw new IllegalArgumentException("不支持的支付类型: " + type);
            }
        }
    }
    
    // ==================== 测试 ====================
    
    public static void main(String[] args) {
        System.out.println("=== 简单工厂模式示例 ===\n");
        
        // 客户端通过工厂获取支付方式，不需要知道具体实现类
        Payment alipay = PaymentFactory.createPayment("alipay");
        Payment wechat = PaymentFactory.createPayment("wechat");
        Payment unionpay = PaymentFactory.createPayment("unionpay");
        
        System.out.println("创建的支付方式：");
        System.out.println("1. " + alipay.getName());
        System.out.println("2. " + wechat.getName());
        System.out.println("3. " + unionpay.getName());
        
        System.out.println("\n执行支付：");
        alipay.pay(100.00);
        wechat.pay(50.00);
        unionpay.pay(200.00);
        
        // 测试异常情况
        System.out.println("\n尝试创建不支持的支付方式：");
        try {
            PaymentFactory.createPayment("paypal");
        } catch (IllegalArgumentException e) {
            System.out.println("异常: " + e.getMessage());
        }
    }
}
