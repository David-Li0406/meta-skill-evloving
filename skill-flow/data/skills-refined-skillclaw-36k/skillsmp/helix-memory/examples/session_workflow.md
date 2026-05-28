# Example: Complete Session Workflow

## Scenario
User starts a new session working on a WordPress plugin they've worked on before.

## Session Start

### 1. Check DB Status
```bash
bash scripts/status.sh
```

Output:
```
=== HelixDB Memory Status ===
✓ HelixDB CLI: Helix CLI 2.1.2
Instance Status: dev (running)
✓ Database accessible at http://localhost:6969
```

### 2. Get Available Contexts
```bash
curl -X POST http://localhost:6969/query/GetAllContexts \
  -H "Content-Type: application/json"
```

Response:
```json
[
  {
    "id": "ctx_user_global",
    "name": "user-preferences",
    "type": "user",
    "description": "Global user preferences and settings"
  },
  {
    "id": "ctx_wp_plugin",
    "name": "wordpress-plugin-dev",
    "type": "project",
    "description": "WordPress plugin development work"
  }
]
```

### 3. Load User Preferences
```bash
curl -X POST http://localhost:6969/query/GetMemoriesInContext \
  -H "Content-Type: application/json" \
  -d '{"context_id": "ctx_user_global"}'
```

Response:
```json
[
  {
    "id": "mem_001",
    "content": "User prefers extremely concise responses",
    "category": "preference",
    "importance": 10,
    "tags": "communication,style"
  },
  {
    "id": "mem_003",
    "content": "Always use git-workflow skill for commits",
    "category": "preference",
    "importance": 9,
    "tags": "git,workflow"
  }
]
```

**Claude applies these preferences immediately**

### 4. Load Project Context
```bash
curl -X POST http://localhost:6969/query/GetMemoriesInContext \
  -H "Content-Type: application/json" \
  -d '{"context_id": "ctx_wp_plugin"}'
```

Response:
```json
[
  {
    "id": "mem_005",
    "content": "Plugin uses custom post types for event management",
    "category": "context",
    "importance": 7,
    "tags": "wordpress,architecture,cpt"
  },
  {
    "id": "mem_006",
    "content": "User prefers Pico.css over custom CSS",
    "category": "preference",
    "importance": 8,
    "tags": "wordpress,css,styling"
  },
  {
    "id": "mem_007",
    "content": "Last session: working on event calendar view",
    "category": "task",
    "importance": 6,
    "tags": "wordpress,wip,calendar"
  }
]
```

**Claude now has full project context**

### 5. Semantic Search for Related Info
User says: "Let's continue with the calendar"

Generate embedding for "calendar event view wordpress" and search:
```bash
curl -X POST http://localhost:6969/query/SearchMemoriesBySimilarity \
  -H "Content-Type: application/json" \
  -d '{
    "query_vector": [0.23, 0.67, ..., 0.45],
    "k": 5
  }'
```

Response includes:
- mem_007 (calendar view task)
- mem_005 (custom post types)
- mem_012 (calendar styling decision)

## During Session

### User Makes Decision
User: "Let's use FullCalendar library for the calendar view"

**Claude stores this:**
```bash
python scripts/memory_helper.py store \
  --content "Decided to use FullCalendar library for event calendar view" \
  --category "decision" \
  --importance 8 \
  --tags "wordpress,calendar,library,fullcalendar"
```

Returns `mem_015`

**Link to project:**
```bash
curl -X POST http://localhost:6969/query/LinkMemoryToContext \
  -H "Content-Type: application/json" \
  -d '{
    "memory_id": "mem_015",
    "context_id": "ctx_wp_plugin"
  }'
```

**Link to related memory:**
```bash
curl -X POST http://localhost:6969/query/LinkRelatedMemories \
  -H "Content-Type: application/json" \
  -d '{
    "from_id": "mem_015",
    "to_id": "mem_007"
  }'
```

### User Shares Preference
User: "I prefer PHPUnit for WordPress plugin testing"

**Claude stores:**
```bash
python scripts/memory_helper.py store \
  --content "User prefers PHPUnit for WordPress plugin testing" \
  --category "preference" \
  --importance 9 \
  --tags "wordpress,testing,phpunit"
```

**Link to both contexts:**
```bash
# Global preference
curl -X POST http://localhost:6969/query/LinkMemoryToContext \
  -d '{"memory_id": "mem_016", "context_id": "ctx_user_global"}'

# Also project-specific
curl -X POST http://localhost:6969/query/LinkMemoryToContext \
  -d '{"memory_id": "mem_016", "context_id": "ctx_wp_plugin"}'
```

## Session End

### Update Task Status
```bash
python scripts/memory_helper.py store \
  --content "Calendar view implemented with FullCalendar, next: add event filters" \
  --category "task" \
  --importance 7 \
  --tags "wordpress,wip,calendar,next"
```

### Store Session Summary
```bash
python scripts/memory_helper.py store \
  --content "Session 2024-11-17: Implemented calendar view, decided on FullCalendar library" \
  --category "context" \
  --importance 6 \
  --tags "wordpress,session,calendar,completed"
```

## Next Session Start

When user returns later, Claude:

1. **Loads user preferences** (mem_001, mem_003, mem_016)
2. **Detects WordPress context** from user's first message
3. **Loads project memories** via GetMemoriesInContext
4. **Finds WIP task** (mem_017: "next: add event filters")
5. **Recalls FullCalendar decision** (mem_015)
6. **Continues seamlessly** without user re-explaining context

## Memory Graph After Session

```
ctx_user_global
├── mem_001 (Concise responses)
├── mem_003 (git-workflow)
└── mem_016 (PHPUnit testing)
      └── RelatesTo → mem_017 (Testing context)

ctx_wp_plugin
├── mem_005 (Custom post types)
├── mem_006 (Pico.css)
├── mem_007 (Calendar task)
│     ├── RelatesTo → mem_015 (FullCalendar decision)
│     └── RelatesTo → mem_017 (Current WIP)
├── mem_015 (FullCalendar decision)
├── mem_016 (PHPUnit testing)
└── mem_017 (Current task: filters)
```

## Benefits Demonstrated

- ✅ No re-explaining preferences
- ✅ Automatic project context loading
- ✅ Decision history preserved
- ✅ Task continuity across sessions
- ✅ Related information discoverable
- ✅ Semantic search finds relevant memories
