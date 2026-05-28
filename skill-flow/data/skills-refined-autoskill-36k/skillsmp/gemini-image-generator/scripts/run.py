#!/usr/bin/env python3
"""
Wrapper script for gemini-image-generator skill.
Automatically manages virtual environment and dependencies.

Usage:
    python scripts/run.py <script_name> [args...]

Example:
    python scripts/run.py image_generator.py --prompt "sunset over mountains"
"""

import os
import sys
import subprocess
from pathlib import Path

# Get skill root directory
SKILL_ROOT = Path(__file__).parent.parent.absolute()
VENV_DIR = SKILL_ROOT / ".venv"
SCRIPTS_DIR = SKILL_ROOT / "scripts"

def setup_venv():
    """Create virtual environment if it doesn't exist."""
    if VENV_DIR.exists():
        return True

    print(f"📦 Creating virtual environment at {VENV_DIR}...")
    try:
        subprocess.run(
            [sys.executable, "-m", "venv", str(VENV_DIR)],
            check=True,
            capture_output=True
        )
        print("✓ Virtual environment created")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to create venv: {e.stderr.decode()}", file=sys.stderr)
        return False

def install_dependencies():
    """Install requirements if needed."""
    requirements_file = SKILL_ROOT / "requirements.txt"

    if not requirements_file.exists():
        return True

    # Check if already installed
    marker_file = VENV_DIR / ".installed"
    if marker_file.exists():
        return True

    print(f"📦 Installing dependencies from {requirements_file}...")

    # Get pip path
    if sys.platform == "win32":
        pip_path = VENV_DIR / "Scripts" / "pip.exe"
    else:
        pip_path = VENV_DIR / "bin" / "pip"

    try:
        # Install requirements
        subprocess.run(
            [str(pip_path), "install", "-r", str(requirements_file)],
            check=True,
            capture_output=True
        )

        # Install chromium for patchright
        python_path = pip_path.parent / ("python.exe" if sys.platform == "win32" else "python")
        subprocess.run(
            [str(python_path), "-m", "patchright", "install", "chromium"],
            check=True,
            capture_output=True
        )

        # Create marker file
        marker_file.write_text("installed")

        print("✓ Dependencies installed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e.stderr.decode()}", file=sys.stderr)
        return False

def run_script(script_name, args):
    """Run the target script in the virtual environment."""
    # Get python path from venv
    if sys.platform == "win32":
        python_path = VENV_DIR / "Scripts" / "python.exe"
    else:
        python_path = VENV_DIR / "bin" / "python"

    # Find script
    script_path = SCRIPTS_DIR / script_name
    if not script_path.exists():
        print(f"❌ Script not found: {script_path}", file=sys.stderr)
        return 1

    # Run script
    try:
        result = subprocess.run(
            [str(python_path), str(script_path)] + args,
            cwd=SKILL_ROOT,
            env={**os.environ, "PYTHONPATH": str(SKILL_ROOT)}
        )
        return result.returncode
    except Exception as e:
        print(f"❌ Failed to run script: {e}", file=sys.stderr)
        return 1

def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/run.py <script_name> [args...]", file=sys.stderr)
        print("\nAvailable scripts:", file=sys.stderr)
        for script in SCRIPTS_DIR.glob("*.py"):
            if script.name != "run.py":
                print(f"  - {script.name}", file=sys.stderr)
        return 1

    script_name = sys.argv[1]
    script_args = sys.argv[2:]

    # Setup environment
    if not setup_venv():
        return 1

    if not install_dependencies():
        return 1

    # Run script
    return run_script(script_name, script_args)

if __name__ == "__main__":
    sys.exit(main())
