# Ml Memory - Sharp Edges

## Entity Duplication Explosion

### **Id**
entity-duplication-explosion
### **Summary**
Same entity appears hundreds of times with different names
### **Severity**
critical
### **Situation**
  You ingest user conversations without entity resolution. Months later,
  you realize "John", "John Smith", "my husband", "him", and "Dr. Smith"
  are all the same person with 5 different memory graphs.
  
### **Why**
  Users refer to entities in many ways. Without resolution, each variant
  creates new nodes. Queries return fragmented results. Memory is split
  across entities that should be unified.
  
### **Solution**
  # Implement entity resolution pipeline
  class EntityResolver:
      CONFIDENCE_THRESHOLD = 0.7
  
      async def resolve_or_create(
          self,
          mention: str,
          context: str,
          user_id: UUID,
      ) -> Entity:
          # 1. Exact match first
          exact = await self.db.find_entity_exact(mention, user_id)
          if exact:
              return exact
  
          # 2. Semantic similarity search
          candidates = await self.find_similar_entities(
              mention, context, user_id
          )
  
          for candidate in candidates:
              # 3. LLM-based coreference resolution
              is_same, confidence = await self.llm_coreference_check(
                  mention, context, candidate
              )
  
              if is_same and confidence > self.CONFIDENCE_THRESHOLD:
                  # 4. Add alias to existing entity
                  await self.add_alias(candidate, mention)
                  return candidate
  
          # 5. Create new entity only if no match
          return await self.create_entity(mention, user_id)
  
  # Run periodic entity merge jobs to fix historical issues
  
### **Symptoms**
  - Memory graph has duplicate nodes for same person
  - Queries miss relevant memories because entity name differs
  - Entity count growing linearly with conversation length
  - User says 'I already told you about John' but system doesn't find it
### **Detection Pattern**
store.*entity|create.*entity|new.*Entity
### **Version Range**
>=1.0.0

## Zep Graphiti Llm Costs

### **Id**
zep-graphiti-llm-costs
### **Summary**
LLM calls during every ingestion creates massive API bills
### **Severity**
high
### **Situation**
  You use Graphiti/Zep's entity extraction which calls LLM for every
  ingested message. At scale, you're making 100K+ LLM calls per day
  just for entity extraction.
  
### **Why**
  Graphiti uses LLMs for entity extraction, relationship detection, and
  summarization. Each ingested message can trigger 2-5 LLM calls.
  At conversation scale, this becomes prohibitively expensive.
  
### **Solution**
  # Batch extraction to reduce LLM calls
  class BatchEntityExtractor:
      BATCH_SIZE = 10
      MAX_BATCH_DELAY = timedelta(seconds=30)
  
      def __init__(self):
          self.pending_messages = []
          self.last_flush = datetime.utcnow()
  
      async def queue_for_extraction(self, message: Message) -> None:
          self.pending_messages.append(message)
  
          if (
              len(self.pending_messages) >= self.BATCH_SIZE or
              datetime.utcnow() - self.last_flush > self.MAX_BATCH_DELAY
          ):
              await self.flush()
  
      async def flush(self) -> List[Entity]:
          if not self.pending_messages:
              return []
  
          # Single LLM call for entire batch
          combined_text = "\n---\n".join(
              m.content for m in self.pending_messages
          )
  
          entities = await self.llm.extract_entities(combined_text)
  
          # Clear batch
          self.pending_messages = []
          self.last_flush = datetime.utcnow()
  
          return entities
  
  # Also consider: local NER models for first pass
  # spacy, GLiNER, or fine-tuned BERT for entity extraction
  # Only use LLM for relationship inference
  
### **Symptoms**
  - API costs growing linearly with message volume
  - Ingestion latency high due to LLM calls
  - Rate limit errors from embedding/LLM provider
  - Entity extraction is slowest part of pipeline
### **Detection Pattern**
graphiti|zep.*add_episode|extract.*entities.*await
### **Version Range**
>=1.0.0

## Temporal Staleness Current

### **Id**
temporal-staleness-current
### **Summary**
"Current" facts become stale without temporal validity
### **Severity**
high
### **Situation**
  You store "user works at Google" as a fact. Six months later,
  user mentions new job. System still retrieves old job as current
  because it has higher salience.
  
### **Why**
  Facts have temporal validity. "Current job" changes. "Lives in"
  changes. Without valid_until handling, stale facts accumulate
  and pollute retrieval.
  
### **Solution**
  # Always store temporal validity for mutable facts
  @dataclass
  class MemoryFact:
      entity_id: UUID
      predicate: str  # "works_at", "lives_in"
      value: str
      valid_from: datetime
      valid_until: Optional[datetime]  # None = still valid
  
      # Mutable predicates that need temporal handling
      MUTABLE_PREDICATES = {
          "works_at", "lives_in", "married_to", "age",
          "role", "company", "location", "status",
      }
  
  class TemporalFactStore:
      async def add_fact(
          self,
          entity_id: UUID,
          predicate: str,
          value: str,
      ) -> MemoryFact:
          # If mutable predicate, close previous fact
          if predicate in MemoryFact.MUTABLE_PREDICATES:
              await self.db.execute(
                  """
                  UPDATE memory_facts
                  SET valid_until = NOW()
                  WHERE entity_id = $1
                    AND predicate = $2
                    AND valid_until IS NULL
                  """,
                  entity_id, predicate
              )
  
          # Insert new fact
          return await self.db.insert_fact(
              entity_id=entity_id,
              predicate=predicate,
              value=value,
              valid_from=datetime.utcnow(),
              valid_until=None,
          )
  
      async def get_current_facts(self, entity_id: UUID) -> List[MemoryFact]:
          # Only return currently valid facts
          return await self.db.query(
              """
              SELECT * FROM memory_facts
              WHERE entity_id = $1 AND valid_until IS NULL
              """
          )
  
### **Symptoms**
  - Old facts returned instead of current ones
  - User corrects 'I don't work there anymore'
  - Contradictory facts about same entity
  - Memory shows outdated information
### **Detection Pattern**
store.*fact|insert.*fact(?!.*valid_until)
### **Version Range**
>=1.0.0

## Consolidation Conflicts

### **Id**
consolidation-conflicts
### **Summary**
Concurrent consolidation corrupts memory state
### **Severity**
high
### **Situation**
  You run consolidation jobs on a schedule. Two jobs overlap because
  the first one took longer than expected. Memories get promoted twice
  or corrupted.
  
### **Why**
  Consolidation reads, processes, and writes memory state. Without
  locking, concurrent jobs read same state, make conflicting decisions,
  and corrupt data.
  
### **Solution**
  # Use distributed locking for consolidation
  from redis.lock import Lock
  
  class SafeConsolidator:
      LOCK_TIMEOUT = timedelta(minutes=30)
  
      async def consolidate(self, user_id: UUID) -> ConsolidationResult:
          lock_key = f"consolidation:{user_id}"
  
          # Acquire distributed lock
          async with self.redis.lock(
              lock_key,
              timeout=self.LOCK_TIMEOUT.total_seconds(),
              blocking=False,  # Don't wait, skip if locked
          ) as lock:
              if not lock:
                  logger.info(f"Consolidation already running for {user_id}")
                  return ConsolidationResult(skipped=True)
  
              # Use optimistic locking for individual memory updates
              memories = await self.db.get_memories_for_consolidation(
                  user_id, for_update=True  # SELECT FOR UPDATE
              )
  
              for memory in memories:
                  await self._process_memory(memory)
  
              return ConsolidationResult(processed=len(memories))
  
      async def _process_memory(self, memory: Memory) -> None:
          # Include version check in update
          result = await self.db.execute(
              """
              UPDATE memories
              SET temporal_level = $1, version = version + 1
              WHERE memory_id = $2 AND version = $3
              """,
              new_level, memory.memory_id, memory.version
          )
  
          if result.rowcount == 0:
              raise ConcurrencyError(f"Memory {memory.memory_id} modified")
  
### **Symptoms**
  - Memories promoted multiple times
  - Consolidation logs show overlapping runs
  - Inconsistent memory counts after consolidation
  - Database deadlocks during consolidation
### **Detection Pattern**
consolidat.*async|schedule.*consolidat
### **Version Range**
>=1.0.0

## Salience Never Decreases

### **Id**
salience-never-decreases
### **Summary**
Salience only increases, noise accumulates
### **Severity**
medium
### **Situation**
  You implement salience boosting when memories are accessed. Over time,
  all frequently accessed memories have max salience. The ranking becomes
  meaningless.
  
### **Why**
  Without decrease mechanism, salience saturates. Old but once-useful
  memories stay at top. New important memories can't compete. The
  system becomes increasingly noisy.
  
### **Solution**
  # Implement bidirectional salience adjustment
  class BidirectionalSalience:
      BOOST_RATE = 0.1
      DECAY_RATE = 0.02
      OUTCOME_WEIGHT = 0.15
  
      async def on_memory_used(
          self,
          memory_id: UUID,
          outcome: Optional[float],  # -1 to 1, None if unknown
      ) -> None:
          memory = await self.db.get_memory(memory_id)
  
          if outcome is not None:
              # Outcome-based: boost if good, penalize if bad
              adjustment = outcome * self.OUTCOME_WEIGHT
          else:
              # Access-based: small boost for being useful enough to retrieve
              adjustment = self.BOOST_RATE
  
          new_salience = max(0.01, min(1.0, memory.salience + adjustment))
          await self.db.update_salience(memory_id, new_salience)
  
      async def apply_periodic_decay(self, user_id: UUID) -> None:
          """Run daily to decay all memories slightly."""
          await self.db.execute(
              """
              UPDATE memories
              SET salience = GREATEST(0.01, salience - $1)
              WHERE user_id = $2
                AND last_accessed < NOW() - INTERVAL '24 hours'
              """,
              self.DECAY_RATE, user_id
          )
  
      async def penalize_unused(self, user_id: UUID) -> None:
          """Penalize memories that were retrieved but not used."""
          await self.db.execute(
              """
              UPDATE memories
              SET salience = GREATEST(0.01, salience - 0.05)
              WHERE memory_id IN (
                  SELECT memory_id FROM retrieval_log
                  WHERE retrieved_at > NOW() - INTERVAL '24 hours'
                    AND was_used = FALSE
              )
              """
          )
  
### **Symptoms**
  - Most memories at maximum salience
  - New memories hard to surface
  - Retrieval quality degrading over time
  - Old irrelevant memories dominating results
### **Detection Pattern**
salience.*\\+|boost.*salience|increase.*salience
### **Version Range**
>=1.0.0

## Forgetting Breaks References

### **Id**
forgetting-breaks-references
### **Summary**
Forgotten memories leave dangling references
### **Severity**
medium
### **Situation**
  You implement memory forgetting to manage storage. A memory is forgotten,
  but graph edges still point to it. Entity relationships break.
  
### **Why**
  Memories connect to entities, other memories, and decision traces.
  Hard delete without cascade leaves orphaned references and broken
  relationships.
  
### **Solution**
  # Implement soft delete with reference handling
  class SafeForgetting:
      async def forget_memory(
          self,
          memory_id: UUID,
          hard_delete: bool = False,
      ) -> None:
          # 1. Check for active references
          references = await self.db.count_references(memory_id)
  
          if references > 0 and not hard_delete:
              # Soft delete: mark as forgotten but keep for references
              await self.db.execute(
                  """
                  UPDATE memories
                  SET status = 'forgotten',
                      content = '[FORGOTTEN]',  # Clear content
                      embedding = NULL
                  WHERE memory_id = $1
                  """,
                  memory_id
              )
          else:
              # Hard delete: must clean up references first
              async with self.db.transaction():
                  # Remove graph edges
                  await self.graph.delete_memory_edges(memory_id)
  
                  # Remove from decision traces (or mark as unavailable)
                  await self.db.execute(
                      """
                      UPDATE decision_memory_attribution
                      SET memory_available = FALSE
                      WHERE memory_id = $1
                      """,
                      memory_id
                  )
  
                  # Now safe to delete
                  await self.db.delete_memory(memory_id)
  
      async def cleanup_orphaned_references(self) -> int:
          """Periodic job to clean up dangling references."""
          # Find edges pointing to non-existent memories
          orphans = await self.db.query(
              """
              SELECT edge_id FROM memory_edges e
              LEFT JOIN memories m ON e.target_id = m.memory_id
              WHERE m.memory_id IS NULL
              """
          )
  
          for orphan in orphans:
              await self.graph.delete_edge(orphan.edge_id)
  
          return len(orphans)
  
### **Symptoms**
  - Graph queries return null for memory properties
  - Foreign key violations when deleting memories
  - 'Memory not found' errors in decision traces
  - Orphaned edges accumulating in graph
### **Detection Pattern**
delete.*memory|remove.*memory|forget.*memory
### **Version Range**
>=1.0.0

## Embedding Model Mismatch

### **Id**
embedding-model-mismatch
### **Summary**
Query embeddings from different model than stored embeddings
### **Severity**
high
### **Situation**
  You upgrade your embedding model. New queries use the new model,
  but stored embeddings are from the old model. Similarity search
  returns garbage.
  
### **Why**
  Different embedding models produce incompatible vector spaces.
  "text-embedding-3-small" vectors are meaningless when compared to
  "text-embedding-ada-002" vectors. Cosine similarity becomes random.
  
### **Solution**
  # Track embedding model version with each memory
  @dataclass
  class Memory:
      memory_id: UUID
      content: str
      embedding: List[float]
      embedding_model: str  # "text-embedding-3-small"
      embedding_version: str  # "v1.0"
  
  class EmbeddingMigrator:
      async def migrate_embeddings(
          self,
          target_model: str,
          batch_size: int = 100,
      ) -> MigrationResult:
          """Re-embed all memories with new model."""
          cursor = None
          migrated = 0
  
          while True:
              # Get batch of memories with old model
              memories = await self.db.query(
                  """
                  SELECT memory_id, content FROM memories
                  WHERE embedding_model != $1
                  ORDER BY memory_id
                  LIMIT $2 OFFSET $3
                  """,
                  target_model, batch_size, cursor or 0
              )
  
              if not memories:
                  break
  
              # Batch embed
              contents = [m.content for m in memories]
              new_embeddings = await self.embedder.embed_batch(
                  contents, model=target_model
              )
  
              # Update
              for memory, embedding in zip(memories, new_embeddings):
                  await self.db.execute(
                      """
                      UPDATE memories
                      SET embedding = $1, embedding_model = $2
                      WHERE memory_id = $3
                      """,
                      embedding, target_model, memory.memory_id
                  )
  
              migrated += len(memories)
              cursor = (cursor or 0) + batch_size
  
          return MigrationResult(migrated=migrated)
  
  # Query must use same model as stored embeddings
  async def search(self, query: str, user_id: UUID) -> List[Memory]:
      # Get user's embedding model
      model = await self.db.get_user_embedding_model(user_id)
  
      # Embed query with same model
      query_embedding = await self.embedder.embed(query, model=model)
  
      return await self.vector_store.search(query_embedding)
  
### **Symptoms**
  - Vector search returns irrelevant results
  - Similarity scores near zero or random
  - Search quality degraded after model update
  - Some memories never retrieved
### **Detection Pattern**
embed.*model|embedding_model|text-embedding
### **Version Range**
>=1.0.0

## Memory Attribution Missing

### **Id**
memory-attribution-missing
### **Summary**
Can't learn from outcomes without tracking which memories were used
### **Severity**
medium
### **Situation**
  You want to implement outcome-based learning but realize you never
  tracked which memories influenced each decision. You have outcomes
  but no way to credit or blame memories.
  
### **Why**
  Outcome learning requires attribution: which memories were retrieved,
  which were actually used, and what the outcome was. Without this trace,
  you can't close the learning loop.
  
### **Solution**
  # Implement decision tracing from day one
  @dataclass
  class DecisionTrace:
      trace_id: UUID
      user_id: UUID
      decision_context: str  # What was the user asking
      timestamp: datetime
  
      # Memory attribution
      memories_retrieved: List[UUID]  # What was found
      memories_used: List[UUID]  # What was actually in the response
      memory_influence: Dict[UUID, float]  # How much each influenced
  
      # Outcome (filled later)
      outcome_quality: Optional[float]  # -1 to 1
      outcome_source: Optional[str]  # "explicit", "implicit", "inferred"
  
  class DecisionTracer:
      async def start_trace(
          self,
          user_id: UUID,
          context: str,
      ) -> DecisionTrace:
          trace = DecisionTrace(
              trace_id=uuid4(),
              user_id=user_id,
              decision_context=context,
              timestamp=datetime.utcnow(),
              memories_retrieved=[],
              memories_used=[],
              memory_influence={},
          )
          await self.db.insert_trace(trace)
          return trace
  
      async def record_retrieval(
          self,
          trace: DecisionTrace,
          memory_ids: List[UUID],
      ) -> None:
          trace.memories_retrieved = memory_ids
          await self.db.update_trace(trace)
  
      async def record_usage(
          self,
          trace: DecisionTrace,
          memory_ids: List[UUID],
          influence_scores: Dict[UUID, float],
      ) -> None:
          trace.memories_used = memory_ids
          trace.memory_influence = influence_scores
          await self.db.update_trace(trace)
  
      async def record_outcome(
          self,
          trace_id: UUID,
          quality: float,
          source: str,
      ) -> None:
          await self.db.execute(
              """
              UPDATE decision_traces
              SET outcome_quality = $1, outcome_source = $2
              WHERE trace_id = $3
              """,
              quality, source, trace_id
          )
  
          # Trigger salience learning
          trace = await self.db.get_trace(trace_id)
          await self.salience_learner.update_from_outcome(trace)
  
### **Symptoms**
  - Can't implement outcome-based learning
  - No data on which memories were useful
  - Salience remains static
  - Can't debug why bad memories were retrieved
### **Detection Pattern**
retrieve.*memor|search.*memor(?!.*trace|.*log)
### **Version Range**
>=1.0.0