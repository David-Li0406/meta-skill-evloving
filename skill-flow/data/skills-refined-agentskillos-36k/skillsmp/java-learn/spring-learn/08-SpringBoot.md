# Spring Boot 架构深入与源码分析

## 一、自动装配 (Auto Configuration) 原理

### 1.1 核心注解 `@SpringBootApplication`
这是一个组合注解，核心包含三个：
1.  `@SpringBootConfiguration`: 标识这是一个配置类。
2.  `@ComponentScan`: 扫描当前包及其子包下的 Bean。
3.  `@EnableAutoConfiguration`: **自动装配的核心**。

### 1.2 `@EnableAutoConfiguration` 源码解析
该注解通过 `@Import(AutoConfigurationImportSelector.class)` 导入选择器。

#### 执行流程：
1.  **加载配置**: `AutoConfigurationImportSelector` 会通过 `SpringFactoriesLoader` 加载 `META-INF/spring.factories` (2.7 以前) 或 `META-INF/spring/org.springframework.boot.autoconfigure.AutoConfiguration.imports` (2.7 以后) 文件。
2.  **筛选配置**: 读取到所有可能的 AutoConfiguration 类（如 `RedisAutoConfiguration`, `JdbcTemplateAutoConfiguration` 等）。
3.  **条件过滤 (`@Conditional`)**: 并不是所有加载的类都会生效。Spring Boot 使用 `@ConditionalOnClass`, `@ConditionalOnMissingBean`, `@ConditionalOnProperty` 等注解进行过滤。
    *   *例如*: `RedisAutoConfiguration` 只有在 classpath 下存在 `RedisOperations` 类时才会生效。

### 1.3 手写自定义 Starter
架构师必须掌握如何封装通用的 Starter 给业务团队使用。

#### 1.3.1 项目结构
*   `my-common-starter` (Maven 项目)

#### 1.3.2 编写业务服务类
```java
public class MySmsService {
    private String apiKey;
    private String apiSecret;

    public MySmsService(String apiKey, String apiSecret) {
        this.apiKey = apiKey;
        this.apiSecret = apiSecret;
    }

    public void send(String phone, String content) {
        System.out.printf("使用 Key=[%s] 发送短信给 [%s]: %s%n", apiKey, phone, content);
    }
}
```

#### 1.3.3 编写配置属性类 (`@ConfigurationProperties`)
```java
@ConfigurationProperties(prefix = "my.sms")
public class MySmsProperties {
    private String apiKey;
    private String apiSecret;
    private boolean enable = true;
    // getters & setters
}
```

#### 1.3.4 编写自动配置类
```java
@Configuration
@EnableConfigurationProperties(MySmsProperties.class)
@ConditionalOnProperty(prefix = "my.sms", name = "enable", havingValue = "true", matchIfMissing = true)
public class MySmsAutoConfiguration {

    @Bean
    @ConditionalOnMissingBean
    public MySmsService mySmsService(MySmsProperties properties) {
        return new MySmsService(properties.getApiKey(), properties.getApiSecret());
    }
}
```

#### 1.3.5 注册自动配置
在 `src/main/resources/META-INF/spring/org.springframework.boot.autoconfigure.AutoConfiguration.imports` 文件中添加：
```text
com.example.starter.MySmsAutoConfiguration
```

## 二、Spring Boot 启动流程深度剖析

`SpringApplication.run(App.class, args)` 究竟做了什么？

### 2.1 核心步骤图解
1.  **构造 SpringApplication 对象**:
    *   推断应用类型 (Servlet? Reactive? None?)。
    *   加载所有的 `ApplicationContextInitializer`。
    *   加载所有的 `ApplicationListener`。
    *   推断 main 方法所在的类。
2.  **执行 run() 方法**:
    *   **准备 Environment**: 加载 `application.yml`，读取系统变量、环境变量。
    *   **创建 ApplicationContext**: 根据类型创建容器 (如 `AnnotationConfigServletWebServerApplicationContext`)。
    *   **准备 Context (prepareContext)**: 执行 Initializer，通过 BeanDefinitionLoader 加载启动类 Bean。
    *   **刷新 Context (refreshContext)**: **这是 Spring IOC 的核心**，扫描 Bean，执行自动装配，启动 Tomcat (如果是 Web 应用)。
    *   **运行 Runners**: 执行所有的 `CommandLineRunner` 和 `ApplicationRunner`。

### 2.2 Tomcat 是如何启动的？
在 `onRefresh()` 阶段，Servlet Web 容器会调用 `createWebServer()`。
*   Spring Boot 默认使用内嵌的 Tomcat。
*   它不依赖外部 `web.xml`，而是通过代码方式配置 Servlet、Filter。

## 三、生产环境优化与运维

### 3.1 优雅停机 (Graceful Shutdown)
防止 kill -9 导致正在处理的请求中断。
```yaml
server:
  shutdown: graceful # 开启优雅停机
spring:
  lifecycle:
    timeout-per-shutdown-phase: 30s # 最长等待时间
```

### 3.2 Actuator 监控
暴露 `/actuator/health`, `/actuator/metrics`, `/actuator/prometheus` 端点，配合 Prometheus + Grafana 搭建监控体系。

### 3.3 配置文件加载顺序
1.  命令行参数 (`--server.port=8080`)
2.  JVM 系统属性 (`-Dserver.port=8080`)
3.  环境变量
4.  jar 包外部的 `application-{profile}.yml`
5.  jar 包内部的 `application-{profile}.yml`
6.  jar 包外部的 `application.yml`
7.  jar 包内部的 `application.yml`
*   **原则**: 外部优先于内部，Profile 优先于默认。
