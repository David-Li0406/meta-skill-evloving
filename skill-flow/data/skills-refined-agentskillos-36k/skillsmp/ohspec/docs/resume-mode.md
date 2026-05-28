# Resume Mode Guide

## What is Resume Mode?

Resume mode allows using a **single subagent** to execute multiple phases consecutively by using the `resume` parameter to restore context, thereby avoiding repeated persona loading.

## Why Use Resume Mode?

**Problems with Traditional Mode**:
- Each phase starts a new subagent → repeated persona loading (~2,800 tokens × 4 phases = ~11,200 tokens)
- Cross-phase context passing relies on file system (findings.json, progress.json)
- High overhead for context switching between phases

**Advantages of Resume Mode**:
- Single subagent + resume → load persona only once (~2,800 tokens)
- Natural context continuity without frequent external file reads
- Saves ~7,400 tokens (11,200 - 2,800 - 1,000 resume overhead)

## Complexity-Based Usage

根据 `config.yaml` 中的复杂度配置选择执行模式：

| 复杂度 | 执行模式 | Subagent 数量 | 用户确认次数 |
|--------|----------|---------------|--------------|
| **SIMPLE** | 合并执行 (analyze+design+precheck) | 1 | 1 (最终审批) |
| **MEDIUM** | Resume 模式 (可选确认) | 1-2 | 2 (设计+审批) |
| **COMPLEX** | 独立 Subagent (每阶段确认) | 4 | 4 (每阶段) |

## SIMPLE Task: Merged Execution

SIMPLE 任务将 analyze、design、precheck 合并到单个 Subagent 执行：

```python
def execute_simple_task(requirement: str, rfc_dir: str, project_root: str):
    """SIMPLE 任务：单个 Subagent 执行所有阶段"""

    result = Task(
        subagent_type="Explore",
        description="SIMPLE task: merged analyze+design+precheck",
        model="haiku",
        prompt=f"""
## SIMPLE 任务：合并执行模式

你将连续执行以下阶段，无需中间用户确认：

### 强制工作目录
- 项目根目录: {project_root}
- RFC 目录: {rfc_dir}

### 阶段 1: 需求分析 (analyze)
{Read personas/core/analyst-core.md}

**任务**:
1. 完成基线扫描（scan-of-record）：补齐 key_files≥3（覆盖入口/配置/依赖或测试/可观测）与 facts（项目事实+锚点），并记录现有模式锚点（如存在）
2. 理解用户需求: {requirement}
3. 输出 RFC §1-§2 到 {rfc_dir}/rfc.md

### 阶段 2: 方案设计 (design)
{Read personas/core/architect-core.md}

**任务**:
1. 基于需求分析结果设计技术方案
2. 定义 API 契约和数据结构
3. 输出 RFC §3-§5 到 {rfc_dir}/rfc.md

### 阶段 3: 自动预检 (precheck)
**任务**:
1. 检查 RFC 结构完整性（5 个章节）
2. 验证场景覆盖（正常/异常/边界/不支持）
3. 检查 DFX 8 维度完整性
4. 检测模糊描述

### 输出要求
返回 JSON 格式结果：
```json
{{
  "status": "completed",
  "phases_executed": ["analyze", "design", "precheck"],
  "rfc_sections": ["§1", "§2", "§3", "§4", "§5"],
  "precheck_result": {{
    "passed": true/false,
    "issues": []
  }},
  "files_written": [
    {{"path": "{rfc_dir}/rfc.md", "written": true}},
    {{"path": "{rfc_dir}/findings.json", "written": true}},
    {{"path": "{rfc_dir}/progress.json", "written": true}}
  ],
  "ready_for_audit": true/false
}}
```
"""
    )

    # 解析结果
    merged_result = json.loads(result)

    # 验证文件写入
    verify_files_written(merged_result, rfc_dir)

    # 如果预检通过，直接进入审查
    if merged_result.get("ready_for_audit"):
        return execute_audit_phase(rfc_dir, project_root)
    else:
        # 预检失败，返回问题列表
        return merged_result
```

## MEDIUM Task: Resume Mode

MEDIUM 任务使用 Resume 模式，可选用户确认：

```python
def execute_medium_task(requirement: str, rfc_dir: str, project_root: str):
    """MEDIUM 任务：Resume 模式，可选确认"""

    # Phase 1: Analyze
    analyze_result = Task(
        subagent_type="Explore",
        description="Analyze requirements",
        model="haiku",
        prompt=f"""
## 需求分析阶段

{Read personas/core/analyst-core.md}

### 强制工作目录
- RFC 目录: {rfc_dir}

### 任务
分析需求: {requirement}
输出 RFC §1-§2

### 输出格式
JSON with files_written
"""
    )

    # 可选：检查是否需要用户确认（根据 config.yaml gate 配置）
    # MEDIUM 默认 auto，可跳过

    # Phase 2: Design (Resume)
    design_result = Task(
        subagent_type="Explore",
        description="Design solution",
        model="haiku",
        resume=True,  # 复用上一个 Subagent 的上下文
        prompt=f"""
## 方案设计阶段（Resume 模式）

你现在从 **需求分析师** 切换到 **架构设计师**。

{Read personas/core/architect-core.md}

### 上一阶段结果
{analyze_result}

### 任务
基于需求分析，设计技术方案
输出 RFC §3-§5

### 输出格式
JSON with files_written
"""
    )

    # Phase 3: Precheck (Resume)
    precheck_result = Task(
        subagent_type="Explore",
        description="Precheck RFC",
        model="haiku",
        resume=True,
        prompt=f"""
## 自动预检阶段（Resume 模式）

### 任务
检查 {rfc_dir}/rfc.md 的完整性

### 输出格式
JSON with precheck_result
"""
    )

    return precheck_result
```

## Implementation Examples

### Basic Usage: Execute Two Phases Consecutively

```python
# First call: Start subagent and execute analyze phase
analyst_result = Task(
    subagent_type="Explore",
    description="Analyst analyzes requirements",
    model="haiku",
    prompt=f"""
You are now the **Requirements Analyst** of the OHSpec expert team.

## Your Persona
{Read complete content of personas/core/analyst-core.md}

## Current Task
Execute requirements analysis phase (analyze)...

## After Phase Completion
After completing this phase, you will continue to the next phase (via resume parameter).
"""
)

# Parse result
analysis = json.loads(analyst_result)

# Check if user confirmation needed
if analysis["next_action"] == "user_review":
    # Show result, wait for user confirmation
    confirm = AskUserQuestion(...)
    if not confirm:
        return

# Second call: resume to same subagent, execute design phase
architect_result = Task(
    subagent_type="Explore",
    description="Architect designs solution",
    model="haiku",
    resume=True,  # Key: use resume instead of starting new subagent
    prompt=f"""
## Continue to Next Phase: Solution Design (design)

You are now switching to the **Solution Architect** role.

## Your Persona
{Read complete content of personas/core/architect-core.md}

## Previous Phase Result
{analysis["summary"]}

## Current Task
Execute solution design phase (design)...
"""
)
```

### Advanced Usage: Dynamic Phase Flow

```python
def execute_workflow_with_resume(requirement: str, complexity: str):
    """Execute complete workflow using Resume mode"""

    # Phase definitions
    phases = [
        {"id": "analyze", "expert": "analyst-core.md", "gate": "user_review"},
        {"id": "design", "expert": "architect-core.md", "gate": "user_review"},
        {"id": "audit", "expert": "auditor-core.md", "gate": "user_review"}
    ]

    # Simple tasks skip some gates
    if complexity == "SIMPLE":
        phases[0]["gate"] = "auto"  # analyze phase auto-flows
        phases[1]["gate"] = "auto"  # design phase auto-flows

    current_result = None
    use_resume = False

    for phase in phases:
        # Build prompt
        prompt = build_phase_prompt(phase, current_result)

        # Execute phase
        result = Task(
            subagent_type="Explore",
            description=f"{phase['id']} phase execution",
            model="haiku",
            resume=use_resume,  # First time False, subsequent True
            prompt=prompt
        )

        current_result = json.loads(result)

        # Check gate
        if phase["gate"] == "user_review" and current_result["next_action"] == "user_review":
            confirm = AskUserQuestion(f"Confirm {phase['id']} phase result?")
            if not confirm:
                break

        # Subsequent phases use resume
        use_resume = True

    return current_result
```

## Best Practices

### 1. Explicitly Switch Persona

```python
# ✅ Correct: Explicitly notify role switch
prompt = """
## Role Switch Notification
You are now switching from **Requirements Analyst** to **Solution Architect**.

## Your New Persona
{Read architect-core.md}

## Inherited Context
Key findings from previous phase (analyze):
- {key_finding_1}
- {key_finding_2}
"""

# ❌ Wrong: Assume subagent automatically knows role change
prompt = """
Now execute design phase...
"""
```

### 2. Pass Key Context

```python
# ✅ Correct: Explicitly pass key information
prompt = f"""
## Previous Phase Summary
{previous_result["summary"]}

## Key Findings
{json.dumps(previous_result["key_findings"], ensure_ascii=False)}

## Current Task
Based on the above analysis, design technical solution...
"""

# ❌ Wrong: Assume subagent remembers all details
prompt = "Continue design phase"
```

### 3. Update progress.json to Track Subagent ID

Update `templates/progress.json` to support Resume mode:

```markdown
## Phase Progress

### Phase 1: Requirements Analysis (analyze)
- **Status:** complete
- **Expert:** Requirements Analyst
- **Subagent ID:** [Record first-started subagent ID]  ← New field
- Actions performed: ...

### Phase 2: Solution Design (design)
- **Status:** in_progress
- **Expert:** Solution Architect
- **Subagent ID:** [same as Phase 1]  ← Indicates using resume
- Actions performed: ...
```

### 4. Error Recovery Handling

```python
try:
    result = Task(
        subagent_type="Explore",
        resume=True,
        prompt=prompt
    )
except SubagentError as e:
    # Resume failed, restart new subagent
    logging.warning(f"Resume failed, restarting: {e}")
    result = Task(
        subagent_type="Explore",
        resume=False,  # Don't use resume
        prompt=prompt
    )
```

## Performance Comparison

| Mode | Persona Load Count | Token Consumption | Use Case |
|------|-------------------|------------------|----------|
| Traditional Mode | 4 times (per phase) | ~11,200 | COMPLEX tasks (require per-phase confirmation) |
| Resume Mode | 1 time (first only) | ~3,800 | SIMPLE/MEDIUM tasks (auto-flow) |
| Savings | -3 times | ~7,400 | - |

## Considerations

### 1. Resume Limitations
- Resume relies on subagent session persistence; if timeout or network interruption occurs, session will be lost
- Long-running tasks (>5 minutes) not recommended for resume due to potential timeout

### 2. Context Pollution Risk
- In Resume mode, previous phase context is retained
- If previous phase has large code scan results, may pollute subsequent phase context
- Recommendation: Write key findings to findings.json, don't pass detailed scan results

### 3. Debugging Difficulty
- Debugging Resume mode is more difficult than independent subagents
- Recommendation: Use traditional mode during development, use resume optimization in production
