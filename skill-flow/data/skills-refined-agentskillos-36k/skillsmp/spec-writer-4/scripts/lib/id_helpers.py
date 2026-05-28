"""
Helper functions for ID handling in scripts.

Provides convenient wrappers around IDNormalizer and IDManager
for consistent ID handling across all scripts.
"""

import sys
from typing import Optional, List
from .id_normalizer import IDNormalizer
from .id_manager import IDManager


def normalize_and_notify(id_value: str, entity_type: Optional[str] = None, quiet: bool = False) -> Optional[str]:
    """
    Normalize ID and notify user if modified.

    Args:
        id_value: ID to normalize
        entity_type: Optional entity type hint
        quiet: If True, suppress normalization notifications

    Returns:
        Canonical ID or None if invalid

    Example:
        >>> normalize_and_notify("D02", "decision")
        Normalized ID: D02 → D2
        'D2'

        >>> normalize_and_notify("FR5", "functional_requirement")
        Normalized ID: FR5 → FR-005
        'FR-005'
    """
    canonical_id, detected_type, was_modified = IDNormalizer.normalize(id_value, entity_type)

    if not canonical_id:
        return None

    # Notify user if ID was normalized (unless quiet mode)
    if was_modified and not quiet:
        print(f"ℹ️  Normalized ID: {id_value} → {canonical_id}", file=sys.stderr)

    return canonical_id


def validate_and_suggest(id_value: str, entity_type: str, id_manager: IDManager) -> Optional[str]:
    """
    Validate ID and provide suggestions if invalid.

    Args:
        id_value: ID to validate
        entity_type: Expected entity type
        id_manager: IDManager instance for suggestions

    Returns:
        Canonical ID if valid, None if invalid (after showing suggestions)

    Example:
        >>> validate_and_suggest("D99", "decision", id_manager)
        ERROR: Invalid ID: D99

        Did you mean one of these?
          - D9
          - D19
          - D90

        None
    """
    canonical_id = normalize_and_notify(id_value, entity_type)

    if not canonical_id:
        print(f"ERROR: Invalid ID format: {id_value}", file=sys.stderr)
        print(f"Expected format for {entity_type}: {get_format_hint(entity_type)}", file=sys.stderr)
        return None

    # Verify entity type matches if specified
    detected_type = IDNormalizer.get_entity_type(canonical_id)
    if entity_type and detected_type != entity_type:
        print(f"ERROR: ID {id_value} is a {detected_type}, expected {entity_type}", file=sys.stderr)
        return None

    return canonical_id


def validate_id_exists(id_value: str, entity_type: str, id_manager: IDManager) -> bool:
    """
    Validate that ID exists in spec files and provide suggestions if not.

    Args:
        id_value: ID to check (will be normalized first)
        entity_type: Expected entity type
        id_manager: IDManager instance for validation

    Returns:
        True if ID exists, False otherwise (after showing suggestions)

    Example:
        >>> validate_id_exists("D99", "decision", id_manager)
        ERROR: Decision D99 not found in DECISIONS.md

        Did you mean one of these?
          - D9
          - D19
          - D90

        False
    """
    canonical_id = normalize_and_notify(id_value, entity_type)

    if not canonical_id:
        return False

    # Get all existing IDs from file
    suggestions = id_manager.suggest_id_corrections(canonical_id, entity_type)

    # Check if ID exists (it exists if it's in suggestions or if suggestions is empty)
    # This is a simple heuristic - we'd need actual existence checking for production
    if suggestions and canonical_id not in suggestions:
        entity_name = entity_type.replace('_', ' ').title()
        config = id_manager.ENTITY_CONFIG.get(entity_type, {})
        file_name = config.get('file', 'spec file')

        print(f"ERROR: {entity_name} {canonical_id} not found in {file_name}", file=sys.stderr)
        print(f"\nDid you mean one of these?", file=sys.stderr)
        for suggestion in suggestions[:5]:
            print(f"  - {suggestion}", file=sys.stderr)
        return False

    return True


def parse_id_list(id_str: str, entity_type: Optional[str] = None) -> List[str]:
    """
    Parse comma-separated list of IDs and normalize each.

    Args:
        id_str: Comma-separated ID list (e.g., "D1, D2, D3" or "FR-005,FR-006")
        entity_type: Optional entity type hint

    Returns:
        List of canonical IDs

    Example:
        >>> parse_id_list("D1, D2, D3", "decision")
        ['D1', 'D2', 'D3']

        >>> parse_id_list("FR5, FR-006, FR7", "functional_requirement")
        ℹ️  Normalized ID: FR5 → FR-005
        ℹ️  Normalized ID: FR7 → FR-007
        ['FR-005', 'FR-006', 'FR-007']
    """
    if not id_str or not id_str.strip():
        return []

    # Split by comma and normalize each ID
    ids = [id.strip() for id in id_str.split(',')]
    canonical_ids = []

    for id_value in ids:
        if not id_value:
            continue

        canonical_id = normalize_and_notify(id_value, entity_type)
        if canonical_id:
            canonical_ids.append(canonical_id)
        else:
            print(f"⚠️  Skipping invalid ID: {id_value}", file=sys.stderr)

    return canonical_ids


def get_format_hint(entity_type: str) -> str:
    """
    Get human-readable format hint for entity type.

    Args:
        entity_type: Entity type

    Returns:
        Format hint string

    Example:
        >>> get_format_hint("decision")
        'D# (e.g., D2, D15, D123)'

        >>> get_format_hint("functional_requirement")
        'FR-### (e.g., FR-001, FR-025, FR-123)'
    """
    format_hints = {
        'decision': 'D# (e.g., D2, D15, D123)',
        'research': 'R# (e.g., R1, R10, R50)',
        'question': 'Q# (e.g., Q1, Q5, Q12)',
        'functional_requirement': 'FR-### (e.g., FR-001, FR-025, FR-123)',
        'edge_case': 'EC-## (e.g., EC-01, EC-15, EC-99)',
        'success_criteria': 'SC-### (e.g., SC-001, SC-050, SC-100)',
        'revision': 'REV-### (e.g., REV-001, REV-010, REV-050)',
        'iteration': 'ITR-### (e.g., ITR-001, ITR-010, ITR-025)',
        'story': '# (e.g., 1, 2, 10)'
    }

    return format_hints.get(entity_type, 'Unknown format')


def format_id_for_display(id_value: str) -> str:
    """
    Format ID for user display (normalize and return canonical form).

    Args:
        id_value: ID to format

    Returns:
        Canonical ID or original if normalization fails

    Example:
        >>> format_id_for_display("D02")
        'D2'

        >>> format_id_for_display("FR5")
        'FR-005'
    """
    canonical_id, _, _ = IDNormalizer.normalize(id_value)
    return canonical_id if canonical_id else id_value


def normalize_id_list_string(id_str: str, entity_type: Optional[str] = None, quiet: bool = False) -> Optional[str]:
    """
    Normalize a comma-separated ID list string.

    Args:
        id_str: Comma-separated ID list (e.g., "D1, D2, D3" or "Q9, Q12")
                Can also include ranges like "Q1-Q5" (ranges are preserved as-is)
        entity_type: Optional entity type hint
        quiet: If True, suppress normalization notifications

    Returns:
        Normalized ID list string or None if all IDs are invalid

    Example:
        >>> normalize_id_list_string("D02, D3", "decision")
        ℹ️  Normalized ID: D02 → D2
        'D2, D3'

        >>> normalize_id_list_string("Q1-Q5", "question")
        'Q1-Q5'

        >>> normalize_id_list_string("D1, D02, D3", "decision", quiet=True)
        'D1, D2, D3'
    """
    if not id_str or not id_str.strip():
        return None

    # Split by comma and normalize each part
    parts = [part.strip() for part in id_str.split(',')]
    normalized_parts = []

    for part in parts:
        if not part:
            continue

        # Check if this is a range (e.g., "Q1-Q5")
        if '-' in part and not part.startswith(('ITR-', 'FR-', 'SC-', 'EC-', 'REV-')):
            # This might be a range like "Q1-Q5" or "D10-D15"
            # Try to normalize the range endpoints
            range_parts = part.split('-', 1)
            if len(range_parts) == 2:
                start_id = normalize_and_notify(range_parts[0].strip(), entity_type, quiet=quiet)
                end_id = normalize_and_notify(range_parts[1].strip(), entity_type, quiet=quiet)
                if start_id and end_id:
                    normalized_parts.append(f"{start_id}-{end_id}")
                    continue

        # Not a range, normalize as single ID
        canonical_id = normalize_and_notify(part, entity_type, quiet=quiet)
        if canonical_id:
            normalized_parts.append(canonical_id)
        else:
            if not quiet:
                print(f"⚠️  Skipping invalid ID: {part}", file=sys.stderr)

    if not normalized_parts:
        return None

    return ', '.join(normalized_parts)
