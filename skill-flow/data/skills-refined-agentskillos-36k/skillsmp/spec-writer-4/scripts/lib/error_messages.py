"""
Standardized error messages with helpful context and fix guidance.

Provides consistent, informative error messages across all spec-writer scripts.
Each error includes:
- What went wrong
- Expected format/value
- What was received
- How to fix it
- Example of correct usage
"""

from typing import List, Optional


class ErrorMessages:
    """Standard error message templates."""

    @staticmethod
    def format_error(what: str, expected: str, received: str, fix: str, example: str) -> str:
        """
        Format a comprehensive error message.

        Args:
            what: Description of what went wrong
            expected: What format/value was expected
            received: What was actually received
            fix: How to fix the error
            example: Example of correct usage

        Returns:
            Formatted multi-line error message
        """
        return f"""
ERROR: {what}

EXPECTED: {expected}
RECEIVED: {received}

FIX: {fix}

EXAMPLE: {example}
""".strip()

    @staticmethod
    def missing_required_field(field: str, script: str) -> str:
        """Error for missing required arguments."""
        return ErrorMessages.format_error(
            what=f"Missing required field: {field}",
            expected=f"The --{field} argument must be provided",
            received="No value provided",
            fix=f"Add --{field} \"your value here\" to the command",
            example=f"{script} --{field} \"example value\" [other required args...]"
        )

    @staticmethod
    def invalid_id_format(
        received: str,
        entity_type: str,
        expected_format: str,
        suggestions: Optional[List[str]] = None
    ) -> str:
        """Error for wrong ID format with suggestions."""
        fix_parts = [f"Use the expected format: {expected_format}"]

        if suggestions:
            fix_parts.append("Or did you mean one of these?")
            for suggestion in suggestions[:5]:
                fix_parts.append(f"  - {suggestion}")

        fix_text = "\n".join(fix_parts)

        return ErrorMessages.format_error(
            what=f"Invalid {entity_type.replace('_', ' ')} ID format",
            expected=f"{expected_format}",
            received=f"{received}",
            fix=fix_text,
            example=f"Flexible formats accepted:\n  - {expected_format.split()[0]}\n  - Variations like {expected_format.split('(')[1].split(')')[0] if '(' in expected_format else 'various formats'}"
        )

    @staticmethod
    def invalid_reference(
        id_value: str,
        entity_type: str,
        file_name: str,
        suggestions: Optional[List[str]] = None
    ) -> str:
        """Error for broken references with suggestions."""
        entity_name = entity_type.replace('_', ' ').title()

        fix_parts = [f"Verify that {entity_name} {id_value} exists in {file_name}"]

        if suggestions:
            fix_parts.append("\nDid you mean one of these?")
            for suggestion in suggestions[:5]:
                fix_parts.append(f"  - {suggestion}")
        else:
            fix_parts.append(f"\nRun the appropriate find-* script to see all available {entity_type}s")

        fix_text = "\n".join(fix_parts)

        return ErrorMessages.format_error(
            what=f"{entity_name} {id_value} not found",
            expected=f"A {entity_name} that exists in {file_name}",
            received=f"{id_value}",
            fix=fix_text,
            example=f"Check existing IDs with: find-{entity_type.replace('_', '-')}s.py"
        )

    @staticmethod
    def pipe_input_format_error(expected_fields: List[str], received_count: int, example: str) -> str:
        """Error for pipe-separated input format issues."""
        field_list = " | ".join(expected_fields)

        return ErrorMessages.format_error(
            what="Invalid pipe-separated input format",
            expected=f"Pipe-separated fields: {field_list}",
            received=f"{received_count} field(s) provided",
            fix=f"Ensure input has {len(expected_fields)} pipe-separated fields.\nFor complex data with special characters, consider using JSON input instead (--from-json)",
            example=f'echo "{example}" | script.py --from-stdin'
        )

    @staticmethod
    def validation_failed(
        what_failed: str,
        why: str,
        how_to_fix: str,
        example: Optional[str] = None
    ) -> str:
        """Error for validation failures."""
        msg = f"""
ERROR: Validation failed: {what_failed}

REASON: {why}

FIX: {how_to_fix}
"""
        if example:
            msg += f"\nEXAMPLE: {example}"

        return msg.strip()

    @staticmethod
    def story_not_ready_for_graduation(
        story_num: int,
        failing_checks: List[str],
        current_status: Optional[str] = None
    ) -> str:
        """Error when story cannot be graduated."""
        checks_text = "\n".join(f"  ❌ {check}" for check in failing_checks)

        if current_status:
            status_info = f"\n\nCurrent status: {current_status}"
        else:
            status_info = ""

        return ErrorMessages.validation_failed(
            what_failed=f"Story {story_num} is not ready for graduation",
            why=f"The following pre-graduation checks failed:\n{checks_text}{status_info}",
            how_to_fix=f"Complete the failing requirements:\n"
                      f"1. Ensure story is marked '🔄 In Progress' in STATE.md status table\n"
                      f"2. Add story details to '## In-Progress Story Detail' section\n"
                      f"3. Include 'Draft Acceptance Scenarios' with Given/When/Then format\n"
                      f"4. Resolve any blocking questions\n\n"
                      f"Then run: graduate-story.py --story {story_num}",
            example=f"Check story status with: story-status.sh"
        )

    @staticmethod
    def file_not_found_with_init_suggestion(file_name: str, discovery_dir: str) -> str:
        """Error when required file doesn't exist."""
        return ErrorMessages.validation_failed(
            what_failed=f"{file_name} not found",
            why=f"The required file {file_name} doesn't exist in {discovery_dir}",
            how_to_fix=f"Initialize the spec structure with: init-spec.sh\n"
                      f"Or create {file_name} manually following the template structure",
            example="cd /path/to/spec && ../scripts/init-spec.sh"
        )

    @staticmethod
    def stdin_json_parse_error(error_detail: str, json_content: str) -> str:
        """Error when JSON input cannot be parsed."""
        # Truncate JSON if too long
        json_preview = json_content[:200] + "..." if len(json_content) > 200 else json_content

        return ErrorMessages.format_error(
            what="Failed to parse JSON input",
            expected="Valid JSON object matching the schema",
            received=f"Invalid JSON:\n{json_preview}",
            fix=f"Check JSON syntax:\n"
                f"  - All strings use double quotes, not single quotes\n"
                f"  - No trailing commas\n"
                f"  - Properly escaped special characters\n"
                f"  - Balanced brackets and braces\n\n"
                f"Error details: {error_detail}",
            example='cat > /tmp/input.json <<EOF\n'
                   '{\n'
                   '  "field1": "value1",\n'
                   '  "field2": "value2"\n'
                   '}\n'
                   'EOF\n'
                   'cat /tmp/input.json | script.py --from-json'
        )

    @staticmethod
    def json_schema_validation_error(errors: List[str], schema_file: Optional[str] = None) -> str:
        """Error when JSON doesn't match schema."""
        error_list = "\n".join(f"  - {err}" for err in errors)

        schema_info = f"\nSee schema: {schema_file}" if schema_file else ""

        return ErrorMessages.validation_failed(
            what_failed="JSON input doesn't match expected schema",
            why=f"The following validation errors were found:\n{error_list}{schema_info}",
            how_to_fix="Review the schema requirements and fix the JSON structure.\n"
                      "Ensure all required fields are present and have correct types.",
            example="See schemas/ directory for examples and documentation"
        )

    @staticmethod
    def cross_reference_validation_failed(
        reference_type: str,
        reference_id: str,
        source_file: str,
        suggestions: Optional[List[str]] = None
    ) -> str:
        """Error when cross-reference validation fails."""
        ref_name = reference_type.replace('_', ' ').title()

        fix_parts = [
            f"Ensure {ref_name} {reference_id} exists before referencing it",
            f"Run validation: validate-spec.py"
        ]

        if suggestions:
            fix_parts.append("\nDid you mean one of these?")
            for suggestion in suggestions[:5]:
                fix_parts.append(f"  - {suggestion}")

        fix_text = "\n".join(fix_parts)

        return ErrorMessages.validation_failed(
            what_failed=f"Cross-reference validation failed",
            why=f"{ref_name} {reference_id} referenced in {source_file} doesn't exist",
            how_to_fix=fix_text,
            example=f"Create the {reference_type} first, then reference it"
        )
