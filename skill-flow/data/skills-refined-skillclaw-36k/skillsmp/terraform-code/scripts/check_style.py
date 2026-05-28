#!/usr/bin/env python3
"""
Terraform style compliance checker
Validates HashiCorp style conventions
"""

import sys
import re
from pathlib import Path
from typing import List, Tuple

class StyleViolation:
    def __init__(self, file: str, line: int, message: str, severity: str = "warning"):
        self.file = file
        self.line = line
        self.message = message
        self.severity = severity

    def __str__(self):
        icon = "⚠️" if self.severity == "warning" else "❌"
        return f"{icon} {self.file}:{self.line} - {self.message}"


def check_naming_conventions(content: str, filepath: str) -> List[StyleViolation]:
    """Check for naming convention violations"""
    violations = []

    # Check for hyphens in resource names
    hyphen_pattern = r'(resource|data)\s+"[^"]+"\s+"[^"]*-[^"]*"'
    for i, line in enumerate(content.split('\n'), 1):
        if re.search(hyphen_pattern, line):
            violations.append(StyleViolation(
                filepath, i,
                "Resource/data names should use underscores, not hyphens",
                "error"
            ))

    # Check for redundant resource type in name
    redundant_pattern = r'resource\s+"(\w+)"\s+"[^"]*\1[^"]*"'
    for i, line in enumerate(content.split('\n'), 1):
        match = re.search(redundant_pattern, line)
        if match:
            violations.append(StyleViolation(
                filepath, i,
                f"Resource name contains redundant type '{match.group(1)}'",
                "warning"
            ))

    return violations


def check_indentation(content: str, filepath: str) -> List[StyleViolation]:
    """Check for indentation issues (should be 2 spaces)"""
    violations = []

    for i, line in enumerate(content.split('\n'), 1):
        if line and not line.strip().startswith('#'):
            # Count leading spaces
            leading_spaces = len(line) - len(line.lstrip(' '))
            if leading_spaces > 0 and leading_spaces % 2 != 0:
                violations.append(StyleViolation(
                    filepath, i,
                    f"Indentation should be multiples of 2 spaces (found {leading_spaces})",
                    "error"
                ))

    return violations


def check_variable_descriptions(content: str, filepath: str) -> List[StyleViolation]:
    """Check that variables have type and description"""
    violations = []

    # Find all variable blocks
    variable_blocks = re.finditer(
        r'variable\s+"([^"]+)"\s*\{([^}]+)\}',
        content,
        re.MULTILINE | re.DOTALL
    )

    for match in variable_blocks:
        var_name = match.group(1)
        var_content = match.group(2)
        line_num = content[:match.start()].count('\n') + 1

        if 'type' not in var_content:
            violations.append(StyleViolation(
                filepath, line_num,
                f"Variable '{var_name}' missing type declaration",
                "error"
            ))

        if 'description' not in var_content:
            violations.append(StyleViolation(
                filepath, line_num,
                f"Variable '{var_name}' missing description",
                "error"
            ))

    return violations


def check_output_descriptions(content: str, filepath: str) -> List[StyleViolation]:
    """Check that outputs have descriptions"""
    violations = []

    # Find all output blocks
    output_blocks = re.finditer(
        r'output\s+"([^"]+)"\s*\{([^}]+)\}',
        content,
        re.MULTILINE | re.DOTALL
    )

    for match in output_blocks:
        output_name = match.group(1)
        output_content = match.group(2)
        line_num = content[:match.start()].count('\n') + 1

        if 'description' not in output_content:
            violations.append(StyleViolation(
                filepath, line_num,
                f"Output '{output_name}' missing description",
                "warning"
            ))

    return violations


def check_file_organization(terraform_dir: Path) -> List[StyleViolation]:
    """Check for proper file organization"""
    violations = []

    # Check for recommended file structure
    recommended_files = {
        'variables.tf': 'Variables should be in variables.tf',
        'outputs.tf': 'Outputs should be in outputs.tf',
        'providers.tf': 'Provider configuration should be in providers.tf'
    }

    tf_files = list(terraform_dir.glob('*.tf'))

    for tf_file in tf_files:
        content = tf_file.read_text()

        # Check if variables are in non-variables.tf files
        if tf_file.name != 'variables.tf' and 'variable "' in content:
            violations.append(StyleViolation(
                str(tf_file), 1,
                "Variables should be defined in variables.tf",
                "warning"
            ))

        # Check if outputs are in non-outputs.tf files
        if tf_file.name != 'outputs.tf' and 'output "' in content:
            violations.append(StyleViolation(
                str(tf_file), 1,
                "Outputs should be defined in outputs.tf",
                "warning"
            ))

    return violations


def main():
    if len(sys.argv) < 2:
        print("Usage: check_style.py <terraform_directory>")
        sys.exit(1)

    terraform_dir = Path(sys.argv[1])

    if not terraform_dir.exists():
        print(f"❌ Directory not found: {terraform_dir}")
        sys.exit(1)

    print(f"🔍 Checking Terraform style in: {terraform_dir}\n")

    all_violations = []

    # Check file organization
    all_violations.extend(check_file_organization(terraform_dir))

    # Check individual .tf files
    for tf_file in terraform_dir.glob('*.tf'):
        content = tf_file.read_text()
        filepath = str(tf_file.relative_to(terraform_dir))

        all_violations.extend(check_naming_conventions(content, filepath))
        all_violations.extend(check_indentation(content, filepath))
        all_violations.extend(check_variable_descriptions(content, filepath))
        all_violations.extend(check_output_descriptions(content, filepath))

    # Report violations
    errors = [v for v in all_violations if v.severity == "error"]
    warnings = [v for v in all_violations if v.severity == "warning"]

    if errors:
        print("❌ ERRORS:\n")
        for violation in errors:
            print(f"  {violation}")
        print()

    if warnings:
        print("⚠️  WARNINGS:\n")
        for violation in warnings:
            print(f"  {violation}")
        print()

    if not all_violations:
        print("✅ No style violations found!")
        return 0

    print(f"\n📊 Summary: {len(errors)} errors, {len(warnings)} warnings")

    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
