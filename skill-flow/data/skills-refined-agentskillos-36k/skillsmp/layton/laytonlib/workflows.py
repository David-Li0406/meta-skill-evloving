"""Workflow management for Layton.

Workflow files are stored in .layton/workflows/<name>.md with YAML frontmatter.
The CLI can list workflows and bootstrap new workflow files from templates.
"""

import re
from dataclasses import dataclass, field
from pathlib import Path

from laytonlib.doctor import get_layton_dir


@dataclass
class WorkflowInfo:
    """Parsed workflow file information."""

    name: str
    description: str
    triggers: list[str] = field(default_factory=list)
    path: Path | None = None

    def to_dict(self) -> dict:
        result = {
            "name": self.name,
            "description": self.description,
            "triggers": self.triggers,
        }
        if self.path:
            result["path"] = str(self.path)
        return result


def get_workflow_template() -> str:
    """Read the workflow template from the templates directory.

    Returns:
        The workflow template content with {name} placeholder.
    """
    # Template is in templates/workflow.md relative to this file's parent
    template_path = Path(__file__).parent.parent / "templates" / "workflow.md"
    return template_path.read_text()


# Keep for backwards compatibility with tests
WORKFLOW_TEMPLATE = get_workflow_template()


def get_workflows_dir() -> Path:
    """Get the .layton/workflows/ directory path."""
    return get_layton_dir() / "workflows"


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
    current_key = None
    current_list = None

    # Simple YAML parsing for key: value pairs and lists
    for line in frontmatter_text.split("\n"):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue

        # Check for list item (- value)
        if stripped.startswith("- ") and current_key:
            if current_list is None:
                current_list = []
            current_list.append(stripped[2:].strip())
            result[current_key] = current_list
            continue

        # Check for key: value
        if ":" in stripped:
            # Save previous list if any
            if current_list is not None and current_key:
                result[current_key] = current_list

            key, _, value = stripped.partition(":")
            current_key = key.strip()
            value = value.strip()

            if value:
                result[current_key] = value
                current_list = None
            else:
                # Might be start of a list
                current_list = []

    return result if result else None


def list_workflows() -> list[WorkflowInfo]:
    """List all workflows from .layton/workflows/.

    Returns:
        List of WorkflowInfo objects, sorted by name
    """
    workflows_dir = get_workflows_dir()
    if not workflows_dir.exists():
        return []

    workflows = []
    for path in workflows_dir.glob("*.md"):
        if path.name == ".gitkeep":
            continue

        try:
            content = path.read_text()
            frontmatter = parse_frontmatter(content)
            if frontmatter and "name" in frontmatter:
                triggers = frontmatter.get("triggers", [])
                if isinstance(triggers, str):
                    triggers = [triggers]
                workflows.append(
                    WorkflowInfo(
                        name=frontmatter.get("name", path.stem),
                        description=frontmatter.get("description", ""),
                        triggers=triggers,
                        path=path,
                    )
                )
        except Exception:
            # Skip files that can't be read
            continue

    return sorted(workflows, key=lambda w: w.name)


def add_workflow(name: str) -> Path:
    """Create a new workflow file from template.

    Args:
        name: Workflow name (lowercase identifier)

    Returns:
        Path to the created file

    Raises:
        FileExistsError: If workflow file already exists (code: WORKFLOW_EXISTS)
    """
    workflows_dir = get_workflows_dir()
    workflow_path = workflows_dir / f"{name}.md"

    if workflow_path.exists():
        raise FileExistsError(f"Workflow file already exists: {workflow_path}")

    # Create directory if needed
    workflows_dir.mkdir(parents=True, exist_ok=True)

    # Write template
    content = WORKFLOW_TEMPLATE.format(name=name)
    workflow_path.write_text(content)

    return workflow_path
