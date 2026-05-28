#!/usr/bin/env python3
"""
Validate a Duplocloud Terraform module structure and patterns.

Usage:
    python validate_module.py <module-path>
    python validate_module.py modules/myapp
    python validate_module.py .  # Validate all modules in current project

Checks:
    - Required files exist (main.tf, providers.tf)
    - module.ctx is properly configured
    - Backend configuration is present
    - Workspace references follow conventions
    - Outputs are properly defined
"""

import argparse
import re
import sys
from pathlib import Path
from typing import List, Tuple

# Validation results
PASS = "✓"
FAIL = "✗"
WARN = "⚠"


class ValidationResult:
    def __init__(self):
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.passes: List[str] = []

    def error(self, msg: str):
        self.errors.append(msg)

    def warn(self, msg: str):
        self.warnings.append(msg)

    def ok(self, msg: str):
        self.passes.append(msg)

    def is_valid(self) -> bool:
        return len(self.errors) == 0

    def print_summary(self):
        for msg in self.passes:
            print(f"  {PASS} {msg}")
        for msg in self.warnings:
            print(f"  {WARN} {msg}")
        for msg in self.errors:
            print(f"  {FAIL} {msg}")


def read_file_content(path: Path) -> str:
    """Read file content, return empty string if file doesn't exist."""
    if not path.exists():
        return ""
    with open(path, "r") as f:
        return f.read()


def validate_required_files(module_path: Path, result: ValidationResult) -> None:
    """Check that required files exist."""
    required = ["main.tf", "providers.tf"]
    recommended = ["variables.tf", "outputs.tf"]

    for filename in required:
        if (module_path / filename).exists():
            result.ok(f"{filename} exists")
        else:
            result.error(f"Missing required file: {filename}")

    for filename in recommended:
        if (module_path / filename).exists():
            result.ok(f"{filename} exists")
        else:
            result.warn(f"Recommended file missing: {filename}")


def validate_context_module(module_path: Path, result: ValidationResult) -> None:
    """Validate module.ctx configuration."""
    main_tf = read_file_content(module_path / "main.tf")

    # Check for context module
    ctx_pattern = r'module\s+"ctx"\s*\{'
    if re.search(ctx_pattern, main_tf):
        result.ok("module.ctx defined")
    else:
        result.error("Missing module.ctx - required for Duplocloud modules")
        return

    # Check source
    source_pattern = r'source\s*=\s*"duplocloud/components/duplocloud//modules/context"'
    if re.search(source_pattern, main_tf):
        result.ok("module.ctx uses correct source")
    else:
        result.warn("module.ctx source may be incorrect")

    # Check version
    version_pattern = r'version\s*=\s*"([^"]+)"'
    version_match = re.search(version_pattern, main_tf)
    if version_match:
        result.ok(f"module.ctx version: {version_match.group(1)}")
    else:
        result.warn("module.ctx version not pinned")

    # Check admin flag
    admin_pattern = r'admin\s*=\s*(true|false)'
    admin_match = re.search(admin_pattern, main_tf)
    if admin_match:
        result.ok(f"admin = {admin_match.group(1)}")
    else:
        result.warn("admin flag not explicitly set")


def validate_backend(module_path: Path, result: ValidationResult) -> None:
    """Validate backend configuration."""
    providers_tf = read_file_content(module_path / "providers.tf")

    # Check for backend block
    s3_pattern = r'backend\s+"s3"\s*\{'
    gcs_pattern = r'backend\s+"gcs"\s*\{'

    if re.search(s3_pattern, providers_tf):
        result.ok("S3 backend configured")
        # Check for key and workspace_key_prefix
        if re.search(r'key\s*=', providers_tf):
            result.ok("backend key defined")
        else:
            result.error("S3 backend missing 'key' configuration")

        if re.search(r'workspace_key_prefix\s*=', providers_tf):
            result.ok("workspace_key_prefix defined")
        else:
            result.warn("workspace_key_prefix not set - may affect state organization")

        if re.search(r'encrypt\s*=\s*true', providers_tf):
            result.ok("S3 encryption enabled")
        else:
            result.warn("S3 encryption not explicitly enabled")

    elif re.search(gcs_pattern, providers_tf):
        result.ok("GCS backend configured")
        if re.search(r'prefix\s*=', providers_tf):
            result.ok("backend prefix defined")
        else:
            result.error("GCS backend missing 'prefix' configuration")
    else:
        result.error("No backend configuration found (expected s3 or gcs)")


def validate_providers(module_path: Path, result: ValidationResult) -> None:
    """Validate provider configuration."""
    providers_tf = read_file_content(module_path / "providers.tf")

    # Check for duplocloud provider
    if re.search(r'provider\s+"duplocloud"', providers_tf):
        result.ok("duplocloud provider configured")
    else:
        result.error("Missing duplocloud provider")

    # Check for required_providers block
    if re.search(r'required_providers\s*\{', providers_tf):
        result.ok("required_providers block exists")
    else:
        result.warn("required_providers block not found")

    # Check terraform version
    version_pattern = r'required_version\s*=\s*"([^"]+)"'
    version_match = re.search(version_pattern, providers_tf)
    if version_match:
        result.ok(f"Terraform version constraint: {version_match.group(1)}")
    else:
        result.warn("No terraform version constraint")


def validate_workspaces(module_path: Path, result: ValidationResult) -> None:
    """Validate workspace reference patterns."""
    main_tf = read_file_content(module_path / "main.tf")

    # Check for workspaces block
    workspaces_pattern = r'workspaces\s*=\s*\{'
    if re.search(workspaces_pattern, main_tf):
        result.ok("workspaces block defined")

        # Check for common workspace references
        if re.search(r'tenant\s*=\s*\{\s*\}', main_tf):
            result.ok("tenant workspace uses terraform.workspace pattern")
        elif re.search(r'tenant\s*=\s*\{', main_tf):
            result.ok("tenant workspace configured")

        if re.search(r'shared\s*=\s*\{', main_tf):
            result.ok("shared workspace reference found")

        if re.search(r'portal\s*=\s*\{', main_tf):
            result.ok("portal workspace reference found")

        if re.search(r'infra\s*=\s*\{', main_tf):
            result.ok("infra workspace reference found")
    else:
        # Check if tenant is set directly
        if re.search(r'tenant\s*=\s*"', main_tf):
            result.ok("tenant set directly (portal module pattern)")
        else:
            result.warn("No workspaces block - may be missing dependencies")


def validate_outputs(module_path: Path, result: ValidationResult) -> None:
    """Validate output definitions."""
    outputs_tf = read_file_content(module_path / "outputs.tf")

    if not outputs_tf:
        result.warn("No outputs.tf file")
        return

    # Count outputs
    output_count = len(re.findall(r'output\s+"[^"]+"\s*\{', outputs_tf))
    if output_count > 0:
        result.ok(f"{output_count} outputs defined")
    else:
        result.warn("No outputs defined")


def validate_naming(module_path: Path, result: ValidationResult) -> None:
    """Validate naming conventions."""
    module_name = module_path.name

    # Check module name format
    if re.match(r'^[a-z][a-z0-9-]*$', module_name):
        result.ok(f"Module name '{module_name}' follows convention")
    else:
        result.warn(f"Module name '{module_name}' should be lowercase with hyphens")


def validate_module(module_path: Path) -> ValidationResult:
    """Run all validations on a module."""
    result = ValidationResult()

    print(f"\nValidating: {module_path}")
    print("-" * 50)

    validate_required_files(module_path, result)
    validate_context_module(module_path, result)
    validate_backend(module_path, result)
    validate_providers(module_path, result)
    validate_workspaces(module_path, result)
    validate_outputs(module_path, result)
    validate_naming(module_path, result)

    result.print_summary()

    return result


def find_modules(path: Path) -> List[Path]:
    """Find all module directories in a project."""
    modules = []
    modules_dir = path / "modules"

    if modules_dir.exists():
        for item in modules_dir.iterdir():
            if item.is_dir() and (item / "main.tf").exists():
                modules.append(item)
    elif (path / "main.tf").exists():
        # Path is itself a module
        modules.append(path)

    return modules


def main():
    parser = argparse.ArgumentParser(
        description="Validate Duplocloud Terraform module structure"
    )
    parser.add_argument(
        "path",
        nargs="?",
        default=".",
        help="Module path or project root (default: current directory)",
    )
    parser.add_argument(
        "--all",
        "-a",
        action="store_true",
        help="Validate all modules in project",
    )

    args = parser.parse_args()
    path = Path(args.path).resolve()

    if not path.exists():
        print(f"Error: Path does not exist: {path}", file=sys.stderr)
        sys.exit(1)

    if args.all or (path / "modules").exists():
        modules = find_modules(path)
        if not modules:
            print("No modules found to validate", file=sys.stderr)
            sys.exit(1)
    else:
        modules = [path]

    all_valid = True
    for module_path in modules:
        result = validate_module(module_path)
        if not result.is_valid():
            all_valid = False

    print("\n" + "=" * 50)
    if all_valid:
        print(f"{PASS} All validations passed")
        sys.exit(0)
    else:
        print(f"{FAIL} Some validations failed")
        sys.exit(1)


if __name__ == "__main__":
    main()
