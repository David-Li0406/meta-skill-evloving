# /ohspec:resume - 交互式恢复

## 命令说明
自动检测未完成的 RFC 项目，展示列表供用户选择，读取上下文并恢复到对应阶段继续工作。

## 使用方式
```bash
/ohspec:resume                              # 自动检测并选择
/ohspec:resume RFC-20240114-120000          # 直接恢复指定 RFC
/ohspec:resume RFC-20240114-120000 --restart  # 从头开始（忽略当前进度）
/ohspec:resume RFC-20240114-120000 --from-checkpoint  # 从检查点恢复
/ohspec:checkpoint RFC-20240114-120000      # 手动创建检查点
```

## 状态机定义

### 状态流转图
```
INIT → DISPATCHING → ANALYZING → DESIGNING → PRECHECKING → AUDITING → APPROVED
                         ↑            ↑            ↑             ↓
                         └────────────┴────────────┴─────────REJECTED
                                                                 ↓
                                                               INIT
```

### 状态说明
| 状态 | 说明 | 可转换到 |
|------|------|----------|
| INIT | 初始状态，RFC 刚创建 | DISPATCHING |
| DISPATCHING | 调度器分析需求复杂度 | ANALYZING |
| ANALYZING | 需求分析阶段 | DESIGNING, INIT（放弃） |
| DESIGNING | 方案设计阶段 | PRECHECKING, ANALYZING（退回） |
| PRECHECKING | 自动预检阶段 | AUDITING, DESIGNING（退回） |
| AUDITING | 质量审查阶段 | APPROVED, REJECTED, DESIGNING（退回） |
| APPROVED | 审批通过（终态） | - |
| REJECTED | 审批拒绝 | INIT（重新开始） |

### 状态转换规则
```python
STATE_TRANSITIONS = {
    "INIT": ["DISPATCHING"],
    "DISPATCHING": ["ANALYZING"],
    "ANALYZING": ["DESIGNING", "INIT"],
    "DESIGNING": ["PRECHECKING", "ANALYZING"],
    "PRECHECKING": ["AUDITING", "DESIGNING"],
    "AUDITING": ["APPROVED", "REJECTED", "DESIGNING"],
    "APPROVED": [],
    "REJECTED": ["INIT"]
}

def can_transition(current: str, target: str) -> bool:
    """检查状态转换是否合法"""
    return target in STATE_TRANSITIONS.get(current, [])
```

## 断点恢复逻辑

### 中断原因分类
| 原因 | 说明 | 恢复策略 |
|------|------|----------|
| user_abort | 用户主动中断 | resume_current |
| error | 执行错误（参考错误处理协议） | 根据错误级别决定 |
| timeout | 执行超时 | restart_state |
| context_lost | 上下文丢失 | rollback |

### 恢复策略
| 策略 | 说明 | 适用场景 |
|------|------|----------|
| resume_current | 从中断点继续 | 用户中断、L1/L2 错误 |
| restart_state | 重新执行当前状态 | 超时、L3 错误 |
| rollback | 回退到上一状态 | 上下文丢失、L4 错误 |

### 恢复决策流程
```python
def determine_recovery_strategy(checkpoint: dict) -> str:
    """根据中断信息决定恢复策略"""
    reason = checkpoint.get("interrupt_reason")
    attempts = checkpoint.get("recovery_attempts", 0)

    # 超过 3 次恢复尝试，强制回退
    if attempts >= 3:
        return "rollback"

    strategy_map = {
        "user_abort": "resume_current",
        "error": "restart_state",  # 具体根据错误级别调整
        "timeout": "restart_state",
        "context_lost": "rollback"
    }

    return strategy_map.get(reason, "restart_state")
```

### 状态恢复映射
```python
STATE_TO_WORKFLOW = {
    "INIT": "start",
    "DISPATCHING": "start",
    "ANALYZING": "analyze",
    "DESIGNING": "design",
    "PRECHECKING": "precheck",
    "AUDITING": "audit"
}

def get_resume_workflow(state: str) -> str:
    """获取状态对应的工作流命令"""
    return STATE_TO_WORKFLOW.get(state, "start")
```

## 工作流程

### 步骤1：检测未完成的 RFC
扫描所有 RFC，过滤出未完成的项目：

```python
import os
import re
from datetime import datetime

RFC_BASE_DIR = ".ohspec/rfcs"

def detect_incomplete_rfcs(limit=5):
    """检测未完成的 RFC 项目"""
    # 复用 list.md 的扫描逻辑
    from workflows.list import scan_rfcs

    all_rfcs = scan_rfcs()

    # 过滤未完成的 RFC（状态不是 APPROVED 或 REJECTED）
    incomplete_rfcs = [
        rfc for rfc in all_rfcs
        if rfc.get('status') not in ['APPROVED', 'REJECTED']
    ]

    # 按最后更新时间倒序排序
    incomplete_rfcs.sort(key=lambda x: x.get('last_updated', ''), reverse=True)

    # 限制显示数量
    if limit:
        incomplete_rfcs = incomplete_rfcs[:limit]

    return incomplete_rfcs
```

### 步骤2：展示 RFC 列表供用户选择
使用交互式界面让用户选择要恢复的 RFC：

```python
def show_resume_menu(rfcs):
    """展示恢复菜单"""
    if not rfcs:
        print("未找到未完成的 RFC 项目")
        print("\n💡 提示：使用 /ohspec:start 创建新的 RFC")
        return None

    print("\n📋 未完成的 RFC 项目（最近 5 个）\n")
    print("=" * 100)

    for idx, rfc in enumerate(rfcs, 1):
        rfc_id = rfc.get('rfc_id', 'N/A')
        title = rfc.get('title', 'N/A')
        status = rfc.get('status', 'N/A')
        phase = rfc.get('current_phase', 'N/A')
        progress = rfc.get('progress', 0)
        last_updated = rfc.get('last_updated', 'N/A')

        print(f"{idx}. {rfc_id}")
        print(f"   标题: {title}")
        print(f"   状态: {status} | 阶段: {phase} | 完成度: {progress}%")
        print(f"   最后更新: {last_updated}")
        print()

    print("=" * 100)
    print("\n请选择要恢复的 RFC（输入数字 1-{}）：".format(len(rfcs)))

    # 等待用户输入
    choice = input("> ")

    try:
        idx = int(choice) - 1
        if 0 <= idx < len(rfcs):
            return rfcs[idx]
        else:
            print("❌ 无效的选择")
            return None
    except ValueError:
        print("❌ 请输入数字")
        return None
```

### 步骤3：读取 RFC 上下文
读取选中 RFC 的所有相关文件，恢复上下文：

```python
def load_rfc_context(rfc_id):
    """加载 RFC 上下文"""
    rfc_dir = os.path.join(RFC_BASE_DIR, rfc_id)

    if not os.path.exists(rfc_dir):
        print(f"❌ RFC 目录不存在：{rfc_dir}")
        return None

    context = {
        'rfc_id': rfc_id,
        'rfc_dir': rfc_dir
    }

    # 读取 progress.json
    progress_file = os.path.join(rfc_dir, "progress.json")
    if os.path.exists(progress_file):
        with open(progress_file, 'r', encoding='utf-8') as f:
            context['progress'] = f.read()

        # 提取关键信息
        context['metadata'] = extract_metadata(progress_file)
    else:
        print(f"⚠️ 未找到 progress.json")

    # 读取 rfc.md
    rfc_file = os.path.join(rfc_dir, "rfc.md")
    if os.path.exists(rfc_file):
        with open(rfc_file, 'r', encoding='utf-8') as f:
            context['rfc'] = f.read()
    else:
        print(f"⚠️ 未找到 rfc.md")

    # 读取 findings.json
    findings_file = os.path.join(rfc_dir, "findings.json")
    if os.path.exists(findings_file):
        with open(findings_file, 'r', encoding='utf-8') as f:
            context['findings'] = f.read()
    else:
        print(f"⚠️ 未找到 findings.json")

    return context
```

### 步骤4：显示上下文摘要
向用户展示 RFC 的当前状态和上下文摘要：

```python
def show_context_summary(context):
    """显示上下文摘要"""
    metadata = context.get('metadata', {})

    print("\n" + "=" * 80)
    print("📄 RFC 上下文摘要")
    print("=" * 80)

    print(f"\nRFC ID: {metadata.get('rfc_id', 'N/A')}")
    print(f"标题: {metadata.get('title', 'N/A')}")
    print(f"用户需求: {metadata.get('user_requirement', 'N/A')}")
    print(f"\n当前状态: {metadata.get('status', 'N/A')}")
    print(f"当前阶段: {metadata.get('current_phase', 'N/A')}")
    print(f"完成度: {metadata.get('progress', 0)}%")
    print(f"最后更新: {metadata.get('last_updated', 'N/A')}")

    # 显示 5-Question Reboot Check
    print("\n## 5-Question Reboot Check")
    print("-" * 80)

    progress_content = context.get('progress', '')

    # 提取 5-Question Reboot Check 表格
    match = re.search(
        r'## 5-Question Reboot Check.*?\n(.*?)(?=\n##|\n---|$)',
        progress_content,
        re.DOTALL
    )

    if match:
        reboot_check = match.group(1).strip()
        print(reboot_check)
    else:
        print("（未找到 5-Question Reboot Check）")

    print("\n" + "=" * 80)
```

### 步骤5：基于状态机的恢复决策
根据状态机信息决定恢复策略：

```python
def execute_recovery(context: dict) -> tuple[str, str]:
    """
    基于状态机执行恢复决策
    返回：(恢复策略, 目标工作流)
    """
    progress = context.get('progress_data', {})
    state_machine = progress.get('state_machine', {})
    checkpoint = state_machine.get('checkpoint', {})

    current_state = state_machine.get('current_state', 'INIT')
    interrupted_state = checkpoint.get('interrupted_state')
    last_completed = checkpoint.get('last_completed_state')

    # 决定恢复策略
    strategy = determine_recovery_strategy(checkpoint)

    # 根据策略决定目标状态
    if strategy == "rollback":
        target_state = last_completed or "INIT"
    elif strategy == "restart_state":
        target_state = interrupted_state or current_state
    else:  # resume_current
        target_state = current_state

    # 获取对应工作流
    workflow = get_resume_workflow(target_state)

    return strategy, workflow

def record_state_transition(rfc_id: str, from_state: str, to_state: str, reason: str):
    """记录状态转换"""
    transition = {
        "from": from_state,
        "to": to_state,
        "reason": reason,
        "timestamp": datetime.now().isoformat()
    }
    # 追加到 progress.json 的 state_machine.transitions
    # ...
```

### 步骤6：选择恢复模式
让用户确认或调整恢复策略：

```python
def choose_resume_mode(context: dict) -> str:
    """选择恢复模式（基于状态机）"""
    progress = context.get('progress_data', {})
    state_machine = progress.get('state_machine', {})
    checkpoint = state_machine.get('checkpoint', {})

    current_state = state_machine.get('current_state', 'INIT')
    strategy, workflow = execute_recovery(context)

    print(f"\n当前状态: {current_state}")
    print(f"推荐恢复策略: {strategy}")
    print(f"目标工作流: /ohspec:{workflow}")

    if checkpoint.get('interrupt_reason'):
        print(f"中断原因: {checkpoint['interrupt_reason']}")
        print(f"恢复尝试次数: {checkpoint.get('recovery_attempts', 0)}")

    print("\n请选择恢复模式：")
    print(f"1. {strategy}（推荐）- 执行 /ohspec:{workflow}")
    print("2. 回退到上一状态")
    print("3. 从头开始（重置为 INIT）")

    choice = input("> ")

    if choice == "1":
        return workflow
    elif choice == "2":
        prev_state = state_machine.get('previous_state') or 'INIT'
        return get_resume_workflow(prev_state)
    elif choice == "3":
        return "start"
    else:
        print("无效选择，使用推荐策略")
        return workflow
```

### 步骤7：调用对应工作流
根据状态机执行恢复：

```python
def resume_workflow(rfc_id: str, workflow: str, context: dict) -> bool:
    """基于状态机恢复工作流"""
    progress = context.get('progress_data', {})
    state_machine = progress.get('state_machine', {})
    checkpoint = state_machine.get('checkpoint', {})

    # 更新恢复尝试次数
    checkpoint['recovery_attempts'] = checkpoint.get('recovery_attempts', 0) + 1

    # 记录状态转换
    current_state = state_machine.get('current_state', 'INIT')
    target_state = {
        'start': 'DISPATCHING',
        'analyze': 'ANALYZING',
        'design': 'DESIGNING',
        'precheck': 'PRECHECKING',
        'audit': 'AUDITING'
    }.get(workflow, 'INIT')

    # 验证状态转换合法性
    if not can_transition(current_state, target_state) and current_state != target_state:
        print(f"警告: 状态转换 {current_state} -> {target_state} 不合法")
        print("允许的转换:", STATE_TRANSITIONS.get(current_state, []))
        return False

    record_state_transition(rfc_id, current_state, target_state, "resume")

    print(f"\n恢复 RFC {rfc_id}")
    print(f"状态转换: {current_state} -> {target_state}")
    print(f"执行命令: /ohspec:{workflow} {rfc_id}\n")

    # 调用对应工作流
    workflow_map = {
        'start': f'/ohspec:start {rfc_id}',
        'analyze': f'/ohspec:analyze {rfc_id}',
        'design': f'/ohspec:design {rfc_id}',
        'precheck': f'/ohspec:precheck {rfc_id}',
        'audit': f'/ohspec:audit {rfc_id}'
    }

    cmd = workflow_map.get(workflow)
    if cmd:
        print(f"调用命令: {cmd}")
        return True
    else:
        print(f"未知工作流: {workflow}")
        return False
```

## 完整示例

### 基于状态机的恢复流程
```python
def resume_rfc(rfc_id: str = None, restart: bool = False):
    """基于状态机恢复 RFC 工作流"""

    # 1. 选择 RFC
    if not rfc_id:
        print("检测未完成的 RFC 项目...")
        incomplete_rfcs = detect_incomplete_rfcs(limit=5)
        selected_rfc = show_resume_menu(incomplete_rfcs)
        if not selected_rfc:
            return False
        rfc_id = selected_rfc.get('rfc_id')

    # 2. 加载上下文（包含状态机信息）
    context = load_rfc_context(rfc_id)
    if not context:
        return False

    show_context_summary(context)

    # 3. 基于状态机决定恢复策略
    if restart:
        # 强制重置状态机
        workflow = "start"
        reset_state_machine(rfc_id)
    else:
        workflow = choose_resume_mode(context)

    # 4. 执行恢复
    return resume_workflow(rfc_id, workflow, context)

def reset_state_machine(rfc_id: str):
    """重置状态机到初始状态"""
    # 更新 progress.json 中的 state_machine
    state_machine = {
        "current_state": "INIT",
        "previous_state": None,
        "transitions": [],
        "checkpoint": {
            "last_completed_state": None,
            "interrupted_state": None,
            "interrupt_reason": None,
            "interrupted_at": None,
            "recovery_strategy": None,
            "recovery_attempts": 0
        }
    }
    # 写入文件...
```

## 调用示例
```bash
# 自动检测并选择
/ohspec:resume

# 直接恢复指定 RFC
/ohspec:resume RFC-20240114-120000

# 从头开始（重置状态机）
/ohspec:resume RFC-20240114-120000 --restart
```

## 输出示例

### 自动检测模式
```
检测未完成的 RFC 项目...

📋 未完成的 RFC 项目（最近 5 个）

====================================================================================================
1. RFC-20240114-120000
   标题: 为音频服务增加3D音效开关
   状态: DESIGNING | 阶段: design | 完成度: 60%
   最后更新: 2024-01-14 12:30:00

2. RFC-20240112-090000
   标题: 优化内存管理
   状态: ANALYZING | 阶段: analyze | 完成度: 30%
   最后更新: 2024-01-12 09:30:00

====================================================================================================

请选择要恢复的 RFC（输入数字 1-2）：
> 1

================================================================================
📄 RFC 上下文摘要
================================================================================

RFC ID: RFC-20240114-120000
标题: 为音频服务增加3D音效开关
用户需求: 为音频服务增加3D音效开关

当前状态: DESIGNING
当前阶段: design
完成度: 60%
最后更新: 2024-01-14 12:30:00

## 5-Question Reboot Check
--------------------------------------------------------------------------------
| 问题 | 答案 |
|------|------|
| 我在哪里？ | Phase 2: 方案设计 |
| 我要去哪里？ | Phase 3: 质量审查 |
| 目标是什么？ | 为音频服务增加3D音效开关 |
| 我学到了什么？ | 找到 5 个相关文件，2 种实现模式 |
| 我做了什么？ | 完成代码扫描、用户访谈、需求分析 |

================================================================================

请选择恢复模式：
1. 继续当前阶段（推荐）
2. 从头开始（重新执行 analyze 阶段）
> 1

🚀 恢复 RFC RFC-20240114-120000，阶段：design

调用命令：/ohspec:design RFC-20240114-120000
```

### 直接恢复模式
```
恢复 RFC：RFC-20240114-120000

================================================================================
📄 RFC 上下文摘要
================================================================================

RFC ID: RFC-20240114-120000
标题: 为音频服务增加3D音效开关
用户需求: 为音频服务增加3D音效开关

当前状态: DESIGNING
当前阶段: design
完成度: 60%
最后更新: 2024-01-14 12:30:00

...

🚀 恢复 RFC RFC-20240114-120000，阶段：design

调用命令：/ohspec:design RFC-20240114-120000
```

## 输出物
- 控制台输出：RFC 列表、上下文摘要、恢复提示
- 自动调用对应工作流（analyze/design/audit）

## 错误处理
- 无未完成的 RFC → 提示使用 /ohspec:start 创建新 RFC
- RFC 目录不存在 → 提示 RFC ID 无效
- progress.json 文件损坏 → 提示无法恢复，建议从头开始
- 用户输入无效 → 提示重新输入

## 依赖关系
- 依赖 `workflows/list.md` 的 RFC 扫描逻辑（`scan_rfcs` 函数）
- 依赖 `workflows/analyze.md`、`workflows/design.md`、`workflows/audit.md` 的工作流执行逻辑

## 集成建议

### 与工作锁机制集成
在恢复 RFC 前，检查是否存在工作锁：

```python
def check_work_lock():
    """检查工作锁"""
    lock_file = ".ohspec/.current-rfc"

    if os.path.exists(lock_file):
        with open(lock_file, 'r', encoding='utf-8') as f:
            lock_content = f.read()

        print("⚠️ 检测到未完成的工作：")
        print(lock_content)
        print("\n是否继续？（y/n）")

        choice = input("> ")
        if choice.lower() != 'y':
            return False

    return True
```

### 与 start 工作流集成
在 `start.md` 中添加恢复提示：

```python
# 在 start.md 的开始处
incomplete_rfcs = detect_incomplete_rfcs(limit=3)

if incomplete_rfcs:
    print("💡 检测到未完成的 RFC 项目：")
    for rfc in incomplete_rfcs:
        print(f"  - {rfc['rfc_id']}: {rfc['title']}")

    print("\n是否恢复现有 RFC？（y/n）")
    choice = input("> ")

    if choice.lower() == 'y':
        resume_rfc()
        return
```

## 扩展功能（未来版本）

### 批量恢复
```bash
/ohspec:resume --all  # 恢复所有未完成的 RFC（按顺序）
```

### 恢复到指定阶段
```bash
/ohspec:resume RFC-20240114-120000 --phase=audit  # 跳到 audit 阶段
```

### 恢复历史记录
```bash
/ohspec:resume --history  # 显示最近恢复的 RFC 历史
```

## 检查点与恢复机制（P2-7）

### 检查点触发条件

检查点在以下三种情况下自动创建：

| 触发条件 | 说明 | 优先级 |
|---------|------|--------|
| 阶段完成 | 当 phase.status 从 pending/in_progress 变为 completed | 高 |
| Token 70% | 当 token_usage.usage_ratio >= 0.70（橙色预警） | 高 |
| 用户请求 | 通过 `/ohspec:checkpoint RFC-ID` 命令手动创建 | 中 |

### 检查点创建逻辑

```python
import hashlib
import json
import os
from datetime import datetime

CHECKPOINTS_DIR = ".ohspec/checkpoints"

def create_checkpoint(rfc_id: str, trigger_reason: str, phase: str = None) -> bool:
    """
    创建检查点快照

    参数：
        rfc_id: RFC 标识
        trigger_reason: 触发原因（phase_completed | token_threshold | user_request）
        phase: 当前阶段

    返回：
        True 表示创建成功，False 表示失败
    """
    try:
        rfc_dir = os.path.join(".ohspec/rfcs", rfc_id)

        # 1. 读取当前状态
        progress_file = os.path.join(rfc_dir, "progress.json")
        findings_file = os.path.join(rfc_dir, "findings.json")
        rfc_file = os.path.join(rfc_dir, "rfc.md")

        if not os.path.exists(progress_file):
            print(f"❌ progress.json 不存在：{progress_file}")
            return False

        with open(progress_file, 'r', encoding='utf-8') as f:
            progress_data = json.load(f)

        with open(findings_file, 'r', encoding='utf-8') as f:
            findings_data = json.load(f)

        # 2. 计算文件校验和
        def calculate_checksum(file_path: str) -> str:
            """计算文件 SHA-256 校验和（前 8 位）"""
            if not os.path.exists(file_path):
                return "N/A"

            sha256_hash = hashlib.sha256()
            with open(file_path, "rb") as f:
                for byte_block in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(byte_block)
            return sha256_hash.hexdigest()[:8]

        # 3. 构建检查点数据
        checkpoint_data = {
            "meta": {
                "rfc_id": rfc_id,
                "created_at": datetime.now().isoformat(),
                "trigger_reason": trigger_reason,
                "phase": phase or progress_data.get("current", {}).get("phase", "unknown"),
                "version": "1.0"
            },
            "state_snapshot": {
                "current_state": progress_data.get("state_machine", {}).get("current_state", "INIT"),
                "previous_state": progress_data.get("state_machine", {}).get("previous_state"),
                "last_completed_state": progress_data.get("state_machine", {}).get("checkpoint", {}).get("last_completed_state"),
                "recent_transitions": progress_data.get("state_machine", {}).get("transitions", [])[-10:]
            },
            "context_snapshot": {
                "l0_metadata": {
                    "requirement": findings_data.get("requirement", {}).get("original", ""),
                    "intent": findings_data.get("requirement", {}).get("intent", ""),
                    "complexity": findings_data.get("dispatcher", {}).get("complexity", "unknown"),
                    "keywords": findings_data.get("requirement", {}).get("keywords", [])
                },
                "l1_decisions": {
                    "decisions": findings_data.get("confirmed", {}).get("decisions", []),
                    "constraints": findings_data.get("confirmed", {}).get("constraints", {}),
                    "key_files": findings_data.get("confirmed", {}).get("key_files", [])
                },
                "l2_dependencies": {
                    "internal": findings_data.get("confirmed", {}).get("dependencies", {}).get("internal", []),
                    "external": findings_data.get("confirmed", {}).get("dependencies", {}).get("external", []),
                    "integration_points": findings_data.get("confirmed", {}).get("dependencies", {}).get("integration_points", [])
                }
            },
            "file_checksums": {
                "rfc_md": {
                    "path": rfc_file,
                    "checksum": calculate_checksum(rfc_file),
                    "size": os.path.getsize(rfc_file) if os.path.exists(rfc_file) else 0,
                    "modified_at": datetime.fromtimestamp(os.path.getmtime(rfc_file)).isoformat() if os.path.exists(rfc_file) else None
                },
                "findings_json": {
                    "path": findings_file,
                    "checksum": calculate_checksum(findings_file),
                    "size": os.path.getsize(findings_file) if os.path.exists(findings_file) else 0,
                    "modified_at": datetime.fromtimestamp(os.path.getmtime(findings_file)).isoformat() if os.path.exists(findings_file) else None
                },
                "progress_json": {
                    "path": progress_file,
                    "checksum": calculate_checksum(progress_file),
                    "size": os.path.getsize(progress_file) if os.path.exists(progress_file) else 0,
                    "modified_at": datetime.fromtimestamp(os.path.getmtime(progress_file)).isoformat() if os.path.exists(progress_file) else None
                }
            },
            "token_snapshot": {
                "current_tokens": progress_data.get("token_usage", {}).get("current", 0),
                "usage_ratio": progress_data.get("token_usage", {}).get("usage_ratio", 0.0),
                "alert_level": progress_data.get("token_usage", {}).get("alert_level", "none"),
                "by_phase": progress_data.get("observability", {}).get("token_metrics", {}).get("by_phase", {})
            },
            "recovery_guide": {
                "recommended_strategy": determine_recovery_strategy(progress_data.get("state_machine", {}).get("checkpoint", {})),
                "steps": [
                    {
                        "step": 1,
                        "action": "验证检查点完整性",
                        "command": "验证 file_checksums 中所有文件的校验和"
                    },
                    {
                        "step": 2,
                        "action": "恢复上下文",
                        "command": "加载 context_snapshot 中的 L0 和 L1 信息"
                    },
                    {
                        "step": 3,
                        "action": "恢复状态机",
                        "command": f"设置 state_machine.current_state 为 {progress_data.get('state_machine', {}).get('current_state', 'INIT')}"
                    },
                    {
                        "step": 4,
                        "action": "执行恢复工作流",
                        "command": f"/ohspec:resume {rfc_id} --from-checkpoint"
                    }
                ],
                "resume_command": f"/ohspec:resume {rfc_id} --from-checkpoint",
                "fallback_options": [
                    {
                        "option": 1,
                        "description": "重新执行当前阶段",
                        "command": f"/ohspec:{phase or 'analyze'} {rfc_id} --restart"
                    },
                    {
                        "option": 2,
                        "description": "回退到上一阶段",
                        "command": f"/ohspec:resume {rfc_id} --rollback"
                    },
                    {
                        "option": 3,
                        "description": "从头开始",
                        "command": f"/ohspec:resume {rfc_id} --restart"
                    }
                ]
            },
            "validation": {
                "checkpoint_checksum": None,  # 将在下面计算
                "status": "valid",
                "validated_at": datetime.now().isoformat(),
                "required_fields_check": {
                    "meta": True,
                    "state_snapshot": True,
                    "context_snapshot": True,
                    "file_checksums": True,
                    "recovery_guide": True
                },
                "ttl_hours": 24,
                "expires_at": None  # 将在下面计算
            },
            "notes": {
                "reason": f"检查点由 {trigger_reason} 触发",
                "progress": f"{progress_data.get('meta', {}).get('completion', 0)}%",
                "pending_issues": findings_data.get("issues", [])[:5],
                "next_steps": []
            }
        }

        # 4. 计算检查点校验和
        checkpoint_json_str = json.dumps(checkpoint_data, ensure_ascii=False, sort_keys=True)
        checkpoint_checksum = hashlib.sha256(checkpoint_json_str.encode()).hexdigest()[:8]
        checkpoint_data["validation"]["checkpoint_checksum"] = checkpoint_checksum

        # 5. 计算过期时间
        from datetime import timedelta
        expires_at = datetime.now() + timedelta(hours=24)
        checkpoint_data["validation"]["expires_at"] = expires_at.isoformat()

        # 6. 保存检查点
        checkpoint_dir = os.path.join(CHECKPOINTS_DIR, rfc_id)
        os.makedirs(checkpoint_dir, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        checkpoint_file = os.path.join(checkpoint_dir, f"checkpoint-{timestamp}.json")

        with open(checkpoint_file, 'w', encoding='utf-8') as f:
            json.dump(checkpoint_data, f, ensure_ascii=False, indent=2)

        # 7. 更新 progress.json 中的检查点引用
        progress_data["token_usage"]["checkpoint"] = {
            "created_at": checkpoint_data["meta"]["created_at"],
            "phase": checkpoint_data["meta"]["phase"],
            "rfc_sections_completed": [
                phase for phase in ["dispatcher", "analyze", "design", "precheck", "audit"]
                if progress_data.get("phases", {}).get(phase, {}).get("status") == "completed"
            ],
            "checkpoint_file": checkpoint_file
        }

        with open(progress_file, 'w', encoding='utf-8') as f:
            json.dump(progress_data, f, ensure_ascii=False, indent=2)

        print(f"✅ 检查点创建成功")
        print(f"   位置: {checkpoint_file}")
        print(f"   校验和: {checkpoint_checksum}")
        print(f"   触发原因: {trigger_reason}")
        print(f"   过期时间: {checkpoint_data['validation']['expires_at']}")

        return True

    except Exception as e:
        print(f"❌ 创建检查点失败: {str(e)}")
        return False
```

### 检查点恢复逻辑

```python
def restore_from_checkpoint(rfc_id: str, checkpoint_file: str = None) -> bool:
    """
    从检查点恢复上下文和状态

    参数：
        rfc_id: RFC 标识
        checkpoint_file: 检查点文件路径（如果为 None，使用最新的检查点）

    返回：
        True 表示恢复成功，False 表示失败
    """
    try:
        # 1. 查找检查点文件
        if not checkpoint_file:
            checkpoint_dir = os.path.join(CHECKPOINTS_DIR, rfc_id)
            if not os.path.exists(checkpoint_dir):
                print(f"❌ 检查点目录不存在：{checkpoint_dir}")
                return False

            # 获取最新的检查点
            checkpoint_files = sorted([
                f for f in os.listdir(checkpoint_dir)
                if f.startswith("checkpoint-") and f.endswith(".json")
            ], reverse=True)

            if not checkpoint_files:
                print(f"❌ 未找到检查点文件")
                return False

            checkpoint_file = os.path.join(checkpoint_dir, checkpoint_files[0])

        # 2. 读取检查点
        with open(checkpoint_file, 'r', encoding='utf-8') as f:
            checkpoint_data = json.load(f)

        # 3. 验证检查点完整性
        validation = checkpoint_data.get("validation", {})

        # 检查过期时间
        expires_at = datetime.fromisoformat(validation.get("expires_at", ""))
        if datetime.now() > expires_at:
            print(f"⚠️ 检查点已过期（过期时间：{validation['expires_at']}）")
            print(f"   建议使用 /ohspec:resume {rfc_id} --rollback 回退到上一阶段")
            return False

        # 验证文件校验和
        rfc_dir = os.path.join(".ohspec/rfcs", rfc_id)
        file_checksums = checkpoint_data.get("file_checksums", {})

        print("\n验证文件完整性...")
        for file_key, file_info in file_checksums.items():
            file_path = file_info.get("path")
            expected_checksum = file_info.get("checksum")

            if not os.path.exists(file_path):
                print(f"⚠️ 文件不存在：{file_path}")
                continue

            actual_checksum = calculate_checksum(file_path)
            if actual_checksum != expected_checksum:
                print(f"⚠️ 文件已修改：{file_path}")
                print(f"   预期校验和：{expected_checksum}")
                print(f"   实际校验和：{actual_checksum}")

        # 4. 恢复上下文
        print("\n恢复上下文...")

        # 恢复 L0 元数据
        l0_metadata = checkpoint_data.get("context_snapshot", {}).get("l0_metadata", {})
        print(f"  需求：{l0_metadata.get('requirement', 'N/A')[:50]}...")
        print(f"  复杂度：{l0_metadata.get('complexity', 'N/A')}")

        # 恢复 L1 决策
        l1_decisions = checkpoint_data.get("context_snapshot", {}).get("l1_decisions", {})
        decisions = l1_decisions.get("decisions", [])
        print(f"  已确认决策数：{len(decisions)}")

        # 5. 恢复状态机
        print("\n恢复状态机...")
        state_snapshot = checkpoint_data.get("state_snapshot", {})
        current_state = state_snapshot.get("current_state", "INIT")
        print(f"  当前状态：{current_state}")

        # 6. 更新 progress.json
        progress_file = os.path.join(rfc_dir, "progress.json")
        with open(progress_file, 'r', encoding='utf-8') as f:
            progress_data = json.load(f)

        # 记录检查点恢复
        progress_data["state_machine"]["checkpoint"]["recovery_strategy"] = "from_checkpoint"
        progress_data["state_machine"]["checkpoint"]["recovery_attempts"] = \
            progress_data["state_machine"]["checkpoint"].get("recovery_attempts", 0) + 1

        with open(progress_file, 'w', encoding='utf-8') as f:
            json.dump(progress_data, f, ensure_ascii=False, indent=2)

        print(f"\n✅ 检查点恢复成功")
        print(f"   RFC ID：{rfc_id}")
        print(f"   当前状态：{current_state}")
        print(f"   恢复策略：{checkpoint_data.get('recovery_guide', {}).get('recommended_strategy', 'N/A')}")

        return True

    except Exception as e:
        print(f"❌ 恢复检查点失败：{str(e)}")
        return False

def calculate_checksum(file_path: str) -> str:
    """计算文件 SHA-256 校验和（前 8 位）"""
    if not os.path.exists(file_path):
        return "N/A"

    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()[:8]
```

### 检查点触发集成

在各个阶段完成时自动创建检查点：

```python
# 在 workflows/analyze.md、design.md、precheck.md、audit.md 中集成

def on_phase_completed(rfc_id: str, phase: str):
    """阶段完成时的回调"""
    # 1. 更新 progress.json
    # ...

    # 2. 创建检查点
    create_checkpoint(
        rfc_id=rfc_id,
        trigger_reason="phase_completed",
        phase=phase
    )

    # 3. 继续下一阶段
    # ...

def on_token_threshold_reached(rfc_id: str, usage_ratio: float):
    """Token 使用达到阈值时的回调"""
    if usage_ratio >= 0.70:  # 橙色预警
        print(f"🟠 Token 使用达到 {usage_ratio*100:.1f}%，创建检查点...")
        create_checkpoint(
            rfc_id=rfc_id,
            trigger_reason="token_threshold",
            phase=get_current_phase(rfc_id)
        )
```

### 检查点管理命令

```python
def list_checkpoints(rfc_id: str):
    """列出指定 RFC 的所有检查点"""
    checkpoint_dir = os.path.join(CHECKPOINTS_DIR, rfc_id)

    if not os.path.exists(checkpoint_dir):
        print(f"未找到检查点目录：{checkpoint_dir}")
        return

    checkpoint_files = sorted([
        f for f in os.listdir(checkpoint_dir)
        if f.startswith("checkpoint-") and f.endswith(".json")
    ], reverse=True)

    if not checkpoint_files:
        print(f"未找到 {rfc_id} 的检查点")
        return

    print(f"\n📋 {rfc_id} 的检查点列表\n")
    print("=" * 80)

    for idx, checkpoint_file in enumerate(checkpoint_files, 1):
        checkpoint_path = os.path.join(checkpoint_dir, checkpoint_file)
        with open(checkpoint_path, 'r', encoding='utf-8') as f:
            checkpoint_data = json.load(f)

        meta = checkpoint_data.get("meta", {})
        validation = checkpoint_data.get("validation", {})

        print(f"{idx}. {checkpoint_file}")
        print(f"   创建时间：{meta.get('created_at', 'N/A')}")
        print(f"   触发原因：{meta.get('trigger_reason', 'N/A')}")
        print(f"   阶段：{meta.get('phase', 'N/A')}")
        print(f"   状态：{validation.get('status', 'N/A')}")
        print(f"   过期时间：{validation.get('expires_at', 'N/A')}")
        print()

    print("=" * 80)

def cleanup_expired_checkpoints(rfc_id: str = None):
    """清理过期的检查点"""
    checkpoint_base_dir = CHECKPOINTS_DIR

    if rfc_id:
        checkpoint_dirs = [os.path.join(checkpoint_base_dir, rfc_id)]
    else:
        checkpoint_dirs = [
            os.path.join(checkpoint_base_dir, d)
            for d in os.listdir(checkpoint_base_dir)
            if os.path.isdir(os.path.join(checkpoint_base_dir, d))
        ]

    total_removed = 0

    for checkpoint_dir in checkpoint_dirs:
        if not os.path.exists(checkpoint_dir):
            continue

        for checkpoint_file in os.listdir(checkpoint_dir):
            if not checkpoint_file.endswith(".json"):
                continue

            checkpoint_path = os.path.join(checkpoint_dir, checkpoint_file)

            try:
                with open(checkpoint_path, 'r', encoding='utf-8') as f:
                    checkpoint_data = json.load(f)

                validation = checkpoint_data.get("validation", {})
                expires_at = datetime.fromisoformat(validation.get("expires_at", ""))

                if datetime.now() > expires_at:
                    os.remove(checkpoint_path)
                    print(f"✅ 已删除过期检查点：{checkpoint_path}")
                    total_removed += 1
            except Exception as e:
                print(f"⚠️ 处理检查点失败：{checkpoint_path}，错误：{str(e)}")

    print(f"\n总共删除 {total_removed} 个过期检查点")
```

## 下一步
- 恢复后自动执行对应阶段的工作流
- 完成后更新 progress.json 和工作锁
