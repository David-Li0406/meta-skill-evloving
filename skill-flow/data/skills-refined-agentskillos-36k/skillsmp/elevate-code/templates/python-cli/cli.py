"""CLI entry point. Argument parsing only - no business logic here."""
import argparse
import sys
import shutil
import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class CheckResult:
    """Result of a dependency check."""
    ok: bool
    message: str
    fix_command: Optional[str] = None


def check_binary(name: str) -> CheckResult:
    """Check if a binary exists in PATH."""
    path = shutil.which(name)
    if not path:
        return CheckResult(
            ok=False,
            message=f"{name} not found in PATH",
            fix_command=f"brew install {name}  # or apt-get install {name}"
        )
    return CheckResult(ok=True, message=f"{name} found at {path}")


def check_env_var(name: str) -> CheckResult:
    """Check if an environment variable is set."""
    value = os.environ.get(name)
    if not value:
        return CheckResult(
            ok=False,
            message=f"Environment variable {name} not set",
            fix_command=f"export {name}=<your-value>"
        )
    return CheckResult(ok=True, message=f"{name} is set")


def doctor():
    """Run all health checks and report results."""
    print("Running health checks...\n")

    checks = [
        # Add your dependency checks here
        # ("binary-name", check_binary("binary-name")),
        # ("ENV_VAR", check_env_var("ENV_VAR")),
    ]

    if not checks:
        print("No dependencies configured. Add checks in cli.py:doctor()")
        return

    all_passed = True
    for name, result in checks:
        status = "✓" if result.ok else "✗"
        print(f"{status} {name}: {result.message}")
        if not result.ok:
            all_passed = False
            if result.fix_command:
                print(f"  Fix: {result.fix_command}")

    print()
    if all_passed:
        print("All checks passed! Ready to run.")
    else:
        print("Some checks failed. Fix the issues above and run again.")
        sys.exit(1)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        prog="my-tool",
        description="A production-quality CLI tool.",
        epilog="Examples:\n"
               "  my-tool process input.txt\n"
               "  my-tool doctor",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # Doctor command
    subparsers.add_parser("doctor", help="Check dependencies and configuration")

    # Process command (example)
    process_parser = subparsers.add_parser("process", help="Process input files")
    process_parser.add_argument("input", help="Input file path")
    process_parser.add_argument("-o", "--output", help="Output file path")
    process_parser.add_argument("--dry-run", action="store_true", help="Preview changes")
    process_parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")

    # Global options
    parser.add_argument("--version", action="version", version="%(prog)s 0.1.0")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--quiet", action="store_true", help="Suppress output")

    args = parser.parse_args()

    if args.command == "doctor":
        doctor()
    elif args.command == "process":
        # Import and call your processing logic here
        print(f"Processing: {args.input}")
        if args.dry_run:
            print("(dry-run mode - no changes made)")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
