#!/usr/bin/env python
"""Diagnose issues in AgRAG headless outputs and propose fixes.

Usage:
  python diagnose_headless_output.py <output_file>

Works with:
- JSON output files (one JSON object per response)
- JSONL stream output files (stream-json events)
- Batch outputs that include {"type": "prompt"} markers
"""

from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set


ENTITY_PATTERNS = {
    "TestCase": r"TC_[A-Z]+_\d+",
    "Requirement": r"REQ_[A-Z]+_\d+",
    "Function": r"FUNC_[A-Za-z_]+(?:_\d+)?",
    "Class": r"CLASS_[A-Za-z_]+(?:_\d+)?",
    "Module": r"MOD_[A-Za-z_.]+(?:_\d+)?",
    "ChangeRequest": r"CR_[A-Z]+_\d+",
    "File": r"FILE_[A-Za-z0-9_]+",
    "Component": r"COMP_[A-Za-z0-9_]+",
}

RELATIONSHIP_TYPES = {
    "TOUCHES",
    "DEFINED_IN",
    "PART_OF",
    "COVERS",
    "VERIFIES",
}

TOOL_NAMES = {"vector_search", "keyword_search", "hybrid_search", "graph_traverse"}


@dataclass
class Record:
    prompt: str = ""
    response: str = ""
    tool_calls: Set[str] = field(default_factory=set)
    tool_results: Set[str] = field(default_factory=set)
    stats: Dict[str, object] = field(default_factory=dict)
    session_id: Optional[str] = None


@dataclass
class Issue:
    code: str
    message: str
    fix: str


def _iter_json_objects(path: str) -> List[dict]:
    objects: List[dict] = []
    with open(path, "r", encoding="utf-8") as handle:
        content = handle.read().strip()
        if not content:
            return objects

        lines = content.splitlines()
        for line in lines:
            line = line.strip()
            if not line:
                continue
            try:
                objects.append(json.loads(line))
            except json.JSONDecodeError:
                # Ignore non-JSON lines
                continue
    return objects


def _determine_target(prompt: str) -> Optional[str]:
    lowered = prompt.lower()
    if "function" in lowered:
        return "Function"
    if "requirement" in lowered or "req_" in lowered:
        return "Requirement"
    if "component" in lowered:
        return "Component"
    if "module" in lowered:
        return "Module"
    if "class" in lowered:
        return "Class"
    if "file" in lowered:
        return "File"
    if "change request" in lowered or "cr_" in lowered:
        return "ChangeRequest"
    if "test" in lowered or "tc_" in lowered:
        return "TestCase"
    return None


def _extract_entity_ids(text: str) -> Dict[str, List[str]]:
    results: Dict[str, List[str]] = {}
    for entity_type, pattern in ENTITY_PATTERNS.items():
        matches = re.findall(pattern, text or "")
        if matches:
            results[entity_type] = list(dict.fromkeys(matches))
    return results


def _extract_relationship_labels(text: str) -> Set[str]:
    labels = set()
    for match in re.findall(r"\-\[([A-Za-z0-9_]+)\]\-", text or ""):
        labels.add(match.upper())
    return labels


def _parse_evidence_lines(text: str) -> List[str]:
    lines = []
    for line in (text or "").splitlines():
        if "source:" in line:
            lines.append(line.strip())
    return lines


def _detect_issues(record: Record) -> List[Issue]:
    issues: List[Issue] = []

    if not record.response.strip():
        issues.append(
            Issue(
                code="empty_response",
                message="No assistant response captured.",
                fix="Re-run with a fresh thread id or increase MAX_TOOL_CALLS; inspect stream-json for tool results.",
            )
        )

    # Tool result mismatch (stream-json only)
    if record.tool_calls and record.tool_results:
        missing = record.tool_calls - record.tool_results
        if missing:
            issues.append(
                Issue(
                    code="missing_tool_results",
                    message=f"Missing tool_result events for {len(missing)} tool call(s).",
                    fix="Check MAX_TOOL_CALLS/MAX_MODEL_CALLS limits and ensure graph reaches execute_tools.",
                )
            )
    elif record.tool_calls and not record.tool_results:
        issues.append(
            Issue(
                code="no_tool_results",
                message="Tool calls were issued but no tool results were captured.",
                fix="Re-run with stream-json and verify tool execution; ensure counters are reset per prompt.",
            )
        )

    # Entity type mismatch
    target = _determine_target(record.prompt)
    entities = _extract_entity_ids(record.response)
    if target and not entities.get(target):
        issues.append(
            Issue(
                code="entity_type_mismatch",
                message=f"Prompt targets {target} but response contains no {target} IDs.",
                fix="Adjust retrieval to filter by entity type and use 'Ranked Results' for the requested entity.",
            )
        )

    # Relationship labels outside ontology
    rel_labels = _extract_relationship_labels(record.response)
    invalid = {label for label in rel_labels if label not in RELATIONSHIP_TYPES}
    if invalid:
        issues.append(
            Issue(
                code="invalid_relationship_labels",
                message=f"Response includes non-ontology relationship labels: {', '.join(sorted(invalid))}.",
                fix="Ensure graph_traverse outputs relationship types and only cite those in Graph Paths.",
            )
        )

    # Evidence uses tool names without entity IDs
    evidence_lines = _parse_evidence_lines(record.response)
    for line in evidence_lines:
        if any(tool in line for tool in TOOL_NAMES):
            if not _extract_entity_ids(line):
                issues.append(
                    Issue(
                        code="tool_only_evidence",
                        message="Evidence cites tool name without entity ID.",
                        fix="Cite entity IDs from tool output; keep tool name only if no IDs appear.",
                    )
                )
                break

    # Tool errors from stats (json output)
    tools = record.stats.get("tools") if record.stats else None
    if isinstance(tools, dict):
        total_fail = tools.get("totalFail")
        if isinstance(total_fail, int) and total_fail > 0:
            issues.append(
                Issue(
                    code="tool_failures",
                    message=f"{total_fail} tool call(s) failed.",
                    fix="Inspect tool outputs and logs; retry with narrower queries or check DB connectivity.",
                )
            )

    return issues


def _print_report(records: List[Record]) -> int:
    total_issues = 0
    for idx, record in enumerate(records, 1):
        issues = _detect_issues(record)
        total_issues += len(issues)
        prompt = record.prompt or "<missing prompt>"
        print(f"Prompt {idx}: {prompt}")
        if not issues:
            print("- No issues detected.")
            print("")
            continue
        for issue in issues:
            print(f"- Issue: {issue.message}")
            print(f"  Fix: {issue.fix}")
        print("")

    if total_issues:
        print("Detected issues. Review fixes and confirm before applying changes.")
        return 2

    print("No issues detected.")
    return 0


def _build_records(objects: List[dict]) -> List[Record]:
    records: List[Record] = []
    current: Optional[Record] = None

    for obj in objects:
        if not isinstance(obj, dict):
            continue

        obj_type = obj.get("type")
        if obj_type == "prompt":
            current = Record(prompt=obj.get("content", ""))
            records.append(current)
            continue

        if obj_type == "message" and obj.get("role") == "user":
            current = Record(prompt=obj.get("content", ""), session_id=obj.get("session_id"))
            records.append(current)
            continue

        if obj_type == "tool_use":
            if current is None:
                current = Record()
                records.append(current)
            tool_id = str(obj.get("tool_id", ""))
            if tool_id:
                current.tool_calls.add(tool_id)
            continue

        if obj_type == "tool_result":
            if current is None:
                current = Record()
                records.append(current)
            tool_id = str(obj.get("tool_id", ""))
            if tool_id:
                current.tool_results.add(tool_id)
            continue

        if obj_type == "result":
            if current is None:
                current = Record()
                records.append(current)
            current.response = obj.get("response", "") or ""
            current.stats = obj.get("stats", {}) or {}
            current.session_id = obj.get("session_id") or current.session_id
            continue

        # JSON output format
        if "response" in obj and "stats" in obj:
            if current is None:
                current = Record()
                records.append(current)
            current.response = obj.get("response", "") or ""
            current.stats = obj.get("stats", {}) or {}
            continue

    return records


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: python diagnose_headless_output.py <output_file>")
        return 1

    path = sys.argv[1]
    objects = _iter_json_objects(path)
    if not objects:
        print("No JSON objects found in output file.")
        return 1

    records = _build_records(objects)
    if not records:
        print("No records found to analyze.")
        return 1

    return _print_report(records)


if __name__ == "__main__":
    raise SystemExit(main())
