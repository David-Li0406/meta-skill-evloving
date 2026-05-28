# JVM Tools (常用工具)

JDK 提供了丰富的命令行工具和可视化工具，用于监控和故障排查。

## 一、命令行工具

这些工具通常位于 JDK 的 `bin` 目录下。

### 1. jps (JVM Process Status Tool)
- **作用**：列出正在运行的虚拟机进程，并显示虚拟机执行主类（Main Class, main() 函数所在的类）名称以及这些进程的本地虚拟机唯一 ID (LVMID, Local Virtual Machine Identifier)。
- **常用命令**：
    - `jps`：显示进程 ID 和类名。
    - `jps -l`：输出主类的全名，如果进程执行的是 Jar 包，则输出 Jar 路径。
    - `jps -v`：输出虚拟机进程启动时 JVM 参数。

### 2. jstat (JVM Statistics Monitoring Tool)
- **作用**：用于监视虚拟机各种运行状态信息。可以显示类加载、内存、垃圾收集、JIT 编译等运行数据。
- **格式**：`jstat [option vmid [interval[s|ms] [count]] ]`
- **常用命令**：
    - `jstat -gc <pid> 1000 10`：每隔 1000ms 打印一次 GC 统计信息，共打印 10 次。
    - **输出字段解释**：
        - `S0C`, `S1C`, `S0U`, `S1U`：Survivor 0/1 区容量 (Capacity) 和使用量 (Usage)。
        - `EC`, `EU`：Eden 区容量和使用量。
        - `OC`, `OU`：老年代容量和使用量。
        - `MC`, `MU`：元空间容量和使用量。
        - `YGC`, `YGCT`：Young GC 次数和时间。
        - `FGC`, `FGCT`：Full GC 次数和时间。
        - `GCT`：GC 总时间。

### 3. jinfo (Configuration Info for Java)
- **作用**：实时地查看和调整虚拟机各项参数。
- **常用命令**：
    - `jinfo -flags <pid>`：查看所有 JVM 参数。
    - `jinfo -flag <name> <pid>`：查看指定参数的值。
    - `jinfo -flag [+|-]<name> <pid>`：开启或关闭指定布尔类型参数。
    - `jinfo -flag <name>=<value> <pid>`：修改指定参数的值。

### 4. jmap (Memory Map for Java)
- **作用**：用于生成堆转储快照 (heapdump 或 dump 文件)。还可以查询 finalize 执行队列、Java 堆和永久代的详细信息。
- **常用命令**：
    - `jmap -heap <pid>`：显示 Java 堆详细信息（如 GC 算法、堆配置、分代状况）。
    - `jmap -histo <pid>`：显示堆中对象统计信息（包括类、实例数量、合计容量）。
    - `jmap -dump:format=b,file=heap.hprof <pid>`：生成堆转储快照。

### 5. jstack (Stack Trace for Java)
- **作用**：用于生成虚拟机当前时刻的线程快照 (threaddump 或 javacore 文件)。
- **目的**：定位线程出现长时间停顿的原因，如线程间死锁、死循环、请求外部资源导致的长时间等待等。
- **常用命令**：
    - `jstack <pid>`：打印线程堆栈信息。
    - `jstack -l <pid>`：除堆栈外，显示关于锁的附加信息。
- **常见线程状态**：
    - `RUNNABLE`：运行中。
    - `BLOCKED`：被阻塞（等待锁）。
    - `WAITING`：无限等待。
    - `TIMED_WAITING`：有限期等待。

## 二、可视化工具

### 1. jconsole (Java Monitoring and Management Console)
- **作用**：基于 JMX 的可视化监控工具。
- **功能**：
    - **内存**：监控堆和非堆内存变化，执行 GC。
    - **线程**：查看线程堆栈，检测死锁。
    - **类**：查看类加载数量。
    - **VM 概要**：查看 JVM 参数等。

### 2. jvisualvm (All-in-One Java Troubleshooting Tool)
- **作用**：功能最强大的运行监视和故障处理程序之一。
- **功能**：
    - 显示虚拟机进程以及进程的配置、环境信息（jps, jinfo）。
    - 监视应用程序的 CPU、GC、堆、方法区以及线程的信息（jstat, jstack）。
    - dump 以及分析堆转储快照（jmap, jhat）。
    - 方法级的性能分析。
    - 插件扩展（如 Visual GC）。

### 3. Arthas (Alibaba 开源)
- **作用**：线上监控诊断产品，无需重启，动态跟踪。
- **常用命令**：
    - `dashboard`：实时面板。
    - `thread`：查看线程堆栈。
    - `jvm`：查看 JVM 信息。
    - `trace`：方法内部调用路径，并输出方法路径上的每个节点上耗时。
    - `watch`：观测方法执行数据。
