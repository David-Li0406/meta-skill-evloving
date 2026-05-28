---
id: message-queues
name: "Message Queues"
domain: DEV
skill: faion-software-developer
category: "development"
---

# Message Queues

## Overview

Message queues enable asynchronous communication between services, providing decoupling, load leveling, and reliability. This methodology covers queue patterns, implementation with popular brokers (RabbitMQ, Redis, SQS, Kafka), and best practices for reliable message processing.

## When to Use

- Decoupling services in distributed systems
- Handling background jobs and async processing
- Load leveling during traffic spikes
- Event-driven architectures
- Reliable delivery requirements (at-least-once, exactly-once)

## Key Principles

- **Design for idempotency**: Messages may be delivered multiple times
- **Handle failures gracefully**: Dead letter queues, retries, circuit breakers
- **Monitor queue depth**: Growing queues indicate processing issues
- **Right-size consumers**: Balance throughput with resource usage
- **Preserve message ordering**: When business logic requires it

## Best Practices

### Queue Patterns

```
1. Point-to-Point (Work Queue)
   Producer → Queue → Consumer (one consumer processes each message)

2. Publish/Subscribe (Fan-out)
   Producer → Exchange → Queue1 → Consumer1
                      → Queue2 → Consumer2

3. Request/Reply
   Client → Request Queue → Server
   Client ← Reply Queue ← Server

4. Dead Letter Queue
   Producer → Main Queue → Consumer
                        ↓ (failed)
                   DLQ → Error Handler
```

### RabbitMQ Implementation

```python
import pika
import json
from typing import Callable, Optional
from dataclasses import dataclass
from functools import wraps
import time

@dataclass
class QueueConfig:
    name: str
    durable: bool = True
    exclusive: bool = False
    auto_delete: bool = False
    dead_letter_exchange: Optional[str] = None
    message_ttl: Optional[int] = None

class RabbitMQClient:
    def __init__(self, host: str = 'localhost', port: int = 5672):
        self.connection_params = pika.ConnectionParameters(
            host=host,
            port=port,
            heartbeat=600,
            blocked_connection_timeout=300
        )
        self._connection = None
        self._channel = None

    @property
    def channel(self):
        if not self._connection or self._connection.is_closed:
            self._connection = pika.BlockingConnection(self.connection_params)
            self._channel = self._connection.channel()
            self._channel.basic_qos(prefetch_count=10)
        return self._channel

    def declare_queue(self, config: QueueConfig):
        arguments = {}
        if config.dead_letter_exchange:
            arguments['x-dead-letter-exchange'] = config.dead_letter_exchange
        if config.message_ttl:
            arguments['x-message-ttl'] = config.message_ttl

        self.channel.queue_declare(
            queue=config.name,
            durable=config.durable,
            exclusive=config.exclusive,
            auto_delete=config.auto_delete,
            arguments=arguments or None
        )

    def publish(self, queue: str, message: dict, persistent: bool = True):
        properties = pika.BasicProperties(
            delivery_mode=2 if persistent else 1,  # 2 = persistent
            content_type='application/json'
        )

        self.channel.basic_publish(
            exchange='',
            routing_key=queue,
            body=json.dumps(message),
            properties=properties
        )

    def consume(self, queue: str, callback: Callable, auto_ack: bool = False):
        def wrapper(ch, method, properties, body):
            try:
                message = json.loads(body)
                callback(message)
                if not auto_ack:
                    ch.basic_ack(delivery_tag=method.delivery_tag)
            except Exception as e:
                if not auto_ack:
                    # Reject and requeue or send to DLQ
                    ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
                raise

        self.channel.basic_consume(
            queue=queue,
            on_message_callback=wrapper,
            auto_ack=auto_ack
        )
        self.channel.start_consuming()

# Usage
client = RabbitMQClient()

# Setup queues with DLQ
client.declare_queue(QueueConfig(
    name='orders.dlq',
    durable=True
))
client.declare_queue(QueueConfig(
    name='orders',
    durable=True,
    dead_letter_exchange='',
    dead_letter_routing_key='orders.dlq'
))

# Publish
client.publish('orders', {'order_id': '123', 'action': 'process'})

# Consume
def process_order(message):
    print(f"Processing order: {message['order_id']}")

client.consume('orders', process_order)
```

### Redis Streams for Event Sourcing

```python
import redis
from typing import Optional, List, Dict, Callable
from dataclasses import dataclass
import json

@dataclass
class StreamMessage:
    id: str
    data: Dict

class RedisStreamClient:
    def __init__(self, host: str = 'localhost', port: int = 6379):
        self.redis = redis.Redis(host=host, port=port, decode_responses=True)

    def create_consumer_group(self, stream: str, group: str):
        try:
            self.redis.xgroup_create(stream, group, id='0', mkstream=True)
        except redis.exceptions.ResponseError as e:
            if 'BUSYGROUP' not in str(e):
                raise

    def publish(self, stream: str, data: dict, max_len: int = 10000) -> str:
        return self.redis.xadd(stream, data, maxlen=max_len, approximate=True)

    def consume(
        self,
        stream: str,
        group: str,
        consumer: str,
        callback: Callable[[StreamMessage], bool],
        batch_size: int = 10,
        block_ms: int = 5000
    ):
        while True:
            messages = self.redis.xreadgroup(
                groupname=group,
                consumername=consumer,
                streams={stream: '>'},
                count=batch_size,
                block=block_ms
            )

            if not messages:
                continue

            for stream_name, stream_messages in messages:
                for msg_id, data in stream_messages:
                    message = StreamMessage(id=msg_id, data=data)
                    try:
                        if callback(message):
                            self.redis.xack(stream, group, msg_id)
                        else:
                            # Handle failed processing
                            pass
                    except Exception as e:
                        # Log error, message will be reclaimed after timeout
                        print(f"Error processing {msg_id}: {e}")

    def claim_pending(
        self,
        stream: str,
        group: str,
        consumer: str,
        min_idle_ms: int = 60000,
        count: int = 10
    ) -> List[StreamMessage]:
        """Claim messages that other consumers failed to process."""
        pending = self.redis.xpending_range(
            stream, group, '-', '+', count
        )

        if not pending:
            return []

        message_ids = [
            msg['message_id'] for msg in pending
            if msg['time_since_delivered'] > min_idle_ms
        ]

        if not message_ids:
            return []

        claimed = self.redis.xclaim(
            stream, group, consumer, min_idle_ms, message_ids
        )

        return [StreamMessage(id=msg_id, data=data) for msg_id, data in claimed]

# Usage
stream_client = RedisStreamClient()

# Create consumer group
stream_client.create_consumer_group('events', 'processors')

# Publish events
stream_client.publish('events', {
    'type': 'order_created',
    'order_id': '123',
    'user_id': '456',
    'total': '99.99'
})

# Consume events
def process_event(message: StreamMessage) -> bool:
    print(f"Processing: {message.data}")
    return True  # Return True to acknowledge

stream_client.consume('events', 'processors', 'worker-1', process_event)
```

### Celery Task Queue

```python
from celery import Celery, Task
from celery.exceptions import MaxRetriesExceededError
import logging

app = Celery(
    'tasks',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/1'
)

app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    task_acks_late=True,  # Acknowledge after processing
    task_reject_on_worker_lost=True,
    worker_prefetch_multiplier=1,  # One task at a time per worker
)

class BaseTask(Task):
    """Base task with automatic retries and error handling."""

    autoretry_for = (Exception,)
    retry_backoff = True
    retry_backoff_max = 600
    retry_jitter = True
    max_retries = 5

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        logging.error(f"Task {task_id} failed: {exc}")
        # Send to error tracking service
        notify_error(exc, task_id, args, kwargs)

@app.task(base=BaseTask, bind=True)
def process_order(self, order_id: str):
    """Process an order with automatic retries."""
    try:
        order = get_order(order_id)
        validate_order(order)
        charge_payment(order)
        send_confirmation(order)
        return {'status': 'completed', 'order_id': order_id}
    except PaymentError as e:
        # Specific retry logic for payment failures
        raise self.retry(exc=e, countdown=60)
    except ValidationError as e:
        # Don't retry validation errors
        return {'status': 'failed', 'error': str(e)}

@app.task(bind=True)
def send_email(self, to: str, subject: str, body: str):
    """Send email with retry on failure."""
    send_email_via_smtp(to, subject, body)

# Chain tasks
from celery import chain, group, chord

# Sequential execution
workflow = chain(
    process_order.s(order_id),
    send_confirmation_email.s(),
    update_analytics.s()
)
workflow.apply_async()

# Parallel execution
parallel = group(
    send_email.s(email1),
    send_email.s(email2),
    send_email.s(email3)
)
parallel.apply_async()

# Parallel then callback
chord_workflow = chord(
    [process_item.s(item_id) for item_id in items],
    finalize_batch.s()
)
chord_workflow.apply_async()

# Periodic tasks
from celery.schedules import crontab

app.conf.beat_schedule = {
    'cleanup-expired-sessions': {
        'task': 'tasks.cleanup_sessions',
        'schedule': crontab(hour=3, minute=0),  # Daily at 3 AM
    },
    'send-daily-digest': {
        'task': 'tasks.send_digest',
        'schedule': crontab(hour=8, minute=0),
    },
}
```

### AWS SQS with Dead Letter Queue

```python
import boto3
import json
from typing import Callable, Optional
import time

class SQSClient:
    def __init__(self, region: str = 'us-east-1'):
        self.sqs = boto3.client('sqs', region_name=region)

    def create_queue_with_dlq(
        self,
        queue_name: str,
        dlq_name: str,
        max_receive_count: int = 3
    ) -> tuple[str, str]:
        # Create DLQ first
        dlq_response = self.sqs.create_queue(
            QueueName=dlq_name,
            Attributes={
                'MessageRetentionPeriod': '1209600',  # 14 days
            }
        )
        dlq_url = dlq_response['QueueUrl']

        # Get DLQ ARN
        dlq_attrs = self.sqs.get_queue_attributes(
            QueueUrl=dlq_url,
            AttributeNames=['QueueArn']
        )
        dlq_arn = dlq_attrs['Attributes']['QueueArn']

        # Create main queue with DLQ redrive policy
        redrive_policy = {
            'deadLetterTargetArn': dlq_arn,
            'maxReceiveCount': str(max_receive_count)
        }

        queue_response = self.sqs.create_queue(
            QueueName=queue_name,
            Attributes={
                'VisibilityTimeout': '30',
                'MessageRetentionPeriod': '345600',  # 4 days
                'RedrivePolicy': json.dumps(redrive_policy)
            }
        )

        return queue_response['QueueUrl'], dlq_url

    def send_message(
        self,
        queue_url: str,
        body: dict,
        delay_seconds: int = 0,
        deduplication_id: Optional[str] = None
    ):
        params = {
            'QueueUrl': queue_url,
            'MessageBody': json.dumps(body),
            'DelaySeconds': delay_seconds
        }

        if deduplication_id:
            params['MessageDeduplicationId'] = deduplication_id

        return self.sqs.send_message(**params)

    def receive_and_process(
        self,
        queue_url: str,
        callback: Callable[[dict], bool],
        batch_size: int = 10,
        wait_time: int = 20
    ):
        while True:
            response = self.sqs.receive_message(
                QueueUrl=queue_url,
                MaxNumberOfMessages=batch_size,
                WaitTimeSeconds=wait_time,
                AttributeNames=['All'],
                MessageAttributeNames=['All']
            )

            messages = response.get('Messages', [])

            for message in messages:
                body = json.loads(message['Body'])
                receipt_handle = message['ReceiptHandle']

                try:
                    if callback(body):
                        self.sqs.delete_message(
                            QueueUrl=queue_url,
                            ReceiptHandle=receipt_handle
                        )
                except Exception as e:
                    # Message will become visible again after visibility timeout
                    print(f"Error processing message: {e}")

            if not messages:
                time.sleep(1)

# Usage
client = SQSClient()
queue_url, dlq_url = client.create_queue_with_dlq('orders', 'orders-dlq')

# Send message
client.send_message(queue_url, {
    'order_id': '123',
    'action': 'process'
})

# Process messages
def handler(message: dict) -> bool:
    print(f"Processing: {message}")
    return True

client.receive_and_process(queue_url, handler)
```

## Anti-patterns

- **No idempotency**: Assuming exactly-once delivery
- **Unbounded retries**: Poison messages blocking the queue
- **Missing DLQ**: Failed messages lost forever
- **Large messages**: Queues aren't for large payloads (use S3 + reference)
- **Synchronous expectations**: Using queues for request-response
- **No monitoring**: Queue depth, processing rate, error rate
- **Missing correlation IDs**: Can't trace messages through system

## References

- [RabbitMQ Tutorials](https://www.rabbitmq.com/tutorials)
- [Redis Streams](https://redis.io/docs/data-types/streams/)
- [Celery Documentation](https://docs.celeryq.dev/)
- [AWS SQS Best Practices](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-best-practices.html)
- [Enterprise Integration Patterns](https://www.enterpriseintegrationpatterns.com/)
