# Event Architect

## Patterns


---
  #### **Name**
Event Envelope Pattern
  #### **Description**
Wrap all events in a consistent envelope with metadata
  #### **When**
Designing any event schema
  #### **Example**
    @dataclass(frozen=True)
    class EventEnvelope:
        event_id: UUID
        event_type: str
        event_version: int
        correlation_id: UUID
        causation_id: UUID
        user_id: UUID
        occurred_at: datetime
        recorded_at: datetime
        payload: Dict[str, Any]
    
        def to_bytes(self) -> bytes:
            return msgpack.packb(asdict(self))
    

---
  #### **Name**
Projection with Checkpoint
  #### **Description**
Store projection position atomically with updates
  #### **When**
Building read models from events
  #### **Example**
    async def update_projection(event: Event):
        async with db.transaction():
            # Update the read model
            await db.execute(
                "UPDATE memories SET salience = $1 WHERE id = $2",
                event.payload["new_salience"],
                event.payload["memory_id"]
            )
            # Store position atomically
            await db.execute(
                "UPDATE projection_checkpoints SET position = $1 WHERE projection = $2",
                event.position,
                "memory_salience"
            )
    

---
  #### **Name**
Optimistic Locking for Aggregates
  #### **Description**
Use version numbers to prevent concurrent updates
  #### **When**
Multiple writers could update the same aggregate
  #### **Example**
    async def append_event(stream_id: str, event: Event, expected_version: int):
        result = await db.execute(
            """
            INSERT INTO events (stream_id, version, data)
            SELECT $1, $2, $3
            WHERE (SELECT COALESCE(MAX(version), 0) FROM events WHERE stream_id = $1) = $4
            RETURNING id
            """,
            stream_id, expected_version + 1, event.to_bytes(), expected_version
        )
        if not result:
            raise OptimisticConcurrencyError(f"Stream {stream_id} modified concurrently")
    

---
  #### **Name**
Consumer Groups for Scaling
  #### **Description**
Use NATS consumer groups for horizontal scaling
  #### **When**
Need to scale event processing across multiple workers
  #### **Example**
    # Each worker in the group gets different events
    subscription = await js.subscribe(
        "memories.>",
        durable="memory-projector",
        deliver_policy=DeliverPolicy.ALL,
        ack_policy=AckPolicy.EXPLICIT,
        ack_wait=60,  # 60s for ML workloads
    )
    
    async for msg in subscription.messages:
        try:
            await process_event(msg.data)
            await msg.ack()
        except Exception as e:
            await msg.nak(delay=30)  # Retry in 30s
    

## Anti-Patterns


---
  #### **Name**
Mutable Events
  #### **Description**
Modifying events after they're stored
  #### **Why**
Events are facts about the past. Modifying them breaks auditability and replay.
  #### **Instead**
Append compensating events to fix mistakes

---
  #### **Name**
Large Binary Payloads in Events
  #### **Description**
Storing images, files, or large blobs in event payloads
  #### **Why**
Events should be small and fast. Large payloads kill performance and storage.
  #### **Instead**
Store content hash/reference in event, content in blob storage

---
  #### **Name**
Projections That Query Services
  #### **Description**
Making API calls from inside projection handlers
  #### **Why**
Projections must be deterministic. External calls break replay.
  #### **Instead**
Include all needed data in the event, or use saga pattern

---
  #### **Name**
Missing Correlation IDs
  #### **Description**
Events without correlation/causation chain
  #### **Why**
Debugging distributed systems without traces is impossible
  #### **Instead**
Always include correlation_id (request) and causation_id (parent event)

---
  #### **Name**
Non-Deterministic Handlers
  #### **Description**
Using random(), datetime.now(), or external state in handlers
  #### **Why**
Replay produces different results, breaking the fundamental guarantee
  #### **Instead**
Put all randomness in the event, use event timestamp