#!/usr/bin/env python3
"""
Sync GitHub Copilot agents, prompts, and docs to project folders.

Usage:
    python sync_agents.py --target /path/to/project
    python sync_agents.py --target /path/to/project --agents noctis,lunafreya,ignis
    python sync_agents.py --target /path/to/project --prompts-only
    python sync_agents.py --target /path/to/project --docs-only
    python sync_agents.py --list
"""

import argparse
import re
import shutil
import sys
from pathlib import Path

# Markers for AGENTS.md sync
START_MARKER = "<!-- SOFTWARE DEVELOPMENT POLICIES:START -->"
END_MARKER = "<!-- SOFTWARE DEVELOPMENT POLICIES:END -->"


def get_skill_root() -> Path:
    """Get the root directory of this skill."""
    return Path(__file__).parent.parent


def get_available_agents() -> list[str]:
    """Get list of available agent files."""
    agents_dir = get_skill_root() / "agents"
    if not agents_dir.exists():
        return []
    return [f.stem.replace(".agent", "") for f in agents_dir.glob("*.agent.md")]


def get_available_prompts() -> list[str]:
    """Get list of available prompt files."""
    prompts_dir = get_skill_root() / "prompts"
    if not prompts_dir.exists():
        return []
    return [f.stem for f in prompts_dir.glob("*.prompt.md")]


def get_available_docs() -> list[str]:
    """Get list of available documentation files."""
    docs_dir = get_skill_root() / "docs" / "policies"
    if not docs_dir.exists():
        return []
    return [f.name for f in docs_dir.glob("*.md")]


def list_items():
    """List all available agents, prompts, and docs."""
    print("Available Agents:")
    print("-" * 40)
    for agent in sorted(get_available_agents()):
        print(f"  - {agent}")
    
    print("\nAvailable Prompts:")
    print("-" * 40)
    for prompt in sorted(get_available_prompts()):
        print(f"  - {prompt}")
    
    print("\nAvailable Docs:")
    print("-" * 40)
    for doc in sorted(get_available_docs()):
        print(f"  - {doc}")


def sync_files(
    source_dir: Path,
    target_dir: Path,
    pattern: str,
    selected: list[str] | None,
    force: bool,
    dry_run: bool,
) -> int:
    """Sync files from source to target directory."""
    if not source_dir.exists():
        print(f"Source directory not found: {source_dir}")
        return 0
    
    target_dir.mkdir(parents=True, exist_ok=True)
    synced = 0
    
    for source_file in source_dir.glob(pattern):
        name = source_file.stem.replace(".prompt", "").replace(".agent", "")
        
        if selected and name not in selected:
            continue
        
        target_file = target_dir / source_file.name
        
        if target_file.exists() and not force:
            if dry_run:
                print(f"[SKIP] {target_file} (exists, use --force to overwrite)")
            else:
                response = input(f"Overwrite {target_file}? [y/N] ").strip().lower()
                if response != "y":
                    print(f"[SKIP] {target_file}")
                    continue
        
        if dry_run:
            print(f"[SYNC] {source_file.name} -> {target_file}")
        else:
            shutil.copy2(source_file, target_file)
            print(f"[SYNC] {source_file.name} -> {target_file}")
        
        synced += 1
    
    return synced


def sync_agents_md(
    skill_root: Path,
    target_root: Path,
    dry_run: bool,
) -> bool:
    """Sync AGENTS.md content between markers or create new file if not exists."""
    source_file = skill_root / "AGENTS.md"
    target_file = target_root / "AGENTS.md"
    
    if not source_file.exists():
        print(f"Source AGENTS.md not found: {source_file}")
        return False
    
    # Read source content
    source_content = source_file.read_text(encoding="utf-8")
    
    # If target doesn't exist, create it with template
    if not target_file.exists():
        if dry_run:
            print(f"[CREATE] {target_file} (with policy section)")
            return True
        
        template = f"""# Guidelines

{START_MARKER}
{source_content}
{END_MARKER}
"""
        target_file.write_text(template, encoding="utf-8")
        print(f"[CREATE] {target_file} (with policy section)")
        return True
    
    # Read target content
    target_content = target_file.read_text(encoding="utf-8")
    
    # Check if markers exist
    if START_MARKER in target_content and END_MARKER in target_content:
        # Replace content between markers
        pattern = re.escape(START_MARKER) + r".*?" + re.escape(END_MARKER)
        replacement = f"{START_MARKER}\n{source_content}\n{END_MARKER}"
        new_content = re.sub(pattern, replacement, target_content, flags=re.DOTALL)
        
        if dry_run:
            print(f"[UPDATE] {target_file} (between markers)")
            return True
        
        target_file.write_text(new_content, encoding="utf-8")
        print(f"[UPDATE] {target_file} (between markers)")
        return True
    else:
        # Markers don't exist, append to end of file
        if dry_run:
            print(f"[APPEND] {target_file} (add policy section at end)")
            return True
        
        # Add newlines if file doesn't end with one
        if not target_content.endswith("\n"):
            target_content += "\n"
        
        target_content += f"\n{START_MARKER}\n{source_content}\n{END_MARKER}\n"
        target_file.write_text(target_content, encoding="utf-8")
        print(f"[APPEND] {target_file} (add policy section at end)")
        return True


def main():
    parser = argparse.ArgumentParser(
        description="Sync GitHub Copilot agents, prompts, and docs to project folders"
    )
    parser.add_argument(
        "--target",
        type=Path,
        help="Target project directory",
    )
    parser.add_argument(
        "--agents",
        type=str,
        help="Comma-separated list of agents to sync (noctis,lunafreya,ignis,gladiolus,aranea,prompto,ardyn)",
    )
    parser.add_argument(
        "--prompts",
        type=str,
        help="Comma-separated list of prompts to sync",
    )
    parser.add_argument(
        "--docs",
        type=str,
        help="Comma-separated list of docs to sync (or sync all if not specified)",
    )
    parser.add_argument(
        "--agents-only",
        action="store_true",
        help="Sync only agents, skip prompts and docs",
    )
    parser.add_argument(
        "--prompts-only",
        action="store_true",
        help="Sync only prompts, skip agents and docs",
    )
    parser.add_argument(
        "--docs-only",
        action="store_true",
        help="Sync only docs, skip agents and prompts",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing files without confirmation",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be synced without making changes",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List available agents, prompts, and docs",
    )
    
    args = parser.parse_args()
    
    if args.list:
        list_items()
        return 0
    
    if not args.target:
        print("Error: --target is required for sync operations")
        parser.print_help()
        return 1
    
    if not args.target.exists():
        print(f"Error: Target directory does not exist: {args.target}")
        return 1
    
    skill_root = get_skill_root()
    total_synced = 0
    
    # Parse selected items
    selected_agents = args.agents.split(",") if args.agents else None
    selected_prompts = args.prompts.split(",") if args.prompts else None
    selected_docs = args.docs.split(",") if args.docs else None
    
    # Sync agents
    if not args.prompts_only and not args.docs_only:
        print("\n=== Syncing Agents ===")
        agents_synced = sync_files(
            source_dir=skill_root / "agents",
            target_dir=args.target / ".github" / "agents",
            pattern="*.agent.md",
            selected=selected_agents,
            force=args.force,
            dry_run=args.dry_run,
        )
        print(f"Agents synced: {agents_synced}")
        total_synced += agents_synced
    
    # Sync prompts
    if not args.agents_only and not args.docs_only:
        print("\n=== Syncing Prompts ===")
        prompts_synced = sync_files(
            source_dir=skill_root / "prompts",
            target_dir=args.target / ".github" / "prompts",
            pattern="*.prompt.md",
            selected=selected_prompts,
            force=args.force,
            dry_run=args.dry_run,
        )
        print(f"Prompts synced: {prompts_synced}")
        total_synced += prompts_synced
    
    # Sync docs
    if not args.agents_only and not args.prompts_only:
        print("\n=== Syncing Docs ===")
        docs_synced = sync_files(
            source_dir=skill_root / "docs" / "policies",
            target_dir=args.target / "docs" / "policies",
            pattern="*.md",
            selected=selected_docs,
            force=args.force,
            dry_run=args.dry_run,
        )
        print(f"Docs synced: {docs_synced}")
        total_synced += docs_synced
    
    # Sync AGENTS.md (always run by default)
    print("\n=== Syncing AGENTS.md ===")
    agents_md_synced = sync_agents_md(
        skill_root=skill_root,
        target_root=args.target,
        dry_run=args.dry_run,
    )
    if agents_md_synced:
        total_synced += 1
    
    print(f"\n=== Total files synced: {total_synced} ===")
    
    if args.dry_run:
        print("\n(Dry run - no files were actually modified)")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
