---
name: java-basics
description: Java 基础与进阶核心
---

# Java 学习资料（基础到进阶）

> 目标：用“可运行代码 + 关键概念 + 常见坑 + 面试提问”的方式，把 Java 基础打牢。

## 0. 学习建议（强烈推荐的顺序）
1. 语法与类型系统 → 面向对象 → 集合/泛型 → 异常/日志
2. I/O（NIO 优先理解模型）→ 反射/注解 → JVM/并发
3. 每个知识点：先写 demo 跑通，再解释原理，再归纳坑。

---

## 1. 开发环境与项目结构
### 1.1 JDK/IDE
- 推荐：JDK 17（或至少 8），IDEA
- 关键命令：
  - `java -version`
  - `javac -version`

### 1.2 Maven/Gradle（知道它解决什么）
- 依赖管理：解决“jar 冲突、传递依赖、版本统一”
- 构建：编译、测试、打包
- 常见坑：
  - `dependencyManagement` 只管版本不引入
  - 同一个类多版本（ClassPath 冲突）导致诡异问题

---

## 2. 基础语法与类型系统
### 2.1 基本类型 vs 引用类型
- 基本类型：`byte/short/int/long/float/double/char/boolean`
- 引用类型：对象、数组、String
- 关键点：
  - Java 只有值传递（pass-by-value）。对象引用也是“引用值”的拷贝。

### 2.2 自动装箱/拆箱
- `Integer a = 1;` 自动装箱
- `int b = a;` 自动拆箱
- 常见坑：
  - `Integer` 的缓存：`[-128, 127]`
  - `==` 比较引用地址，`equals` 比较值（多数包装类重写 equals）

### 2.3 String 与字符串拼接
- String 不可变：拼接多用 `StringBuilder`
- 常见坑：
  - `"a" + i` 在循环里可能产生大量对象
  - `intern()` 影响常量池（面试常问）

---

## 3. 面向对象（OOP）
### 3.1 核心概念
- 封装：隐藏实现细节
- 继承：复用 + 多态基础
- 多态：编译看左边，运行看右边（动态绑定）

### 3.2 重载 vs 重写
- 重载（Overload）：同名不同参，编译期决定
- 重写（Override）：子类覆盖父类方法，运行期决定

### 3.3 equals/hashCode 合同
- 规则：相等对象必须有相同 hashCode
- 用途：HashMap/HashSet 的正确性

---

## 4. 集合框架（Collections）
### 4.1 List
- `ArrayList`：动态数组，随机访问快；插入删除中间慢
- `LinkedList`：链表，插入删除快；随机访问慢

### 4.2 Set
- `HashSet`：基于 HashMap，无序
- `TreeSet`：红黑树，有序，要求可比较

### 4.3 Map
- `HashMap`：JDK8 之后“数组 + 链表/红黑树”
- `ConcurrentHashMap`：并发版，分段/桶级锁 + CAS（JDK8）
- 常见坑：
  - HashMap 允许 `null` key/value；CHM 不允许 `null`
  - key 可变会导致找不回（hashCode 变化）

---

## 5. 泛型（Generics）
### 5.1 为什么要泛型
- 编译期类型安全
- 减少强制类型转换

### 5.2 类型擦除
- 运行期几乎没有泛型信息
- 常见限制：
  - `new T()` 不行
  - `T.class` 不行

### 5.3 通配符
- `? extends T`：上界，读多写少
- `? super T`：下界，写多读少

---

## 6. 异常体系与最佳实践
### 6.1 体系
- `Throwable` → `Error`（不可恢复）/ `Exception`
- `Exception` → `RuntimeException`（非受检）/ checked exception

### 6.2 最佳实践
- 业务异常：自定义 `RuntimeException` + 错误码
- 不要吞异常：至少记录日志 + 关键信息

---

## 7. I/O 与 NIO（必须理解“模型”）
### 7.1 BIO/NIO/AIO
- BIO：阻塞式，每连接一线程（扩展差）
- NIO：非阻塞 + 多路复用（Selector）
- AIO：异步回调（Linux 下实现不如 NIO 常用）

### 7.2 常见面试
- select/poll/epoll 区别
- Reactor 模型是什么（Netty 基础）

---

## 8. 反射与注解
### 8.1 反射用途
- 框架：Spring、MyBatis、序列化
- 核心类：`Class`、`Method`、`Field`

### 8.2 注解与元注解
- `@Retention`、`@Target`、`@Inherited`、`@Repeatable`

---

## 9. 常用工具类与编码规范
- `Objects.requireNonNull`
- `Optional`：别滥用；避免 `Optional.get()`
- 时间：优先 `java.time`（LocalDateTime、Instant）
- 日志：slf4j 门面

---

## 10. 可运行示例代码索引（对应 src/main/java）
- `com.example.basics.EqualsHashCodeDemo`
- `com.example.basics.GenericsDemo`
- `com.example.basics.ReflectionAnnotationDemo`
- `com.example.basics.IODemo`

---

## 11. 高频面试题（带提示）
1. Java 为什么是值传递？对象怎么传？
2. `==` 和 `equals()` 的区别？为什么要重写 hashCode？
3. HashMap 在 JDK8 做了哪些优化？为什么要树化？
4. 泛型为什么要类型擦除？`? extends` 和 `? super` 怎么选？
5. 反射为什么慢？能做哪些优化（缓存、MethodHandle）？
