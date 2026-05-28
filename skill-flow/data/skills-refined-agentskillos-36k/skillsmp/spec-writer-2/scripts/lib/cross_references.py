"""
Cross-reference validation utilities.
"""

import re
from pathlib import Path
from typing import Dict, Set, List
from dataclasses import dataclass


@dataclass
class ValidationError:
    """Validation error details."""
    severity: str  # 'ERROR' or 'WARN'
    message: str
    file: str = None
    line_num: int = None


class CrossReferenceValidator:
    """Validate cross-references across spec files."""

    # Reference patterns
    PATTERNS = {
        'decision': r'\bD(\d+)\b',
        'research': r'\bR(\d+)\b',
        'question': r'\bQ(\d+)\b',
        'story': r'\bStory (\d+)\b',
        'functional_requirement': r'\bFR-(\d+)\b',
        'edge_case': r'\bEC-(\d+)\b',
        'success_criteria': r'\bSC-(\d+)\b',
        'revision': r'\bREV-(\d+)\b'
    }

    def __init__(self, discovery_dir: Path):
        """
        Initialize validator.

        Args:
            discovery_dir: Path to discovery/ directory
        """
        self.discovery_dir = Path(discovery_dir)

    def find_references(self, text: str) -> Dict[str, List[str]]:
        """
        Find all cross-references in text.

        Args:
            text: Text to search

        Returns:
            Dict of entity_type -> list of IDs found

        Example:
            "See D1, D3 and Q5" -> {
                'decision': ['D1', 'D3'],
                'question': ['Q5']
            }
        """
        references = {}

        for entity_type, pattern in self.PATTERNS.items():
            matches = re.findall(pattern, text)
            if matches:
                # Build full IDs
                if entity_type == 'decision':
                    ids = [f'D{m}' for m in matches]
                elif entity_type == 'research':
                    ids = [f'R{m}' for m in matches]
                elif entity_type == 'question':
                    ids = [f'Q{m}' for m in matches]
                elif entity_type == 'story':
                    ids = [m for m in matches]  # Just the number
                elif entity_type == 'functional_requirement':
                    ids = [f'FR-{m}' for m in matches]
                elif entity_type == 'edge_case':
                    ids = [f'EC-{m}' for m in matches]
                elif entity_type == 'success_criteria':
                    ids = [f'SC-{m}' for m in matches]
                elif entity_type == 'revision':
                    ids = [f'REV-{m}' for m in matches]

                references[entity_type] = list(set(ids))  # Deduplicate

        return references

    def get_reference_targets(self) -> Dict[str, Set[str]]:
        """
        Get all valid reference targets from spec files.

        Returns:
            Dict of entity_type -> set of valid IDs

        Example:
            {
                'decision': {'D1', 'D2', 'D3'},
                'question': {'Q1', 'Q2'},
                ...
            }
        """
        targets = {
            'decision': set(),
            'research': set(),
            'question': set(),
            'story': set(),
            'functional_requirement': set(),
            'edge_case': set(),
            'success_criteria': set(),
            'revision': set()
        }

        # Scan DECISIONS.md for D#
        decisions_file = self.discovery_dir / 'archive' / 'DECISIONS.md'
        if decisions_file.exists():
            content = decisions_file.read_text(encoding='utf-8')
            matches = re.findall(r'^## (D\d+):', content, re.MULTILINE)
            targets['decision'].update(matches)

        # Scan RESEARCH.md for R#
        research_file = self.discovery_dir / 'archive' / 'RESEARCH.md'
        if research_file.exists():
            content = research_file.read_text(encoding='utf-8')
            matches = re.findall(r'^## (R\d+):', content, re.MULTILINE)
            targets['research'].update(matches)

        # Scan OPEN_QUESTIONS.md for Q# (active questions)
        questions_file = self.discovery_dir / 'OPEN_QUESTIONS.md'
        if questions_file.exists():
            content = questions_file.read_text(encoding='utf-8')
            matches = re.findall(r'\*\*(Q\d+)\*\*:', content)
            targets['question'].update(matches)

        # Scan DECISIONS.md and RESEARCH.md for resolved questions
        # (Questions can be referenced even after resolution)
        for file in [decisions_file, research_file]:
            if file.exists():
                content = file.read_text(encoding='utf-8')
                matches = re.findall(r'\b(Q\d+)\b', content)
                targets['question'].update(matches)

        # Scan STATE.md for story numbers
        state_file = self.discovery_dir / 'STATE.md'
        if state_file.exists():
            content = state_file.read_text(encoding='utf-8')
            matches = re.findall(r'^\| (\d+) \|', content, re.MULTILINE)
            targets['story'].update(matches)

        # Scan SPEC.md for story numbers and requirements/edge cases/success criteria
        spec_file = self.discovery_dir / 'SPEC.md'
        if spec_file.exists():
            content = spec_file.read_text(encoding='utf-8')

            # Stories
            matches = re.findall(r'^### (?:🔄 )?User Story (\d+)', content, re.MULTILINE)
            targets['story'].update(matches)

            # Functional requirements
            matches = re.findall(r'^\| (FR-\d+) \|', content, re.MULTILINE)
            targets['functional_requirement'].update(matches)

            # Edge cases
            matches = re.findall(r'^\| (EC-\d+) \|', content, re.MULTILINE)
            targets['edge_case'].update(matches)

            # Success criteria
            matches = re.findall(r'^\| (SC-\d+) \|', content, re.MULTILINE)
            targets['success_criteria'].update(matches)

        # Scan REVISIONS.md for REV-#
        revisions_file = self.discovery_dir / 'archive' / 'REVISIONS.md'
        if revisions_file.exists():
            content = revisions_file.read_text(encoding='utf-8')
            matches = re.findall(r'^## (REV-\d+):', content, re.MULTILINE)
            targets['revision'].update(matches)

        return targets

    def validate_references(self) -> List[ValidationError]:
        """
        Validate all cross-references in spec files.

        Returns:
            List of validation errors
        """
        errors = []

        # Get valid targets
        targets = self.get_reference_targets()

        # Files to check
        files_to_check = [
            self.discovery_dir / 'SPEC.md',
            self.discovery_dir / 'STATE.md',
            self.discovery_dir / 'archive' / 'DECISIONS.md',
            self.discovery_dir / 'archive' / 'RESEARCH.md',
            self.discovery_dir / 'archive' / 'REVISIONS.md'
        ]

        for file_path in files_to_check:
            if not file_path.exists():
                continue

            content = file_path.read_text(encoding='utf-8')
            references = self.find_references(content)

            # Validate each reference
            for entity_type, ref_ids in references.items():
                valid_ids = targets[entity_type]

                for ref_id in ref_ids:
                    # For stories, compare just the number
                    if entity_type == 'story':
                        if ref_id not in valid_ids:
                            errors.append(ValidationError(
                                severity='ERROR',
                                message=f"Story {ref_id} referenced but not found in STATE.md or SPEC.md",
                                file=str(file_path.relative_to(self.discovery_dir))
                            ))
                    else:
                        if ref_id not in valid_ids:
                            errors.append(ValidationError(
                                severity='ERROR',
                                message=f"{ref_id} referenced but not found in appropriate file",
                                file=str(file_path.relative_to(self.discovery_dir))
                            ))

        return errors

    def extract_cross_refs_from_story(self, story_content: str) -> Set[str]:
        """
        Extract all cross-references from a story section.

        Args:
            story_content: Story content text

        Returns:
            Set of all reference IDs (D1, R2, Q3, etc.)
        """
        all_refs = set()
        references = self.find_references(story_content)

        for entity_type, ref_ids in references.items():
            all_refs.update(ref_ids)

        return all_refs
