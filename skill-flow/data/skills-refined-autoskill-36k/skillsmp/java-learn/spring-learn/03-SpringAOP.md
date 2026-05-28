# Spring AOP 详解

## 一、AOP 概述

### 1.1 什么是 AOP

AOP（Aspect-Oriented Programming，面向切面编程）是一种编程范式，它通过预编译或运行时动态代理实现程序功能的统一维护。

### 1.2 AOP 核心概念

| 术语 | 说明 | 示例 |
|------|------|------|
| **Aspect（切面）** | 横切关注点的模块化 | 日志、事务、安全 |
| **Join Point（连接点）** | 程序执行的某个点 | 方法调用、异常抛出 |
| **Pointcut（切入点）** | 匹配连接点的表达式 | execution(* com.example.*.*(..)) |
| **Advice（通知）** | 在切入点执行的动作 | @Before, @After, @Around |
| **Target（目标对象）** | 被代理的对象 | UserService |
| **Proxy（代理）** | 增强后的对象 | UserService$$EnhancerByCGLIB |
| **Weaving（织入）** | 将切面应用到目标对象的过程 | 编译期、加载期、运行期 |

### 1.3 AOP 执行流程图

```
┌────────────────────────────────────────────────────────────────┐
│                        客户端调用                               │
└────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌────────────────────────────────────────────────────────────────┐
│                        代理对象                                 │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │ @Around (前半部分)                                       │  │
│  │   ┌──────────────────────────────────────────────────┐  │  │
│  │   │ @Before                                          │  │  │
│  │   │   ┌───────────────────────────────────────────┐  │  │  │
│  │   │   │         目标方法执行                       │  │  │  │
│  │   │   └───────────────────────────────────────────┘  │  │  │
│  │   │ @AfterReturning (正常返回) / @AfterThrowing (异常)│  │  │
│  │   └──────────────────────────────────────────────────┘  │  │
│  │ @After (无论如何都执行)                                  │  │
│  │ @Around (后半部分)                                       │  │
│  └─────────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌────────────────────────────────────────────────────────────────┐
│                        返回结果                                 │
└────────────────────────────────────────────────────────────────┘
```

## 二、AOP 核心功能

### 2.1 切入点表达式

```java
@Aspect
@Component
public class PointcutExamples {

    /**
     * execution - 方法执行
     * 格式：execution(修饰符? 返回类型 类路径?方法名(参数) 异常?)
     */
    // 匹配 public 方法
    @Pointcut("execution(public * *(..))")
    public void publicMethod() {}
    
    // 匹配所有 service 包的方法
    @Pointcut("execution(* com.example.service.*.*(..))")
    public void serviceLayer() {}
    
    // 匹配所有 save 开头的方法
    @Pointcut("execution(* save*(..))")
    public void saveMethod() {}
    
    // 匹配第一个参数为 String 的方法
    @Pointcut("execution(* *(String, ..))")
    public void firstParamString() {}
    
    /**
     * within - 类型匹配
     */
    // 匹配 service 包下所有类
    @Pointcut("within(com.example.service.*)")
    public void withinService() {}
    
    // 匹配 service 包及子包
    @Pointcut("within(com.example.service..*)")
    public void withinServiceAndSub() {}
    
    /**
     * @annotation - 方法注解匹配
     */
    @Pointcut("@annotation(com.example.annotation.Log)")
    public void logAnnotation() {}
    
    /**
     * @within - 类注解匹配
     */
    @Pointcut("@within(org.springframework.stereotype.Service)")
    public void serviceAnnotation() {}
    
    /**
     * bean - Bean 名称匹配（Spring 特有）
     */
    @Pointcut("bean(userService)")
    public void userServiceBean() {}
    
    @Pointcut("bean(*Service)")
    public void anyServiceBean() {}
    
    /**
     * this - 代理对象类型匹配
     */
    @Pointcut("this(com.example.service.UserService)")
    public void thisUserService() {}
    
    /**
     * target - 目标对象类型匹配
     */
    @Pointcut("target(com.example.service.UserService)")
    public void targetUserService() {}
    
    /**
     * args - 参数类型匹配
     */
    @Pointcut("args(String, Integer)")
    public void stringIntegerArgs() {}
    
    /**
     * 组合切入点
     */
    @Pointcut("serviceLayer() && @annotation(Log)")
    public void serviceWithLog() {}
    
    @Pointcut("serviceLayer() || within(com.example.controller.*)")
    public void serviceOrController() {}
    
    @Pointcut("serviceLayer() && !saveMethod()")
    public void serviceExceptSave() {}
}
```

### 2.2 五种通知类型

```java
@Aspect
@Component
@Order(1) // 切面执行顺序
public class LogAspect {
    
    private static final Logger log = LoggerFactory.getLogger(LogAspect.class);
    
    /**
     * @Before - 前置通知
     * 在目标方法执行前执行
     */
    @Before("execution(* com.example.service.*.*(..))")
    public void before(JoinPoint joinPoint) {
        String methodName = joinPoint.getSignature().getName();
        Object[] args = joinPoint.getArgs();
        log.info("【前置通知】方法: {}, 参数: {}", methodName, Arrays.toString(args));
    }
    
    /**
     * @After - 后置通知
     * 无论方法是否正常返回都会执行（类似 finally）
     */
    @After("execution(* com.example.service.*.*(..))")
    public void after(JoinPoint joinPoint) {
        log.info("【后置通知】方法: {}", joinPoint.getSignature().getName());
    }
    
    /**
     * @AfterReturning - 返回通知
     * 方法正常返回后执行
     */
    @AfterReturning(
        pointcut = "execution(* com.example.service.*.*(..))",
        returning = "result"
    )
    public void afterReturning(JoinPoint joinPoint, Object result) {
        log.info("【返回通知】方法: {}, 返回值: {}", 
            joinPoint.getSignature().getName(), result);
    }
    
    /**
     * @AfterThrowing - 异常通知
     * 方法抛出异常后执行
     */
    @AfterThrowing(
        pointcut = "execution(* com.example.service.*.*(..))",
        throwing = "ex"
    )
    public void afterThrowing(JoinPoint joinPoint, Exception ex) {
        log.error("【异常通知】方法: {}, 异常: {}", 
            joinPoint.getSignature().getName(), ex.getMessage());
    }
    
    /**
     * @Around - 环绕通知
     * 最强大的通知，可以控制目标方法是否执行
     */
    @Around("execution(* com.example.service.*.*(..))")
    public Object around(ProceedingJoinPoint pjp) throws Throwable {
        String methodName = pjp.getSignature().getName();
        long start = System.currentTimeMillis();
        
        log.info("【环绕通知-前】方法: {} 开始执行", methodName);
        
        try {
            // 执行目标方法
            Object result = pjp.proceed();
            
            log.info("【环绕通知-后】方法: {} 执行成功", methodName);
            return result;
            
        } catch (Throwable e) {
            log.error("【环绕通知-异常】方法: {} 执行异常", methodName);
            throw e;
        } finally {
            long cost = System.currentTimeMillis() - start;
            log.info("【环绕通知-完成】方法: {} 耗时: {}ms", methodName, cost);
        }
    }
}
```

### 2.3 获取切入点信息

```java
@Aspect
@Component
public class DetailAspect {
    
    @Before("@annotation(log)")
    public void before(JoinPoint joinPoint, Log log) {
        // 获取方法签名
        MethodSignature signature = (MethodSignature) joinPoint.getSignature();
        
        // 获取目标类
        Class<?> targetClass = joinPoint.getTarget().getClass();
        
        // 获取方法
        Method method = signature.getMethod();
        
        // 获取参数名
        String[] paramNames = signature.getParameterNames();
        
        // 获取参数值
        Object[] args = joinPoint.getArgs();
        
        // 获取注解属性
        String value = log.value();
        
        System.out.println("目标类: " + targetClass.getName());
        System.out.println("方法名: " + method.getName());
        System.out.println("参数: " + Arrays.toString(args));
        System.out.println("注解值: " + value);
    }
    
    /**
     * 修改参数
     */
    @Around("execution(* com.example.service.*.*(..))")
    public Object modifyArgs(ProceedingJoinPoint pjp) throws Throwable {
        Object[] args = pjp.getArgs();
        
        // 修改参数
        if (args.length > 0 && args[0] instanceof String) {
            args[0] = ((String) args[0]).toUpperCase();
        }
        
        // 使用修改后的参数执行
        return pjp.proceed(args);
    }
    
    /**
     * 修改返回值
     */
    @Around("execution(* com.example.service.*.*(..))")
    public Object modifyResult(ProceedingJoinPoint pjp) throws Throwable {
        Object result = pjp.proceed();
        
        // 修改返回值
        if (result instanceof String) {
            return ((String) result).toUpperCase();
        }
        
        return result;
    }
}
```

## 三、AOP 实际应用

### 3.1 日志切面

```java
/**
 * 自定义日志注解
 */
@Target(ElementType.METHOD)
@Retention(RetentionPolicy.RUNTIME)
public @interface Log {
    String value() default "";
    boolean recordParams() default true;
    boolean recordResult() default true;
}

/**
 * 日志切面
 */
@Aspect
@Component
public class LogAspect {
    
    private static final Logger log = LoggerFactory.getLogger(LogAspect.class);
    
    @Around("@annotation(logAnnotation)")
    public Object around(ProceedingJoinPoint pjp, Log logAnnotation) throws Throwable {
        MethodSignature signature = (MethodSignature) pjp.getSignature();
        String methodName = signature.getDeclaringType().getSimpleName() + 
            "." + signature.getName();
        
        String description = logAnnotation.value();
        if (StringUtils.isEmpty(description)) {
            description = methodName;
        }
        
        // 记录请求参数
        if (logAnnotation.recordParams()) {
            log.info("[{}] 请求参数: {}", description, Arrays.toString(pjp.getArgs()));
        }
        
        long start = System.currentTimeMillis();
        try {
            Object result = pjp.proceed();
            
            // 记录返回结果
            if (logAnnotation.recordResult()) {
                log.info("[{}] 返回结果: {}", description, result);
            }
            
            return result;
        } catch (Throwable e) {
            log.error("[{}] 执行异常: {}", description, e.getMessage());
            throw e;
        } finally {
            long cost = System.currentTimeMillis() - start;
            log.info("[{}] 执行耗时: {}ms", description, cost);
        }
    }
}
```

### 3.2 权限校验切面

```java
/**
 * 权限注解
 */
@Target(ElementType.METHOD)
@Retention(RetentionPolicy.RUNTIME)
public @interface RequirePermission {
    String[] value();
    Logical logical() default Logical.AND;
}

public enum Logical {
    AND, OR
}

/**
 * 权限切面
 */
@Aspect
@Component
public class PermissionAspect {
    
    @Autowired
    private SecurityService securityService;
    
    @Before("@annotation(permission)")
    public void checkPermission(JoinPoint joinPoint, RequirePermission permission) {
        String[] requiredPermissions = permission.value();
        Logical logical = permission.logical();
        
        User currentUser = securityService.getCurrentUser();
        Set<String> userPermissions = currentUser.getPermissions();
        
        boolean hasPermission;
        if (logical == Logical.AND) {
            hasPermission = userPermissions.containsAll(Arrays.asList(requiredPermissions));
        } else {
            hasPermission = Arrays.stream(requiredPermissions)
                .anyMatch(userPermissions::contains);
        }
        
        if (!hasPermission) {
            throw new AccessDeniedException("无权访问");
        }
    }
}
```

### 3.3 缓存切面

```java
/**
 * 缓存注解
 */
@Target(ElementType.METHOD)
@Retention(RetentionPolicy.RUNTIME)
public @interface Cached {
    String key() default "";
    int expireSeconds() default 300;
}

/**
 * 缓存切面
 */
@Aspect
@Component
public class CacheAspect {
    
    @Autowired
    private RedisTemplate<String, Object> redisTemplate;
    
    @Around("@annotation(cached)")
    public Object around(ProceedingJoinPoint pjp, Cached cached) throws Throwable {
        // 生成缓存 key
        String key = generateKey(pjp, cached.key());
        
        // 查询缓存
        Object cachedValue = redisTemplate.opsForValue().get(key);
        if (cachedValue != null) {
            return cachedValue;
        }
        
        // 执行方法
        Object result = pjp.proceed();
        
        // 放入缓存
        if (result != null) {
            redisTemplate.opsForValue().set(key, result, 
                cached.expireSeconds(), TimeUnit.SECONDS);
        }
        
        return result;
    }
    
    private String generateKey(ProceedingJoinPoint pjp, String keyExpression) {
        if (StringUtils.hasText(keyExpression)) {
            // 解析 SpEL 表达式
            return parseSpEL(keyExpression, pjp);
        }
        
        // 默认 key：类名.方法名:参数
        MethodSignature signature = (MethodSignature) pjp.getSignature();
        return signature.getDeclaringTypeName() + "." + 
            signature.getName() + ":" + 
            Arrays.toString(pjp.getArgs());
    }
}
```

### 3.4 重试切面

```java
/**
 * 重试注解
 */
@Target(ElementType.METHOD)
@Retention(RetentionPolicy.RUNTIME)
public @interface Retry {
    int maxAttempts() default 3;
    long delay() default 1000;
    Class<? extends Throwable>[] retryFor() default {Exception.class};
}

/**
 * 重试切面
 */
@Aspect
@Component
public class RetryAspect {
    
    private static final Logger log = LoggerFactory.getLogger(RetryAspect.class);
    
    @Around("@annotation(retry)")
    public Object around(ProceedingJoinPoint pjp, Retry retry) throws Throwable {
        int maxAttempts = retry.maxAttempts();
        long delay = retry.delay();
        Class<? extends Throwable>[] retryFor = retry.retryFor();
        
        Throwable lastException = null;
        
        for (int attempt = 1; attempt <= maxAttempts; attempt++) {
            try {
                return pjp.proceed();
            } catch (Throwable e) {
                lastException = e;
                
                // 检查是否需要重试
                boolean shouldRetry = Arrays.stream(retryFor)
                    .anyMatch(clazz -> clazz.isInstance(e));
                
                if (!shouldRetry || attempt == maxAttempts) {
                    throw e;
                }
                
                log.warn("方法执行失败，第 {} 次重试，延迟 {}ms", attempt, delay);
                Thread.sleep(delay);
            }
        }
        
        throw lastException;
    }
}
```

## 四、AOP 源码分析

### 4.1 AOP 代理创建流程

```java
/**
 * AOP 代理创建核心流程
 */
public abstract class AbstractAutoProxyCreator extends ProxyProcessorSupport
        implements SmartInstantiationAwareBeanPostProcessor {
    
    /**
     * 在 Bean 初始化后创建代理
     */
    @Override
    public Object postProcessAfterInitialization(Object bean, String beanName) {
        if (bean != null) {
            Object cacheKey = getCacheKey(bean.getClass(), beanName);
            if (this.earlyProxyReferences.remove(cacheKey) != bean) {
                return wrapIfNecessary(bean, beanName, cacheKey);
            }
        }
        return bean;
    }
    
    /**
     * 决定是否需要代理
     */
    protected Object wrapIfNecessary(Object bean, String beanName, Object cacheKey) {
        // 1. 获取匹配的增强器
        Object[] specificInterceptors = getAdvicesAndAdvisorsForBean(
            bean.getClass(), beanName, null);
        
        if (specificInterceptors != DO_NOT_PROXY) {
            // 2. 创建代理
            this.advisedBeans.put(cacheKey, Boolean.TRUE);
            Object proxy = createProxy(
                bean.getClass(), beanName, specificInterceptors, 
                new SingletonTargetSource(bean));
            this.proxyTypes.put(cacheKey, proxy.getClass());
            return proxy;
        }
        
        return bean;
    }
    
    /**
     * 创建代理对象
     */
    protected Object createProxy(Class<?> beanClass, String beanName,
            Object[] specificInterceptors, TargetSource targetSource) {
        
        ProxyFactory proxyFactory = new ProxyFactory();
        proxyFactory.copyFrom(this);
        
        // 决定使用 JDK 还是 CGLIB
        if (!proxyFactory.isProxyTargetClass()) {
            if (shouldProxyTargetClass(beanClass, beanName)) {
                proxyFactory.setProxyTargetClass(true);
            } else {
                evaluateProxyInterfaces(beanClass, proxyFactory);
            }
        }
        
        // 添加增强器
        Advisor[] advisors = buildAdvisors(beanName, specificInterceptors);
        proxyFactory.addAdvisors(advisors);
        proxyFactory.setTargetSource(targetSource);
        
        // 创建代理
        return proxyFactory.getProxy(getProxyClassLoader());
    }
}
```

### 4.2 代理执行流程

```java
/**
 * JDK 动态代理执行
 */
final class JdkDynamicAopProxy implements AopProxy, InvocationHandler {
    
    @Override
    public Object invoke(Object proxy, Method method, Object[] args) throws Throwable {
        // 1. 获取拦截器链
        List<Object> chain = this.advised.getInterceptorsAndDynamicInterceptionAdvice(
            method, targetClass);
        
        if (chain.isEmpty()) {
            // 没有拦截器，直接调用目标方法
            return AopUtils.invokeJoinpointUsingReflection(target, method, args);
        }
        
        // 2. 创建方法调用对象
        MethodInvocation invocation = new ReflectiveMethodInvocation(
            proxy, target, method, args, targetClass, chain);
        
        // 3. 执行拦截器链
        return invocation.proceed();
    }
}

/**
 * 拦截器链执行
 */
public class ReflectiveMethodInvocation implements ProxyMethodInvocation {
    
    protected final List<?> interceptorsAndDynamicMethodMatchers;
    private int currentInterceptorIndex = -1;
    
    @Override
    public Object proceed() throws Throwable {
        // 执行完所有拦截器后，执行目标方法
        if (this.currentInterceptorIndex == 
                this.interceptorsAndDynamicMethodMatchers.size() - 1) {
            return invokeJoinpoint();
        }
        
        // 获取下一个拦截器
        Object interceptorOrInterceptionAdvice = 
            this.interceptorsAndDynamicMethodMatchers.get(++this.currentInterceptorIndex);
        
        if (interceptorOrInterceptionAdvice instanceof MethodInterceptor) {
            MethodInterceptor mi = (MethodInterceptor) interceptorOrInterceptionAdvice;
            // 调用拦截器
            return mi.invoke(this);
        }
        
        // 继续下一个
        return proceed();
    }
}
```

## 五、常见面试问题

### Q1: Spring AOP 和 AspectJ 的区别？
> 答：Spring AOP 是运行时通过动态代理实现，只支持方法级别的切入；AspectJ 是编译时织入，支持更多切入点（字段、构造器等）。Spring AOP 更简单，AspectJ 更强大。

### Q2: JDK 动态代理和 CGLIB 代理的选择？
> 答：目标类有接口时默认用 JDK 动态代理，无接口时用 CGLIB。可以通过 `proxyTargetClass=true` 强制使用 CGLIB。

### Q3: 为什么同一个类中方法互调不会触发 AOP？
> 答：因为同类方法互调是 `this.method()` 而不是通过代理对象调用，所以不会经过代理。解决方法：1）注入自身代理 2）`AopContext.currentProxy()`。

### Q4: @Around 通知能阻止目标方法执行吗？
> 答：可以。在环绕通知中不调用 `pjp.proceed()` 即可阻止目标方法执行。

### Q5: 多个切面的执行顺序如何控制？
> 答：通过 `@Order` 注解或实现 `Ordered` 接口。数值越小优先级越高。
