"""Validation engine for orchestrating sheet validation.

This module provides the main entry points for validating sheets:
- validate_sheet(): Validate a single sheet
- validate_all_sheets(): Validate all sheets in a directory
- validate_row(): Validate a single row (for debugging/testing)
"""

from __future__ import annotations

import csv
import json
import logging
from pathlib import Path  # noqa: TC003 - Path is used at runtime
from typing import Any

from cmm_ai_automation.validation.base import (
    FieldValidator,
    Severity,
    ValidationReport,
)
from cmm_ai_automation.validation.schemas import SHEET_SCHEMAS, get_schema_for_sheet
from cmm_ai_automation.validation.validators.ncbi_taxon import (
    NCBITaxonListValidator,
    NCBITaxonValidator,
)

logger = logging.getLogger(__name__)

# Registry of validator names to classes
VALIDATOR_REGISTRY: dict[str, type[FieldValidator]] = {
    "ncbi_taxon": NCBITaxonValidator,
    "ncbi_taxon_list": NCBITaxonListValidator,
}


def get_validator(name: str, options: dict[str, Any]) -> FieldValidator:
    """Create a validator instance by name.

    Args:
        name: Validator name (must be in VALIDATOR_REGISTRY)
        options: Options to pass to validator constructor

    Returns:
        Configured FieldValidator instance

    Raises:
        ValueError: If validator name not found
    """
    if name not in VALIDATOR_REGISTRY:
        raise ValueError(f"Unknown validator: {name}. Available: {list(VALIDATOR_REGISTRY.keys())}")

    validator_class = VALIDATOR_REGISTRY[name]
    return validator_class(**options)


def validate_row(
    row: dict[str, str],
    sheet: str,
    row_num: int,
    schema: dict[str, tuple[str, dict[str, Any]]] | None = None,
) -> ValidationReport:
    """Validate a single row against a schema.

    Args:
        row: Dict mapping column names to values
        sheet: Sheet name for reporting
        row_num: Row number (1-indexed) for reporting
        schema: Optional schema override. If None, uses SHEET_SCHEMAS.

    Returns:
        ValidationReport with any issues found
    """
    report = ValidationReport(sheets_checked=[sheet], rows_checked=1)

    if schema is None:
        schema = get_schema_for_sheet(sheet)

    if not schema:
        logger.debug(f"No schema defined for {sheet}")
        return report

    # Create validator instances
    validators: dict[str, FieldValidator] = {}
    for field, (validator_name, options) in schema.items():
        try:
            validators[field] = get_validator(validator_name, options)
        except ValueError as e:
            logger.warning(f"Skipping {field}: {e}")

    # Validate each field
    context = dict(row)  # All row values available as context

    for field, validator in validators.items():
        value = row.get(field, "")
        if value:  # Skip empty values (handled by required field checks)
            issues = validator.validate(
                value=value,
                context=context,
                sheet=sheet,
                row=row_num,
                field=field,
            )
            for issue in issues:
                report.add_issue(issue)

    return report


def validate_sheet(
    sheet_path: Path,
    schema: dict[str, tuple[str, dict[str, Any]]] | None = None,
) -> ValidationReport:
    """Validate a single sheet against its schema.

    Args:
        sheet_path: Path to TSV file
        schema: Optional schema override. If None, uses SHEET_SCHEMAS.

    Returns:
        ValidationReport with all issues found
    """
    sheet_name = sheet_path.name
    report = ValidationReport(sheets_checked=[sheet_name])

    if schema is None:
        schema = get_schema_for_sheet(sheet_name)

    if not schema:
        logger.info(f"No schema defined for {sheet_name}, skipping")
        return report

    if not sheet_path.exists():
        logger.warning(f"Sheet not found: {sheet_path}")
        return report

    # Create validator instances (shared across rows for caching)
    validators: dict[str, FieldValidator] = {}
    for field, (validator_name, options) in schema.items():
        try:
            validators[field] = get_validator(validator_name, options)
        except ValueError as e:
            logger.warning(f"Skipping {field}: {e}")

    # Read and validate each row
    with sheet_path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="\t")

        for row_num, row in enumerate(reader, start=2):  # Row 1 is header
            report.rows_checked += 1
            context = dict(row)

            for field, validator in validators.items():
                value = row.get(field, "")
                if value:
                    issues = validator.validate(
                        value=value,
                        context=context,
                        sheet=sheet_name,
                        row=row_num,
                        field=field,
                    )
                    for issue in issues:
                        report.add_issue(issue)

    logger.info(f"Validated {sheet_name}: {report.rows_checked} rows, {len(report.issues)} issues")
    return report


def validate_all_sheets(
    sheets_dir: Path,
    schemas: dict[str, dict[str, tuple[str, dict[str, Any]]]] | None = None,
) -> ValidationReport:
    """Validate all sheets in a directory.

    Args:
        sheets_dir: Directory containing TSV files
        schemas: Optional schemas override. If None, uses SHEET_SCHEMAS.

    Returns:
        Combined ValidationReport from all sheets
    """
    if schemas is None:
        schemas = SHEET_SCHEMAS

    report = ValidationReport()

    for sheet_name in schemas:
        sheet_path = sheets_dir / sheet_name
        if sheet_path.exists():
            sheet_report = validate_sheet(sheet_path, schemas.get(sheet_name))
            report.merge(sheet_report)
        else:
            logger.debug(f"Sheet not found, skipping: {sheet_path}")

    return report


def print_validation_report(report: ValidationReport, verbose: bool = False) -> None:
    """Print human-readable validation report.

    Args:
        report: ValidationReport to print
        verbose: If True, include INFO-level issues
    """
    print("\nVALIDATION REPORT")
    print("=" * 60)
    print(f"Sheets checked: {', '.join(report.sheets_checked)}")
    print(f"Rows checked:   {report.rows_checked}")
    print(f"Issues found:   {len(report.issues)}")
    print()

    # Print errors
    errors = report.get_issues_by_severity(Severity.ERROR)
    if errors:
        print(f"ERRORS ({len(errors)}):")
        for issue in errors:
            print(f"  {issue}")
            if issue.suggestion:
                print(f"    -> {issue.suggestion}")
        print()

    # Print warnings
    warnings = report.get_issues_by_severity(Severity.WARNING)
    if warnings:
        print(f"WARNINGS ({len(warnings)}):")
        for issue in warnings:
            print(f"  {issue}")
            if issue.suggestion:
                print(f"    -> {issue.suggestion}")
        print()

    # Print info (only if verbose)
    if verbose:
        infos = report.get_issues_by_severity(Severity.INFO)
        if infos:
            print(f"INFO ({len(infos)}):")
            for issue in infos:
                print(f"  {issue}")
            print()

    # Summary by type
    if report.stats:
        print("Summary by type:")
        for issue_type, count in sorted(report.stats.items()):
            print(f"  {issue_type}: {count}")


def export_validation_report(report: ValidationReport, path: Path) -> None:
    """Export validation report to JSON file.

    Args:
        report: ValidationReport to export
        path: Output file path
    """
    data = {
        "sheets_checked": report.sheets_checked,
        "rows_checked": report.rows_checked,
        "stats": report.stats,
        "issues": [
            {
                "sheet": i.sheet,
                "row": i.row,
                "field": i.field,
                "issue_type": i.issue_type.value,
                "severity": i.severity.value,
                "value": i.value,
                "expected": i.expected,
                "actual": i.actual,
                "message": i.message,
                "suggestion": i.suggestion,
            }
            for i in report.issues
        ],
    }

    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    logger.info(f"Exported validation report to {path}")
