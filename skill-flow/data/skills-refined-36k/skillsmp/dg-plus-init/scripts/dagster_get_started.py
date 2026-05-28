#!/usr/bin/env python3
"""
Dagster+ Cloud Onboarding Script

This script automates the setup of Dagster+ Cloud projects, including:
- Serverless and Hybrid deployments
- dbt and Airlift integrations
- CI/CD workflows
- Agent deployments
"""

import os
import sys
import subprocess
import shutil
import yaml
import json
import platform
import time
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

# Default example source
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

def extract_migrated_configs(project_dir):
    """Extract migrated configurations from OSS dagster.yaml backup file."""
    migrated_configs = {}
    backup_path = os.path.join(project_dir, "dagster.yaml.oss-backup")
    
    if os.path.exists(backup_path):
        try:
            import yaml
            with open(backup_path, "r") as f:
                oss_config = yaml.safe_load(f)
            
            if oss_config:
                # Extract configurations that should be preserved
                preserved_configs = {}
                
                # Migrate telemetry settings
                if "telemetry" in oss_config:
                    preserved_configs["telemetry"] = oss_config["telemetry"]
                    print(f"   📊 Found telemetry configuration to migrate")
                
                # Migrate compute log manager settings (if not using default storage)
                if "compute_logs" in oss_config:
                    compute_logs = oss_config["compute_logs"]
                    preserved_configs["compute_logs"] = compute_logs
                    print(f"   🔒 Found compute_logs configuration to migrate")
                
                # Migrate logger settings
                if "loggers" in oss_config:
                    preserved_configs["loggers"] = oss_config["loggers"]
                    print(f"   📝 Found loggers configuration to migrate")
                
                # Migrate python_environment settings (if present)
                if "python_environment" in oss_config:
                    preserved_configs["python_environment"] = oss_config["python_environment"]
                    print(f"   🐍 Found python_environment configuration to migrate")
                
                # Migrate code_servers settings (if present)
                if "code_servers" in oss_config:
                    preserved_configs["code_servers"] = oss_config["code_servers"]
                    print(f"   🖥️  Found code_servers configuration to migrate")
                
                migrated_configs = preserved_configs
        except Exception as e:
            print(f"⚠️  Could not extract migrated configs from backup: {e}")
    
    return migrated_configs

def update_dagster_cloud_yaml_for_components(project_dir, package_name, working_directory, is_components, cli_param_type, cli_param_value):
    """Update dagster_cloud.yaml with the correct configuration for Components projects."""
    dagster_cloud_path = os.path.join(project_dir, "dagster_cloud.yaml")
    
    if not os.path.exists(dagster_cloud_path):
        print(f"⚠️  dagster_cloud.yaml not found - skipping update")
        return
    
    try:
        import yaml
        with open(dagster_cloud_path, 'r') as f:
            yaml_data = yaml.safe_load(f)
        
        if not yaml_data or "locations" not in yaml_data:
            print(f"⚠️  Invalid dagster_cloud.yaml structure - skipping update")
            return
        
        updated = False
        for location in yaml_data["locations"]:
            if "code_source" in location:
                # Update the code_source configuration
                if cli_param_type == "module-name":
                    # For Components projects with load_from_defs_folder, use package_name
                    if "module_name" in location["code_source"]:
                        del location["code_source"]["module_name"]
                    location["code_source"]["package_name"] = cli_param_value
                    print(f"✅ Updated dagster_cloud.yaml: module_name -> package_name {cli_param_value}")
                    updated = True
                elif cli_param_type == "package-name":
                    # For standard projects, use package_name
                    if "module_name" in location["code_source"]:
                        del location["code_source"]["module_name"]
                    location["code_source"]["package_name"] = cli_param_value
                    print(f"✅ Updated dagster_cloud.yaml: module_name -> package_name {cli_param_value}")
                    updated = True
                
                # Update working_directory if needed
                if working_directory != ".":
                    location["working_directory"] = working_directory
                    print(f"✅ Updated dagster_cloud.yaml working_directory: {working_directory}")
                    updated = True
        
        if updated:
            with open(dagster_cloud_path, 'w') as f:
                yaml.dump(yaml_data, f, default_flow_style=False, sort_keys=False)
            print(f"✅ Updated dagster_cloud.yaml for Components project")
        else:
            print(f"✅ dagster_cloud.yaml already correctly configured")
            
    except Exception as e:
        print(f"⚠️  Could not update dagster_cloud.yaml: {e}")

def detect_definitions_type(project_dir, package_name, working_directory):
    """Detect if a project uses load_from_defs_folder() or direct Definitions().
    
    Returns:
        tuple: (is_components_project, cli_param_type, cli_param_value)
        - is_components_project: True if uses load_from_defs_folder()
        - cli_param_type: "module-name" or "package-name"
        - cli_param_value: The value to use for the CLI parameter
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
        # Default to standard project
        return False, "package-name", package_name

def detect_package_name(project_dir, structure_working_dir=None, structure_package=None):
    """Detect the correct package name for a project with enhanced support for various layouts.
    
    Returns a tuple of (package_name, working_directory_relative_to_project)
    """
    package_name = "unknown"
    working_directory = structure_working_dir or "."  # Use structure-detected working directory
    
    # Note: structure_package is only used for debugging, not for override
    # Let the normal detection logic run completely
    
    try:
        # First try to get from dagster_cloud.yaml
        dagster_cloud_path = os.path.join(project_dir, "dagster_cloud.yaml")
        if os.path.exists(dagster_cloud_path):
            import yaml
            with open(dagster_cloud_path, "r") as f:
                cloud_config = yaml.safe_load(f)
            
            if cloud_config and "locations" in cloud_config:
                for location in cloud_config["locations"]:
                    code_source = location.get("code_source", {})
                    
                    # Handle python_file configuration (convert to package_name)
                    if "python_file" in code_source:
                        python_file = code_source["python_file"]
                        print(f"🔍 Found python_file configuration: {python_file}")
                        
                        # Convert python_file to package_name
                        if python_file.startswith("src/"):
                            # src/my_package/definitions.py -> my_package.definitions
                            rel_path = python_file[4:]  # Remove "src/"
                            if rel_path.endswith("/definitions.py"):
                                pkg_name = rel_path[:-len("/definitions.py")]
                                package_name = f"{pkg_name}.definitions"
                                working_directory = "src"
                                print(f"💡 Converted to package_name: {package_name} (working_directory: {working_directory})")
                            elif rel_path.endswith(".py"):
                                # Extract package from file path
                                pkg_path = rel_path[:-3].replace("/", ".")
                                package_name = pkg_path
                                working_directory = "src"
                                print(f"💡 Converted to package_name: {package_name} (working_directory: {working_directory})")
                        else:
                            # Regular python file -> try to extract package
                            if python_file.endswith("/definitions.py"):
                                pkg_name = python_file[:-len("/definitions.py")]
                                package_name = f"{pkg_name}.definitions"
                                print(f"💡 Converted to package_name: {package_name}")
                        
                        # Update the dagster_cloud.yaml to use package_name instead
                        if package_name != "unknown":
                            location["code_source"] = {
                                "package_name": package_name
                            }
                            location["working_directory"] = working_directory
                            
                            with open(dagster_cloud_path, "w") as f:
                                yaml.dump(cloud_config, f, default_flow_style=False, sort_keys=False)
                            print(f"✅ Updated dagster_cloud.yaml: python_file -> package_name")
                            return package_name, working_directory
                    
                    # Handle existing package_name configuration
                    elif "package_name" in code_source:
                        yaml_package_name = code_source["package_name"]
                        
                        # Also check for working_directory in the location config
                        yaml_working_directory = location.get("working_directory", ".")
                        
                        # Validate if this package name is problematic (like "definitions")
                        if yaml_package_name in ["definitions", "my_package.definitions", "my_package"]:
                            print(f"⚠️  Package name '{yaml_package_name}' detected - this may need correction")
                            # Don't use this, continue to better detection
                            break
                        else:
                            package_name = yaml_package_name
                            working_directory = yaml_working_directory
                            print(f"✅ Found package name in dagster_cloud.yaml: {package_name}")
                            if working_directory != ".":
                                print(f"✅ Found working directory in dagster_cloud.yaml: {working_directory}")
                            return package_name, working_directory  # Return early if we found a good one
                    break
        
        # If we couldn't get package name from dagster_cloud.yaml, try other sources
        if package_name == "unknown":
            # Check pyproject.toml for [tool.dagster] module_name
            pyproject_path = os.path.join(project_dir, "pyproject.toml")
            if os.path.exists(pyproject_path):
                try:
                    with open(pyproject_path, "r") as f:
                        content = f.read()
                    
                    # Look for [tool.dagster] module_name
                    import re
                    dagster_match = re.search(r'\[tool\.dagster\].*?module_name\s*=\s*["\']([^"\']+)["\']', content, re.DOTALL)
                    if dagster_match:
                        module_name = dagster_match.group(1)
                        print(f"✅ Found module_name in pyproject.toml: {module_name}")
                        
                        # Check if this is a src/ layout first
                        src_package_path = os.path.join(project_dir, "src", module_name)
                        if os.path.exists(src_package_path):
                            working_directory = "src"
                            package_path = src_package_path
                            print(f"💡 Detected src/ layout for {module_name}")
                        else:
                            package_path = os.path.join(project_dir, module_name)
                        
                        # Check if definitions are in __init__.py or definitions.py
                        init_py_path = os.path.join(package_path, "__init__.py")
                        definitions_py_path = os.path.join(package_path, "definitions.py")
                        
                        if os.path.exists(init_py_path):
                            try:
                                with open(init_py_path, "r") as f:
                                    init_content = f.read()
                                if "defs" in init_content or "Definitions" in init_content:
                                    package_name = module_name  # Just the package name
                                    print(f"💡 Definitions found in {module_name}/__init__.py, using package name: {package_name}")
                                elif os.path.exists(definitions_py_path):
                                    package_name = f"{module_name}.definitions"
                                    print(f"💡 Definitions found in {module_name}/definitions.py, using: {package_name}")
                                else:
                                    package_name = f"{module_name}.definitions"  # Default fallback
                            except Exception:
                                package_name = f"{module_name}.definitions"  # Default fallback
                        else:
                            package_name = f"{module_name}.definitions"  # Default fallback
                        
                        # Update dagster_cloud.yaml if it has problematic package names
                        try:
                            dagster_cloud_path = os.path.join(project_dir, "dagster_cloud.yaml")
                            if os.path.exists(dagster_cloud_path):
                                import yaml
                                with open(dagster_cloud_path, "r") as f:
                                    yaml_data = yaml.safe_load(f)
                                
                                updated = False
                                if yaml_data and "locations" in yaml_data:
                                    for location in yaml_data["locations"]:
                                        if "code_source" in location and "package_name" in location["code_source"]:
                                            old_package = location["code_source"]["package_name"]
                                            if old_package in ["definitions", "my_package.definitions", "my_package"]:
                                                location["code_source"]["package_name"] = package_name
                                                print(f"✅ Updated dagster_cloud.yaml package name from '{old_package}' to '{package_name}'")
                                                updated = True
                                
                                if updated:
                                    # Write back the updated YAML
                                    with open(dagster_cloud_path, "w") as f:
                                        yaml.dump(yaml_data, f, default_flow_style=False, sort_keys=False)
                        except Exception as e:
                            print(f"⚠️  Could not update dagster_cloud.yaml: {e}")
                    else:
                        # Look for [tool.dg.project] root_module
                        dg_match = re.search(r'\[tool\.dg\.project\].*?root_module\s*=\s*["\']([^"\']+)["\']', content, re.DOTALL)
                        if dg_match:
                            root_module = dg_match.group(1)
                            
                            # Check if this is a src/ layout
                            src_package_path = os.path.join(project_dir, "src", root_module)
                            if os.path.exists(src_package_path):
                                working_directory = "src"
                                print(f"💡 Detected src/ layout for {root_module}")
                            
                            package_name = f"{root_module}.definitions"
                        
                except Exception as e:
                    print(f"⚠️  Could not parse pyproject.toml: {e}")
            
            # If still unknown, do enhanced smart package detection
            if package_name == "unknown":
                print(f"💡 Checking for common project structures...")
                
                # Look for Python packages with Dagster definitions
                potential_packages = []
                working_dir_suggestion = "."
                original_cwd = os.getcwd()
                os.chdir(project_dir)
                
                try:
                    # Check for src/ directory layout first
                    if os.path.exists("src") and os.path.isdir("src"):
                        print(f"🔍 Found src/ directory - checking for packages...")
                        src_packages = []
                        for item in os.listdir("src"):
                            src_item_path = os.path.join("src", item)
                            if os.path.isdir(src_item_path) and not item.startswith("."):
                                init_py_path = os.path.join(src_item_path, "__init__.py")
                                definitions_py_path = os.path.join(src_item_path, "definitions.py")
                                
                                # Check for package with definitions.py
                                if os.path.exists(init_py_path) and os.path.exists(definitions_py_path):
                                    src_packages.append((item, "definitions", "src"))
                                # Check for package with __init__.py containing definitions
                                elif os.path.exists(init_py_path):
                                    try:
                                        with open(init_py_path, "r") as f:
                                            init_content = f.read()
                                        if "defs" in init_content or "Definitions" in init_content or "definitions" in init_content:
                                            src_packages.append((item, "init", "src"))
                                    except Exception:
                                        pass
                        
                        if src_packages:
                            potential_packages.extend(src_packages)
                            working_dir_suggestion = "src"
                            print(f"📦 Found {len(src_packages)} package(s) in src/ directory")
                    
                    # Check root directory for packages
                    for item in os.listdir("."):
                        if os.path.isdir(item) and not item.startswith(".") and item != "src":
                            init_py_path = os.path.join(item, "__init__.py")
                            definitions_py_path = os.path.join(item, "definitions.py")
                            
                            # Check for package with definitions.py
                            if os.path.exists(init_py_path) and os.path.exists(definitions_py_path):
                                potential_packages.append((item, "definitions", "."))
                            # Check for package with __init__.py containing definitions
                            elif os.path.exists(init_py_path):
                                try:
                                    with open(init_py_path, "r") as f:
                                        init_content = f.read()
                                    if "defs" in init_content or "Definitions" in init_content or "definitions" in init_content:
                                        potential_packages.append((item, "init", "."))
                                except Exception:
                                    pass
                    
                    if potential_packages:
                        # Display found packages with their types
                        package_descriptions = []
                        for pkg_name, pkg_type, location in potential_packages:
                            location_desc = f"in {location}/" if location != "." else ""
                            if pkg_type == "definitions":
                                package_descriptions.append(f"{pkg_name} ({location_desc}has definitions.py)")
                            else:
                                package_descriptions.append(f"{pkg_name} ({location_desc}has definitions in __init__.py)")
                        
                        print(f"📁 Found potential package(s): {', '.join(package_descriptions)}")
                        
                        # Prioritize src/ packages, then determine correct package name
                        src_packages = [p for p in potential_packages if p[2] == "src"]
                        if src_packages:
                            first_pkg, first_type, first_location = src_packages[0]
                            working_dir_suggestion = "src"
                        else:
                            first_pkg, first_type, first_location = potential_packages[0]
                            working_dir_suggestion = first_location
                        
                        if first_type == "definitions":
                            suggested_package = f"{first_pkg}.definitions"
                            print(f"💡 Suggested package_name: {suggested_package}")
                        else:  # init type
                            suggested_package = first_pkg
                            print(f"💡 Suggested package_name: {suggested_package}")
                            print(f"💡 (Since definitions are in {first_pkg}/__init__.py, just use the package name)")
                        
                        if working_dir_suggestion != ".":
                            print(f"💡 Suggested working_directory: {working_dir_suggestion}")
                        
                        package_name = suggested_package
                        working_directory = working_dir_suggestion
                        
                        # Also update the dagster_cloud.yaml file if it exists with bad package name
                        try:
                            dagster_cloud_path = os.path.join(project_dir, "dagster_cloud.yaml")
                            if os.path.exists(dagster_cloud_path):
                                import yaml
                                with open(dagster_cloud_path, "r") as f:
                                    yaml_data = yaml.safe_load(f)
                                
                                updated = False
                                # Update package names in locations
                                if yaml_data and "locations" in yaml_data:
                                    for location in yaml_data["locations"]:
                                        # Update package_name if it's problematic
                                        if "code_source" in location:
                                            code_source = location["code_source"]
                                            
                                            # Handle package_name updates
                                            if "package_name" in code_source:
                                                old_package = code_source["package_name"]
                                                if old_package in ["definitions", "my_package.definitions", "my_package"]:
                                                    code_source["package_name"] = suggested_package
                                                    print(f"✅ Updated dagster_cloud.yaml package name from '{old_package}' to '{suggested_package}'")
                                                    updated = True
                                            
                                            # Handle python_file -> package_name conversion
                                            elif "python_file" in code_source:
                                                code_source["package_name"] = suggested_package
                                                del code_source["python_file"]  # Remove python_file
                                                print(f"✅ Converted python_file to package_name: {suggested_package}")
                                                updated = True
                                        
                                        # Update working_directory if needed
                                        if working_dir_suggestion != "." and "working_directory" not in location:
                                            location["working_directory"] = working_dir_suggestion
                                            print(f"✅ Set working_directory to: {working_dir_suggestion}")
                                            updated = True
                                        elif working_dir_suggestion != "." and location.get("working_directory", ".") != working_dir_suggestion:
                                            location["working_directory"] = working_dir_suggestion
                                            print(f"✅ Updated working_directory to: {working_dir_suggestion}")
                                            updated = True
                                
                                # Write back the updated YAML if changes were made
                                if updated:
                                    with open(dagster_cloud_path, "w") as f:
                                        yaml.dump(yaml_data, f, default_flow_style=False, sort_keys=False)
                        except Exception as e:
                            print(f"⚠️  Could not update dagster_cloud.yaml: {e}")
                    else:
                        # Last resort: use directory name (with proper Python identifier conversion)
                        dir_name = os.path.basename(os.path.abspath(project_dir))
                        if "quickstart" in dir_name.lower():
                            package_name = "quickstart_etl.definitions"
                        else:
                            # Convert directory name to valid Python identifier
                            python_safe_name = dir_name.replace("-", "_").replace(" ", "_")
                            # Remove any other invalid characters
                            import re
                            python_safe_name = re.sub(r'[^a-zA-Z0-9_]', '_', python_safe_name)
                            
                            package_name = f"{python_safe_name}.definitions"
                            if python_safe_name != dir_name:
                                print(f"💡 Directory name '{dir_name}' converted to Python-safe '{python_safe_name}'")
                            print(f"💡 Using directory-based package name: {package_name}")
                            print(f"⚠️  Note: This is a fallback - consider creating a proper Python package structure")
                            
                finally:
                    os.chdir(original_cwd)
        
    except Exception as e:
        print(f"⚠️  Could not detect package name: {e}")
        # Final fallback
        dir_name = os.path.basename(os.path.abspath(project_dir))
        package_name = f"{dir_name}.definitions"
    
    # Note: structure_package fallback removed - let normal detection handle everything
    
    return package_name, working_directory

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
                return False, "agent", None, "Invalid agent token format: missing organization or token hash"
        else:
            return False, "agent", None, "Invalid agent token format: expected 'agent:organization:token'"
    
    # Check for user token format: user:token-hash
    elif api_token.startswith("user:"):
        parts = api_token.split(":")
        if len(parts) == 2:
            _, token_hash = parts
            if token_hash:
                # Accept user tokens - deployment type compatibility will be checked later
                return True, "user", None, None
            else:
                return False, "user", None, "Invalid user token format: missing token hash"
        else:
            return False, "user", None, "Invalid user token format: expected 'user:token'"
    
    # Unknown token format
    else:
        return False, "unknown", None, "Unrecognized token format. Expected agent token like 'agent:organization:token' or user token like 'user:token'"

def check_existing_locations(org_name, api_token, deployment_name):
    """Check for existing code locations and detect potential conflicts."""
    try:
        result = subprocess.run(
            ["dagster-cloud", "workspace", "list", "--organization", org_name, "--deployment", deployment_name],
            capture_output=True, text=True, 
            env={**os.environ, "DAGSTER_CLOUD_API_TOKEN": api_token}
        )
        
        if result.returncode == 0:
            locations = {}
            lines = result.stdout.strip().split('\n')
            for line in lines[1:]:  # Skip header
                if line.strip():
                    parts = line.split()
                    if len(parts) >= 2:
                        location_name = parts[0]
                        package_info = ' '.join(parts[1:])
                        # Extract package name from "Package: package_name" format
                        if "Package:" in package_info:
                            package_name = package_info.split("Package:")[-1].strip()
                            locations[location_name] = package_name
            
            return locations
        else:
            print(f"⚠️  Could not list existing locations: {result.stderr}")
            return {}
    except Exception as e:
        print(f"⚠️  Error checking existing locations: {e}")
        return {}

def detect_and_adjust_project_structure():
    """Detect project structure and return the correct project directory and working directory."""
    current_dir = os.getcwd()
    current_basename = os.path.basename(current_dir)
    
    # Check if we're inside a src/ structure (package subdirectory)
    if "src" in current_dir and current_basename != "src":
        parent_dir = os.path.dirname(current_dir)
        if os.path.basename(parent_dir) == "src":
            # We're in /project/src/package_name/
            project_root = os.path.dirname(parent_dir)  # /project/
            src_dir = parent_dir  # /project/src/
            package_name = current_basename.replace("-", "_")  # Fix hyphens
            
            print(f"\n🔍 Detected src/ layout structure:")
            print(f"   📁 Project root: {project_root}")
            print(f"   📁 Source directory: {src_dir}")
            print(f"   📦 Package name: {package_name}")
            print(f"   📍 Current location: {current_dir}")
            
            choice = choose(
                "How would you like to proceed?",
                [
                    f"Auto-adjust: Use {src_dir} as working directory (recommended)",
                    "Continue from current directory (may cause issues)",
                    "Exit and run from project root manually"
                ]
            )
            
            if choice == 1:
                print(f"✅ Auto-adjusting to use proper working directory")
                return project_root, "src", package_name, True
            elif choice == 2:
                print(f"⚠️  Continuing from current directory - please verify configurations carefully")
                return current_dir, ".", current_basename.replace("-", "_"), False
            else:
                print(f"✅ Please run the script from the project root directory: {project_root}")
                sys.exit(0)
    
    # Default: use current directory as project root
    return current_dir, ".", None, False

def stop_running_agents():
    """Stop any running Dagster agents to prevent log flooding during location changes."""
    try:
        print(f"🛑 Stopping any running agents to prevent log conflicts...")
        result = subprocess.run(["pkill", "-f", "dagster.*agent"], 
                              check=False, capture_output=True, text=True)
        
        # Check if any processes were killed
        if result.returncode == 0:
            print(f"✅ Stopped running agents")
            time.sleep(2)  # Give processes time to stop
        else:
            print(f"💡 No running agents found to stop")
            
        return True
    except Exception as e:
        print(f"⚠️  Could not stop agents: {e}")
        return False

def check_agent_running(org_name, deployment_name, api_token):
    """Check if any agents are running for the deployment."""
    try:
        # Method 1: Check if there are any running local processes
        process_check = subprocess.run(
            ["pgrep", "-f", "dagster.*agent"], 
            capture_output=True, text=True
        )
        local_agent_running = process_check.returncode == 0
        
        # Method 2: Try to list workspace (simple check)
        result = subprocess.run([
            "dagster-cloud", "workspace", "list",
            "--organization", org_name,
            "--deployment", deployment_name,
            "--api-token", api_token
        ], capture_output=True, text=True, timeout=10)
        
        cloud_accessible = result.returncode == 0
        
        print(f"🔍 Agent detection:")
        print(f"   Local agent process: {'✅ Running' if local_agent_running else '❌ Not found'}")
        print(f"   Cloud accessibility: {'✅ Connected' if cloud_accessible else '❌ No connection'}")
        
        # If we can access the workspace OR there's a local agent process, assume agent is working
        return local_agent_running or cloud_accessible
        
    except Exception as e:
        print(f"🔍 Agent check failed: {e}")
        # Fallback: check for local processes only
        try:
            process_check = subprocess.run(
                ["pgrep", "-f", "dagster.*agent"], 
                capture_output=True, text=True
            )
            return process_check.returncode == 0
        except:
            return False

def scan_for_problematic_yaml_files(project_dir):
    """Scan for problematic dagster_cloud.yaml files in subdirectories."""
    problematic_files = []
    
    try:
        for root, dirs, files in os.walk(project_dir):
            if "dagster_cloud.yaml" in files:
                yaml_path = os.path.join(root, "dagster_cloud.yaml")
                # Skip the main project dagster_cloud.yaml
                if os.path.abspath(yaml_path) == os.path.abspath(os.path.join(project_dir, "dagster_cloud.yaml")):
                    continue
                
                try:
                    import yaml
                    with open(yaml_path, "r") as f:
                        yaml_content = yaml.safe_load(f)
                    
                    if yaml_content and "locations" in yaml_content:
                        for location in yaml_content["locations"]:
                            if "code_source" in location and "package_name" in location["code_source"]:
                                package_name = location["code_source"]["package_name"]
                                if package_name.startswith(".."):
                                    relative_path = os.path.relpath(yaml_path, project_dir)
                                    problematic_files.append({
                                        "file": relative_path,
                                        "package": package_name,
                                        "location": location.get("location_name", "unknown")
                                    })
                except Exception as e:
                    # Skip files that can't be parsed
                    continue
    except Exception as e:
        # Skip if directory scanning fails
        pass
    
    return problematic_files

def validate_package_configuration(package_name, working_directory):
    """Validate package configuration and warn about potential issues."""
    issues = []
    
    # Check for problematic package names
    if package_name.startswith(".."):
        issues.append(f"❌ Invalid package name '{package_name}' - relative imports not allowed")
    elif package_name == "definitions":
        issues.append(f"⚠️  Generic package name '{package_name}' - consider using a more specific name")
    elif package_name in ["my_package.definitions", "my_package"]:
        issues.append(f"⚠️  Placeholder package name '{package_name}' - update to your actual package name")
    
    # Check working directory issues
    if "src" in package_name and working_directory == ".":
        issues.append(f"💡 Package name suggests src/ layout but working directory is current dir")
    
    return issues

def handle_location_conflict(location_name, existing_package, new_package, existing_locations):
    """Handle conflicts when a location already exists with different configuration."""
    print(f"\n⚠️  Location '{location_name}' already exists!")
    print(f"   Existing package: {existing_package}")
    print(f"   New package: {new_package}")
    
    # Check for problematic existing configurations
    is_existing_problematic = existing_package in ["..definitions", "definitions", "my_package.definitions"]
    is_new_better = not new_package.startswith("..") and "definitions" in new_package
    
    if is_existing_problematic and is_new_better:
        print(f"💡 The existing configuration appears problematic (invalid package name)")
        choice = choose(
            f"How would you like to handle this conflict?",
            [
                f"Update existing location with correct package ({new_package})",
                f"Create new location with different name", 
                f"Skip adding this location"
            ]
        )
    else:
        choice = choose(
            f"How would you like to handle this conflict?",
            [
                f"Update existing location with new package ({new_package})",
                f"Create new location with different name",
                f"Skip adding this location"
            ]
        )
    
    if choice == 1:
        return "update", location_name
    elif choice == 2:
        # Suggest alternative names
        base_name = location_name.rstrip('-0123456789')
        suggestions = [
            f"{base_name}-v2",
            f"{base_name}-new", 
            f"{base_name}-{len(existing_locations) + 1}"
        ]
        
        print(f"\n💡 Suggested alternative names:")
        for i, suggestion in enumerate(suggestions, 1):
            print(f"   {i}. {suggestion}")
        
        new_name = input(f"Enter new location name (or press Enter for '{suggestions[0]}'): ").strip()
        if not new_name:
            new_name = suggestions[0]
        
        return "create", new_name
    else:
        return "skip", None

def get_organization_and_token():
    """Get and validate organization name and API token with smart extraction."""
    
    # Check for environment variable first
    api_token = os.environ.get("DAGSTER_CLOUD_API_TOKEN", "").strip()
    
    if api_token:
        print("\n🔑 API Token Configuration:")
        print("✅ Using API token from environment variable")
    else:
        # Get API token interactively if not in environment
        print("\n🔑 API Token Configuration:")
        api_token = input("Enter your Dagster+ API token: ").strip()
        if not api_token:
            print("❌ API token is required")
            return None, None
    
    # Validate and extract info from token
    is_valid, token_type, extracted_org, error_msg = validate_and_extract_token_info(api_token)
    
    if not is_valid:
        print(f"❌ {error_msg}")
        if token_type == "user":
            print("💡 To create an agent token:")
            print("   1. Go to your Dagster+ organization settings")
            print("   2. Navigate to 'Tokens' section")
            print("   3. Click 'Create Agent Token'")
            print("   4. Copy the token that starts with 'agent:'")
        return None, None
    
    # Get organization name with smart default from token
    print(f"\n🏢 Organization Configuration:")
    if extracted_org:
        print(f"💡 Detected organization from token: {extracted_org}")
        org_prompt = f"Enter your Dagster+ organization name (or press Enter for '{extracted_org}'): "
        org_name = input(org_prompt).strip()
        if not org_name:
            org_name = extracted_org
            print(f"✅ Using organization: {org_name}")
    else:
        org_name = input("Enter your Dagster+ organization name: ").strip()
        if not org_name:
            print("❌ Organization name is required")
            return None, None
    
    return org_name, api_token

def diagnose_agent_issues(org_name, api_token):
    """Diagnose potential agent creation issues in Dagster+ organization."""
    print(f"\n🔍 Diagnosing Dagster+ Organization State...")
    print(f"   Organization: {org_name}")
    print(f"")
    
    try:
        # Check if dagster-cloud CLI is available
        if not has_cmd("dagster-cloud"):
            print(f"❌ dagster-cloud CLI not available for diagnostics")
            print(f"💡 Install with: pip install dagster-cloud")
            return
        
        print(f"🔍 Checking deployments...")
        deployments_result = subprocess.run(
            ["dagster-cloud", "deployment", "list", "--organization", org_name],
            capture_output=True, text=True, env={**os.environ, "DAGSTER_CLOUD_API_TOKEN": api_token}
        )
        
        if deployments_result.returncode == 0:
            print(f"✅ Deployments in organization:")
            print(f"   {deployments_result.stdout}")
        else:
            print(f"⚠️  Could not list deployments: {deployments_result.stderr}")
        
        print(f"\n🔍 Checking for agents...")
        # Try to list agent tokens (might indicate agent setup)
        agent_result = subprocess.run(
            ["dagster-cloud", "agent", "list-tokens", "--organization", org_name],
            capture_output=True, text=True, env={**os.environ, "DAGSTER_CLOUD_API_TOKEN": api_token}
        )
        
        if agent_result.returncode == 0:
            if agent_result.stdout.strip():
                print(f"⚠️  Found agent tokens in organization:")
                print(f"   {agent_result.stdout}")
                print(f"   💡 These may indicate hybrid agents are configured")
            else:
                print(f"✅ No agent tokens found (good for serverless)")
        else:
            print(f"⚠️  Could not check agent tokens: {agent_result.stderr}")
            
        print(f"\n💡 Troubleshooting Tips:")
        print(f"   • Check Dagster+ UI: https://cloud.dagster.io/{org_name}")
        print(f"   • Look for 'Agents' section in left sidebar")
        print(f"   • Serverless deployments should show 'No agents' or only show code locations")
        print(f"   • If you see running agents, they may be from previous hybrid setups")
        
    except Exception as e:
        print(f"❌ Diagnostic failed: {e}")

def check_and_recommend_venv():
    """Check if running in virtual environment and recommend activation if needed."""
    venv_info = detect_virtual_environment()
    current_python = detect_python_executable()
    
    print(f"\n🔍 Environment Check:")
    print(f"   Current Python: {current_python}")
    
    if venv_info["in_venv"]:
        print(f"   ✅ Virtual Environment: {venv_info['venv_name']} ({venv_info['venv_path']})")
        print(f"   💡 Perfect! You're running in a virtual environment.")
        print(f"   💡 This ensures PEX builds will include your project dependencies.")
        return
    
    print(f"   ⚠️  Not running in a virtual environment")
    print(f"")
    print(f"   🚨 IMPORTANT: Virtual Environment Recommended!")
    print(f"   ")
    print(f"   Why this matters:")
    print(f"   • PEX builds (serverless) use the current Python environment")
    print(f"   • System-wide packages may not be included in PEX")
    print(f"   • Virtual environments ensure consistent deployments")
    print(f"   • Prevents conflicts with system packages")
    
    # Check if there's a venv directory in current project
    common_venv_paths = ['venv', '.venv', 'env', '.env']
    found_venvs = []
    for venv_name in common_venv_paths:
        if os.path.exists(venv_name) and os.path.isdir(venv_name):
            venv_python = get_virtual_env_python(venv_name)
            if os.path.exists(venv_python):
                found_venvs.append(venv_name)
    
    if found_venvs:
        print(f"")
        print(f"   🎯 Found virtual environment(s) in your project:")
        for venv in found_venvs:
            print(f"      • {venv}/")
        print(f"")
        print(f"   💡 To activate and run this script from your venv:")
        venv_to_show = found_venvs[0]  # Show commands for the first found venv
        if platform.system() == "Windows":
            print(f"      {venv_to_show}\\Scripts\\activate")
        else:
            print(f"      source {venv_to_show}/bin/activate")
        print(f"      python onboard.py")
    else:
        print(f"")
        print(f"   💡 To create and activate a virtual environment:")
        print(f"      python -m venv venv")
        if platform.system() == "Windows":
            print(f"      venv\\Scripts\\activate")
        else:
            print(f"      source venv/bin/activate")
        print(f"      python onboard.py")
    
    print(f"")
    continue_choice = choose(
        "How would you like to proceed?",
        [
            "Create a virtual environment for me now",
            "Continue anyway (may cause PEX deployment issues)",
            "Exit and activate virtual environment first (recommended)"
        ]
    )
    
    if continue_choice == 1:
        # Create virtual environment
        setup_virtual_environment()
    elif continue_choice == 2:
        print(f"")
        print(f"⚠️  Continuing without virtual environment.")
        print(f"💡 If you encounter PEX deployment issues, consider using Docker build instead.")
        print(f"")
    else:  # continue_choice == 3
        print(f"")
        print(f"✅ Good choice! Please activate your virtual environment and run the script again.")
        print(f"💡 This will ensure the best deployment experience.")
        sys.exit(0)

def setup_virtual_environment():
    """Set up a virtual environment for the project."""
    print(f"\n🏗️  Setting up virtual environment...")
    
    # Suggest venv name based on current directory or common names
    current_dir = os.path.basename(os.getcwd())
    suggested_names = [f"{current_dir}-env", "venv", ".venv", "dagster-env"]
    
    # Check which names are available
    available_names = []
    for name in suggested_names:
        if not os.path.exists(name):
            available_names.append(name)
    
    if not available_names:
        available_names = [f"{current_dir}-env-{int(time.time())}"]  # Fallback with timestamp
    
    suggested_name = available_names[0]
    
    print(f"💡 Suggested virtual environment name: {suggested_name}")
    venv_name = input(f"Enter virtual environment name (or press Enter for '{suggested_name}'): ").strip()
    if not venv_name:
        venv_name = suggested_name
    
    # Check if name already exists
    if os.path.exists(venv_name):
        print(f"⚠️  Directory '{venv_name}' already exists!")
        overwrite = choose(
            f"What would you like to do?",
            [
                f"Use a different name",
                f"Remove existing '{venv_name}' and create new",
                f"Cancel venv creation"
            ]
        )
        
        if overwrite == 1:
            new_name = input(f"Enter a different name: ").strip()
            if new_name and not os.path.exists(new_name):
                venv_name = new_name
            else:
                print(f"❌ Invalid name or already exists. Cancelling venv creation.")
                return False
        elif overwrite == 2:
            try:
                shutil.rmtree(venv_name)
                print(f"🗑️  Removed existing '{venv_name}'")
            except Exception as e:
                print(f"❌ Failed to remove existing directory: {e}")
                return False
        else:
            print(f"❌ Cancelled virtual environment creation.")
            return False
    
    try:
        # Create virtual environment
        print(f"📦 Creating virtual environment '{venv_name}'...")
        subprocess.run([sys.executable, "-m", "venv", venv_name], check=True)
        
        # Get activation command based on OS
        if platform.system() == "Windows":
            activate_cmd = f"{venv_name}\\Scripts\\activate"
            python_path = f"{venv_name}\\Scripts\\python"
        else:  # Unix/Linux/macOS
            activate_cmd = f"source {venv_name}/bin/activate"
            python_path = f"{venv_name}/bin/python"
        
        print(f"✅ Virtual environment '{venv_name}' created successfully!")
        print(f"")
        print(f"🎯 To use your new virtual environment:")
        print(f"   1. Activate it: {activate_cmd}")
        print(f"   2. Re-run this script in the activated environment")
        print(f"")
        print(f"💡 Your virtual environment is located at: {os.path.abspath(venv_name)}")
        print(f"")
        
        # Ask if they want to continue or restart
        continue_choice = choose(
            "What would you like to do now?",
            [
                "Continue setup in current environment (not recommended)",
                "Exit so I can activate the venv and restart (recommended)"
            ]
        )
        
        if continue_choice == 2:
            print(f"")
            print(f"👋 Please activate your virtual environment and re-run this script:")
            print(f"   {activate_cmd}")
            script_name = os.path.basename(sys.argv[0])
            print(f"   python3 {script_name}")
            print(f"")
            print(f"💡 This will ensure all packages are installed in your virtual environment!")
            sys.exit(0)
        else:
            print(f"⚠️  Continuing in current environment...")
            print(f"💡 Remember to activate your venv for future runs!")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to create virtual environment: {e}")
        print(f"💡 You can create one manually:")
        print(f"   python3 -m venv {venv_name}")
        print(f"   {activate_cmd}")
        
        continue_anyway = choose(
            "Continue without virtual environment?",
            ["Yes, continue", "No, exit"]
        )
        
        if continue_anyway == 2:
            sys.exit(0)
        
        return False
    
    except Exception as e:
        print(f"❌ Unexpected error creating virtual environment: {e}")
        return False

def prompt_for_python_environment(project_dir=None):
    """Prompt user to configure Python environment for code location."""
    venv_info = detect_virtual_environment()
    current_python = detect_python_executable()
    python_version = detect_python_version()
    
    print(f"\n🐍 Python Environment Configuration:")
    print(f"   Current Python: {current_python}")
    print(f"   Python Version: {python_version}")
    
    if venv_info["in_venv"]:
        print(f"   ✅ Virtual Environment: {venv_info['venv_name']} ({venv_info['venv_path']})")
    else:
        print(f"   ⚠️  No virtual environment detected (using system Python)")
    
    # Give user options for Python environment
    options = [
        f"Use current Python environment ({current_python})",
        "Specify a different Python executable path",
        "Use project virtual environment (if exists)"
    ]
    
    choice = choose("Which Python environment should be used for this code location?", options)
    
    if choice == 1:
        return current_python
    elif choice == 2:
        while True:
            custom_python = input("Enter path to Python executable: ").strip()
            if os.path.exists(custom_python) and os.access(custom_python, os.X_OK):
                return custom_python
            else:
                print("❌ Invalid Python executable path. Please try again.")
    elif choice == 3:
        if project_dir:
            # Check for common virtual environment locations
            common_venv_paths = [
                os.path.join(project_dir, ".venv"),
                os.path.join(project_dir, "venv"),
                os.path.join(project_dir, "env")
            ]
            
            for venv_path in common_venv_paths:
                if os.path.exists(venv_path):
                    python_exec = get_virtual_env_python(venv_path)
                    if os.path.exists(python_exec):
                        print(f"✅ Found project virtual environment: {venv_path}")
                        # Return absolute path to avoid relative path issues
                        return os.path.abspath(python_exec)
            
            print("❌ No project virtual environment found. Using current Python.")
            return current_python
        else:
            print("❌ No project directory specified. Using current Python.")
            return current_python

# -------------------------------
# Existing Project Detection
# -------------------------------

def detect_dagster_project(project_dir="."):
    """Detect if a directory contains a Dagster project and analyze its structure."""
    project_info = {
        "is_dagster_project": False,
        "has_definitions": False,
        "definitions_files": [],
        "package_structure": [],
        "has_assets": False,
        "has_jobs": False,
        "has_schedules": False,
        "has_sensors": False,
        "suggested_package_name": None,
        "is_components_compatible": False,
        "setup_py_exists": False,
        "pyproject_toml_exists": False
    }
    
    if not os.path.exists(project_dir):
        return project_info
    
    # Check for common Dagster files
    dagster_files = []
    
    # Walk through the directory to find Python files with Dagster imports
    for root, dirs, files in os.walk(project_dir):
        # Skip hidden directories and common ignore patterns
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['__pycache__', 'node_modules']]
        
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        
                    # Check for Dagster imports
                    if any(import_stmt in content for import_stmt in [
                        'import dagster', 'from dagster', 'dagster.', '@asset', '@job', '@schedule', '@sensor'
                    ]):
                        dagster_files.append(file_path)
                        project_info["is_dagster_project"] = True
                        
                        # Check for specific Dagster constructs
                        if '@asset' in content or 'AssetDefinition' in content:
                            project_info["has_assets"] = True
                        if '@job' in content or 'JobDefinition' in content:
                            project_info["has_jobs"] = True
                        if '@schedule' in content or 'ScheduleDefinition' in content:
                            project_info["has_schedules"] = True
                        if '@sensor' in content or 'SensorDefinition' in content:
                            project_info["has_sensors"] = True
                        
                        # Check for Definitions object
                        if 'Definitions(' in content or 'defs =' in content:
                            project_info["has_definitions"] = True
                            project_info["definitions_files"].append(file_path)
                
                except (UnicodeDecodeError, FileNotFoundError):
                    continue
    
    # Detect package structure
    if project_info["is_dagster_project"]:
        # Find Python packages (directories with __init__.py)
        for root, dirs, files in os.walk(project_dir):
            if '__init__.py' in files:
                rel_path = os.path.relpath(root, project_dir)
                if rel_path != '.':
                    package_name = rel_path.replace(os.sep, '.')
                    project_info["package_structure"].append(package_name)
        
        # Suggest package name based on definitions files or structure
        if project_info["definitions_files"]:
            # Use the directory of the first definitions file
            def_file = project_info["definitions_files"][0]
            def_dir = os.path.dirname(def_file)
            rel_path = os.path.relpath(def_dir, project_dir)
            
            if rel_path == '.':
                # definitions.py in root
                if os.path.exists(os.path.join(project_dir, '__init__.py')):
                    project_info["suggested_package_name"] = os.path.basename(project_dir) + ".definitions"
                else:
                    project_info["suggested_package_name"] = "definitions"
            else:
                # definitions.py in subdirectory
                package_path = rel_path.replace(os.sep, '.')
                if os.path.basename(def_file) == 'definitions.py':
                    project_info["suggested_package_name"] = package_path + ".definitions"
                else:
                    project_info["suggested_package_name"] = package_path + "." + os.path.splitext(os.path.basename(def_file))[0]
        elif project_info["package_structure"]:
            # Use first package + .definitions
            project_info["suggested_package_name"] = project_info["package_structure"][0] + ".definitions"
    
    # Check for project files
    project_info["setup_py_exists"] = os.path.exists(os.path.join(project_dir, "setup.py"))
    project_info["pyproject_toml_exists"] = os.path.exists(os.path.join(project_dir, "pyproject.toml"))
    project_info["is_components_compatible"] = is_components_compatible(project_dir)
    
    return project_info

def setup_existing_project(project_dir, pkg_mgr, org_name, deployment_name, location_name=None):
    """Set up an existing Dagster project for Dagster+ deployment."""
    print(f"\n📁 Setting up existing Dagster project: {os.path.abspath(project_dir)}")
    
    # Analyze the project
    project_info = detect_dagster_project(project_dir)
    
    if not project_info["is_dagster_project"]:
        print(f"❌ No Dagster code detected in {project_dir}")
        print(f"💡 Make sure the directory contains Python files with Dagster imports")
        return False
    
    print(f"✅ Dagster project detected!")
    print(f"   📊 Found {len(project_info['package_structure'])} Python packages")
    print(f"   📄 Found {len(project_info['definitions_files'])} definitions files")
    
    if project_info["has_assets"]:
        print(f"   💎 Contains assets")
    if project_info["has_jobs"]:
        print(f"   🏗️  Contains jobs")
    if project_info["has_schedules"]:
        print(f"   ⏰ Contains schedules")
    if project_info["has_sensors"]:
        print(f"   👁️  Contains sensors")
    
    # Ensure dagster-cloud dependency is present
    print(f"\n🔧 Ensuring dagster-cloud dependency is available...")
    project_name = os.path.basename(os.path.abspath(project_dir))
    
    # Check if we need to create setup files
    if not project_info["setup_py_exists"] and not project_info["pyproject_toml_exists"]:
        print(f"📁 Creating project configuration files...")
        
        # Create pyproject.toml
        pyproject_content = f"""[project]
name = "{project_name}"
version = "0.1.0"
description = "Dagster project migrated to Dagster+"
dependencies = [
    "dagster",
    "dagster-cloud",
    "PyYAML",
]

[build-system]
requires = ["setuptools"]
build-backend = "setuptools.build_meta"

[tool.dg]
project = true
"""
        
        pyproject_path = os.path.join(project_dir, "pyproject.toml")
        with open(pyproject_path, "w") as f:
            f.write(pyproject_content)
        print(f"✅ Created pyproject.toml")
        
        # Create setup.py for deployment compatibility
        setup_content = f"""from setuptools import find_packages, setup

setup(
    name="{project_name}",
    packages=find_packages(),
    install_requires=[
        "dagster",
        "dagster-cloud",
        "PyYAML",
    ],
)
"""
        
        setup_path = os.path.join(project_dir, "setup.py")
        with open(setup_path, "w") as f:
            f.write(setup_content)
        print(f"✅ Created setup.py")
    else:
        # Update existing files to ensure dagster-cloud is included
        print(f"📝 Updating existing dependency files to include dagster-cloud...")
        
        # Update pyproject.toml if it exists
        pyproject_path = os.path.join(project_dir, "pyproject.toml")
        if project_info["pyproject_toml_exists"]:
            try:
                with open(pyproject_path, "r") as f:
                    content = f.read()
                
                # Check if dagster-cloud is already in dependencies
                if "dagster-cloud" not in content:
                    print(f"⚙️  Adding dagster-cloud to pyproject.toml dependencies...")
                    
                    # Add dagster-cloud to dependencies section
                    if "dependencies = [" in content:
                        # Find the dependencies section and add dagster-cloud
                        import re
                        # Look for dependencies array and add dagster-cloud if not present
                        if not re.search(r'["\']dagster-cloud["\']', content):
                            # Insert dagster-cloud after dagster if present, or at the end of dependencies
                            if '"dagster"' in content or "'dagster'" in content:
                                content = re.sub(
                                    r'(["\']dagster["\'],?\s*\n)',
                                    r'\1    "dagster-cloud",\n',
                                    content
                                )
                            else:
                                # Add to the end of the dependencies list
                                content = re.sub(
                                    r'(dependencies\s*=\s*\[\s*\n)(.*?)(\s*\])',
                                    r'\1\2    "dagster-cloud",\n\3',
                                    content,
                                    flags=re.DOTALL
                                )
                    else:
                        # Add entire dependencies section if missing
                        content = content.replace(
                            '[project]',
                            '[project]\ndependencies = [\n    "dagster",\n    "dagster-cloud",\n]'
                        )
                    
                    with open(pyproject_path, "w") as f:
                        f.write(content)
                    print(f"✅ Updated pyproject.toml with dagster-cloud dependency")
                else:
                    print(f"✅ dagster-cloud already present in pyproject.toml")
                    
            except Exception as e:
                print(f"⚠️  Could not update pyproject.toml: {e}")
        
        # Update setup.py if it exists
        setup_path = os.path.join(project_dir, "setup.py")
        if project_info["setup_py_exists"]:
            try:
                with open(setup_path, "r") as f:
                    content = f.read()
                
                if "dagster-cloud" not in content:
                    print(f"⚙️  Adding dagster-cloud to setup.py install_requires...")
                    
                    # Add dagster-cloud to install_requires
                    import re
                    if "install_requires" in content:
                        if not re.search(r'["\']dagster-cloud["\']', content):
                            # Insert after dagster if present
                            if '"dagster"' in content or "'dagster'" in content:
                                content = re.sub(
                                    r'(["\']dagster["\'],?\s*\n)',
                                    r'\1        "dagster-cloud",\n',
                                    content
                                )
                            else:
                                # Add to install_requires list
                                content = re.sub(
                                    r'(install_requires\s*=\s*\[\s*\n)(.*?)(\s*\])',
                                    r'\1\2        "dagster-cloud",\n\3',
                                    content,
                                    flags=re.DOTALL
                                )
                    
                    with open(setup_path, "w") as f:
                        f.write(content)
                    print(f"✅ Updated setup.py with dagster-cloud dependency")
                else:
                    print(f"✅ dagster-cloud already present in setup.py")
                    
            except Exception as e:
                print(f"⚠️  Could not update setup.py: {e}")
        
        # Check for requirements.txt and update it if it exists
        requirements_path = os.path.join(project_dir, "requirements.txt")
        if os.path.exists(requirements_path):
            try:
                with open(requirements_path, "r") as f:
                    content = f.read()
                
                if "dagster-cloud" not in content:
                    print(f"⚙️  Adding dagster-cloud to requirements.txt...")
                    
                    # Add dagster-cloud to requirements.txt
                    with open(requirements_path, "a") as f:
                        f.write("\ndagster-cloud\n")
                    print(f"✅ Updated requirements.txt with dagster-cloud dependency")
                else:
                    print(f"✅ dagster-cloud already present in requirements.txt")
                    
            except Exception as e:
                print(f"⚠️  Could not update requirements.txt: {e}")
    
    # Check for existing OSS dagster.yaml and migrate relevant configurations
    oss_dagster_yaml_path = os.path.join(project_dir, "dagster.yaml")
    migrated_configs = {}
    
    if os.path.exists(oss_dagster_yaml_path):
        print(f"\n🔍 Found existing OSS dagster.yaml - checking for configurations to migrate...")
        
        try:
            import yaml
            with open(oss_dagster_yaml_path, "r") as f:
                oss_config = yaml.safe_load(f)
            
            if oss_config:
                # Extract configurations that should be preserved
                preserved_configs = {}
                
                # Migrate telemetry settings
                if "telemetry" in oss_config:
                    preserved_configs["telemetry"] = oss_config["telemetry"]
                    print(f"   📊 Preserving telemetry configuration")
                
                # Migrate compute log manager settings (if not using default storage)
                if "compute_logs" in oss_config:
                    compute_logs = oss_config["compute_logs"]
                    print(f"   🔍 Found compute_logs config: {compute_logs}")
                    
                    # Preserve custom compute log managers (like PII managers)
                    if isinstance(compute_logs, dict):
                        module_name = compute_logs.get("module", "")
                        class_name = compute_logs.get("class", "")
                        
                        # Skip only the default Dagster file manager
                        if module_name == "dagster.core.storage.file_manager":
                            print(f"   ⏭️  Skipping default file manager (Dagster+ provides this)")
                        else:
                            # Preserve all custom compute log managers
                            preserved_configs["compute_logs"] = compute_logs
                            if "pii" in module_name.lower() or "pii" in class_name.lower():
                                print(f"   🔒 Preserving PII-aware compute log manager: {module_name}.{class_name}")
                            else:
                                print(f"   💾 Preserving custom compute log manager: {module_name}.{class_name}")
                    else:
                        # Non-dict compute_logs config - preserve as-is
                        preserved_configs["compute_logs"] = compute_logs
                        print(f"   💾 Preserving compute logs configuration")
                
                # Migrate custom logger configurations
                if "loggers" in oss_config:
                    preserved_configs["loggers"] = oss_config["loggers"]
                    print(f"   📝 Preserving custom logger configuration")
                
                # Migrate python environment settings
                if "python_environment" in oss_config:
                    preserved_configs["python_environment"] = oss_config["python_environment"]
                    print(f"   🐍 Preserving Python environment configuration")
                
                # Migrate code server settings (if they exist and are custom)
                if "code_servers" in oss_config:
                    preserved_configs["code_servers"] = oss_config["code_servers"]
                    print(f"   ⚙️  Preserving code server configuration")
                
                # Store for later use
                migrated_configs = preserved_configs
                
                if preserved_configs:
                    print(f"✅ Found {len(preserved_configs)} configuration(s) to preserve")
                    
                    # Create a backup of the original
                    backup_path = os.path.join(project_dir, "dagster.yaml.oss-backup")
                    import shutil
                    shutil.copy2(oss_dagster_yaml_path, backup_path)
                    print(f"📄 Created backup: {backup_path}")
                else:
                    print(f"ℹ️  No preservable configurations found (storage/execution handled by Dagster+)")
                
                # Warn about configurations that won't be migrated
                excluded_keys = []
                for key in oss_config.keys():
                    if key not in preserved_configs:
                        excluded_keys.append(key)
                
                if excluded_keys:
                    print(f"⚠️  The following configurations will NOT be migrated (handled by Dagster+):")
                    for key in excluded_keys:
                        if key in ["storage", "run_storage", "event_log_storage", "schedule_storage"]:
                            print(f"   - {key} (Dagster+ manages storage)")
                        elif key in ["run_launcher", "executor"]:
                            print(f"   - {key} (Dagster+ manages execution)")
                        elif key in ["run_coordinator"]:
                            print(f"   - {key} (Dagster+ manages coordination)")
                        else:
                            print(f"   - {key} (not applicable to Dagster+)")
                            
        except ImportError:
            print(f"⚠️  PyYAML not available - cannot parse existing dagster.yaml")
            print(f"💡 Install with: pip install PyYAML")
        except Exception as e:
            print(f"⚠️  Could not parse existing dagster.yaml: {e}")
    
    # Create dagster_cloud.yaml if it doesn't exist
    dagster_cloud_path = os.path.join(project_dir, "dagster_cloud.yaml")
    if not os.path.exists(dagster_cloud_path):
        print(f"\n🔧 Creating dagster_cloud.yaml for Dagster+ deployment...")
        
        # Get package name suggestion
        if project_info["suggested_package_name"]:
            suggested_package = project_info["suggested_package_name"]
        else:
            suggested_package = f"{os.path.basename(os.path.abspath(project_dir))}.definitions"
        
        package_name = input(f"Enter package name for your definitions [{suggested_package}]: ").strip()
        if not package_name:
            package_name = suggested_package
        
        if location_name is None:
            location_name = input(f"Enter location name [main]: ").strip() or "main"
        
        # Create basic dagster_cloud.yaml content
        dagster_cloud_content = f"""locations:
  - location_name: {location_name}
    code_source:
      package_name: {package_name}
    build:
      directory: ./
"""
        
        # Add migrated configurations if any exist
        if migrated_configs:
            print(f"🔧 Including {len(migrated_configs)} migrated configuration(s) from OSS dagster.yaml...")
            
            # Add migrated configurations to the YAML content
            import yaml
            try:
                # Parse the basic content
                yaml_data = yaml.safe_load(dagster_cloud_content)
                
                # Add migrated configurations
                for key, value in migrated_configs.items():
                    yaml_data[key] = value
                    print(f"   ✅ Added {key} configuration")
                
                # Convert back to YAML string
                dagster_cloud_content = yaml.dump(yaml_data, default_flow_style=False, sort_keys=False)
                
            except Exception as e:
                print(f"⚠️  Could not merge migrated configurations: {e}")
                print(f"💡 Configurations will be added manually to dagster_cloud.yaml")
        
        with open(dagster_cloud_path, "w") as f:
            f.write(dagster_cloud_content)
        
        print(f"✅ Created dagster_cloud.yaml")
        print(f"   📍 Location: {location_name}")
        print(f"   📦 Package: {package_name}")
    else:
        # dagster_cloud.yaml already exists, but we might have migrated configurations to add
        if migrated_configs:
            print(f"\n🔧 Adding migrated configurations to existing dagster_cloud.yaml...")
            
            try:
                # Read existing content
                with open(dagster_cloud_path, "r") as f:
                    existing_content = f.read()
                
                # Parse and merge configurations
                import yaml
                yaml_data = yaml.safe_load(existing_content)
                
                # Add migrated configurations (don't overwrite existing ones)
                for key, value in migrated_configs.items():
                    if key not in yaml_data:
                        yaml_data[key] = value
                        if key == "compute_logs":
                            print(f"   🔒 Added PII-aware compute_logs configuration")
                        else:
                            print(f"   ✅ Added {key} configuration")
                    else:
                        print(f"   ⚠️  {key} already exists in dagster_cloud.yaml - skipping")
                
                # Write back the updated content
                updated_content = yaml.dump(yaml_data, default_flow_style=False, sort_keys=False)
                with open(dagster_cloud_path, "w") as f:
                    f.write(updated_content)
                
                print(f"✅ Updated existing dagster_cloud.yaml with migrated configurations")
                
            except Exception as e:
                print(f"⚠️  Could not update existing dagster_cloud.yaml: {e}")
                print(f"💡 You may need to manually add configurations from dagster.yaml.oss-backup")
        
        # Check if compute_logs is missing and offer to add it manually
        else:
            try:
                with open(dagster_cloud_path, "r") as f:
                    existing_content = f.read()
                
                # Check if we're missing compute_logs but have a backup
                if "compute_logs" not in existing_content:
                    backup_path = os.path.join(project_dir, "dagster.yaml.oss-backup")
                    if os.path.exists(backup_path):
                        print(f"\n💡 Checking for missing compute_logs configuration...")
                        
                        with open(backup_path, "r") as f:
                            backup_content = f.read()
                        
                        if "compute_logs:" in backup_content:
                            import yaml
                            try:
                                backup_yaml = yaml.safe_load(backup_content)
                                if "compute_logs" in backup_yaml:
                                    compute_logs_config = backup_yaml["compute_logs"]
                                    
                                    if isinstance(compute_logs_config, dict):
                                        module_name = compute_logs_config.get("module", "")
                                        if "pii" in module_name.lower():
                                            print(f"   🔍 Found PII compute_logs in backup: {module_name}")
                                            
                                            add_compute_logs = choose(
                                                "Add PII-aware compute_logs configuration to dagster_cloud.yaml?",
                                                ["Yes, add it now", "No, skip for now"]
                                            )
                                            
                                            if add_compute_logs == 1:
                                                # Add compute_logs to dagster_cloud.yaml
                                                import yaml
                                                existing_yaml = yaml.safe_load(existing_content)
                                                existing_yaml["compute_logs"] = compute_logs_config
                                                
                                                updated_content = yaml.dump(existing_yaml, default_flow_style=False, sort_keys=False)
                                                with open(dagster_cloud_path, "w") as f:
                                                    f.write(updated_content)
                                                
                                                print(f"   ✅ Added PII compute_logs configuration to dagster_cloud.yaml")
                            
                            except Exception as e:
                                print(f"   ⚠️  Could not parse backup file: {e}")
            
            except Exception:
                pass  # Ignore errors in this optional check
    
    # Set up Components compatibility if needed
    if not project_info["is_components_compatible"]:
        enable_components = choose(
            "Your project is not Components-compatible. Enable Components for dbt/Airlift integrations?",
            ["Yes, enable Components", "No, skip for now"]
        )
        
        if enable_components == 1:
            # Install dagster-dg-cli
            print("📦 Installing dagster-dg-cli...")
            original_dir = os.getcwd()
            os.chdir(project_dir)
            
            try:
                if pkg_mgr == 2:  # uv
                    subprocess.run(["uv", "add", "dagster-dg-cli"], check=False)
                else:  # pip
                    subprocess.run(["python3", "-m", "pip", "install", "dagster-dg-cli"], check=True)
                
                # Initialize Components
                subprocess.run(["dg", "project", "init"], check=True)
                print("✅ Enabled Dagster Components!")
                
            except subprocess.CalledProcessError as e:
                print(f"❌ Failed to enable Components: {e}")
            finally:
                os.chdir(original_dir)
    
    return True

def detect_components_project(project_dir):
    """Detect if this is a Dagster Components project.
    
    Returns:
        bool: True if Components project, False if flat/traditional
    """
    # Check 1: Look for defs/ folder anywhere in the project
    for root, dirs, files in os.walk(project_dir):
        # Skip hidden directories and venvs
        if '/.venv' in root or '/.git' in root or '/__pycache__' in root:
            continue
        if 'defs' in dirs:
            # Found a defs/ folder - check if it's a Dagster defs folder
            defs_path = os.path.join(root, 'defs')
            # It should have Python files or be in a module
            if any(f.endswith('.py') for f in os.listdir(defs_path)):
                return True
    
    # Check 2: Look for load_from_defs_folder() in definitions.py
    definitions_files = []
    for root, dirs, files in os.walk(project_dir):
        if '/.venv' in root or '/.git' in root:
            continue
        if 'definitions.py' in files:
            definitions_files.append(os.path.join(root, 'definitions.py'))
    
    for def_file in definitions_files:
        try:
            with open(def_file, 'r') as f:
                content = f.read()
                if 'load_from_defs_folder' in content or 'dg.load_from_defs_folder' in content:
                    return True
        except Exception:
            pass
    
    # Check 3: Look for [tool.dg.project] in pyproject.toml
    pyproject_path = os.path.join(project_dir, "pyproject.toml")
    if os.path.exists(pyproject_path):
        try:
            with open(pyproject_path, 'r') as f:
                content = f.read()
                if '[tool.dg.project]' in content or '[tool.dg]' in content:
                    # Has Components config
                    return True
        except Exception:
            pass
    
    return False

def find_dagster_projects_in_monorepo(root_dir):
    """Find all Dagster projects in a monorepo.
    
    Args:
        root_dir: Root directory of the monorepo
        
    Returns:
        list: List of dicts with project info
    """
    projects = []
    
    # Only look at direct subdirectories, not nested ones
    for item in os.listdir(root_dir):
        item_path = os.path.join(root_dir, item)
        
        # Skip files, hidden directories, and common non-project dirs
        if not os.path.isdir(item_path) or item.startswith('.') or item in ['node_modules', '__pycache__', 'venv', '.venv', 'tests']:
            continue
            
        # Check if this directory is a Dagster project
        if detect_dagster_project(item_path):
            project_name = item
            relative_path = f"./{item}"
            
            projects.append({
                'path': item_path,
                'name': project_name,
                'relative_path': relative_path,
                'is_components': detect_components_project(item_path)
            })
    
    return projects

def detect_monorepo_structure(project_dir):
    """Detect if this is a monorepo with multiple Dagster projects.
    
    Args:
        project_dir: Directory to check
        
    Returns:
        tuple: (is_monorepo, projects_list)
    """
    projects = find_dagster_projects_in_monorepo(project_dir)
    return len(projects) > 1, projects

def update_shared_dagster_cloud_yaml(root_dir, projects, deployment_type="serverless"):
    """Update shared dagster_cloud.yaml with all projects.
    
    Args:
        root_dir: Root directory of the monorepo
        projects: List of project dicts from find_dagster_projects_in_monorepo
        deployment_type: "serverless" or "hybrid"
    """
    dagster_cloud_path = os.path.join(root_dir, "dagster_cloud.yaml")
    
    # Check if dagster_cloud.yaml already exists
    existing_locations = []
    if os.path.exists(dagster_cloud_path):
        print(f"📄 Found existing dagster_cloud.yaml")
        try:
            import yaml
            with open(dagster_cloud_path, 'r') as f:
                existing_config = yaml.safe_load(f)
                if existing_config and 'locations' in existing_config:
                    existing_locations = existing_config['locations']
                    print(f"✅ Found {len(existing_locations)} existing locations")
                else:
                    print(f"⚠️  Existing file doesn't have locations section")
        except Exception as e:
            print(f"⚠️  Could not parse existing dagster_cloud.yaml: {e}")
            existing_locations = []
    
    # Build new locations list
    new_locations = []
    project_names = {project['name'] for project in projects}
    
    # Keep existing locations that aren't in our project list
    for existing_location in existing_locations:
        if existing_location.get('location_name') not in project_names:
            new_locations.append(existing_location)
            print(f"📌 Preserving existing location: {existing_location.get('location_name')}")
    
    # Add/update locations for our projects
    for project in projects:
        # Determine package name
        package_name = f"{project['name'].replace('-', '_')}.definitions"
        
        location = {
            "location_name": project['name'],
            "code_source": {
                "package_name": package_name
            }
        }
        
        # Add working_directory if not root
        if project['relative_path'] != '.':
            location["code_source"]["working_directory"] = project['relative_path']
        
        # Add build configuration for hybrid deployments
        if deployment_type == "hybrid":
            # For hybrid, we might need directory and registry
            # But these are typically set per deployment, not per location
            # So we'll leave build section empty for now
            pass
        
        new_locations.append(location)
        print(f"📝 {'Updated' if any(loc.get('location_name') == project['name'] for loc in existing_locations) else 'Added'} location: {project['name']}")
    
    # Generate YAML content
    yaml_content = {"locations": new_locations}
    
    # Write the file
    with open(dagster_cloud_path, 'w') as f:
        import yaml
        yaml.dump(yaml_content, f, default_flow_style=False, sort_keys=False)
    
    print(f"✅ Updated shared dagster_cloud.yaml with {len(new_locations)} total locations")
    print(f"📄 File: {dagster_cloud_path}")
    
    return dagster_cloud_path


def ensure_dagster_project_files(project_dir):
    """Ensure a cloned project has all necessary Dagster configuration files."""
    print(f"\n🔧 Ensuring Dagster project configuration...")
    
    # Get project name from directory
    project_name = os.path.basename(os.path.abspath(project_dir))
    
    # Detect if this is a Components project
    use_components = detect_components_project(project_dir)
    has_src_layout = os.path.exists(os.path.join(project_dir, "src"))
    
    # Determine the correct configuration based on project structure
    if use_components:
        # Components project structure
        print(f"📁 Detected Dagster Components project")
        module_name = "definitions"
        directory_type = "project" 
    else:
        # Traditional flat project structure
        print(f"📁 Detected traditional Dagster project")
        module_name = "definitions"
        directory_type = "project"
    
    # Create pyproject.toml if missing
    pyproject_path = os.path.join(project_dir, "pyproject.toml")
    if not os.path.exists(pyproject_path):
        print(f"📄 Creating pyproject.toml...")
        
        # Read requirements.txt to get dependencies
        requirements_path = os.path.join(project_dir, "requirements.txt")
        dependencies = []
        if os.path.exists(requirements_path):
            with open(requirements_path, 'r') as f:
                dependencies = [line.strip() for line in f if line.strip() and not line.startswith('#')]
        
        # Create README.md if it doesn't exist (required by pyproject.toml)
        readme_path = os.path.join(project_dir, "README.md")
        if not os.path.exists(readme_path):
            with open(readme_path, 'w') as f:
                f.write(f"""# {project_name}

A Dagster project for data orchestration.

## Getting Started

### For flat projects:
```bash
dagster dev
```

### For Components projects:
```bash
dg dev
```

## Learn More

- [Dagster Documentation](https://docs.dagster.io/)
- [Dagster Components Guide](https://docs.dagster.io/guides/build/projects/moving-to-components)
""")
        
        # Determine if this is a flat project structure
        is_flat_structure = os.path.exists(os.path.join(project_dir, "definitions.py"))
        
        # Create pyproject.toml content
        pyproject_content = f"""[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "{project_name}"
version = "0.1.0"
description = "Dagster project: {project_name}"
readme = "README.md"
requires-python = ">=3.8"
dependencies = [
"""
        
        # Add dependencies from requirements.txt
        for dep in dependencies:
            pyproject_content += f'    "{dep}",\n'
        
        # Ensure dagster-cloud is always included for deployment
        if not any("dagster-cloud" in dep for dep in dependencies):
            pyproject_content += '    "dagster-cloud",\n'
        
        # Configure build system for flat vs package structure
        if is_flat_structure:
            pyproject_content += f"""]

[project.optional-dependencies]
dev = [
    "dagster-webserver",
    "pytest",
]

[tool.hatch.build.targets.wheel]
packages = ["."]

[tool.dagster]
module_name = "definitions"

[tool.dg]
directory_type = "project"

[tool.dg.project]
root_module = "definitions"
"""
        else:
            pyproject_content += f"""]

[project.optional-dependencies]
dev = [
    "dagster-webserver", 
    "pytest",
]

[tool.dagster]
module_name = "definitions"

[tool.dg]
directory_type = "project"

[tool.dg.project]
root_module = "definitions"
"""
        
        with open(pyproject_path, 'w') as f:
            f.write(pyproject_content)
        print(f"✅ Created pyproject.toml")
        if use_components:
            print(f"   🧩 Configured for Dagster Components")
            print(f"   💡 Use 'dg dev' to run this project")
        else:
            print(f"   📄 Configured for flat project structure")
            print(f"   💡 Use 'dagster dev' to run this project")
            
            # Offer Components upgrade for flat projects (experimental)
            print(f"\n🧪 Experimental: Components Upgrade Available")
            print(f"   Dagster Components provide enhanced project structure with:")
            print(f"   • Better organization with definitions/defs folder")
            print(f"   • Built-in integrations (dbt, Fivetran, Airbyte, etc.)")
            print(f"   • Modern development workflow with 'dg dev'")
            print(f"   • Enhanced scaffolding and code generation")
            print(f"")
            print(f"   ⚠️  Note: Components upgrade is experimental for existing projects")
            print(f"   ⚠️  Complex projects may require manual adjustments")
            print(f"   ✅ Works best with new projects or simple existing projects")
            
            upgrade_choice = choose(
                "Would you like to upgrade this project to use Dagster Components?",
                [
                    "Yes, upgrade to Components (experimental)",
                    "No, keep flat structure (recommended for existing projects)"
                ]
            )
            
            if upgrade_choice == 1:
                upgrade_to_components(project_dir, project_name)
            else:
                print(f"✅ Keeping flat project structure")
                print(f"💡 Use 'dagster dev' to run this project")
                print(f"💡 To upgrade to Components later, run: dg project scaffold-from-example --name {project_name}")
    else:
        print(f"✅ pyproject.toml already exists")
        
        # Check existing project type and provide guidance
        if use_components:
            print(f"   🧩 This is a Dagster Components project")
            print(f"   💡 Use 'dg dev' to run this project locally")
        else:
            print(f"   📄 This is a traditional Dagster project")
            print(f"   💡 Use 'dagster dev' to run this project locally")
            print(f"   🔄 Consider upgrading to Components: dg project scaffold-from-example --name {project_name}")
    
    # Create dagster_cloud.yaml if missing (for deployment readiness)
    dagster_cloud_path = os.path.join(project_dir, "dagster_cloud.yaml")
    if not os.path.exists(dagster_cloud_path):
        print(f"📄 Creating dagster_cloud.yaml...")
        
        # Detect if this is a src-layout project
        has_src_layout = os.path.exists(os.path.join(project_dir, "src"))
        working_directory = "src" if has_src_layout else "."
        
        # Determine the correct module_name based on project structure
        # First try to get it from pyproject.toml
        detected_module_name = None
        pyproject_path = os.path.join(project_dir, "pyproject.toml")
        if os.path.exists(pyproject_path):
            try:
                with open(pyproject_path, 'r') as f:
                    pyproject_content = f.read()
                
                # Try to extract root_module from [tool.dg.project]
                import re
                root_module_match = re.search(r'root_module\s*=\s*["\']([^"\']+)["\']', pyproject_content)
                if root_module_match:
                    detected_module_name = root_module_match.group(1)
                    print(f"💡 Detected root_module from pyproject.toml: {detected_module_name}")
            except Exception as e:
                print(f"⚠️  Could not parse pyproject.toml: {e}")
        
        # If not found in pyproject, try to detect from directory structure
        if not detected_module_name:
            if has_src_layout:
                # Look for modules in src/
                src_dir = os.path.join(project_dir, "src")
                modules = [d for d in os.listdir(src_dir) 
                          if os.path.isdir(os.path.join(src_dir, d)) 
                          and not d.startswith('.') 
                          and not d.startswith('_')]
                
                if len(modules) == 1:
                    detected_module_name = f"{modules[0]}.definitions"
                    print(f"💡 Detected module from src/ directory: {modules[0]}")
                elif len(modules) > 1:
                    print(f"⚠️  Multiple modules found in src/: {modules}")
                    # Try to pick the one with definitions
                    for mod in modules:
                        if os.path.exists(os.path.join(src_dir, mod, "definitions.py")) or \
                           os.path.exists(os.path.join(src_dir, mod, "definitions")):
                            detected_module_name = f"{mod}.definitions"
                            print(f"💡 Selected module with definitions: {mod}")
                            break
        
        # Fallback to just "definitions" if nothing detected
        if not detected_module_name:
            detected_module_name = "definitions"
            print(f"💡 Using default module_name: definitions")
        
        # Create basic dagster_cloud.yaml
        # For Components projects, use package_name instead of module_name
        if use_components:
            dagster_cloud_content = f"""locations:
  - location_name: {project_name}
    code_source:
      package_name: {detected_module_name}
"""
        else:
            dagster_cloud_content = f"""locations:
  - location_name: {project_name}
    code_source:
      package_name: {detected_module_name}
"""
        
        if working_directory != ".":
            dagster_cloud_content += f"      working_directory: {working_directory}\n"
        
        with open(dagster_cloud_path, 'w') as f:
            f.write(dagster_cloud_content)
        print(f"✅ Created dagster_cloud.yaml with package_name: {detected_module_name}")
    else:
        print(f"✅ dagster_cloud.yaml already exists")
    
    # Ensure dagster-cloud is in requirements.txt if it exists
    requirements_path = os.path.join(project_dir, "requirements.txt")
    if os.path.exists(requirements_path):
        print(f"🔧 Checking requirements.txt for dagster-cloud...")
        
        with open(requirements_path, 'r') as f:
            requirements_content = f.read()
        
        # Check for exact match of dagster-cloud (not just substring)
        requirements_lines = [line.strip() for line in requirements_content.strip().split('\n') if line.strip()]
        has_dagster_cloud = any(line == "dagster-cloud" or line.startswith("dagster-cloud==") or line.startswith("dagster-cloud>=") for line in requirements_lines)
        
        if not has_dagster_cloud:
            print(f"📦 Adding dagster-cloud to requirements.txt...")
            
            # Add dagster-cloud after dagster if it exists, otherwise at the top
            lines = requirements_content.strip().split('\n')
            new_lines = []
            dagster_cloud_added = False
            
            for line in lines:
                new_lines.append(line)
                # Add dagster-cloud right after dagster (but not dagster-webserver, etc.)
                if line.strip() == "dagster" and not dagster_cloud_added:
                    new_lines.append("dagster-cloud")
                    dagster_cloud_added = True
            
            # If dagster wasn't found, add dagster-cloud at the beginning
            if not dagster_cloud_added:
                new_lines.insert(0, "dagster-cloud")
            
            # Write back the updated requirements
            with open(requirements_path, 'w') as f:
                f.write('\n'.join(new_lines) + '\n')
            
            print(f"✅ Added dagster-cloud to requirements.txt")
        else:
            print(f"✅ dagster-cloud already present in requirements.txt")
    
    # Also check pyproject.toml if it exists and has dependencies
    pyproject_path = os.path.join(project_dir, "pyproject.toml")
    if os.path.exists(pyproject_path):
        print(f"🔧 Checking pyproject.toml for dagster-cloud...")
        
        with open(pyproject_path, 'r') as f:
            pyproject_content = f.read()
        
        if "dagster-cloud" not in pyproject_content and "dependencies" in pyproject_content:
            print(f"📦 Adding dagster-cloud to pyproject.toml dependencies...")
            
            # Find the dependencies section and add dagster-cloud
            lines = pyproject_content.split('\n')
            new_lines = []
            in_dependencies = False
            dagster_cloud_added = False
            
            for line in lines:
                if line.strip().startswith('dependencies = ['):
                    in_dependencies = True
                    new_lines.append(line)
                elif in_dependencies and line.strip() == ']':
                    # End of dependencies section
                    if not dagster_cloud_added:
                        # Add dagster-cloud before closing bracket
                        new_lines.append('    "dagster-cloud",')
                        dagster_cloud_added = True
                    new_lines.append(line)
                    in_dependencies = False
                elif in_dependencies and '"dagster",' in line and not dagster_cloud_added:
                    # Add dagster-cloud right after dagster
                    new_lines.append(line)
                    new_lines.append('    "dagster-cloud",')
                    dagster_cloud_added = True
                else:
                    new_lines.append(line)
            
            # Write back the updated pyproject.toml
            with open(pyproject_path, 'w') as f:
                f.write('\n'.join(new_lines))
            
            print(f"✅ Added dagster-cloud to pyproject.toml")
        else:
            print(f"✅ dagster-cloud already present in pyproject.toml or no dependencies section found")
    
    print(f"🎯 Project is now ready for local development and deployment!")

def upgrade_to_components(project_dir, project_name):
    """Upgrade a flat project to use Dagster Components structure following official Dagster guidance."""
    print(f"\n🔄 Upgrading to Dagster Components...")
    print(f"📖 Following official guide: https://docs.dagster.io/guides/build/projects/moving-to-components/migrating-project")
    
    original_dir = os.getcwd()
    os.chdir(project_dir)
    
    try:
        # Step 1: Install dagster-dg-cli (following official guide)
        print(f"\n📦 Step 1: Installing dagster-dg-cli...")
        try:
            subprocess.run(["dg", "--version"], check=True, capture_output=True)
            print(f"   ✅ dagster-dg-cli already available")
        except (subprocess.CalledProcessError, FileNotFoundError):
            print(f"   📥 Installing dagster-dg-cli...")
            subprocess.run(["pip", "install", "dagster-dg-cli"], check=True)
            print(f"   ✅ Installed dagster-dg-cli")
        
        # Step 2: Update pyproject.toml with dg configuration (following official guide)
        print(f"\n🔧 Step 2: Adding dg configuration to pyproject.toml...")
        pyproject_path = "pyproject.toml"
        if os.path.exists(pyproject_path):
            with open(pyproject_path, "r") as f:
                content = f.read()
            
            # Add the required dg configuration sections
            if "[tool.dg]" not in content:
                # For Components projects upgrading from flat structure:
                # - root_module points to the definitions package (for Components)
                # - code_location_target_module points to the main definitions file
                content += f"""
[tool.dg]
directory_type = "project"

[tool.dg.project]
root_module = "definitions"
code_location_target_module = "definitions"
"""
                with open(pyproject_path, "w") as f:
                    f.write(content)
                print(f"   ✅ Added [tool.dg] and [tool.dg.project] sections")
            else:
                print(f"   ✅ dg configuration already present")
        
        # Step 3: Create definitions package structure (following official guide)
        print(f"\n🏗️  Step 3: Creating definitions package structure...")
        
        # Create main definitions directory and make it a Python package
        definitions_dir = "definitions"
        os.makedirs(definitions_dir, exist_ok=True)
        
        # Create definitions/__init__.py to make it a proper Python package
        definitions_init_path = os.path.join(definitions_dir, "__init__.py")
        if not os.path.exists(definitions_init_path):
            with open(definitions_init_path, "w") as f:
                f.write("# Dagster Components definitions package\n")
            print(f"   ✅ Created definitions/__init__.py")
        
        # Create components submodule for custom component types
        components_dir = os.path.join("definitions", "components")
        os.makedirs(components_dir, exist_ok=True)
        
        components_init_path = os.path.join(components_dir, "__init__.py")
        if not os.path.exists(components_init_path):
            with open(components_init_path, "w") as f:
                f.write("# Custom component types for this project\n")
            print(f"   ✅ Created definitions/components/__init__.py")
        
        # Step 4: Add entry point to pyproject.toml (following official guide)
        print(f"\n⚙️  Step 4: Adding entry point for custom components...")
        if os.path.exists(pyproject_path):
            with open(pyproject_path, "r") as f:
                content = f.read()
            
            if "[project.entry-points" not in content:
                content += f"""
[project.entry-points."dagster_dg_cli.registry_modules"]
{project_name} = "definitions.components"
"""
                with open(pyproject_path, "w") as f:
                    f.write(content)
                print(f"   ✅ Added entry point for {project_name}.components")
                
                # Reinstall package to pick up entry point
                print(f"   🔄 Reinstalling package to register entry point...")
                try:
                    subprocess.run(["pip", "install", "--editable", "."], check=True)
                    print(f"   ✅ Package reinstalled with entry point")
                except subprocess.CalledProcessError as e:
                    print(f"   ⚠️  Package reinstall failed: {e}")
                    print(f"   💡 You may need to run 'pip install --editable .' manually")
        
        # Step 5: Create defs submodule for autoloading (following official guide)
        print(f"\n📁 Step 5: Creating defs submodule for autoloading...")
        defs_dir = os.path.join("definitions", "defs")
        os.makedirs(defs_dir, exist_ok=True)
        
        # Create an empty __init__.py in defs (autoloading will pick up other files)
        defs_init_path = os.path.join(defs_dir, "__init__.py")
        if not os.path.exists(defs_init_path):
            with open(defs_init_path, "w") as f:
                f.write("# Definitions in this folder will be autoloaded\n")
            print(f"   ✅ Created definitions/defs/__init__.py")
        
        # Step 6: Move definitions into the definitions package (following official guide)
        print(f"\n🔄 Step 6: Moving definitions into Components structure...")
        root_definitions_path = "definitions.py"
        package_definitions_path = os.path.join("definitions", "__init__.py")
        
        if os.path.exists(root_definitions_path):
            # Read existing definitions.py
            with open(root_definitions_path, "r") as f:
                existing_content = f.read()
            
            # Backup original
            backup_path = "definitions.py.backup"
            with open(backup_path, "w") as f:
                f.write(existing_content)
            print(f"   📄 Backed up original to definitions.py.backup")
            
            # Create definitions/__init__.py with merged content
            new_content = f"""# Dagster Components definitions - merged from original definitions.py
from pathlib import Path
import dagster as dg

# Original definitions from definitions.py
{existing_content.replace('defs = ', 'existing_defs = ')}

# Merge existing definitions with autoloaded ones from defs folder
defs = dg.Definitions.merge(
    existing_defs,
    dg.load_from_defs_folder(project_root=Path(__file__).parent.parent),
)
"""
            
            # Write to definitions/__init__.py (overwrite the simple comment we created earlier)
            with open(package_definitions_path, "w") as f:
                f.write(new_content)
            print(f"   ✅ Moved definitions to definitions/__init__.py")
            
            # Remove the original definitions.py since it's now in the package
            os.remove(root_definitions_path)
            print(f"   🗑️  Removed original definitions.py (now in definitions/__init__.py)")
            
            # Update workspace.yaml if it exists and references definitions.py
            workspace_yaml_path = "workspace.yaml"
            if os.path.exists(workspace_yaml_path):
                with open(workspace_yaml_path, "r") as f:
                    workspace_content = f.read()
                
                if "definitions.py" in workspace_content:
                    # Update to use python_package instead of python_file
                    updated_content = workspace_content.replace(
                        "python_file:\n      relative_path: definitions.py",
                        "python_package:\n      package_name: definitions"
                    )
                    
                    with open(workspace_yaml_path, "w") as f:
                        f.write(updated_content)
                    print(f"   ✅ Updated workspace.yaml to use definitions package")
        else:
            print(f"   ⚠️  No definitions.py found to migrate")
        
        # Step 7: Test the configuration
        print(f"\n🧪 Step 7: Testing Components configuration...")
        try:
            result = subprocess.run(["dg", "list", "defs"], capture_output=True, text=True, check=True)
            print(f"   ✅ Components configuration working!")
            print(f"   📋 Found definitions:")
            # Show a summary of the output
            lines = result.stdout.split('\n')
            for line in lines:
                if '│' in line and ('asset' in line.lower() or 'job' in line.lower()):
                    print(f"      {line.strip()}")
        except subprocess.CalledProcessError as e:
            print(f"   ⚠️  Configuration test failed: {e}")
            print(f"   💡 You may need to run 'dg list defs' manually to verify")
        
        print(f"\n✅ Successfully upgraded to Dagster Components!")
        print(f"🎯 New project structure (following official guide):")
        print(f"   📁 Project Root/")
        print(f"   ├── 📄 definitions.py (merges existing + autoloaded)")
        print(f"   ├── 📁 definitions/")
        print(f"   │   ├── 📁 components/ (for custom component types)")
        print(f"   │   └── 📁 defs/ (autoloaded definitions)")
        print(f"   └── 📄 pyproject.toml (with [tool.dg] configuration)")
        print(f"")
        print(f"💡 Next steps:")
        print(f"   • Run 'dg dev' to start the development server")
        print(f"   • Run 'dg list components' to see available components")
        print(f"   • Run 'dg scaffold component MyComponent' to create custom components")
        print(f"   • Add new assets to definitions/defs/ for automatic loading")
        print(f"")
        print(f"📖 Learn more: https://docs.dagster.io/guides/build/projects/moving-to-components")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Components upgrade failed: {e}")
        print(f"💡 You can upgrade manually following the official guide:")
        print(f"   https://docs.dagster.io/guides/build/projects/moving-to-components/migrating-project")
    except Exception as e:
        print(f"❌ Unexpected error during upgrade: {e}")
        print(f"💡 Keeping flat project structure")
        print(f"💡 Manual upgrade guide: https://docs.dagster.io/guides/build/projects/moving-to-components/migrating-project")
    finally:
        os.chdir(original_dir)

def create_new_dagster_project(pkg_mgr):
    """Create a new empty Dagster project using create-dagster CLI."""
    print("\n🆕 Creating new Dagster project...")
    print("💡 This will scaffold a clean, Components-compatible project structure")
    
    # Get project name
    project_name = input("Enter project name (or press Enter for 'my-dagster-project'): ").strip()
    if not project_name:
        project_name = "my-dagster-project"
    
    # Validate project name
    import re
    if not re.match(r'^[a-zA-Z][a-zA-Z0-9_-]*$', project_name):
        print("⚠️  Invalid project name. Using 'my-dagster-project' instead.")
        project_name = "my-dagster-project"
    
    # Check if directory already exists
    if os.path.exists(project_name):
        overwrite = choose(
            f"Directory '{project_name}' already exists. What would you like to do?",
            ["Use a different name", "Remove and recreate", "Cancel"]
        )
        
        if overwrite == 1:
            project_name = input("Enter a different project name: ").strip()
            if not project_name or os.path.exists(project_name):
                print("❌ Invalid or existing project name")
                return None
        elif overwrite == 2:
            shutil.rmtree(project_name)
            print(f"🗑️  Removed existing directory: {project_name}")
        else:
            return None
    
    # Scaffold the project using create-dagster
    print(f"\n📦 Scaffolding new Dagster project: {project_name}")
    
    if pkg_mgr == 2:  # uv
        print("🔧 Using uv to create project...")
        try:
            # Use uvx to run create-dagster
            result = subprocess.run([
                "uvx", "create-dagster@latest", "project", project_name
            ], capture_output=True, text=True)
            
            if result.returncode != 0:
                print(f"❌ Failed to create project with uv")
                print(f"Error: {result.stderr}")
                return None
            
            print(f"✅ Project scaffolded successfully with uv")
            
            # Navigate to project directory
            project_dir = os.path.abspath(project_name)
            os.chdir(project_dir)
            
            # Run uv sync to install dependencies
            print("📦 Installing dependencies with uv sync...")
            sync_result = subprocess.run(["uv", "sync"], capture_output=True, text=True)
            
            if sync_result.returncode == 0:
                print("✅ Dependencies installed successfully")
            else:
                print(f"⚠️  uv sync had issues: {sync_result.stderr}")
            
            return project_dir
            
        except FileNotFoundError:
            print("❌ uv not found. Please install uv first:")
            print("   curl -LsSf https://astral.sh/uv/install.sh | sh")
            return None
    
    else:  # pip
        print("🔧 Using pip to create project...")
        try:
            # Check if create-dagster is available
            create_dagster_check = subprocess.run(
                ["create-dagster", "--version"], 
                capture_output=True, 
                text=True
            )
            
            if create_dagster_check.returncode != 0:
                print("⚠️  create-dagster CLI not found. Installing it now...")
                subprocess.run(["pip", "install", "create-dagster"], check=True)
            
            # Run create-dagster
            result = subprocess.run([
                "create-dagster", "project", project_name
            ], capture_output=True, text=True)
            
            if result.returncode != 0:
                print(f"❌ Failed to create project with create-dagster")
                print(f"Error: {result.stderr}")
                return None
            
            print(f"✅ Project scaffolded successfully")
            
            # Navigate to project directory
            project_dir = os.path.abspath(project_name)
            os.chdir(project_dir)
            
            # Create virtual environment
            print("🔧 Creating virtual environment...")
            subprocess.run(["python3", "-m", "venv", ".venv"], check=True)
            
            # Determine activation script
            if platform.system() == "Windows":
                pip_path = os.path.join(".venv", "Scripts", "pip")
                python_path = os.path.join(".venv", "Scripts", "python")
            else:
                pip_path = os.path.join(".venv", "bin", "pip")
                python_path = os.path.join(".venv", "bin", "python")
            
            # Install project as editable package
            print("📦 Installing project dependencies...")
            subprocess.run([python_path, "-m", "pip", "install", "--editable", "."], check=True)
            
            print(f"✅ Dependencies installed successfully")
            print(f"")
            print(f"💡 To activate the virtual environment later:")
            if platform.system() == "Windows":
                print(f"   .venv\\Scripts\\activate")
            else:
                print(f"   source .venv/bin/activate")
            
            return project_dir
            
        except FileNotFoundError:
            print("❌ create-dagster not found and could not be installed")
            return None
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to create project: {e}")
            return None

def choose_project_source():
    """Let user choose the source for their Dagster project."""
    print("\n🎯 Choose your project source:")
    
    source_choice = choose(
        "Where would you like to get your Dagster project from?",
        [
            "Create new empty Dagster project (recommended)",
            "Dagster quickstart templates",
            "Eric Thomas's example projects", 
            "Custom GitHub repository or user/organization",
            "Use current directory"
        ]
    )
    
    if source_choice == 1:
        # New empty Dagster project
        return "new_project", []
    elif source_choice == 2:
        # Original quickstart logic
        return "quickstart", []
    elif source_choice == 3:
        # Eric's example repositories
        return "eric_examples", EXAMPLE_REPOSITORIES[DEFAULT_EXAMPLE_SOURCE]
    elif source_choice == 4:
        # Custom GitHub input
        github_input = input("Enter GitHub user/organization or repository URL: ").strip()
        if not github_input:
            print("❌ No input provided. Using current directory.")
            return "current_dir", []
        
        repos = fetch_github_repos(github_input)
        if not repos:
            print("❌ No repositories found. Using current directory.")
            return "current_dir", []
        
        return "custom_github", repos
    else:
        # Use current directory
        return "current_dir", []

def select_repository(repos):
    """Display and allow selection of repositories."""
    if not repos:
        return None
    
    print(f"\n📋 Available repositories:")
    for i, repo in enumerate(repos, 1):
        print(f"   {i}. {repo['name']}")
        if 'description' in repo:
            print(f"      {repo['description']}")
    
    while True:
        try:
            choice = int(input(f"\nEnter your choice (1-{len(repos)}): "))
            if 1 <= choice <= len(repos):
                return repos[choice - 1]
            else:
                print(f"❌ Please enter a number between 1 and {len(repos)}")
        except ValueError:
            print("❌ Please enter a valid number")
    
    return None

def clone_selected_repository(repo_info, target_dir=None):
    """Clone a selected repository to the target directory."""
    if not repo_info:
        return None
    
    if not target_dir:
        target_dir = repo_info["name"]
    
    if os.path.exists(target_dir):
        overwrite = choose(
            f"Directory '{target_dir}' already exists. What would you like to do?",
            ["Overwrite it", "Use existing directory", "Cancel"]
        )
        
        if overwrite == 1:
            shutil.rmtree(target_dir)
        elif overwrite == 2:
            return os.path.abspath(target_dir)
        else:
            return None
    
    try:
        print(f"📥 Cloning {repo_info['name']}...")
        subprocess.run(["git", "clone", repo_info["url"], target_dir], check=True)
        print(f"✅ Successfully cloned {repo_info['name']}")
        return os.path.abspath(target_dir)
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to clone repository: {e}")
        return None
    except Exception as e:
        print(f"❌ Error cloning repository: {e}")
        return None

def fetch_github_repos(github_input):
    """Fetch repositories from GitHub user/organization or parse single repo URL."""
    repos = []
    
    # Check if it's a full repository URL
    if github_input.startswith("https://github.com/") and github_input.count("/") >= 4:
        # Extract repo info from URL
        parts = github_input.replace("https://github.com/", "").split("/")
        if len(parts) >= 2:
            owner, repo_name = parts[0], parts[1]
            repos.append({
                "name": repo_name,
                "url": github_input if github_input.endswith(".git") else f"{github_input}.git",
                "description": f"Repository: {owner}/{repo_name}"
            })
    else:
        # Try to fetch repositories from user/organization
        # For now, return empty list - this would need GitHub API integration
        print("⚠️  GitHub API integration not implemented. Please provide a direct repository URL.")
    
    return repos

# -------------------------------
# Utility Functions
# -------------------------------

def choose(prompt, options):
    """Display a choice prompt and return the selected option index (1-based)."""
    print(f"\n{prompt}")
    for i, option in enumerate(options, 1):
        print(f"{i}. {option}")
    
    while True:
        try:
            choice = int(input("Enter your choice: ").strip())
            if 1 <= choice <= len(options):
                return choice
            else:
                print(f"Please enter a number between 1 and {len(options)}")
        except ValueError:
            print("Please enter a valid number")

def ensure_profiles_has_dev(profiles_path):
    """Ensure profiles.yml has a dev target."""
    try:
        import yaml
        with open(profiles_path, "r") as f:
            profiles = yaml.safe_load(f)
        
        if "jaffle_shop" in profiles and "dev" not in profiles["jaffle_shop"]["outputs"]:
            # Add dev target
            profiles["jaffle_shop"]["outputs"]["dev"] = {
                "type": "duckdb",
                "path": "jaffle_shop.duckdb"
            }
            
            with open(profiles_path, "w") as f:
                yaml.safe_dump(profiles, f, default_flow_style=False)
            print("✅ Added dev target to profiles.yml")
    except Exception as e:
        print(f"⚠️  Could not update profiles.yml: {e}")

def detect_git_host(project_directory: str) -> str:
    """Detect the Git hosting platform from the project directory."""
    try:
        result = subprocess.run(
            ["git", "remote", "get-url", "origin"],
            cwd=project_directory,
            capture_output=True,
            text=True,
            check=True
        )
        remote_url = result.stdout.strip()
        
        if "github.com" in remote_url:
            return "github"
        elif "gitlab.com" in remote_url or "gitlab." in remote_url:
            return "gitlab"
        elif "dev.azure.com" in remote_url or "visualstudio.com" in remote_url:
            return "azure"
        else:
            return "unknown"
    except subprocess.CalledProcessError:
        return "unknown"

def fetch_text(url: str, timeout: int = 15, attempts: int = 3) -> str:
    """Fetch text content from a URL with retries."""
    import urllib.request
    
    for attempt in range(attempts):
        try:
            with urllib.request.urlopen(url, timeout=timeout) as response:
                return response.read().decode('utf-8')
        except Exception as e:
            if attempt == attempts - 1:
                raise e
            print(f"Attempt {attempt + 1} failed, retrying...")
    
    return ""

def has_cmd(cmd: str) -> bool:
    """Check if a command is available in PATH."""
    return shutil.which(cmd) is not None

def uncomment_registry_section(workflow_content: str, section_name: str) -> str:
    """Uncomment a specific section in workflow content."""
    lines = workflow_content.split('\n')
    in_section = False
    uncommented = []
    
    for line in lines:
        if f"# {section_name}:" in line:
            in_section = True
            uncommented.append(line[2:])  # Remove the comment
        elif in_section and line.strip().startswith("#") and ":" in line:
            # End of section
            in_section = False
            uncommented.append(line)
        elif in_section and line.strip().startswith("#"):
            # Commented line in section - uncomment it
            uncommented.append(line[1:])
        else:
            uncommented.append(line)
    
    return '\n'.join(uncommented)

def detect_root_module_name(project_root: str) -> str:
    """Detect the root module name from pyproject.toml or directory name."""
    # Check for pyproject.toml first
    pyproject_path = os.path.join(project_root, "pyproject.toml")
    if os.path.exists(pyproject_path):
        try:
            with open(pyproject_path, "r") as f:
                content = f.read()
                # Look for [tool.dg.project] section with root_module
                import re
                match = re.search(r'\[tool\.dg\.project\]\s*\n\s*root_module\s*=\s*"([^"]+)"', content)
                if match:
                    return match.group(1)
        except Exception:
            pass
    
    # Fallback: use directory name
    return os.path.basename(project_root)

def ensure_project_table(project_root: str) -> bool:
    """Ensure pyproject.toml has [project] table for tool compatibility."""
    # Convert to absolute path to avoid issues with working directory changes
    if not os.path.isabs(project_root):
        project_root = os.path.abspath(project_root)
    
    pyproject_path = os.path.join(project_root, "pyproject.toml")
    
    if not os.path.exists(pyproject_path):
        print(f"⚠️  {pyproject_path} not found")
        return False
    
    try:
        with open(pyproject_path, "r") as f:
            content = f.read()
        
        # Check if [project] table already exists
        if "[project]" in content:
            print("✅ pyproject.toml already has [project] table")
            return True
        
        # Parse the existing content to preserve structure
        lines = content.split('\n')
        
        # Find where to insert [project] table - after [build-system] and before [tool.dg]
        insert_index = 0
        for i, line in enumerate(lines):
            if line.strip() == "[tool.dg]":
                insert_index = i
                break
            elif line.strip() == "[tool.dg.project]":
                insert_index = i
                break
        
        # If no [tool.dg] section found, insert after [build-system]
        if insert_index == 0:
            for i, line in enumerate(lines):
                if line.strip() == "[build-system]":
                    insert_index = i + 1
                    break
        
        # Get project name from directory or use default
        project_name = os.path.basename(project_root)
        if project_name.startswith("dagster-"):
            project_name = project_name.replace("dagster-", "")
        
        # Insert [project] table
        project_lines = [
            "",
            "[project]",
            f'name = "{project_name}"',
            "version = \"0.1.0\"",
            f'description = "Dagster {project_name} project"',
            "requires-python = \">=3.8\"",
            ""
        ]
        
        # Insert the project lines
        lines[insert_index:insert_index] = project_lines
        
        # Write back to file
        with open(pyproject_path, "w") as f:
            f.write('\n'.join(lines))
        
        print("✅ Added [project] table to pyproject.toml for tool compatibility")
        return True
        
    except Exception as e:
        print(f"⚠️  Could not update pyproject.toml: {e}")
        return False


def handle_deployment_error(error_output: str, deployment_name: str, org_name: str) -> None:
    """Handle deployment errors and provide guidance."""
    print(f"\n❌ Deployment failed for {deployment_name}")
    
    if "already exists" in error_output.lower():
        print("⚠️  Deployment already exists. You can:")
        print(f"   1. Use a different name for {deployment_name}")
        print(f"   2. Delete existing deployment: dagster-cloud deployment delete {deployment_name}")
        print(f"   3. Check status: dagster-cloud deployment status {deployment_name}")
    elif "not found" in error_output.lower():
        print("⚠️  Organization not found. Check:")
        print(f"   1. Organization name: {org_name}")
        print(f"   2. API token permissions")
        print(f"   3. Organization exists in Dagster+ Cloud")
    else:
        print("💡 Check the error details above and try again")
        print("   Common issues:")
        print("   - Invalid API token")
        print("   - Network connectivity")
        print("   - Organization permissions")

def install_python_packages(packages):
    """Install Python packages using pip."""
    try:
        # Use python3 -m pip to ensure we're using the right pip
        cmd = ["python3", "-m", "pip", "install"] + packages
        subprocess.run(cmd, check=True)
        print(f"✅ Installed packages: {', '.join(packages)}")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install packages: {e}")
        print("💡 You may need to install pip or check your Python environment")
        raise

def preflight_checks():
    """Run preflight checks for required tools."""
    print("\n🧰 Preflight: tooling availability")
    tools = {
        "git": has_cmd("git"),
        "docker": has_cmd("docker"),
        "kubectl": has_cmd("kubectl"),
        "helm": has_cmd("helm"),
        "aws": has_cmd("aws"),
        "dagster": has_cmd("dagster"),
        "dagster-cloud": has_cmd("dagster-cloud"),
        # pex is checked only when needed for serverless PEX deployment
    }
    for name, ok in tools.items():
        print(f"  {'✅' if ok else '⚠️ '} {name}")
    if not tools["git"]:
        print("⚠️  git not found. Repo cloning will fail; install git from https://git-scm.com/downloads")
    if not tools["docker"]:
        print("⚠️  docker not found. Hybrid container deploys and image builds will require Docker.")
    if not tools["kubectl"] or not tools["helm"]:
        print("⚠️  kubectl/helm missing. Kubernetes agent install scripts will require them to run.")
    if not tools["aws"]:
        print("⚠️  aws CLI not found. ECS CloudFormation deploy requires AWS CLI.")
    if not tools["dagster"]:
        print("⚠️  dagster CLI not found. Scaffolding and some commands use it; we attempt to install dagster below.")
    if not tools["dagster-cloud"]:
        print("⚠️  dagster-cloud CLI not found. Direct deploy and validation will require it; try 'pip install dagster-cloud'.")
    # PEX check is done later only if serverless PEX deployment is chosen

def is_components_compatible(project_dir=None):
    """Check if project has Components configuration."""
    try:
        if project_dir:
            # Check in the specified project directory
            pyproject_path = os.path.join(project_dir, "pyproject.toml")
            dg_toml_path = os.path.join(project_dir, "dg.toml")
        else:
            # Check in current working directory
            pyproject_path = "pyproject.toml"
            dg_toml_path = "dg.toml"
        
        # Check for pyproject.toml with [tool.dg] section
        if os.path.exists(pyproject_path):
            with open(pyproject_path, "r") as f:
                content = f.read()
                if "[tool.dg]" in content:
                    return True
        
        # Check for dg.toml file
        if os.path.exists(dg_toml_path):
            return True
            
        return False
    except Exception:
        return False

# -------------------------------
# Constants
# -------------------------------

SERVERLESS_WORKFLOW_URL = "https://raw.githubusercontent.com/dagster-io/dagster-cloud-serverless-quickstart/main/.github/workflows/dagster-plus-deploy.yml"
HYBRID_WORKFLOW_URL = "https://raw.githubusercontent.com/dagster-io/dagster-cloud-hybrid-quickstart/main/.github/workflows/dagster-cloud-deploy.yml"

SERVERLESS_QUICKSTART_REPO = "https://github.com/dagster-io/dagster-cloud-serverless-quickstart.git"
HYBRID_QUICKSTART_REPO = "https://github.com/dagster-io/dagster-cloud-hybrid-quickstart.git"

# Baseline dagster_cloud.yaml templates
SERVERLESS_DAGSTER_CLOUD_YAML_URL = "https://raw.githubusercontent.com/dagster-io/dagster-cloud-serverless-quickstart/main/dagster_cloud.yaml"
SERVERLESS_PEX_DAGSTER_CLOUD_YAML_URL = "https://raw.githubusercontent.com/dagster-io/dagster-cloud-serverless-quickstart-fast-deploys-enabled/main/dagster_cloud.yaml"
HYBRID_DAGSTER_CLOUD_YAML_URL = "https://raw.githubusercontent.com/dagster-io/dagster-cloud-hybrid-quickstart/main/dagster_cloud.yaml"

# GitLab CI templates
GITLAB_HYBRID_CI_URL = "https://raw.githubusercontent.com/dagster-io/dagster-cloud-action/main/gitlab/hybrid-ci.yml"
GITLAB_SERVERLESS_CI_URL = "https://raw.githubusercontent.com/dagster-io/dagster-cloud-action/main/gitlab/serverless-ci.yml"

JAFFLE_SHOP_REPO = "https://github.com/dbt-labs/jaffle_shop.git"

ECS_STACK_EXISTING = "https://console.aws.amazon.com/cloudformation/home#/stacks/create/review?templateURL=https://s3.amazonaws.com/dagster.cloud/cloudformation/ecs-agent.yaml"
ECS_STACK_NEW_VPC = "https://console.aws.amazon.com/cloudformation/home#/stacks/create/review?templateURL=https://s3.amazonaws.com/dagster.cloud/cloudformation/ecs-agent-vpc.yaml"

ECS_DOC_NEW_VPC = "https://docs.dagster.io/deployment/dagster-plus/hybrid/amazon-ecs/new-vpc"
ECS_DOC_EXISTING_VPC = "https://docs.dagster.io/deployment/dagster-plus/hybrid/amazon-ecs/existing-vpc"

K8S_DOC = "https://docs.dagster.io/deployment/dagster-plus/hybrid/kubernetes/setup"

# -------------------------------
# Main Onboarding Functions
# -------------------------------

def install_dagster(pkg_mgr):
    """Install Dagster and related packages."""
    print(f"\n⚙️  Installing Dagster...")
    
    if pkg_mgr == 2:  # uv
        subprocess.run(["uv", "pip", "install", "dagster", "dagster-cloud", "PyYAML"])
    else:  # pip
        subprocess.run(["python3", "-m", "pip", "install", "dagster", "dagster-cloud", "PyYAML"])

def install_pex(pkg_mgr):
    """Install PEX for serverless PEX deployments."""
    print(f"\n⚙️  Installing PEX for serverless deployment...")
    
    if pkg_mgr == 2:  # uv
        print("⚙️  Installing pex as a uv tool...")
        subprocess.run(["uv", "tool", "install", "pex"])
        print("⚙️  Installing pex in system Python for dagster-cloud compatibility...")
        try:
            subprocess.run(["python3", "-m", "pip", "install", "pex"], check=True)
        except subprocess.CalledProcessError:
            print("⚠️  Warning: Could not install pex in system Python. PEX deploys may fail.")
    else:  # pip
        subprocess.run(["python3", "-m", "pip", "install", "pex"])

def start_docker_daemon():
    """Start Docker daemon if it's not running."""
    try:
        # Check if Docker daemon is running
        result = subprocess.run(["docker", "info"], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Docker daemon is running")
            return True
        else:
            print("🐳 Starting Docker daemon...")
            if platform.system() == "Darwin":  # macOS
                subprocess.run(["open", "-a", "Docker"], check=False)
                print("💡 Docker Desktop is starting... Please wait a moment")
                time.sleep(10)  # Give Docker time to start
                
                # Check again
                result = subprocess.run(["docker", "info"], capture_output=True, text=True)
                if result.returncode == 0:
                    print("✅ Docker daemon started successfully")
                    return True
                else:
                    print("⚠️  Docker daemon may still be starting. Please ensure Docker Desktop is running.")
                    return False
            else:
                print("💡 Please start Docker daemon manually")
                return False
    except FileNotFoundError:
        print("❌ Docker not found. Please install Docker first.")
        return False

def generate_dockerfile(project_dir, package_name, python_version="3.11"):
    """Generate a Dockerfile for Dagster+ serverless deployment."""
    print(f"\n🐳 Generating Dockerfile for Docker deployment...")
    
    # Detect requirements file
    requirements_file = None
    for req_file in ["requirements.txt", "pyproject.toml", "setup.py"]:
        if os.path.exists(os.path.join(project_dir, req_file)):
            requirements_file = req_file
            break
    
    if not requirements_file:
        print(f"⚠️  No requirements file found. Creating basic requirements.txt...")
        requirements_content = "dagster\ndagster-cloud\n"
        with open(os.path.join(project_dir, "requirements.txt"), "w") as f:
            f.write(requirements_content)
        requirements_file = "requirements.txt"
    
    # Generate Dockerfile content
    dockerfile_content = f"""# Dockerfile for Dagster+ Serverless Deployment
# Auto-generated by onboard.py

FROM python:{python_version}-slim

# Set working directory
WORKDIR /opt/dagster/app

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    gcc \\
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY {requirements_file} .
"""

    if requirements_file == "requirements.txt":
        dockerfile_content += "RUN pip install --no-cache-dir -r requirements.txt\n"
    elif requirements_file == "pyproject.toml":
        dockerfile_content += "RUN pip install --no-cache-dir -e .\n"  # Install in development mode for src-layout
    elif requirements_file == "setup.py":
        dockerfile_content += "RUN pip install --no-cache-dir -e .\n"  # Install in development mode for src-layout
    
    dockerfile_content += f"""
# Copy the entire project
COPY . .

# Set environment variables for Dagster
ENV DAGSTER_HOME=/opt/dagster/dagster_home
ENV PYTHONPATH=/opt/dagster/app/src:/opt/dagster/app:$PYTHONPATH

# Create dagster home directory
RUN mkdir -p $DAGSTER_HOME

# Expose the port that Dagster uses
EXPOSE 3000

# Set the default command
CMD ["dagster", "api", "grpc", "-p", "3000", "-m", "{package_name}"]
"""

    dockerfile_path = os.path.join(project_dir, "Dockerfile")
    with open(dockerfile_path, "w") as f:
        f.write(dockerfile_content)
    
    print(f"✅ Generated Dockerfile at {dockerfile_path}")
    
    # Also generate .dockerignore
    dockerignore_content = """# Docker ignore file for Dagster+ deployment
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
env/
venv/
.venv/
pip-log.txt
pip-delete-this-directory.txt
.tox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.log
.git/
.mypy_cache/
.pytest_cache/
.hypothesis/
.DS_Store
*.swp
*.swo
*~
"""
    
    dockerignore_path = os.path.join(project_dir, ".dockerignore")
    with open(dockerignore_path, "w") as f:
        f.write(dockerignore_content)
    
    print(f"✅ Generated .dockerignore at {dockerignore_path}")
    
    return dockerfile_path

def setup_ecs_agent(org_name, deployment_name, api_token, cf_template_url, setup_type, doc_url, enable_branch_deployments, ecs_choice):
    """Generate ECS agent setup scripts and files."""
    ecs_dir = "dagster-plus-ecs"
    
    # Generate CloudFormation parameters file
    if ecs_choice == 3:  # Existing VPC
        cf_params_content = f"""[
  {{"ParameterKey": "DagsterOrganization", "ParameterValue": "{org_name}"}},
  {{"ParameterKey": "DagsterDeployment", "ParameterValue": "{deployment_name}"}},
  {{"ParameterKey": "EnableBranchDeployments", "ParameterValue": "{str(enable_branch_deployments).lower()}"}},
  {{"ParameterKey": "AgentToken", "ParameterValue": "{api_token}"}},
  {{"ParameterKey": "DeployVPC", "ParameterValue": "REPLACE_WITH_YOUR_VPC_ID"}},
  {{"ParameterKey": "DeployVPCSubnet", "ParameterValue": "REPLACE_WITH_YOUR_SUBNET_ID"}},
  {{"ParameterKey": "ExistingECSCluster", "ParameterValue": ""}},
  {{"ParameterKey": "TaskLaunchType", "ParameterValue": "FARGATE"}}
]"""
    else:  # New VPC
        cf_params_content = f"""[
  {{"ParameterKey": "DagsterOrganization", "ParameterValue": "{org_name}"}},
  {{"ParameterKey": "DagsterDeployment", "ParameterValue": "{deployment_name}"}},
  {{"ParameterKey": "EnableBranchDeployments", "ParameterValue": "{str(enable_branch_deployments).lower()}"}},
  {{"ParameterKey": "AgentToken", "ParameterValue": "{api_token}"}}
]"""
    
    cf_params_path = os.path.join(ecs_dir, "cloudformation-parameters.json")
    with open(cf_params_path, "w") as f:
        f.write(cf_params_content)
    
    # Generate AWS CLI deployment script
    stack_name = f"dagster-plus-agent-{deployment_name}"
    deploy_script_content = f"""#!/bin/bash
# AWS ECS Dagster+ Agent Deployment Script
# Generated by onboard.py for {org_name}/{deployment_name}

set -e

echo "☁️  Deploying Dagster+ ECS Agent..."
echo "📍 Organization: {org_name}"
echo "🚀 Deployment: {deployment_name}"
echo "🔧 Setup Type: {setup_type}"
echo ""

# Check if AWS CLI is installed
if ! command -v aws &> /dev/null; then
    echo "❌ AWS CLI not found. Please install AWS CLI first:"
    echo "   https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html"
    exit 1
fi

# Check AWS credentials
echo "🔐 Checking AWS credentials..."
if ! aws sts get-caller-identity &> /dev/null; then
    echo "❌ AWS credentials not configured. Run 'aws configure' first."
    exit 1
fi

echo "✅ AWS credentials configured"
CALLER_IDENTITY=$(aws sts get-caller-identity)
ACCOUNT_ID=$(echo $CALLER_IDENTITY | grep -o '"Account": "[^"]*"' | cut -d'"' -f4)
USER_ARN=$(echo $CALLER_IDENTITY | grep -o '"Arn": "[^"]*"' | cut -d'"' -f4)
echo "📋 Account: $ACCOUNT_ID"
echo "👤 User: $USER_ARN"
echo ""

# Get current region
AWS_REGION=$(aws configure get region)
if [ -z "$AWS_REGION" ]; then
    echo "⚠️  No default region set. Using us-east-1"
    AWS_REGION="us-east-1"
fi

echo "🌎 Using AWS region: $AWS_REGION"
echo ""

echo "🚀 Deploying CloudFormation stack..."
echo "📋 Stack name: {stack_name}"
echo "🔗 Template: {cf_template_url}"
echo ""

# Deploy the CloudFormation stack
aws cloudformation deploy \\
    --template-url "{cf_template_url}" \\
    --stack-name "{stack_name}" \\
    --parameter-overrides file://cloudformation-parameters.json \\
    --capabilities CAPABILITY_IAM \\
    --region "$AWS_REGION"

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ CloudFormation stack deployed successfully!"
    echo ""
    echo "📊 Stack details:"
    aws cloudformation describe-stacks \\
        --stack-name "{stack_name}" \\
        --region "$AWS_REGION" \\
        --query 'Stacks[0].[StackName,StackStatus,CreationTime]' \\
        --output table
    
    echo ""
    echo "🔗 View in AWS Console:"
    echo "   https://console.aws.amazon.com/cloudformation/home?region=$AWS_REGION#/stacks/stackinfo?stackId={stack_name}"
    echo ""
    echo "📊 Check agent status in Dagster+ UI:"
    echo "   https://{org_name}.dagster.plus/deployment/{deployment_name}/agents"
else
    echo ""
    echo "❌ CloudFormation deployment failed!"
    echo "💡 Check the AWS CloudFormation console for error details:"
    echo "   https://console.aws.amazon.com/cloudformation/home?region=$AWS_REGION"
    exit 1
fi
"""
    
    deploy_script_path = os.path.join(ecs_dir, "deploy-ecs-agent.sh")
    with open(deploy_script_path, "w") as f:
        f.write(deploy_script_content)
    os.chmod(deploy_script_path, 0o755)
    
    # Generate stack deletion script
    delete_script_content = f"""#!/bin/bash
# Delete Dagster+ ECS Agent CloudFormation Stack
# Generated by onboard.py for {org_name}/{deployment_name}

set -e

echo "🗑️  Deleting Dagster+ ECS Agent stack..."
echo "📋 Stack name: {stack_name}"
echo ""

# Get current region
AWS_REGION=$(aws configure get region)
if [ -z "$AWS_REGION" ]; then
    AWS_REGION="us-east-1"
fi

echo "🌎 Using AWS region: $AWS_REGION"
echo ""

read -p "⚠️  Are you sure you want to delete the stack '{stack_name}'? (y/N): " confirm
if [[ $confirm != [yY] && $confirm != [yY][eE][sS] ]]; then
    echo "❌ Deletion cancelled"
    exit 0
fi

echo "🗑️  Deleting CloudFormation stack..."
aws cloudformation delete-stack \\
    --stack-name "{stack_name}" \\
    --region "$AWS_REGION"

echo "✅ Stack deletion initiated"
echo "💡 Monitor deletion progress:"
echo "   aws cloudformation describe-stacks --stack-name {stack_name} --region $AWS_REGION"
"""
    
    delete_script_path = os.path.join(ecs_dir, "delete-ecs-agent.sh")
    with open(delete_script_path, "w") as f:
        f.write(delete_script_content)
    os.chmod(delete_script_path, 0o755)
    
    return cf_params_path, deploy_script_path, delete_script_path

def setup_project_structure(deploy_type, quickstart_dir):
    """Set up the project directory structure."""
    if deploy_type == 3:  # Custom project
        print("📁 Setting up custom project structure...")
        # Create basic project files
        if not os.path.exists("pyproject.toml"):
            with open("pyproject.toml", "w") as f:
                f.write('''[build-system]
requires = ["setuptools"]
build-backend = "setuptools.build_meta"

[tool.dg]
directory_type = "project"

[tool.dg.project]
root_module = "dagster_project"
registry_modules = [
    "dagster_project.components.*",
]
''')
            print("✅ Created pyproject.toml")
    else:
        # Quickstart project - don't recreate existing structure
        print("🔧 Using existing quickstart project structure...")
        if quickstart_dir and os.path.exists(quickstart_dir):
            print(f"   ✅ Using existing {quickstart_dir} directory")
            print(f"   ✅ Project structure already configured")
        else:
            print("   ⚠️  Quickstart directory not found")

def setup_components_migration(project_dir, pkg_mgr):
    """Set up Components migration for the project."""
    print("\n🔧 Checking if your project is Components-compatible...")
    print("For dbt and Airlift integrations, your project needs to support Dagster Components.")
    
    if is_components_compatible(project_dir):
        print("✅ Project is already Components-compatible!")
        return True
    else:
        print("⚠️  Project needs Components migration to use dbt/Airlift integrations.")
        
        if choose("Make your project Components-compatible?", ["Yes (required for dbt/Airlift)", "Skip for now"]) == 1:
            print("\n🔧 Making project Components-compatible...")
            print("📋 Following: https://docs.dagster.io/guides/build/projects/moving-to-components/migrating-project")
            
            # Navigate to project directory
            original_dir = os.getcwd()
            os.chdir(project_dir)

            try:
                # Step 1: Ensure pyproject.toml has [project] table for tool compatibility
                print("\n1️⃣ Checking pyproject.toml configuration...")
                ensure_project_table(project_dir)
                
                # Step 2: Install dagster-dg-cli
                print("\n2️⃣ Installing dagster-dg-cli...")
                if pkg_mgr == 2:  # uv
                    subprocess.run(["uv", "add", "dagster-dg-cli"], check=False)
                else:  # pip
                    install_python_packages(["dagster-dg-cli"])
                
                # Step 3: Check if dg configuration already exists
                print("\n3️⃣ Checking Components configuration...")
                
                # Check if dg.toml exists or if pyproject.toml has [tool.dg] section
                dg_toml_path = os.path.join(project_dir, "dg.toml")
                pyproject_path = os.path.join(project_dir, "pyproject.toml")
                
                if os.path.exists(dg_toml_path):
                    print("✅ dg.toml already exists")
                elif os.path.exists(pyproject_path):
                    with open(pyproject_path, "r") as f:
                        content = f.read()
                        if "[tool.dg]" in content:
                            print("✅ pyproject.toml already has [tool.dg] section")
                        else:
                            print("⚠️  pyproject.toml missing [tool.dg] section")
                            return False
                else:
                    print("❌ No project configuration found")
                    return False
                
                print("✅ Project is already Components-compatible!")
                print("💡 Skipping dagster-dg-cli installation since project is already configured")
                os.chdir(original_dir)
                return True
                
            except Exception as e:
                print(f"❌ Components migration failed: {e}")
                os.chdir(original_dir)
                return False
        else:
            print("⚠️  Skipping Components migration. dbt/Airlift integrations will not work.")
            return False

def setup_dbt_integration(project_dir, pkg_mgr):
    """Set up dbt integration."""
    print("\n🔧 Setting up dbt integration...")
    
    if choose("Do you want to add dbt integration to your Dagster project?", ["Yes", "No"]) == 1:
        print("\n📋 This will add dbt integration as a component within your main Dagster project.")
        
        # Install dependencies for dbt integration
        print("\n📦 Installing dbt dependencies...")
        
        # Change to project directory for package installation
        original_dir = os.getcwd()
        os.chdir(project_dir)
        
        try:
            # Ensure pyproject.toml has [project] table for uv compatibility
            ensure_project_table(project_dir)
            
            if pkg_mgr == 2:  # uv
                subprocess.run(["uv", "add", "dagster-dbt", "dbt-core", "dbt-duckdb"], check=False)
            else:  # pip
                install_python_packages(["dagster-dbt", "dbt-core", "dbt-duckdb"])
            
            # Update setup.py to include dbt dependencies for deployment
            print("\n🔧 Updating setup.py with dbt dependencies...")
            setup_py_path = os.path.join(project_dir, "setup.py")
            if os.path.exists(setup_py_path):
                with open(setup_py_path, "r") as f:
                    setup_content = f.read()
                
                                    # Check if dagster-dbt is already in install_requires
                    if "dagster-dbt" not in setup_content:
                        # Add dagster-dbt, dbt-core, and dbt-duckdb to install_requires
                        lines = setup_content.split('\n')
                        for i, line in enumerate(lines):
                            if 'install_requires=[' in line:
                                # Find the closing bracket
                                for j in range(i, len(lines)):
                                    if ']' in lines[j] and lines[j].strip().startswith(']'):
                                        # Insert the new dependencies before the closing bracket
                                        lines.insert(j, '        "dagster-dbt",')
                                        lines.insert(j, '        "dbt-core",')
                                        lines.insert(j, '        "dbt-duckdb",')
                                        break
                                break
                    
                        # Write back to setup.py
                        with open(setup_py_path, "w") as f:
                            f.write('\n'.join(lines))
                        print("✅ Added dagster-dbt, dbt-core, and dbt-duckdb to setup.py install_requires")
                    else:
                        print("✅ setup.py already includes dbt dependencies")
            else:
                print("⚠️  setup.py not found - dbt dependencies may not be included in deployment")
            
            # Update dagster_cloud.yaml to include dbt packages for deployment
            print("\n🔧 Updating dagster_cloud.yaml with dbt packages...")
            dagster_cloud_path = os.path.join(project_dir, "dagster_cloud.yaml")
            if os.path.exists(dagster_cloud_path):
                with open(dagster_cloud_path, "r") as f:
                    yaml_content = f.read()
                
                                    # Check if dagster-dbt is already in python_packages
                    if "dagster-dbt" not in yaml_content:
                        # Add dagster-dbt, dbt-core, and dbt-duckdb to python_packages
                        lines = yaml_content.split('\n')
                        for i, line in enumerate(lines):
                            if 'python_packages:' in line:
                                # Find the end of the python_packages list
                                for j in range(i + 1, len(lines)):
                                    if lines[j].strip().startswith('-') and 'dagster' in lines[j]:
                                        # Insert the new packages after existing dagster packages
                                        lines.insert(j + 1, '        - dagster-dbt')
                                        lines.insert(j + 2, '        - dbt-core')
                                        lines.insert(j + 3, '        - dbt-duckdb')
                                        break
                                    elif lines[j].strip() == '' or not lines[j].strip().startswith('-'):
                                        # End of list, insert before this line
                                        lines.insert(j, '        - dagster-dbt')
                                        lines.insert(j + 1, '        - dbt-core')
                                        lines.insert(j + 2, '        - dbt-duckdb')
                                        break
                                break
                    
                        # Write back to dagster_cloud.yaml
                        with open(dagster_cloud_path, "w") as f:
                            f.write('\n'.join(lines))
                        print("✅ Added dagster-dbt, dbt-core, and dbt-duckdb to dagster_cloud.yaml python_packages")
                    else:
                        print("✅ dagster_cloud.yaml already includes dbt packages")
            else:
                print("⚠️  dagster_cloud.yaml not found - dbt packages may not be included in deployment")
        
        except Exception as e:
            print(f"❌ Failed to install dbt dependencies: {e}")
            print("💡 Continuing with dbt component setup...")
        finally:
            # Always return to original directory
            os.chdir(original_dir)
        
        # Use modern dg scaffold approach for dbt integration
        print(f"⚙️  Scaffolding dbt component with 'dg scaffold'...")
        
        # Change to project directory for dg commands
        original_dir = os.getcwd()
        os.chdir(project_dir)
        
        try:
            # Ensure we're using the project's virtual environment
            if pkg_mgr == 2:  # uv
                print("🔧 Activating project virtual environment for dg commands...")
                env = os.environ.copy()
                env["VIRTUAL_ENV"] = os.path.join(project_dir, ".venv")
                env["PATH"] = os.path.join(project_dir, ".venv", "bin") + os.pathsep + env.get("PATH", "")
            else:
                env = os.environ.copy()
            # Clean up existing defs/transform directory if it exists
            defs_transform_path = os.path.join("quickstart_etl", "defs", "transform")
            if os.path.exists(defs_transform_path):
                print(f"🗑️  Removing existing {defs_transform_path} directory...")
                shutil.rmtree(defs_transform_path)
            
            subprocess.run([
                "dg", "scaffold", "defs", 
                "dagster_dbt.DbtProjectComponent", 
                "transform", 
                "--project-path", "transform"
            ], check=True, env=env)
            print("✅ dbt component scaffolded successfully")
            
            # Find and update the defs.yaml with proper configuration
            import glob
            
            # Try multiple possible patterns for defs.yaml location
            defs_yaml_patterns = [
                "quickstart_etl/defs/transform/defs.yaml",  # Quickstart layout
                "src/*/defs/transform/defs.yaml",  # Standard src layout
                "*/defs/transform/defs.yaml",     # Top-level package layout  
                "**/defs/transform/defs.yaml"     # Recursive search
            ]
            
            defs_yaml_path = None
            for pattern in defs_yaml_patterns:
                defs_yaml_files = glob.glob(pattern, recursive=True)
                if defs_yaml_files:
                    defs_yaml_path = defs_yaml_files[0]
                    break
            
            if defs_yaml_path:
                print(f"⚙️  Updating {defs_yaml_path} with dbt project configuration...")

                # Write simple YAML mapping with 'type' first (Python 3.7+ preserves insertion order)
                defs_config = {
                    "type": "dagster_dbt.DbtProjectComponent",
                    "attributes": {
                        "project": "{{ project_root }}/transform",
                        "translation": {
                            "key": "target/main/{{ node.name }}"
                        }
                    }
                }

                try:
                    import yaml
                except ImportError:
                    print(f"⚠️  PyYAML not available - installing it now...")
                    if pkg_mgr == 2:  # uv
                        subprocess.run(["uv", "pip", "install", "PyYAML"], check=True)
                    else:  # pip
                        subprocess.run(["python3", "-m", "pip", "install", "PyYAML"], check=True)
                    import yaml

                with open(defs_yaml_path, "w") as f:
                    yaml.safe_dump(defs_config, f, sort_keys=False)
                
                print(f"✅ Updated defs.yaml with dbt project configuration")
                
                # Set up dbt project
                print(f"\n🔧 Setting up dbt project...")
                
                # Ask user about dbt project
                dbt_project_choice = choose(
                    "Which dbt project would you like to use?",
                    [
                        "Jaffle Shop (example dbt project)", 
                        "Existing local dbt project", 
                        "External dbt repository (separate repo)",
                        "Create new dbt project"
                    ]
                )
                
                if dbt_project_choice == 1:  # Jaffle Shop
                    transform_dir = os.path.join(project_dir, "transform")
                    if not os.path.exists(transform_dir):
                        print(f"📁 Cloning jaffle_shop dbt project...")
                        subprocess.run(["git", "clone", JAFFLE_SHOP_REPO, transform_dir])
                        
                        # Create or update profiles.yml
                        profiles_path = os.path.join(transform_dir, "profiles.yml")
                        if os.path.exists(profiles_path):
                            ensure_profiles_has_dev(profiles_path)
                        else:
                            print(f"📝 Creating profiles.yml for Jaffle Shop project...")
                            # Create a basic profiles.yml for the Jaffle Shop project
                            profiles_content = """jaffle_shop:
  target: dev
  outputs:
    dev:
      type: duckdb
      path: jaffle_shop.duckdb
      schema: main
"""
                            with open(profiles_path, "w") as f:
                                f.write(profiles_content)
                            print(f"✅ Created profiles.yml with DuckDB configuration")
                    else:
                        print(f"✅ dbt project directory {transform_dir} already exists")
                    
                    # Compile the dbt project to generate manifest.json
                    print(f"🔧 Compiling dbt project to generate manifest.json...")
                    try:
                        # Change to transform directory and run dbt compile
                        original_cwd = os.getcwd()
                        os.chdir(transform_dir)
                        
                        compile_result = subprocess.run(["dbt", "compile"], capture_output=True, text=True)
                        if compile_result.returncode == 0:
                            print(f"✅ dbt project compiled successfully")
                        else:
                            print(f"⚠️  dbt compile had warnings/errors:")
                            print(f"   stdout: {compile_result.stdout}")
                            print(f"   stderr: {compile_result.stderr}")
                            print(f"💡 Continuing anyway - manifest.json may have been created")
                        
                        os.chdir(original_cwd)
                    except subprocess.CalledProcessError as e:
                        print(f"❌ Failed to compile dbt project: {e}")
                        print(f"💡 You may need to run 'dbt compile' manually in {transform_dir}")
                        os.chdir(original_cwd)
                    except FileNotFoundError:
                        print(f"⚠️  dbt command not found - you may need to install dbt-core")
                        print(f"💡 Run 'pip install dbt-core' and then 'dbt compile' in {transform_dir}")
                        os.chdir(original_cwd)
                    
                elif dbt_project_choice == 2:  # Existing project
                    existing_path = input("Enter the path to your existing dbt project: ").strip()
                    if existing_path and os.path.exists(existing_path):
                        # Try to detect the database adapter from profiles.yml
                        detected_adapter = None
                        profiles_path = os.path.join(existing_path, "profiles.yml")
                        
                        if os.path.exists(profiles_path):
                            print(f"🔍 Analyzing profiles.yml to detect database adapter...")
                            try:
                                import yaml
                                with open(profiles_path, "r") as f:
                                    profiles = yaml.safe_load(f)
                                
                                # Look for adapter type in any profile
                                for profile_name, profile_config in profiles.items():
                                    if isinstance(profile_config, dict) and "outputs" in profile_config:
                                        for output_name, output_config in profile_config["outputs"].items():
                                            if isinstance(output_config, dict) and "type" in output_config:
                                                detected_adapter = output_config["type"]
                                                print(f"✅ Detected database adapter: {detected_adapter}")
                                                break
                                        if detected_adapter:
                                            break
                            except Exception as e:
                                print(f"⚠️  Could not parse profiles.yml: {e}")
                        
                        # Map common adapter types to package names
                        adapter_packages = {
                            "postgres": "dbt-postgres",
                            "redshift": "dbt-redshift", 
                            "bigquery": "dbt-bigquery",
                            "snowflake": "dbt-snowflake",
                            "duckdb": "dbt-duckdb",
                            "sqlite": "dbt-sqlite",
                            "mysql": "dbt-mysql",
                            "oracle": "dbt-oracle",
                            "spark": "dbt-spark",
                            "trino": "dbt-trino",
                            "clickhouse": "dbt-clickhouse"
                        }
                        
                        # Ask user to confirm or choose adapter
                        if detected_adapter and detected_adapter in adapter_packages:
                            confirm_adapter = choose(
                                f"Detected '{detected_adapter}' adapter. Is this correct?",
                                ["Yes, use detected adapter", "No, let me choose manually"]
                            )
                            if confirm_adapter == 1:
                                dbt_adapter_package = adapter_packages[detected_adapter]
                            else:
                                detected_adapter = None
                        
                        if not detected_adapter or detected_adapter not in adapter_packages:
                            # Ask user to choose adapter manually
                            print(f"🔧 Please select your database adapter:")
                            adapter_choices = list(adapter_packages.keys())
                            adapter_choice = choose(
                                "Which database adapter does your dbt project use?",
                                adapter_choices + ["Other (manual setup required)"]
                            )
                            
                            if adapter_choice <= len(adapter_choices):
                                chosen_adapter = adapter_choices[adapter_choice - 1]
                                dbt_adapter_package = adapter_packages[chosen_adapter]
                                print(f"✅ Will install {dbt_adapter_package}")
                            else:
                                dbt_adapter_package = None
                                print(f"⚠️  You'll need to manually install your dbt adapter package")
                        
                        # Install the adapter package if we have one
                        if dbt_adapter_package:
                            print(f"📦 Installing {dbt_adapter_package}...")
                            try:
                                if pkg_mgr == 2:  # uv
                                    subprocess.run(["uv", "add", dbt_adapter_package], check=False)
                                else:  # pip
                                    install_python_packages([dbt_adapter_package])
                                
                                # Also add to setup.py and dagster_cloud.yaml
                                # Update setup.py
                                if os.path.exists(setup_py_path):
                                    with open(setup_py_path, "r") as f:
                                        setup_content = f.read()
                                    
                                    if dbt_adapter_package not in setup_content:
                                        lines = setup_content.split('\n')
                                        for i, line in enumerate(lines):
                                            if 'install_requires=[' in line:
                                                for j in range(i, len(lines)):
                                                    if ']' in lines[j] and lines[j].strip().startswith(']'):
                                                        lines.insert(j, f'        "{dbt_adapter_package}",')
                                                        break
                                                break
                                        
                                        with open(setup_py_path, "w") as f:
                                            f.write('\n'.join(lines))
                                        print(f"✅ Added {dbt_adapter_package} to setup.py")
                                
                                # Update dagster_cloud.yaml
                                if os.path.exists(dagster_cloud_path):
                                    with open(dagster_cloud_path, "r") as f:
                                        yaml_content = f.read()
                                    
                                    if dbt_adapter_package not in yaml_content:
                                        lines = yaml_content.split('\n')
                                        for i, line in enumerate(lines):
                                            if 'python_packages:' in line:
                                                for j in range(i + 1, len(lines)):
                                                    if lines[j].strip().startswith('-') and 'dagster' in lines[j]:
                                                        lines.insert(j + 1, f'        - {dbt_adapter_package}')
                                                        break
                                                    elif lines[j].strip() == '' or not lines[j].strip().startswith('-'):
                                                        lines.insert(j, f'        - {dbt_adapter_package}')
                                                        break
                                                break
                                        
                                        with open(dagster_cloud_path, "w") as f:
                                            f.write('\n'.join(lines))
                                        print(f"✅ Added {dbt_adapter_package} to dagster_cloud.yaml")
                                
                            except Exception as e:
                                print(f"⚠️  Could not install {dbt_adapter_package}: {e}")
                        
                        # Copy the project
                        transform_dir = os.path.join(project_dir, "transform")
                        if os.path.exists(transform_dir):
                            shutil.rmtree(transform_dir)
                        shutil.copytree(existing_path, transform_dir)
                        print(f"✅ Copied existing dbt project to {transform_dir}")
                        
                        # Try to compile the existing project
                        print(f"🔧 Attempting to compile existing dbt project...")
                        try:
                            original_cwd = os.getcwd()
                            os.chdir(transform_dir)
                            
                            compile_result = subprocess.run(["dbt", "compile"], capture_output=True, text=True)
                            if compile_result.returncode == 0:
                                print(f"✅ dbt project compiled successfully")
                            else:
                                print(f"⚠️  dbt compile had warnings/errors:")
                                print(f"   stdout: {compile_result.stdout}")
                                print(f"   stderr: {compile_result.stderr}")
                                print(f"💡 You may need to check your profiles.yml configuration")
                            
                            os.chdir(original_cwd)
                        except Exception as e:
                            print(f"⚠️  Could not compile dbt project: {e}")
                            print(f"💡 You may need to run 'dbt compile' manually in {transform_dir}")
                            os.chdir(original_cwd)
                            
                    else:
                        print(f"⚠️  Path not found: {existing_path}")
                
                elif dbt_project_choice == 3:  # External dbt repository
                    print(f"\n🔗 External dbt Repository Setup")
                    print(f"💡 This will:")
                    print(f"   1. Clone the dbt repo locally for development")
                    print(f"   2. Configure CI/CD to clone it during deployment")
                    
                    dbt_repo_url = input("Enter the dbt repository URL (e.g., https://github.com/user/dbt-project.git): ").strip()
                    if dbt_repo_url:
                        dbt_repo_branch = input("Enter the dbt repository branch (or press Enter for 'main'): ").strip()
                        if not dbt_repo_branch:
                            dbt_repo_branch = "main"
                        
                        dbt_project_path = input("Enter the path within the repo to dbt project (or press Enter for root): ").strip()
                        if not dbt_project_path:
                            dbt_project_path = "."
                        
                        # Clone the dbt repository locally first
                        transform_dir = os.path.join(project_dir, "transform")
                        if os.path.exists(transform_dir):
                            print(f"⚠️  transform/ directory already exists")
                            replace_choice = choose(
                                "What would you like to do?",
                                ["Replace it with external dbt repo", "Keep existing", "Cancel"]
                            )
                            if replace_choice == 1:
                                shutil.rmtree(transform_dir)
                            elif replace_choice == 2:
                                print(f"✅ Keeping existing transform/ directory")
                                print(f"⚠️  Skipping local clone - CI/CD will still be configured")
                                # Just configure CI/CD without cloning locally
                                setup_external_dbt_integration(project_dir, dbt_repo_url, dbt_repo_branch, dbt_project_path)
                                # Skip the rest of the local clone logic
                                dbt_repo_url = None
                            else:
                                print(f"❌ Cancelled external dbt setup")
                                # Skip the rest of the logic
                                dbt_repo_url = None
                        
                        # Only proceed with local clone if dbt_repo_url is still set
                        if dbt_repo_url:
                            # Clone the external dbt repository locally
                            print(f"\n📥 Cloning external dbt repository locally...")
                            try:
                                # Clone to a temporary directory first
                                import tempfile
                                with tempfile.TemporaryDirectory() as temp_dir:
                                    clone_result = subprocess.run([
                                        "git", "clone", 
                                        "--branch", dbt_repo_branch,
                                        "--depth", "1",  # Shallow clone for speed
                                        dbt_repo_url, 
                                        temp_dir
                                    ], capture_output=True, text=True)
                                    
                                    if clone_result.returncode != 0:
                                        print(f"❌ Failed to clone dbt repository")
                                        print(f"Error: {clone_result.stderr}")
                                        print(f"⚠️  Skipping local clone - you'll need to clone manually")
                                    else:
                                        # Copy the dbt project to transform/
                                        source_path = os.path.join(temp_dir, dbt_project_path)
                                        if os.path.exists(source_path):
                                            shutil.copytree(source_path, transform_dir)
                                            print(f"✅ Cloned external dbt repository to transform/")
                                            
                                            # Install dbt dependencies and compile
                                            print(f"🔧 Installing dbt dependencies and compiling...")
                                            try:
                                                original_cwd = os.getcwd()
                                                os.chdir(transform_dir)
                                                
                                                deps_result = subprocess.run(["dbt", "deps"], capture_output=True, text=True)
                                                if deps_result.returncode == 0:
                                                    print(f"✅ dbt deps completed successfully")
                                                else:
                                                    print(f"⚠️  dbt deps had warnings: {deps_result.stderr}")
                                                
                                                compile_result = subprocess.run(["dbt", "compile"], capture_output=True, text=True)
                                                if compile_result.returncode == 0:
                                                    print(f"✅ dbt compile completed successfully")
                                                else:
                                                    print(f"⚠️  dbt compile had warnings: {compile_result.stderr}")
                                                
                                                os.chdir(original_cwd)
                                            except FileNotFoundError:
                                                print(f"⚠️  dbt command not found - you'll need to run 'dbt deps && dbt compile' manually")
                                                os.chdir(original_cwd)
                                            except Exception as e:
                                                print(f"⚠️  Could not compile dbt project: {e}")
                                                os.chdir(original_cwd)
                                        else:
                                            print(f"❌ dbt project path '{dbt_project_path}' not found in repository")
                                            print(f"⚠️  Please check the path and clone manually")
                            
                            except Exception as e:
                                print(f"❌ Failed to clone external dbt repository: {e}")
                                print(f"⚠️  You'll need to clone it manually to transform/")
                            
                            # Ask about deployment type for CI/CD configuration
                            print(f"\n🚀 Deployment Configuration")
                            print(f"💡 To configure CI/CD properly, we need to know your deployment type")
                            
                            deployment_type_choice = choose(
                                "What type of Dagster+ deployment will you use?",
                                ["Serverless (PEX)", "Hybrid (Docker + Agent)", "Skip CI/CD configuration"]
                            )
                            
                            if deployment_type_choice == 1:
                                deployment_type = "serverless"
                                container_registry = None
                            elif deployment_type_choice == 2:
                                deployment_type = "hybrid"
                                # Prompt for container registry
                                print(f"\n📦 Container Registry Configuration")
                                print(f"💡 Hybrid deployments require a container registry")
                                
                                registry_choice = choose(
                                    "Which container registry will you use?",
                                    ["DockerHub", "Amazon ECR", "Google GCR", "Other"]
                                )
                                
                                container_registry = ["DockerHub", "ECR", "GCR", "Other"][registry_choice - 1]
                            else:
                                deployment_type = None
                                container_registry = None
                            
                            # Set up external dbt integration for CI/CD
                            if deployment_type:
                                setup_external_dbt_integration(project_dir, dbt_repo_url, dbt_repo_branch, dbt_project_path, deployment_type, container_registry)
                            else:
                                print(f"⏭️  Skipped CI/CD configuration - you can configure it manually later")
                    else:
                        print(f"⚠️  Repository URL required for external dbt setup")
                
                elif dbt_project_choice == 4:  # Create new
                    transform_dir = os.path.join(project_dir, "transform")
                    if not os.path.exists(transform_dir):
                        os.makedirs(transform_dir)
                        print(f"📁 Created new dbt project directory: {transform_dir}")
                        print(f"💡 You'll need to initialize it with 'dbt init' and configure it manually")
                    else:
                        print(f"✅ dbt project directory {transform_dir} already exists")
                
                print(f"✅ dbt project setup complete!")
                    
            else:
                print(f"⚠️  Could not find defs.yaml in expected locations")
                print(f"💡 Component was scaffolded but may need manual configuration")
                print(f"   Look for defs.yaml files and update them with dbt project settings")
                
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            print(f"❌ dg scaffold failed: {e}")
            print("⚠️  Make sure 'dg' command is available (part of dagster installation)")
            print("💡 You can manually run: dg scaffold defs dagster_dbt.DbtProjectComponent transform --project-path transform")
            
            # Fallback: Create the component files manually
            print("\n🔧 Creating dbt component files manually...")
            try:
                    # Create the transform component directory structure
                    transform_component_dir = os.path.join("quickstart_etl", "defs", "transform")
                    os.makedirs(transform_component_dir, exist_ok=True)
                    
                    # Create __init__.py
                    with open(os.path.join(transform_component_dir, "__init__.py"), "w") as f:
                        f.write("# Dagster dbt component\n")
                    
                    # Create the main component file
                    transform_component_content = '''from dagster import Definitions
from dagster_dbt import DbtProjectComponent

# Create the dbt project component
dbt_project = DbtProjectComponent(
    project_dir="{{ project_root }}/transform"
)

# Create definitions that include the dbt component
defs = dbt_project.create_definitions()

# Export the definitions
__all__ = ["defs"]
'''
                    
                    with open(os.path.join(transform_component_dir, "dbt_component.py"), "w") as f:
                        f.write(transform_component_content)
                    
                    # Create defs.yaml
                    defs_yaml_content = '''type: dagster_dbt.DbtProjectComponent
attributes:
  project: "{{ project_root }}/transform"
  translation:
    key: "target/main/{{ node.name }}"
'''
                    
                    with open(os.path.join(transform_component_dir, "defs.yaml"), "w") as f:
                        f.write(defs_yaml_content)
                    
                    print("✅ Created dbt component files manually:")
                    print(f"   - {transform_component_dir}/__init__.py")
                    print(f"   - {transform_component_dir}/dbt_component.py")
                    print(f"   - {transform_component_dir}/defs.yaml")
                    
            except Exception as manual_error:
                print(f"❌ Manual file creation also failed: {manual_error}")
                print("💡 You'll need to create the component files manually")
        
        finally:
            # Always return to original directory
            os.chdir(original_dir)

def setup_airlift_integration(project_dir, pkg_mgr):
    """Set up Airlift integration."""
    print("\n🔧 Setting up Airlift integration...")
    
    if choose("Do you want to add Airlift integration to your Dagster project?", ["Yes", "No"]) == 1:
        print("\n📋 This will add Airlift integration as a component within your main Dagster project.")
        
        # Get Airflow instance name
        airflow_name = input("Enter a name for your Airflow instance (or press Enter for 'my_airflow'): ").strip()
        if not airflow_name:
            airflow_name = "my_airflow"
        
        # Install dependencies for Airlift integration
        print("\n📦 Installing Airlift dependencies...")
        
        # Change to project directory for package installation
        original_dir = os.getcwd()
        os.chdir(project_dir)
        
        try:
            # Ensure pyproject.toml has [project] table for uv compatibility
            ensure_project_table(project_dir)
            
            if pkg_mgr == 2:  # uv
                subprocess.run(["uv", "add", "dagster-airlift"], check=False)
            else:  # pip
                install_python_packages(["dagster-airlift"])
            
            # Use modern dg scaffold approach for Airlift integration
            print(f"⚙️  Scaffolding Airlift component with 'dg scaffold'...")
            
            # Ensure we're using the project's virtual environment
            if pkg_mgr == 2:  # uv
                print("🔧 Activating project virtual environment for dg commands...")
                env = os.environ.copy()
                env["VIRTUAL_ENV"] = os.path.join(project_dir, ".venv")
                env["PATH"] = os.path.join(project_dir, ".venv", "bin") + os.pathsep + env.get("PATH", "")
            else:
                env = os.environ.copy()
            
            try:
                # Clean up existing defs/airflow directory if it exists
                defs_airflow_path = os.path.join("quickstart_etl", "defs", "airflow")
                if os.path.exists(defs_airflow_path):
                    print(f"🗑️  Removing existing {defs_airflow_path} directory...")
                    shutil.rmtree(defs_airflow_path)
                
                subprocess.run([
                    "dg", "scaffold", "defs",
                    "dagster_airlift.core.components.AirflowInstanceComponent",
                    "airflow",
                    "--name", airflow_name,
                    "--auth-type", "basic_auth"
                ], check=True, env=env)
                print("✅ Airlift component scaffolded successfully")
                
                # Find and update the defs.yaml with proper configuration
                import glob
                
                # Try multiple possible patterns for defs.yaml location
                defs_yaml_patterns = [
                    "quickstart_etl/defs/airflow/defs.yaml",  # Quickstart layout
                    "src/*/defs/airflow/defs.yaml",  # Standard src layout
                    "*/defs/airflow/defs.yaml",     # Top-level package layout  
                    "**/defs/airflow/defs.yaml"     # Recursive search
                ]
                
                defs_yaml_path = None
                for pattern in defs_yaml_patterns:
                    defs_yaml_files = glob.glob(pattern, recursive=True)
                    if defs_yaml_files:
                        defs_yaml_path = defs_yaml_files[0]
                        break
                
                if defs_yaml_path:
                    print(f"⚙️  Updating {defs_yaml_path} with Airflow configuration...")

                    # Write simple YAML mapping with type first
                    defs_config = {
                        "type": "dagster_airlift.core.components.AirflowInstanceComponent",
                        "attributes": {
                            "name": airflow_name,
                            "auth": {
                                "type": "basic_auth",
                                "webserver_url": '{{ env("AIRFLOW_WEBSERVER_URL") }}',
                                "username": '{{ env("AIRFLOW_USERNAME") }}',
                                "password": '{{ env("AIRFLOW_PASSWORD") }}'
                            }
                        }
                    }

                    try:
                        import yaml
                    except ImportError:
                        print(f"⚠️  PyYAML not available - installing it now...")
                        if pkg_mgr == 2:  # uv
                            subprocess.run(["uv", "pip", "install", "PyYAML"], check=True)
                        else:  # pip
                            subprocess.run(["python3", "-m", "pip", "install", "PyYAML"], check=True)
                        import yaml

                    with open(defs_yaml_path, "w") as f:
                        yaml.safe_dump(defs_config, f, sort_keys=False)
                    
                    print(f"✅ Updated defs.yaml with Airflow configuration")
                    print("👉 Store AIRFLOW_WEBSERVER_URL, AIRFLOW_USERNAME, and AIRFLOW_PASSWORD as environment variables!")
                else:
                    print(f"⚠️  Could not find defs.yaml in expected locations")
                    print(f"💡 Component was scaffolded but may need manual configuration")
                    print(f"   Look for defs.yaml files and update them with Airflow settings")
                    print("👉 Store AIRFLOW_WEBSERVER_URL, AIRFLOW_USERNAME, and AIRFLOW_PASSWORD as environment variables!")
                    
            except (subprocess.CalledProcessError, FileNotFoundError) as e:
                print(f"❌ dg scaffold failed: {e}")
                print("⚠️  Make sure 'dg' command is available (part of dagster installation)")
                print("💡 You can manually run: dg scaffold defs dagster_airlift.core.components.AirflowInstanceComponent airflow --name my_airflow --auth-type basic_auth")
                
                # Fallback: Create the component files manually
                print("\n🔧 Creating Airlift component files manually...")
                try:
                    # Create the airflow component directory structure
                    airflow_component_dir = os.path.join("quickstart_etl", "defs", "airflow")
                    os.makedirs(airflow_component_dir, exist_ok=True)
                    
                    # Create __init__.py
                    with open(os.path.join(airflow_component_dir, "__init__.py"), "w") as f:
                        f.write("# Dagster Airlift component\n")
                    
                    # Create the main component file
                    airflow_component_content = f'''from dagster import Definitions
from dagster_airlift.core.components import AirflowInstanceComponent

# Create the Airflow instance component
airflow_instance = AirflowInstanceComponent(
    name="{airflow_name}",
    auth_type="basic_auth",
    webserver_url="{{{{ env("AIRFLOW_WEBSERVER_URL") }}}}",
    username="{{{{ env("AIRFLOW_USERNAME") }}}}",
    password="{{{{ env("AIRFLOW_PASSWORD") }}}}"
)

# Create definitions that include the Airflow component
defs = airflow_instance.create_definitions()

# Export the definitions
__all__ = ["defs"]
'''
                    
                    with open(os.path.join(airflow_component_dir, "airflow_component.py"), "w") as f:
                        f.write(airflow_component_content)
                    
                    # Create defs.yaml
                    defs_yaml_content = f'''type: dagster_airlift.core.components.AirflowInstanceComponent
attributes:
  name: {airflow_name}
  auth:
    type: basic_auth
    webserver_url: '{{{{ env("AIRFLOW_WEBSERVER_URL") }}}}'
    username: '{{{{ env("AIRFLOW_USERNAME") }}}}'
    password: '{{{{ env("AIRFLOW_PASSWORD") }}}}'
'''
                    
                    with open(os.path.join(airflow_component_dir, "defs.yaml"), "w") as f:
                        f.write(defs_yaml_content)
                    
                    print("✅ Created Airlift component files manually:")
                    print(f"   - {airflow_component_dir}/__init__.py")
                    print(f"   - {airflow_component_dir}/airflow_component.py")
                    print(f"   - {airflow_component_dir}/defs.yaml")
                    
                except Exception as manual_error:
                    print(f"❌ Manual file creation also failed: {manual_error}")
                    print("💡 You'll need to create the component files manually")
        
        finally:
            # Always return to original directory
            os.chdir(original_dir)

def setup_fivetran_integration(project_dir, pkg_mgr):
    """Set up Fivetran integration using Dagster Components."""
    print("\n🔧 Setting up Fivetran integration...")
    print("📋 This will add Fivetran components to sync data from SaaS applications")
    
    # Change to project directory for package installation
    original_dir = os.getcwd()
    os.chdir(project_dir)
    
    try:
        # Install dependencies
        print("\n📦 Installing Fivetran dependencies...")
        if pkg_mgr == 2:  # uv
            subprocess.run(["uv", "add", "dagster-fivetran"], check=False)
        else:  # pip
            install_python_packages(["dagster-fivetran"])
        
        # Prompt for Fivetran credentials
        print("\n🔑 Fivetran API Configuration")
        print("💡 You'll need your Fivetran API key and secret from: https://fivetran.com/account/settings/api")
        
        api_key = input("Enter your Fivetran API key (or press Enter to skip): ").strip()
        if api_key:
            api_secret = input("Enter your Fivetran API secret: ").strip()
            
            if api_secret:
                # Create Fivetran component
                print("🔧 Creating Fivetran component...")
                
                # Try using dg command first
                try:
                    result = subprocess.run([
                        "dg", "component", "generate", 
                        "--name", "fivetran_ingest",
                        "--type", "dagster_fivetran.FivetranInstanceComponent"
                    ], capture_output=True, text=True)
                    
                    if result.returncode == 0:
                        print("✅ Generated Fivetran component using dg")
                        update_fivetran_component(project_dir, api_key, api_secret)
                    else:
                        print("⚠️  dg component generate failed, creating manually...")
                        create_manual_fivetran_component(project_dir, api_key, api_secret)
                        
                except FileNotFoundError:
                    print("⚠️  dg command not found, creating component manually...")
                    create_manual_fivetran_component(project_dir, api_key, api_secret)
                
                print("✅ Fivetran integration setup completed!")
                print("💡 Your Fivetran connectors will be automatically synced")
            else:
                print("⚠️  API secret required for Fivetran integration")
        else:
            print("⚠️  Skipping Fivetran setup. You can add it later.")
            
    except Exception as e:
        print(f"❌ Fivetran integration setup failed: {e}")
    finally:
        os.chdir(original_dir)

def update_fivetran_component(project_dir, api_key, api_secret):
    """Update Fivetran component with API credentials."""
    component_dir = os.path.join(project_dir, "definitions", "components", "fivetran_ingest")
    defs_yaml = os.path.join(component_dir, "defs.yaml")
    
    if os.path.exists(defs_yaml):
        defs_content = f"""type: dagster_fivetran.FivetranInstanceComponent

attributes:
  api_key: '{api_key}'
  api_secret: '{api_secret}'
"""
        
        with open(defs_yaml, "w") as f:
            f.write(defs_content)
        
        print(f"✅ Updated Fivetran component with API credentials")
    else:
        print(f"⚠️  Component defs.yaml not found at {defs_yaml}")

def create_manual_fivetran_component(project_dir, api_key, api_secret):
    """Create Fivetran component manually."""
    print(f"🔧 Creating Fivetran component manually...")
    
    try:
        component_dir = os.path.join(project_dir, "definitions", "components", "fivetran_ingest")
        os.makedirs(component_dir, exist_ok=True)
        
        defs_content = f"""type: dagster_fivetran.FivetranInstanceComponent

attributes:
  api_key: '{api_key}'
  api_secret: '{api_secret}'
"""
        
        with open(os.path.join(component_dir, "defs.yaml"), "w") as f:
            f.write(defs_content)
        
        print(f"✅ Created Fivetran component manually")
        
    except Exception as e:
        print(f"❌ Failed to create Fivetran component: {e}")

def setup_airbyte_integration(project_dir, pkg_mgr):
    """Set up Airbyte integration using Dagster Components."""
    print("\n🔧 Setting up Airbyte integration...")
    print("📋 This will add Airbyte components for open-source data integration")
    
    # Change to project directory for package installation
    original_dir = os.getcwd()
    os.chdir(project_dir)
    
    try:
        # Install dependencies
        print("\n📦 Installing Airbyte dependencies...")
        if pkg_mgr == 2:  # uv
            subprocess.run(["uv", "add", "dagster-airbyte"], check=False)
        else:  # pip
            install_python_packages(["dagster-airbyte"])
        
        # Prompt for Airbyte configuration
        print("\n🔑 Airbyte Configuration")
        print("💡 You'll need your Airbyte server details")
        
        host = input("Enter your Airbyte host (or press Enter for localhost:8000): ").strip()
        if not host:
            host = "localhost:8000"
        
        username = input("Enter your Airbyte username (or press Enter for airbyte): ").strip()
        if not username:
            username = "airbyte"
        
        password = input("Enter your Airbyte password (or press Enter for password): ").strip()
        if not password:
            password = "password"
        
        # Create Airbyte component
        print("🔧 Creating Airbyte component...")
        
        # Try using dg command first
        try:
            result = subprocess.run([
                "dg", "component", "generate", 
                "--name", "airbyte_ingest",
                "--type", "dagster_airbyte.AirbyteInstanceComponent"
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✅ Generated Airbyte component using dg")
                update_airbyte_component(project_dir, host, username, password)
            else:
                print("⚠️  dg component generate failed, creating manually...")
                create_manual_airbyte_component(project_dir, host, username, password)
                
        except FileNotFoundError:
            print("⚠️  dg command not found, creating component manually...")
            create_manual_airbyte_component(project_dir, host, username, password)
        
        print("✅ Airbyte integration setup completed!")
        print("💡 Your Airbyte connections will be automatically synced")
            
    except Exception as e:
        print(f"❌ Airbyte integration setup failed: {e}")
    finally:
        os.chdir(original_dir)

def update_airbyte_component(project_dir, host, username, password):
    """Update Airbyte component with server configuration."""
    component_dir = os.path.join(project_dir, "definitions", "components", "airbyte_ingest")
    defs_yaml = os.path.join(component_dir, "defs.yaml")
    
    if os.path.exists(defs_yaml):
        defs_content = f"""type: dagster_airbyte.AirbyteInstanceComponent

attributes:
  host: '{host}'
  port: '8000'
  username: '{username}'
  password: '{password}'
"""
        
        with open(defs_yaml, "w") as f:
            f.write(defs_content)
        
        print(f"✅ Updated Airbyte component with server configuration")
    else:
        print(f"⚠️  Component defs.yaml not found at {defs_yaml}")

def create_manual_airbyte_component(project_dir, host, username, password):
    """Create Airbyte component manually."""
    print(f"🔧 Creating Airbyte component manually...")
    
    try:
        component_dir = os.path.join(project_dir, "definitions", "components", "airbyte_ingest")
        os.makedirs(component_dir, exist_ok=True)
        
        defs_content = f"""type: dagster_airbyte.AirbyteInstanceComponent

attributes:
  host: '{host}'
  port: '8000'
  username: '{username}'
  password: '{password}'
"""
        
        with open(os.path.join(component_dir, "defs.yaml"), "w") as f:
            f.write(defs_content)
        
        print(f"✅ Created Airbyte component manually")
        
    except Exception as e:
        print(f"❌ Failed to create Airbyte component: {e}")

def setup_powerbi_integration(project_dir, pkg_mgr):
    """Set up Power BI integration using Dagster Components."""
    print("\n🔧 Setting up Power BI integration...")
    print("📋 This will add Power BI components for business intelligence")
    
    # Change to project directory for package installation
    original_dir = os.getcwd()
    os.chdir(project_dir)
    
    try:
        # Install dependencies
        print("\n📦 Installing Power BI dependencies...")
        if pkg_mgr == 2:  # uv
            subprocess.run(["uv", "add", "dagster-powerbi"], check=False)
        else:  # pip
            install_python_packages(["dagster-powerbi"])
        
        # Prompt for Power BI configuration
        print("\n🔑 Power BI Configuration")
        print("💡 You'll need your Power BI workspace details and credentials")
        
        workspace_id = input("Enter your Power BI workspace ID (or press Enter to skip): ").strip()
        if workspace_id:
            client_id = input("Enter your Azure AD client ID: ").strip()
            client_secret = input("Enter your Azure AD client secret: ").strip()
            tenant_id = input("Enter your Azure AD tenant ID: ").strip()
            
            if client_id and client_secret and tenant_id:
                # Create Power BI component
                print("🔧 Creating Power BI component...")
                
                # Try using dg command first
                try:
                    result = subprocess.run([
                        "dg", "component", "generate", 
                        "--name", "powerbi_workspace",
                        "--type", "dagster_powerbi.PowerBIWorkspaceComponent"
                    ], capture_output=True, text=True)
                    
                    if result.returncode == 0:
                        print("✅ Generated Power BI component using dg")
                        update_powerbi_component(project_dir, workspace_id, client_id, client_secret, tenant_id)
                    else:
                        print("⚠️  dg component generate failed, creating manually...")
                        create_manual_powerbi_component(project_dir, workspace_id, client_id, client_secret, tenant_id)
                        
                except FileNotFoundError:
                    print("⚠️  dg command not found, creating component manually...")
                    create_manual_powerbi_component(project_dir, workspace_id, client_id, client_secret, tenant_id)
                
                print("✅ Power BI integration setup completed!")
                print("💡 Your Power BI workspace will be automatically synced")
            else:
                print("⚠️  All Azure AD credentials required for Power BI integration")
        else:
            print("⚠️  Skipping Power BI setup. You can add it later.")
            
    except Exception as e:
        print(f"❌ Power BI integration setup failed: {e}")
    finally:
        os.chdir(original_dir)

def update_powerbi_component(project_dir, workspace_id, client_id, client_secret, tenant_id):
    """Update Power BI component with workspace configuration."""
    component_dir = os.path.join(project_dir, "definitions", "components", "powerbi_workspace")
    defs_yaml = os.path.join(component_dir, "defs.yaml")
    
    if os.path.exists(defs_yaml):
        defs_content = f"""type: dagster_powerbi.PowerBIWorkspaceComponent

attributes:
  workspace_id: '{workspace_id}'
  client_id: '{client_id}'
  client_secret: '{client_secret}'
  tenant_id: '{tenant_id}'
"""
        
        with open(defs_yaml, "w") as f:
            f.write(defs_content)
        
        print(f"✅ Updated Power BI component with workspace configuration")
    else:
        print(f"⚠️  Component defs.yaml not found at {defs_yaml}")

def create_manual_powerbi_component(project_dir, workspace_id, client_id, client_secret, tenant_id):
    """Create Power BI component manually."""
    print(f"🔧 Creating Power BI component manually...")
    
    try:
        component_dir = os.path.join(project_dir, "definitions", "components", "powerbi_workspace")
        os.makedirs(component_dir, exist_ok=True)
        
        defs_content = f"""type: dagster_powerbi.PowerBIWorkspaceComponent

attributes:
  workspace_id: '{workspace_id}'
  client_id: '{client_id}'
  client_secret: '{client_secret}'
  tenant_id: '{tenant_id}'
"""
        
        with open(os.path.join(component_dir, "defs.yaml"), "w") as f:
            f.write(defs_content)
        
        print(f"✅ Created Power BI component manually")
        
    except Exception as e:
        print(f"❌ Failed to create Power BI component: {e}")

def generate_gitlab_ci_template(workflow_path, deployment_type, org_name, deployment_name):
    """Generate GitLab CI/CD template based on official Dagster documentation."""
    if deployment_type == "serverless":
        template_content = f"""# GitLab CI/CD Pipeline for Dagster+ Serverless Deployment
# Based on official Dagster documentation: https://docs.dagster.io/deployment/dagster-plus/ci-cd/branch-deployments/setting-up-branch-deployments

variables:
  DAGSTER_CLOUD_API_TOKEN: $DAGSTER_CLOUD_API_TOKEN
  DAGSTER_CLOUD_ORGANIZATION: "{org_name}"
  DAGSTER_CLOUD_DEPLOYMENT: "{deployment_name}"
  PYTHON_VERSION: "3.10"
  ENABLE_FAST_DEPLOYS: "true"

stages:
  - validate
  - build
  - deploy

# Serverless deployment job
serverless-deploy:
  stage: deploy
  image: python:$PYTHON_VERSION
  before_script:
    - pip install dagster-cloud
  script:
    # Validate configuration
    - dagster-cloud ci check --project-dir . --dagster-cloud-yaml-path dagster_cloud.yaml
    
    # Initialize build session
    - dagster-cloud ci init --project-dir . --dagster-cloud-yaml-path dagster_cloud.yaml --deployment {deployment_name}
    
    # Build PEX (fast deploys)
    - dagster-cloud ci build --build-strategy=python-executable --python-version $PYTHON_VERSION --pex-deps-cache-from="$CI_PROJECT_PATH" --pex-deps-cache-to="$CI_PROJECT_PATH"
    
    # Deploy to Dagster Cloud
    - dagster-cloud ci deploy
    
    # Update PR comment for branch deployments
    - dagster-cloud ci notify --project-dir=.
    
    # Generate summary
    - dagster-cloud ci status --output-format=markdown
  rules:
    - if: $CI_PIPELINE_SOURCE == "push" && ($CI_COMMIT_BRANCH == "main" || $CI_COMMIT_BRANCH == "master")
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
  artifacts:
    reports:
      junit: dagster-cloud-ci-results.xml
    expire_in: 1 week
"""
    else:  # hybrid
        template_content = f"""# GitLab CI/CD Pipeline for Dagster+ Hybrid Deployment
# Based on official Dagster documentation: https://docs.dagster.io/deployment/dagster-plus/ci-cd/branch-deployments/setting-up-branch-deployments

variables:
  DAGSTER_CLOUD_API_TOKEN: $DAGSTER_CLOUD_API_TOKEN
  DAGSTER_CLOUD_ORGANIZATION: "{org_name}"
  DAGSTER_CLOUD_DEPLOYMENT: "{deployment_name}"
  IMAGE_REGISTRY: "$CI_REGISTRY_IMAGE"  # GitLab Container Registry
  # Alternative registries (uncomment and configure as needed):
  # IMAGE_REGISTRY: "your-registry.com/your-image"  # DockerHub
  # IMAGE_REGISTRY: "your-account.dkr.ecr.us-west-2.amazonaws.com/your-image"  # AWS ECR
  # IMAGE_REGISTRY: "gcr.io/your-project/your-image"  # Google GCR

stages:
  - validate
  - build
  - deploy

# Hybrid deployment job
hybrid-deploy:
  stage: deploy
  image: docker:latest
  services:
    - docker:dind
  before_script:
    - apk add --no-cache python3 py3-pip
    - pip install dagster-cloud
    # Login to container registry
    - echo $CI_REGISTRY_PASSWORD | docker login -u $CI_REGISTRY_USER --password-stdin $CI_REGISTRY
    # Alternative registry logins (uncomment as needed):
    # - echo $DOCKERHUB_TOKEN | docker login -u $DOCKERHUB_USERNAME --password-stdin
    # - aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com
    # - echo $GCR_JSON_KEY | docker login -u _json_key --password-stdin gcr.io
  script:
    # Validate configuration
    - dagster-cloud ci check --project-dir . --dagster-cloud-yaml-path dagster_cloud.yaml
    
    # Initialize build session
    - dagster-cloud ci init --project-dir . --dagster-cloud-yaml-path dagster_cloud.yaml --deployment {deployment_name}
    
    # Generate unique image tag
    - export IMAGE_TAG="$CI_COMMIT_SHA-$CI_PIPELINE_ID-$CI_PIPELINE_IID"
    
    # Build and push Docker image
    - docker buildx create --use
    - docker buildx build --platform linux/amd64 --push --tag $IMAGE_REGISTRY:$IMAGE_TAG .
    
    # Set build output for each location
    - dagster-cloud ci set-build-output --location-name=main --image-tag=$IMAGE_TAG
    
    # Deploy to Dagster Cloud
    - dagster-cloud ci deploy
    
    # Update PR comment for branch deployments
    - dagster-cloud ci notify --project-dir=.
    
    # Generate summary
    - dagster-cloud ci status --output-format=markdown
  rules:
    - if: $CI_PIPELINE_SOURCE == "push" && ($CI_COMMIT_BRANCH == "main" || $CI_COMMIT_BRANCH == "master")
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
  artifacts:
    reports:
      junit: dagster-cloud-ci-results.xml
    expire_in: 1 week
"""
    
    with open(workflow_path, 'w') as f:
        f.write(template_content)
    print(f"✅ Generated GitLab CI template for {deployment_type} deployment")

def generate_azure_pipeline_template(workflow_path, deployment_type, org_name, deployment_name):
    """Generate Azure DevOps pipeline template."""
    if deployment_type == "serverless":
        template_content = f"""# Azure DevOps Pipeline for Dagster+ Serverless Deployment
# Based on official Dagster documentation: https://docs.dagster.io/deployment/dagster-plus/ci-cd/branch-deployments/setting-up-branch-deployments

trigger:
  branches:
    include:
      - main
      - master
  pull_request:
    types: [opened, synchronize, reopened, closed]

pool:
  vmImage: 'ubuntu-latest'

variables:
  DAGSTER_CLOUD_API_TOKEN: $(DAGSTER_CLOUD_API_TOKEN)
  DAGSTER_CLOUD_ORGANIZATION: "{org_name}"
  DAGSTER_CLOUD_DEPLOYMENT: "{deployment_name}"
  PYTHON_VERSION: "3.10"
  ENABLE_FAST_DEPLOYS: "true"

stages:
- stage: Deploy
  displayName: 'Deploy to Dagster+ Serverless'
  jobs:
  - job: ServerlessDeploy
    displayName: 'Serverless Deployment'
    steps:
    - checkout: self
      displayName: 'Checkout code'
      fetchDepth: 0

    - task: UsePythonVersion@0
      displayName: 'Set up Python ${{ variables.PYTHON_VERSION }}'
      inputs:
        versionSpec: '${{ variables.PYTHON_VERSION }}'

    - script: |
        pip install dagster-cloud
      displayName: 'Install Dagster Cloud CLI'

    - script: |
        dagster-cloud ci check --project-dir . --dagster-cloud-yaml-path dagster_cloud.yaml
      displayName: 'Validate configuration'

    - script: |
        dagster-cloud ci init --project-dir . --dagster-cloud-yaml-path dagster_cloud.yaml --deployment {deployment_name}
      displayName: 'Initialize build session'

    - script: |
        dagster-cloud ci build --build-strategy=python-executable --python-version ${{ variables.PYTHON_VERSION }} --pex-deps-cache-from="$(System.TeamFoundationCollectionUri)$(System.TeamProject)/$(Build.Repository.Name)" --pex-deps-cache-to="$(System.TeamFoundationCollectionUri)$(System.TeamProject)/$(Build.Repository.Name)"
      displayName: 'Build PEX'

    - script: |
        dagster-cloud ci deploy
      displayName: 'Deploy to Dagster Cloud'

    - script: |
        dagster-cloud ci notify --project-dir=.
      displayName: 'Update PR comment'

    - script: |
        dagster-cloud ci status --output-format=markdown
      displayName: 'Generate summary'
"""
    else:  # hybrid
        template_content = f"""# Azure DevOps Pipeline for Dagster+ Hybrid Deployment
# Based on official Dagster documentation: https://docs.dagster.io/deployment/dagster-plus/ci-cd/branch-deployments/setting-up-branch-deployments

trigger:
  branches:
    include:
      - main
      - master
  pull_request:
    types: [opened, synchronize, reopened, closed]

pool:
  vmImage: 'ubuntu-latest'

variables:
  DAGSTER_CLOUD_API_TOKEN: $(DAGSTER_CLOUD_API_TOKEN)
  DAGSTER_CLOUD_ORGANIZATION: "{org_name}"
  DAGSTER_CLOUD_DEPLOYMENT: "{deployment_name}"
  IMAGE_REGISTRY: "$(ACR_LOGIN_SERVER)/$(ACR_REPOSITORY)"  # Azure Container Registry
  # Alternative registries (uncomment and configure as needed):
  # IMAGE_REGISTRY: "your-registry.com/your-image"  # DockerHub
  # IMAGE_REGISTRY: "your-account.dkr.ecr.us-west-2.amazonaws.com/your-image"  # AWS ECR
  # IMAGE_REGISTRY: "gcr.io/your-project/your-image"  # Google GCR

stages:
- stage: Deploy
  displayName: 'Deploy to Dagster+ Hybrid'
  jobs:
  - job: HybridDeploy
    displayName: 'Hybrid Deployment'
    steps:
    - checkout: self
      displayName: 'Checkout code'
      fetchDepth: 0

    - task: DockerInstaller@0
      displayName: 'Install Docker'

    - task: UsePythonVersion@0
      displayName: 'Set up Python'
      inputs:
        versionSpec: '3.10'

    - script: |
        pip install dagster-cloud
      displayName: 'Install Dagster Cloud CLI'

    # Login to container registry
    - task: Docker@2
      displayName: 'Login to Azure Container Registry'
      inputs:
        command: 'login'
        containerRegistry: '$(ACR_SERVICE_CONNECTION)'
    # Alternative registry logins (uncomment as needed):
    # - script: |
    #     echo $(DOCKERHUB_TOKEN) | docker login -u $(DOCKERHUB_USERNAME) --password-stdin
    #   displayName: 'Login to DockerHub'
    # - script: |
    #     aws ecr get-login-password --region $(AWS_REGION) | docker login --username AWS --password-stdin $(AWS_ACCOUNT_ID).dkr.ecr.$(AWS_REGION).amazonaws.com
    #   displayName: 'Login to AWS ECR'
    # - script: |
    #     echo $(GCR_JSON_KEY) | docker login -u _json_key --password-stdin gcr.io
    #   displayName: 'Login to Google GCR'

    - script: |
        dagster-cloud ci check --project-dir . --dagster-cloud-yaml-path dagster_cloud.yaml
      displayName: 'Validate configuration'

    - script: |
        dagster-cloud ci init --project-dir . --dagster-cloud-yaml-path dagster_cloud.yaml --deployment {deployment_name}
      displayName: 'Initialize build session'

    - script: |
        export IMAGE_TAG="$(Build.SourceVersion)-$(Build.BuildId)-$(Build.BuildNumber)"
      displayName: 'Generate image tag'

    - task: Docker@2
      displayName: 'Build and push Docker image'
      inputs:
        command: 'buildAndPush'
        repository: '$(ACR_REPOSITORY)'
        dockerfile: '**/Dockerfile'
        containerRegistry: '$(ACR_SERVICE_CONNECTION)'
        tags: |
          $(IMAGE_TAG)

    - script: |
        dagster-cloud ci set-build-output --location-name=main --image-tag=$(IMAGE_TAG)
      displayName: 'Set build output'

    - script: |
        dagster-cloud ci deploy
      displayName: 'Deploy to Dagster Cloud'

    - script: |
        dagster-cloud ci notify --project-dir=.
      displayName: 'Update PR comment'

    - script: |
        dagster-cloud ci status --output-format=markdown
      displayName: 'Generate summary'
"""
    
    with open(workflow_path, 'w') as f:
        f.write(template_content)
    print(f"✅ Generated Azure DevOps pipeline template for {deployment_type} deployment")

def generate_bitbucket_pipeline_template(workflow_path, deployment_type, org_name, deployment_name):
    """Generate Bitbucket pipeline template."""
    if deployment_type == "serverless":
        template_content = f"""# Bitbucket Pipeline for Dagster+ Serverless Deployment
# Based on official Dagster documentation: https://docs.dagster.io/deployment/dagster-plus/ci-cd/branch-deployments/setting-up-branch-deployments

image: python:3.10

definitions:
  caches:
    pip: ~/.cache/pip
  steps:
    - step: &serverless-deploy
        name: Deploy to Dagster+ Serverless
        caches:
          - pip
        script:
          - pip install dagster-cloud
          - export DAGSTER_CLOUD_API_TOKEN=$DAGSTER_CLOUD_API_TOKEN
          - export DAGSTER_CLOUD_ORGANIZATION="{org_name}"
          - export DAGSTER_CLOUD_DEPLOYMENT="{deployment_name}"
          - export PYTHON_VERSION="3.10"
          - export ENABLE_FAST_DEPLOYS="true"
          # Validate configuration
          - dagster-cloud ci check --project-dir . --dagster-cloud-yaml-path dagster_cloud.yaml
          # Initialize build session
          - dagster-cloud ci init --project-dir . --dagster-cloud-yaml-path dagster_cloud.yaml --deployment {deployment_name}
          # Build PEX (fast deploys)
          - dagster-cloud ci build --build-strategy=python-executable --python-version $PYTHON_VERSION --pex-deps-cache-from="$BITBUCKET_REPO_FULL_NAME" --pex-deps-cache-to="$BITBUCKET_REPO_FULL_NAME"
          # Deploy to Dagster Cloud
          - dagster-cloud ci deploy
          # Update PR comment for branch deployments
          - dagster-cloud ci notify --project-dir=.
          # Generate summary
          - dagster-cloud ci status --output-format=markdown
        artifacts:
          - dagster-cloud-ci-results.xml

pipelines:
  branches:
    main:
      - step: *serverless-deploy
    master:
      - step: *serverless-deploy
  pull-requests:
    '**':
      - step: *serverless-deploy
"""
    else:  # hybrid
        template_content = f"""# Bitbucket Pipeline for Dagster+ Hybrid Deployment
# Based on official Dagster documentation: https://docs.dagster.io/deployment/dagster-plus/ci-cd/branch-deployments/setting-up-branch-deployments

image: python:3.10

definitions:
  caches:
    pip: ~/.cache/pip
  steps:
    - step: &hybrid-deploy
        name: Deploy to Dagster+ Hybrid
        services:
          - docker
        caches:
          - pip
        script:
          - pip install dagster-cloud
          - export DAGSTER_CLOUD_API_TOKEN=$DAGSTER_CLOUD_API_TOKEN
          - export DAGSTER_CLOUD_ORGANIZATION="{org_name}"
          - export DAGSTER_CLOUD_DEPLOYMENT="{deployment_name}"
          - export IMAGE_REGISTRY="$BITBUCKET_REPO_FULL_NAME"  # Bitbucket Container Registry
          # Alternative registries (uncomment and configure as needed):
          # - export IMAGE_REGISTRY="your-registry.com/your-image"  # DockerHub
          # - export IMAGE_REGISTRY="your-account.dkr.ecr.us-west-2.amazonaws.com/your-image"  # AWS ECR
          # - export IMAGE_REGISTRY="gcr.io/your-project/your-image"  # Google GCR
          # Login to container registry
          - echo $DOCKER_PASSWORD | docker login -u $DOCKER_USERNAME --password-stdin
          # Alternative registry logins (uncomment as needed):
          # - echo $DOCKERHUB_TOKEN | docker login -u $DOCKERHUB_USERNAME --password-stdin
          # - aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com
          # - echo $GCR_JSON_KEY | docker login -u _json_key --password-stdin gcr.io
          # Validate configuration
          - dagster-cloud ci check --project-dir . --dagster-cloud-yaml-path dagster_cloud.yaml
          # Initialize build session
          - dagster-cloud ci init --project-dir . --dagster-cloud-yaml-path dagster_cloud.yaml --deployment {deployment_name}
          # Generate unique image tag
          - export IMAGE_TAG="$BITBUCKET_COMMIT-$BITBUCKET_BUILD_NUMBER"
          # Build and push Docker image
          - docker buildx create --use
          - docker buildx build --platform linux/amd64 --push --tag $IMAGE_REGISTRY:$IMAGE_TAG .
          # Set build output for each location
          - dagster-cloud ci set-build-output --location-name=main --image-tag=$IMAGE_TAG
          # Deploy to Dagster Cloud
          - dagster-cloud ci deploy
          # Update PR comment for branch deployments
          - dagster-cloud ci notify --project-dir=.
          # Generate summary
          - dagster-cloud ci status --output-format=markdown
        artifacts:
          - dagster-cloud-ci-results.xml

pipelines:
  branches:
    main:
      - step: *hybrid-deploy
    master:
      - step: *hybrid-deploy
  pull-requests:
    '**':
      - step: *hybrid-deploy
"""
    
    with open(workflow_path, 'w') as f:
        f.write(template_content)
    print(f"✅ Generated Bitbucket pipeline template for {deployment_type} deployment")

def setup_external_dbt_integration(project_dir, dbt_repo_url, dbt_repo_branch, dbt_project_path, deployment_type="serverless", container_registry=None):
    """Set up external dbt repository integration for CI/CD workflows.
    
    Args:
        project_dir: Project directory path
        dbt_repo_url: URL of the external dbt repository
        dbt_repo_branch: Branch to clone
        dbt_project_path: Path within the repo to the dbt project
        deployment_type: 'serverless' or 'hybrid'
        container_registry: Container registry URL (required for hybrid)
    """
    print(f"\n🔧 Setting up external dbt repository integration...")
    print(f"🎯 Deployment type: {deployment_type}")
    
    # Detect Git provider
    git_provider = None
    if "github.com" in dbt_repo_url:
        git_provider = "github"
    elif "gitlab.com" in dbt_repo_url:
        git_provider = "gitlab"
    elif "dev.azure.com" in dbt_repo_url or "visualstudio.com" in dbt_repo_url:
        git_provider = "azure"
    elif "bitbucket.org" in dbt_repo_url:
        git_provider = "bitbucket"
    else:
        print(f"⚠️  Unknown Git provider. Defaulting to GitHub workflow.")
        git_provider = "github"
    
    print(f"✅ Detected Git provider: {git_provider}")
    
    # For hybrid deployments, we need Dockerfile
    if deployment_type == "hybrid":
        # Update Dockerfile to clone dbt repository
        update_dockerfile_for_external_dbt(project_dir, dbt_repo_url, dbt_repo_branch, dbt_project_path)
    
    # Update CI/CD workflows based on deployment type
    if git_provider == "github":
        update_github_workflow_for_external_dbt(project_dir, dbt_repo_url, dbt_repo_branch, dbt_project_path, deployment_type, container_registry)
    elif git_provider == "gitlab":
        update_gitlab_ci_for_external_dbt(project_dir, dbt_repo_url, dbt_repo_branch, dbt_project_path, deployment_type, container_registry)
    elif git_provider == "azure":
        create_azure_pipeline_for_external_dbt(project_dir, dbt_repo_url, dbt_repo_branch, dbt_project_path, deployment_type, container_registry)
    elif git_provider == "bitbucket":
        create_bitbucket_pipeline_for_external_dbt(project_dir, dbt_repo_url, dbt_repo_branch, dbt_project_path, deployment_type, container_registry)
    
    # Update dbt component configuration
    update_dbt_component_for_external_repo(project_dir, dbt_project_path)
    
    print(f"✅ External dbt repository integration configured!")
    print(f"📋 Repository: {dbt_repo_url}")
    print(f"🌿 Branch: {dbt_repo_branch}")
    print(f"📁 Project path: {dbt_project_path}")
    print(f"🚀 Deployment: {deployment_type}")
    if deployment_type == "hybrid" and container_registry:
        print(f"📦 Container registry: {container_registry}")
    print(f"💡 Your dbt project will be cloned during CI/CD deployment")

def update_dockerfile_for_external_dbt(project_dir, dbt_repo_url, dbt_repo_branch, dbt_project_path):
    """Update Dockerfile to clone external dbt repository."""
    dockerfile_path = os.path.join(project_dir, "Dockerfile")
    
    if os.path.exists(dockerfile_path):
        with open(dockerfile_path, 'r') as f:
            dockerfile_content = f.read()
        
        # Add dbt repository cloning before the final CMD
        dbt_clone_section = f"""
# Clone external dbt repository
RUN git clone --branch {dbt_repo_branch} {dbt_repo_url} /tmp/dbt-repo && \\
    cp -r /tmp/dbt-repo/{dbt_project_path}/* /opt/dagster/app/transform/ && \\
    rm -rf /tmp/dbt-repo

# Install dbt dependencies and compile
WORKDIR /opt/dagster/app/transform
RUN dbt deps && dbt compile
WORKDIR /opt/dagster/app
"""
        
        # Insert before the final CMD line
        lines = dockerfile_content.split('\n')
        cmd_index = -1
        for i, line in enumerate(lines):
            if line.strip().startswith('CMD'):
                cmd_index = i
                break
        
        if cmd_index != -1:
            lines.insert(cmd_index, dbt_clone_section)
        else:
            lines.append(dbt_clone_section)
        
        with open(dockerfile_path, 'w') as f:
            f.write('\n'.join(lines))
        
        print(f"✅ Updated Dockerfile with external dbt repository cloning")
    else:
        print(f"⚠️  Dockerfile not found - you'll need to manually configure dbt repository cloning")

def update_github_workflow_for_external_dbt(project_dir, dbt_repo_url, dbt_repo_branch, dbt_project_path, deployment_type="serverless", container_registry=None):
    """Update GitHub Actions workflow for external dbt repository."""
    # Different workflow files for serverless vs hybrid
    if deployment_type == "serverless":
        workflow_path = os.path.join(project_dir, ".github", "workflows", "dagster-plus-deploy.yml")
    else:  # hybrid
        workflow_path = os.path.join(project_dir, ".github", "workflows", "dagster-cloud-deploy.yml")
    
    if os.path.exists(workflow_path):
        with open(workflow_path, 'r') as f:
            workflow_content = f.read()
        
        # Add dbt repository checkout step
        dbt_checkout_step = f"""
      - name: Checkout dbt repository
        uses: actions/checkout@v4
        with:
          repository: {dbt_repo_url.replace('https://github.com/', '').replace('.git', '')}
          ref: {dbt_repo_branch}
          path: dbt-repo
          
      - name: Copy dbt project
        run: |
          mkdir -p transform
          cp -r dbt-repo/{dbt_project_path}/* transform/
          
      - name: Install dbt dependencies
        run: |
          cd transform
          dbt deps
          dbt compile
"""
        
        # Insert after the main checkout step
        lines = workflow_content.split('\n')
        checkout_index = -1
        for i, line in enumerate(lines):
            if 'uses: actions/checkout@' in line and 'dbt-repo' not in line:
                checkout_index = i
                break
        
        if checkout_index != -1:
            # Find the end of the checkout step
            for j in range(checkout_index + 1, len(lines)):
                if lines[j].strip().startswith('- name:') or lines[j].strip().startswith('- uses:'):
                    lines.insert(j, dbt_checkout_step)
                    break
        
        # For hybrid deployments, uncomment and configure container registry
        if deployment_type == "hybrid" and container_registry:
            print(f"🔧 Configuring container registry for hybrid deployment...")
            
            # Uncomment registry login step and set registry
            for i, line in enumerate(lines):
                # Uncomment Docker login for the specific registry
                if container_registry == "DockerHub" and "# - name: Log in to DockerHub" in line:
                    lines[i] = line.replace("# ", "")
                    # Uncomment the next few lines
                    for j in range(i+1, min(i+10, len(lines))):
                        if lines[j].strip().startswith("#") and ("uses:" in lines[j] or "with:" in lines[j] or "username:" in lines[j] or "password:" in lines[j]):
                            lines[j] = lines[j].replace("# ", "", 1)
                        elif not lines[j].strip().startswith("#"):
                            break
                elif container_registry == "ECR" and "# - name: Configure AWS credentials" in line:
                    lines[i] = line.replace("# ", "")
                    for j in range(i+1, min(i+15, len(lines))):
                        if lines[j].strip().startswith("#"):
                            lines[j] = lines[j].replace("# ", "", 1)
                        elif not lines[j].strip().startswith("#"):
                            break
                elif container_registry == "GCR" and "# - name: Log in to GCR" in line:
                    lines[i] = line.replace("# ", "")
                    for j in range(i+1, min(i+10, len(lines))):
                        if lines[j].strip().startswith("#"):
                            lines[j] = lines[j].replace("# ", "", 1)
                        elif not lines[j].strip().startswith("#"):
                            break
            
            print(f"✅ Uncommented {container_registry} configuration in workflow")
        
        with open(workflow_path, 'w') as f:
            f.write('\n'.join(lines))
        
        workflow_type = "serverless" if deployment_type == "serverless" else "hybrid"
        print(f"✅ Updated GitHub Actions {workflow_type} workflow with external dbt repository")
    else:
        print(f"⚠️  GitHub workflow not found - you'll need to manually configure dbt repository checkout")

def update_gitlab_ci_for_external_dbt(project_dir, dbt_repo_url, dbt_repo_branch, dbt_project_path, deployment_type="serverless", container_registry=None):
    """Update GitLab CI for external dbt repository."""
    gitlab_ci_path = os.path.join(project_dir, ".gitlab-ci.yml")
    
    # If GitLab CI file doesn't exist, create it using the template
    if not os.path.exists(gitlab_ci_path):
        # Get organization and deployment from environment or prompt
        org_name = os.getenv('DAGSTER_CLOUD_ORGANIZATION', 'your-organization')
        deployment_name = os.getenv('DAGSTER_CLOUD_DEPLOYMENT', 'prod')
        
        generate_gitlab_ci_template(gitlab_ci_path, deployment_type, org_name, deployment_name)
    
    # Now modify the template to include external dbt repository cloning
    with open(gitlab_ci_path, 'r') as f:
        ci_content = f.read()
    
    # Add dbt repository cloning to before_script
    dbt_clone_script = f"""
  - git clone --branch {dbt_repo_branch} {dbt_repo_url} dbt-repo
  - mkdir -p transform
  - cp -r dbt-repo/{dbt_project_path}/* transform/
  - cd transform && pip install dbt-core && dbt deps && dbt compile && cd ..
"""
    
    # Add to before_script section
    if 'before_script:' in ci_content:
        ci_content = ci_content.replace('before_script:', f'before_script:{dbt_clone_script}')
    else:
        # Add before_script section
        lines = ci_content.split('\n')
        lines.insert(1, f'before_script:{dbt_clone_script}')
        ci_content = '\n'.join(lines)
    
    with open(gitlab_ci_path, 'w') as f:
        f.write(ci_content)
    
    print(f"✅ Updated GitLab CI with external dbt repository")

def create_azure_pipeline_for_external_dbt(project_dir, dbt_repo_url, dbt_repo_branch, dbt_project_path, deployment_type="serverless", container_registry=None):
    """Create Azure DevOps pipeline with external dbt repository."""
    pipeline_dir = os.path.join(project_dir, ".azure")
    os.makedirs(pipeline_dir, exist_ok=True)
    
    # Use the new template generation function
    pipeline_path = os.path.join(pipeline_dir, "azure-pipelines.yml")
    
    # Get organization and deployment from environment or prompt
    org_name = os.getenv('DAGSTER_CLOUD_ORGANIZATION', 'your-organization')
    deployment_name = os.getenv('DAGSTER_CLOUD_DEPLOYMENT', 'prod')
    
    generate_azure_pipeline_template(pipeline_path, deployment_type, org_name, deployment_name)
    
    # Now modify the template to include external dbt repository cloning
    with open(pipeline_path, 'r') as f:
        content = f.read()
    
    # Add dbt repository cloning step before the main deployment
    dbt_clone_step = f"""
    - script: |
        git clone --branch {dbt_repo_branch} {dbt_repo_url} dbt-repo
        mkdir -p transform
        cp -r dbt-repo/{dbt_project_path}/* transform/
        cd transform
        pip install dbt-core
        dbt deps
        dbt compile
        cd ..
      displayName: 'Clone and prepare external dbt repository'
"""
    
    # Insert the dbt clone step before the "Validate configuration" step
    content = content.replace(
        "- script: |\n        dagster-cloud ci check",
        dbt_clone_step + "\n    - script: |\n        dagster-cloud ci check"
    )
    
    with open(pipeline_path, 'w') as f:
        f.write(content)
    
    print(f"✅ Created Azure DevOps pipeline with external dbt repository")

def create_bitbucket_pipeline_for_external_dbt(project_dir, dbt_repo_url, dbt_repo_branch, dbt_project_path, deployment_type="serverless", container_registry=None):
    """Create Bitbucket pipeline with external dbt repository."""
    # Use the new template generation function
    pipeline_path = os.path.join(project_dir, "bitbucket-pipelines.yml")
    
    # Get organization and deployment from environment or prompt
    org_name = os.getenv('DAGSTER_CLOUD_ORGANIZATION', 'your-organization')
    deployment_name = os.getenv('DAGSTER_CLOUD_DEPLOYMENT', 'prod')
    
    generate_bitbucket_pipeline_template(pipeline_path, deployment_type, org_name, deployment_name)
    
    # Now modify the template to include external dbt repository cloning
    with open(pipeline_path, 'r') as f:
        content = f.read()
    
    # Add dbt repository cloning step before the main deployment
    dbt_clone_step = f"""          # Clone and prepare external dbt repository
          - git clone --branch {dbt_repo_branch} {dbt_repo_url} dbt-repo
          - mkdir -p transform
          - cp -r dbt-repo/{dbt_project_path}/* transform/
          - cd transform
          - pip install dbt-core
          - dbt deps
          - dbt compile
          - cd ..
"""
    
    # Insert the dbt clone step before the "Validate configuration" step
    content = content.replace(
        "          # Validate configuration",
        dbt_clone_step + "          # Validate configuration"
    )
    
    with open(pipeline_path, 'w') as f:
        f.write(content)
    
    print(f"✅ Created Bitbucket pipeline with external dbt repository")

def update_dbt_component_for_external_repo(project_dir, dbt_project_path):
    """Update dbt component configuration for external repository."""
    # Find defs.yaml files in the project
    defs_yaml_paths = []
    for root, dirs, files in os.walk(project_dir):
        if "defs.yaml" in files and ("dbt" in root.lower() or "transform" in root.lower()):
            defs_yaml_paths.append(os.path.join(root, "defs.yaml"))
    
    for defs_yaml_path in defs_yaml_paths:
        try:
            import yaml
            with open(defs_yaml_path, 'r') as f:
                defs_config = yaml.safe_load(f)
            
            # Update the project path to point to the cloned external repo
            if 'attributes' in defs_config and 'project' in defs_config['attributes']:
                defs_config['attributes']['project'] = "{{ project_root }}/transform"
            
            with open(defs_yaml_path, 'w') as f:
                yaml.safe_dump(defs_config, f, sort_keys=False)
            
            print(f"✅ Updated dbt component configuration: {defs_yaml_path}")
            
        except Exception as e:
            print(f"⚠️  Could not update {defs_yaml_path}: {e}")

def setup_integrations(project_dir, pkg_mgr):
    """Set up integrations (dbt, Fivetran, Airbyte, Power BI) for the project."""
    print(f"\n🔧 Integration Setup")
    print(f"🎯 Add modern data integrations to your Dagster project")
    
    integration_choice = choose(
        "Would you like to set up integrations?",
        [
            "Yes, set up integrations (dbt, Fivetran, Airbyte, Power BI)",
            "Skip integrations for now"
        ]
    )
    
    if integration_choice == 1:
        print(f"\n📋 Available integrations:")
        print(f"   • dbt: Transform data with SQL")
        print(f"   • Fivetran: Extract and load data from SaaS applications")
        print(f"   • Airbyte: Open-source data integration platform")
        print(f"   • Power BI: Business intelligence and analytics")
        print(f"   • Airlift: Migrate from Airflow to Dagster")
        
        # Set up each integration
        setup_dbt_integration(project_dir, pkg_mgr)
        
        # Add other integrations
        if choose("Set up Fivetran integration?", ["Yes", "No"]) == 1:
            setup_fivetran_integration(project_dir, pkg_mgr)
        
        if choose("Set up Airbyte integration?", ["Yes", "No"]) == 1:
            setup_airbyte_integration(project_dir, pkg_mgr)
        
        if choose("Set up Power BI integration?", ["Yes", "No"]) == 1:
            setup_powerbi_integration(project_dir, pkg_mgr)
        
        if choose("Set up Airlift (Airflow migration) integration?", ["Yes", "No"]) == 1:
            setup_airlift_integration(project_dir, pkg_mgr)
        
        print(f"\n✅ Integration setup completed!")
    else:
        print(f"⏭️  Skipping integrations - you can add them later")

def main():
    """Enhanced main onboarding function with goal-based workflow."""
    try:
        print("\n🚀 Starting Enhanced Dagster+ Cloud onboarding...")
        print("🎯 This script helps you set up Dagster projects with modern integrations")
        
        # Check virtual environment early and recommend if not in one
        venv_info = detect_virtual_environment()
        if not venv_info["in_venv"]:
            print(f"\n⚠️  Virtual Environment Recommendation")
            print(f"🐍 You're currently running this script outside of a virtual environment.")
            print(f"💡 For the best experience, we strongly recommend using a virtual environment because:")
            print(f"   • Prevents Python executable issues (like python3.9 not found)")
            print(f"   • Isolates dependencies and prevents conflicts")
            print(f"   • Ensures cleaner PEX builds for deployment")
            print(f"   • Follows Python development best practices")
            print(f"")
            
            venv_choice = choose(
                "How would you like to proceed?",
                [
                    "Create a virtual environment now and restart the script",
                    "Continue anyway (may encounter Python/dependency issues)",
                    "Exit to manually set up virtual environment (recommended)"
                ]
            )
            
            if venv_choice == 1:
                # Create virtual environment and provide restart instructions
                print(f"\n🔧 Creating virtual environment...")
                venv_name = "dagster-venv"
                
                try:
                    subprocess.run(["python3", "-m", "venv", venv_name], check=True)
                    print(f"✅ Created virtual environment: {venv_name}")
                    print(f"")
                    print(f"🎯 Next steps:")
                    print(f"   1. Activate the virtual environment:")
                    if platform.system() == "Windows":
                        print(f"      {venv_name}\\Scripts\\activate")
                    else:
                        print(f"      source {venv_name}/bin/activate")
                    print(f"   2. Re-run this script:")
                    print(f"      python3 {' '.join(sys.argv)}")
                    print(f"")
                    print(f"💡 The virtual environment will provide a clean, isolated Python environment.")
                    return
                except subprocess.CalledProcessError as e:
                    print(f"❌ Failed to create virtual environment: {e}")
                    print(f"💡 Please create one manually and restart the script.")
                    return
                    
            elif venv_choice == 2:
                print(f"\n⚠️  Continuing without virtual environment...")
                print(f"💡 If you encounter Python executable or dependency issues, consider using a venv.")
                print(f"")
            else:  # venv_choice == 3
                print(f"\n✅ Good choice! Please set up a virtual environment:")
                print(f"   1. Create: python3 -m venv dagster-venv")
                if platform.system() == "Windows":
                    print(f"   2. Activate: dagster-venv\\Scripts\\activate")
                else:
                    print(f"   2. Activate: source dagster-venv/bin/activate")
                print(f"   3. Re-run: python3 {' '.join(sys.argv)}")
                print(f"")
                print(f"💡 This will ensure the best deployment experience!")
                return
        else:
            print(f"\n✅ Running in virtual environment: {venv_info['venv_name']}")
            print(f"🎯 Great! This will ensure clean dependency management and deployment.")
        
        # Enhanced goal selection
        main_goal = choose(
            "What would you like to do?",
            [
                "Set up a new Dagster project for local development",
                "Set up a new Dagster project and deploy to Dagster+ Cloud",
                "Prepare existing Dagster project for Dagster+ (generate/fix required files)",
                "Install a Dagster+ agent (for existing projects)",
                "Deploy an existing Dagster project to Dagster+ Cloud"
            ]
        )
        
        # Get package manager preference early
        pkg_mgr = choose("Choose your Python package manager:", ["pip", "uv"])
        
        # Install Dagster for all goals
        install_dagster(pkg_mgr)
        
        project_dir = None
        
        # Handle different goals
        if main_goal == 3:  # Prepare existing project for Dagster+
            print(f"\n🔧 Preparing Dagster project for Dagster+ Cloud")
            print(f"💡 This will generate or fix all required files for deployment")
            
            # Ask for project location
            project_choice = choose(
                "Where is your Dagster project?",
                ["Current directory", "Specify different directory"]
            )
            
            if project_choice == 1:
                project_dir = os.getcwd()
            else:
                project_dir = input("Enter the path to your Dagster project: ").strip()
                if not project_dir or not os.path.exists(project_dir):
                    print(f"❌ Invalid project directory: {project_dir}")
                    return
                project_dir = os.path.abspath(project_dir)
            
            print(f"📁 Using project directory: {project_dir}")
            
            # Check if this is a monorepo
            print(f"\n🔍 Analyzing project structure...")
            is_monorepo, projects = detect_monorepo_structure(project_dir)
            
            if is_monorepo:
                print(f"\n📁 Detected monorepo structure!")
                print(f"Found {len(projects)} Dagster projects:")
                for i, project in enumerate(projects, 1):
                    components_indicator = "🧩 Components" if project['is_components'] else "📄 Traditional"
                    print(f"   {i}. {project['name']} ({project['relative_path']}) - {components_indicator}")
                
                print(f"\n💡 All projects will be prepared for the same deployment type")
                
                # Ask about deployment type (applies to all projects)
                print(f"\n🚀 Deployment Type")
                deploy_type_choice = choose(
                    "What type of Dagster+ deployment will you use for all projects?",
                    ["Serverless", "Hybrid"]
                )
                
                deployment_type = "serverless" if deploy_type_choice == 1 else "hybrid"
                
                # Prepare each project
                print(f"\n📝 Preparing all projects for {deployment_type} deployment...")
                for project in projects:
                    print(f"\n🔧 Preparing {project['name']}...")
                    ensure_dagster_project_files(project['path'])
                
                # Generate shared dagster_cloud.yaml
                print(f"\n📄 Generating shared dagster_cloud.yaml...")
                dagster_cloud_path = update_shared_dagster_cloud_yaml(project_dir, projects, deployment_type)
                
                print(f"\n✅ Monorepo preparation completed!")
                print(f"📁 Root directory: {project_dir}")
                print(f"📄 Shared config: {dagster_cloud_path}")
                print(f"🎯 Projects prepared: {', '.join([p['name'] for p in projects])}")
                
            else:
                # Single project - existing behavior
                print(f"📁 Single Dagster project detected")
                
                # Ask about deployment type to generate appropriate files
                print(f"\n🚀 Deployment Type")
                deploy_type_choice = choose(
                    "What type of Dagster+ deployment will you use?",
                    ["Serverless", "Hybrid"]
                )
                
                deployment_type = "serverless" if deploy_type_choice == 1 else "hybrid"
                
                # Generate/fix all required files
                print(f"\n📝 Generating/fixing Dagster+ configuration files...")
                ensure_dagster_project_files(project_dir)
            
            # Generate appropriate CI/CD workflow
            print(f"\n🔧 Setting up CI/CD workflow for {deployment_type} deployment...")
            
            # Initialize workflow_file variable
            workflow_file = None
            
            # Detect Git provider
            if os.path.exists(os.path.join(project_dir, ".git")):
                # Check for GitHub
                git_config_path = os.path.join(project_dir, ".git", "config")
                git_provider = None
                
                if os.path.exists(git_config_path):
                    with open(git_config_path, 'r') as f:
                        git_config = f.read()
                        if "github.com" in git_config:
                            git_provider = "github"
                        elif "gitlab.com" in git_config:
                            git_provider = "gitlab"
                        elif "dev.azure.com" in git_config or "visualstudio.com" in git_config:
                            git_provider = "azure"
                        elif "bitbucket.org" in git_config:
                            git_provider = "bitbucket"
                
                if not git_provider:
                    git_provider_choice = choose(
                        "Which Git provider are you using?",
                        ["GitHub", "GitLab", "Azure DevOps", "Bitbucket", "Other/None"]
                    )
                    git_provider = ["github", "gitlab", "azure", "bitbucket", None][git_provider_choice - 1]
                
                if git_provider:
                    print(f"✅ Detected Git provider: {git_provider}")
                    
                    # Generate appropriate workflow file
                    workflow_dir = None
                    workflow_file = None
                    
                    if git_provider == "github":
                        workflow_dir = os.path.join(project_dir, ".github", "workflows")
                        if deployment_type == "serverless":
                            workflow_file = "dagster-plus-deploy.yml"
                        else:
                            workflow_file = "dagster-cloud-deploy.yml"
                    elif git_provider == "gitlab":
                        workflow_file = ".gitlab-ci.yml"
                    elif git_provider == "azure":
                        workflow_dir = os.path.join(project_dir, ".azure")
                        workflow_file = "azure-pipelines.yml"
                    elif git_provider == "bitbucket":
                        workflow_file = "bitbucket-pipelines.yml"
                    
                    if workflow_file:
                        if workflow_dir:
                            os.makedirs(workflow_dir, exist_ok=True)
                            workflow_path = os.path.join(workflow_dir, workflow_file)
                        else:
                            workflow_path = os.path.join(project_dir, workflow_file)
                        
                        if not os.path.exists(workflow_path):
                            print(f"📄 Generating {workflow_file}...")
                            # Clone the appropriate quickstart to get the workflow file
                            import tempfile
                            with tempfile.TemporaryDirectory() as temp_dir:
                                quickstart_repo = SERVERLESS_QUICKSTART_REPO if deployment_type == "serverless" else HYBRID_QUICKSTART_REPO
                                clone_result = subprocess.run(
                                    ["git", "clone", "--depth", "1", quickstart_repo, temp_dir],
                                    capture_output=True,
                                    text=True
                                )
                                
                                if clone_result.returncode == 0:
                                    # Copy the workflow file from the quickstart
                                    if git_provider == "github":
                                        source_workflow = os.path.join(temp_dir, ".github", "workflows", workflow_file)
                                        if os.path.exists(source_workflow):
                                            shutil.copy(source_workflow, workflow_path)
                                            print(f"✅ Generated {workflow_file}")
                                        else:
                                            print(f"⚠️  Could not find workflow file in quickstart")
                                    # For other providers, generate template
                                    elif git_provider == "gitlab":
                                        generate_gitlab_ci_template(workflow_path, deployment_type, org_name, deployment_name)
                                    elif git_provider == "azure":
                                        generate_azure_pipeline_template(workflow_path, deployment_type, org_name, deployment_name)
                                    elif git_provider == "bitbucket":
                                        generate_bitbucket_pipeline_template(workflow_path, deployment_type, org_name, deployment_name)
                                else:
                                    print(f"⚠️  Could not clone quickstart - you'll need to create the workflow manually")
                        else:
                            print(f"✅ {workflow_file} already exists")
            else:
                print(f"⚠️  No Git repository detected")
                print(f"💡 Initialize a Git repository to enable CI/CD workflow generation:")
                print(f"   1. git init")
                print(f"   2. git remote add origin <your-repo-url>")
                print(f"   3. Re-run this script to generate CI/CD workflows")
            
            # For hybrid, ask about container registry
            if deployment_type == "hybrid":
                print(f"\n📦 Container Registry Configuration")
                registry_choice = choose(
                    "Which container registry will you use?",
                    ["DockerHub", "Amazon ECR", "Google GCR", "Other/Skip"]
                )
                
                if registry_choice < 4:
                    container_registry = ["DockerHub", "ECR", "GCR"][registry_choice - 1]
                    print(f"💡 Remember to uncomment the {container_registry} login section in your workflow file")
                    print(f"💡 And set the appropriate secrets in your repository settings")
            
            print(f"\n✅ Dagster+ preparation completed!")
            print(f"📁 Project directory: {project_dir}")
            print(f"🚀 Deployment type: {deployment_type}")
            print(f"")
            print(f"📋 Generated/Fixed files:")
            print(f"   • pyproject.toml - Project configuration")
            print(f"   • dagster_cloud.yaml - Dagster+ deployment config")
            if os.path.exists(os.path.join(project_dir, "Dockerfile")):
                print(f"   • Dockerfile - Container image definition")
            if workflow_file:
                print(f"   • {workflow_file} - CI/CD workflow")
            print(f"")
            print(f"🎯 Next steps:")
            print(f"   1. Review the generated files")
            print(f"   2. Set up secrets in your repository (API tokens, etc.)")
            print(f"   3. Commit and push to trigger deployment")
            print(f"   4. Or deploy manually using option 5")
            
            return
        
        elif main_goal in [1, 2]:  # New project setup
            print(f"\n📁 Project Setup Phase")
            
            if main_goal == 1:
                print("🎯 Setting up for local development...")
            else:
                print("🎯 Setting up for cloud deployment...")
            
            # Choose project source
            source_type, repos = choose_project_source()
            
            if source_type == "new_project":
                # Create new empty Dagster project
                project_dir = create_new_dagster_project(pkg_mgr)
                if not project_dir:
                    print("❌ Failed to create new project")
                    return
                
                print(f"✅ Successfully created new Dagster project!")
                print(f"📁 Project directory: {project_dir}")
                print(f"")
                print(f"🎯 Your project has a clean Components-compatible structure:")
                print(f"   • pyproject.toml - Project configuration")
                print(f"   • definitions.py - Main definitions module")
                print(f"   • definitions/defs/ - Components directory")
                print(f"")
                print(f"💡 This is the perfect starting point for adding integrations!")
            
            elif source_type == "quickstart":
                # Original quickstart logic
                if main_goal == 2:
                    deploy_type = choose("Choose deployment type:", ["Serverless", "Hybrid"])
                    quickstart_repo = SERVERLESS_QUICKSTART_REPO if deploy_type == 1 else HYBRID_QUICKSTART_REPO
                    project_name = "dagster-cloud-serverless-quickstart" if deploy_type == 1 else "dagster-cloud-hybrid-quickstart"
                else:  # Local dev - use serverless as template
                    quickstart_repo = SERVERLESS_QUICKSTART_REPO
                    project_name = "dagster-cloud-serverless-quickstart"
                
                # Clone quickstart
                if os.path.exists(project_name):
                    overwrite = choose(
                        f"Directory '{project_name}' already exists. What would you like to do?",
                        ["Overwrite it", "Use existing directory", "Cancel"]
                    )
                    
                    if overwrite == 1:
                        shutil.rmtree(project_name)
                    elif overwrite == 3:
                        return
                
                try:
                    print(f"📥 Cloning {project_name}...")
                    subprocess.run(["git", "clone", quickstart_repo], check=True)
                    project_dir = os.path.abspath(project_name)
                    print(f"✅ Successfully cloned quickstart project")
                    
                except subprocess.CalledProcessError as e:
                    print(f"❌ Failed to clone quickstart: {e}")
                    return
                except Exception as e:
                    print(f"❌ Error cloning quickstart: {e}")
                    return
            
            elif source_type in ["eric_examples", "custom_github"]:
                # Repository selection and cloning
                selected_repo = select_repository(repos)
                if selected_repo:
                    project_dir = clone_selected_repository(selected_repo)
                    if not project_dir:
                        print("❌ Failed to clone repository")
                        return
                    
                    # Ensure the cloned project has all necessary Dagster configuration files
                    ensure_dagster_project_files(project_dir)
                else:
                    print("❌ No repository selected")
                    return
            
            else:  # current_dir
                project_dir = os.getcwd()
                print(f"📁 Using current directory: {project_dir}")
                
                # Ensure the current directory has all necessary Dagster configuration files
                ensure_dagster_project_files(project_dir)
        
        # Set up integrations for local development and deployment projects
        if main_goal in [1, 2] and project_dir:
            setup_integrations(project_dir, pkg_mgr)
        
        elif main_goal == 5:  # Deploy existing project
            print(f"\n📁 Existing Project Setup")
            
            project_choice = choose(
                "Where is your Dagster project?",
                ["Current directory", "Specify different directory"]
            )
            
            if project_choice == 1:
                project_dir = os.getcwd()
            else:
                project_dir = input("Enter the path to your Dagster project: ").strip()
                if not project_dir or not os.path.exists(project_dir):
                    print(f"❌ Invalid project directory: {project_dir}")
                    return
                project_dir = os.path.abspath(project_dir)
            
            print(f"📁 Using project directory: {project_dir}")
            
            # Ensure the existing project has all necessary Dagster configuration files
            ensure_dagster_project_files(project_dir)
            
            # Offer integrations for existing projects too
            setup_integrations(project_dir, pkg_mgr)
        
        # Continue with deployment if needed
        if main_goal in [2, 5]:  # Deploy to cloud
            print(f"\n🔑 Dagster+ Cloud credentials needed for deployment...")
            org_name, api_token = get_organization_and_token()
            if not org_name or not api_token:
                return
            
            deployment_name = input("Enter deployment name (or press Enter for default 'prod'): ").strip()
            if not deployment_name:
                deployment_name = "prod"
            
            # Choose deployment type if not already chosen
            if 'deploy_type' not in locals():
                deploy_type = choose(
                    "What type of deployment do you want to set up?",
                    [
                        "Serverless (recommended for most users)",
                        "Hybrid (self-hosted agent)"
                    ]
                )
            
            # Validate token type compatibility with deployment type
            _, token_type, _, _ = validate_and_extract_token_info(api_token)
            
            if deploy_type == 1:  # Serverless
                if token_type == "agent":
                    print("⚠️  You're using an agent token for serverless deployment.")
                    print("💡 Agent tokens work for serverless, but user tokens (API tokens) are recommended.")
                    print("💡 User tokens provide better security isolation for serverless deployments.")
                    print("💡 To create a user token:")
                    print("   1. Go to your Dagster+ organization settings")
                    print("   2. Navigate to 'Tokens' section") 
                    print("   3. Click 'Create User Token'")
                    print("   4. Copy the token that starts with 'user:'")
            elif deploy_type == 2:  # Hybrid
                if token_type == "user":
                    print("❌ User tokens cannot be used for hybrid agent setup.")
                    print("💡 Please use an agent token for hybrid deployments.")
                    print("💡 To create an agent token:")
                    print("   1. Go to your Dagster+ organization settings")
                    print("   2. Navigate to 'Tokens' section")
                    print("   3. Click 'Create Agent Token'")
                    print("   4. Copy the token that starts with 'agent:'")
                    return
            
            # Continue with serverless deployment
            if deploy_type == 1:  # Serverless
                print(f"\n🚀 Proceeding with serverless deployment...")
                
                # Choose build type
                build_type = choose(
                    "Choose your serverless deployment method:",
                    [
                        "PEX (Python executable - faster, smaller)",
                        "Docker (containerized - more flexible)"
                    ]
                )
                
                # Get deployment details
                project_name = os.path.basename(os.path.abspath(project_dir))
                code_location_name = input(f"Enter code location name [{project_name}]: ").strip() or project_name
                
                # Detect package name from project structure
                # Priority 1: Get from pyproject.toml (most reliable)
                suggested_package = None
                pyproject_path = os.path.join(project_dir, "pyproject.toml")
                if os.path.exists(pyproject_path):
                    try:
                        import re
                        with open(pyproject_path, 'r') as f:
                            pyproject_content = f.read()
                        
                        # Try to extract root_module from [tool.dg.project]
                        root_module_match = re.search(r'root_module\s*=\s*["\']([^"\']+)["\']', pyproject_content)
                        if root_module_match:
                            suggested_package = root_module_match.group(1)
                            print(f"💡 Detected package from pyproject.toml: {suggested_package}")
                    except Exception as e:
                        print(f"⚠️  Could not parse pyproject.toml: {e}")
                
                # Priority 2: Check for flat definitions.py
                if not suggested_package and os.path.exists(os.path.join(project_dir, "definitions.py")):
                    suggested_package = "definitions"
                
                # Priority 3: Check src layout
                if not suggested_package and os.path.exists(os.path.join(project_dir, "src")):
                    src_dir = os.path.join(project_dir, "src")
                    modules = [d for d in os.listdir(src_dir) 
                              if os.path.isdir(os.path.join(src_dir, d)) 
                              and not d.startswith('.') 
                              and not d.startswith('_')]
                    
                    if len(modules) == 1:
                        suggested_package = f"{modules[0]}.definitions"
                        print(f"💡 Detected package from src/ directory: {suggested_package}")
                    elif len(modules) > 1:
                        # Try to find the one with definitions
                        for mod in modules:
                            if os.path.exists(os.path.join(src_dir, mod, "definitions.py")) or \
                               os.path.exists(os.path.join(src_dir, mod, "definitions")):
                                suggested_package = f"{mod}.definitions"
                                print(f"💡 Detected package with definitions: {suggested_package}")
                                break
                
                # Priority 4: Fallback to sanitized project name
                if not suggested_package:
                    # Replace hyphens with underscores (Python module naming requirement)
                    sanitized_name = project_name.replace('-', '_').replace(' ', '_')
                    suggested_package = f"{sanitized_name}.definitions"
                    print(f"💡 Using sanitized project name: {suggested_package}")
                
                package_name = input(f"Enter package name [{suggested_package}]: ").strip() or suggested_package
                
                # Validate that package_name doesn't have hyphens
                if '-' in package_name:
                    print(f"⚠️  Package name '{package_name}' contains hyphens, which are invalid in Python module names")
                    sanitized = package_name.replace('-', '_')
                    print(f"💡 Auto-correcting to: {sanitized}")
                    package_name = sanitized
                
                # Detect if this is a Components project and determine CLI parameters
                working_dir = "./src" if os.path.exists("src") else "."
                is_components, cli_param_type, cli_param_value = detect_definitions_type(project_dir, package_name, working_dir)
                
                if is_components:
                    print(f"✅ Detected Components project - will use --{cli_param_type} {cli_param_value}")
                else:
                    print(f"✅ Detected standard project - will use --{cli_param_type} {cli_param_value}")
                
                # Update dagster_cloud.yaml with the correct configuration
                update_dagster_cloud_yaml_for_components(project_dir, package_name, working_dir, is_components, cli_param_type, cli_param_value)
                
                # Detect the best available Python version for PEX (prefer newer versions)
                current_version = f"{sys.version_info.major}.{sys.version_info.minor}"
                
                # Check for newer Python versions that support modern syntax (3.10+)
                import shutil
                available_pythons = []
                
                # Check common Python version locations
                for version in ["3.12", "3.11", "3.10", current_version]:
                    for python_path in [f"python{version}", f"/opt/homebrew/bin/python{version}", f"/usr/local/bin/python{version}"]:
                        if shutil.which(python_path):
                            available_pythons.append((version, python_path))
                            break
                
                # Use the newest available version (list is sorted newest first)
                if available_pythons:
                    python_version, python_path = available_pythons[0]
                    python_executable = f"python{python_version}"
                    
                    if python_version != current_version:
                        print(f"🐍 Detected newer Python version: {python_version} (current: {current_version})")
                        print(f"💡 Using {python_path} for deployment (supports modern Python syntax)")
                    else:
                        print(f"🐍 Using current Python version: {python_version}")
                else:
                    # Fallback to current version
                    python_version = current_version
                    python_executable = f"python{python_version}"
                    print(f"🐍 Using current Python version: {python_version}")
                
                # Check if we're in a virtual environment (should resolve most Python issues)
                venv_info = detect_virtual_environment()
                
                # CRITICAL: Check if venv has pip (uv venvs often don't)
                if venv_info["in_venv"]:
                    print(f"🔍 Checking virtual environment for pip...")
                    pip_check = subprocess.run(
                        [sys.executable, "-m", "pip", "--version"],
                        capture_output=True,
                        text=True
                    )
                    
                    if pip_check.returncode != 0:
                        print(f"⚠️  Virtual environment is missing pip!")
                        print(f"💡 This is common with uv-created venvs")
                        print(f"💡 The PEX builder needs 'pip' installed (it hardcodes 'python -m pip' calls)")
                        print(f"🔧 Installing pip in virtual environment...")
                        
                        try:
                            # Check if uv is available to install pip faster
                            uv_available = shutil.which("uv") is not None
                            
                            if uv_available:
                                print(f"🚀 Using uv to install pip (faster)...")
                                # Use uv pip to install pip into the venv
                                uv_pip_result = subprocess.run(
                                    ["uv", "pip", "install", "--python", sys.executable, "pip"],
                                    capture_output=True,
                                    text=True
                                )
                                
                                if uv_pip_result.returncode == 0:
                                    print(f"✅ Successfully installed pip using uv")
                                else:
                                    print(f"⚠️  uv pip install failed, trying ensurepip...")
                                    uv_available = False  # Fall back to ensurepip
                            
                            if not uv_available:
                                # Install pip using ensurepip
                                print(f"🔧 Using ensurepip to install pip...")
                                ensurepip_result = subprocess.run(
                                    [sys.executable, "-m", "ensurepip", "--upgrade"],
                                    capture_output=True,
                                    text=True
                                )
                                
                                if ensurepip_result.returncode == 0:
                                    print(f"✅ Successfully installed pip using ensurepip")
                                else:
                                    print(f"⚠️  ensurepip failed, trying get-pip.py...")
                                    # Alternative: use get-pip.py
                                    import urllib.request
                                    get_pip_url = "https://bootstrap.pypa.io/get-pip.py"
                                    get_pip_path = "/tmp/get-pip.py"
                                    
                                    print(f"📥 Downloading get-pip.py...")
                                    urllib.request.urlretrieve(get_pip_url, get_pip_path)
                                    
                                    pip_install_result = subprocess.run(
                                        [sys.executable, get_pip_path],
                                        capture_output=True,
                                        text=True
                                    )
                                    
                                    if pip_install_result.returncode == 0:
                                        print(f"✅ Successfully installed pip using get-pip.py")
                                    else:
                                        print(f"❌ Failed to install pip!")
                                        print(f"💡 The PEX builder requires 'pip' to be installed")
                                        print(f"   Option 1: Manually run: uv pip install --python .venv/bin/python pip")
                                        print(f"   Option 2: Recreate venv: python3 -m venv .venv")
                                        print(f"   Option 3: Choose Docker deployment (doesn't need pip)")
                                        return
                        except Exception as e:
                            print(f"❌ Failed to install pip: {e}")
                            print(f"💡 Please install pip manually or use Docker deployment")
                            print(f"   Manual fix: uv pip install --python .venv/bin/python pip")
                            return
                    else:
                        print(f"✅ Virtual environment has pip installed")
                
                # Set up environment for deployment
                env = os.environ.copy()
                env["DAGSTER_CLOUD_API_TOKEN"] = api_token
                python_symlink_created = False
                
                # Check if the specific Python version executable exists
                if not shutil.which(python_executable):
                    print(f"⚠️  {python_executable} not found in PATH, creating temporary symlink...")
                    
                    # Priority 1: Use the detected python_path from our version detection
                    # Priority 2: If in venv, use the venv's Python (it's the right version)
                    # Priority 3: Fall back to alternatives
                    available_python = None
                    
                    if 'python_path' in locals() and python_path:
                        available_python = python_path
                        print(f"💡 Using detected Python: {python_path}")
                    elif venv_info["in_venv"] and venv_info["venv_path"]:
                        # Use the venv's Python directly - it matches the version we want
                        venv_python = get_virtual_env_python(venv_info["venv_path"])
                        if os.path.exists(venv_python):
                            available_python = venv_python
                            print(f"💡 Using virtual environment Python: {venv_python}")
                        else:
                            print(f"⚠️  Venv Python not found at {venv_python}")
                    
                    # Fallback to alternatives if still not found
                    if not available_python:
                        alternatives = ["python3", "python", f"python{sys.version_info.major}"]
                        for alt in alternatives:
                            alt_path = shutil.which(alt)
                            if alt_path:
                                available_python = alt_path
                                print(f"💡 Using fallback Python: {alt_path}")
                                break
                    
                    if available_python:
                        # Create a temporary symlink
                        symlink_path = f"/tmp/{python_executable}"
                        
                        # Remove old symlink if it exists
                        if os.path.exists(symlink_path) or os.path.islink(symlink_path):
                            try:
                                os.remove(symlink_path)
                            except Exception:
                                pass
                        
                        os.symlink(available_python, symlink_path)
                        
                        # Add /tmp to PATH for this deployment
                        env["PATH"] = f"/tmp:{env.get('PATH', '')}"
                        python_symlink_created = True
                        
                        print(f"✅ Created temporary symlink: {symlink_path} -> {available_python}")
                    else:
                        print(f"❌ No suitable Python executable found")
                        print(f"💡 Consider running this script in a virtual environment")
                        return
                else:
                    print(f"✅ Found {python_executable} - ready for PEX deployment")
                
                # Change to project directory for deployment
                original_dir = os.getcwd()
                os.chdir(project_dir)
                
                try:
                    if build_type == 1:  # PEX deployment
                        print(f"🚀 Deploying serverless Python executable (PEX)...")
                        
                        # Check if src layout
                        working_dir = "./src" if os.path.exists("src") else "."
                        
                        deploy_cmd = [
                            "dagster-cloud", "serverless", "deploy-python-executable", 
                            ".",  # Current directory (project root)
                            "--organization", org_name,
                            "--deployment", deployment_name,
                            "--location-name", code_location_name,
                            f"--{cli_param_type}", cli_param_value,
                            "--python-version", python_version
                        ]
                        
                        if working_dir != ".":
                            deploy_cmd.extend(["--working-directory", working_dir])
                            
                    else:  # Docker deployment
                        print(f"🐳 Deploying serverless Docker image...")
                        
                        # Generate Dockerfile if it doesn't exist
                        dockerfile_path = os.path.join(project_dir, "Dockerfile")
                        if not os.path.exists(dockerfile_path):
                            print(f"📄 Generating Dockerfile...")
                            generate_dockerfile(project_dir, package_name, python_version)
                        else:
                            print(f"✅ Using existing Dockerfile")
                        
                        # Check if Docker is available and running
                        if not has_cmd("docker"):
                            print(f"❌ Docker not found but required for Docker deployment.")
                            print(f"💡 Please install Docker: https://docs.docker.com/get-docker/")
                            return
                        
                        # Start Docker daemon if needed
                        start_docker_daemon()
                        
                        # Build Docker image locally first
                        image_name = f"{org_name}-{deployment_name}-{code_location_name}".lower()
                        print(f"🔨 Building Docker image: {image_name}...")
                        
                        build_result = subprocess.run([
                            "docker", "build", 
                            "-t", image_name,
                            "."
                        ], capture_output=True, text=True)
                        
                        if build_result.returncode != 0:
                            print(f"❌ Docker build failed!")
                            print(f"Error: {build_result.stderr}")
                            return
                        
                        print(f"✅ Docker image built successfully!")
                        
                        # For src-layout projects, specify the working directory inside the container
                        container_working_dir = "/opt/dagster/app/src" if os.path.exists("src") else "/opt/dagster/app"
                        
                        deploy_cmd = [
                            "dagster-cloud", "serverless", "deploy",
                            ".",  # Source directory
                            "--organization", org_name,
                            "--deployment", deployment_name,
                            "--location-name", code_location_name,
                            f"--{cli_param_type}", cli_param_value,
                            "--working-directory", container_working_dir
                        ]
                    
                    print(f"Running: {' '.join(deploy_cmd)}")
                    
                    deploy_result = subprocess.run(deploy_cmd, capture_output=True, text=True, env=env)
                    
                    if deploy_result.returncode == 0:
                        print(f"✅ Deployment successful!")
                        print(f"🎯 Your code location '{code_location_name}' is now deployed to Dagster+ Cloud")
                        print(f"💡 You can view it at: https://cloud.dagster.io/{org_name}/{deployment_name}")
                        print(f"")
                        print(f"🔄 To redeploy after making code changes, run:")
                        if build_type == 1:  # PEX deployment
                            print(f"   dagster-cloud serverless deploy-python-executable . \\")
                            print(f"     --organization {org_name} \\")
                            print(f"     --deployment {deployment_name} \\")
                            print(f"     --location-name {code_location_name} \\")
                            print(f"     --{cli_param_type} {cli_param_value} \\")
                            print(f"     --python-version {python_version}")
                        else:  # Docker deployment
                            print(f"   dagster-cloud serverless deploy . \\")
                            print(f"     --organization {org_name} \\")
                            print(f"     --deployment {deployment_name} \\")
                            print(f"     --location-name {code_location_name} \\")
                            print(f"     --{cli_param_type} {cli_param_value} \\")
                            print(f"     --working-directory {container_working_dir}")
                    else:
                        print(f"❌ Deployment failed!")
                        print(f"Error output: {deploy_result.stderr}")
                        if deploy_result.stdout:
                            print(f"Command output: {deploy_result.stdout}")
                        
                        # Enhanced error handling
                        if "dagster_cloud package dependency was expected but not found" in deploy_result.stderr:
                            print(f"\n💡 Missing dagster-cloud dependency!")
                            print(f"   The project needs 'dagster-cloud' in its dependencies for deployment.")
                            print(f"   Add 'dagster-cloud' to requirements.txt or pyproject.toml and try again.")
                        elif deploy_result.stderr:
                            handle_deployment_error(deploy_result.stderr, deployment_name, org_name)
                            
                finally:
                    os.chdir(original_dir)
                    
                    # Clean up temporary symlink if created
                    if python_symlink_created and 'temp_dir' in locals():
                        try:
                            import shutil
                            shutil.rmtree(temp_dir)
                            print(f"🧹 Cleaned up temporary Python symlink")
                        except Exception as e:
                            print(f"⚠️  Could not clean up temporary directory: {e}")
                    
            elif deploy_type == 2:  # Hybrid deployment
                print(f"\n🔧 Hybrid deployment setup...")
                print(f"💡 Hybrid deployments require Docker images and container registry")
                print(f"💡 Direct deployment to hybrid is not supported - use CI/CD instead")
                print(f"")
                print(f"📋 Next steps for hybrid deployment:")
                print(f"   1. Set up CI/CD workflow (GitHub Actions, GitLab CI, etc.)")
                print(f"   2. Configure container registry (DockerHub, ECR, GCR)")
                print(f"   3. Push your code to trigger CI/CD build")
                print(f"   4. Set up a hybrid agent to execute the deployed code")
                print(f"")
                print(f"💡 To set up CI/CD workflow:")
                print(f"   • Use option 3 (Prepare existing project) to generate workflows")
                print(f"   • Or manually configure CI/CD with container registry")
                print(f"")
                print(f"💡 To set up hybrid agent:")
                print(f"   • Use option 4 (Install agent) in this script")
                print(f"   • Or use the Dagster+ UI to configure agents")
        
        elif main_goal == 4:  # Agent installation only
            print(f"\n🔑 Dagster+ Cloud credentials needed for agent setup...")
            org_name, api_token = get_organization_and_token()
            if not org_name or not api_token:
                return
            
            # Validate token type
            _, token_type, _, _ = validate_and_extract_token_info(api_token)
            if token_type == "user":
                print("❌ User tokens cannot be used for agent installation.")
                print("💡 Please use an agent token for agent setup.")
                print("💡 To create an agent token:")
                print("   1. Go to your Dagster+ organization settings")
                print("   2. Navigate to 'Tokens' section")
                print("   3. Click 'Create Agent Token'")
                print("   4. Copy the token that starts with 'agent:'")
                return
            
            deployment_name = input("Enter deployment name (or press Enter for default 'prod'): ").strip()
            if not deployment_name:
                deployment_name = "prod"
            
            print(f"\n🤖 Agent Installation Setup")
            print(f"💡 Dagster+ agents run your code in your infrastructure")
            print(f"")
            
            agent_type = choose(
                "Which type of agent would you like to set up?",
                [
                    "Local agent (runs on this machine - good for testing)",
                    "Kubernetes agent (Helm chart deployment)",
                    "Amazon ECS agent (CloudFormation deployment)",
                    "Docker agent (runs in Docker container)"
                ]
            )
            
            if agent_type == 1:  # Local agent
                print(f"\n💻 Setting up local Dagster+ agent...")
                print(f"💡 This will run the agent on your local machine")
                print(f"")
                
                # Install dagster-cloud if not already installed
                print(f"📦 Ensuring dagster-cloud is installed...")
                if pkg_mgr == 2:  # uv
                    subprocess.run(["uv", "pip", "install", "dagster-cloud"], check=False)
                else:  # pip
                    install_python_packages(["dagster-cloud"])
                
                print(f"✅ dagster-cloud installed")
                print(f"")
                print(f"🚀 To start the local agent, run:")
                print(f"")
                print(f"   dagster-cloud agent run --agent-token \"{api_token}\" --deployment {deployment_name}")
                print(f"")
                print(f"💡 The agent will run in the foreground. Press Ctrl+C to stop.")
                print(f"")
                
                run_now = choose(
                    "Would you like to start the agent now?",
                    ["Yes, start the agent", "No, I'll start it manually"]
                )
                
                if run_now == 1:
                    agent_cmd = [
                        "dagster-cloud", "agent", "run",
                        "--agent-token", api_token,
                        "--deployment", deployment_name
                    ]
                    
                    print(f"\n🚀 Starting agent...")
                    print(f"💡 Press Ctrl+C to stop the agent")
                    print(f"")
                    try:
                        subprocess.run(agent_cmd)
                    except KeyboardInterrupt:
                        print(f"\n\n🛑 Agent stopped")
            
            elif agent_type == 2:  # Kubernetes
                print(f"\n☸️  Setting up Kubernetes agent with Helm...")
                print(f"💡 This works for both local (Minikube, Kind, k3s) and cloud K8s clusters")
                print(f"")
                print(f"📋 Prerequisites:")
                print(f"   • kubectl configured and connected to your cluster")
                print(f"   • Helm 3 installed")
                print(f"   • Appropriate RBAC permissions")
                print(f"")
                
                # Check if helm is installed
                if not has_cmd("helm"):
                    print(f"❌ Helm not found. Please install Helm first:")
                    print(f"   https://helm.sh/docs/intro/install/")
                    return
                
                if not has_cmd("kubectl"):
                    print(f"❌ kubectl not found. Please install kubectl first:")
                    print(f"   https://kubernetes.io/docs/tasks/tools/")
                    return
                
                print(f"✅ Helm and kubectl found")
                print(f"")
                
                # Check cluster connection and handle different scenarios
                cluster_context = None
                cluster_connected = False
                
                try:
                    # First check if we can connect to any cluster
                    result = subprocess.run(["kubectl", "cluster-info"], capture_output=True, text=True)
                    if result.returncode == 0:
                        cluster_connected = True
                        # Get current context
                        context_result = subprocess.run(["kubectl", "config", "current-context"], capture_output=True, text=True)
                        if context_result.returncode == 0:
                            cluster_context = context_result.stdout.strip()
                            print(f"✅ Connected to cluster")
                            print(f"📋 Current context: {cluster_context}")
                            
                            # Check if it's a local cluster
                            if any(local in cluster_context.lower() for local in ["minikube", "kind", "k3s", "docker-desktop", "rancher-desktop"]):
                                print(f"💡 This appears to be a local Kubernetes cluster - perfect for testing!")
                            else:
                                print(f"💡 This appears to be a cloud/production cluster")
                    else:
                        print(f"❌ Cannot connect to Kubernetes cluster")
                        print(f"")
                        
                        # Check if minikube is available but not running
                        if has_cmd("minikube"):
                            minikube_status = subprocess.run(["minikube", "status"], capture_output=True, text=True)
                            if "Stopped" in minikube_status.stdout:
                                print(f"💡 Minikube is installed but not running")
                                minikube_choice = choose(
                                    "What would you like to do?",
                                    [
                                        "Start Minikube for local testing",
                                        "I have a cloud cluster - help me connect",
                                        "Exit to set up cluster manually"
                                    ]
                                )
                                
                                if minikube_choice == 1:  # Start Minikube
                                    print(f"\n🚀 Starting Minikube...")
                                    print(f"💡 This may take a few minutes...")
                                    
                                    start_result = subprocess.run([
                                        "minikube", "start", 
                                        "--cpus=2", "--memory=4096", "--disk-size=20g", "--driver=docker"
                                    ])
                                    
                                    if start_result.returncode == 0:
                                        print(f"✅ Minikube started successfully!")
                                        cluster_connected = True
                                        cluster_context = "minikube"
                                    else:
                                        print(f"❌ Failed to start Minikube")
                                        print(f"💡 You can start it manually: minikube start")
                                        return
                                        
                                elif minikube_choice == 2:  # Cloud cluster - generate script
                                    print(f"\n☁️  Cloud Kubernetes Cluster Detected")
                                    print(f"💡 We'll generate the agent installation script for you")
                                    print(f"💡 You can run it once your cluster connection is ready")
                                    # Continue to script generation below
                                    
                                else:  # Exit
                                    print(f"💡 Set up your Kubernetes cluster and re-run this script")
                                    return
                        else:
                            # No minikube available
                            print(f"💡 No local Kubernetes cluster detected")
                            cluster_choice = choose(
                                "What would you like to do?",
                                [
                                    "Install Minikube for local testing",
                                    "I have a cloud cluster - help me connect",
                                    "Exit to set up cluster manually"
                                ]
                            )
                            
                            if cluster_choice == 1:  # Install Minikube
                                print(f"\n📦 Installing Minikube...")
                                if platform.system() == "Darwin":  # macOS
                                    if has_cmd("brew"):
                                        install_result = subprocess.run(["brew", "install", "minikube"], check=False)
                                        if install_result.returncode == 0:
                                            print(f"✅ Minikube installed successfully!")
                                            print(f"🚀 Starting Minikube...")
                                            start_result = subprocess.run([
                                                "minikube", "start", 
                                                "--cpus=2", "--memory=4096", "--disk-size=20g", "--driver=docker"
                                            ])
                                            if start_result.returncode == 0:
                                                print(f"✅ Minikube started successfully!")
                                                cluster_connected = True
                                                cluster_context = "minikube"
                                            else:
                                                print(f"❌ Failed to start Minikube")
                                                return
                                        else:
                                            print(f"❌ Failed to install Minikube via Homebrew")
                                            return
                                    else:
                                        print(f"❌ Homebrew not found. Please install Minikube manually:")
                                        print(f"   https://minikube.sigs.k8s.io/docs/start/")
                                        return
                                elif platform.system() == "Linux":
                                    print(f"💡 Installing Minikube on Linux...")
                                    install_result = subprocess.run([
                                        "curl", "-LO", 
                                        "https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64"
                                    ], check=False)
                                    if install_result.returncode == 0:
                                        subprocess.run(["sudo", "install", "minikube-linux-amd64", "/usr/local/bin/minikube"], check=False)
                                        subprocess.run(["rm", "minikube-linux-amd64"], check=False)
                                        print(f"✅ Minikube installed!")
                                        print(f"🚀 Starting Minikube...")
                                        start_result = subprocess.run([
                                            "minikube", "start", 
                                            "--cpus=2", "--memory=4096", "--disk-size=20g", "--driver=docker"
                                        ])
                                        if start_result.returncode == 0:
                                            print(f"✅ Minikube started successfully!")
                                            cluster_connected = True
                                            cluster_context = "minikube"
                                        else:
                                            print(f"❌ Failed to start Minikube")
                                            return
                                    else:
                                        print(f"❌ Failed to download Minikube")
                                        return
                                else:
                                    print(f"❌ Unsupported platform. Please install Minikube manually:")
                                    print(f"   https://minikube.sigs.k8s.io/docs/start/")
                                    return
                                    
                            elif cluster_choice == 2:  # Cloud cluster - generate script
                                print(f"\n☁️  Cloud Kubernetes Cluster Detected")
                                print(f"💡 We'll generate the agent installation script for you")
                                print(f"💡 You can run it once your cluster connection is ready")
                                # Continue to script generation below
                                
                            else:  # Exit
                                print(f"💡 Set up your Kubernetes cluster and re-run this script")
                                return
                                
                except Exception as e:
                    print(f"❌ Error checking cluster connection: {e}")
                    return
                
                if not cluster_connected:
                    print(f"❌ Cannot proceed without a connected Kubernetes cluster")
                    return
                
                print(f"")
                
                # Skip redundant Minikube setup since we handled it in cluster connection check
                namespace = input("Enter Kubernetes namespace (or press Enter for 'dagster'): ").strip()
                if not namespace:
                    namespace = "dagster"
                
                # Ask for agent configuration
                print(f"\n⚙️  Agent Configuration")
                
                # Number of replicas
                try:
                    replicas_input = input("Number of agent replicas (or press Enter for 1): ").strip()
                    replicas = int(replicas_input) if replicas_input else 1
                    if replicas < 1:
                        replicas = 1
                        print(f"⚠️  Minimum replicas is 1, using 1")
                except ValueError:
                    replicas = 1
                    print(f"⚠️  Invalid input, using 1 replica")
                
                # Resource limits
                print(f"\n💾 Resource Configuration")
                cpu_limit = input("CPU limit per replica (e.g., '1000m' or press Enter for '1000m'): ").strip()
                if not cpu_limit:
                    cpu_limit = "1000m"
                
                memory_limit = input("Memory limit per replica (e.g., '2Gi' or press Enter for '2Gi'): ").strip()
                if not memory_limit:
                    memory_limit = "2Gi"
                
                # Resource requests
                cpu_request = input("CPU request per replica (e.g., '500m' or press Enter for '500m'): ").strip()
                if not cpu_request:
                    cpu_request = "500m"
                
                memory_request = input("Memory request per replica (e.g., '1Gi' or press Enter for '1Gi'): ").strip()
                if not memory_request:
                    memory_request = "1Gi"
                
                print(f"\n📋 Configuration Summary:")
                print(f"   • Namespace: {namespace}")
                print(f"   • Replicas: {replicas}")
                print(f"   • CPU Limit: {cpu_limit}, Request: {cpu_request}")
                print(f"   • Memory Limit: {memory_limit}, Request: {memory_request}")
                
                # Ask about branch deployments
                print(f"\n🌿 Branch Deployments")
                print(f"💡 Branch deployments create lightweight staging environments for each code change")
                branch_deployments = choose(
                    "Enable branch deployments?",
                    ["Yes, enable branch deployments (recommended)", "No, just main deployment"]
                )
                enable_branch_deployments = (branch_deployments == 1)
                
                # Ask about high availability
                print(f"\n🔄 High Availability")
                if replicas > 1:
                    print(f"💡 You've configured {replicas} replicas - this enables high availability")
                    isolated_agents = choose(
                        "Are your agents physically isolated (different clusters)?",
                        ["No, same cluster", "Yes, different clusters"]
                    )
                    enable_isolated_agents = (isolated_agents == 2)
                else:
                    enable_isolated_agents = False
                
                print(f"\n📋 Final Configuration Summary:")
                print(f"   • Namespace: {namespace}")
                print(f"   • Replicas: {replicas}")
                print(f"   • CPU Limit: {cpu_limit}, Request: {cpu_request}")
                print(f"   • Memory Limit: {memory_limit}, Request: {memory_request}")
                print(f"   • Branch Deployments: {'Enabled' if enable_branch_deployments else 'Disabled'}")
                if replicas > 1:
                    print(f"   • High Availability: Enabled")
                    print(f"   • Isolated Agents: {'Yes' if enable_isolated_agents else 'No'}")
                
                # Ask about additional configurations
                print(f"\n🔧 Additional Configuration")
                
                # Image pull secrets
                image_pull_secret = choose(
                    "Do you need to configure image pull secrets for private registries?",
                    ["No, using public registry or cloud managed", "Yes, I need to configure image pull secrets"]
                )
                configure_image_pull_secrets = (image_pull_secret == 2)
                
                # Compute logs
                compute_logs = choose(
                    "How should compute logs (stdout/stderr) be handled?",
                    ["Store in Dagster+ (default)", "Store in S3", "Disable compute logs"]
                )
                compute_logs_config = compute_logs
                
                if configure_image_pull_secrets:
                    print(f"\n📦 Image Pull Secrets Configuration")
                    print(f"💡 You'll need to create the secret manually:")
                    print(f"   kubectl create secret docker-registry regCred \\")
                    print(f"     --docker-server=DOCKER_REGISTRY_SERVER \\")
                    print(f"     --docker-username=DOCKER_USER \\")
                    print(f"     --docker-password=DOCKER_PASSWORD \\")
                    print(f"     --docker-email=DOCKER_EMAIL")
                    print(f"💡 Then uncomment imagePullSecrets in values.yaml")
                
                if compute_logs_config == 2:  # S3
                    print(f"\n📊 S3 Compute Logs Configuration")
                    print(f"💡 You'll need to configure S3 bucket details in values.yaml")
                    print(f"💡 Uncomment the computeLogs section and add your bucket/region")
                elif compute_logs_config == 3:  # Disabled
                    print(f"\n📊 Compute Logs Disabled")
                    print(f"💡 stdout/stderr will not be stored or accessible in Dagster+ UI")
                
                # Generate K8s setup directory and files
                k8s_dir = "dagster-plus-k8s"
                print(f"")
                print(f"📁 Generating Kubernetes setup files in '{k8s_dir}/' directory...")
                
                if os.path.exists(k8s_dir):
                    overwrite = choose(
                        f"Directory '{k8s_dir}' already exists. Overwrite?",
                        ["Yes, overwrite", "No, cancel"]
                    )
                    if overwrite == 2:
                        print(f"❌ Cancelled")
                        return
                    import shutil
                    shutil.rmtree(k8s_dir)
                
                os.makedirs(k8s_dir, exist_ok=True)
                
                # Generate installation script
                print(f"📄 Generating install-agent.sh...")
                
                install_script_content = f"""#!/bin/bash
# Dagster+ Kubernetes Agent Installation Script
# Generated by Dagster+ onboarding for {org_name}/{deployment_name}

set -e

echo "☸️  Installing Dagster+ Kubernetes Agent..."
echo "📍 Organization: {org_name}"
echo "🚀 Deployment: {deployment_name}"
echo "📦 Namespace: {namespace}"
echo ""

# Check if kubectl is installed
if ! command -v kubectl &> /dev/null; then
    echo "❌ kubectl not found. Please install kubectl first:"
    echo "   https://kubernetes.io/docs/tasks/tools/"
    exit 1
fi

# Check if helm is installed
if ! command -v helm &> /dev/null; then
    echo "❌ Helm not found. Please install Helm first:"
    echo "   https://helm.sh/docs/intro/install/"
    exit 1
fi

echo "✅ kubectl and helm found"
echo ""

# Check cluster connection
echo "🔍 Checking Kubernetes cluster connection..."
if ! kubectl cluster-info &> /dev/null; then
    echo "❌ Cannot connect to Kubernetes cluster"
    echo "💡 Make sure your kubeconfig is set up correctly"
    exit 1
fi

echo "✅ Connected to cluster"
CONTEXT=$(kubectl config current-context)
echo "📋 Current context: $CONTEXT"
echo ""

# Add Dagster Helm repository
echo "📦 Adding Dagster Helm repository..."
helm repo add dagster-cloud https://dagster-io.github.io/helm-user-cloud
helm repo update

# Create namespace
echo "📁 Creating namespace '{namespace}'..."
kubectl create namespace {namespace} || echo "   (namespace may already exist)"

# Create secret with agent token
echo "🔐 Creating secret with agent token..."
kubectl create secret generic dagster-cloud-agent-token \\
  --from-literal=DAGSTER_CLOUD_AGENT_TOKEN="{api_token}" \\
  --namespace {namespace} \\
  --dry-run=client -o yaml | kubectl apply -f -

# Install agent
echo "☸️  Installing Dagster agent via Helm..."
helm upgrade --install dagster-cloud-agent dagster-cloud/dagster-cloud-agent \\
  --namespace {namespace} \\
  --set dagsterCloud.organization="{org_name}" \\
  --set dagsterCloud.deployment="{deployment_name}" \\
  --set dagsterCloud.branchDeployments={str(enable_branch_deployments).lower()} \\
  --set dagsterCloudAgent.replicas={replicas} \\
  --set dagsterCloudAgent.resources.limits.cpu="{cpu_limit}" \\
  --set dagsterCloudAgent.resources.limits.memory="{memory_limit}" \\
  --set dagsterCloudAgent.resources.requests.cpu="{cpu_request}" \\
  --set dagsterCloudAgent.resources.requests.memory="{memory_request}" \\
  --set isolatedAgents.enabled={str(enable_isolated_agents).lower()}

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Kubernetes agent installed successfully!"
    echo ""
    echo "💡 Check agent status:"
    echo "   kubectl get pods -n {namespace}"
    echo "   kubectl logs -n {namespace} -l app=dagster-cloud-agent"
    echo ""
    echo "📊 Check agent in Dagster+ UI:"
    echo "   https://{org_name}.dagster.cloud/{deployment_name}/agents"
else
    echo ""
    echo "❌ Installation failed!"
    echo "💡 Check the error output above"
    exit 1
fi
"""
                
                install_script_path = os.path.join(k8s_dir, "install-agent.sh")
                with open(install_script_path, "w") as f:
                    f.write(install_script_content)
                os.chmod(install_script_path, 0o755)
                
                # Generate uninstall script
                print(f"📄 Generating uninstall-agent.sh...")
                
                uninstall_script_content = f"""#!/bin/bash
# Uninstall Dagster+ Kubernetes Agent
# Generated by Dagster+ onboarding for {org_name}/{deployment_name}

set -e

echo "🗑️  Uninstalling Dagster+ Kubernetes Agent..."
echo "📦 Namespace: {namespace}"
echo ""

read -p "⚠️  Are you sure you want to uninstall the agent? (y/N): " confirm
if [[ $confirm != [yY] && $confirm != [yY][eE][sS] ]]; then
    echo "❌ Uninstall cancelled"
    exit 0
fi

echo "🗑️  Uninstalling Helm release..."
helm uninstall dagster-cloud-agent --namespace {namespace}

echo "🗑️  Deleting secret..."
kubectl delete secret dagster-cloud-agent-token --namespace {namespace} || true

echo "✅ Agent uninstalled"
echo "💡 To delete the namespace: kubectl delete namespace {namespace}"
"""
                
                uninstall_script_path = os.path.join(k8s_dir, "uninstall-agent.sh")
                with open(uninstall_script_path, "w") as f:
                    f.write(uninstall_script_content)
                os.chmod(uninstall_script_path, 0o755)
                
                # Generate values.yaml for customization
                print(f"📄 Generating values.yaml...")
                
                values_content = f"""# Dagster+ Kubernetes Agent Configuration
# Generated by Dagster+ onboarding for {org_name}/{deployment_name}
#
# To use custom values:
#   helm upgrade --install dagster-cloud-agent dagster-cloud/dagster-cloud-agent \\
#     --namespace {namespace} \\
#     -f values.yaml

dagsterCloud:
  organization: "{org_name}"
  deployment: "{deployment_name}"
  branchDeployments: {str(enable_branch_deployments).lower()}

# Agent configuration
dagsterCloudAgent:
  replicas: {replicas}
  resources:
    limits:
      cpu: "{cpu_limit}"
      memory: "{memory_limit}"
    requests:
      cpu: "{cpu_request}"
      memory: "{memory_request}"

# High availability configuration
isolatedAgents:
  enabled: {str(enable_isolated_agents).lower()}

# Uncomment to set node affinity
# nodeSelector:
#   node-role: dagster

# Uncomment to enable pod autoscaling
# autoscaling:
#   enabled: true
#   minReplicas: 1
#   maxReplicas: 5
#   targetCPUUtilizationPercentage: 80

# Image pull secrets configuration
{f"imagePullSecrets:" if configure_image_pull_secrets else "# Uncomment to configure image pull secrets"}
{f"  - name: regCred" if configure_image_pull_secrets else "# imagePullSecrets:"}
{f"#   - name: regCred" if configure_image_pull_secrets else "#   - name: regCred"}

# Compute logs configuration
{f"computeLogs:" if compute_logs_config == 3 else "# Uncomment to configure compute logs"}
{f"  enabled: false" if compute_logs_config == 3 else "# computeLogs:"}
{f"#   enabled: true" if compute_logs_config == 3 else "#   enabled: true"}
{f"#   custom:" if compute_logs_config == 3 else "#   custom:"}
{f"#     module: dagster_aws.s3.compute_log_manager" if compute_logs_config == 3 else "#     module: dagster_aws.s3.compute_log_manager"}
{f"#     class: S3ComputeLogManager" if compute_logs_config == 3 else "#     class: S3ComputeLogManager"}
{f"#     config:" if compute_logs_config == 3 else "#     config:"}
{f"#       show_url_only: true" if compute_logs_config == 3 else "#       show_url_only: true"}
{f"#       bucket: your-compute-log-storage-bucket" if compute_logs_config == 3 else "#       bucket: your-compute-log-storage-bucket"}
{f"#       region: your-bucket-region" if compute_logs_config == 3 else "#       region: your-bucket-region"}
"""
                
                values_path = os.path.join(k8s_dir, "values.yaml")
                with open(values_path, "w") as f:
                    f.write(values_content)
                
                # Generate README
                print(f"📄 Generating README.md...")
                
                readme_content = f"""# Dagster+ Kubernetes Agent Setup

This directory contains scripts for setting up a Dagster+ Hybrid agent on Kubernetes.

## Configuration Summary

**Organization:** {org_name}  
**Deployment:** {deployment_name}  
**Namespace:** {namespace}  
**Replicas:** {replicas}  
**Resources:** CPU {cpu_limit}/{cpu_request}, Memory {memory_limit}/{memory_request}  
**Branch Deployments:** {'Enabled' if enable_branch_deployments else 'Disabled'}  
**High Availability:** {'Enabled' if replicas > 1 else 'Disabled'}  
**Isolated Agents:** {'Enabled' if enable_isolated_agents else 'Disabled'}

## Files

- `install-agent.sh` - Install the agent on your Kubernetes cluster
- `uninstall-agent.sh` - Remove the agent
- `values.yaml` - Helm values for customization

## Prerequisites

1. **kubectl configured and connected to your cluster:**
   ```bash
   kubectl cluster-info
   kubectl get nodes
   ```

2. **Helm 3 installed:**
   ```bash
   helm version
   ```

3. **Appropriate RBAC permissions** to create:
   - Namespaces
   - Secrets
   - Deployments
   - Services

## Quick Start

### Install the Agent

```bash
cd {k8s_dir}
./install-agent.sh
```

This will:
1. Verify kubectl and helm are available
2. Check cluster connection
3. Add Dagster Helm repository
4. Create namespace and secret
5. Install the agent via Helm with your configuration

### Verify Installation

Check agent status:
```bash
kubectl get pods -n {namespace}
kubectl logs -n {namespace} -l app=dagster-cloud-agent
```

Check in Dagster+ UI:
https://{org_name}.dagster.cloud/{deployment_name}/agents

## Features Enabled

{f"### 🌿 Branch Deployments" if enable_branch_deployments else "### Branch Deployments (Disabled)"}
{f"Branch deployments are **enabled** for this agent. This creates lightweight staging environments for each code change, allowing you to test changes before merging to production." if enable_branch_deployments else "Branch deployments are **disabled**. To enable them, update the values.yaml and redeploy."}

{f"### 🔄 High Availability" if replicas > 1 else "### High Availability (Single Replica)"}
{f"High availability is **enabled** with {replicas} replicas. Work will be load balanced across all replicas." if replicas > 1 else "Running with 1 replica. To enable high availability, increase replicas in values.yaml and redeploy."}

{f"### 🔒 Isolated Agents" if enable_isolated_agents else "### Isolated Agents (Disabled)"}
{f"Isolated agents are **enabled**. This is recommended when agents run on physically separate clusters." if enable_isolated_agents else "Isolated agents are **disabled**. This is fine for single-cluster deployments."}

## Custom Configuration

To customize the agent (resources, scaling, etc.), edit `values.yaml` and run:

```bash
helm upgrade --install dagster-cloud-agent dagster-cloud/dagster-cloud-agent \\
  --namespace {namespace} \\
  -f values.yaml
```

## Uninstall

```bash
./uninstall-agent.sh
```

## Troubleshooting

### Agent Pod Not Starting

Check pod status:
```bash
kubectl describe pod -n {namespace} -l app=dagster-cloud-agent
```

Check logs:
```bash
kubectl logs -n {namespace} -l app=dagster-cloud-agent --tail=100
```

### Connection Issues

Verify token is correct:
```bash
kubectl get secret dagster-cloud-agent-token -n {namespace} -o yaml
```

### Resource Constraints

If the agent is crashing due to resource limits, edit `values.yaml` to increase resources.

## Additional Resources

- [Dagster+ Kubernetes Agent Documentation](https://docs.dagster.io/dagster-plus/deployment/agents/kubernetes)
- [Helm Chart Values](https://github.com/dagster-io/dagster-cloud-helm)
- [Kubernetes Documentation](https://kubernetes.io/docs/home/)

## Support

- [Dagster Slack Community](https://dagster.io/slack)
- [Dagster+ Support](https://dagster.io/support)
"""
                
                readme_path = os.path.join(k8s_dir, "README.md")
                with open(readme_path, "w") as f:
                    f.write(readme_content)
                
                print(f"")
                print(f"✅ Generated Kubernetes setup files in '{k8s_dir}/' directory:")
                print(f"   • install-agent.sh - Installation script (executable)")
                print(f"   • uninstall-agent.sh - Cleanup script (executable)")
                print(f"   • values.yaml - Helm values for customization")
                print(f"   • README.md - Complete setup instructions")
                print(f"")
                
                # Offer to run the commands automatically
                run_now = choose(
                    "Would you like to install the agent now?",
                    ["Yes, run install-agent.sh now", "No, I'll run it manually (on this or another machine)"]
                )
                
                if run_now == 1:
                    print(f"\n🚀 Running installation script...")
                    print(f"")
                    
                    try:
                        result = subprocess.run(
                            ["./install-agent.sh"],
                            cwd=os.path.abspath(k8s_dir)
                        )
                        
                        if result.returncode == 0:
                            print(f"\n✅ Kubernetes agent installation completed!")
                        else:
                            print(f"\n⚠️  Installation script exited with code {result.returncode}")
                            print(f"💡 Check the output above for errors")
                    except Exception as e:
                        print(f"❌ Failed to run installation script: {e}")
                        print(f"💡 You can run it manually: cd {k8s_dir} && ./install-agent.sh")
                else:
                    print(f"\n📁 Setup files ready in '{k8s_dir}/' directory")
                    print(f"💡 To install the agent (on this or another machine):")
                    print(f"   1. Copy the '{k8s_dir}' directory to your target machine")
                    print(f"   2. Run: cd {k8s_dir} && ./install-agent.sh")
                    print(f"")
                    print(f"💡 Or open the directory now:")
                    try:
                        if platform.system() == "Darwin":
                            subprocess.run(["open", os.path.abspath(k8s_dir)], capture_output=True)
                        elif platform.system() == "Linux":
                            subprocess.run(["xdg-open", os.path.abspath(k8s_dir)], capture_output=True)
                    except Exception:
                        pass
                
                print(f"")
                print(f"💡 For more configuration options, see:")
                print(f"   https://docs.dagster.io/dagster-plus/deployment/agents/kubernetes")
                print(f"")
                if cluster_context and "minikube" in cluster_context.lower():
                    print(f"🎯 Local Minikube Management:")
                    print(f"")
                    print(f"📊 Monitor agent:")
                    print(f"   kubectl --namespace {namespace} get pods")
                    print(f"   kubectl --namespace {namespace} logs -l app=dagster-cloud-agent")
                    print(f"   minikube dashboard  # Visual web UI")
                    print(f"")
                    print(f"🛑 Stop/cleanup when done testing:")
                    print(f"   minikube stop  # Pause the cluster")
                    print(f"   minikube delete  # Completely remove the cluster")
                    print(f"")
                    print(f"💡 Your agent will run locally - perfect for testing before production!")
                
            elif agent_type == 3:  # ECS
                print(f"\n🐳 Setting up Amazon ECS agent...")
                print(f"")
                print(f"📋 Prerequisites:")
                print(f"   • AWS CLI configured with appropriate credentials")
                print(f"   • Permissions to create ECS resources and CloudFormation stacks")
                print(f"   • VPC and subnets available (or will create new)")
                print(f"")
                
                # Check if AWS CLI is installed
                if not has_cmd("aws"):
                    print(f"❌ AWS CLI not found. Please install AWS CLI first:")
                    print(f"   https://aws.amazon.com/cli/latest/userguide/getting-started-install.html")
                    return
                
                print(f"✅ AWS CLI found")
                print(f"")
                
                # VPC Configuration
                print(f"🌐 VPC Configuration:")
                vpc_choice = choose(
                    "How would you like to set up networking?",
                    [
                        "Create new VPC (recommended for new deployments)",
                        "Use existing VPC (I'll provide VPC ID and subnet)"
                    ]
                )
                
                # Branch Deployments
                print(f"")
                print(f"🌿 Branch Deployments:")
                print(f"💡 Branch deployments allow you to test code in isolated environments")
                branch_deployments = choose(
                    "Enable branch deployments?",
                    ["Yes, enable branch deployments", "No, just main deployment"]
                )
                enable_branch_deployments = (branch_deployments == 1)
                
                # Generate setup directory and files
                ecs_dir = "dagster-plus-ecs"
                print(f"")
                print(f"📁 Generating ECS setup files in '{ecs_dir}/' directory...")
                
                if os.path.exists(ecs_dir):
                    overwrite = choose(
                        f"Directory '{ecs_dir}' already exists. Overwrite?",
                        ["Yes, overwrite", "No, cancel"]
                    )
                    if overwrite == 2:
                        print(f"❌ Cancelled")
                        return
                    import shutil
                    shutil.rmtree(ecs_dir)
                
                os.makedirs(ecs_dir, exist_ok=True)
                
                # CloudFormation template URL
                cf_template_url = "https://s3.amazonaws.com/dagster.cloud/cloudformation/ecs-agent.yaml"
                stack_name = f"dagster-plus-agent-{deployment_name}"
                
                # Generate CloudFormation parameters file
                print(f"📄 Generating cloudformation-parameters.json...")
                
                if vpc_choice == 2:  # Existing VPC
                    print(f"")
                    fill_now = choose(
                        "Would you like to provide VPC details now?",
                        ["Yes, I'll enter them now", "No, I'll edit the file later"]
                    )
                    
                    vpc_id = "REPLACE_WITH_YOUR_VPC_ID"
                    subnet_id = "REPLACE_WITH_YOUR_SUBNET_ID"
                    ecs_cluster = ""
                    
                    if fill_now == 1:
                        print(f"")
                        print(f"💡 You can find these values in AWS Console → VPC")
                        vpc_id = input("Enter VPC ID (e.g., vpc-1234abcd): ").strip() or vpc_id
                        subnet_id = input("Enter Subnet ID (e.g., subnet-5678efgh): ").strip() or subnet_id
                        
                        print(f"")
                        use_existing_cluster = choose(
                            "Do you have an existing ECS cluster to use?",
                            ["No, create new cluster", "Yes, I'll specify the cluster name"]
                        )
                        
                        if use_existing_cluster == 2:
                            ecs_cluster = input("Enter ECS cluster name: ").strip()
                    
                    cf_params_content = f"""[
  {{"ParameterKey": "DagsterOrganization", "ParameterValue": "{org_name}"}},
  {{"ParameterKey": "DagsterDeployment", "ParameterValue": "{deployment_name}"}},
  {{"ParameterKey": "EnableBranchDeployments", "ParameterValue": "{str(enable_branch_deployments).lower()}"}},
  {{"ParameterKey": "AgentToken", "ParameterValue": "{api_token}"}},
  {{"ParameterKey": "DeployVPC", "ParameterValue": "{vpc_id}"}},
  {{"ParameterKey": "DeployVPCSubnet", "ParameterValue": "{subnet_id}"}},
  {{"ParameterKey": "ExistingECSCluster", "ParameterValue": "{ecs_cluster}"}},
  {{"ParameterKey": "TaskLaunchType", "ParameterValue": "FARGATE"}}
]"""
                    
                    if fill_now == 2 or vpc_id == "REPLACE_WITH_YOUR_VPC_ID":
                        print(f"⚠️  Remember to edit cloudformation-parameters.json to add your VPC ID and subnet ID before deploying")
                else:  # New VPC
                    cf_params_content = f"""[
  {{"ParameterKey": "DagsterOrganization", "ParameterValue": "{org_name}"}},
  {{"ParameterKey": "DagsterDeployment", "ParameterValue": "{deployment_name}"}},
  {{"ParameterKey": "EnableBranchDeployments", "ParameterValue": "{str(enable_branch_deployments).lower()}"}},
  {{"ParameterKey": "AgentToken", "ParameterValue": "{api_token}"}}
]"""
                
                cf_params_path = os.path.join(ecs_dir, "cloudformation-parameters.json")
                with open(cf_params_path, "w") as f:
                    f.write(cf_params_content)
                
                # Generate deployment script
                print(f"📄 Generating deploy-ecs-agent.sh...")
                
                deploy_script_content = f"""#!/bin/bash
# AWS ECS Dagster+ Agent Deployment Script
# Generated by Dagster+ onboarding for {org_name}/{deployment_name}

set -e

echo "☁️  Deploying Dagster+ ECS Agent..."
echo "📍 Organization: {org_name}"
echo "🚀 Deployment: {deployment_name}"
echo "🌿 Branch Deployments: {'Enabled' if enable_branch_deployments else 'Disabled'}"
echo ""

# Check if AWS CLI is installed
if ! command -v aws &> /dev/null; then
    echo "❌ AWS CLI not found. Please install AWS CLI first:"
    echo "   https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html"
    exit 1
fi

# Check AWS credentials
echo "🔐 Checking AWS credentials..."
if ! aws sts get-caller-identity &> /dev/null; then
    echo "❌ AWS credentials not configured. Run 'aws configure' first."
    exit 1
fi

echo "✅ AWS credentials configured"
CALLER_IDENTITY=$(aws sts get-caller-identity)
ACCOUNT_ID=$(echo $CALLER_IDENTITY | grep -o '"Account": "[^"]*"' | cut -d'"' -f4)
USER_ARN=$(echo $CALLER_IDENTITY | grep -o '"Arn": "[^"]*"' | cut -d'"' -f4)
echo "📋 Account: $ACCOUNT_ID"
echo "👤 User: $USER_ARN"
echo ""

# Get current region
AWS_REGION=$(aws configure get region)
if [ -z "$AWS_REGION" ]; then
    echo "⚠️  No default region set. Using us-east-1"
    AWS_REGION="us-east-1"
fi

echo "🌎 Using AWS region: $AWS_REGION"
echo ""

echo "🚀 Deploying CloudFormation stack..."
echo "📋 Stack name: {stack_name}"
echo "🔗 Template: {cf_template_url}"
echo ""

# Deploy the CloudFormation stack
aws cloudformation deploy \\
    --template-url "{cf_template_url}" \\
    --stack-name "{stack_name}" \\
    --parameter-overrides file://cloudformation-parameters.json \\
    --capabilities CAPABILITY_IAM \\
    --region "$AWS_REGION"

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ CloudFormation stack deployed successfully!"
    echo ""
    echo "📊 Stack details:"
    aws cloudformation describe-stacks \\
        --stack-name "{stack_name}" \\
        --region "$AWS_REGION" \\
        --query 'Stacks[0].[StackName,StackStatus,CreationTime]' \\
        --output table
    
    echo ""
    echo "🔗 View in AWS Console:"
    echo "   https://console.aws.amazon.com/cloudformation/home?region=$AWS_REGION#/stacks/stackinfo?stackId={stack_name}"
    echo ""
    echo "📊 Check agent status in Dagster+ UI:"
    echo "   https://{org_name}.dagster.cloud/{deployment_name}/agents"
else
    echo ""
    echo "❌ CloudFormation deployment failed!"
    echo "💡 Check the AWS CloudFormation console for error details:"
    echo "   https://console.aws.amazon.com/cloudformation/home?region=$AWS_REGION"
    exit 1
fi
"""
                
                deploy_script_path = os.path.join(ecs_dir, "deploy-ecs-agent.sh")
                with open(deploy_script_path, "w") as f:
                    f.write(deploy_script_content)
                os.chmod(deploy_script_path, 0o755)
                
                # Generate delete script
                print(f"📄 Generating delete-ecs-agent.sh...")
                
                delete_script_content = f"""#!/bin/bash
# Delete Dagster+ ECS Agent CloudFormation Stack
# Generated by Dagster+ onboarding for {org_name}/{deployment_name}

set -e

echo "🗑️  Deleting Dagster+ ECS Agent stack..."
echo "📋 Stack name: {stack_name}"
echo ""

# Get current region
AWS_REGION=$(aws configure get region)
if [ -z "$AWS_REGION" ]; then
    AWS_REGION="us-east-1"
fi

echo "🌎 Using AWS region: $AWS_REGION"
echo ""

read -p "⚠️  Are you sure you want to delete the stack '{stack_name}'? (y/N): " confirm
if [[ $confirm != [yY] && $confirm != [yY][eE][sS] ]]; then
    echo "❌ Deletion cancelled"
    exit 0
fi

echo "🗑️  Deleting CloudFormation stack..."
aws cloudformation delete-stack \\
    --stack-name "{stack_name}" \\
    --region "$AWS_REGION"

echo "✅ Stack deletion initiated"
echo "💡 Monitor deletion progress:"
echo "   aws cloudformation describe-stacks --stack-name {stack_name} --region $AWS_REGION"
echo ""
echo "💡 Or view in AWS Console:"
echo "   https://console.aws.amazon.com/cloudformation/home?region=$AWS_REGION"
"""
                
                delete_script_path = os.path.join(ecs_dir, "delete-ecs-agent.sh")
                with open(delete_script_path, "w") as f:
                    f.write(delete_script_content)
                os.chmod(delete_script_path, 0o755)
                
                # Generate README
                print(f"📄 Generating README.md...")
                
                readme_content = f"""# Dagster+ ECS Agent Setup

This directory contains scripts for setting up a Dagster+ Hybrid agent on Amazon ECS.

## Configuration Summary

**Organization:** {org_name}  
**Deployment:** {deployment_name}  
**Branch Deployments:** {'Enabled' if enable_branch_deployments else 'Disabled'}  
**VPC Setup:** {'New VPC (automatic)' if vpc_choice == 1 else 'Existing VPC (manual configuration required)'}

## Files

- `cloudformation-parameters.json` - CloudFormation stack parameters
- `deploy-ecs-agent.sh` - Deploy agent to AWS ECS
- `delete-ecs-agent.sh` - Remove the agent stack

## Prerequisites

1. **AWS CLI installed and configured:**
   ```bash
   aws configure
   ```

2. **AWS Permissions required:**
   - ECS: CreateCluster, CreateService, RegisterTaskDefinition
   - IAM: CreateRole, AttachRolePolicy
   - CloudFormation: CreateStack, UpdateStack, DeleteStack
   - VPC: CreateVpc, CreateSubnet (if creating new VPC)

3. **Agent Token:** Already configured in parameters file

## Quick Start

### Deploy the Agent

```bash
cd {ecs_dir}
./deploy-ecs-agent.sh
```

This will:
1. Verify AWS credentials
2. Deploy CloudFormation stack
3. Create ECS cluster and agent service
4. Display stack status and links

### Verify Deployment

Check the agent status in your Dagster+ UI:
https://{org_name}.dagster.cloud/{deployment_name}/agents

Or via AWS Console:
```bash
aws ecs list-services --cluster dagster-plus-{deployment_name}
```

## Manual Deployment

If you prefer to deploy manually:

```bash
aws cloudformation deploy \\
    --template-url https://s3.amazonaws.com/dagster.cloud/cloudformation/ecs-agent.yaml \\
    --stack-name {stack_name} \\
    --parameter-overrides file://cloudformation-parameters.json \\
    --capabilities CAPABILITY_IAM \\
    --region us-east-1
```

## Updating the Agent

To update the agent (e.g., after changing parameters):

```bash
./deploy-ecs-agent.sh
```

CloudFormation will update the existing stack.

## Removing the Agent

```bash
./delete-ecs-agent.sh
```

**Warning:** This will permanently delete the agent and all associated resources.

## Troubleshooting

### Stack Creation Failed

1. Check CloudFormation console for detailed error:
   ```bash
   aws cloudformation describe-stack-events --stack-name {stack_name}
   ```

2. Common issues:
   - Insufficient IAM permissions
   - VPC/subnet configuration errors
   - Region-specific limitations

### Agent Not Showing in UI

1. Verify agent is running:
   ```bash
   aws ecs list-tasks --cluster dagster-plus-{deployment_name}
   ```

2. Check agent logs:
   ```bash
   aws ecs describe-tasks --cluster dagster-plus-{deployment_name} --tasks <task-id>
   ```

3. Verify token is correct in parameters file

### Agent Token Rotation

To rotate the agent token:

1. Generate new token in Dagster+ UI
2. Update `cloudformation-parameters.json`
3. Run `./deploy-ecs-agent.sh` to update

## Additional Resources

- [Dagster+ ECS Agent Documentation](https://docs.dagster.io/dagster-plus/deployment/agents/amazon-ecs)
- [AWS ECS Documentation](https://docs.aws.amazon.com/ecs/)
- [CloudFormation Documentation](https://docs.aws.amazon.com/cloudformation/)

## Support

- [Dagster Slack Community](https://dagster.io/slack)
- [Dagster+ Support](https://dagster.io/support)
"""
                
                readme_path = os.path.join(ecs_dir, "README.md")
                with open(readme_path, "w") as f:
                    f.write(readme_content)
                
                print(f"")
                print(f"✅ Generated ECS setup files in '{ecs_dir}/' directory:")
                print(f"   • cloudformation-parameters.json - Stack parameters")
                print(f"   • deploy-ecs-agent.sh - Deployment script")
                print(f"   • delete-ecs-agent.sh - Cleanup script")
                print(f"   • README.md - Complete setup instructions")
                print(f"")
                
                if vpc_choice == 2:
                    print(f"⚠️  IMPORTANT: Edit cloudformation-parameters.json")
                    print(f"   Replace REPLACE_WITH_YOUR_VPC_ID and REPLACE_WITH_YOUR_SUBNET_ID")
                    print(f"   with your actual AWS VPC and subnet IDs")
                    print(f"")
                
                # Ask user what to do next
                ecs_action = choose(
                    "What would you like to do next?",
                    [
                        "Deploy agent now (run deploy-ecs-agent.sh on this machine)",
                        "I'll run the script manually (on this or another machine)",
                        "Open setup directory"
                    ]
                )
                
                if ecs_action == 1:
                    # Check if VPC values need to be filled in
                    if vpc_choice == 2 and (vpc_id == "REPLACE_WITH_YOUR_VPC_ID" or subnet_id == "REPLACE_WITH_YOUR_SUBNET_ID"):
                        print(f"\n⚠️  Cannot deploy yet - VPC details need to be configured")
                        print(f"💡 Please edit {os.path.join(ecs_dir, 'cloudformation-parameters.json')} first")
                        print(f"   Then run: cd {ecs_dir} && ./deploy-ecs-agent.sh")
                        return
                    
                    print(f"\n🚀 Running deployment script...")
                    print(f"💡 This may take 5-10 minutes...")
                    print(f"")
                    
                    try:
                        result = subprocess.run(
                            ["./deploy-ecs-agent.sh"],
                            cwd=os.path.abspath(ecs_dir)
                        )
                        
                        if result.returncode == 0:
                            print(f"\n✅ ECS agent deployment completed!")
                        else:
                            print(f"\n⚠️  Deployment script exited with code {result.returncode}")
                            print(f"💡 Check the output above for errors")
                    except Exception as e:
                        print(f"❌ Failed to run deployment script: {e}")
                        print(f"💡 You can run it manually: cd {ecs_dir} && ./deploy-ecs-agent.sh")
                        
                elif ecs_action == 2:
                    print(f"\n📁 Setup files ready in '{ecs_dir}/' directory")
                    print(f"💡 To deploy the agent (on this or another machine):")
                    print(f"   1. Copy the '{ecs_dir}' directory to your target machine (if needed)")
                    print(f"   2. Ensure AWS CLI is configured on that machine")
                    print(f"   3. Run: cd {ecs_dir} && ./deploy-ecs-agent.sh")
                    
                    if vpc_choice == 2 and (vpc_id == "REPLACE_WITH_YOUR_VPC_ID" or subnet_id == "REPLACE_WITH_YOUR_SUBNET_ID"):
                        print(f"")
                        print(f"⚠️  Don't forget to edit cloudformation-parameters.json with your VPC details!")
                    
                elif ecs_action == 3:
                    print(f"\n📂 Opening {ecs_dir} directory...")
                    try:
                        if platform.system() == "Darwin":
                            subprocess.run(["open", os.path.abspath(ecs_dir)])
                        elif platform.system() == "Linux":
                            subprocess.run(["xdg-open", os.path.abspath(ecs_dir)])
                        else:
                            print(f"💡 Navigate to: {os.path.abspath(ecs_dir)}")
                    except Exception as e:
                        print(f"💡 Navigate to: {os.path.abspath(ecs_dir)}")
                
                print(f"")
                print(f"💡 For more details, see:")
                print(f"   https://docs.dagster.io/dagster-plus/deployment/agents/amazon-ecs")
            
            elif agent_type == 4:  # Docker
                print(f"\n🐳 Setting up Docker agent...")
                print(f"")
                print(f"📋 Prerequisites:")
                print(f"   • Docker installed and running")
                print(f"")
                
                # Check if Docker is available
                if not has_cmd("docker"):
                    print(f"❌ Docker not found. Please install Docker first:")
                    print(f"   https://docs.docker.com/get-docker/")
                    return
                
                # Start Docker daemon if needed
                start_docker_daemon()
                
                print(f"✅ Docker found and running")
                print(f"")
                
                print(f"🔧 Docker agent command:")
                print(f"")
                print(f"docker run -d \\")
                print(f"  --name dagster-cloud-agent \\")
                print(f"  --restart unless-stopped \\")
                print(f"  dagster/dagster-cloud-agent:latest \\")
                print(f"  dagster-cloud agent run \\")
                print(f"  --agent-token \"{api_token}\" \\")
                print(f"  --deployment {deployment_name}")
                print(f"")
                
                run_now = choose(
                    "Would you like to start the Docker agent now?",
                    ["Yes, start it", "No, I'll start it manually"]
                )
                
                if run_now == 1:
                    print(f"\n🚀 Starting Docker agent...")
                    result = subprocess.run([
                        "docker", "run", "-d",
                        "--name", "dagster-cloud-agent",
                        "--restart", "unless-stopped",
                        "dagster/dagster-cloud-agent:latest",
                        "dagster-cloud", "agent", "run",
                        "--agent-token", api_token,
                        "--deployment", deployment_name
                    ], capture_output=True, text=True)
                    
                    if result.returncode == 0:
                        print(f"✅ Docker agent started successfully!")
                        print(f"💡 To check logs: docker logs dagster-cloud-agent")
                        print(f"💡 To stop: docker stop dagster-cloud-agent")
                        print(f"💡 To remove: docker rm dagster-cloud-agent")
                    else:
                        print(f"❌ Failed to start Docker agent")
                        print(f"Error: {result.stderr}")
            
            print(f"\n✅ Agent setup completed!")
            print(f"💡 Your agent should now appear in the Dagster+ UI")
            print(f"💡 View it at: https://{org_name}.dagster.cloud/{deployment_name}/agents")
        
        print(f"\n✅ Enhanced onboarding completed!")
        if main_goal == 1:
            print(f"💡 Your project is ready for local development!")
            print(f"💡 You can now run 'dg dev' in your project directory")
        elif project_dir:
            print(f"💡 Project directory: {project_dir}")
            print(f"💡 You can now run 'dg dev' in your project directory")
        
    except KeyboardInterrupt:
        print("\n\n👋 Onboarding cancelled by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Onboarding failed: {e}")
        print("💡 Check the error details and try again")
        sys.exit(1)

if __name__ == "__main__":
    import sys
    
    # Check for diagnostic mode
    if len(sys.argv) > 1 and sys.argv[1] == "--diagnose":
        print("🔍 Dagster+ Agent Diagnostic Mode")
        print("=================================")
        
        org_name, api_token = get_organization_and_token()
        if not org_name or not api_token:
            sys.exit(1)
        
        diagnose_agent_issues(org_name, api_token)
    else:
        main()