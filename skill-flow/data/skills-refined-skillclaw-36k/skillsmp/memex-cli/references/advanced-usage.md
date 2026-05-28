# memex-cli Advanced Usage Guide

This document covers advanced features including multi-task execution, DAG dependencies, resume functionality, and file handling.

## Multi-Task Execution

memex-cli supports executing multiple tasks in a single run using two modes:
1. **Parallel Execution** - Tasks run concurrently
2. **DAG Execution** - Tasks run with dependency ordering

### Parallel Execution

Tasks without dependencies execute in parallel by default, maximizing throughput.

**Syntax:**

```bash
memex-cli run --stdin <<'EOF'
---TASK---
id: task-1
backend: codex
workdir: /path/to/project
---CONTENT---
First task prompt
---END---

---TASK---
id: task-2
backend: codex
workdir: /path/to/project
---CONTENT---
Second task prompt
---END---

---TASK---
id: task-3
backend: gemini
workdir: /path/to/project
---CONTENT---
Third task prompt
---END---
EOF
```

**Characteristics:**
- Tasks execute simultaneously
- Each task has independent backend/model configuration
- Total execution time ≈ slowest task duration
- Speedup factor shown in output (e.g., "并行加速 2.6x")

**Use Cases:**
- Independent code generation tasks
- Parallel design explorations
- Batch processing unrelated prompts

**Example Output:**

```
▶ 并行执行 3 个任务...

  ▶ task-1 (codex)
  ▶ task-2 (codex)
  ▶ task-3 (gemini)

  ✓ task-1 2.1s
  ✓ task-2 2.5s
  ✓ task-3 2.8s

───────────────────────────
✓ 完成 3/3 任务 (2.8s, 并行加速 2.6x)
```

### DAG (Directed Acyclic Graph) Execution

Tasks can declare dependencies using the `dependencies:` parameter, creating an execution graph.

**Syntax:**

```bash
memex-cli run --stdin <<'EOF'
---TASK---
id: design
backend: gemini
workdir: /home/user/myapp
---CONTENT---
设计 API 接口
---END---

---TASK---
id: implement
backend: codex
workdir: /home/user/myapp
model: gpt-5.2
dependencies: design
---CONTENT---
实现 API（基于设计阶段的输出）
---END---

---TASK---
id: test
backend: codex
workdir: /home/user/myapp
dependencies: implement
---CONTENT---
编写测试用例（基于实现代码）
---END---
EOF
```

**Dependency Specification:**
- Single dependency: `dependencies: task-a`
- Multiple dependencies: `dependencies: task-a,task-b,task-c`
- Dependencies must be valid task IDs in the same run

**Execution Order:**
1. memex-cli builds dependency graph
2. Tasks execute when all dependencies complete
3. Dependent tasks can access previous task outputs
4. Circular dependencies are rejected

**Example Output:**

```
▶ design (gemini)

设计 REST API...

✓ design 4.2s

▶ implement (codex/gpt-5.2) ← design

实现代码...

» 写入 main.py
✓ implement 6.8s

▶ test (codex) ← implement

编写测试...

» 写入 test_main.py
✓ test 3.1s

───────────────────────────
✓ 完成 3/3 任务 (14.1s)
```

Note the `← design` notation indicating dependency.

### Mixed Parallel and DAG

Complex workflows can combine parallel and sequential execution:

```bash
memex-cli run --stdin <<'EOF'
# Phase 1: Parallel design exploration
---TASK---
id: design-api
backend: gemini
workdir: /project
---CONTENT---
设计 REST API
---END---

---TASK---
id: design-ui
backend: gemini
workdir: /project
---CONTENT---
设计前端界面
---END---

# Phase 2: Implementation (depends on both designs)
---TASK---
id: implement
backend: codex
workdir: /project
dependencies: design-api,design-ui
---CONTENT---
实现完整应用
---END---
EOF
```

**Execution Flow:**
1. `design-api` and `design-ui` run in parallel
2. `implement` waits for both to complete
3. `implement` starts after both designs finish

## Resume Functionality

Resume allows continuing execution from a previous run, preserving context and memory.

### Basic Resume

**Obtain run_id from previous execution:**

```
▶ code-gen-20260109100000 (codex/gpt-5.2)

实现代码...

✓ code-gen-20260109100000 3.5s

Run ID: abc123-def456-789
```

**Resume with new task:**

```bash
memex-cli resume --run-id abc123-def456-789 --stdin <<'EOF'
---TASK---
id: continue-task
backend: codex
workdir: /home/user/project
---CONTENT---
基于之前的实现，添加错误处理
---END---
EOF
```

**Context Preservation:**
- Previous task outputs available to resumed task
- Backend maintains conversation history
- File modifications from previous run are visible

### Resume Use Cases

**1. Iterative Development**

```bash
# Initial implementation
memex-cli run --stdin <<'EOF'
---TASK---
id: initial
backend: codex
workdir: /project
---CONTENT---
实现用户认证
---END---
EOF
# Outputs: Run ID: run-001

# Add feature
memex-cli resume --run-id run-001 --stdin <<'EOF'
---TASK---
id: add-feature
backend: codex
workdir: /project
---CONTENT---
添加密码重置功能
---END---
EOF
# Outputs: Run ID: run-002

# Bug fix
memex-cli resume --run-id run-002 --stdin <<'EOF'
---TASK---
id: bugfix
backend: codex
workdir: /project
---CONTENT---
修复登录验证bug
---END---
EOF
```

**2. Long-Running Workflows**

Resume allows splitting long workflows across multiple sessions:

```bash
# Day 1: Design
memex-cli run --stdin <<'EOF'
---TASK---
id: design
backend: gemini
workdir: /project
---CONTENT---
设计系统架构
---END---
EOF
# Save Run ID: day1-run

# Day 2: Implementation
memex-cli resume --run-id day1-run --stdin <<'EOF'
---TASK---
id: implement
backend: codex
workdir: /project
---CONTENT---
基于昨天的设计实现代码
---END---
EOF
```

**3. Error Recovery**

If a task fails, resume from the same run to retry or adjust:

```bash
# Original run fails
memex-cli run --stdin <<'EOF'
---TASK---
id: complex-task
backend: codex
workdir: /project
---CONTENT---
实现复杂功能（可能失败）
---END---
EOF
# Fails with Run ID: failed-run

# Resume with adjusted prompt
memex-cli resume --run-id failed-run --stdin <<'EOF'
---TASK---
id: retry-task
backend: codex
workdir: /project
---CONTENT---
用更简单的方法实现该功能
---END---
EOF
```

### Resume Limitations

- Run ID must exist in memex-cli's run history
- Context size limits may apply for very long runs
- Backend-specific resume behavior may vary

## File Handling

The `files:` parameter enables loading file context into tasks.

### Basic File Loading

**Single file:**

```bash
---TASK---
id: review
backend: claude
workdir: /project
files: ./design.md
---CONTENT---
审查这个设计文档
---END---
```

**Multiple files:**

```bash
---TASK---
id: refactor
backend: codex
workdir: /project
files: src/main.py,src/utils.py,tests/test_main.py
---CONTENT---
重构这些文件
---END---
```

**Glob patterns:**

```bash
---TASK---
id: analyze
backend: claude
workdir: /project
files: src/**/*.py
---CONTENT---
分析所有 Python 源代码
---END---
```

### File Modes

**`files-mode:` parameter controls how files are handled:**

**1. `embed` (default) - Inline content**

Files are embedded directly in the task context:

```bash
---TASK---
id: review-code
backend: claude
workdir: /project
files: src/main.py
files-mode: embed
---CONTENT---
审查代码质量
---END---
```

**Characteristics:**
- Full file content sent to backend
- Best for small files (<100 KB)
- Higher token usage

**2. `ref` - Reference only**

Files are referenced by path, backend loads on demand:

```bash
---TASK---
id: process-large
backend: codex
workdir: /project
files: data/*.json
files-mode: ref
---CONTENT---
处理这些 JSON 文件
---END---
```

**Characteristics:**
- Only file paths sent initially
- Backend loads files as needed
- Better for large files or many files

**3. `auto` - Automatic selection**

memex-cli decides based on file size:

```bash
---TASK---
id: smart-load
backend: gemini
workdir: /project
files: ./
files-mode: auto
---CONTENT---
分析项目结构
---END---
```

**Auto mode rules:**
- Files < 50 KB: embed
- Files ≥ 50 KB: ref
- Binary files: always ref

### File Encoding

**`files-encoding:` parameter controls encoding:**

**1. `utf-8` (default) - Text files**

```bash
files: config.json
files-encoding: utf-8
```

**2. `base64` - Binary files**

For images, PDFs, etc.:

```bash
---TASK---
id: review-ui
backend: gemini
workdir: /project
files: mockups/*.png
files-encoding: base64
---CONTENT---
审查这些 UI 设计稿
---END---
```

**3. `auto` - Detect automatically**

memex-cli detects file type:

```bash
files: **/*
files-encoding: auto
```

**Detection rules:**
- Text file extensions (.md, .py, .js, etc.): utf-8
- Binary extensions (.png, .jpg, .pdf, etc.): base64
- Unknown: attempt utf-8, fallback to base64

### File Loading Output

When files are loaded, output shows:

```
▶ review-task (claude)

📄 加载 design.md (2.3 KB)
📄 加载 implementation.md (5.1 KB)

审查文档...

✓ review-task 4.2s
```

## Advanced Parameter Configuration

### Timeout and Retry

**timeout:** Maximum execution time in seconds

```bash
---TASK---
id: long-task
backend: codex
workdir: /project
timeout: 600
---CONTENT---
耗时操作（最多10分钟）
---END---
```

**retry:** Number of retry attempts on failure

```bash
---TASK---
id: unstable-task
backend: codex
workdir: /project
retry: 2
---CONTENT---
可能不稳定的任务（失败后重试2次）
---END---
```

**Combined:**

```bash
---TASK---
id: robust-task
backend: codex
workdir: /project
timeout: 300
retry: 3
---CONTENT---
重要任务（5分钟超时，最多3次重试）
---END---
```

### Model Selection

**Codex backend - specify model:**

```bash
---TASK---
id: code-gen
backend: codex
workdir: /project
model: gpt-5.2
model-provider: openai
---CONTENT---
生成代码
---END---
```

**Available models (codex):**
- `gpt-5.2` - Latest general model
- `gpt-5.1-codex-max` - Optimized for code generation
- `gpt-5.0-mini` - Faster, smaller model

**Claude backend - model auto-selected:**

```bash
---TASK---
id: design
backend: claude
workdir: /project
# No model parameter needed
---CONTENT---
设计架构
---END---
```

**Gemini backend - model auto-selected:**

```bash
---TASK---
id: vision-task
backend: gemini
workdir: /project
# Gemini automatically selects best model for multimodal tasks
---CONTENT---
分析图像
---END---
```

## Best Practices

### Task ID Design

**Use descriptive, hierarchical IDs:**

Good:
```
auth.design
auth.implement
auth.test
```

Bad:
```
task1
task2
task3
```

**Include timestamps for unique runs:**

```
implement-20260109143052
```

### Dependency Management

**Keep DAG shallow:**

Good (2-3 levels):
```
design → implement → test
```

Bad (too deep):
```
a → b → c → d → e → f → g
```

**Parallelize when possible:**

```
design-api ──┐
              ├→ integrate → test
design-ui  ──┘
```

### File Loading Optimization

**Use glob patterns efficiently:**

Good:
```
files: src/**/*.py
```

Bad:
```
files: src/a.py,src/b.py,src/c.py,...
```

**Choose appropriate mode:**

- Small configs: `files-mode: embed`
- Large datasets: `files-mode: ref`
- Mixed sizes: `files-mode: auto`

### Resume Strategy

**Save run IDs systematically:**

```bash
RUN_ID=$(memex-cli run --stdin < task.md | grep "Run ID:" | awk '{print $3}')
echo $RUN_ID > .memex-run-id
```

**Resume from saved ID:**

```bash
memex-cli resume --run-id $(cat .memex-run-id) --stdin < continue.md
```

## Troubleshooting

### Circular Dependencies

**Error:**
```
Error: Circular dependency detected: task-a → task-b → task-a
```

**Solution:** Restructure dependencies to form DAG (no cycles)

### File Not Found

**Error:**
```
⚠ File not found: src/missing.py
```

**Solution:** Verify file paths are relative to `workdir:`

### Context Size Exceeded

**Error:**
```
Error: Context size limit exceeded (files too large)
```

**Solution:**
- Use `files-mode: ref` instead of `embed`
- Load fewer files
- Use glob patterns more selectively

### Resume Run Not Found

**Error:**
```
Error: Run ID not found: invalid-run-id
```

**Solution:**
- Verify run ID is correct
- Check run ID exists in memex-cli history
- Run IDs may expire after retention period

## Summary

Advanced memex-cli features enable:
- **Parallel execution** for independent tasks (speedup)
- **DAG dependencies** for sequential workflows (ordering)
- **Resume** for iterative development (continuity)
- **File loading** for context-aware tasks (glob, modes, encoding)
- **Flexible configuration** for timeout, retry, model selection

Combine these features to build sophisticated AI-powered development workflows.
