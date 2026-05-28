"""Layton CLI - argparse structure with global options."""

import argparse
import sys

from laytonlib import __version__
from laytonlib.formatters import OutputFormatter


def create_parser() -> argparse.ArgumentParser:
    """Create the argument parser with all commands."""
    parser = argparse.ArgumentParser(
        prog="layton",
        description="Personal AI assistant for attention management",
    )
    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {__version__}"
    )
    parser.add_argument(
        "--human",
        action="store_true",
        help="Human-readable output (default is JSON)",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Include debug information",
    )

    subparsers = parser.add_subparsers(dest="command")

    # doctor command
    doctor_parser = subparsers.add_parser("doctor", help="Check system health")
    # Hidden --fix flag (not shown in help, but works)
    doctor_parser.add_argument(
        "--fix",
        action="store_true",
        help=argparse.SUPPRESS,  # Hidden from help
    )

    # config command
    config_parser = subparsers.add_parser("config", help="Manage configuration")
    config_subparsers = config_parser.add_subparsers(dest="config_command")

    # config init
    config_init = config_subparsers.add_parser("init", help="Create default config")
    config_init.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing config",
    )

    # config show
    config_subparsers.add_parser("show", help="Display current config")

    # config keys
    config_subparsers.add_parser("keys", help="List all config keys")

    # config get
    config_get = config_subparsers.add_parser("get", help="Get a config value")
    config_get.add_argument(
        "key", help="Key in dot notation (e.g., work.schedule.start)"
    )

    # config set
    config_set = config_subparsers.add_parser("set", help="Set a config value")
    config_set.add_argument("key", help="Key in dot notation")
    config_set.add_argument("value", help="Value to set (JSON parsed if valid)")

    # context command
    subparsers.add_parser("context", help="Show temporal context")

    # skills command
    skills_parser = subparsers.add_parser("skills", help="Manage skill inventory")
    skills_parser.add_argument(
        "--discover",
        action="store_true",
        help="Discover skills from skills/*/SKILL.md",
    )
    skills_subparsers = skills_parser.add_subparsers(dest="skills_command")

    # skills add
    skills_add = skills_subparsers.add_parser("add", help="Create new skill file")
    skills_add.add_argument("name", help="Skill name (lowercase identifier)")

    # workflows command
    workflows_parser = subparsers.add_parser("workflows", help="Manage workflows")
    workflows_subparsers = workflows_parser.add_subparsers(dest="workflows_command")

    # workflows add
    workflows_add = workflows_subparsers.add_parser(
        "add", help="Create new workflow file"
    )
    workflows_add.add_argument("name", help="Workflow name (lowercase identifier)")

    return parser


def run_orientation(formatter: OutputFormatter) -> int:
    """Run orientation - combined doctor + skills + workflows.

    Args:
        formatter: Output formatter

    Returns:
        Exit code (0=success, 1=fixable, 2=critical)
    """
    from laytonlib.doctor import (
        check_beads_available,
        check_beads_initialized,
        check_config_exists,
        check_config_valid,
    )
    from laytonlib.skills import list_skills
    from laytonlib.workflows import list_workflows

    # Run doctor checks
    checks = []
    next_steps = []

    beads_check = check_beads_available()
    checks.append(beads_check)

    if beads_check.status == "fail":
        formatter.error(
            "BEADS_UNAVAILABLE",
            beads_check.message,
            next_steps=["Install Beads CLI: https://github.com/steveyegge/beads"],
        )
        return 2

    beads_init_check = check_beads_initialized()
    checks.append(beads_init_check)
    if beads_init_check.status == "warn":
        next_steps.append("Run 'bd init' to initialize Beads")

    config_exists_check = check_config_exists()
    checks.append(config_exists_check)

    needs_setup = config_exists_check.status == "fail"

    if config_exists_check.status == "pass":
        config_valid_check = check_config_valid()
        checks.append(config_valid_check)

    if needs_setup:
        next_steps.append("Follow workflows/setup.md for guided onboarding")
        next_steps.append("Or run 'layton config init' for quick setup")

    # Get skills inventory
    skills = list_skills()
    skills_data = [{"name": s.name, "description": s.description} for s in skills]

    if not skills:
        next_steps.append("Run 'layton skills --discover' to find available skills")

    # Get workflows inventory
    workflows = list_workflows()
    workflows_data = [
        {"name": w.name, "description": w.description, "triggers": w.triggers}
        for w in workflows
    ]

    if not workflows:
        next_steps.append("Run 'layton workflows add <name>' to create a workflow")

    # Build output
    data = {
        "needs_setup": needs_setup,
        "checks": [c.to_dict() for c in checks],
        "skills": skills_data,
        "workflows": workflows_data,
    }

    if next_steps:
        data["next_steps"] = next_steps

    formatter.success(data, next_steps=next_steps if next_steps else None)
    return 0


def run_skills(
    formatter: OutputFormatter,
    command: str | None,
    discover: bool,
    name: str | None,
) -> int:
    """Run skills command.

    Args:
        formatter: Output formatter
        command: Subcommand (add, or None for list)
        discover: Whether to run discovery
        name: Skill name for add command

    Returns:
        Exit code (0=success, 1=error)
    """
    from laytonlib.skills import add_skill, discover_skills, list_skills

    if command == "add":
        if not name:
            formatter.error("MISSING_NAME", "Skill name is required")
            return 1

        try:
            path = add_skill(name)
            formatter.success(
                {"created": str(path), "name": name},
                next_steps=[f"Edit {path} to configure the skill"],
            )
            return 0
        except FileExistsError as e:
            formatter.error(
                "SKILL_EXISTS",
                str(e),
                next_steps=["Review existing skill file or choose a different name"],
            )
            return 1

    elif discover:
        known, unknown = discover_skills()
        next_steps = []
        if unknown:
            next_steps.append(
                f"Run 'layton skills add <name>' to create skill files for: "
                f"{', '.join(s.name for s in unknown)}"
            )
        formatter.success(
            {
                "known": [s.to_dict() for s in known],
                "unknown": [s.to_dict() for s in unknown],
            },
            next_steps=next_steps if next_steps else None,
        )
        return 0

    else:
        # Default: list skills
        skills = list_skills()
        next_steps = []
        if not skills:
            next_steps.append("Run 'layton skills --discover' to find available skills")
            next_steps.append("Run 'layton skills add <name>' to create a skill file")
        formatter.success(
            {"skills": [s.to_dict() for s in skills]},
            next_steps=next_steps if next_steps else None,
        )
        return 0


def run_workflows(
    formatter: OutputFormatter,
    command: str | None,
    name: str | None,
) -> int:
    """Run workflows command.

    Args:
        formatter: Output formatter
        command: Subcommand (add, or None for list)
        name: Workflow name for add command

    Returns:
        Exit code (0=success, 1=error)
    """
    from laytonlib.workflows import add_workflow, list_workflows

    if command == "add":
        if not name:
            formatter.error("MISSING_NAME", "Workflow name is required")
            return 1

        try:
            path = add_workflow(name)
            formatter.success(
                {"created": str(path), "name": name},
                next_steps=[f"Edit {path} to configure the workflow"],
            )
            return 0
        except FileExistsError as e:
            formatter.error(
                "WORKFLOW_EXISTS",
                str(e),
                next_steps=["Review existing workflow file or choose a different name"],
            )
            return 1

    else:
        # Default: list workflows
        workflows = list_workflows()
        next_steps = []
        if not workflows:
            next_steps.append("Run 'layton workflows add <name>' to create a workflow")
        formatter.success(
            {"workflows": [w.to_dict() for w in workflows]},
            next_steps=next_steps if next_steps else None,
        )
        return 0


def main(argv: list[str] | None = None) -> int:
    """CLI entrypoint.

    Args:
        argv: Command line arguments (defaults to sys.argv[1:])

    Returns:
        Exit code (0=success, 1=fixable, 2=critical)
    """
    parser = create_parser()
    args = parser.parse_args(argv)

    # Create formatter based on --human flag
    formatter = OutputFormatter(human=args.human, verbose=args.verbose)

    # No-arg default: run orientation (doctor + skills + workflows)
    if args.command is None:
        return run_orientation(formatter)

    # Route to command handlers
    if args.command == "doctor":
        from laytonlib.doctor import run_doctor

        return run_doctor(formatter, fix=getattr(args, "fix", False))

    elif args.command == "config":
        from laytonlib.config import run_config

        # No subcommand default: show
        config_cmd = args.config_command or "show"
        return run_config(
            formatter,
            config_cmd,
            key=getattr(args, "key", None),
            value=getattr(args, "value", None),
            force=getattr(args, "force", False),
        )

    elif args.command == "context":
        from laytonlib.context import run_context

        return run_context(formatter)

    elif args.command == "skills":
        return run_skills(
            formatter,
            command=getattr(args, "skills_command", None),
            discover=getattr(args, "discover", False),
            name=getattr(args, "name", None),
        )

    elif args.command == "workflows":
        return run_workflows(
            formatter,
            command=getattr(args, "workflows_command", None),
            name=getattr(args, "name", None),
        )

    else:
        # Unknown command - shouldn't happen with argparse
        formatter.error("UNKNOWN_COMMAND", f"Unknown command: {args.command}")
        return 2


if __name__ == "__main__":
    sys.exit(main())
