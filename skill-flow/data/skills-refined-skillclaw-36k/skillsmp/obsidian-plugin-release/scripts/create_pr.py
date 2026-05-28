#!/usr/bin/env python3
"""
Create Pull Request using GitHub CLI (gh)
"""

import subprocess
import sys
from pathlib import Path


def check_gh_cli() -> bool:
    """Check if GitHub CLI is installed and authenticated"""
    try:
        result = subprocess.run(
            ["gh", "auth", "status"],
            capture_output=True,
            text=True
        )
        return result.returncode == 0
    except FileNotFoundError:
        return False


def create_pr(
    project_root: Path,
    from_branch: str,
    to_branch: str,
    title: str,
    body: str
) -> tuple[bool, str]:
    """
    Create PR using gh CLI.
    
    Returns:
        (success, message): tuple of success status and message
    """
    try:
        result = subprocess.run(
            [
                "gh", "pr", "create",
                "--base", to_branch,
                "--head", from_branch,
                "--title", title,
                "--body", body
            ],
            cwd=project_root,
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            return True, result.stdout.strip()
        else:
            return False, result.stderr.strip()
    
    except Exception as e:
        return False, str(e)


def main():
    """Main entry point"""
    if len(sys.argv) < 4:
        print("Usage: create_pr.py <from_branch> <to_branch> <version> [project_root]")
        print("\nExamples:")
        print("  create_pr.py feature/core main 1.0.0")
        print("  create_pr.py develop main 1.1.0 /path/to/project")
        sys.exit(1)
    
    from_branch = sys.argv[1]
    to_branch = sys.argv[2]
    version = sys.argv[3]
    project_root = Path(sys.argv[4]) if len(sys.argv) > 4 else Path.cwd()
    
    # Check gh CLI
    print("Checking GitHub CLI...")
    if not check_gh_cli():
        print("❌ GitHub CLI (gh) is not installed or not authenticated")
        print()
        print("To install gh:")
        print("  https://cli.github.com/")
        print()
        print("To authenticate:")
        print("  gh auth login")
        sys.exit(1)
    
    print("✓ GitHub CLI authenticated")
    print()
    
    # Generate PR title and body
    title = f"Release v{version}"
    body = f"""## Release v{version}

This PR prepares the release for version {version}.

### Changes

See CHANGELOG.md for detailed changes.

### Release Checklist

- [ ] Version numbers updated in manifest.json, package.json, versions.json
- [ ] CHANGELOG.md updated with release notes
- [ ] Build completes without errors
- [ ] Manual testing completed

### Post-Merge Steps

After merging this PR:

1. Checkout main branch and pull latest changes
2. Run `npm run build` to generate release artifacts
3. Create GitHub Release with tag `{version}` (no 'v' prefix)
4. Attach build artifacts: `main.js`, `manifest.json`, `styles.css`
5. Publish the release
"""
    
    print(f"Creating PR: {from_branch} → {to_branch}")
    print(f"Title: {title}")
    print()
    
    success, message = create_pr(project_root, from_branch, to_branch, title, body)
    
    if success:
        print("✅ Pull Request created successfully")
        print()
        print(message)
    else:
        print("❌ Failed to create Pull Request")
        print()
        print(message)
        sys.exit(1)


if __name__ == "__main__":
    main()
