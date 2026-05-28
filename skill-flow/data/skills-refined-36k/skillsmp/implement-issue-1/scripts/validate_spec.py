#!/usr/bin/env python3
"""
Spec Format Validator for woo-attribution-bridge

Validates that a specification document follows the required format
defined in docs/specs/SPEC_TEMPLATE.md.

Usage:
    python3 validate_spec.py <path-to-spec.md>

Exit codes:
    0 - Validation passed
    1 - Validation failed
    2 - File not found or read error
"""

import sys
import re
from pathlib import Path
from typing import NamedTuple


class ValidationResult(NamedTuple):
    passed: bool
    message: str


class SpecValidator:
    """Validates spec documents against the required format."""

    REQUIRED_SECTIONS = [
        ("## 1. Overview", ["### 1.1 Purpose", "### 1.2 Scope", "### 1.3 Dependencies"]),
        ("## 2. Requirements", ["### 2.1 Functional Requirements", "### 2.2 Non-Functional Requirements"]),
        ("## 3. Technical Design", []),
        ("## 4. Public Interface", []),
        ("## 5. Error Handling", []),
        ("## 6. Security Considerations", []),
        ("## 7. Testing Requirements", ["### 7.1 Unit Tests", "### 7.3 Coverage Target"]),
        ("## 8. Implementation Notes", ["### 8.1 File Locations"]),
        ("## 9. Changelog", []),
    ]

    VALID_STATUSES = ["Draft", "Review", "Approved", "Implemented"]

    def __init__(self, content: str, filename: str):
        self.content = content
        self.filename = filename
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def validate(self) -> bool:
        """Run all validation checks. Returns True if passed."""
        self._validate_spec_id()
        self._validate_status()
        self._validate_sections()
        self._validate_requirements_tables()
        self._validate_coverage_target()
        self._validate_file_locations()

        return len(self.errors) == 0

    def _validate_spec_id(self):
        """Check SPEC-ID format in title."""
        # Support multiple formats:
        # - SPEC-XXX (template format)
        # - WAB-P-XXX (plugin specs)
        # - WAB-D-XXX (dashboard specs)
        match = re.search(r'^# ((?:SPEC|WAB-[PD])-\d{3})', self.content, re.MULTILINE)
        if not match:
            self.errors.append(
                "Missing or invalid SPEC-ID in title. "
                "Expected format: # WAB-P-XXX or # WAB-D-XXX or # SPEC-XXX"
            )
        else:
            spec_id = match.group(1)
            # Check filename matches
            expected_prefix = spec_id.lower()
            if expected_prefix not in self.filename.lower():
                self.warnings.append(
                    f"Filename should contain the SPEC-ID: {spec_id}"
                )

    def _validate_status(self):
        """Check status field is present and valid."""
        match = re.search(r'>\s*\*\*Status:\*\*\s*(.+)', self.content)
        if not match:
            self.errors.append(
                "Missing Status field. Expected: > **Status:** Draft | Review | Approved | Implemented"
            )
            return

        status_line = match.group(1).strip()
        # Check if any valid status is in the line
        if not any(status in status_line for status in self.VALID_STATUSES):
            self.errors.append(
                f"Invalid status. Must be one of: {', '.join(self.VALID_STATUSES)}"
            )

    def _validate_sections(self):
        """Check all required sections are present."""
        for section, subsections in self.REQUIRED_SECTIONS:
            if section not in self.content:
                self.errors.append(f"Missing required section: {section}")
            else:
                for subsection in subsections:
                    if subsection not in self.content:
                        self.warnings.append(f"Missing recommended subsection: {subsection}")

    def _validate_requirements_tables(self):
        """Check requirements section has proper tables."""
        # Check for FR- requirements
        if "## 2. Requirements" in self.content:
            fr_match = re.search(r'\|\s*FR-\d+', self.content)
            if not fr_match:
                self.warnings.append(
                    "No functional requirements (FR-XXX) found in requirements table"
                )

    def _validate_coverage_target(self):
        """Check coverage target is specified."""
        if "### 7.3 Coverage Target" in self.content:
            coverage_section = self.content.split("### 7.3 Coverage Target")[1]
            coverage_section = coverage_section.split("##")[0]  # Get just this section

            if "80%" not in coverage_section and "%" not in coverage_section:
                self.warnings.append(
                    "Coverage target should specify a percentage (minimum 80%)"
                )

    def _validate_file_locations(self):
        """Check file locations are specified."""
        if "### 8.1 File Locations" in self.content:
            locations_section = self.content.split("### 8.1 File Locations")[1]
            locations_section = locations_section.split("##")[0]

            # Check for table with file paths
            if "|" not in locations_section:
                self.warnings.append(
                    "File locations should be in a table format"
                )

    def report(self) -> str:
        """Generate validation report."""
        lines = [f"Spec Validation Report: {self.filename}", "=" * 50]

        if self.errors:
            lines.append(f"\nERRORS ({len(self.errors)}):")
            for err in self.errors:
                lines.append(f"  - {err}")

        if self.warnings:
            lines.append(f"\nWARNINGS ({len(self.warnings)}):")
            for warn in self.warnings:
                lines.append(f"  - {warn}")

        if not self.errors and not self.warnings:
            lines.append("\nAll checks passed!")

        status = "PASSED" if not self.errors else "FAILED"
        lines.append(f"\nResult: {status}")

        return "\n".join(lines)


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 validate_spec.py <path-to-spec.md>")
        sys.exit(2)

    spec_path = Path(sys.argv[1])

    if not spec_path.exists():
        print(f"Error: File not found: {spec_path}")
        sys.exit(2)

    try:
        content = spec_path.read_text()
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(2)

    validator = SpecValidator(content, spec_path.name)
    passed = validator.validate()

    print(validator.report())

    sys.exit(0 if passed else 1)


if __name__ == "__main__":
    main()
