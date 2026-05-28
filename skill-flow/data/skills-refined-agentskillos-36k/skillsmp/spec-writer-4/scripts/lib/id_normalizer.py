"""
Flexible ID parsing and normalization for spec-writer scripts.

Accepts various ID formats and normalizes to canonical form:
- D2, D02, d2, d002 → D2
- FR-5, FR-005, fr5, FR5 → FR-005
- EC-1, EC-01, ec01 → EC-01
"""

import re
from typing import Tuple, Optional, List
from difflib import get_close_matches


class IDNormalizer:
    """Normalize flexible ID formats to canonical form."""

    # Entity type configurations with flexible patterns
    ENTITY_PATTERNS = {
        'decision': {
            'patterns': [
                r'^D-?(\d+)$',  # D2, D-2, D02, D-02
            ],
            'canonical_format': 'D{}',  # D2
            'prefix': 'D'
        },
        'research': {
            'patterns': [
                r'^R-?(\d+)$',  # R5, R-5, R05, R-05
            ],
            'canonical_format': 'R{}',  # R5
            'prefix': 'R'
        },
        'question': {
            'patterns': [
                r'^Q-?(\d+)$',  # Q12, Q-12, Q012
            ],
            'canonical_format': 'Q{}',  # Q12
            'prefix': 'Q'
        },
        'functional_requirement': {
            'patterns': [
                r'^FR-?(\d+)$',  # FR-5, FR5, FR-005, FR005
            ],
            'canonical_format': 'FR-{:03d}',  # FR-005
            'prefix': 'FR'
        },
        'edge_case': {
            'patterns': [
                r'^EC-?(\d+)$',  # EC-1, EC1, EC-01, EC01
            ],
            'canonical_format': 'EC-{:02d}',  # EC-01
            'prefix': 'EC'
        },
        'success_criteria': {
            'patterns': [
                r'^SC-?(\d+)$',  # SC-3, SC3, SC-003, SC003
            ],
            'canonical_format': 'SC-{:03d}',  # SC-003
            'prefix': 'SC'
        },
        'revision': {
            'patterns': [
                r'^REV-?(\d+)$',  # REV-2, REV2, REV-002, REV002
            ],
            'canonical_format': 'REV-{:03d}',  # REV-002
            'prefix': 'REV'
        },
        'iteration': {
            'patterns': [
                r'^ITR-?(\d+)$',  # ITR-1, ITR1, ITR-001, ITR001
            ],
            'canonical_format': 'ITR-{:03d}',  # ITR-001
            'prefix': 'ITR'
        },
        'story': {
            'patterns': [
                r'^(\d+)$',  # Just numbers for stories
            ],
            'canonical_format': '{}',  # 3
            'prefix': ''
        }
    }

    @classmethod
    def normalize(cls, id_input: str, entity_type: Optional[str] = None) -> Tuple[Optional[str], Optional[str], bool]:
        """
        Normalize ID to canonical format.

        Args:
            id_input: ID to normalize (e.g., "D02", "FR5", "ec-01")
            entity_type: Optional entity type hint to try first

        Returns:
            Tuple of (canonical_id, entity_type, was_modified)
            - canonical_id: Normalized ID string or None if invalid
            - entity_type: Detected entity type or None if invalid
            - was_modified: True if normalization changed the input

        Examples:
            normalize("D02") -> ("D2", "decision", True)
            normalize("FR5") -> ("FR-005", "functional_requirement", True)
            normalize("EC-01") -> ("EC-01", "edge_case", False)
            normalize("invalid") -> (None, None, False)
        """
        original_input = id_input
        id_input = id_input.strip().upper()  # Case-insensitive, trim whitespace

        # Try entity_type hint first if provided
        if entity_type and entity_type in cls.ENTITY_PATTERNS:
            result = cls._try_normalize_for_type(id_input, entity_type)
            if result:
                canonical_id, num = result
                was_modified = (canonical_id != original_input)
                return (canonical_id, entity_type, was_modified)

        # Try all entity types
        for etype, config in cls.ENTITY_PATTERNS.items():
            result = cls._try_normalize_for_type(id_input, etype)
            if result:
                canonical_id, num = result
                was_modified = (canonical_id != original_input)
                return (canonical_id, etype, was_modified)

        return (None, None, False)

    @classmethod
    def _try_normalize_for_type(cls, id_input: str, entity_type: str) -> Optional[Tuple[str, int]]:
        """
        Try to normalize ID for specific entity type.

        Args:
            id_input: Uppercase, trimmed ID string
            entity_type: Entity type to try

        Returns:
            Tuple of (canonical_id, number) or None if doesn't match
        """
        config = cls.ENTITY_PATTERNS[entity_type]

        for pattern in config['patterns']:
            match = re.match(pattern, id_input, re.IGNORECASE)
            if match:
                num = int(match.group(1))
                canonical_id = config['canonical_format'].format(num)
                return (canonical_id, num)

        return None

    @classmethod
    def suggest_corrections(cls, invalid_id: str, valid_ids: List[str], max_suggestions: int = 5) -> List[str]:
        """
        Suggest similar valid IDs using fuzzy matching.

        Args:
            invalid_id: The invalid ID that was provided
            valid_ids: List of valid IDs to compare against
            max_suggestions: Maximum number of suggestions to return

        Returns:
            List of suggested IDs, ordered by similarity

        Examples:
            suggest_corrections("D99", ["D1", "D9", "D19", "D90"]) -> ["D9", "D19", "D90"]
            suggest_corrections("FR-99", ["FR-001", "FR-002", "FR-010"]) -> ["FR-001", "FR-002"]
        """
        if not valid_ids:
            return []

        # Use difflib to find close matches
        # cutoff=0.4 is fairly permissive to catch typos
        suggestions = get_close_matches(
            invalid_id.upper(),
            [v.upper() for v in valid_ids],
            n=max_suggestions,
            cutoff=0.4
        )

        # Return original-case versions
        suggestion_map = {v.upper(): v for v in valid_ids}
        return [suggestion_map[s] for s in suggestions if s in suggestion_map]

    @classmethod
    def extract_number(cls, id_value: str) -> Optional[int]:
        """
        Extract numeric portion from any ID format.

        Args:
            id_value: ID string (e.g., "D2", "FR-005", "3")

        Returns:
            Numeric portion as integer, or None if not found

        Examples:
            extract_number("D2") -> 2
            extract_number("FR-005") -> 5
            extract_number("EC-01") -> 1
        """
        canonical_id, entity_type, _ = cls.normalize(id_value)
        if not canonical_id:
            return None

        # Parse number from canonical form
        result = cls._try_normalize_for_type(canonical_id, entity_type)
        if result:
            _, num = result
            return num

        return None

    @classmethod
    def get_entity_type(cls, id_value: str) -> Optional[str]:
        """
        Detect entity type from ID format.

        Args:
            id_value: ID string (e.g., "D2", "FR-005")

        Returns:
            Entity type string or None if invalid

        Examples:
            get_entity_type("D2") -> "decision"
            get_entity_type("FR-005") -> "functional_requirement"
            get_entity_type("invalid") -> None
        """
        _, entity_type, _ = cls.normalize(id_value)
        return entity_type

    @classmethod
    def format_id(cls, entity_type: str, number: int) -> Optional[str]:
        """
        Format ID number to canonical form for entity type.

        Args:
            entity_type: Type of entity
            number: Numeric ID

        Returns:
            Canonical ID string or None if invalid entity type

        Examples:
            format_id("decision", 2) -> "D2"
            format_id("functional_requirement", 5) -> "FR-005"
            format_id("edge_case", 1) -> "EC-01"
        """
        if entity_type not in cls.ENTITY_PATTERNS:
            return None

        config = cls.ENTITY_PATTERNS[entity_type]
        return config['canonical_format'].format(number)

    @classmethod
    def is_valid_format(cls, id_value: str, entity_type: Optional[str] = None) -> bool:
        """
        Check if ID is valid (can be normalized).

        Args:
            id_value: ID to check
            entity_type: Optional entity type to validate against

        Returns:
            True if valid/normalizable, False otherwise

        Examples:
            is_valid_format("D2") -> True
            is_valid_format("D02") -> True
            is_valid_format("FR5") -> True
            is_valid_format("invalid") -> False
        """
        canonical_id, detected_type, _ = cls.normalize(id_value, entity_type)

        if not canonical_id:
            return False

        # If entity_type specified, verify it matches
        if entity_type and detected_type != entity_type:
            return False

        return True
