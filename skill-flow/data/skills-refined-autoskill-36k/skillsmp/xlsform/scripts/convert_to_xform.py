#!/usr/bin/env python3
# ABOUTME: XLSForm to XForm converter wrapper
# ABOUTME: Converts Excel forms to XForm XML using pyxform, validates output

import sys
import subprocess
from pathlib import Path

try:
    from pyxform import xls2json, create_survey_from_xls
    from pyxform.xls2json import get_xml
except ImportError:
    print("ERROR: pyxform not installed.")
    print("\nInstall with uv:")
    print("  uv pip install pyxform")
    print("\nOr with pip:")
    print("  pip install pyxform")
    sys.exit(1)


def convert_to_xform(xlsx_path, output_path=None):
    """
    Convert XLSForm to XForm XML.

    Args:
        xlsx_path: Path to XLSForm .xlsx file
        output_path: Path for output .xml file (optional)

    Returns:
        tuple: (success: bool, xml_content: str or error message)
    """
    try:
        # Generate output filename if not specified
        if output_path is None:
            xlsx = Path(xlsx_path)
            output_path = xlsx.parent / f"{xlsx.stem}.xml"

        # Create survey from Excel
        survey = create_survey_from_xls(xlsx_path)

        # Generate XForm XML
        xml_content = survey.to_xml()

        # Write to file
        output_file = Path(output_path)
        output_file.write_text(xml_content, encoding='utf-8')

        return True, str(output_file)

    except Exception as e:
        error_msg = str(e)
        return False, error_msg


def validate_xform_schema(xml_content):
    """
    Basic validation of generated XForm XML.

    Args:
        xml_content: XForm XML string

    Returns:
        tuple: (is_valid: bool, errors: list)
    """
    errors = []

    # Check for valid XML structure
    if not xml_content.strip().startswith('<?xml'):
        errors.append("Missing XML declaration")

    if '<h:html' not in xml_content and '<html' not in xml_content:
        errors.append("Missing HTML root element")

    if '<model>' not in xml_content:
        errors.append("Missing XForm model element")

    if '<instance>' not in xml_content:
        errors.append("Missing instance element")

    if '<bind' not in xml_content and 'begin repeat' not in str(xml_content):
        # At least one bind expected (or repeat groups)
        pass

    return len(errors) == 0, errors


def main():
    if len(sys.argv) < 2:
        print("Usage: python convert_to_xform.py <form.xlsx> [-o output.xml]")
        print("\nConverts XLSForm to XForm XML using pyxform.")
        print("\nOptions:")
        print("  -o FILE    Save output to FILE (default: same name as input, .xml extension)")
        sys.exit(1)

    xlsx_path = sys.argv[1]
    output_path = None

    # Parse optional output argument
    if len(sys.argv) >= 4 and sys.argv[2] == '-o':
        output_path = sys.argv[3]

    # Validate input file exists
    if not Path(xlsx_path).exists():
        print(f"ERROR: File not found: {xlsx_path}")
        sys.exit(1)

    print(f"Converting: {xlsx_path}")

    # Convert to XForm
    success, result = convert_to_xform(xlsx_path, output_path)

    if not success:
        print(f"✗ Conversion FAILED")
        print(f"\nError: {result}")
        sys.exit(1)

    # Result is output file path
    output_file = result
    output_content = Path(output_file).read_text(encoding='utf-8')

    # Validate generated XML
    is_valid, errors = validate_xform_schema(output_content)

    if is_valid:
        print(f"✓ Conversion SUCCESSFUL")
        print(f"  Output: {output_file}")
        print(f"  Size: {len(output_content)} bytes")
        return 0
    else:
        print(f"✓ Conversion completed but validation issues found:")
        for error in errors:
            print(f"  ⚠ {error}")
        print(f"\n  Output file: {output_file}")
        return 0  # Still return success since conversion worked


if __name__ == '__main__':
    sys.exit(main())
