#!/usr/bin/env python3
"""
Check version consistency across manifest.json, package.json, and versions.json
"""

import json
import sys
from pathlib import Path


def check_versions(project_root: Path) -> tuple[bool, list[str]]:
    """
    Check if versions are consistent across all files.
    
    Returns:
        (success, messages): tuple of success status and list of messages
    """
    messages = []
    
    # Read manifest.json
    manifest_path = project_root / "manifest.json"
    if not manifest_path.exists():
        messages.append("❌ manifest.json not found")
        return False, messages
    
    with open(manifest_path) as f:
        manifest = json.load(f)
        manifest_version = manifest.get("version")
        min_app_version = manifest.get("minAppVersion")
    
    if not manifest_version:
        messages.append("❌ version not found in manifest.json")
        return False, messages
    
    messages.append(f"✓ manifest.json version: {manifest_version}")
    
    # Read package.json
    package_path = project_root / "package.json"
    if not package_path.exists():
        messages.append("⚠️  package.json not found (optional)")
        package_version = None
    else:
        with open(package_path) as f:
            package = json.load(f)
            package_version = package.get("version")
        
        if package_version != manifest_version:
            messages.append(f"❌ package.json version ({package_version}) differs from manifest.json ({manifest_version})")
            return False, messages
        
        messages.append(f"✓ package.json version: {package_version}")
    
    # Read versions.json
    versions_path = project_root / "versions.json"
    if not versions_path.exists():
        messages.append("❌ versions.json not found")
        return False, messages
    
    with open(versions_path) as f:
        versions = json.load(f)
        versions_entry = versions.get(manifest_version)
    
    if versions_entry is None:
        messages.append(f"❌ No entry for version {manifest_version} in versions.json")
        return False, messages
    
    if versions_entry != min_app_version:
        messages.append(f"❌ versions.json entry ({versions_entry}) differs from manifest.json minAppVersion ({min_app_version})")
        return False, messages
    
    messages.append(f"✓ versions.json entry: {manifest_version} -> {versions_entry}")
    
    messages.append("\n✅ All version files are consistent")
    return True, messages


def main():
    """Main entry point"""
    if len(sys.argv) > 1:
        project_root = Path(sys.argv[1])
    else:
        project_root = Path.cwd()
    
    success, messages = check_versions(project_root)
    
    for msg in messages:
        print(msg)
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
