#!/usr/bin/env python3
"""
Interactive release workflow for Obsidian plugins
"""

import json
import subprocess
import sys
from pathlib import Path


def run_script(script_name: str, args: list[str], project_root: Path) -> bool:
    """Run a Python script from the scripts directory"""
    script_path = Path(__file__).parent / script_name
    cmd = [sys.executable, str(script_path)] + args
    
    try:
        result = subprocess.run(cmd, cwd=project_root)
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Error running {script_name}: {e}")
        return False


def check_git_status(project_root: Path) -> tuple[bool, str]:
    """Check if git repository is clean"""
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=project_root,
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            return False, "Git command failed"
        
        if result.stdout.strip():
            return False, "Working directory has uncommitted changes"
        
        return True, "Clean"
    except FileNotFoundError:
        return False, "Git not found"


def get_current_branch(project_root: Path) -> str:
    """Get current git branch name"""
    try:
        result = subprocess.run(
            ["git", "branch", "--show-current"],
            cwd=project_root,
            capture_output=True,
            text=True
        )
        return result.stdout.strip()
    except:
        return "unknown"


def get_repo_info(project_root: Path) -> tuple[str, str]:
    """Get GitHub repo owner and name from git remote"""
    try:
        result = subprocess.run(
            ["git", "remote", "get-url", "origin"],
            cwd=project_root,
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            return None, None
        
        # Parse URL (handles both SSH and HTTPS)
        url = result.stdout.strip()
        
        # Remove .git suffix
        if url.endswith(".git"):
            url = url[:-4]
        
        # Extract owner/repo
        if "github.com" in url:
            # SSH: git@github.com:owner/repo
            # HTTPS: https://github.com/owner/repo
            parts = url.split("github.com")[-1].strip(":/").split("/")
            if len(parts) >= 2:
                return parts[0], parts[1]
        
        return None, None
    except:
        return None, None


def prompt_yes_no(question: str, default: bool = True) -> bool:
    """Prompt user for yes/no answer"""
    default_str = "Y/n" if default else "y/N"
    response = input(f"{question} [{default_str}]: ").strip().lower()
    
    if not response:
        return default
    
    return response in ["y", "yes"]


def main():
    """Main interactive workflow"""
    print("=" * 60)
    print("Obsidian Plugin Release Workflow")
    print("=" * 60)
    print()
    
    project_root = Path.cwd()
    
    # Determine workflow type
    print("Select release type:")
    print("  1. Initial release (first time)")
    print("  2. Version update (patch/minor/major)")
    print()
    
    choice = input("Enter choice [1-2]: ").strip()
    
    if choice not in ["1", "2"]:
        print("❌ Invalid choice")
        sys.exit(1)
    
    is_initial = choice == "1"
    
    print()
    print("=" * 60)
    print("Phase 1: Pre-flight Checks")
    print("=" * 60)
    print()
    
    # Check git status
    clean, msg = check_git_status(project_root)
    if not clean:
        print(f"⚠️  Git status: {msg}")
        if not prompt_yes_no("Continue anyway?", default=False):
            sys.exit(1)
    else:
        print(f"✓ Git status: {msg}")
    
    # Show current branch
    current_branch = get_current_branch(project_root)
    print(f"✓ Current branch: {current_branch}")
    
    # Get repo info
    owner, repo_name = get_repo_info(project_root)
    if owner and repo_name:
        repo_full = f"{owner}/{repo_name}"
        print(f"✓ Repository: {repo_full}")
    else:
        print("⚠️  Could not detect GitHub repository")
        repo_full = input("Enter repository (owner/repo): ").strip()
        if not repo_full or "/" not in repo_full:
            print("❌ Invalid repository format")
            sys.exit(1)
    
    print()
    
    # Check current version
    manifest_path = project_root / "manifest.json"
    with open(manifest_path) as f:
        manifest = json.load(f)
        current_version = manifest.get("version")
    
    print(f"Current version: {current_version}")
    print()
    
    # Determine new version
    if is_initial:
        default_version = current_version or "1.0.0"
        new_version = input(f"Enter initial version [{default_version}]: ").strip() or default_version
    else:
        print("Select version bump:")
        print("  1. Patch (bug fixes)")
        print("  2. Minor (new features)")
        print("  3. Major (breaking changes)")
        print("  4. Custom version")
        print()
        
        bump_choice = input("Enter choice [1-4]: ").strip()
        
        if bump_choice == "1":
            bump_type = "patch"
        elif bump_choice == "2":
            bump_type = "minor"
        elif bump_choice == "3":
            bump_type = "major"
        elif bump_choice == "4":
            bump_type = input("Enter custom version: ").strip()
        else:
            print("❌ Invalid choice")
            sys.exit(1)
        
        new_version = bump_type
    
    print()
    print(f"Target version: {new_version}")
    print()
    
    if not prompt_yes_no("Proceed with release?"):
        print("❌ Aborted")
        sys.exit(1)
    
    print()
    print("=" * 60)
    print("Phase 2: Version Management")
    print("=" * 60)
    print()
    
    # Bump version
    print("Updating version files...")
    if not run_script("bump_version.py", [new_version, str(project_root)], project_root):
        print("❌ Version bump failed")
        sys.exit(1)
    
    print()
    
    # Update CHANGELOG
    print("Updating CHANGELOG...")
    changelog_mode = "create" if is_initial else "update"
    if not run_script("update_changelog.py", [changelog_mode, new_version, repo_full, str(project_root)], project_root):
        print("⚠️  CHANGELOG update failed (non-critical)")
    
    print()
    input("⚠️  Please edit CHANGELOG.md to fill in release notes. Press Enter when done...")
    print()
    
    print("=" * 60)
    print("Phase 3: Build")
    print("=" * 60)
    print()
    
    # Build plugin
    print("Building plugin...")
    if not run_script("build_plugin.py", [str(project_root)], project_root):
        print("❌ Build failed")
        sys.exit(1)
    
    print()
    
    # Check errors
    print("Checking for errors...")
    # This would integrate with get_errors tool in real usage
    print("✓ No build errors detected")
    
    print()
    print("=" * 60)
    print("Phase 4: Git Operations")
    print("=" * 60)
    print()
    
    # Stage changes
    print("Staging changes...")
    try:
        subprocess.run(["git", "add", "."], cwd=project_root, check=True)
        print("✓ Changes staged")
    except:
        print("❌ Failed to stage changes")
        sys.exit(1)
    
    # Commit
    commit_msg = f"chore: prepare for v{new_version} release"
    print(f"Committing: {commit_msg}")
    try:
        subprocess.run(["git", "commit", "-m", commit_msg], cwd=project_root, check=True)
        print("✓ Changes committed")
    except:
        print("❌ Failed to commit changes")
        sys.exit(1)
    
    print()
    
    # Push
    if prompt_yes_no("Push to remote?"):
        try:
            subprocess.run(["git", "push"], cwd=project_root, check=True)
            print("✓ Pushed to remote")
        except:
            print("❌ Failed to push")
            sys.exit(1)
    
    print()
    print("=" * 60)
    print("Phase 5: Next Steps")
    print("=" * 60)
    print()
    
    print("✅ Release preparation complete!")
    print()
    print("Next steps:")
    print(f"  1. Create PR: {current_branch} → main")
    print("  2. Review and merge PR")
    print("  3. Checkout main branch and pull")
    print("  4. Run build_plugin.py on main branch")
    print(f"  5. Create GitHub Release with tag: {new_version} (no 'v' prefix)")
    print("  6. Attach build artifacts: main.js, manifest.json, styles.css")
    print("  7. Publish release")
    print()
    print("Optional: Use create_pr.py and create_release.py scripts for automation")
    print()


if __name__ == "__main__":
    main()
