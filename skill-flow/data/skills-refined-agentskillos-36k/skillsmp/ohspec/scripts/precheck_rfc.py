#!/usr/bin/env python3
"""
OHSpec RFC precheck (executable).

Purpose:
  - Validate that generated artifacts follow OHSpec templates:
      rfc.md, findings.json, progress.json
  - Enforce hard quality gates before audit/approval:
      template structure, required matrices, IDs, mermaid (COMPLEX),
      evidence anchors, and "requirement-driven (less code)" style.

This script is intentionally dependency-free and works in:
  - Linux/macOS: python3
  - Windows: python / py -3
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple


RFC_MD = "rfc.md"
FINDINGS_JSON = "findings.json"
PROGRESS_JSON = "progress.json"
REPORT_MD = "precheck-report.md"


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def load_json(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def dump_json(path: Path, data: Any) -> None:
    tmp = path.with_suffix(path.suffix + ".tmp")
    with tmp.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2, sort_keys=False)
        f.write("\n")
    tmp.replace(path)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def resolve_rfc_dir(rfc_id_or_dir: str) -> Path:
    """
    Resolve either:
      - an RFC directory path
      - an RFC ID, locating it under:
          - .ohspec/rfcs/            (preferred)
          - .claude/ohspec/rfcs/     (legacy)
    """
    def looks_like_ohspec_home(p: Path) -> bool:
        return (p.name == ".ohspec") or (p.name == "ohspec" and p.parent.name == ".claude")

    def looks_like_rfcs_base(p: Path) -> bool:
        if p.name != "rfcs":
            return False
        if p.parent.name == ".ohspec":
            return True
        return p.parent.name == "ohspec" and p.parent.parent.name == ".claude"

    def project_root_from_script() -> Optional[Path]:
        p = Path(__file__).resolve()
        try:
            if p.parent.name == "scripts" and p.parent.parent.name == ".ohspec":
                return p.parent.parent.parent
            if p.parent.name == "scripts" and p.parent.parent.name == "ohspec" and p.parent.parent.parent.name == ".claude":
                return p.parent.parent.parent.parent
        except Exception:
            pass
        return None

    def search_from_root(root: Path, rfc_id: str) -> Optional[Path]:
        for base in [
            root / ".ohspec" / "rfcs" / rfc_id,
            root / ".claude" / "ohspec" / "rfcs" / rfc_id,
        ]:
            if base.exists():
                return base
        return None

    cand = Path(rfc_id_or_dir)
    if cand.exists() and cand.is_dir():
        if looks_like_ohspec_home(cand) or looks_like_rfcs_base(cand):
            raise ValueError(
                f"'{cand}' looks like OHSpec home/rfcs base dir, not an RFC dir. "
                "Pass an RFC dir like .ohspec/rfcs/<RFC-ID>/, or pass the RFC-ID."
            )
        return cand.resolve()

    rfc_id = rfc_id_or_dir

    # 1) From current working directory (and its parents)
    cwd = Path.cwd().resolve()
    for p in [cwd, *cwd.parents]:
        found = search_from_root(p, rfc_id)
        if found:
            return found.resolve()

    # 2) From this script location (project-local bootstrap)
    pr = project_root_from_script()
    if pr:
        found = search_from_root(pr, rfc_id)
        if found:
            return found.resolve()

    raise FileNotFoundError(
        f"Cannot resolve RFC dir for '{rfc_id_or_dir}'. "
        f"Pass an RFC directory path, or run from a project root that has "
        f".ohspec/rfcs/{rfc_id} (preferred) or .claude/ohspec/rfcs/{rfc_id} (legacy)."
    )


def _split_md_row(line: str) -> List[str]:
    # Trim and split a markdown table row: | a | b | -> ["a", "b"]
    placeholder = "\u0000"
    s = line.strip().strip("|").replace("\\|", placeholder)
    parts = [p.strip().replace(placeholder, "|") for p in s.split("|")]
    return parts


def find_table_by_required_columns(rfc_lines: Sequence[str], required_cols: Sequence[str]) -> bool:
    required = [c.strip() for c in required_cols]
    for line in rfc_lines:
        if not line.lstrip().startswith("|"):
            continue
        header = _split_md_row(line)
        if all(c in header for c in required):
            return True
    return False


@dataclass
class Issue:
    issue_id: str
    severity: str  # error|warning
    kind: str
    location: str
    description: str
    fix: str

    def as_progress_issue(self) -> Dict[str, Any]:
        return {
            "id": self.issue_id,
            "severity": self.severity,
            "type": self.kind,
            "location": self.location,
            "description": self.description,
            "fix_suggestion": self.fix,
        }


ANCHOR_RE = re.compile(r"^[^@\s]+@[^:]+:.+#L\d+$")
ID_RE = {
    "REQ": re.compile(r"\bREQ-\d{3}\b"),
    "SCN": re.compile(r"\bSCN-\d{3}\b"),
    "API": re.compile(r"\bAPI-\d{3}\b"),
    "FIELD": re.compile(r"\bFIELD-\d{3}\b"),
    "CHG": re.compile(r"\bCHG-\d{3}\b"),
    "EDGE": re.compile(r"\bEDGE-\d{3}\b"),
    "DEP": re.compile(r"\bDEP-\d{3}\b"),
    "TST": re.compile(r"\bTST-\d{3}\b"),
}
REQ_HEADER_RE = re.compile(r"^####\s+Requirement:\s+(REQ-\d{3})", re.IGNORECASE)
ACCEPTANCE_PLACEHOLDER_TERMS = ["可验证、可量化", "待定义", "TBD", "TODO"]
ACCEPTANCE_HARD_TERMS = ["实现", "编码", "代码", "函数", "类", "方法", "伪代码", "算法"]
ACCEPTANCE_SOFT_TERMS = ["模块", "框架", "SDK", "库", "脚本", "编译", "线程", "锁", "缓存", "队列", "定时任务"]


def parse_complexity_from_rfc(rfc_lines: Sequence[str]) -> str:
    # Best-effort: read metadata table row.
    for line in rfc_lines:
        if "| complexity |" in line:
            parts = _split_md_row(line)
            if len(parts) >= 2:
                return parts[1].strip()
    return ""


def extract_code_blocks(rfc_lines: Sequence[str]) -> List[Dict[str, Any]]:
    blocks: List[Dict[str, Any]] = []
    in_block = False
    lang = ""
    start_line = 0
    buf: List[str] = []
    for idx, line in enumerate(rfc_lines, start=1):
        if line.startswith("```"):
            if not in_block:
                in_block = True
                lang = line[3:].strip().lower()
                start_line = idx
                buf = []
            else:
                blocks.append(
                    {
                        "lang": lang,
                        "start_line": start_line,
                        "end_line": idx,
                        "lines": buf[:],
                        "line_count": len(buf),
                    }
                )
                in_block = False
                lang = ""
                start_line = 0
                buf = []
            continue
        if in_block:
            buf.append(line.rstrip("\n"))
    # Unclosed fences are treated as an error via structure checks (markdown hygiene).
    return blocks


def has_mermaid_block(blocks: Sequence[Dict[str, Any]]) -> bool:
    return any((b.get("lang") or "").strip() == "mermaid" for b in blocks)


def collect_ids(rfc_text: str) -> Dict[str, List[str]]:
    out: Dict[str, List[str]] = {}
    for k, pat in ID_RE.items():
        out[k] = sorted(set(pat.findall(rfc_text)))
    return out


def _derive_role_from_path(path: str) -> str:
    p = (path or "").lower()
    if any(k in p for k in ["config", "setting", "prefs", "state", "store", "db", "schema", "kv"]):
        return "config"
    if any(k in p for k in ["client", "adapter", "driver", "rpc", "grpc", "http", "integration", "external", "hdi", "hdf"]):
        return "dependency"
    if any(k in p for k in ["test", "tests", "e2e", "integration_test", "unit_test"]):
        return "test"
    if any(k in p for k in ["log", "metric", "trace", "telemetry", "monitor", "dump", "hisysevent"]):
        return "observability"
    if any(k in p for k in ["handler", "controller", "service", "api", "endpoint", "cli", "main", "entry"]):
        return "entry"
    return ""


def _extract_requirement_blocks(rfc_lines: Sequence[str]) -> List[Tuple[str, List[str]]]:
    blocks: List[Tuple[str, List[str]]] = []
    current_id = ""
    current_lines: List[str] = []
    for line in rfc_lines:
        m = REQ_HEADER_RE.match(line.strip())
        if m:
            if current_id:
                blocks.append((current_id, current_lines))
            current_id = m.group(1)
            current_lines = []
            continue
        if current_id and line.strip().startswith("#### "):
            blocks.append((current_id, current_lines))
            current_id = ""
            current_lines = []
            continue
        if current_id:
            current_lines.append(line)
    if current_id:
        blocks.append((current_id, current_lines))
    return blocks


def _extract_acceptance_text(line: str) -> str:
    text = re.sub(r"^\\s*-?\\s*\\*\\*?验收标准\\*\\*?\\s*[:：]?", "", line).strip()
    if text.startswith("[") and text.endswith("]"):
        text = text[1:-1].strip()
    return text


def precheck(rfc_dir: Path, strict: bool = False) -> Tuple[List[Issue], Dict[str, Any]]:
    issues: List[Issue] = []

    rfc_path = rfc_dir / RFC_MD
    findings_path = rfc_dir / FINDINGS_JSON
    progress_path = rfc_dir / PROGRESS_JSON

    if not rfc_path.exists():
        issues.append(
            Issue("ISS-001", "error", "missing_file", "rfc.md", "缺少 rfc.md", "生成 RFC 目录时必须创建三文件骨架")
        )
        return issues, {}
    if not findings_path.exists():
        issues.append(
            Issue(
                "ISS-002",
                "error",
                "missing_file",
                "findings.json",
                "缺少 findings.json",
                "初始化时从 OHSpec 模板生成（推荐：.ohspec/templates/findings.json；兼容：.claude/ohspec/templates/findings.json），并在扫描后持续更新",
            )
        )
        return issues, {}
    if not progress_path.exists():
        issues.append(
            Issue(
                "ISS-003",
                "error",
                "missing_file",
                "progress.json",
                "缺少 progress.json",
                "初始化时从 OHSpec 模板生成（推荐：.ohspec/templates/progress.json；兼容：.claude/ohspec/templates/progress.json），并在每阶段结束更新",
            )
        )
        return issues, {}

    rfc_text = read_text(rfc_path)
    rfc_lines = rfc_text.splitlines()

    try:
        findings = load_json(findings_path)
    except Exception as e:
        issues.append(
            Issue("ISS-004", "error", "invalid_json", "findings.json", f"findings.json 不是合法 JSON: {e}", "修复 JSON 格式")
        )
        return issues, {}
    try:
        progress = load_json(progress_path)
    except Exception as e:
        issues.append(
            Issue("ISS-005", "error", "invalid_json", "progress.json", f"progress.json 不是合法 JSON: {e}", "修复 JSON 格式")
        )
        return issues, {}

    # ---- Schema checks (hard gate) ----
    findings_required = {"meta", "requirement", "dispatcher", "confirmed", "working"}
    if not isinstance(findings, dict) or not findings_required.issubset(set(findings.keys())):
        missing = sorted(list(findings_required - set(findings.keys() if isinstance(findings, dict) else [])))
        issues.append(
            Issue(
                "ISS-006",
                "error",
                "schema_error",
                "findings.json",
                f"findings.json schema 不符合 OHSpec（缺少: {missing}）",
                "禁止自造结构；必须从 OHSpec 模板初始化（推荐：.ohspec/templates/findings.json；兼容：.claude/ohspec/templates/findings.json）并按字段写入",
            )
        )

    progress_required = {"meta", "phases", "state_machine", "tooling", "audit_log"}
    if not isinstance(progress, dict) or not progress_required.issubset(set(progress.keys())):
        missing = sorted(list(progress_required - set(progress.keys() if isinstance(progress, dict) else [])))
        issues.append(
            Issue(
                "ISS-007",
                "error",
                "schema_error",
                "progress.json",
                f"progress.json schema 不符合 OHSpec（缺少: {missing}）",
                "禁止自造结构；必须从 OHSpec 模板初始化（推荐：.ohspec/templates/progress.json；兼容：.claude/ohspec/templates/progress.json）并按字段写入",
            )
        )

    # ---- Pending questions/options (hard gate) ----
    working = (findings.get("working") if isinstance(findings, dict) else {}) or {}
    pending_q = working.get("pending_questions") or []
    pending_o = working.get("pending_options") or []
    if pending_q or pending_o:
        issues.append(
            Issue(
                "ISS-008",
                "error",
                "unresolved_questions",
                "findings.working",
                "存在未决问题/选项，禁止进入审查/通过",
                "先完成澄清并清零 pending_questions/pending_options，再进入 design/audit",
            )
        )

    # ---- Parse complexity (for gates) ----
    complexity = parse_complexity_from_rfc(rfc_lines) or str((findings.get("dispatcher") or {}).get("complexity") or "")
    complexity = (complexity or "").strip().upper()

    # ---- RFC structure gates ----
    if not rfc_lines or not rfc_lines[0].startswith("# RFC:"):
        issues.append(
            Issue(
                "ISS-009",
                "error",
                "template_mismatch",
                "rfc.md",
                "RFC 顶部标题不符合模板（必须以 '# RFC:' 开头）",
                "必须以 OHSpec 模板作为骨架（推荐：.ohspec/templates/rfc.md；兼容：.claude/ohspec/templates/rfc.md），只做填空/增量更新，不得重排结构",
            )
        )

    required_h2 = [
        "## §1. 上下文",
        "## §2. 需求",
        "## §3. 契约",
        "## §4. DFX 约束",
        "## §5. 设计决策",
    ]
    for h in required_h2:
        if h not in rfc_text:
            issues.append(
                Issue(
                    "ISS-010",
                    "error",
                    "missing_section",
                    h,
                    f"缺少必需章节: {h}",
                    "按 OHSpec 模板补齐（推荐：.ohspec/templates/rfc.md；兼容：.claude/ohspec/templates/rfc.md）",
                )
            )

    # Optional readability heuristic: avoid auto-generated TOC.
    if "## 目录" in rfc_text:
        issues.append(
            Issue(
                "ISS-022",
                "warning" if not strict else "error",
                "toc_present",
                "rfc.md",
                "检测到“目录/TOC”（通常会降低可读性且易失真）",
                "建议移除目录，改用“审查速览 + 索引”定位关键内容",
            )
        )

    required_substrings = [
        "### 审查速览（人审查优先）",
        "### 1.2.1 项目事实（scan-of-record）",
        "### 1.4 Repo Manifest（多仓适用）",
        "### 2.3 场景概览（需求层）",
        "### 3.1 开发者模型与易用性（Public API）",
        "### 3.2 接口契约表（需求化）",
        "### 3.4 对齐与变更矩阵（必须二选一）",
        "### 3.6 异常与边界矩阵（工业级）",
        "### 3.7 依赖影响矩阵（设计层）",
        "#### 测试矩阵",
        "#### 追溯矩阵（需求→场景→测试）",
    ]
    for s in required_substrings:
        if s not in rfc_text:
            issues.append(Issue("ISS-011", "error", "missing_section", s, f"缺少关键段落: {s}", "按模板补齐该段落"))

    if "**范围**" not in rfc_text:
        issues.append(
            Issue(
                "ISS-028",
                "error",
                "missing_scope",
                "rfc.md:§1.2",
                "背景缺少范围",
                "在 §1.2 背景补充范围说明（包含哪些内容）",
            )
        )

    if "**排除项**" not in rfc_text:
        issues.append(
            Issue(
                "ISS-029",
                "error",
                "missing_exclusions",
                "rfc.md:§1.2",
                "背景缺少排除项",
                "在 §1.2 背景补充明确不包含的内容",
            )
        )

    if "成功指标/业务收益" not in rfc_text:
        issues.append(
            Issue(
                "ISS-030",
                "warning" if not strict else "error",
                "missing_success_metrics",
                "rfc.md:审查速览",
                "审查速览缺少成功指标/业务收益",
                "在审查速览补充可量化指标/业务价值",
            )
        )

    if "灰度/开关策略" not in rfc_text:
        issues.append(
            Issue(
                "ISS-031",
                "warning" if not strict else "error",
                "missing_rollout_strategy",
                "rfc.md:§4.8",
                "可运维性缺少灰度/开关策略",
                "在 §4.8 补充是否需要开关、灰度范围与回退条件",
            )
        )

    # DFX headings (8D)
    dfx_heads = [
        "### 4.1 安全性（Security）",
        "### 4.2 可靠性（Reliability）",
        "### 4.3 性能（Performance）",
        "### 4.4 可测试性（Testability）",
        "### 4.5 可观测性（Observability）",
        "### 4.6 可维护性（Maintainability）",
        "### 4.7 兼容性（Compatibility）",
        "### 4.8 可运维性（Operability）",
    ]
    for h in dfx_heads:
        if h not in rfc_text:
            issues.append(Issue("ISS-012", "error", "missing_dfx_dimension", h, f"缺少 DFX 维度: {h}", "按模板补齐"))

    # Required matrices (table header validation)
    required_tables = [
        ("FACT 表", ["FACT-ID", "事实", "证据锚点"]),
        ("Repo Manifest", ["repo_id", "root", "rev", "owner"]),
        ("API 契约表", ["API-ID", "接口/事件", "层级", "输入/参数", "默认值", "输出/错误码", "兼容策略"]),
        ("数据字典", ["FIELD-ID", "字段", "类型"]),
        ("对齐与变更矩阵", ["CHG-ID", "变更项", "类型", "existing_ref", "new_change_plan"]),
        ("异常/边界矩阵", ["EDGE-ID", "边界/异常", "触发条件", "预期行为"]),
        ("依赖影响矩阵", ["DEP-ID", "依赖方", "调用点", "失败模式"]),
        ("测试矩阵", ["TST-ID", "场景ID", "用例类型", "验收指标"]),
        ("追溯矩阵", ["REQ-ID", "SCN-ID", "TST-ID"]),
    ]
    for name, cols in required_tables:
        if not find_table_by_required_columns(rfc_lines, cols):
            issues.append(
                Issue(
                    "ISS-013",
                    "error",
                    "missing_table",
                    "rfc.md",
                    f"缺少必需表格或列名不匹配: {name}（要求列: {cols}）",
                    "按模板补齐对应表格，且不要改动列名",
                )
            )

    # Acceptance criteria checks (requirement-driven).
    req_blocks = _extract_requirement_blocks(rfc_lines)
    for req_id, block_lines in req_blocks:
        acc_lines = [l for l in block_lines if "验收标准" in l]
        if not acc_lines:
            issues.append(
                Issue(
                    "ISS-023",
                    "error",
                    "missing_acceptance_criteria",
                    f"rfc.md:{req_id}",
                    f"{req_id} 缺少验收标准",
                    "在每条需求下补充可观察结果 + 量化指标（禁止实现步骤/技术选型）",
                )
            )
            continue
        acc_text = _extract_acceptance_text(acc_lines[0])
        if not acc_text:
            issues.append(
                Issue(
                    "ISS-024",
                    "error",
                    "acceptance_empty",
                    f"rfc.md:{req_id}",
                    f"{req_id} 验收标准为空",
                    "填写可观察结果 + 量化指标（避免占位符）",
                )
            )
            continue
        if any(term in acc_text for term in ACCEPTANCE_PLACEHOLDER_TERMS):
            issues.append(
                Issue(
                    "ISS-025",
                    "error",
                    "acceptance_placeholder",
                    f"rfc.md:{req_id}",
                    f"{req_id} 验收标准仍为占位符",
                    "替换为可观察结果 + 量化指标（避免实现步骤/技术选型）",
                )
            )
            continue
        hard_hits = [t for t in ACCEPTANCE_HARD_TERMS if t in acc_text]
        if hard_hits:
            issues.append(
                Issue(
                    "ISS-026",
                    "error",
                    "acceptance_is_how",
                    f"rfc.md:{req_id}",
                    f"{req_id} 验收标准包含实现细节关键词（示例: {hard_hits[:3]}）",
                    "改为可观察结果/指标/错误码/状态",
                )
            )
            continue
        soft_hits = [t for t in ACCEPTANCE_SOFT_TERMS if t in acc_text]
        if soft_hits:
            issues.append(
                Issue(
                    "ISS-027",
                    "warning" if not strict else "error",
                    "acceptance_maybe_how",
                    f"rfc.md:{req_id}",
                    f"{req_id} 验收标准可能包含实现倾向关键词（示例: {soft_hits[:3]}）",
                    "尽量改为可观察结果/指标/错误码/状态",
                )
            )

    # IDs must exist for machine readability.
    ids = collect_ids(rfc_text)
    for k in ["REQ", "SCN", "CHG", "TST"]:
        if not ids.get(k):
            issues.append(
                Issue(
                    "ISS-014",
                    "error",
                    "missing_ids",
                    "rfc.md",
                    f"缺少稳定 ID: {k}-NNN（机器不可读/不可追溯）",
                    "按模板补齐 REQ/SCN/CHG/TST 的编号条目，并在矩阵里引用",
                )
            )

    # Mermaid (COMPLEX hard gate)
    blocks = extract_code_blocks(rfc_lines)
    if complexity == "COMPLEX" and not has_mermaid_block(blocks):
        issues.append(
            Issue(
                "ISS-015",
                "error",
                "missing_mermaid",
                "rfc.md",
                "complexity=COMPLEX 但缺少 Mermaid 图示",
                "在 §5.2/§5.3 或附录 A.1 增加 ```mermaid 图示（交互流程或状态机）",
            )
        )

    # Evidence gates: key_files/facts basics
    confirmed = (findings.get("confirmed") if isinstance(findings, dict) else {}) or {}
    key_files = confirmed.get("key_files") or []
    if not isinstance(key_files, list):
        key_files = []
    if len(key_files) < 3:
        issues.append(
            Issue("ISS-016", "error", "key_files_lt_3", "findings.confirmed.key_files", "key_files < 3", "补齐 ≥3 且覆盖入口/配置/依赖(或测试/可观测)")
        )

    # Coverage check (entry/config/others)
    covered = set()
    anchor_bad: List[str] = []
    for it in key_files:
        if isinstance(it, dict):
            path = str(it.get("path") or "")
            role = str(it.get("role") or "").strip().lower()
        else:
            path = str(it)
            role = ""
        if not role:
            role = _derive_role_from_path(path)
        if role:
            covered.add(role)
        if path and not ANCHOR_RE.match(path):
            anchor_bad.append(path)
    if "entry" not in covered or "config" not in covered or len(covered.intersection({"dependency", "test", "observability"})) < 1:
        issues.append(
            Issue(
                "ISS-017",
                "error",
                "key_files_coverage",
                "findings.confirmed.key_files",
                f"key_files 覆盖面不足（当前 roles: {sorted(list(covered))}）",
                "补齐并标注 role，至少覆盖 entry + config + (dependency|test|observability)",
            )
        )

    facts = confirmed.get("facts") or []
    if not isinstance(facts, list):
        facts = []
    min_facts = 1 if complexity == "SIMPLE" else 3
    if len(facts) < min_facts:
        issues.append(
            Issue(
                "ISS-018",
                "error",
                "facts_insufficient",
                "findings.confirmed.facts",
                f"facts 不足（当前 {len(facts)}，要求 ≥ {min_facts}）",
                "提炼项目事实（配置/存储/权限/错误码/线程模型/可观测等）并附证据锚点",
            )
        )
    fact_anchor_bad = []
    for f in facts:
        if not isinstance(f, dict):
            continue
        ev = f.get("evidence") or []
        if not ev:
            fact_anchor_bad.append("<missing evidence>")
            continue
        for a in ev:
            if not ANCHOR_RE.match(str(a)):
                fact_anchor_bad.append(str(a))

    # In multi-repo, anchor format is a hard gate; single-repo: still warn.
    repos = ((findings.get("meta") or {}).get("repos") if isinstance(findings, dict) else None) or []
    is_multi_repo = isinstance(repos, list) and len(repos) > 1
    if anchor_bad or fact_anchor_bad:
        sev = "error" if is_multi_repo else "warning"
        issues.append(
            Issue(
                "ISS-019",
                sev,
                "anchor_format",
                "evidence",
                f"证据锚点格式不规范（示例: {(anchor_bad or fact_anchor_bad)[:3]}）",
                "统一使用 repo@rev:path#Lline；单仓可用 main@WORKTREE:path#Lline",
            )
        )

    # "Requirement-driven (less code)" heuristic.
    non_mermaid_blocks = [b for b in blocks if (b.get("lang") or "").strip() != "mermaid"]
    non_mermaid_lines = sum(int(b.get("line_count") or 0) for b in non_mermaid_blocks)
    if non_mermaid_blocks:
        sev = "warning"
        if len(non_mermaid_blocks) > 2 or non_mermaid_lines > 50:
            sev = "error"
        issues.append(
            Issue(
                "ISS-020",
                sev,
                "too_much_code",
                "rfc.md",
                f"RFC 包含过多非 Mermaid 代码块（blocks={len(non_mermaid_blocks)}, lines={non_mermaid_lines}）",
                "RFC 应以契约/矩阵表达；仅允许少量调用示意，避免贴实现代码",
            )
        )

    # Very lightweight vague wording check (best-effort).
    vague_phrases = ["性能良好", "尽快", "尽量", "适当", "必要时", "按需", "可能", "大概"]
    vague_hits = [p for p in vague_phrases if p in rfc_text]
    if vague_hits:
        issues.append(
            Issue(
                "ISS-021",
                "warning" if not strict else "error",
                "vague_terms",
                "rfc.md",
                f"检测到可能的模糊词（示例: {vague_hits[:5]}）",
                "将模糊描述改为可量化、可验证的规格（p99/错误码/超时/次数/范围等）",
            )
        )

    # strict mode: warnings become errors.
    if strict:
        for i in issues:
            if i.severity == "warning":
                i.severity = "error"

    result = {
        "complexity": complexity,
        "ids": {k: len(v) for k, v in ids.items()},
        "code_blocks": {
            "total": len(blocks),
            "non_mermaid_blocks": len(non_mermaid_blocks),
            "non_mermaid_lines": non_mermaid_lines,
        },
    }
    return issues, result


def write_report(path: Path, issues: Sequence[Issue], meta: Dict[str, Any], strict: bool) -> None:
    errors = [i for i in issues if i.severity == "error"]
    warnings = [i for i in issues if i.severity == "warning"]
    lines: List[str] = []
    lines.append(f"# OHSpec Precheck Report: {path.parent.name}")
    lines.append("")
    lines.append(f"- 时间: {utc_now_iso()}")
    lines.append(f"- strict: {str(strict).lower()}")
    lines.append(f"- 结论: {'PASS' if not errors else 'FAIL'}")
    lines.append(f"- errors: {len(errors)}, warnings: {len(warnings)}")
    lines.append("")
    if meta:
        lines.append("## 关键统计")
        lines.append("")
        lines.append(f"- complexity: {meta.get('complexity') or ''}")
        ids = meta.get("ids") or {}
        lines.append(f"- ids: {ids}")
        cb = meta.get("code_blocks") or {}
        lines.append(f"- code_blocks: {cb}")
        lines.append("")
    if errors:
        lines.append("## 阻断项（errors）")
        lines.append("")
        for i in errors:
            lines.append(f"- {i.issue_id} [{i.kind}] {i.location}: {i.description} / 修复: {i.fix}")
        lines.append("")
    if warnings:
        lines.append("## 警告（warnings）")
        lines.append("")
        for i in warnings:
            lines.append(f"- {i.issue_id} [{i.kind}] {i.location}: {i.description} / 建议: {i.fix}")
        lines.append("")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def update_progress(progress_path: Path, issues: Sequence[Issue], meta: Dict[str, Any]) -> None:
    progress = load_json(progress_path)
    now = utc_now_iso()

    phases = progress.setdefault("phases", {})
    pre = phases.setdefault("precheck", {})
    pre["status"] = "completed"
    pre.setdefault("started_at", now)
    pre["completed_at"] = now

    # Map into the existing boolean fields if present.
    result = pre.setdefault(
        "result",
        {"structure_complete": False, "scenario_coverage": False, "dfx_complete": False, "no_vague_terms": False},
    )

    # Best-effort mapping: if any error matches category, mark false; else true.
    has_error = any(i.severity == "error" for i in issues)
    structure_errors = {"missing_section", "missing_table", "missing_ids", "template_mismatch", "schema_error"}
    scenario_errors = {"missing_ids"}  # SCN missing is covered by missing_ids; keep minimal.
    dfx_errors = {"missing_dfx_dimension", "missing_table"}
    vague_errors = {"vague_terms"}

    if not has_error:
        result["structure_complete"] = True
        result["scenario_coverage"] = True
        result["dfx_complete"] = True
        result["no_vague_terms"] = True
    else:
        kinds = {i.kind for i in issues if i.severity == "error"}
        result["structure_complete"] = not bool(kinds.intersection(structure_errors))
        result["scenario_coverage"] = not bool(kinds.intersection(scenario_errors))
        result["dfx_complete"] = not bool(kinds.intersection(dfx_errors))
        result["no_vague_terms"] = not bool(kinds.intersection(vague_errors))

    pre["issues"] = [i.as_progress_issue() for i in issues]
    pre["metrics"] = meta

    # Audit log (keep it simple; the orchestrator can add richer entries).
    progress.setdefault("audit_log", []).append(
        {
            "timestamp": now,
            "action": "precheck_completed",
            "detail": {
                "passed": not has_error,
                "errors": sum(1 for i in issues if i.severity == "error"),
                "warnings": sum(1 for i in issues if i.severity == "warning"),
                "metrics": meta,
            },
        }
    )

    # meta.updated_at
    meta_obj = progress.setdefault("meta", {})
    if isinstance(meta_obj, dict):
        meta_obj["updated_at"] = now

    dump_json(progress_path, progress)


def main(argv: Optional[Sequence[str]] = None) -> int:
    ap = argparse.ArgumentParser(description="OHSpec RFC precheck")
    ap.add_argument("rfc", help="RFC ID or RFC directory path")
    ap.add_argument("--strict", action="store_true", help="treat warnings as errors")
    ap.add_argument("--write-report", action="store_true", help=f"write {REPORT_MD} into RFC dir")
    ap.add_argument("--update-progress", action="store_true", help="update progress.json phases.precheck and audit_log")
    args = ap.parse_args(argv)

    try:
        rfc_dir = resolve_rfc_dir(args.rfc)
    except (FileNotFoundError, ValueError) as e:
        print(str(e), file=sys.stderr)
        return 2
    issues, meta = precheck(rfc_dir, strict=args.strict)

    errors = [i for i in issues if i.severity == "error"]
    warnings = [i for i in issues if i.severity == "warning"]

    # Console summary (small, for agents and humans).
    print(f"precheck: {'PASS' if not errors else 'FAIL'} (errors={len(errors)}, warnings={len(warnings)})")
    if meta:
        print(f"complexity={meta.get('complexity')}, ids={meta.get('ids')}, code_blocks={meta.get('code_blocks')}")
    for i in issues:
        tag = "E" if i.severity == "error" else "W"
        print(f"{tag} {i.issue_id} {i.kind} {i.location}: {i.description}")

    if args.write_report:
        write_report(rfc_dir / REPORT_MD, issues, meta, strict=args.strict)
        print(f"wrote: {rfc_dir / REPORT_MD}")
    if args.update_progress:
        update_progress(rfc_dir / PROGRESS_JSON, issues, meta)
        print(f"updated: {rfc_dir / PROGRESS_JSON}")

    return 0 if not errors else 2


if __name__ == "__main__":
    raise SystemExit(main())
