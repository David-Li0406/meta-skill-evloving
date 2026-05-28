#!/usr/bin/env python3
"""
Dagster+ New Project Creation Script

Creates new Dagster projects from various sources:
- Scaffold new empty projects using create-dagster
- Clone quickstart templates (serverless/hybrid)
- Clone example repositories
- Import custom GitHub repositories

Usage:
    python dagster_new_project.py [--pkg-mgr pip|uv]
"""

import os
import sys
import subprocess
import shutil
import re
from dagster_utils import (
    choose,
    install_dagster,
    SERVERLESS_QUICKSTART_REPO,
    HYBRID_QUICKSTART_REPO,
    EXAMPLE_REPOSITORIES,
    DEFAULT_EXAMPLE_SOURCE
)

def create_new_dagster_project(pkg_mgr):
    """Create a new empty Dagster project using create-dagster CLI."""
    print("\n🆕 Creating new Dagster project...")
    print("💡 This will scaffold a clean, Components-compatible project structure")

    # Get project name
    project_name = input("Enter project name (or press Enter for 'my-dagster-project'): ").strip()
    if not project_name:
        project_name = "my-dagster-project"

    # Validate project name
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
            result = subprocess.run([
                "uvx", "create-dagster@latest", "project", project_name
            ], capture_output=True, text=True)

            if result.returncode != 0:
                print(f"❌ Failed to create project with uv")
                print(f"Error: {result.stderr}")
                return None

            print(f"✅ Project scaffolded successfully with uv")

            project_dir = os.path.abspath(project_name)
            os.chdir(project_dir)

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

            project_dir = os.path.abspath(project_name)
            os.chdir(project_dir)

            print("📦 Installing dependencies...")
            subprocess.run([sys.executable, "-m", "pip", "install", "-e", "."], check=True)
            print("✅ Dependencies installed successfully")

            return project_dir

        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to create project: {e}")
            return None
        except Exception as e:
            print(f"❌ Error creating project: {e}")
            return None

def clone_quickstart_project(deploy_type, project_name=None):
    """Clone a Dagster quickstart template."""
    quickstart_repo = SERVERLESS_QUICKSTART_REPO if deploy_type == 1 else HYBRID_QUICKSTART_REPO

    if not project_name:
        project_name = "dagster-cloud-serverless-quickstart" if deploy_type == 1 else "dagster-cloud-hybrid-quickstart"

    # Clone quickstart
    if os.path.exists(project_name):
        overwrite = choose(
            f"Directory '{project_name}' already exists. What would you like to do?",
            ["Overwrite it", "Use existing directory", "Cancel"]
        )

        if overwrite == 1:
            shutil.rmtree(project_name)
        elif overwrite == 3:
            return None

    try:
        print(f"📥 Cloning {project_name}...")
        subprocess.run(["git", "clone", quickstart_repo, project_name], check=True)
        project_dir = os.path.abspath(project_name)
        print(f"✅ Successfully cloned quickstart project")
        return project_dir

    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to clone quickstart: {e}")
        return None
    except Exception as e:
        print(f"❌ Error cloning quickstart: {e}")
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
        return "new_project", []
    elif source_choice == 2:
        return "quickstart", []
    elif source_choice == 3:
        return "eric_examples", EXAMPLE_REPOSITORIES[DEFAULT_EXAMPLE_SOURCE]
    elif source_choice == 4:
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
        except KeyboardInterrupt:
            print("\n❌ Operation cancelled")
            sys.exit(0)

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
        print("⚠️  GitHub API integration not implemented. Please provide a direct repository URL.")

    return repos

def main():
    """Main function for new project creation."""
    print("\n🚀 Dagster+ New Project Creation")

    # Get package manager preference
    pkg_mgr = choose("Choose your Python package manager:", ["pip", "uv"])

    # Install Dagster
    install_dagster(pkg_mgr)

    # Choose project source
    source_type, repos = choose_project_source()

    project_dir = None

    if source_type == "new_project":
        project_dir = create_new_dagster_project(pkg_mgr)
        if project_dir:
            print(f"\n✅ Successfully created new Dagster project!")
            print(f"📁 Project directory: {project_dir}")
            print(f"\n🎯 Your project has a clean Components-compatible structure:")
            print(f"   • pyproject.toml - Project configuration")
            print(f"   • definitions.py - Main definitions module")
            print(f"   • definitions/defs/ - Components directory")

    elif source_type == "quickstart":
        deploy_type = choose("Choose deployment type:", ["Serverless", "Hybrid"])
        project_dir = clone_quickstart_project(deploy_type)

    elif source_type in ["eric_examples", "custom_github"]:
        selected_repo = select_repository(repos)
        if selected_repo:
            project_dir = clone_selected_repository(selected_repo)

    elif source_type == "current_dir":
        project_dir = os.getcwd()
        print(f"📁 Using current directory: {project_dir}")

    if project_dir:
        print(f"\n✅ Project ready at: {project_dir}")
        print(f"\n💡 Next steps:")
        print(f"   1. cd {os.path.basename(project_dir)}")
        print(f"   2. dagster dev  # Start local development server")
        print(f"\n💡 To prepare for deployment:")
        print(f"   python dagster_prepare_deployment.py")
    else:
        print("\n❌ Project creation failed")
        sys.exit(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Operation cancelled by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
