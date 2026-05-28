#!/usr/bin/env python3
"""
Skill Auto-Fix Script
Automatically fixes common issues in Claude Code skills
"""

import argparse
import re
import shutil
from datetime import datetime
from pathlib import Path
from typing import List, Tuple, Dict

class SkillAutoFixer:
    def __init__(self, skill_path: str, mode: str = 'safe', dry_run: bool = False):
        self.skill_path = Path(skill_path)
        self.skill_md = self.skill_path / 'SKILL.md'
        self.mode = mode  # 'safe' or 'interactive'
        self.dry_run = dry_run
        self.changes = []
        self.content = ""
        self.yaml_content = ""
        self.markdown_content = ""

        if not self.skill_md.exists():
            raise FileNotFoundError(f"SKILL.md not found at {self.skill_md}")

    def run(self):
        """Main execution"""
        print(f"🔧 Skill Auto-Fix - {self.mode} mode {'(DRY RUN)' if self.dry_run else ''}")
        print(f"📁 Skill: {self.skill_path.name}\n")

        # Read skill
        self.read_skill()

        # Run fixes based on mode
        if self.mode == 'safe':
            self.run_safe_fixes()
        elif self.mode == 'interactive':
            self.run_interactive_fixes()

        # Report and write
        self.report()
        if not self.dry_run and self.changes:
            self.backup()
            self.write_skill()
            print(f"\n✅ {len(self.changes)} fixes applied")
        elif self.dry_run:
            print(f"\n🔍 DRY RUN: {len(self.changes)} fixes would be applied")
        else:
            print("\n✨ No issues found")

    def read_skill(self):
        """Read and parse SKILL.md"""
        self.content = self.skill_md.read_text(encoding='utf-8')

        # Split YAML and markdown
        parts = self.content.split('---', 2)
        if len(parts) >= 3:
            self.yaml_content = parts[1]
            self.markdown_content = parts[2]
        else:
            self.markdown_content = self.content

    def write_skill(self):
        """Write updated SKILL.md"""
        if self.yaml_content:
            new_content = f"---{self.yaml_content}---{self.markdown_content}"
        else:
            new_content = self.markdown_content

        self.skill_md.write_text(new_content, encoding='utf-8')

    def backup(self):
        """Create timestamped backup"""
        timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
        backup_path = self.skill_md.with_suffix(f'.md.backup-{timestamp}')
        shutil.copy2(self.skill_md, backup_path)
        print(f"💾 Backup: {backup_path.name}")

    def report(self):
        """Print changes summary"""
        if not self.changes:
            return

        print("📝 Changes:")
        for i, change in enumerate(self.changes, 1):
            print(f"  {i}. {change}")

    # === SAFE FIXES ===

    def run_safe_fixes(self):
        """Run all safe auto-fixes"""
        self.fix_windows_paths()
        self.add_missing_yaml_fields()
        self.check_trigger_count()
        self.generate_toc_if_needed()

    def fix_windows_paths(self):
        """Convert Windows backslashes to forward slashes"""
        # Pattern: C:\path\to\file or \path\to\file
        pattern = r'([C-Z]:\\[\w\\]+|\\[\w\\]+)'

        def replace_backslash(match):
            return match.group(0).replace('\\', '/')

        original = self.markdown_content
        self.markdown_content = re.sub(pattern, replace_backslash, self.markdown_content)

        if self.markdown_content != original:
            count = original.count('\\') - self.markdown_content.count('\\')
            self.changes.append(f"Converted {count} Windows paths (\\ → /)")

    def add_missing_yaml_fields(self):
        """Add version and license if missing"""
        if not self.yaml_content:
            return

        added = []

        # Check for version
        if 'version:' not in self.yaml_content:
            self.yaml_content += '\nversion: "1.0.0"'
            added.append('version: "1.0.0"')

        # Check for license
        if 'license:' not in self.yaml_content:
            self.yaml_content += '\nlicense: Apache-2.0'
            added.append('license: Apache-2.0')

        if added:
            self.changes.append(f"Added missing YAML fields: {', '.join(added)}")

    def check_trigger_count(self):
        """Warn if triggers < 5"""
        if not self.yaml_content:
            return

        # Count triggers
        trigger_match = re.search(r'triggers:\s*(.*?)(?=\n\w+:|$)', self.yaml_content, re.DOTALL)
        if trigger_match:
            triggers = [line.strip() for line in trigger_match.group(1).split('\n') if line.strip().startswith('-')]
            trigger_count = len(triggers)

            if trigger_count < 5:
                self.changes.append(f"⚠️ WARNING: Only {trigger_count} triggers (recommend 10-20)")
        else:
            self.changes.append("⚠️ WARNING: No triggers field found in YAML")

    def generate_toc_if_needed(self):
        """Generate TOC for files > 100 lines"""
        lines = self.markdown_content.split('\n')
        if len(lines) <= 100:
            return

        # Check if TOC already exists
        if '## Table of Contents' in self.markdown_content or '# Table of Contents' in self.markdown_content:
            return

        # Extract headings
        headings = []
        for line in lines:
            match = re.match(r'^(#{2,})\s+(.+)$', line)
            if match:
                level = len(match.group(1)) - 1  # h2 = level 1
                title = match.group(2).strip()
                anchor = title.lower().replace(' ', '-').replace('(', '').replace(')', '')
                headings.append((level, title, anchor))

        if len(headings) < 3:
            return  # Not worth a TOC

        # Generate TOC
        toc_lines = ['\n## Table of Contents\n']
        for level, title, anchor in headings:
            indent = '  ' * (level - 1)
            toc_lines.append(f"{indent}- [{title}](#{anchor})")

        toc = '\n'.join(toc_lines) + '\n'

        # Insert after first heading
        first_heading = re.search(r'^#\s+.+$', self.markdown_content, re.MULTILINE)
        if first_heading:
            pos = first_heading.end()
            self.markdown_content = self.markdown_content[:pos] + toc + self.markdown_content[pos:]
            self.changes.append(f"Generated TOC ({len(headings)} sections)")

    # === INTERACTIVE FIXES ===

    def run_interactive_fixes(self):
        """Run interactive fixes (require approval)"""
        # Run safe fixes first
        self.run_safe_fixes()

        # Interactive fixes
        self.detect_credentials()
        self.suggest_file_splits()
        self.validate_description()

    def detect_credentials(self):
        """Detect hardcoded secrets"""
        patterns = {
            'password': r'password\s*=\s*["\']([^"\']+)["\']',
            'api_key': r'api[_-]?key\s*=\s*["\']([^"\']+)["\']',
            'token': r'token\s*=\s*["\']([^"\']+)["\']',
            'secret': r'secret\s*=\s*["\']([^"\']+)["\']',
        }

        found_secrets = []
        for secret_type, pattern in patterns.items():
            matches = re.findall(pattern, self.markdown_content, re.IGNORECASE)
            if matches:
                found_secrets.append((secret_type, len(matches)))

        if found_secrets:
            summary = ', '.join([f"{count} {stype}" for stype, count in found_secrets])
            self.changes.append(f"⚠️ CREDENTIALS DETECTED: {summary} - suggest using .env")

    def suggest_file_splits(self):
        """Suggest splitting if > 500 lines"""
        line_count = len(self.markdown_content.split('\n'))

        if line_count > 500:
            # Find major sections
            sections = []
            for match in re.finditer(r'^##\s+(.+)$', self.markdown_content, re.MULTILINE):
                sections.append(match.group(1))

            if len(sections) > 3:
                self.changes.append(
                    f"⚠️ FILE TOO LONG: {line_count} lines (max 500). "
                    f"Suggest moving {len(sections)} sections to references/"
                )

    def validate_description(self):
        """Check if description has 'what' and 'when'"""
        if not self.yaml_content:
            return

        desc_match = re.search(r'description:\s*[>|]?\s*(.+?)(?=\n\w+:|$)', self.yaml_content, re.DOTALL)
        if not desc_match:
            self.changes.append("⚠️ WARNING: No description found")
            return

        description = desc_match.group(1).strip()

        # Check for action verbs (the "what")
        action_verbs = ['processes', 'generates', 'creates', 'analyzes', 'executes',
                       'manages', 'deploys', 'validates', 'extracts', 'converts']
        has_what = any(verb in description.lower() for verb in action_verbs)

        # Check for "when" keywords
        when_keywords = ['use when', 'when', 'for', 'if you need', 'to help']
        has_when = any(keyword in description.lower() for keyword in when_keywords)

        if not has_what or not has_when:
            missing = []
            if not has_what:
                missing.append("'what' (action verb)")
            if not has_when:
                missing.append("'when' (use case)")

            self.changes.append(f"⚠️ DESCRIPTION QUALITY: Missing {', '.join(missing)}")


def main():
    parser = argparse.ArgumentParser(description='Auto-fix common skill issues')
    parser.add_argument('skill_path', help='Path to skill directory')
    parser.add_argument('--mode', choices=['safe', 'interactive'], default='safe',
                       help='Fix mode: safe (auto) or interactive (approve each)')
    parser.add_argument('--dry-run', action='store_true',
                       help='Preview changes without applying')

    args = parser.parse_args()

    try:
        fixer = SkillAutoFixer(args.skill_path, args.mode, args.dry_run)
        fixer.run()
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1

    return 0


if __name__ == '__main__':
    exit(main())
