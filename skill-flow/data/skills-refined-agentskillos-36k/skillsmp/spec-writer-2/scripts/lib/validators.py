"""
Structure validation utilities for spec files.
"""

import re
from pathlib import Path
from typing import List
from dataclasses import dataclass

from .cross_references import ValidationError


class StructureValidator:
    """Validate spec file structure and content."""

    # Required sections for each file type
    REQUIRED_SECTIONS = {
        'SPEC.md': [
            '# Feature Specification:',
            '## Problem Statement',
            '## Personas',
            '## User Scenarios & Testing',
            '## Edge Cases',
            '## Requirements',
            '## Success Criteria'
        ],
        'STATE.md': [
            '# Discovery State:',
            '## Problem Understanding',
            '## Story Landscape',
            '## Story Status Overview'
        ],
        'OPEN_QUESTIONS.md': [
            '# Open Questions:',
            '## 🔴 Blocking',
            '## 🟡 Clarifying',
            '## 🔵 Research Pending',
            '## 🟠 Watching'
        ]
    }

    # Valid status values
    VALID_STATUSES = {
        '✅ In SPEC',
        '🔄 In Progress',
        '⏳ Queued',
        '🆕 New'
    }

    def __init__(self, discovery_dir: Path):
        """
        Initialize validator.

        Args:
            discovery_dir: Path to discovery/ directory
        """
        self.discovery_dir = Path(discovery_dir)

    def validate_spec_structure(self) -> List[ValidationError]:
        """
        Validate SPEC.md structure.

        Returns:
            List of validation errors
        """
        errors = []
        spec_file = self.discovery_dir / 'SPEC.md'

        if not spec_file.exists():
            errors.append(ValidationError(
                severity='ERROR',
                message='SPEC.md not found',
                file='SPEC.md'
            ))
            return errors

        content = spec_file.read_text(encoding='utf-8')

        # Check required sections
        for section in self.REQUIRED_SECTIONS['SPEC.md']:
            if section not in content:
                errors.append(ValidationError(
                    severity='ERROR',
                    message=f"Required section missing: {section}",
                    file='SPEC.md'
                ))

        return errors

    def validate_state_structure(self) -> List[ValidationError]:
        """
        Validate STATE.md structure.

        Returns:
            List of validation errors
        """
        errors = []
        state_file = self.discovery_dir / 'STATE.md'

        if not state_file.exists():
            errors.append(ValidationError(
                severity='ERROR',
                message='STATE.md not found',
                file='STATE.md'
            ))
            return errors

        content = state_file.read_text(encoding='utf-8')

        # Check required sections
        for section in self.REQUIRED_SECTIONS['STATE.md']:
            if section not in content:
                errors.append(ValidationError(
                    severity='ERROR',
                    message=f"Required section missing: {section}",
                    file='STATE.md'
                ))

        # Validate at most one story is "In Progress"
        in_progress_count = content.count('🔄 In Progress')
        if in_progress_count > 1:
            errors.append(ValidationError(
                severity='ERROR',
                message=f"Multiple stories marked as 'In Progress' ({in_progress_count}). Only one story should be in progress at a time.",
                file='STATE.md'
            ))

        return errors

    def validate_id_sequence(self, file_path: Path, entity_type: str, pattern: str) -> List[ValidationError]:
        """
        Validate ID sequence has no duplicates and warn on gaps.

        Args:
            file_path: Path to file
            entity_type: Type of entity (for error messages)
            pattern: Regex pattern to extract IDs

        Returns:
            List of validation errors
        """
        errors = []

        if not file_path.exists():
            return errors

        content = file_path.read_text(encoding='utf-8')
        matches = re.findall(pattern, content, re.MULTILINE)

        if not matches:
            return errors

        # Convert to integers
        ids = [int(m) for m in matches]

        # Check for duplicates
        seen = set()
        for id_num in ids:
            if id_num in seen:
                errors.append(ValidationError(
                    severity='ERROR',
                    message=f"Duplicate {entity_type} ID: {id_num}",
                    file=str(file_path.relative_to(self.discovery_dir))
                ))
            seen.add(id_num)

        # Check for gaps (warn only)
        if ids:
            sorted_ids = sorted(ids)
            for i in range(len(sorted_ids) - 1):
                if sorted_ids[i + 1] - sorted_ids[i] > 1:
                    errors.append(ValidationError(
                        severity='WARN',
                        message=f"{entity_type} IDs skip from {sorted_ids[i]} to {sorted_ids[i + 1]}",
                        file=str(file_path.relative_to(self.discovery_dir))
                    ))

        return errors

    def validate_story_completeness(self, story_content: str) -> List[ValidationError]:
        """
        Validate story has minimum required content for graduation.

        Args:
            story_content: Story content text

        Returns:
            List of validation errors
        """
        errors = []

        # Check for acceptance scenarios
        if '**Acceptance Scenarios**:' not in story_content and 'Acceptance Scenarios' not in story_content:
            errors.append(ValidationError(
                severity='ERROR',
                message='Story missing acceptance scenarios'
            ))

        # Check for priority
        if 'Priority:' not in story_content:
            errors.append(ValidationError(
                severity='WARN',
                message='Story missing priority designation'
            ))

        # Check for independent test
        if '**Independent Test**:' not in story_content and 'Independent Test' not in story_content:
            errors.append(ValidationError(
                severity='WARN',
                message='Story missing independent test description'
            ))

        return errors

    def validate_all(self) -> List[ValidationError]:
        """
        Run all validations.

        Returns:
            List of all validation errors
        """
        errors = []

        # Structure validation
        errors.extend(self.validate_spec_structure())
        errors.extend(self.validate_state_structure())

        # ID sequence validation
        errors.extend(self.validate_id_sequence(
            self.discovery_dir / 'archive' / 'DECISIONS.md',
            'Decision',
            r'^## D(\d+):'
        ))
        errors.extend(self.validate_id_sequence(
            self.discovery_dir / 'archive' / 'RESEARCH.md',
            'Research',
            r'^## R(\d+):'
        ))
        errors.extend(self.validate_id_sequence(
            self.discovery_dir / 'OPEN_QUESTIONS.md',
            'Question',
            r'\*\*Q(\d+)\*\*:'
        ))

        spec_file = self.discovery_dir / 'SPEC.md'
        if spec_file.exists():
            errors.extend(self.validate_id_sequence(
                spec_file,
                'Functional Requirement',
                r'^\| FR-(\d+) \|'
            ))
            errors.extend(self.validate_id_sequence(
                spec_file,
                'Edge Case',
                r'^\| EC-(\d+) \|'
            ))
            errors.extend(self.validate_id_sequence(
                spec_file,
                'Success Criteria',
                r'^\| SC-(\d+) \|'
            ))

        return errors
