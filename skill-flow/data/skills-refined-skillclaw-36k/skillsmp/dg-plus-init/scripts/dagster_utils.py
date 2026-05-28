#!/usr/bin/env python3
"""
Dagster+ Shared Utilities Module

Common functions and utilities used across Dagster+ onboarding scripts.
This module provides reusable functionality for:
- Python environment detection
- Project structure analysis
- Package name detection
- Token validation
- Configuration file management
"""

import os
import sys
import subprocess
import shutil
import yaml
import platform
import re
from pathlib import Path

# -------------------------------
# Constants
# -------------------------------

SERVERLESS_QUICKSTART_REPO = "https://github.com/dagster-io/dagster-cloud-serverless-quickstart.git"
HYBRID_QUICKSTART_REPO = "https://github.com/dagster-io/dagster-cloud-hybrid-quickstart.git"

# Example project repositories
EXAMPLE_REPOSITORIES = {
    "eric-thomas-dagster": [
        {
            "name": "dagster-lakehouse",
            "url": "https://github.com/eric-thomas-dagster/dagster-lakehouse.git",
            "description": "Dagster lakehouse architecture example"
        },
        {
            "name": "dagster-mobile",
            "url": "https://github.com/eric-thomas-dagster/dagster-mobile.git",
            "description": "Dagster mobile data pipeline"
        },
        {
            "name": "embedded_elt_demo",
            "url": "https://github.com/eric-thomas-dagster/embedded_elt_demo.git",
            "description": "Embedded ELT demonstration with Dagster"
        },
        {
            "name": "snowflake-dbt-serverless-example",
            "url": "https://github.com/eric-thomas-dagster/snowflake-dbt-serverless-example.git",
            "description": "Snowflake + dbt serverless example"
        },
        {
            "name": "databricks-observe",
            "url": "https://github.com/eric-thomas-dagster/databricks-observe.git",
            "description": "Databricks observability with Dagster"
        }
    ]
}

DEFAULT_EXAMPLE_SOURCE = "eric-thomas-dagster"

# -------------------------------
# Python Environment Detection
# -------------------------------

def detect_python_executable():
    """Detect the current Python executable being used."""
    return sys.executable

def detect_virtual_environment():
    """Detect if we're running in a virtual environment and return info."""
    venv_info = {
        "in_venv": False,
        "venv_path": None,
        "venv_name": None,
        "python_executable": sys.executable
    }

    # Check for virtual environment
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        venv_info["in_venv"] = True
        venv_info["venv_path"] = sys.prefix
        venv_info["venv_name"] = os.path.basename(sys.prefix)

    # Check for conda environment
    conda_default_env = os.environ.get('CONDA_DEFAULT_ENV')
    if conda_default_env and conda_default_env != 'base':
        venv_info["in_venv"] = True
        venv_info["venv_name"] = conda_default_env
        venv_info["venv_path"] = sys.prefix

    return venv_info

def get_virtual_env_python(venv_path):
    """Get Python executable from a virtual environment path."""
    if platform.system() == "Windows":
        return os.path.join(venv_path, "Scripts", "python.exe")
    else:
        return os.path.join(venv_path, "bin", "python")

def detect_python_version():
    """Detect Python version from the current executable."""
    version_info = sys.version_info
    return f"{version_info.major}.{version_info.minor}"

# -------------------------------
# Project Structure Detection
# -------------------------------

def detect_definitions_type(project_dir, package_name, working_directory):
    """Detect if a project uses load_from_defs_folder() or direct Definitions().

    Returns:
        tuple: (is_components_project, cli_param_type, cli_param_value)
    """
    try:
        # Look for definitions.py in the package
        if working_directory == "src":
            definitions_path = os.path.join(project_dir, "src", package_name, "definitions.py")
        else:
            definitions_path = os.path.join(project_dir, package_name, "definitions.py")

        if os.path.exists(definitions_path):
            with open(definitions_path, 'r') as f:
                content = f.read()

            # Check if it uses load_from_defs_folder
            if "load_from_defs_folder" in content:
                print(f"🔍 Detected Components project using load_from_defs_folder()")
                return True, "module-name", f"{package_name}.definitions"
            elif "Definitions(" in content and "defs" in content:
                print(f"🔍 Detected Components project using direct Definitions()")
                return True, "package-name", package_name
            else:
                print(f"🔍 Detected standard project structure")
                return False, "package-name", package_name
        else:
            # Check if there's a defs/ folder (Components structure)
            if working_directory == "src":
                defs_path = os.path.join(project_dir, "src", package_name, "defs")
            else:
                defs_path = os.path.join(project_dir, package_name, "defs")

            if os.path.exists(defs_path) and os.path.isdir(defs_path):
                print(f"🔍 Detected Components project with defs/ folder")
                return True, "module-name", f"{package_name}.definitions"
            else:
                print(f"🔍 Detected standard project structure")
                return False, "package-name", package_name

    except Exception as e:
        print(f"⚠️  Could not detect definitions type: {e}")
        return False, "package-name", package_name

def detect_package_name(project_dir, structure_working_dir=None, structure_package=None):
    """Detect the correct package name for a project.

    Returns a tuple of (package_name, working_directory_relative_to_project)
    """
    package_name = "unknown"
    working_directory = structure_working_dir or "."

    try:
        # First try to get from dagster_cloud.yaml
        dagster_cloud_path = os.path.join(project_dir, "dagster_cloud.yaml")
        if os.path.exists(dagster_cloud_path):
            with open(dagster_cloud_path, "r") as f:
                cloud_config = yaml.safe_load(f)

            if cloud_config and "locations" in cloud_config:
                for location in cloud_config["locations"]:
                    code_source = location.get("code_source", {})

                    # Handle python_file configuration
                    if "python_file" in code_source:
                        python_file = code_source["python_file"]
                        print(f"🔍 Found python_file configuration: {python_file}")
                        # Convert to package_name (implementation simplified for brevity)
                        if python_file.startswith("src/"):
                            rel_path = python_file[4:]
                            if rel_path.endswith("/definitions.py"):
                                pkg_name = rel_path[:-len("/definitions.py")]
                                package_name = f"{pkg_name}.definitions"
                                working_directory = "src"
                        return package_name, working_directory

                    # Handle existing package_name configuration
                    elif "package_name" in code_source:
                        yaml_package_name = code_source["package_name"]
                        yaml_working_directory = location.get("working_directory", ".")

                        if yaml_package_name not in ["definitions", "my_package.definitions", "my_package"]:
                            package_name = yaml_package_name
                            working_directory = yaml_working_directory
                            print(f"✅ Found package name in dagster_cloud.yaml: {package_name}")
                            return package_name, working_directory
                    break

        # Check pyproject.toml for package information
        pyproject_path = os.path.join(project_dir, "pyproject.toml")
        if os.path.exists(pyproject_path):
            with open(pyproject_path, "r") as f:
                content = f.read()

            # Look for [tool.dagster] module_name or [tool.dg.project] root_module
            dagster_match = re.search(r'\[tool\.dagster\].*?module_name\s*=\s*["\']([^"\']+)["\']', content, re.DOTALL)
            dg_match = re.search(r'\[tool\.dg\.project\].*?root_module\s*=\s*["\']([^"\']+)["\']', content, re.DOTALL)

            if dagster_match:
                module_name = dagster_match.group(1)
                print(f"✅ Found module_name in pyproject.toml: {module_name}")

                # Check if src/ layout
                if os.path.exists(os.path.join(project_dir, "src", module_name)):
                    working_directory = "src"

                # Check for definitions location
                package_path = os.path.join(project_dir, working_directory, module_name) if working_directory != "." else os.path.join(project_dir, module_name)
                init_py = os.path.join(package_path, "__init__.py")
                definitions_py = os.path.join(package_path, "definitions.py")

                if os.path.exists(definitions_py):
                    package_name = f"{module_name}.definitions"
                elif os.path.exists(init_py):
                    with open(init_py, "r") as f:
                        if "defs" in f.read() or "Definitions" in f.read():
                            package_name = module_name
                        else:
                            package_name = f"{module_name}.definitions"
                else:
                    package_name = f"{module_name}.definitions"

                return package_name, working_directory

            elif dg_match:
                root_module = dg_match.group(1)
                if os.path.exists(os.path.join(project_dir, "src", root_module)):
                    working_directory = "src"
                package_name = f"{root_module}.definitions"
                return package_name, working_directory

        # Fallback: scan for Python packages
        print(f"💡 Scanning for project structure...")
        potential_packages = []

        # Check src/ directory
        if os.path.exists(os.path.join(project_dir, "src")):
            src_dir = os.path.join(project_dir, "src")
            for item in os.listdir(src_dir):
                item_path = os.path.join(src_dir, item)
                if os.path.isdir(item_path) and not item.startswith("."):
                    if os.path.exists(os.path.join(item_path, "__init__.py")):
                        potential_packages.append((item, "src"))

        # Check root directory
        for item in os.listdir(project_dir):
            item_path = os.path.join(project_dir, item)
            if os.path.isdir(item_path) and not item.startswith(".") and item != "src":
                if os.path.exists(os.path.join(item_path, "__init__.py")):
                    potential_packages.append((item, "."))

        if potential_packages:
            pkg, location = potential_packages[0]
            package_name = f"{pkg}.definitions"
            working_directory = location
            print(f"📦 Found package: {pkg}")
            return package_name, working_directory

    except Exception as e:
        print(f"⚠️  Could not detect package name: {e}")

    # Final fallback
    dir_name = os.path.basename(os.path.abspath(project_dir))
    package_name = f"{dir_name.replace('-', '_')}.definitions"

    return package_name, working_directory

def detect_components_project(project_dir):
    """Check if a project uses the new Components architecture."""
    try:
        # Look for defs/ folder or load_from_defs_folder usage
        for root, dirs, files in os.walk(project_dir):
            if "defs" in dirs:
                return True
            for file in files:
                if file.endswith(".py"):
                    filepath = os.path.join(root, file)
                    try:
                        with open(filepath, 'r') as f:
                            content = f.read()
                            if "load_from_defs_folder" in content:
                                return True
                    except:
                        pass
        return False
    except:
        return False

def detect_monorepo_structure(project_dir):
    """Detect if this is a monorepo with multiple Dagster projects."""
    projects = []

    # Look for directories with pyproject.toml and Dagster code
    for item in os.listdir(project_dir):
        item_path = os.path.join(project_dir, item)

        if os.path.isdir(item_path) and not item.startswith('.'):
            pyproject_path = os.path.join(item_path, 'pyproject.toml')

            if os.path.exists(pyproject_path):
                # Check if it's a Dagster project
                try:
                    with open(pyproject_path, 'r') as f:
                        content = f.read()
                    if 'dagster' in content.lower():
                        # Detect package name and Components status
                        package_name, working_dir = detect_package_name(item_path)
                        is_components = detect_components_project(item_path)

                        projects.append({
                            'name': item,
                            'path': item_path,
                            'relative_path': item,
                            'package_name': package_name,
                            'working_directory': working_dir,
                            'is_components': is_components
                        })
                except:
                    pass

    is_monorepo = len(projects) > 1
    return is_monorepo, projects

# -------------------------------
# Token Validation
# -------------------------------

def validate_and_extract_token_info(api_token):
    """Validate API token format and extract organization name if possible.

    Returns:
        tuple: (is_valid, token_type, org_name, error_message)
    """
    if not api_token:
        return False, None, None, "API token is required"

    # Check for agent token format: agent:org-name:token-hash
    if api_token.startswith("agent:"):
        parts = api_token.split(":")
        if len(parts) == 3:
            _, org_name, token_hash = parts
            if org_name and token_hash:
                return True, "agent", org_name, None
            else:
                return False, "agent", None, "Invalid agent token format"
        else:
            return False, "agent", None, "Invalid agent token format"

    # Check for user token format: user:token-hash
    elif api_token.startswith("user:"):
        parts = api_token.split(":")
        if len(parts) == 2:
            _, token_hash = parts
            if token_hash:
                return True, "user", None, None
            else:
                return False, "user", None, "Invalid user token format"
        else:
            return False, "user", None, "Invalid user token format"

    else:
        return False, "unknown", None, "Unrecognized token format"

# -------------------------------
# Helper Functions
# -------------------------------

def choose(prompt, options):
    """Interactive menu selection."""
    print(f"\n{prompt}")
    for i, option in enumerate(options, 1):
        print(f"   {i}. {option}")

    while True:
        try:
            choice = input(f"Enter your choice (1-{len(options)}): ").strip()
            choice_num = int(choice)
            if 1 <= choice_num <= len(options):
                return choice_num
            else:
                print(f"Please enter a number between 1 and {len(options)}")
        except ValueError:
            print(f"Please enter a valid number")
        except KeyboardInterrupt:
            print("\n\n❌ Operation cancelled by user")
            sys.exit(0)

def has_cmd(cmd):
    """Check if a command is available."""
    return shutil.which(cmd) is not None

def install_python_packages(packages):
    """Install Python packages using pip."""
    try:
        subprocess.run([sys.executable, "-m", "pip", "install"] + packages, check=True)
        print(f"✅ Installed: {', '.join(packages)}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install packages: {e}")
        return False

def ensure_project_table(project_root):
    """Ensure pyproject.toml has [project] table for uv compatibility."""
    pyproject_path = os.path.join(project_root, "pyproject.toml")

    if not os.path.exists(pyproject_path):
        return False

    try:
        with open(pyproject_path, "r") as f:
            content = f.read()

        # Check if [project] section exists
        if "[project]" not in content:
            # Add a minimal [project] section at the top
            project_name = os.path.basename(project_root).replace("-", "_")
            new_content = f'''[project]
name = "{project_name}"
version = "0.1.0"
dependencies = []

{content}'''
            with open(pyproject_path, "w") as f:
                f.write(new_content)
            print(f"✅ Added [project] table to pyproject.toml")
            return True

        return True
    except Exception as e:
        print(f"⚠️  Could not update pyproject.toml: {e}")
        return False

def check_existing_locations(org_name, api_token, deployment_name):
    """Check for existing code locations."""
    try:
        result = subprocess.run(
            ["dagster-cloud", "workspace", "list", "--organization", org_name, "--deployment", deployment_name],
            capture_output=True, text=True,
            env={**os.environ, "DAGSTER_CLOUD_API_TOKEN": api_token}
        )

        if result.returncode == 0:
            locations = {}
            lines = result.stdout.strip().split('\n')
            for line in lines[1:]:
                if line.strip():
                    parts = line.split()
                    if len(parts) >= 2:
                        location_name = parts[0]
                        package_info = ' '.join(parts[1:])
                        if "Package:" in package_info:
                            package_name = package_info.split("Package:")[-1].strip()
                            locations[location_name] = package_name
            return locations
        else:
            return {}
    except Exception as e:
        print(f"⚠️  Error checking existing locations: {e}")
        return {}

def install_dagster(pkg_mgr):
    """Install Dagster and dagster-cloud packages."""
    print("\n📦 Installing Dagster packages...")

    if pkg_mgr == 2:  # uv
        try:
            subprocess.run(["uv", "pip", "install", "dagster", "dagster-cloud", "dagster-webserver"], check=True)
            print("✅ Dagster packages installed successfully with uv")
        except subprocess.CalledProcessError:
            print("⚠️  uv installation failed, falling back to pip")
            install_python_packages(["dagster", "dagster-cloud", "dagster-webserver"])
    else:  # pip
        install_python_packages(["dagster", "dagster-cloud", "dagster-webserver"])

def get_organization_and_token():
    """Prompt for Dagster+ organization and API token."""
    print("\n🔑 Dagster+ Cloud Authentication")
    print("💡 Get your token from: https://YOUR_ORG.dagster.cloud/settings/tokens")

    api_token = input("Enter your Dagster+ API token: ").strip()

    # Validate and extract info from token
    is_valid, token_type, extracted_org, error_msg = validate_and_extract_token_info(api_token)

    if not is_valid:
        print(f"❌ {error_msg}")
        return None, None

    print(f"✅ Valid {token_type} token detected")

    # For agent tokens, we can extract the org name
    if extracted_org:
        print(f"📊 Organization detected from token: {extracted_org}")
        use_extracted = choose(
            "Use this organization name?",
            ["Yes", "No, enter manually"]
        )

        if use_extracted == 1:
            org_name = extracted_org
        else:
            org_name = input("Enter organization name: ").strip()
    else:
        org_name = input("Enter your Dagster+ organization name: ").strip()

    if not org_name:
        print("❌ Organization name is required")
        return None, None

    return org_name, api_token
