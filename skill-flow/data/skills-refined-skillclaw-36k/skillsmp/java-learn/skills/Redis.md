---
name: redis
description: Redis 学习资料（数据结构 + 场景）
---

# Redis 学习资料

## 1. 为什么 Redis 快
- 内存数据库
- 单线程事件循环（避免频繁上下文切换）+ IO 多路复用
- 高效数据结构（SDS、Dict、ZipList/ListPack 等）

---

## 2. 常用数据结构与场景
- String：缓存/计数器/分布式锁辅助
- Hash：对象缓存
- List：消息队列（简单）
- Set：去重、共同好友
- ZSet：排行榜、延时队列（score）
- Bitmap/HyperLogLog：签到/UV

---

## 3. 持久化
- RDB：快照，恢复快，可能丢数据
- AOF：追加日志，更安全，文件可能大（rewrite）

---

## 4. 高可用
- 主从复制
- Sentinel：故障转移
- Cluster：分片

---

## 5. 缓存问题
- 缓存穿透：布隆过滤器/空值缓存
- 缓存击穿：热点 key 互斥锁/逻辑过期
- 缓存雪崩：过期时间打散/多级缓存

---

## 6. 分布式锁（常见坑）
- 正确姿势：`SET key value NX PX ttl`
- 解锁：校验 value 再删（Lua 原子性）
- RedLock：了解即可，重点是业务是否真的需要

---

## 7. 可运行示例代码建议
- Redis demo 需要依赖 redis-server；如果你本机有 Redis，我可以补 Jedis/Lettuce 的最小可运行示例（需你确认要哪个客户端）。
