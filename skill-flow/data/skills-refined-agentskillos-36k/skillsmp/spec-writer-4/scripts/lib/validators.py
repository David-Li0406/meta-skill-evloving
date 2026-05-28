"""
Structure validation utilities for spec files.
"""

import re
from pathlib import Path
from typing import List, Tuple, Optional
from dataclasses import dataclass

from .cross_references import ValidationError
from .id_manager import IDManager
from .file_operations import SafeFileOperations


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


# Cross-reference validation functions

def validate_story_exists(story_num: int, discovery_dir: Path) -> Tuple[bool, Optional[List[int]]]:
    """
    Check if story exists in STATE.md Story Status Overview table.

    Args:
        story_num: Story number to check
        discovery_dir: Path to discovery/ directory

    Returns:
        Tuple of (exists: bool, suggested_story_numbers: Optional[List[int]])
        If story doesn't exist, returns list of existing story numbers as suggestions.

    Example:
        >>> exists, suggestions = validate_story_exists(99, discovery_dir)
        >>> if not exists:
        ...     print(f"Story 99 not found. Did you mean: {suggestions}")
    """
    state_file = discovery_dir / 'STATE.md'
    if not state_file.exists():
        return False, None

    content = SafeFileOperations.read_file(state_file)

    # Extract all story numbers from the Story Status Overview table
    # Format: | 1 | Title | Priority | Status | Confidence |
    story_pattern = re.compile(r'^\| (\d+) \|', re.MULTILINE)
    matches = story_pattern.findall(content)

    existing_stories = [int(num) for num in matches]

    # Check if requested story exists
    if story_num in existing_stories:
        return True, None

    # Story doesn't exist - provide suggestions
    # Sort by proximity to requested number
    if existing_stories:
        sorted_stories = sorted(existing_stories, key=lambda x: abs(x - story_num))
        suggestions = sorted_stories[:5]  # Return up to 5 closest matches
        return False, suggestions

    return False, []


def validate_question_exists(question_id: str, discovery_dir: Path, id_manager: IDManager) -> Tuple[bool, Optional[List[str]]]:
    """
    Check if question exists in OPEN_QUESTIONS.md.

    Args:
        question_id: Question ID to check (e.g., "Q23")
        discovery_dir: Path to discovery/ directory
        id_manager: IDManager instance for ID suggestions

    Returns:
        Tuple of (exists: bool, suggested_question_ids: Optional[List[str]])
        If question doesn't exist, returns list of similar question IDs as suggestions.

    Example:
        >>> exists, suggestions = validate_question_exists("Q99", discovery_dir, id_manager)
        >>> if not exists:
        ...     print(f"Q99 not found. Did you mean: {', '.join(suggestions)}")
    """
    questions_file = discovery_dir / 'OPEN_QUESTIONS.md'
    if not questions_file.exists():
        return False, None

    content = SafeFileOperations.read_file(questions_file)

    # Extract all question IDs from OPEN_QUESTIONS.md
    # Format: - **Q23**: Question text
    question_pattern = re.compile(r'\*\*Q(\d+)\*\*:', re.MULTILINE)
    matches = question_pattern.findall(content)

    existing_questions = [f"Q{num}" for num in matches]

    # Check if requested question exists
    if question_id in existing_questions:
        return True, None

    # Question doesn't exist - use ID manager for fuzzy suggestions
    suggestions = id_manager.suggest_id_corrections(question_id, 'question')

    if suggestions:
        # Filter to only existing questions
        filtered_suggestions = [q for q in suggestions if q in existing_questions]
        return False, filtered_suggestions[:5] if filtered_suggestions else suggestions[:5]

    return False, existing_questions[:5] if existing_questions else []


def validate_decision_exists(decision_id: str, discovery_dir: Path, id_manager: IDManager) -> Tuple[bool, Optional[List[str]]]:
    """
    Check if decision exists in archive/DECISIONS.md.

    Args:
        decision_id: Decision ID to check (e.g., "D15")
        discovery_dir: Path to discovery/ directory
        id_manager: IDManager instance for ID suggestions

    Returns:
        Tuple of (exists: bool, suggested_decision_ids: Optional[List[str]])
        If decision doesn't exist, returns list of similar decision IDs as suggestions.

    Example:
        >>> exists, suggestions = validate_decision_exists("D99", discovery_dir, id_manager)
        >>> if not exists:
        ...     print(f"D99 not found. Did you mean: {', '.join(suggestions)}")
    """
    decisions_file = discovery_dir / 'archive' / 'DECISIONS.md'
    if not decisions_file.exists():
        return False, None

    content = SafeFileOperations.read_file(decisions_file)

    # Extract all decision IDs from DECISIONS.md
    # Format: ## D15: Title — Date
    decision_pattern = re.compile(r'^## D(\d+):', re.MULTILINE)
    matches = decision_pattern.findall(content)

    existing_decisions = [f"D{num}" for num in matches]

    # Check if requested decision exists
    if decision_id in existing_decisions:
        return True, None

    # Decision doesn't exist - use ID manager for fuzzy suggestions
    suggestions = id_manager.suggest_id_corrections(decision_id, 'decision')

    if suggestions:
        # Filter to only existing decisions
        filtered_suggestions = [d for d in suggestions if d in existing_decisions]
        return False, filtered_suggestions[:5] if filtered_suggestions else suggestions[:5]

    return False, existing_decisions[:5] if existing_decisions else []


def validate_research_exists(research_id: str, discovery_dir: Path, id_manager: IDManager) -> Tuple[bool, Optional[List[str]]]:
    """
    Check if research exists in archive/RESEARCH.md.

    Args:
        research_id: Research ID to check (e.g., "R5")
        discovery_dir: Path to discovery/ directory
        id_manager: IDManager instance for ID suggestions

    Returns:
        Tuple of (exists: bool, suggested_research_ids: Optional[List[str]])
        If research doesn't exist, returns list of similar research IDs as suggestions.

    Example:
        >>> exists, suggestions = validate_research_exists("R99", discovery_dir, id_manager)
        >>> if not exists:
        ...     print(f"R99 not found. Did you mean: {', '.join(suggestions)}")
    """
    research_file = discovery_dir / 'archive' / 'RESEARCH.md'
    if not research_file.exists():
        return False, None

    content = SafeFileOperations.read_file(research_file)

    # Extract all research IDs from RESEARCH.md
    # Format: ## R5: Topic — Date
    research_pattern = re.compile(r'^## R(\d+):', re.MULTILINE)
    matches = research_pattern.findall(content)

    existing_research = [f"R{num}" for num in matches]

    # Check if requested research exists
    if research_id in existing_research:
        return True, None

    # Research doesn't exist - use ID manager for fuzzy suggestions
    suggestions = id_manager.suggest_id_corrections(research_id, 'research')

    if suggestions:
        # Filter to only existing research
        filtered_suggestions = [r for r in suggestions if r in existing_research]
        return False, filtered_suggestions[:5] if filtered_suggestions else suggestions[:5]

    return False, existing_research[:5] if existing_research else []
