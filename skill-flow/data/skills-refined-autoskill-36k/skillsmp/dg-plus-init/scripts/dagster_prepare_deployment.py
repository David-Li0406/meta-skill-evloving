#!/usr/bin/env python3
"""
Dagster+ Deployment Preparation Script

Prepares existing Dagster projects for Dagster+ Cloud deployment by:
- Generating/fixing required configuration files (pyproject.toml, dagster_cloud.yaml)
- Creating CI/CD workflow files for various Git providers
- Supporting monorepo and single-project structures
- Handling both Components and traditional project layouts

Usage:
    python dagster_prepare_deployment.py [project_dir]
"""

import os
import sys
import subprocess
import yaml
import re
import shutil
from dagster_utils import (
    choose,
    detect_package_name,
    detect_monorepo_structure,
    detect_components_project,
    SERVERLESS_QUICKSTART_REPO,
    HYBRID_QUICKSTART_REPO
)

def ensure_dagster_project_files(project_dir):
    """Ensure project has all necessary Dagster+ configuration files."""
    print(f"\n🔧 Ensuring Dagster project configuration...")

    project_name = os.path.basename(os.path.abspath(project_dir))
    use_components = detect_components_project(project_dir)
    has_src_layout = os.path.exists(os.path.join(project_dir, "src"))

    # Create pyproject.toml if missing
    pyproject_path = os.path.join(project_dir, "pyproject.toml")
    if not os.path.exists(pyproject_path):
        print(f"📄 Creating pyproject.toml...")
        create_pyproject_toml(project_dir, project_name, use_components)
    else:
        print(f"✅ pyproject.toml already exists")
        ensure_dagster_cloud_dependency(pyproject_path)

    # Create dagster_cloud.yaml if missing
    dagster_cloud_path = os.path.join(project_dir, "dagster_cloud.yaml")
    if not os.path.exists(dagster_cloud_path):
        print(f"📄 Creating dagster_cloud.yaml...")
        create_dagster_cloud_yaml(project_dir, project_name, use_components, has_src_layout)
    else:
        print(f"✅ dagster_cloud.yaml already exists")

    # Ensure dagster-cloud in requirements.txt if it exists
    requirements_path = os.path.join(project_dir, "requirements.txt")
    if os.path.exists(requirements_path):
        ensure_requirements_txt(requirements_path)

def create_pyproject_toml(project_dir, project_name, use_components):
    """Create pyproject.toml file."""
    # Read existing requirements.txt
    requirements_path = os.path.join(project_dir, "requirements.txt")
    dependencies = []
    if os.path.exists(requirements_path):
        with open(requirements_path, 'r') as f:
            dependencies = [line.strip() for line in f if line.strip() and not line.startswith('#')]

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

    for dep in dependencies:
        pyproject_content += f'    "{dep}",\n'

    if not any("dagster-cloud" in dep for dep in dependencies):
        pyproject_content += '    "dagster-cloud",\n'

    pyproject_content += """]

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

    pyproject_path = os.path.join(project_dir, "pyproject.toml")
    with open(pyproject_path, 'w') as f:
        f.write(pyproject_content)

    print(f"✅ Created pyproject.toml")

def create_dagster_cloud_yaml(project_dir, project_name, use_components, has_src_layout):
    """Create dagster_cloud.yaml file."""
    working_directory = "src" if has_src_layout else "."

    # Detect module name
    package_name, _ = detect_package_name(project_dir)

    dagster_cloud_content = f"""locations:
  - location_name: {project_name}
    code_source:
      package_name: {package_name}
"""

    if working_directory != ".":
        dagster_cloud_content += f"    working_directory: {working_directory}\n"

    dagster_cloud_path = os.path.join(project_dir, "dagster_cloud.yaml")
    with open(dagster_cloud_path, 'w') as f:
        f.write(dagster_cloud_content)

    print(f"✅ Created dagster_cloud.yaml with package_name: {package_name}")

def ensure_dagster_cloud_dependency(pyproject_path):
    """Ensure dagster-cloud is in pyproject.toml dependencies."""
    with open(pyproject_path, 'r') as f:
        content = f.read()

    if "dagster-cloud" not in content:
        print(f"📦 Adding dagster-cloud to pyproject.toml...")
        # Simple append to dependencies
        if "dependencies = [" in content:
            content = content.replace(
                "dependencies = [",
                'dependencies = [\n    "dagster-cloud",'
            )
            with open(pyproject_path, 'w') as f:
                f.write(content)
            print(f"✅ Added dagster-cloud to pyproject.toml")

def ensure_requirements_txt(requirements_path):
    """Ensure dagster-cloud is in requirements.txt."""
    with open(requirements_path, 'r') as f:
        content = f.read()

    lines = content.strip().split('\n')
    has_dagster_cloud = any(
        line.strip() == "dagster-cloud" or
        line.strip().startswith("dagster-cloud==") or
        line.strip().startswith("dagster-cloud>=")
        for line in lines
    )

    if not has_dagster_cloud:
        print(f"📦 Adding dagster-cloud to requirements.txt...")
        new_lines = []
        added = False

        for line in lines:
            new_lines.append(line)
            if line.strip() == "dagster" and not added:
                new_lines.append("dagster-cloud")
                added = True

        if not added:
            new_lines.insert(0, "dagster-cloud")

        with open(requirements_path, 'w') as f:
            f.write('\n'.join(new_lines) + '\n')
        print(f"✅ Added dagster-cloud to requirements.txt")

def update_shared_dagster_cloud_yaml(root_dir, projects, deployment_type="serverless"):
    """Generate shared dagster_cloud.yaml for monorepo."""
    dagster_cloud_content = f"""# Monorepo configuration for {len(projects)} Dagster projects\n"""
    dagster_cloud_content += "locations:\n"

    for project in projects:
        package_name = project['package_name']
        working_dir = project['relative_path']

        dagster_cloud_content += f"  - location_name: {project['name']}\n"
        dagster_cloud_content += f"    code_source:\n"
        dagster_cloud_content += f"      package_name: {package_name}\n"

        if project['working_directory'] != ".":
            dagster_cloud_content += f"    working_directory: {working_dir}/{project['working_directory']}\n"
        else:
            dagster_cloud_content += f"    working_directory: {working_dir}\n"

    dagster_cloud_path = os.path.join(root_dir, "dagster_cloud.yaml")
    with open(dagster_cloud_path, 'w') as f:
        f.write(dagster_cloud_content)

    print(f"✅ Created shared dagster_cloud.yaml at {dagster_cloud_path}")
    return dagster_cloud_path

def generate_github_workflow(workflow_path, deployment_type):
    """Generate GitHub Actions workflow file."""
    import tempfile

    quickstart_repo = SERVERLESS_QUICKSTART_REPO if deployment_type == "serverless" else HYBRID_QUICKSTART_REPO
    workflow_file = "dagster-plus-deploy.yml" if deployment_type == "serverless" else "dagster-cloud-deploy.yml"

    with tempfile.TemporaryDirectory() as temp_dir:
        result = subprocess.run(
            ["git", "clone", "--depth", "1", quickstart_repo, temp_dir],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            source_workflow = os.path.join(temp_dir, ".github", "workflows", workflow_file)
            if os.path.exists(source_workflow):
                os.makedirs(os.path.dirname(workflow_path), exist_ok=True)
                shutil.copy(source_workflow, workflow_path)
                print(f"✅ Generated {os.path.basename(workflow_path)}")
                return True

    print(f"⚠️  Could not generate workflow file")
    return False

def detect_git_provider(project_dir):
    """Detect which Git provider is being used."""
    git_config_path = os.path.join(project_dir, ".git", "config")

    if not os.path.exists(git_config_path):
        return None

    with open(git_config_path, 'r') as f:
        git_config = f.read()

    if "github.com" in git_config:
        return "github"
    elif "gitlab.com" in git_config:
        return "gitlab"
    elif "dev.azure.com" in git_config or "visualstudio.com" in git_config:
        return "azure"
    elif "bitbucket.org" in git_config:
        return "bitbucket"

    return None

def main():
    """Main function for deployment preparation."""
    print("\n🚀 Dagster+ Deployment Preparation")

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
            sys.exit(1)
        project_dir = os.path.abspath(project_dir)

    print(f"📁 Using project directory: {project_dir}")

    # Check if this is a monorepo
    print(f"\n🔍 Analyzing project structure...")
    is_monorepo, projects = detect_monorepo_structure(project_dir)

    # Ask about deployment type
    deploy_type_choice = choose(
        "What type of Dagster+ deployment will you use?",
        ["Serverless", "Hybrid"]
    )
    deployment_type = "serverless" if deploy_type_choice == 1 else "hybrid"

    if is_monorepo:
        print(f"\n📁 Detected monorepo structure!")
        print(f"Found {len(projects)} Dagster projects:")
        for i, project in enumerate(projects, 1):
            indicator = "🧩 Components" if project['is_components'] else "📄 Traditional"
            print(f"   {i}. {project['name']} ({project['relative_path']}) - {indicator}")

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
    else:
        # Single project
        print(f"📁 Single Dagster project detected")
        ensure_dagster_project_files(project_dir)

    # Generate CI/CD workflow
    print(f"\n🔧 Setting up CI/CD workflow for {deployment_type} deployment...")

    if os.path.exists(os.path.join(project_dir, ".git")):
        git_provider = detect_git_provider(project_dir)

        if not git_provider:
            git_provider_choice = choose(
                "Which Git provider are you using?",
                ["GitHub", "GitLab", "Azure DevOps", "Bitbucket", "Other/None"]
            )
            git_provider = ["github", "gitlab", "azure", "bitbucket", None][git_provider_choice - 1]

        if git_provider:
            print(f"✅ Detected Git provider: {git_provider}")

            if git_provider == "github":
                workflow_dir = os.path.join(project_dir, ".github", "workflows")
                workflow_file = "dagster-plus-deploy.yml" if deployment_type == "serverless" else "dagster-cloud-deploy.yml"
                workflow_path = os.path.join(workflow_dir, workflow_file)

                if not os.path.exists(workflow_path):
                    print(f"📄 Generating {workflow_file}...")
                    generate_github_workflow(workflow_path, deployment_type)
                else:
                    print(f"✅ {workflow_file} already exists")
            else:
                print(f"💡 For {git_provider}, please manually create the CI/CD configuration")
                print(f"💡 See: https://docs.dagster.io/dagster-plus/deployment/ci-cd")
    else:
        print(f"⚠️  No Git repository detected")
        print(f"💡 Initialize a Git repository to enable CI/CD workflow generation")

    # Final summary
    print(f"\n✅ Dagster+ preparation completed!")
    print(f"📁 Project directory: {project_dir}")
    print(f"🚀 Deployment type: {deployment_type}")
    print(f"\n📋 Generated/Fixed files:")
    print(f"   • pyproject.toml - Project configuration")
    print(f"   • dagster_cloud.yaml - Dagster+ deployment config")
    print(f"\n🎯 Next steps:")
    print(f"   1. Review the generated files")
    print(f"   2. Set up secrets in your repository (API tokens, etc.)")
    print(f"   3. Commit and push to trigger deployment")
    print(f"   4. Or deploy manually using: python dagster_deploy.py")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Operation cancelled by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
