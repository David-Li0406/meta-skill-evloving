---
name: design-patterns
description: 设计模式（结合 Java & Spring 实战）
---

# 设计模式学习资料

> 目标：不背“定义”，而是能在代码里识别与落地：解耦、可扩展、可测试。

## 1. 设计原则（先于模式）
- 单一职责：变化原因尽量只有一个
- 开闭原则：对扩展开放，对修改关闭（多用组合/多态）
- 里氏替换：子类必须能替换父类
- 接口隔离：不要强迫实现用不到的方法
- 依赖倒置：依赖抽象，不依赖实现

---

## 2. 创建型模式
### 2.1 单例（Singleton）
- 常见写法：饿汉、DCL、静态内部类、枚举
- 推荐：枚举（最安全）；或静态内部类（懒加载且线程安全）
- 常见坑：反射破坏、序列化破坏、多 ClassLoader 多实例

### 2.2 工厂（Factory）
- 简单工厂：一处集中创建（但易变成 if-else 地狱）
- 工厂方法：把创建延迟到子类
- 抽象工厂：产品族
- Spring 对应：BeanFactory / FactoryBean

### 2.3 建造者（Builder）
- 解决“构造参数爆炸”
- Java 实战：不可变对象 + builder；或 Lombok @Builder

---

## 3. 结构型模式
### 3.1 代理（Proxy）
- 静态代理：手写包装
- JDK 动态代理：基于接口
- CGLIB：基于继承（final 类/方法受限）
- Spring AOP：默认 JDK 代理，必要时 CGLIB

### 3.2 装饰器（Decorator）
- 在不修改原类的基础上增强功能
- Java 实战：`InputStream`/`BufferedInputStream`

### 3.3 适配器（Adapter）
- 兼容旧接口/第三方接口
- Spring 实战：HandlerAdapter

---

## 4. 行为型模式
### 4.1 策略（Strategy）
- 用多态消灭 if-else
- 实战：支付策略、优惠策略、路由策略

### 4.2 模板方法（Template Method）
- 固定流程 + 可变步骤
- Spring 实战：JdbcTemplate

### 4.3 责任链（Chain of Responsibility）
- 一组处理器按顺序处理
- Spring 实战：Filter、Interceptor、Spring Security

### 4.4 观察者（Observer）
- 事件驱动
- Spring 实战：ApplicationEventPublisher

---

## 5. 可运行示例代码索引（对应 src/main/java）
- `com.example.designpatterns.strategy.StrategyPatternDemo`（仓库已有）
- `com.example.designpatterns.template.TemplateMethodDemo`（仓库已有）
- `com.example.designpatterns.proxy.ProxyPatternDemo`（仓库已有）
- `com.example.designpatterns.factory.SimpleFactoryDemo`（仓库已有）
- 新增：`com.example.designpatterns.decorator.DecoratorDemo`
- 新增：`com.example.designpatterns.chain.ChainOfResponsibilityDemo`

---

## 6. 高频面试题
1. 什么时候用组合替代继承？
2. JDK 动态代理与 CGLIB 的差异与选型？
3. 策略模式如何避免 if-else？策略如何注册（Map/SPI/Spring 注入）？
4. 责任链的优缺点是什么？如何避免“链条过长难排查”？
