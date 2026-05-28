#!/usr/bin/env python3
"""
Feature File Generator

Generates a new feature specification file from the template.
Creates the necessary folder structure if it doesn't exist.

Usage:
    python generate_feature.py <program>/<module>/<feature-name> [--doc-root path]
    python generate_feature.py kitchen/planning/create-meal-plan
    python generate_feature.py garden/tasks/track-watering --doc-root ./Documentation
"""

import argparse
import re
import sys
from datetime import date
from pathlib import Path


FEATURE_TEMPLATE = '''# {feature_title}

> {description}

**Module:** {program_title} / {module_title}
**Status:** Planned
**Started:** —
**Completed:** —
**GitHub Issue:** #

---

## User Story

**As a** [user type],
**I want** [action or capability],
**So that** [benefit or outcome].

---

## Overview

[Describe the feature in 2-3 paragraphs. Explain what it does, why it's needed, and how it fits into the larger system.]

### Basic Scenario

1. User [initiates the action]
2. System [processes/responds]
3. User [sees the result]

---

## Acceptance Criteria

### Core Functionality

- [ ] [Primary requirement 1]
- [ ] [Primary requirement 2]
- [ ] [Primary requirement 3]

### User Experience

- [ ] [UX requirement 1]
- [ ] [UX requirement 2]

### Edge Cases

- [ ] [Edge case 1]
- [ ] [Edge case 2]

---

## Data Model

_If this feature involves new data structures, define them here. Remove this section if not applicable._

### [Entity Name]

| Field | Type | Description |
|-------|------|-------------|
| id | UUID | Unique identifier |
| [field_name] | [type] | [description] |
| created_at | DateTime | When created |
| updated_at | DateTime | When last modified |

---

## Technical Notes

### Approach

[Describe the implementation approach. What patterns will be used? What are the key components?]

### Dependencies

- [Dependency 1 - what and why]
- [Dependency 2 - what and why]

### Performance Considerations

[Note any performance requirements or concerns]

### Standards Checklist

Before marking this feature complete, verify:

#### Code Quality
- [ ] Tests written first (TDD red-green-refactor)
- [ ] All tests pass
- [ ] 3-tier architecture followed (presentation → logic → data)
- [ ] No reverse imports (data → logic forbidden)
- [ ] Functions/classes follow naming conventions
- [ ] Docstrings on all public APIs

#### Architecture
- [ ] Module boundaries respected
- [ ] No circular dependencies introduced
- [ ] Single index.ts entry point (if new module)
- [ ] Dependencies are explicit

#### Design
- [ ] Design tokens used (no hardcoded values)
- [ ] Semantic HTML used
- [ ] All interactive states implemented (hover, focus, active, disabled)
- [ ] Accessible (keyboard nav, screen reader support)

#### Security
- [ ] Input validation implemented
- [ ] No hardcoded secrets
- [ ] Authorization checks in place
- [ ] Errors don't leak sensitive info

#### Documentation
- [ ] This feature spec is complete
- [ ] Acceptance criteria all checked
- [ ] Open questions resolved
- [ ] Module explainer updated

---

## Open Questions

- [ ] **Open:** [Question that needs to be resolved]

---

## Related Features

- [Related Feature](./related-feature.md)

---

## Revision History

| Date | Author | Change |
|------|--------|--------|
| {today} | | Initial spec |
'''

MODULE_TEMPLATE = '''# {module_title}

> [One-line description of what this module does]

**Program:** {program_title}
**Status:** 0/1 features complete

---

## Overview

[Describe the module's purpose, what problems it solves, and how it fits into the system]

### Purpose

[Why this module exists]

### Scope

**In Scope:**
- [What this module handles]

**Out of Scope:**
- [What this module does NOT handle]

---

## Features

| Feature | Status | Description | Priority |
|---------|--------|-------------|----------|
| [{feature_title}](./{feature_kebab}.md) | ⏳ | [Description] | High |

### Status Legend

| Icon | Status |
|------|--------|
| ⏳ | Planned |
| 🔄 | In Progress |
| ✅ | Complete |
| 🚫 | Blocked |

---

## Dependencies

### This Module Depends On

| Module | What We Use |
|--------|-------------|
| [Module Name](../module/_module.md) | [What we need] |

### Modules That Depend On This

| Module | What They Use |
|--------|---------------|
| — | — |

---

## Architecture

### Key Components

| Component | Responsibility |
|-----------|----------------|
| [Component] | [What it does] |

---

## Open Questions

- [ ] **Open:** [Question]

---

## Related Documentation

- [Architecture](/Documentation/architecture.md)
'''


def kebab_to_title(kebab: str) -> str:
    """Convert kebab-case to Title Case."""
    return " ".join(word.capitalize() for word in kebab.split("-"))


def validate_path(path_str: str) -> tuple[str, str, str]:
    """Validate and parse the program/module/feature path."""
    parts = path_str.strip("/").split("/")

    if len(parts) != 3:
        raise ValueError(
            f"Expected format: program/module/feature-name, got: {path_str}"
        )

    program, module, feature = parts

    # Validate kebab-case
    kebab_pattern = r"^[a-z][a-z0-9]*(-[a-z0-9]+)*$"
    for part, name in [(program, "Program"), (module, "Module"), (feature, "Feature")]:
        if not re.match(kebab_pattern, part):
            raise ValueError(
                f"{name} '{part}' must be kebab-case (lowercase with hyphens)"
            )

    return program, module, feature


def find_doc_root(start_path: Path) -> Path:
    """Find Documentation folder from start path."""
    # Check if start_path IS the Documentation folder
    if start_path.name.lower() == "documentation":
        return start_path

    # Check for Documentation subfolder
    doc_path = start_path / "Documentation"
    if doc_path.exists():
        return doc_path

    # Walk up to find it
    current = start_path
    for _ in range(5):  # Max 5 levels up
        parent = current.parent
        if parent == current:
            break
        doc_path = parent / "Documentation"
        if doc_path.exists():
            return doc_path
        current = parent

    # Default to creating in start_path
    return start_path / "Documentation"


def generate_feature(
    program: str,
    module: str,
    feature: str,
    doc_root: Path,
    description: str = "",
) -> tuple[Path, Path | None]:
    """
    Generate feature file and optionally module explainer.
    Returns (feature_path, module_explainer_path or None if already existed)
    """
    # Create paths
    module_dir = doc_root / "features" / program / module
    feature_path = module_dir / f"{feature}.md"
    explainer_path = module_dir / f"_{module}.md"

    # Create directory structure
    module_dir.mkdir(parents=True, exist_ok=True)

    # Convert names to titles
    program_title = kebab_to_title(program)
    module_title = kebab_to_title(module)
    feature_title = kebab_to_title(feature)

    # Generate feature file
    if feature_path.exists():
        raise FileExistsError(f"Feature file already exists: {feature_path}")

    feature_content = FEATURE_TEMPLATE.format(
        feature_title=feature_title,
        description=description or f"[Description of {feature_title}]",
        program_title=program_title,
        module_title=module_title,
        today=date.today().isoformat(),
    )

    feature_path.write_text(feature_content, encoding="utf-8")

    # Generate module explainer if it doesn't exist
    created_explainer = None
    if not explainer_path.exists():
        module_content = MODULE_TEMPLATE.format(
            module_title=module_title,
            program_title=program_title,
            feature_title=feature_title,
            feature_kebab=feature,
        )
        explainer_path.write_text(module_content, encoding="utf-8")
        created_explainer = explainer_path

    return feature_path, created_explainer


def main():
    parser = argparse.ArgumentParser(
        description="Generate a new feature specification file"
    )
    parser.add_argument(
        "path",
        help="Feature path in format: program/module/feature-name"
    )
    parser.add_argument(
        "--doc-root",
        help="Path to Documentation folder (auto-detected if not specified)"
    )
    parser.add_argument(
        "--description",
        "-d",
        default="",
        help="One-line description for the feature"
    )

    args = parser.parse_args()

    # Validate path format
    try:
        program, module, feature = validate_path(args.path)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    # Find/set documentation root
    if args.doc_root:
        doc_root = Path(args.doc_root)
    else:
        doc_root = find_doc_root(Path.cwd())

    # Generate files
    try:
        feature_path, explainer_path = generate_feature(
            program, module, feature, doc_root, args.description
        )
    except FileExistsError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    # Report success
    print(f"✅ Created feature file: {feature_path}")
    if explainer_path:
        print(f"✅ Created module explainer: {explainer_path}")

    print(f"\n📝 Next steps:")
    print(f"   1. Edit {feature_path.name} to fill in the specification")
    if explainer_path:
        print(f"   2. Edit {explainer_path.name} to describe the module")
    print(f"   3. Update project-roadmap.md if this is a new milestone")


if __name__ == "__main__":
    main()
