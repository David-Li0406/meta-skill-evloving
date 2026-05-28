"""
Kafka Python Examples
This file contains simple examples of Kafka producers and consumers using the kafka-python library.
"""

from kafka import KafkaProducer, KafkaConsumer
import json
import time

def create_producer():
    """Create a Kafka producer instance."""
    producer = KafkaProducer(
        bootstrap_servers=['localhost:9092'],
        value_serializer=lambda v: json.dumps(v).encode('utf-8'),
        key_serializer=lambda k: json.dumps(k).encode('utf-8') if k else None
    )
    return producer

def create_consumer(topic_name, group_id='python-consumer-group'):
    """Create a Kafka consumer instance."""
    consumer = KafkaConsumer(
        topic_name,
        bootstrap_servers=['localhost:9092'],
        group_id=group_id,
        value_deserializer=lambda m: json.loads(m.decode('utf-8')),
        key_deserializer=lambda k: json.loads(k.decode('utf-8')) if k else None,
        auto_offset_reset='earliest'
    )
    return consumer

def send_message(producer, topic, key, value):
    """Send a single message to Kafka."""
    future = producer.send(topic, key=key, value=value)
    result = future.get(timeout=10)
    print(f'Message sent to partition {result.partition}, offset {result.offset}')
    return result

def send_batch_messages(producer, topic, messages):
    """Send multiple messages to Kafka."""
    for msg in messages:
        send_message(producer, topic, msg['key'], msg['value'])
        time.sleep(0.1)  # Small delay between messages

def consume_messages(consumer, max_messages=None):
    """Consume messages from Kafka topic."""
    message_count = 0
    try:
        for message in consumer:
            print(f'Received message: Key={message.key}, Value={message.value}, '
                  f'Partition={message.partition}, Offset={message.offset}')

            message_count += 1
            if max_messages and message_count >= max_messages:
                break

    except KeyboardInterrupt:
        print("Consumer interrupted by user")
    finally:
        consumer.close()

# Example usage
if __name__ == "__main__":
    # Create producer and send messages
    producer = create_producer()

    # Sample messages to send
    sample_messages = [
        {'key': 'user-1', 'value': {'action': 'login', 'timestamp': time.time()}},
        {'key': 'user-2', 'value': {'action': 'purchase', 'amount': 99.99}},
        {'key': 'user-3', 'value': {'action': 'logout', 'duration': 1200}}
    ]

    print("Sending sample messages...")
    send_batch_messages(producer, 'sample-topic', sample_messages)
    producer.flush()
    producer.close()

    # Create consumer and receive messages
    print("\nStarting consumer...")
    consumer = create_consumer('sample-topic')
    consume_messages(consumer, max_messages=3)