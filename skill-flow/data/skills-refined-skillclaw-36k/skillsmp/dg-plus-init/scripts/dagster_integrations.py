#!/usr/bin/env python3
"""
Dagster+ Integrations Setup Script

Adds integration capabilities to Dagster projects:
- dbt (Data Build Tool)
- Airflow (via Dagster Airlift)
- Fivetran (ELT connector)
- Airbyte (Open-source data integration)
- Power BI (Business Intelligence)

Usage:
    python dagster_integrations.py [project_dir]
"""

import os
import sys
import subprocess
from dagster_utils import (
    choose,
    install_python_packages,
    ensure_project_table
)

def setup_dbt_integration(project_dir, pkg_mgr):
    """Set up dbt integration."""
    print("\n🔧 Setting up dbt integration...")

    if choose("Do you want to add dbt integration to your Dagster project?", ["Yes", "No"]) == 2:
        return

    print("\n📋 This will add dbt integration to your Dagster project")

    # Install dependencies
    print("\n📦 Installing dbt dependencies...")
    original_dir = os.getcwd()
    os.chdir(project_dir)

    try:
        ensure_project_table(project_dir)

        if pkg_mgr == 2:  # uv
            subprocess.run(["uv", "add", "dagster-dbt", "dbt-core", "dbt-duckdb"], check=False)
        else:  # pip
            install_python_packages(["dagster-dbt", "dbt-core", "dbt-duckdb"])

        print("\n✅ dbt integration dependencies installed")
        print("\n💡 Next steps:")
        print("   1. Initialize a dbt project: dbt init")
        print("   2. Create a Dagster dbt asset using dagster-dbt components")
        print("   3. See: https://docs.dagster.io/integrations/dbt")

    except Exception as e:
        print(f"❌ Failed to install dbt dependencies: {e}")
    finally:
        os.chdir(original_dir)

def setup_airlift_integration(project_dir, pkg_mgr):
    """Set up Airlift (Airflow migration) integration."""
    print("\n🔧 Setting up Airlift integration...")

    if choose("Do you want to add Airlift (Airflow migration) to your project?", ["Yes", "No"]) == 2:
        return

    print("\n📋 Airlift helps migrate Airflow DAGs to Dagster")

    # Install dependencies
    print("\n📦 Installing Airlift dependencies...")
    original_dir = os.getcwd()
    os.chdir(project_dir)

    try:
        ensure_project_table(project_dir)

        if pkg_mgr == 2:  # uv
            subprocess.run(["uv", "add", "dagster-airlift[core]", "apache-airflow"], check=False)
        else:  # pip
            install_python_packages(["dagster-airlift[core]", "apache-airflow"])

        print("\n✅ Airlift integration dependencies installed")
        print("\n💡 Next steps:")
        print("   1. Point Airlift to your Airflow instance")
        print("   2. Create proxied Dagster assets from Airflow DAGs")
        print("   3. Gradually migrate DAGs to native Dagster")
        print("   4. See: https://docs.dagster.io/integrations/airlift")

    except Exception as e:
        print(f"❌ Failed to install Airlift dependencies: {e}")
    finally:
        os.chdir(original_dir)

def setup_fivetran_integration(project_dir, pkg_mgr):
    """Set up Fivetran integration."""
    print("\n🔧 Setting up Fivetran integration...")

    if choose("Do you want to add Fivetran integration to your project?", ["Yes", "No"]) == 2:
        return

    print("\n📋 Fivetran integration allows you to orchestrate Fivetran connectors")

    # Install dependencies
    print("\n📦 Installing Fivetran dependencies...")
    original_dir = os.getcwd()
    os.chdir(project_dir)

    try:
        ensure_project_table(project_dir)

        if pkg_mgr == 2:  # uv
            subprocess.run(["uv", "add", "dagster-fivetran"], check=False)
        else:  # pip
            install_python_packages(["dagster-fivetran"])

        print("\n✅ Fivetran integration dependencies installed")
        print("\n💡 Next steps:")
        print("   1. Get your Fivetran API key and secret")
        print("   2. Create Fivetran assets using dagster-fivetran")
        print("   3. See: https://docs.dagster.io/integrations/fivetran")

    except Exception as e:
        print(f"❌ Failed to install Fivetran dependencies: {e}")
    finally:
        os.chdir(original_dir)

def setup_airbyte_integration(project_dir, pkg_mgr):
    """Set up Airbyte integration."""
    print("\n🔧 Setting up Airbyte integration...")

    if choose("Do you want to add Airbyte integration to your project?", ["Yes", "No"]) == 2:
        return

    print("\n📋 Airbyte integration allows you to orchestrate Airbyte connections")

    # Install dependencies
    print("\n📦 Installing Airbyte dependencies...")
    original_dir = os.getcwd()
    os.chdir(project_dir)

    try:
        ensure_project_table(project_dir)

        if pkg_mgr == 2:  # uv
            subprocess.run(["uv", "add", "dagster-airbyte"], check=False)
        else:  # pip
            install_python_packages(["dagster-airbyte"])

        print("\n✅ Airbyte integration dependencies installed")
        print("\n💡 Next steps:")
        print("   1. Set up your Airbyte instance (Cloud or OSS)")
        print("   2. Create Airbyte assets using dagster-airbyte")
        print("   3. See: https://docs.dagster.io/integrations/airbyte")

    except Exception as e:
        print(f"❌ Failed to install Airbyte dependencies: {e}")
    finally:
        os.chdir(original_dir)

def setup_powerbi_integration(project_dir, pkg_mgr):
    """Set up Power BI integration."""
    print("\n🔧 Setting up Power BI integration...")

    if choose("Do you want to add Power BI integration to your project?", ["Yes", "No"]) == 2:
        return

    print("\n📋 Power BI integration allows you to manage Power BI assets in Dagster")

    # Install dependencies
    print("\n📦 Installing Power BI dependencies...")
    original_dir = os.getcwd()
    os.chdir(project_dir)

    try:
        ensure_project_table(project_dir)

        if pkg_mgr == 2:  # uv
            subprocess.run(["uv", "add", "dagster-powerbi"], check=False)
        else:  # pip
            install_python_packages(["dagster-powerbi"])

        print("\n✅ Power BI integration dependencies installed")
        print("\n💡 Next steps:")
        print("   1. Get your Power BI credentials (client ID, secret, tenant ID)")
        print("   2. Create Power BI assets using dagster-powerbi")
        print("   3. See: https://docs.dagster.io/integrations/powerbi")

    except Exception as e:
        print(f"❌ Failed to install Power BI dependencies: {e}")
    finally:
        os.chdir(original_dir)

def setup_integrations(project_dir, pkg_mgr):
    """Interactive setup for multiple integrations."""
    print("\n🔌 Dagster Integrations Setup")
    print(f"📁 Project: {project_dir}")

    while True:
        integration_choice = choose(
            "Which integration would you like to add?",
            [
                "dbt (Data Build Tool)",
                "Airlift (Airflow Migration)",
                "Fivetran (ELT Connector)",
                "Airbyte (Data Integration)",
                "Power BI (Business Intelligence)",
                "Done - Exit integrations setup"
            ]
        )

        if integration_choice == 1:
            setup_dbt_integration(project_dir, pkg_mgr)
        elif integration_choice == 2:
            setup_airlift_integration(project_dir, pkg_mgr)
        elif integration_choice == 3:
            setup_fivetran_integration(project_dir, pkg_mgr)
        elif integration_choice == 4:
            setup_airbyte_integration(project_dir, pkg_mgr)
        elif integration_choice == 5:
            setup_powerbi_integration(project_dir, pkg_mgr)
        else:
            print("\n✅ Integration setup complete!")
            break

def main():
    """Main function for integrations setup."""
    print("\n🚀 Dagster+ Integrations Setup")

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

    # Get package manager preference
    pkg_mgr = choose("Choose your Python package manager:", ["pip", "uv"])

    # Run integration setup
    setup_integrations(project_dir, pkg_mgr)

    print(f"\n✅ All integrations have been configured!")
    print(f"💡 Don't forget to run `dagster dev` to test your integrations locally")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Operation cancelled by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
