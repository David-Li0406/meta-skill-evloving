"""
ID sequence management for all entity types in spec files.
"""

import re
from pathlib import Path
from typing import Tuple, Optional, List
from .id_normalizer import IDNormalizer


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
        Validate ID format for entity type (flexible - accepts variants).

        Args:
            id_value: ID to validate (e.g., "D15", "D-15", "D015", "FR-007", "FR7")
            entity_type: Type of entity

        Returns:
            True if valid/normalizable format, False otherwise

        Note:
            Now accepts flexible formats via IDNormalizer:
            - D2, D02, d2 all valid for decision
            - FR-5, FR5, FR-005 all valid for functional_requirement
            - EC-1, EC1, EC-01 all valid for edge_case
        """
        if entity_type not in IDManager.ENTITY_CONFIG:
            return False

        return IDNormalizer.is_valid_format(id_value, entity_type)

    @staticmethod
    def normalize_id(id_value: str, entity_type: Optional[str] = None) -> Tuple[Optional[str], Optional[str], bool]:
        """
        Normalize ID to canonical format.

        Args:
            id_value: ID to normalize (e.g., "D02", "FR5", "ec-01")
            entity_type: Optional entity type hint

        Returns:
            Tuple of (canonical_id, detected_type, was_modified)

        Examples:
            normalize_id("D02") -> ("D2", "decision", True)
            normalize_id("FR5") -> ("FR-005", "functional_requirement", True)
            normalize_id("EC-01") -> ("EC-01", "edge_case", False)
        """
        return IDNormalizer.normalize(id_value, entity_type)

    def suggest_id_corrections(self, invalid_id: str, entity_type: str) -> List[str]:
        """
        Suggest similar valid IDs based on existing IDs in files.

        Args:
            invalid_id: The invalid ID that was provided
            entity_type: Entity type to search for suggestions

        Returns:
            List of suggested IDs from the spec files

        Example:
            suggest_id_corrections("D99", "decision") -> ["D9", "D19", "D90"]
        """
        if entity_type not in self.ENTITY_CONFIG:
            return []

        config = self.ENTITY_CONFIG[entity_type]
        file_path = self.discovery_dir / config['file']

        if not file_path.exists():
            return []

        # Extract all existing IDs from file
        content = file_path.read_text(encoding='utf-8')
        pattern_re = re.compile(config['pattern'], re.MULTILINE)
        matches = pattern_re.findall(content)

        if not matches:
            return []

        # Format IDs in canonical form
        valid_ids = [config['format'].format(int(m)) for m in matches]

        # Use fuzzy matching to find similar IDs
        return IDNormalizer.suggest_corrections(invalid_id, valid_ids)

    @staticmethod
    def parse_id(id_value: str) -> Tuple[Optional[str], Optional[int]]:
        """
        Parse ID into entity type and number (flexible - accepts variants).

        Args:
            id_value: ID to parse (e.g., "D15", "D-15", "FR-007", "FR7")

        Returns:
            Tuple of (entity_type, number) or (None, None) if invalid

        Examples:
            "D15" -> ("decision", 15)
            "D-15" -> ("decision", 15)
            "FR-007" -> ("functional_requirement", 7)
            "FR7" -> ("functional_requirement", 7)
            "Q23" -> ("question", 23)

        Note:
            Now uses IDNormalizer for flexible parsing:
            - Accepts D2, D02, D-2 all as decision #2
            - Accepts FR-5, FR5, FR-005 all as functional_requirement #5
        """
        canonical_id, entity_type, _ = IDNormalizer.normalize(id_value)

        if not canonical_id or not entity_type:
            return (None, None)

        # Extract number from canonical ID
        num = IDNormalizer.extract_number(canonical_id)
        if num is None:
            return (None, None)

        return (entity_type, num)
