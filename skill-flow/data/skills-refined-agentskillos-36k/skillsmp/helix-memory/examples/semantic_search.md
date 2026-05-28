# Example: Semantic Search and Discovery

## Scenario
User asks: "What were my Python testing preferences?"

Claude doesn't remember from current session, but it's stored in memory.

## Semantic Search Workflow

### 1. Generate Query Embedding
```python
# Pseudo-code - Claude's internal understanding
query = "Python testing preferences"
query_embedding = generate_embedding(query)
# Returns: [0.34, 0.12, 0.78, ..., 0.56]
```

### 2. Search Similar Memories
```bash
curl -X POST http://localhost:6969/query/SearchMemoriesBySimilarity \
  -H "Content-Type: application/json" \
  -d '{
    "query_vector": [0.34, 0.12, 0.78, ..., 0.56],
    "k": 5
  }'
```

### 3. Results Ranked by Similarity
```json
[
  {
    "id": "mem_016",
    "content": "User prefers PHPUnit for WordPress plugin testing",
    "category": "preference",
    "importance": 9,
    "tags": "wordpress,testing,phpunit",
    "similarity": 0.89
  },
  {
    "id": "mem_025",
    "content": "User prefers pytest over unittest for Python",
    "category": "preference",
    "importance": 8,
    "tags": "python,testing,pytest",
    "similarity": 0.92  // Highest similarity!
  },
  {
    "id": "mem_031",
    "content": "Always use coverage.py for test coverage",
    "category": "preference",
    "importance": 7,
    "tags": "python,testing,coverage",
    "similarity": 0.85
  },
  {
    "id": "mem_042",
    "content": "Prefer TDD approach for new features",
    "category": "preference",
    "importance": 6,
    "tags": "testing,methodology,tdd",
    "similarity": 0.73
  },
  {
    "id": "mem_019",
    "content": "Python 3.11+ required for project",
    "category": "fact",
    "importance": 7,
    "tags": "python,version",
    "similarity": 0.68
  }
]
```

### 4. Filter and Rank
Claude applies additional filtering:
- **Primary match:** mem_025 (pytest, highest similarity, Python-specific)
- **Related:** mem_031 (coverage.py, also Python testing)
- **General:** mem_042 (TDD, testing methodology)
- **Less relevant:** mem_016 (WordPress, different context)
- **Tangential:** mem_019 (Python, but not testing-specific)

### 5. Follow Relationships
Get related memories to primary match:
```bash
curl -X POST http://localhost:6969/query/GetRelatedMemories \
  -H "Content-Type: application/json" \
  -d '{"memory_id": "mem_025"}'
```

Response:
```json
[
  {
    "id": "mem_031",
    "content": "Always use coverage.py for test coverage",
    "relationship": "related"
  },
  {
    "id": "mem_048",
    "content": "Use pytest-mock for mocking in tests",
    "relationship": "related"
  }
]
```

### 6. Claude's Response
Based on semantic search and graph traversal:

> "For Python testing, you prefer:
> - pytest over unittest (importance: 8)
> - coverage.py for test coverage (importance: 7)
> - pytest-mock for mocking
> - TDD approach for new features (importance: 6)"

## Why Semantic Search?

### Handles Synonyms
Query: "Python unit testing tools"
Finds: "pytest over unittest" (even though exact words don't match)

### Cross-Domain Discovery
Query: "testing frameworks"
Finds:
- pytest (Python)
- PHPUnit (WordPress/PHP)
- Jest (mentioned in old JavaScript project)

### Contextual Understanding
Query: "code quality tools"
Finds:
- pytest (testing)
- coverage.py (coverage)
- ruff (linting - if stored)
- mypy (type checking - if stored)

All related to code quality even with different terminology.

## Advanced Patterns

### Multi-Step Discovery

**Step 1:** Search for "frontend preferences"
```
Results: React, Tailwind CSS, TypeScript
```

**Step 2:** Get related memories for top result (React)
```
Related: Component patterns, state management (Redux), testing (Jest)
```

**Step 3:** Follow project context
```
Context: ecommerce-frontend
Other memories: API endpoints, authentication flow, deployment
```

**Result:** Complete picture of frontend preferences + project specifics

### Temporal Context

Search: "recent decisions about database"

Results sorted by:
1. Similarity to "database decisions"
2. Filtered by category="decision"
3. Ranked by timestamp (recent first)

Finds:
- "Chose HelixDB for memory storage" (today)
- "Using PostgreSQL for main app data" (last week)
- "Migrated from MySQL to PostgreSQL" (last month)

### Importance Weighting

Search results can be weighted by:
```python
score = (similarity * 0.7) + (importance / 10 * 0.3)
```

High-importance memories rank higher even with slightly lower similarity.

## Handling Ambiguity

### Query: "testing setup"

Could mean:
- Testing preferences/tools
- Test environment setup
- Testing methodology

Semantic search returns all relevant:
```json
[
  {"content": "pytest for Python", "similarity": 0.85, "category": "preference"},
  {"content": "Use Docker for test environments", "similarity": 0.82, "category": "context"},
  {"content": "TDD approach", "similarity": 0.79, "category": "preference"},
  {"content": "CI/CD with GitHub Actions", "similarity": 0.76, "category": "decision"}
]
```

Claude interprets based on conversation context or asks for clarification.

## Optimization Tips

### Limit Results Appropriately
```bash
# Quick check
k=3

# Standard search
k=5

# Comprehensive search
k=10

# Avoid
k=100  # Too many, lose relevance
```

### Use Importance Thresholds
Filter results:
```python
results = [m for m in search_results if m['importance'] >= 7]
```

Only high-importance matches for critical decisions.

### Combine with Graph Traversal
```
1. Semantic search (find entry points)
2. Graph traversal (expand context)
3. Context filtering (project-specific)
4. Importance ranking (prioritize)
```

### Cache Embeddings
Don't regenerate embeddings for common queries:
- "user preferences"
- "current project"
- "recent decisions"

Store query embeddings for reuse.

## Future Enhancements

- **Hybrid search:** Combine semantic + keyword + graph
- **Personalized ranking:** Learn which memories are most useful
- **Auto-linking:** Suggest relationships based on similarity
- **Decay function:** Reduce importance of old memories over time
- **Context-aware search:** Weight results based on current conversation topic
