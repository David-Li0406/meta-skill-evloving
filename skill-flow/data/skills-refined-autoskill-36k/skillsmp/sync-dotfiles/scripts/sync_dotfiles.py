#!/usr/bin/env python3
"""
Sync dotfiles from chezmoi (private) to public dotfiles repo.
Renders templates and copies files while respecting a safety blocklist.
Leaves all changes unstaged for manual review.
"""

import argparse
import os
import subprocess
import sys
from pathlib import Path
from typing import List, Set, Tuple
import fnmatch
import shutil

# Safety blocklist patterns - files matching these will NOT be synced
SENSITIVE_PATTERNS = [
    # SSH and GPG
    ".ssh/*",
    ".gnupg/*",
    "*.pem",
    "*.key",
    "*_rsa",
    "*_dsa",
    "*_ecdsa",
    "*_ed25519",

    # Credentials and secrets
    "*secret*",
    "*password*",
    "*token*",
    "*credential*",
    "*.env",
    ".env.*",
    "*api_key*",
    "*apikey*",

    # AWS and cloud credentials
    ".aws/credentials",
    ".aws/config",
    ".azure/*",
    ".gcloud/*",

    # Other sensitive
    ".netrc",
    ".docker/config.json",
    "*_history",  # shell histories
    ".local/share/fish/fish_history",
]


def is_sensitive(file_path: str, patterns: List[str]) -> bool:
    """Check if a file path matches any sensitive patterns."""
    file_path_lower = file_path.lower()

    for pattern in patterns:
        # Match against full path
        if fnmatch.fnmatch(file_path_lower, pattern.lower()):
            return True
        # Match against basename
        if fnmatch.fnmatch(os.path.basename(file_path_lower), pattern.lower()):
            return True

    return False


def get_chezmoi_files(chezmoi_dir: Path) -> List[str]:
    """Get list of files managed by chezmoi."""
    try:
        result = subprocess.run(
            ["chezmoi", "managed", "--include=files"],
            capture_output=True,
            text=True,
            check=True
        )
        files = [line.strip() for line in result.stdout.split('\n') if line.strip()]
        return files
    except subprocess.CalledProcessError as e:
        print(f"Error getting chezmoi managed files: {e}", file=sys.stderr)
        print(f"stderr: {e.stderr}", file=sys.stderr)
        sys.exit(1)
    except FileNotFoundError:
        print("Error: chezmoi command not found. Is chezmoi installed?", file=sys.stderr)
        sys.exit(1)


def render_file(file_path: str) -> bytes:
    """Use chezmoi to render a file (processes templates)."""
    # chezmoi cat expects paths with ~ prefix (target paths, not source paths)
    target_path = f"~/{file_path}" if not file_path.startswith("~") else file_path

    try:
        result = subprocess.run(
            ["chezmoi", "cat", target_path],
            capture_output=True,
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Warning: Could not render {file_path}: {e}", file=sys.stderr)
        return None


def sync_files(chezmoi_dir: Path, public_repo_dir: Path, dry_run: bool = False) -> Tuple[Set[str], Set[str], Set[str]]:
    """
    Sync files from chezmoi to public repo.

    Returns:
        Tuple of (synced_files, skipped_files, failed_files)
    """
    synced = set()
    skipped = set()
    failed = set()

    files = get_chezmoi_files(chezmoi_dir)
    print(f"Found {len(files)} files managed by chezmoi\n")

    for file_path in files:
        # Remove leading ~ or / to get relative path
        rel_path = file_path.lstrip('~').lstrip('/')

        # Check if file is sensitive
        if is_sensitive(rel_path, SENSITIVE_PATTERNS):
            skipped.add(rel_path)
            continue

        # Render the file content
        content = render_file(file_path)
        if content is None:
            failed.add(rel_path)
            continue

        # Determine destination path
        dest_path = public_repo_dir / rel_path

        if dry_run:
            print(f"[DRY RUN] Would copy: {rel_path}")
            synced.add(rel_path)
            continue

        # Create parent directories if needed
        dest_path.parent.mkdir(parents=True, exist_ok=True)

        # Write the rendered content
        try:
            dest_path.write_bytes(content)
            synced.add(rel_path)
        except Exception as e:
            print(f"Error writing {dest_path}: {e}", file=sys.stderr)
            failed.add(rel_path)

    return synced, skipped, failed


def print_summary(synced: Set[str], skipped: Set[str], failed: Set[str]):
    """Print a summary of the sync operation."""
    print("\n" + "="*70)
    print("SYNC SUMMARY")
    print("="*70)

    print(f"\n✅ Synced: {len(synced)} files")
    if synced:
        for f in sorted(synced)[:10]:  # Show first 10
            print(f"   - {f}")
        if len(synced) > 10:
            print(f"   ... and {len(synced) - 10} more")

    print(f"\n🚫 Skipped (sensitive): {len(skipped)} files")
    if skipped:
        for f in sorted(skipped)[:10]:
            print(f"   - {f}")
        if len(skipped) > 10:
            print(f"   ... and {len(skipped) - 10} more")

    if failed:
        print(f"\n❌ Failed: {len(failed)} files")
        for f in sorted(failed):
            print(f"   - {f}")

    print("\n" + "="*70)
    print("All changes are UNSTAGED. Review with:")
    print("  cd ~/Developer/misc/dot")
    print("  git status")
    print("  git diff")
    print("="*70)


def main():
    parser = argparse.ArgumentParser(
        description="Sync dotfiles from chezmoi (private) to public repo"
    )
    parser.add_argument(
        "--chezmoi-dir",
        type=Path,
        default=Path.home() / ".local/share/chezmoi",
        help="Path to chezmoi source directory (default: ~/.local/share/chezmoi)"
    )
    parser.add_argument(
        "--public-repo",
        type=Path,
        default=Path.home() / "Developer/misc/dot",
        help="Path to public dotfiles repo (default: ~/Developer/misc/dot)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be synced without actually copying files"
    )

    args = parser.parse_args()

    # Validate paths
    if not args.chezmoi_dir.exists():
        print(f"Error: chezmoi directory not found: {args.chezmoi_dir}", file=sys.stderr)
        sys.exit(1)

    if not args.public_repo.exists():
        print(f"Error: public repo directory not found: {args.public_repo}", file=sys.stderr)
        sys.exit(1)

    # Check if public repo is a git repo
    if not (args.public_repo / ".git").exists():
        print(f"Warning: {args.public_repo} doesn't appear to be a git repository", file=sys.stderr)

    print(f"Syncing dotfiles:")
    print(f"  From: {args.chezmoi_dir}")
    print(f"  To:   {args.public_repo}")
    if args.dry_run:
        print("  Mode: DRY RUN")
    print()

    # Perform sync
    synced, skipped, failed = sync_files(args.chezmoi_dir, args.public_repo, args.dry_run)

    # Print summary
    print_summary(synced, skipped, failed)

    if failed:
        sys.exit(1)


if __name__ == "__main__":
    main()
