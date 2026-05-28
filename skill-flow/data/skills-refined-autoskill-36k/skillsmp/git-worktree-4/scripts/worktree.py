#!/usr/bin/env python3
"""Git worktree management utility.

Provides commands for creating, listing, removing, and pruning git worktrees
with support for automatic branch creation and post-setup automation.
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path


def run_git(
    *args: str, cwd: str | None = None, check: bool = True
) -> subprocess.CompletedProcess[str]:
    """Run a git command and return the result."""
    result = subprocess.run(
        ["git", *args],
        cwd=cwd,
        capture_output=True,
        text=True,
        check=False,
    )
    if check and result.returncode != 0:
        print(f"Error: {result.stderr.strip()}", file=sys.stderr)
        sys.exit(1)
    return result


def get_repo_root(cwd: str | None = None) -> Path:
    """Get the root directory of the git repository."""
    result = run_git("rev-parse", "--show-toplevel", cwd=cwd)
    return Path(result.stdout.strip())


def get_main_branch() -> str:
    """Detect the main branch name (main, master, or default)."""
    result = run_git("symbolic-ref", "refs/remotes/origin/HEAD", check=False)
    if result.returncode == 0:
        return result.stdout.strip().split("/")[-1]

    # Fallback: check if main or master exists
    for branch in ["main", "master"]:
        result = run_git("rev-parse", "--verify", f"refs/heads/{branch}", check=False)
        if result.returncode == 0:
            return branch

    return "main"


def create_worktree(
    branch: str,
    base_branch: str | None = None,
    path: str | None = None,
    install_deps: bool = False,
    open_editor: str | None = None,
) -> None:
    """Create a new worktree, optionally with a new branch."""
    repo_root = get_repo_root()
    repo_name = repo_root.name

    # Default path: sibling directory named repo-branch
    if path is None:
        worktree_path = repo_root.parent / f"{repo_name}-{branch}"
    else:
        worktree_path = Path(path).resolve()

    if worktree_path.exists():
        print(f"Error: Path already exists: {worktree_path}", file=sys.stderr)
        sys.exit(1)

    # Check if branch exists
    branch_exists = (
        run_git("rev-parse", "--verify", f"refs/heads/{branch}", check=False).returncode == 0
    )

    if branch_exists:
        # Use existing branch
        run_git("worktree", "add", str(worktree_path), branch)
        print(f"Created worktree at {worktree_path} using existing branch '{branch}'")
    else:
        # Create new branch from base
        if base_branch is None:
            base_branch = get_main_branch()

        # Fetch latest from origin first
        run_git("fetch", "origin", base_branch, check=False)

        # Create worktree with new branch
        run_git("worktree", "add", "-b", branch, str(worktree_path), f"origin/{base_branch}")
        print(
            f"Created worktree at {worktree_path} with new branch '{branch}' from '{base_branch}'"
        )

    # Post-create: install dependencies
    if install_deps:
        install_dependencies(worktree_path)

    # Post-create: open in editor
    if open_editor:
        open_in_editor(worktree_path, open_editor)

    print(f"\nWorktree ready: {worktree_path}")


def install_dependencies(path: Path) -> None:
    """Detect and install dependencies based on project type."""
    print("\nInstalling dependencies...")

    # Node.js projects
    if (path / "package-lock.json").exists():
        subprocess.run(["npm", "ci"], cwd=path, check=False)
    elif (path / "yarn.lock").exists():
        subprocess.run(["yarn", "install", "--frozen-lockfile"], cwd=path, check=False)
    elif (path / "pnpm-lock.yaml").exists():
        subprocess.run(["pnpm", "install", "--frozen-lockfile"], cwd=path, check=False)
    elif (path / "bun.lockb").exists():
        subprocess.run(["bun", "install", "--frozen-lockfile"], cwd=path, check=False)
    elif (path / "package.json").exists():
        subprocess.run(["npm", "install"], cwd=path, check=False)

    # Python projects
    elif (path / "uv.lock").exists():
        subprocess.run(["uv", "sync"], cwd=path, check=False)
    elif (path / "poetry.lock").exists():
        subprocess.run(["poetry", "install"], cwd=path, check=False)
    elif (path / "Pipfile.lock").exists():
        subprocess.run(["pipenv", "install"], cwd=path, check=False)
    elif (path / "requirements.txt").exists():
        subprocess.run(["pip", "install", "-r", "requirements.txt"], cwd=path, check=False)

    # Ruby projects
    elif (path / "Gemfile.lock").exists():
        subprocess.run(["bundle", "install"], cwd=path, check=False)

    # Go projects
    elif (path / "go.mod").exists():
        subprocess.run(["go", "mod", "download"], cwd=path, check=False)

    # Rust projects
    elif (path / "Cargo.lock").exists():
        subprocess.run(["cargo", "fetch"], cwd=path, check=False)

    else:
        print("No recognized dependency file found, skipping installation.")


def open_in_editor(path: Path, editor: str) -> None:
    """Open the worktree in the specified editor."""
    print(f"\nOpening in {editor}...")

    editor_commands = {
        "code": ["code", str(path)],
        "vscode": ["code", str(path)],
        "cursor": ["cursor", str(path)],
        "idea": ["idea", str(path)],
        "webstorm": ["webstorm", str(path)],
        "pycharm": ["pycharm", str(path)],
        "zed": ["zed", str(path)],
        "sublime": ["subl", str(path)],
        "vim": ["vim", str(path)],
        "nvim": ["nvim", str(path)],
    }

    cmd = editor_commands.get(editor.lower(), [editor, str(path)])
    subprocess.Popen(cmd, start_new_session=True)


def list_worktrees(output_format: str = "table") -> None:
    """List all worktrees for the current repository."""
    result = run_git("worktree", "list", "--porcelain")

    worktrees = []
    current = {}

    for line in result.stdout.strip().split("\n"):
        if not line:
            if current:
                worktrees.append(current)
                current = {}
        elif line.startswith("worktree "):
            current["path"] = line[9:]
        elif line.startswith("HEAD "):
            current["head"] = line[5:]
        elif line.startswith("branch "):
            current["branch"] = line[7:].replace("refs/heads/", "")
        elif line == "bare":
            current["bare"] = True
        elif line == "detached":
            current["detached"] = True

    if current:
        worktrees.append(current)

    if output_format == "json":
        print(json.dumps(worktrees, indent=2))
    else:
        if not worktrees:
            print("No worktrees found.")
            return

        print(f"{'Path':<50} {'Branch':<30} {'HEAD':<12}")
        print("-" * 92)
        for wt in worktrees:
            path = wt.get("path", "")
            branch = wt.get(
                "branch", "(detached)" if wt.get("detached") else "(bare)" if wt.get("bare") else ""
            )
            head = wt.get("head", "")[:10]
            print(f"{path:<50} {branch:<30} {head:<12}")


def remove_worktree(path: str, force: bool = False) -> None:
    """Remove a worktree."""
    worktree_path = Path(path).resolve()

    if force:
        run_git("worktree", "remove", "--force", str(worktree_path))
    else:
        run_git("worktree", "remove", str(worktree_path))

    print(f"Removed worktree: {worktree_path}")


def prune_worktrees() -> None:
    """Remove stale worktree references."""
    run_git("worktree", "prune", "-v")
    print("Pruned stale worktree references.")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Git worktree management utility",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Create command
    create_parser = subparsers.add_parser("create", help="Create a new worktree")
    create_parser.add_argument("branch", help="Branch name (created if doesn't exist)")
    create_parser.add_argument(
        "-b", "--base", help="Base branch for new branch (default: main/master)"
    )
    create_parser.add_argument(
        "-p", "--path", help="Custom path for worktree (default: sibling directory)"
    )
    create_parser.add_argument(
        "-i", "--install", action="store_true", help="Install dependencies after creation"
    )
    create_parser.add_argument("-e", "--editor", help="Open in editor (code, cursor, idea, etc.)")

    # List command
    list_parser = subparsers.add_parser("list", help="List all worktrees")
    list_parser.add_argument(
        "-f", "--format", choices=["table", "json"], default="table", help="Output format"
    )

    # Remove command
    remove_parser = subparsers.add_parser("remove", help="Remove a worktree")
    remove_parser.add_argument("path", help="Path to the worktree to remove")
    remove_parser.add_argument(
        "-f", "--force", action="store_true", help="Force removal even if dirty"
    )

    # Prune command
    subparsers.add_parser("prune", help="Remove stale worktree references")

    args = parser.parse_args()

    if args.command == "create":
        create_worktree(
            branch=args.branch,
            base_branch=args.base,
            path=args.path,
            install_deps=args.install,
            open_editor=args.editor,
        )
    elif args.command == "list":
        list_worktrees(output_format=args.format)
    elif args.command == "remove":
        remove_worktree(args.path, force=args.force)
    elif args.command == "prune":
        prune_worktrees()


if __name__ == "__main__":
    main()
