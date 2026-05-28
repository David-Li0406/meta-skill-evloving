#!/usr/bin/env python3
"""
Export machine-readable artifacts from an OHSpec RFC directory.

Outputs (in the RFC dir):
  - rfc.digest.json        (always)
  - tasks.json             (optional, --tasks)

Design notes:
  - RFC (`rfc.md`) is the single source of truth for humans.
  - Digest/tasks are derived artifacts; they should not be edited by hand.
  - Parsing is best-effort: if a section/table is missing, it exports an empty list
    rather than crashing, but it will mark stability as "draft".
"""

from __future__ import annotations

import argparse
import hashlib
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
DIGEST_JSON = "rfc.digest.json"
TASKS_JSON = "tasks.json"


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


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


def looks_like_dir(p: str) -> bool:
    try:
        return Path(p).exists() and Path(p).is_dir()
    except OSError:
        return False


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
    # Support escaped pipes "\|" inside cells.
    placeholder = "\u0000"
    s = line.strip().strip("|").replace("\\|", placeholder)
    parts = [p.strip().replace(placeholder, "|") for p in s.split("|")]
    return parts


def parse_markdown_table(lines: Sequence[str], header_index: int) -> Tuple[List[str], List[Dict[str, str]], int]:
    """
    Parse a markdown pipe table starting at header_index.
    Returns: (header_cols, rows, next_index)
    """
    header = _split_md_row(lines[header_index])
    i = header_index + 1
    # Skip separator line(s)
    if i < len(lines) and set(lines[i].replace("|", "").strip()) <= set("-: "):
        i += 1
    rows: List[Dict[str, str]] = []
    while i < len(lines):
        line = lines[i].strip()
        if not line.startswith("|"):
            break
        cols = _split_md_row(line)
        # Pad/truncate to header length
        if len(cols) < len(header):
            cols += [""] * (len(header) - len(cols))
        cols = cols[: len(header)]
        rows.append({header[j]: cols[j] for j in range(len(header))})
        i += 1
    return header, rows, i


def find_table_by_required_columns(rfc_lines: Sequence[str], required_cols: Sequence[str]) -> Optional[List[Dict[str, str]]]:
    required = [c.strip() for c in required_cols]
    for idx, line in enumerate(rfc_lines):
        if not line.lstrip().startswith("|"):
            continue
        header = _split_md_row(line)
        if all(c in header for c in required):
            _, rows, _ = parse_markdown_table(rfc_lines, idx)
            return rows
    return None


REQ_HEADER_RE = re.compile(r"^####\s+Requirement:\s+(REQ-\d{3})\s*(.*)$")
SCN_HEADER_RE = re.compile(r"^####\s+Scenario:\s+(SCN-\d{3})\s*(.*)$")


def extract_title(rfc_text: str) -> str:
    for line in rfc_text.splitlines():
        if line.startswith("# RFC:"):
            return line[len("# RFC:") :].strip()
    return ""


def extract_requirements(rfc_lines: Sequence[str]) -> List[Dict[str, Any]]:
    reqs: List[Dict[str, Any]] = []
    i = 0
    while i < len(rfc_lines):
        m = REQ_HEADER_RE.match(rfc_lines[i].strip())
        if not m:
            i += 1
            continue
        req_id = m.group(1)
        title = m.group(2).strip().strip("[]")
        block: List[str] = []
        i += 1
        while i < len(rfc_lines):
            line = rfc_lines[i]
            if REQ_HEADER_RE.match(line.strip()):
                break
            if line.startswith("### ") or line.startswith("## "):
                break
            block.append(line.rstrip())
            i += 1
        acceptance: List[str] = []
        scenarios: List[str] = []
        statements: List[str] = []
        for bl in block:
            t = bl.strip()
            if t.startswith("- **验收标准**"):
                val = t.split("：", 1)[1].strip() if "：" in t else t
                acceptance.append(val.strip("[]"))
                continue
            if t.startswith("- **覆盖场景**"):
                scenarios = sorted(set(re.findall(r"\bSCN-\d{3}\b", t)))
                continue
            if t.startswith("- "):
                statements.append(t[2:].strip())
            elif t:
                statements.append(t)
        reqs.append(
            {
                "id": req_id,
                "title": title,
                "acceptance": acceptance,
                "scenarios": scenarios,
                "statements": statements,
            }
        )
    return reqs


def extract_scenarios(rfc_lines: Sequence[str]) -> List[Dict[str, Any]]:
    scenarios: List[Dict[str, Any]] = []
    current_type = ""
    i = 0
    while i < len(rfc_lines):
        line = rfc_lines[i].strip()
        if line.startswith("#### 正常场景"):
            current_type = "normal"
        elif line.startswith("#### 异常场景"):
            current_type = "exception"
        elif line.startswith("#### 边界场景"):
            current_type = "boundary"
        elif line.startswith("#### 不支持场景"):
            current_type = "unsupported"

        m = SCN_HEADER_RE.match(line)
        if not m:
            i += 1
            continue
        scn_id = m.group(1)
        title = m.group(2).strip().strip("[]")
        given: List[str] = []
        when: List[str] = []
        then: List[str] = []
        reason = ""
        i += 1
        while i < len(rfc_lines):
            t = rfc_lines[i].strip()
            if SCN_HEADER_RE.match(t) or t.startswith("### ") or t.startswith("## ") or t.startswith("#### 正常场景") or t.startswith("#### 异常场景") or t.startswith("#### 边界场景") or t.startswith("#### 不支持场景"):
                break
            if t.startswith("- **GIVEN**"):
                given.append(t.split("**", 2)[-1].strip().lstrip("*").strip())
            elif t.startswith("- **WHEN**"):
                when.append(t.split("**", 2)[-1].strip().lstrip("*").strip())
            elif t.startswith("- **THEN**"):
                then.append(t.split("**", 2)[-1].strip().lstrip("*").strip())
            elif t.startswith("- **REASON**"):
                reason = t.split("**", 2)[-1].strip().lstrip("*").strip()
            i += 1
        scenarios.append(
            {
                "id": scn_id,
                "type": current_type or "unknown",
                "title": title,
                "given": given,
                "when": when,
                "then": then,
                "reason": reason,
            }
        )
    return scenarios


def extract_review_digest_risk(rfc_lines: Sequence[str]) -> List[Dict[str, str]]:
    # Pull "关键风险" from the "审查速览" table if present.
    risks: List[Dict[str, str]] = []
    in_review = False
    for i, line in enumerate(rfc_lines):
        if "审查速览" in line:
            in_review = True
            continue
        if in_review and line.strip().startswith("|"):
            cols = _split_md_row(line)
            if len(cols) >= 2 and cols[0] == "关键风险":
                val = cols[1].strip()
                if val and val != "[依赖不可用/权限/并发/兼容等]":
                    risks.append({"id": "RISK-001", "summary": val, "mitigation": "", "rollback": ""})
                break
        if in_review and line.strip() == "" and i > 0:
            break
    return risks


def normalize_key_files(key_files: Any) -> List[Dict[str, str]]:
    out: List[Dict[str, str]] = []
    if not isinstance(key_files, list):
        return out
    for item in key_files:
        if isinstance(item, dict):
            out.append(
                {
                    "path": str(item.get("path", "")),
                    "role": str(item.get("role", "")),
                    "reason": str(item.get("reason", "")),
                }
            )
        else:
            out.append({"path": str(item), "role": "", "reason": ""})
    return out


def build_digest(rfc_dir: Path, include_tasks: bool) -> Tuple[Dict[str, Any], Optional[Dict[str, Any]]]:
    rfc_path = rfc_dir / RFC_MD
    findings_path = rfc_dir / FINDINGS_JSON
    progress_path = rfc_dir / PROGRESS_JSON

    rfc_text = read_text(rfc_path)
    rfc_lines = rfc_text.splitlines()
    findings = load_json(findings_path)
    progress = load_json(progress_path)

    title = extract_title(rfc_text)
    meta = progress.get("meta", {}) if isinstance(progress, dict) else {}
    rfc_id = meta.get("rfc_id") or rfc_dir.name
    status = (meta.get("status") or "").upper()

    # Best-effort complexity: prefer RFC metadata table; fallback to dispatcher complexity.
    complexity = ""
    for line in rfc_lines:
        if line.strip().startswith("| complexity |") or line.strip().startswith("| scope |"):
            parts = _split_md_row(line)
            if len(parts) >= 2:
                complexity = parts[1].strip()
            break
    if not complexity:
        complexity = str(findings.get("dispatcher", {}).get("complexity", "")) if isinstance(findings, dict) else ""

    # "approved" should only be used when both progress marks APPROVED and
    # the RFC still contains the required structured sections for downstream agents.
    stability = "approved" if status == "APPROVED" else "draft"

    # Tables
    repo_rows = find_table_by_required_columns(rfc_lines, ["repo_id", "root", "rev", "owner"])
    repos: List[Dict[str, str]] = []
    if repo_rows:
        for row in repo_rows:
            repos.append(
                {
                    "id": row.get("repo_id", "").strip() or row.get("id", "").strip(),
                    "root": row.get("root", "").strip(),
                    "rev": row.get("rev", "").strip(),
                    "owner": row.get("owner", "").strip(),
                    "compat": row.get("兼容范围", "").strip(),
                    "notes": row.get("说明", "").strip(),
                }
            )
    else:
        # Fallback: findings.meta.repos
        for r in findings.get("meta", {}).get("repos", []) or []:
            if isinstance(r, dict):
                repos.append(
                    {
                        "id": str(r.get("id", "")),
                        "root": str(r.get("root", "")),
                        "rev": str(r.get("rev", "")),
                        "owner": str(r.get("owner", "")),
                        "compat": str(r.get("compat", "")),
                        "notes": str(r.get("notes", "")),
                    }
                )

    facts_rows = find_table_by_required_columns(rfc_lines, ["FACT-ID", "事实", "证据锚点"])
    facts: List[Dict[str, Any]] = []
    if facts_rows:
        for row in facts_rows:
            evidence_raw = row.get("证据锚点", "").strip()
            evidence_list = [e for e in re.split(r"[,\s]+", evidence_raw) if e]
            facts.append(
                {
                    "id": row.get("FACT-ID", "").strip(),
                    "fact": row.get("事实", "").strip(),
                    "evidence": evidence_list,
                    "impact": row.get("影响", "").strip(),
                }
            )
    else:
        # Fallback: findings.confirmed.facts
        for f in findings.get("confirmed", {}).get("facts", []) or []:
            if not isinstance(f, dict):
                continue
            facts.append(
                {
                    "id": str(f.get("id", "")),
                    "fact": str(f.get("fact", "")),
                    "evidence": list(f.get("evidence", []) or []),
                    "impact": str(f.get("impact", "")),
                }
            )

    api_rows = find_table_by_required_columns(rfc_lines, ["API-ID", "接口/事件", "层级"])
    field_rows = find_table_by_required_columns(rfc_lines, ["FIELD-ID", "字段", "类型"])
    chg_rows = find_table_by_required_columns(rfc_lines, ["CHG-ID", "变更项", "类型"])
    edge_rows = find_table_by_required_columns(rfc_lines, ["EDGE-ID", "边界/异常", "触发条件"])
    dep_rows = find_table_by_required_columns(rfc_lines, ["DEP-ID", "依赖方", "调用点"])
    tst_rows = find_table_by_required_columns(rfc_lines, ["TST-ID", "场景ID", "用例类型"])
    trace_rows = find_table_by_required_columns(rfc_lines, ["REQ-ID", "SCN-ID", "TST-ID"])

    requirements = extract_requirements(rfc_lines)
    scenarios = extract_scenarios(rfc_lines)
    risks = extract_review_digest_risk(rfc_lines)

    key_files = normalize_key_files(findings.get("confirmed", {}).get("key_files", []))

    warnings: List[str] = []
    if not repos:
        warnings.append("missing_repo_manifest")
    if len(key_files) < 3:
        warnings.append("key_files_lt_3")
    if not facts:
        warnings.append("missing_facts")
    if not requirements:
        warnings.append("missing_requirements")
    if not scenarios:
        warnings.append("missing_scenarios")
    if not (chg_rows or []):
        warnings.append("missing_changes")
    if not (tst_rows or []):
        warnings.append("missing_test_matrix")
    if not (trace_rows or []):
        warnings.append("missing_traceability")

    if stability == "approved" and warnings:
        stability = "draft"

    exported_at = utc_now_iso()
    digest: Dict[str, Any] = {
        "schema_version": "1.0",
        "stability": stability,
        "warnings": warnings,
        "meta": {
            "rfc_id": rfc_id,
            "title": title,
            # Prefer "complexity"; keep "scope" for backward compatibility with older exports.
            "complexity": complexity,
            "scope": complexity,
            "created_at": meta.get("created_at") or "",
            "updated_at": meta.get("updated_at") or "",
            "exported_at": exported_at,
        },
        "repos": repos,
        "anchors": {"key_files": key_files},
        "facts": facts,
        "requirements": [
            {
                "id": r.get("id", ""),
                "title": r.get("title", ""),
                "acceptance": r.get("acceptance", []),
                "scenarios": r.get("scenarios", []),
            }
            for r in requirements
        ],
        "contracts": {
            "apis": [
                {
                    "id": row.get("API-ID", ""),
                    "name": row.get("接口/事件", ""),
                    "layer": row.get("层级", ""),
                    "inputs": row.get("输入/参数", ""),
                    "defaults": row.get("默认值", ""),
                    "outputs": row.get("输出/错误码", ""),
                    "compat": row.get("兼容策略", ""),
                    "notes": row.get("说明", ""),
                }
                for row in (api_rows or [])
            ],
            "fields": [
                {
                    "id": row.get("FIELD-ID", ""),
                    "name": row.get("字段", ""),
                    "type": row.get("类型", ""),
                    "range_unit": row.get("范围/单位", ""),
                    "source": row.get("来源", ""),
                    "default": row.get("默认值", ""),
                    "notes": row.get("说明", ""),
                }
                for row in (field_rows or [])
            ],
        },
        "changes": [
            {
                "id": row.get("CHG-ID", ""),
                "item": row.get("变更项", ""),
                "kind": row.get("类型", ""),
                "existing_ref": row.get("existing_ref", ""),
                "new_change_plan": row.get("new_change_plan", ""),
                "target": row.get("目标落点", ""),
                "compat": row.get("兼容/迁移", ""),
                "test_rollback": row.get("测试/回滚", ""),
            }
            for row in (chg_rows or [])
        ],
        "scenarios": scenarios,
        "edges": [
            {
                "id": row.get("EDGE-ID", ""),
                "case": row.get("边界/异常", ""),
                "trigger": row.get("触发条件", ""),
                "expected": row.get("预期行为", ""),
                "error_code": row.get("错误码", ""),
                "fallback": row.get("回退/恢复", ""),
                "timing_concurrency": row.get("时序/并发说明", ""),
            }
            for row in (edge_rows or [])
        ],
        "dependencies": [
            {
                "id": row.get("DEP-ID", ""),
                "party": row.get("依赖方", ""),
                "callsite": row.get("调用点", ""),
                "failure_mode": row.get("失败模式", ""),
                "fallback": row.get("回退/降级", ""),
                "observability": row.get("观测/告警", ""),
                "impact": row.get("影响范围", ""),
            }
            for row in (dep_rows or [])
        ],
        "tests": {
            "matrix": [
                {
                    "id": row.get("TST-ID", ""),
                    "scenario": row.get("场景ID", ""),
                    "type": row.get("用例类型", ""),
                    "acceptance": row.get("验收指标", ""),
                    "fault_injection": row.get("依赖故障注入", ""),
                    "compat_regression": row.get("兼容回归", ""),
                }
                for row in (tst_rows or [])
            ],
            "traceability": [
                {
                    "req": row.get("REQ-ID", ""),
                    "scn": row.get("SCN-ID", ""),
                    "tst": row.get("TST-ID", ""),
                    "notes": row.get("说明", ""),
                }
                for row in (trace_rows or [])
            ],
        },
        "risks": risks,
        "provenance": {
            "sources": {
                "rfc_md": {"path": RFC_MD, "sha256": sha256_file(rfc_path)},
                "findings_json": {"path": FINDINGS_JSON, "sha256": sha256_file(findings_path)},
                "progress_json": {"path": PROGRESS_JSON, "sha256": sha256_file(progress_path)},
            }
        },
    }

    tasks: Optional[Dict[str, Any]] = None
    if include_tasks:
        tasks_list: List[Dict[str, Any]] = []
        for row in (chg_rows or []):
            chg_id = row.get("CHG-ID", "")
            title_part = row.get("变更项", "") or ""
            tasks_list.append(
                {
                    "id": f"TASK-{chg_id}" if chg_id else f"TASK-{len(tasks_list)+1:03d}",
                    "title": f"{chg_id} {title_part}".strip(),
                    "repo_id": "main",
                    "references": {
                        "changes": [chg_id] if chg_id else [],
                        "requirements": sorted(set(re.findall(r"REQ-\d{3}", title_part))),
                        "scenarios": sorted(set(re.findall(r"SCN-\d{3}", title_part))),
                    },
                    "acceptance": [row.get("测试/回滚", "")] if row.get("测试/回滚") else [],
                    "rollback": "",
                    "notes": "Derived skeleton; refine with RFC before coding.",
                }
            )
        tasks = {
            "schema_version": "1.0",
            "rfc_id": rfc_id,
            "generated_at": exported_at,
            "tasks": tasks_list,
            "provenance": digest["provenance"],
        }

    return digest, tasks


def update_progress_artifacts(progress_path: Path, digest: Dict[str, Any], tasks: Optional[Dict[str, Any]]) -> None:
    progress = load_json(progress_path)
    artifacts = progress.setdefault("artifacts", {})

    src = digest.get("provenance", {}).get("sources", {})
    dig_meta = digest.get("meta", {})
    stability = digest.get("stability")

    artifacts.setdefault("digest", {})
    artifacts["digest"].update(
        {
            "path": DIGEST_JSON,
            "exported_at": dig_meta.get("exported_at"),
            "stability": stability,
            "sources_sha256": {
                "rfc_md": src.get("rfc_md", {}).get("sha256"),
                "findings_json": src.get("findings_json", {}).get("sha256"),
                "progress_json": src.get("progress_json", {}).get("sha256"),
            },
        }
    )

    if tasks is not None:
        artifacts.setdefault("tasks", {})
        artifacts["tasks"].update(
            {
                "path": TASKS_JSON,
                "exported_at": tasks.get("generated_at"),
                "stability": stability,
                "sources_sha256": artifacts["digest"]["sources_sha256"],
            }
        )

    progress["meta"]["updated_at"] = utc_now_iso() if isinstance(progress.get("meta"), dict) else utc_now_iso()
    dump_json(progress_path, progress)


def main(argv: Optional[Sequence[str]] = None) -> int:
    p = argparse.ArgumentParser(description="Export OHSpec RFC digest/tasks JSON.")
    p.add_argument("rfc", help="RFC ID (RFC-...) or RFC directory path")
    p.add_argument("--tasks", action="store_true", help="Also export tasks.json (skeleton)")
    p.add_argument("--force", action="store_true", help="Force rewrite even if inputs unchanged")
    args = p.parse_args(argv)

    try:
        rfc_dir = resolve_rfc_dir(args.rfc)
    except (FileNotFoundError, ValueError) as e:
        print(str(e), file=sys.stderr)
        return 2

    for required in [RFC_MD, FINDINGS_JSON, PROGRESS_JSON]:
        if not (rfc_dir / required).exists():
            print(f"Missing {required} in {rfc_dir}", file=sys.stderr)
            return 2

    digest_path = rfc_dir / DIGEST_JSON
    # Staleness: if digest exists and provenance matches current, skip unless --force.
    if digest_path.exists() and not args.force:
        try:
            existing = load_json(digest_path)
            src = existing.get("provenance", {}).get("sources", {})
            cur = {
                "rfc_md": sha256_file(rfc_dir / RFC_MD),
                "findings_json": sha256_file(rfc_dir / FINDINGS_JSON),
                "progress_json": sha256_file(rfc_dir / PROGRESS_JSON),
            }
            if (
                src.get("rfc_md", {}).get("sha256") == cur["rfc_md"]
                and src.get("findings_json", {}).get("sha256") == cur["findings_json"]
                and src.get("progress_json", {}).get("sha256") == cur["progress_json"]
            ):
                # Inputs unchanged; nothing to do.
                return 0
        except Exception:
            # Fall through to regenerate.
            pass

    digest, tasks = build_digest(rfc_dir, include_tasks=args.tasks)
    dump_json(rfc_dir / DIGEST_JSON, digest)
    if tasks is not None:
        dump_json(rfc_dir / TASKS_JSON, tasks)
    update_progress_artifacts(rfc_dir / PROGRESS_JSON, digest, tasks)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
