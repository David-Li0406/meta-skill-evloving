#!/usr/bin/env python3
import glob
import os
import sys
import xml.etree.ElementTree as ET


def _ns(root):
    if root.tag.startswith("{") and "}" in root.tag:
        return root.tag.split("}")[0][1:]
    return ""


def _q(ns, tag):
    return f"{{{ns}}}{tag}" if ns else tag


def _read_text(node):
    if node is None or node.text is None:
        return ""
    return node.text.strip()


def _snippet(message, stack):
    parts = [p for p in (message, stack) if p]
    raw = "\n".join(parts).strip()
    if not raw:
        return "(no error output captured)"
    lines = raw.splitlines()
    if len(lines) > 20:
        lines = lines[:20] + ["..."]
    snippet = "\n".join(lines)
    if len(snippet) > 2000:
        snippet = snippet[:2000] + "..."
    return snippet


def _parse_trx(path):
    try:
        tree = ET.parse(path)
    except ET.ParseError as exc:
        print(f"Failed to parse TRX {path}: {exc}", file=sys.stderr)
        return []

    root = tree.getroot()
    ns = _ns(root)
    q = lambda tag: _q(ns, tag)

    unit_tests = {}
    for unit_test in root.findall(f".//{q('UnitTest')}"):
        test_id = unit_test.get("id")
        test_name = unit_test.get("name")
        test_method = unit_test.find(q("TestMethod"))
        class_name = test_method.get("className") if test_method is not None else None
        method_name = test_method.get("name") if test_method is not None else None
        if class_name and method_name:
            fqn = f"{class_name}.{method_name}"
        else:
            fqn = test_name or method_name or class_name or "UnknownTest"
        if test_id:
            unit_tests[test_id] = fqn

    failures = []
    for result in root.findall(f".//{q('UnitTestResult')}"):
        if result.get("outcome") != "Failed":
            continue
        test_id = result.get("testId")
        test_name = result.get("testName") or unit_tests.get(test_id) or "UnknownTest"
        fqn = unit_tests.get(test_id) or test_name

        message = _read_text(result.find(f"{q('Output')}/{q('ErrorInfo')}/{q('Message')}"))
        stack = _read_text(result.find(f"{q('Output')}/{q('ErrorInfo')}/{q('StackTrace')}"))
        failures.append(
            {
                "display": test_name,
                "fqn": fqn,
                "snippet": _snippet(message, stack),
            }
        )

    return failures


def _write_outputs(failures, output_md, output_filter):
    with open(output_md, "w", encoding="utf-8") as md:
        md.write("# Test failures\n\n")
        if not failures:
            md.write("No failed tests found.\n")
        else:
            for failure in failures:
                md.write(f"- `{failure['display']}`\n")
                md.write("```\n")
                md.write(f"{failure['snippet']}\n")
                md.write("```\n")

    seen = set()
    names = []
    for failure in failures:
        name = failure["fqn"]
        if name and name not in seen:
            seen.add(name)
            names.append(name)

    expr = "|".join([f"FullyQualifiedName={name}" for name in names]) if names else ""
    with open(output_filter, "w", encoding="utf-8") as filter_file:
        filter_file.write(expr + "\n")


def main():
    if len(sys.argv) != 4:
        print("Usage: collect-test-failures.py <results_dir> <output_md> <output_filter>")
        return 2

    results_dir = sys.argv[1]
    output_md = sys.argv[2]
    output_filter = sys.argv[3]

    trx_files = sorted(glob.glob(os.path.join(results_dir, "*.trx")))
    failures = []
    for trx in trx_files:
        failures.extend(_parse_trx(trx))

    _write_outputs(failures, output_md, output_filter)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
