---
name: kaizen-persistent-memory
description: "Kaizen persistent buffer memory with DataFlow backend - conversation persistence, dual-buffer architecture, auto-persist. Use when asking about 'persistent memory', 'conversation history', 'buffer memory', 'DataFlow memory', 'cross-session persistence', 'auto-persist', 'memory compression', 'conversational agents', or 'stateful agents'."
---

# Kaizen Persistent Buffer Memory (v0.6.0)

Production-ready conversation persistence with DataFlow backend and dual-buffer architecture.

## Overview

Persistent Buffer Memory provides:
- **DataFlow Backend**: Zero-config database persistence with automatic schema
- **Dual-Buffer Architecture**: In-memory buffer + database storage
- **Auto-Persist**: Configurable auto-persist interval (every N messages)
- **JSONL Compression**: Reduces storage by 60%+ with gzip
- **Multi-Instance**: Agent-specific memory isolation (agent_id scoping)
- **Cross-Session**: Load conversation history across restarts

## Quick Start

### Basic Usage

```python
from kaizen.memory import PersistentBufferMemory
from dataflow import DataFlow

# Initialize DataFlow backend (automatic schema creation)
db = DataFlow(
    database_type="sqlite",
    database_config={"database": "./agent_memory.db"}
)

# Create persistent buffer memory
memory = PersistentBufferMemory(
    db=db,
    agent_id="agent_001",
    buffer_size=100,              # Keep last 100 messages in memory
    auto_persist_interval=10,     # Auto-persist every 10 messages
    enable_compression=True       # JSONL compression for storage
)

# Add conversation turns
memory.add_message(role="user", content="What is AI?")
memory.add_message(role="assistant", content="AI is artificial intelligence...")

# Retrieve conversation history
history = memory.get_history(limit=10)  # Last 10 messages

# Persist to database
memory.persist()  # Manual persist (or waits for auto_persist_interval)

# Load from database in next session
memory_loaded = PersistentBufferMemory(db=db, agent_id="agent_001")
memory_loaded.load_from_db()  # Restores conversation history
```

## Architecture

### Dual-Buffer Design

1. **In-Memory Buffer**: Fast access to recent messages (<1ms retrieval)
2. **Database Storage**: Persistent storage survives restarts
3. **Auto-Sync**: Automatic persist when buffer reaches threshold

```
┌─────────────────────────────────────┐
│  In-Memory Buffer (Last 100 msgs)  │  ← Fast reads
├─────────────────────────────────────┤
│      Auto-Persist (Every 10)       │  ← Automatic sync
├─────────────────────────────────────┤
│  DataFlow Database (All history)   │  ← Persistent storage
└─────────────────────────────────────┘
```

### Key Benefits

- **Fast Access**: In-memory buffer for recent messages
- **Persistent**: Database storage survives restarts
- **Automatic**: Auto-persist prevents data loss
- **Scalable**: DataFlow handles multi-tenancy and sharding
- **Efficient**: Compression reduces storage by 60%+

## Conversational Agent Pattern

### Example: Conversational QA Agent

```python
from kaizen.agents import SimpleQAAgent
from kaizen.memory import PersistentBufferMemory

class ConversationalAgent(SimpleQAAgent):
    def __init__(self, config, db):
        super().__init__(config)
        self.memory = PersistentBufferMemory(
            db=db,
            agent_id=self.agent_id,
            buffer_size=50,
            auto_persist_interval=5
        )
        # Load previous conversations
        self.memory.load_from_db()

    def ask(self, question: str) -> dict:
        # Add user message to memory
        self.memory.add_message(role="user", content=question)

        # Get conversation context
        history = self.memory.get_history(limit=10)

        # Run agent with context
        result = self.run(question=question, context=history)

        # Add assistant response to memory
        self.memory.add_message(role="assistant", content=result["answer"])

        return result

# Usage - conversation persists across sessions
agent = ConversationalAgent(config, db)
result1 = agent.ask("What is AI?")
result2 = agent.ask("Can you elaborate?")  # Uses history from previous question

# Stop and restart - history preserved
agent2 = ConversationalAgent(config, db)
result3 = agent2.ask("What did we discuss?")  # Remembers previous conversation
```

## Configuration Options

### Buffer Size

```python
# Small buffer for recent context only
memory = PersistentBufferMemory(
    db=db,
    agent_id="agent_001",
    buffer_size=20  # Last 20 messages only
)

# Large buffer for extended context
memory = PersistentBufferMemory(
    db=db,
    agent_id="agent_001",
    buffer_size=200  # Last 200 messages
)
```

### Auto-Persist Interval

```python
# Persist every message (safest, but slower)
memory = PersistentBufferMemory(
    db=db,
    agent_id="agent_001",
    auto_persist_interval=1
)

# Persist every 50 messages (faster, less safe)
memory = PersistentBufferMemory(
    db=db,
    agent_id="agent_001",
    auto_persist_interval=50
)

# Manual persist only (full control)
memory = PersistentBufferMemory(
    db=db,
    agent_id="agent_001",
    auto_persist_interval=None  # No auto-persist
)
memory.persist()  # Call manually
```

### Compression

```python
# Enable compression (reduces storage by 60%+)
memory = PersistentBufferMemory(
    db=db,
    agent_id="agent_001",
    enable_compression=True  # Default
)

# Disable compression (faster, but larger storage)
memory = PersistentBufferMemory(
    db=db,
    agent_id="agent_001",
    enable_compression=False
)
```

## Multi-Instance Support

Isolate memory per agent using agent_id:

```python
# Agent 1 memory
memory1 = PersistentBufferMemory(db=db, agent_id="agent_001")
memory1.add_message(role="user", content="Hello from agent 1")

# Agent 2 memory (isolated)
memory2 = PersistentBufferMemory(db=db, agent_id="agent_002")
memory2.add_message(role="user", content="Hello from agent 2")

# Agent 1 cannot see agent 2's messages
history1 = memory1.get_history()  # Only agent_001 messages
history2 = memory2.get_history()  # Only agent_002 messages
```

## Database Backend Options

### SQLite (Default)

```python
from dataflow import DataFlow

db = DataFlow(
    database_type="sqlite",
    database_config={"database": "./agent_memory.db"}
)
memory = PersistentBufferMemory(db=db, agent_id="agent_001")
```

### PostgreSQL

```python
db = DataFlow(
    database_type="postgresql",
    database_config={
        "host": "localhost",
        "port": 5432,
        "database": "agent_memory",
        "user": "postgres",
        "password": "password"
    }
)
memory = PersistentBufferMemory(db=db, agent_id="agent_001")
```

## Advanced Operations

### Manual Persist

```python
# Add messages without auto-persist
memory = PersistentBufferMemory(
    db=db,
    agent_id="agent_001",
    auto_persist_interval=None
)

memory.add_message(role="user", content="Question 1")
memory.add_message(role="assistant", content="Answer 1")
memory.add_message(role="user", content="Question 2")

# Manually persist when ready
memory.persist()
```

### Clear Buffer (Keep Database)

```python
# Clear in-memory buffer, keep database
memory.clear_buffer()

# Buffer is empty, but database still has history
history = memory.get_history()  # Returns []

# Reload from database
memory.load_from_db()
history = memory.get_history()  # Returns all messages
```

### Delete Agent History

```python
# Delete all messages for agent from database
memory.delete_history()

# Buffer and database are now empty
history = memory.get_history()  # Returns []
```

## Performance Characteristics

**Benchmarks** (10,000 entries per agent):
- **Retrieval Latency (p95)**: <1ms (in-memory buffer)
- **Persist Latency (p95)**: <100ms (with compression)
- **Storage Efficiency**: 60%+ reduction with compression
- **Multi-Instance**: Support for 1,000+ agents simultaneously

**Capacity**:
- SQLite: 10,000+ messages per agent, unlimited agents
- PostgreSQL: Millions of messages (production scale)

## Use Cases

### Long-Running Conversational Agents

```python
# Customer support agent with conversation history
agent = ConversationalAgent(config, db)

# Day 1
agent.ask("How do I reset my password?")
agent.ask("Thanks!")

# Day 2 (new session)
agent = ConversationalAgent(config, db)  # Loads history
agent.ask("I forgot the steps you mentioned")  # Remembers previous conversation
```

### Multi-Turn Reasoning

```python
# Agent maintains context across multiple questions
agent.ask("What is the capital of France?")
agent.ask("What's its population?")  # "its" refers to Paris from previous question
agent.ask("What's the weather like there?")  # "there" refers to Paris
```

### Session Resumption After Failures

```python
# Agent crashes mid-conversation
agent.ask("Question 1")
agent.ask("Question 2")
# CRASH

# Restart - conversation preserved
agent_new = ConversationalAgent(config, db)
agent_new.ask("What did we discuss?")  # Remembers questions 1 and 2
```

## When to Use

Use persistent buffer memory when:
- **Conversational Agents**: Need to remember past interactions
- **Stateful Workflows**: Agent behavior depends on history
- **Cross-Session Persistence**: Conversation survives restarts
- **Long-Running Sessions**: 30+ hour conversations with context
- **Multi-Turn Reasoning**: Questions depend on previous answers

## Common Patterns

### Pattern 1: Context-Aware Agent

```python
class ContextAwareAgent(BaseAgent):
    def __init__(self, config, db):
        super().__init__(config=config, signature=MySignature())
        self.memory = PersistentBufferMemory(
            db=db,
            agent_id=self.agent_id,
            buffer_size=50,
            auto_persist_interval=5
        )
        self.memory.load_from_db()

    def process(self, input_data: str) -> dict:
        # Get context from previous interactions
        context = self.memory.get_history(limit=10)

        # Process with context
        result = self.run(input=input_data, context=context)

        # Store interaction
        self.memory.add_message(role="user", content=input_data)
        self.memory.add_message(role="assistant", content=result["output"])

        return result
```

### Pattern 2: Multi-Agent Shared History

```python
# Supervisor and workers share conversation history
db = DataFlow(database_type="sqlite", database_config={"database": "./shared.db"})

# All agents use same agent_id for shared history
shared_id = "team_001"

supervisor = SupervisorAgent(config, db, agent_id=shared_id)
worker1 = WorkerAgent(config, db, agent_id=shared_id)
worker2 = WorkerAgent(config, db, agent_id=shared_id)

# All agents see the same conversation history
```

## References

- **Implementation**: `src/kaizen/memory/persistent_buffer.py`
- **Tests**: `tests/integration/memory/test_persistent_buffer_dataflow.py` (28 E2E tests)
- **DataFlow Guide**: `sdk-users/apps/dataflow/README.md`
- **Memory Patterns**: `docs/reference/memory-patterns-guide.md`

## Related Skills

- **[kaizen-memory-system](kaizen-memory-system.md)** - Complete memory system overview
- **[kaizen-checkpoint-resume](kaizen-checkpoint-resume.md)** - Checkpoint and resume
- **[02-dataflow](../../02-dataflow/SKILL.md)** - DataFlow framework
