"""Add missing metadata (frontmatter) to permanent notes.

Logic:
- content in 10_hub -> k/hub
- content in 20_leaf -> k/leaf
- missing summary -> "..."
- missing status -> seed
- missing created -> today (or file stat)
"""

from __future__ import annotations

import argparse
import re
from datetime import datetime
from pathlib import Path

# Regex for frontmatter: starting with ---, ending with ---
FM_PATTERN = re.compile(r"^---\s*\r?\n(.*?)\r?\n---\s*\r?\n", re.DOTALL)

def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")

def get_today() -> str:
    return datetime.now().strftime("%Y-%m-%d")

def fix_frontmatter(content: str, path: Path) -> str | None:
    match = FM_PATTERN.match(content)
    
    lines = []
    
    if match:
        # Existing frontmatter
        fm_body = match.group(1)
        body_content = content[match.end():]
        
        # Parse existing keys (simple regex)
        has_summary = re.search(r"^summary:", fm_body, re.MULTILINE)
        has_status = re.search(r"^status:", fm_body, re.MULTILINE)
        has_created = re.search(r"^created:", fm_body, re.MULTILINE)
        has_tags = re.search(r"^tags:", fm_body, re.MULTILINE)

        new_fm_lines = fm_body.splitlines()

        changes = False

        if not has_summary:
            new_fm_lines.append('summary: "..."')
            changes = True
        
        if not has_status:
            new_fm_lines.append('status: seed')
            changes = True
        
        if not has_created:
            new_fm_lines.append(f'created: {get_today()}')
            changes = True

        # Determine tag based on folder
        folder_tag = "k/leaf"
        if "10_hub" in path.parts:
            folder_tag = "k/hub"
        
        if not has_tags:
            new_fm_lines.append(f'tags: [{folder_tag}, s/seed]')
            changes = True
        else:
            # We won't try to parse and merge list tags with regex heavily, 
            # but if it's missing the kind tag, we might want to warn or append.
            # For now, just leave existing tags alone to avoid breaking complex yaml.
            pass

        if not changes:
            return None

        new_fm = "---\n" + "\n".join(new_fm_lines) + "\n---\n"
        return new_fm + body_content

    else:
        # No frontmatter
        folder_tag = "k/leaf"
        if "10_hub" in path.parts:
            folder_tag = "k/hub"

        fm_lines = [
            "---",
            'summary: "..."',
            f"created: {get_today()}",
            "updated: " + get_today(),
            "status: seed",
            f"tags: [{folder_tag}, s/seed]",
            "related: []",
            "---",
            ""
        ]
        return "\n".join(fm_lines) + content

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--vault-root", default=str(Path.cwd()), help="Vault root directory")
    parser.add_argument(
        "--permanent-folder",
        default="permanent",
        help="Permanent notes folder (relative to vault root)",
    )
    parser.add_argument("--dry-run", action="store_true", help="Preview changes")

    args = parser.parse_args()
    vault_root = Path(args.vault_root).expanduser().resolve()
    permanent_path = (vault_root / args.permanent_folder).resolve()

    if not permanent_path.exists():
        raise SystemExit(f"Permanent folder not found: {permanent_path}")

    files = [p for p in permanent_path.rglob("*.md") if ".obsidian" not in p.parts]

    count = 0
    for f in files:
        if f.name.startswith("Index｜") or f.name.startswith("Str｜"):
             # skip indexes/structures if they are just auto-gen files? 
             # No, user moved them to leaf/hub so they are notes now.
             pass

        original = read_text(f)
        new_content = fix_frontmatter(original, f)
        
        if new_content:
            text_diff = "Update frontmatter"
            if args.dry_run:
                print(f"DRYRUN {text_diff}: {f.relative_to(vault_root)}")
            else:
                f.write_text(new_content, encoding="utf-8")
                print(f"FIXED: {f.relative_to(vault_root)}")
                count += 1
    
    print(f"Updated {count} files.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
