#!/usr/bin/env python3
"""
Article Validation Script (Polished Tone)

Validates Japanese technical articles against polished tone requirements,
forbidden patterns, and professional standards.

Usage:
    python validate_article.py <article-path>

Example:
    python validate_article.py ../outputs/20260110-typescript-guide.md
"""

import argparse
import re
import sys
from pathlib import Path
from typing import List


class PolishedArticleValidator:
    """Validates articles against polished tone style guide requirements."""

    def __init__(self, article_path: Path):
        self.article_path = article_path
        self.content = article_path.read_text(encoding='utf-8')
        self.errors: List[str] = []
        self.warnings: List[str] = []
        
    def validate(self) -> bool:
        """Run all validation checks. Returns True if no critical errors found."""
        print(f"Validating (Polished Tone): {self.article_path}")
        print("=" * 60)
        
        self._check_frontmatter()
        self._check_forbidden_casual_patterns()
        self._check_unprofessional_connectors()
        self._check_ai_isms()
        self._check_colons_in_prose()
        self._check_polite_form_consistency()
        
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
    
    def _check_forbidden_casual_patterns(self):
        """Check for casual/slang sentence endings."""
        # Remove code blocks to avoid false positives
        content_no_code = re.sub(r'```.*?```', '', self.content, flags=re.DOTALL)
        
        casual_patterns = [
            (r'だね。', 'だね。'),
            (r'じゃん。', 'じゃん。'),
            (r'してる。', 'してる。'),
            (r'てる。', 'てる。'),
            (r'ちゃう。', 'ちゃう。'),
            (r'とく。', 'とく。'),
            (r'的な。', '的な。'),
        ]
        
        for pattern, display in casual_patterns:
            matches = re.finditer(pattern, content_no_code)
            for match in matches:
                line_num = self.content[:match.start()].count('\n') + 1
                self.errors.append(
                    f"FORBIDDEN PATTERN #1 at line {line_num}: "
                    f"Casual/slang ending '{display}'"
                )
    
    def _check_unprofessional_connectors(self):
        """Check for unprofessional connectors."""
        content_no_code = re.sub(r'```.*?```', '', self.content, flags=re.DOTALL)
        
        unprofessional = [
            (r'で、', 'で、'),
            (r'なんか、', 'なんか、'),
            (r'ぶっちゃけ', 'ぶっちゃけ'),
        ]
        
        lines = content_no_code.split('\n')
        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            for pattern, display in unprofessional:
                if display in stripped:
                    self.errors.append(
                        f"FORBIDDEN PATTERN #2 at line {i}: "
                        f"Unprofessional connector '{display}'"
                    )
    
    def _check_ai_isms(self):
        """Check for robotic AI patterns."""
        content_no_code = re.sub(r'```.*?```', '', self.content, flags=re.DOTALL)
        
        # Check for consecutive paragraphs starting with また、or さらに、
        paragraphs = [p.strip() for p in content_no_code.split('\n\n') if p.strip()]
        consecutive_mata = 0
        consecutive_sarani = 0
        
        for para in paragraphs:
            if para.startswith('また、'):
                consecutive_mata += 1
                if consecutive_mata >= 2:
                    self.warnings.append(
                        "PATTERN #3: Multiple consecutive paragraphs starting with 'また、' (AI-ism)"
                    )
                    break
            else:
                consecutive_mata = 0
            
            if para.startswith('さらに、'):
                consecutive_sarani += 1
                if consecutive_sarani >= 2:
                    self.warnings.append(
                        "PATTERN #3: Multiple consecutive paragraphs starting with 'さらに、' (AI-ism)"
                    )
                    break
            else:
                consecutive_sarani = 0
        
        # Check for いかがでしたでしょうか
        if 'いかがでしたでしょうか' in content_no_code:
            self.warnings.append(
                "PATTERN #3: Found 'いかがでしたでしょうか' (AI-ism cliché)"
            )
        
        # Check for excessive することができます
        can_do_count = len(re.findall(r'することができます', content_no_code))
        if can_do_count > 5:
            self.warnings.append(
                f"PATTERN #3: Overuse of 'することができます' ({can_do_count} times). "
                f"Consider 'できます' or '可能です'"
            )
    
    def _check_colons_in_prose(self):
        """Check for colons before code/lists."""
        content_no_code_blocks = self.content
        
        # Check colon before code blocks
        colon_before_code = re.finditer(r'：\s*\n\s*```', content_no_code_blocks)
        for match in colon_before_code:
            line_num = self.content[:match.start()].count('\n') + 1
            self.errors.append(
                f"FORBIDDEN PATTERN #4 at line {line_num}: "
                f"Colon (：) before code block"
            )
        
        # Check colon before lists
        colon_before_list = re.finditer(r'：\s*\n\s*-', content_no_code_blocks)
        for match in colon_before_list:
            line_num = self.content[:match.start()].count('\n') + 1
            self.errors.append(
                f"FORBIDDEN PATTERN #4 at line {line_num}: "
                f"Colon (：) before list"
            )
    
    def _check_polite_form_consistency(self):
        """Check polite form (です/ます) consistency."""
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
        
        print(f"\nPolite Form Consistency (Polished Tone):")
        print(f"  Total sentences: {total_sentences}")
        print(f"  Polite endings (です/ます): {polite_count}")
        print(f"  Distribution: {percentage:.1f}%")
        
        # Polished tone expects high consistency (90%+)
        if percentage < 70:
            self.errors.append(
                f"Low polite form consistency ({percentage:.1f}%). "
                f"Polished tone requires consistent です/ます (target: 90%+)"
            )
        elif percentage < 85:
            self.warnings.append(
                f"Moderate polite form consistency ({percentage:.1f}%). "
                f"Target: 90%+ for professional tone"
            )
        elif percentage < 90:
            self.warnings.append(
                f"Good polite form consistency ({percentage:.1f}%). "
                f"Target: 90%+ for optimal professional quality"
            )
    
    def _print_results(self):
        """Print validation results."""
        print("\n" + "=" * 60)
        print("VALIDATION RESULTS (Polished Tone)")
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
            print("\n✅ ALL CHECKS PASSED - Professional quality maintained")
        elif not self.errors:
            print("\n✅ No critical errors (warnings only)")
        else:
            print("\n❌ VALIDATION FAILED - Article needs revision")
        
        print("=" * 60)


def main():
    parser = argparse.ArgumentParser(
        description="Validate Japanese technical articles against polished tone style guide"
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
    
    validator = PolishedArticleValidator(args.article_path)
    success = validator.validate()
    
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
