#!/usr/bin/env python3
"""
Agent Skills CLI - Manage skills for AI coding assistants.

Commands:
    skills list              List registered skills
    skills add <path>        Add a skill from a directory with SKILL.md
    skills remove <name>     Remove a skill
    skills sync              Sync skills to all CLIs (Codex, Claude, Cursor)
    skills sync <cli>        Sync to specific CLI
    skills scan <path>       Scan directory for SKILL.md files
    skills auto <path>       Scan and auto-register new skills
    skills info <name>       Show skill details
"""
import argparse
import json
import sys
from pathlib import Path

from .discovery import (
    list_skills,
    add_skill,
    remove_skill,
    sync_to_cli,
    sync_all_clis,
    scan_for_skills,
    auto_register_from_scan,
    get_skill_info,
    SKILLS_DIR,
    CLI_SKILL_DIRS,
)


def cmd_list(args):
    """List all registered skills."""
    skills = list_skills()
    
    if args.json:
        print(json.dumps(skills, indent=2))
        return 0
    
    if not skills:
        print(f"No skills registered in {SKILLS_DIR}")
        print(f"\nAdd skills with: skills add <path-to-skill>")
        print(f"Or scan for skills: skills scan ~/scripts/modules")
        return 0
    
    print(f"Registered Skills ({len(skills)}):\n")
    for s in skills:
        name = s.get("registered_name", s.get("name", "unknown"))
        desc = s.get("description", "No description")[:60]
        version = s.get("metadata", {}).get("version") if isinstance(s.get("metadata"), dict) else s.get("version", "")
        ver_str = f" v{version}" if version else ""
        print(f"  {name}{ver_str}")
        print(f"    {desc}...")
        print(f"    → {s.get('path')}")
        print()
    
    return 0


def cmd_add(args):
    """Add a skill."""
    success, msg = add_skill(args.path, args.name)
    print(msg)
    
    if success and args.sync:
        results = sync_all_clis()
        for r in results:
            print(f"  {r}")
    
    return 0 if success else 1


def cmd_remove(args):
    """Remove a skill."""
    success, msg = remove_skill(args.name)
    print(msg)
    return 0 if success else 1


def cmd_sync(args):
    """Sync skills to CLI directories."""
    if args.cli:
        success, msg = sync_to_cli(args.cli)
        print(msg)
        return 0 if success else 1
    else:
        results = sync_all_clis()
        for r in results:
            print(r)
        return 0


def cmd_scan(args):
    """Scan directory for skills."""
    skills = scan_for_skills(args.path)
    
    if args.json:
        print(json.dumps(skills, indent=2))
        return 0
    
    if not skills:
        print(f"No SKILL.md files found in {args.path}")
        return 0
    
    print(f"Found {len(skills)} skills in {args.path}:\n")
    for s in skills:
        name = s.get("name", "unknown")
        registered = "✓" if s.get("is_registered") else "✗"
        desc = s.get("description", "")[:50]
        print(f"  [{registered}] {name}")
        print(f"      {desc}...")
        print(f"      {s.get('path')}")
        print()
    
    unregistered = [s for s in skills if not s.get("is_registered")]
    if unregistered:
        print(f"To register {len(unregistered)} new skills: skills auto {args.path}")
    
    return 0


def cmd_auto(args):
    """Auto-register skills from scan."""
    results = auto_register_from_scan(args.path)
    
    if not results:
        print("No new skills to register.")
        return 0
    
    for r in results:
        print(r)
    
    if args.sync:
        print("\nSyncing to CLIs...")
        sync_results = sync_all_clis()
        for r in sync_results:
            print(f"  {r}")
    
    return 0


def cmd_info(args):
    """Show skill details."""
    info = get_skill_info(args.name)
    
    if not info:
        print(f"Skill '{args.name}' not found")
        return 1
    
    if args.json:
        print(json.dumps(info, indent=2))
        return 0
    
    print(f"Skill: {info.get('name', args.name)}")
    print(f"Path: {info.get('path')}")
    if info.get("description"):
        print(f"\nDescription:\n  {info['description']}")
    if info.get("compatibility"):
        print(f"\nCompatibility: {info['compatibility']}")
    if info.get("metadata"):
        print(f"\nMetadata: {json.dumps(info['metadata'], indent=2)}")
    
    return 0


def main():
    parser = argparse.ArgumentParser(
        description="Manage skills for AI coding assistants (Codex, Claude, Cursor)",
        prog="skills"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Command")
    
    # list
    p_list = subparsers.add_parser("list", help="List registered skills")
    p_list.add_argument("-j", "--json", action="store_true", help="Output as JSON")
    p_list.set_defaults(func=cmd_list)
    
    # add
    p_add = subparsers.add_parser("add", help="Add a skill")
    p_add.add_argument("path", help="Path to skill directory (must contain SKILL.md)")
    p_add.add_argument("-n", "--name", help="Override skill name")
    p_add.add_argument("-s", "--sync", action="store_true", help="Sync to CLIs after adding")
    p_add.set_defaults(func=cmd_add)
    
    # remove
    p_remove = subparsers.add_parser("remove", help="Remove a skill")
    p_remove.add_argument("name", help="Skill name")
    p_remove.set_defaults(func=cmd_remove)
    
    # sync
    p_sync = subparsers.add_parser("sync", help="Sync skills to CLI directories")
    p_sync.add_argument("cli", nargs="?", choices=list(CLI_SKILL_DIRS.keys()), help="Specific CLI (default: all)")
    p_sync.set_defaults(func=cmd_sync)
    
    # scan
    p_scan = subparsers.add_parser("scan", help="Scan directory for SKILL.md files")
    p_scan.add_argument("path", help="Directory to scan")
    p_scan.add_argument("-j", "--json", action="store_true", help="Output as JSON")
    p_scan.set_defaults(func=cmd_scan)
    
    # auto
    p_auto = subparsers.add_parser("auto", help="Scan and auto-register new skills")
    p_auto.add_argument("path", help="Directory to scan")
    p_auto.add_argument("-s", "--sync", action="store_true", help="Sync to CLIs after registering")
    p_auto.set_defaults(func=cmd_auto)
    
    # info
    p_info = subparsers.add_parser("info", help="Show skill details")
    p_info.add_argument("name", help="Skill name")
    p_info.add_argument("-j", "--json", action="store_true", help="Output as JSON")
    p_info.set_defaults(func=cmd_info)
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
