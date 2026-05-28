#!/usr/bin/env python3
"""
Build the plugin and verify build artifacts
"""

import subprocess
import sys
from pathlib import Path


def build_plugin(project_root: Path) -> tuple[bool, list[str]]:
    """
    Build the plugin using npm run build.
    
    Returns:
        (success, messages): tuple of success status and list of messages
    """
    messages = []
    
    # Check if package.json exists
    package_json = project_root / "package.json"
    if not package_json.exists():
        messages.append("❌ package.json not found")
        return False, messages
    
    # Run npm run build
    messages.append("Building plugin...")
    try:
        result = subprocess.run(
            ["npm", "run", "build"],
            cwd=project_root,
            capture_output=True,
            text=True,
            timeout=120
        )
        
        if result.returncode != 0:
            messages.append(f"❌ Build failed with exit code {result.returncode}")
            if result.stderr:
                messages.append(f"Error output:\n{result.stderr}")
            return False, messages
        
        messages.append("✓ Build completed successfully")
        
    except subprocess.TimeoutExpired:
        messages.append("❌ Build timed out after 120 seconds")
        return False, messages
    except FileNotFoundError:
        messages.append("❌ npm command not found. Is Node.js installed?")
        return False, messages
    
    # Verify build artifacts
    required_files = ["main.js", "manifest.json"]
    optional_files = ["styles.css"]
    
    missing_files = []
    for file in required_files:
        file_path = project_root / file
        if not file_path.exists():
            missing_files.append(file)
        else:
            size = file_path.stat().st_size
            messages.append(f"✓ {file} ({size:,} bytes)")
    
    if missing_files:
        messages.append(f"❌ Missing required files: {', '.join(missing_files)}")
        return False, messages
    
    # Check optional files
    for file in optional_files:
        file_path = project_root / file
        if file_path.exists():
            size = file_path.stat().st_size
            messages.append(f"✓ {file} ({size:,} bytes)")
    
    messages.append("\n✅ Build artifacts verified successfully")
    return True, messages


def main():
    """Main entry point"""
    if len(sys.argv) > 1:
        project_root = Path(sys.argv[1])
    else:
        project_root = Path.cwd()
    
    success, messages = build_plugin(project_root)
    
    for msg in messages:
        print(msg)
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
