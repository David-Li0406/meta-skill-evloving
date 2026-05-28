"""
Agent Skills - Universal skill manager for AI coding assistants.

Manages skills for Codex CLI, Claude Code, Cursor, and other Agent Skills compatible CLIs.
"""
from .discovery import (
    list_skills,
    add_skill,
    remove_skill,
    sync_to_cli,
    sync_all_clis,
    scan_for_skills,
    auto_register_from_scan,
    get_skill_info,
    SKILLS_DIR,
    CLI_SKILL_DIRS,
)

__version__ = "0.1.0"

__all__ = [
    "list_skills",
    "add_skill", 
    "remove_skill",
    "sync_to_cli",
    "sync_all_clis",
    "scan_for_skills",
    "auto_register_from_scan",
    "get_skill_info",
    "SKILLS_DIR",
    "CLI_SKILL_DIRS",
]
