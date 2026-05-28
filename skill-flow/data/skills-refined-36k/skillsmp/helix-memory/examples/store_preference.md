# Example: Storing User Preferences

## Scenario
User says: "I prefer concise responses. Sacrifice grammar if needed to be brief."

## Detection
Claude recognizes this as an important preference that should persist across sessions.

## Storage Workflow

### Step 1: Analyze the Information
- **Type:** User preference (high importance)
- **Category:** "preference"
- **Importance:** 10 (affects all interactions)
- **Tags:** "communication", "style", "conciseness"

### Step 2: Store Memory
```bash
python scripts/memory_helper.py store \
  --content "User prefers extremely concise responses, sacrifice grammar if needed" \
  --category "preference" \
  --importance 10 \
  --tags "communication,style,conciseness"
```

Or via API:
```bash
curl -X POST http://localhost:6969/query/StoreMemory \
  -H "Content-Type: application/json" \
  -d '{
    "content": "User prefers extremely concise responses, sacrifice grammar if needed",
    "category": "preference",
    "importance": 10,
    "tags": "communication,style,conciseness"
  }'
```

**Result:** Memory node created with ID (e.g., `mem_001`)

### Step 3: Generate Embedding
```python
# Pseudo-code - embedding generation
embedding = generate_embedding("User prefers extremely concise responses, sacrifice grammar if needed")
# Returns vector like [0.12, 0.45, ..., 0.89]
```

### Step 4: Store Embedding
```bash
curl -X POST http://localhost:6969/query/StoreMemoryEmbedding \
  -H "Content-Type: application/json" \
  -d '{
    "memory_id": "mem_001",
    "vector": [0.12, 0.45, ..., 0.89],
    "content": "User prefers extremely concise responses, sacrifice grammar if needed"
  }'
```

### Step 5: Link to User Context
```bash
curl -X POST http://localhost:6969/query/LinkMemoryToContext \
  -H "Content-Type: application/json" \
  -d '{
    "memory_id": "mem_001",
    "context_id": "ctx_user_global"
  }'
```

## Retrieval in Next Session

### Session Start
```bash
# Search for communication preferences
curl -X POST http://localhost:6969/query/SearchMemoriesBySimilarity \
  -H "Content-Type: application/json" \
  -d '{
    "query_vector": [embedding of "communication style"],
    "k": 5
  }'
```

**Result:** Finds "User prefers extremely concise responses..." as top result

### Application
Claude applies this preference to all responses in the session.

## Related Preferences
If user later says: "Always list questions at end if any"

Link the memories:
```bash
curl -X POST http://localhost:6969/query/LinkRelatedMemories \
  -H "Content-Type: application/json" \
  -d '{
    "from_id": "mem_001",
    "to_id": "mem_002"
  }'
```

Now retrieving communication preferences will also surface related preferences via graph traversal.

## Complete Graph Structure
```
Context: ctx_user_global
   ↑
   | (BelongsTo)
   |
Memory: mem_001 (Concise responses)
   |
   ├─ (HasEmbedding) → MemoryEmbedding: emb_001
   |
   └─ (RelatesTo) → Memory: mem_002 (List questions)
         |
         └─ (HasEmbedding) → MemoryEmbedding: emb_002
```
