# Spring Bean 生命周期

## 一、Spring Bean 生命周期概述

Spring Bean 的生命周期是指 Bean 从创建到销毁的整个过程。理解 Bean 生命周期对于正确使用 Spring、扩展 Spring 功能至关重要。

### 生命周期主要阶段
1. **实例化（Instantiation）**：创建 Bean 实例
2. **属性填充（Populate）**：注入依赖属性
3. **初始化（Initialization）**：执行初始化方法
4. **使用（In Use）**：Bean 可以被使用
5. **销毁（Destruction）**：执行销毁方法

## 二、Bean 生命周期完整流程图

```
┌────────────────────────────────────────────────────────────────┐
│                        Bean 生命周期                            │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. 实例化 Bean                                                 │
│     └─ 调用构造函数创建对象                                      │
│              │                                                  │
│              ▼                                                  │
│  2. 属性填充 (populateBean)                                     │
│     └─ @Autowired, @Value, setter 注入                         │
│              │                                                  │
│              ▼                                                  │
│  3. Aware 接口回调                                              │
│     ├─ BeanNameAware.setBeanName()                             │
│     ├─ BeanClassLoaderAware.setBeanClassLoader()               │
│     ├─ BeanFactoryAware.setBeanFactory()                       │
│     ├─ EnvironmentAware.setEnvironment()                       │
│     ├─ ApplicationContextAware.setApplicationContext()         │
│     └─ 其他 Aware 接口...                                       │
│              │                                                  │
│              ▼                                                  │
│  4. BeanPostProcessor.postProcessBeforeInitialization()        │
│     └─ @PostConstruct 在此执行                                  │
│              │                                                  │
│              ▼                                                  │
│  5. InitializingBean.afterPropertiesSet()                      │
│              │                                                  │
│              ▼                                                  │
│  6. 自定义 init-method                                          │
│              │                                                  │
│              ▼                                                  │
│  7. BeanPostProcessor.postProcessAfterInitialization()         │
│     └─ AOP 代理在此创建                                         │
│              │                                                  │
│              ▼                                                  │
│  8. Bean 就绪，可以使用                                          │
│              │                                                  │
│              ▼                                                  │
│  9. DisposableBean.destroy()                                   │
│     └─ @PreDestroy 在此执行                                     │
│              │                                                  │
│              ▼                                                  │
│  10. 自定义 destroy-method                                      │
│                                                                 │
└────────────────────────────────────────────────────────────────┘
```

## 三、生命周期各阶段详解

### 3.1 实例化阶段

```java
/**
 * 实例化阶段 - 调用构造函数
 */
@Component
public class UserService {
    
    public UserService() {
        System.out.println("1. 构造函数执行 - Bean 实例化");
    }
}
```

### 3.2 属性填充阶段

```java
@Component
public class UserService {
    
    @Autowired
    private UserRepository userRepository;
    
    @Value("${app.name}")
    private String appName;
    
    // setter 注入
    @Autowired
    public void setOrderService(OrderService orderService) {
        System.out.println("2. 属性填充 - setter 注入");
        this.orderService = orderService;
    }
}
```

### 3.3 Aware 接口回调

```java
/**
 * 实现多个 Aware 接口
 */
@Component
public class MyAwareBean implements BeanNameAware, BeanFactoryAware, 
        ApplicationContextAware, EnvironmentAware {
    
    private String beanName;
    private BeanFactory beanFactory;
    private ApplicationContext applicationContext;
    private Environment environment;
    
    @Override
    public void setBeanName(String name) {
        System.out.println("3.1 BeanNameAware.setBeanName: " + name);
        this.beanName = name;
    }
    
    @Override
    public void setBeanFactory(BeanFactory beanFactory) throws BeansException {
        System.out.println("3.2 BeanFactoryAware.setBeanFactory");
        this.beanFactory = beanFactory;
    }
    
    @Override
    public void setApplicationContext(ApplicationContext applicationContext) {
        System.out.println("3.3 ApplicationContextAware.setApplicationContext");
        this.applicationContext = applicationContext;
    }
    
    @Override
    public void setEnvironment(Environment environment) {
        System.out.println("3.4 EnvironmentAware.setEnvironment");
        this.environment = environment;
    }
}
```

### 3.4 BeanPostProcessor - 前置处理

```java
/**
 * BeanPostProcessor - 对所有 Bean 生效
 */
@Component
public class MyBeanPostProcessor implements BeanPostProcessor {
    
    @Override
    public Object postProcessBeforeInitialization(Object bean, String beanName) {
        System.out.println("4. BeanPostProcessor.postProcessBeforeInitialization: " + beanName);
        // 可以在这里修改 bean 或返回代理对象
        return bean;
    }
    
    @Override
    public Object postProcessAfterInitialization(Object bean, String beanName) {
        System.out.println("7. BeanPostProcessor.postProcessAfterInitialization: " + beanName);
        // AOP 代理在这里创建
        return bean;
    }
}
```

### 3.5 初始化阶段

```java
@Component
public class UserService implements InitializingBean, DisposableBean {
    
    // 1. @PostConstruct（由 CommonAnnotationBeanPostProcessor 处理）
    @PostConstruct
    public void postConstruct() {
        System.out.println("4.1 @PostConstruct 执行");
    }
    
    // 2. InitializingBean 接口
    @Override
    public void afterPropertiesSet() throws Exception {
        System.out.println("5. InitializingBean.afterPropertiesSet() 执行");
    }
    
    // 3. 自定义 init-method
    // @Bean(initMethod = "customInit")
    public void customInit() {
        System.out.println("6. 自定义 init-method 执行");
    }
    
    // 销毁阶段
    @PreDestroy
    public void preDestroy() {
        System.out.println("9.1 @PreDestroy 执行");
    }
    
    @Override
    public void destroy() throws Exception {
        System.out.println("9.2 DisposableBean.destroy() 执行");
    }
    
    public void customDestroy() {
        System.out.println("10. 自定义 destroy-method 执行");
    }
}
```

## 四、完整生命周期演示

```java
/**
 * 完整生命周期演示 Bean
 */
@Component
public class LifecycleBean implements BeanNameAware, BeanFactoryAware,
        ApplicationContextAware, InitializingBean, DisposableBean {
    
    private String beanName;
    
    // 1. 构造函数
    public LifecycleBean() {
        System.out.println("【1】构造函数执行");
    }
    
    // 2. 属性注入
    @Autowired
    public void setDependency(SomeDependency dependency) {
        System.out.println("【2】依赖注入");
    }
    
    // 3. BeanNameAware
    @Override
    public void setBeanName(String name) {
        System.out.println("【3】BeanNameAware.setBeanName: " + name);
        this.beanName = name;
    }
    
    // 4. BeanFactoryAware
    @Override
    public void setBeanFactory(BeanFactory beanFactory) {
        System.out.println("【4】BeanFactoryAware.setBeanFactory");
    }
    
    // 5. ApplicationContextAware
    @Override
    public void setApplicationContext(ApplicationContext ctx) {
        System.out.println("【5】ApplicationContextAware.setApplicationContext");
    }
    
    // 6. @PostConstruct
    @PostConstruct
    public void postConstruct() {
        System.out.println("【6】@PostConstruct");
    }
    
    // 7. InitializingBean
    @Override
    public void afterPropertiesSet() {
        System.out.println("【7】InitializingBean.afterPropertiesSet");
    }
    
    // 8. 自定义 init
    public void customInit() {
        System.out.println("【8】自定义 init-method");
    }
    
    // === Bean 使用中 ===
    
    // 9. @PreDestroy
    @PreDestroy
    public void preDestroy() {
        System.out.println("【9】@PreDestroy");
    }
    
    // 10. DisposableBean
    @Override
    public void destroy() {
        System.out.println("【10】DisposableBean.destroy");
    }
    
    // 11. 自定义 destroy
    public void customDestroy() {
        System.out.println("【11】自定义 destroy-method");
    }
}

/**
 * 配置类
 */
@Configuration
public class BeanConfig {
    
    @Bean(initMethod = "customInit", destroyMethod = "customDestroy")
    public LifecycleBean lifecycleBean() {
        return new LifecycleBean();
    }
}
```

## 五、核心扩展点

### 5.1 BeanPostProcessor

```java
/**
 * BeanPostProcessor - Bean 后置处理器
 * 对所有 Bean 生效，可用于：
 * 1. 修改 Bean 属性
 * 2. 创建代理对象（AOP）
 * 3. 验证 Bean 配置
 */
@Component
public class CustomBeanPostProcessor implements BeanPostProcessor, Ordered {
    
    @Override
    public Object postProcessBeforeInitialization(Object bean, String beanName) {
        if (bean instanceof UserService) {
            System.out.println("处理 UserService 初始化前");
            // 可以修改 bean 的属性
        }
        return bean;
    }
    
    @Override
    public Object postProcessAfterInitialization(Object bean, String beanName) {
        if (bean instanceof UserService) {
            // 创建代理
            return Proxy.newProxyInstance(
                bean.getClass().getClassLoader(),
                bean.getClass().getInterfaces(),
                (proxy, method, args) -> {
                    System.out.println("代理执行前");
                    Object result = method.invoke(bean, args);
                    System.out.println("代理执行后");
                    return result;
                }
            );
        }
        return bean;
    }
    
    @Override
    public int getOrder() {
        return 0; // 执行顺序，数字越小越先执行
    }
}
```

### 5.2 BeanFactoryPostProcessor

```java
/**
 * BeanFactoryPostProcessor - BeanFactory 后置处理器
 * 在 Bean 实例化之前执行，可以修改 BeanDefinition
 */
@Component
public class CustomBeanFactoryPostProcessor implements BeanFactoryPostProcessor {
    
    @Override
    public void postProcessBeanFactory(ConfigurableListableBeanFactory beanFactory) {
        System.out.println("BeanFactoryPostProcessor 执行");
        
        // 获取 BeanDefinition
        BeanDefinition bd = beanFactory.getBeanDefinition("userService");
        
        // 修改 Bean 的作用域
        bd.setScope("prototype");
        
        // 修改初始化方法
        bd.setInitMethodName("customInit");
        
        // 添加属性值
        bd.getPropertyValues().add("name", "modified");
    }
}
```

### 5.3 BeanDefinitionRegistryPostProcessor

```java
/**
 * BeanDefinitionRegistryPostProcessor
 * 可以动态注册新的 BeanDefinition
 */
@Component
public class CustomBeanDefinitionRegistrar implements BeanDefinitionRegistryPostProcessor {
    
    @Override
    public void postProcessBeanDefinitionRegistry(BeanDefinitionRegistry registry) {
        System.out.println("动态注册 Bean");
        
        // 创建 BeanDefinition
        GenericBeanDefinition bd = new GenericBeanDefinition();
        bd.setBeanClass(DynamicBean.class);
        bd.setScope("singleton");
        bd.setLazyInit(false);
        
        // 注册到容器
        registry.registerBeanDefinition("dynamicBean", bd);
    }
    
    @Override
    public void postProcessBeanFactory(ConfigurableListableBeanFactory beanFactory) {
        // 可以在这里修改已注册的 BeanDefinition
    }
}
```

### 5.4 InstantiationAwareBeanPostProcessor

```java
/**
 * InstantiationAwareBeanPostProcessor
 * 更细粒度的控制，可以介入实例化过程
 */
@Component
public class CustomInstantiationAwareBeanPostProcessor 
        implements InstantiationAwareBeanPostProcessor {
    
    /**
     * 实例化前调用
     * 返回非 null 则跳过默认实例化
     */
    @Override
    public Object postProcessBeforeInstantiation(Class<?> beanClass, String beanName) {
        if ("userService".equals(beanName)) {
            System.out.println("实例化前处理: " + beanName);
            // 返回自定义实例，跳过默认实例化
            // return new UserService();
        }
        return null;
    }
    
    /**
     * 实例化后调用
     * 返回 false 则跳过属性填充
     */
    @Override
    public boolean postProcessAfterInstantiation(Object bean, String beanName) {
        System.out.println("实例化后处理: " + beanName);
        return true; // 返回 true 继续属性填充
    }
    
    /**
     * 属性填充时调用
     */
    @Override
    public PropertyValues postProcessProperties(PropertyValues pvs, 
            Object bean, String beanName) {
        System.out.println("属性处理: " + beanName);
        return pvs;
    }
}
```

## 六、源码分析

### 6.1 AbstractAutowireCapableBeanFactory.doCreateBean

```java
// 核心创建 Bean 的方法
protected Object doCreateBean(String beanName, RootBeanDefinition mbd, Object[] args) {
    
    // 1. 实例化 Bean
    BeanWrapper instanceWrapper = createBeanInstance(beanName, mbd, args);
    Object bean = instanceWrapper.getWrappedInstance();
    
    // 2. 提前暴露（解决循环依赖）
    boolean earlySingletonExposure = (mbd.isSingleton() && 
        this.allowCircularReferences && isSingletonCurrentlyInCreation(beanName));
    if (earlySingletonExposure) {
        addSingletonFactory(beanName, () -> getEarlyBeanReference(beanName, mbd, bean));
    }
    
    Object exposedObject = bean;
    try {
        // 3. 属性填充
        populateBean(beanName, mbd, instanceWrapper);
        
        // 4. 初始化 Bean
        exposedObject = initializeBean(beanName, exposedObject, mbd);
    } catch (Throwable ex) {
        // 处理异常
    }
    
    // 5. 注册销毁方法
    registerDisposableBeanIfNecessary(beanName, bean, mbd);
    
    return exposedObject;
}
```

### 6.2 initializeBean 源码

```java
protected Object initializeBean(String beanName, Object bean, RootBeanDefinition mbd) {
    
    // 1. Aware 接口回调
    invokeAwareMethods(beanName, bean);
    
    Object wrappedBean = bean;
    
    // 2. BeanPostProcessor 前置处理
    if (mbd == null || !mbd.isSynthetic()) {
        wrappedBean = applyBeanPostProcessorsBeforeInitialization(wrappedBean, beanName);
    }
    
    // 3. 执行初始化方法
    try {
        invokeInitMethods(beanName, wrappedBean, mbd);
    } catch (Throwable ex) {
        throw new BeanCreationException(...);
    }
    
    // 4. BeanPostProcessor 后置处理
    if (mbd == null || !mbd.isSynthetic()) {
        wrappedBean = applyBeanPostProcessorsAfterInitialization(wrappedBean, beanName);
    }
    
    return wrappedBean;
}

private void invokeAwareMethods(String beanName, Object bean) {
    if (bean instanceof Aware) {
        if (bean instanceof BeanNameAware) {
            ((BeanNameAware) bean).setBeanName(beanName);
        }
        if (bean instanceof BeanClassLoaderAware) {
            ((BeanClassLoaderAware) bean).setBeanClassLoader(getBeanClassLoader());
        }
        if (bean instanceof BeanFactoryAware) {
            ((BeanFactoryAware) bean).setBeanFactory(this);
        }
    }
}

protected void invokeInitMethods(String beanName, Object bean, RootBeanDefinition mbd) {
    
    // 1. InitializingBean.afterPropertiesSet()
    if (bean instanceof InitializingBean) {
        ((InitializingBean) bean).afterPropertiesSet();
    }
    
    // 2. 自定义 init-method
    if (mbd != null && bean.getClass() != NullBean.class) {
        String initMethodName = mbd.getInitMethodName();
        if (StringUtils.hasLength(initMethodName)) {
            invokeCustomInitMethod(beanName, bean, mbd);
        }
    }
}
```

## 七、常见面试问题

### Q1: Spring Bean 的生命周期有哪些阶段？
> 答：主要包括实例化、属性填充、Aware 接口回调、BeanPostProcessor 前置处理、初始化方法调用、BeanPostProcessor 后置处理、使用、销毁等阶段。

### Q2: @PostConstruct 和 InitializingBean 的执行顺序？
> 答：@PostConstruct 先执行，InitializingBean.afterPropertiesSet() 后执行，最后是自定义 init-method。

### Q3: BeanPostProcessor 和 BeanFactoryPostProcessor 的区别？
> 答：BeanFactoryPostProcessor 在 Bean 实例化之前执行，可以修改 BeanDefinition；BeanPostProcessor 在 Bean 实例化之后执行，可以修改 Bean 实例或创建代理。

### Q4: 如何在 Bean 初始化时获取 ApplicationContext？
> 答：实现 ApplicationContextAware 接口，Spring 会自动注入 ApplicationContext。

### Q5: Spring AOP 代理是在什么阶段创建的？
> 答：在 BeanPostProcessor.postProcessAfterInitialization() 阶段，由 AbstractAutoProxyCreator 创建代理对象。
