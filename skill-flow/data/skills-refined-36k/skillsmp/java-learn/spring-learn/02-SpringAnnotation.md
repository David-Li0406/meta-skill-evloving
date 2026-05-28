# Spring 注解详解

## 一、Spring 核心注解

### 1.1 组件注册注解

```java
/**
 * @Component - 通用组件注解
 */
@Component
public class CommonComponent {
}

/**
 * @Service - 业务层注解
 */
@Service
public class UserService {
}

/**
 * @Repository - 数据访问层注解
 * 会自动转换数据库异常为 Spring 的 DataAccessException
 */
@Repository
public class UserRepository {
}

/**
 * @Controller - 控制层注解
 */
@Controller
public class UserController {
}

/**
 * @RestController = @Controller + @ResponseBody
 */
@RestController
public class UserApiController {
}
```

### 1.2 依赖注入注解

```java
@Service
public class UserService {
    
    /**
     * @Autowired - 按类型自动注入
     * 可用于构造器、setter、字段
     */
    @Autowired
    private UserRepository userRepository;
    
    /**
     * @Qualifier - 指定注入的 Bean 名称
     * 当有多个同类型 Bean 时使用
     */
    @Autowired
    @Qualifier("mysqlUserRepository")
    private UserRepository specificRepository;
    
    /**
     * @Resource - JSR-250 注解，按名称注入
     */
    @Resource(name = "orderService")
    private OrderService orderService;
    
    /**
     * @Value - 注入配置值
     */
    @Value("${app.name}")
    private String appName;
    
    @Value("${app.timeout:5000}") // 带默认值
    private int timeout;
    
    @Value("#{systemProperties['user.name']}") // SpEL 表达式
    private String systemUser;
    
    /**
     * @Autowired(required = false) - 非必须注入
     */
    @Autowired(required = false)
    private Optional<CacheService> cacheService;
    
    /**
     * 构造器注入 - 推荐方式
     */
    @Autowired
    public UserService(UserRepository userRepository) {
        this.userRepository = userRepository;
    }
}
```

### 1.3 配置类注解

```java
/**
 * @Configuration - 配置类
 * 相当于 XML 配置文件
 */
@Configuration
@ComponentScan("com.example")
@PropertySource("classpath:application.properties")
@Import({DataSourceConfig.class, CacheConfig.class})
public class AppConfig {
    
    /**
     * @Bean - 定义 Bean
     */
    @Bean
    public DataSource dataSource() {
        return new HikariDataSource();
    }
    
    /**
     * @Bean 带参数 - Spring 自动注入依赖
     */
    @Bean
    public JdbcTemplate jdbcTemplate(DataSource dataSource) {
        return new JdbcTemplate(dataSource);
    }
    
    /**
     * @Bean 指定初始化和销毁方法
     */
    @Bean(initMethod = "init", destroyMethod = "cleanup")
    public ConnectionPool connectionPool() {
        return new ConnectionPool();
    }
}
```

### 1.4 作用域注解

```java
/**
 * @Scope - 定义 Bean 作用域
 */
@Component
@Scope("singleton") // 默认，单例
public class SingletonBean {}

@Component
@Scope("prototype") // 每次获取新实例
public class PrototypeBean {}

@Component
@Scope(value = "request", proxyMode = ScopedProxyMode.TARGET_CLASS)
public class RequestBean {} // Web 请求作用域

@Component
@Scope(value = "session", proxyMode = ScopedProxyMode.TARGET_CLASS)
public class SessionBean {} // Web Session 作用域

/**
 * @Lazy - 延迟加载
 */
@Component
@Lazy
public class LazyBean {
    public LazyBean() {
        System.out.println("延迟加载的 Bean 被创建");
    }
}
```

## 二、架构师常用注解

### 2.1 条件注解

```java
/**
 * @Conditional - 条件化 Bean 注册
 */
@Configuration
public class ConditionalConfig {
    
    /**
     * @ConditionalOnProperty - 根据配置属性
     */
    @Bean
    @ConditionalOnProperty(name = "cache.enabled", havingValue = "true")
    public CacheManager cacheManager() {
        return new RedisCacheManager();
    }
    
    /**
     * @ConditionalOnClass - 类路径存在某个类
     */
    @Bean
    @ConditionalOnClass(name = "redis.clients.jedis.Jedis")
    public RedisTemplate redisTemplate() {
        return new RedisTemplate();
    }
    
    /**
     * @ConditionalOnMissingBean - 容器中不存在某个 Bean
     */
    @Bean
    @ConditionalOnMissingBean(CacheManager.class)
    public CacheManager defaultCacheManager() {
        return new SimpleCacheManager();
    }
    
    /**
     * @ConditionalOnBean - 容器中存在某个 Bean
     */
    @Bean
    @ConditionalOnBean(DataSource.class)
    public JdbcTemplate jdbcTemplate(DataSource dataSource) {
        return new JdbcTemplate(dataSource);
    }
    
    /**
     * @Profile - 根据环境激活
     */
    @Bean
    @Profile("dev")
    public DataSource devDataSource() {
        return new EmbeddedDatabaseBuilder().build();
    }
    
    @Bean
    @Profile("prod")
    public DataSource prodDataSource() {
        return new HikariDataSource();
    }
}

/**
 * 自定义条件
 */
public class OnLinuxCondition implements Condition {
    @Override
    public boolean matches(ConditionContext context, AnnotatedTypeMetadata metadata) {
        return context.getEnvironment().getProperty("os.name").contains("Linux");
    }
}

@Bean
@Conditional(OnLinuxCondition.class)
public LinuxService linuxService() {
    return new LinuxService();
}
```

### 2.2 @Import 高级用法

```java
/**
 * @Import - 导入配置类或 Bean
 */
@Configuration
@Import({
    DataSourceConfig.class,        // 导入配置类
    MyImportSelector.class,        // 导入选择器
    MyImportBeanDefinitionRegistrar.class  // 导入注册器
})
public class MainConfig {
}

/**
 * ImportSelector - 动态选择导入的配置类
 */
public class MyImportSelector implements ImportSelector {
    @Override
    public String[] selectImports(AnnotationMetadata metadata) {
        // 可以根据条件返回不同的配置类
        if (checkCondition()) {
            return new String[]{CacheConfig.class.getName()};
        }
        return new String[]{DefaultConfig.class.getName()};
    }
}

/**
 * ImportBeanDefinitionRegistrar - 动态注册 Bean
 */
public class MyImportBeanDefinitionRegistrar implements ImportBeanDefinitionRegistrar {
    @Override
    public void registerBeanDefinitions(AnnotationMetadata metadata, 
            BeanDefinitionRegistry registry) {
        // 扫描并注册 Mapper 接口（类似 MyBatis）
        GenericBeanDefinition bd = new GenericBeanDefinition();
        bd.setBeanClass(UserMapper.class);
        registry.registerBeanDefinition("userMapper", bd);
    }
}
```

### 2.3 自定义启动注解

```java
/**
 * 自定义启用注解（类似 @EnableXxx）
 */
@Target(ElementType.TYPE)
@Retention(RetentionPolicy.RUNTIME)
@Documented
@Import(MyFeatureConfiguration.class)
public @interface EnableMyFeature {
    boolean enableCache() default true;
    String[] scanPackages() default {};
}

/**
 * 配合 ImportSelector 使用
 */
@Target(ElementType.TYPE)
@Retention(RetentionPolicy.RUNTIME)
@Import(MyFeatureImportSelector.class)
public @interface EnableMyFeature {
    String mode() default "simple";
}

public class MyFeatureImportSelector implements ImportSelector {
    @Override
    public String[] selectImports(AnnotationMetadata metadata) {
        Map<String, Object> attrs = metadata.getAnnotationAttributes(
            EnableMyFeature.class.getName());
        String mode = (String) attrs.get("mode");
        
        if ("advanced".equals(mode)) {
            return new String[]{AdvancedFeatureConfig.class.getName()};
        }
        return new String[]{SimpleFeatureConfig.class.getName()};
    }
}
```

### 2.4 事件相关注解

```java
/**
 * @EventListener - 事件监听
 */
@Component
public class OrderEventListener {
    
    @EventListener
    public void handleOrderCreated(OrderCreatedEvent event) {
        System.out.println("订单创建: " + event.getOrderId());
    }
    
    /**
     * 条件事件监听
     */
    @EventListener(condition = "#event.amount > 1000")
    public void handleLargeOrder(OrderCreatedEvent event) {
        System.out.println("大额订单: " + event.getOrderId());
    }
    
    /**
     * 异步事件监听
     */
    @Async
    @EventListener
    public void handleOrderCreatedAsync(OrderCreatedEvent event) {
        // 异步处理
    }
    
    /**
     * 事务提交后执行
     */
    @TransactionalEventListener(phase = TransactionPhase.AFTER_COMMIT)
    public void handleAfterCommit(OrderCreatedEvent event) {
        // 事务提交后执行
    }
}

/**
 * 发布事件
 */
@Service
public class OrderService {
    
    @Autowired
    private ApplicationEventPublisher eventPublisher;
    
    public void createOrder(Order order) {
        // 业务逻辑...
        eventPublisher.publishEvent(new OrderCreatedEvent(order));
    }
}
```

## 三、AOP 相关注解

```java
/**
 * @Aspect - 切面类
 */
@Aspect
@Component
public class LogAspect {
    
    /**
     * @Pointcut - 定义切入点
     */
    @Pointcut("execution(* com.example.service.*.*(..))")
    public void serviceLayer() {}
    
    @Pointcut("@annotation(com.example.annotation.Log)")
    public void logAnnotation() {}
    
    /**
     * @Before - 前置通知
     */
    @Before("serviceLayer()")
    public void before(JoinPoint joinPoint) {
        System.out.println("方法执行前: " + joinPoint.getSignature().getName());
    }
    
    /**
     * @After - 后置通知（无论是否异常都执行）
     */
    @After("serviceLayer()")
    public void after(JoinPoint joinPoint) {
        System.out.println("方法执行后");
    }
    
    /**
     * @AfterReturning - 返回通知
     */
    @AfterReturning(pointcut = "serviceLayer()", returning = "result")
    public void afterReturning(JoinPoint joinPoint, Object result) {
        System.out.println("方法返回: " + result);
    }
    
    /**
     * @AfterThrowing - 异常通知
     */
    @AfterThrowing(pointcut = "serviceLayer()", throwing = "ex")
    public void afterThrowing(JoinPoint joinPoint, Exception ex) {
        System.out.println("方法异常: " + ex.getMessage());
    }
    
    /**
     * @Around - 环绕通知
     */
    @Around("logAnnotation()")
    public Object around(ProceedingJoinPoint pjp) throws Throwable {
        long start = System.currentTimeMillis();
        try {
            Object result = pjp.proceed();
            return result;
        } finally {
            long cost = System.currentTimeMillis() - start;
            System.out.println("方法耗时: " + cost + "ms");
        }
    }
}
```

## 四、事务相关注解

```java
/**
 * @Transactional - 事务管理
 */
@Service
public class OrderService {
    
    /**
     * 默认事务
     */
    @Transactional
    public void createOrder(Order order) {
        // 业务逻辑
    }
    
    /**
     * 只读事务
     */
    @Transactional(readOnly = true)
    public Order getOrder(Long id) {
        return orderRepository.findById(id);
    }
    
    /**
     * 指定隔离级别和传播行为
     */
    @Transactional(
        isolation = Isolation.READ_COMMITTED,
        propagation = Propagation.REQUIRED,
        timeout = 30,
        rollbackFor = Exception.class,
        noRollbackFor = BusinessException.class
    )
    public void processOrder(Order order) {
        // 业务逻辑
    }
    
    /**
     * 新开事务
     */
    @Transactional(propagation = Propagation.REQUIRES_NEW)
    public void logOperation(String message) {
        // 独立事务，不受外层事务影响
    }
}
```

## 五、缓存相关注解

```java
@Service
public class UserService {
    
    /**
     * @Cacheable - 缓存结果
     */
    @Cacheable(value = "users", key = "#id")
    public User getUser(Long id) {
        return userRepository.findById(id);
    }
    
    /**
     * @Cacheable 复杂 key
     */
    @Cacheable(value = "users", key = "#p0 + '_' + #p1")
    public User getUser(Long id, String type) {
        return userRepository.findByIdAndType(id, type);
    }
    
    /**
     * @Cacheable 条件缓存
     */
    @Cacheable(value = "users", key = "#id", condition = "#id > 0", unless = "#result == null")
    public User getUserWithCondition(Long id) {
        return userRepository.findById(id);
    }
    
    /**
     * @CachePut - 更新缓存
     */
    @CachePut(value = "users", key = "#user.id")
    public User updateUser(User user) {
        return userRepository.save(user);
    }
    
    /**
     * @CacheEvict - 删除缓存
     */
    @CacheEvict(value = "users", key = "#id")
    public void deleteUser(Long id) {
        userRepository.deleteById(id);
    }
    
    /**
     * @CacheEvict 清空所有
     */
    @CacheEvict(value = "users", allEntries = true)
    public void clearAllUsers() {
    }
    
    /**
     * @Caching - 组合多个缓存操作
     */
    @Caching(
        put = @CachePut(value = "users", key = "#user.id"),
        evict = @CacheEvict(value = "userList", allEntries = true)
    )
    public User saveUser(User user) {
        return userRepository.save(user);
    }
}
```

## 六、异步相关注解

```java
/**
 * @EnableAsync - 启用异步
 */
@Configuration
@EnableAsync
public class AsyncConfig implements AsyncConfigurer {
    
    @Override
    public Executor getAsyncExecutor() {
        ThreadPoolTaskExecutor executor = new ThreadPoolTaskExecutor();
        executor.setCorePoolSize(10);
        executor.setMaxPoolSize(20);
        executor.setQueueCapacity(500);
        executor.setThreadNamePrefix("Async-");
        executor.initialize();
        return executor;
    }
    
    @Override
    public AsyncUncaughtExceptionHandler getAsyncUncaughtExceptionHandler() {
        return (ex, method, params) -> {
            System.err.println("异步方法异常: " + method.getName());
            ex.printStackTrace();
        };
    }
}

@Service
public class NotificationService {
    
    /**
     * @Async - 异步执行
     */
    @Async
    public void sendEmail(String to, String content) {
        // 异步发送邮件
    }
    
    /**
     * @Async 带返回值
     */
    @Async
    public CompletableFuture<String> sendEmailAsync(String to, String content) {
        // 发送邮件逻辑
        return CompletableFuture.completedFuture("success");
    }
    
    /**
     * @Async 指定线程池
     */
    @Async("emailExecutor")
    public void sendEmailWithExecutor(String to) {
        // 使用指定的线程池
    }
}
```

## 七、调度相关注解

```java
/**
 * @EnableScheduling - 启用调度
 */
@Configuration
@EnableScheduling
public class ScheduleConfig {
}

@Component
public class ScheduledTasks {
    
    /**
     * @Scheduled - 定时任务
     */
    @Scheduled(fixedRate = 5000) // 每 5 秒执行
    public void reportCurrentTime() {
        System.out.println("当前时间: " + new Date());
    }
    
    @Scheduled(fixedDelay = 5000) // 上次执行完后 5 秒执行
    public void taskWithDelay() {
    }
    
    @Scheduled(cron = "0 0 8 * * ?") // 每天 8 点执行
    public void dailyTask() {
    }
    
    @Scheduled(cron = "${task.cron}") // 从配置读取
    public void configuredTask() {
    }
    
    @Scheduled(initialDelay = 10000, fixedRate = 5000) // 延迟 10 秒后开始
    public void taskWithInitialDelay() {
    }
}
```

## 八、验证相关注解

```java
public class UserDTO {
    
    @NotNull(message = "ID 不能为空")
    private Long id;
    
    @NotBlank(message = "用户名不能为空")
    @Size(min = 2, max = 20, message = "用户名长度 2-20")
    private String username;
    
    @Email(message = "邮箱格式不正确")
    private String email;
    
    @Pattern(regexp = "^1[3-9]\\d{9}$", message = "手机号格式不正确")
    private String phone;
    
    @Min(value = 0, message = "年龄不能为负")
    @Max(value = 150, message = "年龄不能超过 150")
    private Integer age;
    
    @Past(message = "生日必须是过去的日期")
    private Date birthday;
    
    @Valid // 嵌套验证
    private AddressDTO address;
}

@RestController
public class UserController {
    
    @PostMapping("/users")
    public Result createUser(@Valid @RequestBody UserDTO user) {
        // 自动验证
        return Result.success();
    }
}
```

## 九、面试常见问题

### Q1: @Autowired 和 @Resource 的区别？
> 答：@Autowired 是 Spring 注解，默认按类型注入；@Resource 是 JSR-250 注解，默认按名称注入。

### Q2: @Component 和 @Bean 的区别？
> 答：@Component 用于类，通过组件扫描发现；@Bean 用于方法，在 @Configuration 类中使用，适合创建第三方类的实例。

### Q3: @Configuration 和 @Component 的区别？
> 答：@Configuration 类中的 @Bean 方法是 Full 模式，会被 CGLIB 代理，多次调用返回同一实例；@Component 类是 Lite 模式，每次调用都会创建新实例。

### Q4: 如何自定义条件注解？
> 答：实现 Condition 接口，重写 matches 方法，然后用 @Conditional 注解引用。
