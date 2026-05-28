#!/usr/bin/env python3
import fnmatch
import subprocess
import sys
from pathlib import Path

TEMP_FILE_PATTERNS = [
    "*.swp",
    "*.swo",
    "*~",
    "*.tmp",
    "*.temp",
    "*.log",
    ".DS_Store",
    "Thumbs.db",
    "*.o",
    "*.obj",
    "*.a",
    "*.so",
    "*.dylib",
    "*.exe",
]

TEMP_DIR_NAMES = {
    "build",
    "dist",
    "out",
    ".cache",
    ".pytest_cache",
    "node_modules",
    ".venv",
    "venv",
    ".idea",
    ".vscode",
}


def run(cmd, capture=False):
    return subprocess.run(
        cmd,
        check=True,
        universal_newlines=True,
        stdout=subprocess.PIPE if capture else None,
        stderr=subprocess.PIPE if capture else None,
    )


def is_temp_path(path_str: str) -> bool:
    path = Path(path_str)
    name = path.name

    for pattern in TEMP_FILE_PATTERNS:
        if fnmatch.fnmatch(name, pattern) or fnmatch.fnmatch(path_str, pattern):
            return True

    for part in path.parts:
        if part in TEMP_DIR_NAMES:
            return True

    return False


def main() -> int:
    # Stage tracked changes (modified/deleted/renamed).
    run(["git", "add", "-u"])

    # Stage untracked files that are not ignored and not temp-like.
    result = run(["git", "ls-files", "-o", "--exclude-standard"], capture=True)
    untracked = [line for line in result.stdout.splitlines() if line.strip()]

    staged_untracked = []
    skipped_untracked = []

    for path_str in untracked:
        if is_temp_path(path_str):
            skipped_untracked.append(path_str)
            continue
        run(["git", "add", "--", path_str])
        staged_untracked.append(path_str)

    if staged_untracked or skipped_untracked:
        print("Staged untracked files:")
        if staged_untracked:
            for path_str in staged_untracked:
                print(f"  + {path_str}")
        else:
            print("  (none)")

        print("Skipped untracked files:")
        if skipped_untracked:
            for path_str in skipped_untracked:
                print(f"  - {path_str}")
        else:
            print("  (none)")

    # Final check to see if anything is staged.
    diff_check = run(["git", "diff", "--cached", "--name-only"], capture=True)
    if not diff_check.stdout.strip():
        print("No relevant changes staged.")
        return 2

    return 0


if __name__ == "__main__":
    sys.exit(main())
