# Spring IOC 容器源码深度剖析

## 一、IOC 容器启动核心：refresh()

`AbstractApplicationContext.refresh()` 是 Spring 容器启动的核心，包含 12 个关键步骤。

### 1.1 核心流程源码解析
```java
@Override
public void refresh() throws BeansException, IllegalStateException {
    synchronized (this.startupShutdownMonitor) {
        // 1. 准备环境 (属性验证、监听器重置)
        prepareRefresh();

        // 2. 获取 BeanFactory (加载 BeanDefinition)
        // 核心：XML 解析或 @ComponentScan 扫描都在这里完成
        ConfigurableListableBeanFactory beanFactory = obtainFreshBeanFactory();

        // 3. 准备 BeanFactory (设置 ClassLoader、SpEL 表达式解析器、注册特定 Bean)
        prepareBeanFactory(beanFactory);

        try {
            // 4. 子类后置处理 (模板方法，如 Web 容器注册 ServletContext)
            postProcessBeanFactory(beanFactory);

            // 5. 调用 BeanFactoryPostProcessor (BFPP)
            // 核心：处理 @Configuration、@ComponentScan、@PropertySource
            invokeBeanFactoryPostProcessors(beanFactory);

            // 6. 注册 BeanPostProcessor (BPP)
            // 只是注册，不执行。BPP 会在 Bean 初始化前后执行
            registerBeanPostProcessors(beanFactory);

            // 7. 初始化消息源 (国际化 i18n)
            initMessageSource();

            // 8. 初始化事件广播器 (ApplicationEventMulticaster)
            initApplicationEventMulticaster();

            // 9. 子类刷新 (模板方法，SpringBoot 在这里启动 Tomcat)
            onRefresh();

            // 10. 注册监听器 (ApplicationListener)
            registerListeners();

            // 11. 实例化所有非懒加载单例 Bean (核心中的核心)
            finishBeanFactoryInitialization(beanFactory);

            // 12. 完成刷新 (发布 ContextRefreshedEvent)
            finishRefresh();
        }
        catch (BeansException ex) {
            destroyBeans();
            cancelRefresh(ex);
            throw ex;
        }
    }
}
```

## 二、Bean 的生命周期与扩展点

Spring Bean 的生命周期远不止 `new` 出来这么简单。

### 2.1 完整生命周期图
```
1. 实例化 (Instantiation)
   └─ Constructor / FactoryMethod
        │
2. 属性填充 (Populate)
   └─ @Autowired, @Value, Setter
        │
3. Aware 接口回调
   ├─ BeanNameAware
   ├─ BeanFactoryAware
   └─ ApplicationContextAware
        │
4. BeanPostProcessor.before (前置处理)
   ├─ @PostConstruct (CommonAnnotationBeanPostProcessor)
   └─ ApplicationContextAwareProcessor
        │
5. 初始化 (Initialization)
   ├─ InitializingBean.afterPropertiesSet()
   └─ init-method (XML/@Bean)
        │
6. BeanPostProcessor.after (后置处理)
   └─ AOP 代理创建 (AbstractAutoProxyCreator)
        │
7. 使用中 (In Use)
        │
8. 销毁 (Destruction)
   ├─ @PreDestroy
   ├─ DisposableBean.destroy()
   └─ destroy-method
```

### 2.2 核心扩展点实战

#### 2.2.1 BeanPostProcessor (BPP)
干涉 **Bean 初始化** 前后的逻辑。AOP 就是在这里实现的。

```java
@Component
public class MyBeanPostProcessor implements BeanPostProcessor {
    @Override
    public Object postProcessAfterInitialization(Object bean, String beanName) {
        if (bean instanceof MyService) {
            System.out.println("MyService 初始化完成，可以进行代理或修改");
            // return Proxy.newProxyInstance(...)
        }
        return bean;
    }
}
```

#### 2.2.2 BeanFactoryPostProcessor (BFPP)
干涉 **BeanDefinition 加载** 后的逻辑。此时 Bean 还没实例化。

```java
@Component
public class MyBFPP implements BeanFactoryPostProcessor {
    @Override
    public void postProcessBeanFactory(ConfigurableListableBeanFactory beanFactory) {
        // 可以修改 Bean 的定义，例如把某个 Singleton 改成 Prototype
        BeanDefinition bd = beanFactory.getBeanDefinition("myService");
        bd.setScope("prototype");
    }
}
```

#### 2.2.3 FactoryBean (工厂 Bean)
**注意区分 BeanFactory**。
*   `BeanFactory`: 容器本身。
*   `FactoryBean`: 一个特殊的 Bean，用于创建复杂的对象 (如 MyBatis 的 `SqlSessionFactoryBean`)。

```java
@Component
public class MyComplexObjectFactoryBean implements FactoryBean<ComplexObject> {
    @Override
    public ComplexObject getObject() {
        // 复杂的创建逻辑
        return new ComplexObjectBuilder().build();
    }

    @Override
    public Class<?> getObjectType() {
        return ComplexObject.class;
    }
}

// 获取 ComplexObject
context.getBean("myComplexObjectFactoryBean"); 
// 获取 FactoryBean 本身
context.getBean("&myComplexObjectFactoryBean");
```

## 三、Spring 是如何解决循环依赖的？

### 3.1 三级缓存机制
Spring 只能解决 **单例 (Singleton)** 且 **非构造器注入** 的循环依赖。

*   **一级缓存 (`singletonObjects`)**: 存放完全初始化好的成品 Bean。
*   **二级缓存 (`earlySingletonObjects`)**: 存放原始的 Bean 对象 (尚未填充属性)，或者早期的代理对象。
*   **三级缓存 (`singletonFactories`)**: 存放 `ObjectFactory` Lambda 表达式。

### 3.2 为什么需要三级缓存？
主要是为了 **AOP**。
如果 A 依赖 B，B 依赖 A。
1.  A 实例化，放入三级缓存 (Lambda: `() -> getEarlyBeanReference(A)` )。
2.  A 注入 B，触发 B 实例化。
3.  B 注入 A，从三级缓存获取 A。
    *   此时调用 `getEarlyBeanReference`。
    *   如果 A 需要被 AOP 代理，这里会**提前创建代理对象**并返回。
    *   将代理对象放入二级缓存。
4.  B 初始化完成。
5.  A 继续初始化，注入 B。
6.  A 初始化完成，从二级缓存取出（可能是代理对象），放入一级缓存。

**结论**: 如果没有 AOP，二级缓存就够了。三级缓存是为了在“需要时”才创建代理，避免所有 Bean 都提前创建代理。
