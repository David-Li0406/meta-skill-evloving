#!/usr/bin/env python3
"""
Deploy Obsidian plugin to test vault
Supports both WSL and Windows environments
"""

import subprocess
import sys
from pathlib import Path
import shutil
import platform

# Configuration
PLUGIN_ID = "ai-terminal"
OBSIDIAN_TEST_VAULT = Path("/mnt/c/obsidian/test")  # WSL path
PLUGIN_DIR = OBSIDIAN_TEST_VAULT / ".obsidian" / "plugins" / PLUGIN_ID

# Colors for output (cross-platform)
class Colors:
    GREEN = '\033[0;32m'
    BLUE = '\033[0;34m'
    RED = '\033[0;31m'
    NC = '\033[0m'  # No Color
    
    @staticmethod
    def is_supported():
        """Check if terminal supports colors"""
        return sys.stdout.isatty() and platform.system() != 'Windows'
    
    @classmethod
    def print_colored(cls, text, color):
        if cls.is_supported():
            print(f"{color}{text}{cls.NC}")
        else:
            print(text)

def detect_vault_path():
    """Detect correct vault path based on environment"""
    if platform.system() == 'Windows':
        # Native Windows
        return Path(r"C:\obsidian\test")
    else:
        # WSL or Linux - use mounted Windows path
        wsl_path = Path("/mnt/c/obsidian/test")
        if wsl_path.exists():
            return wsl_path
        # Fallback to Windows path if available
        win_path = Path(r"C:\obsidian\test")
        if win_path.exists():
            return win_path
    return OBSIDIAN_TEST_VAULT

def run_build():
    """Run npm build command"""
    Colors.print_colored("Building plugin...", Colors.BLUE)
    try:
        result = subprocess.run(
            ["npm", "run", "build"],
            check=True,
            capture_output=True,
            text=True
        )
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        Colors.print_colored(f"Build failed: {e.stderr}", Colors.RED)
        return False

def check_build_output():
    """Check if build output exists"""
    main_js = Path("main.js")
    if not main_js.exists():
        Colors.print_colored("Error: Build failed - main.js not found", Colors.RED)
        return False
    return True

def deploy_files(plugin_dir):
    """Copy plugin files to vault"""
    Colors.print_colored(f"Creating plugin directory...", Colors.BLUE)
    plugin_dir.mkdir(parents=True, exist_ok=True)
    
    Colors.print_colored(f"Copying files to {plugin_dir}...", Colors.BLUE)
    
    # Copy required files
    files_to_copy = [
        ("main.js", True),
        ("manifest.json", True),
        ("styles.css", False)  # Optional
    ]
    
    for filename, required in files_to_copy:
        src = Path(filename)
        if src.exists():
            dst = plugin_dir / filename
            shutil.copy2(src, dst)
            print(f"  ✓ Copied {filename}")
        elif required:
            Colors.print_colored(f"Error: Required file {filename} not found", Colors.RED)
            return False
    
    return True

def main():
    """Main deployment workflow"""
    Colors.print_colored("Starting Obsidian plugin deployment...", Colors.BLUE)
    
    # Run build
    if not run_build():
        sys.exit(1)
    
    # Check build output
    if not check_build_output():
        sys.exit(1)
    
    # Detect vault path
    vault_path = detect_vault_path()
    plugin_dir = vault_path / ".obsidian" / "plugins" / PLUGIN_ID
    
    # Deploy files
    if not deploy_files(plugin_dir):
        sys.exit(1)
    
    # Success message
    Colors.print_colored("✓ Deployment complete!", Colors.GREEN)
    print(f"Plugin deployed to: {plugin_dir}")
    print("Reload Obsidian to see changes.")

if __name__ == "__main__":
    main()
