## Python Consumer Examples

### Basic Consumer
```python
from kafka import KafkaConsumer
import json

# Create consumer
consumer = KafkaConsumer(
    'my-topic',
    group_id='my-consumer-group',
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='earliest',  # Start from beginning if no committed offsets
    enable_auto_commit=False  # Manual offset management
)

# Consume messages
for message in consumer:
    # message value and key are raw bytes -- decode if necessary
    key = message.key.decode('utf-8') if message.key else None
    value = message.value.decode('utf-8')

    print(f'Consumed record: key={key}, value={value}, '
          f'partition={message.partition}, offset={message.offset}')

    # Process the record
    process_record(message)

    # Manually commit offsets after processing
    # consumer.commit()

def process_record(message):
    """Process an individual record/message"""
    # Add your message processing logic here
    pass
```

### JSON Deserializing Consumer
```python
# Consumer with JSON deserialization
json_consumer = KafkaConsumer(
    'my-topic',
    group_id='json-consumer-group',
    bootstrap_servers=['localhost:9092'],
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)
```

### Multiple Topics Subscription
```python
# Subscribe to multiple topics
consumer.subscribe(topics=['topic1', 'topic2'])
```

### Pattern-based Subscription
```python
# Subscribe to topics matching a pattern
consumer.subscribe(pattern='^my-topic.*')
```

### SSL Encrypted Consumer
```python
# Python consumer with SSL configuration
consumer = KafkaConsumer(
    'my-topic',
    group_id='secure-consumer-group',
    bootstrap_servers=['localhost:9092'],
    security_protocol='SSL',
    ssl_cafile='/path/to/ca-cert',
    ssl_certfile='/path/to/client-cert.pem',
    ssl_keyfile='/path/to/client-key.pem',
    ssl_password='key-password',  # if key file is encrypted
    auto_offset_reset='earliest'
)
```

### SASL/PLAIN Authenticated Consumer
```python
# Python consumer with SASL/PLAIN authentication
consumer = KafkaConsumer(
    'my-topic',
    group_id='plain-consumer-group',
    bootstrap_servers=['localhost:9092'],
    security_protocol='SASL_PLAINTEXT',  # or SASL_SSL for encrypted
    sasl_mechanism='PLAIN',
    sasl_plain_username='username',
    sasl_plain_password='password',
    auto_offset_reset='earliest'
)
```

### SASL/GSSAPI (Kerberos) Consumer
```python
# Python configuration for SASL/GSSAPI (Kerberos)
consumer = KafkaConsumer(
    'my-topic',
    group_id='kerberos-consumer-group',
    bootstrap_servers=['localhost:9092'],
    security_protocol='SASL_PLAINTEXT',  # or SASL_SSL
    sasl_mechanism='GSSAPI',
    sasl_kerberos_service_name='kafka'
)
# Note: Kerberos must be properly configured on the system
```

### Exactly-Once Consumer
```python
# Configure consumer for exactly-once processing
consumer = KafkaConsumer(
    'input-topic',
    group_id='exactly-once-consumer',
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='earliest',
    enable_auto_commit=False  # Manual offset management for exactly-once
)

try:
    for message in consumer:
        # Process the message
        processed_value = process_message(message.value)

        # Send to output topic
        future = producer.send('output-topic', processed_value)
        record_metadata = future.get(timeout=10)  # Wait for acknowledgment

        # Commit offset only after successful processing and sending
        consumer.commit()

except KeyboardInterrupt:
    print("Processing interrupted")
finally:
    consumer.close()

def process_message(value):
    # Add your message processing logic here
    return value
```
