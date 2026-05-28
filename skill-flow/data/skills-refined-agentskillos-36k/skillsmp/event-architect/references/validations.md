# Event Architect - Validations

## Event Without Correlation ID

### **Id**
event-missing-correlation-id
### **Severity**
error
### **Type**
regex
### **Pattern**
  - @dataclass.*Event[\\s\\S]*?(?!correlation_id)
  - class.*Event.*:[\\s\\S]{0,500}(?!correlation_id)[\\s\\S]*?def to_
### **Message**
Event class missing correlation_id field. Required for distributed tracing.
### **Fix Action**
Add correlation_id: UUID and causation_id: UUID fields to event class
### **Applies To**
  - *.py
  - **/events/*.py
  - **/domain/*.py

## Event Without Version Number

### **Id**
event-missing-version
### **Severity**
error
### **Type**
regex
### **Pattern**
  - @dataclass.*Event[\\s\\S]{0,300}(?!event_version|version)
### **Message**
Event class missing version number. Required for schema evolution.
### **Fix Action**
Add event_version: int = 1 field to event class
### **Applies To**
  - *.py
  - **/events/*.py

## Event Dataclass Not Frozen

### **Id**
event-mutable-dataclass
### **Severity**
error
### **Type**
regex
### **Pattern**
  - @dataclass(?!.*frozen=True).*Event
  - @dataclass\\s*\\n\\s*class.*Event
### **Message**
Event dataclass should be frozen (immutable). Events are facts.
### **Fix Action**
Change @dataclass to @dataclass(frozen=True)
### **Applies To**
  - *.py
  - **/events/*.py

## Projection INSERT Without ON CONFLICT

### **Id**
projection-insert-not-idempotent
### **Severity**
error
### **Type**
regex
### **Pattern**
  - INSERT INTO(?!.*ON CONFLICT)
  - execute.*INSERT(?!.*ON CONFLICT)
### **Message**
INSERT without ON CONFLICT is not idempotent. Projection replay will fail.
### **Fix Action**
Add ON CONFLICT (id) DO UPDATE or DO NOTHING for idempotent upserts
### **Applies To**
  - **/projections/*.py
  - **/handlers/*.py

## NATS Subscription Without Durable Name

### **Id**
nats-missing-durable
### **Severity**
error
### **Type**
regex
### **Pattern**
  - subscribe\\([^)]*(?!durable)[^)]*\\)
  - \\.subscribe\\(.*\\)(?!.*durable)
### **Message**
NATS subscription without durable name. Position lost on restart.
### **Fix Action**
Add durable='consumer-name' parameter to subscription
### **Applies To**
  - *.py
  - **/consumers/*.py

## NATS AckNone for Important Events

### **Id**
nats-ack-none
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - AckPolicy\\.NONE
  - ack_policy.*none
### **Message**
AckNone means no delivery guarantee. Use AckExplicit for important events.
### **Fix Action**
Change to AckPolicy.EXPLICIT for events that matter
### **Applies To**
  - *.py
  - **/consumers/*.py

## Event Timestamp Without Timezone

### **Id**
event-datetime-without-timezone
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - datetime\\.now\\(\\)
  - datetime\\.utcnow\\(\\)
### **Message**
Use datetime.now(timezone.utc) for timezone-aware timestamps.
### **Fix Action**
Replace with datetime.now(timezone.utc) or use occurred_at from event
### **Applies To**
  - *.py
  - **/events/*.py

## External API Call in Event Handler

### **Id**
event-handler-external-call
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - async def handle.*event[\\s\\S]*?await.*(?:httpx|aiohttp|requests)\\.(?:get|post)
  - def handle.*event[\\s\\S]*?requests\\.(?:get|post)
### **Message**
External API calls in handlers break replay determinism. Use saga pattern.
### **Fix Action**
Move external calls to separate saga/workflow or include data in event
### **Applies To**
  - **/handlers/*.py
  - **/projections/*.py

## Non-Deterministic Operation in Handler

### **Id**
event-random-in-handler
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - def handle[\\s\\S]*?random\\.
  - def handle[\\s\\S]*?uuid4\\(\\)
### **Message**
Random values in handlers break replay. Put randomness in event payload.
### **Fix Action**
Generate UUIDs/random values when creating event, not when handling
### **Applies To**
  - **/handlers/*.py
  - **/projections/*.py

## Large Object in Event Payload

### **Id**
event-large-payload
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - embedding:\\s*List\\[float\\](?!.*Optional)
  - content:\\s*str(?!.*hash)
### **Message**
Consider storing large data (embeddings, content) by reference, not in event.
### **Fix Action**
Store content_hash or embedding_ref instead of full data
### **Applies To**
  - **/events/*.py

## Projection Without Position Checkpoint

### **Id**
projection-missing-checkpoint
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - class.*Projection[\\s\\S]*?async def handle[\\s\\S]*?(?!position|checkpoint)
### **Message**
Projection should store checkpoint position for recovery.
### **Fix Action**
Store event position atomically with projection updates
### **Applies To**
  - **/projections/*.py

## Event Name Not Past Tense

### **Id**
event-past-tense-name
### **Severity**
info
### **Type**
regex
### **Pattern**
  - class\\s+(?:Create|Update|Delete|Send|Process)\\w+Event
  - event_type.*=.*'(?:Create|Update|Delete)'
### **Message**
Events should be past tense (MemoryCreated not CreateMemory). Events are facts.
### **Fix Action**
Rename to past tense: Created, Updated, Deleted, Sent, Processed
### **Applies To**
  - **/events/*.py