#!/usr/bin/env python3
"""Container environment detection utilities.

Shared utilities for detecting whether code is running inside a container
(Docker/Podman) and determining the appropriate command prefix.
"""

from pathlib import Path


def is_inside_container() -> bool:
    """Detect if running inside a container (Docker/Podman).

    Checks for:
    - /.dockerenv (Docker)
    - /run/.containerenv (Podman)
    - /app/pyproject.toml (mounted workspace)

    Returns:
        True if running inside a container, False otherwise.
    """
    return Path("/.dockerenv").exists() or Path("/run/.containerenv").exists() or (Path("/app").exists() and Path("/app/pyproject.toml").exists())


def get_command_prefix() -> list[str]:
    """Get command prefix based on environment.

    Returns:
        ['uv', 'run'] if inside container,
        ['podman-compose', 'run', '--rm', 'dev'] if on host.
    """
    if is_inside_container():
        return ["uv", "run"]
    return ["podman-compose", "run", "--rm", "dev"]


def get_uv_command_prefix() -> list[str]:
    """Get command prefix for uv commands (build, sync).

    Returns:
        ['uv'] if inside container,
        ['podman-compose', 'run', '--rm', 'dev', 'uv'] if on host.
    """
    if is_inside_container():
        return ["uv"]
    return ["podman-compose", "run", "--rm", "dev", "uv"]
