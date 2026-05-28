# ConcurrentHashMap 源码与原理深度解析

## 一、JDK 1.7 与 1.8 架构对比

### 1.1 JDK 1.7：分段锁 (Segment)
*   **结构**: `Segment` 数组 + `HashEntry` 数组 + 链表。
*   **锁机制**: `Segment` 继承自 `ReentrantLock`。每个 `Segment` 守护一个 `HashEntry` 数组。
*   **并发度**: 等于 `Segment` 数组长度 (默认 16)。即最多支持 16 个线程同时写。
*   **put 操作**: 
    1.  Hash(key) 定位到 Segment。
    2.  `segment.lock()` 加锁。
    3.  Hash(key) 定位到 HashEntry，插入链表。
    4.  `segment.unlock()`。

### 1.2 JDK 1.8：Node + CAS + Synchronized
*   **结构**: `Node` 数组 + 链表/红黑树 (类似 HashMap)。
*   **锁机制**: 抛弃 `Segment`，直接锁住 **链表/红黑树的头节点**。
*   **并发度**: 理论上等于数组长度 (默认 16，扩容后更大)，并发度远高于 1.7。
*   **put 操作**:
    1.  如果没有初始化，CAS 初始化数组。
    2.  Hash(key) 定位到 Node 数组下标 `i`。
    3.  如果 `table[i]` 为空，**CAS** 尝试插入。
    4.  如果 `table[i]` 不为空，`synchronized(table[i])` 加锁，插入链表或红黑树。

## 二、JDK 1.8 核心源码分析

### 2.1 核心属性
```java
// 默认为 null，懒加载
transient volatile Node<K,V>[] table;

// 扩容时的临时表
private transient volatile Node<K,V>[] nextTable;

// 默认为 0
// -1: 正在初始化
// -N: 正在扩容 (N-1 个线程参与)
// >0: 下一次扩容的阈值 (0.75 * capacity)
private transient volatile int sizeCtl;
```

### 2.2 put 方法解析
```java
final V putVal(K key, V value, boolean onlyIfAbsent) {
    if (key == null || value == null) throw new NullPointerException();
    int hash = spread(key.hashCode()); // 计算 hash，保证正数
    int binCount = 0;
    
    for (Node<K,V>[] tab = table;;) {
        Node<K,V> f; int n, i, fh;
        
        // 1. 懒加载初始化
        if (tab == null || (n = tab.length) == 0)
            tab = initTable();
            
        // 2. 槽位为空，CAS 插入
        else if ((f = tabAt(tab, i = (n - 1) & hash)) == null) {
            if (casTabAt(tab, i, null, new Node<K,V>(hash, key, value, null)))
                break; 
        }
        
        // 3. 正在扩容 (MOVED = -1)，帮忙扩容
        else if ((fh = f.hash) == MOVED)
            tab = helpTransfer(tab, f);
            
        // 4. 发生哈希冲突，加锁
        else {
            V oldVal = null;
            synchronized (f) { // 锁住头节点
                if (tabAt(tab, i) == f) { // 双重检查
                    if (fh >= 0) { // 链表
                        // ... 遍历链表插入 ...
                    }
                    else if (f instanceof TreeBin) { // 红黑树
                        // ... 树操作 ...
                    }
                }
            }
            // 5. 链表转红黑树 (阈值 8)
            if (binCount != 0) {
                if (binCount >= TREEIFY_THRESHOLD)
                    treeifyBin(tab, i);
                if (oldVal != null)
                    return oldVal;
                break;
            }
        }
    }
    // 6. 增加计数 (LongAdder 思想)
    addCount(1L, binCount);
    return null;
}
```

### 2.3 扩容 (Transfer) 源码精髓
CHM 的扩容是 **多线程协同** 的。

1.  **触发条件**: `size >= sizeCtl` (0.75 * n)。
2.  **创建新表**: `nextTable` 大小翻倍。
3.  **分段迁移**: 
    *   将数组按 `stride` (步长) 分成多个段。
    *   每个线程领取一段区间 (例如 16 个槽位)，负责将这部分的 Node 迁移到 `nextTable`。
    *   迁移完的槽位放置 `ForwardingNode` (hash = -1)，表示该位置已迁移。
4.  **并发扩容**: 如果线程 B 在 put 时发现当前槽位是 `ForwardingNode`，它不会阻塞，而是去协助线程 A 进行扩容。

## 三、常见面试问题

### 3.1 为什么 1.8 放弃了 Segment？
1.  **粒度更细**: 1.7 锁一段，1.8 锁一个槽位 (Node)。
2.  **内存占用**: Segment 对象本身有内存开销。
3.  **JVM 优化**: synchronized 在 JDK 1.6 后优化了 (偏向锁、轻量级锁)，性能不输 ReentrantLock。

### 3.2 什么时候转红黑树？
同时满足两个条件：
1.  链表长度 >= 8。
2.  数组长度 >= 64。
*   如果链表长但数组短，优先扩容 (`tryPresize`) 而不是转树。

### 3.3 get 方法需要加锁吗？
不需要。
*   `Node` 的 `val` 和 `next` 指针都是 `volatile` 的，保证可见性。
*   如果遇到扩容 (`ForwardingNode`)，会调用 `find` 方法去 `nextTable` 查找。
