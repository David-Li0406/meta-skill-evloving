# Data Engineer - Sharp Edges

## Late Arriving Data

### **Id**
late-arriving-data
### **Summary**
Late data arrives after window closes, gets dropped or duplicated
### **Severity**
high
### **Situation**
Processing time-windowed aggregations
### **Why**
  You aggregate hourly. Window closes at 1:00 AM. Data with timestamp 12:30 AM
  arrives at 1:05 AM (network delay, batch upload, timezone issues).
  Either dropped (missing data) or counted in wrong window (inflated counts).
  
### **Solution**
  1. Use watermarks with allowed lateness:
     # Flink/Spark Streaming
     .watermark(col("event_time"), "5 minutes")
     .withWatermarkDelay("10 minutes")
  
  2. Use event time, not processing time:
     # Aggregate by event_time, not arrival_time
     GROUP BY TUMBLE(event_time, INTERVAL '1' HOUR)
  
  3. For batch: allow for late data in window query:
     WHERE event_time >= window_start - INTERVAL '1 hour'
       AND event_time < window_end + INTERVAL '15 minutes'
  
  4. Reprocess recent windows on backfill:
     # Always recompute last N windows on each run
  
### **Symptoms**
  - Counts change when you re-run pipeline
  - Missing data for recent periods
  - Inconsistent numbers between systems
### **Detection Pattern**
watermark|late.*data|event_time|processing_time

## Schema Evolution Breaks

### **Id**
schema-evolution-breaks
### **Summary**
Producer schema change breaks consumer pipeline
### **Severity**
critical
### **Situation**
Data flowing between systems with schema
### **Why**
  Producer adds required field. Consumer schema expects old format.
  Pipeline fails. Or producer removes field. Consumer references it.
  NullPointerException at 3 AM.
  
### **Solution**
  1. Use schema registry with compatibility checks:
     # Confluent Schema Registry
     curl -X POST -H "Content-Type: application/vnd.schemaregistry.v1+json" \
       --data '{"schema": "..."}' \
       http://schema-registry:8081/subjects/memories-value/versions
  
  2. Set compatibility mode:
     # BACKWARD: new schema can read old data
     # FORWARD: old schema can read new data
     # FULL: both directions
     compatibility: BACKWARD
  
  3. Only additive changes without registry:
     # Add optional fields with defaults
     # Never remove or rename fields
     # Never change field types
  
  4. Version your schemas:
     class MemoryV2(MemoryV1):
         new_field: str = ""  # Optional with default
  
### **Symptoms**
  - "Schema not found" or "Field not found" errors
  - Pipeline breaks after producer deployment
  - Deserialization exceptions
### **Detection Pattern**
schema.*registry|avro|protobuf|evolution

## Cdc Slot Overflow

### **Id**
cdc-slot-overflow
### **Summary**
Replication slot fills up, blocks database writes
### **Severity**
critical
### **Situation**
Change Data Capture with PostgreSQL logical replication
### **Why**
  CDC consumer is down. PostgreSQL keeps WAL for the replication slot.
  Slot retains data until consumer confirms. WAL grows unbounded.
  Disk fills up. Database stops accepting writes.
  
### **Solution**
  1. Monitor replication slot lag:
     SELECT slot_name,
            pg_size_pretty(pg_wal_lsn_diff(pg_current_wal_lsn(), restart_lsn))
            AS replication_lag
     FROM pg_replication_slots;
  
  2. Set max slot WAL keep size:
     # postgresql.conf
     max_slot_wal_keep_size = 10GB  # PostgreSQL 13+
  
  3. Alert on slot lag:
     - alert: ReplicationSlotLag
       expr: pg_replication_slot_wal_bytes > 1e9  # 1GB
       for: 5m
  
  4. Have runbook for dropping stuck slot:
     SELECT pg_drop_replication_slot('debezium_mind');
     # Then recreate and backfill
  
### **Symptoms**
  - Database disk filling up
  - "no space left on device" in PostgreSQL logs
  - Consumer can't keep up with producer
### **Detection Pattern**
replication_slot|wal.*size|slot.*lag

## Exactly Once Illusion

### **Id**
exactly-once-illusion
### **Summary**
Claiming exactly-once when it's actually at-least-once
### **Severity**
high
### **Situation**
Designing pipeline delivery guarantees
### **Why**
  Kafka consumer commits offset, then crashes before writing to sink.
  On restart, message is re-processed. Sink now has duplicate.
  Your "exactly-once" pipeline is actually at-least-once.
  
### **Solution**
  1. Use idempotent writes:
     # Upsert with natural key
     INSERT INTO memories (memory_id, content, ...)
     VALUES (...)
     ON CONFLICT (memory_id) DO UPDATE SET ...
  
  2. Use transactional outbox:
     # Write to outbox table in same transaction
     async with db.transaction():
         await db.insert("memories", data)
         await db.insert("outbox", {"topic": "memories", "payload": data})
  
  3. For Kafka, use transactions:
     producer.begin_transaction()
     producer.send(...)
     consumer.commit_offsets()
     producer.commit_transaction()
  
  4. Or accept at-least-once and handle dedup:
     # Track processed message IDs
     if not await is_processed(message_id):
         await process(message)
         await mark_processed(message_id)
  
### **Symptoms**
  - Duplicate records in sink
  - Counts higher than expected
  - Same record processed multiple times
### **Detection Pattern**
exactly.once|at.least.once|idempotent|dedup

## Backfill Corrupts Production

### **Id**
backfill-corrupts-production
### **Summary**
Backfill job interferes with live pipeline
### **Severity**
high
### **Situation**
Running backfill while production pipeline is active
### **Why**
  Backfill reprocesses old data. Production pipeline processes new data.
  Both write to same table. Race condition: backfill overwrites recent
  data with old data, or production overwrites backfill.
  
### **Solution**
  1. Use separate targets for backfill:
     # Backfill to staging table
     await pipeline.run(target="memories_backfill")
     # Swap when complete
     await db.execute("ALTER TABLE memories RENAME TO memories_old")
     await db.execute("ALTER TABLE memories_backfill RENAME TO memories")
  
  2. Partition by date, backfill by partition:
     # Each partition is independent
     # Backfill writes to historical partitions only
     WHERE created_at < '2024-01-01'
  
  3. Use versioning:
     # Each run has version, query uses MAX(version)
     INSERT INTO memories (memory_id, data, version)
     VALUES (..., $run_version)
  
  4. Lock mechanism:
     # Only one pipeline per table at a time
     SELECT pg_advisory_lock(hash_of('memories'))
  
### **Symptoms**
  - Recent data disappears after backfill
  - Inconsistent data between old and new records
  - Count drops then recovers
### **Detection Pattern**
backfill|reprocess|historical|advisory_lock

## Timezone Chaos

### **Id**
timezone-chaos
### **Summary**
Timestamps in mixed timezones cause incorrect aggregations
### **Severity**
medium
### **Situation**
Processing data from multiple sources or regions
### **Why**
  Source A sends UTC. Source B sends local time without timezone.
  Source C sends epoch milliseconds. You assume all are UTC.
  Daily aggregations are off by hours for some sources.
  
### **Solution**
  1. Store everything in UTC:
     created_at TIMESTAMP WITH TIME ZONE
  
  2. Convert on ingestion:
     # Python
     if tz_naive:
         dt = dt.replace(tzinfo=ZoneInfo("America/New_York"))
     dt_utc = dt.astimezone(ZoneInfo("UTC"))
  
  3. Validate timezone on arrival:
     def validate_timestamp(ts: str) -> datetime:
         dt = datetime.fromisoformat(ts)
         if dt.tzinfo is None:
             raise ValueError("Timestamp must include timezone")
         return dt.astimezone(ZoneInfo("UTC"))
  
  4. Document timezone requirements in schema:
     # All timestamps MUST be ISO 8601 with timezone
     # Example: 2024-01-15T10:30:00+00:00
  
### **Symptoms**
  - Daily counts vary by source
  - Data "jumps" hours when viewed in different timezone
  - Aggregations shift during DST changes
### **Detection Pattern**
timezone|tz|UTC|ZoneInfo|timestamp

## Large State Shuffle

### **Id**
large-state-shuffle
### **Summary**
Stateful operation causes OOM on large key cardinality
### **Severity**
high
### **Situation**
Aggregating or joining by high-cardinality key
### **Why**
  GROUP BY user_id with 10 million users. Each user's state in memory.
  Shuffle partitions fill up. Workers run out of memory.
  Job fails or slows to crawl.
  
### **Solution**
  1. Pre-aggregate before join:
     # Reduce cardinality first
     daily_stats = memories.groupBy("user_id", "date").agg(...)
     # Then join on smaller dataset
     users.join(daily_stats, "user_id")
  
  2. Increase partitions:
     spark.conf.set("spark.sql.shuffle.partitions", 1000)
  
  3. Use salting for skewed keys:
     # Add random salt to spread hot keys
     df.withColumn("salted_key", concat(col("key"), lit("_"), (rand() * 10).cast("int")))
  
  4. Use incremental processing:
     # Process user by user in batches
     for user_batch in chunk(users, 10000):
         process_users(user_batch)
  
### **Symptoms**
  - OOM during shuffle stage
  - Executor lost errors
  - Job stuck at certain percentage
### **Detection Pattern**
shuffle|OOM|out.*memory|partitions

## Silent Data Loss

### **Id**
silent-data-loss
### **Summary**
Pipeline drops records silently, no alerts
### **Severity**
critical
### **Situation**
Error handling in data pipelines
### **Why**
  try: process(record) except: pass  # "Handling" errors by ignoring them.
  You never know records are being dropped. Data quality degrades silently.
  Discovered months later when reports don't match.
  
### **Solution**
  1. Never silently drop records:
     try:
         process(record)
     except Exception as e:
         await dead_letter_queue.send(record, error=str(e))
         DROPPED_RECORDS.inc()
  
  2. Alert on dead letter queue:
     - alert: DeadLetterQueueGrowing
       expr: rate(dead_letter_records_total[5m]) > 0
       for: 5m
  
  3. Track input vs output counts:
     RECORDS_IN.inc()
     result = process(record)
     RECORDS_OUT.inc()
     # Alert if IN - OUT grows
  
  4. Regular reconciliation:
     # Daily check: source count vs sink count
     SELECT COUNT(*) FROM source WHERE date = today()
     SELECT COUNT(*) FROM sink WHERE date = today()
  
### **Symptoms**
  - Counts don't match between systems
  - Specific records missing
  - No errors in logs but data is wrong
### **Detection Pattern**
dead.*letter|DLQ|except.*pass|silent