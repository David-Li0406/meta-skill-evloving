# Kafka 架构师学习资料

## 一、核心概念与基础操作

### 1.1 Maven 依赖
在学习 Kafka 之前，首先引入官方客户端依赖：
```xml
<dependency>
    <groupId>org.apache.kafka</groupId>
    <artifactId>kafka-clients</artifactId>
    <version>3.4.0</version>
</dependency>
```

### 1.2 高可靠生产者 (Producer) 实现
生产环境通常需要异步发送并处理回调，同时配置 ACK 机制保证数据不丢。

```java
import org.apache.kafka.clients.producer.*;
import org.apache.kafka.common.serialization.StringSerializer;
import java.util.Properties;

public class KafkaProducerService {
    public static void main(String[] args) {
        Properties props = new Properties();
        // 1. 连接地址
        props.put(ProducerConfig.BOOTSTRAP_SERVERS_CONFIG, "192.168.1.10:9092,192.168.1.11:9092");
        
        // 2. 序列化配置
        props.put(ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG, StringSerializer.class.getName());
        props.put(ProducerConfig.VALUE_SERIALIZER_CLASS_CONFIG, StringSerializer.class.getName());

        // 3. 生产高可靠性配置 (核心)
        // acks=0: 不等待服务器确认 (最快，易丢)
        // acks=1: Leader 写入即确认 (折中)
        // acks=all/-1: ISR 中所有副本写入才确认 (最慢，最安全)
        props.put(ProducerConfig.ACKS_CONFIG, "all");
        
        // 重试次数，建议设置很大，配合 retry.backoff.ms
        props.put(ProducerConfig.RETRIES_CONFIG, 3); 
        
        // 批处理配置 (吞吐量优化)
        props.put(ProducerConfig.BATCH_SIZE_CONFIG, 16384); // 16KB
        props.put(ProducerConfig.LINGER_MS_CONFIG, 10);     // 等待10ms凑批次

        KafkaProducer<String, String> producer = new KafkaProducer<>(props);

        for (int i = 0; i < 100; i++) {
            ProducerRecord<String, String> record = 
                new ProducerRecord<>("order-topic", "order-" + i, "{\"amount\": 100}");
            
            // 异步发送带回调
            producer.send(record, (metadata, exception) -> {
                if (exception == null) {
                    System.out.printf("发送成功: Topic=%s, Partition=%d, Offset=%d%n",
                            metadata.topic(), metadata.partition(), metadata.offset());
                } else {
                    System.err.println("发送失败: " + exception.getMessage());
                    // 实际场景可能需要记录日志或存入死信队列
                }
            });
        }
        
        producer.close();
    }
}
```

### 1.3 手动提交消费者 (Consumer) 实现
生产环境强烈建议关闭自动提交 (`enable.auto.commit=false`)，采用手动提交以防止消息丢失或重复消费。

```java
import org.apache.kafka.clients.consumer.*;
import org.apache.kafka.common.serialization.StringDeserializer;
import java.time.Duration;
import java.util.Collections;
import java.util.Properties;

public class KafkaConsumerService {
    public static void main(String[] args) {
        Properties props = new Properties();
        props.put(ConsumerConfig.BOOTSTRAP_SERVERS_CONFIG, "192.168.1.10:9092");
        props.put(ConsumerConfig.GROUP_ID_CONFIG, "order-service-group");
        
        // 反序列化
        props.put(ConsumerConfig.KEY_DESERIALIZER_CLASS_CONFIG, StringDeserializer.class.getName());
        props.put(ConsumerConfig.VALUE_DESERIALIZER_CLASS_CONFIG, StringDeserializer.class.getName());

        // 核心：关闭自动提交
        props.put(ConsumerConfig.ENABLE_AUTO_COMMIT_CONFIG, "false");
        
        // 当没有初始 offset 时从哪里读取：earliest (从头), latest (最新)
        props.put(ConsumerConfig.AUTO_OFFSET_RESET_CONFIG, "earliest");

        KafkaConsumer<String, String> consumer = new KafkaConsumer<>(props);
        consumer.subscribe(Collections.singletonList("order-topic"));

        try {
            while (true) {
                // 拉取消息
                ConsumerRecords<String, String> records = consumer.poll(Duration.ofMillis(100));
                
                for (ConsumerRecord<String, String> record : records) {
                    // 业务逻辑处理
                    processOrder(record.value());
                }
                
                // 业务处理成功后，同步提交当前批次的 Offset
                // 也可以使用 commitAsync 提高性能
                consumer.commitSync();
            }
        } catch (Exception e) {
            e.printStackTrace();
        } finally {
            consumer.close();
        }
    }

    private static void processOrder(String orderJson) {
        System.out.println("处理订单: " + orderJson);
    }
}
```

## 二、源码分析与核心原理

### 2.1 生产者发送流程 (RecordAccumulator)
Kafka 生产者并非直接发送网络请求，而是将消息缓存到内存池。
1. **拦截器 (Interceptor)**: 对消息进行加工。
2. **序列化 (Serializer)**: 转换字节数组。
3. **分区器 (Partitioner)**: 计算消息发往哪个 Partition (默认 hash(key) % partitions)。
4. **累加器 (RecordAccumulator)**: 
   - 内部维护一个 `ConcurrentMap<TopicPartition, Deque<ProducerBatch>>`。
   - 消息被追加到双端队列的尾部 Batch 中。
   - 这是一个典型的 **生产-消费者模型**，主线程生产，Sender 线程消费。
5. **Sender 线程**:
   - 只要 Batch 满了或者 linger.ms 到了，Sender 线程就会将 Batch 取出。
   - 封装成 `ClientRequest` 发送给 Broker。

### 2.2 零拷贝 (Zero Copy) 原理
Kafka 的高吞吐很大程度上依赖于操作系统的零拷贝技术 `sendfile`。
- **传统流程**: 磁盘 -> 内核 Buffer -> 用户 Buffer -> Socket Buffer -> 网卡。 (4次拷贝，4次切换)
- **Zero Copy**: 磁盘 -> 内核 Buffer -> 网卡。 (2次拷贝，2次切换，且 CPU 参与极少)
- **Java 实现**: `FileChannel.transferTo()` 方法。

## 三、常见生产问题与解决方案

### 3.1 消息积压
**现象**: Consumer 消费速度远低于 Producer 生产速度，导致 Lag 值飙升。
**解决方案**:
1. **扩容**: 增加 Topic 的 Partition 数量 (如从 3 扩到 10)。
2. **多线程/多实例**: 部署更多 Consumer 实例 (数量 <= Partition 数)。
3. **本地并发**: 如果 Partition 无法扩容，Consumer 内部使用线程池处理业务逻辑，实现单 Consumer 多线程消费 (需注意 Offset 提交管理，防止乱序提交)。

### 3.2 消息重复 (Exactly Once 语义)
**原因**: Consumer 消费成功，但提交 Offset 失败（如宕机），重启后重读。
**解决方案**:
1. **幂等性设计**: 数据库唯一键约束、Redis Set 去重。
2. **Kafka 幂等性 Producer**: 配置 `enable.idempotence=true`，Kafka 会自动生成 PID 和 Sequence Number 去重 (仅限单分区单会话)。
3. **Kafka 事务**: 配合 `isolation.level=read_committed` 实现端到端的 Exactly Once。

### 3.3 消息乱序
**原因**: 
1. 消息重试导致顺序打乱 (`max.in.flight.requests.per.connection > 1`)。
2. 发送到不同的 Partition。
**解决方案**:
1. 确保同一业务 ID (如 OrderID) 必须发送到同一 Partition (指定 Key)。
2. Producer 端设置 `max.in.flight.requests.per.connection=1` (会降低吞吐) 或者开启 `enable.idempotence=true` (推荐，既保证顺序又保证不丢)。
