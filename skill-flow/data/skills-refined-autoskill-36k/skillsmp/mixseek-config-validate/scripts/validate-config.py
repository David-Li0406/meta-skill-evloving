#!/usr/bin/env python3
"""
MixSeek Configuration Validator

Validates MixSeek TOML configuration files against their schemas.
Uses existing Pydantic schemas from mixseek.config.schema.

Usage:
    python validate-config.py <config-file> [--type TYPE] [--json] [--verbose]

Arguments:
    config-file     Path to the TOML configuration file

Options:
    --type TYPE     Config type: team, orchestrator, evaluator, judgment (auto-detected if not specified)
    --json          Output results as JSON
    --verbose       Show detailed validation information
"""

from __future__ import annotations

import argparse
import json
import sys
import tomllib
from pathlib import Path
from typing import NotRequired, TypedDict

from pydantic import ValidationError


class ValidationError_(TypedDict):
    """Structure for validation errors."""

    type: str
    location: NotRequired[str]
    message: str
    input: NotRequired[object]


class ValidationDetails(TypedDict):
    """Structure for verbose details."""

    config_type: str
    parsed_data: dict[str, object]


class ValidationResult(TypedDict):
    """Structure for validation results."""

    file: str
    valid: bool
    errors: list[ValidationError_]
    warnings: list[ValidationError_]
    config_type: NotRequired[str]
    details: NotRequired[ValidationDetails]


def detect_config_type(file_path: Path, data: dict[str, object]) -> str | None:
    """Detect configuration type from file path or content."""
    name = file_path.name.lower()

    # Detect from filename
    if name.startswith("team") or "team" in name:
        return "team"
    if name.startswith("orchestrator") or "orchestrator" in name:
        return "orchestrator"
    if name.startswith("evaluator") or "evaluator" in name:
        return "evaluator"
    if name.startswith("judgment") or "judgment" in name:
        return "judgment"

    # Detect from content
    if "team" in data:
        return "team"
    if "orchestrator" in data:
        return "orchestrator"
    if "metrics" in data or "default_model" in data:
        return "evaluator"

    return None


def _extract_section(data: dict[str, object], section_key: str) -> dict[str, object]:
    """Extract nested section from TOML data if present.

    TOML files use section headers like [team], [orchestrator], etc.
    Pydantic schemas expect the inner dict without the wrapper key.

    Args:
        data: Parsed TOML data
        section_key: The section key to extract (e.g., "team", "orchestrator")

    Returns:
        The inner dict if section_key exists, otherwise the original data
    """
    section = data.get(section_key)
    if isinstance(section, dict):
        return section
    return data


def validate_team_config(data: dict[str, object]) -> list[ValidationError_]:
    """Validate team configuration using Pydantic schema."""
    from mixseek.config.schema import TeamSettings

    errors: list[ValidationError_] = []
    # Extract [team] section if present
    team_data = _extract_section(data, "team")

    try:
        TeamSettings.model_validate(team_data)
    except ValidationError as e:
        for error in e.errors():
            errors.append(
                ValidationError_(
                    type="schema_error",
                    location=".".join(str(loc) for loc in error["loc"]),
                    message=error["msg"],
                    input=error.get("input"),
                )
            )

    return errors


def validate_orchestrator_config(data: dict[str, object]) -> list[ValidationError_]:
    """Validate orchestrator configuration using Pydantic schema."""
    from mixseek.config.schema import OrchestratorSettings

    errors: list[ValidationError_] = []
    # Extract [orchestrator] section if present
    orchestrator_data = _extract_section(data, "orchestrator")

    try:
        OrchestratorSettings.model_validate(orchestrator_data)
    except ValidationError as e:
        for error in e.errors():
            errors.append(
                ValidationError_(
                    type="schema_error",
                    location=".".join(str(loc) for loc in error["loc"]),
                    message=error["msg"],
                    input=error.get("input"),
                )
            )

    return errors


def validate_evaluator_config(data: dict[str, object]) -> list[ValidationError_]:
    """Validate evaluator configuration using Pydantic schema."""
    from mixseek.config.schema import EvaluatorSettings

    errors: list[ValidationError_] = []
    # Evaluator config does not use a wrapper section

    try:
        EvaluatorSettings.model_validate(data)
    except ValidationError as e:
        for error in e.errors():
            errors.append(
                ValidationError_(
                    type="schema_error",
                    location=".".join(str(loc) for loc in error["loc"]),
                    message=error["msg"],
                    input=error.get("input"),
                )
            )

    return errors


def validate_judgment_config(data: dict[str, object]) -> list[ValidationError_]:
    """Validate judgment configuration using Pydantic schema."""
    from mixseek.config.schema import JudgmentSettings

    errors: list[ValidationError_] = []
    # Judgment config does not use a wrapper section

    try:
        JudgmentSettings.model_validate(data)
    except ValidationError as e:
        for error in e.errors():
            errors.append(
                ValidationError_(
                    type="schema_error",
                    location=".".join(str(loc) for loc in error["loc"]),
                    message=error["msg"],
                    input=error.get("input"),
                )
            )

    return errors


def validate_config(
    file_path: Path, config_type: str | None = None, verbose: bool = False
) -> ValidationResult:
    """Validate a configuration file.

    Args:
        file_path: Path to the configuration file
        config_type: Type of configuration (team, orchestrator, evaluator, judgment)
        verbose: Include detailed validation information

    Returns:
        Validation result dictionary
    """
    errors: list[ValidationError_] = []
    warnings: list[ValidationError_] = []

    # Check file exists
    if not file_path.exists():
        errors.append(
            ValidationError_(
                type="file_error",
                message=f"File not found: {file_path}",
            )
        )
        return ValidationResult(
            file=str(file_path),
            valid=False,
            errors=errors,
            warnings=warnings,
        )

    # Parse TOML
    try:
        with open(file_path, "rb") as f:
            data: dict[str, object] = tomllib.load(f)
    except tomllib.TOMLDecodeError as e:
        errors.append(
            ValidationError_(
                type="toml_syntax_error",
                message=str(e),
            )
        )
        return ValidationResult(
            file=str(file_path),
            valid=False,
            errors=errors,
            warnings=warnings,
        )

    # Detect config type if not specified
    if config_type is None:
        config_type = detect_config_type(file_path, data)
        if config_type is None:
            errors.append(
                ValidationError_(
                    type="detection_error",
                    message="Could not detect configuration type. Use --type to specify.",
                )
            )
            return ValidationResult(
                file=str(file_path),
                valid=False,
                errors=errors,
                warnings=warnings,
            )

    # Validate based on type
    validators = {
        "team": validate_team_config,
        "orchestrator": validate_orchestrator_config,
        "evaluator": validate_evaluator_config,
        "judgment": validate_judgment_config,
    }

    validator = validators.get(config_type)
    if validator is None:
        errors.append(
            ValidationError_(
                type="type_error",
                message=f"Unknown config type: {config_type}",
            )
        )
        return ValidationResult(
            file=str(file_path),
            valid=False,
            errors=errors,
            warnings=warnings,
            config_type=config_type,
        )

    validation_errors = validator(data)
    errors.extend(validation_errors)

    # Build result
    is_valid = len(errors) == 0
    result = ValidationResult(
        file=str(file_path),
        valid=is_valid,
        errors=errors,
        warnings=warnings,
        config_type=config_type,
    )

    # Add verbose information
    if verbose and is_valid:
        result["details"] = ValidationDetails(
            config_type=config_type,
            parsed_data=data,
        )

    return result


def format_result_text(result: ValidationResult) -> str:
    """Format validation result as human-readable text."""
    lines: list[str] = []

    file_name = Path(result["file"]).name
    lines.append(f"Validating: {file_name}")
    lines.append("")

    config_type = result.get("config_type")
    if config_type:
        lines.append(f"Config type: {config_type}")
        lines.append("")

    if result["valid"]:
        lines.append("✅ Validation PASSED")
        lines.append("")
        lines.append("All checks passed:")
        lines.append("  ✓ TOML syntax: OK")
        lines.append("  ✓ Required fields: OK")
        lines.append("  ✓ Field types: OK")
        lines.append("  ✓ Value ranges: OK")
    else:
        lines.append("❌ Validation FAILED")
        lines.append("")
        lines.append(f"Found {len(result['errors'])} error(s):")
        lines.append("")

        for i, error in enumerate(result["errors"], 1):
            error_type = error.get("type", "unknown")
            location = error.get("location", "")
            message = error.get("message", "Unknown error")

            lines.append(f"{i}. [{error_type}]")
            if location:
                lines.append(f"   Location: {location}")
            lines.append(f"   Message: {message}")

            # Add fix suggestion
            if "input" in error:
                lines.append(f"   Current value: {error['input']}")

            lines.append("")

    if result.get("warnings"):
        lines.append("Warnings:")
        for warning in result["warnings"]:
            lines.append(f"  ⚠ {warning['message']}")

    return "\n".join(lines)


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Validate MixSeek TOML configuration files"
    )
    parser.add_argument("config_file", type=Path, help="Path to configuration file")
    parser.add_argument(
        "--type",
        choices=["team", "orchestrator", "evaluator", "judgment"],
        help="Configuration type (auto-detected if not specified)",
    )
    parser.add_argument("--json", action="store_true", help="Output results as JSON")
    parser.add_argument(
        "--verbose", action="store_true", help="Show detailed information"
    )

    args = parser.parse_args()

    # Run validation
    result = validate_config(
        file_path=args.config_file,
        config_type=args.type,
        verbose=args.verbose,
    )

    # Output result
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(format_result_text(result))

    # Return exit code
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    sys.exit(main())
