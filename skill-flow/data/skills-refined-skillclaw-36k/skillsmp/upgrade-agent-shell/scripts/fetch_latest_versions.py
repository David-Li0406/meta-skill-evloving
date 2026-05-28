#!/usr/bin/env python3

import json
import subprocess
import sys
from typing import Dict, Optional


def run_command(cmd: list[str]) -> str:
    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error running command {' '.join(cmd)}: {e.stderr}", file=sys.stderr)
        sys.exit(1)


def get_latest_release(owner: str, repo: str) -> Optional[Dict[str, str]]:
    try:
        output = run_command([
            "curl", "-s",
            f"https://api.github.com/repos/{owner}/{repo}/tags"
        ])
        data = json.loads(output)
        
        if not data or not isinstance(data, list) or len(data) == 0:
            print(f"Warning: No tags found for {owner}/{repo}", file=sys.stderr)
            return None
        
        tag = data[0]["name"]
            
        tarball_url = f"https://github.com/{owner}/{repo}/archive/{tag}.tar.gz"
        sha256 = run_command([
            "nix-prefetch-url", "--unpack", tarball_url
        ])
        
        return {
            "repo": repo,
            "owner": owner,
            "tag": tag,
            "sha256": sha256
        }
    except Exception as e:
        print(f"Error fetching release for {owner}/{repo}: {e}", file=sys.stderr)
        return None


def main():
    packages = [
        ("xenodium", "agent-shell"),
        ("xenodium", "shell-maker"),
        ("xenodium", "acp.el"),
    ]
    
    results = {}
    for owner, repo in packages:
        print(f"Fetching latest version for {owner}/{repo}...", file=sys.stderr)
        release = get_latest_release(owner, repo)
        if release:
            key = "acp" if repo == "acp.el" else repo
            results[key] = release
    
    if not results:
        print("Error: No releases found", file=sys.stderr)
        sys.exit(1)
    
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
