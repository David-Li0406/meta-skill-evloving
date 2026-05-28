# Redis 集群架构与实战

## 一、Redis Cluster (切片集群)

### 1.1 架构原理
- **去中心化**: 没有中心节点，客户端连接任意节点。
- **Slot (槽)**: 整个集群共有 16384 个槽。
- **分片规则**: `CRC16(key) % 16384`。
- **MOVED 错误**: 客户端请求 Key，如果不在当前节点，节点返回 MOVED (包含新地址)，客户端更新路由表并重试。
- **ASK 错误**: 正在迁移 Slot 时，节点返回 ASK，客户端临时访问新节点 (不更新路由表)。

### 1.2 Java 连接集群 (JedisCluster)

```java
import redis.clients.jedis.HostAndPort;
import redis.clients.jedis.JedisCluster;
import java.util.HashSet;
import java.util.Set;

public class RedisClusterDemo {
    public static void main(String[] args) {
        Set<HostAndPort> nodes = new HashSet<>();
        nodes.add(new HostAndPort("192.168.1.10", 7001));
        nodes.add(new HostAndPort("192.168.1.10", 7002));
        nodes.add(new HostAndPort("192.168.1.10", 7003));
        
        // JedisCluster 内部会自动发现其他节点
        JedisCluster cluster = new JedisCluster(nodes);

        cluster.set("name", "ClusterUser");
        System.out.println(cluster.get("name"));

        cluster.close();
    }
}
```

### 1.3 HashTag (解决多 Key 操作)
Redis Cluster 要求 `MGET`、`MSET`、`Lua` 脚本涉及的所有 Key 必须在 **同一个 Slot**，否则报错。
- **HashTag**: 只根据 `{}` 内部的字符串计算 Slot。
- **示例**:
  - `user:100:profile` -> Hash("user:100:profile")
  - `user:100:orders` -> Hash("user:100:orders")
  - 这两个大概率不在同 Slot。
- **优化**:
  - `{user:100}:profile` -> Hash("user:100")
  - `{user:100}:orders` -> Hash("user:100")
  - 这样它们一定在同一个 Slot，支持事务操作。

## 二、哨兵模式 (Sentinel)

### 2.1 架构
- 也是主从结构，但多了 Sentinel 进程监控。
- **自动故障转移**: Master 挂了，Sentinel 自动选 Slave 上位。

### 2.2 Java 连接哨兵
客户端 **不能直接连 Master**，必须连 Sentinel，询问谁是 Master。

```java
import redis.clients.jedis.JedisSentinelPool;
import java.util.HashSet;
import java.util.Set;

public class SentinelDemo {
    public static void main(String[] args) {
        Set<String> sentinels = new HashSet<>();
        sentinels.add("192.168.1.10:26379");
        sentinels.add("192.168.1.10:26380");
        sentinels.add("192.168.1.10:26381");

        // masterName 是配置哨兵时指定的，如 mymaster
        JedisSentinelPool pool = new JedisSentinelPool("mymaster", sentinels);

        try (Jedis jedis = pool.getResource()) {
            // 这里拿到的 jedis 已经是连接到当前 Master 的了
            jedis.set("key", "val");
        }
    }
}
```

## 三、常见集群问题

### 3.1 数据倾斜
- **BigKey**: 某个 Key Value 特别大 (如几百万元素的 Set)，导致该 Slot 所在节点内存飙升、网络阻塞。
  - **解决**: 拆分 BigKey，比如 `big:hash` 拆成 `big:hash:1` ... `big:hash:100`。
- **热点 Key**: 某个 Key QPS 特别高 (如秒杀商品)。
  - **解决**: 使用 LocalCache (Guava/Caffeine) 在应用层做一级缓存，减少 Redis 压力。

### 3.2 脑裂 (Split-Brain)
- **现象**: 网络分区导致出现两个 Master。客户端往旧 Master 写入，旧 Master 恢复后降级为 Slave，同步新 Master 数据，导致期间写入的数据 **丢失**。
- **解决**: 设置 `min-replicas-to-write 1` (至少有 1 个 Slave 同步成功才允许写入)，牺牲可用性保证一致性。
