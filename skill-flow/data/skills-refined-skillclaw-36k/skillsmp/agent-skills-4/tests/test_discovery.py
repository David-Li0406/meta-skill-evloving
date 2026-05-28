"""Tests for agent_skills module."""
import tempfile
import os
from pathlib import Path
import pytest

from agent_skills.discovery import (
    list_skills,
    add_skill,
    remove_skill,
    scan_for_skills,
    get_skill_info,
    parse_skill_md,
    SKILLS_DIR,
)


@pytest.fixture
def temp_skill_dir():
    """Create a temporary skill directory with SKILL.md."""
    with tempfile.TemporaryDirectory() as tmpdir:
        skill_md = Path(tmpdir) / "SKILL.md"
        skill_md.write_text("""---
name: test-skill
description: A test skill for pytest
metadata:
  version: 1.0.0
compatibility:
  - codex-cli
  - claude-code
---

# Test Skill

This is a test skill.
""")
        yield tmpdir


def test_parse_skill_md(temp_skill_dir):
    """Test parsing SKILL.md file."""
    # parse_skill_md expects directory path, not file path
    result = parse_skill_md(Path(temp_skill_dir))
    
    assert result is not None
    assert result["name"] == "test-skill"
    assert result["description"] == "A test skill for pytest"
    assert result["metadata"]["version"] == "1.0.0"


def test_scan_for_skills(temp_skill_dir):
    """Test scanning for skills."""
    skills = scan_for_skills(temp_skill_dir)
    
    assert len(skills) == 1
    assert skills[0]["name"] == "test-skill"


def test_add_and_remove_skill(temp_skill_dir):
    """Test adding and removing a skill."""
    # Add
    success, msg = add_skill(temp_skill_dir, "pytest-test-skill")
    assert success
    assert "pytest-test-skill" in msg
    
    # Verify it exists
    skills = list_skills()
    names = [s.get("registered_name", s.get("name")) for s in skills]
    assert "pytest-test-skill" in names
    
    # Get info
    info = get_skill_info("pytest-test-skill")
    assert info is not None
    assert info["description"] == "A test skill for pytest"
    
    # Remove
    success, msg = remove_skill("pytest-test-skill")
    assert success
    
    # Verify removed
    info = get_skill_info("pytest-test-skill")
    assert info is None


def test_list_skills():
    """Test listing skills."""
    skills = list_skills()
    assert isinstance(skills, list)


def test_add_nonexistent_path():
    """Test adding from nonexistent path fails."""
    success, msg = add_skill("/nonexistent/path/to/skill")
    assert not success
    assert "not found" in msg.lower() or "does not exist" in msg.lower()


def test_remove_nonexistent_skill():
    """Test removing nonexistent skill fails."""
    success, msg = remove_skill("definitely-not-a-real-skill-name-xyz")
    assert not success


def test_get_skill_info_nonexistent():
    """Test getting info for nonexistent skill."""
    info = get_skill_info("definitely-not-a-real-skill-name-xyz")
    assert info is None


def test_scan_empty_directory():
    """Test scanning directory with no skills."""
    with tempfile.TemporaryDirectory() as tmpdir:
        skills = scan_for_skills(tmpdir)
        assert skills == []
