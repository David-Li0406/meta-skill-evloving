#!/usr/bin/env python3
import argparse
import json
import os
import re
import shutil
import sys
from typing import Dict, Tuple

PROFILE_LIMITS = {
    "codex": {"name_max": 100, "desc_max": 500, "name_re": None},
    "claude": {"name_max": 64, "desc_max": 1024, "name_re": re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")},
    "opencode": {"name_max": 64, "desc_max": 1024, "name_re": re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")},
    "universal": {"name_max": 64, "desc_max": 500, "name_re": re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")},
}

DEFAULT_INSTALL_DIRS = {
    "codex": os.path.expanduser("~/.codex/skills"),
    "claude": os.path.expanduser("~/.claude/skills"),
    "opencode": os.path.expanduser("~/.config/opencode/skills"),
    "universal": os.path.expanduser("~/.codex/skills"),
}


def split_frontmatter(text: str) -> Tuple[str, str]:
    lines = text.splitlines(keepends=True)
    if not lines or lines[0].strip() != "---":
        raise ValueError("SKILL.md must start with '---' frontmatter")
    end_idx = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end_idx = i
            break
    if end_idx is None:
        raise ValueError("SKILL.md frontmatter not closed with '---'")
    frontmatter = "".join(lines[1:end_idx])
    body = "".join(lines[end_idx + 1 :])
    return frontmatter, body


def parse_frontmatter(frontmatter: str) -> Dict[str, str]:
    try:
        import yaml  # type: ignore

        data = yaml.safe_load(frontmatter) or {}
        if not isinstance(data, dict):
            raise ValueError("Frontmatter must be a mapping")
        return data
    except Exception:
        data: Dict[str, str] = {}
        for line in frontmatter.splitlines():
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue
            match = re.match(r"^([A-Za-z0-9_-]+)\s*:\s*(.*)$", line)
            if not match:
                continue
            key, value = match.group(1), match.group(2).strip()
            if len(value) >= 2 and value[0] == value[-1] and value[0] in ('"', "'"):
                value = value[1:-1]
            data[key] = value
        return data


def normalize_name(name: str) -> str:
    name = name.strip().lower()
    name = re.sub(r"[^a-z0-9-]+", "-", name)
    name = re.sub(r"-+", "-", name).strip("-")
    return name


def yaml_quote(value: str) -> str:
    return json.dumps(value, ensure_ascii=True)


def validate_name(name: str, profile: str) -> None:
    limits = PROFILE_LIMITS[profile]
    if not name:
        raise ValueError("name is required")
    if len(name) > limits["name_max"]:
        raise ValueError(f"name exceeds {limits['name_max']} characters")
    name_re = limits["name_re"]
    if name_re and not name_re.match(name):
        raise ValueError("name does not match required pattern")


def validate_description(desc: str, profile: str) -> None:
    limits = PROFILE_LIMITS[profile]
    if not desc:
        raise ValueError("description is required")
    if len(desc) > limits["desc_max"]:
        raise ValueError(f"description exceeds {limits['desc_max']} characters")


def write_skill_md(dest_dir: str, name: str, description: str, body: str) -> None:
    skill_md_path = os.path.join(dest_dir, "SKILL.md")
    with open(skill_md_path, "w", encoding="utf-8") as f:
        f.write("---\n")
        f.write(f"name: {yaml_quote(name)}\n")
        f.write(f"description: {yaml_quote(description)}\n")
        f.write("---\n")
        if body and not body.startswith("\n"):
            f.write("\n")
        f.write(body)


def copy_skill(src_dir: str, dest_dir: str, overwrite: bool) -> None:
    if os.path.abspath(src_dir) == os.path.abspath(dest_dir):
        raise ValueError("destination cannot be the same as source")
    if os.path.exists(dest_dir):
        if not overwrite:
            raise ValueError(f"destination already exists: {dest_dir}")
        shutil.rmtree(dest_dir)
    shutil.copytree(src_dir, dest_dir)


def main() -> int:
    parser = argparse.ArgumentParser(description="Transcode skills across agent formats")
    parser.add_argument("--src", required=True, help="Source skill directory (contains SKILL.md)")
    parser.add_argument(
        "--target",
        required=True,
        choices=sorted(PROFILE_LIMITS.keys()),
        help="Target profile",
    )
    parser.add_argument("--out", help="Destination directory for the transcoded skill")
    parser.add_argument("--install", action="store_true", help="Install into the default agent directory")
    parser.add_argument("--install-dir", help="Override default install directory")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite destination if it exists")
    parser.add_argument("--normalize-name", action="store_true", help="Normalize name to lowercase hyphenated")
    parser.add_argument(
        "--truncate-description",
        action="store_true",
        help="Truncate description to fit the target profile",
    )
    parser.add_argument("--dry-run", action="store_true", help="Show actions without writing")
    args = parser.parse_args()

    src_dir = os.path.abspath(args.src)
    if not os.path.isdir(src_dir):
        print(f"Source directory does not exist: {src_dir}", file=sys.stderr)
        return 2
    skill_md = os.path.join(src_dir, "SKILL.md")
    if not os.path.isfile(skill_md):
        print(f"SKILL.md not found in {src_dir}", file=sys.stderr)
        return 2

    with open(skill_md, "r", encoding="utf-8") as f:
        content = f.read()

    frontmatter, body = split_frontmatter(content)
    data = parse_frontmatter(frontmatter)
    name = str(data.get("name", "")).strip()
    description = str(data.get("description", "")).strip()

    if args.normalize_name:
        name = normalize_name(name)

    description = re.sub(r"\s+", " ", description).strip()

    if args.truncate_description and description:
        max_len = PROFILE_LIMITS[args.target]["desc_max"]
        if len(description) > max_len:
            description = description[:max_len].rstrip()

    try:
        validate_name(name, args.target)
        validate_description(description, args.target)
    except ValueError as exc:
        print(f"Validation error: {exc}", file=sys.stderr)
        return 2

    if args.install and args.out:
        print("Use either --install or --out, not both", file=sys.stderr)
        return 2

    if args.install:
        base_dir = args.install_dir or DEFAULT_INSTALL_DIRS[args.target]
        dest_dir = os.path.join(os.path.abspath(os.path.expanduser(base_dir)), name)
    elif args.out:
        dest_dir = os.path.abspath(os.path.expanduser(args.out))
    else:
        print("Provide --out or --install", file=sys.stderr)
        return 2

    if args.dry_run:
        print(f"Source: {src_dir}")
        print(f"Target profile: {args.target}")
        print(f"Destination: {dest_dir}")
        return 0

    os.makedirs(os.path.dirname(dest_dir), exist_ok=True)
    copy_skill(src_dir, dest_dir, args.overwrite)
    write_skill_md(dest_dir, name, description, body)

    print(dest_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
