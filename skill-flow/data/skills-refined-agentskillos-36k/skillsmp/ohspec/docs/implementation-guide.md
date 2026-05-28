# Implementation Guide

This guide provides detailed implementation steps for the Orchestrator to execute the OHSpec workflow.

---

## 子代理输入契约

所有子代理调用必须遵循标准化输入契约，详见 [subagent-contract.md](./subagent-contract.md)。

契约包含 4 个必需部分：
1. **原始需求** - 用户原始输入
2. **上下文包** - findings.json 摘要、progress.json 状态、前序输出
3. **当前任务** - 本阶段具体任务
4. **验收标准** - 输出必须满足的条件

### 上下文传递机制

上下文包采用分级传递机制，详见 [context-transfer.md](./context-transfer.md)。

| 级别 | 内容 | Token 预算 | 传递时机 |
|------|------|-----------|---------|
| L0 | 核心元数据 | ~100 | 必传 |
| L1 | 关键决策 | ~300 | 必传 |
| L2 | 扫描摘要 | ~500 | 按需 |
| L3 | 详细分析 | ~2000+ | 按需读取 |

模板文件：`templates/context-pack.json`

### 上下文验证机制

为确保 Subagent 间传递的数据完整性，Orchestrator 必须执行以下验证流程。

#### 验证流程

```
传递前 → 计算 checksum → 传递 → 接收后重新计算 → 比对 → 不匹配则恢复
```

#### Checksum 计算

```python
import hashlib
import json

def compute_checksum(context_pack: dict) -> str:
    """
    计算上下文包的校验和（SHA-256 前 8 位）

    参数:
        context_pack: 上下文包字典

    返回:
        8 位十六进制校验和
    """
    # 序列化时排序键，确保一致性
    content = json.dumps(context_pack, sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(content.encode()).hexdigest()[:8]
```

#### 必填字段检查规则

| 级别 | 必填字段 | 检查条件 |
|------|---------|---------|
| L0 | `rfc_id`, `phase`, `intent`, `complexity` | 非空且类型正确 |
| L1 | `decisions`, `constraints` | 数组/对象存在 |
| L2 | `key_files`, `dependencies` | 按需时必须非空 |

```python
def validate_required_fields(context_pack: dict, strategy: str) -> dict:
    """
    验证必填字段

    参数:
        context_pack: 上下文包
        strategy: 压缩策略 (minimal/standard/full)

    返回:
        验证结果字典
    """
    result = {"l0_meta": False, "l1_decisions": False, "l2_summary": False}

    # L0: 必传
    l0 = context_pack.get("l0_meta", {})
    result["l0_meta"] = all([
        l0.get("rfc_id"),
        l0.get("phase"),
        l0.get("intent"),
        l0.get("complexity") in ["SIMPLE", "MEDIUM", "COMPLEX"]
    ])

    if strategy == "minimal":
        return result

    # L1: standard/full 必传
    l1 = context_pack.get("l1_decisions", {})
    result["l1_decisions"] = (
        isinstance(l1.get("decisions"), list) and
        isinstance(l1.get("constraints"), dict)
    )

    # L2: standard/full 按需
    l2 = context_pack.get("l2_summary", {})
    result["l2_summary"] = (
        isinstance(l2.get("key_files"), list) and
        isinstance(l2.get("dependencies"), dict)
    )

    return result
```

#### 传递失败恢复机制

```python
from datetime import datetime

def validate_and_recover(
    context_pack: dict,
    expected_checksum: str,
    rfc_dir: str,
    progress: dict
) -> dict:
    """
    验证上下文包，失败时从文件恢复

    参数:
        context_pack: 接收到的上下文包
        expected_checksum: 预期校验和
        rfc_dir: RFC 目录路径
        progress: progress.json 内容

    返回:
        验证后的上下文包（可能是恢复后的）
    """
    actual_checksum = compute_checksum(context_pack)
    validation = progress.setdefault("context_validation", {})

    if actual_checksum == expected_checksum:
        # 验证通过
        validation["checksum"] = actual_checksum
        validation["validation_status"] = "valid"
        validation["validated_at"] = datetime.now().isoformat()
        return context_pack

    # 验证失败，尝试恢复
    validation["validation_status"] = "invalid"
    recovery_entry = {
        "timestamp": datetime.now().isoformat(),
        "expected": expected_checksum,
        "actual": actual_checksum,
        "action": "reload_from_file"
    }

    # 从 findings.json 重新构建上下文包
    recovered_pack = build_context_pack(rfc_dir, context_pack.get("strategy", "standard"))
    recovered_checksum = compute_checksum(recovered_pack)

    recovery_entry["recovered_checksum"] = recovered_checksum
    recovery_entry["success"] = True
    validation.setdefault("recovery_log", []).append(recovery_entry)
    validation["validation_status"] = "recovered"
    validation["checksum"] = recovered_checksum
    validation["validated_at"] = datetime.now().isoformat()

    return recovered_pack
```

#### 验证状态说明

| 状态 | 含义 | 后续动作 |
|------|------|---------|
| `pending` | 未验证 | 执行验证 |
| `valid` | 校验和匹配 | 继续执行 |
| `invalid` | 校验和不匹配 | 触发恢复 |
| `recovered` | 已从文件恢复 | 继续执行 |

---

## Step 0: Initialize RFC Directory

Before launching any subagent, the Orchestrator must initialize the RFC directory structure.

### RFC ID Generation

RFC ID 格式: `RFC-{YYYYMMDD}-{slug}-{hash4}`

```python
import os
import json
import re
import hashlib
from datetime import datetime

def generate_rfc_id(requirement: str) -> str:
    """
    生成 RFC ID

    格式: RFC-{YYYYMMDD}-{slug}-{hash4}
    示例: RFC-20260115-3d-audio-toggle-a3f2

    参数:
        requirement: 用户需求描述

    返回:
        RFC ID
    """
    # 1. 日期部分
    date_part = datetime.now().strftime("%Y%m%d")

    # 2. Slug 部分（从需求中提取关键词）
    slug = generate_slug(requirement, max_length=30)

    # 3. 短哈希（保证唯一性）
    hash_input = f"{requirement}{datetime.now().isoformat()}"
    short_hash = hashlib.md5(hash_input.encode()).hexdigest()[:4]

    return f"RFC-{date_part}-{slug}-{short_hash}"

def generate_slug(text: str, max_length: int = 30) -> str:
    """
    从需求文本生成 URL 友好的 slug

    示例:
        "为音频服务增加 3D 音效开关" → "3d-audio"
        "Fix login page captcha issue" → "fix-login-page-captcha"
    """
    # 提取英文单词和数字
    words = re.findall(r'[a-zA-Z0-9]+', text.lower())

    # 最多取4个词
    slug = '-'.join(words[:4]) if words else 'unnamed'

    return slug[:max_length].strip('-')
```

### Directory Initialization（强制早落盘）

> **必须在任何扫描/分析前执行**，确保 rfc/findings/progress 三文件立即落盘。

```python
def init_rfc_directory(project_root: str, rfc_id: str) -> str:
    """
    初始化 RFC 目录结构

    参数:
        project_root: 项目根目录（绝对路径）
        rfc_id: RFC ID

    返回:
        RFC 目录的绝对路径
    """
    rfc_dir = f"{project_root}/.ohspec/rfcs/{rfc_id}"

    # 创建目录
    os.makedirs(rfc_dir, exist_ok=True)

    # 初始化三文件（强制早落盘，且格式必须正确）
    #
    # - rfc.md: Markdown（建议从 templates/rfc.md 复制并填充时间/状态）
    # - findings.json: JSON（优先从 templates/findings.json 复制并替换占位符；避免 JSONC 去注释导致 schema 漂移）
    # - progress.json: JSON（优先从 templates/progress.json 复制并替换占位符；避免 JSONC 去注释导致 schema 漂移）
    #
    # 关键点：不要往 .json 写入 Markdown 文本，否则后续阶段会解析失败。
    rfc_md_path = os.path.join(rfc_dir, "rfc.md")
    findings_path = os.path.join(rfc_dir, "findings.json")
    progress_path = os.path.join(rfc_dir, "progress.json")

    if not os.path.exists(rfc_md_path):
        with open(rfc_md_path, "w", encoding="utf-8") as f:
            f.write(f"# RFC: [功能标题]\\n\\n> 状态: DRAFT\\n> 创建时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\\n> 最后更新: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\\n\\n")

    if not os.path.exists(findings_path):
        with open(findings_path, "w", encoding="utf-8") as f:
            json.dump(
                {
                    "meta": {
                        "rfc_id": rfc_id,
                        "project_root": project_root,
                        "rfc_dir": rfc_dir,
                        "created_at": datetime.now().isoformat(),
                        "updated_at": datetime.now().isoformat(),
                        "repos": [{"id": "main", "root": project_root, "rev": "", "owner": "", "compat": "", "notes": ""}],
                    },
                    "requirement": {"original": "", "intent": "", "keywords": []},
                    "dispatcher": {"complexity": "", "reasoning": "", "experts": {"core": [], "extension": []}, "mode": "standard"},
                    "confirmed": {"decisions": [], "facts": [], "constraints": {"technical": [], "business": [], "scope": []}, "key_files": [], "dependencies": {"internal": [], "external": [], "integration_points": []}},
                    "working": {"phase": "", "scan_results": [], "pending_options": [], "pending_questions": []},
                    "issues": [],
                    "references": [],
                },
                f,
                ensure_ascii=False,
                indent=2,
            )

    if not os.path.exists(progress_path):
        with open(progress_path, "w", encoding="utf-8") as f:
            json.dump(
                {
                    "meta": {"rfc_id": rfc_id, "status": "DRAFT", "created_at": datetime.now().isoformat(), "updated_at": datetime.now().isoformat(), "completion": 0},
                    "tooling": {"search_tool": "", "fallback_used": "", "scan_scope": "", "metrics": {"total_searches": 0, "total_time_sec": 0, "avg_time_sec": 0}},
                    "audit_log": [],
                    "phases": {"dispatcher": {"status": "pending"}, "analyze": {"status": "pending"}, "design": {"status": "pending"}, "precheck": {"status": "pending"}, "audit": {"status": "pending"}},
                },
                f,
                ensure_ascii=False,
                indent=2,
            )

    return rfc_dir
```

### Usage Example

```python
# Orchestrator 初始化流程
project_root = os.getcwd()  # 或从环境获取
rfc_id = generate_rfc_id(user_requirement)
rfc_dir = init_rfc_directory(project_root, rfc_id)

# 后续所有 subagent 都使用这个 rfc_dir
print(f"RFC 目录已创建: {rfc_dir}")
```

---

## Step 0.5: Run ASSESS (Tooling/Scale Decision)

在启动 Dispatcher 基线扫描前，先执行 ASSESS（仅做工具/规模/分区决策，不 Read 代码内容）：
- 选择搜索工具（rg → ag → grep），并记录到 progress.json.tooling
- 估算扫描范围与策略（direct/grep_prefilter/parallel/summary）
- 输出到 progress.json（assess/strategy）

权威定义见：[workflows/assess.md](../workflows/assess.md)

---

## Step 1: Launch Dispatcher Subagent

> **Codex 兼容模式**：若 Task 子代理不可用，执行最小化 scan-of-record 回退（rg/ag/grep），并记录 audit_log/tooling。未满足 key_files ≥ 3（覆盖面达标）或 facts（项目事实+锚点）不足时，停在澄清阶段，并先给出候选锚点/模块供确认，最后才请求人工锚点。

Use the Task tool to launch the Dispatcher subagent, executing code scanning and complexity assessment in an isolated context:

### Model Selection Logic

```python
def get_model_for_phase(phase: str, complexity: str, user_override: str = None) -> str:
    """
    获取指定阶段应使用的模型

    参数:
        phase: 阶段名称 (dispatcher/analyze/design/audit)
        complexity: 复杂度 (simple/medium/complex)
        user_override: 用户覆盖 (high_quality/fast/None)

    返回:
        模型名称 (haiku/sonnet/opus)
    """
    # 用户覆盖优先
    if user_override == "high_quality" or user_override == "high":
        return "sonnet"  # 或 "opus"
    if user_override == "fast":
        return "haiku"

    # 按配置选择
    model_config = {
        "dispatcher": "sonnet",  # 始终 sonnet
        "audit": "sonnet",       # 始终 sonnet
        "analyze": {
            "simple": "haiku",
            "medium": "sonnet",
            "complex": "sonnet"
        },
        "design": {
            "simple": "haiku",
            "medium": "sonnet",
            "complex": "sonnet"
        }
    }

    if phase in ["dispatcher", "audit"]:
        return model_config[phase]
    else:
        return model_config.get(phase, {}).get(complexity, "sonnet")
```

### Dispatcher Prompt

```python
# 获取模型（Dispatcher 始终用 sonnet，除非用户指定 fast）
dispatcher_model = get_model_for_phase("dispatcher", None, user_model_override)

dispatcher_result = Task(
    subagent_type="Explore",
    description="Dispatcher analyzes requirements",
    model=dispatcher_model,  # 默认 sonnet
    prompt=f"""
You are now the **Dispatcher** of the OHSpec expert team.

## Your Persona
{Read complete content of personas/core/dispatcher-core.md}

## Current Task
User requirement: {user_input}

## 强制工作目录配置（必须遵守）
- 项目根目录: {project_root}
- RFC ID: {rfc_id}
- RFC 目录: {rfc_dir}

## 文件写入规则（强制）
所有文件必须写入以下绝对路径：
| 文件 | 绝对路径 |
|------|----------|
| findings.json | {rfc_dir}/findings.json |
| progress.json | {rfc_dir}/progress.json |

⚠️ 禁止使用相对路径
⚠️ 禁止写入 /tmp 或其他临时目录
⚠️ 写入前确认目录存在

## Your Tasks
1. Use Grep/Glob to scan codebase
2. Assess complexity level (SIMPLE/MEDIUM/COMPLEX)
3. Select expert combination (core + extension)
4. **Write detailed scan results to {rfc_dir}/findings.json**
5. **Update {rfc_dir}/progress.json with current status**
6. Generate analysis result summary (JSON format)

## Output Requirements
Generate a structured analysis result summary (JSON format), including:
- intent: One-sentence description of user requirement
- complexity: Complexity level (SIMPLE/MEDIUM/COMPLEX)
- reasoning: Rationale for complexity judgment
- scope: Scope involved (modules, files, dependencies)
  - modules: Module list
  - key_files: Key file list (format: {path, role}, path uses repo@rev:path#Lline)
  - dependencies: Dependency relationship list
- experts: Expert combination
  - core: Core expert list
  - extension: Extension expert list
- mode: Recommended execution mode (standard/fast)
- rfc_id: "{rfc_id}"
- files_written: List of files written with absolute paths

## 输出格式示例
```json
{{
  "intent": "为音频服务增加 3D 音效开关",
  "complexity": "MEDIUM",
  "reasoning": "涉及 3-5 个文件，单子系统内",
  "scope": {{
    "modules": ["AudioService", "AudioConfig"],
    "key_files": [
      {"path": "main@HEAD:src/audio/service.ts#L123", "role": "entry"},
      {"path": "main@HEAD:src/audio/config.ts#L45", "role": "config"}
    ],
    "dependencies": ["AudioManager", "PermissionManager"]
  }},
  "experts": {{
    "core": ["需求分析师", "架构设计师", "质量审查员"],
    "extension": []
  }},
  "mode": "standard",
  "rfc_id": "{rfc_id}",
  "files_written": [
    {{"path": "{rfc_dir}/findings.json", "written": true}},
    {{"path": "{rfc_dir}/progress.json", "written": true}}
  ]
}}
```

## Mandatory Checklist
- [ ] Used Grep/Glob to scan codebase
- [ ] Identified at least 3 relevant files with role coverage (entry/config/dependency or test/observability)
- [ ] Identified existing implementation patterns
- [ ] Analyzed dependency relationships
- [ ] **Written findings.json to {rfc_dir}/findings.json**
- [ ] **Updated progress.json at {rfc_dir}/progress.json**
"""
)
```

**Why Use Subagent**:
- Avoid main thread context consumption (save 19k-59k tokens)
- Code scan results don't pollute main thread
- Only return key summary information

### Verify Files Written

After Dispatcher returns, verify files were actually written:

```python
def verify_dispatcher_output(result: dict, rfc_dir: str) -> bool:
    """验证 Dispatcher 输出的文件是否实际写入"""
    import os

    files_written = result.get("files_written", [])
    if not files_written:
        raise ValueError("Dispatcher 未返回 files_written 字段")

    for file_info in files_written:
        path = file_info.get("path")
        if not path:
            continue
        if not os.path.exists(path):
            raise FileNotFoundError(f"文件未写入: {path}")
        if os.path.getsize(path) < 100:  # 至少 100 字节
            raise ValueError(f"文件内容过少: {path}")

    return True

# 使用示例
try:
    verify_dispatcher_output(dispatcher_result, rfc_dir)
    print("✅ Dispatcher 文件验证通过")
except Exception as e:
    print(f"❌ Dispatcher 文件验证失败: {e}")
    # 可选：重试或报错
```

---

## Step 2: User Confirmation

Present analysis results to user and confirm execution mode:

```
📋 Requirements Analysis Result

【Intent Understanding】
{One-sentence description of user requirement}

【Complexity Assessment】
Level: {SIMPLE/MEDIUM/COMPLEX}
Rationale: {Judgment basis}

【Scope Involved】
- Modules: {Module list}
- Files: {Key files}
- Dependencies: {Dependency relationships}

【Expert Combination】
- Core: Requirements Analyst, Solution Architect, Quality Auditor
- Extension: {On-demand experts}

【Execution Mode】
  [A] Standard Flow (Recommended)
  [B] Fast Track
```

## Step 3: Execute Workflow

Execute each phase in sequence based on user selection.

### Requirements Analysis Phase

```markdown
1. Read `workflows/analyze.md` and `personas/core/analyst-core.md`（或需要更多细节时读取 `personas/full/analyst.md`）
2. Use Task tool to launch Requirements Analyst subagent
3. Output RFC §1-§2 to `{RFC_DIR}/rfc.md`
4. User gate: Confirm requirements understanding is correct
```

**Question Template** (Requirements Analyst must use):
```
Based on code scanning, found [X] implementation approaches:
A. [Option A] (Reference: [file_path:line_number]) - [Pros/Cons]
B. [Option B] (Reference: [file_path:line_number]) - [Pros/Cons]
C. [Option C] (if applicable)

Which approach do you want the new feature to use?
```

**Prohibited**: Open-ended questions like "How do you want to implement?"

### Feasibility Validation Phase (If Needed)

```markdown
1. Read `workflows/spike.md` and `personas/extension/prototyper.md`
2. Use Task tool to launch Prototyper subagent
3. Output feasibility report to RFC §2
4. User gate: Confirm feasibility
```

### Solution Design Phase

```markdown
1. Read `workflows/design.md` and relevant expert Personas
2. Launch Solution Architect + extension experts (parallel or serial)
3. Output RFC §3-§5
4. User gate: Confirm design solution
```

### Automatic Precheck Phase

```markdown
1. Read `workflows/precheck.md`
2. Automatically check structure completeness, scenario coverage, DFX checklist
3. Generate precheck report
4. If blocking issues exist, return for modification
```

**Automatic Detection Rules**:
- **Vague Description Detection**: Flag vague terms like "requires permission", "good performance"
- **Gherkin Format Check**: Verify scenarios follow `#### Scenario:` + GIVEN/WHEN/THEN format
- **DFX Dimension Completeness**: Verify all 8 dimensions are covered
- **Scenario Coverage Check**: Verify inclusion of normal/exception/boundary/unsupported scenarios

### Quality Audit Phase

```markdown
1. Read `workflows/audit.md` and `personas/core/auditor-core.md`（或需要更多细节时读取 `personas/full/auditor.md`）
2. Use Task tool to launch Quality Auditor subagent
3. Output audit report and comprehensive score
4. Check if auto-fix is needed
5. User decision: Approve/Needs Discussion/Reject
```

**Audit Attitude**: Zero tolerance for ambiguity, directly point out issues

### Auto-Fix Loop (New)

当审查评分 < 80 且存在可自动修复的问题时，执行自动修复循环：

```python
def audit_with_auto_fix(rfc_dir: str, project_root: str, max_attempts: int = 3):
    """带自动修复的审查流程"""

    for attempt in range(1, max_attempts + 1):
        # 1. 执行审查
        audit_result = Task(
            subagent_type="Explore",
            description=f"Audit RFC (attempt {attempt})",
            model="haiku",
            prompt=f"""
## 质量审查阶段

{Read personas/core/auditor-core.md}

### 工作目录
- RFC 目录: {rfc_dir}

### 任务
审查 {rfc_dir}/rfc.md，输出包含问题分类的 JSON 结果

### 输出要求
必须包含 issues 数组，每个 issue 标注 auto_fixable
"""
        )

        result = json.loads(audit_result)

        # 2. 检查是否通过
        if result["score"] >= 80:
            return {
                "status": "passed",
                "score": result["score"],
                "decision": result["decision"],
                "attempts": attempt
            }

        # 3. 分离问题类型
        auto_fixable = [i for i in result["issues"] if i.get("auto_fixable")]
        manual_required = [i for i in result["issues"] if not i.get("auto_fixable")]

        # 4. 如果没有可自动修复的问题，退回用户
        if not auto_fixable:
            return {
                "status": "manual_required",
                "score": result["score"],
                "issues": manual_required,
                "attempts": attempt,
                "message": "所有问题都需要人工介入"
            }

        # 5. 执行自动修复
        fix_result = Task(
            subagent_type="Explore",
            description=f"Auto-fix issues (attempt {attempt})",
            model="haiku",
            prompt=f"""
## 自动修复任务（第 {attempt} 次尝试）

### 需要修复的问题
{json.dumps(auto_fixable, ensure_ascii=False, indent=2)}

### 修复规则
- vague_description: 使用 fix_suggestion 中的量化描述替换
- format_error: 转换为 Gherkin 格式（#### Scenario: + GIVEN/WHEN/THEN）
- missing_scenario: 基于模板补充缺失的场景类型
- missing_section: 生成章节骨架
- dfx_incomplete: 基于 findings.json 中的代码扫描结果补充

### 工作目录
- RFC 文件: {rfc_dir}/rfc.md

### 输出要求
返回 JSON：
{{
  "fixed_count": 3,
  "fixed_issues": ["ISS-001", "ISS-002", "ISS-003"],
  "files_updated": ["{rfc_dir}/rfc.md"]
}}
"""
        )

        # 6. 记录修复日志
        log_fix_attempt(rfc_dir, attempt, auto_fixable, fix_result)

        # 继续下一轮审查

    # 7. 超过最大尝试次数
    return {
        "status": "max_attempts_exceeded",
        "score": result["score"],
        "issues": result["issues"],
        "attempts": max_attempts,
        "message": f"已尝试 {max_attempts} 次自动修复，仍有问题未解决"
    }


def log_fix_attempt(rfc_dir: str, attempt: int, issues: list, result: dict):
    """记录修复尝试到 progress.json"""
    import json
    from datetime import datetime

    progress_path = f"{rfc_dir}/progress.json"
    with open(progress_path, 'r') as f:
        progress = json.load(f)

    # 添加修复记录
    if "auto_fix_log" not in progress:
        progress["auto_fix_log"] = []

    progress["auto_fix_log"].append({
        "attempt": attempt,
        "timestamp": datetime.now().isoformat(),
        "issues_count": len(issues),
        "issues": [i["id"] for i in issues],
        "result": result
    })

    with open(progress_path, 'w') as f:
        json.dump(progress, f, ensure_ascii=False, indent=2)
```

---

## 阶段转换清理

阶段切换时，Orchestrator 必须执行 findings.json 的数据清理，将有价值的信息迁移到 `confirmed` 分区，清空 `working` 分区。

### 清理规则

| 数据类型 | 清理规则 | 目标位置 |
|---------|---------|---------|
| `pending_options` | 用户选中 → 迁移 | `confirmed.decisions` |
| `pending_options` | 未选中 → 删除 | - |
| `scan_results` | 去重后迁移 | `confirmed.key_files` |
| `pending_questions` | 已解答 → 删除 | - |
| `pending_questions` | 未解答 → 保留到 `issues` | `issues` |
| `working.phase` | 更新为下一阶段 | - |

### 执行时机

```
阶段完成 → 用户确认 → 执行清理 → 进入下一阶段
```

### 清理函数

```python
def cleanup_phase_transition(rfc_dir: str, next_phase: str, selected_options: list[str] = None):
    """
    阶段转换时清理 findings.json

    参数:
        rfc_dir: RFC 目录路径
        next_phase: 下一阶段名称
        selected_options: 用户选中的选项 ID 列表
    """
    import json
    from datetime import datetime

    findings_path = f"{rfc_dir}/findings.json"
    with open(findings_path, 'r') as f:
        findings = json.load(f)

    working = findings.get("working", {})
    confirmed = findings.get("confirmed", {})
    selected_options = selected_options or []

    # 1. pending_options: 选中→confirmed，未选中→删除
    for opt in working.get("pending_options", []):
        if opt["id"] in selected_options:
            confirmed.setdefault("decisions", []).append({
                "id": opt["id"],
                "decision": opt["option"],
                "rationale": f"用户选择，优势: {opt.get('pros', [])}",
                "confirmed_at": datetime.now().isoformat()
            })

    # 2. scan_results: 去重→合并到 confirmed.key_files
    existing_paths = {f["path"] for f in confirmed.get("key_files", [])}
    for scan in working.get("scan_results", []):
        if scan.get("path") and scan["path"] not in existing_paths:
            confirmed.setdefault("key_files", []).append({
                "path": scan["path"],
                "role": scan.get("role", "related"),
                "reason": scan.get("reason", "阶段扫描发现")
            })
            existing_paths.add(scan["path"])

    # 3. pending_questions: 未解答→issues
    for q in working.get("pending_questions", []):
        if not q.get("resolved"):
            findings.setdefault("issues", []).append({
                "id": q.get("id"),
                "description": q.get("question"),
                "from_phase": working.get("phase"),
                "created_at": datetime.now().isoformat()
            })

    # 4. 清空 working，准备下一阶段
    findings["working"] = {
        "phase": next_phase,
        "scan_results": [],
        "pending_options": [],
        "pending_questions": []
    }

    findings["confirmed"] = confirmed
    findings["meta"]["updated_at"] = datetime.now().isoformat()

    with open(findings_path, 'w') as f:
        json.dump(findings, f, ensure_ascii=False, indent=2)
```

### 清理前后示例

**清理前** (`working` 分区):
```json
{
  "working": {
    "phase": "requirement",
    "scan_results": [
      {"path": "src/audio/service.ts", "role": "core", "reason": "音频服务主文件"},
      {"path": "src/audio/config.ts", "role": "config", "reason": "配置文件"}
    ],
    "pending_options": [
      {"id": "O001", "option": "使用 WebAudio API", "pros": ["原生支持"], "cons": ["兼容性"]},
      {"id": "O002", "option": "使用 Howler.js", "pros": ["跨平台"], "cons": ["额外依赖"]}
    ],
    "pending_questions": [
      {"id": "Q001", "question": "是否需要支持 IE11?", "resolved": true},
      {"id": "Q002", "question": "性能基准是多少?", "resolved": false}
    ]
  }
}
```

**用户选择**: `["O001"]` (选择 WebAudio API)

**清理后**:
```json
{
  "confirmed": {
    "decisions": [
      {"id": "O001", "decision": "使用 WebAudio API", "rationale": "用户选择，优势: ['原生支持']", "confirmed_at": "2026-01-16T10:30:00"}
    ],
    "key_files": [
      {"path": "src/audio/service.ts", "role": "core", "reason": "音频服务主文件"},
      {"path": "src/audio/config.ts", "role": "config", "reason": "配置文件"}
    ]
  },
  "working": {
    "phase": "design",
    "scan_results": [],
    "pending_options": [],
    "pending_questions": []
  },
  "issues": [
    {"id": "Q002", "description": "性能基准是多少?", "from_phase": "requirement", "created_at": "2026-01-16T10:30:00"}
  ]
}
```

---

## 并行执行指南

### 概述

并行执行可显著提升工作流效率，适用于无数据依赖的任务组合。

### 可并行场景

| 场景 | 任务组合 | 条件 | 收益 |
|------|----------|------|------|
| 初始化 | Dispatcher + 项目上下文加载 | 首次运行 | ~30s |
| 深度分析 | 代码扫描 + 竞品分析 | COMPLEX 任务 | ~60s |
| 多模块 | 模块 A 扫描 + 模块 B 扫描 | 跨子系统 | ~40s |

### 并行执行实现

```python
import asyncio
from concurrent.futures import ThreadPoolExecutor

async def parallel_init(project_root: str, rfc_id: str, user_requirement: str):
    """
    并行执行 Dispatcher 和项目上下文加载

    条件：首次运行，两任务无数据依赖
    """
    async def run_dispatcher():
        return Task(
            subagent_type="Explore",
            description="Dispatcher 分析",
            prompt=f"... dispatcher prompt ..."
        )

    async def load_project_context():
        return Task(
            subagent_type="Explore",
            description="加载项目上下文",
            prompt=f"读取 {project_root}/.claude/project-context.json"
        )

    # 并行执行
    dispatcher_result, context_result = await asyncio.gather(
        run_dispatcher(),
        load_project_context()
    )

    # 合并结果
    return merge_results(dispatcher_result, context_result)


async def parallel_deep_analysis(rfc_dir: str, complexity: str):
    """
    并行执行代码扫描和竞品分析

    条件：COMPLEX 任务，结果写入独立分区
    """
    if complexity != "COMPLEX":
        return None

    async def code_scan():
        return Task(
            subagent_type="Explore",
            description="深度代码扫描",
            prompt="扫描代码库，输出到 findings.working.scan_results"
        )

    async def competitive_analysis():
        return Task(
            subagent_type="Explore",
            description="竞品分析",
            prompt="分析竞品方案，输出到 findings.confirmed.competitive"
        )

    scan_result, competitive_result = await asyncio.gather(
        code_scan(),
        competitive_analysis()
    )

    return {
        "scan": scan_result,
        "competitive": competitive_result
    }
```

### 结果合并函数

```python
def merge_results(dispatcher_result: dict, context_result: dict) -> dict:
    """
    合并并行任务结果到 findings.json

    规则：
    - Dispatcher 结果为主数据源
    - 项目上下文补充到 confirmed.context
    - 冲突时 Dispatcher 优先
    """
    merged = dispatcher_result.copy()

    # 合并项目上下文到独立分区
    merged.setdefault("confirmed", {})
    merged["confirmed"]["context"] = context_result

    return merged
```

### 依赖关系检查

```python
def can_parallelize(task_a: str, task_b: str) -> bool:
    """
    检查两个任务是否可并行

    返回 True 的条件：
    1. 无数据依赖
    2. 无资源冲突（不同时写入同一文件）
    3. 结果可独立合并
    """
    # 定义任务依赖图
    dependencies = {
        "dispatcher": [],
        "project_context": [],
        "code_scan": ["dispatcher"],
        "competitive_analysis": ["dispatcher"],
        "analyze": ["dispatcher"],
        "design": ["analyze"],
        "audit": ["design"]
    }

    # 检查是否存在依赖
    if task_b in dependencies.get(task_a, []):
        return False
    if task_a in dependencies.get(task_b, []):
        return False

    return True
```

### 使用示例

```python
# Orchestrator 中的并行执行流程
async def optimized_workflow(user_requirement: str, project_root: str):
    rfc_id = generate_rfc_id(user_requirement)
    rfc_dir = init_rfc_directory(project_root, rfc_id)

    # 阶段 1：并行初始化
    init_result = await parallel_init(project_root, rfc_id, user_requirement)
    complexity = init_result["complexity"]

    # 用户确认
    await user_confirmation(init_result)

    # 阶段 2：COMPLEX 任务并行深度分析
    if complexity == "COMPLEX":
        deep_result = await parallel_deep_analysis(rfc_dir, complexity)
        merge_to_findings(rfc_dir, deep_result)

    # 后续阶段串行执行（存在数据依赖）
    await execute_analyze(rfc_dir)
    await execute_design(rfc_dir)
    await execute_audit(rfc_dir)
```

---

## Step 4: Output Final RFC

After completing all phases, output complete RFC document.

---

## 项目知识库使用指南

### 概述

项目知识库（`project-knowledge.json`）用于跨 RFC 积累可复用的知识，包括：
- 常见需求模式
- 可复用的 DFX 模板
- 历史决策经验
- 项目技术约束汇总

### 知识库位置

```
{PROJECT_ROOT}/.ohspec/project-knowledge.json
```

模板文件：`templates/project-knowledge.json`

### 知识提炼规则

#### 提炼时机

RFC 完成审查后，Orchestrator 执行知识提炼：

```
RFC 审查通过 → 提炼知识 → 更新 project-knowledge.json
```

#### 提炼标准

| 知识类型 | 提炼条件 | 目标分区 |
|---------|---------|---------|
| 需求模式 | 相似需求出现 ≥2 次 | `patterns` |
| DFX 模板 | 检查项可跨项目复用 | `dfx_templates` |
| 技术决策 | 决策具有参考价值 | `decisions` |
| 技术约束 | 项目级硬性约束 | `constraints` |
| 反模式 | 发现应避免的实现 | `anti_patterns` |

#### 提炼函数

```python
def extract_knowledge(rfc_dir: str, knowledge_path: str):
    """
    从完成的 RFC 中提炼知识

    参数:
        rfc_dir: RFC 目录路径
        knowledge_path: project-knowledge.json 路径
    """
    import json
    from datetime import datetime

    # 读取 RFC 相关文件
    with open(f"{rfc_dir}/findings.json", 'r') as f:
        findings = json.load(f)
    with open(f"{rfc_dir}/rfc.md", 'r') as f:
        rfc_content = f.read()

    # 读取现有知识库
    with open(knowledge_path, 'r') as f:
        knowledge = json.load(f)

    rfc_id = findings["meta"]["rfc_id"]

    # 1. 提炼技术决策
    for decision in findings.get("confirmed", {}).get("decisions", []):
        if is_reusable_decision(decision):
            knowledge["decisions"].append({
                "id": generate_decision_id(knowledge),
                "title": decision.get("decision"),
                "context": decision.get("rationale"),
                "decision": decision.get("decision"),
                "related_rfcs": [rfc_id],
                "created_at": datetime.now().strftime("%Y-%m-%d")
            })

    # 2. 提炼约束条件
    constraints = findings.get("confirmed", {}).get("constraints", {})
    merge_constraints(knowledge["constraints"], constraints)

    # 3. 更新元数据
    knowledge["meta"]["updated_at"] = datetime.now().isoformat()

    # 写回知识库
    with open(knowledge_path, 'w') as f:
        json.dump(knowledge, f, ensure_ascii=False, indent=2)


def is_reusable_decision(decision: dict) -> bool:
    """判断决策是否值得提炼"""
    # 有明确理由且非临时性决策
    return bool(decision.get("rationale")) and not decision.get("temporary")


def generate_decision_id(knowledge: dict) -> str:
    """生成决策 ID"""
    count = len(knowledge.get("decisions", []))
    return f"DEC-{count + 1:03d}"


def merge_constraints(target: dict, source: dict):
    """合并约束条件，避免重复"""
    for key, values in source.items():
        if key not in target:
            target[key] = {}
        if isinstance(values, list):
            existing = target[key] if isinstance(target[key], list) else []
            for v in values:
                if v not in existing:
                    existing.append(v)
            target[key] = existing
        elif isinstance(values, dict):
            target[key].update(values)
```

### 知识库查询

Dispatcher 和其他 Subagent 在执行前应查询知识库：

```python
def query_patterns(knowledge_path: str, keywords: list[str]) -> list[dict]:
    """
    查询匹配的需求模式

    参数:
        knowledge_path: 知识库路径
        keywords: 需求关键词

    返回:
        匹配的模式列表
    """
    import json

    with open(knowledge_path, 'r') as f:
        knowledge = json.load(f)

    matches = []
    for category in knowledge.get("patterns", {}).values():
        for pattern in category:
            # 检查关键词匹配
            applicable = pattern.get("applicable_when", [])
            if any(kw in ' '.join(applicable).lower() for kw in keywords):
                matches.append(pattern)

    return matches


def get_dfx_checklist(knowledge_path: str, dimension: str) -> dict:
    """
    获取指定 DFX 维度的检查清单

    参数:
        knowledge_path: 知识库路径
        dimension: DFX 维度 (performance/reliability/...)

    返回:
        检查清单
    """
    import json

    with open(knowledge_path, 'r') as f:
        knowledge = json.load(f)

    return knowledge.get("dfx_templates", {}).get(dimension, {})
```

### 与 findings.json 的关系

| 文件 | 作用域 | 生命周期 | 内容 |
|------|--------|---------|------|
| `findings.json` | 单个 RFC | RFC 生命周期内 | 当前需求的扫描结果和决策 |
| `project-knowledge.json` | 整个项目 | 长期积累 | 跨 RFC 的可复用知识 |

数据流向：
```
findings.json (RFC 完成) → 提炼 → project-knowledge.json
project-knowledge.json → 查询 → 新 RFC 的 Dispatcher
```

---

## Token 优化指南

### 优化目标

| 优化点 | 优化前 | 优化后 | 节省比例 |
|--------|--------|--------|----------|
| Dispatcher 返回 | ~5000 tokens | ~500 tokens | 90% |
| Persona 加载 | ~700 tokens/个 | ~300 tokens/个 | 57% |
| 上下文传递 | ~2000 tokens | ~500 tokens | 75% |
| 单次工作流总计 | ~15000 tokens | ~5000 tokens | 67% |

### 各阶段 Token 预算

| 阶段 | JSON 摘要 | 文件输出 | 总预算 |
|------|-----------|----------|--------|
| Dispatcher | ≤500 | ≤2000 (findings.json) | ≤2500 |
| Analyst | ≤400 | ≤1500 (RFC §1-§2) | ≤2000 |
| Architect | ≤400 | ≤2000 (RFC §3-§5) | ≤2500 |
| Auditor | ≤500 | ≤1000 (审查报告) | ≤1500 |

### 核心优化策略

#### 1. 强制 JSON 摘要返回

所有 Persona 必须返回精简 JSON 摘要，详细内容写入文件：

```python
# 错误示例：返回完整扫描结果
return {
    "scan_results": [... 大量代码片段 ...],  # ❌ ~3000 tokens
    "analysis": "详细分析..."  # ❌ ~1500 tokens
}

# 正确示例：返回摘要，详情写文件
return {
    "summary": "扫描完成，发现3个核心文件",  # ✅ ~50 tokens
    "key_files": [
        {"path": "src/a.ts:10", "role": "entry"},
        {"path": "src/b.ts:20", "role": "config"}
    ],  # ✅ ~60 tokens
    "files_updated": ["findings.json"]  # 详情已写入文件
}
```

#### 2. Persona 按需加载

```python
def load_persona(phase: str, complexity: str) -> str:
    """按需加载 Persona，优先使用 core 版本"""
    if complexity == "SIMPLE":
        return read_file(f"personas/core/{phase}-core.md")  # ~300 tokens
    return read_file(f"personas/full/{phase}.md")  # ~700 tokens
```

#### 3. 上下文分级传递

| 级别 | 内容 | Token 预算 | 传递条件 |
|------|------|-----------|----------|
| L0 | RFC ID、阶段、状态 | ~100 | 必传 |
| L1 | 关键决策、复杂度 | ~300 | 必传 |
| L2 | 扫描摘要（≤5文件） | ~500 | 按需 |
| L3 | 详细分析 | ~2000+ | 引用文件路径 |

#### 4. 数组长度限制

- modules: ≤3 个
- key_files: ≤5 个
- dependencies: ≤5 个
- issues: ≤10 个（info 级别只计数）

### Token 超限处理

```python
def validate_response(response: dict, phase: str) -> dict:
    """验证响应是否符合 Token 预算"""
    limits = {"dispatcher": 500, "analyst": 400, "architect": 400, "auditor": 500}
    json_str = json.dumps(response, ensure_ascii=False)
    estimated_tokens = len(json_str) // 4

    if estimated_tokens > limits.get(phase, 500):
        return compress_response(response, limits[phase])
    return response
```

---

## RFC 完成后提炼流程

### 概述

RFC 完成审查并获得批准后，Orchestrator 需要自动执行知识提炼流程，将 RFC 中的可复用知识提取并积累到项目知识库中。这个流程确保项目经验得到系统化积累，后续 RFC 可以复用这些知识。

### 触发条件

提炼流程在以下条件满足时自动触发：

```
RFC 状态变为 APPROVED → 执行提炼 → 更新 project-knowledge.json
```

**触发检查清单**：
- [ ] RFC 审查评分 ≥ 80 分
- [ ] RFC 状态已更新为 APPROVED
- [ ] findings.json 和 rfc.md 都已完成
- [ ] project-knowledge.json 文件存在

### 提炼规则详解

#### 1. 可复用模式提炼（patterns）

**提炼条件**：相似需求在历史 RFC 中出现 ≥ 2 次

**提炼维度**：

| 模式类型 | 提炼来源 | 提炼规则 | 示例 |
|---------|---------|---------|------|
| 功能模式 | RFC §2 需求 | 识别通用的功能实现模式 | 开关类、配置类、权限类功能 |
| 集成模式 | RFC §3 契约 | 识别与外部系统的集成方式 | API 集成、数据库集成、第三方服务 |
| 数据模式 | RFC §3 数据结构 | 识别数据处理和存储的标准方案 | 缓存策略、同步策略、版本管理 |
| UI 模式 | RFC §3 场景规格 | 识别界面交互的标准方案 | 表单、列表、对话框、通知 |

**提炼函数**：

```python
def extract_patterns(rfc_content: str, findings: dict, knowledge: dict) -> list[dict]:
    """
    从 RFC 中提炼可复用的模式
    
    参数:
        rfc_content: RFC 文件内容
        findings: findings.json 内容
        knowledge: 现有知识库
    
    返回:
        新提炼的模式列表
    """
    import re
    from datetime import datetime
    
    patterns = []
    rfc_id = findings["meta"]["rfc_id"]
    
    # 1. 从 RFC §2 需求中识别功能模式
    requirement_section = extract_section(rfc_content, "§2")
    if requirement_section:
        # 检查是否为开关类功能
        if re.search(r'(启用|禁用|开关|toggle|enable|disable)', requirement_section, re.I):
            pattern = {
                "id": generate_pattern_id(knowledge, "feature"),
                "name": "开关类功能",
                "description": "布尔开关的标准实现模式",
                "category": "feature",
                "applicable_when": ["需要启用/禁用某功能", "需要配置项控制行为"],
                "template": {
                    "config_key": "{feature}_enabled",
                    "api_pattern": "enable{Feature}() / disable{Feature}() / is{Feature}Enabled()",
                    "storage": "SharedPreferences / UserDefaults / localStorage"
                },
                "examples": [rfc_id],
                "created_at": datetime.now().strftime("%Y-%m-%d")
            }
            patterns.append(pattern)
    
    # 2. 从 RFC §3 契约中识别集成模式
    contract_section = extract_section(rfc_content, "§3")
    if contract_section:
        # 检查是否涉及 API 集成
        if re.search(r'(API|接口|endpoint|request|response)', contract_section, re.I):
            pattern = {
                "id": generate_pattern_id(knowledge, "integration"),
                "name": "API 集成模式",
                "description": "与外部 API 集成的标准方案",
                "category": "integration",
                "applicable_when": ["需要调用外部 API", "需要处理网络请求"],
                "template": {
                    "error_handling": "Result<T> 包装",
                    "retry_strategy": "指数退避",
                    "timeout": "30s"
                },
                "examples": [rfc_id],
                "created_at": datetime.now().strftime("%Y-%m-%d")
            }
            patterns.append(pattern)
    
    return patterns


def extract_section(content: str, section_marker: str) -> str:
    """提取 RFC 中的指定章节"""
    import re
    pattern = rf"## {section_marker}.*?(?=## §|$)"
    match = re.search(pattern, content, re.DOTALL)
    return match.group(0) if match else ""


def generate_pattern_id(knowledge: dict, category: str) -> str:
    """生成模式 ID"""
    patterns = knowledge.get("patterns", {}).get(category, [])
    count = len(patterns)
    return f"P-{category.upper()}-{count + 1:03d}"
```

#### 2. DFX 模板提炼（dfx_templates）

**提炼条件**：检查项可跨项目复用

**提炼维度**：8 个 DFX 维度

| 维度 | 提炼来源 | 提炼规则 | 示例 |
|------|---------|---------|------|
| Performance | RFC §4.3 | 提取性能指标和检查项 | API 响应时间、吞吐量 |
| Reliability | RFC §4.2 | 提取可靠性指标和检查项 | 异常处理、降级方案 |
| Usability | RFC §4.4 | 提取可用性指标和检查项 | 用户界面、易用性 |
| Maintainability | RFC §4.6 | 提取可维护性指标和检查项 | 代码复杂度、文档要求 |
| Testability | RFC §4.4 | 提取可测试性指标和检查项 | 测试覆盖率、Mock 策略 |
| Observability | RFC §4.5 | 提取可观测性指标和检查项 | 日志规范、监控指标 |
| Compatibility | RFC §4.7 | 提取兼容性指标和检查项 | API 版本、向后兼容 |
| Scalability | RFC §4.8 | 提取可扩展性指标和检查项 | 部署策略、扩展方案 |

**提炼函数**：

```python
def extract_dfx_templates(rfc_content: str, findings: dict, knowledge: dict) -> dict:
    """
    从 RFC §4 DFX 约束中提炼可复用的 DFX 模板
    
    参数:
        rfc_content: RFC 文件内容
        findings: findings.json 内容
        knowledge: 现有知识库
    
    返回:
        按维度组织的 DFX 模板字典
    """
    import re
    from datetime import datetime
    
    dfx_templates = {}
    rfc_id = findings["meta"]["rfc_id"]
    
    # 定义 DFX 维度和对应的 RFC 章节
    dfx_dimensions = {
        "performance": "§4.3",
        "reliability": "§4.2",
        "usability": "§4.4",
        "maintainability": "§4.6",
        "testability": "§4.4",
        "observability": "§4.5",
        "compatibility": "§4.7",
        "scalability": "§4.8"
    }
    
    for dimension, section in dfx_dimensions.items():
        section_content = extract_section(rfc_content, section)
        if not section_content:
            continue
        
        # 提取指标（metrics）
        metrics = extract_metrics(section_content, dimension)
        
        # 提取检查项（checklist）
        checklist = extract_checklist(section_content, dimension)
        
        if metrics or checklist:
            dfx_templates[dimension] = {
                "metrics": metrics,
                "checklist": checklist,
                "source_rfc": rfc_id,
                "created_at": datetime.now().strftime("%Y-%m-%d")
            }
    
    return dfx_templates


def extract_metrics(content: str, dimension: str) -> list[dict]:
    """从内容中提取指标定义"""
    import re
    
    metrics = []
    # 查找形如 "指标名: 目标值" 的行
    pattern = r'[-•]\s*\*\*([^*]+)\*\*[:\s]+([^(\n]+)'
    matches = re.findall(pattern, content)
    
    for name, target in matches:
        metrics.append({
            "id": f"METRIC-{dimension.upper()}-{len(metrics) + 1:03d}",
            "name": name.strip(),
            "target": target.strip(),
            "measurement": "待定义"
        })
    
    return metrics


def extract_checklist(content: str, dimension: str) -> list[str]:
    """从内容中提取检查项"""
    import re
    
    checklist = []
    # 查找检查项（通常以 - 或 • 开头）
    pattern = r'[-•]\s+([^(\n]+?)(?:\(|$)'
    matches = re.findall(pattern, content)
    
    for item in matches:
        item = item.strip()
        if item and len(item) > 5:  # 过滤过短的项
            checklist.append(item)
    
    return checklist
```

#### 3. 技术决策提炼（decisions）

**提炼条件**：决策具有参考价值且有明确理由

**提炼来源**：RFC §5 设计决策

**提炼函数**：

```python
def extract_decisions(rfc_content: str, findings: dict, knowledge: dict) -> list[dict]:
    """
    从 RFC §5 设计决策中提炼技术决策
    
    参数:
        rfc_content: RFC 文件内容
        findings: findings.json 内容
        knowledge: 现有知识库
    
    返回:
        新提炼的决策列表
    """
    import re
    from datetime import datetime
    
    decisions = []
    rfc_id = findings["meta"]["rfc_id"]
    
    # 提取 §5.1 架构决策记录 (ADR)
    adr_section = extract_section(rfc_content, "§5.1")
    if adr_section:
        # 查找表格行
        pattern = r'\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|'
        matches = re.findall(pattern, adr_section)
        
        for decision_point, options, choice, rationale in matches:
            if decision_point.strip() and choice.strip():
                decision = {
                    "id": generate_decision_id(knowledge),
                    "title": decision_point.strip(),
                    "context": f"在 {rfc_id} 中做出",
                    "options_considered": [
                        {"option": opt.strip(), "pros": [], "cons": []}
                        for opt in options.split("/") if opt.strip()
                    ],
                    "decision": choice.strip(),
                    "rationale": rationale.strip(),
                    "outcome": "待验证",
                    "related_rfcs": [rfc_id],
                    "created_at": datetime.now().strftime("%Y-%m-%d")
                }
                decisions.append(decision)
    
    # 从 findings.json 中提取已确认的决策
    for confirmed_decision in findings.get("confirmed", {}).get("decisions", []):
        if is_reusable_decision(confirmed_decision):
            decision = {
                "id": generate_decision_id(knowledge),
                "title": confirmed_decision.get("decision", "未命名决策"),
                "context": confirmed_decision.get("rationale", ""),
                "decision": confirmed_decision.get("decision"),
                "related_rfcs": [rfc_id],
                "created_at": datetime.now().strftime("%Y-%m-%d")
            }
            decisions.append(decision)
    
    return decisions


def is_reusable_decision(decision: dict) -> bool:
    """判断决策是否值得提炼"""
    return bool(decision.get("rationale")) and not decision.get("temporary")


def generate_decision_id(knowledge: dict) -> str:
    """生成决策 ID"""
    count = len(knowledge.get("decisions", []))
    return f"DEC-{count + 1:03d}"
```

#### 4. 技术约束提炼（constraints）

**提炼条件**：项目级别的硬性约束

**提炼来源**：findings.json 中的约束信息

**提炼函数**：

```python
def extract_constraints(findings: dict, knowledge: dict) -> dict:
    """
    从 findings.json 中提炼技术约束
    
    参数:
        findings: findings.json 内容
        knowledge: 现有知识库
    
    返回:
        新提炼的约束字典
    """
    constraints = {}
    
    # 从 findings.json 中提取约束
    confirmed_constraints = findings.get("confirmed", {}).get("constraints", {})
    
    for constraint_type, constraint_values in confirmed_constraints.items():
        if constraint_type not in constraints:
            constraints[constraint_type] = {}
        
        if isinstance(constraint_values, dict):
            constraints[constraint_type].update(constraint_values)
        elif isinstance(constraint_values, list):
            if constraint_type not in constraints:
                constraints[constraint_type] = []
            for value in constraint_values:
                if value not in constraints[constraint_type]:
                    constraints[constraint_type].append(value)
    
    return constraints
```

### 去重和合并机制

**去重规则**：

```python
def deduplicate_knowledge(new_knowledge: dict, existing_knowledge: dict) -> dict:
    """
    去重新提炼的知识，避免重复
    
    参数:
        new_knowledge: 新提炼的知识
        existing_knowledge: 现有知识库
    
    返回:
        去重后的知识
    """
    import json
    
    # 1. 去重模式（patterns）
    for category, patterns in new_knowledge.get("patterns", {}).items():
        existing_patterns = existing_knowledge.get("patterns", {}).get(category, [])
        for pattern in patterns:
            # 检查是否已存在相同的模式
            if not any(
                p["name"] == pattern["name"] and p["category"] == pattern["category"]
                for p in existing_patterns
            ):
                existing_knowledge.setdefault("patterns", {}).setdefault(category, []).append(pattern)
    
    # 2. 去重 DFX 模板（dfx_templates）
    for dimension, template in new_knowledge.get("dfx_templates", {}).items():
        existing_template = existing_knowledge.get("dfx_templates", {}).get(dimension, {})
        
        # 合并 metrics
        existing_metrics = existing_template.get("metrics", [])
        for metric in template.get("metrics", []):
            if not any(m["name"] == metric["name"] for m in existing_metrics):
                existing_metrics.append(metric)
        
        # 合并 checklist
        existing_checklist = existing_template.get("checklist", [])
        for item in template.get("checklist", []):
            if item not in existing_checklist:
                existing_checklist.append(item)
        
        existing_knowledge.setdefault("dfx_templates", {})[dimension] = {
            "metrics": existing_metrics,
            "checklist": existing_checklist
        }
    
    # 3. 去重决策（decisions）
    existing_decisions = existing_knowledge.get("decisions", [])
    for decision in new_knowledge.get("decisions", []):
        if not any(
            d["title"] == decision["title"] and d["decision"] == decision["decision"]
            for d in existing_decisions
        ):
            existing_decisions.append(decision)
    
    # 4. 合并约束（constraints）
    merge_constraints(
        existing_knowledge.get("constraints", {}),
        new_knowledge.get("constraints", {})
    )
    
    return existing_knowledge


def merge_constraints(target: dict, source: dict):
    """合并约束条件，避免重复"""
    for key, values in source.items():
        if key not in target:
            target[key] = {}
        
        if isinstance(values, list):
            existing = target[key] if isinstance(target[key], list) else []
            for v in values:
                if v not in existing:
                    existing.append(v)
            target[key] = existing
        elif isinstance(values, dict):
            if not isinstance(target[key], dict):
                target[key] = {}
            target[key].update(values)
```

### 完整的提炼流程

```python
def extract_knowledge_from_rfc(rfc_dir: str, project_root: str):
    """
    RFC 完成后的完整知识提炼流程
    
    参数:
        rfc_dir: RFC 目录路径
        project_root: 项目根目录路径
    """
    import json
    import os
    from datetime import datetime
    
    knowledge_path = f"{project_root}/.ohspec/project-knowledge.json"
    
    # 1. 验证触发条件
    if not verify_extraction_conditions(rfc_dir, knowledge_path):
        print("提炼条件不满足，跳过提炼")
        return False
    
    # 2. 读取源文件
    with open(f"{rfc_dir}/findings.json", 'r') as f:
        findings = json.load(f)
    
    with open(f"{rfc_dir}/rfc.md", 'r') as f:
        rfc_content = f.read()
    
    with open(knowledge_path, 'r') as f:
        knowledge = json.load(f)
    
    # 3. 执行提炼
    print(f"开始从 {findings['meta']['rfc_id']} 提炼知识...")
    
    new_knowledge = {
        "patterns": {},
        "dfx_templates": {},
        "decisions": [],
        "constraints": {},
        "anti_patterns": []
    }
    
    # 3.1 提炼模式
    patterns = extract_patterns(rfc_content, findings, knowledge)
    for category, pattern_list in group_patterns_by_category(patterns).items():
        new_knowledge["patterns"][category] = pattern_list
    print(f"  提炼模式: {len(patterns)} 个")
    
    # 3.2 提炼 DFX 模板
    dfx_templates = extract_dfx_templates(rfc_content, findings, knowledge)
    new_knowledge["dfx_templates"] = dfx_templates
    print(f"  提炼 DFX 模板: {len(dfx_templates)} 个维度")
    
    # 3.3 提炼决策
    decisions = extract_decisions(rfc_content, findings, knowledge)
    new_knowledge["decisions"] = decisions
    print(f"  提炼决策: {len(decisions)} 个")
    
    # 3.4 提炼约束
    constraints = extract_constraints(findings, knowledge)
    new_knowledge["constraints"] = constraints
    print(f"  提炼约束: {len(constraints)} 个类型")
    
    # 4. 去重和合并
    knowledge = deduplicate_knowledge(new_knowledge, knowledge)
    
    # 5. 更新元数据
    knowledge["meta"]["updated_at"] = datetime.now().isoformat()
    knowledge["meta"]["last_extraction_rfc"] = findings["meta"]["rfc_id"]
    
    # 6. 写回知识库
    with open(knowledge_path, 'w') as f:
        json.dump(knowledge, f, ensure_ascii=False, indent=2)
    
    # 7. 记录提炼日志
    log_extraction(rfc_dir, findings["meta"]["rfc_id"], new_knowledge)
    
    print(f"知识提炼完成，已更新 {knowledge_path}")
    return True


def verify_extraction_conditions(rfc_dir: str, knowledge_path: str) -> bool:
    """验证提炼条件是否满足"""
    import json
    import os
    
    # 检查必要文件
    required_files = [
        f"{rfc_dir}/findings.json",
        f"{rfc_dir}/rfc.md",
        f"{rfc_dir}/progress.json",
        knowledge_path
    ]
    
    for filepath in required_files:
        if not os.path.exists(filepath):
            print(f"缺少必要文件: {filepath}")
            return False
    
    # 检查 RFC 状态
    with open(f"{rfc_dir}/progress.json", 'r') as f:
        progress = json.load(f)
    
    if progress.get("status") != "APPROVED":
        print(f"RFC 状态不是 APPROVED，当前状态: {progress.get('status')}")
        return False
    
    return True


def group_patterns_by_category(patterns: list[dict]) -> dict:
    """按类别分组模式"""
    grouped = {}
    for pattern in patterns:
        category = pattern.get("category", "other")
        if category not in grouped:
            grouped[category] = []
        grouped[category].append(pattern)
    return grouped


def log_extraction(rfc_dir: str, rfc_id: str, extracted_knowledge: dict):
    """记录提炼日志"""
    import json
    from datetime import datetime
    
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "rfc_id": rfc_id,
        "patterns_count": sum(len(p) for p in extracted_knowledge.get("patterns", {}).values()),
        "dfx_templates_count": len(extracted_knowledge.get("dfx_templates", {})),
        "decisions_count": len(extracted_knowledge.get("decisions", [])),
        "constraints_count": len(extracted_knowledge.get("constraints", {}))
    }
    
    progress_path = f"{rfc_dir}/progress.json"
    with open(progress_path, 'r') as f:
        progress = json.load(f)
    
    if "extraction_log" not in progress:
        progress["extraction_log"] = []
    
    progress["extraction_log"].append(log_entry)
    
    with open(progress_path, 'w') as f:
        json.dump(progress, f, ensure_ascii=False, indent=2)
```

### 与 Orchestrator 工作流的集成

在 Orchestrator 的审查完成后，自动调用提炼流程：

```python
def orchestrator_post_audit_workflow(rfc_dir: str, project_root: str, audit_result: dict):
    """
    审查完成后的 Orchestrator 工作流
    
    参数:
        rfc_dir: RFC 目录路径
        project_root: 项目根目录路径
        audit_result: 审查结果
    """
    import json
    
    # 1. 检查审查结果
    if audit_result.get("score", 0) < 80:
        print("审查评分不足 80 分，不执行提炼")
        return
    
    if audit_result.get("decision") != "APPROVED":
        print(f"RFC 未获批准，决策: {audit_result.get('decision')}")
        return
    
    # 2. 更新 RFC 状态
    progress_path = f"{rfc_dir}/progress.json"
    with open(progress_path, 'r') as f:
        progress = json.load(f)
    
    progress["status"] = "APPROVED"
    progress["approved_at"] = datetime.now().isoformat()
    
    with open(progress_path, 'w') as f:
        json.dump(progress, f, ensure_ascii=False, indent=2)
    
    # 3. 执行知识提炼
    success = extract_knowledge_from_rfc(rfc_dir, project_root)
    
    if success:
        print("RFC 已批准并完成知识提炼")
    else:
        print("知识提炼失败，请检查日志")
```

### 验收标准

- [x] 提炼规则清晰定义（4 个维度）
- [x] 触发条件明确（RFC 状态 = APPROVED）
- [x] 提供完整的提炼函数实现
- [x] 包含去重和合并机制
- [x] 与 project-knowledge.json 保持一致
- [x] 与 Orchestrator 工作流集成
- [x] 提供使用示例和日志记录
