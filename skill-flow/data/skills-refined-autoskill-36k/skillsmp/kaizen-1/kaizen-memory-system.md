# Kaizen Memory & Learning System

**Available in**: v0.5.0+
**Complexity**: Medium
**Use Case**: Persistent agent memory, learning from interactions, FAQ detection, preference adaptation

---

## Quick Reference

```python
from kaizen.memory.storage import FileStorage, SQLiteStorage
from kaizen.memory import ShortTermMemory, LongTermMemory, SemanticMemory
from kaizen.memory import (
    PatternRecognizer,       # FAQ detection
    PreferenceLearner,       # User preferences
    MemoryPromoter,          # Memory promotion
    ErrorCorrectionLearner   # Error learning
)

# Storage backend
storage = FileStorage("memory.jsonl")  # or SQLiteStorage("memory.db")

# Memory types
short_term = ShortTermMemory(storage, ttl_seconds=3600)
long_term = LongTermMemory(storage)
semantic = SemanticMemory(storage)

# Learning mechanisms
promoter = MemoryPromoter(short_term, long_term)
pattern_recognizer = PatternRecognizer(long_term)
preference_learner = PreferenceLearner(long_term)
error_learner = ErrorCorrectionLearner(long_term)
```

---

## Architecture

### Storage Layer (3 Backends)

**FileStorage** - Lightweight JSONL file-based storage
```python
from kaizen.memory.storage import FileStorage

storage = FileStorage("agent_memory.jsonl")

# Store entry
entry_id = storage.create(
    content="User prefers JSON output format",
    metadata={"user_id": "alice", "category": "preference"},
    importance=0.8,
    tags=["preference", "format"]
)

# Read entry
entry = storage.read(entry_id)

# Search entries
results = storage.search(
    query="user preferences",
    filters={"user_id": "alice"},
    limit=10
)

# Update entry
storage.update(entry_id, importance=0.9)

# Delete entry
storage.delete(entry_id)
```

**SQLiteStorage** - Production-grade SQL database with FTS5
```python
from kaizen.memory.storage import SQLiteStorage

storage = SQLiteStorage("agent_memory.db")

# Same API as FileStorage
entry_id = storage.create(content="...", metadata={}, importance=0.8)

# Full-text search (FTS5)
results = storage.search(
    query="python coding preferences",
    filters={"category": "code"},
    limit=5
)

# Vector similarity search (cosine)
similar = storage.similarity_search(
    embedding=[0.1, 0.2, ...],  # Query embedding
    top_k=5
)
```

**PostgreSQLStorage** - Enterprise backend (planned)
```python
# Future: DataFlow integration for PostgreSQL
from kaizen.memory.storage import PostgreSQLStorage

storage = PostgreSQLStorage(database_url="postgresql://...")
```

---

## Memory Types

### ShortTermMemory - Session-scoped memory

**Use Case**: Temporary session context, cleared after session ends

```python
from kaizen.memory import ShortTermMemory

short_term = ShortTermMemory(
    storage=storage,
    ttl_seconds=3600,  # 1 hour TTL
    session_id="user_123_session_456"
)

# Store session-specific memory
short_term.store(
    content="User asked about Python decorators",
    metadata={"topic": "python", "difficulty": "intermediate"},
    importance=0.6
)

# Retrieve recent memories
recent = short_term.retrieve(
    query="python questions",
    top_k=5,
    filters={"topic": "python"}
)

# Clear expired memories (automatic)
short_term.cleanup_expired()

# Clear all session memories
short_term.clear()
```

**Key Features**:
- TTL-based expiration
- Session isolation
- Automatic cleanup
- <20ms retrieval latency

---

### LongTermMemory - Persistent cross-session memory

**Use Case**: Persistent agent knowledge, user history, learned patterns

```python
from kaizen.memory import LongTermMemory

long_term = LongTermMemory(storage=storage)

# Store persistent memory
long_term.store(
    content="User is a senior Python developer",
    metadata={"user_id": "alice", "category": "profile"},
    importance=0.9,
    tags=["profile", "expertise"]
)

# Retrieve by importance
important = long_term.retrieve_by_importance(
    min_importance=0.8,
    limit=10
)

# Retrieve by time range
recent = long_term.retrieve_by_time_range(
    start_timestamp=1697068800,  # Oct 12, 2023
    end_timestamp=1697155200,    # Oct 13, 2023
    limit=50
)

# Consolidate similar memories (reduce redundancy)
result = long_term.consolidate(
    similarity_threshold=0.9,
    merge_strategy="keep_highest_importance"
)
print(f"Merged {result['merged']} duplicate memories")

# Archive old memories
long_term.archive(
    age_threshold_days=90,
    min_importance=0.5
)
```

**Key Features**:
- Persistent storage
- Importance-based retrieval
- Memory consolidation
- Archival support

---

### SemanticMemory - Concept extraction and retrieval

**Use Case**: Knowledge graphs, concept relationships, semantic search

```python
from kaizen.memory import SemanticMemory

semantic = SemanticMemory(storage=storage)

# Store with concept extraction
semantic.store(
    content="Python decorators are functions that modify other functions",
    metadata={"source": "conversation", "timestamp": 1697068800},
    importance=0.7
)
# Automatically extracts concepts: ["python", "decorators", "functions"]

# Semantic similarity search
similar = semantic.search_similar(
    query="What are Python function modifiers?",
    top_k=5,
    similarity_threshold=0.7
)

# Retrieve by concept
decorator_memories = semantic.retrieve_by_concept(
    concept="decorators",
    limit=10
)

# Get concept relationships
relationships = semantic.get_concept_relationships(
    concept="python",
    max_depth=2
)
# Returns: {"decorators": 0.9, "functions": 0.85, ...}

# Extract concepts from text
concepts = semantic.extract_concepts(
    text="User wants to learn about async/await in Python"
)
# Returns: ["async", "await", "python", "concurrency"]
```

**Key Features**:
- Automatic concept extraction
- Cosine similarity search
- Concept relationships
- <50ms semantic search

---

## Learning Mechanisms

### PatternRecognizer - FAQ detection and access patterns

**Use Case**: Detect frequently asked questions, common workflows

```python
from kaizen.memory import PatternRecognizer

recognizer = PatternRecognizer(memory=long_term)

# Detect FAQs (frequently asked questions)
faqs = recognizer.detect_faqs(
    min_frequency=5,           # Asked 5+ times
    similarity_threshold=0.85,  # 85% similar questions
    time_window_days=30        # In last 30 days
)

for faq in faqs:
    print(f"FAQ: {faq['question']}")
    print(f"  Asked {faq['frequency']} times")
    print(f"  Best answer: {faq['best_answer']}")
    print(f"  Confidence: {faq['confidence']:.2f}")

# Detect access patterns
patterns = recognizer.detect_patterns(
    pattern_type="sequential",  # or "parallel", "cyclic"
    min_occurrences=3,
    time_window_hours=24
)

for pattern in patterns:
    print(f"Pattern: {pattern['steps']}")
    print(f"  Frequency: {pattern['frequency']}")
    print(f"  Avg duration: {pattern['avg_duration_seconds']}s")

# Get pattern recommendations
recommendations = recognizer.recommend_based_on_patterns(
    current_context="User is writing a Python function",
    top_k=3
)
```

**Key Features**:
- FAQ detection with similarity clustering
- Sequential, parallel, cyclic pattern detection
- Pattern-based recommendations
- Confidence scoring

---

### PreferenceLearner - User preference learning

**Use Case**: Learn user preferences over time, personalize responses

```python
from kaizen.memory import PreferenceLearner

learner = PreferenceLearner(memory=long_term)

# Learn preferences from interactions
preferences = learner.learn_preferences(
    user_id="alice",
    min_occurrences=3,  # Require 3+ examples
    time_window_days=90
)

for pref in preferences:
    print(f"Preference: {pref['category']}")
    print(f"  Value: {pref['value']}")
    print(f"  Confidence: {pref['confidence']:.2f}")
    print(f"  Examples: {pref['example_count']}")

# Example output:
# Preference: output_format
#   Value: json
#   Confidence: 0.95
#   Examples: 12
#
# Preference: code_style
#   Value: functional
#   Confidence: 0.85
#   Examples: 8

# Get preference for category
format_pref = learner.get_preference(
    user_id="alice",
    category="output_format"
)
# Returns: {"value": "json", "confidence": 0.95}

# Update preference based on new data
learner.update_preference(
    user_id="alice",
    category="verbosity",
    value="concise",
    importance=0.8
)

# Get all preferences for user
all_prefs = learner.get_user_preferences(user_id="alice")
```

**Key Features**:
- Multi-category preference learning
- Confidence scoring
- Automatic aggregation
- Preference history tracking

---

### MemoryPromoter - Short-term to long-term promotion

**Use Case**: Auto-promote important session memories to persistent storage

```python
from kaizen.memory import MemoryPromoter

promoter = MemoryPromoter(
    short_term_memory=short_term,
    long_term_memory=long_term
)

# Auto-promote based on criteria
result = promoter.auto_promote(
    min_importance=0.7,         # Importance >= 0.7
    min_access_count=3,         # Accessed 3+ times
    age_threshold_seconds=3600  # Older than 1 hour
)

print(f"Promoted {result['promoted']} memories")
print(f"Skipped {result['skipped']} (already in long-term)")
print(f"Failed {result['failed']} (promotion errors)")

# Manual promotion with filtering
result = promoter.promote_by_filter(
    filters={"category": "important", "user_id": "alice"},
    copy_metadata=True,
    increase_importance=0.1  # Boost importance by 0.1
)

# Promote specific memory
success = promoter.promote_memory(
    memory_id="mem_123",
    override_importance=0.9
)

# Get promotion candidates
candidates = promoter.get_promotion_candidates(
    min_importance=0.6,
    min_access_count=2,
    age_threshold_seconds=7200  # 2 hours
)
print(f"Found {len(candidates)} memories ready for promotion")
```

**Key Features**:
- Automatic promotion based on criteria
- Importance boosting
- Duplicate detection
- Batch promotion

---

### ErrorCorrectionLearner - Learn from mistakes

**Use Case**: Track errors, learn patterns, avoid repeating mistakes

```python
from kaizen.memory import ErrorCorrectionLearner

learner = ErrorCorrectionLearner(memory=long_term)

# Analyze error patterns
errors = learner.analyze_errors(
    min_frequency=2,              # Occurred 2+ times
    time_window_seconds=604800,   # In last 7 days
    similarity_threshold=0.8
)

for error in errors:
    print(f"Error Pattern: {error['error_type']}")
    print(f"  Frequency: {error['frequency']}")
    print(f"  Last seen: {error['last_occurrence']}")
    print(f"  Corrective action: {error['correction']}")
    print(f"  Success rate: {error['correction_success_rate']:.2f}")

# Record error with correction
learner.record_error(
    error_type="type_error",
    context="User passed string instead of int to calculate_age()",
    correction="Added type validation with descriptive error message",
    success=True
)

# Get correction for error
correction = learner.get_correction(
    error_type="type_error",
    context="Invalid input type",
    top_k=1
)

if correction:
    print(f"Suggested fix: {correction['action']}")
    print(f"Confidence: {correction['confidence']:.2f}")
    print(f"Success rate: {correction['success_rate']:.2f}")

# Get error prevention recommendations
recommendations = learner.recommend_preventions(
    current_context="Processing user input for numeric calculation",
    top_k=3
)
```

**Key Features**:
- Error pattern clustering
- Corrective action tracking
- Success rate metrics
- Prevention recommendations

---

## Integration with BaseAgent

### Option 1: Manual Memory Management

```python
from kaizen.core.base_agent import BaseAgent
from kaizen.memory import LongTermMemory, SemanticMemory
from kaizen.memory.storage import SQLiteStorage

class MemoryEnabledAgent(BaseAgent):
    def __init__(self, config):
        super().__init__(config=config, signature=MySignature())

        # Setup memory system
        storage = SQLiteStorage("agent_memory.db")
        self.long_term = LongTermMemory(storage)
        self.semantic = SemanticMemory(storage)

    def process_with_memory(self, user_input: str, user_id: str):
        # Retrieve relevant memories
        relevant = self.semantic.search_similar(
            query=user_input,
            top_k=5,
            similarity_threshold=0.7
        )

        # Add context to prompt
        memory_context = "\n".join([m.content for m in relevant])
        enhanced_input = f"{memory_context}\n\nUser: {user_input}"

        # Execute agent
        result = self.run(input=enhanced_input)

        # Store interaction in memory
        self.long_term.store(
            content=f"Q: {user_input}\nA: {result['output']}",
            metadata={"user_id": user_id, "timestamp": time.time()},
            importance=0.7
        )

        return result
```

### Option 2: BaseAgent Memory Integration (Future)

```python
# Future: Built-in memory support
from kaizen.core.base_agent import BaseAgent

class MyAgent(BaseAgent):
    def __init__(self, config):
        super().__init__(
            config=config,
            signature=MySignature(),
            enable_memory=True,           # Enable memory system
            memory_backend="sqlite",       # Storage backend
            memory_config={
                "database_path": "memory.db",
                "enable_semantic": True,
                "enable_learning": True
            }
        )

    def ask(self, question: str, user_id: str):
        # Memory automatically injected into context
        result = self.run(question=question, user_id=user_id)

        # Memory automatically stored
        return result
```

---

## Performance Characteristics

| Operation | Latency (p95) | Throughput | Notes |
|-----------|---------------|------------|-------|
| Store (FileStorage) | <5ms | 1000/s | JSONL append |
| Store (SQLiteStorage) | <20ms | 500/s | SQL insert with index |
| Retrieve (FileStorage) | <30ms | 200/s | Linear scan with index |
| Retrieve (SQLiteStorage) | <10ms | 1000/s | B-tree index |
| Semantic search | <50ms | 100/s | Cosine similarity |
| Pattern detection | <500ms | 10/s | Clustering algorithm |
| Preference learning | <200ms | 50/s | Aggregation query |

**Tested with**: 10,000 entries per agent

---

## Best Practices

### 1. Choose the Right Backend

```python
# Development/prototyping: FileStorage
storage = FileStorage("dev_memory.jsonl")

# Production (single instance): SQLiteStorage
storage = SQLiteStorage("prod_memory.db")

# Production (distributed): PostgreSQLStorage (future)
storage = PostgreSQLStorage(database_url="postgresql://...")
```

### 2. Set Appropriate Importance Scores

```python
# Critical user preferences
importance = 0.9

# Important conversation context
importance = 0.7

# General interaction history
importance = 0.5

# Temporary session data
importance = 0.3
```

### 3. Use Memory Consolidation

```python
# Run consolidation daily
import schedule

def consolidate_memories():
    result = long_term.consolidate(
        similarity_threshold=0.9,
        merge_strategy="keep_highest_importance"
    )
    print(f"Merged {result['merged']} duplicate memories")

schedule.every().day.at("03:00").do(consolidate_memories)
```

### 4. Implement Memory Archival

```python
# Archive old, low-importance memories monthly
def archive_old_memories():
    long_term.archive(
        age_threshold_days=90,  # 90+ days old
        min_importance=0.5      # Importance < 0.5
    )

schedule.every().month.do(archive_old_memories)
```

### 5. Monitor Memory Growth

```python
# Check memory size regularly
stats = storage.get_statistics()
print(f"Total entries: {stats['total_entries']}")
print(f"Storage size: {stats['size_mb']} MB")
print(f"Avg importance: {stats['avg_importance']:.2f}")

# Alert if too large
if stats['size_mb'] > 1000:  # 1GB
    print("WARNING: Memory size exceeds 1GB, consider archival")
```

---

## Common Patterns

### Pattern 1: FAQ Bot with Memory

```python
recognizer = PatternRecognizer(long_term)

def handle_question(question: str):
    # Check if FAQ
    faqs = recognizer.detect_faqs(
        min_frequency=3,
        similarity_threshold=0.85
    )

    for faq in faqs:
        if is_similar(question, faq['question'], threshold=0.85):
            return faq['best_answer']

    # Not FAQ, process normally
    result = agent.ask(question)

    # Store for future FAQ detection
    long_term.store(
        content=f"Q: {question}\nA: {result['answer']}",
        metadata={"category": "qa"},
        importance=0.6
    )

    return result
```

### Pattern 2: Personalized Agent

```python
preference_learner = PreferenceLearner(long_term)

def personalized_response(user_id: str, prompt: str):
    # Get user preferences
    prefs = preference_learner.get_user_preferences(user_id)

    # Customize prompt based on preferences
    if prefs.get("verbosity") == "concise":
        prompt += "\n(Keep response brief)"
    if prefs.get("format") == "json":
        prompt += "\n(Return as JSON)"

    result = agent.run(input=prompt)

    # Learn new preferences from interaction
    preference_learner.update_preference(
        user_id=user_id,
        category="topic_interest",
        value=extract_topic(prompt),
        importance=0.7
    )

    return result
```

### Pattern 3: Error-Aware Agent

```python
error_learner = ErrorCorrectionLearner(long_term)

def execute_with_error_learning(task: str):
    try:
        # Check for known errors
        known_errors = error_learner.analyze_errors(
            min_frequency=1,
            time_window_seconds=2592000  # 30 days
        )

        # Apply preventions
        for error in known_errors:
            if error['context'] in task:
                print(f"Applying prevention: {error['correction']}")
                task = apply_correction(task, error['correction'])

        # Execute
        result = agent.run(task=task)
        return result

    except Exception as e:
        # Record error for learning
        error_learner.record_error(
            error_type=type(e).__name__,
            context=task,
            correction="",  # To be filled manually
            success=False
        )
        raise
```

---

## Troubleshooting

### Issue 1: Slow Retrieval

**Problem**: Memory retrieval takes >100ms

**Solutions**:
```python
# 1. Use SQLite instead of FileStorage
storage = SQLiteStorage("memory.db")  # Much faster for large datasets

# 2. Add indexes to metadata fields
storage.create_index("user_id")
storage.create_index("category")

# 3. Limit result set
results = memory.retrieve(query="...", top_k=10)  # Instead of top_k=100

# 4. Archive old memories
long_term.archive(age_threshold_days=90, min_importance=0.5)
```

### Issue 2: Memory Growing Too Large

**Problem**: Storage file/database growing unbounded

**Solutions**:
```python
# 1. Enable automatic consolidation
result = long_term.consolidate(
    similarity_threshold=0.9,
    merge_strategy="keep_highest_importance"
)

# 2. Archive old memories
long_term.archive(age_threshold_days=90)

# 3. Set TTL for short-term memory
short_term = ShortTermMemory(storage, ttl_seconds=3600)

# 4. Delete low-importance memories
storage.delete_by_filter(filters={"importance": {"$lt": 0.3}})
```

### Issue 3: Poor Semantic Search Results

**Problem**: Semantic search returns irrelevant results

**Solutions**:
```python
# 1. Increase similarity threshold
results = semantic.search_similar(
    query="...",
    similarity_threshold=0.8  # Instead of 0.5
)

# 2. Use better embeddings
# (Future: Switch to sentence-transformers or OpenAI embeddings)

# 3. Add metadata filters
results = semantic.search_similar(
    query="...",
    filters={"category": "technical", "user_id": "alice"}
)

# 4. Use keyword search as fallback
semantic_results = semantic.search_similar(query="...")
if not semantic_results:
    keyword_results = storage.search(query="...")
```

---

## References

- **Source Code**: `src/kaizen/memory/`
- **Tests**: `tests/unit/memory/`

---

**Status**: Production-ready (v0.5.0+)
**Performance**: All targets met (<50ms retrieval, <100ms storage)
**Backward Compatible**: 100% (opt-in, no breaking changes)
