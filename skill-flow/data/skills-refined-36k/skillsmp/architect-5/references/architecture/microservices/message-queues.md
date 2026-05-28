# Message Queue Communication Patterns

**Category**: architecture/microservices
**Description**: Detect message queue producers/consumers for async service mapping
**Purpose**: Map asynchronous microservice communication patterns

---

## Apache Kafka

### Python Kafka Producer
**Type**: semgrep
**Severity**: info
**Languages**: [python]
**Pattern**: `KafkaProducer(bootstrap_servers=$SERVERS, ...)`
- Creates Kafka producer
- Example: `KafkaProducer(bootstrap_servers=['kafka:9092'])`
- Captures: Broker addresses

### Python Kafka Consumer
**Type**: semgrep
**Severity**: info
**Languages**: [python]
**Pattern**: `KafkaConsumer($TOPIC, ..., bootstrap_servers=$SERVERS, ...)`
- Creates Kafka consumer
- Example: `KafkaConsumer('orders', bootstrap_servers=['kafka:9092'])`
- Captures: Topic, brokers

### Python Send Message
**Type**: semgrep
**Severity**: info
**Languages**: [python]
**Pattern**: `$PRODUCER.send($TOPIC, ...)`
- Sends message to Kafka topic
- Example: `producer.send('user-events', value=event)`
- Captures: Topic name

### JavaScript KafkaJS Producer
**Type**: semgrep
**Severity**: info
**Languages**: [javascript, typescript]
**Pattern**: `$KAFKA.producer(...)`
- Creates KafkaJS producer
- Example: `kafka.producer()`

### JavaScript KafkaJS Consumer
**Type**: semgrep
**Severity**: info
**Languages**: [javascript, typescript]
**Pattern**: `$KAFKA.consumer({ groupId: $GROUP })`
- Creates KafkaJS consumer
- Example: `kafka.consumer({ groupId: 'order-processor' })`
- Captures: Consumer group

### Go Kafka Producer
**Type**: semgrep
**Severity**: info
**Languages**: [go]
**Pattern**: `kafka.NewProducer($CONFIG)`
- Creates Confluent Kafka producer
- Example: `kafka.NewProducer(&kafka.ConfigMap{"bootstrap.servers": "kafka:9092"})`

### Go Sarama Producer
**Type**: semgrep
**Severity**: info
**Languages**: [go]
**Pattern**: `sarama.NewSyncProducer($BROKERS, ...)`
- Creates Sarama sync producer
- Example: `sarama.NewSyncProducer([]string{"kafka:9092"}, config)`

### Java Kafka Producer
**Type**: semgrep
**Severity**: info
**Languages**: [java]
**Pattern**: `new KafkaProducer<>($PROPS)`
- Creates Kafka producer
- Example: `new KafkaProducer<>(props)`

### Java Kafka Consumer
**Type**: semgrep
**Severity**: info
**Languages**: [java]
**Pattern**: `new KafkaConsumer<>($PROPS)`
- Creates Kafka consumer
- Example: `new KafkaConsumer<>(props)`

### Spring Kafka Listener
**Type**: semgrep
**Severity**: info
**Languages**: [java]
**Pattern**: `@KafkaListener(topics = $TOPICS, ...)`
- Spring Kafka topic listener
- Example: `@KafkaListener(topics = "orders", groupId = "order-service")`
- Captures: Topics, consumer group

---

## RabbitMQ

### Python Pika Connection
**Type**: semgrep
**Severity**: info
**Languages**: [python]
**Pattern**: `pika.BlockingConnection(pika.ConnectionParameters($HOST, ...))`
- Creates RabbitMQ connection
- Example: `pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))`

### Python Queue Declare
**Type**: semgrep
**Severity**: info
**Languages**: [python]
**Pattern**: `$CHANNEL.queue_declare(queue=$QUEUE, ...)`
- Declares RabbitMQ queue
- Example: `channel.queue_declare(queue='order_queue')`
- Captures: Queue name

### Python Basic Publish
**Type**: semgrep
**Severity**: info
**Languages**: [python]
**Pattern**: `$CHANNEL.basic_publish(exchange=$EXCHANGE, routing_key=$KEY, ...)`
- Publishes message to RabbitMQ
- Example: `channel.basic_publish(exchange='', routing_key='orders', body=message)`
- Captures: Exchange, routing key

### Python Basic Consume
**Type**: semgrep
**Severity**: info
**Languages**: [python]
**Pattern**: `$CHANNEL.basic_consume(queue=$QUEUE, ...)`
- Consumes from RabbitMQ queue
- Example: `channel.basic_consume(queue='orders', on_message_callback=callback)`

### JavaScript amqplib Connect
**Type**: semgrep
**Severity**: info
**Languages**: [javascript, typescript]
**Pattern**: `amqp.connect($URL)`
- Connects to RabbitMQ
- Example: `amqp.connect('amqp://rabbitmq')`

### JavaScript Send to Queue
**Type**: semgrep
**Severity**: info
**Languages**: [javascript, typescript]
**Pattern**: `$CHANNEL.sendToQueue($QUEUE, ...)`
- Sends message to queue
- Example: `channel.sendToQueue('orders', Buffer.from(message))`

### Go RabbitMQ Dial
**Type**: semgrep
**Severity**: info
**Languages**: [go]
**Pattern**: `amqp.Dial($URL)`
- Connects to RabbitMQ
- Example: `amqp.Dial("amqp://guest:guest@rabbitmq:5672/")`

### Spring AMQP Listener
**Type**: semgrep
**Severity**: info
**Languages**: [java]
**Pattern**: `@RabbitListener(queues = $QUEUES, ...)`
- Spring AMQP queue listener
- Example: `@RabbitListener(queues = "order-queue")`
- Captures: Queue names

### Spring AMQP Handler
**Type**: semgrep
**Severity**: info
**Languages**: [java]
**Pattern**: `@RabbitHandler`
- Marks RabbitMQ message handler
- Example: `@RabbitHandler public void process(Order order)`

---

## AWS SQS

### Python Boto3 SQS Send
**Type**: semgrep
**Severity**: info
**Languages**: [python]
**Pattern**: `$CLIENT.send_message(QueueUrl=$QUEUE, ...)`
- Sends SQS message
- Example: `sqs.send_message(QueueUrl=queue_url, MessageBody=json.dumps(event))`

### Python Boto3 SQS Receive
**Type**: semgrep
**Severity**: info
**Languages**: [python]
**Pattern**: `$CLIENT.receive_message(QueueUrl=$QUEUE, ...)`
- Receives SQS messages
- Example: `sqs.receive_message(QueueUrl=queue_url, MaxNumberOfMessages=10)`

### JavaScript AWS SDK SQS Send
**Type**: semgrep
**Severity**: info
**Languages**: [javascript, typescript]
**Pattern**: `$SQS.sendMessage($PARAMS)`
- Sends SQS message
- Example: `sqs.sendMessage({ QueueUrl, MessageBody })`

### Go AWS SDK SQS
**Type**: semgrep
**Severity**: info
**Languages**: [go]
**Pattern**: `$SQS.SendMessage($CTX, $INPUT)`
- Sends SQS message in Go
- Example: `sqs.SendMessage(ctx, &sqs.SendMessageInput{QueueUrl: &queueURL})`

---

## Redis Pub/Sub

### Python Redis Publish
**Type**: semgrep
**Severity**: info
**Languages**: [python]
**Pattern**: `$REDIS.publish($CHANNEL, ...)`
- Publishes to Redis channel
- Example: `redis.publish('notifications', json.dumps(event))`

### Python Redis Subscribe
**Type**: semgrep
**Severity**: info
**Languages**: [python]
**Pattern**: `$PUBSUB.subscribe($CHANNEL)`
- Subscribes to Redis channel
- Example: `pubsub.subscribe('notifications')`

### JavaScript Redis Publish
**Type**: semgrep
**Severity**: info
**Languages**: [javascript, typescript]
**Pattern**: `$REDIS.publish($CHANNEL, ...)`
- Publishes to Redis channel
- Example: `redis.publish('events', JSON.stringify(data))`

### Go Redis Publish
**Type**: semgrep
**Severity**: info
**Languages**: [go]
**Pattern**: `$CLIENT.Publish($CTX, $CHANNEL, ...)`
- Publishes to Redis channel in Go
- Example: `rdb.Publish(ctx, "notifications", message)`

---

## NATS

### Go NATS Publish
**Type**: semgrep
**Severity**: info
**Languages**: [go]
**Pattern**: `$NC.Publish($SUBJECT, ...)`
- Publishes to NATS subject
- Example: `nc.Publish("orders.created", data)`

### Go NATS Subscribe
**Type**: semgrep
**Severity**: info
**Languages**: [go]
**Pattern**: `$NC.Subscribe($SUBJECT, ...)`
- Subscribes to NATS subject
- Example: `nc.Subscribe("orders.*", handler)`

### Python NATS Publish
**Type**: semgrep
**Severity**: info
**Languages**: [python]
**Pattern**: `await $NC.publish($SUBJECT, ...)`
- Publishes to NATS in Python
- Example: `await nc.publish("events.user", payload)`

---

## Google Cloud Pub/Sub

### Python Pub/Sub Publish
**Type**: semgrep
**Severity**: info
**Languages**: [python]
**Pattern**: `$PUBLISHER.publish($TOPIC, ...)`
- Publishes to GCP Pub/Sub
- Example: `publisher.publish(topic_path, data.encode())`

### Python Pub/Sub Subscribe
**Type**: semgrep
**Severity**: info
**Languages**: [python]
**Pattern**: `$SUBSCRIBER.subscribe($SUBSCRIPTION, ...)`
- Subscribes to GCP Pub/Sub
- Example: `subscriber.subscribe(subscription_path, callback)`

### Go Pub/Sub Publish
**Type**: semgrep
**Severity**: info
**Languages**: [go]
**Pattern**: `$TOPIC.Publish($CTX, ...)`
- Publishes to GCP Pub/Sub in Go
- Example: `topic.Publish(ctx, &pubsub.Message{Data: data})`

---

## Detection Confidence

**Kafka Detection**: 95%
**RabbitMQ Detection**: 90%
**Cloud Queues Detection**: 85%

---

## References

- Apache Kafka Documentation
- RabbitMQ Documentation
- AWS SQS Developer Guide
- NATS Documentation
