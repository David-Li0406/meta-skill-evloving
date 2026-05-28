# 模板方法模式 (Template Method Pattern)

## 一、什么是模板方法模式

模板方法模式是一种行为型设计模式，它在父类中定义算法的骨架，将某些步骤的实现延迟到子类中。模板方法使得子类可以在不改变算法结构的情况下，重新定义算法的某些步骤。

### 核心思想
- **定义算法骨架**：父类定义算法的整体流程
- **延迟实现**：具体步骤由子类实现
- **钩子方法**：提供可选的扩展点

## 二、模板方法模式结构

```
┌─────────────────────────────┐
│      AbstractClass          │
│  +templateMethod()          │  // 模板方法，定义算法骨架
│  +primitiveOperation1()     │  // 抽象方法，子类必须实现
│  +primitiveOperation2()     │  // 抽象方法，子类必须实现
│  +hook()                    │  // 钩子方法，子类可选覆盖
└─────────────────────────────┘
              △
              │
     ┌────────┴────────┐
     │                 │
┌────┴─────┐    ┌──────┴────┐
│ConcreteA │    │ ConcreteB │
└──────────┘    └───────────┘
```

## 三、基本实现

```java
/**
 * 抽象类 - 定义模板方法
 */
public abstract class AbstractClass {
    
    /**
     * 模板方法 - 定义算法骨架
     * 使用 final 防止子类覆盖
     */
    public final void templateMethod() {
        // 步骤1：固定实现
        step1();
        
        // 步骤2：子类实现
        step2();
        
        // 步骤3：子类实现
        step3();
        
        // 步骤4：钩子方法，可选实现
        if (hook()) {
            step4();
        }
    }
    
    // 固定实现的步骤
    private void step1() {
        System.out.println("执行步骤1 - 固定实现");
    }
    
    // 抽象方法 - 子类必须实现
    protected abstract void step2();
    
    // 抽象方法 - 子类必须实现
    protected abstract void step3();
    
    // 可选步骤
    private void step4() {
        System.out.println("执行步骤4 - 可选步骤");
    }
    
    /**
     * 钩子方法 - 子类可选覆盖
     * 默认返回 true，表示执行 step4
     */
    protected boolean hook() {
        return true;
    }
}

/**
 * 具体实现类 A
 */
public class ConcreteClassA extends AbstractClass {
    
    @Override
    protected void step2() {
        System.out.println("ConcreteA: 执行步骤2");
    }
    
    @Override
    protected void step3() {
        System.out.println("ConcreteA: 执行步骤3");
    }
}

/**
 * 具体实现类 B
 */
public class ConcreteClassB extends AbstractClass {
    
    @Override
    protected void step2() {
        System.out.println("ConcreteB: 执行步骤2");
    }
    
    @Override
    protected void step3() {
        System.out.println("ConcreteB: 执行步骤3");
    }
    
    // 覆盖钩子方法，不执行 step4
    @Override
    protected boolean hook() {
        return false;
    }
}
```

## 四、实际应用案例

### 4.1 数据导出模板

```java
/**
 * 数据导出抽象模板
 */
public abstract class DataExporter<T> {
    
    /**
     * 模板方法 - 导出数据
     */
    public final void export(String destination) {
        // 1. 开始导出
        beforeExport();
        
        // 2. 查询数据
        List<T> data = queryData();
        
        if (data.isEmpty()) {
            System.out.println("没有数据需要导出");
            return;
        }
        
        // 3. 转换数据
        String content = convertData(data);
        
        // 4. 写入文件
        writeToFile(content, destination);
        
        // 5. 结束导出
        afterExport();
    }
    
    // 钩子方法 - 导出前操作
    protected void beforeExport() {
        System.out.println("开始导出数据...");
    }
    
    // 抽象方法 - 查询数据
    protected abstract List<T> queryData();
    
    // 抽象方法 - 转换数据格式
    protected abstract String convertData(List<T> data);
    
    // 通用方法 - 写入文件
    private void writeToFile(String content, String destination) {
        try {
            Files.write(Paths.get(destination), content.getBytes());
            System.out.println("数据已写入: " + destination);
        } catch (IOException e) {
            throw new RuntimeException("写入文件失败", e);
        }
    }
    
    // 钩子方法 - 导出后操作
    protected void afterExport() {
        System.out.println("导出完成");
    }
}

/**
 * CSV 导出器
 */
public class CsvExporter extends DataExporter<User> {
    
    private UserRepository userRepository;
    
    @Override
    protected List<User> queryData() {
        return userRepository.findAll();
    }
    
    @Override
    protected String convertData(List<User> data) {
        StringBuilder sb = new StringBuilder();
        sb.append("ID,姓名,邮箱,手机\n");
        for (User user : data) {
            sb.append(String.format("%d,%s,%s,%s\n",
                user.getId(),
                user.getName(),
                user.getEmail(),
                user.getPhone()
            ));
        }
        return sb.toString();
    }
}

/**
 * Excel 导出器
 */
public class ExcelExporter extends DataExporter<Order> {
    
    private OrderRepository orderRepository;
    
    @Override
    protected List<Order> queryData() {
        return orderRepository.findAll();
    }
    
    @Override
    protected String convertData(List<Order> data) {
        // 实际应使用 POI 等库生成 Excel
        // 这里简化为 TSV 格式
        StringBuilder sb = new StringBuilder();
        sb.append("订单ID\t用户ID\t金额\t状态\n");
        for (Order order : data) {
            sb.append(String.format("%s\t%d\t%.2f\t%s\n",
                order.getOrderId(),
                order.getUserId(),
                order.getAmount(),
                order.getStatus()
            ));
        }
        return sb.toString();
    }
    
    @Override
    protected void afterExport() {
        super.afterExport();
        // 发送通知
        System.out.println("导出完成，已发送邮件通知");
    }
}
```

### 4.2 支付流程模板

```java
/**
 * 支付流程模板
 */
public abstract class PaymentTemplate {
    
    /**
     * 支付流程 - 模板方法
     */
    public final PaymentResult pay(PaymentRequest request) {
        try {
            // 1. 参数校验
            validate(request);
            
            // 2. 创建订单
            String orderId = createOrder(request);
            
            // 3. 调用支付
            PaymentResponse response = doPayment(request, orderId);
            
            // 4. 处理支付结果
            PaymentResult result = handleResponse(response);
            
            // 5. 记录日志
            logPayment(request, result);
            
            // 6. 通知（钩子方法）
            if (needNotify()) {
                notify(request, result);
            }
            
            return result;
            
        } catch (Exception e) {
            return handleException(e);
        }
    }
    
    // 参数校验 - 通用实现
    protected void validate(PaymentRequest request) {
        if (request.getAmount() == null || request.getAmount().compareTo(BigDecimal.ZERO) <= 0) {
            throw new IllegalArgumentException("支付金额必须大于0");
        }
    }
    
    // 创建订单 - 通用实现
    protected String createOrder(PaymentRequest request) {
        return "ORD" + System.currentTimeMillis();
    }
    
    // 支付实现 - 抽象方法，子类实现
    protected abstract PaymentResponse doPayment(PaymentRequest request, String orderId);
    
    // 处理响应 - 通用实现
    protected PaymentResult handleResponse(PaymentResponse response) {
        PaymentResult result = new PaymentResult();
        result.setSuccess(response.isSuccess());
        result.setMessage(response.getMessage());
        result.setTransactionId(response.getTransactionId());
        return result;
    }
    
    // 记录日志 - 通用实现
    protected void logPayment(PaymentRequest request, PaymentResult result) {
        System.out.println("支付记录: " + request + " -> " + result);
    }
    
    // 钩子方法 - 是否需要通知
    protected boolean needNotify() {
        return true;
    }
    
    // 通知 - 子类可覆盖
    protected void notify(PaymentRequest request, PaymentResult result) {
        System.out.println("发送支付通知");
    }
    
    // 异常处理 - 通用实现
    protected PaymentResult handleException(Exception e) {
        PaymentResult result = new PaymentResult();
        result.setSuccess(false);
        result.setMessage("支付失败: " + e.getMessage());
        return result;
    }
}

/**
 * 支付宝支付
 */
public class AlipayPayment extends PaymentTemplate {
    
    @Override
    protected PaymentResponse doPayment(PaymentRequest request, String orderId) {
        System.out.println("调用支付宝支付接口");
        // 调用支付宝 SDK
        PaymentResponse response = new PaymentResponse();
        response.setSuccess(true);
        response.setTransactionId("ALIPAY_" + orderId);
        response.setMessage("支付成功");
        return response;
    }
}

/**
 * 微信支付
 */
public class WechatPayment extends PaymentTemplate {
    
    @Override
    protected PaymentResponse doPayment(PaymentRequest request, String orderId) {
        System.out.println("调用微信支付接口");
        // 调用微信支付 SDK
        PaymentResponse response = new PaymentResponse();
        response.setSuccess(true);
        response.setTransactionId("WECHAT_" + orderId);
        response.setMessage("支付成功");
        return response;
    }
    
    @Override
    protected boolean needNotify() {
        // 微信支付不需要额外通知
        return false;
    }
}
```

### 4.3 数据库操作模板

```java
/**
 * JDBC 操作模板
 */
public abstract class JdbcTemplate<T> {
    
    private DataSource dataSource;
    
    public JdbcTemplate(DataSource dataSource) {
        this.dataSource = dataSource;
    }
    
    /**
     * 查询操作模板方法
     */
    public final List<T> query(String sql, Object... params) {
        Connection conn = null;
        PreparedStatement ps = null;
        ResultSet rs = null;
        
        try {
            // 1. 获取连接
            conn = getConnection();
            
            // 2. 创建 PreparedStatement
            ps = createPreparedStatement(conn, sql);
            
            // 3. 设置参数
            setParameters(ps, params);
            
            // 4. 执行查询
            rs = executeQuery(ps);
            
            // 5. 处理结果集 - 抽象方法
            return handleResultSet(rs);
            
        } catch (SQLException e) {
            throw new RuntimeException("查询失败", e);
        } finally {
            // 6. 关闭资源
            closeResources(conn, ps, rs);
        }
    }
    
    /**
     * 更新操作模板方法
     */
    public final int update(String sql, Object... params) {
        Connection conn = null;
        PreparedStatement ps = null;
        
        try {
            conn = getConnection();
            ps = createPreparedStatement(conn, sql);
            setParameters(ps, params);
            return ps.executeUpdate();
        } catch (SQLException e) {
            throw new RuntimeException("更新失败", e);
        } finally {
            closeResources(conn, ps, null);
        }
    }
    
    protected Connection getConnection() throws SQLException {
        return dataSource.getConnection();
    }
    
    protected PreparedStatement createPreparedStatement(Connection conn, String sql) 
            throws SQLException {
        return conn.prepareStatement(sql);
    }
    
    protected void setParameters(PreparedStatement ps, Object... params) 
            throws SQLException {
        for (int i = 0; i < params.length; i++) {
            ps.setObject(i + 1, params[i]);
        }
    }
    
    protected ResultSet executeQuery(PreparedStatement ps) throws SQLException {
        return ps.executeQuery();
    }
    
    // 抽象方法 - 子类实现结果集映射
    protected abstract List<T> handleResultSet(ResultSet rs) throws SQLException;
    
    protected void closeResources(Connection conn, PreparedStatement ps, ResultSet rs) {
        try {
            if (rs != null) rs.close();
            if (ps != null) ps.close();
            if (conn != null) conn.close();
        } catch (SQLException e) {
            // ignore
        }
    }
}

/**
 * 用户查询模板
 */
public class UserJdbcTemplate extends JdbcTemplate<User> {
    
    public UserJdbcTemplate(DataSource dataSource) {
        super(dataSource);
    }
    
    @Override
    protected List<User> handleResultSet(ResultSet rs) throws SQLException {
        List<User> users = new ArrayList<>();
        while (rs.next()) {
            User user = new User();
            user.setId(rs.getLong("id"));
            user.setName(rs.getString("name"));
            user.setEmail(rs.getString("email"));
            users.add(user);
        }
        return users;
    }
}
```

### 4.4 Servlet 中的模板方法

```java
/**
 * HttpServlet 就是典型的模板方法模式
 */
public abstract class HttpServlet extends GenericServlet {
    
    // 模板方法
    protected void service(HttpServletRequest req, HttpServletResponse resp) {
        String method = req.getMethod();
        
        if (method.equals("GET")) {
            doGet(req, resp);
        } else if (method.equals("POST")) {
            doPost(req, resp);
        } else if (method.equals("PUT")) {
            doPut(req, resp);
        } else if (method.equals("DELETE")) {
            doDelete(req, resp);
        }
        // ...
    }
    
    // 子类可以覆盖这些方法
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) {
        // 默认实现
    }
    
    protected void doPost(HttpServletRequest req, HttpServletResponse resp) {
        // 默认实现
    }
    
    protected void doPut(HttpServletRequest req, HttpServletResponse resp) {
        // 默认实现
    }
    
    protected void doDelete(HttpServletRequest req, HttpServletResponse resp) {
        // 默认实现
    }
}
```

## 五、模板方法在框架中的应用

### 5.1 Spring 中的 JdbcTemplate

```java
// Spring 的 JdbcTemplate 使用回调模式（模板方法的变体）
public class JdbcTemplate {
    
    public <T> T query(String sql, ResultSetExtractor<T> rse) {
        // 获取连接、创建语句、执行查询
        // 调用 rse.extractData(rs) 处理结果
        // 关闭资源
    }
    
    public <T> List<T> query(String sql, RowMapper<T> rowMapper) {
        // 获取连接、创建语句、执行查询
        // 遍历结果集，调用 rowMapper.mapRow(rs, rowNum)
        // 关闭资源
    }
}
```

### 5.2 Spring 中的 AbstractApplicationContext

```java
// Spring 容器刷新流程
public abstract class AbstractApplicationContext {
    
    public void refresh() {
        // 1. 准备刷新
        prepareRefresh();
        
        // 2. 获取 BeanFactory
        ConfigurableListableBeanFactory beanFactory = obtainFreshBeanFactory();
        
        // 3. 准备 BeanFactory
        prepareBeanFactory(beanFactory);
        
        // 4. 后处理 BeanFactory - 钩子方法
        postProcessBeanFactory(beanFactory);
        
        // 5. 调用 BeanFactoryPostProcessor
        invokeBeanFactoryPostProcessors(beanFactory);
        
        // 6. 注册 BeanPostProcessor
        registerBeanPostProcessors(beanFactory);
        
        // ... 更多步骤
        
        // 12. 完成刷新 - 钩子方法
        finishRefresh();
    }
    
    // 钩子方法
    protected void postProcessBeanFactory(ConfigurableListableBeanFactory beanFactory) {
    }
    
    protected void finishRefresh() {
    }
}
```

## 六、模板方法 vs 策略模式

| 特性 | 模板方法模式 | 策略模式 |
|------|------------|---------|
| 关系 | 继承 | 组合 |
| 控制权 | 父类控制算法流程 | 客户端控制策略选择 |
| 变化点 | 算法的某些步骤 | 整个算法 |
| 扩展方式 | 继承抽象类 | 实现策略接口 |
| 运行时切换 | 不可以 | 可以 |

## 七、优缺点

### 优点
1. **复用代码**：公共代码放在父类中，避免重复
2. **扩展灵活**：子类可以灵活实现具体步骤
3. **符合开闭原则**：新增实现只需新增子类
4. **控制反转**：父类调用子类方法，而非子类调用父类

### 缺点
1. **继承的缺点**：子类与父类紧密耦合
2. **限制灵活性**：算法骨架固定，无法运行时改变
3. **可能违反里氏替换**：子类实现可能改变父类行为

## 八、面试常见问题

### Q1: 模板方法模式的核心是什么？
> 答：定义算法骨架，将具体步骤延迟到子类实现。父类控制整体流程，子类负责具体实现。

### Q2: 什么是钩子方法？
> 答：钩子方法是父类中提供的空实现或默认实现的方法，子类可以选择性覆盖来影响模板方法的执行流程。

### Q3: 模板方法和策略模式如何选择？
> 答：如果算法骨架固定，只有部分步骤变化，用模板方法；如果整个算法需要替换，用策略模式。

### Q4: Spring 中哪里使用了模板方法模式？
> 答：JdbcTemplate、RestTemplate、AbstractApplicationContext、HttpServlet 等都是模板方法模式的应用。
