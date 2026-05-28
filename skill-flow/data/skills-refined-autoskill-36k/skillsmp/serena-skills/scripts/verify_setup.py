#!/usr/bin/env python3
"""
Verify serena-skills setup and dependencies
"""
import sys
import importlib.util
from pathlib import Path


def check_python_version():
    """Check Python version"""
    version = sys.version_info
    if version.major == 3 and version.minor >= 8:
        print(f"✓ Python version: {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"✗ Python version: {version.major}.{version.minor}.{version.micro} (requires 3.8+)")
        return False


def check_package(package_name: str, import_name: str = None) -> bool:
    """Check if a package is installed"""
    if import_name is None:
        import_name = package_name
    
    spec = importlib.util.find_spec(import_name)
    if spec is not None:
        print(f"✓ {package_name} installed")
        return True
    else:
        print(f"✗ {package_name} NOT installed")
        return False


def check_lib_directory():
    """Check if lib directory exists and is accessible"""
    script_dir = Path(__file__).parent.parent
    lib_dir = script_dir / "lib"
    
    if lib_dir.exists() and lib_dir.is_dir():
        print(f"✓ lib directory found: {lib_dir}")
        return True
    else:
        print(f"✗ lib directory NOT found at: {lib_dir}")
        return False


def check_scripts_directory():
    """Check if scripts directories exist"""
    script_dir = Path(__file__).parent
    categories = [
        "code-editor",
        "file-ops",
        "memory-manager",
        "project-config",
        "shell-executor",
        "symbol-search",
        "workflow-assistant"
    ]
    
    missing = []
    for category in categories:
        category_dir = script_dir / category
        if not category_dir.exists():
            missing.append(category)
    
    if not missing:
        print(f"✓ All script categories present ({len(categories)} categories)")
        return True
    else:
        print(f"✗ Missing script categories: {', '.join(missing)}")
        return False


def main():
    """Run all verification checks"""
    print("=" * 60)
    print("Serena Skills - Setup Verification")
    print("=" * 60)
    print()
    
    all_checks = []
    
    # Check Python version
    print("1. Checking Python version...")
    all_checks.append(check_python_version())
    print()
    
    # Check required packages
    print("2. Checking required packages...")
    required_packages = [
        ("pathspec", "pathspec"),
        ("requests", "requests"),
        ("pyright", "pyright"),
        ("joblib", "joblib"),
        ("pyyaml", "yaml"),
        ("psutil", "psutil"),
        ("overrides", "overrides"),
        ("python-dotenv", "dotenv"),
        ("typing-extensions", "typing_extensions"),
    ]
    
    for package_name, import_name in required_packages:
        all_checks.append(check_package(package_name, import_name))
    print()
    
    # Check lib directory
    print("3. Checking lib directory...")
    all_checks.append(check_lib_directory())
    print()
    
    # Check scripts directory
    print("4. Checking script categories...")
    all_checks.append(check_scripts_directory())
    print()
    
    # Summary
    print("=" * 60)
    passed = sum(all_checks)
    total = len(all_checks)
    
    if all(all_checks):
        print(f"✓ ALL CHECKS PASSED ({passed}/{total})")
        print()
        print("serena-skills is ready to use!")
        print()
        print("Next steps:")
        print("1. Activate your project:")
        print("   python scripts/project-config/activate_project.py --project-path /path/to/project")
        print()
        print("2. Try listing files:")
        print("   python scripts/file-ops/list_dir.py --project-root /path/to/project --path .")
        print()
        print("3. See SETUP.md for more usage examples")
        return 0
    else:
        print(f"✗ SOME CHECKS FAILED ({passed}/{total} passed)")
        print()
        print("Please address the issues above and run this script again.")
        print()
        print("Installation command:")
        print("python -m pip install pathspec requests pyright joblib pyyaml psutil overrides python-dotenv typing-extensions")
        return 1


if __name__ == "__main__":
    sys.exit(main())
