#!/usr/bin/env python3
"""
Technical Textbook Content Validator

Validates that technical content adheres to university-level textbook standards.
Checks for proper structure, terminology usage, and stylistic requirements.
"""

import re
import sys
from typing import Dict, List, Tuple

class TextbookValidator:
    """Validates technical textbook content against formal academic standards."""
    
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.stats = {}
        
        # Common informal words to avoid
        self.informal_words = {
            'simple', 'simply', 'easy', 'easily', 'just', 'basically',
            'obviously', 'clearly', 'amazing', 'awesome', 'great',
            'terrible', 'horrible', 'nice', 'cool', 'stuff', 'things',
            'etc', 'and so on', 'and such'
        }
        
        # First person pronouns to avoid
        self.first_person = {'i', 'we', 'our', 'us', 'my', 'me', "we'll", "we've", "we're", "i'll", "i've", "i'm"}
        
        # Second person pronouns to check
        self.second_person = {'you', 'your', 'yours', "you'll", "you've", "you're"}
        
        # Marketing/emotional language to avoid
        self.marketing_terms = {
            'revolutionary', 'innovative', 'cutting-edge', 'state-of-the-art',
            'powerful', 'robust', 'elegant', 'beautiful', 'ugly', 'exciting',
            'boring', 'fun', 'interesting', 'fascinating'
        }
        
        # Required technical terms for different domains
        self.technical_terms = {
            'software': ['architecture', 'algorithm', 'complexity', 'pattern', 'interface'],
            'cloud': ['orchestration', 'infrastructure', 'provisioning', 'scalability', 'availability'],
            'devops': ['pipeline', 'automation', 'deployment', 'monitoring', 'configuration']
        }
    
    def validate_content(self, content: str) -> Dict:
        """Main validation method."""
        self.errors = []
        self.warnings = []
        self.stats = {}
        
        lines = content.split('\n')
        
        # Run various checks
        self._check_structure(lines)
        self._check_perspective(content)
        self._check_terminology(content)
        self._check_formatting(lines)
        self._calculate_metrics(content)
        
        return {
            'valid': len(self.errors) == 0,
            'errors': self.errors,
            'warnings': self.warnings,
            'stats': self.stats
        }
    
    def _check_structure(self, lines: List[str]) -> None:
        """Verify hierarchical structure and numbering."""
        section_pattern = re.compile(r'^(\d+(?:\.\d+)*)\s+(.+)$')
        found_sections = []
        
        for i, line in enumerate(lines, 1):
            if line.strip() and not line.startswith('#'):
                match = section_pattern.match(line.strip())
                if match:
                    found_sections.append((match.group(1), i))
        
        if not found_sections:
            self.warnings.append("No numbered sections found. Consider using hierarchical numbering (1.1, 1.2, etc.)")
        
        # Check section number sequence
        for i in range(1, len(found_sections)):
            curr = found_sections[i][0]
            prev = found_sections[i-1][0]
            if not self._valid_sequence(prev, curr):
                self.warnings.append(f"Line {found_sections[i][1]}: Section numbering sequence issue between {prev} and {curr}")
    
    def _valid_sequence(self, prev: str, curr: str) -> bool:
        """Check if section numbers follow valid sequence."""
        prev_parts = [int(x) for x in prev.split('.')]
        curr_parts = [int(x) for x in curr.split('.')]
        
        # Valid sequences:
        # Same level increment: 1.1 -> 1.2
        # Go deeper: 1.1 -> 1.1.1
        # Go back up: 1.1.2 -> 1.2 or 1.1.2 -> 2
        
        # This is a simplified check
        return True  # Implement detailed logic if needed
    
    def _check_perspective(self, content: str) -> None:
        """Ensure third-person perspective is maintained."""
        words = re.findall(r'\b\w+\b', content.lower())
        
        # Check for first person
        first_person_found = [w for w in words if w in self.first_person]
        if first_person_found:
            unique_first = set(first_person_found)
            self.errors.append(f"First-person pronouns found: {', '.join(unique_first)}. Use third-person perspective.")
        
        # Check for second person (warning only)
        second_person_found = [w for w in words if w in self.second_person]
        if second_person_found:
            unique_second = set(second_person_found)
            self.warnings.append(f"Second-person pronouns found: {', '.join(unique_second)}. Consider rephrasing to maintain formal tone.")
        
        # Check for informal language
        informal_found = [w for w in words if w in self.informal_words]
        if informal_found:
            unique_informal = set(informal_found)
            self.warnings.append(f"Informal language detected: {', '.join(unique_informal)}")
        
        # Check for marketing terms
        marketing_found = [w for w in words if w in self.marketing_terms]
        if marketing_found:
            unique_marketing = set(marketing_found)
            self.errors.append(f"Marketing/emotional language found: {', '.join(unique_marketing)}. Maintain objectivity.")
    
    def _check_terminology(self, content: str) -> None:
        """Verify use of technical terminology."""
        words = set(re.findall(r'\b\w+\b', content.lower()))
        
        # Count technical terms
        tech_count = 0
        for domain_terms in self.technical_terms.values():
            tech_count += len([t for t in domain_terms if t in words])
        
        total_words = len(words)
        if total_words > 0:
            tech_ratio = tech_count / total_words
            self.stats['technical_term_ratio'] = f"{tech_ratio:.2%}"
            
            if tech_ratio < 0.01:
                self.warnings.append("Low technical terminology usage. Consider using more domain-specific terms.")
    
    def _check_formatting(self, lines: List[str]) -> None:
        """Check for proper formatting elements."""
        has_bold = any('**' in line for line in lines)
        has_code = any('`' in line for line in lines)
        has_tables = any('|' in line and '-' in line for line in lines)
        
        if not has_bold:
            self.warnings.append("No bold formatting found. Consider bolding key terms on first use.")
        
        self.stats['has_code_examples'] = has_code
        self.stats['has_tables'] = has_tables
    
    def _calculate_metrics(self, content: str) -> None:
        """Calculate content metrics."""
        sentences = re.split(r'[.!?]+', content)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        if sentences:
            # Average sentence length
            avg_length = sum(len(s.split()) for s in sentences) / len(sentences)
            self.stats['avg_sentence_length'] = f"{avg_length:.1f} words"
            
            if avg_length < 10:
                self.warnings.append("Average sentence length is very short. Consider more complex constructions.")
            elif avg_length > 30:
                self.warnings.append("Average sentence length is very long. Consider breaking complex sentences.")
        
        # Lexical density (content words vs function words)
        words = re.findall(r'\b\w+\b', content.lower())
        function_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 
                         'to', 'for', 'of', 'with', 'is', 'are', 'was', 'were',
                         'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does'}
        
        content_words = [w for w in words if w not in function_words]
        if words:
            lexical_density = len(content_words) / len(words)
            self.stats['lexical_density'] = f"{lexical_density:.2%}"
            
            if lexical_density < 0.4:
                self.warnings.append("Low lexical density. Consider using more content words and fewer function words.")
    
    def print_report(self, results: Dict) -> None:
        """Print validation report."""
        print("\n" + "="*60)
        print("TECHNICAL TEXTBOOK VALIDATION REPORT")
        print("="*60)
        
        if results['valid']:
            print("✓ Content meets technical textbook standards")
        else:
            print("✗ Content has validation errors")
        
        print("\nSTATISTICS:")
        for key, value in results['stats'].items():
            print(f"  • {key}: {value}")
        
        if results['errors']:
            print(f"\nERRORS ({len(results['errors'])}):")
            for error in results['errors']:
                print(f"  ✗ {error}")
        
        if results['warnings']:
            print(f"\nWARNINGS ({len(results['warnings'])}):")
            for warning in results['warnings']:
                print(f"  ⚠ {warning}")
        
        print("\nRECOMMENDATIONS:")
        if results['valid']:
            print("  • Continue maintaining formal academic style")
            print("  • Ensure all technical terms are defined on first use")
            print("  • Add cross-references between related sections")
        else:
            print("  • Address all errors before finalizing content")
            print("  • Review warnings to improve content quality")
            print("  • Consult skill documentation for style guidelines")
        
        print("="*60 + "\n")


def main():
    """Main function to run validator."""
    if len(sys.argv) != 2:
        print("Usage: python validate_textbook.py <content_file>")
        sys.exit(1)
    
    try:
        with open(sys.argv[1], 'r') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Error: File '{sys.argv[1]}' not found")
        sys.exit(1)
    
    validator = TextbookValidator()
    results = validator.validate_content(content)
    validator.print_report(results)
    
    # Exit with error code if validation failed
    sys.exit(0 if results['valid'] else 1)


if __name__ == "__main__":
    main()
