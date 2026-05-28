#!/usr/bin/env python3
"""
Generate commit messages from git diff output.

This script analyzes staged changes and generates a Conventional Commits
formatted message.

Usage:
    python generate_commit_msg.py
    python generate_commit_msg.py --no-body
    python generate_commit_msg.py --include-claude-footer
"""

import subprocess
import sys
import argparse
import re
from typing import List, Tuple, Optional, Set
from collections import Counter


class CommitMessageGenerator:
    """Generates commit messages from git diff."""

    TYPE_KEYWORDS = {
        'feat': ['add', 'implement', 'create', 'new'],
        'fix': ['fix', 'resolve', 'correct', 'patch', 'repair'],
        'docs': ['document', 'readme', 'comment'],
        'test': ['test', 'spec'],
        'refactor': ['refactor', 'restructure', 'reorganize', 'extract'],
        'style': ['format', 'style', 'prettier', 'eslint', 'lint'],
        'perf': ['optimize', 'performance', 'speed', 'cache'],
        'chore': ['update', 'upgrade', 'dependency', 'deps', 'package'],
        'ci': ['ci', 'github', 'workflow', 'action'],
        'build': ['build', 'webpack', 'rollup', 'vite'],
    }

    def __init__(self):
        """Initialize generator."""
        self.files_changed: List[str] = []
        self.additions: int = 0
        self.deletions: int = 0
        self.diff_content: str = ""

    def get_staged_changes(self) -> bool:
        """
        Get staged changes from git.

        Returns:
            True if there are staged changes, False otherwise
        """
        try:
            # Get diff stats
            result = subprocess.run(
                ['git', 'diff', '--cached', '--stat'],
                capture_output=True,
                text=True,
                check=True
            )
            if not result.stdout.strip():
                print("No staged changes found. Use 'git add' first.", file=sys.stderr)
                return False

            # Get file names
            result = subprocess.run(
                ['git', 'diff', '--cached', '--name-only'],
                capture_output=True,
                text=True,
                check=True
            )
            self.files_changed = result.stdout.strip().split('\n')

            # Get full diff
            result = subprocess.run(
                ['git', 'diff', '--cached'],
                capture_output=True,
                text=True,
                check=True
            )
            self.diff_content = result.stdout

            # Get numstat
            result = subprocess.run(
                ['git', 'diff', '--cached', '--numstat'],
                capture_output=True,
                text=True,
                check=True
            )
            for line in result.stdout.strip().split('\n'):
                parts = line.split('\t')
                if len(parts) >= 2:
                    try:
                        self.additions += int(parts[0]) if parts[0] != '-' else 0
                        self.deletions += int(parts[1]) if parts[1] != '-' else 0
                    except ValueError:
                        pass

            return True

        except subprocess.CalledProcessError as e:
            print(f"Git error: {e}", file=sys.stderr)
            return False
        except FileNotFoundError:
            print("Git not found. Is git installed?", file=sys.stderr)
            return False

    def determine_type(self) -> str:
        """
        Determine commit type from changes.

        Returns:
            Commit type (feat, fix, docs, etc.)
        """
        # Check file patterns first
        file_patterns = {
            'docs': [r'README', r'\.md$', r'docs/', r'documentation/'],
            'test': [r'\.test\.', r'\.spec\.', r'test/', r'tests/', r'__tests__/'],
            'ci': [r'\.github/workflows/', r'\.gitlab-ci', r'\.travis', r'Jenkinsfile'],
            'build': [r'package\.json', r'package-lock\.json', r'yarn\.lock',
                     r'webpack\.', r'vite\.', r'rollup\.'],
            'style': [r'\.css$', r'\.scss$', r'\.less$'],
        }

        for commit_type, patterns in file_patterns.items():
            for pattern in patterns:
                for file in self.files_changed:
                    if re.search(pattern, file):
                        return commit_type

        # Check diff content for keywords
        diff_lower = self.diff_content.lower()
        type_scores: Counter = Counter()

        for commit_type, keywords in self.TYPE_KEYWORDS.items():
            for keyword in keywords:
                # Count occurrences in added lines
                count = len(re.findall(r'^\+.*\b' + keyword + r'\b', diff_lower, re.MULTILINE))
                type_scores[commit_type] += count

        # Check if mostly deletions (might be refactor or chore)
        if self.deletions > self.additions * 2:
            type_scores['refactor'] += 2

        # Default to feat for new files, fix for modifications
        new_files = [f for f in self.files_changed if self._is_new_file(f)]
        if new_files and not type_scores:
            return 'feat'

        if type_scores:
            return type_scores.most_common(1)[0][0]

        # Default to chore
        return 'chore'

    def _is_new_file(self, file_path: str) -> bool:
        """Check if file is new (not in git history)."""
        try:
            result = subprocess.run(
                ['git', 'log', '--oneline', '--', file_path],
                capture_output=True,
                text=True,
                check=True
            )
            return not result.stdout.strip()
        except subprocess.CalledProcessError:
            return True

    def determine_scope(self) -> Optional[str]:
        """
        Determine scope from file paths.

        Returns:
            Scope string or None
        """
        # Extract common directory
        paths = [f for f in self.files_changed if '/' in f]
        if not paths:
            return None

        # Get first-level directories
        dirs: Set[str] = set()
        for path in paths:
            parts = path.split('/')
            if len(parts) > 1:
                # Skip common dirs like src, lib
                if parts[0] in ['src', 'lib']:
                    if len(parts) > 2:
                        dirs.add(parts[1])
                else:
                    dirs.add(parts[0])

        # If single directory, use as scope
        if len(dirs) == 1:
            scope = list(dirs)[0]
            # Clean up scope
            scope = re.sub(r'[^a-z0-9-]', '', scope.lower())
            return scope if scope else None

        # If multiple dirs but similar, extract common prefix
        if len(dirs) <= 3:
            # Find common prefix
            sorted_dirs = sorted(dirs)
            prefix = sorted_dirs[0]
            for d in sorted_dirs[1:]:
                while not d.startswith(prefix) and prefix:
                    prefix = prefix[:-1]
            if len(prefix) >= 3:
                return prefix.lower()

        return None

    def generate_subject(self, commit_type: str, scope: Optional[str]) -> str:
        """
        Generate commit subject line.

        Args:
            commit_type: The commit type
            scope: The scope (optional)

        Returns:
            Subject line
        """
        # Analyze changes to create subject
        new_files = [f for f in self.files_changed if self._is_new_file(f)]
        modified_files = [f for f in self.files_changed if not self._is_new_file(f)]

        # Generate action verb
        if commit_type == 'feat':
            verb = 'add'
        elif commit_type == 'fix':
            verb = 'fix'
        elif commit_type == 'docs':
            verb = 'update' if modified_files else 'add'
        elif commit_type == 'test':
            verb = 'add' if new_files else 'update'
        elif commit_type == 'refactor':
            verb = 'refactor'
        elif commit_type == 'style':
            verb = 'format'
        elif commit_type == 'perf':
            verb = 'optimize'
        elif commit_type == 'chore':
            verb = 'update'
        else:
            verb = 'update'

        # Generate description
        if len(self.files_changed) == 1:
            file_name = self.files_changed[0].split('/')[-1]
            file_base = file_name.split('.')[0]
            description = file_base.replace('_', ' ').replace('-', ' ')
        elif scope:
            description = f"{scope} module"
        else:
            description = f"{len(self.files_changed)} files"

        subject = f"{verb} {description}"

        # Truncate if too long
        max_len = 50 - len(commit_type) - (len(scope) + 3 if scope else 2)
        if len(subject) > max_len:
            subject = subject[:max_len - 3] + '...'

        return subject

    def generate_body(self) -> Optional[str]:
        """
        Generate commit body with details.

        Returns:
            Body text or None
        """
        lines = []

        # Add file summary if many files
        if len(self.files_changed) > 3:
            lines.append(f"Changes across {len(self.files_changed)} files:")
            for file in self.files_changed[:5]:
                lines.append(f"- {file}")
            if len(self.files_changed) > 5:
                lines.append(f"- ... and {len(self.files_changed) - 5} more")

        # Add stats
        if self.additions or self.deletions:
            lines.append("")
            lines.append(f"Stats: +{self.additions} -{self.deletions}")

        return '\n'.join(lines) if lines else None

    def generate(self, include_body: bool = True, include_claude_footer: bool = False) -> str:
        """
        Generate complete commit message.

        Args:
            include_body: Whether to include body
            include_claude_footer: Whether to include Claude Code attribution

        Returns:
            Complete commit message
        """
        commit_type = self.determine_type()
        scope = self.determine_scope()
        subject = self.generate_subject(commit_type, scope)

        # Build header
        if scope:
            header = f"{commit_type}({scope}): {subject}"
        else:
            header = f"{commit_type}: {subject}"

        # Build message
        message_parts = [header]

        # Add body
        if include_body:
            body = self.generate_body()
            if body:
                message_parts.append("")
                message_parts.append(body)

        # Add Claude footer
        if include_claude_footer:
            message_parts.append("")
            message_parts.append("🤖 Generated with [Claude Code](https://claude.com/claude-code)")
            message_parts.append("")
            message_parts.append("Co-Authored-By: Claude <noreply@anthropic.com>")

        return '\n'.join(message_parts)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Generate commit messages from staged changes'
    )
    parser.add_argument(
        '--no-body',
        action='store_true',
        help='Generate header only (no body)'
    )
    parser.add_argument(
        '--include-claude-footer',
        action='store_true',
        help='Include Claude Code attribution footer'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show generated message without committing'
    )

    args = parser.parse_args()

    # Generate message
    generator = CommitMessageGenerator()

    if not generator.get_staged_changes():
        sys.exit(1)

    message = generator.generate(
        include_body=not args.no_body,
        include_claude_footer=args.include_claude_footer
    )

    # Output
    print("Generated commit message:")
    print("=" * 60)
    print(message)
    print("=" * 60)

    if not args.dry_run:
        print("\nUse this message? (y/n): ", end='')
        response = input().strip().lower()
        if response == 'y':
            try:
                subprocess.run(
                    ['git', 'commit', '-m', message],
                    check=True
                )
                print("✅ Commit created successfully")
            except subprocess.CalledProcessError as e:
                print(f"❌ Commit failed: {e}", file=sys.stderr)
                sys.exit(1)


if __name__ == '__main__':
    main()
