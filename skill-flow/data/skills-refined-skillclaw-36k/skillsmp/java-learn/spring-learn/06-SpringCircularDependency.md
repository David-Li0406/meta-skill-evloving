# Spring 三级缓存与循环依赖

## 一、什么是循环依赖

循环依赖是指两个或多个 Bean 相互依赖，形成一个闭环。

### 1.1 循环依赖示例

```java
@Service
public class ServiceA {
    @Autowired
    private ServiceB serviceB;
}

@Service
public class ServiceB {
    @Autowired
    private ServiceA serviceA;
}
```

### 1.2 循环依赖类型

| 类型 | 说明 | Spring 能否解决 |
|------|------|----------------|
| 构造器注入 | 构造函数互相依赖 | ❌ 不能 |
| Setter/字段注入（单例） | 属性互相依赖 | ✅ 能 |
| Setter/字段注入（原型） | prototype 作用域 | ❌ 不能 |

## 二、三级缓存结构

### 2.1 三级缓存定义

```java
public class DefaultSingletonBeanRegistry {
    
    /**
     * 一级缓存：成品 Bean
     * 存放完全初始化好的单例 Bean
     */
    private final Map<String, Object> singletonObjects = new ConcurrentHashMap<>(256);
    
    /**
     * 二级缓存：半成品 Bean
     * 存放提前暴露的 Bean（已实例化，未初始化）
     */
    private final Map<String, Object> earlySingletonObjects = new ConcurrentHashMap<>(16);
    
    /**
     * 三级缓存：Bean 工厂
     * 存放 Bean 的 ObjectFactory，用于创建早期引用
     */
    private final Map<String, ObjectFactory<?>> singletonFactories = new HashMap<>(16);
    
    /**
     * 正在创建的单例 Bean 名称集合
     */
    private final Set<String> singletonsCurrentlyInCreation = 
        Collections.newSetFromMap(new ConcurrentHashMap<>(16));
}
```

### 2.2 缓存关系图

```
┌────────────────────────────────────────────────────────────────────┐
│                         三级缓存结构                                │
├────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐  │
│  │  一级缓存 (singletonObjects)                                 │  │
│  │  ┌───────────────────────────────────────────────────────┐  │  │
│  │  │  Bean Name  →  完全初始化的 Bean 实例                   │  │  │
│  │  └───────────────────────────────────────────────────────┘  │  │
│  │  状态：已实例化 ✓  已填充属性 ✓  已初始化 ✓                  │  │
│  └─────────────────────────────────────────────────────────────┘  │
│                              ↑                                      │
│                              │ 初始化完成后移入                      │
│                              │                                      │
│  ┌─────────────────────────────────────────────────────────────┐  │
│  │  二级缓存 (earlySingletonObjects)                           │  │
│  │  ┌───────────────────────────────────────────────────────┐  │  │
│  │  │  Bean Name  →  提前暴露的 Bean 引用（可能是代理）        │  │  │
│  │  └───────────────────────────────────────────────────────┘  │  │
│  │  状态：已实例化 ✓  已填充属性 ✗  已初始化 ✗                  │  │
│  └─────────────────────────────────────────────────────────────┘  │
│                              ↑                                      │
│                              │ 从三级缓存获取后移入                  │
│                              │                                      │
│  ┌─────────────────────────────────────────────────────────────┐  │
│  │  三级缓存 (singletonFactories)                               │  │
│  │  ┌───────────────────────────────────────────────────────┐  │  │
│  │  │  Bean Name  →  ObjectFactory (创建早期引用的工厂)       │  │  │
│  │  └───────────────────────────────────────────────────────┘  │  │
│  │  状态：刚实例化，未填充属性，未初始化                         │  │
│  └─────────────────────────────────────────────────────────────┘  │
│                                                                     │
└────────────────────────────────────────────────────────────────────┘
```

## 三、循环依赖解决流程

### 3.1 详细流程图

```
假设 A 依赖 B，B 依赖 A

1. 创建 A
   ├─ 1.1 createBeanInstance(A) → 实例化 A
   ├─ 1.2 addSingletonFactory(A, ObjectFactory) → 放入三级缓存
   ├─ 1.3 populateBean(A) → 填充属性，发现依赖 B
   │       │
   │       ▼
   │   2. 创建 B
   │      ├─ 2.1 createBeanInstance(B) → 实例化 B
   │      ├─ 2.2 addSingletonFactory(B, ObjectFactory) → 放入三级缓存
   │      ├─ 2.3 populateBean(B) → 填充属性，发现依赖 A
   │      │       │
   │      │       ▼
   │      │   3. 获取 A
   │      │      ├─ 3.1 getSingleton(A) 
   │      │      │      └─ 一级缓存没有 A
   │      │      │      └─ 二级缓存没有 A
   │      │      │      └─ 三级缓存有 A 的工厂
   │      │      ├─ 3.2 调用 ObjectFactory.getObject()
   │      │      │      └─ 获取 A 的早期引用（可能是代理）
   │      │      ├─ 3.3 放入二级缓存，删除三级缓存
   │      │      └─ 3.4 返回 A 的早期引用
   │      │
   │      ├─ 2.4 B 注入 A 的早期引用
   │      ├─ 2.5 initializeBean(B) → 初始化 B
   │      └─ 2.6 addSingleton(B) → B 放入一级缓存
   │
   ├─ 1.4 A 注入完整的 B
   ├─ 1.5 initializeBean(A) → 初始化 A
   └─ 1.6 addSingleton(A) → A 放入一级缓存，删除二级缓存
```

### 3.2 核心源码分析

#### getSingleton - 获取单例

```java
protected Object getSingleton(String beanName, boolean allowEarlyReference) {
    // 1. 先从一级缓存获取
    Object singletonObject = this.singletonObjects.get(beanName);
    
    if (singletonObject == null && isSingletonCurrentlyInCreation(beanName)) {
        // 2. 一级缓存没有，且 Bean 正在创建中，从二级缓存获取
        singletonObject = this.earlySingletonObjects.get(beanName);
        
        if (singletonObject == null && allowEarlyReference) {
            synchronized (this.singletonObjects) {
                // 双重检查
                singletonObject = this.singletonObjects.get(beanName);
                if (singletonObject == null) {
                    singletonObject = this.earlySingletonObjects.get(beanName);
                    if (singletonObject == null) {
                        // 3. 从三级缓存获取 ObjectFactory
                        ObjectFactory<?> singletonFactory = 
                            this.singletonFactories.get(beanName);
                        if (singletonFactory != null) {
                            // 4. 调用 ObjectFactory 获取早期引用
                            singletonObject = singletonFactory.getObject();
                            // 5. 放入二级缓存
                            this.earlySingletonObjects.put(beanName, singletonObject);
                            // 6. 删除三级缓存
                            this.singletonFactories.remove(beanName);
                        }
                    }
                }
            }
        }
    }
    return singletonObject;
}
```

#### addSingletonFactory - 添加到三级缓存

```java
protected void addSingletonFactory(String beanName, ObjectFactory<?> singletonFactory) {
    synchronized (this.singletonObjects) {
        if (!this.singletonObjects.containsKey(beanName)) {
            // 放入三级缓存
            this.singletonFactories.put(beanName, singletonFactory);
            // 删除二级缓存（如果有）
            this.earlySingletonObjects.remove(beanName);
            // 标记为已注册
            this.registeredSingletons.add(beanName);
        }
    }
}
```

#### doCreateBean - 创建 Bean 时的处理

```java
protected Object doCreateBean(String beanName, RootBeanDefinition mbd, Object[] args) {
    
    // 1. 实例化 Bean
    BeanWrapper instanceWrapper = createBeanInstance(beanName, mbd, args);
    Object bean = instanceWrapper.getWrappedInstance();
    
    // 2. 判断是否需要提前暴露
    boolean earlySingletonExposure = (mbd.isSingleton() && 
        this.allowCircularReferences && 
        isSingletonCurrentlyInCreation(beanName));
    
    if (earlySingletonExposure) {
        // 3. 添加到三级缓存
        // ObjectFactory 会在需要时调用 getEarlyBeanReference
        addSingletonFactory(beanName, () -> getEarlyBeanReference(beanName, mbd, bean));
    }
    
    Object exposedObject = bean;
    try {
        // 4. 属性填充（可能触发依赖 Bean 的创建）
        populateBean(beanName, mbd, instanceWrapper);
        
        // 5. 初始化
        exposedObject = initializeBean(beanName, exposedObject, mbd);
    } catch (Throwable ex) {
        throw new BeanCreationException(beanName, ex);
    }
    
    // 6. 处理循环依赖的最终检查
    if (earlySingletonExposure) {
        Object earlySingletonReference = getSingleton(beanName, false);
        if (earlySingletonReference != null) {
            if (exposedObject == bean) {
                exposedObject = earlySingletonReference;
            }
        }
    }
    
    return exposedObject;
}
```

#### getEarlyBeanReference - 获取早期引用

```java
protected Object getEarlyBeanReference(String beanName, RootBeanDefinition mbd, Object bean) {
    Object exposedObject = bean;
    
    // 如果有 SmartInstantiationAwareBeanPostProcessor，可能返回代理
    if (!mbd.isSynthetic() && hasInstantiationAwareBeanPostProcessors()) {
        for (SmartInstantiationAwareBeanPostProcessor bp : 
                getBeanPostProcessorCache().smartInstantiationAware) {
            // AOP 在这里创建代理
            exposedObject = bp.getEarlyBeanReference(exposedObject, beanName);
        }
    }
    return exposedObject;
}
```

## 四、为什么需要三级缓存

### 4.1 为什么不只用二级缓存？

如果只有二级缓存：

```java
// 假设只有二级缓存
Map<String, Object> singletonObjects;      // 完整 Bean
Map<String, Object> earlySingletonObjects; // 早期 Bean

// 问题：每次实例化后都要立即创建代理
Object bean = createBeanInstance();

// 需要在这里就创建代理（AOP）
Object proxy = createProxyIfNeeded(bean);

earlySingletonObjects.put(beanName, proxy);
```

问题：
1. **性能浪费**：不是所有 Bean 都有循环依赖，没必要每个 Bean 都提前创建代理
2. **设计不合理**：AOP 代理应该在初始化后创建，而不是实例化后

### 4.2 三级缓存的优势

```java
// 三级缓存存储 ObjectFactory
singletonFactories.put(beanName, () -> getEarlyBeanReference(beanName, mbd, bean));

// 只有真正发生循环依赖时，才会调用 ObjectFactory 创建代理
// 没有循环依赖的 Bean，ObjectFactory 永远不会被调用
```

优势：
1. **延迟创建代理**：只在需要时才创建代理
2. **保持正确的代理创建时机**：没有循环依赖时，代理在 postProcessAfterInitialization 创建

## 五、无法解决的循环依赖

### 5.1 构造器注入

```java
@Service
public class ServiceA {
    private final ServiceB serviceB;
    
    @Autowired
    public ServiceA(ServiceB serviceB) { // 构造器注入
        this.serviceB = serviceB;
    }
}

@Service
public class ServiceB {
    private final ServiceA serviceA;
    
    @Autowired
    public ServiceB(ServiceA serviceA) { // 构造器注入
        this.serviceA = serviceA;
    }
}
```

**为什么无法解决？**

因为三级缓存的前提是 Bean 已经实例化（调用了构造函数）。构造器注入时，在调用构造函数之前就需要依赖，此时 Bean 还未实例化，无法放入任何缓存。

### 5.2 prototype 作用域

```java
@Service
@Scope("prototype")
public class PrototypeA {
    @Autowired
    private PrototypeB prototypeB;
}

@Service
@Scope("prototype")
public class PrototypeB {
    @Autowired
    private PrototypeA prototypeA;
}
```

**为什么无法解决？**

三级缓存只缓存单例 Bean。原型 Bean 每次获取都是新实例，不会被缓存。

### 5.3 解决方案

```java
// 1. 使用 @Lazy 延迟注入
@Service
public class ServiceA {
    @Autowired
    @Lazy
    private ServiceB serviceB;
}

// 2. 使用 setter 注入代替构造器注入
@Service
public class ServiceA {
    private ServiceB serviceB;
    
    @Autowired
    public void setServiceB(ServiceB serviceB) {
        this.serviceB = serviceB;
    }
}

// 3. 使用 ObjectFactory/Provider
@Service
public class ServiceA {
    @Autowired
    private ObjectFactory<ServiceB> serviceBFactory;
    
    public void doSomething() {
        ServiceB serviceB = serviceBFactory.getObject();
    }
}

// 4. 使用 @PostConstruct
@Service
public class ServiceA {
    @Autowired
    private ApplicationContext context;
    
    private ServiceB serviceB;
    
    @PostConstruct
    public void init() {
        this.serviceB = context.getBean(ServiceB.class);
    }
}
```

## 六、循环依赖检测

### 6.1 检测原理

```java
/**
 * 正在创建的单例 Bean 集合
 */
private final Set<String> singletonsCurrentlyInCreation = 
    Collections.newSetFromMap(new ConcurrentHashMap<>(16));

/**
 * 创建前标记
 */
protected void beforeSingletonCreation(String beanName) {
    if (!this.inCreationCheckExclusions.contains(beanName) && 
        !this.singletonsCurrentlyInCreation.add(beanName)) {
        throw new BeanCurrentlyInCreationException(beanName);
    }
}

/**
 * 创建后移除标记
 */
protected void afterSingletonCreation(String beanName) {
    if (!this.inCreationCheckExclusions.contains(beanName) && 
        !this.singletonsCurrentlyInCreation.remove(beanName)) {
        throw new IllegalStateException("Singleton '" + beanName + "' isn't currently in creation");
    }
}
```

### 6.2 prototype 循环依赖检测

```java
/**
 * 正在创建的 prototype Bean（ThreadLocal）
 */
private final ThreadLocal<Object> prototypesCurrentlyInCreation = 
    new NamedThreadLocal<>("Prototype beans currently in creation");

protected boolean isPrototypeCurrentlyInCreation(String beanName) {
    Object curVal = this.prototypesCurrentlyInCreation.get();
    return (curVal != null && 
        (curVal.equals(beanName) || (curVal instanceof Set && ((Set<?>) curVal).contains(beanName))));
}
```

## 七、常见面试问题

### Q1: Spring 为什么使用三级缓存？两级行不行？
> 答：两级缓存可以解决循环依赖，但会导致每个 Bean 实例化后都需要立即创建代理。三级缓存通过 ObjectFactory 延迟代理创建，只在真正需要时才创建，提高性能并保持正确的代理创建时机。

### Q2: 循环依赖中 AOP 代理是什么时候创建的？
> 答：有循环依赖时，代理在 getEarlyBeanReference 方法中创建（调用三级缓存的 ObjectFactory 时）。没有循环依赖时，代理在 postProcessAfterInitialization 中创建。

### Q3: 构造器注入为什么不能解决循环依赖？
> 答：因为三级缓存需要 Bean 已经实例化（调用过构造函数）。构造器注入时，在构造函数调用之前就需要依赖的 Bean，此时当前 Bean 还未实例化，无法放入缓存。

### Q4: 如何解决构造器注入的循环依赖？
> 答：1）使用 @Lazy 注解延迟注入；2）改用 setter/字段注入；3）使用 ObjectFactory/Provider；4）重新设计，消除循环依赖。

### Q5: prototype Bean 的循环依赖能解决吗？
> 答：不能。因为 prototype Bean 每次获取都是新实例，Spring 不会缓存 prototype Bean，所以无法解决循环依赖。
