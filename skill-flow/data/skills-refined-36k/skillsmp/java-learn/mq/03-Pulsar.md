# Pulsar 架构师学习资料

## 一、Pulsar 独特架构：存算分离

### 1.1 组件拆解
- **Broker (计算层)**: 
  - 无状态，不存数据。
  - 负责协议解析、权限控制、负载均衡、消息分发。
  - 扩容非常容易，启动新节点即可。
- **BookKeeper (存储层)**:
  - 有状态，由多个 **Bookie** 节点组成。
  - 负责数据持久化 (Ledger)。
  - 扩容时，新数据自动写入新节点，旧数据无需迁移 (Rebalance)，这是相比 Kafka 的巨大优势。
- **ZooKeeper**: 存储元数据 (租户、Namespace、Topic 配置、Ledger 归属)。

### 1.2 Java 客户端实战

#### Maven 依赖
```xml
<dependency>
    <groupId>org.apache.pulsar</groupId>
    <artifactId>pulsar-client</artifactId>
    <version>3.0.0</version>
</dependency>
```

#### 生产者与消费者示例
```java
import org.apache.pulsar.client.api.*;

public class PulsarDemo {
    public static void main(String[] args) throws Exception {
        // 1. 创建客户端
        PulsarClient client = PulsarClient.builder()
            .serviceUrl("pulsar://localhost:6650")
            .build();

        // 2. 创建生产者
        Producer<byte[]> producer = client.newProducer()
            .topic("my-topic")
            .create();

        // 3. 发送消息
        producer.send("Hello Pulsar".getBytes());
        // 异步发送
        producer.sendAsync("Async Msg".getBytes()).thenAccept(msgId -> {
            System.out.println("发送成功: " + msgId);
        });

        // 4. 创建消费者
        Consumer<byte[]> consumer = client.newConsumer()
            .topic("my-topic")
            .subscriptionName("my-sub")
            // 订阅模式核心
            .subscriptionType(SubscriptionType.Shared) 
            .subscribe();

        // 5. 消费消息
        while (true) {
            Message<byte[]> msg = consumer.receive();
            try {
                System.out.println("收到: " + new String(msg.getData()));
                // 确认消息 (Ack)
                consumer.acknowledge(msg);
            } catch (Exception e) {
                // 否定确认 (Nack)，稍后重投
                consumer.negativeAcknowledge(msg);
            }
        }
    }
}
```

## 二、四大订阅模式详解

| 模式 | 描述 | 适用场景 |
| :--- | :--- | :--- |
| **Exclusive** (独占) | 默认模式。一个 Subscription 只能有一个 Consumer 连接。 | 顺序消费，单体处理。 |
| **Failover** (灾备) | 多个 Consumer 连接，但只有一个 Master 消费。Master 挂了，Slave 自动接管。 | 顺序消费，高可用。 |
| **Shared** (共享) | 多个 Consumer 同时消费，消息**轮询**分发。不保证顺序。 | 高吞吐，无序队列 (类似 RabbitMQ Work Queue)。 |
| **Key_Shared** | 相同 Key 的消息发给同一个 Consumer。 | 有序的高吞吐并发消费。 |

## 三、源码与高级特性

### 3.1 消息确认机制 (Ack)
- **Cumulative Ack (累积确认)**: `acknowledgeCumulative`。确认 msgId 及其之前的所有消息。适合 Exclusive/Failover。
- **Individual Ack (单条确认)**: `acknowledge`。只确认当前那条。适合 Shared 模式。

### 3.2 延时消息
Pulsar 原生支持任意时间的延时消息，不需要像 RocketMQ 那样分等级。
```java
producer.newMessage()
    .deliverAfter(10, TimeUnit.MINUTES) // 10分钟后投递
    .value("Delayed Msg".getBytes())
    .send();
```
**原理**: 延时消息会被 Tracker 追踪，到达时间后再推送到 Topic。

### 3.3 多租户 (Multi-Tenancy)
Pulsar url 结构: `persistent://tenant/namespace/topic`。
- **Tenant (租户)**: 对应公司的一个部门。
- **Namespace (命名空间)**: 对应一个应用或环境 (dev/prod)。
- 资源隔离、权限控制都在租户/命名空间级别配置。

## 四、对比总结

| 特性 | Kafka | RocketMQ | Pulsar |
| :--- | :--- | :--- | :--- |
| **架构** | 存算一体 (Broker 存数据) | 存算一体 (Broker 存数据) | **存算分离** (Broker + Bookie) |
| **扩容** | 需数据迁移 (Rebalance) | 需手动配置 | **自动负载，无迁移** |
| **顺序消息** | 支持 (Partition 级) | 支持 | 支持 (Key_Shared) |
| **延时消息** | 不支持 (需第三方) | 支持 (固定等级) | **支持 (任意时间)** |
| **适用场景** | 日志收集、超大吞吐 | 业务消息、事务消息 | 云原生、金融级一致性 |
