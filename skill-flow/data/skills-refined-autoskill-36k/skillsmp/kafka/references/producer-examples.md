## Python Producer Examples

### Basic Producer
```python
from kafka import KafkaProducer
from kafka.errors import KafkaError
import json

# Create producer
producer = KafkaProducer(bootstrap_servers=['localhost:9092'])

# Asynchronous send
future = producer.send('my-topic', key=b'1', value=b'hello world')

# Block for synchronous send
try:
    record_metadata = future.get(timeout=10)
    print(f'Message delivered to {record_metadata.topic} [{record_metadata.partition}] at offset {record_metadata.offset}')
except KafkaError as e:
    print(f'Message delivery failed: {e}')
```

### JSON Messages Producer
```python
# Send JSON messages
json_producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda m: json.dumps(m).encode('ascii')
)
json_producer.send('my-topic', {'message': 'hello world'})
```

### Producer with Key for Partitioning
```python
# Send with key for partitioning
producer.send('my-topic', key=b'user123', value=b'important message')
```

### Multiple Asynchronous Messages
```python
# Send multiple messages asynchronously
for i in range(10):
    producer.send('my-topic', value=f'message {i}'.encode('utf-8'))

# Block until all async messages are sent
producer.flush()

# Close producer
producer.close()
```

### Idempotent Producer for Exactly-Once Delivery
```python
# Configure idempotent producer for exactly-once delivery
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    enable_idempotence=True,  # Ensures exactly-once delivery semantics
    acks='all',  # Wait for all replicas to acknowledge
    retries=2147483647  # Maximum retries
)
```

### SSL Encrypted Producer
```python
# Python producer with SSL configuration
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    security_protocol='SSL',
    ssl_cafile='/path/to/ca-cert',
    ssl_certfile='/path/to/client-cert.pem',
    ssl_keyfile='/path/to/client-key.pem',
    ssl_password='key-password'  # if key file is encrypted
)
```

### SASL/PLAIN Authenticated Producer
```python
# Python producer with SASL/PLAIN authentication
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    security_protocol='SASL_PLAINTEXT',  # or SASL_SSL for encrypted
    sasl_mechanism='PLAIN',
    sasl_plain_username='username',
    sasl_plain_password='password'
)
```

### SASL/SCRAM Authenticated Producer
```python
# Python configuration for SASL/SCRAM
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    security_protocol='SASL_SSL',  # or SASL_PLAINTEXT
    sasl_mechanism='SCRAM-SHA-256',  # or 'SCRAM-SHA-512'
    sasl_plain_username='username',
    sasl_plain_password='password'
)
```
