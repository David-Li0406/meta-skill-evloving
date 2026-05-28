---
name: spring-learn
description: Spring 学习（IOC/AOP/事务/Boot）
---

# Spring 学习资料

> 目标：能解释 Spring 的“为什么这么设计”，并能解决常见生产问题：循环依赖、事务失效、AOP 不生效、Bean 冲突。

## 1. Spring 核心心智模型
- IOC：对象创建与依赖装配交给容器
- DI：依赖注入（构造器/Setter/字段）
- AOP：横切关注点（事务、鉴权、日志、监控）

---

## 2. Bean 生命周期（必会）
### 2.1 关键阶段
1. 实例化（反射/工厂方法）
2. 属性填充（依赖注入）
3. Aware 回调（BeanNameAware 等）
4. BeanPostProcessor 前置
5. 初始化（@PostConstruct / InitializingBean / init-method）
6. BeanPostProcessor 后置（AOP 代理通常在这里生成）
7. 销毁（@PreDestroy / DisposableBean / destroy-method）

### 2.2 扩展点
- BeanFactoryPostProcessor：修改 BeanDefinition（早于实例化）
- BeanPostProcessor：干预 Bean 创建（AOP、注解解析）

---

## 3. IOC/DI：容器与注入
### 3.1 BeanFactory vs ApplicationContext
- BeanFactory：基础能力
- ApplicationContext：国际化、事件、资源加载、更多自动化

### 3.2 常用注入方式与建议
- 推荐：构造器注入（不可变、可测试、避免 NPE）
- 避免：大量字段注入（不好测）

### 3.3 Bean 冲突与装配
- `@Primary` / `@Qualifier` / `@Resource(name=...)`
- 条件化：`@Conditional`/`@Profile`

---

## 4. AOP：原理与坑
### 4.1 核心概念
- 切面（Aspect）、切点（Pointcut）、通知（Advice）
- 代理：JDK 动态代理（接口）/ CGLIB（子类）

### 4.2 事务/AOP 不生效的常见原因
- 同类方法自调用（绕过代理）
- 方法不是 public（默认代理策略下）
- final 类/方法（CGLIB 受限）
- Bean 没有被 Spring 管理

---

## 5. 循环依赖：三级缓存
### 5.1 三级缓存是什么
- 一级：singletonObjects（完整单例）
- 二级：earlySingletonObjects（早期引用）
- 三级：singletonFactories（ObjectFactory，用于提前暴露代理）

### 5.2 能解决/不能解决
- 能解决：单例 + setter 注入的循环依赖
- 不能：构造器循环依赖；prototype 循环依赖

---

## 6. 事务：传播与隔离
### 6.1 传播行为（常问）
- REQUIRED（默认）
- REQUIRES_NEW
- NESTED

### 6.2 事务失效典型场景
- 异常被吞掉/捕获后不抛出
- 抛出异常不是 RuntimeException（未配置 rollbackFor）
- 自调用

---

## 7. Spring Boot：自动装配
- `@SpringBootApplication` = `@Configuration + @EnableAutoConfiguration + @ComponentScan`
- 自动装配入口：`spring.factories`（老）/ `META-INF/spring/org.springframework.boot.autoconfigure.AutoConfiguration.imports`（新）
- 条件注解：`@ConditionalOnClass`/`@ConditionalOnMissingBean` 等

---

## 8. 可运行示例代码索引（对应 src/main/java）
- `com.example.spring.BeanLifecycleMiniDemo`（新增：简化版生命周期演示，不依赖 Spring 也可阅读）
- 如果你希望我加 Spring Boot 工程示例，需要新增 pom 与依赖（你确认我再加）。

---

## 9. 高频面试题
1. Bean 生命周期详细流程？BPP 与 BFPP 的区别？
2. AOP 代理什么时候生成？JDK vs CGLIB 选型？
3. 三级缓存分别解决什么问题？为什么要第三级？
4. 事务传播行为有哪些？REQUIRES_NEW 与 NESTED 区别？
5. 事务为什么会失效？如何规避自调用？
