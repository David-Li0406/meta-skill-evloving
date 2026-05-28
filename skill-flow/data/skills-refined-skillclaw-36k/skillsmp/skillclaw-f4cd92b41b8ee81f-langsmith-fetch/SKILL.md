---
name: langsmith-fetch
description: Use this skill when debugging LangChain and LangGraph agents by fetching execution traces from LangSmith Studio to analyze performance, investigate errors, and check tool calls.
---

# Skill body

## Prerequisites

### 1. Install langsmith-fetch
```bash
pip install langsmith-fetch
```

### 2. Set Environment Variables
```bash
export LANGSMITH_API_KEY="your_langsmith_api_key"
export LANGSMITH_PROJECT="your_project_name"
```

**Verify setup:**
```bash
echo $LANGSMITH_API_KEY
echo $LANGSMITH_PROJECT
```

## When to Use This Skill

Automatically activate when user mentions:
- 🐛 "Debug my agent" or "What went wrong?"
- 🔍 "Show me recent traces" or "What happened?"
- ❌ "Check for errors" or "Why did it fail?"
- 💾 "Analyze memory operations" or "Check LTM"
- 📊 "Review agent performance" or "Check token usage"
- 🔧 "What tools were called?" or "Show execution flow"

## Core Workflows

### Workflow 1: Quick Debug Recent Activity

**When user asks:** "What just happened?" or "Debug my agent"

**Execute:**
```bash
langsmith-fetch traces --last-n-minutes 5 --limit 5 --format pretty
```

**Analyze and report:**
1. ✅ Number of traces found
2. ⚠️ Any errors or failures
3. 🛠️ Tools that were called
4. ⏱️ Execution times
5. 💰 Token usage

**Example response format:**
```
Found 3 traces in the last 5 minutes:

Trace 1: ✅ Success
- Agent: memento
- Tools: recall_memories, create_entities
- Duration: 2.3s
- Tokens: 1,245

Trace 2: ❌ Error
- Agent: cypher
- Error: "Neo4j connection timeout"
- Duration: 15.1s
- Failed at: search_nodes tool

Trace 3: ✅ Success
- Agent: memento
- Tools: store_memory
- Duration: 1.8s
- Tokens: 892

💡 Issue found: Trace 2 failed due to Neo4j timeout. Recommend checking database connection.
```

### Workflow 2: Deep Dive Specific Trace

**When user provides:** Trace ID or says "investigate that error"

**Execute:**
```bash
langsmith-fetch trace <trace-id> --format json
```

**Analyze JSON and report:**
1. 🎯 What the agent was trying to do
2. 🛠️ Which tools were called (in order)
3. ✅ Tool results (success/failure)
4. ❌ Error messages (if any)
5. 💡 Root cause analysis
6. 🔧 Suggested fix