# AWS Stream Processing Examples

Practical examples showing how to implement stream processing concepts using AWS services in the sandbox environment.

## Core AWS Services for Stream Processing

- **Amazon Kinesis Data Streams**: Managed data streaming service (like Kafka)
- **Amazon Kinesis Firehose**: Load streaming data into destinations
- **Amazon SQS**: Message queue service
- **Amazon SNS**: Pub/sub messaging service
- **AWS Lambda**: Serverless stream processing
- **Amazon DynamoDB Streams**: CDC from DynamoDB tables
- **Amazon MSK**: Managed Apache Kafka

## Concept-to-AWS Mapping

| DDIA Concept | AWS Implementation |
|--------------|-------------------|
| Partitioned Log | Kinesis Data Stream with shards |
| Message Broker | SQS, SNS, or MSK |
| Stream Processor | Lambda, Kinesis Data Analytics |
| Change Data Capture | DynamoDB Streams, RDS CDC to Kinesis |
| Event Sourcing | Events in Kinesis/S3 with replay |
| Consumer Groups | Kinesis with multiple consumers |
| Log Compaction | S3 with lifecycle policies |

## Hands-On Examples

### Example 1: Creating a Simple Event Stream (Partitioned Log)

**Concept**: Chapter 11 discusses partitioned logs as the foundation of stream processing.

**Python (Recommended for experimentation)**:
```python
import boto3
import json
from datetime import datetime

kinesis = boto3.client('kinesis', region_name='us-east-1')

# Create a Kinesis stream with 2 shards (partitions)
kinesis.create_stream(StreamName='user-events', ShardCount=2)

# Describe the stream
response = kinesis.describe_stream(StreamName='user-events')
print(f"Stream Status: {response['StreamDescription']['StreamStatus']}")
print(f"Shards: {len(response['StreamDescription']['Shards'])}")

# Put a record (event) into the stream
event = {
    'userId': 'user123',
    'action': 'login',
    'timestamp': datetime.utcnow().isoformat() + 'Z'
}

response = kinesis.put_record(
    StreamName='user-events',
    Data=json.dumps(event),
    PartitionKey='user123'
)
print(f"Event sent to: {response['ShardId']}")

# Read records from the stream
shard_iterator_response = kinesis.get_shard_iterator(
    StreamName='user-events',
    ShardId='shardId-000000000000',
    ShardIteratorType='TRIM_HORIZON'
)

records_response = kinesis.get_records(
    ShardIterator=shard_iterator_response['ShardIterator']
)

for record in records_response['Records']:
    data = json.loads(record['Data'])
    print(f"Read event: {data}")
```

**AWS CLI (for reference)**:
```bash
# Create a Kinesis stream with 2 shards (partitions)
aws kinesis create-stream \
  --stream-name user-events \
  --shard-count 2

# Describe the stream
aws kinesis describe-stream --stream-name user-events

# Put a record (event) into the stream
aws kinesis put-record \
  --stream-name user-events \
  --partition-key user123 \
  --data '{"userId":"user123","action":"login","timestamp":"2024-01-21T10:00:00Z"}'

# Read records from the stream
SHARD_ITERATOR=$(aws kinesis get-shard-iterator \
  --stream-name user-events \
  --shard-id shardId-000000000000 \
  --shard-iterator-type TRIM_HORIZON \
  --query 'ShardIterator' \
  --output text)

aws kinesis get-records --shard-iterator $SHARD_ITERATOR
```

**Key concepts demonstrated**:
- Partitioned log (shards)
- Partition key determines which partition
- Sequential reads per partition
- Retention (24hrs default, up to 365 days)

### Example 2: Fan-Out Pattern with SNS

**Concept**: Chapter 11 discusses fan-out where multiple consumers get same message.

**AWS CLI**:
```bash
# Create SNS topic
aws sns create-topic --name order-events

# Create multiple SQS queues (different consumers)
aws sqs create-queue --queue-name warehouse-processor
aws sqs create-queue --queue-name analytics-processor
aws sqs create-queue --queue-name notification-processor

# Subscribe queues to topic
TOPIC_ARN=$(aws sns list-topics --query "Topics[?contains(TopicArn, 'order-events')].TopicArn" --output text)
WAREHOUSE_ARN=$(aws sqs get-queue-attributes --queue-url $(aws sqs get-queue-url --queue-name warehouse-processor --query QueueUrl --output text) --attribute-names QueueArn --query Attributes.QueueArn --output text)

aws sns subscribe \
  --topic-arn $TOPIC_ARN \
  --protocol sqs \
  --notification-endpoint $WAREHOUSE_ARN

# Publish event (all subscribers get it)
aws sns publish \
  --topic-arn $TOPIC_ARN \
  --message '{"orderId":"order456","items":[{"sku":"ITEM1","qty":2}]}'
```

**Key concepts demonstrated**:
- Fan-out messaging pattern
- Decoupled producers and consumers
- Each consumer gets independent copy

### Example 3: Change Data Capture with DynamoDB Streams

**Concept**: Chapter 11 discusses CDC as a way to capture database changes as events.

**AWS CLI**:
```bash
# Create DynamoDB table with streams enabled
aws dynamodb create-table \
  --table-name users \
  --attribute-definitions AttributeName=userId,AttributeType=S \
  --key-schema AttributeName=userId,KeyType=HASH \
  --billing-mode PAY_PER_REQUEST \
  --stream-specification StreamEnabled=true,StreamViewType=NEW_AND_OLD_IMAGES

# Put an item (this creates a change event)
aws dynamodb put-item \
  --table-name users \
  --item '{"userId":{"S":"user789"},"email":{"S":"user@example.com"},"status":{"S":"active"}}'

# Get the stream ARN
STREAM_ARN=$(aws dynamodb describe-table --table-name users --query Table.LatestStreamArn --output text)

# Describe the stream
aws dynamodbstreams describe-stream --stream-arn $STREAM_ARN

# Get records from stream (would be processed by Lambda in practice)
SHARD_ID=$(aws dynamodbstreams describe-stream --stream-arn $STREAM_ARN --query StreamDescription.Shards[0].ShardId --output text)
SHARD_ITERATOR=$(aws dynamodbstreams get-shard-iterator \
  --stream-arn $STREAM_ARN \
  --shard-id $SHARD_ID \
  --shard-iterator-type TRIM_HORIZON \
  --query ShardIterator \
  --output text)

aws dynamodbstreams get-records --shard-iterator $SHARD_ITERATOR
```

**Key concepts demonstrated**:
- Database changes as event stream
- NEW_AND_OLD_IMAGES captures before/after state
- Can replay changes to rebuild state

### Example 4: Stream Processing with Lambda

**Concept**: Chapter 11 discusses stream processing operations like filtering, transforming, aggregating.

**Setup**:
```bash
# Create Lambda function (inline for simplicity)
cat > /tmp/lambda-function.py << 'EOF'
import json
import base64

def lambda_handler(event, context):
    for record in event['Records']:
        # Kinesis data is base64 encoded
        payload = json.loads(base64.b64decode(record['kinesis']['data']))

        # Stream processing: filter and transform
        if payload.get('amount', 0) > 1000:
            print(f"High-value transaction: {payload}")
            # Could write to another stream, DynamoDB, etc.

    return {'statusCode': 200}
EOF

# Create execution role (simplified)
# In practice, create proper IAM role with policies

# Create Lambda function
zip /tmp/function.zip /tmp/lambda-function.py
aws lambda create-function \
  --function-name transaction-processor \
  --runtime python3.11 \
  --handler lambda-function.lambda_handler \
  --zip-file fileb:///tmp/function.zip \
  --role arn:aws:iam::ACCOUNT:role/lambda-kinesis-role

# Connect Lambda to Kinesis stream
aws lambda create-event-source-mapping \
  --function-name transaction-processor \
  --event-source-arn arn:aws:kinesis:REGION:ACCOUNT:stream/user-events \
  --starting-position LATEST
```

**Key concepts demonstrated**:
- Continuous processing of stream events
- Stateless operations (filter, map)
- Automatic scaling of processing

### Example 5: Event Sourcing Pattern

**Concept**: Chapter 11 discusses event sourcing - storing events rather than current state.

**AWS CLI**:
```bash
# Stream for all events
aws kinesis create-stream --stream-name account-events --shard-count 1

# Store events (never update, only append)
aws kinesis put-record \
  --stream-name account-events \
  --partition-key account123 \
  --data '{"type":"AccountCreated","accountId":"acc123","balance":0,"timestamp":"2024-01-01T10:00:00Z"}'

aws kinesis put-record \
  --stream-name account-events \
  --partition-key account123 \
  --data '{"type":"MoneyDeposited","accountId":"acc123","amount":100,"timestamp":"2024-01-02T11:00:00Z"}'

aws kinesis put-record \
  --stream-name account-events \
  --partition-key account123 \
  --data '{"type":"MoneyWithdrawn","accountId":"acc123","amount":30,"timestamp":"2024-01-03T14:30:00Z"}'

# Archive to S3 for permanent storage
aws kinesis create-delivery-stream \
  --delivery-stream-name account-events-archive \
  --s3-destination-configuration \
  RoleARN=arn:aws:iam::ACCOUNT:role/firehose-role,BucketARN=arn:aws:s3:::event-archive

# Current state is computed from events (via Lambda/DynamoDB)
# State: balance = 0 + 100 - 30 = 70
```

**Key concepts demonstrated**:
- Immutable event log
- State derived from events
- Ability to replay events to rebuild state
- Events as source of truth

### Example 6: Time Windowing with Kinesis Data Analytics

**Concept**: Chapter 11 discusses windowing for time-based aggregations.

**SQL in Kinesis Data Analytics**:
```sql
-- Tumbling window: count events per 5-minute window
CREATE OR REPLACE STREAM "DESTINATION_SQL_STREAM" (
    event_count INTEGER,
    window_start TIMESTAMP,
    window_end TIMESTAMP
);

CREATE OR REPLACE PUMP "STREAM_PUMP" AS
INSERT INTO "DESTINATION_SQL_STREAM"
SELECT STREAM
    COUNT(*) as event_count,
    STEP(input_stream.ROWTIME BY INTERVAL '5' MINUTE) as window_start,
    STEP(input_stream.ROWTIME BY INTERVAL '5' MINUTE) + INTERVAL '5' MINUTE as window_end
FROM "SOURCE_SQL_STREAM_001" as input_stream
GROUP BY STEP(input_stream.ROWTIME BY INTERVAL '5' MINUTE);
```

**Key concepts demonstrated**:
- Tumbling windows (non-overlapping time periods)
- Event time vs processing time
- Aggregations over windows

### Example 7: Message Ordering with Partition Keys

**Concept**: Chapter 11 discusses message ordering guarantees.

**AWS CLI**:
```bash
# Send ordered events for same user
aws kinesis put-record \
  --stream-name user-events \
  --partition-key user456 \
  --data '{"userId":"user456","action":"view_item","itemId":"item1"}'

aws kinesis put-record \
  --stream-name user-events \
  --partition-key user456 \
  --data '{"userId":"user456","action":"add_to_cart","itemId":"item1"}'

aws kinesis put-record \
  --stream-name user-events \
  --partition-key user456 \
  --data '{"userId":"user456","action":"checkout"}'

# All events with same partition key go to same shard in order
# Events for different users may be processed in parallel
```

**Key concepts demonstrated**:
- Per-partition ordering guarantee
- Partition key determines routing
- Trade-off: ordering vs parallelism

## Comparison: Building Blocks

### Traditional Message Queue (SQS)
- **Use case**: Task distribution, decoupling services
- **Ordering**: FIFO queues (limited throughput) or standard (best-effort)
- **Consumers**: Messages deleted after processing
- **Replay**: Not possible

### Partitioned Log (Kinesis)
- **Use case**: Event streaming, CDC, analytics
- **Ordering**: Per-shard ordering
- **Consumers**: Multiple independent consumers
- **Replay**: Can replay from any point in retention period

### Pub/Sub (SNS)
- **Use case**: Fan-out, notifications
- **Ordering**: No guarantees (use SNS FIFO for ordering)
- **Consumers**: Push to multiple subscribers
- **Replay**: Not possible

## Common Patterns

### Pattern 1: Lambda Architecture (Batch + Stream)
```bash
# Speed layer: real-time with Kinesis + Lambda
# Batch layer: historical processing with S3 + EMR/Glue
# Serving layer: combined views in DynamoDB

# Stream layer
aws kinesis create-stream --stream-name real-time-events --shard-count 2

# Archive to batch layer
aws firehose create-delivery-stream \
  --delivery-stream-name events-to-s3 \
  --s3-destination-configuration BucketARN=arn:aws:s3:::batch-data
```

### Pattern 2: Kappa Architecture (Stream-only)
```bash
# Everything is a stream, batch = reprocessing the stream
# Single pipeline for both real-time and historical

aws kinesis create-stream --stream-name unified-events --shard-count 5
# Set long retention
aws kinesis increase-stream-retention-period \
  --stream-name unified-events \
  --retention-period-hours 168  # 7 days
```

## Cleanup Commands

```bash
# Delete Kinesis streams
aws kinesis delete-stream --stream-name user-events
aws kinesis delete-stream --stream-name account-events

# Delete SNS topic
aws sns delete-topic --topic-arn $TOPIC_ARN

# Delete SQS queues
aws sqs delete-queue --queue-url $(aws sqs get-queue-url --queue-name warehouse-processor --query QueueUrl --output text)

# Delete DynamoDB table
aws dynamodb delete-table --table-name users

# Delete Lambda function
aws lambda delete-function --function-name transaction-processor
```

## Key Takeaways

1. **Kinesis ≈ Kafka**: Partitioned log with ordering per shard
2. **DynamoDB Streams = CDC**: Database changes as events
3. **Lambda = Stream Processor**: Stateless processing at scale
4. **SNS = Fan-out**: One message to many consumers
5. **SQS = Message Queue**: Task distribution, at-least-once delivery
6. **Event Sourcing**: Store events in Kinesis/S3, derive state
7. **Time Windows**: Use Kinesis Data Analytics for SQL-based windowing

## Practice Exercises

As you progress through the learning plan, try these AWS implementations:

- **Phase 1**: Create a Kinesis stream and practice producing/consuming
- **Phase 2**: Compare SQS, SNS, and Kinesis for different use cases
- **Phase 3**: Enable DynamoDB Streams and observe CDC events
- **Phase 4**: Build a Lambda processor that aggregates events

The sandbox environment allows you to experiment freely with these services!
