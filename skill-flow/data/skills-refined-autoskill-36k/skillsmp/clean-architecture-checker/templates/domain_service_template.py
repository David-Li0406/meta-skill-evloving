"""
Template for creating a domain service in the Domain layer.

Replace:
- EntityName: Your entity name
- EntityNameDomainService: Your service name

Domain services contain business logic that:
- Doesn't naturally belong to any single entity
- Involves multiple entities
- Is a pure algorithm or calculation
- Requires external dependencies (but not repositories directly)
"""

from src.domain.entities.entity_name import EntityName


class EntityNameDomainService:
    """
    Domain service for [entity] business logic.

    This service encapsulates business rules and logic that don't
    naturally fit into a single entity.

    Examples of what belongs here:
    - Validation across multiple entities
    - Complex calculations
    - Name normalization algorithms
    - Similarity/matching algorithms
    - Deduplication logic
    """

    # Constants used in business logic
    VALID_STATUSES = ["active", "inactive", "pending"]
    MAX_NAME_LENGTH = 100

    def __init__(self):
        """
        Initialize domain service.

        Note: Domain services typically don't have dependencies.
        If you need repositories, consider if the logic should be
        in a use case instead.
        """
        pass

    def validate(self, entity: EntityName) -> tuple[bool, list[str]]:
        """
        Validate entity against business rules.

        Args:
            entity: Entity to validate

        Returns:
            Tuple of (is_valid, list of error messages)
        """
        errors = []

        # Example validation rules
        if not entity.name or not entity.name.strip():
            errors.append("Name is required")

        if len(entity.name) > self.MAX_NAME_LENGTH:
            errors.append(f"Name too long (max {self.MAX_NAME_LENGTH})")

        # Add your business rule validations here

        return (len(errors) == 0, errors)

    def normalize_name(self, raw_name: str) -> str:
        """
        Normalize entity name according to business rules.

        Args:
            raw_name: Raw name to normalize

        Returns:
            Normalized name

        Example business rules:
        - Remove extra whitespace
        - Convert to standard format
        - Remove special characters
        """
        if not raw_name:
            return ""

        # Example normalization
        name = raw_name.strip()
        name = " ".join(name.split())  # Collapse multiple spaces
        # Add your normalization logic

        return name

    def calculate_similarity(self, entity1: EntityName, entity2: EntityName) -> float:
        """
        Calculate similarity score between two entities.

        Args:
            entity1: First entity
            entity2: Second entity

        Returns:
            Similarity score between 0.0 and 1.0
        """
        # Example: Simple name similarity
        if entity1.name == entity2.name:
            return 1.0

        # Implement your similarity algorithm
        # Could use Levenshtein distance, fuzzy matching, etc.
        return 0.0

    def is_duplicate(
        self, entity: EntityName, existing_entities: list[EntityName]
    ) -> tuple[bool, EntityName | None]:
        """
        Check if entity is a duplicate of existing entities.

        Args:
            entity: Entity to check
            existing_entities: List of existing entities

        Returns:
            Tuple of (is_duplicate, matching_entity)
        """
        for existing in existing_entities:
            similarity = self.calculate_similarity(entity, existing)
            if similarity >= 0.9:  # Business rule: 90% similarity = duplicate
                return (True, existing)

        return (False, None)

    def merge_entities(self, primary: EntityName, duplicate: EntityName) -> EntityName:
        """
        Merge two duplicate entities.

        Business rules for merging:
        - Keep primary entity's ID
        - Prefer non-null values
        - Concatenate unique data

        Args:
            primary: Primary entity to keep
            duplicate: Duplicate entity to merge from

        Returns:
            Merged entity
        """
        # Example merge logic
        merged_name = primary.name or duplicate.name

        # Create merged entity
        merged = EntityName(
            id=primary.id,
            name=merged_name,
            # Add merge logic for other fields
        )

        return merged

    def categorize(self, entity: EntityName) -> str:
        """
        Categorize entity based on business rules.

        Args:
            entity: Entity to categorize

        Returns:
            Category name
        """
        # Example categorization logic
        if len(entity.name) < 10:
            return "short"
        elif len(entity.name) < 50:
            return "medium"
        else:
            return "long"

    def calculate_score(self, entity: EntityName) -> float:
        """
        Calculate business score for entity.

        Args:
            entity: Entity to score

        Returns:
            Score value
        """
        score = 0.0

        # Example scoring logic
        if entity.name:
            score += 10.0

        # Add your scoring algorithm

        return score

    def apply_business_rule(self, entity: EntityName) -> EntityName:
        """
        Apply complex business rule to entity.

        Args:
            entity: Entity to process

        Returns:
            Processed entity
        """
        # Example business rule application
        processed_name = self.normalize_name(entity.name)

        # Create new entity with rule applied
        processed = EntityName(
            id=entity.id,
            name=processed_name,
            # Copy other fields
        )

        return processed


class EntityNameMatchingService:
    """
    Specialized domain service for entity matching.

    When domain services get large, consider splitting into
    focused services like this one.
    """

    SIMILARITY_THRESHOLD = 0.8

    def find_best_match(
        self, entity: EntityName, candidates: list[EntityName]
    ) -> tuple[EntityName | None, float]:
        """
        Find best matching entity from candidates.

        Args:
            entity: Entity to match
            candidates: List of candidate entities

        Returns:
            Tuple of (best_match, confidence_score)
        """
        if not candidates:
            return (None, 0.0)

        best_match = None
        best_score = 0.0

        for candidate in candidates:
            score = self._calculate_match_score(entity, candidate)
            if score > best_score and score >= self.SIMILARITY_THRESHOLD:
                best_score = score
                best_match = candidate

        return (best_match, best_score)

    def _calculate_match_score(self, entity1: EntityName, entity2: EntityName) -> float:
        """Calculate match score between two entities."""
        # Implement matching algorithm
        # Consider multiple factors (name, attributes, etc.)
        return 0.0


class EntityNameValidationService:
    """
    Specialized domain service for entity validation.

    Complex validation logic can be extracted to its own service.
    """

    def validate_for_creation(self, entity: EntityName) -> tuple[bool, list[str]]:
        """
        Validate entity for creation operation.

        Args:
            entity: Entity to validate

        Returns:
            Tuple of (is_valid, error_messages)
        """
        errors = []

        # Add creation-specific validation rules
        if entity.id is not None:
            errors.append("New entity should not have ID")

        return (len(errors) == 0, errors)

    def validate_for_update(self, entity: EntityName) -> tuple[bool, list[str]]:
        """
        Validate entity for update operation.

        Args:
            entity: Entity to validate

        Returns:
            Tuple of (is_valid, error_messages)
        """
        errors = []

        # Add update-specific validation rules
        if entity.id is None:
            errors.append("Entity must have ID for update")

        return (len(errors) == 0, errors)
