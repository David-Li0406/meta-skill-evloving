#!/usr/bin/env python3
"""
Log Validation Utilities

This script validates log files against expected schemas and formats.
"""

import json
import re
import sys
import argparse
from typing import Dict, List, Any, Optional, Tuple
import jsonschema
from datetime import datetime


class LogValidator:
    def __init__(self):
        # Base schema for structured logs
        self.base_schema = {
            "type": "object",
            "required": ["timestamp", "level", "event"],
            "properties": {
                "timestamp": {
                    "type": "string",
                    "pattern": r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}"
                },
                "level": {
                    "type": "string",
                    "enum": ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
                },
                "event": {
                    "type": "string",
                    "minLength": 1
                }
            }
        }

        # Recommended fields
        self.recommended_fields = {
            "logger": {"type": "string"},
            "service": {"type": "string"},
            "request_id": {"type": "string"},
            "user_id": {"type": ["string", "integer"]},
            "duration": {"type": "number"},
            "status_code": {"type": "integer"}
        }

    def validate_json_syntax(self, line: str) -> Tuple[bool, Optional[str]]:
        """Validate JSON syntax of a log line."""
        try:
            json.loads(line.strip())
            return True, None
        except json.JSONDecodeError as e:
            return False, f"JSON syntax error: {e}"

    def validate_log_schema(self, log_entry: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """Validate log entry against schema."""
        errors = []
        warnings = []

        try:
            jsonschema.validate(log_entry, self.base_schema)
        except jsonschema.ValidationError as e:
            errors.append(f"Schema validation error: {e.message}")

        # Check recommended fields
        for field, schema in self.recommended_fields.items():
            if field not in log_entry:
                warnings.append(f"Missing recommended field: {field}")

        # Validate timestamp format
        if 'timestamp' in log_entry:
            timestamp = log_entry['timestamp']
            try:
                # Try parsing timestamp
                datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            except ValueError:
                errors.append(f"Invalid timestamp format: {timestamp}")

        # Validate level consistency
        if 'level' in log_entry:
            level = log_entry['level'].upper()
            if level not in ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']:
                errors.append(f"Invalid log level: {level}")

        # Check for sensitive data patterns
        sensitive_patterns = [
            (r'password\s*[:=]\s*[^\s]+', "Password in log"),
            (r'api_key\s*[:=]\s*[^\s]+', "API key in log"),
            (r'token\s*[:=]\s*[^\s]+', "Token in log"),
            (r'secret\s*[:=]\s*[^\s]+', "Secret in log"),
        ]

        log_text = json.dumps(log_entry, default=str).lower()
        for pattern, message in sensitive_patterns:
            if re.search(pattern, log_text):
                warnings.append(message)

        return len(errors) == 0, errors + warnings

    def validate_log_file(self, file_path: str) -> Dict[str, Any]:
        """Validate an entire log file."""
        results = {
            'total_lines': 0,
            'valid_json': 0,
            'valid_schema': 0,
            'errors': [],
            'warnings': [],
            'error_count': 0,
            'warning_count': 0,
            'validation_errors': {}
        }

        with open(file_path, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                if not line.strip():
                    continue

                results['total_lines'] += 1

                # Validate JSON syntax
                is_valid_json, json_error = self.validate_json_syntax(line)
                if not is_valid_json:
                    results['errors'].append(f"Line {line_num}: {json_error}")
                    results['validation_errors'][line_num] = ['json_syntax_error']
                    continue

                results['valid_json'] += 1

                # Parse and validate schema
                try:
                    log_entry = json.loads(line.strip())
                    is_valid_schema, issues = self.validate_log_schema(log_entry)

                    if is_valid_schema:
                        results['valid_schema'] += 1
                    else:
                        results['validation_errors'][line_num] = issues
                        for issue in issues:
                            if 'error' in issue.lower():
                                results['errors'].append(f"Line {line_num}: {issue}")
                                results['error_count'] += 1
                            else:
                                results['warnings'].append(f"Line {line_num}: {issue}")
                                results['warning_count'] += 1

                except Exception as e:
                    results['errors'].append(f"Line {line_num}: Unexpected error: {e}")
                    results['error_count'] += 1

        return results

    def generate_validation_report(self, results: Dict[str, Any]) -> str:
        """Generate a validation report."""
        report = []
        report.append("=== LOG VALIDATION REPORT ===\n")

        # Summary statistics
        report.append(f"Total lines processed: {results['total_lines']:,}")
        report.append(f"Valid JSON entries: {results['valid_json']:,}")
        report.append(f"Valid schema entries: {results['valid_schema']:,}")

        if results['total_lines'] > 0:
            json_valid_rate = (results['valid_json'] / results['total_lines']) * 100
            schema_valid_rate = (results['valid_schema'] / results['total_lines']) * 100
            report.append(f"JSON validity rate: {json_valid_rate:.2f}%")
            report.append(f"Schema validity rate: {schema_valid_rate:.2f}%")

        report.append(f"Errors: {results['error_count']:,}")
        report.append(f"Warnings: {results['warning_count']:,}")
        report.append("")

        # Errors
        if results['errors']:
            report.append("ERRORS:")
            for error in results['errors'][:20]:  # Limit to first 20 errors
                report.append(f"  {error}")
            if len(results['errors']) > 20:
                report.append(f"  ... and {len(results['errors']) - 20} more errors")
            report.append("")

        # Warnings
        if results['warnings']:
            report.append("WARNINGS:")
            for warning in results['warnings'][:20]:  # Limit to first 20 warnings
                report.append(f"  {warning}")
            if len(results['warnings']) > 20:
                report.append(f"  ... and {len(results['warnings']) - 20} more warnings")
            report.append("")

        # Validation summary
        if results['validation_errors']:
            report.append("VALIDATION SUMMARY:")
            error_types = {}
            for line_issues in results['validation_errors'].values():
                for issue in line_issues:
                    error_type = issue.split(':')[0] if ':' in issue else issue
                    error_types[error_type] = error_types.get(error_type, 0) + 1

            for error_type, count in sorted(error_types.items()):
                report.append(f"  {error_type}: {count:,} occurrences")

        # Overall status
        report.append("")
        if results['error_count'] == 0 and results['warning_count'] == 0:
            report.append("✅ PASSED: All log entries are valid")
        elif results['error_count'] == 0:
            report.append("⚠️  PASSED WITH WARNINGS: All log entries are structurally valid but have warnings")
        else:
            report.append("❌ FAILED: Log file contains errors")

        return "\n".join(report)


def main():
    parser = argparse.ArgumentParser(description="Validate log files")
    parser.add_argument("log_file", help="Path to log file")
    parser.add_argument("--schema", help="Custom schema file (JSON)")
    parser.add_argument("--output", help="Output file for validation report")
    parser.add_argument("--strict", action="store_true", help="Fail on warnings")

    args = parser.parse_args()

    validator = LogValidator()

    # Load custom schema if provided
    if args.schema:
        try:
            with open(args.schema, 'r') as f:
                custom_schema = json.load(f)
            validator.base_schema.update(custom_schema)
        except Exception as e:
            print(f"Error loading custom schema: {e}", file=sys.stderr)
            sys.exit(1)

    try:
        print(f"Validating {args.log_file}...")
        results = validator.validate_log_file(args.log_file)
        report = validator.generate_validation_report(results)

        if args.output:
            with open(args.output, 'w') as f:
                f.write(report)
            print(f"Validation report saved to {args.output}")
        else:
            print(report)

        # Exit code based on validation results
        if args.strict and results['warning_count'] > 0:
            sys.exit(1)
        elif results['error_count'] > 0:
            sys.exit(1)
        else:
            sys.exit(0)

    except FileNotFoundError:
        print(f"Error: File {args.log_file} not found", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()