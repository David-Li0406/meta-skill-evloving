#!/usr/bin/env python3
"""
Agent Skills Manager - Discover, register, and manage skills for AI CLIs.

Works with: Codex CLI, Claude Code, Cursor, and any Agent Skills compatible CLI.

Central skills directory: ~/.local/share/agent-skills/
Each skill is a symlink to a directory containing SKILL.md
"""
import json
import os
from pathlib import Path
from typing import Optional, List, Dict, Any

# Default paths
SKILLS_DIR = Path.home() / ".local/share/agent-skills"
CONFIG_DIR = Path.home() / ".config/agent-skills"
INDEX_FILE = SKILLS_DIR / "skills-index.json"

# Known CLI skill directories
CLI_SKILL_DIRS = {
    "codex": Path.home() / ".codex/skills",
    "claude": Path.home() / ".claude/skills", 
    "cursor": Path.home() / ".cursor/skills",
}


def ensure_dirs():
    """Ensure skills directories exist."""
    SKILLS_DIR.mkdir(parents=True, exist_ok=True)
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)


def parse_skill_md(skill_path: Path) -> Optional[Dict[str, Any]]:
    """Parse SKILL.md frontmatter and content."""
    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        return None
    
    content = skill_md.read_text()
    
    # Parse YAML frontmatter
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            try:
                import yaml
                frontmatter = yaml.safe_load(parts[1])
                body = parts[2].strip()
                return {
                    "path": str(skill_path),
                    "skill_md": str(skill_md),
                    **frontmatter,
                    "body_preview": body[:500] + "..." if len(body) > 500 else body,
                }
            except Exception:
                pass
    
    return {
        "path": str(skill_path),
        "skill_md": str(skill_md),
        "name": skill_path.name,
        "description": "No frontmatter found",
    }


def list_skills() -> List[Dict[str, Any]]:
    """List all registered skills."""
    ensure_dirs()
    skills = []
    
    for item in SKILLS_DIR.iterdir():
        if item.name.startswith('.'):
            continue
        if item.is_symlink() or item.is_dir():
            target = item.resolve() if item.is_symlink() else item
            skill_info = parse_skill_md(target)
            if skill_info:
                skill_info["registered_name"] = item.name
                skill_info["is_symlink"] = item.is_symlink()
                skills.append(skill_info)
    
    return skills


def add_skill(source_path: str, name: Optional[str] = None) -> tuple[bool, str]:
    """Add a skill to the central directory."""
    ensure_dirs()
    
    source = Path(source_path).expanduser().resolve()
    
    if not source.exists():
        return False, f"Source path does not exist: {source}"
    
    # Check for SKILL.md
    skill_md = source / "SKILL.md"
    if not skill_md.exists():
        return False, f"No SKILL.md found in {source}"
    
    # Parse to get name
    skill_info = parse_skill_md(source)
    if not skill_info:
        return False, f"Could not parse SKILL.md in {source}"
    
    skill_name = name or skill_info.get("name", source.name)
    
    # Create symlink in central dir
    dest = SKILLS_DIR / skill_name
    if dest.exists() or dest.is_symlink():
        dest.unlink()
    
    dest.symlink_to(source)
    
    # Update index
    update_index()
    
    return True, f"✓ Added skill '{skill_name}' → {source}"


def remove_skill(name: str) -> tuple[bool, str]:
    """Remove a skill from the central directory."""
    ensure_dirs()
    
    skill_path = SKILLS_DIR / name
    if not skill_path.exists() and not skill_path.is_symlink():
        return False, f"Skill '{name}' not found"
    
    skill_path.unlink()
    update_index()
    
    return True, f"✓ Removed skill '{name}'"


def sync_to_cli(cli: str) -> tuple[bool, str]:
    """Sync skills to a specific CLI's skill directory."""
    if cli not in CLI_SKILL_DIRS:
        return False, f"Unknown CLI: {cli}. Known: {list(CLI_SKILL_DIRS.keys())}"
    
    cli_dir = CLI_SKILL_DIRS[cli]
    cli_dir.mkdir(parents=True, exist_ok=True)
    
    synced = []
    for skill in list_skills():
        name = skill["registered_name"]
        source = SKILLS_DIR / name
        dest = cli_dir / name
        
        # Skip if non-symlink exists (don't overwrite user files)
        if dest.exists() and not dest.is_symlink():
            continue
        
        if dest.is_symlink():
            dest.unlink()
        
        dest.symlink_to(source)
        synced.append(name)
    
    return True, f"✓ Synced {len(synced)} skills to {cli}: {synced}"


def sync_all_clis() -> List[str]:
    """Sync skills to all known CLIs."""
    results = []
    for cli in CLI_SKILL_DIRS:
        success, msg = sync_to_cli(cli)
        results.append(msg)
    return results


def scan_for_skills(search_path: str) -> List[Dict[str, Any]]:
    """Scan a directory for SKILL.md files."""
    search = Path(search_path).expanduser().resolve()
    found = []
    
    for skill_md in search.rglob("SKILL.md"):
        skill_dir = skill_md.parent
        skill_info = parse_skill_md(skill_dir)
        if skill_info:
            # Check if already registered
            skill_name = skill_info.get("name", skill_dir.name)
            registered = SKILLS_DIR / skill_name
            skill_info["is_registered"] = registered.exists() or registered.is_symlink()
            found.append(skill_info)
    
    return found


def auto_register_from_scan(search_path: str) -> List[str]:
    """Scan for skills and auto-register any not already registered."""
    results = []
    for skill in scan_for_skills(search_path):
        if not skill.get("is_registered"):
            name = skill.get("name", Path(skill["path"]).name)
            success, msg = add_skill(skill["path"], name)
            results.append(msg)
    return results


def update_index():
    """Update the skills index file."""
    skills = list_skills()
    index = {
        "version": "1.0",
        "skills_dir": str(SKILLS_DIR),
        "skills_count": len(skills),
        "skills": {s["registered_name"]: {
            "name": s.get("name"),
            "description": str(s.get("description", ""))[:200],
            "path": s.get("path"),
            "version": s.get("metadata", {}).get("version") if isinstance(s.get("metadata"), dict) else s.get("version"),
        } for s in skills}
    }
    
    INDEX_FILE.write_text(json.dumps(index, indent=2))


def get_skill_info(name: str) -> Optional[Dict[str, Any]]:
    """Get detailed info about a skill."""
    skill_path = SKILLS_DIR / name
    if not skill_path.exists() and not skill_path.is_symlink():
        return None
    
    target = skill_path.resolve() if skill_path.is_symlink() else skill_path
    return parse_skill_md(target)
