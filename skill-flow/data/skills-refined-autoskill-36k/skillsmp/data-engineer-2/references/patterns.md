# Data Engineer

## Patterns


---
  #### **Name**
Idempotent Pipeline Design
  #### **Description**
Pipelines safe to re-run without side effects
  #### **When**
Any data pipeline that may need retry or backfill
  #### **Example**
    from datetime import datetime
    from typing import Optional
    import hashlib
    
    class IdempotentPipeline:
        """Pipeline that can be safely re-run."""
    
        def __init__(self, db, target_table: str):
            self.db = db
            self.target_table = target_table
    
        async def run(
            self,
            start_date: datetime,
            end_date: datetime,
            run_id: Optional[str] = None
        ):
            # Generate deterministic run_id for idempotency tracking
            run_id = run_id or self._generate_run_id(start_date, end_date)
    
            # Check if already processed (idempotency)
            if await self._already_processed(run_id):
                logger.info(f"Run {run_id} already processed, skipping")
                return
    
            # Use atomic replace for target partition
            # Delete-then-insert in transaction
            async with self.db.transaction():
                await self._delete_partition(start_date, end_date)
                data = await self._extract(start_date, end_date)
                transformed = await self._transform(data)
                await self._load(transformed, run_id)
                await self._mark_processed(run_id)
    
        def _generate_run_id(self, start: datetime, end: datetime) -> str:
            """Deterministic run ID for date range."""
            key = f"{self.target_table}:{start.isoformat()}:{end.isoformat()}"
            return hashlib.sha256(key.encode()).hexdigest()[:16]
    
        async def _already_processed(self, run_id: str) -> bool:
            result = await self.db.fetchone(
                "SELECT 1 FROM pipeline_runs WHERE run_id = $1",
                run_id
            )
            return result is not None
    
        async def _delete_partition(self, start: datetime, end: datetime):
            """Delete existing data for date range (allows re-run)."""
            await self.db.execute(
                f"""
                DELETE FROM {self.target_table}
                WHERE created_at >= $1 AND created_at < $2
                """,
                start, end
            )
    
        async def _mark_processed(self, run_id: str):
            await self.db.execute(
                """
                INSERT INTO pipeline_runs (run_id, completed_at)
                VALUES ($1, NOW())
                """,
                run_id
            )
    
    # Usage: Can safely re-run for any date range
    pipeline = IdempotentPipeline(db, "memory_aggregates")
    await pipeline.run(
        start_date=datetime(2024, 1, 1),
        end_date=datetime(2024, 1, 2)
    )
    

---
  #### **Name**
Change Data Capture Pattern
  #### **Description**
Capture and process database changes in real-time
  #### **When**
Need to sync data between systems without polling
  #### **Example**
    # PostgreSQL logical replication with Debezium
    
    # 1. Enable logical replication in PostgreSQL
    # postgresql.conf
    wal_level = logical
    max_replication_slots = 10
    max_wal_senders = 10
    
    # 2. Create publication for tables
    CREATE PUBLICATION mind_cdc FOR TABLE memories, entities;
    
    # 3. Debezium connector configuration
    # debezium-connector.json
    {
      "name": "mind-postgres-connector",
      "config": {
        "connector.class": "io.debezium.connector.postgresql.PostgresConnector",
        "database.hostname": "postgres",
        "database.port": "5432",
        "database.user": "cdc_user",
        "database.password": "${secrets.db_password}",
        "database.dbname": "memory_service",
        "database.server.name": "memory",
        "plugin.name": "pgoutput",
        "publication.name": "mind_cdc",
        "slot.name": "debezium_mind",
        "table.include.list": "public.memories,public.entities",
        "transforms": "unwrap",
        "transforms.unwrap.type": "io.debezium.transforms.ExtractNewRecordState",
        "key.converter": "org.apache.kafka.connect.json.JsonConverter",
        "value.converter": "org.apache.kafka.connect.json.JsonConverter"
      }
    }
    
    # 4. Consumer processing CDC events
    from dataclasses import dataclass
    from enum import Enum
    
    class Operation(Enum):
        CREATE = "c"
        UPDATE = "u"
        DELETE = "d"
    
    @dataclass
    class CDCEvent:
        operation: Operation
        table: str
        before: dict | None
        after: dict | None
        timestamp: datetime
    
    class CDCProcessor:
        async def process(self, event: CDCEvent):
            if event.table == "memories":
                await self._process_memory_change(event)
            elif event.table == "entities":
                await self._process_entity_change(event)
    
        async def _process_memory_change(self, event: CDCEvent):
            if event.operation == Operation.CREATE:
                # Sync to vector store
                await self.vector_store.upsert(
                    id=event.after["memory_id"],
                    embedding=event.after["embedding"],
                    metadata=event.after
                )
            elif event.operation == Operation.DELETE:
                await self.vector_store.delete(
                    id=event.before["memory_id"]
                )
    

---
  #### **Name**
Data Quality Validation
  #### **Description**
Validate data at ingestion and transformation
  #### **When**
Any data pipeline where quality matters
  #### **Example**
    from pydantic import BaseModel, validator, Field
    from typing import List, Optional
    from enum import Enum
    import great_expectations as ge
    
    # Schema validation with Pydantic
    class MemoryRecord(BaseModel):
        memory_id: str = Field(..., regex=r'^mem_[a-zA-Z0-9]+$')
        agent_id: str
        content: str = Field(..., min_length=1, max_length=100000)
        salience: float = Field(..., ge=0.0, le=1.0)
        created_at: datetime
    
        @validator('content')
        def content_not_empty(cls, v):
            if not v.strip():
                raise ValueError('Content cannot be empty or whitespace')
            return v
    
    # Statistical validation with Great Expectations
    def create_memory_expectations(context: ge.DataContext):
        suite = context.create_expectation_suite("memory_quality")
    
        # Completeness expectations
        suite.add_expectation(
            ge.core.ExpectColumnToExist(column="memory_id")
        )
        suite.add_expectation(
            ge.core.ExpectColumnValuesToNotBeNull(column="content")
        )
    
        # Uniqueness expectations
        suite.add_expectation(
            ge.core.ExpectColumnValuesToBeUnique(column="memory_id")
        )
    
        # Value range expectations
        suite.add_expectation(
            ge.core.ExpectColumnValuesToBeBetween(
                column="salience",
                min_value=0.0,
                max_value=1.0
            )
        )
    
        # Freshness expectations
        suite.add_expectation(
            ge.core.ExpectColumnValuesToBeBetween(
                column="created_at",
                min_value=datetime.now() - timedelta(days=1)
            )
        )
    
        return suite
    
    # Pipeline with validation
    class ValidatedPipeline:
        async def run(self, batch: List[dict]):
            # 1. Schema validation (fast, per-record)
            valid_records = []
            invalid_records = []
    
            for record in batch:
                try:
                    validated = MemoryRecord(**record)
                    valid_records.append(validated.dict())
                except ValidationError as e:
                    invalid_records.append({
                        "record": record,
                        "errors": e.errors()
                    })
    
            # 2. Log validation failures
            if invalid_records:
                await self._log_quality_issues(invalid_records)
    
            # 3. Statistical validation (batch-level)
            df = pd.DataFrame(valid_records)
            result = self.ge_context.run_validation(
                batch=df,
                expectation_suite_name="memory_quality"
            )
    
            if not result.success:
                raise DataQualityError(
                    f"Batch failed quality checks: {result.statistics}"
                )
    
            # 4. Proceed with clean data
            await self._load(valid_records)
    

---
  #### **Name**
Backfill Pattern
  #### **Description**
Safely backfill historical data
  #### **When**
Need to reprocess historical data or initialize new pipeline
  #### **Example**
    from datetime import datetime, timedelta
    from typing import Iterator
    import asyncio
    
    class BackfillManager:
        """Manage safe backfills with checkpointing."""
    
        def __init__(self, db, pipeline):
            self.db = db
            self.pipeline = pipeline
    
        async def backfill(
            self,
            start_date: datetime,
            end_date: datetime,
            chunk_size: timedelta = timedelta(days=1),
            parallelism: int = 4
        ):
            """Run backfill with checkpointing and parallelism."""
            chunks = list(self._generate_chunks(start_date, end_date, chunk_size))
    
            # Resume from checkpoint if exists
            completed = await self._get_completed_chunks()
            remaining = [c for c in chunks if c not in completed]
    
            logger.info(
                f"Backfill: {len(remaining)}/{len(chunks)} chunks remaining"
            )
    
            # Process in parallel batches
            for i in range(0, len(remaining), parallelism):
                batch = remaining[i:i + parallelism]
    
                tasks = [
                    self._process_chunk(chunk_start, chunk_end)
                    for chunk_start, chunk_end in batch
                ]
    
                results = await asyncio.gather(*tasks, return_exceptions=True)
    
                # Handle failures
                for (chunk_start, chunk_end), result in zip(batch, results):
                    if isinstance(result, Exception):
                        logger.error(f"Chunk {chunk_start} failed: {result}")
                        await self._mark_failed(chunk_start, chunk_end, str(result))
                    else:
                        await self._mark_completed(chunk_start, chunk_end)
    
        def _generate_chunks(
            self,
            start: datetime,
            end: datetime,
            size: timedelta
        ) -> Iterator[tuple[datetime, datetime]]:
            current = start
            while current < end:
                chunk_end = min(current + size, end)
                yield (current, chunk_end)
                current = chunk_end
    
        async def _process_chunk(self, start: datetime, end: datetime):
            logger.info(f"Processing chunk: {start} to {end}")
            await self.pipeline.run(start_date=start, end_date=end)
    
        async def _mark_completed(self, start: datetime, end: datetime):
            await self.db.execute(
                """
                INSERT INTO backfill_checkpoints (chunk_start, chunk_end, status, completed_at)
                VALUES ($1, $2, 'completed', NOW())
                ON CONFLICT (chunk_start, chunk_end) DO UPDATE SET
                    status = 'completed', completed_at = NOW()
                """,
                start, end
            )
    

## Anti-Patterns


---
  #### **Name**
Non-Idempotent Pipelines
  #### **Description**
Pipelines that produce duplicates on re-run
  #### **Why**
Every pipeline will need re-running. Duplicates corrupt data, break aggregations.
  #### **Instead**
Design for delete-then-insert, use upserts, track processed records

---
  #### **Name**
No Data Validation
  #### **Description**
Loading data without checking quality
  #### **Why**
Garbage in, garbage out. Bad data propagates and is hard to fix.
  #### **Instead**
Validate schema, check business rules, monitor quality metrics

---
  #### **Name**
Polling for Changes
  #### **Description**
Repeatedly querying for updated records
  #### **Why**
Inefficient, misses rapid changes, loads database unnecessarily.
  #### **Instead**
Use CDC (Change Data Capture) for change streaming

---
  #### **Name**
No Checkpointing
  #### **Description**
Long pipelines without progress tracking
  #### **Why**
Failure after 10 hours means restarting from scratch.
  #### **Instead**
Checkpoint progress, enable resumable pipelines

---
  #### **Name**
Mixing Batch and Stream Semantics
  #### **Description**
Treating streaming data like batch or vice versa
  #### **Why**
Different guarantees, different patterns. Mixing causes inconsistency.
  #### **Instead**
Choose the right paradigm, or use Lambda/Kappa architecture