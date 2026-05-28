#!/usr/bin/env python3
# Copyright (c) HashiCorp, Inc.
# SPDX-License-Identifier: MPL-2.0

"""
Terraform Provider Test Coverage Analyzer (v2.0)

Enhanced analyzer with:
- Severity classification (CRITICAL/WARNING/INFO/NOISE)
- Domain-specific name allowlists
- Test step type detection
- Smart ID tracking analysis
- Configurable analysis rules
- Context-aware legacy check analysis
- Actionable summary generation

Usage:
    python3 analyze_gap.py <test_directory> [--output report.md] [--config config.yaml]

Example:
    python3 analyze_gap.py ./internal/provider/ --output ./ai_reports/tf_provider_tests_gap.md
"""

import os
import re
import sys
import argparse
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Tuple, Set, Optional, Any
from datetime import datetime
from enum import Enum

# YAML is optional - only needed for custom config files
try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False


# =============================================================================
# CONFIGURATION AND CONSTANTS
# =============================================================================

class FindingSeverity(Enum):
    """Severity levels for findings."""
    CRITICAL = "critical"   # Must fix: security, missing CRUD
    WARNING = "warning"     # Should fix: missing drift/import
    INFO = "info"           # Nice to have: style improvements
    NOISE = "noise"         # False positive, suppress from report


class TestStepType(Enum):
    """Types of test steps."""
    CREATE = "create"
    UPDATE = "update"
    IMPORT = "import"
    IDEMPOTENCY = "idempotency"
    DRIFT = "drift"
    REFRESH = "refresh"
    UNKNOWN = "unknown"


# Domain-specific names that are NOT resource identifiers
DOMAIN_SPECIFIC_NAMES = {
    # Linux network interface names
    'eth0', 'eth1', 'eth2', 'eth3', 'eth4', 'eth5',
    'ens0', 'ens1', 'ens2', 'ens3',
    'enp0s0', 'enp0s1', 'enp0s2', 'enp0s3',
    # Bond interfaces
    'bond0', 'bond1', 'bond2',
    # BMC/IPMI interfaces (BCM-specific)
    'ipmi0', 'ipmi1', 'ilo0', 'ilo1', 'cimc0', 'cimc1', 'drac0', 'drac1', 'rf0', 'rf1',
    # Other common interfaces
    'vlan0', 'vlan1', 'br0', 'br1', 'lo', 'lo0',
    # Virtual interfaces
    'virbr0', 'docker0', 'veth0',
}

# Default configuration
DEFAULT_CONFIG = {
    'rules': {
        'id_tracking': {
            'enabled': True,
            'exclude_step_types': ['idempotency', 'drift', 'refresh'],
            'min_trackable_steps': 2,
        },
        'hardcoded_names': {
            'enabled': True,
            'domain_allowlist': list(DOMAIN_SPECIFIC_NAMES),
            'prefix_allowlist': ['eth', 'bond', 'ipmi', 'ilo', 'cimc', 'drac', 'rf', 'ens', 'enp'],
        },
        'legacy_checks': {
            'enabled': True,
            'ignore_when_modern_exists': True,
            'functional_patterns': ['TestCheckResourceAttrWith'],
        },
        'optional_fields': {
            'enabled': False,  # Disabled by default - over-testing concern
            'report_threshold': 10,  # Only report if >10 untested
        },
        'validation_tests': {
            'enabled': True,
            'required_only': True,  # Only check required fields
        },
    },
    'severity_overrides': {
        'partial_id_tracking': 'info',  # Downgrade from warning
        'legacy_with_modern': 'noise',  # Suppress if modern exists
        'domain_specific_names': 'noise',  # Suppress interface names
    },
}


def load_config(config_path: Optional[str]) -> dict:
    """Load configuration from file or use defaults."""
    config = DEFAULT_CONFIG.copy()

    if config_path and Path(config_path).exists():
        if not HAS_YAML:
            print(f"Warning: PyYAML not installed, ignoring config file: {config_path}")
            print("  Install with: pip install pyyaml")
            return config

        with open(config_path, 'r') as f:
            user_config = yaml.safe_load(f)
            if user_config:
                # Deep merge user config into defaults
                _deep_merge(config, user_config)

    return config


def _deep_merge(base: dict, override: dict) -> dict:
    """Deep merge override into base dict."""
    for key, value in override.items():
        if key in base and isinstance(base[key], dict) and isinstance(value, dict):
            _deep_merge(base[key], value)
        else:
            base[key] = value
    return base


# =============================================================================
# FINDING CLASS
# =============================================================================

class Finding:
    """Represents a single analysis finding."""

    def __init__(
        self,
        finding_type: str,
        severity: FindingSeverity,
        message: str,
        file_name: str = "",
        line_number: int = 0,
        context: Optional[Dict[str, Any]] = None,
    ):
        self.finding_type = finding_type
        self.severity = severity
        self.message = message
        self.file_name = file_name
        self.line_number = line_number
        self.context = context or {}

    def __repr__(self):
        return f"Finding({self.severity.value}: {self.finding_type} - {self.message})"


# =============================================================================
# RESOURCE SCHEMA CLASS
# =============================================================================

class ResourceSchema:
    """Represents parsed resource schema."""

    def __init__(self, path: str):
        self.path = path
        self.name = os.path.basename(path).replace('resource_', '').replace('.go', '')
        self.required_fields = []  # List of (field_name, has_validator)
        self.optional_fields = []  # List of optional field names
        self.content = ""

    def load(self):
        """Load file content."""
        with open(self.path, 'r') as f:
            self.content = f.read()

    def parse_schema(self):
        """Extract required fields and their validators from schema."""
        lines = self.content.split('\n')

        in_nested_object = False
        nested_depth = 0

        for i, line in enumerate(lines):
            # Track when we enter/exit nested objects
            if 'NestedObject:' in line or 'NestedAttributeObject' in line:
                in_nested_object = True
                nested_depth = 0

            # Count braces to track nesting depth
            if in_nested_object:
                nested_depth += line.count('{') - line.count('}')
                if nested_depth <= 0:
                    in_nested_object = False
                    continue

            # Skip fields inside nested objects
            if in_nested_object:
                continue

            # Look for field definitions at top level only
            field_match = re.match(r'\s*"(\w+)":\s*schema\.\w+Attribute\{', line)
            if not field_match:
                continue

            field_name = field_match.group(1)

            # Check next 15 lines for Required: true and Validators
            has_required = False
            has_validator = False

            for j in range(i, min(i + 15, len(lines))):
                check_line = lines[j]

                if 'Required:' in check_line and 'true' in check_line:
                    has_required = True

                if 'Validators:' in check_line:
                    has_validator = True

                if j > i and check_line.strip() == '},':
                    break

            # Check if field is optional
            has_optional = False
            for j in range(i, min(i + 15, len(lines))):
                if 'Optional:' in lines[j] and 'true' in lines[j]:
                    has_optional = True
                    break

            if has_required and has_validator:
                self.required_fields.append((field_name, True))
            elif has_optional and not has_required:
                self.optional_fields.append(field_name)


# =============================================================================
# TEST FILE CLASS
# =============================================================================

class TestFile:
    """Represents a single test file with analysis results."""

    def __init__(self, path: str, config: dict):
        self.path = path
        self.name = os.path.basename(path)
        self.content = ""
        self.config = config

        # Basic metrics
        self.legacy_checks = []  # List of (line_num, pattern, has_modern_equivalent)
        self.modern_state_checks = 0
        self.modern_plan_checks = 0
        self.has_import_test = False
        self.has_drift_test = False
        self.idempotency_checks = 0
        self.compare_value_usage = 0
        self.test_functions = []
        self.is_mock_test = '_mock_test.go' in self.name
        self.is_error_only_test = False
        self.uses_httptest = False
        self.validation_tests = []

        # CRUD operation coverage
        self.has_create_test = False
        self.has_update_test = False
        self.has_delete_test = False

        # Test quality metrics
        self.uses_unique_names = False
        self.uses_env_vars = False
        self.has_precheck = False
        self.has_check_destroy = False
        self.quality_score = 0

        # Cleanup metrics
        self.has_robust_check_destroy = False
        self.uses_cleanup_names = False
        self.cleanup_issues = []

        # Naming issues (with severity awareness)
        self.hardcoded_names = []  # List of (line_number, field, value, severity)
        self.non_unique_patterns = []

        # ID consistency tracking (with step type awareness)
        self.has_compare_value_for_id = False
        self.id_tracking_steps = 0
        self.total_test_steps = 0
        self.trackable_test_steps = 0  # Steps where ID tracking makes sense
        self.test_step_types = []  # List of TestStepType
        self.legacy_id_checks = []
        self.modern_id_checks = 0
        self.id_consistency_issues = []

        # Security
        self.hardcoded_credentials = []

        # Findings with severity
        self.findings: List[Finding] = []

    def load(self):
        """Load file content."""
        with open(self.path, 'r') as f:
            self.content = f.read()

    def analyze(self):
        """Analyze file for patterns."""
        self._find_test_functions()
        self._detect_mock_and_error_tests()
        self._analyze_test_steps()  # New: classify all test steps
        self._find_legacy_checks()
        self._find_modern_patterns()
        self._find_import_tests()
        self._find_drift_tests()
        self._find_idempotency_checks()
        self._find_validation_tests()
        self._analyze_crud_coverage()
        self._analyze_quality_metrics()
        self._analyze_cleanup_patterns()
        self._detect_hardcoded_names()
        self._analyze_id_consistency()
        self._detect_hardcoded_credentials()
        self._calculate_quality_score()
        self._generate_findings()

    def _find_test_functions(self):
        """Extract test function names."""
        pattern = r'func\s+(TestAcc\w+)\s*\('
        self.test_functions = re.findall(pattern, self.content)

    def _detect_mock_and_error_tests(self):
        """Detect if this is a mock server or error-only test file."""
        self.uses_httptest = bool(re.search(r'httptest\.(?:New)?Server', self.content))

        test_steps = re.findall(r'Steps:\s*\[\]resource\.TestStep\{', self.content)

        if test_steps:
            expect_errors = len(re.findall(r'ExpectError:\s*regexp\.MustCompile', self.content))

            if expect_errors >= len(self.test_functions) * 0.8 and self.uses_httptest:
                self.is_error_only_test = True

            if re.search(r'type\s+\w+Scenario\s+string', self.content):
                if re.search(r'scenario\w+Error', self.content) or re.search(r'scenario\w+Failed', self.content):
                    self.is_error_only_test = True

        if self.is_error_only_test:
            self.is_mock_test = True

    def _analyze_test_steps(self):
        """Analyze and classify all test steps."""
        # Find all test step blocks
        # Pattern: look for { followed by Config: or ImportState: or RefreshState:
        step_pattern = r'\{\s*(?:Config:|ImportState:|RefreshState:)'

        # More precise: find TestStep blocks within Steps: []resource.TestStep{...}
        steps_block_pattern = r'Steps:\s*\[\]resource\.TestStep\{(.*?)\},\s*\}\)'

        for match in re.finditer(steps_block_pattern, self.content, re.DOTALL):
            steps_content = match.group(1)
            self._classify_steps_in_block(steps_content)

    def _classify_steps_in_block(self, steps_content: str):
        """Classify individual steps within a Steps block."""
        # Split by step boundaries (roughly: { followed by Config/Import/Refresh)
        # This is a heuristic - Go parsing would be more accurate

        depth = 0
        current_step = []
        in_step = False

        for line in steps_content.split('\n'):
            # Track brace depth
            depth += line.count('{') - line.count('}')

            # Detect step start
            if re.search(r'^\s*\{', line) and depth == 1:
                in_step = True
                current_step = [line]
            elif in_step:
                current_step.append(line)

                # Detect step end
                if depth == 0:
                    step_content = '\n'.join(current_step)
                    step_type = self._classify_single_step(step_content)
                    self.test_step_types.append(step_type)
                    self.total_test_steps += 1

                    # Count trackable steps (where ID tracking makes sense)
                    if step_type in [TestStepType.CREATE, TestStepType.UPDATE, TestStepType.IMPORT]:
                        self.trackable_test_steps += 1

                    in_step = False
                    current_step = []

    def _classify_single_step(self, step_content: str) -> TestStepType:
        """Classify what a single test step is doing."""
        # Import step
        if 'ImportState:' in step_content and 'true' in step_content:
            return TestStepType.IMPORT

        # Refresh step
        if 'RefreshState:' in step_content and 'true' in step_content:
            return TestStepType.REFRESH

        # Idempotency check (ExpectEmptyPlan)
        if 'ExpectEmptyPlan' in step_content:
            return TestStepType.IDEMPOTENCY

        # Drift detection (ExpectNonEmptyPlan)
        if 'ExpectNonEmptyPlan' in step_content:
            return TestStepType.DRIFT

        # Has Config - either CREATE or UPDATE
        if 'Config:' in step_content:
            # First config step is CREATE, but we can't easily tell order here
            # Check for hints in comments or test structure
            if 'Create' in step_content or 'create' in step_content:
                return TestStepType.CREATE
            if 'Update' in step_content or 'update' in step_content:
                return TestStepType.UPDATE
            # Default to CREATE for first, but this is tracked elsewhere
            return TestStepType.CREATE

        return TestStepType.UNKNOWN

    def _find_legacy_checks(self):
        """Find legacy Check blocks with context awareness."""
        legacy_patterns = [
            r'resource\.TestCheckResourceAttr\(',
            r'resource\.TestCheckResourceAttrSet\(',
            r'resource\.TestCheckResourceAttrPair\(',
            r'resource\.TestCheckNoResourceAttr\(',
        ]

        rules = self.config.get('rules', {}).get('legacy_checks', {})
        ignore_when_modern = rules.get('ignore_when_modern_exists', True)
        functional_patterns = rules.get('functional_patterns', ['TestCheckResourceAttrWith'])

        for pattern in legacy_patterns:
            matches = re.finditer(pattern, self.content)
            for match in matches:
                line_num = self.content[:match.start()].count('\n') + 1

                # Check if this is a functional legacy check
                is_functional = self._is_functional_legacy_check(match.start())

                # Check if modern equivalent exists nearby
                has_modern = self._has_modern_equivalent_nearby(line_num) if ignore_when_modern else False

                self.legacy_checks.append((line_num, match.group(), has_modern or is_functional))

    def _is_functional_legacy_check(self, match_start: int) -> bool:
        """Check if legacy check serves a specific purpose that can't be easily replaced."""
        context = self.content[match_start:match_start + 300]

        # TestCheckResourceAttrWith is used for value capture
        if 'TestCheckResourceAttrWith' in context:
            return True

        # Check for variable capture patterns (e.g., storing UUID for later comparison)
        if re.search(r'func\s*\(\s*value\s+string\s*\)', context):
            return True

        return False

    def _has_modern_equivalent_nearby(self, line_num: int) -> bool:
        """Check if modern ConfigStateChecks exist in the same test step."""
        lines = self.content.split('\n')

        # Look within ±30 lines for ConfigStateChecks
        start = max(0, line_num - 30)
        end = min(len(lines), line_num + 30)
        nearby_content = '\n'.join(lines[start:end])

        return 'ConfigStateChecks' in nearby_content and 'statecheck.ExpectKnownValue' in nearby_content

    def _find_modern_patterns(self):
        """Count modern pattern usage."""
        self.modern_state_checks = len(re.findall(r'statecheck\.ExpectKnownValue\(', self.content))
        self.modern_plan_checks = len(re.findall(r'plancheck\.ExpectEmptyPlan\(', self.content))
        self.modern_plan_checks += len(re.findall(r'plancheck\.ExpectNonEmptyPlan\(', self.content))
        self.compare_value_usage = len(re.findall(r'statecheck\.CompareValue\(', self.content))

    def _find_import_tests(self):
        """Check for import test patterns."""
        self.has_import_test = 'ImportState:' in self.content and 'ImportStateVerify:' in self.content

    def _find_drift_tests(self):
        """Check for drift detection test patterns."""
        drift_pattern = r'func\s+TestAcc\w*Drift\w*\s*\('
        self.has_drift_test = bool(re.search(drift_pattern, self.content))

        if not self.has_drift_test:
            self.has_drift_test = 'ExpectNonEmptyPlan' in self.content

    def _find_idempotency_checks(self):
        """Count idempotency verification patterns."""
        self.idempotency_checks = len(re.findall(r'plancheck\.ExpectEmptyPlan\(', self.content))

    def _find_validation_tests(self):
        """Find validation tests using ExpectError."""
        validation_pattern = r'func\s+(TestAcc\w*(?:Validation|Error|Invalid)\w*)\s*\('
        self.validation_tests = re.findall(validation_pattern, self.content)

    def _analyze_crud_coverage(self):
        """Detect CRUD operation test coverage."""
        self.has_create_test = bool(re.search(r'Steps:\s*\[\]resource\.TestStep\{', self.content))
        config_steps = len(re.findall(r'Config:\s+\w+', self.content))
        self.has_update_test = config_steps >= 2
        self.has_delete_test = 'CheckDestroy:' in self.content

    def _analyze_quality_metrics(self):
        """Analyze test quality indicators."""
        self.uses_unique_names = 'generateUniqueTestName' in self.content
        self.uses_env_vars = 'os.Getenv' in self.content
        self.has_precheck = 'PreCheck:' in self.content
        self.has_check_destroy = 'CheckDestroy:' in self.content

    def _analyze_cleanup_patterns(self):
        """Analyze test cleanup patterns and identify issues."""
        if self.has_check_destroy:
            check_destroy_patterns = [
                r'CheckDestroy:\s*testAccCheck\w+Destroy',
                r'verifyResourceDeleted\(',
                r'client\.CallJSONRPC.*remove',
                r'if\s+.*still\s+exists',
            ]

            self.has_robust_check_destroy = any(
                re.search(pattern, self.content)
                for pattern in check_destroy_patterns
            )

            if re.search(r'CheckDestroy:\s*nil', self.content):
                self.cleanup_issues.append("CheckDestroy is nil (no cleanup verification)")
            elif not self.has_robust_check_destroy and self.has_check_destroy:
                self.cleanup_issues.append("CheckDestroy present but may lack verification logic")

        cleanup_name_patterns = [
            r'generateUniqueTestName\(',
            r'citest[-_]',
            r'tftest[-_]',
            r'test-\w+-\d+',
            r'fmt\.Sprintf.*%d.*time\.',
        ]

        self.uses_cleanup_names = any(
            re.search(pattern, self.content)
            for pattern in cleanup_name_patterns
        )

        if self.has_create_test and not self.has_check_destroy and not self.is_error_only_test:
            self.cleanup_issues.append("Creates resources but missing CheckDestroy")

        if not self.uses_cleanup_names and not self.uses_unique_names:
            if re.search(r'name.*=.*"test-.*"', self.content, re.IGNORECASE):
                self.cleanup_issues.append("Uses hardcoded resource names (harder to clean up)")

        if 'createTestBCMClient' in self.content:
            if not self.has_robust_check_destroy:
                self.cleanup_issues.append("Creates external resources via API but cleanup verification unclear")

    def _detect_hardcoded_names(self):
        """Detect hardcoded test resource names with domain-specific awareness."""
        lines = self.content.split('\n')

        if self.is_error_only_test:
            return

        rules = self.config.get('rules', {}).get('hardcoded_names', {})
        domain_allowlist = set(rules.get('domain_allowlist', DOMAIN_SPECIFIC_NAMES))
        prefix_allowlist = rules.get('prefix_allowlist', [])

        in_block_comment = False

        for i, line in enumerate(lines, 1):
            stripped = line.strip()

            if '/*' in line:
                in_block_comment = True
            if '*/' in line:
                in_block_comment = False
                continue

            if in_block_comment or stripped.startswith('//') or stripped.startswith('*'):
                continue

            if any(keyword in stripped for keyword in [
                'Scenario', 'Solution:', 'Before:', 'After:', 'Expected:',
                'Trigger Conditions:', 'User Experience:', 'Recovery Strategy:'
            ]):
                continue

            # Check context for nested structures
            context_start = max(0, i - 10)
            context_lines = lines[context_start:i]
            context = '\n'.join(context_lines)

            if any(pattern in context for pattern in [
                'modules = [', 'storage_classes = jsonencode', 'addons = jsonencode',
                'ingress_controller = jsonencode', 'parameters = {'
            ]):
                continue

            hardcoded_patterns = [
                (r'\bname\s*=\s*"([^"]+)"', 'name'),
                (r'\bhostname\s*=\s*"([^"]+)"', 'hostname'),
                (r'\bimage_name\s*=\s*"([^"]+)"', 'image_name'),
            ]

            if re.search(r'"\s*\+\s*\w+\s*\+\s*"', line):
                continue

            if '`' in line and '+' in line:
                continue

            for pattern, field in hardcoded_patterns:
                matches = re.finditer(pattern, line)
                for match in matches:
                    value = match.group(1)

                    if '%' in value or '$' in value or '{' in value:
                        continue

                    if value.startswith('.') or value.startswith('_'):
                        continue

                    # Check domain-specific allowlist
                    if value.lower() in domain_allowlist:
                        continue

                    # Check prefix allowlist
                    if any(value.lower().startswith(prefix) for prefix in prefix_allowlist):
                        continue

                    if any(keyword in value for keyword in [
                        'localhost', 'example', 'base', 'default', 'node',
                        'proxy', 'direct', 'standard', 'fast', 'prometheus'
                    ]):
                        continue

                    extended_context_start = max(0, i - 5)
                    extended_context = '\n'.join(lines[extended_context_start:i])

                    if f'"{value}"' in extended_context and 'generateUniqueTestName' in extended_context:
                        continue

                    if re.search(rf'\w+\s*:=.*"{re.escape(value)}".*generateUniqueTestName', extended_context):
                        continue

                    # Determine severity
                    if value.startswith('tftest-') or value.startswith('citest-'):
                        severity = FindingSeverity.INFO  # Has prefix, just informational
                    else:
                        severity = FindingSeverity.WARNING  # Missing unique prefix

                    self.hardcoded_names.append((i, field, value, severity))
                    self.non_unique_patterns.append(f"Line {i}: {field} = \"{value}\"")

    def _analyze_id_consistency(self):
        """Analyze ID property usage with step type awareness."""
        if 'data_source_' in self.name:
            return

        if self.is_error_only_test:
            return

        # Check for CompareValue usage for ID tracking
        compare_value_id_pattern = r'compareID\s*:=\s*statecheck\.CompareValue\(compare\.ValuesSame\(\)\)'
        self.has_compare_value_for_id = bool(re.search(compare_value_id_pattern, self.content))

        # Count steps with ID tracking via AddStateValue
        add_state_id_pattern = r'compareID\.AddStateValue\s*\(\s*[^)]+,\s*tfjsonpath\.New\s*\(\s*"id"\s*\)'
        self.id_tracking_steps = len(re.findall(add_state_id_pattern, self.content))

        # Find legacy ID checks
        legacy_id_patterns = [
            r'resource\.TestCheckResourceAttr\s*\([^,]+,\s*"id"',
            r'resource\.TestCheckResourceAttrSet\s*\([^,]+,\s*"id"',
        ]
        for pattern in legacy_id_patterns:
            matches = re.finditer(pattern, self.content)
            for match in matches:
                line_num = self.content[:match.start()].count('\n') + 1
                self.legacy_id_checks.append((line_num, match.group()))

        # Count modern ID checks
        modern_id_pattern = r'tfjsonpath\.New\s*\(\s*"id"\s*\)'
        self.modern_id_checks = len(re.findall(modern_id_pattern, self.content))

        # Identify issues with step-type awareness
        self._identify_id_consistency_issues()

    def _identify_id_consistency_issues(self):
        """Identify specific ID consistency problems with smart filtering."""
        rules = self.config.get('rules', {}).get('id_tracking', {})
        min_trackable = rules.get('min_trackable_steps', 2)

        # Issue 1: Uses legacy ID checks (only if no modern equivalent)
        legacy_without_modern = [
            check for check in self.legacy_id_checks
            if not self._has_modern_equivalent_nearby(check[0])
        ]
        if legacy_without_modern:
            self.id_consistency_issues.append({
                'type': 'legacy_id_checks',
                'severity': FindingSeverity.INFO,
                'message': f"Uses legacy ID checks ({len(legacy_without_modern)} occurrences) - migrate to statecheck.ExpectKnownValue",
                'count': len(legacy_without_modern),
            })

        # Issue 2: Multiple trackable steps but no ID tracking
        # Only flag if there are enough trackable steps (Create + Import + Update)
        if self.trackable_test_steps >= min_trackable and not self.has_compare_value_for_id:
            self.id_consistency_issues.append({
                'type': 'missing_id_tracking',
                'severity': FindingSeverity.INFO,  # Downgraded - often not critical
                'message': f"Multiple trackable steps ({self.trackable_test_steps}) without ID consistency tracking",
                'count': self.trackable_test_steps,
            })

        # Issue 3: Partial ID tracking - only flag if significantly incomplete
        if self.has_compare_value_for_id and self.id_tracking_steps > 0:
            # Compare against trackable steps, not total steps
            if self.trackable_test_steps > 0:
                tracking_ratio = self.id_tracking_steps / self.trackable_test_steps

                # Only flag if less than 50% of trackable steps are tracked
                if tracking_ratio < 0.5:
                    self.id_consistency_issues.append({
                        'type': 'partial_id_tracking',
                        'severity': FindingSeverity.INFO,  # Low severity - often acceptable
                        'message': f"Partial ID tracking: {self.id_tracking_steps}/{self.trackable_test_steps} trackable steps",
                        'count': self.trackable_test_steps - self.id_tracking_steps,
                    })

        # Issue 4: No ID verification at all in resource tests (only for non-mock)
        if (self.trackable_test_steps > 0 and
            self.modern_id_checks == 0 and
            len(self.legacy_id_checks) == 0 and
            'resource_' in self.name and
            not self.is_mock_test):
            self.id_consistency_issues.append({
                'type': 'no_id_verification',
                'severity': FindingSeverity.WARNING,
                'message': "No ID verification in any test step - resources should verify ID persistence",
                'count': 0,
            })

    def _detect_hardcoded_credentials(self):
        """Detect hardcoded credentials, secrets, and sensitive values."""
        lines = self.content.split('\n')
        in_block_comment = False

        credential_patterns = [
            (r'password\s*[=:]\s*["\']([^"\']{4,})["\']', 'password', 'critical'),
            (r'passwd\s*[=:]\s*["\']([^"\']{4,})["\']', 'password', 'critical'),
            (r'pwd\s*[=:]\s*["\']([^"\']{4,})["\']', 'password', 'critical'),
            (r'api[_-]?key\s*[=:]\s*["\']([^"\']{8,})["\']', 'api_key', 'critical'),
            (r'apikey\s*[=:]\s*["\']([^"\']{8,})["\']', 'api_key', 'critical'),
            (r'secret[_-]?key\s*[=:]\s*["\']([^"\']{8,})["\']', 'secret_key', 'critical'),
            (r'access[_-]?key\s*[=:]\s*["\']([^"\']{8,})["\']', 'access_key', 'critical'),
            (r'auth[_-]?token\s*[=:]\s*["\']([^"\']{8,})["\']', 'auth_token', 'critical'),
            (r'bearer\s+([A-Za-z0-9_-]{20,})', 'bearer_token', 'critical'),
            (r'AKIA[0-9A-Z]{16}', 'aws_access_key', 'critical'),
            (r'aws[_-]?secret[_-]?access[_-]?key\s*[=:]\s*["\']([^"\']{20,})["\']', 'aws_secret_key', 'critical'),
            (r'-----BEGIN\s+(?:RSA\s+)?PRIVATE\s+KEY-----', 'private_key', 'critical'),
            (r'-----BEGIN\s+OPENSSH\s+PRIVATE\s+KEY-----', 'ssh_private_key', 'critical'),
            (r'://[^:]+:([^@]{4,})@', 'connection_string_password', 'critical'),
            (r'endpoint\s*[=:]\s*["\']https?://(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})[:\d]*["\']', 'hardcoded_ip', 'warning'),
            (r'secret\s*[=:]\s*["\']([^"\']{8,})["\']', 'secret', 'warning'),
            (r'credential\s*[=:]\s*["\']([^"\']{8,})["\']', 'credential', 'warning'),
        ]

        safe_patterns = [
            r'os\.Getenv\s*\(\s*["\']',
            r'\$\{?\w+\}?',
            r'%\[\d+\]',
            r'%[sqvd]',
        ]

        for i, line in enumerate(lines, 1):
            stripped = line.strip()

            if '/*' in line:
                in_block_comment = True
            if '*/' in line:
                in_block_comment = False
                continue

            if in_block_comment or stripped.startswith('//'):
                continue

            if any(re.search(pattern, line) for pattern in safe_patterns):
                continue

            for pattern, cred_type, severity in credential_patterns:
                matches = re.finditer(pattern, line, re.IGNORECASE)
                for match in matches:
                    value = match.group(1) if match.lastindex else match.group(0)

                    placeholder_indicators = [
                        'example', 'placeholder', 'changeme', 'xxx', 'yyy', 'zzz',
                        'your-', 'my-', 'test', 'dummy', 'fake', 'mock', 'sample',
                        '...', '***', '${', '%[', '%s', '%q', '<', '>'
                    ]
                    if any(ind in value.lower() for ind in placeholder_indicators):
                        continue

                    if re.match(r'^[a-z_]+$', value) and len(value) < 20:
                        continue

                    if len(value.strip()) < 4:
                        continue

                    if cred_type == 'hardcoded_ip':
                        if re.match(r'^(127\.|10\.|192\.168\.|172\.(1[6-9]|2[0-9]|3[01])\.)', value):
                            severity = 'info'

                    self.hardcoded_credentials.append((i, cred_type, value[:50], severity))

    def _calculate_quality_score(self):
        """Calculate overall quality score (0-100)."""
        if self.is_error_only_test:
            score = 0
            if len(self.test_functions) > 0:
                score += 40
            if self.uses_httptest:
                score += 30
            if len(self.legacy_checks) == 0:
                score += 20
            if self.has_precheck:
                score += 10
            self.quality_score = score
            return

        score = 0

        # Modern patterns (40 points)
        if self.modern_state_checks > 0:
            score += 20
        if self.modern_plan_checks > 0:
            score += 10
        # Only penalize legacy if no modern equivalent
        actionable_legacy = [lc for lc in self.legacy_checks if not lc[2]]
        if len(actionable_legacy) == 0:
            score += 10

        # CRUD coverage (20 points)
        if self.has_create_test:
            score += 5
        if self.has_update_test:
            score += 5
        if self.has_delete_test:
            score += 10

        # Test completeness (20 points)
        if self.has_import_test:
            score += 10
        if self.has_drift_test or self.is_mock_test:
            score += 10

        # Quality practices (20 points)
        if self.uses_unique_names or self.uses_cleanup_names:
            score += 5
        if self.uses_env_vars:
            score += 5
        if self.has_precheck:
            score += 5
        if self.has_robust_check_destroy:
            score += 5
        elif self.has_check_destroy:
            score += 2

        # Reduced penalties for non-critical issues
        if not self.is_mock_test:
            cleanup_penalty = min(len(self.cleanup_issues) * 2, 10)  # Reduced from 3/15
            score = max(0, score - cleanup_penalty)

        # Only penalize hardcoded names without tftest/citest prefix
        critical_names = [n for n in self.hardcoded_names if n[3] == FindingSeverity.WARNING]
        if critical_names:
            naming_penalty = min(len(critical_names) * 3, 15)  # Reduced
            score = max(0, score - naming_penalty)

        # Only penalize critical ID issues
        critical_id_issues = [i for i in self.id_consistency_issues
                             if i.get('severity') == FindingSeverity.WARNING]
        if 'resource_' in self.name and critical_id_issues:
            id_penalty = min(len(critical_id_issues) * 5, 10)
            score = max(0, score - id_penalty)

        # Bonus for proper ID consistency tracking
        if self.has_compare_value_for_id and self.id_tracking_steps > 0:
            score = min(100, score + 5)

        # Severe penalty for hardcoded credentials
        critical_creds = [c for c in self.hardcoded_credentials if c[3] == 'critical']
        if critical_creds:
            cred_penalty = min(len(critical_creds) * 20, 50)
            score = max(0, score - cred_penalty)

        self.quality_score = score

    def _generate_findings(self):
        """Generate all findings with appropriate severity."""
        # Legacy checks
        actionable_legacy = [lc for lc in self.legacy_checks if not lc[2]]
        if actionable_legacy:
            self.findings.append(Finding(
                finding_type='legacy_checks',
                severity=FindingSeverity.INFO,  # Downgraded - often not critical
                message=f"{len(actionable_legacy)} legacy check calls without modern equivalent",
                file_name=self.name,
                context={'count': len(actionable_legacy), 'lines': [lc[0] for lc in actionable_legacy[:5]]}
            ))

        # Hardcoded names (only WARNING severity)
        critical_names = [n for n in self.hardcoded_names if n[3] == FindingSeverity.WARNING]
        if critical_names:
            self.findings.append(Finding(
                finding_type='hardcoded_names',
                severity=FindingSeverity.WARNING,
                message=f"{len(critical_names)} hardcoded resource names without unique prefix",
                file_name=self.name,
                context={'names': [(n[0], n[1], n[2]) for n in critical_names[:5]]}
            ))

        # ID consistency (use stored severity)
        for issue in self.id_consistency_issues:
            self.findings.append(Finding(
                finding_type=issue['type'],
                severity=issue['severity'],
                message=issue['message'],
                file_name=self.name,
            ))

        # Missing tests (resource only)
        if 'resource_' in self.name and not self.is_mock_test:
            if not self.has_import_test:
                self.findings.append(Finding(
                    finding_type='missing_import',
                    severity=FindingSeverity.WARNING,
                    message="Missing import test",
                    file_name=self.name,
                ))
            if not self.has_drift_test:
                self.findings.append(Finding(
                    finding_type='missing_drift',
                    severity=FindingSeverity.WARNING,
                    message="Missing drift detection test",
                    file_name=self.name,
                ))

        # Credentials
        critical_creds = [c for c in self.hardcoded_credentials if c[3] == 'critical']
        if critical_creds:
            self.findings.append(Finding(
                finding_type='hardcoded_credentials',
                severity=FindingSeverity.CRITICAL,
                message=f"{len(critical_creds)} hardcoded credentials",
                file_name=self.name,
                context={'credentials': critical_creds[:3]}
            ))


# =============================================================================
# GAP ANALYZER CLASS
# =============================================================================

class GapAnalyzer:
    """Analyzes test directory for modernization gaps."""

    def __init__(self, test_dir: str, config: dict):
        self.test_dir = Path(test_dir)
        self.config = config
        self.resource_tests: List[TestFile] = []
        self.data_source_tests: List[TestFile] = []
        self.other_tests: List[TestFile] = []
        self.resource_schemas: Dict[str, ResourceSchema] = {}
        self.validation_coverage: Dict[str, List[str]] = {}
        self.optional_field_coverage: Dict[str, List[str]] = {}
        self.codebase_stats: Dict[str, Dict] = {}

        # Aggregated findings
        self.all_findings: List[Finding] = []
        self.suppressed_findings: List[Finding] = []

    def scan(self):
        """Scan directory for test files and resource schemas."""
        if not self.test_dir.exists():
            print(f"Error: Directory {self.test_dir} does not exist")
            sys.exit(1)

        # Scan test files
        for file_path in self.test_dir.glob('*_test.go'):
            test_file = TestFile(str(file_path), self.config)
            test_file.load()
            test_file.analyze()

            if 'resource_' in test_file.name:
                self.resource_tests.append(test_file)
            elif 'data_source_' in test_file.name:
                self.data_source_tests.append(test_file)
            else:
                self.other_tests.append(test_file)

        # Scan resource schema files
        for file_path in self.test_dir.glob('resource_*.go'):
            if '_test.go' in str(file_path):
                continue

            schema = ResourceSchema(str(file_path))
            schema.load()
            schema.parse_schema()

            if schema.required_fields:
                self.resource_schemas[schema.name] = schema

        # Analyze validation coverage
        self._analyze_validation_coverage()

        # Only analyze optional fields if enabled
        if self.config.get('rules', {}).get('optional_fields', {}).get('enabled', False):
            self._analyze_optional_field_coverage()

        # Analyze codebase line counts
        self._analyze_codebase_lines()

        # Aggregate and classify findings
        self._aggregate_findings()

    def _aggregate_findings(self):
        """Aggregate findings from all test files and classify by severity."""
        for test in self.resource_tests + self.data_source_tests:
            for finding in test.findings:
                if finding.severity == FindingSeverity.NOISE:
                    self.suppressed_findings.append(finding)
                else:
                    self.all_findings.append(finding)

    def _analyze_optional_field_coverage(self):
        """Check which optional fields are never tested."""
        for schema_name, schema in self.resource_schemas.items():
            if not schema.optional_fields:
                continue

            matching_tests = [t for t in self.resource_tests
                            if schema_name in t.name.replace('_test.go', '')]

            if not matching_tests:
                self.optional_field_coverage[schema_name] = schema.optional_fields
                continue

            all_test_content = '\n'.join(t.content for t in matching_tests)

            untested_fields = []
            for field_name in schema.optional_fields:
                field_lower = field_name.lower()
                field_no_underscore = field_lower.replace('_', '')
                test_content_lower = all_test_content.lower()
                test_content_no_underscore = test_content_lower.replace('_', '')

                config_pattern_match = (
                    f'{field_lower} =' in test_content_lower or
                    f'{field_lower}:' in test_content_lower or
                    f'"{field_lower}"' in test_content_lower or
                    f'({field_lower})' in test_content_lower
                )

                no_underscore_match = (
                    field_no_underscore in test_content_no_underscore
                )

                field_tested = config_pattern_match or no_underscore_match

                if not field_tested:
                    untested_fields.append(field_name)

            # Only report if above threshold
            threshold = self.config.get('rules', {}).get('optional_fields', {}).get('report_threshold', 10)
            if len(untested_fields) >= threshold:
                self.optional_field_coverage[schema_name] = untested_fields

    def _analyze_validation_coverage(self):
        """Cross-reference required fields with validation tests."""
        if not self.config.get('rules', {}).get('validation_tests', {}).get('enabled', True):
            return

        for schema_name, schema in self.resource_schemas.items():
            matching_tests = [t for t in self.resource_tests
                            if schema_name in t.name.replace('_test.go', '')]

            if not matching_tests:
                self.validation_coverage[schema_name] = [f[0] for f in schema.required_fields]
                continue

            all_validation_tests = []
            for test_file in matching_tests:
                all_validation_tests.extend(test_file.validation_tests)

            missing_validations = []
            for field_name, has_validator in schema.required_fields:
                field_lower = field_name.lower()
                field_no_underscore = field_lower.replace('_', '')

                field_tested = any(
                    field_lower in test_name.lower() or
                    field_no_underscore in test_name.lower().replace('_', '')
                    for test_name in all_validation_tests
                )

                if has_validator and not field_tested:
                    missing_validations.append(field_name)

            if missing_validations:
                self.validation_coverage[schema_name] = missing_validations

    def _analyze_codebase_lines(self):
        """Analyze line counts for Go files in the internal directory."""
        internal_dir = self.test_dir.parent
        if internal_dir.name != 'internal':
            if self.test_dir.name == 'provider' and internal_dir.name == 'internal':
                pass
            else:
                for parent in self.test_dir.parents:
                    if parent.name == 'internal':
                        internal_dir = parent
                        break
                    internal_internal = parent / 'internal'
                    if internal_internal.exists():
                        internal_dir = internal_internal
                        break

        if not internal_dir.exists():
            return

        stats = {
            'total': {'files': 0, 'lines': 0, 'code_lines': 0, 'comment_lines': 0, 'blank_lines': 0},
            'by_type': {
                'resource': {'files': 0, 'lines': 0, 'code_lines': 0},
                'data_source': {'files': 0, 'lines': 0, 'code_lines': 0},
                'test': {'files': 0, 'lines': 0, 'code_lines': 0},
                'other': {'files': 0, 'lines': 0, 'code_lines': 0},
            },
            'by_extension': {},
        }

        for root, dirs, files in os.walk(internal_dir):
            dirs[:] = [d for d in dirs if not d.startswith('.') and d != 'vendor']

            for filename in files:
                file_path = Path(root) / filename
                ext = file_path.suffix

                if ext != '.go':
                    if ext not in stats['by_extension']:
                        stats['by_extension'][ext] = {'files': 0, 'lines': 0}
                    try:
                        with open(file_path, 'r', errors='ignore') as f:
                            line_count = sum(1 for _ in f)
                        stats['by_extension'][ext]['files'] += 1
                        stats['by_extension'][ext]['lines'] += line_count
                    except:
                        pass
                    continue

                try:
                    with open(file_path, 'r', errors='ignore') as f:
                        content = f.read()
                        lines = content.split('\n')
                except:
                    continue

                total_lines = len(lines)
                blank_lines = sum(1 for line in lines if not line.strip())
                comment_lines = 0
                in_block_comment = False

                for line in lines:
                    stripped = line.strip()
                    if in_block_comment:
                        comment_lines += 1
                        if '*/' in stripped:
                            in_block_comment = False
                    elif stripped.startswith('//'):
                        comment_lines += 1
                    elif stripped.startswith('/*'):
                        comment_lines += 1
                        if '*/' not in stripped:
                            in_block_comment = True

                code_lines = total_lines - blank_lines - comment_lines

                stats['total']['files'] += 1
                stats['total']['lines'] += total_lines
                stats['total']['code_lines'] += code_lines
                stats['total']['comment_lines'] += comment_lines
                stats['total']['blank_lines'] += blank_lines

                if ext not in stats['by_extension']:
                    stats['by_extension'][ext] = {'files': 0, 'lines': 0}
                stats['by_extension'][ext]['files'] += 1
                stats['by_extension'][ext]['lines'] += total_lines

                fname = filename.lower()
                if '_test.go' in fname:
                    category = 'test'
                elif fname.startswith('resource_'):
                    category = 'resource'
                elif fname.startswith('data_source_'):
                    category = 'data_source'
                else:
                    category = 'other'

                stats['by_type'][category]['files'] += 1
                stats['by_type'][category]['lines'] += total_lines
                stats['by_type'][category]['code_lines'] += code_lines

        self.codebase_stats = stats

    def generate_report(self) -> str:
        """Generate markdown gap analysis report."""
        report = []
        report.append("# Terraform Provider Test Modernization Gap Analysis\n")
        report.append(f"**Analysis Date:** {self._get_date()}\n")
        report.append(f"**Test Directory:** `{self.test_dir}`\n")
        report.append(f"**Analyzer Version:** 2.0 (with severity classification)\n")

        # Actionable Summary (NEW)
        report.append("\n## Actionable Summary\n")
        report.append(self._generate_actionable_summary())

        # Codebase statistics
        if self.codebase_stats and self.codebase_stats.get('total', {}).get('files', 0) > 0:
            report.append("\n## Codebase Statistics\n")
            report.append(self._generate_codebase_stats())

        # Executive Summary
        report.append("\n## Executive Summary\n")
        report.append(self._generate_executive_summary())

        # Detailed analysis
        report.append("\n## Resource Tests Analysis\n")
        report.append(self._analyze_category(self.resource_tests, "Resource"))

        report.append("\n## Data Source Tests Analysis\n")
        report.append(self._analyze_category(self.data_source_tests, "Data Source"))

        # Gaps and recommendations
        report.append("\n## Gaps and Recommendations\n")
        report.append(self._generate_recommendations())

        # Pattern reference
        report.append("\n## Modern Testing Patterns Quick Reference\n")
        report.append(self._pattern_reference())

        return ''.join(report)

    def _generate_actionable_summary(self) -> str:
        """Generate summary showing only actionable items by severity."""
        lines = []

        # Count by severity
        by_severity = {
            FindingSeverity.CRITICAL: [],
            FindingSeverity.WARNING: [],
            FindingSeverity.INFO: [],
        }

        for finding in self.all_findings:
            if finding.severity in by_severity:
                by_severity[finding.severity].append(finding)

        critical_count = len(by_severity[FindingSeverity.CRITICAL])
        warning_count = len(by_severity[FindingSeverity.WARNING])
        info_count = len(by_severity[FindingSeverity.INFO])
        suppressed_count = len(self.suppressed_findings)

        # Overall status
        if critical_count > 0:
            status_emoji = "🚨"
            status_text = "Action Required"
        elif warning_count > 0:
            status_emoji = "⚠️"
            status_text = "Improvements Recommended"
        else:
            status_emoji = "✅"
            status_text = "Good Shape"

        lines.append(f"**Status:** {status_emoji} {status_text}\n\n")

        lines.append("| Severity | Count | Description |\n")
        lines.append("|----------|------:|-------------|\n")
        lines.append(f"| 🚨 Critical | {critical_count} | Must fix (security, missing CRUD) |\n")
        lines.append(f"| ⚠️ Warning | {warning_count} | Should fix (missing tests, hardcoded names) |\n")
        lines.append(f"| ℹ️ Info | {info_count} | Nice to have (style, minor improvements) |\n")
        lines.append(f"| 🔇 Suppressed | {suppressed_count} | False positives filtered out |\n")

        # Top issues
        if critical_count > 0:
            lines.append("\n### 🚨 Critical Issues\n")
            for finding in by_severity[FindingSeverity.CRITICAL][:5]:
                lines.append(f"- **{finding.file_name}**: {finding.message}\n")

        if warning_count > 0:
            lines.append("\n### ⚠️ Warning Issues\n")
            for finding in by_severity[FindingSeverity.WARNING][:5]:
                lines.append(f"- **{finding.file_name}**: {finding.message}\n")
            if warning_count > 5:
                lines.append(f"- *(and {warning_count - 5} more)*\n")

        return ''.join(lines)

    def _generate_codebase_stats(self) -> str:
        """Generate codebase statistics section."""
        lines = []
        stats = self.codebase_stats
        total = stats['total']
        by_type = stats['by_type']

        lines.append(f"**Total Go Files:** {total['files']:,} files | {total['lines']:,} lines\n")
        lines.append(f"- Code: {total['code_lines']:,} lines ({total['code_lines']*100//total['lines'] if total['lines'] else 0}%)\n")
        lines.append(f"- Comments: {total['comment_lines']:,} lines ({total['comment_lines']*100//total['lines'] if total['lines'] else 0}%)\n")
        lines.append(f"- Blank: {total['blank_lines']:,} lines ({total['blank_lines']*100//total['lines'] if total['lines'] else 0}%)\n")

        lines.append("\n**By File Type:**\n")
        lines.append("| Type | Files | Lines | Code Lines |\n")
        lines.append("|------|------:|------:|-----------:|\n")

        for type_name, type_stats in sorted(by_type.items(), key=lambda x: x[1]['lines'], reverse=True):
            if type_stats['files'] > 0:
                display_name = type_name.replace('_', ' ').title()
                lines.append(f"| {display_name} | {type_stats['files']:,} | {type_stats['lines']:,} | {type_stats['code_lines']:,} |\n")

        lines.append(f"| **Total** | **{total['files']:,}** | **{total['lines']:,}** | **{total['code_lines']:,}** |\n")

        impl_lines = by_type['resource']['code_lines'] + by_type['data_source']['code_lines'] + by_type['other']['code_lines']
        test_lines = by_type['test']['code_lines']
        if impl_lines > 0:
            ratio = test_lines / impl_lines
            lines.append(f"\n**Test-to-Implementation Ratio:** {ratio:.2f}:1 ({test_lines:,} test lines / {impl_lines:,} impl lines)\n")

        return ''.join(lines)

    def _generate_executive_summary(self) -> str:
        """Generate executive summary."""
        lines = []

        # Calculate statistics
        total_legacy = sum(len([lc for lc in t.legacy_checks if not lc[2]])
                          for t in self.resource_tests + self.data_source_tests)
        total_modern_state = sum(t.modern_state_checks for t in self.resource_tests + self.data_source_tests)
        total_modern_plan = sum(t.modern_plan_checks for t in self.resource_tests + self.data_source_tests)

        real_resources = [t for t in self.resource_tests if not t.is_mock_test]
        mock_resources = [t for t in self.resource_tests if t.is_mock_test]

        resources_with_drift = sum(1 for t in real_resources if t.has_drift_test)
        resources_with_import = sum(1 for t in real_resources if t.has_import_test)

        total_required_fields = sum(len(schema.required_fields) for schema in self.resource_schemas.values())
        missing_validation_count = sum(len(fields) for fields in self.validation_coverage.values())
        covered_validation_count = total_required_fields - missing_validation_count

        resources_with_create = sum(1 for t in real_resources if t.has_create_test)
        resources_with_update = sum(1 for t in real_resources if t.has_update_test)
        resources_with_delete = sum(1 for t in real_resources if t.has_delete_test)

        avg_quality_score = sum(t.quality_score for t in real_resources) / len(real_resources) if real_resources else 0

        real_resources_non_error = [t for t in real_resources if not t.is_error_only_test]
        resources_with_robust_cleanup = sum(1 for t in real_resources_non_error if t.has_robust_check_destroy)

        # Only count critical hardcoded names
        all_tests_non_error = [t for t in self.resource_tests + self.data_source_tests if not t.is_error_only_test]
        tests_with_hardcoded_names = sum(1 for t in all_tests_non_error
                                         if any(n[3] == FindingSeverity.WARNING for n in t.hardcoded_names))
        total_hardcoded_names = sum(len([n for n in t.hardcoded_names if n[3] == FindingSeverity.WARNING])
                                    for t in all_tests_non_error)

        # Only count significant ID issues
        resources_with_id_tracking = sum(1 for t in real_resources if t.has_compare_value_for_id)
        resources_with_id_issues = sum(1 for t in real_resources
                                       if any(i.get('severity') == FindingSeverity.WARNING for i in t.id_consistency_issues))

        lines.append(f"- **{total_modern_state}** modern state checks (`statecheck.ExpectKnownValue`)\n")
        lines.append(f"- **{total_modern_plan}** modern plan checks (`plancheck.Expect*`)\n")
        if total_legacy > 0:
            lines.append(f"- **{total_legacy}** actionable legacy check calls\n")
        else:
            lines.append(f"- **No actionable legacy checks** ✅\n")
        lines.append(f"- **{resources_with_drift}/{len(real_resources)}** acceptance test resources have drift detection tests\n")
        lines.append(f"- **{resources_with_import}/{len(real_resources)}** acceptance test resources have import tests\n")

        if total_required_fields > 0:
            lines.append(f"- **{covered_validation_count}/{total_required_fields}** required fields have validation tests\n")

        lines.append(f"\n**CRUD Coverage:**\n")
        lines.append(f"- Create: {resources_with_create}/{len(real_resources)}\n")
        lines.append(f"- Update: {resources_with_update}/{len(real_resources)}\n")
        lines.append(f"- Delete: {resources_with_delete}/{len(real_resources)}\n")

        lines.append(f"\n**Cleanup Analysis:**\n")
        if len(real_resources_non_error) > 0:
            lines.append(f"- **{resources_with_robust_cleanup}/{len(real_resources_non_error)}** resources have robust cleanup verification\n")

        lines.append(f"\n**Naming Uniqueness:**\n")
        if total_hardcoded_names > 0:
            lines.append(f"- **{tests_with_hardcoded_names}** tests use non-unique names ({total_hardcoded_names} total) ⚠️\n")
        else:
            lines.append(f"- **All tests use unique name generation** ✅\n")

        lines.append(f"\n**ID Consistency Tracking:**\n")
        if len(real_resources) > 0:
            lines.append(f"- **{resources_with_id_tracking}/{len(real_resources)}** resources use `CompareValue(ValuesSame())` for ID tracking\n")
            if resources_with_id_issues > 0:
                lines.append(f"- **{resources_with_id_issues}** resources have significant ID consistency issues ⚠️\n")
            else:
                lines.append(f"- **ID tracking looks good** ✅\n")

        lines.append(f"\n**Average Quality Score:** {avg_quality_score:.0f}/100\n")

        if mock_resources:
            error_only_count = sum(1 for t in mock_resources if t.is_error_only_test)
            if error_only_count > 0:
                lines.append(f"\n**{len(mock_resources)}** mock/unit test files ({error_only_count} error-only, import/drift N/A)\n")

        # Overall grade
        critical_findings = len([f for f in self.all_findings if f.severity == FindingSeverity.CRITICAL])
        warning_findings = len([f for f in self.all_findings if f.severity == FindingSeverity.WARNING])

        if critical_findings == 0 and warning_findings <= 5:
            grade = "A"
        elif critical_findings == 0 and warning_findings <= 15:
            grade = "B"
        else:
            grade = "C"

        lines.append(f"\n**Overall Grade: {grade}**\n")

        return ''.join(lines)

    def _analyze_category(self, tests: List[TestFile], category: str) -> str:
        """Analyze a category of tests."""
        if not tests:
            return f"No {category.lower()} tests found.\n"

        lines = []
        for test in tests:
            lines.append(f"\n### {test.name}\n")
            lines.append(f"- **Test functions:** {len(test.test_functions)}\n")
            lines.append(f"- **Modern state checks:** {test.modern_state_checks}\n")
            lines.append(f"- **Modern plan checks:** {test.modern_plan_checks}\n")

            if category == "Resource":
                if test.is_error_only_test:
                    lines.append(f"- **Test type:** Error-only tests (uses httptest mock servers)\n")
                elif test.is_mock_test:
                    lines.append(f"- **Test type:** Mock/Unit tests (import/drift N/A)\n")
                else:
                    lines.append(f"- **Has import test:** {'✅' if test.has_import_test else '❌'}\n")
                    lines.append(f"- **Has drift test:** {'✅' if test.has_drift_test else '❌'}\n")
                lines.append(f"- **Idempotency checks:** {test.idempotency_checks}\n")
                lines.append(f"- **Validation tests:** {len(test.validation_tests)}\n")

                crud_ops = []
                if test.has_create_test:
                    crud_ops.append("Create")
                if test.has_update_test:
                    crud_ops.append("Update")
                if test.has_delete_test:
                    crud_ops.append("Delete")
                lines.append(f"- **CRUD coverage:** {', '.join(crud_ops) if crud_ops else 'None'}\n")

                lines.append(f"- **Quality score:** {test.quality_score}/100\n")

                if test.cleanup_issues:
                    lines.append(f"- **Cleanup issues:** {len(test.cleanup_issues)} ⚠️\n")
                    for issue in test.cleanup_issues:
                        lines.append(f"  - {issue}\n")
                else:
                    cleanup_status = "✅ Robust" if test.has_robust_check_destroy else "✅ Basic"
                    if test.has_check_destroy:
                        lines.append(f"- **Cleanup:** {cleanup_status}\n")

                # Only show WARNING level hardcoded names
                critical_names = [n for n in test.hardcoded_names if n[3] == FindingSeverity.WARNING]
                if critical_names:
                    lines.append(f"- **Hardcoded names:** {len(critical_names)} ⚠️\n")
                    for line_num, field, value, _ in critical_names[:3]:
                        lines.append(f"  - Line {line_num}: {field} = \"{value}\"\n")
                    if len(critical_names) > 3:
                        lines.append(f"  - (and {len(critical_names) - 3} more)\n")

                # ID consistency - show trackable vs total
                if test.has_compare_value_for_id:
                    lines.append(f"- **ID tracking:** ✅ Uses CompareValue ({test.id_tracking_steps}/{test.trackable_test_steps} trackable steps)\n")

                # Only show significant ID issues
                significant_issues = [i for i in test.id_consistency_issues if i.get('severity') == FindingSeverity.WARNING]
                if significant_issues:
                    lines.append(f"- **ID consistency issues:** {len(significant_issues)} ⚠️\n")
                    for issue in significant_issues:
                        lines.append(f"  - {issue['message']}\n")

            # Credentials
            if test.hardcoded_credentials:
                critical_creds = [c for c in test.hardcoded_credentials if c[3] == 'critical']
                if critical_creds:
                    lines.append(f"- **🚨 Hardcoded credentials:** {len(critical_creds)} CRITICAL\n")
                    for line_num, cred_type, value, severity in critical_creds[:3]:
                        masked = value[:4] + '*' * (len(value) - 4) if len(value) > 4 else '****'
                        lines.append(f"  - Line {line_num}: `{cred_type}` = `{masked}`\n")

            # Legacy checks - only actionable ones
            actionable_legacy = [lc for lc in test.legacy_checks if not lc[2]]
            if actionable_legacy:
                lines.append(f"- **Legacy checks:** {len(actionable_legacy)} (actionable)\n")
                lines.append(f"  - Lines: {', '.join(str(line) for line, _, _ in actionable_legacy[:5])}")
                if len(actionable_legacy) > 5:
                    lines.append(f" (and {len(actionable_legacy) - 5} more)")
                lines.append("\n")
            else:
                lines.append(f"- **Legacy checks:** None ✅\n")

            # Status
            status = self._file_status(test, category == "Resource")
            lines.append(f"- **Status:** {status}\n")

        return ''.join(lines)

    def _file_status(self, test: TestFile, is_resource: bool) -> str:
        """Determine file modernization status."""
        # Check for critical findings first
        critical_findings = [f for f in test.findings if f.severity == FindingSeverity.CRITICAL]
        if critical_findings:
            return f"🚨 Critical issues ({len(critical_findings)})"

        # Check for actionable legacy
        actionable_legacy = [lc for lc in test.legacy_checks if not lc[2]]
        if actionable_legacy:
            return f"🟡 Has legacy checks ({len(actionable_legacy)} actionable)"

        if test.is_error_only_test:
            return "✅ Error path coverage (httptest mocks)"

        if is_resource and not test.is_mock_test:
            if not test.has_import_test:
                return "⚠️ Missing import test"
            if not test.has_drift_test:
                return "⚠️ Missing drift detection test"

        if test.is_mock_test:
            return "✅ Mock/unit tests (error validation)"

        if test.modern_state_checks > 0:
            return "✅ Fully modernized"

        return "❓ Needs review"

    def _generate_recommendations(self) -> str:
        """Generate prioritized recommendations based on severity."""
        lines = []

        # Group findings by severity
        by_severity = {
            FindingSeverity.CRITICAL: [],
            FindingSeverity.WARNING: [],
            FindingSeverity.INFO: [],
        }

        for finding in self.all_findings:
            if finding.severity in by_severity:
                by_severity[finding.severity].append(finding)

        # CRITICAL
        if by_severity[FindingSeverity.CRITICAL]:
            lines.append("\n### 🚨 CRITICAL (Must Fix)\n")
            for finding in by_severity[FindingSeverity.CRITICAL]:
                lines.append(f"- **{finding.file_name}**: {finding.message}\n")
                if finding.context:
                    if 'credentials' in finding.context:
                        for line_num, cred_type, value, _ in finding.context['credentials']:
                            masked = value[:4] + '*' * (len(value) - 4) if len(value) > 4 else '****'
                            lines.append(f"  - Line {line_num}: `{cred_type}` = `{masked}` → Use `os.Getenv()`\n")

        # WARNING
        if by_severity[FindingSeverity.WARNING]:
            lines.append("\n### ⚠️ WARNING (Should Fix)\n")

            # Group by type
            by_type = defaultdict(list)
            for finding in by_severity[FindingSeverity.WARNING]:
                by_type[finding.finding_type].append(finding)

            for finding_type, findings in by_type.items():
                if finding_type == 'missing_drift':
                    lines.append("\n**Missing Drift Detection Tests:**\n")
                    for f in findings:
                        lines.append(f"- `{f.file_name}`\n")
                elif finding_type == 'missing_import':
                    lines.append("\n**Missing Import Tests:**\n")
                    for f in findings:
                        lines.append(f"- `{f.file_name}`\n")
                elif finding_type == 'hardcoded_names':
                    lines.append("\n**Non-Unique Resource Names:**\n")
                    for f in findings:
                        lines.append(f"- `{f.file_name}`: {f.message}\n")
                        if f.context and 'names' in f.context:
                            for line_num, field, value in f.context['names'][:3]:
                                lines.append(f"  - Line {line_num}: `{field} = \"{value}\"` → Use `generateUniqueTestName()`\n")
                elif finding_type == 'no_id_verification':
                    lines.append("\n**Missing ID Verification:**\n")
                    for f in findings:
                        lines.append(f"- `{f.file_name}`: {f.message}\n")
                else:
                    lines.append(f"\n**{finding_type.replace('_', ' ').title()}:**\n")
                    for f in findings:
                        lines.append(f"- `{f.file_name}`: {f.message}\n")

        # Validation coverage (if any missing)
        if self.validation_coverage:
            lines.append("\n### 📋 Validation Test Gaps\n")
            for resource_name, missing_fields in sorted(self.validation_coverage.items()):
                lines.append(f"- **`{resource_name}`**: {', '.join(missing_fields)}\n")

        # INFO (collapsed)
        info_count = len(by_severity[FindingSeverity.INFO])
        if info_count > 0:
            lines.append(f"\n### ℹ️ INFO ({info_count} items - optional improvements)\n")
            lines.append("<details>\n<summary>Click to expand</summary>\n\n")
            for finding in by_severity[FindingSeverity.INFO][:10]:
                lines.append(f"- **{finding.file_name}**: {finding.message}\n")
            if info_count > 10:
                lines.append(f"\n*...and {info_count - 10} more*\n")
            lines.append("\n</details>\n")

        # Suppressed findings note
        if self.suppressed_findings:
            lines.append(f"\n### 🔇 Suppressed Findings\n")
            lines.append(f"**{len(self.suppressed_findings)}** false positives were automatically filtered:\n")
            lines.append("- Domain-specific names (eth0, bond0, ipmi0, etc.)\n")
            lines.append("- Legacy checks with modern equivalents\n")
            lines.append("- Non-trackable test steps (idempotency, drift)\n")

        if not by_severity[FindingSeverity.CRITICAL] and not by_severity[FindingSeverity.WARNING]:
            lines.append("\n✅ **No critical or warning issues found!**\n")
            lines.append("\nThe test suite is in good shape. Consider addressing INFO items for further improvement.\n")

        return ''.join(lines)

    def _pattern_reference(self) -> str:
        """Generate pattern reference section."""
        return """
### Required Imports
```go
import (
    "github.com/hashicorp/terraform-plugin-testing/helper/resource"
    "github.com/hashicorp/terraform-plugin-testing/plancheck"
    "github.com/hashicorp/terraform-plugin-testing/statecheck"
    "github.com/hashicorp/terraform-plugin-testing/knownvalue"
    "github.com/hashicorp/terraform-plugin-testing/tfjsonpath"
    "github.com/hashicorp/terraform-plugin-testing/compare"
)
```

### Modern State Check
```go
ConfigStateChecks: []statecheck.StateCheck{
    statecheck.ExpectKnownValue(
        "example_resource.test",
        tfjsonpath.New("name"),
        knownvalue.StringExact("expected-value"),
    ),
}
```

### Idempotency Check
```go
ConfigPlanChecks: resource.ConfigPlanChecks{
    PreApply: []plancheck.PlanCheck{
        plancheck.ExpectEmptyPlan(),
    },
}
```

### ID Consistency Tracking
```go
// Initialize ID tracker at test start (before Steps)
compareID := statecheck.CompareValue(compare.ValuesSame())

// Track in Create, Import, and Update steps (NOT idempotency/drift steps)
{
    Config: testAccResourceConfig(name),
    ConfigStateChecks: []statecheck.StateCheck{
        compareID.AddStateValue("example_resource.test", tfjsonpath.New("id")),
    },
}
```

### Cleanup-Friendly Naming
```go
// Use unique names with cleanup-friendly prefixes
resourceName := generateUniqueTestName("tftest-resource")
```
"""

    def _get_date(self) -> str:
        """Get current date string."""
        return datetime.now().strftime("%Y-%m-%d")


# =============================================================================
# MAIN ENTRY POINT
# =============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Analyze Terraform provider test coverage and quality (v2.0)"
    )
    parser.add_argument(
        "test_dir",
        help="Directory containing test files (e.g., ./internal/provider/)"
    )
    parser.add_argument(
        "--output", "-o",
        help="Output file path (default: stdout)",
        default=None
    )
    parser.add_argument(
        "--config", "-c",
        help="Configuration file path (YAML)",
        default=None
    )

    args = parser.parse_args()

    # Load configuration
    config = load_config(args.config)

    # Run analysis
    analyzer = GapAnalyzer(args.test_dir, config)
    analyzer.scan()
    report = analyzer.generate_report()

    # Output
    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w') as f:
            f.write(report)
        print(f"✅ Gap analysis report written to: {output_path}")
    else:
        print(report)


if __name__ == "__main__":
    main()
