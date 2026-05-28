# Event Architect - Sharp Edges

## Event Schema Breaking Change

### **Id**
event-schema-breaking-change
### **Summary**
Removing or renaming event fields breaks replay
### **Severity**
critical
### **Situation**
  You need to change an event schema - maybe rename a field or change its type.
  The "easy" fix is to just update the event class. This breaks everything.
  
### **Why**
  Old events in the store use the old schema. When you replay (for projections,
  debugging, or disaster recovery), deserialization fails. You've corrupted your
  entire event history. Recovery requires downtime and data migration.
  
### **Solution**
  # NEVER remove or rename fields. NEVER change types.
  
  # Step 1: Add new fields as optional with defaults
  @dataclass
  class MemoryCreatedV1:
      memory_id: UUID
      content: str
      created_at: datetime
  
  # V2 adds embedding - existing events still work
  @dataclass
  class MemoryCreatedV2:
      memory_id: UUID
      content: str
      created_at: datetime
      embedding: Optional[List[float]] = None  # New, optional
  
  # Step 2: Use explicit version numbers
  event_type = "MemoryCreated"
  event_version = 2
  
  # Step 3: Upcasters transform old events to new schema
  def upcast_memory_created(event: dict, version: int) -> dict:
      if version == 1:
          event["embedding"] = None
      return event
  
### **Symptoms**
  - Deserialization error during replay
  - KeyError on event field
  - Projections stuck at old position
  - TypeError: unexpected keyword argument
### **Detection Pattern**
class.*Event.*:\s*\n(?!.*version)
### **Version Range**
>=1.0.0

## Nats Ack Timeout Too Short

### **Id**
nats-ack-timeout-too-short
### **Summary**
Default NATS ack timeout is too short for ML workloads
### **Severity**
critical
### **Situation**
  You're using NATS JetStream to process events that trigger ML operations
  (embeddings, LLM calls). Events keep getting redelivered even though
  processing succeeds.
  
### **Why**
  Default ack timeout is 30 seconds. Embedding generation or LLM calls can
  take 60+ seconds. NATS times out, redelivers, and you process the same
  event multiple times. At scale, this creates duplicate entries and
  wastes expensive API calls.
  
### **Solution**
  # Set appropriate ack timeout for ML workloads
  subscription = await js.subscribe(
      "memories.extract",
      durable="memory-extractor",
      ack_wait=120,  # 2 minutes for ML operations
      max_deliver=3,  # Limit retries
  )
  
  # For long operations, use heartbeat pattern
  async def process_with_heartbeat(msg):
      async def heartbeat():
          while True:
              await asyncio.sleep(10)
              await msg.in_progress()  # Reset ack timeout
  
      heartbeat_task = asyncio.create_task(heartbeat())
      try:
          await expensive_ml_operation(msg.data)
          await msg.ack()
      finally:
          heartbeat_task.cancel()
  
### **Symptoms**
  - Events processed multiple times
  - Duplicate entries in database
  - High API costs from repeated LLM calls
  - NATS logs show 'redelivery' messages
### **Detection Pattern**
subscribe.*(?!ack_wait)
### **Version Range**
>=1.0.0

## Projection Not Idempotent

### **Id**
projection-not-idempotent
### **Summary**
Projection handlers that aren't safe to replay
### **Severity**
critical
### **Situation**
  Your projection works fine normally, but when you rebuild it (deploy new
  version, fix bug, add new projection), data is corrupted or duplicated.
  
### **Why**
  Projections MUST be replayable from position 0. If your handler uses
  INSERT without ON CONFLICT, or increments counters without checking
  event position, replay creates duplicates or wrong counts.
  
### **Solution**
  # BAD: Not idempotent
  async def handle_memory_created(event):
      await db.execute("INSERT INTO memories ...")  # Fails on replay
  
  # GOOD: Idempotent with upsert
  async def handle_memory_created(event):
      await db.execute(
          """
          INSERT INTO memories (id, content, created_at)
          VALUES ($1, $2, $3)
          ON CONFLICT (id) DO UPDATE SET
              content = EXCLUDED.content,
              created_at = EXCLUDED.created_at
          """,
          event.memory_id, event.content, event.created_at
      )
  
  # For counters, use event-sourced approach
  async def handle_memory_accessed(event):
      await db.execute(
          """
          INSERT INTO memory_access_log (event_id, memory_id, accessed_at)
          VALUES ($1, $2, $3)
          ON CONFLICT (event_id) DO NOTHING
          """,
          event.event_id, event.memory_id, event.accessed_at
      )
      # Derive count from log, don't increment
  
### **Symptoms**
  - Duplicate rows after projection rebuild
  - Counts are wrong after replay
  - Unique constraint violations during replay
  - Fear of rebuilding projections
### **Detection Pattern**
INSERT(?!.*ON CONFLICT)
### **Version Range**
>=1.0.0

## Stream Retention Silent Drop

### **Id**
stream-retention-silent-drop
### **Summary**
NATS stream retention limits silently drop events
### **Severity**
high
### **Situation**
  You set up a NATS stream with limits (max_msgs, max_bytes, max_age).
  Months later, you try to replay from the beginning and events are missing.
  
### **Why**
  When limits are exceeded, NATS silently drops old events. There's no error,
  no warning. Your event store just lost data. If you depend on complete
  history for projections or audit, you're in trouble.
  
### **Solution**
  # Option 1: Archive to permanent storage
  async def archive_and_delete(js, stream_name):
      # Read events before they're dropped
      consumer = await js.subscribe(stream_name)
      async for msg in consumer.messages:
          # Write to permanent store (S3, DB, etc.)
          await archive_store.write(msg.data)
          await msg.ack()
  
  # Option 2: Use unlimited retention with external archival
  stream_config = StreamConfig(
      name="memories",
      subjects=["memories.>"],
      retention=RetentionPolicy.LIMITS,
      max_msgs=-1,  # Unlimited
      max_bytes=-1,  # Unlimited
      max_age=0,     # Never expire
      # Use separate archival job to move old events to cold storage
  )
  
  # Option 3: Monitor and alert
  async def monitor_stream_usage():
      info = await js.stream_info("memories")
      if info.state.messages > threshold:
          alert("Stream approaching limits - archive needed")
  
### **Symptoms**
  - Events missing when replaying from start
  - Projection rebuild produces different results
  - Gaps in event sequence numbers
  - Audit trail incomplete
### **Detection Pattern**
StreamConfig.*max_msgs.*[^-]\\d+
### **Version Range**
>=1.0.0

## Event Ordering Assumption

### **Id**
event-ordering-assumption
### **Summary**
Assuming events arrive in order across partitions
### **Severity**
high
### **Situation**
  You have multiple producers writing to the same event stream. Your handler
  assumes EventA always comes before EventB. Occasionally, logic breaks.
  
### **Why**
  Distributed systems don't guarantee global ordering. Even with Kafka
  partitioning, events from different producers can interleave. If your
  handler assumes sequence, it fails intermittently.
  
### **Solution**
  # Design handlers to handle out-of-order events
  
  # BAD: Assumes order
  async def handle_event(event):
      if event.type == "MemoryCreated":
          self.memory = event.memory
      elif event.type == "MemoryUpdated":
          self.memory.update(event.changes)  # Fails if Created not received
  
  # GOOD: Idempotent and order-independent
  async def handle_event(event):
      if event.type == "MemoryCreated":
          await db.execute(
              "INSERT INTO memories (id, ...) ON CONFLICT DO NOTHING",
              ...
          )
      elif event.type == "MemoryUpdated":
          await db.execute(
              """
              UPDATE memories SET ...
              WHERE id = $1 AND updated_at < $2  -- Only apply if newer
              """,
              event.memory_id, event.occurred_at
          )
  
  # Or use sequence numbers per entity
  async def handle_with_sequence(event):
      await db.execute(
          """
          UPDATE memories SET ..., version = $2
          WHERE id = $1 AND version < $2
          """,
          event.memory_id, event.sequence
      )
  
### **Symptoms**
  - Intermittent 'not found' errors
  - Updates applied to wrong state
  - Tests pass but production fails
  - Errors correlate with high load
### **Detection Pattern**

### **Version Range**
>=1.0.0

## Projection Rebuild Blocks Writes

### **Id**
projection-rebuild-blocks-writes
### **Summary**
Projection rebuild takes hours and blocks new events
### **Severity**
high
### **Situation**
  You need to rebuild a projection (bug fix, schema change). You stop the
  old projector, start replay from position 0. Meanwhile, new events
  pile up. Users see stale data for hours.
  
### **Why**
  Naive rebuild processes events sequentially from the beginning.
  With millions of events, this takes hours. During this time, the
  projection is either stale or inconsistent.
  
### **Solution**
  # Use blue-green projection pattern
  
  # 1. Create new projection table (v2)
  await db.execute("CREATE TABLE memories_v2 (LIKE memories)")
  
  # 2. Start new projector writing to v2, from position 0
  async def rebuild_projector():
      await project_all_events(target_table="memories_v2")
  
  # 3. Keep old projector running on memories (v1)
  # Users still see live data
  
  # 4. When v2 catches up to live, atomic swap
  async def swap_when_caught_up():
      while True:
          v2_pos = await get_position("memories_v2")
          live_pos = await get_current_position()
          if live_pos - v2_pos < 100:  # Close enough
              break
          await asyncio.sleep(60)
  
      async with db.transaction():
          await db.execute("ALTER TABLE memories RENAME TO memories_old")
          await db.execute("ALTER TABLE memories_v2 RENAME TO memories")
  
  # 5. Clean up old table after validation
  
### **Symptoms**
  - Stale data during deploys
  - Users complain about 'missing' recent items
  - Fear of changing projections
  - Deployment windows limited by rebuild time
### **Detection Pattern**

### **Version Range**
>=1.0.0

## Consumer Position Not Stored

### **Id**
consumer-position-not-stored
### **Summary**
Consumer position lost on restart
### **Severity**
high
### **Situation**
  Your event consumer crashes or restarts. When it comes back up, it either
  reprocesses all events or skips to the latest, missing events.
  
### **Why**
  If you don't durably store consumer position, restart means either
  full replay (slow, duplicate processing) or data loss (missed events).
  
### **Solution**
  # Store position in database, not memory
  
  class DurableConsumer:
      def __init__(self, consumer_name: str):
          self.name = consumer_name
  
      async def get_position(self) -> int:
          result = await db.fetchval(
              "SELECT position FROM consumer_positions WHERE name = $1",
              self.name
          )
          return result or 0
  
      async def process_from_position(self):
          position = await self.get_position()
  
          async for event in event_store.read_from(position):
              await self.handle(event)
  
              # Store position after successful processing
              await db.execute(
                  """
                  INSERT INTO consumer_positions (name, position)
                  VALUES ($1, $2)
                  ON CONFLICT (name) DO UPDATE SET position = $2
                  """,
                  self.name, event.position
              )
  
  # With NATS JetStream, use durable consumers
  subscription = await js.subscribe(
      "memories.>",
      durable="my-consumer",  # Position stored in NATS
  )
  
### **Symptoms**
  - Duplicate processing after restart
  - Events missing after restart
  - Inconsistent data between instances
  - Full replay on every deploy
### **Detection Pattern**
subscribe.*(?!durable)
### **Version Range**
>=1.0.0

## Event Too Many Fields

### **Id**
event-too-many-fields
### **Summary**
Event payloads that contain the world
### **Severity**
medium
### **Situation**
  Your event contains 50+ fields including nested objects, full entity
  snapshots, and "might need this later" data. Storage grows fast.
  
### **Why**
  Fat events cause storage bloat, slow serialization, and schema rigidity.
  Every field is a contract - you can never remove it. Changes require
  migrating millions of events.
  
### **Solution**
  # WRONG: Kitchen sink event
  class UserSignedUp:
      user_id: UUID
      email: str
      name: str
      address: Address  # Full nested object
      preferences: Dict  # Everything they might ever want
      session_data: Dict  # Why is this here?
      request_headers: Dict  # Definitely not needed
  
  # RIGHT: Minimal event with references
  class UserSignedUp:
      user_id: UUID
      email: str
      correlation_id: UUID
      occurred_at: datetime
      # That's it. Profile details go in UserProfileUpdated.
      # Address goes in AddressAdded. Single responsibility.
  
  # If you need denormalized data for a projection, derive it
  # in the projection, don't store it in events.
  
### **Symptoms**
  - Events are several KB each
  - Schema changes require migration scripts
  - Storage costs growing faster than users
  - Serialization is slow
### **Detection Pattern**
@dataclass[\\s\\S]*?:\\s*\\w+[\\s\\S]{500,}?def to_bytes
### **Version Range**
>=1.0.0

## Sync Projection In Handler

### **Id**
sync-projection-in-handler
### **Summary**
Blocking on projection update in event handler
### **Severity**
medium
### **Situation**
  Your event handler updates all projections synchronously before
  acknowledging the event. As you add projections, throughput drops.
  
### **Why**
  Event ingestion should be fast. Projections can be eventually consistent.
  Synchronous projection updates create cascading slowdowns and timeouts.
  
### **Solution**
  # BAD: Synchronous projection
  async def handle_event(event):
      await update_projection_1(event)
      await update_projection_2(event)
      await update_projection_3(event)
      await msg.ack()  # Takes 3x as long
  
  # GOOD: Async projection with separate consumers
  # Event store handles ingestion only
  async def handle_event(event):
      await event_store.append(event)
      await msg.ack()  # Fast
  
  # Separate projector processes for each projection
  # projection_1_consumer.py
  async def project_1():
      async for event in event_store.subscribe():
          await update_projection_1(event)
  
  # projection_2_consumer.py
  async def project_2():
      async for event in event_store.subscribe():
          await update_projection_2(event)
  
### **Symptoms**
  - Event ingestion slows as projections increase
  - Ack timeouts during high load
  - Adding new projection slows everything
  - Single projection failure blocks all events
### **Detection Pattern**

### **Version Range**
>=1.0.0