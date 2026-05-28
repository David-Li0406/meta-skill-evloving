# Spring 事务详解

## 一、事务基础

### 1.1 事务的 ACID 特性

| 特性 | 说明 |
|------|------|
| **原子性（Atomicity）** | 事务是最小执行单位，要么全部成功，要么全部回滚 |
| **一致性（Consistency）** | 事务执行前后，数据库状态保持一致 |
| **隔离性（Isolation）** | 并发事务之间相互隔离，互不影响 |
| **持久性（Durability）** | 事务提交后，数据永久保存 |

### 1.2 Spring 事务管理

```java
// 编程式事务
@Autowired
private TransactionTemplate transactionTemplate;

public void transfer() {
    transactionTemplate.execute(status -> {
        // 业务逻辑
        return null;
    });
}

// 声明式事务（推荐）
@Transactional
public void transfer() {
    // 业务逻辑
}
```

## 二、事务传播机制

### 2.1 七种传播行为

| 传播行为 | 说明 | 使用场景 |
|---------|------|---------|
| **REQUIRED（默认）** | 有事务就加入，没有就创建新事务 | 大多数业务方法 |
| **SUPPORTS** | 有事务就加入，没有就非事务运行 | 查询方法 |
| **MANDATORY** | 必须有事务，没有就抛异常 | 必须在事务中调用 |
| **REQUIRES_NEW** | 总是创建新事务，挂起当前事务 | 日志记录、审计 |
| **NOT_SUPPORTED** | 非事务运行，挂起当前事务 | 某些不需要事务的操作 |
| **NEVER** | 非事务运行，有事务就抛异常 | 确保不在事务中运行 |
| **NESTED** | 有事务就创建嵌套事务，没有就创建新事务 | 部分回滚 |

### 2.2 传播行为详解

```java
@Service
public class OrderService {
    
    @Autowired
    private OrderRepository orderRepository;
    
    @Autowired
    private LogService logService;
    
    /**
     * REQUIRED - 默认传播行为
     * 如果当前有事务，就加入；没有就创建新事务
     */
    @Transactional(propagation = Propagation.REQUIRED)
    public void createOrder(Order order) {
        orderRepository.save(order);
        // 调用日志服务，共用同一个事务
        logService.log("创建订单: " + order.getId());
    }
}

@Service
public class LogService {
    
    /**
     * REQUIRES_NEW - 总是创建新事务
     * 挂起当前事务，创建独立的新事务
     */
    @Transactional(propagation = Propagation.REQUIRES_NEW)
    public void log(String message) {
        // 即使外层事务回滚，日志也会保存
        logRepository.save(new Log(message));
    }
    
    /**
     * NESTED - 嵌套事务
     * 创建一个保存点，可以单独回滚到保存点
     */
    @Transactional(propagation = Propagation.NESTED)
    public void logWithNested(String message) {
        // 如果这里异常，只回滚到保存点，外层事务可以选择继续
        logRepository.save(new Log(message));
    }
}
```

### 2.3 传播行为流程图

```
REQUIRED（默认）:
┌─────────────────────────────────────┐
│ ServiceA.methodA() [事务A]          │
│   │                                 │
│   └─> ServiceB.methodB() [加入事务A] │
│                                     │
│   methodB 和 methodA 共用事务A       │
│   任何一个回滚，整个事务都回滚        │
└─────────────────────────────────────┘

REQUIRES_NEW:
┌─────────────────────────────────────┐
│ ServiceA.methodA() [事务A]          │
│   │                                 │
│   │  ┌─────────────────────────┐   │
│   └─>│ ServiceB.methodB()      │   │
│      │ [新事务B，事务A被挂起]    │   │
│      └─────────────────────────┘   │
│                                     │
│   事务B独立于事务A                   │
│   事务B回滚不影响事务A               │
└─────────────────────────────────────┘

NESTED:
┌─────────────────────────────────────┐
│ ServiceA.methodA() [事务A]          │
│   │                                 │
│   │  ┌─────────────────────────┐   │
│   └─>│ ServiceB.methodB()      │   │
│      │ [嵌套事务，创建保存点]    │   │
│      └─────────────────────────┘   │
│                                     │
│   嵌套事务回滚到保存点              │
│   外层事务可以选择继续或回滚        │
└─────────────────────────────────────┘
```

## 三、事务失效场景

### 3.1 常见失效场景

```java
@Service
public class OrderService {
    
    /**
     * 失效场景1：非 public 方法
     * Spring AOP 无法代理非 public 方法
     */
    @Transactional
    private void privateMethod() {
        // 事务不生效！
    }
    
    /**
     * 失效场景2：同一类中方法调用
     * 通过 this 调用，不经过代理
     */
    public void methodA() {
        this.methodB(); // 事务不生效！
    }
    
    @Transactional
    public void methodB() {
        // 期望有事务，但实际没有
    }
    
    /**
     * 失效场景3：异常被捕获
     * Spring 默认只回滚 RuntimeException
     */
    @Transactional
    public void catchException() {
        try {
            // 业务逻辑
            throw new RuntimeException("error");
        } catch (Exception e) {
            // 异常被捕获，不会回滚！
            log.error("error", e);
        }
    }
    
    /**
     * 失效场景4：抛出检查异常
     * 默认只回滚 RuntimeException 和 Error
     */
    @Transactional
    public void checkedException() throws Exception {
        // 业务逻辑
        throw new Exception("checked exception");
        // 不会回滚！需要 rollbackFor = Exception.class
    }
    
    /**
     * 失效场景5：数据库不支持事务
     * 如 MyISAM 存储引擎
     */
    @Transactional
    public void unsupportedEngine() {
        // MyISAM 表不支持事务
    }
    
    /**
     * 失效场景6：Bean 未被 Spring 管理
     */
    // 没有 @Service 注解
    public class NotManagedService {
        @Transactional
        public void method() {
            // 事务不生效！
        }
    }
    
    /**
     * 失效场景7：多线程调用
     * 新线程不在同一个事务中
     */
    @Transactional
    public void multiThread() {
        new Thread(() -> {
            // 这里是新线程，不在事务中！
            orderRepository.save(new Order());
        }).start();
    }
}
```

### 3.2 解决方案

```java
@Service
public class OrderService {
    
    @Autowired
    private OrderService self; // 注入自己
    
    // 或者使用 AopContext
    // @EnableAspectJAutoProxy(exposeProxy = true)
    
    /**
     * 解决同类方法调用问题
     */
    public void methodA() {
        // 方式1：注入自己
        self.methodB();
        
        // 方式2：使用 AopContext
        ((OrderService) AopContext.currentProxy()).methodB();
    }
    
    @Transactional
    public void methodB() {
        // 现在有事务了
    }
    
    /**
     * 解决检查异常问题
     */
    @Transactional(rollbackFor = Exception.class)
    public void handleCheckedException() throws Exception {
        // 现在检查异常也会回滚
    }
    
    /**
     * 解决异常捕获问题
     */
    @Transactional
    public void handleCatchException() {
        try {
            // 业务逻辑
        } catch (Exception e) {
            log.error("error", e);
            // 手动设置回滚
            TransactionAspectSupport.currentTransactionStatus().setRollbackOnly();
            // 或者重新抛出异常
            throw new RuntimeException(e);
        }
    }
}
```

### 3.3 失效场景总结表

| 失效场景 | 原因 | 解决方案 |
|---------|------|---------|
| 非 public 方法 | AOP 无法代理 | 改为 public |
| 同类方法调用 | 不经过代理 | 注入自己或使用 AopContext |
| 异常被捕获 | Spring 感知不到异常 | 重新抛出或手动回滚 |
| 抛出检查异常 | 默认只回滚 RuntimeException | rollbackFor = Exception.class |
| Bean 未被管理 | 不是 Spring Bean | 添加 @Component 等注解 |
| 多线程 | 新线程不在事务中 | 使用编程式事务 |
| 数据库不支持 | 如 MyISAM | 使用 InnoDB |

## 四、事务隔离级别

### 4.1 四种隔离级别

| 隔离级别 | 脏读 | 不可重复读 | 幻读 | 说明 |
|---------|------|-----------|------|------|
| READ_UNCOMMITTED | ✓ | ✓ | ✓ | 读取未提交数据 |
| READ_COMMITTED | ✗ | ✓ | ✓ | 读取已提交数据（Oracle 默认） |
| REPEATABLE_READ | ✗ | ✗ | ✓ | 可重复读（MySQL 默认） |
| SERIALIZABLE | ✗ | ✗ | ✗ | 串行化，性能最差 |

### 4.2 使用示例

```java
@Service
public class OrderService {
    
    /**
     * 指定隔离级别
     */
    @Transactional(isolation = Isolation.READ_COMMITTED)
    public Order getOrder(Long id) {
        return orderRepository.findById(id);
    }
    
    /**
     * 使用默认隔离级别（数据库默认）
     */
    @Transactional(isolation = Isolation.DEFAULT)
    public void createOrder(Order order) {
        orderRepository.save(order);
    }
}
```

## 五、源码分析

### 5.1 @Transactional 处理流程

```java
/**
 * TransactionInterceptor 事务拦截器
 */
public class TransactionInterceptor extends TransactionAspectSupport {
    
    @Override
    public Object invoke(MethodInvocation invocation) throws Throwable {
        // 获取目标类
        Class<?> targetClass = (invocation.getThis() != null ? 
            AopUtils.getTargetClass(invocation.getThis()) : null);
        
        // 调用父类方法执行事务
        return invokeWithinTransaction(invocation.getMethod(), targetClass, 
            invocation::proceed);
    }
}

/**
 * TransactionAspectSupport 事务切面支持
 */
public abstract class TransactionAspectSupport {
    
    protected Object invokeWithinTransaction(Method method, Class<?> targetClass,
            InvocationCallback invocation) throws Throwable {
        
        // 1. 获取事务属性
        TransactionAttributeSource tas = getTransactionAttributeSource();
        TransactionAttribute txAttr = (tas != null ? 
            tas.getTransactionAttribute(method, targetClass) : null);
        
        // 2. 获取事务管理器
        TransactionManager tm = determineTransactionManager(txAttr);
        PlatformTransactionManager ptm = asPlatformTransactionManager(tm);
        
        // 3. 获取连接点标识
        String joinpointIdentification = methodIdentification(method, targetClass, txAttr);
        
        // 4. 创建事务（如果需要）
        TransactionInfo txInfo = createTransactionIfNecessary(ptm, txAttr, joinpointIdentification);
        
        Object retVal;
        try {
            // 5. 执行目标方法
            retVal = invocation.proceedWithInvocation();
        } catch (Throwable ex) {
            // 6. 异常处理（回滚或提交）
            completeTransactionAfterThrowing(txInfo, ex);
            throw ex;
        } finally {
            // 7. 清理事务信息
            cleanupTransactionInfo(txInfo);
        }
        
        // 8. 提交事务
        commitTransactionAfterReturning(txInfo);
        
        return retVal;
    }
}
```

### 5.2 事务创建流程

```java
/**
 * AbstractPlatformTransactionManager
 */
public abstract class AbstractPlatformTransactionManager {
    
    @Override
    public final TransactionStatus getTransaction(TransactionDefinition definition) {
        
        // 1. 获取当前事务对象
        Object transaction = doGetTransaction();
        
        // 2. 检查是否已存在事务
        if (isExistingTransaction(transaction)) {
            // 处理已存在事务的情况（根据传播行为）
            return handleExistingTransaction(definition, transaction, debugEnabled);
        }
        
        // 3. 没有现有事务，检查传播行为
        if (definition.getPropagationBehavior() == TransactionDefinition.PROPAGATION_MANDATORY) {
            throw new IllegalTransactionStateException("No existing transaction");
        }
        
        if (definition.getPropagationBehavior() == TransactionDefinition.PROPAGATION_REQUIRED ||
            definition.getPropagationBehavior() == TransactionDefinition.PROPAGATION_REQUIRES_NEW ||
            definition.getPropagationBehavior() == TransactionDefinition.PROPAGATION_NESTED) {
            
            // 4. 挂起当前事务（如果有）
            SuspendedResourcesHolder suspendedResources = suspend(null);
            
            try {
                // 5. 开始新事务
                return startTransaction(definition, transaction, debugEnabled, suspendedResources);
            } catch (RuntimeException | Error ex) {
                resume(null, suspendedResources);
                throw ex;
            }
        }
        
        // 其他情况：SUPPORTS、NOT_SUPPORTED、NEVER
        return prepareTransactionStatus(definition, null, true, 
            definition.isReadOnly(), debugEnabled, null);
    }
    
    /**
     * 处理已存在事务
     */
    private TransactionStatus handleExistingTransaction(
            TransactionDefinition definition, Object transaction, boolean debugEnabled) {
        
        // NEVER - 不允许有事务
        if (definition.getPropagationBehavior() == TransactionDefinition.PROPAGATION_NEVER) {
            throw new IllegalTransactionStateException("Existing transaction found");
        }
        
        // NOT_SUPPORTED - 挂起当前事务
        if (definition.getPropagationBehavior() == TransactionDefinition.PROPAGATION_NOT_SUPPORTED) {
            Object suspendedResources = suspend(transaction);
            return prepareTransactionStatus(definition, null, false, 
                definition.isReadOnly(), debugEnabled, suspendedResources);
        }
        
        // REQUIRES_NEW - 挂起当前事务，创建新事务
        if (definition.getPropagationBehavior() == TransactionDefinition.PROPAGATION_REQUIRES_NEW) {
            SuspendedResourcesHolder suspendedResources = suspend(transaction);
            return startTransaction(definition, transaction, debugEnabled, suspendedResources);
        }
        
        // NESTED - 创建保存点
        if (definition.getPropagationBehavior() == TransactionDefinition.PROPAGATION_NESTED) {
            if (useSavepointForNestedTransaction()) {
                DefaultTransactionStatus status = prepareTransactionStatus(
                    definition, transaction, false, false, debugEnabled, null);
                status.createAndHoldSavepoint();
                return status;
            }
        }
        
        // REQUIRED、SUPPORTS、MANDATORY - 加入当前事务
        return prepareTransactionStatus(definition, transaction, false, 
            definition.isReadOnly(), debugEnabled, null);
    }
}
```

### 5.3 事务回滚逻辑

```java
/**
 * 异常后处理
 */
protected void completeTransactionAfterThrowing(TransactionInfo txInfo, Throwable ex) {
    if (txInfo != null && txInfo.getTransactionStatus() != null) {
        
        // 判断是否需要回滚
        if (txInfo.transactionAttribute != null && 
            txInfo.transactionAttribute.rollbackOn(ex)) {
            
            try {
                // 回滚事务
                txInfo.getTransactionManager().rollback(txInfo.getTransactionStatus());
            } catch (TransactionSystemException ex2) {
                ex2.initApplicationException(ex);
                throw ex2;
            }
        } else {
            // 不需要回滚，提交事务
            try {
                txInfo.getTransactionManager().commit(txInfo.getTransactionStatus());
            } catch (TransactionSystemException ex2) {
                ex2.initApplicationException(ex);
                throw ex2;
            }
        }
    }
}

/**
 * 默认回滚规则
 */
public class DefaultTransactionAttribute {
    
    @Override
    public boolean rollbackOn(Throwable ex) {
        // 默认只回滚 RuntimeException 和 Error
        return (ex instanceof RuntimeException || ex instanceof Error);
    }
}
```

## 六、@Transactional 属性详解

```java
@Transactional(
    // 事务管理器
    transactionManager = "transactionManager",
    
    // 传播行为
    propagation = Propagation.REQUIRED,
    
    // 隔离级别
    isolation = Isolation.DEFAULT,
    
    // 超时时间（秒）
    timeout = 30,
    
    // 只读事务
    readOnly = false,
    
    // 回滚的异常类型
    rollbackFor = {RuntimeException.class, BusinessException.class},
    
    // 不回滚的异常类型
    noRollbackFor = {IgnoreException.class},
    
    // 回滚的异常类名
    rollbackForClassName = {"java.lang.RuntimeException"},
    
    // 不回滚的异常类名
    noRollbackForClassName = {"com.example.IgnoreException"}
)
public void transactionalMethod() {
    // 业务逻辑
}
```

## 七、常见面试问题

### Q1: Spring 事务的传播行为有哪些？
> 答：REQUIRED（默认，有则加入，无则创建）、SUPPORTS（有则加入，无则非事务）、MANDATORY（必须有事务）、REQUIRES_NEW（创建新事务）、NOT_SUPPORTED（非事务运行）、NEVER（不能有事务）、NESTED（嵌套事务）。

### Q2: 事务失效的常见场景？
> 答：1）非 public 方法；2）同类方法调用；3）异常被捕获；4）抛出检查异常；5）Bean 未被 Spring 管理；6）多线程调用；7）数据库不支持事务。

### Q3: REQUIRED 和 REQUIRES_NEW 的区别？
> 答：REQUIRED 是加入现有事务或创建新事务，共用同一个事务；REQUIRES_NEW 总是创建新事务，挂起当前事务，两个事务相互独立。

### Q4: 为什么同类方法调用事务不生效？
> 答：因为 Spring 事务是基于 AOP 代理实现的，同类方法调用是通过 this 调用，不经过代理对象，所以事务拦截器不会生效。

### Q5: 如何解决同类方法调用事务失效？
> 答：1）注入自己（@Autowired private OrderService self）；2）使用 AopContext.currentProxy()；3）拆分到不同的类中。
