#!/usr/bin/env bash
set -euo pipefail

repo_root="$(pwd)"

if ! command -v rg >/dev/null 2>&1; then
  echo "rg is required but not found." >&2
  exit 1
fi

if ! command -v dotnet >/dev/null 2>&1; then
  echo "dotnet is required but not found." >&2
  exit 1
fi

if ! command -v python3 >/dev/null 2>&1; then
  echo "python3 is required but not found." >&2
  exit 1
fi

solutions=$(rg --files -g "*.sln" -g "*.slnx")
if [ -z "$solutions" ]; then
  echo "No .sln or .slnx files found." >&2
  exit 1
fi

primary_sln=$(printf '%s\n' "$solutions" | python3 -c 'import sys
lines = [line.strip() for line in sys.stdin if line.strip()]
root = [line for line in lines if "/" not in line]
print(sorted(root)[0] if root else sorted(lines, key=len)[0])
')

solution_dir=$(dirname "$primary_sln")
projects=$(dotnet sln "$primary_sln" list | awk '/\.csproj$/ {print $0}')
if [ -z "$projects" ]; then
  echo "No projects found in solution: $primary_sln" >&2
  exit 1
fi

tmpfile=$(mktemp)
trap 'rm -f "$tmpfile"' EXIT

printf '%s\n' "$projects" | python3 - "$solution_dir" "$repo_root" <<'PY' >> "$tmpfile"
import os
import sys
import xml.etree.ElementTree as ET
import json
import subprocess

solution_dir = sys.argv[1]
repo_root = sys.argv[2]

def normalize_path(path):
    if os.path.isabs(path):
        return os.path.normpath(path)
    return os.path.normpath(os.path.join(solution_dir, path))

def relpath(path):
    return os.path.relpath(path, repo_root)

def parse_project(path):
    frameworks = []
    is_test = False
    try:
        result = subprocess.run(
            [
                "dotnet",
                "msbuild",
                path,
                "-nologo",
                "-getProperty:TargetFramework",
                "-getProperty:TargetFrameworks",
                "-getProperty:IsTestProject",
                "-getItem:PackageReference",
            ],
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode == 0:
            payload = json.loads(result.stdout)
            props = payload.get("Properties", {})
            tfm = (props.get("TargetFramework") or "").strip()
            tfms = (props.get("TargetFrameworks") or "").strip()
            if tfms:
                frameworks = [t.strip() for t in tfms.split(";") if t.strip()]
            elif tfm:
                frameworks = [tfm]
            is_test = (props.get("IsTestProject") or "").strip().lower() in ("true", "1", "yes")
            if not is_test:
                items = payload.get("Items", {}).get("PackageReference", [])
                for item in items:
                    if (item.get("Identity") or "").lower() == "microsoft.net.test.sdk":
                        is_test = True
                        break
            return frameworks, is_test
    except Exception:
        pass

    try:
        tree = ET.parse(path)
        root = tree.getroot()

        def tag_name(tag):
            return tag.split('}', 1)[-1]

        for elem in root.iter():
            name = tag_name(elem.tag)
            text = (elem.text or "").strip()
            if name == "TargetFramework" and text:
                frameworks = [text]
            elif name == "TargetFrameworks" and text:
                frameworks = [t.strip() for t in text.split(';') if t.strip()]
            elif name == "IsTestProject" and text:
                if text.lower() in ("true", "1", "yes"):
                    is_test = True
    except Exception:
        frameworks = []
        is_test = False
    return frameworks, is_test

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    proj_path = normalize_path(line)
    frameworks, is_test = parse_project(proj_path)
    print("\t".join([relpath(proj_path), ";".join(frameworks), "true" if is_test else "false"]))
PY

python3 - "$primary_sln" "$tmpfile" "$repo_root" <<'PY'
import json
from pathlib import Path
import sys

sln = sys.argv[1]
rows_path = sys.argv[2]
repo_root = sys.argv[3]
projects = []

with open(rows_path, "r", encoding="utf-8") as handle:
    for line in handle:
        line = line.rstrip("\n")
        if not line:
            continue
        path, tfms, is_test = line.split("\t")
        frameworks = [t for t in tfms.split(";") if t]
        projects.append({
            "path": path,
            "targetFrameworks": frameworks,
            "isTestProject": is_test == "true",
        })

payload = {
    "solution": str(Path(sln).resolve().relative_to(Path(repo_root).resolve())),
    "projects": projects,
}

out_dir = Path("artifacts/codex")
out_dir.mkdir(parents=True, exist_ok=True)

json_path = out_dir / "solution-map.json"
json_path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")

md_lines = [
    "# Solution Map",
    "",
    f"Solution: `{payload['solution']}`",
    "",
    "| Project | TargetFramework(s) | IsTestProject |",
    "| --- | --- | --- |",
]

for proj in projects:
    tfm_text = ", ".join(proj["targetFrameworks"]) if proj["targetFrameworks"] else "-"
    is_test = "true" if proj["isTestProject"] else "false"
    md_lines.append(f"| `{proj['path']}` | {tfm_text} | {is_test} |")

md_path = out_dir / "solution-map.md"
md_path.write_text("\n".join(md_lines) + "\n", encoding="utf-8")
PY

echo "Wrote artifacts/codex/solution-map.json"
echo "Wrote artifacts/codex/solution-map.md"
