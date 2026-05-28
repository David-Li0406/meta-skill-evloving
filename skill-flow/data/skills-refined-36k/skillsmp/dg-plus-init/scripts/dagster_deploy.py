#!/usr/bin/env python3
"""
Dagster+ Deployment Script

Deploys Dagster projects to Dagster+ Cloud using:
- Serverless deployment (PEX or Docker)
- Hybrid deployment (requires agent)

Usage:
    python dagster_deploy.py [project_dir]
"""

import os
import sys
import subprocess
import shutil
from dagster_utils import (
    choose,
    get_organization_and_token,
    validate_and_extract_token_info,
    detect_package_name,
    detect_definitions_type,
    detect_virtual_environment,
    get_virtual_env_python,
    detect_python_version,
    has_cmd
)

def generate_dockerfile(project_dir, package_name, python_version="3.11"):
    """Generate a Dockerfile for the project."""
    dockerfile_content = f"""FROM python:{python_version}-slim

WORKDIR /opt/dagster/app

# Copy project files
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -e .

# Expose Dagster webserver port (if needed for local testing)
EXPOSE 3000

# Run Dagster code server
CMD ["dagster", "api", "grpc", "-h", "0.0.0.0", "-p", "4000", "-m", "{package_name}"]
"""

    dockerfile_path = os.path.join(project_dir, "Dockerfile")
    with open(dockerfile_path, 'w') as f:
        f.write(dockerfile_content)

    print(f"✅ Generated Dockerfile")

def start_docker_daemon():
    """Check if Docker is running and start if possible."""
    try:
        result = subprocess.run(
            ["docker", "info"],
            capture_output=True,
            text=True,
            timeout=5
        )

        if result.returncode == 0:
            print(f"✅ Docker daemon is running")
            return True
        else:
            print(f"⚠️  Docker daemon is not running")
            print(f"💡 Please start Docker Desktop or Docker daemon")
            return False
    except Exception:
        print(f"⚠️  Could not connect to Docker")
        return False

def deploy_serverless_pex(project_dir, org_name, deployment_name, location_name, package_name, cli_param_type, cli_param_value, working_dir, api_token):
    """Deploy using serverless PEX method."""
    print(f"🚀 Deploying serverless Python executable (PEX)...")

    # Detect Python version
    python_version = detect_python_version()
    print(f"🐍 Using Python version: {python_version}")

    # Build deploy command
    deploy_cmd = [
        "dagster-cloud", "serverless", "deploy-python-executable",
        ".",
        "--organization", org_name,
        "--deployment", deployment_name,
        "--location-name", location_name,
        f"--{cli_param_type}", cli_param_value,
        "--python-version", python_version
    ]

    if working_dir != ".":
        deploy_cmd.extend(["--working-directory", working_dir])

    # Set up environment
    env = os.environ.copy()
    env["DAGSTER_CLOUD_API_TOKEN"] = api_token

    print(f"Running: {' '.join(deploy_cmd)}")

    deploy_result = subprocess.run(deploy_cmd, capture_output=True, text=True, env=env)

    if deploy_result.returncode == 0:
        print(f"✅ Deployment successful!")
        print(f"🎯 Your code location '{location_name}' is now deployed to Dagster+ Cloud")
        print(f"💡 You can view it at: https://cloud.dagster.io/{org_name}/{deployment_name}")
        return True
    else:
        print(f"❌ Deployment failed!")
        print(f"Error: {deploy_result.stderr}")
        return False

def deploy_serverless_docker(project_dir, org_name, deployment_name, location_name, package_name, cli_param_type, cli_param_value, api_token):
    """Deploy using serverless Docker method."""
    print(f"🐳 Deploying serverless Docker image...")

    # Generate Dockerfile if it doesn't exist
    dockerfile_path = os.path.join(project_dir, "Dockerfile")
    if not os.path.exists(dockerfile_path):
        print(f"📄 Generating Dockerfile...")
        python_version = detect_python_version()
        generate_dockerfile(project_dir, package_name, python_version)
    else:
        print(f"✅ Using existing Dockerfile")

    # Check Docker
    if not has_cmd("docker"):
        print(f"❌ Docker not found but required for Docker deployment")
        print(f"💡 Please install Docker: https://docs.docker.com/get-docker/")
        return False

    if not start_docker_daemon():
        return False

    # Build Docker image
    image_name = f"{org_name}-{deployment_name}-{location_name}".lower()
    print(f"🔨 Building Docker image: {image_name}...")

    build_result = subprocess.run([
        "docker", "build",
        "-t", image_name,
        "."
    ], capture_output=True, text=True)

    if build_result.returncode != 0:
        print(f"❌ Docker build failed!")
        print(f"Error: {build_result.stderr}")
        return False

    print(f"✅ Docker image built successfully!")

    # Deploy
    container_working_dir = "/opt/dagster/app/src" if os.path.exists(os.path.join(project_dir, "src")) else "/opt/dagster/app"

    deploy_cmd = [
        "dagster-cloud", "serverless", "deploy",
        ".",
        "--organization", org_name,
        "--deployment", deployment_name,
        "--location-name", location_name,
        f"--{cli_param_type}", cli_param_value,
        "--working-directory", container_working_dir
    ]

    env = os.environ.copy()
    env["DAGSTER_CLOUD_API_TOKEN"] = api_token

    print(f"Running: {' '.join(deploy_cmd)}")

    deploy_result = subprocess.run(deploy_cmd, capture_output=True, text=True, env=env)

    if deploy_result.returncode == 0:
        print(f"✅ Deployment successful!")
        print(f"🎯 Your code location '{location_name}' is now deployed to Dagster+ Cloud")
        print(f"💡 You can view it at: https://cloud.dagster.io/{org_name}/{deployment_name}")
        return True
    else:
        print(f"❌ Deployment failed!")
        print(f"Error: {deploy_result.stderr}")
        return False

def main():
    """Main function for deployment."""
    print("\n🚀 Dagster+ Cloud Deployment")

    # Get project directory
    project_choice = choose(
        "Where is your Dagster project?",
        ["Current directory", "Specify different directory"]
    )

    if project_choice == 1:
        project_dir = os.getcwd()
    else:
        project_dir = input("Enter the path to your Dagster project: ").strip()
        if not project_dir or not os.path.exists(project_dir):
            print(f"❌ Invalid project directory")
            sys.exit(1)
        project_dir = os.path.abspath(project_dir)

    print(f"📁 Using project directory: {project_dir}")

    # Get credentials
    print(f"\n🔑 Dagster+ Cloud credentials needed for deployment...")
    org_name, api_token = get_organization_and_token()
    if not org_name or not api_token:
        print("❌ Valid credentials required")
        sys.exit(1)

    # Get deployment name
    deployment_name = input("Enter deployment name (or press Enter for default 'prod'): ").strip()
    if not deployment_name:
        deployment_name = "prod"

    # Choose deployment type
    deploy_type = choose(
        "What type of deployment do you want to set up?",
        ["Serverless (recommended for most users)", "Hybrid (self-hosted agent)"]
    )

    # Validate token type
    _, token_type, _, _ = validate_and_extract_token_info(api_token)

    if deploy_type == 1:  # Serverless
        if token_type == "agent":
            print("⚠️  You're using an agent token for serverless deployment")
            print("💡 User tokens are recommended for serverless")

        # Choose build type
        build_type = choose(
            "Choose your serverless deployment method:",
            ["PEX (Python executable - faster, smaller)", "Docker (containerized - more flexible)"]
        )

        # Get deployment details
        project_name = os.path.basename(os.path.abspath(project_dir))
        code_location_name = input(f"Enter code location name [{project_name}]: ").strip() or project_name

        # Detect package name
        package_name, working_dir = detect_package_name(project_dir)
        print(f"💡 Detected package name: {package_name}")

        # Detect project type
        is_components, cli_param_type, cli_param_value = detect_definitions_type(project_dir, package_name, working_dir)

        # Change to project directory
        original_dir = os.getcwd()
        os.chdir(project_dir)

        try:
            if build_type == 1:  # PEX
                success = deploy_serverless_pex(
                    project_dir, org_name, deployment_name, code_location_name,
                    package_name, cli_param_type, cli_param_value, working_dir, api_token
                )
            else:  # Docker
                success = deploy_serverless_docker(
                    project_dir, org_name, deployment_name, code_location_name,
                    package_name, cli_param_type, cli_param_value, api_token
                )

            if not success:
                sys.exit(1)

        finally:
            os.chdir(original_dir)

    else:  # Hybrid
        if token_type == "user":
            print("❌ User tokens cannot be used for hybrid agent setup")
            print("💡 Please use an agent token for hybrid deployments")
            sys.exit(1)

        print(f"\n🔧 Hybrid deployment requires an agent to be set up")
        print(f"💡 Please run: python dagster_agent_setup.py")
        sys.exit(0)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Operation cancelled by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
