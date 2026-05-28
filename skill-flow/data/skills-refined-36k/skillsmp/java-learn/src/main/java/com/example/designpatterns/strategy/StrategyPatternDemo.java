package com.example.designpatterns.strategy;

import java.math.BigDecimal;
import java.math.RoundingMode;
import java.util.HashMap;
import java.util.Map;

/**
 * 策略模式示例
 * 
 * 场景：电商平台促销价格计算
 * 
 * 策略模式定义了一系列算法，把它们一个个封装起来，并且使它们可以相互替换。
 * 本模式使得算法可独立于使用它的客户而变化。
 * 
 * 特点：
 * 1. 定义一系列算法
 * 2. 将每个算法封装起来
 * 3. 算法之间可以相互替换
 * 4. 消除大量的 if-else 或 switch-case
 * 
 * @author java_learn
 */
public class StrategyPatternDemo {
    
    // ==================== 策略接口 ====================
    
    /**
     * 促销策略接口
     */
    public interface PromotionStrategy {
        /**
         * 计算促销后的价格
         * @param originalPrice 原价
         * @return 促销后的价格
         */
        BigDecimal calculatePrice(BigDecimal originalPrice);
        
        /**
         * 获取策略名称
         */
        String getName();
        
        /**
         * 获取策略描述
         */
        String getDescription();
    }
    
    // ==================== 具体策略 ====================
    
    /**
     * 无促销策略
     */
    public static class NoPromotionStrategy implements PromotionStrategy {
        @Override
        public BigDecimal calculatePrice(BigDecimal originalPrice) {
            return originalPrice;
        }
        
        @Override
        public String getName() {
            return "无促销";
        }
        
        @Override
        public String getDescription() {
            return "原价销售";
        }
    }
    
    /**
     * 折扣策略
     */
    public static class DiscountStrategy implements PromotionStrategy {
        private final BigDecimal discount; // 折扣率，如 0.8 表示 8 折
        
        public DiscountStrategy(double discount) {
            if (discount <= 0 || discount > 1) {
                throw new IllegalArgumentException("折扣率必须在 0 到 1 之间");
            }
            this.discount = BigDecimal.valueOf(discount);
        }
        
        @Override
        public BigDecimal calculatePrice(BigDecimal originalPrice) {
            return originalPrice.multiply(discount).setScale(2, RoundingMode.HALF_UP);
        }
        
        @Override
        public String getName() {
            return "折扣促销";
        }
        
        @Override
        public String getDescription() {
            return discount.multiply(BigDecimal.TEN).intValue() + " 折优惠";
        }
    }
    
    /**
     * 满减策略
     */
    public static class FullReductionStrategy implements PromotionStrategy {
        private final BigDecimal threshold; // 满减门槛
        private final BigDecimal reduction; // 减免金额
        
        public FullReductionStrategy(double threshold, double reduction) {
            this.threshold = BigDecimal.valueOf(threshold);
            this.reduction = BigDecimal.valueOf(reduction);
        }
        
        @Override
        public BigDecimal calculatePrice(BigDecimal originalPrice) {
            if (originalPrice.compareTo(threshold) >= 0) {
                BigDecimal result = originalPrice.subtract(reduction);
                return result.compareTo(BigDecimal.ZERO) > 0 ? result : BigDecimal.ZERO;
            }
            return originalPrice;
        }
        
        @Override
        public String getName() {
            return "满减促销";
        }
        
        @Override
        public String getDescription() {
            return "满 " + threshold + " 减 " + reduction;
        }
    }
    
    /**
     * 阶梯满减策略
     */
    public static class TieredReductionStrategy implements PromotionStrategy {
        private final Map<BigDecimal, BigDecimal> tiers = new HashMap<>();
        
        public TieredReductionStrategy() {
            // 阶梯满减规则
            tiers.put(BigDecimal.valueOf(100), BigDecimal.valueOf(10));
            tiers.put(BigDecimal.valueOf(200), BigDecimal.valueOf(30));
            tiers.put(BigDecimal.valueOf(300), BigDecimal.valueOf(50));
            tiers.put(BigDecimal.valueOf(500), BigDecimal.valueOf(100));
        }
        
        @Override
        public BigDecimal calculatePrice(BigDecimal originalPrice) {
            BigDecimal reduction = BigDecimal.ZERO;
            
            for (Map.Entry<BigDecimal, BigDecimal> tier : tiers.entrySet()) {
                if (originalPrice.compareTo(tier.getKey()) >= 0) {
                    if (tier.getValue().compareTo(reduction) > 0) {
                        reduction = tier.getValue();
                    }
                }
            }
            
            return originalPrice.subtract(reduction);
        }
        
        @Override
        public String getName() {
            return "阶梯满减";
        }
        
        @Override
        public String getDescription() {
            return "满100减10，满200减30，满300减50，满500减100";
        }
    }
    
    /**
     * 会员策略
     */
    public static class VipStrategy implements PromotionStrategy {
        private final int vipLevel;
        
        public VipStrategy(int vipLevel) {
            this.vipLevel = vipLevel;
        }
        
        @Override
        public BigDecimal calculatePrice(BigDecimal originalPrice) {
            BigDecimal discount;
            switch (vipLevel) {
                case 1:
                    discount = BigDecimal.valueOf(0.95);
                    break;
                case 2:
                    discount = BigDecimal.valueOf(0.90);
                    break;
                case 3:
                    discount = BigDecimal.valueOf(0.85);
                    break;
                case 4:
                    discount = BigDecimal.valueOf(0.80);
                    break;
                default:
                    discount = BigDecimal.ONE;
            }
            return originalPrice.multiply(discount).setScale(2, RoundingMode.HALF_UP);
        }
        
        @Override
        public String getName() {
            return "VIP会员";
        }
        
        @Override
        public String getDescription() {
            return "VIP" + vipLevel + " 会员折扣";
        }
    }
    
    // ==================== 上下文 ====================
    
    /**
     * 促销上下文 - 持有策略引用
     */
    public static class PromotionContext {
        private PromotionStrategy strategy;
        
        public PromotionContext() {
            this.strategy = new NoPromotionStrategy();
        }
        
        public PromotionContext(PromotionStrategy strategy) {
            this.strategy = strategy;
        }
        
        public void setStrategy(PromotionStrategy strategy) {
            this.strategy = strategy;
        }
        
        public BigDecimal executeStrategy(BigDecimal originalPrice) {
            return strategy.calculatePrice(originalPrice);
        }
        
        public void showPromotion() {
            System.out.println("当前策略: " + strategy.getName());
            System.out.println("描述: " + strategy.getDescription());
        }
    }
    
    // ==================== 策略工厂 (结合工厂模式) ====================
    
    /**
     * 策略工厂 - 避免客户端直接 new 策略对象
     */
    public static class StrategyFactory {
        private static final Map<String, PromotionStrategy> strategies = new HashMap<>();
        
        static {
            strategies.put("none", new NoPromotionStrategy());
            strategies.put("discount", new DiscountStrategy(0.8));
            strategies.put("fullReduction", new FullReductionStrategy(200, 30));
            strategies.put("tiered", new TieredReductionStrategy());
            strategies.put("vip1", new VipStrategy(1));
            strategies.put("vip2", new VipStrategy(2));
            strategies.put("vip3", new VipStrategy(3));
        }
        
        public static PromotionStrategy getStrategy(String type) {
            PromotionStrategy strategy = strategies.get(type);
            if (strategy == null) {
                throw new IllegalArgumentException("未知的策略类型: " + type);
            }
            return strategy;
        }
    }
    
    // ==================== 测试 ====================
    
    public static void main(String[] args) {
        System.out.println("=== 策略模式示例 - 电商促销 ===\n");
        
        BigDecimal originalPrice = BigDecimal.valueOf(250.00);
        System.out.println("商品原价: " + originalPrice + " 元\n");
        System.out.println("=".repeat(50));
        
        // 创建上下文
        PromotionContext context = new PromotionContext();
        
        // 测试各种策略
        String[] strategyTypes = {"none", "discount", "fullReduction", "tiered", "vip2"};
        
        for (String type : strategyTypes) {
            PromotionStrategy strategy = StrategyFactory.getStrategy(type);
            context.setStrategy(strategy);
            
            System.out.println();
            context.showPromotion();
            BigDecimal finalPrice = context.executeStrategy(originalPrice);
            System.out.println("促销后价格: " + finalPrice + " 元");
            System.out.println("节省: " + originalPrice.subtract(finalPrice) + " 元");
            System.out.println("-".repeat(50));
        }
        
        // 演示策略的动态切换
        System.out.println("\n=== 动态切换策略 ===");
        System.out.println("用户升级为 VIP3，重新计算价格...");
        context.setStrategy(new VipStrategy(3));
        context.showPromotion();
        System.out.println("VIP3 价格: " + context.executeStrategy(originalPrice) + " 元");
    }
}
