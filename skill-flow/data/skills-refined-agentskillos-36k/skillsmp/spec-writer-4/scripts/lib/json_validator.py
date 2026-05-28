"""
JSON schema validation for script inputs.

Provides validation of JSON input against schemas for complex scripts
like log-decision, log-iteration, and log-research.
"""

import json
import sys
from pathlib import Path
from typing import Dict, Any, List, Tuple, Optional


class JSONValidator:
    """Validate JSON input against schemas."""

    # Schema file paths (relative to schemas/ directory)
    SCHEMAS = {
        'decision': 'decision-input.json',
        'iteration': 'iteration-input.json',
        'research': 'research-input.json'
    }

    @classmethod
    def get_schema_path(cls, schema_name: str) -> Path:
        """
        Get path to schema file.

        Args:
            schema_name: Name of schema (decision, iteration, research)

        Returns:
            Path to schema file

        Raises:
            ValueError: If schema_name is invalid
        """
        if schema_name not in cls.SCHEMAS:
            valid_schemas = ', '.join(cls.SCHEMAS.keys())
            raise ValueError(f"Invalid schema name: {schema_name}. Valid schemas: {valid_schemas}")

        # Find schemas directory (relative to this file)
        lib_dir = Path(__file__).parent
        scripts_dir = lib_dir.parent
        spec_writer_dir = scripts_dir.parent
        schemas_dir = spec_writer_dir / 'schemas'

        schema_file = schemas_dir / cls.SCHEMAS[schema_name]

        if not schema_file.exists():
            raise FileNotFoundError(f"Schema file not found: {schema_file}")

        return schema_file

    @classmethod
    def load_json_from_stdin(cls) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
        """
        Load and parse JSON from stdin.

        Returns:
            Tuple of (parsed_json, error_message)
            - If successful: (dict, None)
            - If failed: (None, error_message)
        """
        try:
            content = sys.stdin.read().strip()
            if not content:
                return (None, "Empty input received from stdin")

            data = json.loads(content)

            if not isinstance(data, dict):
                return (None, f"Expected JSON object, got {type(data).__name__}")

            return (data, None)

        except json.JSONDecodeError as e:
            return (None, f"JSON parse error: {e}")
        except Exception as e:
            return (None, f"Unexpected error reading JSON: {e}")

    @classmethod
    def load_json_from_file(cls, file_path: str) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
        """
        Load and parse JSON from file.

        Args:
            file_path: Path to JSON file

        Returns:
            Tuple of (parsed_json, error_message)
            - If successful: (dict, None)
            - If failed: (None, error_message)
        """
        try:
            path = Path(file_path)
            if not path.exists():
                return (None, f"File not found: {file_path}")

            content = path.read_text(encoding='utf-8')
            data = json.loads(content)

            if not isinstance(data, dict):
                return (None, f"Expected JSON object, got {type(data).__name__}")

            return (data, None)

        except json.JSONDecodeError as e:
            return (None, f"JSON parse error in {file_path}: {e}")
        except Exception as e:
            return (None, f"Error reading {file_path}: {e}")

    @classmethod
    def basic_validate(cls, data: Dict[str, Any], schema_name: str) -> Tuple[bool, List[str]]:
        """
        Perform basic validation against schema.

        This is a simplified validator that checks:
        - Required fields are present
        - Basic type checking for known fields

        Args:
            data: JSON data to validate
            schema_name: Schema to validate against

        Returns:
            Tuple of (is_valid, error_messages)
        """
        errors = []

        # Define required fields and types for each schema
        schema_rules = {
            'decision': {
                'required': ['title', 'context'],
                'optional': {
                    'decision': str,
                    'options_considered': (str, list),
                    'rationale': str,
                    'implications': str,
                    'stories': (int, str, list),
                    'questions': (str, list),
                    'tags': str
                }
            },
            'iteration': {
                'required': ['title', 'focus'],
                'optional': {
                    'plan': str,
                    'execution': str,
                    'results': str,
                    'learnings': str,
                    'next_actions': str,
                    'stories': (int, str, list),
                    'decisions': (str, list)
                }
            },
            'research': {
                'required': ['title', 'question'],
                'optional': {
                    'approach': str,
                    'findings': str,
                    'implications': str,
                    'recommendations': str,
                    'sources': str,
                    'questions': (str, list),
                    'stories': (int, str, list)
                }
            }
        }

        if schema_name not in schema_rules:
            return (False, [f"Unknown schema: {schema_name}"])

        rules = schema_rules[schema_name]

        # Check required fields
        for field in rules['required']:
            if field not in data:
                errors.append(f"Missing required field: '{field}'")
            elif not data[field] or (isinstance(data[field], str) and not data[field].strip()):
                errors.append(f"Required field '{field}' cannot be empty")

        # Check optional field types
        for field, expected_types in rules['optional'].items():
            if field in data and data[field] is not None:
                # Normalize to tuple
                if not isinstance(expected_types, tuple):
                    expected_types = (expected_types,)

                # Check if value matches any expected type
                if not isinstance(data[field], expected_types):
                    type_names = ' or '.join(t.__name__ for t in expected_types)
                    actual_type = type(data[field]).__name__
                    errors.append(f"Field '{field}' has wrong type: expected {type_names}, got {actual_type}")

        return (len(errors) == 0, errors)

    @classmethod
    def normalize_field_value(cls, value: Any, field_name: str) -> str:
        """
        Normalize field values for storage.

        Converts arrays to comma-separated strings, etc.

        Args:
            value: Field value
            field_name: Name of field

        Returns:
            Normalized string value
        """
        if value is None:
            return ""

        if isinstance(value, list):
            # Convert list to comma-separated string
            if all(isinstance(item, (int, str)) for item in value):
                return ", ".join(str(item) for item in value)
            else:
                return str(value)
        elif isinstance(value, (int, float)):
            return str(value)
        elif isinstance(value, str):
            return value.strip()
        else:
            return str(value)

    @classmethod
    def validate_and_normalize(
        cls,
        data: Dict[str, Any],
        schema_name: str
    ) -> Tuple[Optional[Dict[str, str]], Optional[List[str]]]:
        """
        Validate JSON and normalize to string values.

        Args:
            data: JSON data to validate
            schema_name: Schema to validate against

        Returns:
            Tuple of (normalized_data, errors)
            - If valid: (dict with string values, None)
            - If invalid: (None, list of error messages)
        """
        # Validate
        is_valid, errors = cls.basic_validate(data, schema_name)

        if not is_valid:
            return (None, errors)

        # Normalize all values to strings
        normalized = {}
        for key, value in data.items():
            normalized[key] = cls.normalize_field_value(value, key)

        return (normalized, None)
