#!/usr/bin/env python3
"""
Validate commit messages against Conventional Commits specification.

Usage:
    python validate_commit_msg.py "feat(auth): add OAuth login"
    python validate_commit_msg.py --file .git/COMMIT_EDITMSG
    echo "feat: add feature" | python validate_commit_msg.py --stdin
"""

import re
import sys
import argparse
from typing import Tuple, List, Optional


class CommitMessageValidator:
    """Validates commit messages against Conventional Commits spec."""

    VALID_TYPES = [
        'feat', 'fix', 'docs', 'style', 'refactor',
        'test', 'chore', 'perf', 'ci', 'build', 'revert'
    ]

    SUBJECT_MAX_LENGTH = 50
    BODY_LINE_MAX_LENGTH = 72

    # Regex for conventional commit format
    PATTERN = re.compile(
        r'^(?P<type>\w+)'  # type
        r'(?:\((?P<scope>[\w-]+)\))?'  # optional scope
        r'(?P<breaking>!)?'  # optional breaking change indicator
        r': '  # colon-space separator
        r'(?P<subject>.+)$'  # subject
    )

    def __init__(self, strict: bool = True):
        """
        Initialize validator.

        Args:
            strict: If True, enforce all rules strictly
        """
        self.strict = strict
        self.errors: List[str] = []
        self.warnings: List[str] = []

    def validate(self, message: str) -> Tuple[bool, List[str], List[str]]:
        """
        Validate a commit message.

        Args:
            message: The commit message to validate

        Returns:
            Tuple of (is_valid, errors, warnings)
        """
        self.errors = []
        self.warnings = []

        if not message or not message.strip():
            self.errors.append("Commit message is empty")
            return False, self.errors, self.warnings

        lines = message.split('\n')
        header = lines[0].strip()
        body_lines = lines[2:] if len(lines) > 2 else []  # Skip blank line

        # Validate header
        self._validate_header(header)

        # Validate body if present
        if body_lines:
            self._validate_body(body_lines)

        is_valid = len(self.errors) == 0
        return is_valid, self.errors, self.warnings

    def _validate_header(self, header: str) -> None:
        """Validate the commit message header."""
        match = self.PATTERN.match(header)

        if not match:
            self.errors.append(
                f"Header does not match Conventional Commits format: '{header}'\n"
                f"Expected: <type>(<scope>): <subject>\n"
                f"Example: feat(auth): add OAuth login"
            )
            return

        commit_type = match.group('type')
        scope = match.group('scope')
        breaking = match.group('breaking')
        subject = match.group('subject')

        # Validate type
        if commit_type not in self.VALID_TYPES:
            self.errors.append(
                f"Invalid commit type: '{commit_type}'\n"
                f"Valid types: {', '.join(self.VALID_TYPES)}"
            )

        # Validate subject
        if len(subject) > self.SUBJECT_MAX_LENGTH:
            if self.strict:
                self.errors.append(
                    f"Subject exceeds {self.SUBJECT_MAX_LENGTH} characters: "
                    f"{len(subject)} chars"
                )
            else:
                self.warnings.append(
                    f"Subject should be ≤{self.SUBJECT_MAX_LENGTH} characters: "
                    f"{len(subject)} chars"
                )

        # Check subject ends with period
        if subject.endswith('.'):
            self.warnings.append("Subject should not end with a period")

        # Check subject starts with lowercase (should be lowercase for imperative)
        if subject and subject[0].isupper():
            first_word = subject.split()[0] if subject.split() else subject
            # Allow uppercase if it's an acronym or proper noun
            if not first_word.isupper() and len(first_word) > 1:
                self.warnings.append(
                    "Subject should start with lowercase (imperative mood)\n"
                    f"Example: 'add' not 'Add', 'fix' not 'Fix'"
                )

        # Check for past tense (common mistake)
        past_tense_words = ['added', 'fixed', 'updated', 'changed', 'removed']
        first_word = subject.split()[0].lower() if subject.split() else ''
        if first_word in past_tense_words:
            self.warnings.append(
                f"Subject appears to use past tense: '{first_word}'\n"
                f"Use imperative mood: '{first_word[:-1] if first_word.endswith('ed') else first_word}'"
            )

    def _validate_body(self, body_lines: List[str]) -> None:
        """Validate the commit message body."""
        for i, line in enumerate(body_lines, start=3):
            if len(line) > self.BODY_LINE_MAX_LENGTH:
                if self.strict:
                    self.errors.append(
                        f"Line {i} exceeds {self.BODY_LINE_MAX_LENGTH} characters: "
                        f"{len(line)} chars"
                    )
                else:
                    self.warnings.append(
                        f"Line {i} should wrap at {self.BODY_LINE_MAX_LENGTH} characters: "
                        f"{len(line)} chars"
                    )


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Validate commit messages against Conventional Commits spec'
    )
    parser.add_argument(
        'message',
        nargs='?',
        help='Commit message to validate'
    )
    parser.add_argument(
        '--file',
        help='Read commit message from file (e.g., .git/COMMIT_EDITMSG)'
    )
    parser.add_argument(
        '--stdin',
        action='store_true',
        help='Read commit message from stdin'
    )
    parser.add_argument(
        '--strict',
        action='store_true',
        default=True,
        help='Strict validation mode (default: True)'
    )
    parser.add_argument(
        '--no-strict',
        dest='strict',
        action='store_false',
        help='Non-strict validation mode (warnings only)'
    )

    args = parser.parse_args()

    # Get commit message
    message: Optional[str] = None
    if args.file:
        try:
            with open(args.file, 'r') as f:
                message = f.read()
        except FileNotFoundError:
            print(f"Error: File not found: {args.file}", file=sys.stderr)
            sys.exit(1)
    elif args.stdin:
        message = sys.stdin.read()
    elif args.message:
        message = args.message
    else:
        parser.print_help()
        sys.exit(1)

    # Validate
    validator = CommitMessageValidator(strict=args.strict)
    is_valid, errors, warnings = validator.validate(message)

    # Print results
    if errors:
        print("❌ Validation failed:\n")
        for error in errors:
            print(f"  ERROR: {error}\n")

    if warnings:
        print("⚠️  Warnings:\n")
        for warning in warnings:
            print(f"  WARNING: {warning}\n")

    if is_valid and not warnings:
        print("✅ Commit message is valid")
        sys.exit(0)
    elif is_valid and warnings:
        print("✅ Commit message is valid (with warnings)")
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == '__main__':
    main()
