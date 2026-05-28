#!/usr/bin/env python3
"""
Article Validation Script

Validates Japanese technical articles against forbidden patterns and style requirements
defined in the style guide.

Usage:
    python validate_article.py <article-path>

Example:
    python validate_article.py ../outputs/20260110-typescript-tips.md
"""

import argparse
import re
import sys
from pathlib import Path
from typing import List, Tuple


class ArticleValidator:
    """Validates articles against style guide requirements."""

    def __init__(self, article_path: Path):
        self.article_path = article_path
        self.content = article_path.read_text(encoding='utf-8')
        self.errors: List[str] = []
        self.warnings: List[str] = []
        
    def validate(self) -> bool:
        """Run all validation checks. Returns True if no critical errors found."""
        print(f"Validating: {self.article_path}")
        print("=" * 60)
        
        self._check_frontmatter()
        self._check_forbidden_patterns()
        self._check_polite_form_distribution()
        self._check_section_count()
        
        self._print_results()
        
        return len(self.errors) == 0
    
    def _check_frontmatter(self):
        """Check for valid frontmatter."""
        required_fields = ['title', 'emoji', 'type', 'topics', 'published']
        
        if not self.content.startswith('---'):
            self.errors.append("Missing frontmatter (must start with ---)")
            return
        
        frontmatter_match = re.search(r'^---\n(.*?)\n---', self.content, re.DOTALL)
        if not frontmatter_match:
            self.errors.append("Invalid frontmatter format")
            return
        
        frontmatter = frontmatter_match.group(1)
        for field in required_fields:
            if not re.search(rf'^{field}:', frontmatter, re.MULTILINE):
                self.errors.append(f"Missing required frontmatter field: {field}")
    
    def _check_forbidden_patterns(self):
        """Check for forbidden writing patterns."""
        # Remove code blocks to avoid false positives
        content_no_code = re.sub(r'```.*?```', '', self.content, flags=re.DOTALL)
        
        # Pattern 1: Sentence-ending contracted forms
        contracted_patterns = [
            (r'てる。', 'てる。'),
            (r'てた。', 'てた。'),
            (r'てます。', 'てます。'),
            (r'てない。', 'てない。'),
            (r'てなかった。', 'てなかった。'),
        ]
        
        for pattern, display in contracted_patterns:
            matches = re.finditer(pattern, content_no_code)
            for match in matches:
                line_num = self.content[:match.start()].count('\n') + 1
                self.errors.append(
                    f"FORBIDDEN PATTERN #1 at line {line_num}: "
                    f"Sentence-ending contracted form '{display}'"
                )
        
        # Pattern 2: Paragraph-initial "で、"
        lines = content_no_code.split('\n')
        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            if stripped.startswith('で、'):
                self.errors.append(
                    f"FORBIDDEN PATTERN #2 at line {i}: "
                    f"Paragraph-initial 'で、'"
                )
        
        # Pattern 3: Colons before code/lists
        colon_before_code = re.finditer(r'：\s*\n\s*```', content_no_code)
        for match in colon_before_code:
            line_num = self.content[:match.start()].count('\n') + 1
            self.errors.append(
                f"FORBIDDEN PATTERN #3 at line {line_num}: "
                f"Colon (：) before code block"
            )
        
        colon_before_list = re.finditer(r'：\s*\n\s*-', content_no_code)
        for match in colon_before_list:
            line_num = self.content[:match.start()].count('\n') + 1
            self.errors.append(
                f"FORBIDDEN PATTERN #3 at line {line_num}: "
                f"Colon (：) before list"
            )
    
    def _check_polite_form_distribution(self):
        """Check polite form (です/ます) distribution."""
        # Remove code blocks and frontmatter
        content_no_code = re.sub(r'```.*?```', '', self.content, flags=re.DOTALL)
        content_no_code = re.sub(r'^---\n.*?\n---\n', '', content_no_code, flags=re.DOTALL)
        
        # Count sentences (rough approximation using 。)
        sentences = [s.strip() for s in content_no_code.split('。') if s.strip()]
        total_sentences = len(sentences)
        
        if total_sentences == 0:
            self.warnings.append("No sentences found for polite form analysis")
            return
        
        # Count です/ます endings
        polite_count = 0
        polite_patterns = [r'です$', r'ます$', r'ません$', r'でした$', r'ました$', r'ませんでした$']
        
        for sentence in sentences:
            for pattern in polite_patterns:
                if re.search(pattern, sentence):
                    polite_count += 1
                    break
        
        percentage = (polite_count / total_sentences) * 100 if total_sentences > 0 else 0
        
        print(f"\nPolite Form Distribution:")
        print(f"  Total sentences: {total_sentences}")
        print(f"  Polite endings (です/ます): {polite_count}")
        print(f"  Distribution: {percentage:.1f}%")
        
        if polite_count < 15:
            self.errors.append(
                f"PUBLICATION BLOCKER: Too few polite form endings "
                f"({polite_count} found, minimum 15 required)"
            )
        elif percentage < 40:
            self.warnings.append(
                f"Low polite form distribution ({percentage:.1f}%). "
                f"Target: 45-60% for optimal quality"
            )
        elif percentage < 45:
            self.warnings.append(
                f"Acceptable polite form distribution ({percentage:.1f}%). "
                f"Target: 45-60% for top-tier quality (9.0+)"
            )
        elif percentage > 60:
            self.warnings.append(
                f"High polite form distribution ({percentage:.1f}%). "
                f"Target: 45-60% for natural tone"
            )
    
    def _check_section_count(self):
        """Check H2 section count (max 6-7 recommended)."""
        h2_sections = re.findall(r'^## ', self.content, re.MULTILINE)
        section_count = len(h2_sections)
        
        print(f"\nSection Structure:")
        print(f"  H2 sections: {section_count}")
        
        if section_count >= 8:
            self.warnings.append(
                f"Too many H2 sections ({section_count}). "
                f"Target: 6-7 max for natural flow (8+ feels encyclopedic)"
            )
    
    def _print_results(self):
        """Print validation results."""
        print("\n" + "=" * 60)
        print("VALIDATION RESULTS")
        print("=" * 60)
        
        if self.errors:
            print(f"\n❌ CRITICAL ERRORS ({len(self.errors)}):")
            for error in self.errors:
                print(f"  - {error}")
        
        if self.warnings:
            print(f"\n⚠️  WARNINGS ({len(self.warnings)}):")
            for warning in self.warnings:
                print(f"  - {warning}")
        
        if not self.errors and not self.warnings:
            print("\n✅ ALL CHECKS PASSED")
        elif not self.errors:
            print("\n✅ No critical errors (warnings only)")
        else:
            print("\n❌ VALIDATION FAILED")
        
        print("=" * 60)


def main():
    parser = argparse.ArgumentParser(
        description="Validate Japanese technical articles against style guide"
    )
    parser.add_argument(
        'article_path',
        type=Path,
        help="Path to the article markdown file"
    )
    
    args = parser.parse_args()
    
    if not args.article_path.exists():
        print(f"Error: File not found: {args.article_path}", file=sys.stderr)
        sys.exit(1)
    
    validator = ArticleValidator(args.article_path)
    success = validator.validate()
    
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
