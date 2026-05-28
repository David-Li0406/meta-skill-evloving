---
name: mq
description: MQ 学习资料（Kafka/RocketMQ 通用方法论）
---

# MQ 学习资料

## 1. 为什么需要 MQ
- 削峰填谷
- 系统解耦
- 异步化（提升响应）

---

## 2. 核心概念（通用）
- Producer / Consumer / Broker
- Topic / Partition
- Consumer Group
- Offset

---

## 3. 投递语义
- At most once：可能丢但不重复
- At least once：可能重复但不丢（最常见）
- Exactly once：成本高，需要端到端设计

---

## 4. 可靠性设计
- 生产端：重试、ACK、幂等 key
- Broker：复制、刷盘策略
- 消费端：手动提交 offset、失败重试、死信队列

---

## 5. 顺序与事务
- 顺序消息：同 key 路由到同分区/队列
- 事务消息：本地事务 + 半消息/回查（RocketMQ 思路）

---

## 6. 常见问题
- 消息重复：幂等（数据库唯一键/去重表/业务幂等）
- 消息堆积：扩容消费者、排查慢消费、优化批量拉取
- 消息丢失：端到端链路压测 + 关键 ack/offset 策略

---

## 7. 可运行示例代码建议
- MQ demo 通常需要中间件环境；如果你希望我补 Kafka/RocketMQ 的 producer/consumer 示例，需要你提供本机环境或允许我加 docker-compose（你确认后我再做）。
