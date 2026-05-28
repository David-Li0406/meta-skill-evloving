# 委派模式 (Delegate Pattern)

## 一、什么是委派模式

委派模式不属于 GoF 23 种设计模式，但在实际开发中非常常用。它的基本思想是：一个对象接收到请求后，将请求委派给另一个对象来处理。

### 核心思想
- **任务分发**：委派者负责分发任务
- **结果汇总**：委派者负责收集结果
- **隐藏细节**：客户端不需要知道具体执行者

### 与其他模式的关系
- **与代理模式**：代理注重过程控制，委派注重结果
- **与策略模式**：策略模式由客户端选择策略，委派模式由委派者选择

## 二、委派模式结构

```
┌─────────────┐
│   Client    │
└─────────────┘
       │
       │ 请求
       ▼
┌─────────────┐      分发任务      ┌─────────────┐
│  Delegate   │───────────────────>│   Worker    │
│  (Boss)     │                    │  Interface  │
└─────────────┘                    └─────────────┘
                                          △
                                          │
                                ┌─────────┴─────────┐
                                │                   │
                          ┌─────┴─────┐       ┌─────┴─────┐
                          │  WorkerA  │       │  WorkerB  │
                          └───────────┘       └───────────┘
```

## 三、代码实现

### 3.1 基础实现

```java
/**
 * 员工接口
 */
public interface Employee {
    void doTask(String task);
}

/**
 * 程序员
 */
public class Programmer implements Employee {
    @Override
    public void doTask(String task) {
        System.out.println("程序员正在编写: " + task);
    }
}

/**
 * 设计师
 */
public class Designer implements Employee {
    @Override
    public void doTask(String task) {
        System.out.println("设计师正在设计: " + task);
    }
}

/**
 * 测试工程师
 */
public class Tester implements Employee {
    @Override
    public void doTask(String task) {
        System.out.println("测试工程师正在测试: " + task);
    }
}

/**
 * 项目经理（委派者）
 */
public class ProjectManager implements Employee {
    
    private Map<String, Employee> employees = new HashMap<>();
    
    public ProjectManager() {
        employees.put("开发", new Programmer());
        employees.put("设计", new Designer());
        employees.put("测试", new Tester());
    }
    
    @Override
    public void doTask(String task) {
        String taskType = parseTaskType(task);
        Employee employee = employees.get(taskType);
        
        if (employee != null) {
            System.out.println("项目经理分配任务: " + task);
            employee.doTask(task);
        } else {
            System.out.println("没有合适的员工处理该任务: " + task);
        }
    }
    
    private String parseTaskType(String task) {
        if (task.contains("开发") || task.contains("编码")) {
            return "开发";
        } else if (task.contains("设计") || task.contains("UI")) {
            return "设计";
        } else if (task.contains("测试") || task.contains("QA")) {
            return "测试";
        }
        return "";
    }
}

// 使用示例
public class Client {
    public static void main(String[] args) {
        ProjectManager pm = new ProjectManager();
        pm.doTask("开发用户模块");
        pm.doTask("设计首页UI");
        pm.doTask("测试登录功能");
    }
}
```

## 四、实际应用案例

### 4.1 Spring MVC 中的 DispatcherServlet

```java
/**
 * 模拟 Spring MVC 的 DispatcherServlet
 * DispatcherServlet 就是典型的委派模式
 */
public class DispatcherServlet extends HttpServlet {
    
    // Handler 映射
    private Map<String, Object> handlerMapping = new HashMap<>();
    
    @Override
    public void init() {
        // 初始化 Handler 映射
        handlerMapping.put("/user/list", new UserController());
        handlerMapping.put("/order/create", new OrderController());
        handlerMapping.put("/product/detail", new ProductController());
    }
    
    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) {
        doDispatch(req, resp);
    }
    
    @Override
    protected void doPost(HttpServletRequest req, HttpServletResponse resp) {
        doDispatch(req, resp);
    }
    
    /**
     * 委派分发
     */
    private void doDispatch(HttpServletRequest req, HttpServletResponse resp) {
        String uri = req.getRequestURI();
        
        // 1. 根据 URI 查找 Handler
        Object handler = handlerMapping.get(uri);
        
        if (handler == null) {
            try {
                resp.getWriter().write("404 Not Found");
            } catch (IOException e) {
                e.printStackTrace();
            }
            return;
        }
        
        // 2. 委派给具体的 Handler 处理
        try {
            // 这里简化处理，实际 Spring MVC 会调用 HandlerAdapter
            Method method = handler.getClass().getMethod("handle", 
                HttpServletRequest.class, HttpServletResponse.class);
            method.invoke(handler, req, resp);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}

/**
 * Controller 接口
 */
public interface Controller {
    void handle(HttpServletRequest req, HttpServletResponse resp);
}

/**
 * 用户控制器
 */
public class UserController implements Controller {
    @Override
    public void handle(HttpServletRequest req, HttpServletResponse resp) {
        System.out.println("处理用户请求");
    }
}
```

### 4.2 任务调度器

```java
/**
 * 任务接口
 */
public interface Task {
    void execute();
    String getType();
}

/**
 * 同步任务
 */
public class SyncTask implements Task {
    private String name;
    private Runnable runnable;
    
    public SyncTask(String name, Runnable runnable) {
        this.name = name;
        this.runnable = runnable;
    }
    
    @Override
    public void execute() {
        System.out.println("同步执行任务: " + name);
        runnable.run();
    }
    
    @Override
    public String getType() {
        return "sync";
    }
}

/**
 * 异步任务
 */
public class AsyncTask implements Task {
    private String name;
    private Runnable runnable;
    
    public AsyncTask(String name, Runnable runnable) {
        this.name = name;
        this.runnable = runnable;
    }
    
    @Override
    public void execute() {
        System.out.println("异步执行任务: " + name);
        new Thread(runnable).start();
    }
    
    @Override
    public String getType() {
        return "async";
    }
}

/**
 * 任务调度器（委派者）
 */
public class TaskScheduler {
    
    private Map<String, TaskExecutor> executors = new HashMap<>();
    
    public TaskScheduler() {
        executors.put("sync", new SyncTaskExecutor());
        executors.put("async", new AsyncTaskExecutor());
    }
    
    /**
     * 提交任务
     */
    public void submit(Task task) {
        TaskExecutor executor = executors.get(task.getType());
        if (executor != null) {
            System.out.println("调度器分配任务到: " + task.getType() + " 执行器");
            executor.execute(task);
        }
    }
}

/**
 * 任务执行器接口
 */
public interface TaskExecutor {
    void execute(Task task);
}

/**
 * 同步任务执行器
 */
public class SyncTaskExecutor implements TaskExecutor {
    @Override
    public void execute(Task task) {
        task.execute();
    }
}

/**
 * 异步任务执行器
 */
public class AsyncTaskExecutor implements TaskExecutor {
    private ExecutorService threadPool = Executors.newFixedThreadPool(5);
    
    @Override
    public void execute(Task task) {
        threadPool.submit(task::execute);
    }
}
```

### 4.3 消息路由器

```java
/**
 * 消息处理器接口
 */
public interface MessageHandler {
    boolean canHandle(Message message);
    void handle(Message message);
}

/**
 * 订单消息处理器
 */
public class OrderMessageHandler implements MessageHandler {
    @Override
    public boolean canHandle(Message message) {
        return "ORDER".equals(message.getType());
    }
    
    @Override
    public void handle(Message message) {
        System.out.println("处理订单消息: " + message.getContent());
    }
}

/**
 * 用户消息处理器
 */
public class UserMessageHandler implements MessageHandler {
    @Override
    public boolean canHandle(Message message) {
        return "USER".equals(message.getType());
    }
    
    @Override
    public void handle(Message message) {
        System.out.println("处理用户消息: " + message.getContent());
    }
}

/**
 * 通知消息处理器
 */
public class NotificationMessageHandler implements MessageHandler {
    @Override
    public boolean canHandle(Message message) {
        return "NOTIFICATION".equals(message.getType());
    }
    
    @Override
    public void handle(Message message) {
        System.out.println("处理通知消息: " + message.getContent());
    }
}

/**
 * 消息路由器（委派者）
 */
public class MessageRouter {
    
    private List<MessageHandler> handlers = new ArrayList<>();
    
    public MessageRouter() {
        handlers.add(new OrderMessageHandler());
        handlers.add(new UserMessageHandler());
        handlers.add(new NotificationMessageHandler());
    }
    
    /**
     * 路由消息
     */
    public void route(Message message) {
        for (MessageHandler handler : handlers) {
            if (handler.canHandle(message)) {
                System.out.println("路由消息到: " + handler.getClass().getSimpleName());
                handler.handle(message);
                return;
            }
        }
        System.out.println("没有找到合适的处理器: " + message.getType());
    }
    
    /**
     * 广播消息
     */
    public void broadcast(Message message) {
        for (MessageHandler handler : handlers) {
            if (handler.canHandle(message)) {
                handler.handle(message);
            }
        }
    }
}

/**
 * 消息
 */
@Data
public class Message {
    private String type;
    private String content;
    private Map<String, Object> headers;
}
```

### 4.4 负载均衡委派

```java
/**
 * 服务器接口
 */
public interface Server {
    void handleRequest(Request request);
    String getName();
    int getWeight();
    boolean isAvailable();
}

/**
 * 负载均衡策略接口
 */
public interface LoadBalanceStrategy {
    Server select(List<Server> servers);
}

/**
 * 轮询策略
 */
public class RoundRobinStrategy implements LoadBalanceStrategy {
    private AtomicInteger index = new AtomicInteger(0);
    
    @Override
    public Server select(List<Server> servers) {
        List<Server> available = servers.stream()
            .filter(Server::isAvailable)
            .collect(Collectors.toList());
        
        if (available.isEmpty()) {
            throw new RuntimeException("没有可用的服务器");
        }
        
        int i = index.getAndIncrement() % available.size();
        return available.get(i);
    }
}

/**
 * 随机策略
 */
public class RandomStrategy implements LoadBalanceStrategy {
    private Random random = new Random();
    
    @Override
    public Server select(List<Server> servers) {
        List<Server> available = servers.stream()
            .filter(Server::isAvailable)
            .collect(Collectors.toList());
        
        return available.get(random.nextInt(available.size()));
    }
}

/**
 * 加权轮询策略
 */
public class WeightedRoundRobinStrategy implements LoadBalanceStrategy {
    // 实现加权轮询逻辑
    @Override
    public Server select(List<Server> servers) {
        // 根据权重选择服务器
        return null;
    }
}

/**
 * 负载均衡器（委派者）
 */
public class LoadBalancer {
    
    private List<Server> servers = new ArrayList<>();
    private LoadBalanceStrategy strategy;
    
    public LoadBalancer(LoadBalanceStrategy strategy) {
        this.strategy = strategy;
    }
    
    public void addServer(Server server) {
        servers.add(server);
    }
    
    public void removeServer(Server server) {
        servers.remove(server);
    }
    
    /**
     * 分发请求
     */
    public void dispatch(Request request) {
        Server server = strategy.select(servers);
        System.out.println("委派请求到服务器: " + server.getName());
        server.handleRequest(request);
    }
}
```

## 五、委派模式在 Spring 中的应用

### 5.1 BeanDefinitionParserDelegate

```java
// Spring XML 解析中的委派
public class BeanDefinitionParserDelegate {
    
    public BeanDefinition parseCustomElement(Element ele) {
        // 获取命名空间
        String namespaceUri = getNamespaceURI(ele);
        
        // 获取对应的 NamespaceHandler
        NamespaceHandler handler = this.readerContext.getNamespaceHandlerResolver()
            .resolve(namespaceUri);
        
        // 委派给具体的 Handler 解析
        return handler.parse(ele, new ParserContext(this.readerContext, this, containingBd));
    }
}
```

### 5.2 ClassLoader 双亲委派

```java
/**
 * 类加载器的双亲委派模型
 */
public abstract class ClassLoader {
    
    private final ClassLoader parent;
    
    protected Class<?> loadClass(String name, boolean resolve) {
        synchronized (getClassLoadingLock(name)) {
            // 1. 检查是否已加载
            Class<?> c = findLoadedClass(name);
            
            if (c == null) {
                // 2. 委派给父类加载器
                if (parent != null) {
                    c = parent.loadClass(name, false);
                } else {
                    c = findBootstrapClassOrNull(name);
                }
                
                // 3. 父类加载不了，自己加载
                if (c == null) {
                    c = findClass(name);
                }
            }
            
            return c;
        }
    }
}
```

## 六、优缺点

### 优点
1. **简化调用**：客户端不需要知道具体执行者
2. **解耦**：任务分发与任务执行解耦
3. **扩展性好**：新增执行者无需修改委派者

### 缺点
1. **增加复杂度**：引入委派者增加系统层级
2. **调试困难**：调用链变长，调试较困难

## 七、面试常见问题

### Q1: 委派模式和代理模式的区别？
> 答：代理模式注重控制对目标对象的访问过程；委派模式注重任务分发，关注的是结果而非过程。

### Q2: 委派模式和策略模式的区别？
> 答：策略模式由客户端选择具体策略；委派模式由委派者内部决定使用哪个执行者，客户端不感知。

### Q3: Spring 中哪里用到了委派模式？
> 答：DispatcherServlet 分发请求、BeanDefinitionParserDelegate 解析 XML、ClassLoader 双亲委派等。
