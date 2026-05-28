#!/usr/bin/env python3
"""CLI entrypoint for cli-duo."""
import argparse
import json
import sys

from . import __version__
from .orchestrator import (
    create_session,
    end_session,
    get_session,
    list_registered_clis,
    list_sessions,
    register_cli,
    remove_cli,
    render_session_summary,
    swap_roles,
)


def handle_cli_register(args) -> int:
    success, msg = register_cli(
        name=args.name,
        command=args.command,
        repo=args.repo,
        cli_type=args.cli_type,
        description=args.description,
    )
    print(msg)
    return 0 if success else 1


def handle_cli_list(args) -> int:
    clis = list_registered_clis()
    if args.json:
        print(json.dumps(clis, indent=2))
        return 0
    if not clis:
        print("No CLIs registered. Add one with: duo cli register -n <name> -c <command>")
        return 0
    for cli in clis:
        line = f"{cli['name']}: {cli.get('command')}"
        if cli.get("type"):
            line += f" [{cli['type']}]"
        if cli.get("default_repo"):
            line += f" repo={cli['default_repo']}"
        print(line)
        if cli.get("description"):
            print(f"  {cli['description']}")
    return 0


def handle_cli_remove(args) -> int:
    success, msg = remove_cli(args.name)
    print(msg)
    return 0 if success else 1


def handle_pair_create(args) -> int:
    success, msg, _payload = create_session(
        session=args.session,
        primary_cli=args.primary,
        secondary_cli=args.secondary,
        mode=args.mode,
        repo=args.repo,
        worktree_path=args.worktree,
        rounds_per_role=args.rounds,
        description=args.description,
        dry_run=args.dry_run,
        confirm=args.confirm,
    )
    print(msg)
    return 0 if success else 1


def handle_pair_list(args) -> int:
    sessions = list_sessions()
    if args.json:
        print(json.dumps(sessions, indent=2))
        return 0
    if not sessions:
        print("No sessions found. Create one with: duo pair create -s <name> ...")
        return 0
    for session in sessions:
        print(render_session_summary(session["name"], session))
        print()
    return 0


def handle_pair_info(args) -> int:
    payload = get_session(args.session)
    if not payload:
        print(f"Session '{args.session}' not found")
        return 1
    print(render_session_summary(args.session, payload))
    return 0


def handle_pair_swap(args) -> int:
    success, msg, _payload = swap_roles(args.session)
    print(msg)
    return 0 if success else 1


def handle_pair_end(args) -> int:
    success, msg = end_session(args.session, confirm=args.confirm, dry_run=args.dry_run)
    print(msg)
    return 0 if success else 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Coordinate two AI CLIs on the same repository.",
        prog="duo",
    )
    parser.add_argument(
        "-V",
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )
    subparsers = parser.add_subparsers(dest="command", help="Top-level command")

    # cli subcommands
    cli_parser = subparsers.add_parser("cli", help="Manage CLI registry")
    cli_sub = cli_parser.add_subparsers(dest="cli_command", help="CLI registry commands")

    cli_register = cli_sub.add_parser("register", help="Register a CLI")
    cli_register.add_argument("-n", "--name", required=True, help="Registry name")
    cli_register.add_argument("-c", "--command", required=True, help="Command to launch the CLI")
    cli_register.add_argument("-r", "--repo", help="Default repo path for this CLI")
    cli_register.add_argument("-t", "--cli-type", dest="cli_type", help="CLI type (claude, cursor, etc.)")
    cli_register.add_argument("-d", "--description", help="Notes about this CLI")
    cli_register.set_defaults(func=handle_cli_register)

    cli_list = cli_sub.add_parser("list", help="List registered CLIs")
    cli_list.add_argument("-j", "--json", action="store_true", help="JSON output")
    cli_list.set_defaults(func=handle_cli_list)

    cli_remove = cli_sub.add_parser("remove", help="Remove a CLI")
    cli_remove.add_argument("-n", "--name", required=True, help="CLI name to remove")
    cli_remove.set_defaults(func=handle_cli_remove)

    # pair subcommands
    pair_parser = subparsers.add_parser("pair", help="Manage collaboration pairs")
    pair_sub = pair_parser.add_subparsers(dest="pair_command", help="Pair commands")

    pair_create = pair_sub.add_parser("create", help="Create a collaboration session")
    pair_create.add_argument("-s", "--session", required=True, help="Session name")
    pair_create.add_argument("-p", "--primary", required=True, help="Primary CLI name")
    pair_create.add_argument("-b", "--secondary", required=True, help="Secondary CLI name")
    pair_create.add_argument(
        "-m",
        "--mode",
        choices=["subordinate", "engineer-judge"],
        default="engineer-judge",
        help="Collaboration mode",
    )
    pair_create.add_argument("-r", "--repo", help="Repository path (required for subordinate)")
    pair_create.add_argument("-w", "--worktree", help="Custom subordinate worktree path")
    pair_create.add_argument(
        "-R",
        "--rounds",
        type=int,
        default=1,
        help="Rounds before swapping roles (engineer-judge mode)",
    )
    pair_create.add_argument("-d", "--description", help="Session notes")
    pair_create.add_argument("-n", "--dry-run", action="store_true", help="Plan without making changes")
    pair_create.add_argument(
        "-y",
        "--confirm",
        action="store_true",
        help="Required when creating subordinate worktrees",
    )
    pair_create.set_defaults(func=handle_pair_create)

    pair_list = pair_sub.add_parser("list", help="List collaboration sessions")
    pair_list.add_argument("-j", "--json", action="store_true", help="JSON output")
    pair_list.set_defaults(func=handle_pair_list)

    pair_info = pair_sub.add_parser("info", help="Show session details")
    pair_info.add_argument("-s", "--session", required=True, help="Session name")
    pair_info.set_defaults(func=handle_pair_info)

    pair_swap = pair_sub.add_parser("swap", help="Swap roles for a session")
    pair_swap.add_argument("-s", "--session", required=True, help="Session name")
    pair_swap.set_defaults(func=handle_pair_swap)

    pair_end = pair_sub.add_parser("end", help="Delete a session and clean up worktrees")
    pair_end.add_argument("-s", "--session", required=True, help="Session name")
    pair_end.add_argument("-n", "--dry-run", action="store_true", help="Plan cleanup only")
    pair_end.add_argument(
        "-y",
        "--confirm",
        action="store_true",
        help="Required when removing worktrees",
    )
    pair_end.set_defaults(func=handle_pair_end)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        return 1
    if args.command == "cli" and not getattr(args, "cli_command", None):
        parser.parse_args(["cli", "--help"])
        return 1
    if args.command == "pair" and not getattr(args, "pair_command", None):
        parser.parse_args(["pair", "--help"])
        return 1
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
