---
name: jvm
description: JVM 学习资料（原理 + 排错 + 调优）
---

# JVM 学习资料

> 目标：能解释 JVM 关键机制、能定位常见问题（OOM/死锁/CPU 飙高）、能做基础调优。

## 1. Class 文件与类加载
### 1.1 Class 文件结构（知道有什么）
- 魔数、版本号、常量池、字段表、方法表、属性表
- 常量池：符号引用 → 解析后变直接引用

### 1.2 类加载过程
- Loading（加载）→ Linking（验证/准备/解析）→ Initialization（初始化）
- 初始化触发：
  - `new`、访问静态字段/方法、反射、main 启动、子类初始化触发父类

### 1.3 类加载器
- Bootstrap / Platform / Application
- 双亲委派：避免核心类被篡改，避免重复加载
- 破坏双亲委派：SPI、Tomcat、OSGi（“隔离”需求）

---

## 2. 运行时数据区（内存结构）
### 2.1 线程私有
- 程序计数器（PC）
- 虚拟机栈（Stack Frame：局部变量表、操作数栈、动态链接、返回地址）
- 本地方法栈

### 2.2 线程共享
- 堆（Heap）：对象实例与数组
- 方法区（Method Area）：类元数据、常量、静态变量、JIT 代码缓存（JDK8 后元空间 Metaspace 在本地内存）

### 2.3 常见 OOM
- `Java heap space`
- `GC overhead limit exceeded`
- `Metaspace`
- `Direct buffer memory`
- `unable to create new native thread`

---

## 3. 对象与引用
### 3.1 对象创建大致流程
- 类已加载检查 → 分配内存（TLAB/指针碰撞/空闲列表）→ 设置对象头 → 执行 `<init>`

### 3.2 对象内存布局（概念级）
- 对象头（Mark Word + Klass Pointer）
- 实例数据
- 对齐填充

### 3.3 四种引用
- 强引用 / 软引用 / 弱引用 / 虚引用
- ThreadLocal 泄漏：key 弱引用 + value 强引用，线程池场景要主动 remove

---

## 4. GC 基础
### 4.1 如何判定垃圾
- 引用计数（缺点：循环引用）
- 可达性分析（GC Roots）

### 4.2 常见算法
- 标记清除（碎片）
- 标记整理（停顿较长）
- 复制算法（空间换时间）
- 分代收集：新生代 Minor GC，老年代 Major/Full GC

### 4.3 常见收集器（以 HotSpot 为主）
- Serial / Parallel / CMS / G1（以及 ZGC/Shenandoah 了解即可）
- CMS：并发标记清除，问题：碎片、浮动垃圾、并发失败
- G1：Region + Remembered Set，目标是可预测停顿

---

## 5. JVM 参数速查
### 5.1 查看参数
- `java -XX:+PrintCommandLineFlags -version`

### 5.2 常用参数（示例）
- 堆：`-Xms -Xmx -Xmn`
- 元空间：`-XX:MaxMetaspaceSize`
- GC 日志（JDK9+）：`-Xlog:gc*:file=gc.log:time,uptime,level,tags`

---

## 6. 排错工具链（必会）
- `jps`：查看进程
- `jstack`：线程栈（死锁、阻塞、热点线程）
- `jmap -histo`：对象直方图
- `jmap -dump:format=b,file=heap.hprof <pid>`：堆 dump
- `jstat -gc <pid> <interval>`：GC 指标
- `jcmd <pid> VM.native_memory summary`：本地内存（NMT）

---

## 7. 典型问题：OOM 处理流程
1. 先区分：堆/元空间/直接内存/线程数
2. 采集：GC 日志 + heap dump + 线程栈（必要时）
3. 分析：
   - MAT/IDEA Analyze Dump：看 dominator tree / retained size
   - 是否缓存未淘汰、集合无限增长、ThreadLocal 未清理
4. 修复：
   - 代码：释放引用、限流/分页、缓存策略
   - 参数：合理堆大小、G1 参数、直接内存上限

---

## 8. 可运行示例代码索引（对应 src/main/java）
- `com.example.jvm.GcLogDemo`：制造 GC 压力（仅演示）
- `com.example.jvm.OomHeapDemo`：堆 OOM（仅演示，慎跑）
- `com.example.jvm.ClassLoaderDemo`：类加载器与双亲委派示意

---

## 9. 高频面试题
1. 双亲委派是什么？为什么要它？哪些场景会打破？
2. 新生代/老年代为什么要分代？
3. CMS vs G1 的核心区别？各自问题是什么？
4. OOM 你怎么排查？需要哪些现场信息？
