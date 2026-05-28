# Redis 基础与实战

## 一、Redis 客户端对比与 Java 实战

### 1.1 主流客户端
- **Jedis**: 老牌客户端，直接映射 Redis 命令。**线程不安全**，多线程必须使用连接池 (`JedisPool`)。
- **Lettuce**: Spring Boot 2.x 默认客户端。基于 Netty NIO，**线程安全**，单连接支持高并发。
- **Redisson**: 提供了分布式的 Java 对象和服务 (Lock, Map, Set)，功能最丰富，但对原始命令支持不如前两者直观。

### 1.2 Jedis/Lettuce 代码示例

#### Maven 依赖
```xml
<dependency>
    <groupId>redis.clients</groupId>
    <artifactId>jedis</artifactId>
    <version>4.3.1</version>
</dependency>
```

#### Jedis 工具类 (连接池模式)
```java
import redis.clients.jedis.Jedis;
import redis.clients.jedis.JedisPool;
import redis.clients.jedis.JedisPoolConfig;

public class RedisUtil {
    private static JedisPool pool;

    static {
        JedisPoolConfig config = new JedisPoolConfig();
        config.setMaxTotal(100);
        config.setMaxIdle(10);
        // 连接 Redis
        pool = new JedisPool(config, "localhost", 6379);
    }

    public static void main(String[] args) {
        try (Jedis jedis = pool.getResource()) {
            // String
            jedis.set("user:1:name", "Alice");
            System.out.println(jedis.get("user:1:name"));

            // Hash
            jedis.hset("user:1:info", "age", "18");
            
            // List (队列)
            jedis.lpush("tasks", "task1", "task2");
            String task = jedis.rpop("tasks");
            
            // Set (去重)
            jedis.sadd("likes", "1001", "1002", "1001");
            
            // ZSet (排行榜)
            jedis.zadd("rank", 100, "PlayerA");
            jedis.zadd("rank", 95, "PlayerB");
            System.out.println("Top 1: " + jedis.zrevrange("rank", 0, 0));
        }
    }
}
```

## 二、底层数据结构深度剖析

### 2.1 SDS (Simple Dynamic String)
Redis 没有直接使用 C 语言的字符串 (`char*`)，而是自己构建了 SDS。
```c
struct sdshdr {
    int len;    // 已使用长度
    int free;   // 剩余可用长度
    char buf[]; // 字符数组
};
```
- **二进制安全**: C 字符串以 `\0` 结尾，不能存图片等二进制；SDS 记录了 `len`，可以存任意数据。
- **O(1) 获取长度**: C 字符串需要遍历，SDS 直接读 `len`。
- **空间预分配**: 修改字符串时，如果空间不够，会预留多余空间，防止频繁 `realloc`。

### 2.2 字典 (Dict) 与 渐进式 Rehash
Redis 的 Hash、Set 都是基于 Dict 实现的。
- **结构**: 两个 Hash 表 (`ht[0]`, `ht[1]`)。
- **Rehash**: 当扩容时，不会一次性把所有数据从 `ht[0]` 搬到 `ht[1]` (会卡死主线程)。
- **渐进式**: 
  - 每次执行增删改查时，顺便搬运一个 Bucket 的数据。
  - 有专门的定时任务搬运数据。
  - 最终 `ht[0]` 变空，交换两个表。

### 2.3 跳跃表 (SkipList)
ZSet (Sorted Set) 当元素多时使用 SkipList。
- **原理**: 也就是“多级索引的链表”。
- **层级**: 随机生成层高 (Level)，第 1 层有所有节点，第 N 层节点更稀疏。
- **查找**: 从最高层开始找，大了就往右，小了就往下。复杂度 **O(logN)**。
- **为什么不用红黑树?**: 
  - 实现简单。
  - 范围查询 (Range Query) 更高效 (直接在 Level 1 链表遍历)。

## 三、单线程模型与 IO 多路复用

Redis 所谓“单线程”是指 **网络 IO 和键值对读写** 是由一个主线程完成的。
- **IO 多路复用 (epoll)**: 
  - 这里的“多路”指多个 TCP 连接。
  - “复用”指复用一个线程。
  - 也就是一个线程监听多个 Socket 的就绪事件 (Readable/Writable)，谁来了处理谁，非阻塞。
- **为什么不允许多线程?**
  - CPU 不是瓶颈，内存和网络才是。
  - 多线程加锁复杂，容易死锁，上下文切换有开销。
- **Redis 6.0 变化**: 引入了多线程处理 **网络数据的读写 (Read/Write)**，但 **命令执行 (Execute)** 依然是单线程，所以依然无需考虑线程安全问题。
