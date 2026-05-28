#!/usr/bin/env python3
"""
Shared utilities for Agent Centric framework.

Managed by: agent-centric skill (auto-updated, do not edit manually)
To disable auto-update, add this filename to disableAutoUpdateScripts in config.json.
"""

import json
import os
import re
import sys
from pathlib import Path

# Directory constants
AGENTS_DIR = '.agents'
DECISIONS_DIR = 'decisions'
AGD_PATTERN = 'AGD-*.md'

# Frontmatter field constants
REF_FIELDS = ['obsoleted_by', 'updated_by', 'updates', 'obsoletes']

# Relationship type constants (for index generation)
REL_OBSOLETES = 'o'
REL_UPDATES = 'u'
RELATION_FIELDS = [
    ('obsoletes', REL_OBSOLETES),
    ('updates', REL_UPDATES),
]


def get_project_dir() -> Path:
    """Get project directory from CLAUDE_PROJECT_DIR env var or CLI argument.

    Exits with error if neither is available.
    """
    project_dir_str = os.environ.get('CLAUDE_PROJECT_DIR', '')
    if project_dir_str:
        return Path(project_dir_str)
    if len(sys.argv) >= 2:
        return Path(sys.argv[1])
    print("Error: CLAUDE_PROJECT_DIR not set", file=sys.stderr)
    sys.exit(2)


def load_config(config_path: Path) -> dict | None:
    """Load config.json, returning None on failure."""
    if not config_path.exists():
        return None
    try:
        with open(config_path) as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return None


def parse_frontmatter(content: str) -> dict[str, str]:
    """Parse YAML frontmatter from markdown content."""
    if not content.startswith('---'):
        return {}

    parts = content.split('---', 2)
    if len(parts) < 3:
        return {}

    frontmatter = {}
    for line in parts[1].strip().split('\n'):
        if ':' in line:
            key, value = line.split(':', 1)
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            frontmatter[key] = value

    return frontmatter


def get_agd_id(filename: str) -> str | None:
    """Extract AGD ID from filename (e.g., AGD-001 from AGD-001_name.md)."""
    match = re.match(r'(AGD-\d+)', filename)
    return match.group(1) if match else None


def get_agd_sort_key(path: str) -> int:
    """Extract AGD number as integer for sorting."""
    match = re.search(r'AGD-(\d+)', path)
    return int(match.group(1)) if match else 0


def find_agd_file(decisions_dir: Path, agd_ref: str) -> Path | None:
    """Find AGD file by its number reference."""
    agd_id = get_agd_id(agd_ref)
    if not agd_id:
        return None

    matches = list(decisions_dir.glob(f'{agd_id}_*.md'))
    return matches[0] if matches else None


def get_decisions_dir(project_dir: Path) -> Path:
    """Get the decisions directory path."""
    return project_dir / AGENTS_DIR / DECISIONS_DIR


def get_agents_dir(project_dir: Path) -> Path:
    """Get the .agents directory path."""
    return project_dir / AGENTS_DIR
