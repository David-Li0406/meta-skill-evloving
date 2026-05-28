# 代理模式 (Proxy Pattern)

## 一、什么是代理模式

代理模式是一种结构型设计模式，它提供一个代理对象来控制对另一个对象的访问。代理对象在客户端和目标对象之间起到中介作用。

### 核心思想
- **控制访问**：代理控制对真实对象的访问
- **增强功能**：在不修改原对象的情况下增强功能
- **解耦**：客户端与真实对象解耦

### 代理模式分类
1. **静态代理**：编译期确定代理类
2. **动态代理**：运行期动态生成代理类
   - JDK 动态代理（基于接口）
   - CGLIB 动态代理（基于继承）

## 二、静态代理

### 2.1 结构图

```
┌─────────────┐        ┌─────────────┐
│   Client    │───────>│  Subject    │ (接口)
└─────────────┘        └─────────────┘
                              △
                              │
                    ┌─────────┴─────────┐
                    │                   │
            ┌───────┴───────┐   ┌───────┴───────┐
            │   RealSubject │   │     Proxy     │
            └───────────────┘   └───────────────┘
                                       │
                                       │ 持有
                                       ▼
                               ┌───────────────┐
                               │  RealSubject  │
                               └───────────────┘
```

### 2.2 代码实现

```java
/**
 * 主题接口
 */
public interface UserService {
    void addUser(User user);
    User getUser(Long id);
    void deleteUser(Long id);
}

/**
 * 真实主题
 */
public class UserServiceImpl implements UserService {
    
    @Override
    public void addUser(User user) {
        System.out.println("添加用户: " + user.getName());
    }
    
    @Override
    public User getUser(Long id) {
        System.out.println("查询用户: " + id);
        return new User(id, "用户" + id);
    }
    
    @Override
    public void deleteUser(Long id) {
        System.out.println("删除用户: " + id);
    }
}

/**
 * 静态代理 - 日志代理
 */
public class UserServiceLogProxy implements UserService {
    
    private UserService target;
    
    public UserServiceLogProxy(UserService target) {
        this.target = target;
    }
    
    @Override
    public void addUser(User user) {
        System.out.println("[LOG] 开始添加用户: " + user.getName());
        long start = System.currentTimeMillis();
        
        target.addUser(user);
        
        long cost = System.currentTimeMillis() - start;
        System.out.println("[LOG] 添加用户完成，耗时: " + cost + "ms");
    }
    
    @Override
    public User getUser(Long id) {
        System.out.println("[LOG] 开始查询用户: " + id);
        long start = System.currentTimeMillis();
        
        User user = target.getUser(id);
        
        long cost = System.currentTimeMillis() - start;
        System.out.println("[LOG] 查询用户完成，耗时: " + cost + "ms");
        return user;
    }
    
    @Override
    public void deleteUser(Long id) {
        System.out.println("[LOG] 开始删除用户: " + id);
        long start = System.currentTimeMillis();
        
        target.deleteUser(id);
        
        long cost = System.currentTimeMillis() - start;
        System.out.println("[LOG] 删除用户完成，耗时: " + cost + "ms");
    }
}

// 使用示例
public class Client {
    public static void main(String[] args) {
        UserService target = new UserServiceImpl();
        UserService proxy = new UserServiceLogProxy(target);
        
        proxy.addUser(new User(1L, "张三"));
        proxy.getUser(1L);
    }
}
```

### 2.3 静态代理的优缺点

**优点：**
- 简单直观，易于理解
- 编译期检查类型安全

**缺点：**
- 需要为每个接口创建代理类
- 接口方法增加时，代理类也需要同步修改
- 代码重复，维护成本高

## 三、JDK 动态代理

### 3.1 原理

JDK 动态代理基于 Java 反射机制，通过 `java.lang.reflect.Proxy` 类在运行时动态生成代理类。

**核心组件：**
- `Proxy`：用于创建代理实例
- `InvocationHandler`：代理逻辑的处理器

### 3.2 代码实现

```java
/**
 * JDK 动态代理 - InvocationHandler
 */
public class LogInvocationHandler implements InvocationHandler {
    
    private Object target;
    
    public LogInvocationHandler(Object target) {
        this.target = target;
    }
    
    @Override
    public Object invoke(Object proxy, Method method, Object[] args) throws Throwable {
        String methodName = method.getName();
        
        // 前置处理
        System.out.println("[LOG] 开始执行: " + methodName);
        long start = System.currentTimeMillis();
        
        try {
            // 调用目标方法
            Object result = method.invoke(target, args);
            
            // 后置处理
            long cost = System.currentTimeMillis() - start;
            System.out.println("[LOG] 执行成功: " + methodName + ", 耗时: " + cost + "ms");
            
            return result;
        } catch (Exception e) {
            // 异常处理
            System.out.println("[LOG] 执行异常: " + methodName + ", 错误: " + e.getMessage());
            throw e;
        }
    }
}

/**
 * JDK 动态代理工厂
 */
public class JdkProxyFactory {
    
    @SuppressWarnings("unchecked")
    public static <T> T createProxy(T target) {
        return (T) Proxy.newProxyInstance(
            target.getClass().getClassLoader(),     // 类加载器
            target.getClass().getInterfaces(),      // 目标接口
            new LogInvocationHandler(target)        // 调用处理器
        );
    }
    
    /**
     * 带自定义 Handler 的代理工厂
     */
    @SuppressWarnings("unchecked")
    public static <T> T createProxy(T target, InvocationHandler handler) {
        return (T) Proxy.newProxyInstance(
            target.getClass().getClassLoader(),
            target.getClass().getInterfaces(),
            handler
        );
    }
}

// 使用示例
public class Client {
    public static void main(String[] args) {
        UserService target = new UserServiceImpl();
        UserService proxy = JdkProxyFactory.createProxy(target);
        
        proxy.addUser(new User(1L, "张三"));
        proxy.getUser(1L);
    }
}
```

### 3.3 通用代理 Handler

```java
/**
 * 通用代理 Handler - 支持多种增强
 */
public class GenericInvocationHandler implements InvocationHandler {
    
    private Object target;
    private BeforeAdvice beforeAdvice;
    private AfterAdvice afterAdvice;
    private ExceptionAdvice exceptionAdvice;
    
    public GenericInvocationHandler(Object target) {
        this.target = target;
    }
    
    public GenericInvocationHandler before(BeforeAdvice advice) {
        this.beforeAdvice = advice;
        return this;
    }
    
    public GenericInvocationHandler after(AfterAdvice advice) {
        this.afterAdvice = advice;
        return this;
    }
    
    public GenericInvocationHandler onException(ExceptionAdvice advice) {
        this.exceptionAdvice = advice;
        return this;
    }
    
    @Override
    public Object invoke(Object proxy, Method method, Object[] args) throws Throwable {
        try {
            // 前置通知
            if (beforeAdvice != null) {
                beforeAdvice.before(method, args);
            }
            
            // 执行目标方法
            Object result = method.invoke(target, args);
            
            // 后置通知
            if (afterAdvice != null) {
                afterAdvice.after(method, args, result);
            }
            
            return result;
            
        } catch (InvocationTargetException e) {
            Throwable cause = e.getCause();
            // 异常通知
            if (exceptionAdvice != null) {
                exceptionAdvice.onException(method, args, cause);
            }
            throw cause;
        }
    }
}

// 函数式接口
@FunctionalInterface
public interface BeforeAdvice {
    void before(Method method, Object[] args);
}

@FunctionalInterface
public interface AfterAdvice {
    void after(Method method, Object[] args, Object result);
}

@FunctionalInterface
public interface ExceptionAdvice {
    void onException(Method method, Object[] args, Throwable e);
}

// 使用示例
public class Client {
    public static void main(String[] args) {
        UserService target = new UserServiceImpl();
        
        GenericInvocationHandler handler = new GenericInvocationHandler(target)
            .before((method, params) -> System.out.println("Before: " + method.getName()))
            .after((method, params, result) -> System.out.println("After: " + result))
            .onException((method, params, e) -> System.out.println("Exception: " + e.getMessage()));
        
        UserService proxy = JdkProxyFactory.createProxy(target, handler);
        proxy.getUser(1L);
    }
}
```

### 3.4 JDK 动态代理原理分析

```java
/**
 * 生成的代理类大致结构（反编译后）
 */
public final class $Proxy0 extends Proxy implements UserService {
    
    private static Method m3; // addUser
    private static Method m4; // getUser
    private static Method m5; // deleteUser
    
    static {
        try {
            m3 = Class.forName("UserService").getMethod("addUser", User.class);
            m4 = Class.forName("UserService").getMethod("getUser", Long.class);
            m5 = Class.forName("UserService").getMethod("deleteUser", Long.class);
        } catch (Exception e) {
            throw new RuntimeException(e);
        }
    }
    
    public $Proxy0(InvocationHandler h) {
        super(h);
    }
    
    @Override
    public void addUser(User user) {
        try {
            // 调用 InvocationHandler.invoke()
            h.invoke(this, m3, new Object[]{user});
        } catch (Throwable e) {
            throw new RuntimeException(e);
        }
    }
    
    @Override
    public User getUser(Long id) {
        try {
            return (User) h.invoke(this, m4, new Object[]{id});
        } catch (Throwable e) {
            throw new RuntimeException(e);
        }
    }
    
    @Override
    public void deleteUser(Long id) {
        try {
            h.invoke(this, m5, new Object[]{id});
        } catch (Throwable e) {
            throw new RuntimeException(e);
        }
    }
}
```

## 四、CGLIB 动态代理

### 4.1 原理

CGLIB（Code Generation Library）通过**继承**目标类，在运行时动态生成子类来实现代理。

**核心组件：**
- `Enhancer`：用于创建代理实例
- `MethodInterceptor`：方法拦截器

### 4.2 依赖配置

```xml
<dependency>
    <groupId>cglib</groupId>
    <artifactId>cglib</artifactId>
    <version>3.3.0</version>
</dependency>
```

### 4.3 代码实现

```java
/**
 * 目标类（不需要实现接口）
 */
public class OrderService {
    
    public Order createOrder(String productId, int quantity) {
        System.out.println("创建订单: " + productId + ", 数量: " + quantity);
        return new Order(UUID.randomUUID().toString(), productId, quantity);
    }
    
    public void cancelOrder(String orderId) {
        System.out.println("取消订单: " + orderId);
    }
    
    // final 方法不能被代理
    public final void finalMethod() {
        System.out.println("这是 final 方法，不能被代理");
    }
}

/**
 * CGLIB 方法拦截器
 */
public class LogMethodInterceptor implements MethodInterceptor {
    
    @Override
    public Object intercept(Object obj, Method method, Object[] args, 
                           MethodProxy proxy) throws Throwable {
        String methodName = method.getName();
        
        // 前置处理
        System.out.println("[CGLIB LOG] 开始执行: " + methodName);
        long start = System.currentTimeMillis();
        
        try {
            // 调用父类方法（即原始方法）
            Object result = proxy.invokeSuper(obj, args);
            
            // 后置处理
            long cost = System.currentTimeMillis() - start;
            System.out.println("[CGLIB LOG] 执行成功: " + methodName + ", 耗时: " + cost + "ms");
            
            return result;
        } catch (Exception e) {
            System.out.println("[CGLIB LOG] 执行异常: " + methodName);
            throw e;
        }
    }
}

/**
 * CGLIB 代理工厂
 */
public class CglibProxyFactory {
    
    @SuppressWarnings("unchecked")
    public static <T> T createProxy(Class<T> clazz) {
        Enhancer enhancer = new Enhancer();
        // 设置父类
        enhancer.setSuperclass(clazz);
        // 设置回调
        enhancer.setCallback(new LogMethodInterceptor());
        // 创建代理对象
        return (T) enhancer.create();
    }
    
    /**
     * 带构造参数的代理创建
     */
    @SuppressWarnings("unchecked")
    public static <T> T createProxy(Class<T> clazz, Class<?>[] argTypes, Object[] args) {
        Enhancer enhancer = new Enhancer();
        enhancer.setSuperclass(clazz);
        enhancer.setCallback(new LogMethodInterceptor());
        return (T) enhancer.create(argTypes, args);
    }
    
    /**
     * 带自定义拦截器的代理创建
     */
    @SuppressWarnings("unchecked")
    public static <T> T createProxy(Class<T> clazz, MethodInterceptor interceptor) {
        Enhancer enhancer = new Enhancer();
        enhancer.setSuperclass(clazz);
        enhancer.setCallback(interceptor);
        return (T) enhancer.create();
    }
}

// 使用示例
public class Client {
    public static void main(String[] args) {
        OrderService proxy = CglibProxyFactory.createProxy(OrderService.class);
        
        proxy.createOrder("P001", 2);
        proxy.cancelOrder("ORD001");
        proxy.finalMethod(); // 不会被代理
    }
}
```

### 4.4 多个拦截器

```java
/**
 * 使用 CallbackFilter 实现不同方法使用不同拦截器
 */
public class CglibProxyWithFilter {
    
    public static OrderService createProxy() {
        Enhancer enhancer = new Enhancer();
        enhancer.setSuperclass(OrderService.class);
        
        // 多个回调
        Callback[] callbacks = new Callback[]{
            new LogMethodInterceptor(),      // 索引 0
            new SecurityMethodInterceptor(), // 索引 1
            NoOp.INSTANCE                    // 索引 2（不拦截）
        };
        enhancer.setCallbacks(callbacks);
        
        // 回调过滤器
        enhancer.setCallbackFilter(method -> {
            String name = method.getName();
            if (name.startsWith("create")) {
                return 1; // 使用 SecurityMethodInterceptor
            } else if (name.startsWith("cancel")) {
                return 0; // 使用 LogMethodInterceptor
            } else {
                return 2; // 不拦截
            }
        });
        
        return (OrderService) enhancer.create();
    }
}

/**
 * 安全检查拦截器
 */
public class SecurityMethodInterceptor implements MethodInterceptor {
    
    @Override
    public Object intercept(Object obj, Method method, Object[] args, 
                           MethodProxy proxy) throws Throwable {
        // 安全检查
        System.out.println("[SECURITY] 执行安全检查...");
        if (!checkPermission()) {
            throw new SecurityException("没有权限执行此操作");
        }
        
        return proxy.invokeSuper(obj, args);
    }
    
    private boolean checkPermission() {
        // 检查权限逻辑
        return true;
    }
}
```

## 五、JDK 代理 vs CGLIB 代理

| 特性 | JDK 动态代理 | CGLIB 代理 |
|------|-------------|-----------|
| 实现方式 | 基于接口 | 基于继承 |
| 要求 | 目标类必须实现接口 | 目标类不能是 final |
| 代理对象 | 实现相同接口的新类 | 目标类的子类 |
| 方法限制 | 只能代理接口方法 | 不能代理 final/private 方法 |
| 性能（创建） | 较快 | 较慢 |
| 性能（调用） | 反射调用，较慢 | FastClass 机制，较快 |
| 依赖 | JDK 自带 | 需要引入 cglib 库 |
| Spring 默认 | 有接口时默认使用 | 无接口时使用 |

## 六、Spring AOP 中的代理选择

```java
/**
 * Spring AOP 代理选择策略
 */
@Configuration
@EnableAspectJAutoProxy(proxyTargetClass = false) // false: 优先 JDK, true: 强制 CGLIB
public class AopConfig {
    // proxyTargetClass = false（默认）:
    // - 目标类有接口 -> JDK 动态代理
    // - 目标类无接口 -> CGLIB 代理
    
    // proxyTargetClass = true:
    // - 无论有无接口，都使用 CGLIB 代理
}

// Spring Boot 2.x 默认使用 CGLIB
// 可以通过配置修改：
// spring.aop.proxy-target-class=false
```

## 七、代理模式应用场景

### 7.1 远程代理（RPC）

```java
/**
 * RPC 代理 - 隐藏远程调用细节
 */
public class RpcProxyHandler implements InvocationHandler {
    
    private String serviceAddress;
    
    @Override
    public Object invoke(Object proxy, Method method, Object[] args) throws Throwable {
        // 1. 构建请求
        RpcRequest request = new RpcRequest();
        request.setClassName(method.getDeclaringClass().getName());
        request.setMethodName(method.getName());
        request.setParameterTypes(method.getParameterTypes());
        request.setParameters(args);
        
        // 2. 发送网络请求
        RpcResponse response = sendRequest(serviceAddress, request);
        
        // 3. 返回结果
        return response.getResult();
    }
    
    private RpcResponse sendRequest(String address, RpcRequest request) {
        // 网络通信逻辑
        return null;
    }
}
```

### 7.2 缓存代理

```java
/**
 * 缓存代理
 */
public class CacheProxy implements InvocationHandler {
    
    private Object target;
    private Map<String, Object> cache = new ConcurrentHashMap<>();
    
    @Override
    public Object invoke(Object proxy, Method method, Object[] args) throws Throwable {
        // 只缓存 get 方法
        if (method.getName().startsWith("get")) {
            String key = generateKey(method, args);
            
            Object result = cache.get(key);
            if (result != null) {
                System.out.println("从缓存获取: " + key);
                return result;
            }
            
            result = method.invoke(target, args);
            cache.put(key, result);
            System.out.println("放入缓存: " + key);
            return result;
        }
        
        return method.invoke(target, args);
    }
    
    private String generateKey(Method method, Object[] args) {
        return method.getName() + "_" + Arrays.toString(args);
    }
}
```

### 7.3 延迟加载代理

```java
/**
 * 延迟加载代理
 */
public class LazyLoadProxy<T> implements InvocationHandler {
    
    private Supplier<T> supplier;
    private T target;
    
    public LazyLoadProxy(Supplier<T> supplier) {
        this.supplier = supplier;
    }
    
    @Override
    public Object invoke(Object proxy, Method method, Object[] args) throws Throwable {
        // 延迟初始化
        if (target == null) {
            synchronized (this) {
                if (target == null) {
                    System.out.println("延迟加载目标对象...");
                    target = supplier.get();
                }
            }
        }
        return method.invoke(target, args);
    }
}
```

## 八、面试常见问题

### Q1: JDK 动态代理和 CGLIB 的区别？
> 答：JDK 动态代理基于接口，通过反射实现；CGLIB 基于继承，通过生成子类实现。JDK 代理只能代理接口方法，CGLIB 可以代理普通类但不能代理 final 方法。

### Q2: 为什么 JDK 动态代理必须基于接口？
> 答：因为 JDK 动态代理生成的代理类继承了 Proxy 类，Java 单继承的限制使得它只能通过实现接口来实现代理。

### Q3: Spring AOP 默认使用哪种代理？
> 答：Spring AOP 默认情况下，如果目标类有接口则使用 JDK 动态代理，无接口则使用 CGLIB。Spring Boot 2.x 默认使用 CGLIB。

### Q4: 代理模式和装饰器模式的区别？
> 答：目的不同。代理模式控制对对象的访问，装饰器模式增强对象功能。代理通常在编译期确定代理关系，装饰器可以动态组合。
