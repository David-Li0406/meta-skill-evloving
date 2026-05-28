# JVM Parameters (JVM 参数)

JVM 参数主要用于配置 JVM 的运行环境，包括内存大小、垃圾收集器选择、日志输出等。

## 一、参数类型

### 1. 标准参数
- 以 `-` 开头，所有的 JVM 实现都必须支持这些参数，且向后兼容。
- 例：
    - `-version`：查看版本
    - `-help`：查看帮助
    - `-cp` / `-classpath`：设置类路径

### 2. -X 参数 (非标准参数)
- 以 `-X` 开头，特定的 JVM 实现特有的参数，不保证所有 JVM 都支持，也不保证向后兼容。
- 例：
    - `-Xmx`：设置最大堆内存 (等同于 `-XX:MaxHeapSize`)
    - `-Xms`：设置初始堆内存 (等同于 `-XX:InitialHeapSize`)
    - `-Xss`：设置每个线程的栈大小 (等同于 `-XX:ThreadStackSize`)

### 3. -XX 参数 (不稳定参数)
- 以 `-XX` 开头，专门用于 JVM 调优和 Debug，可能会在不同版本中有所变化。
- **Boolean 类型**：
    - 格式：`-XX:+<name>` (开启) 或 `-XX:-<name>` (关闭)
    - 例：`-XX:+UseG1GC` (开启 G1 收集器), `-XX:+PrintGCDetails` (打印 GC 详情)
- **KV 类型**：
    - 格式：`-XX:<name>=<value>`
    - 例：`-XX:MaxGCPauseMillis=200`

## 二、常用参数详解

### 1. 内存设置
| 参数 | 说明 | 示例 |
| :--- | :--- | :--- |
| `-Xms` | 初始堆大小 | `-Xms1024m` |
| `-Xmx` | 最大堆大小 | `-Xmx1024m` (通常设置与 Xms 相同，避免扩容抖动) |
| `-Xmn` | 新生代大小 | `-Xmn512m` |
| `-Xss` | 线程栈大小 | `-Xss1m` (默认通常是 1m) |
| `-XX:MetaspaceSize` | 元空间初始大小 | `-XX:MetaspaceSize=128m` |
| `-XX:MaxMetaspaceSize` | 元空间最大大小 | `-XX:MaxMetaspaceSize=256m` |
| `-XX:SurvivorRatio` | Eden 区与 Survivor 区的比例 | `-XX:SurvivorRatio=8` (默认 8:1:1) |
| `-XX:MaxDirectMemorySize` | 最大直接内存 | `-XX:MaxDirectMemorySize=1g` |

### 2. 垃圾收集器选择
| 参数 | 说明 |
| :--- | :--- |
| `-XX:+UseSerialGC` | 使用 Serial + Serial Old |
| `-XX:+UseParNewGC` | 使用 ParNew + Serial Old (JDK 9+ 已废弃) |
| `-XX:+UseParallelGC` | 使用 Parallel Scavenge + Parallel Old (JDK 8 默认) |
| `-XX:+UseConcMarkSweepGC` | 使用 ParNew + CMS + Serial Old |
| `-XX:+UseG1GC` | 使用 G1 收集器 (JDK 9+ 默认) |
| `-XX:+UseZGC` | 使用 ZGC (JDK 11+) |

### 3. GC 日志与排查
| 参数 | 说明 |
| :--- | :--- |
| `-XX:+PrintGC` | 打印简要 GC 日志 |
| `-XX:+PrintGCDetails` | 打印详细 GC 日志 |
| `-XX:+PrintGCTimeStamps` | 打印 GC 发生的时间戳 |
| `-Xloggc:<file>` | 将 GC 日志输出到文件 |
| `-XX:+HeapDumpOnOutOfMemoryError` | 发生 OOM 时自动生成堆转储文件 (Dump) |
| `-XX:HeapDumpPath=<path>` | 指定 Dump 文件路径 |

## 三、如何查看参数

1.  **命令行查看**：
    - `java -XX:+PrintFlagsFinal -version`：查看所有参数的最终值。
    - `java -XX:+PrintFlagsInitial -version`：查看所有参数的默认值。
2.  **运行时查看**：
    - 使用 `jinfo` 命令 (见 JVM 工具章节)。

## 四、设置参数的方式

1.  **IDE 中设置**：
    - Eclipse/IntelliJ IDEA 的 VM Options 中添加。
2.  **命令行启动时设置**：
    - `java -Xms512m -Xmx512m -jar app.jar`
3.  **Tomcat/WebLogic 等容器中设置**：
    - 修改 `catalina.sh` 或 `setenv.sh` 中的 `JAVA_OPTS`。
