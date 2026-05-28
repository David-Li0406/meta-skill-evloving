#!/usr/bin/env python
"""
AgentSkillOS CLI.

Usage:
    python run.py                              # Start Web UI (default)
    python run.py webui                        # Start Web UI (explicit)
    python run.py webui --port 8080            # Specify port
    python run.py webui --no-browser           # Don't auto-open browser
    python run.py build                        # Build capability tree
    python run.py build -g top500              # Build tree for specific skill group
    python run.py cli --task tasks.yaml         # Run tasks from YAML config
    python run.py cli -T tasks.yaml --parallel 3  # Override parallel count
    python run.py cli -T tasks.yaml --dry-run  # Preview mode

    # Override plugins via CLI
    python run.py --manager vector
    python run.py --manager vector --orchestrator free-style
    python run.py build --manager vector
    python run.py webui --manager vector
"""

import argparse
import os
import sys
from pathlib import Path
from typing import Optional

from rich.console import Console

# Load unified config (triggers .env loading and validates config.yaml)
import config  # noqa: F401
from config import get_config
from constants import SKILL_GROUPS, SKILL_GROUP_ALIASES

console = Console()


# =============================================================================
# Web UI Command
# =============================================================================

def cmd_ui(args):
    """Launch Web UI."""
    from web.app import run_server

    cfg = get_config({"port": args.port})

    console.print(f"Starting Web UI at http://127.0.0.1:{cfg.port}")
    console.print("Press Ctrl+C to stop")

    run_server(
        host="127.0.0.1",
        port=cfg.port,
        open_browser=not args.no_browser,
    )


# =============================================================================
# Helpers for dormant index building
# =============================================================================

def _build_dormant_vector_index(dormant_index_path: Path) -> None:
    """Build dormant vector index from dormant_index.yaml."""
    console.print(f"\n[dim]Building dormant vector index...[/dim]")
    try:
        from manager.tree.dormant_indexer import DormantIndexBuilder
        builder = DormantIndexBuilder(dormant_index_path=dormant_index_path)
        result = builder.build()
        status = "cached" if result["cached"] else "built"
        console.print(f"[green]Dormant vector index {status}: {result['total_skills']} skills[/green]")
    except ValueError as e:
        console.print(f"[yellow]Skipping dormant vector index: {e}[/yellow]")


def _scan_dormant_directory(dormant_dir: Path, output_parent: Path) -> Optional[Path]:
    """Scan dormant skills dir and write dormant_index.yaml. Returns index path."""
    from manager.tree.layer_processor import build_dormant_index_from_directory, atomic_yaml_write

    console.print(f"[dim]Scanning dormant skills directory: {dormant_dir}[/dim]")
    dormant_index = build_dormant_index_from_directory(dormant_dir)
    dormant_index_path = output_parent / "dormant_index.yaml"
    atomic_yaml_write(dormant_index_path, dormant_index.to_dict())
    console.print(f"[green]Dormant index: {dormant_index.skills_count} skills[/green]")
    return dormant_index_path


# =============================================================================
# Build Command
# =============================================================================

def cmd_build(args):
    """Build capability tree from skill_seeds."""
    from manager import create_manager
    from config import get_config

    cfg = get_config()

    # Resolve skill group (from -g flag or config default)
    group_id = args.skill_group or cfg.skill_group
    resolved_group = SKILL_GROUP_ALIASES.get(group_id, group_id)
    group = next((g for g in SKILL_GROUPS if g["id"] == resolved_group), None)

    skills_dir = None
    output_path = None
    vector_db_path = None

    if group:
        skills_dir = group["skills_dir"]
        output_path = group["tree_path"]
        vector_db_path = group.get("vector_db_path")
        console.print(f"[dim]Building for skill group: {resolved_group}[/dim]")
    elif args.skill_group:
        console.print(f"[red]Unknown skill group: {args.skill_group}[/red]")
        sys.exit(1)

    manager = create_manager(vector_db_path=vector_db_path)
    manager.build(
        skills_dir=skills_dir,
        output_path=output_path,
        verbose=args.verbose,
        show_tree=not args.quiet,
        generate_html=not args.no_html,
    )

    # Directory-based dormant index: scan dormant_skills_dir from config
    layering_cfg = cfg.layering_config()
    if layering_cfg.is_directory_mode and layering_cfg.dormant_skills_dir and output_path:
        from config import PROJECT_ROOT
        dormant_dir = PROJECT_ROOT / layering_cfg.dormant_skills_dir
        if dormant_dir.exists():
            dormant_index_path = _scan_dormant_directory(dormant_dir, Path(output_path).parent)
            _build_dormant_vector_index(dormant_index_path)
        else:
            console.print(f"[yellow]Warning: dormant_skills_dir not found: {dormant_dir}[/yellow]")

    # Post-process with layering if install-count mode is enabled
    if layering_cfg.is_install_count_mode and output_path:
        from manager.tree.layer_processor import LayerPostProcessor

        tree_path = Path(output_path)
        if tree_path.exists():
            console.print(f"\n[dim]Running layering post-processing...[/dim]")

            processor = LayerPostProcessor(config=layering_cfg)
            output = processor.process(tree_path)

            # Determine output paths (same directory as tree)
            output_dir = tree_path.parent
            active_tree_path = output_dir / "active_tree.yaml"
            dormant_index_path = output_dir / "dormant_index.yaml"

            # Save output
            output.save(active_tree_path, dormant_index_path)

            console.print(f"\n[bold green]Layering complete![/bold green]")
            console.print(f"  Total skills: {output.stats['total_skills']}")
            console.print(f"  Active skills: {output.stats['active_skills']} (threshold: {output.stats['threshold']})")
            console.print(f"  Dormant skills: {output.stats['dormant_skills']}")
            console.print(f"  Pinned skills: {output.stats['pinned_skills']}")
            console.print(f"\n[dim]Output files:[/dim]")
            console.print(f"  Active tree: {active_tree_path}")
            console.print(f"  Dormant index: {dormant_index_path}")

            # Automatically build dormant vector index
            _build_dormant_vector_index(dormant_index_path)


def cmd_update_layer(args):
    """Update active/dormant sets from latest install data."""
    from config import get_config

    cfg = get_config()
    layering_cfg = cfg.layering_config()

    # Resolve skill group (from -g flag or config default)
    group_id = args.skill_group or cfg.skill_group
    resolved_group = SKILL_GROUP_ALIASES.get(group_id, group_id)
    group = next((g for g in SKILL_GROUPS if g["id"] == resolved_group), None)

    if not group:
        console.print(f"[red]Unknown skill group: {group_id}[/red]")
        sys.exit(1)

    tree_path = Path(group["tree_path"])
    if not tree_path.exists():
        console.print(f"[red]Tree file not found: {tree_path}[/red]")
        console.print("[dim]Run 'python run.py build' first to generate the tree.[/dim]")
        sys.exit(1)

    console.print(f"[dim]Updating layering for skill group: {resolved_group}[/dim]")

    # Directory-based mode: re-scan the dormant directory
    if layering_cfg.is_directory_mode:
        from config import PROJECT_ROOT
        if not layering_cfg.dormant_skills_dir:
            console.print("[red]dormant_skills_dir not configured for directory mode[/red]")
            sys.exit(1)
        dormant_dir = PROJECT_ROOT / layering_cfg.dormant_skills_dir
        if not dormant_dir.exists():
            console.print(f"[red]Dormant skills directory not found: {dormant_dir}[/red]")
            sys.exit(1)

        dormant_index_path = _scan_dormant_directory(dormant_dir, tree_path.parent)
        _build_dormant_vector_index(dormant_index_path)
        return

    # Install-count based: use ScheduledUpdater
    if not layering_cfg.is_install_count_mode:
        console.print("[yellow]Layering is disabled in config.[/yellow]")
        console.print("[dim]Enable with: layering.mode: install-count (or directory) in config.yaml[/dim]")
        sys.exit(0)

    from manager.tree.scheduled_updater import run_update

    result = run_update(tree_path, verbose=args.verbose)

    if result.success:
        console.print(f"[green]Update successful![/green]")

        # Rebuild dormant vector index
        dormant_index_path = tree_path.parent / "dormant_index.yaml"
        if dormant_index_path.exists():
            _build_dormant_vector_index(dormant_index_path)
    else:
        console.print(f"[red]Update failed: {result.error}[/red]")
        sys.exit(1)


# =============================================================================

# Run Command (Execute tasks from YAML configuration)
# =============================================================================

def cmd_run(args):
    """Execute tasks from YAML configuration."""
    from workflow.loader import TaskLoader
    from workflow.executor import BatchExecutor

    config_path = Path(args.task)
    if not config_path.exists():
        console.print(f"[red]Task file not found: {args.task}[/red]")
        sys.exit(1)

    # Load configuration
    loader = TaskLoader()
    batch_config = loader.load_batch_config(config_path)

    # Validate configuration
    errors = loader.validate_batch_config(batch_config)
    if errors:
        console.print("[red]Configuration errors:[/red]")
        for error in errors:
            console.print(f"  - {error}")
        sys.exit(1)

    # Override from CLI
    if args.parallel is not None:
        batch_config.parallel = args.parallel
    if args.output_dir:
        batch_config.output_dir = args.output_dir

    # --resume: scan completed tasks and filter remaining
    prior_results = []
    total_override = None
    if args.resume:
        from workflow.loader import scan_completed_tasks
        from workflow.models import TaskResult, TaskStatus
        from datetime import datetime as _dt

        resume_dir = Path(args.resume).resolve()
        if not resume_dir.is_dir():
            console.print(f"[red]Resume directory not found: {args.resume}[/red]")
            sys.exit(1)

        completed_map = scan_completed_tasks(resume_dir)

        # Override batch_id and output_dir to reuse the existing directory
        batch_config.batch_id = resume_dir.name
        batch_config.output_dir = str(resume_dir.parent)

        # Save original task list, then filter out completed
        original_tasks = list(batch_config.tasks)
        original_task_ids = {t.task_id for t in original_tasks}
        total_override = len(original_tasks)

        # Build prior_results from completed scan (only for tasks in current config)
        for task_id, data in completed_map.items():
            if task_id not in original_task_ids:
                continue
            meta = data["meta"]
            started = None
            completed_at = None
            if meta.get("started_at"):
                try:
                    started = _dt.fromisoformat(meta["started_at"])
                except (ValueError, TypeError):
                    pass
            if meta.get("completed_at"):
                try:
                    completed_at = _dt.fromisoformat(meta["completed_at"])
                except (ValueError, TypeError):
                    pass
            duration = (completed_at - started).total_seconds() if started and completed_at else 0.0
            tr = TaskResult(
                task_id=task_id,
                status=TaskStatus.COMPLETED,
                run_id=data.get("run_id"),
                started_at=started,
                completed_at=completed_at,
                duration_seconds=duration,
                skills_used=meta.get("skills", []),
                summary="Resumed from prior run",
                evaluation=data.get("evaluation"),
            )
            prior_results.append(tr)

        # Filter out completed tasks
        completed_ids = {tr.task_id for tr in prior_results}
        batch_config.tasks = [t for t in original_tasks if t.task_id not in completed_ids]

        # Print resume summary
        console.print(f"[bold cyan]Resume:[/bold cyan] {resume_dir}")
        console.print(f"  Previously completed: [green]{len(prior_results)}[/green]")
        console.print(f"  Remaining: [yellow]{len(batch_config.tasks)}[/yellow]")
        console.print()

        if not batch_config.tasks:
            console.print("[green]All tasks already completed. Nothing to do.[/green]")
            sys.exit(0)

    # Show summary
    console.print(f"[bold]Run: {batch_config.batch_id}[/bold]")
    console.print(f"Tasks: {len(batch_config.tasks)}")
    console.print(f"Parallel: {batch_config.parallel}")
    console.print(f"Output: {batch_config.output_dir}")
    console.print()

    if args.dry_run:
        console.print("[yellow]Dry run mode - tasks will not be executed[/yellow]")
        console.print()

    # Execute
    executor = BatchExecutor(
        batch_config,
        console=console,
        dry_run=args.dry_run,
        prior_results=prior_results if prior_results else None,
        total_override=total_override,
    )
    result = executor.run()

    # Exit with appropriate code
    if result.failed > 0:
        sys.exit(1)


# =============================================================================
# Claude Code Profile
# =============================================================================

_CC_PROFILE_ENV_MAP = {
    "default_model": "ANTHROPIC_MODEL",
    "opus": "ANTHROPIC_DEFAULT_OPUS_MODEL",
    "sonnet": "ANTHROPIC_DEFAULT_SONNET_MODEL",
    "haiku": "ANTHROPIC_DEFAULT_HAIKU_MODEL",
    "base_url": "ANTHROPIC_BASE_URL",
    "auth_token": "ANTHROPIC_API_KEY",
}


def _apply_cc_profile(profiles_path: str, profile_name: str = None):
    """Load Claude Code profile and inject env vars."""
    import yaml as _yaml

    path = Path(profiles_path)
    if not path.exists():
        console.print(f"[red]CC profiles file not found: {profiles_path}[/red]")
        sys.exit(1)

    with open(path, encoding="utf-8") as f:
        try:
            data = _yaml.safe_load(f) or {}
        except _yaml.YAMLError as e:
            console.print(f"[red]Failed to parse {profiles_path}: {e}[/red]")
            sys.exit(1)

    profiles = data.get("profiles", {})
    if not profiles:
        console.print(f"[red]No profiles defined in {profiles_path}[/red]")
        sys.exit(1)

    name = profile_name or data.get("active")
    if not name:
        console.print("[red]No active profile set and --cc-profile not specified[/red]")
        sys.exit(1)

    profile = profiles.get(name)
    if not profile:
        available = ", ".join(profiles.keys())
        console.print(f"[red]Profile '{name}' not found. Available: {available}[/red]")
        sys.exit(1)

    # Clear all Claude Code env vars first
    for env_key in _CC_PROFILE_ENV_MAP.values():
        os.environ.pop(env_key, None)

    # Set env vars from profile fields
    for field, env_key in _CC_PROFILE_ENV_MAP.items():
        value = profile.get(field)
        if value is not None:
            expanded = os.path.expandvars(str(value))
            if "${" in expanded:
                console.print(
                    f"[yellow]Warning: {env_key} contains unexpanded variable: {expanded}[/yellow]"
                )
            os.environ[env_key] = expanded

    # Log
    desc = profile.get("description", "")
    console.print(f"[dim]CC Profile: {name} — {desc}[/dim]")
    for field, env_key in _CC_PROFILE_ENV_MAP.items():
        value = os.environ.get(env_key)
        if value is None:
            continue
        display = "****" if ("TOKEN" in env_key or "KEY" in env_key) else value
        console.print(f"[dim]  {env_key}={display}[/dim]")


# =============================================================================
# Main Entry Point
# =============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="AgentSkillOS - Intelligent Task Orchestration",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Start Web UI (default or explicit)
  python run.py
  python run.py webui
  python run.py webui --port 8080
  python run.py webui --no-browser

  # Build capability tree
  python run.py build
  python run.py build -g top500

  # Run tasks from YAML config
  python run.py cli --task tasks.yaml
  python run.py cli -T tasks.yaml --parallel 3
  python run.py cli -T tasks.yaml --dry-run

  # Override plugins
  python run.py --manager vector
  python run.py --manager vector --orchestrator free-style
  python run.py build --manager vector
        """,
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # -------------------------------------------------------------------------
    # Default: Web UI (when no subcommand)
    # -------------------------------------------------------------------------
    parser.add_argument("--config", "-C", default=None, metavar="PATH",
                        help="Path to config.yaml (default: config/config.yaml)")
    parser.add_argument("--port", type=int, default=None,
                        help="Web UI port (default: from config.yaml)")
    parser.add_argument("--no-browser", action="store_true",
                        help="Don't open browser automatically")
    parser.add_argument("--manager", "-m", default=None,
                        help="Override manager plugin (e.g., 'tree', 'vector')")
    parser.add_argument("--orchestrator", default=None,
                        help="Override orchestrator plugin (e.g., 'dag', 'free-style')")
    parser.add_argument("--cc-profiles", default=None, metavar="PATH",
                        help="Path to Claude Code profiles YAML (model/provider switching)")
    parser.add_argument("--cc-profile", default=None, metavar="NAME",
                        help="Override active profile name from cc-profiles file")

    # -------------------------------------------------------------------------
    # Subcommand: build
    # -------------------------------------------------------------------------
    build_parser = subparsers.add_parser("build", help="Build capability tree")
    build_parser.add_argument("--skill-group", "-g",
                              help="Skill group to build (e.g., 'skill_seeds', 'top500')")
    build_parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    build_parser.add_argument("--quiet", "-q", action="store_true", help="Don't show tree")
    build_parser.add_argument("--no-html", action="store_true", help="Skip HTML generation")
    build_parser.add_argument("--manager", "-m", default=None,
                              help="Override manager plugin (e.g., 'tree', 'vector')")
    build_parser.add_argument("--config", "-C", default=None, metavar="PATH",
                              help="Path to config.yaml")
    build_parser.set_defaults(func=cmd_build)

    # -------------------------------------------------------------------------
    # Subcommand: update-layer (refresh active/dormant sets from latest data)
    # -------------------------------------------------------------------------
    update_layer_parser = subparsers.add_parser("update-layer",
                                                 help="Update active/dormant sets from latest install data")
    update_layer_parser.add_argument("--skill-group", "-g",
                                      help="Skill group to update (e.g., 'skill_seeds', 'top500')")
    update_layer_parser.add_argument("--verbose", "-v", action="store_true",
                                      help="Show detailed update report")
    update_layer_parser.add_argument("--config", "-C", default=None, metavar="PATH",
                                      help="Path to config.yaml")
    update_layer_parser.set_defaults(func=cmd_update_layer)

    # -------------------------------------------------------------------------
    # Subcommand: cli (execute tasks from YAML config)
    # -------------------------------------------------------------------------
    run_parser = subparsers.add_parser("cli", help="Run tasks from YAML configuration")
    run_parser.add_argument("--task", "-T", required=True, metavar="PATH",
                            help="Path to YAML task config file")
    run_parser.add_argument("--parallel", "-p", type=int, metavar="N",
                            help="Override parallel task count")
    run_parser.add_argument("--output-dir", "-o", metavar="PATH",
                            help="Override output directory")
    run_parser.add_argument("--resume", "-R", metavar="PATH",
                            help="Resume interrupted batch from given directory")
    run_parser.add_argument("--dry-run", action="store_true",
                            help="Preview mode (don't execute tasks)")
    run_parser.add_argument("--verbose", "-v", action="store_true",
                            help="Show detailed logs in terminal")
    run_parser.add_argument("--manager", "-m", default=None,
                            help="Override manager plugin (e.g., 'tree', 'vector')")
    run_parser.add_argument("--orchestrator", default=None,
                            help="Override orchestrator plugin (e.g., 'dag', 'free-style')")
    run_parser.add_argument("--config", "-C", default=None, metavar="PATH",
                            help="Path to config.yaml")
    run_parser.add_argument("--cc-profiles", default=None, metavar="PATH",
                            help="Path to Claude Code profiles YAML")
    run_parser.add_argument("--cc-profile", default=None, metavar="NAME",
                            help="Override active profile name")
    run_parser.set_defaults(func=cmd_run)

    # -------------------------------------------------------------------------
    # Subcommand: webui (explicit Web UI launch)
    # -------------------------------------------------------------------------
    webui_parser = subparsers.add_parser("webui", help="Launch Web UI")
    webui_parser.add_argument("--port", type=int, default=None,
                              help="Web UI port (default: from config.yaml)")
    webui_parser.add_argument("--no-browser", action="store_true",
                              help="Don't open browser automatically")
    webui_parser.add_argument("--manager", "-m", default=None,
                              help="Override manager plugin (e.g., 'tree', 'vector')")
    webui_parser.add_argument("--orchestrator", default=None,
                              help="Override orchestrator plugin (e.g., 'dag', 'free-style')")
    webui_parser.add_argument("--config", "-C", default=None, metavar="PATH",
                              help="Path to config.yaml")
    webui_parser.set_defaults(func=cmd_ui)

    # -------------------------------------------------------------------------
    # Parse arguments
    # -------------------------------------------------------------------------
    args = parser.parse_args()

    # Initialize config and logging (pass CLI overrides)
    cli_overrides = {}
    if getattr(args, "manager", None):
        cli_overrides["manager"] = args.manager
    if getattr(args, "orchestrator", None):
        cli_overrides["orchestrator"] = args.orchestrator
    config_path = getattr(args, "config", None)
    get_config(cli_overrides or None, config_path=config_path)

    cc_profiles_path = getattr(args, "cc_profiles", None)
    cc_profile_name = getattr(args, "cc_profile", None)
    if cc_profile_name and not cc_profiles_path:
        console.print(
            "[yellow]Warning: --cc-profile specified without --cc-profiles, ignored[/yellow]"
        )
    if cc_profiles_path:
        _apply_cc_profile(cc_profiles_path, cc_profile_name)

    from logging_config import setup_logging
    console_level = "DEBUG" if getattr(args, "verbose", False) else "WARNING"
    setup_logging(console_level=console_level)

    try:
        # Handle subcommands
        if args.command and hasattr(args, "func"):
            args.func(args)
            return

        # Default: launch Web UI
        cmd_ui(args)

    except KeyboardInterrupt:
        console.print("\n[yellow]Interrupted[/yellow]")
        sys.exit(130)


if __name__ == "__main__":
    main()
