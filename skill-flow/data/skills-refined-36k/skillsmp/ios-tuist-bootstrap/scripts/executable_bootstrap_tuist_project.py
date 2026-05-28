#!/usr/bin/env python3
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path
import re


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Initialize a Tuist project and apply the ios-tuist-bootstrap template."
    )
    parser.add_argument("--dest", required=True, help="Destination project root.")
    parser.add_argument(
        "--repo-name",
        help="Folder name for the repo (e.g. kebab-case). If set, a new folder is created under --dest.",
    )
    parser.add_argument("--project-name", required=True, help="Project/app name.")
    parser.add_argument(
        "--scheme",
        help="Scheme name (defaults to project name).",
    )
    parser.add_argument(
        "--workspace",
        help="Workspace name (defaults to '<project-name>.xcworkspace').",
    )
    parser.add_argument(
        "--skip-init",
        action="store_true",
        help="Skip `tuist init` (use when the manifest already exists).",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing files when applying template files.",
    )
    return parser.parse_args()


def run(cmd: list[str], cwd: Path) -> None:
    print(f"+ {' '.join(cmd)}")
    subprocess.run(cmd, cwd=cwd, check=True)

def find_matching(text: str, start: int, open_char: str, close_char: str) -> int | None:
    depth = 0
    in_string = False
    escape = False
    for idx in range(start, len(text)):
        ch = text[idx]
        if in_string:
            if escape:
                escape = False
            elif ch == "\\":
                escape = True
            elif ch == '"':
                in_string = False
            continue
        if ch == '"':
            in_string = True
            continue
        if ch == open_char:
            depth += 1
        elif ch == close_char:
            depth -= 1
            if depth == 0:
                return idx
    return None


def patch_project_swift(project_root: Path, project_name: str) -> None:
    manifest = project_root / "Project.swift"
    if not manifest.exists():
        print(f"Warning: {manifest} not found; skipping patch.", file=sys.stderr)
        return

    text = manifest.read_text(encoding="utf-8")
    original = text

    # Insert project-level settings if missing.
    if "settings:" not in text:
        name_match = re.search(r"\bname:\s+\"[^\"]+\",\s*\n", text)
        if name_match:
            insert = (
                "    settings: .settings(\n"
                "        base: SettingsDictionary()\n"
                "            .swiftVersion(\"6.2\")\n"
                "            .merging(\n"
                "                [\n"
                "                    \"SWIFT_STRICT_CONCURRENCY\": \"Complete\",\n"
                "                    \"SWIFT_DEFAULT_ACTOR_ISOLATION\": \"MainActor\",\n"
                "                    \"SWIFT_APPROACHABLE_CONCURRENCY\": \"YES\",\n"
                "                    \"SWIFT_UPCOMING_FEATURE_INFER_ISOLATED_CONFORMANCES\": \"YES\",\n"
                "                    \"SWIFT_UPCOMING_FEATURE_NONISOLATED_NONSENDING_BY_DEFAULT\": \"YES\",\n"
                "                ],\n"
                "                uniquingKeysWith: { _, new in new }\n"
                "            )\n"
                "    ),\n"
            )
            text = text[: name_match.end()] + insert + text[name_match.end() :]

    # Insert fileHeaderTemplate/resourceSynthesizers if missing.
    if "fileHeaderTemplate:" not in text or "resourceSynthesizers:" not in text:
        targets_idx = text.find("targets:")
        if targets_idx != -1:
            list_start = text.find("[", targets_idx)
            list_end = find_matching(text, list_start, "[", "]") if list_start != -1 else None
            if list_end is not None:
                suffix = text[list_end + 1 :]
                next_non_ws = next((c for c in suffix if not c.isspace()), "")
                comma = "" if next_non_ws == "," else ","
                insert = (
                    f"{comma}\n"
                    "    fileHeaderTemplate: .string(\"// TODO: Remove this comment\"),\n"
                    "    resourceSynthesizers: .default + [.files(extensions: [\"json\"])],\n"
                )
                text = text[: list_end + 1] + insert + text[list_end + 1 :]

    # Insert build scripts into the main app target.
    if "Script/swiftlint.sh" not in text or "Script/swift-format-changed.sh" not in text:
        for match in re.finditer(r"\.target\s*\(", text):
            start = match.end() - 1
            end = find_matching(text, start, "(", ")")
            if end is None:
                continue
            block = text[start : end + 1]
            if f'name: "{project_name}"' not in block:
                continue
            if "product: .app" not in block:
                continue

            indent = " " * 12
            scripts_block = (
                f"{indent}scripts: [\n"
                f"{indent}    .pre(\n"
                f"{indent}        path: .path(\"Script/swift-format-changed.sh\"),\n"
                f"{indent}        name: \"SwiftFormat\",\n"
                f"{indent}        basedOnDependencyAnalysis: false\n"
                f"{indent}    ),\n"
                f"{indent}    .pre(\n"
                f"{indent}        path: .path(\"Script/swiftlint.sh\"),\n"
                f"{indent}        name: \"SwiftLint\",\n"
                f"{indent}        basedOnDependencyAnalysis: false\n"
                f"{indent}    )\n"
                f"{indent}],\n"
            )
            dep_match = re.search(r"\n(\s*)dependencies:\s*\[", block)
            if dep_match and "scripts:" not in block:
                insert_at = dep_match.start()
                block = block[:insert_at] + "\n" + scripts_block + block[insert_at:]
                text = text[:start] + block + text[end + 1 :]
            break

    if text != original:
        manifest.write_text(text, encoding="utf-8")
        print(f"Patched {manifest}")


def main() -> int:
    args = parse_args()
    dest_root = Path(args.dest).expanduser().resolve()
    if args.repo_name:
        dest_root = dest_root / args.repo_name
    project_name = args.project_name
    scheme = args.scheme or project_name
    workspace = args.workspace or f"{project_name}.xcworkspace"

    dest_root.mkdir(parents=True, exist_ok=True)

    if not args.skip_init:
        if shutil.which("mise"):
            run(["mise", "x", "tuist@latest", "--", "tuist", "init"], dest_root)
        else:
            print("Warning: mise not found; running `tuist init` directly.", file=sys.stderr)
            run(["tuist", "init"], dest_root)

    target_root = dest_root
    candidate = dest_root / project_name
    if candidate.exists() and not (dest_root / "Project.swift").exists():
        extras = [p for p in dest_root.iterdir() if p.name != candidate.name]
        if extras:
            target_root = candidate
            print(f"Using generated project directory: {target_root}")
        else:
            temp_dir = dest_root / ".tuist-tmp"
            if temp_dir.exists():
                raise RuntimeError(f"Temp directory already exists: {temp_dir}")
            candidate.rename(temp_dir)
            for item in temp_dir.iterdir():
                shutil.move(str(item), dest_root)
            temp_dir.rmdir()
            target_root = dest_root
            print(f"Flattened generated project into: {target_root}")

    script_root = Path(__file__).resolve().parent
    apply_script = script_root / "apply_template.py"
    if not apply_script.exists():
        print(f"Missing apply_template.py at {apply_script}", file=sys.stderr)
        return 1

    cmd = [
        sys.executable,
        str(apply_script),
        "--dest",
        str(target_root),
        "--project-name",
        project_name,
        "--scheme",
        scheme,
        "--workspace",
        workspace,
    ]
    if args.force or not args.skip_init:
        cmd.append("--force")

    run(cmd, dest_root)
    patch_project_swift(target_root, project_name)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
