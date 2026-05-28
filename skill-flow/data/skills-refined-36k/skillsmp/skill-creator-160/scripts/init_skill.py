#!/usr/bin/env python3
"""
SEMO Skill Initializer - Creates a new skill from template

Usage:
    init_skill.py <skill-name> --path <path>

Examples:
    init_skill.py health-check --path semo-next/skills
    init_skill.py epic-master --path semo-po/skills
"""

import sys
from pathlib import Path

SKILL_TEMPLATE = """---
name: {skill_name}
description: |
  [TODO: 역할 설명]. Use when:
  (1) [조건1], (2) [조건2], (3) [조건3].
---

# {skill_title}

> [TODO: 1줄 핵심 설명]

## Quick Start

```bash
# [TODO: 사용 예시]
```

## Process

[TODO: 간략한 프로세스 설명]

## SEMO Message

```markdown
[SEMO] Skill: {skill_name} 실행 - {{context}}
```

## References

- [Workflow](references/workflow.md) (필요 시 생성)

## Related

- [TODO: 관련 Agent/Skill 링크]
"""

EXAMPLE_WORKFLOW = """# Workflow

> {skill_title} 상세 워크플로우

## Phase 1: [Phase Name]

### Step 1.1: [Step Name]

[TODO: 상세 설명]

### Step 1.2: [Step Name]

[TODO: 상세 설명]

## Phase 2: [Phase Name]

[TODO: 추가 Phase]
"""


def title_case_skill_name(skill_name):
    """Convert hyphenated skill name to Title Case."""
    return ' '.join(word.capitalize() for word in skill_name.split('-'))


def init_skill(skill_name, path):
    """Initialize a new SEMO skill directory."""
    skill_dir = Path(path).resolve() / skill_name

    if skill_dir.exists():
        print(f"❌ Error: Skill directory already exists: {skill_dir}")
        return None

    try:
        skill_dir.mkdir(parents=True, exist_ok=False)
        print(f"✅ Created skill directory: {skill_dir}")
    except Exception as e:
        print(f"❌ Error creating directory: {e}")
        return None

    # Create SKILL.md
    skill_title = title_case_skill_name(skill_name)
    skill_content = SKILL_TEMPLATE.format(
        skill_name=skill_name,
        skill_title=skill_title
    )

    skill_md_path = skill_dir / 'SKILL.md'
    try:
        skill_md_path.write_text(skill_content)
        print("✅ Created SKILL.md")
    except Exception as e:
        print(f"❌ Error creating SKILL.md: {e}")
        return None

    # Create references/ directory with example
    try:
        references_dir = skill_dir / 'references'
        references_dir.mkdir(exist_ok=True)

        example_workflow = references_dir / 'workflow.md'
        example_workflow.write_text(EXAMPLE_WORKFLOW.format(skill_title=skill_title))
        print("✅ Created references/workflow.md")
    except Exception as e:
        print(f"❌ Error creating references: {e}")
        return None

    print(f"\n✅ Skill '{skill_name}' initialized at {skill_dir}")
    print("\nNext steps:")
    print("1. Edit SKILL.md - complete TODO items")
    print("2. Customize references/workflow.md or delete if not needed")
    print("3. Run quick_validate.py to verify structure")
    print("4. Connect to Agent if needed")

    return skill_dir


def main():
    if len(sys.argv) < 4 or sys.argv[2] != '--path':
        print("Usage: init_skill.py <skill-name> --path <path>")
        print("\nSkill name requirements:")
        print("  - hyphen-case (e.g., 'health-check')")
        print("  - lowercase letters, digits, hyphens only")
        print("  - max 64 characters")
        print("\nExamples:")
        print("  init_skill.py health-check --path semo-next/skills")
        print("  init_skill.py epic-master --path semo-po/skills")
        sys.exit(1)

    skill_name = sys.argv[1]
    path = sys.argv[3]

    print(f"🚀 Initializing SEMO skill: {skill_name}")
    print(f"   Location: {path}")
    print()

    result = init_skill(skill_name, path)
    sys.exit(0 if result else 1)


if __name__ == "__main__":
    main()
