#!/usr/bin/env python3
"""
Check for Separation of Concerns violations in Claude Code skills.

Detects:
- Template/asset duplication across skills
- Script functionality overlap
- Reference content duplication
- Domain boundary violations
- Documentation/implementation mismatches
"""

import os
import sys
import json
import argparse
from pathlib import Path
from typing import Dict, List, Set, Optional
import difflib


class SoCValidator:
    """Validates separation of concerns for Claude Code skills."""

    def __init__(self, skill_path: str, skills_base_dir: str = None):
        self.skill_path = Path(skill_path).resolve()

        # Default to ~/.claude/skills if not specified
        if skills_base_dir is None:
            self.skills_base_dir = Path.home() / ".claude" / "skills"
        else:
            self.skills_base_dir = Path(skills_base_dir)

        self.skill_name = self.skill_path.name
        self.violations = []
        self.warnings = []
        self.info = []

    def validate(self) -> Dict:
        """Run all SoC validation checks."""
        result = {
            "skill": self.skill_name,
            "skill_path": str(self.skill_path),
            "violations": [],
            "warnings": [],
            "info": [],
            "score": 5,
            "recommendation": "APPROVE"
        }

        try:
            # 1. Check template duplication
            self._check_template_duplication()

            # 2. Check script duplication
            self._check_script_duplication()

            # 3. Check reference duplication
            self._check_reference_duplication()

            # 4. Check domain overlap
            self._check_domain_overlap()

            # 5. Check documentation vs implementation
            self._check_doc_implementation_match()

            # Compile results
            result["violations"] = self.violations
            result["warnings"] = self.warnings
            result["info"] = self.info

            # Calculate score based on findings
            result["score"] = self._calculate_score()
            result["recommendation"] = self._get_recommendation(result["score"])

        except Exception as e:
            result["error"] = str(e)
            result["score"] = 1
            result["recommendation"] = "ERROR"

        return result

    def _check_template_duplication(self):
        """Check for template files duplicated across skills."""
        templates_dir = self.skill_path / "templates"
        if not templates_dir.exists():
            self.info.append({
                "category": "templates",
                "message": "No templates directory found"
            })
            return

        # Get all template files in this skill
        template_files = list(templates_dir.rglob("*"))
        template_files = [f for f in template_files if f.is_file()]

        if not template_files:
            return

        # Check against other skills
        for other_skill_dir in self.skills_base_dir.iterdir():
            if not other_skill_dir.is_dir() or other_skill_dir == self.skill_path:
                continue

            other_templates = other_skill_dir / "templates"
            if not other_templates.exists():
                continue

            # Compare template files
            for template in template_files:
                template_name = template.name

                # Check for files with same name
                other_template_files = list(other_templates.rglob(template_name))
                if other_template_files:
                    # Found duplicate template name
                    self._check_template_content_similarity(
                        template,
                        other_template_files[0],
                        other_skill_dir.name
                    )

    def _check_template_content_similarity(self, file1: Path, file2: Path, other_skill: str):
        """Check if two template files have similar content."""
        try:
            content1 = file1.read_text()
            content2 = file2.read_text()

            # Calculate similarity ratio
            similarity = difflib.SequenceMatcher(None, content1, content2).ratio()

            if similarity > 0.8:
                self.violations.append({
                    "category": "template_duplication",
                    "severity": "critical",
                    "message": f"Template '{file1.name}' duplicates content from '{other_skill}' skill",
                    "details": {
                        "file": str(file1.relative_to(self.skill_path)),
                        "duplicate_in": other_skill,
                        "similarity": f"{similarity:.1%}"
                    },
                    "suggestion": f"Remove template or delegate to '{other_skill}' skill"
                })
            elif similarity > 0.5:
                self.warnings.append({
                    "category": "template_similarity",
                    "message": f"Template '{file1.name}' has similar content to '{other_skill}' skill",
                    "details": {
                        "file": str(file1.relative_to(self.skill_path)),
                        "similar_to": other_skill,
                        "similarity": f"{similarity:.1%}"
                    },
                    "suggestion": "Review for potential consolidation or delegation"
                })
        except Exception as e:
            # Skip files that can't be read as text
            pass

    def _check_script_duplication(self):
        """Check for scripts with similar functionality."""
        scripts_dir = self.skill_path / "scripts"
        if not scripts_dir.exists():
            return

        script_files = [f for f in scripts_dir.iterdir() if f.is_file() and f.suffix == '.py']

        if not script_files:
            return

        # Check against other skills
        for other_skill_dir in self.skills_base_dir.iterdir():
            if not other_skill_dir.is_dir() or other_skill_dir == self.skill_path:
                continue

            other_scripts = other_skill_dir / "scripts"
            if not other_scripts.exists():
                continue

            for script in script_files:
                # Check for scripts with same or similar names
                for other_script in other_scripts.iterdir():
                    if not other_script.is_file() or other_script.suffix != '.py':
                        continue

                    if script.name == other_script.name:
                        self.violations.append({
                            "category": "script_duplication",
                            "severity": "major",
                            "message": f"Script '{script.name}' exists in '{other_skill_dir.name}' skill",
                            "details": {
                                "file": str(script.relative_to(self.skill_path)),
                                "duplicate_in": other_skill_dir.name
                            },
                            "suggestion": f"Consolidate scripts or justify duplication"
                        })

    def _check_reference_duplication(self):
        """Check for reference content duplication."""
        references_dir = self.skill_path / "references"
        if not references_dir.exists():
            return

        ref_files = [f for f in references_dir.iterdir() if f.is_file()]

        if not ref_files:
            return

        # Check for very generic reference file names that strongly suggest duplication
        # Only flag if the ENTIRE filename is generic (not just containing the word)
        very_generic_names = {
            'template.md', 'example.md', 'guide.md', 'workflow.md',
            'best-practices.md', 'patterns.md', 'structure.md', 'readme.md'
        }

        for ref_file in ref_files:
            ref_name_lower = ref_file.name.lower()

            # Only flag if filename is entirely generic
            if ref_name_lower in very_generic_names:
                self.warnings.append({
                    "category": "reference_naming",
                    "message": f"Reference '{ref_file.name}' has very generic name that might indicate shared domain",
                    "details": {
                        "file": str(ref_file.relative_to(self.skill_path))
                    },
                    "suggestion": "Consider more specific naming or verify content is skill-specific"
                })

    def _check_domain_overlap(self):
        """Check for domain overlap with other skills."""
        skill_md = self.skill_path / "SKILL.md"
        if not skill_md.exists():
            self.violations.append({
                "category": "missing_skill_md",
                "severity": "critical",
                "message": "SKILL.md not found",
                "suggestion": "Create SKILL.md with proper frontmatter"
            })
            return

        try:
            content = skill_md.read_text()

            # Extract description from frontmatter
            description = self._extract_description(content)
            if not description:
                return

            # Get key terms from description
            key_terms = self._extract_key_terms(description)

            # Check other skills for similar terms
            for other_skill_dir in self.skills_base_dir.iterdir():
                if not other_skill_dir.is_dir() or other_skill_dir == self.skill_path:
                    continue

                other_skill_md = other_skill_dir / "SKILL.md"
                if not other_skill_md.exists():
                    continue

                other_content = other_skill_md.read_text()
                other_description = self._extract_description(other_content)

                if not other_description:
                    continue

                # Check for overlapping terms
                other_terms = self._extract_key_terms(other_description)
                overlap = key_terms & other_terms

                if len(overlap) >= 3:  # 3+ overlapping terms suggests domain overlap
                    self.warnings.append({
                        "category": "domain_overlap",
                        "message": f"Potential domain overlap with '{other_skill_dir.name}' skill",
                        "details": {
                            "overlapping_terms": sorted(list(overlap)),
                            "skill": other_skill_dir.name
                        },
                        "suggestion": f"Review skill boundaries and delegation to '{other_skill_dir.name}'"
                    })

        except Exception as e:
            self.info.append({
                "category": "domain_check",
                "message": f"Could not check domain overlap: {str(e)}"
            })

    def _check_doc_implementation_match(self):
        """Check if SKILL.md claims match actual implementation."""
        skill_md = self.skill_path / "SKILL.md"
        if not skill_md.exists():
            return

        try:
            content = skill_md.read_text()
            scripts_dir = self.skill_path / "scripts"

            # Look for script references in SKILL.md
            script_mentions = []
            for line in content.split('\n'):
                if 'scripts/' in line.lower() or '.py' in line:
                    script_mentions.append(line.strip())

            if not script_mentions:
                return

            # Check if mentioned scripts exist
            if scripts_dir.exists():
                existing_scripts = {f.name for f in scripts_dir.iterdir() if f.is_file()}

                for mention in script_mentions:
                    # Extract script names mentioned
                    for script_name in existing_scripts:
                        if script_name not in mention:
                            # Script mentioned but might not exist
                            # This is a simple check - could be enhanced
                            pass
            else:
                if script_mentions:
                    self.violations.append({
                        "category": "doc_implementation_mismatch",
                        "severity": "major",
                        "message": "SKILL.md references scripts/ but directory doesn't exist",
                        "suggestion": "Create scripts/ directory or remove references from SKILL.md"
                    })

        except Exception as e:
            self.info.append({
                "category": "doc_check",
                "message": f"Could not verify doc/implementation match: {str(e)}"
            })

    def _extract_description(self, content: str) -> Optional[str]:
        """Extract description from YAML frontmatter."""
        lines = content.split('\n')
        in_frontmatter = False
        description = None

        for line in lines:
            if line.strip() == '---':
                if not in_frontmatter:
                    in_frontmatter = True
                else:
                    break
            elif in_frontmatter and line.startswith('description:'):
                description = line.replace('description:', '').strip()
                # Handle multi-line descriptions
                continue

        return description

    def _extract_key_terms(self, text: str) -> Set[str]:
        """Extract key terms from description text."""
        # Expanded stop words to filter out common skill description terms
        stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'for', 'with', 'to', 'from',
            'this', 'that', 'these', 'those', 'is', 'are', 'was', 'were',
            'when', 'should', 'be', 'used', 'skill', 'claude', 'code',
            # Common action words in all skills
            'creates', 'create', 'creating', 'created',
            'provides', 'provide', 'providing', 'provided',
            'manages', 'manage', 'managing', 'managed',
            'helps', 'help', 'helping', 'helped',
            'uses', 'use', 'using',
            'triggers', 'trigger', 'requests', 'request',
            # Common qualifiers
            'new', 'existing', 'current', 'updated',
            'when', 'where', 'what', 'how', 'which',
            # Generic terms
            'like', 'such', 'also', 'well', 'make', 'made',
            'file', 'files', 'folder', 'folders',
            'guide', 'workflow', 'process', 'task', 'tasks'
        }

        words = text.lower().split()
        terms = {
            word.strip('.,!?;:()[]{}"\'')
            for word in words
            if len(word) > 4 and word.lower() not in stop_words  # Increased min length to 5
        }

        return terms

    def _calculate_score(self) -> int:
        """Calculate SoC score based on violations and warnings."""
        score = 5

        # Deduct points for violations
        critical_violations = sum(1 for v in self.violations if v.get('severity') == 'critical')
        major_violations = sum(1 for v in self.violations if v.get('severity') == 'major')

        score -= critical_violations * 2
        score -= major_violations * 1
        score -= len(self.warnings) * 0.5

        return max(1, min(5, int(score)))

    def _get_recommendation(self, score: int) -> str:
        """Get recommendation based on score."""
        if score >= 4:
            return "APPROVE"
        elif score >= 3:
            return "NEEDS_MINOR_REVISION"
        else:
            return "NEEDS_MAJOR_REVISION"


def main():
    parser = argparse.ArgumentParser(
        description="Check separation of concerns violations in Claude Code skills"
    )
    parser.add_argument(
        "skill_path",
        help="Path to skill directory to check"
    )
    parser.add_argument(
        "--skills-dir",
        help="Base directory containing all skills (default: ~/.claude/skills)",
        default=None
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output results in JSON format"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show detailed output including info messages"
    )

    args = parser.parse_args()

    # Validate skill path
    skill_path = Path(args.skill_path)
    if not skill_path.exists():
        print(f"Error: Skill path does not exist: {skill_path}", file=sys.stderr)
        sys.exit(1)

    # Run validation
    validator = SoCValidator(args.skill_path, args.skills_dir)
    result = validator.validate()

    # Output results
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        # Human-readable output
        print(f"\n{'='*60}")
        print(f"Separation of Concerns Check: {result['skill']}")
        print(f"{'='*60}\n")

        print(f"Score: {result['score']}/5")
        print(f"Recommendation: {result['recommendation']}\n")

        if result.get('error'):
            print(f"❌ Error: {result['error']}\n")
            sys.exit(1)

        # Show violations
        if result['violations']:
            print(f"🚨 Violations ({len(result['violations'])}):")
            for v in result['violations']:
                severity = v.get('severity', 'unknown').upper()
                print(f"\n  [{severity}] {v['message']}")
                if 'details' in v:
                    for key, value in v['details'].items():
                        print(f"    {key}: {value}")
                if 'suggestion' in v:
                    print(f"    💡 {v['suggestion']}")

        # Show warnings
        if result['warnings']:
            print(f"\n⚠️  Warnings ({len(result['warnings'])}):")
            for w in result['warnings']:
                print(f"\n  {w['message']}")
                if 'details' in w:
                    for key, value in w['details'].items():
                        print(f"    {key}: {value}")
                if 'suggestion' in w:
                    print(f"    💡 {w['suggestion']}")

        # Show info if verbose
        if args.verbose and result['info']:
            print(f"\nℹ️  Info ({len(result['info'])}):")
            for i in result['info']:
                print(f"  • {i['message']}")

        if not result['violations'] and not result['warnings']:
            print("✅ No separation of concerns violations found!\n")

        print()

    # Exit with appropriate code
    if result['score'] < 4:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
