#!/usr/bin/env python3
"""
Claude Tools Installation Script

Discovers and installs Claude tools (skills, agents, commands) from this repository
to either global (~/.claude/) or project (.claude/) locations.

Usage:
    uv run install.py --list              # Show available tools
    uv run install.py --install           # Install tools interactively
        --target global|project           # Target location
        --mode copy|symlink               # Installation mode
        --tools tool1,tool2,...           # Tools to install (comma-separated)
"""

import argparse
import json
import shutil
import sys
from pathlib import Path
from typing import TypedDict


class ToolComponents(TypedDict):
    """Components found within a tool directory."""
    skill: bool  # Has skills/SKILL.md
    scripts: bool  # Has skills/scripts/
    references: bool  # Has skills/references/
    assets: bool  # Has skills/assets/
    agents: list[str]  # List of agent .md files
    commands: list[str]  # List of command .md files


class ToolInfo(TypedDict):
    """Information about a discovered tool."""
    name: str
    path: Path
    components: ToolComponents


def find_repo_root() -> Path:
    """Find the repository root by looking for CLAUDE.md or .git."""
    current = Path(__file__).resolve().parent

    # Walk up looking for markers
    while current != current.parent:
        if (current / "CLAUDE.md").exists() or (current / ".git").exists():
            return current
        current = current.parent

    # Fall back to parent of .claude directory
    script_path = Path(__file__).resolve()
    # .claude/skills/install/install.py -> go up 4 levels
    return script_path.parents[3]


def discover_tools(repo_root: Path) -> dict[str, ToolInfo]:
    """
    Scan repository for tools.

    A tool is a top-level directory (excluding .claude, hidden dirs) that contains
    at least one of: skills/, agents/, commands/
    """
    tools: dict[str, ToolInfo] = {}

    # Directories to skip
    skip_dirs = {".claude", ".git", ".github", "__pycache__", "node_modules", ".venv", "venv"}

    for item in repo_root.iterdir():
        # Skip non-directories and hidden/excluded directories
        if not item.is_dir():
            continue
        if item.name.startswith(".") or item.name in skip_dirs:
            continue

        components = detect_components(item)

        # Only include if it has at least one component
        has_components = (
            components["skill"] or
            components["scripts"] or
            components["references"] or
            components["assets"] or
            components["agents"] or
            components["commands"]
        )

        if has_components:
            tools[item.name] = {
                "name": item.name,
                "path": item,
                "components": components,
            }

    return tools


def detect_components(tool_dir: Path) -> ToolComponents:
    """Detect all component types within a tool directory."""
    skills_dir = tool_dir / "skills"
    agents_dir = tool_dir / "agents"
    commands_dir = tool_dir / "commands"

    components: ToolComponents = {
        "skill": False,
        "scripts": False,
        "references": False,
        "assets": False,
        "agents": [],
        "commands": [],
    }

    # Check skills directory
    if skills_dir.exists():
        components["skill"] = (skills_dir / "SKILL.md").exists()
        components["scripts"] = (skills_dir / "scripts").is_dir()
        components["references"] = (skills_dir / "references").is_dir()
        components["assets"] = (skills_dir / "assets").is_dir()

    # Check agents directory
    if agents_dir.exists():
        components["agents"] = [
            f.name for f in agents_dir.glob("*.md")
            if f.is_file()
        ]

    # Check commands directory (legacy format)
    if commands_dir.exists():
        components["commands"] = [
            f.name for f in commands_dir.glob("*.md")
            if f.is_file()
        ]

    return components


def format_tool_list(tools: dict[str, ToolInfo]) -> str:
    """Format tools for display."""
    if not tools:
        return "No tools found in this repository."

    lines = ["Available tools:\n"]

    for name in sorted(tools.keys()):
        info = tools[name]
        comp = info["components"]

        lines.append(f"  {name}/")

        # Show skill components
        if comp["skill"] or comp["scripts"] or comp["references"] or comp["assets"]:
            skill_parts = []
            if comp["skill"]:
                skill_parts.append("SKILL.md")
            if comp["scripts"]:
                skill_parts.append("scripts/")
            if comp["references"]:
                skill_parts.append("references/")
            if comp["assets"]:
                skill_parts.append("assets/")
            lines.append(f"    skills/ [{', '.join(skill_parts)}]")

        # Show agents
        if comp["agents"]:
            agents_str = ", ".join(comp["agents"])
            lines.append(f"    agents/ [{agents_str}]")

        # Show commands
        if comp["commands"]:
            cmds_str = ", ".join(comp["commands"])
            lines.append(f"    commands/ [{cmds_str}]")

        lines.append("")  # Blank line between tools

    return "\n".join(lines)


def resolve_target(target: str) -> Path:
    """Resolve target name to actual path."""
    if target == "global":
        return Path.home() / ".claude"
    elif target == "project":
        return Path.cwd() / ".claude"
    else:
        # Treat as explicit path
        return Path(target).expanduser()


def install_skill(tool_info: ToolInfo, target_dir: Path, mode: str) -> list[str]:
    """
    Install a skill to the target directory.

    Copies/symlinks the entire skills/ tree to {target}/skills/{tool_name}/
    """
    messages = []
    source_skills = tool_info["path"] / "skills"

    if not source_skills.exists():
        return messages

    dest_skills = target_dir / "skills" / tool_info["name"]

    # Ensure parent directory exists
    dest_skills.parent.mkdir(parents=True, exist_ok=True)

    # Remove existing if present
    if dest_skills.exists() or dest_skills.is_symlink():
        if dest_skills.is_symlink():
            dest_skills.unlink()
        else:
            shutil.rmtree(dest_skills)

    if mode == "symlink":
        dest_skills.symlink_to(source_skills.resolve())
        messages.append(f"  Linked skills/{tool_info['name']}/ -> {source_skills}")
    else:
        shutil.copytree(source_skills, dest_skills)
        messages.append(f"  Copied skills/{tool_info['name']}/")

    return messages


def install_agents(tool_info: ToolInfo, target_dir: Path, mode: str) -> list[str]:
    """
    Install agents to the target directory.

    Copies/symlinks agent .md files flat to {target}/agents/
    """
    messages = []
    source_agents = tool_info["path"] / "agents"

    if not source_agents.exists():
        return messages

    dest_agents = target_dir / "agents"
    dest_agents.mkdir(parents=True, exist_ok=True)

    for agent_file in source_agents.glob("*.md"):
        dest_file = dest_agents / agent_file.name

        # Remove existing if present
        if dest_file.exists() or dest_file.is_symlink():
            dest_file.unlink()

        if mode == "symlink":
            dest_file.symlink_to(agent_file.resolve())
            messages.append(f"  Linked agents/{agent_file.name}")
        else:
            shutil.copy2(agent_file, dest_file)
            messages.append(f"  Copied agents/{agent_file.name}")

    return messages


def install_commands(tool_info: ToolInfo, target_dir: Path, mode: str) -> list[str]:
    """
    Install commands to the target directory.

    Copies/symlinks command .md files flat to {target}/commands/
    """
    messages = []
    source_commands = tool_info["path"] / "commands"

    if not source_commands.exists():
        return messages

    dest_commands = target_dir / "commands"
    dest_commands.mkdir(parents=True, exist_ok=True)

    for cmd_file in source_commands.glob("*.md"):
        dest_file = dest_commands / cmd_file.name

        # Remove existing if present
        if dest_file.exists() or dest_file.is_symlink():
            dest_file.unlink()

        if mode == "symlink":
            dest_file.symlink_to(cmd_file.resolve())
            messages.append(f"  Linked commands/{cmd_file.name}")
        else:
            shutil.copy2(cmd_file, dest_file)
            messages.append(f"  Copied commands/{cmd_file.name}")

    return messages


def install_tool(tool_info: ToolInfo, target_dir: Path, mode: str) -> list[str]:
    """Install all components of a tool."""
    messages = []
    messages.append(f"\nInstalling {tool_info['name']}...")

    # Install skill (entire directory tree)
    if tool_info["components"]["skill"]:
        messages.extend(install_skill(tool_info, target_dir, mode))

    # Install agents (flat)
    if tool_info["components"]["agents"]:
        messages.extend(install_agents(tool_info, target_dir, mode))

    # Install commands (flat)
    if tool_info["components"]["commands"]:
        messages.extend(install_commands(tool_info, target_dir, mode))

    return messages


def main():
    parser = argparse.ArgumentParser(
        description="Discover and install Claude tools",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "--list",
        action="store_true",
        help="List available tools and their components",
    )

    parser.add_argument(
        "--install",
        action="store_true",
        help="Install selected tools",
    )

    parser.add_argument(
        "--target",
        choices=["global", "project"],
        help="Installation target: global (~/.claude/) or project (.claude/)",
    )

    parser.add_argument(
        "--mode",
        choices=["copy", "symlink"],
        help="Installation mode: copy files or create symlinks",
    )

    parser.add_argument(
        "--tools",
        type=str,
        help="Comma-separated list of tool names to install",
    )

    parser.add_argument(
        "--json",
        action="store_true",
        help="Output in JSON format (for --list)",
    )

    args = parser.parse_args()

    # Find repository root
    repo_root = find_repo_root()

    # Discover tools
    tools = discover_tools(repo_root)

    if args.list:
        if args.json:
            # JSON output for programmatic use
            output = {
                "repo_root": str(repo_root),
                "tools": {
                    name: {
                        "path": str(info["path"]),
                        "components": {
                            "skill": info["components"]["skill"],
                            "scripts": info["components"]["scripts"],
                            "references": info["components"]["references"],
                            "assets": info["components"]["assets"],
                            "agents": info["components"]["agents"],
                            "commands": info["components"]["commands"],
                        }
                    }
                    for name, info in tools.items()
                }
            }
            print(json.dumps(output, indent=2))
        else:
            print(format_tool_list(tools))
        return 0

    if args.install:
        # Validate required arguments
        if not args.target:
            print("Error: --target is required for --install", file=sys.stderr)
            return 1
        if not args.mode:
            print("Error: --mode is required for --install", file=sys.stderr)
            return 1
        if not args.tools:
            print("Error: --tools is required for --install", file=sys.stderr)
            return 1

        # Parse tool names
        tool_names = [t.strip() for t in args.tools.split(",")]

        # Validate tool names
        invalid_tools = [t for t in tool_names if t not in tools]
        if invalid_tools:
            print(f"Error: Unknown tools: {', '.join(invalid_tools)}", file=sys.stderr)
            print(f"Available tools: {', '.join(tools.keys())}", file=sys.stderr)
            return 1

        # Resolve target directory
        target_dir = resolve_target(args.target)

        print(f"Installing to: {target_dir}")
        print(f"Mode: {args.mode}")

        # Install each tool
        all_messages = []
        for tool_name in tool_names:
            messages = install_tool(tools[tool_name], target_dir, args.mode)
            all_messages.extend(messages)

        # Print results
        for msg in all_messages:
            print(msg)

        print("\nInstallation complete!")
        return 0

    # No action specified
    parser.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
