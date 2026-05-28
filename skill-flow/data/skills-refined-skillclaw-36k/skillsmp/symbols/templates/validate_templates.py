#!/usr/bin/env python3
"""
Validate all symbol configuration templates against the JSON schema.

This script validates each template file to ensure:
1. JSON syntax is valid
2. Configuration conforms to symbols-config-schema.json
3. All required fields are present
4. Field values match expected patterns

Usage:
    python validate_templates.py
    python validate_templates.py --verbose
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Tuple

try:
    import jsonschema
    from jsonschema import Draft7Validator
except ImportError:
    print("Error: jsonschema package is required")
    print("Install with: pip install jsonschema")
    sys.exit(1)


class TemplateValidator:
    """Validates symbol configuration templates against the schema."""

    def __init__(self, schema_path: Path, templates_dir: Path):
        """Initialize validator with schema and templates directory.

        Args:
            schema_path: Path to symbols-config-schema.json
            templates_dir: Path to templates directory
        """
        self.schema_path = schema_path
        self.templates_dir = templates_dir
        self.schema = self._load_schema()
        self.validator = Draft7Validator(self.schema)

    def _load_schema(self) -> dict:
        """Load and parse the JSON schema."""
        try:
            with open(self.schema_path) as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Error: Schema file not found at {self.schema_path}")
            sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON in schema file: {e}")
            sys.exit(1)

    def validate_template(self, template_path: Path) -> Tuple[bool, List[str]]:
        """Validate a single template file.

        Args:
            template_path: Path to template JSON file

        Returns:
            Tuple of (is_valid, error_messages)
        """
        errors = []

        # Load template
        try:
            with open(template_path) as f:
                template = json.load(f)
        except json.JSONDecodeError as e:
            return False, [f"Invalid JSON: {e}"]
        except FileNotFoundError:
            return False, [f"File not found: {template_path}"]

        # Validate against schema
        schema_errors = list(self.validator.iter_errors(template))
        if schema_errors:
            for error in schema_errors:
                path = ".".join(str(p) for p in error.path) if error.path else "root"
                errors.append(f"  [{path}] {error.message}")

        # Additional validation checks
        errors.extend(self._validate_placeholders(template))
        errors.extend(self._validate_structure(template))

        return len(errors) == 0, errors

    def _validate_placeholders(self, template: dict) -> List[str]:
        """Validate that template uses proper placeholders.

        Args:
            template: Parsed template configuration

        Returns:
            List of error messages
        """
        errors = []

        # Check projectName placeholder
        project_name = template.get("projectName", "")
        if "{{" not in project_name and project_name != "{{PROJECT_NAME}}":
            errors.append(
                "  [projectName] Should use {{PROJECT_NAME}} placeholder in template"
            )

        # Check symbolsDir placeholder
        symbols_dir = template.get("symbolsDir", "")
        if "{{" not in symbols_dir and symbols_dir != "{{SYMBOLS_DIR}}":
            errors.append(
                "  [symbolsDir] Should use {{SYMBOLS_DIR}} placeholder in template"
            )

        return errors

    def _validate_structure(self, template: dict) -> List[str]:
        """Validate template structure and consistency.

        Args:
            template: Parsed template configuration

        Returns:
            List of error messages
        """
        errors = []

        # Check that all domains have descriptions
        domains = template.get("domains", {})
        for domain_name, domain_config in domains.items():
            if not domain_config.get("description"):
                errors.append(
                    f"  [domains.{domain_name}] Missing description"
                )

        # Check that all API layers have descriptions
        api_layers = template.get("apiLayers", {})
        for layer_name, layer_config in api_layers.items():
            if not layer_config.get("description"):
                errors.append(
                    f"  [apiLayers.{layer_name}] Missing description"
                )

        # Check extraction configuration
        extraction = template.get("extraction", {})

        # Python extraction
        python_config = extraction.get("python", {})
        if python_config:
            directories = python_config.get("directories", [])
            if not directories:
                errors.append(
                    "  [extraction.python.directories] Should specify at least one directory (or empty array if not used)"
                )

        # TypeScript extraction
        ts_config = extraction.get("typescript", {})
        if ts_config:
            directories = ts_config.get("directories", [])
            if not directories:
                errors.append(
                    "  [extraction.typescript.directories] Should specify at least one directory (or empty array if not used)"
                )

        return errors

    def validate_all(self, verbose: bool = False) -> Tuple[int, int]:
        """Validate all template files in the templates directory.

        Args:
            verbose: If True, print detailed error messages

        Returns:
            Tuple of (valid_count, total_count)
        """
        template_files = sorted(self.templates_dir.glob("*.json"))

        if not template_files:
            print(f"No template files found in {self.templates_dir}")
            return 0, 0

        valid_count = 0
        total_count = len(template_files)

        print(f"Validating {total_count} template(s)...\n")

        for template_path in template_files:
            is_valid, errors = self.validate_template(template_path)

            status = "✓" if is_valid else "✗"
            print(f"{status} {template_path.name}")

            if not is_valid:
                if verbose:
                    print(f"\n  Errors in {template_path.name}:")
                    for error in errors:
                        print(f"    {error}")
                    print()
                else:
                    print(f"  {len(errors)} error(s) found (use --verbose for details)")
            else:
                valid_count += 1

        return valid_count, total_count


def main():
    """Main entry point."""
    # Parse arguments
    verbose = "--verbose" in sys.argv or "-v" in sys.argv

    # Determine paths
    script_dir = Path(__file__).parent
    schema_path = script_dir.parent / "symbols-config-schema.json"
    templates_dir = script_dir

    # Validate templates
    validator = TemplateValidator(schema_path, templates_dir)
    valid_count, total_count = validator.validate_all(verbose=verbose)

    # Print summary
    print(f"\n{'='*60}")
    print(f"Validation Summary:")
    print(f"  Valid:   {valid_count}/{total_count}")
    print(f"  Invalid: {total_count - valid_count}/{total_count}")
    print(f"{'='*60}\n")

    # Exit with appropriate code
    if valid_count == total_count:
        print("✓ All templates are valid!")
        sys.exit(0)
    else:
        print("✗ Some templates failed validation")
        print("  Run with --verbose for detailed error messages")
        sys.exit(1)


if __name__ == "__main__":
    main()
