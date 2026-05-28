# ThreadLocal 原理与高并发陷阱

## 一、ThreadLocal 核心原理

### 1.1 内存模型
*   每个 `Thread` 对象内部有一个 `ThreadLocalMap threadLocals`。
*   `ThreadLocalMap` 是一个定制的 Hash Map。
*   **Key**: `ThreadLocal` 对象本身 (弱引用)。
*   **Value**: 线程存储的具体值 (强引用)。

```java
// Thread.java
ThreadLocal.ThreadLocalMap threadLocals = null;

// ThreadLocal.java
public void set(T value) {
    Thread t = Thread.currentThread();
    ThreadLocalMap map = getMap(t);
    if (map != null)
        map.set(this, value);
    else
        createMap(t, value);
}
```

### 1.2 弱引用与内存泄漏 (Memory Leak)
`Entry extends WeakReference<ThreadLocal<?>>`

*   **Key 泄漏?** 不会。Key 是弱引用，GC 时会被回收。Map 中会出现 Key=null 的 Entry。
*   **Value 泄漏?** **会！**
    *   `CurrentThread` -> `ThreadLocalMap` -> `Entry` -> `Value`。
    *   这是一条强引用链。
    *   如果线程一直存活 (线程池)，且没有手动 remove，Value 永远不会被回收。

**最佳实践**:
```java
try {
    threadLocal.set(val);
    // ...
} finally {
    threadLocal.remove(); // 必须清理
}
```

## 二、高并发场景下的进阶 ThreadLocal

### 2.1 FastThreadLocal (Netty)
JDK 的 `ThreadLocal` 使用线性探测法解决 Hash 冲突，在高并发下性能一般。
Netty 的 `FastThreadLocal` 配合 `FastThreadLocalThread` 使用 **数组下标** 直接定位，无 Hash 冲突，性能极高。

```java
// 使用示例
private static final FastThreadLocal<String> FAST_TL = new FastThreadLocal<>();

public void test() {
    // 必须在 FastThreadLocalThread 中运行才有优化效果
    new FastThreadLocalThread(() -> {
        FAST_TL.set("Hello");
        System.out.println(FAST_TL.get());
    }).start();
}
```

### 2.2 TransmittableThreadLocal (Alibaba)
JDK 的 `InheritableThreadLocal` 只能在 `new Thread()` 时传递父线程上下文。但在线程池中，线程是复用的，不会重复创建，导致上下文丢失。

`TransmittableThreadLocal (TTL)` 解决了这个问题。

```xml
<dependency>
    <groupId>com.alibaba</groupId>
    <artifactId>transmittable-thread-local</artifactId>
    <version>2.14.2</version>
</dependency>
```

```java
// 1. 定义 TTL
TransmittableThreadLocal<String> context = new TransmittableThreadLocal<>();

// 2. 包装线程池 (核心步骤)
ExecutorService executor = Executors.newFixedThreadPool(1);
ExecutorService ttlExecutor = TtlExecutors.getTtlExecutorService(executor);

// 3. 使用
context.set("Trace-ID-001");
ttlExecutor.submit(() -> {
    // 这里能取到父线程的值，即使线程是复用的
    System.out.println(context.get()); 
});
```

## 三、ThreadLocal 源码深度解析

### 3.1 ThreadLocalMap 的 Hash 算法

```java
// ThreadLocal.java
private final int threadLocalHashCode = nextHashCode();

// 神奇的哈希增量：0x61c88647
private static final int HASH_INCREMENT = 0x61c88647;

private static int nextHashCode() {
    return nextHashCode.getAndAdd(HASH_INCREMENT);
}
```

**为什么是 0x61c88647？**
- 这是一个黄金分割数，能让哈希码均匀分布
- 与 2^n 取模后，能尽量避免冲突

### 3.2 线性探测法解决冲突

```java
// ThreadLocalMap.set()
private void set(ThreadLocal<?> key, Object value) {
    Entry[] tab = table;
    int len = tab.length;
    int i = key.threadLocalHashCode & (len-1);

    // 线性探测：如果当前槽位被占用，向后找
    for (Entry e = tab[i]; e != null; e = tab[i = nextIndex(i, len)]) {
        ThreadLocal<?> k = e.get();
        
        // key 相同，更新值
        if (k == key) {
            e.value = value;
            return;
        }
        
        // key 为 null（被 GC 回收），替换 stale entry
        if (k == null) {
            replaceStaleEntry(key, value, i);
            return;
        }
    }
    
    // 找到空槽位，插入新 Entry
    tab[i] = new Entry(key, value);
    // ...
}
```

### 3.3 过期 Entry 清理机制

ThreadLocalMap 在以下时机清理过期 Entry（key=null）：
1. `set()` 时遇到 stale entry
2. `get()` 时遇到 stale entry
3. `remove()` 时
4. `rehash()` 时

```java
// 探测式清理
private int expungeStaleEntry(int staleSlot) {
    Entry[] tab = table;
    int len = tab.length;

    // 清理 staleSlot 位置
    tab[staleSlot].value = null;
    tab[staleSlot] = null;
    size--;

    // 向后遍历，清理所有连续的 stale entry
    // ...
}
```

## 四、ThreadLocal 使用场景总结

1.  **数据库连接/Session 管理**: `DataSourceTransactionManager`, `Hibernate Session`.
2.  **Web 上下文**: Spring MVC `RequestContextHolder` (存储 `HttpServletRequest`).
3.  **日志追踪**: MDC (Log4j/Logback) 存储 TraceID。
4.  **SimpleDateFormat**: 避免每次 new，且保证线程安全。
5.  **用户上下文传递**: 登录用户信息在调用链中传递。

## 五、常见面试题

### Q1: ThreadLocal 会造成内存泄漏吗？如何避免？
**答**：会。
- Entry 的 Key 是弱引用，GC 后变成 null
- 但 Value 是强引用，如果线程不结束，Value 不会被回收
- 解决方案：使用完毕后调用 `remove()` 方法

### Q2: 为什么 Entry 的 Key 是弱引用？
**答**：
- 如果是强引用，即使 ThreadLocal 不再使用，也无法被 GC
- 使用弱引用可以让 ThreadLocal 在没有外部引用时被回收
- 但这只解决了 Key 的内存问题，Value 仍需手动 remove

### Q3: ThreadLocal 如何保证线程安全？
**答**：
- 每个线程有自己的 ThreadLocalMap
- 读写操作只在当前线程的 Map 中进行
- 不存在并发访问，天然线程安全

### Q4: InheritableThreadLocal 在线程池中的问题？
**答**：
- InheritableThreadLocal 只在创建子线程时复制父线程的值
- 线程池中线程是复用的，不会重复复制
- 解决方案：使用阿里的 TransmittableThreadLocal

### Q5: FastThreadLocal 为什么比 ThreadLocal 快？
**答**：
- ThreadLocal 使用哈希表 + 线性探测，有冲突处理开销
- FastThreadLocal 使用数组，每个实例有唯一 index，直接定位
- FastThreadLocal 需要配合 FastThreadLocalThread 使用

## 六、代码示例

完整示例代码请参考：
`src/main/java/com/example/thread/ThreadLocalDemo.java`
