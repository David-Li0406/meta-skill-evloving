#!/usr/bin/env python3
"""
Create GitHub Release using GitHub CLI (gh)
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


def read_changelog_section(changelog_path: Path, version: str) -> str:
    """Extract changelog section for specific version"""
    if not changelog_path.exists():
        return ""
    
    with open(changelog_path) as f:
        lines = f.readlines()
    
    section_lines = []
    in_section = False
    
    for line in lines:
        # Start of our version section
        if f"## [{version}]" in line:
            in_section = True
            continue
        
        # Start of next section (stop)
        if in_section and line.startswith("## ["):
            break
        
        # Collect section content
        if in_section:
            section_lines.append(line)
    
    return "".join(section_lines).strip()


def create_release(
    project_root: Path,
    version: str,
    draft: bool = True
) -> tuple[bool, str]:
    """
    Create GitHub Release using gh CLI.
    
    Args:
        project_root: Project root directory
        version: Version tag (e.g., "1.0.0" - no 'v' prefix)
        draft: Create as draft (default True)
    
    Returns:
        (success, message): tuple of success status and message
    """
    # Check required artifacts
    required_files = ["main.js", "manifest.json"]
    optional_files = ["styles.css"]
    
    artifacts = []
    missing_files = []
    
    for file in required_files:
        file_path = project_root / file
        if file_path.exists():
            artifacts.append(str(file_path))
        else:
            missing_files.append(file)
    
    if missing_files:
        return False, f"Missing required build artifacts: {', '.join(missing_files)}"
    
    for file in optional_files:
        file_path = project_root / file
        if file_path.exists():
            artifacts.append(str(file_path))
    
    # Generate release notes
    changelog_path = project_root / "CHANGELOG.md"
    changelog_notes = read_changelog_section(changelog_path, version)
    
    if changelog_notes:
        notes = f"""# Release v{version}

{changelog_notes}

## Installation

### Via BRAT
1. Install [BRAT plugin](https://github.com/TfTHacker/obsidian42-brat)
2. Add this repository URL in BRAT settings
3. BRAT will auto-update to this version

### Manual
1. Download the attached files: `main.js`, `manifest.json`, `styles.css`
2. Place them in: `<VaultFolder>/.obsidian/plugins/ai-terminal/`
3. Restart Obsidian and enable the plugin
"""
    else:
        notes = f"""# Release v{version}

See full changelog at CHANGELOG.md

## Installation

### Via BRAT
1. Install [BRAT plugin](https://github.com/TfTHacker/obsidian42-brat)
2. Add this repository URL in BRAT settings
3. BRAT will auto-update to this version

### Manual
1. Download the attached files: `main.js`, `manifest.json`, `styles.css`
2. Place them in: `<VaultFolder>/.obsidian/plugins/ai-terminal/`
3. Restart Obsidian and enable the plugin
"""
    
    # Build gh release create command
    cmd = [
        "gh", "release", "create",
        version,  # Tag (no 'v' prefix for Obsidian)
        "--title", f"v{version}",
        "--notes", notes
    ]
    
    if draft:
        cmd.append("--draft")
    
    # Add artifacts
    for artifact in artifacts:
        cmd.append(artifact)
    
    try:
        result = subprocess.run(
            cmd,
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
    if len(sys.argv) < 2:
        print("Usage: create_release.py <version> [--publish] [project_root]")
        print("\nExamples:")
        print("  create_release.py 1.0.0              # Create draft release")
        print("  create_release.py 1.0.0 --publish    # Create and publish immediately")
        print("  create_release.py 1.0.0 --publish /path/to/project")
        print()
        print("Note: Tag will be '1.0.0' without 'v' prefix (Obsidian requirement)")
        sys.exit(1)
    
    version = sys.argv[1]
    publish = "--publish" in sys.argv
    
    # Find project root (last non-flag argument or cwd)
    project_root = Path.cwd()
    for arg in sys.argv[2:]:
        if not arg.startswith("--"):
            project_root = Path(arg)
            break
    
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
    
    # Verify artifacts
    print("Checking build artifacts...")
    artifacts = []
    for file in ["main.js", "manifest.json", "styles.css"]:
        file_path = project_root / file
        if file_path.exists():
            size = file_path.stat().st_size
            print(f"  ✓ {file} ({size:,} bytes)")
            artifacts.append(file)
        elif file != "styles.css":  # styles.css is optional
            print(f"  ❌ {file} not found")
            sys.exit(1)
    print()
    
    # Create release
    draft_str = "draft " if not publish else ""
    print(f"Creating {draft_str}release with tag: {version}")
    print(f"Artifacts: {', '.join(artifacts)}")
    print()
    
    success, message = create_release(project_root, version, draft=not publish)
    
    if success:
        print(f"✅ Release {draft_str}created successfully")
        print()
        print(message)
        print()
        
        if not publish:
            print("⚠️  Release created as DRAFT")
            print("   Visit GitHub to review and publish:")
            print(f"   https://github.com/<owner>/<repo>/releases")
            print()
            print("   Or publish from CLI:")
            print(f"   gh release edit {version} --draft=false")
    else:
        print(f"❌ Failed to create release")
        print()
        print(message)
        sys.exit(1)


if __name__ == "__main__":
    main()
