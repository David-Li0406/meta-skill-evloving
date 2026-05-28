#!/usr/bin/env python3
"""
Scaffold a new data model with all layers (schema, entity, shared, orpc).

Usage:
    python scaffold.py <EntityName> <domain> [--dry-run]

Example:
    python scaffold.py Campaign marketing
    python scaffold.py BlogPost content --dry-run
"""

import argparse
import re
import sys
from pathlib import Path

# Paths relative to repo root
REPO_ROOT = Path(__file__).parent.parent.parent.parent.parent
TEMPLATES_DIR = Path(__file__).parent.parent / "templates"

TARGETS = {
    "schema": "packages/foundation/schemas/src/{entity_kebab}.sql.ts",
    "entity": "packages/core/src/domain/{domain}/entity/Ent{entity_pascal}.ts",
    "shared": "packages/shared/src/{domain}/{entity_kebab}.ts",
    "orpc": "packages/dash/worker/src/orpc/routes/{entity_kebab}.ts",
}


def to_camel(name: str) -> str:
    """PascalCase -> camelCase"""
    return name[0].lower() + name[1:] if name else name


def to_snake(name: str) -> str:
    """PascalCase -> snake_case"""
    return re.sub(r"(?<!^)(?=[A-Z])", "_", name).lower()


def to_kebab(name: str) -> str:
    """PascalCase -> kebab-case"""
    return re.sub(r"(?<!^)(?=[A-Z])", "-", name).lower()


def pluralize(name: str) -> str:
    """Simple pluralization"""
    if name.endswith("y"):
        return name[:-1] + "ies"
    if name.endswith(("s", "x", "z", "ch", "sh")):
        return name + "es"
    return name + "s"


def replace_placeholders(content: str, entity: str, domain: str) -> str:
    """Replace all template placeholders."""
    entities_pascal = pluralize(entity)
    entities_camel = to_camel(entities_pascal)

    replacements = {
        "{{EntityName}}": entity,
        "{{entityName}}": to_camel(entity),
        "{{entity_name}}": to_snake(entity),
        "{{entity-name}}": to_kebab(entity),
        "{{entities}}": entities_camel,
        "{{Entities}}": entities_pascal,
        "{{domain}}": domain,
    }

    for placeholder, value in replacements.items():
        content = content.replace(placeholder, value)

    return content


def update_entity_index(domain: str, entity: str, dry_run: bool) -> None:
    """Update or create packages/core/src/domain/{domain}/entity/index.ts"""
    index_path = REPO_ROOT / f"packages/core/src/domain/{domain}/entity/index.ts"
    export_line = f'export {{ Ent{entity} }} from "./Ent{entity}";\n'

    if index_path.exists():
        content = index_path.read_text()
        if f"Ent{entity}" in content:
            print(f"  [skip] Entity index already has Ent{entity}")
            return
        content += export_line
    else:
        content = export_line

    if dry_run:
        print(f"  [DRY RUN] Would update: packages/core/src/domain/{domain}/entity/index.ts")
    else:
        index_path.parent.mkdir(parents=True, exist_ok=True)
        index_path.write_text(content)
        print(f"  Updated: packages/core/src/domain/{domain}/entity/index.ts")


def update_domain_index(domain: str, dry_run: bool) -> None:
    """Update or create packages/core/src/domain/{domain}/index.ts"""
    index_path = REPO_ROOT / f"packages/core/src/domain/{domain}/index.ts"
    export_line = 'export * from "./entity";\n'

    if index_path.exists():
        content = index_path.read_text()
        if 'from "./entity"' in content:
            print(f"  [skip] Domain index already exports entity")
            return
        content += export_line
    else:
        content = export_line

    if dry_run:
        print(f"  [DRY RUN] Would update: packages/core/src/domain/{domain}/index.ts")
    else:
        index_path.parent.mkdir(parents=True, exist_ok=True)
        index_path.write_text(content)
        print(f"  Updated: packages/core/src/domain/{domain}/index.ts")


def update_shared_index(domain: str, entity_kebab: str, dry_run: bool) -> None:
    """Update packages/shared/src/index.ts"""
    index_path = REPO_ROOT / "packages/shared/src/index.ts"
    export_line = f'export * from "./{domain}/{entity_kebab}";\n'

    if not index_path.exists():
        print(f"  [error] Shared index not found: {index_path}")
        return

    content = index_path.read_text()
    if f'"./{domain}/{entity_kebab}"' in content:
        print(f"  [skip] Shared index already exports {domain}/{entity_kebab}")
        return

    content += export_line

    if dry_run:
        print(f"  [DRY RUN] Would update: packages/shared/src/index.ts")
    else:
        index_path.write_text(content)
        print(f"  Updated: packages/shared/src/index.ts")


def update_orpc_index(entity: str, entity_kebab: str, dry_run: bool) -> None:
    """Update packages/dash/worker/src/orpc/index.ts"""
    index_path = REPO_ROOT / "packages/dash/worker/src/orpc/index.ts"
    entity_camel = to_camel(entity)

    if not index_path.exists():
        print(f"  [error] oRPC index not found: {index_path}")
        return

    content = index_path.read_text()

    # Check if already added
    if f'"{entity_camel}Router"' in content or f'from "./routes/{entity_kebab}"' in content:
        print(f"  [skip] oRPC index already has {entity_camel}Router")
        return

    # 1. Add type export after last type export block
    type_export = f'''export type {{
  {entity}RouterInputs,
  {entity}RouterOutputs,
}} from "./routes/{entity_kebab}";
export {{ {entity_camel}Router }} from "./routes/{entity_kebab}";
'''

    # Find position to insert type exports (before the imports section)
    import_match = re.search(r'\nimport \{ getPostHogClient', content)
    if import_match:
        insert_pos = import_match.start()
        content = content[:insert_pos] + type_export + content[insert_pos:]
    else:
        print(f"  [warn] Could not find import section in oRPC index")

    # 2. Add import line before `export const orpcRouter`
    import_line = f'import {{ {entity_camel}Router as {entity_camel} }} from "./routes/{entity_kebab}";\n'
    router_match = re.search(r'\nexport const orpcRouter', content)
    if router_match:
        insert_pos = router_match.start()
        content = content[:insert_pos] + "\n" + import_line + content[insert_pos:]
    else:
        print(f"  [warn] Could not find orpcRouter in oRPC index")

    # 3. Add to router object (before closing brace)
    router_entry = f"    {entity_camel},\n"
    # Find the .router({ block and add before the closing });
    router_block_match = re.search(r'\.router\(\{([^}]+)\}\)', content, re.DOTALL)
    if router_block_match:
        # Insert before the last item or closing brace
        block_end = router_block_match.end() - 2  # Position before })
        content = content[:block_end] + router_entry + "  " + content[block_end:]
    else:
        print(f"  [warn] Could not find .router({{ block in oRPC index")

    if dry_run:
        print(f"  [DRY RUN] Would update: packages/dash/worker/src/orpc/index.ts")
    else:
        index_path.write_text(content)
        print(f"  Updated: packages/dash/worker/src/orpc/index.ts")


def scaffold(entity: str, domain: str, dry_run: bool = False) -> list[tuple[str, str]]:
    """
    Generate all files for a new entity.

    Returns list of (path, content) tuples.
    """
    results = []
    entity_kebab = to_kebab(entity)

    # Generate main files from templates
    print("\n[1/2] Generating files from templates...")
    for template_name, target_pattern in TARGETS.items():
        template_file = f"{template_name}.sql.ts.tmpl" if template_name == "schema" else f"{template_name}.ts.tmpl"
        template_path = TEMPLATES_DIR / template_file

        if not template_path.exists():
            print(f"  [warn] Template not found: {template_path}")
            continue

        # Read template
        content = template_path.read_text()

        # Replace placeholders in content
        content = replace_placeholders(content, entity, domain)

        # Build target path
        target_rel = target_pattern.format(
            entity_pascal=entity,
            entity_camel=to_camel(entity),
            entity_kebab=entity_kebab,
            domain=domain,
        )
        target_path = REPO_ROOT / target_rel

        results.append((str(target_path), content))

        if dry_run:
            print(f"  [DRY RUN] Would create: {target_rel}")
        else:
            # Create parent directories
            target_path.parent.mkdir(parents=True, exist_ok=True)
            target_path.write_text(content)
            print(f"  Created: {target_rel}")

    # Update index files
    print("\n[2/2] Updating index files...")
    update_entity_index(domain, entity, dry_run)
    update_domain_index(domain, dry_run)
    update_shared_index(domain, entity_kebab, dry_run)
    update_orpc_index(entity, entity_kebab, dry_run)

    return results


def print_next_steps(entity: str, domain: str):
    """Print manual steps needed after scaffolding."""
    entity_kebab = to_kebab(entity)

    print("\n" + "=" * 60)
    print("NEXT STEPS:")
    print("=" * 60)
    print(f"""
1. Add custom fields to schema:
   packages/foundation/schemas/src/{entity_kebab}.sql.ts

2. Generate migration:
   cd packages/foundation/schemas && pnpm db generate

3. Run lint:
   pnpm lint
""")


def main():
    parser = argparse.ArgumentParser(
        description="Scaffold a new data model with all layers"
    )
    parser.add_argument(
        "entity",
        help="Entity name in PascalCase (e.g., Campaign, BlogPost)"
    )
    parser.add_argument(
        "domain",
        help="Domain grouping (e.g., marketing, content, radar)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be created without writing files"
    )

    args = parser.parse_args()

    # Validate entity name is PascalCase
    if not args.entity[0].isupper():
        print(f"Error: Entity name must be PascalCase (e.g., Campaign, not {args.entity})", file=sys.stderr)
        sys.exit(1)

    print(f"Scaffolding entity: {args.entity} in domain: {args.domain}")
    print("-" * 40)

    scaffold(args.entity, args.domain, args.dry_run)

    if not args.dry_run:
        print_next_steps(args.entity, args.domain)


if __name__ == "__main__":
    main()
