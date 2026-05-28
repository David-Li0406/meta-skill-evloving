#!/usr/bin/env python3
"""
Initialize a new Duplocloud Terraform module.

Usage:
    python init_module.py <module-name> --type <module-type> [--cloud <aws|gcp>] [--path <output-path>]

Examples:
    python init_module.py myapp --type app --cloud aws
    python init_module.py myapp --type app --cloud gcp --path ./modules
    python init_module.py operators --type operators --cloud aws
"""

import argparse
import os
import sys
from pathlib import Path

# Template placeholders
PLACEHOLDERS = {
    "{{APP_NAME}}": "",
    "{{CTX_VERSION}}": "0.0.41",
    "{{WORKSPACE_NAME}}": "dev01",
    "{{MODULE_NAME}}": "",
    "{{MODULE_DISPLAY_NAME}}": "",
}

MODULE_TYPES = ["app", "tenant", "shared", "infrastructure", "portal", "operators"]
CLOUD_PROVIDERS = ["aws", "gcp"]


def get_script_dir() -> Path:
    """Get the directory where this script is located."""
    return Path(__file__).parent.resolve()


def get_assets_dir() -> Path:
    """Get the assets directory relative to script location."""
    return get_script_dir().parent / "assets"


def replace_placeholders(content: str, replacements: dict) -> str:
    """Replace all placeholders in content."""
    for placeholder, value in replacements.items():
        content = content.replace(placeholder, value)
    return content


def copy_template_file(
    src: Path, dest: Path, replacements: dict, rename_map: dict = None
) -> None:
    """Copy a template file with placeholder replacement."""
    if not src.exists():
        return

    # Handle file renaming
    dest_name = dest.name
    if rename_map:
        for old_name, new_name in rename_map.items():
            if dest_name == old_name:
                dest = dest.parent / new_name
                break

    # Skip .template files if a non-template version exists
    if dest.name.endswith(".template"):
        return

    dest.parent.mkdir(parents=True, exist_ok=True)

    with open(src, "r") as f:
        content = f.read()

    content = replace_placeholders(content, replacements)

    with open(dest, "w") as f:
        f.write(content)

    print(f"  Created: {dest}")


def init_app_module(
    name: str, output_path: Path, cloud: str, replacements: dict
) -> None:
    """Initialize an app module."""
    assets_dir = get_assets_dir()
    app_assets = assets_dir / "app"
    module_dir = output_path / "modules" / name
    config_dir = output_path / "config" / name / "dev01"
    workflow_dir = output_path / ".github" / "workflows"

    # Provider file based on cloud
    provider_file = f"providers-{cloud}.tf"
    rename_map = {provider_file: "providers.tf"}

    # Copy module files
    for src_file in app_assets.iterdir():
        if src_file.is_file():
            # Skip the other cloud provider file
            if src_file.name.startswith("providers-") and src_file.name != provider_file:
                continue
            dest_file = module_dir / src_file.name
            copy_template_file(src_file, dest_file, replacements, rename_map)

    # Create config directory with tfvars
    config_dir.mkdir(parents=True, exist_ok=True)
    tfvars_content = f"# {name} configuration for dev01\n"
    tfvars_path = config_dir / f"{name}.tfvars"
    with open(tfvars_path, "w") as f:
        f.write(tfvars_content)
    print(f"  Created: {tfvars_path}")

    # Create workflow
    workflow_assets = assets_dir / "workflow"
    workflow_template = workflow_assets / "module.yml.template"
    if workflow_template.exists():
        workflow_dir.mkdir(parents=True, exist_ok=True)
        workflow_dest = workflow_dir / f"{name}.yml"
        copy_template_file(workflow_template, workflow_dest, replacements)


def init_tenant_module(
    name: str, output_path: Path, cloud: str, replacements: dict
) -> None:
    """Initialize a tenant module."""
    assets_dir = get_assets_dir()
    tenant_assets = assets_dir / "tenant"
    module_dir = output_path / "modules" / "tenant"
    config_dir = output_path / "config" / "tenant" / "dev01"

    provider_file = f"providers-{cloud}.tf"
    rename_map = {provider_file: "providers.tf"}

    # Copy module files
    for src_file in tenant_assets.iterdir():
        if src_file.is_file():
            if src_file.name.startswith("providers-") and src_file.name != provider_file:
                continue
            dest_file = module_dir / src_file.name
            copy_template_file(src_file, dest_file, replacements, rename_map)

    # Create config
    config_dir.mkdir(parents=True, exist_ok=True)
    tfvars_template = assets_dir / "config" / "tenant.tfvars"
    if tfvars_template.exists():
        copy_template_file(
            tfvars_template, config_dir / "tenant.tfvars", replacements
        )


def init_shared_module(
    name: str, output_path: Path, cloud: str, replacements: dict
) -> None:
    """Initialize a shared module."""
    assets_dir = get_assets_dir()
    shared_assets = assets_dir / "shared"
    module_dir = output_path / "modules" / "shared"
    config_dir = output_path / "config" / "shared" / "shrd01"

    provider_file = f"providers-{cloud}.tf"
    rename_map = {provider_file: "providers.tf"}

    # Copy module files
    for src_file in shared_assets.iterdir():
        if src_file.is_file():
            if src_file.name.startswith("providers-") and src_file.name != provider_file:
                continue
            dest_file = module_dir / src_file.name
            copy_template_file(src_file, dest_file, replacements, rename_map)

    # Create config
    config_dir.mkdir(parents=True, exist_ok=True)
    tfvars_template = assets_dir / "config" / "shared.tfvars"
    if tfvars_template.exists():
        copy_template_file(
            tfvars_template, config_dir / "shared.tfvars", replacements
        )


def init_base_workflow(output_path: Path) -> None:
    """Initialize the base tf-module.yml workflow."""
    assets_dir = get_assets_dir()
    workflow_assets = assets_dir / "workflow"
    workflow_dir = output_path / ".github" / "workflows"

    base_workflow = workflow_assets / "tf-module.yml"
    if base_workflow.exists():
        workflow_dir.mkdir(parents=True, exist_ok=True)
        dest = workflow_dir / "tf-module.yml"
        if not dest.exists():
            copy_template_file(base_workflow, dest, {})


def main():
    parser = argparse.ArgumentParser(
        description="Initialize a new Duplocloud Terraform module"
    )
    parser.add_argument("name", help="Module name (e.g., myapp)")
    parser.add_argument(
        "--type",
        "-t",
        choices=MODULE_TYPES,
        required=True,
        help="Module type",
    )
    parser.add_argument(
        "--cloud",
        "-c",
        choices=CLOUD_PROVIDERS,
        default="aws",
        help="Cloud provider (default: aws)",
    )
    parser.add_argument(
        "--path",
        "-p",
        default=".",
        help="Output path (default: current directory)",
    )

    args = parser.parse_args()

    output_path = Path(args.path).resolve()
    name = args.name.lower().replace(" ", "-").replace("_", "-")

    # Build replacements
    replacements = PLACEHOLDERS.copy()
    replacements["{{APP_NAME}}"] = name
    replacements["{{MODULE_NAME}}"] = name
    replacements["{{MODULE_DISPLAY_NAME}}"] = name.replace("-", " ").title()

    print(f"\nInitializing {args.type} module: {name}")
    print(f"Cloud: {args.cloud}")
    print(f"Output: {output_path}\n")

    # Always ensure base workflow exists
    init_base_workflow(output_path)

    # Initialize based on type
    if args.type == "app":
        init_app_module(name, output_path, args.cloud, replacements)
    elif args.type == "tenant":
        init_tenant_module(name, output_path, args.cloud, replacements)
    elif args.type == "shared":
        init_shared_module(name, output_path, args.cloud, replacements)
    elif args.type in ["infrastructure", "portal", "operators"]:
        print(f"  Note: {args.type} module templates not yet implemented.")
        print(f"  See references/{args.type}.md for manual setup guidance.")
    else:
        print(f"Unknown module type: {args.type}", file=sys.stderr)
        sys.exit(1)

    print(f"\nModule initialized successfully!")
    print(f"\nNext steps:")
    print(f"  1. Review generated files in modules/{name}/")
    print(f"  2. Customize main.tf with your resources")
    print(f"  3. Run: tf init -chdir=modules/{name}")
    print(f"  4. Run: tf ctx dev01")
    print(f"  5. Run: tf plan -chdir=modules/{name}")


if __name__ == "__main__":
    main()
