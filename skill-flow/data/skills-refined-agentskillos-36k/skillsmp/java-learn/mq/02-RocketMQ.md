# RocketMQ 架构师学习资料

## 一、核心功能与 Java 实战

### 1.1 Maven 依赖
```xml
<dependency>
    <groupId>org.apache.rocketmq</groupId>
    <artifactId>rocketmq-client</artifactId>
    <version>5.1.0</version>
</dependency>
```

### 1.2 事务消息 (Transaction Message)
RocketMQ 最强杀手锏，用于解决 **分布式事务** 最终一致性问题 (如：下订单 -> 扣减库存/加积分)。

#### 事务监听器实现
```java
import org.apache.rocketmq.client.producer.LocalTransactionState;
import org.apache.rocketmq.client.producer.TransactionListener;
import org.apache.rocketmq.common.message.Message;
import org.apache.rocketmq.common.message.MessageExt;
import java.util.concurrent.ConcurrentHashMap;

public class OrderTransactionListener implements TransactionListener {
    
    // 模拟本地事务状态存储
    private ConcurrentHashMap<String, Integer> localTrans = new ConcurrentHashMap<>();

    /**
     * 执行本地事务 (扣减库存、保存订单等)
     */
    @Override
    public LocalTransactionState executeLocalTransaction(Message msg, Object arg) {
        String transId = msg.getTransactionId();
        System.out.println("执行本地事务: " + transId);
        try {
            // TODO: 执行数据库操作
            // int status = orderService.createOrder(...);
            localTrans.put(transId, 1); // 1=Success
            
            // 提交事务，消息对消费者可见
            return LocalTransactionState.COMMIT_MESSAGE;
        } catch (Exception e) {
            // 回滚事务，消息被丢弃
            return LocalTransactionState.ROLLBACK_MESSAGE;
        }
    }

    /**
     * 事务回查 (当 Broker 收不到 Commit/Rollback 时回调)
     */
    @Override
    public LocalTransactionState checkLocalTransaction(MessageExt msg) {
        String transId = msg.getTransactionId();
        System.out.println("执行事务回查: " + transId);
        
        Integer status = localTrans.get(transId);
        if (status != null && status == 1) {
            return LocalTransactionState.COMMIT_MESSAGE;
        }
        // 继续等待 (UNKNOW 会让 Broker 过段时间再查)
        return LocalTransactionState.UNKNOW;
    }
}
```

#### 事务生产者发送
```java
import org.apache.rocketmq.client.producer.TransactionMQProducer;
import org.apache.rocketmq.common.message.Message;
import java.util.concurrent.*;

public class TransactionProducerDemo {
    public static void main(String[] args) throws Exception {
        TransactionMQProducer producer = new TransactionMQProducer("tx-group");
        producer.setNamesrvAddr("127.0.0.1:9876");
        
        // 设置自定义线程池处理回查
        ExecutorService executor = new ThreadPoolExecutor(2, 5, 100, TimeUnit.SECONDS, 
            new ArrayBlockingQueue<>(2000), r -> new Thread(r, "TxCheckThread"));
        producer.setExecutorService(executor);
        
        // 设置监听器
        producer.setTransactionListener(new OrderTransactionListener());
        
        producer.start();

        Message msg = new Message("TopicTx", "TagA", "KEY-001", "OrderData".getBytes());
        // 发送半消息 (Half Message)
        producer.sendMessageInTransaction(msg, null);
        
        // 保持进程存活以便回查
        Thread.sleep(100000);
        producer.shutdown();
    }
}
```

### 1.3 顺序消息 (Ordered Message)
保证同一订单的操作 (创建->支付->发货) 被同一个 Consumer 线程顺序消费。

**生产者**：使用 `MessageQueueSelector` 将同一 ID 发送到同一 Queue。
```java
producer.send(msg, new MessageQueueSelector() {
    @Override
    public MessageQueue select(List<MessageQueue> mqs, Message msg, Object arg) {
        Long orderId = (Long) arg;
        long index = orderId % mqs.size();
        return mqs.get((int) index);
    }
}, orderId); // 传入 orderId 作为 arg
```

**消费者**：使用 `MessageListenerOrderly` 而非 `MessageListenerConcurrently`。
```java
consumer.registerMessageListener(new MessageListenerOrderly() {
    @Override
    public ConsumeOrderlyStatus consumeMessage(List<MessageExt> msgs, ConsumeOrderlyContext context) {
        // 框架会自动加锁，保证单线程处理
        System.out.println("顺序消费: " + new String(msgs.get(0).getBody()));
        return ConsumeOrderlyStatus.SUCCESS;
    }
});
```

## 二、部署架构与 NameServer

### 2.1 NameServer 作用
- **无状态**: 节点之间互不通信，Broker 向所有 NameServer 注册。
- **服务发现**: Producer/Consumer 轮询 NameServer 获取 Broker 地址。
- **对比 Zookeeper**: ZK 强一致性 (CP)，NameServer 追求可用性 (AP)，设计更轻量，适合消息中间件场景。

### 2.2 刷盘机制 (FlushDiskType)
1. **SYNC_FLUSH (同步刷盘)**: 消息写入内存且刷到磁盘才返回成功。数据最安全，性能低。
2. **ASYNC_FLUSH (异步刷盘)**: 消息写入内存即返回成功，后台线程定时刷盘。性能高，断电可能丢少量数据。

## 三、源码分析：消息存储

RocketMQ 采用 **CommitLog + ConsumeQueue** 的混合存储设计。
- **CommitLog**: 1G 一个文件，所有 Topic 混写，保证**顺序写**磁盘，速度极快。
- **ConsumeQueue**: 相当于索引，记录 Message 在 CommitLog 中的 Offset、Size、TagHash。
- **好处**:
  1. 写入速度极快 (顺序 IO)。
  2. 读写分离 (读 ConsumeQueue，再读 CommitLog)。
  3. 利用操作系统的 PageCache 缓存热点数据。

## 四、常见问题

### 4.1 消息堆积如何处理？
1. **检查 Consumer**: 是否有死锁、耗时 SQL、外部接口超时。
2. **增加 Consumer**: 只要 `Consumer 实例数 < Queue 数量`，增加实例就能提升并行度。
3. **增加 Queue**: 如果实例数已等于 Queue 数，需修改 Topic 配置增加 Queue，并同时扩容 Consumer。

### 4.2 为什么 RocketMQ 延时消息不支持任意时间？
- 开源版只支持 18 个等级 (1s, 5s... 2h)。
- **原理**: 消息先发到系统内置 Topic `SCHEDULE_TOPIC_XXXX` 的对应队列 (如 level 1 对应 queue 0)。Broker 有定时任务轮询这些队列，时间到了再把消息还原到真实 Topic。
- **原因**: 支持任意精度的延时需要对海量消息进行排序，成本过高。商业版使用时间轮 (Timing Wheel) 实现了任意精度。
