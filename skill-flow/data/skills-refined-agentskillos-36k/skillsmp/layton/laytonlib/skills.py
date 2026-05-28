"""Skill inventory management for Layton.

Skill files are stored in .layton/skills/<name>.md with YAML frontmatter.
The CLI can list known skills, discover new skills, and bootstrap skill files.
"""

import re
from dataclasses import dataclass
from pathlib import Path

from laytonlib.doctor import find_git_root, get_layton_dir


@dataclass
class SkillInfo:
    """Parsed skill file information."""

    name: str
    description: str
    source: str
    path: Path

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "description": self.description,
            "source": self.source,
            "path": str(self.path),
        }


@dataclass
class DiscoveredSkill:
    """Skill discovered from skills/*/SKILL.md."""

    name: str
    description: str
    source: str

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "description": self.description,
            "source": self.source,
        }


def get_skill_template() -> str:
    """Read the skill template from the templates directory.

    Returns:
        The skill template content with {name} placeholder.
    """
    # Template is in templates/skill.md relative to this file's parent
    template_path = Path(__file__).parent.parent / "templates" / "skill.md"
    return template_path.read_text()


# Keep for backwards compatibility with tests
SKILL_TEMPLATE = get_skill_template()


def get_skills_dir() -> Path:
    """Get the .layton/skills/ directory path."""
    return get_layton_dir() / "skills"


def parse_frontmatter(content: str) -> dict | None:
    """Parse YAML frontmatter from markdown content.

    Args:
        content: Markdown file content

    Returns:
        Dict of frontmatter fields, or None if no valid frontmatter
    """
    # Match frontmatter between --- markers
    match = re.match(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return None

    frontmatter_text = match.group(1)
    result = {}

    # Simple YAML parsing for key: value pairs
    for line in frontmatter_text.split("\n"):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" in line:
            key, _, value = line.partition(":")
            result[key.strip()] = value.strip()

    return result if result else None


def list_skills() -> list[SkillInfo]:
    """List all known skills from .layton/skills/.

    Returns:
        List of SkillInfo objects, sorted by name
    """
    skills_dir = get_skills_dir()
    if not skills_dir.exists():
        return []

    skills = []
    for path in skills_dir.glob("*.md"):
        if path.name == ".gitkeep":
            continue

        try:
            content = path.read_text()
            frontmatter = parse_frontmatter(content)
            if frontmatter and "name" in frontmatter:
                skills.append(
                    SkillInfo(
                        name=frontmatter.get("name", path.stem),
                        description=frontmatter.get("description", ""),
                        source=frontmatter.get("source", ""),
                        path=path,
                    )
                )
        except Exception:
            # Skip files that can't be read
            continue

    return sorted(skills, key=lambda s: s.name)


def discover_skills() -> tuple[list[SkillInfo], list[DiscoveredSkill]]:
    """Discover skills by scanning skills/*/SKILL.md.

    Returns:
        Tuple of (known skills, unknown skills)
        - known: Skills with files in .layton/skills/
        - unknown: Skills without files (need to be added)
    """
    git_root = find_git_root()
    base = git_root if git_root else Path.cwd()
    skills_root = base / "skills"

    if not skills_root.exists():
        return [], []

    # Get current known skills
    known_skills = {s.name: s for s in list_skills()}

    # Scan for SKILL.md files
    known = []
    unknown = []

    for skill_md in skills_root.glob("*/SKILL.md"):
        skill_name = skill_md.parent.name

        # Exclude layton itself
        if skill_name == "layton":
            continue

        # Parse frontmatter from SKILL.md
        try:
            content = skill_md.read_text()
            frontmatter = parse_frontmatter(content)
            description = frontmatter.get("description", "") if frontmatter else ""
        except Exception:
            description = ""

        source = f"skills/{skill_name}/SKILL.md"

        if skill_name in known_skills:
            known.append(known_skills[skill_name])
        else:
            unknown.append(
                DiscoveredSkill(
                    name=skill_name,
                    description=description,
                    source=source,
                )
            )

    return known, unknown


def add_skill(name: str) -> Path:
    """Create a new skill file from template.

    Args:
        name: Skill name (lowercase identifier)

    Returns:
        Path to the created file

    Raises:
        FileExistsError: If skill file already exists (code: SKILL_EXISTS)
    """
    skills_dir = get_skills_dir()
    skill_path = skills_dir / f"{name}.md"

    if skill_path.exists():
        raise FileExistsError(f"Skill file already exists: {skill_path}")

    # Create directory if needed
    skills_dir.mkdir(parents=True, exist_ok=True)

    # Write template
    content = SKILL_TEMPLATE.format(name=name)
    skill_path.write_text(content)

    return skill_path
