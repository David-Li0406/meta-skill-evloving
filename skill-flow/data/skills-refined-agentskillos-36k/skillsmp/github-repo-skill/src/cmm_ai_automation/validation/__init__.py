"""Sheet data validation framework.

This package provides tools to validate data integrity in sheets by
cross-checking field values against authoritative sources (NCBI, BacDive, etc.).

Main entry points:
    - validate_sheet(): Validate a single sheet
    - validate_all_sheets(): Validate all sheets in a directory
    - validate_row(): Validate a single row

Example:
    from cmm_ai_automation.validation import validate_sheet, print_validation_report

    report = validate_sheet(Path("data/private/strains.tsv"))
    print_validation_report(report)
"""

from cmm_ai_automation.validation.base import (
    FieldValidator,
    IssueType,
    ListValidator,
    Severity,
    ValidationIssue,
    ValidationReport,
)
from cmm_ai_automation.validation.engine import (
    export_validation_report,
    print_validation_report,
    validate_all_sheets,
    validate_row,
    validate_sheet,
)
from cmm_ai_automation.validation.schemas import (
    SHEET_SCHEMAS,
    get_schema_for_sheet,
    list_validated_columns,
    list_validated_sheets,
)

__all__ = [
    "SHEET_SCHEMAS",
    "FieldValidator",
    "IssueType",
    "ListValidator",
    "Severity",
    "ValidationIssue",
    "ValidationReport",
    "export_validation_report",
    "get_schema_for_sheet",
    "list_validated_columns",
    "list_validated_sheets",
    "print_validation_report",
    "validate_all_sheets",
    "validate_row",
    "validate_sheet",
]
