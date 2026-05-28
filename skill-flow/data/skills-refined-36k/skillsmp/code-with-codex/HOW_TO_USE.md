# How to Use code-with-codex Skill

This guide explains when and how to use the `code-with-codex` skill for code generation tasks using memex-cli with OpenAI Codex backend.

---

## When to Use This Skill

Use `code-with-codex` when you need to:

1. **Generate code files and scripts**
   - Python, JavaScript, Go, Rust, etc.
   - Command-line utilities
   - Data processing scripts

2. **Refactor existing code**
   - Apply design patterns
   - Extract common logic
   - Improve code quality and testability

3. **Write tests**
   - Unit tests (pytest, jest, go test)
   - Integration tests
   - Test coverage >80%

4. **Create project scaffolds**
   - Boilerplate code generation
   - Project structure setup
   - Configuration files

5. **Implement algorithms or features**
   - Data structures (trees, graphs, heaps)
   - Algorithms (sorting, searching, pathfinding)
   - API endpoints and services

6. **Code review and optimization**
   - Analyze existing code for issues
   - Identify performance bottlenecks
   - Security vulnerability detection

7. **Complex multi-file projects**
   - Microservices architecture
   - Full-stack applications
   - System design and implementation

---

## Relationship with memex-cli

`code-with-codex` is a **specialized skill** built on top of `memex-cli`:

```
┌─────────────────────────────────────┐
│     code-with-codex (Skill)         │
│  ┌───────────────────────────────┐  │
│  │   Code Generation Focus       │  │
│  │   Complexity-based guidance   │  │
│  │   Examples for 5 levels       │  │
│  └───────────────────────────────┘  │
└─────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────┐
│        memex-cli (Tool)             │
│  ┌───────────────────────────────┐  │
│  │   Backend orchestration       │  │
│  │   Multi-task DAG execution    │  │
│  │   Memory & resume support     │  │
│  │   Supports 3 backends:        │  │
│  │   - Codex                     │  │
│  │   - Claude                    │  │
│  │   - Gemini                    │  │
│  └───────────────────────────────┘  │
└─────────────────────────────────────┘
```

**Key Differences:**

| Feature | code-with-codex | memex-cli |
|---------|----------------|-----------|
| **Scope** | Code generation tasks | General AI task orchestration |
| **Backend** | Codex only | Codex, Claude, Gemini |
| **Focus** | Programming, algorithms, refactoring | Any AI task (design, research, coding) |
| **Guidance** | 5 complexity levels, model selection | Generic task execution |
| **Examples** | Code-specific (scripts, APIs, tests) | Multi-domain workflows |

**When to use memex-cli directly:**
- Multi-backend workflows (e.g., Claude for design, Codex for implementation)
- Non-coding tasks (UX design, content generation)
- Advanced DAG workflows with dependencies across different backends

**When to use code-with-codex:**
- Focus on code generation quality
- Need complexity-based model guidance
- Want code-specific examples and best practices

---

## Execution Strategy

| Level | Model | files-mode | Dependency Analysis | Task Decomposition | Execution |
|:-----:|-------|:----------:|:-------------------:|:------------------:|:---------:|
| **L1** | `gpt-5.1-codex-mini` | ref | ❌ | ❌ | **Serial** |
| **L2** | `gpt-5.1-codex-max` | ref | ✅ | ❌ | **Parallel** |
| **L3** | `gpt-5.2-codex` | ref | ✅ | ✅ | **Parallel** |
| **L4** | `gpt-5.2` | ref | ✅ | ✅ | **Parallel** |
| **L5** | `gpt-5.2` | ref | ✅ | ✅ | **Parallel** |

---

## Automated Capabilities

The skill provides automatic optimization based on task complexity:

| Capability | Description | Active Level |
|------------|-------------|:------------:|
| **Auto Model Selection** | Automatically select optimal model based on complexity | L1-L5 |
| **Auto Grading** | Evaluate task complexity via Decision Tree | L1-L5 |
| **Dependency Analysis** | Analyze task/file dependencies, build DAG | L2+ |
| **Task Decomposition** | Auto-split large tasks into subtasks | L3+ |
| **Parallel Execution** | Execute independent subtasks in parallel | L2+ |

**How it works:**
1. Analyze task description to determine complexity level
2. Auto-select appropriate model for the level
3. For L2+: Analyze dependencies between tasks/files
4. For L3+: Decompose large tasks into manageable subtasks
5. Execute with optimal parallelization strategy

---

## Quick Start Example

### Step 1: Install memex-cli

```bash
npm install -g memex-cli
```

### Step 2: Choose Complexity Level

Refer to the [complexity guide](references/complexity-guide.md) or use this quick table:

| Task | Level | Model | Example |
|------|-------|-------|---------|
| Batch rename files | 1 | codex-mini | [Level 1](examples/level1-simple-scripts.md) |
| Email validator | 2 | codex-max | [Level 2](examples/level2-utilities.md) |
| HTTP client module | 3 | gpt-5.2-codex | [Level 3](examples/level3-modules.md) |
| Skip list algorithm | 4 | gpt-5.2 | [Level 4](examples/level4-algorithms.md) |
| Auth microservice | 5 | gpt-5.2 | [Level 5](examples/level5-architecture.md) |

### Step 3: Run Generation Task

```bash
memex-cli run --backend codex --stdin <<'EOF'
---TASK---
id: my-task
backend: codex
workdir: /path/to/project
model: gpt-5.2-codex        # Choose based on complexity
timeout: 120                 # Optional
---CONTENT---
[Your task description in natural language]
---END---
EOF
```

**Example:**

```bash
memex-cli run --backend codex --stdin <<'EOF'
---TASK---
id: validators
backend: codex
workdir: ./utils
model: gpt-5.1-codex-max
---CONTENT---
编写邮箱、手机号、身份证号验证函数（Python）
---END---
EOF
```

---

## Model Selection Tips

### 1. Match Model to Task Complexity (Auto-Selected)

| Level | Model | Cost | Speed | Quality |
|:-----:|-------|------|-------|---------|
| L1 | codex-mini | $ | Fast | Good |
| L2 | codex-max | $$ | Medium | Better |
| L3 | gpt-5.2-codex | $$$ | Slower | Best balance |
| L4-5 | gpt-5.2 | $$$$ | Slowest | Highest quality |

**Note:** Model is automatically selected based on task complexity. Manual override is available via `model` field.

### 2. Model Performance by Task Type

**Fast models (codex-mini)**:
- ✅ Simple scripts and utilities
- ✅ Data processing and file operations
- ✅ Quick prototypes
- ❌ Complex algorithms
- ❌ System architecture

**Balanced models (codex-max, gpt-5.2-codex)**:
- ✅ Production-grade modules
- ✅ Code review and refactoring
- ✅ Comprehensive testing
- ⚠️ May need upgrade for complex algorithms

**Powerful models (gpt-5.2)**:
- ✅ Complex algorithms
- ✅ Microservices and architecture
- ✅ System design
- ⚠️ Higher cost for simple tasks

---

## Common Workflow References

For advanced workflows (multi-task, parallel execution, resume), refer to memex-cli documentation:

- **Multi-task workflows**: [memex-cli/references/advanced-usage.md](../memex-cli/references/advanced-usage.md)
- **Parallel execution**: [memex-cli/examples/parallel-tasks.md](../memex-cli/examples/parallel-tasks.md)
- **Resume interrupted runs**: [memex-cli/examples/resume-workflow.md](../memex-cli/examples/resume-workflow.md)

These features are part of memex-cli and work the same way across all backends (Codex, Claude, Gemini).

---

## Task Design Best Practices

### 1. Be Specific

**Bad**:
```
Write a web scraper
```

**Good**:
```
Python web scraper using requests + BeautifulSoup:
- Target: https://example.com/products
- Extract: product name, price, image URL
- Output: JSON file
- Include error handling and rate limiting
```

### 2. Include Context

**For code review/refactoring**, use `files` field:
```bash
---TASK---
id: review
backend: codex
model: gpt-5.2-codex
files: ./src/auth.py, ./src/user.py
files-mode: ref
---CONTENT---
Review for security issues and performance
---END---
```

### 3. Specify Standards

**Include in prompt**:
- Programming language and version
- Framework (FastAPI, React, Flask)
- Coding style (PEP 8, Google style guide)
- Testing framework (pytest, jest)

### 4. Break Down Large Tasks

**Instead of**:
```
Build a complete e-commerce backend
```

**Use multi-task DAG**:
```
Task 1: Design database schema
Task 2: Implement models (depends on Task 1)
Task 3: Implement API endpoints (depends on Task 2)
Task 4: Write tests (depends on Task 3)
```

---

## Field Reference

### Required Fields

| Field | Description | Example |
|-------|-------------|---------|
| `id` | Unique task identifier | `impl-auth`, `test-validators` |
| `backend` | Always `codex` for this skill | `codex` |
| `workdir` | Working directory path | `./src`, `/home/user/project` |

### Optional Fields

| Field | Default | Description |
|-------|---------|-------------|
| `model` | gpt-5.2-codex | Model name (see complexity guide) |
| `timeout` | 300 | Max execution time (seconds) |
| `dependencies` | - | Comma-separated task IDs |
| `files` | - | Source files to reference |
| `files-mode` | ref | `ref` (path only) - unified across all levels |
| `retry` | 0 | Retry count on failure |
| `stream-format` | jsonl | `jsonl` / `text` |

---

## Examples by Use Case

### Code Generation (Level 3)

```bash
memex-cli run --backend codex --stdin <<'EOF'
---TASK---
id: http-client
backend: codex
model: gpt-5.2-codex
workdir: ./lib
---CONTENT---
Python HTTP client with retry, timeout, interceptors
---END---
EOF
```

### Code Review (Level 3)

```bash
memex-cli run --backend codex --stdin <<'EOF'
---TASK---
id: review
backend: codex
model: gpt-5.2-codex
files: ./src/auth.py
files-mode: ref
workdir: ./project
---CONTENT---
Review for security issues, performance, best practices
---END---
EOF
```

### Refactoring (Level 4)

```bash
memex-cli run --backend codex --stdin <<'EOF'
---TASK---
id: refactor
backend: codex
model: gpt-5.2
files: ./legacy_code.py
files-mode: ref
workdir: ./project
---CONTENT---
Refactor: apply design patterns, extract common logic, improve testability
---END---
EOF
```

### Unit Testing (Level 3)

```bash
memex-cli run --backend codex --stdin <<'EOF'
---TASK---
id: tests
backend: codex
model: gpt-5.2-codex
files: ./calculator.py
files-mode: ref
workdir: ./project
---CONTENT---
Write pytest tests with >90% coverage, including edge cases
---END---
EOF
```

---

## Troubleshooting

### Issue: Generated code has bugs

**Solution**:
1. Upgrade to higher-tier model (codex → codex-max → gpt-5.2)
2. Add more context in prompt (framework version, requirements)
3. Request specific error handling in prompt

### Issue: Task timeout

**Solution**:
1. Increase `timeout` field (default 300s)
2. Break large tasks into smaller subtasks
3. Use parallel execution for independent modules

### Issue: Model not following instructions

**Solution**:
1. Be more specific in prompt (include examples)
2. Use higher-tier model for complex tasks
3. Check if task matches model capabilities

### Issue: Need multi-backend workflow

**Solution**:
Use memex-cli directly with multiple backends:
```bash
---TASK---
id: design
backend: claude    # Claude for design
...
---TASK---
id: implement
backend: codex     # Codex for implementation
dependencies: design
...
```

---

## Further Reading

- [SKILL.md](SKILL.md) - Main skill reference
- [references/complexity-guide.md](references/complexity-guide.md) - Detailed complexity guide
- [examples/](examples/) - Runnable examples for all levels
- [skills/memex-cli/SKILL.md](../memex-cli/SKILL.md) - Memex CLI full documentation

---

**Need help?** Check the examples directory for runnable code samples matching your use case.
