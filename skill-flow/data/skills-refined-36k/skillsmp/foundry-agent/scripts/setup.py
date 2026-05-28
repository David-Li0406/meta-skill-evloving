#!/usr/bin/env python3
"""
Setup script for the Foundry Agent skill.
Handles virtual environment creation, dependency installation, and configuration.
"""

import os
import subprocess
import sys
from pathlib import Path


SKILL_DIR = Path(__file__).parent.parent
VENV_DIR = SKILL_DIR / ".venv"
REQUIREMENTS_FILE = SKILL_DIR / "requirements.txt"
ENV_EXAMPLE = SKILL_DIR / ".env.example"
ENV_FILE = SKILL_DIR / ".env"


def print_header(text: str):
    """Print a formatted header."""
    print(f"\n{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}\n")


def print_step(step: int, text: str):
    """Print a step number."""
    print(f"\n[{step}/5] {text}")


def check_python_version() -> bool:
    """Check Python version is 3.9+."""
    if sys.version_info < (3, 9):
        print(f"  ✗ Python 3.9+ required (you have {sys.version})")
        return False
    print(f"  ✓ Python {sys.version_info.major}.{sys.version_info.minor}")
    return True


def check_venv_exists() -> bool:
    """Check if virtual environment exists."""
    venv_python = VENV_DIR / "bin" / "python"
    return venv_python.exists()


def create_venv() -> bool:
    """Create virtual environment."""
    print(f"  Creating virtual environment at {VENV_DIR}...")
    try:
        result = subprocess.run(
            [sys.executable, "-m", "venv", str(VENV_DIR)],
            capture_output=True,
            text=True,
            timeout=60
        )
        if result.returncode == 0:
            print(f"  ✓ Virtual environment created")
            return True
        else:
            print(f"  ✗ Failed to create venv: {result.stderr}")
            return False
    except subprocess.TimeoutExpired:
        print("  ✗ Venv creation timed out")
        return False


def get_venv_python() -> Path:
    """Get path to venv Python executable."""
    return VENV_DIR / "bin" / "python"


def install_dependencies() -> bool:
    """Install Python dependencies into venv."""
    venv_pip = VENV_DIR / "bin" / "pip"
    print(f"  Installing dependencies into venv...")
    
    try:
        result = subprocess.run(
            [str(venv_pip), "install", "--pre", "-r", str(REQUIREMENTS_FILE)],
            capture_output=True,
            text=True,
            timeout=180
        )
        
        if result.returncode == 0:
            print("  ✓ Dependencies installed")
            return True
        else:
            print(f"  ✗ Installation failed:\n{result.stderr}")
            return False
    except subprocess.TimeoutExpired:
        print("  ✗ Installation timed out")
        return False


def check_dependencies() -> bool:
    """Check if required packages are installed in venv."""
    if not check_venv_exists():
        return False
    
    venv_python = get_venv_python()
    try:
        result = subprocess.run(
            [str(venv_python), "-c", "import azure.ai.projects; import azure.identity; print('OK')"],
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode == 0 and "OK" in result.stdout:
            print("  ✓ Azure packages installed in venv")
            return True
    except subprocess.TimeoutExpired:
        pass
    
    print("  ✗ Azure packages not installed")
    return False


def check_azure_cli() -> bool:
    """Check if Azure CLI is installed."""
    try:
        result = subprocess.run(
            ["az", "--version"],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            version_line = result.stdout.split('\n')[0]
            print(f"  ✓ Azure CLI: {version_line}")
            return True
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass
    
    print("  ✗ Azure CLI not installed")
    print("\n  Install it:")
    print("    macOS:   brew install azure-cli")
    print("    Windows: winget install Microsoft.AzureCLI")
    print("    Linux:   curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash")
    return False


def check_azure_login() -> tuple[bool, str | None]:
    """Check if user is logged into Azure."""
    try:
        result = subprocess.run(
            ["az", "account", "show", "--query", "user.name", "-o", "tsv"],
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode == 0:
            user = result.stdout.strip()
            print(f"  ✓ Logged in as: {user}")
            return True, user
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass
    
    print("  ✗ Not logged into Azure")
    return False, None


def run_az_login() -> bool:
    """Run az login interactively."""
    print("\n  Starting Azure login (a browser window will open)...")
    try:
        result = subprocess.run(["az", "login"], timeout=300)
        return result.returncode == 0
    except subprocess.TimeoutExpired:
        print("  Login timed out")
        return False


def setup_env_file() -> bool:
    """Create .env file from example if needed."""
    if ENV_FILE.exists():
        print(f"  ✓ .env file exists")
        return True
    
    if ENV_EXAMPLE.exists():
        print(f"  Creating .env from example...")
        ENV_FILE.write_text(ENV_EXAMPLE.read_text())
        print(f"  ✓ Created .env")
        print(f"\n  ⚠ Edit the file and set PROJECT_ENDPOINT:")
        print(f"    {ENV_FILE}")
        return True
    
    print("  ✗ No .env.example found")
    return False


def main() -> int:
    """Main setup entry point."""
    print_header("Foundry Agent Skill Setup")
    
    all_ok = True
    
    # Step 1: Check Python version
    print_step(1, "Checking Python version")
    if not check_python_version():
        return 1
    
    # Step 2: Create/check virtual environment
    print_step(2, "Setting up virtual environment")
    if check_venv_exists():
        print(f"  ✓ Virtual environment exists at {VENV_DIR}")
    else:
        if not create_venv():
            print("\n  To create manually:")
            print(f"    python3 -m venv {VENV_DIR}")
            all_ok = False
    
    # Step 3: Install dependencies
    print_step(3, "Installing dependencies")
    if check_venv_exists():
        if not check_dependencies():
            if not install_dependencies():
                all_ok = False
    else:
        print("  ⚠ Skipping (no venv)")
        all_ok = False
    
    # Step 4: Check Azure CLI and login
    print_step(4, "Checking Azure authentication")
    if check_azure_cli():
        logged_in, user = check_azure_login()
        if not logged_in:
            response = input("\n  Login to Azure now? [Y/n]: ").strip().lower()
            if response in ('', 'y', 'yes'):
                if run_az_login():
                    check_azure_login()
                else:
                    all_ok = False
            else:
                print("\n  To login later, run: az login")
                all_ok = False
    else:
        all_ok = False
    
    # Step 5: Setup .env file
    print_step(5, "Configuring environment")
    setup_env_file()
    
    # Summary
    print_header("Setup Complete" if all_ok else "Setup Incomplete")
    
    if all_ok:
        print("You're ready to use the skill!")
        print("\nTest it with:")
        print(f"  python {SKILL_DIR}/scripts/call_agent.py \"Rate my task: test\"")
        print("\nOr activate the venv and use directly:")
        print(f"  source {VENV_DIR}/bin/activate")
        print(f"  python scripts/call_agent.py \"Rate my task: test\"")
    else:
        print("Some steps need attention. See messages above.")
        print("\nAfter fixing issues, run setup again:")
        print(f"  python {SKILL_DIR}/scripts/setup.py")
    
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
