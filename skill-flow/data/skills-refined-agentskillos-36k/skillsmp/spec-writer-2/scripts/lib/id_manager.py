"""
ID sequence management for all entity types in spec files.
"""

import re
from pathlib import Path
from typing import Tuple, Optional


class IDManager:
    """Manage ID sequences across all entity types."""

    # Entity type configurations
    ENTITY_CONFIG = {
        'decision': {
            'file': 'archive/DECISIONS.md',
            'pattern': r'^## D(\d+):',
            'format': 'D{}'
        },
        'research': {
            'file': 'archive/RESEARCH.md',
            'pattern': r'^## R(\d+):',
            'format': 'R{}'
        },
        'question': {
            'file': 'OPEN_QUESTIONS.md',
            'pattern': r'\*\*Q(\d+)\*\*:',
            'format': 'Q{}'
        },
        'functional_requirement': {
            'file': 'SPEC.md',
            'pattern': r'^\| FR-(\d+) \|',
            'format': 'FR-{:03d}'
        },
        'edge_case': {
            'file': 'SPEC.md',
            'pattern': r'^\| EC-(\d+) \|',
            'format': 'EC-{:02d}'
        },
        'success_criteria': {
            'file': 'SPEC.md',
            'pattern': r'^\| SC-(\d+) \|',
            'format': 'SC-{:03d}'
        },
        'revision': {
            'file': 'archive/REVISIONS.md',
            'pattern': r'^## REV-(\d+):',
            'format': 'REV-{:03d}'
        },
        'iteration': {
            'file': 'archive/ITERATIONS.md',
            'pattern': r'^## ITR-(\d+):',
            'format': 'ITR-{:03d}'
        },
        'story': {
            'file': 'STATE.md',
            'pattern': r'^\| (\d+) \|',
            'format': '{}'
        }
    }

    def __init__(self, discovery_dir: Path):
        """
        Initialize ID manager.

        Args:
            discovery_dir: Path to discovery/ directory
        """
        self.discovery_dir = Path(discovery_dir)

    def get_next_id(self, entity_type: str) -> str:
        """
        Get next sequential ID for entity type.

        Args:
            entity_type: Type of entity (decision, research, question, etc.)

        Returns:
            Next ID as formatted string

        Raises:
            ValueError: If entity_type is invalid
            FileNotFoundError: If required file doesn't exist
        """
        if entity_type not in self.ENTITY_CONFIG:
            valid_types = ', '.join(self.ENTITY_CONFIG.keys())
            raise ValueError(
                f"Invalid entity_type: {entity_type}. "
                f"Valid types: {valid_types}"
            )

        config = self.ENTITY_CONFIG[entity_type]
        file_path = self.discovery_dir / config['file']

        if not file_path.exists():
            # File doesn't exist yet, return ID 1
            return config['format'].format(1)

        max_id = self.find_max_id(file_path, config['pattern'])
        next_id_num = max_id + 1

        return config['format'].format(next_id_num)

    @staticmethod
    def find_max_id(file_path: Path, pattern: str) -> int:
        """
        Find maximum ID number in file.

        Args:
            file_path: Path to file to scan
            pattern: Regex pattern with capture group for ID number

        Returns:
            Maximum ID number found (0 if none found)
        """
        content = file_path.read_text(encoding='utf-8')
        pattern_re = re.compile(pattern, re.MULTILINE)
        matches = pattern_re.findall(content)

        if not matches:
            return 0

        # Convert to integers and find max
        ids = [int(m) for m in matches]
        return max(ids)

    @staticmethod
    def validate_id(id_value: str, entity_type: str) -> bool:
        """
        Validate ID format for entity type.

        Args:
            id_value: ID to validate (e.g., "D15", "FR-007")
            entity_type: Type of entity

        Returns:
            True if valid format, False otherwise
        """
        if entity_type not in IDManager.ENTITY_CONFIG:
            return False

        config = IDManager.ENTITY_CONFIG[entity_type]
        format_pattern = config['format']

        # Build validation pattern from format string
        if entity_type == 'decision':
            pattern = r'^D\d+$'
        elif entity_type == 'research':
            pattern = r'^R\d+$'
        elif entity_type == 'question':
            pattern = r'^Q\d+$'
        elif entity_type == 'functional_requirement':
            pattern = r'^FR-\d{3}$'
        elif entity_type == 'edge_case':
            pattern = r'^EC-\d{2}$'
        elif entity_type == 'success_criteria':
            pattern = r'^SC-\d{3}$'
        elif entity_type == 'revision':
            pattern = r'^REV-\d{3}$'
        elif entity_type == 'iteration':
            pattern = r'^ITR-\d{3}$'
        elif entity_type == 'story':
            pattern = r'^\d+$'
        else:
            return False

        return bool(re.match(pattern, id_value))

    @staticmethod
    def parse_id(id_value: str) -> Tuple[Optional[str], Optional[int]]:
        """
        Parse ID into entity type and number.

        Args:
            id_value: ID to parse (e.g., "D15", "FR-007")

        Returns:
            Tuple of (entity_type, number) or (None, None) if invalid

        Examples:
            "D15" -> ("decision", 15)
            "FR-007" -> ("functional_requirement", 7)
            "Q23" -> ("question", 23)
        """
        # Try each entity type pattern
        patterns = {
            'decision': r'^D(\d+)$',
            'research': r'^R(\d+)$',
            'question': r'^Q(\d+)$',
            'functional_requirement': r'^FR-(\d+)$',
            'edge_case': r'^EC-(\d+)$',
            'success_criteria': r'^SC-(\d+)$',
            'revision': r'^REV-(\d+)$',
            'iteration': r'^ITR-(\d+)$',
            'story': r'^(\d+)$'  # Note: Only use this for explicit story context
        }

        for entity_type, pattern in patterns.items():
            match = re.match(pattern, id_value)
            if match:
                return (entity_type, int(match.group(1)))

        return (None, None)
