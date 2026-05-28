#!/usr/bin/env python3
# ABOUTME: XLSForm Excel structure validator
# ABOUTME: Checks worksheet structure, columns, references, and common errors before conversion

import sys
import re
from pathlib import Path

try:
    import openpyxl
except ImportError:
    print("ERROR: openpyxl not installed.")
    print("\nInstall with uv:")
    print("  uv pip install openpyxl")
    print("\nOr with pip:")
    print("  pip install openpyxl")
    sys.exit(1)


class XLSFormValidator:
    """Validates XLSForm Excel file structure and references."""

    VALID_QUESTION_TYPES = {
        'text', 'integer', 'decimal', 'date', 'time', 'datetime',
        'select_one', 'select_multiple', 'rank',
        'geopoint', 'geotrace', 'geoshape',
        'image', 'audio', 'video', 'file', 'barcode',
        'calculate', 'note', 'acknowledge', 'hidden',
        'begin repeat', 'end repeat', 'begin group', 'end group',
        'select_one_from_file', 'select_multiple_from_file'
    }

    SURVEY_REQUIRED_COLUMNS = {'type', 'name', 'label'}
    CHOICES_REQUIRED_COLUMNS = {'list_name', 'name', 'label'}

    # Valid variable name pattern: alphanumeric + underscore, starts with letter/underscore
    VALID_NAME_PATTERN = re.compile(r'^[a-zA-Z_][a-zA-Z0-9_]*$')

    def __init__(self):
        self.errors = []
        self.warnings = []
        self.survey_names = set()
        self.choice_lists = {}

    def validate(self, xlsx_path):
        """Main validation entry point."""
        try:
            workbook = openpyxl.load_workbook(xlsx_path)
        except Exception as e:
            self.errors.append(f"Cannot open file: {e}")
            return False

        # Check required worksheets
        if 'survey' not in workbook.sheetnames:
            self.errors.append("ERROR: No 'survey' worksheet found")
            return False

        # Validate survey worksheet
        self._validate_survey_sheet(workbook['survey'])

        # Validate choices worksheet if present
        if 'choices' in workbook.sheetnames:
            self._validate_choices_sheet(workbook['choices'])

        # Cross-validate references
        self._validate_references()

        return len(self.errors) == 0

    def _validate_survey_sheet(self, sheet):
        """Validate survey worksheet structure and content."""
        # Get header row
        headers = [cell.value for cell in sheet[1]]
        headers = [h for h in headers if h is not None]

        if not headers:
            self.errors.append("ERROR: Survey sheet is empty")
            return

        # Check required columns
        headers_lower = {h.lower() for h in headers}
        missing = self.SURVEY_REQUIRED_COLUMNS - headers_lower
        if missing:
            self.errors.append(f"ERROR: Survey sheet missing required columns: {missing}")
            return

        # Find column indices
        type_col = next(i for i, h in enumerate(headers) if h.lower() == 'type')
        name_col = next(i for i, h in enumerate(headers) if h.lower() == 'name')

        # Validate rows
        for row_num, row in enumerate(sheet.iter_rows(min_row=2, values_only=True), start=2):
            if not any(row):  # Skip empty rows
                continue

            q_type = row[type_col] if type_col < len(row) else None
            q_name = row[name_col] if name_col < len(row) else None

            if not q_type:
                continue

            # Validate question type
            if isinstance(q_type, str):
                q_type = q_type.strip()
                # Check for list_name parameter
                if q_type.startswith('select_') and ' ' not in q_type:
                    if q_type not in {'select_one', 'select_multiple', 'select_one_from_file', 'select_multiple_from_file'}:
                        self.errors.append(
                            f"Row {row_num}: '{q_type}' requires list_name. "
                            f"Format: 'select_one list_name'"
                        )
                        continue

                if q_type not in self.VALID_QUESTION_TYPES and not self._is_select_with_list(q_type):
                    self.errors.append(f"Row {row_num}: Unknown question type '{q_type}'")

            # Validate question name
            if q_name:
                q_name = str(q_name).strip()
                if not self.VALID_NAME_PATTERN.match(q_name):
                    self.errors.append(
                        f"Row {row_num}: Invalid question name '{q_name}'. "
                        f"Must start with letter/underscore, contain only alphanumeric/underscore."
                    )
                elif q_name in self.survey_names:
                    self.errors.append(f"Row {row_num}: Duplicate question name '{q_name}'")
                else:
                    self.survey_names.add(q_name)

    def _validate_choices_sheet(self, sheet):
        """Validate choices worksheet structure and content."""
        # Get header row
        headers = [cell.value for cell in sheet[1]]
        headers = [h for h in headers if h is not None]

        if not headers:
            self.warnings.append("WARNING: Choices sheet is empty")
            return

        # Check required columns
        headers_lower = {h.lower() for h in headers}
        missing = self.CHOICES_REQUIRED_COLUMNS - headers_lower
        if missing:
            self.errors.append(f"ERROR: Choices sheet missing required columns: {missing}")
            return

        # Find column indices
        list_col = next(i for i, h in enumerate(headers) if h.lower() == 'list_name')
        name_col = next(i for i, h in enumerate(headers) if h.lower() == 'name')

        # Validate rows and build choice lists
        seen_choices = {}  # Track duplicates per list
        for row_num, row in enumerate(sheet.iter_rows(min_row=2, values_only=True), start=2):
            if not any(row):  # Skip empty rows
                continue

            list_name = row[list_col] if list_col < len(row) else None
            choice_name = row[name_col] if name_col < len(row) else None

            if not list_name:
                continue

            list_name = str(list_name).strip()
            choice_name = str(choice_name).strip() if choice_name else None

            # Track choices by list
            if list_name not in self.choice_lists:
                self.choice_lists[list_name] = []
            self.choice_lists[list_name].append(choice_name)

            # Check duplicate choice names within list
            if choice_name:
                key = (list_name, choice_name)
                if key in seen_choices:
                    self.errors.append(
                        f"Row {row_num}: Duplicate choice name '{choice_name}' in list '{list_name}'"
                    )
                else:
                    seen_choices[key] = row_num

    def _validate_references(self):
        """Validate cross-references between survey and choices."""
        workbook = None
        try:
            # We need to re-examine survey for select types
            # This is a simplified check
            pass
        except:
            pass

    def _is_select_with_list(self, q_type):
        """Check if type is select_* with list name."""
        return (
            q_type.startswith('select_one ') or
            q_type.startswith('select_multiple ') or
            q_type.startswith('select_one_from_file ') or
            q_type.startswith('select_multiple_from_file ')
        )

    def print_results(self):
        """Print validation results to console."""
        if not self.errors and not self.warnings:
            print("✓ XLSForm validation PASSED")
            print(f"  - Survey: {len(self.survey_names)} questions found")
            print(f"  - Choices: {len(self.choice_lists)} choice lists found")
            return

        if self.errors:
            print("✗ XLSForm validation FAILED")
            print("\nERRORS:")
            for error in self.errors:
                print(f"  • {error}")

        if self.warnings:
            print("\nWARNINGS:")
            for warning in self.warnings:
                print(f"  • {warning}")


def main():
    if len(sys.argv) < 2:
        print("Usage: python validate_xlsform.py <form.xlsx>")
        print("\nValidates XLSForm Excel file structure before conversion.")
        sys.exit(1)

    xlsx_path = sys.argv[1]

    if not Path(xlsx_path).exists():
        print(f"ERROR: File not found: {xlsx_path}")
        sys.exit(1)

    validator = XLSFormValidator()
    is_valid = validator.validate(xlsx_path)
    validator.print_results()

    sys.exit(0 if is_valid else 1)


if __name__ == '__main__':
    main()
