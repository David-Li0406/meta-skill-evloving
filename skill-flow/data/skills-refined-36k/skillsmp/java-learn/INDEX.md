# Java 架构师学习资料索引

> 📚 本索引为 Java 架构师进阶学习提供完整的知识导航

---

## 目录总览

| 模块 | 文件数 | 核心内容 |
|------|--------|----------|
| [设计模式](#一设计模式-design-patterns) | 6 | 单例、工厂、策略、模板、代理、委派 |
| [Spring 生态](#二spring-生态-spring-learn) | 10 | Bean、AOP、MVC、IOC、事务、Boot、Netty |
| [Java 并发](#三java-并发-java-thread) | 6 | 线程基础、锁机制、线程池、并发容器 |
| [JVM 深入](#四jvm-深入-jvm) | 7 | 类加载、内存结构、GC、调优 |
| [MySQL 精通](#五mysql-精通-mysql) | 4 | 执行流程、索引、Explain、事务与锁 |

---

## 一、设计模式 (design-patterns)

### 📖 学习路径
```
01-Singleton → 02-Factory → 03-Strategy → 04-Template → 05-Proxy → 06-Delegate
```

### 📂 文件清单

| 序号 | 文件 | 内容概要 | 关键知识点 |
|------|------|----------|------------|
| 01 | [01-Singleton.md](./design-patterns/01-Singleton.md) | 单例模式 | 饿汉式、懒汉式、双重检查、枚举单例、Spring 应用 |
| 02 | [02-Factory.md](./design-patterns/02-Factory.md) | 工厂模式 | 简单工厂、工厂方法、抽象工厂、Spring BeanFactory |
| 03 | [03-Strategy.md](./design-patterns/03-Strategy.md) | 策略模式 | 策略接口、上下文、消除 if-else、支付/排序案例 |
| 04 | [04-Template.md](./design-patterns/04-Template.md) | 模板模式 | 模板方法、钩子方法、JdbcTemplate、AbstractList |
| 05 | [05-Proxy.md](./design-patterns/05-Proxy.md) | 代理模式 | 静态代理、JDK 动态代理、CGLIB、Spring AOP 原理 |
| 06 | [06-Delegate.md](./design-patterns/06-Delegate.md) | 委派模式 | 任务分发、DispatcherServlet、策略+委派组合 |

### 🎯 面试高频
- 单例模式有几种写法？各自优缺点？
- JDK 动态代理和 CGLIB 的区别？
- 策略模式如何消除 if-else？

---

## 二、Spring 生态 (spring-learn)

### 📖 学习路径
```
01-Bean → 02-Annotation → 03-AOP → 04-MVC → 05-IOC → 06-CircularDependency → 07-Transaction → 08-SpringBoot → 09-Netty → 10-Interview
```

### 📂 文件清单

| 序号 | 文件 | 内容概要 | 关键知识点 |
|------|------|----------|------------|
| 01 | [01-SpringBean.md](./spring-learn/01-SpringBean.md) | Bean 生命周期 | 实例化、属性填充、初始化、销毁、扩展点 |
| 02 | [02-SpringAnnotation.md](./spring-learn/02-SpringAnnotation.md) | 常用注解 | @Component、@Autowired、@Conditional、自定义注解 |
| 03 | [03-SpringAOP.md](./spring-learn/03-SpringAOP.md) | AOP 原理 | 切面、切点、通知、代理创建流程、源码分析 |
| 04 | [04-SpringMVC.md](./spring-learn/04-SpringMVC.md) | MVC 流程 | DispatcherServlet、HandlerMapping、ViewResolver |
| 05 | [05-SpringIOC.md](./spring-learn/05-SpringIOC.md) | IOC 容器 | BeanFactory、ApplicationContext、依赖注入 |
| 06 | [06-SpringCircularDependency.md](./spring-learn/06-SpringCircularDependency.md) | 循环依赖 | 三级缓存、getSingleton、提前暴露 |
| 07 | [07-SpringTransaction.md](./spring-learn/07-SpringTransaction.md) | 事务机制 | 传播行为、隔离级别、事务失效场景、源码分析 |
| 08 | [08-SpringBoot.md](./spring-learn/08-SpringBoot.md) | SpringBoot | 启动流程、自动装配、SPI 机制对比 |
| 09 | [09-Netty.md](./spring-learn/09-Netty.md) | Netty 网络 | 网络分层、TCP/UDP、Reactor 模型、源码分析 |
| 10 | [10-SpringInterview.md](./spring-learn/10-SpringInterview.md) | 面试汇总 | 高频面试题及详细答案 |

### 🎯 面试高频
- Spring Bean 的生命周期？
- Spring 如何解决循环依赖？三级缓存的作用？
- Spring 事务失效的场景有哪些？
- SpringBoot 自动装配原理？

---

## 三、Java 并发 (java-thread)

### 📖 学习路径
```
01-ThreadBasics → 02-Synchronized → 03-ThreadLocal → 04-ReentrantLock → 05-ConcurrentHashMap → 06-ThreadPool
```

### 📂 文件清单

| 序号 | 文件 | 内容概要 | 关键知识点 |
|------|------|----------|------------|
| 01 | [01-ThreadBasics.md](./java-thread/01-ThreadBasics.md) | 线程基础 | 生命周期、创建方式、启动停止、线程通信 |
| 02 | [02-Synchronized.md](./java-thread/02-Synchronized.md) | 同步机制 | synchronized、锁升级、volatile、Happens-Before |
| 03 | [03-ThreadLocal.md](./java-thread/03-ThreadLocal.md) | 线程本地 | 数据结构、Hash 冲突、弱引用、内存泄漏 |
| 04 | [04-ReentrantLock.md](./java-thread/04-ReentrantLock.md) | 重入锁 | AQS、公平/非公平锁、读写锁、Condition |
| 05 | [05-ConcurrentHashMap.md](./java-thread/05-ConcurrentHashMap.md) | 并发容器 | 数据结构、put/get 流程、扩容、size 计算 |
| 06 | [06-ThreadPool.md](./java-thread/06-ThreadPool.md) | 线程池 | 核心参数、执行流程、拒绝策略、源码分析 |

### 🎯 面试高频
- synchronized 锁升级过程？
- volatile 的作用和原理？
- ThreadLocal 为什么用弱引用？如何避免内存泄漏？
- 线程池的核心参数？如何合理配置？

---

## 四、JVM 深入 (jvm)

### 📖 学习路径
```
01-ClassLifecycle → 02-MemoryStructure → 03-GC_Algorithm → 04-GC_Collector → 05-JVM_Parameters → 06-JVM_Tools → 07-JVM_Tuning
```

### 📂 文件清单

| 序号 | 文件 | 内容概要 | 关键知识点 |
|------|------|----------|------------|
| 01 | [01-ClassLifecycle.md](./jvm/01-ClassLifecycle.md) | 类生命周期 | 加载、验证、准备、解析、初始化、卸载 |
| 02 | [02-MemoryStructure.md](./jvm/02-MemoryStructure.md) | 内存结构 | 程序计数器、栈、堆、方法区、OOM 案例 |
| 03 | [03-GC_Algorithm.md](./jvm/03-GC_Algorithm.md) | GC 算法 | 引用计数、可达性分析、标记清除/整理/复制 |
| 04 | [04-GC_Collector.md](./jvm/04-GC_Collector.md) | 垃圾收集器 | Serial、ParNew、CMS、G1、ZGC |
| 05 | [05-JVM_Parameters.md](./jvm/05-JVM_Parameters.md) | JVM 参数 | 标准参数、-X 参数、-XX 参数、常用配置 |
| 06 | [06-JVM_Tools.md](./jvm/06-JVM_Tools.md) | 命令与工具 | jps、jinfo、jstat、jstack、jmap、jconsole |
| 07 | [07-JVM_Tuning.md](./jvm/07-JVM_Tuning.md) | JVM 调优 | 调优步骤、生产案例、参数模板 |

### 🎯 面试高频
- JVM 内存结构？各区域存放什么？
- 如何判断对象可以被回收？
- CMS 和 G1 的区别？
- 生产环境 OOM 如何排查？

---

## 五、MySQL 精通 (mysql)

### 📖 学习路径
```
01-ExecutionFlow → 02-Index → 03-Explain → 04-Transaction_Lock
```

### 📂 文件清单

| 序号 | 文件 | 内容概要 | 关键知识点 |
|------|------|----------|------------|
| 01 | [01-ExecutionFlow.md](./mysql/01-ExecutionFlow.md) | 执行流程 | SQL 执行过程、Buffer Pool、Redo/Undo/Bin Log |
| 02 | [02-Index.md](./mysql/02-Index.md) | 索引原理 | Page 页、B+ 树、聚簇索引、二级索引、联合索引 |
| 03 | [03-Explain.md](./mysql/03-Explain.md) | 执行计划 | Explain 各字段含义、type 类型、优化建议 |
| 04 | [04-Transaction_Lock.md](./mysql/04-Transaction_Lock.md) | 事务与锁 | ACID、隔离级别、MVCC、LBCC、死锁分析 |

### 🎯 面试高频
- 一条 SQL 的执行流程？
- 聚簇索引和非聚簇索引的区别？
- MVCC 如何实现？
- 什么情况下会产生死锁？如何避免？

---

## 六、知识图谱

```
                                    ┌─────────────────────────────────────┐
                                    │           Java 架构师               │
                                    └─────────────────────────────────────┘
                                                    │
                ┌───────────────┬───────────────┬───┴───┬───────────────┬───────────────┐
                │               │               │       │               │               │
                ▼               ▼               ▼       ▼               ▼               ▼
        ┌───────────┐   ┌───────────┐   ┌───────────┐  ┌───────────┐   ┌───────────┐
        │  设计模式  │   │   Spring  │   │  并发编程  │  │    JVM    │   │   MySQL   │
        └───────────┘   └───────────┘   └───────────┘  └───────────┘   └───────────┘
              │               │               │              │               │
              │               │               │              │               │
     ┌────────┴────────┐     │        ┌──────┴──────┐      │        ┌──────┴──────┐
     │                 │     │        │             │      │        │             │
  创建型           结构型    │     线程基础      锁机制    │      索引         事务
  单例/工厂       代理/委派   │    生命周期     synchronized│    B+树       ACID/隔离级别
                            │    创建方式     ReentrantLock│   聚簇/二级    MVCC/LBCC
                            │                              │
                      ┌─────┴─────┐                 ┌──────┴──────┐
                      │           │                 │             │
                   IOC/DI       AOP              内存结构        GC
                  Bean生命周期  代理创建          堆/栈/方法区    算法/收集器
                  循环依赖     切面/切点          OOM分析        调优
```

---

## 七、学习建议

### 📅 学习顺序建议

**第一阶段（2-3 周）：基础夯实**
1. 设计模式：重点掌握单例、工厂、代理
2. Java 并发：线程基础 → synchronized → 线程池

**第二阶段（3-4 周）：框架深入**
1. Spring 核心：Bean 生命周期 → IOC → AOP → 循环依赖
2. SpringBoot：启动流程 → 自动装配

**第三阶段（2-3 周）：JVM 精通**
1. 内存结构 → GC 算法 → 垃圾收集器
2. JVM 参数 → 调优实战

**第四阶段（2 周）：MySQL 进阶**
1. 索引原理 → Explain 分析
2. 事务与锁 → MVCC/LBCC

### 📝 学习方法

1. **理论 + 实践**：每个知识点都要写代码验证
2. **源码阅读**：Spring、JDK 源码是最好的老师
3. **总结输出**：用自己的话复述知识点
4. **面试驱动**：带着面试问题去学习

---

## 八、快速导航

### 按难度分类

| 难度 | 内容 |
|------|------|
| ⭐ 入门 | 线程基础、设计模式基础、JVM 内存结构 |
| ⭐⭐ 进阶 | Spring Bean、ThreadLocal、索引原理 |
| ⭐⭐⭐ 高级 | 循环依赖、ReentrantLock 源码、CMS/G1 |
| ⭐⭐⭐⭐ 专家 | JVM 调优实战、MVCC/LBCC、Netty 源码 |

### 按场景分类

| 场景 | 推荐阅读 |
|------|----------|
| 面试准备 | 各模块面试题 + INDEX 中的高频考点 |
| 排查 OOM | JVM 内存结构 → JVM 工具 → JVM 调优 |
| SQL 优化 | 索引原理 → Explain → 事务与锁 |
| Spring 问题 | 循环依赖 → 事务失效 → AOP 不生效 |

---

> 💡 **持续更新中**：本学习资料会不断完善和补充，欢迎提出建议！
