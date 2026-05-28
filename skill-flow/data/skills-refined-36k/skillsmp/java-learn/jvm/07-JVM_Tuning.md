# JVM 调优实战指南

## 一、生产环境 JVM 参数模板

### 1.1 标准 4C8G 服务参数
```bash
java -server \
# 堆内存设置 (建议 Xms=Xmx 避免抖动)
-Xmx4g -Xms4g \
# 元空间设置
-XX:MetaspaceSize=256m -XX:MaxMetaspaceSize=512m \
# 开启 G1 垃圾收集器 (JDK 8 推荐，JDK 11+ 默认)
-XX:+UseG1GC \
# 最大停顿时间目标 200ms
-XX:MaxGCPauseMillis=200 \
# 并行 GC 线程数 (逻辑核数)
-XX:ParallelGCThreads=4 \
# 开启 GC 日志 (JDK 8)
-XX:+PrintGCDetails -XX:+PrintGCDateStamps -Xloggc:/logs/gc.log \
# 开启 GC 日志 (JDK 9+)
# -Xlog:gc*:file=/logs/gc.log:time,tags:filecount=10,filesize=10M \
# OOM 时自动 Dump 堆内存
-XX:+HeapDumpOnOutOfMemoryError -XX:HeapDumpPath=/logs/dump.hprof \
-jar app.jar
```

## 二、OOM (OutOfMemoryError) 实战分析

### 2.1 堆溢出 (Java heap space)
**现象**: 频繁 Full GC，CPU 飙高，最后抛出 OOM。
**案例**: 导出大量 Excel 数据，将所有数据一次性加载到 List 中。
**分析**: Dump 文件分析，查找最大的对象 (Dominator Tree)。
**解决**:
1.  **代码层面**: 分批查询，流式写入 Excel (EasyExcel)。
2.  **参数层面**: 调大 `-Xmx` (治标不治本)。

### 2.2 元空间溢出 (Metaspace)
**现象**: 程序启动不久后 OOM，或者运行几天后 OOM。
**原因**: 动态生成了大量类 (CGLib, Proxy, JSP)。
**案例**: 某 RPC 框架在循环中不断创建代理类，没有缓存。
**解决**: 增加 `-XX:MaxMetaspaceSize`，检查反射/代理类的缓存机制。

### 2.3 堆外内存溢出 (Direct buffer memory)
**现象**: 堆内存很少，但物理内存被吃光。
**原因**: Netty 使用了大量 DirectByteBuffer 但没有释放。
**解决**: 使用 `-XX:MaxDirectMemorySize` 限制，使用 Arthas 监控堆外内存。

## 三、调优工具：Arthas

阿里巴巴开源的神器，无需重启即可诊断。

### 3.1 常用命令
```bash
# 1. 启动
java -jar arthas-boot.jar

# 2. dashboard - 查看全局状态 (线程、内存、GC)
$ dashboard

# 3. thread - 查看最忙的线程 (排查 CPU 100%)
$ thread -n 3

# 4. jad - 反编译代码 (检查线上代码版本)
$ jad com.example.MyService

# 5. watch - 观察方法入参/返回值/异常
$ watch com.example.MyService methodA "{params, returnObj, throwExp}" -x 2

# 6. trace - 方法内部调用耗时 (排查慢接口)
$ trace com.example.MyService methodA

# 7. heapdump - 导出堆快照
$ heapdump /tmp/dump.hprof
```

## 四、GC 日志分析 (G1)

### 4.1 日志片段
```text
[GC pause (G1 Evacuation Pause) (young), 0.0302120 secs]
   [Parallel Time: 25.1 ms, GC Workers: 4]
      [GC Worker Start (ms): Min: 123.1, Avg: 123.2, Max: 123.3]
      [Ext Root Scanning (ms): Min: 0.5, Avg: 0.7, Max: 1.0]
      [Object Copy (ms): Min: 20.0, Avg: 22.1, Max: 23.5]
   [Eden: 512.0M(512.0M)->0.0B(512.0M) Survivors: 64.0M->64.0M Heap: 1200.0M(4096.0M)->688.0M(4096.0M)]
```
### 4.2 关键指标解读
- **Evacuation Pause (young)**: Young GC，将存活对象从 Eden/Survivor 拷贝到 Survivor/Old。
- **Object Copy**: 对象拷贝耗时。如果该值很高，说明存活对象很多，Young 区可能设置过大，或者短命对象变成了长命对象。
- **Eden: 512.0M -> 0.0B**: Eden 区被清空。

### 4.3 调优思路
1.  **Mixed GC 过于频繁**: 调低 `-XX:InitiatingHeapOccupancyPercent` (默认 45%)，让并发标记更早开始。
2.  **Humongous Allocation (大对象)**: 可以在日志中看到 `Humongous` 字样。G1 中超过 Region 50% 的对象直接进老年代。解决办法是调大 Region 大小 `-XX:G1HeapRegionSize`。
