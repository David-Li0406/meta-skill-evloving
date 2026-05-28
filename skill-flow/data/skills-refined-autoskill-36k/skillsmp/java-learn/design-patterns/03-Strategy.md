# 策略模式 (Strategy Pattern)

## 一、什么是策略模式

策略模式是一种行为型设计模式，它定义了一系列算法，将每个算法封装起来，并使它们可以相互替换。策略模式让算法的变化独立于使用算法的客户端。

### 核心思想
- **封装变化**：将易变的算法封装成独立的策略类
- **面向接口编程**：客户端依赖抽象策略接口
- **组合优于继承**：通过组合策略对象实现行为变化

## 二、策略模式结构

```
┌─────────────────┐
│    Context      │
│  -strategy      │───────────────┐
│  +execute()     │               │
└─────────────────┘               │
                                  ▼
                        ┌─────────────────┐
                        │   <<interface>> │
                        │    Strategy     │
                        │   +algorithm()  │
                        └─────────────────┘
                                  △
                                  │
                    ┌─────────────┼─────────────┐
                    │             │             │
          ┌─────────┴───┐ ┌──────┴──────┐ ┌────┴────────┐
          │ StrategyA   │ │  StrategyB  │ │  StrategyC  │
          └─────────────┘ └─────────────┘ └─────────────┘
```

## 三、基本实现

```java
/**
 * 策略接口
 */
public interface Strategy {
    void execute();
}

/**
 * 具体策略A
 */
public class ConcreteStrategyA implements Strategy {
    @Override
    public void execute() {
        System.out.println("执行策略A");
    }
}

/**
 * 具体策略B
 */
public class ConcreteStrategyB implements Strategy {
    @Override
    public void execute() {
        System.out.println("执行策略B");
    }
}

/**
 * 上下文类
 */
public class Context {
    private Strategy strategy;
    
    public Context(Strategy strategy) {
        this.strategy = strategy;
    }
    
    // 可以动态切换策略
    public void setStrategy(Strategy strategy) {
        this.strategy = strategy;
    }
    
    public void executeStrategy() {
        strategy.execute();
    }
}

// 使用示例
public class Client {
    public static void main(String[] args) {
        Context context = new Context(new ConcreteStrategyA());
        context.executeStrategy(); // 执行策略A
        
        context.setStrategy(new ConcreteStrategyB());
        context.executeStrategy(); // 执行策略B
    }
}
```

## 四、实际应用案例

### 4.1 支付策略

```java
/**
 * 支付策略接口
 */
public interface PaymentStrategy {
    /**
     * 执行支付
     * @param amount 支付金额
     * @return 支付结果
     */
    PaymentResult pay(BigDecimal amount);
    
    /**
     * 获取支付方式名称
     */
    String getPaymentType();
}

/**
 * 支付结果
 */
@Data
public class PaymentResult {
    private boolean success;
    private String transactionId;
    private String message;
}

/**
 * 支付宝支付策略
 */
@Service
public class AlipayStrategy implements PaymentStrategy {
    
    @Override
    public PaymentResult pay(BigDecimal amount) {
        PaymentResult result = new PaymentResult();
        // 调用支付宝 SDK
        System.out.println("调用支付宝支付接口，金额: " + amount);
        result.setSuccess(true);
        result.setTransactionId(UUID.randomUUID().toString());
        result.setMessage("支付宝支付成功");
        return result;
    }
    
    @Override
    public String getPaymentType() {
        return "ALIPAY";
    }
}

/**
 * 微信支付策略
 */
@Service
public class WechatPayStrategy implements PaymentStrategy {
    
    @Override
    public PaymentResult pay(BigDecimal amount) {
        PaymentResult result = new PaymentResult();
        // 调用微信支付 SDK
        System.out.println("调用微信支付接口，金额: " + amount);
        result.setSuccess(true);
        result.setTransactionId(UUID.randomUUID().toString());
        result.setMessage("微信支付成功");
        return result;
    }
    
    @Override
    public String getPaymentType() {
        return "WECHAT";
    }
}

/**
 * 银联支付策略
 */
@Service
public class UnionPayStrategy implements PaymentStrategy {
    
    @Override
    public PaymentResult pay(BigDecimal amount) {
        PaymentResult result = new PaymentResult();
        System.out.println("调用银联支付接口，金额: " + amount);
        result.setSuccess(true);
        result.setTransactionId(UUID.randomUUID().toString());
        result.setMessage("银联支付成功");
        return result;
    }
    
    @Override
    public String getPaymentType() {
        return "UNIONPAY";
    }
}

/**
 * 支付上下文 - Spring 版本
 */
@Service
public class PaymentContext {
    
    private final Map<String, PaymentStrategy> strategyMap;
    
    // Spring 自动注入所有 PaymentStrategy 实现
    @Autowired
    public PaymentContext(List<PaymentStrategy> strategies) {
        strategyMap = strategies.stream()
            .collect(Collectors.toMap(
                PaymentStrategy::getPaymentType,
                Function.identity()
            ));
    }
    
    /**
     * 执行支付
     */
    public PaymentResult pay(String paymentType, BigDecimal amount) {
        PaymentStrategy strategy = strategyMap.get(paymentType);
        if (strategy == null) {
            throw new IllegalArgumentException("不支持的支付方式: " + paymentType);
        }
        return strategy.pay(amount);
    }
    
    /**
     * 获取所有支持的支付方式
     */
    public Set<String> getSupportedPaymentTypes() {
        return strategyMap.keySet();
    }
}
```

### 4.2 折扣策略

```java
/**
 * 折扣策略接口
 */
public interface DiscountStrategy {
    /**
     * 计算折扣后价格
     * @param originalPrice 原价
     * @return 折扣后价格
     */
    BigDecimal calculate(BigDecimal originalPrice);
    
    /**
     * 获取策略类型
     */
    String getType();
}

/**
 * 无折扣
 */
public class NoDiscountStrategy implements DiscountStrategy {
    @Override
    public BigDecimal calculate(BigDecimal originalPrice) {
        return originalPrice;
    }
    
    @Override
    public String getType() {
        return "NONE";
    }
}

/**
 * 满减折扣
 */
public class FullReductionStrategy implements DiscountStrategy {
    private BigDecimal threshold; // 满多少
    private BigDecimal reduction; // 减多少
    
    public FullReductionStrategy(BigDecimal threshold, BigDecimal reduction) {
        this.threshold = threshold;
        this.reduction = reduction;
    }
    
    @Override
    public BigDecimal calculate(BigDecimal originalPrice) {
        if (originalPrice.compareTo(threshold) >= 0) {
            return originalPrice.subtract(reduction);
        }
        return originalPrice;
    }
    
    @Override
    public String getType() {
        return "FULL_REDUCTION";
    }
}

/**
 * 百分比折扣
 */
public class PercentageDiscountStrategy implements DiscountStrategy {
    private BigDecimal discountRate; // 折扣率，如 0.8 表示 8 折
    
    public PercentageDiscountStrategy(BigDecimal discountRate) {
        this.discountRate = discountRate;
    }
    
    @Override
    public BigDecimal calculate(BigDecimal originalPrice) {
        return originalPrice.multiply(discountRate)
            .setScale(2, RoundingMode.HALF_UP);
    }
    
    @Override
    public String getType() {
        return "PERCENTAGE";
    }
}

/**
 * VIP 会员折扣
 */
public class VipDiscountStrategy implements DiscountStrategy {
    private int vipLevel;
    
    public VipDiscountStrategy(int vipLevel) {
        this.vipLevel = vipLevel;
    }
    
    @Override
    public BigDecimal calculate(BigDecimal originalPrice) {
        // VIP 等级越高，折扣越大
        BigDecimal discount = BigDecimal.ONE.subtract(
            new BigDecimal("0.05").multiply(new BigDecimal(vipLevel))
        );
        return originalPrice.multiply(discount)
            .setScale(2, RoundingMode.HALF_UP);
    }
    
    @Override
    public String getType() {
        return "VIP";
    }
}

/**
 * 价格计算器
 */
public class PriceCalculator {
    private DiscountStrategy strategy = new NoDiscountStrategy();
    
    public void setStrategy(DiscountStrategy strategy) {
        this.strategy = strategy;
    }
    
    public BigDecimal calculate(BigDecimal originalPrice) {
        return strategy.calculate(originalPrice);
    }
}
```

### 4.3 排序策略

```java
/**
 * 排序策略接口
 */
public interface SortStrategy<T> {
    void sort(List<T> list, Comparator<T> comparator);
    String getName();
}

/**
 * 快速排序策略
 */
public class QuickSortStrategy<T> implements SortStrategy<T> {
    @Override
    public void sort(List<T> list, Comparator<T> comparator) {
        quickSort(list, 0, list.size() - 1, comparator);
    }
    
    private void quickSort(List<T> list, int low, int high, Comparator<T> comparator) {
        if (low < high) {
            int pi = partition(list, low, high, comparator);
            quickSort(list, low, pi - 1, comparator);
            quickSort(list, pi + 1, high, comparator);
        }
    }
    
    private int partition(List<T> list, int low, int high, Comparator<T> comparator) {
        T pivot = list.get(high);
        int i = low - 1;
        for (int j = low; j < high; j++) {
            if (comparator.compare(list.get(j), pivot) <= 0) {
                i++;
                Collections.swap(list, i, j);
            }
        }
        Collections.swap(list, i + 1, high);
        return i + 1;
    }
    
    @Override
    public String getName() {
        return "QuickSort";
    }
}

/**
 * 归并排序策略
 */
public class MergeSortStrategy<T> implements SortStrategy<T> {
    @Override
    public void sort(List<T> list, Comparator<T> comparator) {
        if (list.size() > 1) {
            mergeSort(list, comparator);
        }
    }
    
    private void mergeSort(List<T> list, Comparator<T> comparator) {
        // 归并排序实现
        Collections.sort(list, comparator); // 简化实现
    }
    
    @Override
    public String getName() {
        return "MergeSort";
    }
}

/**
 * 排序上下文
 */
public class Sorter<T> {
    private SortStrategy<T> strategy;
    
    public Sorter(SortStrategy<T> strategy) {
        this.strategy = strategy;
    }
    
    public void setStrategy(SortStrategy<T> strategy) {
        this.strategy = strategy;
    }
    
    public void sort(List<T> list, Comparator<T> comparator) {
        long start = System.currentTimeMillis();
        strategy.sort(list, comparator);
        long end = System.currentTimeMillis();
        System.out.println(strategy.getName() + " 耗时: " + (end - start) + "ms");
    }
}
```

### 4.4 文件压缩策略

```java
/**
 * 压缩策略接口
 */
public interface CompressionStrategy {
    byte[] compress(byte[] data);
    byte[] decompress(byte[] data);
    String getExtension();
}

/**
 * ZIP 压缩策略
 */
public class ZipCompressionStrategy implements CompressionStrategy {
    @Override
    public byte[] compress(byte[] data) {
        try (ByteArrayOutputStream baos = new ByteArrayOutputStream();
             ZipOutputStream zos = new ZipOutputStream(baos)) {
            zos.putNextEntry(new ZipEntry("data"));
            zos.write(data);
            zos.closeEntry();
            return baos.toByteArray();
        } catch (IOException e) {
            throw new RuntimeException("压缩失败", e);
        }
    }
    
    @Override
    public byte[] decompress(byte[] data) {
        try (ZipInputStream zis = new ZipInputStream(new ByteArrayInputStream(data));
             ByteArrayOutputStream baos = new ByteArrayOutputStream()) {
            zis.getNextEntry();
            byte[] buffer = new byte[1024];
            int len;
            while ((len = zis.read(buffer)) > 0) {
                baos.write(buffer, 0, len);
            }
            return baos.toByteArray();
        } catch (IOException e) {
            throw new RuntimeException("解压失败", e);
        }
    }
    
    @Override
    public String getExtension() {
        return ".zip";
    }
}

/**
 * GZIP 压缩策略
 */
public class GzipCompressionStrategy implements CompressionStrategy {
    @Override
    public byte[] compress(byte[] data) {
        try (ByteArrayOutputStream baos = new ByteArrayOutputStream();
             GZIPOutputStream gzos = new GZIPOutputStream(baos)) {
            gzos.write(data);
            gzos.finish();
            return baos.toByteArray();
        } catch (IOException e) {
            throw new RuntimeException("GZIP 压缩失败", e);
        }
    }
    
    @Override
    public byte[] decompress(byte[] data) {
        try (GZIPInputStream gzis = new GZIPInputStream(new ByteArrayInputStream(data));
             ByteArrayOutputStream baos = new ByteArrayOutputStream()) {
            byte[] buffer = new byte[1024];
            int len;
            while ((len = gzis.read(buffer)) > 0) {
                baos.write(buffer, 0, len);
            }
            return baos.toByteArray();
        } catch (IOException e) {
            throw new RuntimeException("GZIP 解压失败", e);
        }
    }
    
    @Override
    public String getExtension() {
        return ".gz";
    }
}

/**
 * 文件压缩器
 */
public class FileCompressor {
    private CompressionStrategy strategy;
    
    public FileCompressor(CompressionStrategy strategy) {
        this.strategy = strategy;
    }
    
    public void compressFile(String inputPath, String outputPath) throws IOException {
        byte[] data = Files.readAllBytes(Paths.get(inputPath));
        byte[] compressed = strategy.compress(data);
        Files.write(Paths.get(outputPath + strategy.getExtension()), compressed);
    }
}
```

## 五、策略模式 + 工厂模式

```java
/**
 * 策略工厂 - 消除 if-else
 */
public class StrategyFactory {
    
    private static final Map<String, Supplier<PaymentStrategy>> STRATEGIES = 
        new HashMap<>();
    
    static {
        STRATEGIES.put("ALIPAY", AlipayStrategy::new);
        STRATEGIES.put("WECHAT", WechatPayStrategy::new);
        STRATEGIES.put("UNIONPAY", UnionPayStrategy::new);
    }
    
    public static PaymentStrategy getStrategy(String type) {
        Supplier<PaymentStrategy> supplier = STRATEGIES.get(type);
        if (supplier == null) {
            throw new IllegalArgumentException("不支持的支付类型: " + type);
        }
        return supplier.get();
    }
    
    // 动态注册策略
    public static void register(String type, Supplier<PaymentStrategy> supplier) {
        STRATEGIES.put(type, supplier);
    }
}
```

## 六、策略模式在框架中的应用

### 6.1 Spring 中的 Resource 加载策略

```java
// Spring 根据不同前缀使用不同策略加载资源
Resource resource1 = new ClassPathResource("config.xml");
Resource resource2 = new FileSystemResource("/path/to/file");
Resource resource3 = new UrlResource("http://example.com/file");
```

### 6.2 Comparator 比较策略

```java
List<User> users = new ArrayList<>();

// 按年龄排序策略
users.sort(Comparator.comparing(User::getAge));

// 按姓名排序策略
users.sort(Comparator.comparing(User::getName));

// 组合排序策略
users.sort(Comparator.comparing(User::getAge)
    .thenComparing(User::getName));
```

### 6.3 线程池拒绝策略

```java
// JDK 线程池的拒绝策略就是策略模式
ThreadPoolExecutor executor = new ThreadPoolExecutor(
    10, 20, 60, TimeUnit.SECONDS,
    new LinkedBlockingQueue<>(100),
    new ThreadPoolExecutor.CallerRunsPolicy() // 拒绝策略
);

// 可选的拒绝策略：
// AbortPolicy - 抛出异常
// CallerRunsPolicy - 调用者线程执行
// DiscardPolicy - 直接丢弃
// DiscardOldestPolicy - 丢弃最老的任务
```

## 七、策略模式优缺点

### 优点
1. **遵循开闭原则**：新增策略无需修改现有代码
2. **避免多重条件判断**：消除大量 if-else 或 switch-case
3. **算法可复用**：策略类可以在不同上下文中使用
4. **算法可切换**：运行时动态切换策略

### 缺点
1. **策略类增多**：每个策略都需要一个类
2. **客户端需知道策略**：客户端需要了解不同策略的区别
3. **通信开销**：策略接口可能暴露了不必要的方法

## 八、面试常见问题

### Q1: 策略模式和状态模式的区别？
> 答：策略模式由客户端决定使用哪个策略；状态模式由上下文内部状态决定行为。策略之间是平等的，可互换的；状态之间存在转换关系。

### Q2: 如何避免策略类膨胀？
> 答：1）使用 Lambda 表达式代替策略类；2）使用枚举实现简单策略；3）使用策略工厂集中管理。

### Q3: 策略模式如何与 Spring 集成？
> 答：将策略类定义为 Spring Bean，通过注入 List 或 Map 的方式收集所有策略实现，在 Context 中根据条件选择合适的策略。

### Q4: 什么场景下使用策略模式？
> 答：1）系统需要在多种算法中选择一种；2）需要避免大量条件判断；3）算法需要自由切换或扩展。
