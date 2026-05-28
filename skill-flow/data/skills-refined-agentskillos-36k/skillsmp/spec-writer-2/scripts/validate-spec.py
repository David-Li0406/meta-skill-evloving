#!/usr/bin/env python3
"""
Validate spec cross-references, IDs, and structure.

Usage:
    validate-spec.py
    validate-spec.py --discovery-path ../discovery
"""

import sys
import argparse
from pathlib import Path

# Add lib to path
sys.path.insert(0, str(Path(__file__).parent / 'lib'))

from lib import find_discovery_dir
from lib.cross_references import CrossReferenceValidator
from lib.validators import StructureValidator


def main():
    parser = argparse.ArgumentParser(
        description='Validate spec cross-references, IDs, and structure'
    )
    parser.add_argument(
        '--discovery-path',
        help='Path to discovery/ directory'
    )

    args = parser.parse_args()

    try:
        # Find discovery directory
        discovery_dir = find_discovery_dir(args.discovery_path)

        print(f"Validating spec in: {discovery_dir}")
        print("")

        # Run validations
        errors = []
        warnings = []

        # Structure validation
        print("Checking file structure...")
        validator = StructureValidator(discovery_dir)
        structure_errors = validator.validate_all()
        errors.extend([e for e in structure_errors if e.severity == 'ERROR'])
        warnings.extend([e for e in structure_errors if e.severity == 'WARN'])

        # Cross-reference validation
        print("Checking cross-references...")
        cross_ref_validator = CrossReferenceValidator(discovery_dir)
        ref_errors = cross_ref_validator.validate_references()
        errors.extend([e for e in ref_errors if e.severity == 'ERROR'])
        warnings.extend([e for e in ref_errors if e.severity == 'WARN'])

        print("")

        # Report errors
        if errors:
            print(f"ERRORS ({len(errors)}):")
            for error in errors:
                if error.file:
                    print(f"  ERROR [{error.file}]: {error.message}")
                else:
                    print(f"  ERROR: {error.message}")
            print("")

        # Report warnings
        if warnings:
            print(f"WARNINGS ({len(warnings)}):")
            for warning in warnings:
                if warning.file:
                    print(f"  WARN [{warning.file}]: {warning.message}")
                else:
                    print(f"  WARN: {warning.message}")
            print("")

        # Summary
        if not errors and not warnings:
            print("✓ All validations passed!")
            print("")
            return 0
        elif errors:
            print(f"✗ Validation failed with {len(errors)} error(s) and {len(warnings)} warning(s)")
            print("")
            return 1
        else:
            print(f"⚠ Validation passed with {len(warnings)} warning(s)")
            print("")
            return 2

    except FileNotFoundError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"ERROR: Unexpected error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
