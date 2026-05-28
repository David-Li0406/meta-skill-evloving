# /ohspec:precheck - 自动预检

## 命令说明
在人工审查前自动检查 RFC 的结构完整性、场景覆盖和 DFX 清单，提前发现问题并给出修改建议。

## 使用方式
```bash
/ohspec:precheck RFC-20240112-014500
```

## 强制：优先使用可执行预检脚本（避免“门禁只停留在文档”）

> 预期行为：脚本产出明确的 PASS/FAIL、问题列表与修复建议，并可选择写入 `progress.json.phases.precheck`。

推荐（写报告 + 更新 progress）：
```bash
# Linux/macOS（通常是 python3）
python3 .ohspec/scripts/precheck_rfc.py RFC-... --write-report --update-progress

# Windows（可能只有 python；如有 Python Launcher 可用 py -3）
python .ohspec/scripts/precheck_rfc.py RFC-... --write-report --update-progress
py -3 .ohspec/scripts/precheck_rfc.py RFC-... --write-report --update-progress
```

严格模式（建议用于 COMPLEX，warnings 也视为阻断）：
```bash
python3 .ohspec/scripts/precheck_rfc.py RFC-... --strict --write-report --update-progress
```

说明：
- 推荐把脚本落在项目目录 `.ohspec/scripts/`，保证跨仓/跨环境可执行（见主流程的“初始化/落盘一致性”要求）。
- 若项目里还没有这些脚本/模板，可先执行一次 bootstrap（从 skill 拷贝到项目）：
  - `python3 ~/.codex/skills/ohspec/scripts/bootstrap_project.py --project-root <repo>`
  - 或 `python3 ~/.claude/skills/ohspec/scripts/bootstrap_project.py --project-root <repo>`
- **若脚本 FAIL（退出码非 0）**：必须阻断后续 audit/approve；进入 auto-fix 或退回补齐。

## 预检流程

### 步骤0：自动修复集成（新增）

在执行预检前，启用自动修复反馈循环：

```
precheck → 发现问题 → 判断是否可自动修复
├─ 可修复 → 调用 auto-fix → 验证 → 通过/重试（最多 3 次）
└─ 不可修复 → 生成报告 → 需要人工干预
```

**可自动修复的问题类型**：
1. 格式错误（场景标题、GIVEN/WHEN/THEN 格式）
2. 缺失章节（DFX 8 个维度）
3. 模糊描述（性能、权限、异常处理等）
4. 场景覆盖不全（缺少异常/边界场景）

**重试预算**：最多 3 次自动修复尝试，超过则报告用户

详细说明见 [workflows/auto-fix.md](auto-fix.md)

### 步骤1：结构完整性检查
验证 RFC 是否包含所有必需章节：

| 章节 | 必需 | 检查内容 |
|------|------|---------|
| §1.上下文 | ✅ | 元数据、背景、利益相关方 |
| §2.需求 | ✅ | 功能需求、约束条件 |
| §3.契约 | ✅ | 接口契约表、对齐与变更矩阵、场景规格 |
| §4.DFX约束 | ✅ | 8个维度（安全、可靠性、性能、可测试性、可观测性、可维护性、兼容性、可运维性） |
| §5.设计决策 | ✅ | ADR、交互流程、状态机、算法描述 |

**新增结构要求（需求化设计）**：
- ✅ 场景概览（需求层，快速审查覆盖面）
- ✅ 项目事实（scan-of-record，事实+证据锚点）
- ✅ 背景包含范围/排除项
- ✅ 对齐与变更矩阵（existing_ref 或 new_change_plan 必须二选一）
- ✅ 依赖影响矩阵（依赖方/失败模式/回退/观测/影响范围）
- ✅ 异常与边界矩阵（异常/边界/错误码/降级/时序）
- ✅ 测试矩阵（场景→用例→验收指标，含依赖故障注入与兼容回归）
- ✅ 追溯矩阵（需求→场景→测试闭环）

**补充提醒（warning）**：
- ⚠️ 审查速览包含成功指标/业务收益
- ⚠️ 可运维性明确灰度/开关策略（如适用）
- ⚠️ 如涉及跨团队/陌生术语，补充术语/缩写表

**上下文收集验证（自动检查）**：
```python
def check_findings_quality(findings_path):
    """检查 findings.json 是否包含足够的上下文信息"""
    with open(findings_path, "r", encoding="utf-8") as f:
        findings = json.load(f)

    key_files = findings.get("confirmed", {}).get("key_files", [])
    if len(key_files) < 3:
        return {
            "status": "error",
            "message": f"❌ key_files 仅 {len(key_files)} 个，至少需要 3 个",
            "suggestion": "请扩大代码扫描范围，并补齐入口/配置/依赖等关键锚点"
        }

    def normalize_role(role: str) -> str:
        return (role or "").strip().lower()

    def derive_role_from_path(path: str) -> str:
        p = (path or "").lower()
        if any(k in p for k in ["config", "setting", "prefs", "state", "store", "db", "schema", "kv"]):
            return "config"
        if any(k in p for k in ["client", "adapter", "driver", "rpc", "grpc", "http", "integration", "external"]):
            return "dependency"
        if any(k in p for k in ["test", "tests", "e2e", "integration_test", "unit_test"]):
            return "test"
        if any(k in p for k in ["log", "metric", "trace", "telemetry", "monitor"]):
            return "observability"
        if any(k in p for k in ["handler", "controller", "service", "api", "endpoint", "cli", "main"]):
            return "entry"
        return ""

    role_groups = {
        "entry": {"entry", "入口", "handler", "controller", "service", "api", "endpoint", "flow", "core"},
        "config": {"config", "settings", "state", "storage", "db", "schema", "prefs", "kv"},
        "dependency": {"dependency", "integration", "adapter", "client", "driver", "external", "sdk"},
        "test": {"test", "tests", "e2e", "integration-test", "unit-test"},
        "observability": {"observability", "log", "metric", "trace", "telemetry", "monitor"}
    }

    covered = set()
    for item in key_files:
        if isinstance(item, dict):
            path = item.get("path", "")
            role = normalize_role(item.get("role", ""))
        else:
            path = str(item)
            role = ""
        if not role:
            role = derive_role_from_path(path)
        for group, aliases in role_groups.items():
            if role in aliases:
                covered.add(group)
                break

    if "entry" not in covered or "config" not in covered or len(covered) < 3:
        return {
            "status": "error",
            "message": f"❌ key_files 覆盖面不足（当前: {sorted(list(covered))}）",
            "suggestion": "请补齐入口/配置/依赖(或测试/可观测)等覆盖面，并标注 role"
        }

    # 项目事实（scan-of-record）：SIMPLE 至少 1 条；MEDIUM/COMPLEX 建议 ≥3
    complexity = (findings.get("dispatcher", {}).get("complexity") or "").upper()
    min_facts = 1 if complexity == "SIMPLE" else 3
    facts = findings.get("confirmed", {}).get("facts", [])
    if not isinstance(facts, list) or len(facts) < min_facts:
        return {
            "status": "error",
            "message": f"❌ confirmed.facts 不足（当前: {0 if not isinstance(facts, list) else len(facts)}），要求 ≥ {min_facts}",
            "suggestion": "请提炼配置/存储/权限/错误码/线程模型/可观测等项目事实，并为每条附证据锚点"
        }

    for f in facts:
        if isinstance(f, dict):
            ev = f.get("evidence") or []
            if not ev:
                return {
                    "status": "error",
                    "message": "❌ 项目事实缺少证据锚点（evidence 为空）",
                    "suggestion": "为每条事实补充 repo@rev:path#Lline 证据锚点"
                }

    # 多仓时：锚点必须可复现（repo@rev:path#Lline）
    repos = findings.get("meta", {}).get("repos", [])
    if isinstance(repos, list) and len(repos) > 1:
        bad = []
        for item in key_files:
            path = item.get("path", "") if isinstance(item, dict) else str(item)
            if "@" not in path or "#L" not in path:
                bad.append(path)
        if bad:
            return {
                "status": "error",
                "message": "❌ 多仓锚点格式不规范（需 repo@rev:path#Lline）",
                "suggestion": "请补齐 Repo Manifest，并将 key_files/existing_ref 统一为 repo@rev:path#Lline"
            }

    # 未决问题不得进入审查阶段
    working = findings.get("working", {})
    if working.get("pending_questions") or working.get("pending_options"):
        return {
            "status": "error",
            "message": "❌ 未决问题/选项未清零，禁止进入审查",
            "suggestion": "先完成澄清与选择，再进入审查"
        }

    return {"status": "ok"}
```

**对齐与变更矩阵验证（自动检查）**：
```python
def check_alignment_matrix(rfc_content):
    """
    对齐与变更矩阵必须存在，且每条变更满足：
    - existing_ref（现有实现锚点）
      或
    - new_change_plan（新增落地点 + 兼容/迁移 + 测试/回滚）
    """
    if "对齐与变更矩阵" not in rfc_content:
        return ["❌ 缺少对齐与变更矩阵"]

    # 规则示例：矩阵行中必须出现 existing_ref 或 new_change_plan
    lines = [l for l in rfc_content.splitlines() if "|" in l]
    missing = []
    for line in lines:
        if "existing_ref" in line or "new_change_plan" in line:
            continue
        # 只对矩阵区域做严格检查
    if not lines:
        missing.append("❌ 对齐与变更矩阵为空")
    return missing
```

**开发者模型检查（新增）**：
```python
def check_developer_model(rfc_content):
    if "开发者模型与易用性" not in rfc_content:
        return ["❌ 缺少开发者模型与易用性说明"]
    return []
```

**审查速览检查（新增）**：
```python
def check_review_digest(rfc_content):
    if "审查速览" not in rfc_content:
        return ["❌ 缺少审查速览（人审查优先）"]
    return []
```

**项目事实检查（新增）**：
```python
def check_project_facts(rfc_content):
    if "项目事实" not in rfc_content and "scan-of-record" not in rfc_content:
        return ["❌ 缺少项目事实（scan-of-record）"]
    if "FACT-ID" not in rfc_content:
        return ["❌ 项目事实缺少 FACT-ID 表格（需事实+证据锚点）"]
    return []
```

**场景概览检查（新增）**：
```python
def check_scenario_overview(rfc_content):
    if "场景概览" not in rfc_content:
        return ["❌ 缺少场景概览（需求层）"]
    return []
```

**追溯矩阵检查（新增）**：
```python
def check_traceability_matrix(rfc_content):
    if "追溯矩阵" not in rfc_content:
        return ["❌ 缺少追溯矩阵（需求→场景→测试）"]
    return []
```

**ID 规范与断链检查（新增，机器可读性门禁）**：
```python
ID_PATTERNS = {
    "REQ": r"\bREQ-\d{3}\b",
    "SCN": r"\bSCN-\d{3}\b",
    "API": r"\bAPI-\d{3}\b",
    "FIELD": r"\bFIELD-\d{3}\b",
    "CHG": r"\bCHG-\d{3}\b",
    "EDGE": r"\bEDGE-\d{3}\b",
    "DEP": r"\bDEP-\d{3}\b",
    "TST": r"\bTST-\d{3}\b"
}

def collect_ids(rfc_content: str) -> dict:
    ids = {}
    for k, pat in ID_PATTERNS.items():
        ids[k] = sorted(set(re.findall(pat, rfc_content)))
    return ids

def check_id_norms_and_links(rfc_content: str) -> list:
    """
    目标：
    - 关键实体必须有稳定 ID（便于后续 Agent 消费与跨版本追溯）
    - 追溯矩阵不得引用不存在的 ID（断链视为缺口）
    """
    errors = []
    ids = collect_ids(rfc_content)

    # 至少要求：REQ/SCN/CHG/TST 存在（否则无法闭环）
    required_groups = ["REQ", "SCN", "CHG", "TST"]
    for g in required_groups:
        if not ids.get(g):
            errors.append(f"❌ 缺少 {g}-ID（请使用 {g}-001 形式编号）")

    # 断链检查：追溯矩阵引用必须存在
    # 简化实现：提取追溯矩阵区域的行，检查每列 ID 是否在集合内
    trace_lines = []
    in_trace = False
    for line in rfc_content.splitlines():
        if "追溯矩阵" in line:
            in_trace = True
            continue
        if in_trace and line.strip().startswith("|"):
            trace_lines.append(line)
        if in_trace and line.strip() == "" and trace_lines:
            break

    # 跳过表头/分隔行
    for line in trace_lines:
        if "---" in line:
            continue
        cols = [c.strip() for c in line.strip("|").split("|")]
        if len(cols) < 3:
            continue
        req, scn, tst = cols[0], cols[1], cols[2]
        if req.startswith("REQ-") and req not in ids.get("REQ", []):
            errors.append(f"❌ 追溯矩阵断链：{req} 未定义")
        if scn.startswith("SCN-") and scn not in ids.get("SCN", []):
            errors.append(f"❌ 追溯矩阵断链：{scn} 未定义")
        if tst.startswith("TST-") and tst not in ids.get("TST", []):
            errors.append(f"❌ 追溯矩阵断链：{tst} 未定义")

    return errors
```

**Repo Manifest 检查（新增，多仓适用）**：
```python
def check_repo_manifest(rfc_content, findings):
    repos = findings.get("meta", {}).get("repos", [])
    if isinstance(repos, list) and len(repos) > 1:
        if "Repo Manifest" not in rfc_content:
            return ["❌ 多仓任务缺少 Repo Manifest"]
    return []
```

### 步骤2：场景覆盖检查（含 Gherkin 格式验证）

验证“场景规格”是否完整（模板默认在 §3.5）：

| 场景类型 | 必需 | 检查内容 |
|---------|------|---------|
| 正常场景 | ✅ | 至少1个 Gherkin 场景 |
| 异常场景 | ✅ | 至少1个异常处理场景 |
| 边界场景 | ✅ | 至少1个边界条件场景 |
| 不支持场景 | ⚠️ | 建议提供（如适用） |

**Gherkin 格式自动检查规则**：

1. **标题格式检查**：
   - ✅ 正确：`#### Scenario: 启用 3D 音效`
   - ❌ 错误：`### 场景1` 或 `**场景**：启用 3D 音效`
   - 检测规则：必须使用 `#### Scenario:` 开头

2. **GIVEN/WHEN/THEN 结构检查**：
   - ✅ 正确：
     ```markdown
     - **GIVEN** 用户有 MANAGE_AUDIO 权限
     - **WHEN** 调用 enable3DSound()
     - **THEN** 3D 音效启用，返回成功
     ```
   - ❌ 错误：
     ```markdown
     前置条件：用户有权限
     操作：调用接口
     结果：成功
     ```
   - 检测规则：必须包含 `GIVEN`、`WHEN`、`THEN` 关键词（大写）

3. **场景完整性检查**：
   - 每个场景必须同时包含 GIVEN、WHEN、THEN 三部分
   - 不支持场景必须额外包含 `REASON` 说明原因

**自动检测流程**：
```python
def check_gherkin_format(scenario_text):
    errors = []

    # 检查标题格式
    if not re.search(r'^####\s+Scenario:', scenario_text, re.MULTILINE):
        errors.append('❌ 场景标题必须使用 "#### Scenario:" 格式')

    # 检查 GIVEN/WHEN/THEN 结构
    has_given = 'GIVEN' in scenario_text
    has_when = 'WHEN' in scenario_text
    has_then = 'THEN' in scenario_text

    if not (has_given and has_when and has_then):
        missing = []
        if not has_given: missing.append('GIVEN')
        if not has_when: missing.append('WHEN')
        if not has_then: missing.append('THEN')
        errors.append(f'❌ 缺少 Gherkin 关键词：{", ".join(missing)}')

    return errors
```

**场景覆盖自动检查**：
```python
def check_scenario_coverage(rfc_content):
    scenarios = {
        'normal': re.findall(r'####\s+正常场景|####\s+Scenario:.*正常', rfc_content),
        'exception': re.findall(r'####\s+异常场景|####\s+Scenario:.*异常|错误|失败', rfc_content),
        'boundary': re.findall(r'####\s+边界场景|####\s+Scenario:.*边界|并发|极限', rfc_content),
        'unsupported': re.findall(r'####\s+不支持场景|####\s+Scenario:.*不支持', rfc_content),
    }

    errors = []
    if len(scenarios['normal']) == 0:
        errors.append('❌ 缺少正常场景（必须）')
    if len(scenarios['exception']) == 0:
        errors.append('❌ 缺少异常场景（必须）')
    if len(scenarios['boundary']) == 0:
        errors.append('❌ 缺少边界场景（必须）')
    if len(scenarios['unsupported']) == 0:
        errors.append('⚠️ 建议补充不支持场景（如适用）')

    return errors, scenarios
```

### 步骤3：依赖影响与测试矩阵检查（新增）

**依赖影响矩阵检查**：
```python
def check_dependency_impact(findings, rfc_content):
    deps = findings.get("confirmed", {}).get("dependencies", {})
    has_deps = any(deps.get(k) for k in ["internal", "external", "integration_points"])
    if has_deps and "依赖影响矩阵" not in rfc_content:
        return ["❌ 存在依赖但未提供依赖影响矩阵"]
    return []
```

**测试矩阵检查**：
```python
def check_test_matrix(rfc_content):
    if "测试矩阵" not in rfc_content:
        return ["❌ 缺少测试矩阵（场景→用例→验收）"]
    # 异常/边界场景至少包含错误码或回退行为
    if "异常场景" in rfc_content and "错误码" not in rfc_content and "回退" not in rfc_content:
        return ["❌ 异常/边界场景未给出错误码或回退行为"]
    return []
```

### 步骤4：DFX 清单检查（含模糊描述自动检测）

**自动检测规则（基于正则表达式）**：

验证 §4 DFX 约束是否覆盖 8 个维度，并自动检测模糊描述：

| 维度 | 级别 | 检查要点 | 模糊描述检测规则 |
|------|------|---------|-----------------|
| 安全性 | ❌ error | 权限策略、数据保护、输入验证 | 检测："需要权限"、"数据加密"、"输入校验"（无具体说明） |
| 可靠性 | ❌ error | 异常处理、降级方案、超时重试 | 检测："异常处理"、"错误处理"、"降级"（无具体策略） |
| 性能 | ⚠️ warning | 延迟指标、吞吐量、资源预算 | 检测："性能良好"、"延迟低"、"快速"（无具体数值） |
| 可测试性 | ⚠️ warning | 测试策略、场景覆盖 | 检测："有测试"、"测试完整"（无具体策略） |
| 可观测性 | ⚠️ warning | 日志规范、监控指标、告警策略 | 检测："记录日志"、"监控"（无具体指标） |
| 可维护性 | ℹ️ info | 代码复杂度、文档完整性 | 检测："代码简洁"、"文档齐全"（无量化标准） |
| 兼容性 | ⚠️ warning | API版本、向后兼容、迁移方案 | 检测："向后兼容"、"平滑迁移"（无具体版本） |
| 可运维性 | ℹ️ info | 部署策略、回滚方案 | 检测："灰度发布"、"可回滚"（无具体参数） |

**模糊词汇黑名单（自动标记为 error）**：
```python
VAGUE_PATTERNS = {
    # 安全性模糊词汇
    r'需要权限(?!.*\b[A-Z_]+\.[A-Z_]+\b)': '必须说明具体权限名称（如 ohos.permission.MANAGE_AUDIO）',
    r'数据加密(?!.*AES|RSA|密钥)': '必须说明加密算法（如 AES-256）和密钥管理方式',
    r'输入(?:校验|验证)(?!.*类型|范围|边界)': '必须说明验证规则（类型检查、范围检查、边界条件）',

    # 性能模糊词汇
    r'性能(?:良好|优秀|不错)': '必须量化指标（如 p99 延迟 < 100ms）',
    r'延迟(?:低|小|短)(?!.*\d+\s*ms)': '必须提供具体延迟数值（如 p99 < 50ms）',
    r'(?:快速|高效)(?!.*\d+)': '必须量化性能指标',

    # 可靠性模糊词汇
    r'异常(?:处理|场景)(?!.*返回|抛出|错误码)': '必须说明具体处理策略（返回什么错误码？用户看到什么？）',
    r'降级(?:方案|策略)(?!.*降级到)': '必须说明降级到什么程度（核心功能还能用吗？）',
    r'超时(?:重试)?(?!.*\d+\s*(?:ms|秒|次))': '必须说明超时时间和重试次数',

    # 可观测性模糊词汇
    r'记录日志(?!.*INFO|ERROR|WARN)': '必须说明日志级别（INFO/ERROR/WARN）',
    r'监控(?:指标)?(?!.*具体指标)': '必须说明监控哪些指标（QPS、延迟、错误率等）',
    r'告警(?!.*阈值|条件)': '必须说明告警条件和阈值',

    # 兼容性模糊词汇
    r'向后兼容(?!.*版本|v\d+)': '必须说明兼容到哪个版本',
    r'平滑迁移(?!.*步骤|方案)': '必须提供具体迁移步骤',
}
```

**自动检测流程**：
1. 扫描 §4 DFX 约束全文
2. 对每个维度应用模糊词汇检测规则
3. 标记所有匹配的模糊描述为 ❌ error
4. 生成具体的改进建议（参考 auditor.md 的模糊描述检测规则）
5. 如果存在模糊描述，阻塞进入人工审查阶段

**正向匹配模式（不视为模糊）**：
```python
QUANTIFIED_PATTERNS = [
    r'[<>≤≥]\s*\d+\s*(?:ms|秒|s|分钟|小时)',  # 延迟 < 100ms
    r'p\d+\s*[<>≤≥]\s*\d+',  # p99 < 50ms
    r'\d+\s*(?:MB|GB|KB|%)',  # 内存 < 100MB
    r'(?:AES|RSA|SHA)-\d+',  # AES-256
    r'ohos\.permission\.[A-Z_]+',  # ohos.permission.MANAGE_AUDIO
    r'错误码\s*\d+',  # 错误码 401
]
```

### 步骤4：设计决策检查
验证 §5 设计决策是否完整：

| 检查项 | 必需 | 检查内容 |
|-------|------|---------|
| ADR | ✅ | 至少1个架构决策记录 |
| 交互流程 | ⚠️ | COMPLEX 必须 Mermaid 图示；MEDIUM 建议图示 |
| 状态机 | ℹ️ | 如适用，COMPLEX 必须 Mermaid 图示 |
| 算法描述 | ⚠️ | 关键算法的自然语言描述 |

### 步骤5：生成预检报告
输出预检结果：

```markdown
# RFC 预检报告

## 预检结果
- ✅ 通过：X 项
- ⚠️ 警告：X 项
- ❌ 阻塞：X 项

## 阻塞问题（必须修复）
1. [问题描述] → **建议**：[修改建议]

## 警告问题（建议修复）
1. [问题描述] → **建议**：[修改建议]

## 通过项
- [列出通过的检查项]

## 下一步
- 如有阻塞问题，请修改后重新预检
- 如无阻塞问题，可进入人工审查（/ohspec:audit）
```

## 自动建议生成

### 缺失章节建议
```markdown
❌ 缺少 §4.5 可观测性

**建议补充**：
### 4.5 可观测性（Observability）
- **日志规范**：[日志级别、格式、关键埋点]
- **监控指标**：[需要监控哪些指标？]
- **告警策略**：[什么情况触发告警？]
```

### 场景缺失建议
```markdown
❌ 缺少异常场景

**建议补充**：
#### 异常场景

#### Scenario: [异常场景名称]
- **GIVEN** [前置条件]
- **WHEN** [触发异常的动作]
- **THEN** [错误处理行为]
```

### DFX 缺失建议
```markdown
⚠️ §4.1 安全性描述过于简单

**当前**：需要权限
**建议改为**：
- **权限策略**：需要 audio.manage 权限，通过 PermissionManager.check() 校验
- **数据保护**：敏感数据使用 AES-256 加密，密钥存储在 KeyStore
- **输入验证**：所有外部输入进行类型检查和范围验证
```

## 预检规则配置

### 严格模式（默认）
- 所有 error 级别问题必须修复
- 所有 warning 级别问题建议修复
- info 级别问题可选

### 宽松模式
- 仅 error 级别问题必须修复
- warning 和 info 级别问题可选

## 输出物
- 预检报告（写入 progress.json）
- 修改建议（如有问题）

## 错误处理
- RFC 文件不存在 → 提示用户先执行 analyze/design 阶段
- RFC 格式错误 → 提示具体格式问题
- 预检失败 → 提供详细错误信息和修改建议

## 5-Question Reboot Test 验证（新增）

**目的**：确保上下文充分，防止在长会话中偏离目标

**执行时机**：每个阶段开始前（analyze、design、audit）

**验证清单**：
```markdown
| 问题 | 答案 | 状态 |
|------|------|------|
| 我在哪里？ | [当前阶段] | ✅/❌ |
| 我要去哪里？ | [剩余阶段] | ✅/❌ |
| 目标是什么？ | [用户原始需求] | ✅/❌ |
| 我学到了什么？ | [findings.json 关键发现] | ✅/❌ |
| 我做了什么？ | [progress.json 已完成工作] | ✅/❌ |
```

**验证规则**：
1. **所有问题必须有明确答案**
   - ✅ 通过：所有 5 个问题都能回答
   - ❌ 失败：任何问题无法回答

2. **失败时的处理**：
   - 立即重读 `findings.json` 和 `progress.json`
   - 更新 5-Question Reboot Check 表格
   - 重新验证，直到所有问题都能回答

3. **验证示例**：
   ```markdown
   ✅ 通过示例：
   | 问题 | 答案 |
   |------|------|
   | 我在哪里？ | Phase 2: 方案设计 |
   | 我要去哪里？ | Phase 3: 质量审查 |
   | 目标是什么？ | 为音频服务增加 3D 音效开关 |
   | 我学到了什么？ | 找到 5 个相关文件，2 种实现模式 |
   | 我做了什么？ | 完成代码扫描、用户访谈、需求分析 |

   ❌ 失败示例：
   | 问题 | 答案 |
   |------|------|
   | 我在哪里？ | Phase 2: 方案设计 |
   | 我要去哪里？ | ？（不清楚） ← 失败 |
   | 目标是什么？ | ？（忘记了） ← 失败 |
   ```

4. **集成到预检流程**：
   - 在执行 DFX 检查前，先执行 5-Question Reboot Test
   - 如果验证失败，暂停预检，要求重读上下文文件
   - 验证通过后，继续执行 DFX 检查

**输出**：
- 验证结果记录到 `progress.json` 的 5-Question Reboot Check 表格
- 如果失败，记录失败原因和恢复操作
