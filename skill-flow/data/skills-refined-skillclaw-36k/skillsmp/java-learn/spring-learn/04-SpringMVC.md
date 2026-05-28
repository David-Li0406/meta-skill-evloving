# Spring MVC 架构与高并发实战

## 一、Spring MVC 核心架构

### 1.1 核心组件交互图
```
┌─────────────┐    HTTP Request     ┌─────────────────────┐
│   Client    │ ──────────────────> │  DispatcherServlet  │
└─────────────┘                     └──────────┬──────────┘
       ▲                                       │
       │                                       │ 1. getHandler()
       │                                       ▼
       │                            ┌─────────────────────┐
       │                            │   HandlerMapping    │
       │                            └──────────┬──────────┘
       │                                       │
       │                                       │ 2. HandlerExecutionChain
       │                                       ▼
       │                            ┌─────────────────────┐
       │                            │   HandlerAdapter    │
       │                            └──────────┬──────────┘
       │                                       │
       │                                       │ 3. handle()
       │                                       ▼
       │                            ┌─────────────────────┐
       │                            │     Controller      │
       │                            └──────────┬──────────┘
       │                                       │
       │                                       │ 4. ModelAndView (Legacy)
       │                                       │    or @ResponseBody
       │                                       ▼
       │                            ┌─────────────────────┐
       │                            │    ViewResolver     │
       │                            └──────────┬──────────┘
       │                                       │
       │                                       │ 5. View
       │                                       ▼
HTTP Response <───────────────────── ┌─────────────────────┐
                                     │   View Rendering    │
                                     └─────────────────────┘
```

### 1.2 DispatcherServlet 源码精髓
`doDispatch` 是核心调度方法：
```java
protected void doDispatch(HttpServletRequest request, HttpServletResponse response) {
    HandlerExecutionChain mappedHandler = null;
    try {
        // 1. 查找 Handler (Controller 方法 + 拦截器链)
        mappedHandler = getHandler(request);
        if (mappedHandler == null) {
            noHandlerFound(request, response);
            return;
        }

        // 2. 查找 Adapter (适配器模式，支持多种 Controller 写法)
        HandlerAdapter ha = getHandlerAdapter(mappedHandler.getHandler());

        // 3. 执行拦截器 preHandle
        if (!mappedHandler.applyPreHandle(request, response)) {
            return;
        }

        // 4. 执行业务逻辑
        ModelAndView mv = ha.handle(request, response, mappedHandler.getHandler());

        // 5. 执行拦截器 postHandle
        mappedHandler.applyPostHandle(request, response, mv);

        // 6. 处理视图渲染或异常
        processDispatchResult(request, response, mappedHandler, mv, null);

    } catch (Exception ex) {
        triggerAfterCompletion(request, response, mappedHandler, ex);
    }
}
```

## 二、高并发场景：异步请求处理

在 Tomcat 线程池有限的情况下（默认 200），如果 Controller 执行耗时操作（如 IO、RPC），会耗尽 HTTP 线程。
**解决方案**：释放 Servlet 线程，业务在独立线程池执行。

### 2.1 Callable (Spring MVC 托管线程)
```java
@GetMapping("/async-callable")
public Callable<String> handleAsync() {
    System.out.println("主线程开始: " + Thread.currentThread().getName());
    
    return () -> {
        System.out.println("副线程开始: " + Thread.currentThread().getName());
        Thread.sleep(2000); // 模拟耗时 IO
        return "Callable Result";
    };
}
```

### 2.2 DeferredResult (完全自主控制)
比 Callable 更灵活，适合配合消息队列或长轮询使用。

```java
@RestController
public class AsyncController {
    
    // 保存未完成的请求
    private Map<String, DeferredResult<String>> requestMap = new ConcurrentHashMap<>();

    @GetMapping("/create-order")
    public DeferredResult<String> createOrder(String orderId) {
        // 1. 设置超时时间 10s 和超时结果
        DeferredResult<String> result = new DeferredResult<>(10000L, "Timeout");
        
        // 2. 注册回调
        result.onCompletion(() -> requestMap.remove(orderId));
        
        // 3. 存入 Map，主线程立即释放
        requestMap.put(orderId, result);
        
        // 4. 发送消息到 MQ (异步处理)
        mqProducer.send("order_topic", orderId);
        
        return result; 
    }

    // MQ 消费者收到处理完成消息后调用
    public void onMessageReceived(String orderId, String status) {
        DeferredResult<String> result = requestMap.get(orderId);
        if (result != null) {
            // 5. 设置结果，唤醒前端响应
            result.setResult(status);
        }
    }
}
```

## 三、全局处理与扩展点

### 3.1 ResponseBodyAdvice (统一响应包装)
无侵入地修改 `@ResponseBody` 的返回值。

```java
@ControllerAdvice
public class GlobalResponseHandler implements ResponseBodyAdvice<Object> {
    
    @Override
    public boolean supports(MethodParameter returnType, Class converterType) {
        return true; // 拦截所有
    }

    @Override
    public Object beforeBodyWrite(Object body, MethodParameter returnType, 
                                MediaType selectedContentType, 
                                Class selectedConverterType, 
                                ServerHttpRequest request, 
                                ServerHttpResponse response) {
        // 如果已经是统一格式，直接返回
        if (body instanceof Result) {
            return body;
        }
        // 包装成统一格式
        return Result.success(body);
    }
}
```

### 3.2 全局异常处理的最佳实践
```java
@RestControllerAdvice
public class GlobalExceptionHandler {

    @ExceptionHandler(BusinessException.class)
    public Result<?> handleBusinessException(BusinessException e) {
        return Result.fail(e.getCode(), e.getMessage());
    }

    @ExceptionHandler(MethodArgumentNotValidException.class)
    public Result<?> handleValidException(MethodArgumentNotValidException e) {
        // 提取校验失败的字段
        String msg = e.getBindingResult().getFieldErrors().stream()
            .map(FieldError::getDefaultMessage)
            .collect(Collectors.joining(","));
        return Result.fail(400, msg);
    }
}
```

## 四、常见面试题

### 4.1 Spring MVC 拦截器与 Filter 的区别？
1.  **依赖**：Filter 基于 Servlet 规范，依赖容器；Interceptor 基于 Spring，依赖 ApplicationContext。
2.  **范围**：Filter 过滤所有请求；Interceptor 只拦截进入 DispatcherServlet 的请求。
3.  **能力**：Interceptor 可以通过注入获取 Spring Bean，Filter 也可以但稍微麻烦（DelegatingFilterProxy）。
4.  **粒度**：Interceptor 可以访问 HandlerMethod（知道调用了哪个 Controller 方法），Filter 不行。

### 4.2 什么是参数解析器 (HandlerMethodArgumentResolver)？
它是将 HTTP 请求参数（Query, Body, Header）解析为 Controller 方法参数的核心组件。
*   `@RequestParam` -> `RequestParamMethodArgumentResolver`
*   `@RequestBody` -> `RequestResponseBodyMethodArgumentResolver`
*   **自定义**: 可以实现该接口，例如实现 `@CurrentUser` 自动注入当前登录用户。
