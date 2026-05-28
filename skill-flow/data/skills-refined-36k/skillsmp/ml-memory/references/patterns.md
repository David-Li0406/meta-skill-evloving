# ML Memory Engineer

## Patterns


---
  #### **Name**
Hierarchical Memory Levels
  #### **Description**
Four-level temporal memory with promotion rules
  #### **When**
Designing memory storage architecture
  #### **Example**
    from dataclasses import dataclass
    from datetime import timedelta
    from enum import Enum
    from typing import Optional
    
    class TemporalLevel(Enum):
        IMMEDIATE = "immediate"       # Hours - what just happened
        SITUATIONAL = "situational"   # Days/weeks - current context
        SEASONAL = "seasonal"         # Months - recurring patterns
        IDENTITY = "identity"         # Years - core user facts
    
    @dataclass
    class LevelConfig:
        decay_period: timedelta
        max_items: int
        promotion_threshold: int
        consolidation_frequency: timedelta
    
    LEVEL_CONFIGS = {
        TemporalLevel.IMMEDIATE: LevelConfig(
            decay_period=timedelta(hours=24),
            max_items=100,
            promotion_threshold=5,
            consolidation_frequency=timedelta(hours=6),
        ),
        TemporalLevel.SITUATIONAL: LevelConfig(
            decay_period=timedelta(days=14),
            max_items=500,
            promotion_threshold=10,
            consolidation_frequency=timedelta(days=1),
        ),
        TemporalLevel.SEASONAL: LevelConfig(
            decay_period=timedelta(days=180),
            max_items=1000,
            promotion_threshold=20,
            consolidation_frequency=timedelta(weeks=1),
        ),
        TemporalLevel.IDENTITY: LevelConfig(
            decay_period=timedelta(days=3650),
            max_items=200,
            promotion_threshold=None,  # No promotion from identity
            consolidation_frequency=timedelta(weeks=4),
        ),
    }
    

---
  #### **Name**
Outcome-Based Salience Learning
  #### **Description**
Adjust memory importance based on decision outcomes
  #### **When**
Implementing feedback loops for memory quality
  #### **Example**
    from uuid import UUID
    from typing import Dict
    
    class SalienceLearner:
        """Learn which memories actually help decisions."""
    
        LEARNING_RATE = 0.1
        MIN_SALIENCE = 0.01
        MAX_SALIENCE = 1.0
    
        async def update_from_outcome(
            self,
            trace: DecisionTrace,
        ) -> Dict[UUID, float]:
            """Adjust memory salience based on decision outcomes.
    
            If memory was used and outcome was good: boost salience
            If memory was used and outcome was bad: reduce salience
            """
            if trace.outcome_quality is None:
                return {}
    
            adjustments = {}
    
            for memory_id, influence in trace.memory_attribution.items():
                # Influence: how much this memory affected the decision (0-1)
                # Outcome quality: how good was the decision (-1 to 1)
                adjustment = trace.outcome_quality * influence * self.LEARNING_RATE
    
                # Apply bounded adjustment
                current = await self.db.get_salience(memory_id)
                new_salience = max(
                    self.MIN_SALIENCE,
                    min(self.MAX_SALIENCE, current + adjustment)
                )
    
                await self.db.update_salience(memory_id, new_salience)
                adjustments[memory_id] = adjustment
    
            return adjustments
    

---
  #### **Name**
Memory Decay with Grace Period
  #### **Description**
Exponential decay with protection for recently accessed memories
  #### **When**
Implementing forgetting strategies
  #### **Example**
    from datetime import datetime, timedelta
    import math
    
    class MemoryDecay:
        """Implement forgetting with grace period protection."""
    
        GRACE_PERIOD = timedelta(hours=24)
        DECAY_HALF_LIFE_HOURS = 72  # Memory loses half its salience in 72 hours
    
        def calculate_effective_salience(
            self,
            memory: Memory,
            now: datetime = None,
        ) -> float:
            """Calculate current salience with decay applied."""
            now = now or datetime.utcnow()
    
            # Recently accessed memories don't decay
            if memory.last_accessed:
                time_since_access = now - memory.last_accessed
                if time_since_access < self.GRACE_PERIOD:
                    return memory.base_salience
    
            # Apply exponential decay from last access or creation
            reference_time = memory.last_accessed or memory.created_at
            hours_elapsed = (now - reference_time).total_seconds() / 3600
    
            decay_factor = math.pow(0.5, hours_elapsed / self.DECAY_HALF_LIFE_HOURS)
    
            return memory.base_salience * decay_factor
    
        async def should_forget(
            self,
            memory: Memory,
            config: LevelConfig,
        ) -> bool:
            """Determine if memory should be forgotten."""
            effective_salience = self.calculate_effective_salience(memory)
    
            # Below threshold and past decay period
            if effective_salience < 0.05:
                age = datetime.utcnow() - memory.created_at
                if age > config.decay_period:
                    return True
    
            return False
    

---
  #### **Name**
Contradiction Resolution
  #### **Description**
Handle conflicting memories with temporal precedence
  #### **When**
Same entity has contradictory facts
  #### **Example**
    from typing import List, Optional
    from dataclasses import dataclass
    from datetime import datetime
    
    @dataclass
    class ContradictionResolution:
        winner: Memory
        loser: Memory
        reason: str
        action: str  # "deprecate", "merge", "keep_both"
    
    class ContradictionResolver:
        """Resolve conflicting memories about same entity."""
    
        async def detect_contradiction(
            self,
            new_memory: Memory,
            existing: List[Memory],
        ) -> Optional[ContradictionResolution]:
            """Check if new memory contradicts existing ones."""
    
            for existing_memory in existing:
                if not self._same_entity(new_memory, existing_memory):
                    continue
    
                if self._facts_contradict(new_memory, existing_memory):
                    return await self._resolve(new_memory, existing_memory)
    
            return None
    
        async def _resolve(
            self,
            new: Memory,
            old: Memory,
        ) -> ContradictionResolution:
            """Resolve contradiction between memories."""
    
            # Rule 1: More recent observation wins for mutable facts
            if self._is_mutable_fact(new) and new.observed_at > old.observed_at:
                return ContradictionResolution(
                    winner=new,
                    loser=old,
                    reason="newer_observation",
                    action="deprecate",
                )
    
            # Rule 2: Higher confidence wins
            if new.confidence > old.confidence + 0.2:
                return ContradictionResolution(
                    winner=new,
                    loser=old,
                    reason="higher_confidence",
                    action="deprecate",
                )
    
            # Rule 3: More evidence wins
            if new.evidence_count > old.evidence_count * 2:
                return ContradictionResolution(
                    winner=new,
                    loser=old,
                    reason="more_evidence",
                    action="deprecate",
                )
    
            # Rule 4: When unclear, keep both with temporal validity
            return ContradictionResolution(
                winner=new,
                loser=old,
                reason="temporal_validity",
                action="keep_both",
            )
    

## Anti-Patterns


---
  #### **Name**
Static Salience
  #### **Description**
Hardcoded importance scores that never learn
  #### **Why**
Memory quality depends on actual usefulness. Without learning, you're guessing.
  #### **Instead**
Implement outcome-based salience adjustment from decision traces

---
  #### **Name**
No Forgetting Strategy
  #### **Description**
Keeping all memories forever
  #### **Why**
Unbounded growth. Noise overwhelms signal. Retrieval quality degrades.
  #### **Instead**
Implement decay, consolidation, and explicit forgetting

---
  #### **Name**
Equal Treatment
  #### **Description**
All memories stored and retrieved the same way
  #### **Why**
Episodic and semantic memories have different lifecycle and access patterns.
  #### **Instead**
Use hierarchical levels with different policies

---
  #### **Name**
No Entity Resolution
  #### **Description**
Storing entities as they appear without deduplication
  #### **Why**
Same person appears as "John", "John Smith", "my boss" - massive duplication.
  #### **Instead**
Implement entity resolution pipeline with confidence thresholds

---
  #### **Name**
Missing Outcome Feedback
  #### **Description**
No connection between memory retrieval and decision quality
  #### **Why**
Can't learn what's useful without measuring outcomes.
  #### **Instead**
Track decision traces and attribute outcomes to memories used