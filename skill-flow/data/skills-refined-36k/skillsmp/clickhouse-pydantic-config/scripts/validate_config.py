# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "pydantic>=2.0",
# ]
# ///
"""Validate DBeaver data-sources.json against expected schema.

ADR: 2025-12-09-clickhouse-pydantic-config-skill

This script validates generated DBeaver configurations to ensure they
conform to the expected structure before use.

Usage:
    uv run scripts/validate_config.py --config .dbeaver/data-sources.json
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field, ValidationError


class DBeaverConnectionConfig(BaseModel):
    """DBeaver connection configuration block."""

    host: str
    port: str
    database: str
    url: str
    type: str = Field(pattern=r"^(dev|test|prod)$")


class DBeaverConnection(BaseModel):
    """Single DBeaver connection entry."""

    provider: str = Field(pattern=r"^clickhouse$")
    driver: str = Field(pattern=r"^com_clickhouse$")
    name: str
    configuration: DBeaverConnectionConfig


class DBeaverDataSources(BaseModel):
    """Complete DBeaver data-sources.json structure."""

    folders: dict[str, Any] = Field(default_factory=dict)
    connections: dict[str, DBeaverConnection]


def validate_config(config_path: Path) -> tuple[bool, list[str]]:
    """Validate DBeaver config file.

    Returns:
        Tuple of (is_valid, list of error messages)
    """
    errors: list[str] = []

    if not config_path.exists():
        return False, [f"Config file not found: {config_path}"]

    try:
        config_data = json.loads(config_path.read_text())
    except json.JSONDecodeError as e:
        return False, [f"Invalid JSON: {e}"]

    try:
        datasources = DBeaverDataSources.model_validate(config_data)
    except ValidationError as e:
        for error in e.errors():
            loc = ".".join(str(x) for x in error["loc"])
            errors.append(f"{loc}: {error['msg']}")
        return False, errors

    # Additional validations
    if not datasources.connections:
        errors.append("No connections defined")
        return False, errors

    for conn_id, conn in datasources.connections.items():
        # Validate connection ID format
        if not conn_id.startswith("clickhouse-jdbc-"):
            errors.append(f"Connection ID should start with 'clickhouse-jdbc-': {conn_id}")

        # Validate JDBC URL consistency
        expected_protocol = "https" if conn.configuration.url.startswith("jdbc:clickhouse:https") else "http"
        port = conn.configuration.port
        if expected_protocol == "https" and port != "8443":
            errors.append(f"HTTPS connection should use port 8443, got {port}")
        if expected_protocol == "http" and port not in ("8123", "9000"):
            errors.append(f"HTTP connection should use port 8123 or 9000, got {port}")

    return len(errors) == 0, errors


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Validate DBeaver config")
    parser.add_argument(
        "--config",
        "-c",
        type=Path,
        default=Path(".dbeaver/data-sources.json"),
        help="Path to data-sources.json",
    )

    args = parser.parse_args()

    is_valid, errors = validate_config(args.config)

    if is_valid:
        print(f"Valid: {args.config}")
        return 0

    print(f"Invalid: {args.config}")
    for error in errors:
        print(f"  - {error}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
