# /ohspec:export - 手动导出机读件（Digest/Tasks）

## 命令说明

RFC 的**唯一事实来源**是 `rfc.md`（人审查优先）。  
`/ohspec:export` 用于在 **人工审查通过后**，手动导出派生的机读件（避免在 RFC 内重复维护 JSON/YAML）。

**默认输出**：`rfc.digest.json`  
**可选输出**：`tasks.json`（面向后续编码 Agent 的任务清单）

> 说明：本命令**不会**自动触发（遵循“仅手动 export”决策）。

## 使用方式

```bash
/ohspec:export RFC-20260120-vibration-switches-217d
```

如环境允许执行脚本（推荐，确定性更强）：
```bash
# Linux/macOS（通常是 python3）
python3 .ohspec/scripts/export_digest.py RFC-20260120-vibration-switches-217d
python3 .ohspec/scripts/export_digest.py RFC-20260120-vibration-switches-217d --tasks

# Windows（可能只有 python；如有 Python Launcher 可用 py -3）
python .ohspec/scripts/export_digest.py RFC-20260120-vibration-switches-217d
python .ohspec/scripts/export_digest.py RFC-20260120-vibration-switches-217d --tasks
py -3 .ohspec/scripts/export_digest.py RFC-20260120-vibration-switches-217d
py -3 .ohspec/scripts/export_digest.py RFC-20260120-vibration-switches-217d --tasks
```

可选参数（建议）：
```bash
/ohspec:export RFC-... --tasks        # 同时导出 tasks.json
/ohspec:export RFC-... --force        # 忽略 staleness 检测，强制重导出
```

## 输出位置

输出写入同一 RFC 目录：
```
.ohspec/rfcs/{RFC-ID}/
  rfc.md
  findings.json
  progress.json
  rfc.digest.json      # 新增（派生机读件）
  tasks.json           # 可选（派生机读件）
```

> 兼容（历史）：若项目仍使用 `.claude/ohspec/rfcs/{RFC-ID}/` 目录结构，export 脚本同样支持（可直接传 RFC 目录路径）。

## 运行前置条件（强制）

1. `progress.json.meta.status == APPROVED`（或 audit 决策 passed）
2. `findings.working.pending_questions/pending_options` 为空
3. `findings.confirmed.key_files` ≥ 3 且覆盖面达标
4. `findings.confirmed.facts` 达标（SIMPLE ≥1；MEDIUM/COMPLEX ≥3，且每条有 evidence 锚点）

若不满足：
- **默认阻断**导出（避免把不完整/不一致规格传播给后续 Agent）
- 用户可显式要求 `--force` 进行导出，但必须在 digest 中标记 `stability: "draft"`

## Digest Schema（稳定字段）

`rfc.digest.json` 只包含后续编码/验证所需的“结构化事实”，不复制大段文本。

## 可解析性约束（保证导出稳定）

`export_digest.py` 不是通用 Markdown 解析器，它依赖 OHSpec 的“结构化 Markdown 约定”。

为保证稳定导出：
- 不要改动关键表格的**列名**（如 `API-ID/CHG-ID/EDGE-ID/DEP-ID/TST-ID/REQ-ID/SCN-ID` 等）
- 表格**每行一行**；长说明放到“条目详情”清单（不要在表格单元格里换行）
- 表格单元格尽量避免未转义的 `|`；需要时使用 `\|` 或移出表格
- Requirement/Scenario 标题保持模板格式：`#### Requirement: REQ-001 ...`、`#### Scenario: SCN-001 ...`

字段兼容说明：
- digest 的 `meta.complexity` 为推荐字段；为兼容旧导出同时保留 `meta.scope`（值相同）。

```json
{
  "schema_version": "1.0",
  "stability": "approved|draft",
  "warnings": ["missing_repo_manifest", "missing_facts"],
  "meta": {
    "rfc_id": "RFC-...",
    "title": "...",
    "complexity": "SIMPLE|MEDIUM|COMPLEX",
    "scope": "SIMPLE|MEDIUM|COMPLEX",
    "created_at": "ISO8601",
    "updated_at": "ISO8601",
    "exported_at": "ISO8601"
  },
  "repos": [
    {"id": "main", "root": "...", "rev": "...", "owner": "...", "compat": "...", "notes": "..."}
  ],
  "anchors": {
    "key_files": [
      {"path": "repo@rev:path#Lline", "role": "entry|config|dependency|test|observability", "reason": "..."}
    ]
  },
  "facts": [
    {"id": "FACT-001", "fact": "...", "evidence": ["repo@rev:path#Lline"], "impact": "..."}
  ],
  "requirements": [
    {"id": "REQ-001", "title": "...", "acceptance": ["..."], "scenarios": ["SCN-001"]}
  ],
  "contracts": {
    "apis": [
      {"id": "API-001", "name": "...", "layer": "...", "inputs": "...", "defaults": "...", "outputs": "...", "compat": "...", "notes": "..."}
    ],
    "fields": [
      {"id": "FIELD-001", "name": "...", "type": "...", "range_unit": "...", "source": "...", "default": "...", "notes": "..."}
    ]
  },
  "changes": [
    {"id": "CHG-001", "item": "...", "kind": "existing|new", "existing_ref": "...", "new_change_plan": "...", "target": "...", "compat": "...", "test_rollback": "..."}
  ],
  "scenarios": [
    {"id": "SCN-001", "type": "normal|exception|boundary|unsupported", "title": "...", "given": ["..."], "when": ["..."], "then": ["..."], "reason": "..."}
  ],
  "edges": [
    {"id": "EDGE-001", "case": "...", "trigger": "...", "expected": "...", "error_code": "...", "fallback": "...", "timing_concurrency": "..."}
  ],
  "dependencies": [
    {"id": "DEP-001", "party": "...", "callsite": "...", "failure_mode": "...", "fallback": "...", "observability": "...", "impact": "..."}
  ],
  "tests": {
    "matrix": [
      {"id": "TST-001", "scenario": "SCN-001", "type": "...", "acceptance": "...", "fault_injection": "...", "compat_regression": "..."}
    ],
    "traceability": [
      {"req": "REQ-001", "scn": "SCN-001", "tst": "TST-001", "notes": "..."}
    ]
  },
  "risks": [
    {"id": "RISK-001", "summary": "...", "mitigation": "...", "rollback": "..."}
  ],
  "provenance": {
    "sources": {
      "rfc_md": {"path": "rfc.md", "sha256": "..."},
      "findings_json": {"path": "findings.json", "sha256": "..."},
      "progress_json": {"path": "progress.json", "sha256": "..."}
    }
  }
}
```

## 执行流程

### 步骤 1：加载与一致性检查

读取：
- `rfc.md`
- `findings.json`
- `progress.json`

检查：
- RFC 状态是否 APPROVED
- 未决问题是否清零
- key_files 覆盖是否达标
- 多仓时 Repo Manifest 与锚点格式是否满足 `repo@rev:path#Lline`

### 步骤 2：提取结构化信息（以 ID 为主键）

提取/对齐以下 ID：
- REQ / SCN / API / FIELD / CHG / EDGE / DEP / TST

规则：
- 只导出**可验证的事实**（表格、矩阵、编号条目、锚点）
- 对于长段落：提炼为 1-3 条 acceptance/notes
- 若发现 RFC 中存在未闭环引用（例如 REQ 引用不存在的 SCN），必须阻断导出（除非 --force）

### 步骤 3：生成 rfc.digest.json

生成 digest，并写入 provenance（对 3 个源文件计算 sha256）。

> 不要把 RFC 正文整段复制进 digest；digest 面向机器与后续 Agent 的结构化消费。

### 步骤 4（可选）：生成 tasks.json

当用户启用 `--tasks` 时，按 repo_id 分组生成任务清单：
- 每个任务必须引用 CHG/REQ/SCN/TST 的 ID
- 每个任务必须包含验收标准与回滚提示
- 不写具体代码实现，保持任务可执行且可验证

### 步骤 5：写入 progress.json 的导出记录

在 `progress.json` 中追加导出记录（建议字段）：
- 输出文件名、导出时间
- 源文件 sha256（用于 staleness 检测）
- stability（approved/draft）

### 步骤 6：对用户输出提示

输出给用户的提示应包含：
- 导出的文件路径
- 是否为 approved（或 draft）
- 如为 draft，列出阻断原因（未决项/锚点不足/一致性不通过等）
