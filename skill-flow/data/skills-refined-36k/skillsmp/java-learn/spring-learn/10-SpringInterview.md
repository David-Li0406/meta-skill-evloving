# Spring 常见面试题精选

## 一、基础概念篇

### 1. Spring 是什么？有哪些核心模块？
**答**：
Spring 是一个开源的 Java 企业级应用开发框架，主要目的是简化企业级应用开发。
**核心模块**：
- **Spring Core**：IoC容器，BeanFactory
- **Spring Context**：ApplicationContext，提供国际化、事件传播等
- **Spring AOP**：面向切面编程
- **Spring DAO/JDBC**：数据库访问
- **Spring ORM**：集成Hibernate、MyBatis
- **Spring Web**：Web开发支持
- **Spring MVC**：Web MVC框架

### 2. 什么是 IoC 和 DI？
**答**：
- **IoC（Inversion of Control，控制反转）**：将对象的创建、初始化、销毁等生命周期管理交给容器，而不是由开发者在代码中手动new。
- **DI（Dependency Injection，依赖注入）**：IoC的具体实现方式。容器在运行期间动态地将依赖对象注入到组件中。

### 3. BeanFactory 和 ApplicationContext 有什么区别？
**答**：
| 特性 | BeanFactory | ApplicationContext |
|------|-------------|-------------------|
| 初始化 | 懒加载（Lazy Load） | 预加载（Pre-load） |
| 功能 | 基础IoC功能 | 扩展功能（AOP、Web、国际化） |
| 性能 | 启动快，内存占用小 | 启动慢，内存占用大 |
| 适用场景 | 移动设备、Applet | 企业级Web应用 |

### 4. Spring Bean 的生命周期？
**答**：
1. **实例化**：createBeanInstance
2. **属性赋值**：populateBean
3. **初始化前**：postProcessBeforeInitialization (BeanPostProcessor)
4. **初始化**：invokeInitMethods (InitializingBean/init-method)
5. **初始化后**：postProcessAfterInitialization (BeanPostProcessor/AOP代理)
6. **使用**
7. **销毁**：DisposableBean/destroy-method

### 5. Spring 中的单例 Bean 是线程安全的吗？
**答**：
**不是**。Spring 容器本身不保证 Bean 的线程安全。
- 如果 Bean 是无状态的（如 Service、Dao），通常是线程安全的。
- 如果 Bean 有状态（定义了实例变量），在并发环境下是不安全的。
**解决方案**：
- 将 Scope 设置为 prototype
- 使用 ThreadLocal
- 使用同步锁

---

## 二、高级特性篇

### 6. Spring AOP 的实现原理？
**答**：
Spring AOP 基于动态代理实现：
1. **JDK 动态代理**：
   - 目标对象必须实现接口
   - 基于 `Proxy.newProxyInstance` 生成代理类
   - 效率较高（JDK 8+）
2. **CGLIB 动态代理**：
   - 目标对象没有实现接口
   - 基于 ASM 字节码技术生成子类
   - 这里的"子类"指生成的代理类继承被代理类
   - final 类/方法无法代理

### 7. Spring 事务失效的场景？
**答**：
1. **方法修饰符不对**：必须是 public
2. **同类内部调用**：this.method() 不会经过代理
3. **异常未抛出**：被 catch 吞掉了
4. **异常类型不匹配**：默认只回滚 RuntimeException
5. **数据库不支持事务**：如 MyISAM 引擎
6. **Bean 未被 Spring 管理**
7. **事务传播机制配置错误**：如 propagation=NOT_SUPPORTED

### 8. Spring 如何解决循环依赖？
**答**：
通过**三级缓存**解决（仅限于单例 Setter 注入）：
1. **singletonObjects**（一级缓存）：存放完全初始化好的 Bean
2. **earlySingletonObjects**（二级缓存）：存放原始 Bean（或代理对象），未填充属性
3. **singletonFactories**（三级缓存）：存放 Bean 工厂（ObjectFactory），用于生成代理对象

**流程**：
A 依赖 B → 创建 A → A 放入三级缓存 → 注入 B → 创建 B → B 依赖 A → 从三级缓存获取 A → A 移入二级缓存 → B 初始化完成 → A 初始化完成

### 9. @Autowired 和 @Resource 的区别？
**答**：
| 特性 | @Autowired | @Resource |
|------|------------|-----------|
| 来源 | Spring 注解 | Java 标准注解 (JSR-250) |
| 注入方式 | 默认按类型 (byType) | 默认按名称 (byName) |
| 属性 | required=true/false | name, type |
| 配合注解 | @Qualifier 指定名称 | 无需配合 |

---

## 三、Spring Boot 篇

### 10. Spring Boot 自动装配原理？
**答**：
核心注解 `@SpringBootApplication` = `@Configuration` + `@EnableAutoConfiguration` + `@ComponentScan`
1. `@EnableAutoConfiguration` 引入 `AutoConfigurationImportSelector`
2. 读取 `META-INF/spring.factories` (Spring 2.x) 或 `META-INF/spring/org.springframework.boot.autoconfigure.AutoConfiguration.imports` (Spring 3.x)
3. 加载所有自动配置类 `xxxAutoConfiguration`
4. 通过 `@Conditional` 注解判断是否生效（如 `@ConditionalOnClass`）

### 11. Spring Boot 启动流程？
**答**：
1. 创建 `SpringApplication` 对象
2. `run()` 方法启动
3. 获取并启动监听器 `SpringApplicationRunListeners`
4. 准备环境 `prepareEnvironment`
5. 创建上下文 `createApplicationContext`
6. 准备上下文 `prepareContext`
7. 刷新上下文 `refreshContext` (IoC容器初始化)
8. 调用 Runners (`ApplicationRunner`, `CommandLineRunner`)

---

## 四、Spring MVC 篇

### 12. Spring MVC 执行流程？
**答**：
1. 用户请求发送到 **DispatcherServlet**
2. DispatcherServlet 请求 **HandlerMapping** 查找 Handler
3. HandlerMapping 返回 **HandlerExecutionChain** (Handler + Interceptors)
4. DispatcherServlet 请求 **HandlerAdapter** 执行 Handler
5. Handler 执行业务逻辑，返回 **ModelAndView**
6. HandlerAdapter 返回 ModelAndView 给 DispatcherServlet
7. DispatcherServlet 请求 **ViewResolver** 解析视图
8. ViewResolver 返回 **View** 对象
9. DispatcherServlet 渲染视图并响应用户

### 13. Spring MVC 常用注解？
**答**：
- `@Controller` / `@RestController`
- `@RequestMapping` / `@GetMapping` / `@PostMapping`
- `@RequestParam` / `@PathVariable`
- `@RequestBody` / `@ResponseBody`
- `@ModelAttribute`
- `@ControllerAdvice` / `@ExceptionHandler` (全局异常处理)

---

## 五、实战场景篇

### 14. 多个 AOP 切面的执行顺序如何控制？
**答**：
- 使用 `@Order` 注解
- 实现 `Ordered` 接口
- 值越小，优先级越高，越先执行（在 Before 阶段）

### 15. 如何在 Spring Bean 初始化完成后执行代码？
**答**：
1. 实现 `InitializingBean` 接口 (`afterPropertiesSet`)
2. 使用 `@PostConstruct` 注解
3. 配置 `init-method`
4. 实现 `ApplicationListener<ContextRefreshedEvent>`
5. 实现 `CommandLineRunner` / `ApplicationRunner` (Spring Boot)

### 16. Spring 事务传播机制有哪些？
**答**：
- **REQUIRED** (默认)：有则加入，无则新建
- **REQUIRES_NEW**：新建事务，挂起当前事务
- **SUPPORTS**：有则加入，无则非事务运行
- **NOT_SUPPORTED**：非事务运行，挂起当前事务
- **MANDATORY**：必须有事务，否则抛异常
- **NEVER**：必须无事务，否则抛异常
- **NESTED**：嵌套事务（Savepoint）

### 17. Spring 如何处理高并发请求？
**答**：
Spring MVC 的 Controller 默认是单例的，通过多线程处理请求。
Tomcat 线程池维护工作线程，每个请求分配一个线程。
**注意事项**：
- Controller 中不要定义成员变量（状态）
- 如果必须有状态，使用 `ThreadLocal` 或 `request` 作用域
- 使用异步处理 `Callable` / `DeferredResult` / `WebFlux`
