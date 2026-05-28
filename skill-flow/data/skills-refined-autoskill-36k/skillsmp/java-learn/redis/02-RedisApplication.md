# Redis 核心应用场景与代码

## 一、分布式锁 (Distributed Lock)

### 1.1 错误案例与进化
1. **只用 SETNX**: 没设置过期时间 -> 业务宕机 -> 死锁。
2. **SETNX + EXPIRE**: 分两步执行 -> SETNX 成功后宕机 -> 死锁 (原子性问题)。
3. **SET key val NX PX**: 原子指令 -> 依然有“锁过期但业务没跑完”导致并发的问题。

### 1.2 高可用方案：Redisson
生产环境强烈推荐使用 Redisson，它内置了 **看门狗 (Watch Dog)** 机制。

```java
import org.redisson.Redisson;
import org.redisson.api.RLock;
import org.redisson.api.RedissonClient;
import org.redisson.config.Config;
import java.util.concurrent.TimeUnit;

public class DistributedLockDemo {
    public static void main(String[] args) {
        Config config = new Config();
        config.useSingleServer().setAddress("redis://127.0.0.1:6379");
        RedissonClient redisson = Redisson.create(config);

        RLock lock = redisson.getLock("myLock");

        try {
            // 尝试加锁
            // waitTime: 等待获取锁的时间
            // leaseTime: -1 表示开启看门狗，每隔 10s 自动续期到 30s
            boolean isLocked = lock.tryLock(100, -1, TimeUnit.SECONDS);
            
            if (isLocked) {
                System.out.println("业务执行中...");
                Thread.sleep(5000);
            }
        } catch (InterruptedException e) {
            e.printStackTrace();
        } finally {
            // 必须判断是否持有锁，防止释放了别人的锁
            if (lock.isHeldByCurrentThread()) {
                lock.unlock();
            }
        }
    }
}
```

### 1.3 手写 Redis 分布式锁 (Lua 脚本)
如果不使用 Redisson，必须用 Lua 脚本保证“判断锁 + 删除锁”的原子性。

```java
public boolean unlock(String key, String uuid) {
    String script = 
        "if redis.call('get', KEYS[1]) == ARGV[1] then " +
        "   return redis.call('del', KEYS[1]) " +
        "else " +
        "   return 0 " +
        "end";
    
    Long result = (Long) jedis.eval(script, 
        Collections.singletonList(key), 
        Collections.singletonList(uuid));
        
    return result == 1;
}
```

## 二、缓存一致性 (Cache Consistency)

### 2.1 最佳实践：Cache Aside Pattern
**读**: 读缓存 -> 命中返回 -> 未命中查库 -> 写缓存。
**写**: **先更新 DB，再删除 Cache**。

```java
public User getUser(long id) {
    // 1. 查缓存
    String key = "user:" + id;
    String val = redis.get(key);
    if (val != null) return JSON.parse(val);
    
    // 2. 查库
    User user = userMapper.selectById(id);
    
    // 3. 写缓存 (设置过期时间，兜底)
    if (user != null) {
        redis.setex(key, 3600, JSON.toJSONString(user));
    }
    return user;
}

public void updateUser(User user) {
    // 1. 更新库
    userMapper.update(user);
    // 2. 删缓存
    redis.del("user:" + user.getId());
}
```

### 2.2 延迟双删
解决“主从同步延迟”导致的脏数据问题。
1. 删除缓存。
2. 更新数据库。
3. Sleep (比如 500ms, 大于主从同步时间)。
4. 再次删除缓存。

## 三、布隆过滤器 (Bloom Filter)
用于解决 **缓存穿透** 问题 (查询大量不存在的数据)。

### 3.1 原理
- 一个很长的 Bit 数组。
- 多个 Hash 函数。
- 写入: 对 Key 进行多次 Hash，将对应位置标为 1。
- 查询: 只要有一个位置是 0，则 Key **一定不存在**；全为 1，则 **可能存在** (误判)。

### 3.2 Redisson 实现
```java
RBloomFilter<String> bloomFilter = redisson.getBloomFilter("userBloom");
// 初始化: 预计插入 10000 个元素，误差率 0.03
bloomFilter.tryInit(10000L, 0.03);

bloomFilter.add("user:1");
bloomFilter.add("user:2");

System.out.println(bloomFilter.contains("user:1")); // true
System.out.println(bloomFilter.contains("user:99")); // false (直接返回，不查库)
```

## 四、内存淘汰策略配置
生产环境推荐配置：
```conf
# 内存上限
maxmemory 4gb
# 策略: 移除最近最少使用的 key (LRU)
maxmemory-policy allkeys-lru
```
