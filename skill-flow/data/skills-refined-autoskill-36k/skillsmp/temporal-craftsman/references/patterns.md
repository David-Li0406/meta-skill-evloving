# Temporal Craftsman

## Patterns


---
  #### **Name**
Workflow with Proper Timeouts
  #### **Description**
Set explicit timeouts for all operations
  #### **When**
Defining any workflow or activity
  #### **Example**
    from temporalio import workflow, activity
    from temporalio.common import RetryPolicy
    from datetime import timedelta
    
    @workflow.defn
    class MemoryConsolidationWorkflow:
        @workflow.run
        async def run(self, user_id: str) -> ConsolidationResult:
            # Activity with explicit timeouts
            memories = await workflow.execute_activity(
                fetch_memories,
                user_id,
                start_to_close_timeout=timedelta(minutes=5),
                retry_policy=RetryPolicy(
                    initial_interval=timedelta(seconds=1),
                    maximum_interval=timedelta(minutes=1),
                    maximum_attempts=3,
                    non_retryable_error_types=["ValueError"],
                ),
            )
    
            # Workflow timeout for overall execution
            # Set in workflow starter, not here
    
    # Starting workflow with timeout
    handle = await client.start_workflow(
        MemoryConsolidationWorkflow.run,
        user_id,
        id=f"consolidation-{user_id}",
        task_queue="consolidation",
        execution_timeout=timedelta(hours=24),  # Max workflow duration
        run_timeout=timedelta(hours=1),  # Max single run
    )
    

---
  #### **Name**
Activity with Heartbeat
  #### **Description**
Long-running activities must heartbeat to prevent timeout
  #### **When**
Any activity that might take more than a minute
  #### **Example**
    @activity.defn
    async def process_memories_batch(memory_ids: List[str]) -> int:
        processed = 0
    
        for memory_id in memory_ids:
            # Heartbeat with progress info
            activity.heartbeat(f"Processing {processed}/{len(memory_ids)}")
    
            # Check for cancellation
            if activity.is_cancelled():
                raise asyncio.CancelledError()
    
            await process_single_memory(memory_id)
            processed += 1
    
        return processed
    
    # Activity must be called with heartbeat timeout
    await workflow.execute_activity(
        process_memories_batch,
        memory_ids,
        start_to_close_timeout=timedelta(hours=2),
        heartbeat_timeout=timedelta(minutes=1),  # Fail if no heartbeat for 1 min
    )
    

---
  #### **Name**
Workflow Versioning
  #### **Description**
Handle running workflows during code changes
  #### **When**
Modifying workflow logic that has running instances
  #### **Example**
    @workflow.defn
    class MemoryProcessingWorkflow:
        @workflow.run
        async def run(self, input: ProcessInput) -> ProcessResult:
            # Use patching for deterministic version branching
            if workflow.patched("add-validation-step"):
                # New code path - only for workflows started after patch
                await workflow.execute_activity(
                    validate_memories,
                    input.memories,
                    start_to_close_timeout=timedelta(minutes=5),
                )
    
            # Original code continues
            result = await workflow.execute_activity(
                process_memories,
                input.memories,
                start_to_close_timeout=timedelta(minutes=30),
            )
    
            return result
    
    # After all old workflows complete, simplify:
    if workflow.deprecate_patch("add-validation-step"):
        # This branch runs for all workflows now
        await workflow.execute_activity(validate_memories, ...)
    

---
  #### **Name**
Saga with Compensation
  #### **Description**
Multi-step process with rollback on failure
  #### **When**
Operations that need atomicity across services
  #### **Example**
    @workflow.defn
    class MemoryMigrationSaga:
        def __init__(self):
            self.compensations: List[Callable] = []
    
        @workflow.run
        async def run(self, input: MigrationInput) -> MigrationResult:
            try:
                # Step 1: Export from source
                export_id = await workflow.execute_activity(
                    export_memories,
                    input.source_id,
                    start_to_close_timeout=timedelta(minutes=30),
                )
                self.compensations.append(lambda: delete_export(export_id))
    
                # Step 2: Transform data
                transformed = await workflow.execute_activity(
                    transform_memories,
                    export_id,
                    start_to_close_timeout=timedelta(minutes=30),
                )
                self.compensations.append(lambda: delete_transformed(transformed.id))
    
                # Step 3: Import to destination
                import_id = await workflow.execute_activity(
                    import_memories,
                    transformed.id,
                    input.dest_id,
                    start_to_close_timeout=timedelta(minutes=30),
                )
    
                return MigrationResult(success=True, import_id=import_id)
    
            except Exception as e:
                # Compensate in reverse order
                for compensation in reversed(self.compensations):
                    try:
                        await workflow.execute_activity(
                            compensation,
                            start_to_close_timeout=timedelta(minutes=5),
                        )
                    except Exception:
                        workflow.logger.error("Compensation failed", exc_info=True)
    
                return MigrationResult(success=False, error=str(e))
    

## Anti-Patterns


---
  #### **Name**
I/O in Workflow Code
  #### **Description**
Making HTTP calls, database queries, or file I/O in workflow
  #### **Why**
Workflows are replayed. I/O during replay causes non-determinism and duplicates.
  #### **Instead**
Move all I/O to activities

---
  #### **Name**
Non-Deterministic Operations
  #### **Description**
Using random(), datetime.now(), or UUID generation in workflows
  #### **Why**
Replay produces different values, breaking workflow history.
  #### **Instead**
Use workflow.uuid4(), workflow.now(), or pass values from activities

---
  #### **Name**
Missing Heartbeats
  #### **Description**
Long activities without heartbeat
  #### **Why**
Activity timeout kills the activity, workflow retries, progress lost.
  #### **Instead**
Heartbeat every 10-30 seconds in long activities

---
  #### **Name**
Unbounded Workflow History
  #### **Description**
Workflows that run forever, accumulating history
  #### **Why**
History size limit (50K events default) causes workflow failure.
  #### **Instead**
Use continue-as-new to reset history for long-running workflows

---
  #### **Name**
Skipping Versioning
  #### **Description**
Changing workflow code without patching
  #### **Why**
Running workflows fail on replay with non-determinism errors.
  #### **Instead**
Use workflow.patched() for all logic changes