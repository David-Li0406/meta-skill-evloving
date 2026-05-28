## Kafka Stream Processing with Python

For stream processing applications in Python, kafka-python doesn't have a direct equivalent to the Java Kafka Streams library. However, you can implement stream processing patterns using the kafka-python library:

### Basic Stream Processing Pattern
```python
from kafka import KafkaConsumer, KafkaProducer
from collections import defaultdict
import json

# Configuration
consumer = KafkaConsumer(
    'input-topic',
    bootstrap_servers=['localhost:9092'],
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    auto_offset_reset='earliest',
    enable_auto_commit=False
)

producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda m: json.dumps(m).encode('utf-8')
)

try:
    for message in consumer:
        # Process the incoming message
        data = message.value
        processed_data = process_message(data)

        # Send to output topic
        producer.send('output-topic', processed_data)

        # Commit offset after successful processing
        consumer.commit()

except KeyboardInterrupt:
    print("Processing stopped by user")
finally:
    consumer.close()
    producer.close()

def process_message(data):
    # Add your stream processing logic here
    return data
```

### Word Count Stream Processor
```python
from kafka import KafkaConsumer, KafkaProducer
import json

# Initialize consumer and producer
consumer = KafkaConsumer(
    'streams-plaintext-input',
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='earliest',
    enable_auto_commit=False
)

producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda m: json.dumps(m).encode('utf-8')
)

word_counts = {}

for message in consumer:
    text = message.value.decode('utf-8')
    words = text.lower().split()

    for word in words:
        # Update word count
        current_count = word_counts.get(word, 0) + 1
        word_counts[word] = current_count

        # Send word count to output topic
        output_data = {'word': word, 'count': current_count}
        producer.send('streams-wordcount-output', output_data)

    # Commit offset after processing batch
    consumer.commit()
```

### Alternative: Faust for Advanced Stream Processing
For more sophisticated stream processing, you can use Faust which provides a Kafka Streams-like API:

```python
import faust

# Define the application
app = faust.App(
    'my-stream-processing-app',
    broker='kafka://localhost:9092',
    store='rocksdb://'
)

# Define a model for the data
class WordCount(faust.Record):
    word: str
    count: int

# Define source and sink topics
source_topic = app.topic('streams-plaintext-input', value_type=str)
sink_topic = app.topic('streams-wordcount-output', value_type=WordCount)

# Define a table to hold the counts
word_counts = app.Table('word_counts', default=int)

@app.agent(source_topic)
async def process_words(words):
    async for word in words.group_by(lambda value: value):
        word_counts[word] += 1
        print(f'{word} => {word_counts[word]}')
        # Publish to output topic
        await sink_topic.send(value=WordCount(word=word, count=word_counts[word]))

if __name__ == '__main__':
    app.main()
```

To install Faust:
```bash
pip install faust
```
