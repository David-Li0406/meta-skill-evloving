## Kafka Admin Client Examples

### Topic Management
```python
from kafka import KafkaAdminClient
from kafka.admin import NewTopic
import uuid

# Create admin client
admin_client = KafkaAdminClient(bootstrap_servers=['localhost:9092'])

# Create topic with custom configuration
topic_name = f"my-topic-{str(uuid.uuid4())}"
num_partitions = 12
replication_factor = 3

# Define topic configuration
config = {
    'cleanup.policy': 'compact',  # Use 'compact' for key-value stores
    'retention.ms': '86400000',  # 1 day retention
    'compression.type': 'gzip'
}

# Create new topic
new_topic = NewTopic(
    name=topic_name,
    num_partitions=num_partitions,
    replication_factor=replication_factor,
    topic_configs=config
)

# Create topics
try:
    admin_client.create_topics([new_topic], validate_only=False)
    print(f"Topic {topic_name} created successfully")
except Exception as e:
    print(f"Failed to create topic {topic_name}: {e}")

# Delete topic
try:
    admin_client.delete_topics([topic_name])
    print(f"Topic {topic_name} deleted successfully")
except Exception as e:
    print(f"Failed to delete topic {topic_name}: {e}")
```

### Multiple Topics Creation
```python
# Create multiple topics
topics_list = [
    NewTopic(name="topic1", num_partitions=3, replication_factor=1),
    NewTopic(name="topic2", num_partitions=5, replication_factor=1)
]
admin_client.create_topics(topics_list)
```

### Consumer Group Operations
```python
# List consumer groups
consumer_groups = admin_client.list_consumer_groups()
print("Consumer groups:", consumer_groups)

# Describe consumer groups
group_details = admin_client.describe_consumer_groups(['my-group'])
print("Group details:", group_details)
```

### Using Command Line Tools
You can also manage topics using Kafka's command line tools:

```bash
# Create a topic
kafka-topics --create --topic my-topic --bootstrap-server localhost:9092 --partitions 3 --replication-factor 1

# List all topics
kafka-topics --list --bootstrap-server localhost:9092

# Describe a topic
kafka-topics --describe --topic my-topic --bootstrap-server localhost:9092

# Delete a topic
kafka-topics --delete --topic my-topic --bootstrap-server localhost:9092
```
