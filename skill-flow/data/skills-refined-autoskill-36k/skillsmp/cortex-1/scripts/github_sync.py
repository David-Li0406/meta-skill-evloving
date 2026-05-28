# /// script
# requires-python = ">=3.9"
# dependencies = ["requests"]
# ///
# ABOUTME: Syncs workout files to a GitHub repository using the GitHub API.
# ABOUTME: Usage: uv run github_sync.py --file workouts.csv --dest workouts/workouts.csv

import argparse
import base64
import json
import sys
from pathlib import Path


def load_config():
    """Load config from config.json in scripts directory."""
    script_dir = Path(__file__).parent
    config_path = script_dir / "config.json"

    if config_path.exists():
        with open(config_path) as f:
            return json.load(f)
    return {}


def get_file_info(repo: str, path: str, token: str, branch: str = "main") -> dict | None:
    """Get file info (sha and content) from the repo, or None if it doesn't exist."""
    import requests

    url = f"https://api.github.com/repos/{repo}/contents/{path}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github.v3+json",
    }
    params = {"ref": branch}

    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        content_b64 = data.get("content", "")
        content = base64.b64decode(content_b64).decode("utf-8") if content_b64 else ""
        return {"sha": data.get("sha"), "content": content}
    return None


def get_file_sha(repo: str, path: str, token: str, branch: str = "main") -> str | None:
    """Get the SHA of an existing file in the repo, or None if it doesn't exist."""
    info = get_file_info(repo, path, token, branch)
    return info["sha"] if info else None


def fetch_file(repo: str, path: str, token: str, branch: str = "main") -> str | None:
    """Fetch file content from GitHub repo. Returns content string or None if not found."""
    info = get_file_info(repo, path, token, branch)
    return info["content"] if info else None


def push_file(
    repo: str,
    token: str,
    local_path: str,
    dest_path: str,
    message: str,
    branch: str = "main",
) -> bool:
    """Push a single file to GitHub using the Contents API."""
    import requests

    local_file = Path(local_path)
    if not local_file.exists():
        print(f"Error: Local file not found: {local_path}", file=sys.stderr)
        return False

    content = local_file.read_bytes()
    content_b64 = base64.b64encode(content).decode("utf-8")

    url = f"https://api.github.com/repos/{repo}/contents/{dest_path}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github.v3+json",
    }

    data = {
        "message": message,
        "content": content_b64,
        "branch": branch,
    }

    sha = get_file_sha(repo, dest_path, token, branch)
    if sha:
        data["sha"] = sha

    response = requests.put(url, headers=headers, json=data)

    if response.status_code in (200, 201):
        action = "Updated" if sha else "Created"
        print(f"{action}: https://github.com/{repo}/blob/{branch}/{dest_path}")
        return True
    else:
        print(f"Error pushing {dest_path}: {response.status_code}", file=sys.stderr)
        print(response.json().get("message", "Unknown error"), file=sys.stderr)
        return False


def push_files(
    repo: str,
    token: str,
    files: list[tuple[str, str]],
    message: str,
    branch: str = "main",
) -> bool:
    """Push multiple files to GitHub."""
    success = True
    for local_path, dest_path in files:
        if not push_file(repo, token, local_path, dest_path, message, branch):
            success = False
    return success


def main():
    config = load_config()

    parser = argparse.ArgumentParser(
        description="Sync files with GitHub repository"
    )
    parser.add_argument(
        "--token",
        default=config.get("github_token", ""),
        help="GitHub Personal Access Token (default: from config.json)"
    )
    parser.add_argument(
        "--repo",
        default=config.get("github_repo", ""),
        help="Repository (username/repo-name) (default: from config.json)"
    )
    parser.add_argument(
        "--branch",
        default=config.get("github_branch", "main"),
        help="Target branch (default: from config.json or main)"
    )
    parser.add_argument(
        "--fetch",
        metavar="PATH",
        help="Fetch a file from the repo and print to stdout"
    )
    parser.add_argument(
        "--file",
        action="append",
        dest="files",
        help="Local file to push (can specify multiple)"
    )
    parser.add_argument(
        "--dest",
        action="append",
        dest="dests",
        help="Destination path in repo (can specify multiple)"
    )
    parser.add_argument(
        "--message", "-m",
        default="Update workout files",
        help="Commit message"
    )

    args = parser.parse_args()

    if not args.token:
        print("Error: No GitHub token provided. Set github_token in config.json or use --token", file=sys.stderr)
        sys.exit(1)

    if not args.repo:
        print("Error: No repository provided. Set github_repo in config.json or use --repo", file=sys.stderr)
        sys.exit(1)

    # Fetch mode: retrieve file and print to stdout
    if args.fetch:
        content = fetch_file(args.repo, args.fetch, args.token, args.branch)
        if content is not None:
            print(content, end="")
            sys.exit(0)
        else:
            print(f"File not found: {args.fetch}", file=sys.stderr)
            sys.exit(1)

    # Push mode: upload files
    if not args.files:
        print("Error: No files specified. Use --file to specify files to push", file=sys.stderr)
        sys.exit(1)

    if args.dests and len(args.files) != len(args.dests):
        print("Error: Number of --file and --dest arguments must match", file=sys.stderr)
        sys.exit(1)

    dests = args.dests if args.dests else args.files
    files = list(zip(args.files, dests))

    success = push_files(args.repo, args.token, files, args.message, args.branch)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
