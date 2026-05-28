#!/usr/bin/env python3
"""
Analyze Terraform configuration files for validation and dependency patterns.

This script scans .tf files in a directory and identifies:
- Variables without validation blocks
- Resources without appropriate lifecycle settings
- Missing preconditions/postconditions
- Potential use cases for check blocks
"""

import os
import re
import json
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict


@dataclass
class ValidationIssue:
    """Represents a validation or dependency issue found in Terraform code."""

    file: str
    line: int
    severity: str  # "warning", "info", "suggestion"
    category: str  # "validation", "dependency", "lifecycle", "condition", "check"
    message: str
    suggestion: Optional[str] = None


class TerraformAnalyzer:
    """Analyzes Terraform files for validation and dependency patterns."""

    def __init__(self, directory: str):
        self.directory = Path(directory)
        self.issues: List[ValidationIssue] = []
        self.tf_files: List[Path] = []

    def find_tf_files(self) -> List[Path]:
        """Find all .tf files in the directory recursively."""
        tf_files = list(self.directory.rglob("*.tf"))
        self.tf_files = tf_files
        return tf_files

    def analyze(self) -> Dict[str, Any]:
        """Run all analyses and return results."""
        self.find_tf_files()

        for tf_file in self.tf_files:
            with open(tf_file, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\n')

                self._analyze_variables(tf_file, content, lines)
                self._analyze_resources(tf_file, content, lines)
                self._analyze_data_sources(tf_file, content, lines)
                self._analyze_modules(tf_file, content, lines)
                self._check_for_check_blocks(tf_file, content, lines)

        return self._generate_report()

    def _analyze_variables(self, file: Path, content: str, lines: List[str]):
        """Analyze variable blocks for missing validations."""
        # Find all variable blocks
        var_pattern = re.compile(r'variable\s+"([^"]+)"\s*\{', re.MULTILINE)
        validation_pattern = re.compile(r'validation\s*\{', re.MULTILINE)

        for match in var_pattern.finditer(content):
            var_name = match.group(1)
            start_pos = match.start()

            # Find the closing brace for this variable block
            brace_count = 0
            in_block = False
            block_end = start_pos

            for i, char in enumerate(content[start_pos:], start=start_pos):
                if char == '{':
                    brace_count += 1
                    in_block = True
                elif char == '}':
                    brace_count -= 1
                    if in_block and brace_count == 0:
                        block_end = i
                        break

            var_block = content[start_pos:block_end + 1]
            line_num = content[:start_pos].count('\n') + 1

            # Check if validation block exists
            if not validation_pattern.search(var_block):
                # Check if it's a potentially important variable
                if self._is_important_variable(var_name, var_block):
                    self.issues.append(ValidationIssue(
                        file=str(file.relative_to(self.directory)),
                        line=line_num,
                        severity="warning",
                        category="validation",
                        message=f"Variable '{var_name}' lacks validation block",
                        suggestion="Consider adding validation block to ensure input correctness"
                    ))

            # Check for sensitive variables without sensitive flag
            has_sensitive = re.search(r'^\s*sensitive\s*=\s*true', var_block, re.MULTILINE)
            if self._is_sensitive_variable(var_name) and not has_sensitive:
                self.issues.append(ValidationIssue(
                    file=str(file.relative_to(self.directory)),
                    line=line_num,
                    severity="warning",
                    category="validation",
                    message=f"Variable '{var_name}' appears sensitive but lacks 'sensitive = true'",
                    suggestion="Add 'sensitive = true' to protect sensitive values in output"
                ))

    def _analyze_resources(self, file: Path, content: str, lines: List[str]):
        """Analyze resource blocks for lifecycle and condition patterns."""
        resource_pattern = re.compile(r'resource\s+"([^"]+)"\s+"([^"]+)"\s*\{', re.MULTILINE)
        lifecycle_pattern = re.compile(r'lifecycle\s*\{', re.MULTILINE)

        for match in resource_pattern.finditer(content):
            resource_type = match.group(1)
            resource_name = match.group(2)
            start_pos = match.start()

            # Find the closing brace for this resource block
            block_content = self._extract_block(content, start_pos)
            line_num = content[:start_pos].count('\n') + 1

            # Check for lifecycle block
            has_lifecycle = lifecycle_pattern.search(block_content) is not None

            # Check if resource should have lifecycle management
            if self._should_have_lifecycle(resource_type) and not has_lifecycle:
                self.issues.append(ValidationIssue(
                    file=str(file.relative_to(self.directory)),
                    line=line_num,
                    severity="suggestion",
                    category="lifecycle",
                    message=f"Resource '{resource_type}.{resource_name}' may benefit from lifecycle block",
                    suggestion=self._get_lifecycle_suggestion(resource_type)
                ))

            # Check for precondition/postcondition
            has_condition = 'precondition' in block_content or 'postcondition' in block_content

            if self._should_have_conditions(resource_type) and not has_condition:
                self.issues.append(ValidationIssue(
                    file=str(file.relative_to(self.directory)),
                    line=line_num,
                    severity="info",
                    category="condition",
                    message=f"Resource '{resource_type}.{resource_name}' could use precondition/postcondition",
                    suggestion=self._get_condition_suggestion(resource_type)
                ))

    def _analyze_data_sources(self, file: Path, content: str, lines: List[str]):
        """Analyze data source blocks for preconditions."""
        data_pattern = re.compile(r'data\s+"([^"]+)"\s+"([^"]+)"\s*\{', re.MULTILINE)

        for match in data_pattern.finditer(content):
            data_type = match.group(1)
            data_name = match.group(2)
            start_pos = match.start()

            block_content = self._extract_block(content, start_pos)
            line_num = content[:start_pos].count('\n') + 1

            has_precondition = 'precondition' in block_content

            if not has_precondition and self._should_have_data_precondition(data_type):
                self.issues.append(ValidationIssue(
                    file=str(file.relative_to(self.directory)),
                    line=line_num,
                    severity="info",
                    category="condition",
                    message=f"Data source '{data_type}.{data_name}' could use precondition",
                    suggestion="Add precondition to validate data source attributes"
                ))

    def _analyze_modules(self, file: Path, content: str, lines: List[str]):
        """Analyze module blocks for depends_on usage."""
        module_pattern = re.compile(r'module\s+"([^"]+)"\s*\{', re.MULTILINE)

        for match in module_pattern.finditer(content):
            module_name = match.group(1)
            start_pos = match.start()

            block_content = self._extract_block(content, start_pos)
            line_num = content[:start_pos].count('\n') + 1

            has_depends_on = 'depends_on' in block_content

            # This is informational - not necessarily an issue
            if has_depends_on:
                self.issues.append(ValidationIssue(
                    file=str(file.relative_to(self.directory)),
                    line=line_num,
                    severity="info",
                    category="dependency",
                    message=f"Module '{module_name}' uses explicit depends_on",
                    suggestion="Verify if implicit dependencies through output references would suffice"
                ))

    def _check_for_check_blocks(self, file: Path, content: str, lines: List[str]):
        """Check if check blocks exist for infrastructure validation."""
        has_check = re.search(r'check\s+"[^"]+"\s*\{', content) is not None

        # Only suggest check blocks if there are resources but no checks
        has_resources = re.search(r'resource\s+"[^"]+"\s+"[^"]+"\s*\{', content) is not None

        if has_resources and not has_check:
            self.issues.append(ValidationIssue(
                file=str(file.relative_to(self.directory)),
                line=1,
                severity="suggestion",
                category="check",
                message="Consider adding check blocks for infrastructure validation",
                suggestion="Check blocks can validate runtime state after apply"
            ))

    def _extract_block(self, content: str, start_pos: int) -> str:
        """Extract a block from { to matching }."""
        brace_count = 0
        in_block = False

        for i, char in enumerate(content[start_pos:], start=start_pos):
            if char == '{':
                brace_count += 1
                in_block = True
            elif char == '}':
                brace_count -= 1
                if in_block and brace_count == 0:
                    return content[start_pos:i + 1]

        return content[start_pos:]

    def _is_important_variable(self, name: str, block: str) -> bool:
        """Determine if a variable should have validation."""
        # Variables without defaults should have validation
        if 'default' not in block:
            return True

        # Common important variable patterns
        important_patterns = [
            'count', 'size', 'port', 'cidr', 'ip', 'subnet',
            'instance', 'type', 'class', 'tier', 'version',
            'environment', 'region', 'zone', 'name', 'id'
        ]

        return any(pattern in name.lower() for pattern in important_patterns)

    def _is_sensitive_variable(self, name: str) -> bool:
        """Check if variable name suggests sensitive data."""
        sensitive_patterns = [
            'password', 'secret', 'key', 'token', 'credential',
            'api_key', 'auth', 'private', 'cert', 'certificate'
        ]

        return any(pattern in name.lower() for pattern in sensitive_patterns)

    def _should_have_lifecycle(self, resource_type: str) -> bool:
        """Check if resource type should have lifecycle management."""
        # Resources that often need lifecycle management
        lifecycle_types = [
            'aws_autoscaling_group', 'aws_launch_configuration',
            'aws_db_instance', 'aws_rds_cluster',
            'aws_s3_bucket', 'aws_kms_key',
            'aws_instance', 'aws_ecs_service'
        ]

        return any(rt in resource_type for rt in lifecycle_types)

    def _should_have_conditions(self, resource_type: str) -> bool:
        """Check if resource type should have pre/postconditions."""
        # Resources with important state to validate
        condition_types = [
            'aws_db_instance', 'aws_rds_cluster',
            'aws_instance', 'aws_ecs_service',
            'aws_s3_bucket', 'aws_security_group'
        ]

        return any(ct in resource_type for ct in condition_types)

    def _should_have_data_precondition(self, data_type: str) -> bool:
        """Check if data source should have precondition."""
        # Data sources that fetch critical infrastructure
        return 'ami' in data_type or 'image' in data_type

    def _get_lifecycle_suggestion(self, resource_type: str) -> str:
        """Get specific lifecycle suggestion for resource type."""
        if 'autoscaling' in resource_type or 'launch' in resource_type:
            return "Consider 'create_before_destroy = true' to avoid downtime"
        elif 'db' in resource_type or 'rds' in resource_type:
            return "Consider 'prevent_destroy = true' for production databases"
        elif 's3' in resource_type:
            return "Consider 'prevent_destroy = true' and ignore_changes for tags"
        else:
            return "Review lifecycle requirements for this resource type"

    def _get_condition_suggestion(self, resource_type: str) -> str:
        """Get specific condition suggestion for resource type."""
        if 'db' in resource_type or 'rds' in resource_type:
            return "Add postcondition to verify multi_az and backup_retention_period"
        elif 'instance' in resource_type:
            return "Add precondition to verify AMI attributes"
        elif 's3' in resource_type:
            return "Add postcondition to verify encryption and versioning"
        else:
            return "Consider validation requirements for this resource"

    def _generate_report(self) -> Dict[str, Any]:
        """Generate analysis report."""
        # Group issues by category and severity
        by_category = {}
        by_severity = {}

        for issue in self.issues:
            by_category.setdefault(issue.category, []).append(asdict(issue))
            by_severity.setdefault(issue.severity, []).append(asdict(issue))

        return {
            "summary": {
                "total_files": len(self.tf_files),
                "total_issues": len(self.issues),
                "by_severity": {k: len(v) for k, v in by_severity.items()},
                "by_category": {k: len(v) for k, v in by_category.items()},
            },
            "issues": [asdict(issue) for issue in self.issues],
            "by_category": by_category,
            "by_severity": by_severity,
        }


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: analyze_terraform.py <directory>", file=sys.stderr)
        sys.exit(1)

    directory = sys.argv[1]

    if not os.path.isdir(directory):
        print(f"Error: {directory} is not a directory", file=sys.stderr)
        sys.exit(1)

    analyzer = TerraformAnalyzer(directory)
    report = analyzer.analyze()

    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
