#!/usr/bin/env python3
"""
Scaffold frontend CRUD pages for an entity.

Usage:
    python scaffold.py <EntityName> [--dry-run]

Example:
    python scaffold.py Campaign
    python scaffold.py BlogPost --dry-run

Prerequisites:
    - oRPC routes must exist (run data_model scaffold first)
"""

import argparse
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent.parent.parent.parent
TEMPLATES_DIR = Path(__file__).parent.parent / "templates"

TARGETS = {
    "queries": "packages/dash/ui/src/queries/{entity_kebab}.ts",
    "route": "packages/dash/ui/src/routes/_authenticated/workspaces/$workspaceSlug/{entity_kebab}.tsx",
    "page": "packages/dash/ui/src/components/{entity_kebab}/{EntityName}Page.tsx",
    "table": "packages/dash/ui/src/components/{entity_kebab}/{EntityName}Table.tsx",
    "create-dialog": "packages/dash/ui/src/components/{entity_kebab}/{EntityName}CreateDialog.tsx",
}


def to_camel(name: str) -> str:
    """PascalCase -> camelCase"""
    return name[0].lower() + name[1:] if name else name


def to_kebab(name: str) -> str:
    """PascalCase -> kebab-case"""
    return re.sub(r"(?<!^)(?=[A-Z])", "-", name).lower()


def to_upper_snake(name: str) -> str:
    """PascalCase -> UPPER_SNAKE_CASE"""
    return re.sub(r"(?<!^)(?=[A-Z])", "_", name).upper()


def pluralize(name: str) -> str:
    """Simple pluralization"""
    if name.endswith("y"):
        return name[:-1] + "ies"
    if name.endswith(("s", "x", "z", "ch", "sh")):
        return name + "es"
    return name + "s"


def replace_placeholders(content: str, entity: str) -> str:
    """Replace all template placeholders."""
    entities_pascal = pluralize(entity)
    entities_camel = to_camel(entities_pascal)

    replacements = {
        "{{EntityName}}": entity,
        "{{entityName}}": to_camel(entity),
        "{{entityKebab}}": to_kebab(entity),
        "{{entities}}": entities_camel,
        "{{Entities}}": entities_pascal,
        "{{ENTITY_UPPER}}": to_upper_snake(entity),
    }

    for placeholder, value in replacements.items():
        content = content.replace(placeholder, value)

    return content


def scaffold(entity: str, dry_run: bool = False) -> list[tuple[str, str]]:
    """Generate all frontend files for an entity."""
    results = []
    entity_kebab = to_kebab(entity)

    print(f"\n[1/1] Generating frontend files...")

    for template_name, target_pattern in TARGETS.items():
        template_path = TEMPLATES_DIR / f"{template_name}.tsx.tmpl"
        if template_name == "queries":
            template_path = TEMPLATES_DIR / "queries.ts.tmpl"

        if not template_path.exists():
            print(f"  [warn] Template not found: {template_path}")
            continue

        content = template_path.read_text()
        content = replace_placeholders(content, entity)

        target_rel = target_pattern.format(
            EntityName=entity,
            entity_kebab=entity_kebab,
        )
        target_path = REPO_ROOT / target_rel

        results.append((str(target_path), content))

        if dry_run:
            print(f"  [DRY RUN] Would create: {target_rel}")
        else:
            target_path.parent.mkdir(parents=True, exist_ok=True)
            target_path.write_text(content)
            print(f"  Created: {target_rel}")

    return results


def print_next_steps(entity: str):
    """Print manual steps needed after scaffolding."""
    entity_kebab = to_kebab(entity)

    print("\n" + "=" * 60)
    print("NEXT STEPS:")
    print("=" * 60)
    print(f"""
1. Add route to sidebar (if needed):
   packages/dash/ui/src/components/app-sidebar.tsx

2. Customize table columns:
   packages/dash/ui/src/components/{entity_kebab}/{entity}Table.tsx

3. Add form fields to create dialog:
   packages/dash/ui/src/components/{entity_kebab}/{entity}CreateDialog.tsx

4. Run lint:
   pnpm lint
""")


def main():
    parser = argparse.ArgumentParser(
        description="Scaffold frontend CRUD pages for an entity"
    )
    parser.add_argument(
        "entity",
        help="Entity name in PascalCase (e.g., Campaign, BlogPost)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be created without writing files"
    )

    args = parser.parse_args()

    if not args.entity[0].isupper():
        print(f"Error: Entity name must be PascalCase (e.g., Campaign)", file=sys.stderr)
        sys.exit(1)

    print(f"Scaffolding frontend for: {args.entity}")
    print("-" * 40)

    scaffold(args.entity, args.dry_run)

    if not args.dry_run:
        print_next_steps(args.entity)


if __name__ == "__main__":
    main()
