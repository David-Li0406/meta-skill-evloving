"""NCBITaxon ID validators.

Validates NCBI Taxonomy IDs against the NCBI Entrez API:
- Check that IDs exist
- Check that names match expected values
- Check taxonomic rank
- For lists, verify all IDs are related to the expected species
"""

from __future__ import annotations

import logging
import re
from typing import TYPE_CHECKING, Any

from cmm_ai_automation.validation.base import (
    FieldValidator,
    IssueType,
    ListValidator,
    Severity,
    ValidationIssue,
)

if TYPE_CHECKING:
    from cmm_ai_automation.strains.ncbi import NcbiTaxonData

logger = logging.getLogger(__name__)


def parse_ncbi_taxon_curie(value: str) -> str | None:
    """Extract numeric taxon ID from various formats.

    Handles:
        - "408" (plain number)
        - "NCBITaxon:408"
        - "NCBITaxon:408004"

    Args:
        value: Input value that may be a taxon ID

    Returns:
        Numeric ID as string, or None if not parseable
    """
    if not value:
        return None

    value = value.strip()

    # Plain number
    if value.isdigit():
        return value

    # CURIE format
    match = re.match(r"NCBITaxon:(\d+)", value, re.IGNORECASE)
    if match:
        return match.group(1)

    return None


class NCBITaxonValidator(FieldValidator):
    """Validate a single NCBITaxon ID.

    Checks:
        1. ID is parseable
        2. ID exists in NCBI Taxonomy
        3. Rank matches expected rank (if check_rank option set)
        4. Name matches scientific_name in context (if present)

    Options:
        check_rank: Expected rank (e.g., "species", "strain")
        name_field: Context field to cross-check name against (default: "scientific_name")
    """

    def __init__(
        self,
        check_rank: str | None = None,
        name_field: str = "scientific_name",
    ):
        """Initialize validator.

        Args:
            check_rank: If set, verify the taxon has this rank
            name_field: Context field containing expected name
        """
        self.check_rank = check_rank
        self.name_field = name_field
        self._cache: dict[str, NcbiTaxonData] = {}

    @property
    def name(self) -> str:
        return "ncbi_taxon"

    def _fetch_taxon_data(self, taxon_id: str) -> NcbiTaxonData | None:
        """Fetch taxon data from NCBI, with caching.

        Returns:
            NcbiTaxonData or None if fetch failed
        """
        if taxon_id in self._cache:
            return self._cache[taxon_id]

        try:
            from cmm_ai_automation.strains.ncbi import fetch_ncbi_synonyms

            data = fetch_ncbi_synonyms(taxon_id)
            self._cache[taxon_id] = data
            return data
        except Exception as e:
            logger.warning(f"Failed to fetch NCBI data for {taxon_id}: {e}")
            return None

    def validate(
        self,
        value: str,
        context: dict[str, Any],
        sheet: str,
        row: int,
        field: str,
    ) -> list[ValidationIssue]:
        """Validate an NCBITaxon ID."""
        issues: list[ValidationIssue] = []

        if not value or not value.strip():
            return issues  # Empty is OK, handled by required field checks

        # Parse the ID
        taxon_id = parse_ncbi_taxon_curie(value)
        if taxon_id is None:
            issues.append(
                ValidationIssue(
                    sheet=sheet,
                    row=row,
                    field=field,
                    issue_type=IssueType.INVALID_FORMAT,
                    severity=Severity.ERROR,
                    value=value,
                    message=f"Cannot parse NCBITaxon ID from '{value}'",
                    suggestion="Use format 'NCBITaxon:12345' or plain number",
                )
            )
            return issues

        # Fetch taxon data from NCBI
        data = self._fetch_taxon_data(taxon_id)
        if data is None:
            issues.append(
                ValidationIssue(
                    sheet=sheet,
                    row=row,
                    field=field,
                    issue_type=IssueType.INVALID_ID,
                    severity=Severity.ERROR,
                    value=value,
                    message=f"NCBITaxon:{taxon_id} not found or API error",
                )
            )
            return issues

        # Check rank if required
        if self.check_rank and data.get("rank"):
            actual_rank = data["rank"]
            if actual_rank != self.check_rank:
                issues.append(
                    ValidationIssue(
                        sheet=sheet,
                        row=row,
                        field=field,
                        issue_type=IssueType.FIELD_CONFLICT,
                        severity=Severity.WARNING,
                        value=value,
                        expected=self.check_rank,
                        actual=actual_rank,
                        message=f"NCBITaxon:{taxon_id} has rank '{actual_rank}', expected '{self.check_rank}'",
                        context={"ncbi_data": data},
                    )
                )

        # Cross-check name if present in context
        expected_name = context.get(self.name_field)
        if expected_name and data.get("synonyms"):
            # Check if expected name matches any synonym
            all_names = data.get("synonyms", []) + data.get("equivalent_names", [])
            # Normalize for comparison
            expected_lower = expected_name.lower().strip()
            all_names_lower = [n.lower().strip() for n in all_names]

            if expected_lower not in all_names_lower:
                # Not an exact match - check if it's a substring or close
                # This is informational, not an error
                issues.append(
                    ValidationIssue(
                        sheet=sheet,
                        row=row,
                        field=field,
                        issue_type=IssueType.NAME_MISMATCH,
                        severity=Severity.INFO,
                        value=value,
                        expected=expected_name,
                        actual=", ".join(all_names[:3]),
                        message=f"Name '{expected_name}' not in NCBI synonyms for taxon {taxon_id}",
                        context={"ncbi_synonyms": all_names[:5]},
                    )
                )

        return issues


class NCBITaxonListValidator(ListValidator):
    """Validate semicolon-separated list of NCBITaxon IDs.

    For each ID in the list, checks:
        1. ID is parseable and exists
        2. ID is related to the species_taxon_id (shares same species ancestor)

    Options:
        species_field: Context field containing expected species taxon ID
    """

    def __init__(
        self,
        species_field: str = "species_taxon_id",
        separator: str = ";",
    ):
        """Initialize validator.

        Args:
            species_field: Context field containing expected species taxon ID
            separator: List separator character
        """
        super().__init__(separator=separator)
        self.species_field = species_field
        self._cache: dict[str, NcbiTaxonData] = {}

    @property
    def name(self) -> str:
        return "ncbi_taxon_list"

    def _fetch_taxon_data(self, taxon_id: str) -> NcbiTaxonData | None:
        """Fetch taxon data from NCBI, with caching."""
        if taxon_id in self._cache:
            return self._cache[taxon_id]

        try:
            from cmm_ai_automation.strains.ncbi import fetch_ncbi_synonyms

            data = fetch_ncbi_synonyms(taxon_id)
            self._cache[taxon_id] = data
            return data
        except Exception as e:
            logger.warning(f"Failed to fetch NCBI data for {taxon_id}: {e}")
            return None

    def validate_item(
        self,
        item: str,
        context: dict[str, Any],
        sheet: str,
        row: int,
        field: str,
    ) -> list[ValidationIssue]:
        """Validate a single NCBITaxon ID from the list."""
        issues: list[ValidationIssue] = []

        # Skip non-NCBITaxon items (e.g., "strain:bacdive_12345")
        if not item.startswith("NCBITaxon:") and not item.isdigit():
            return issues

        taxon_id = parse_ncbi_taxon_curie(item)
        if taxon_id is None:
            issues.append(
                ValidationIssue(
                    sheet=sheet,
                    row=row,
                    field=field,
                    issue_type=IssueType.INVALID_FORMAT,
                    severity=Severity.ERROR,
                    value=item,
                    message=f"Cannot parse NCBITaxon ID from '{item}'",
                )
            )
            return issues

        # Fetch taxon data
        data = self._fetch_taxon_data(taxon_id)
        if data is None:
            issues.append(
                ValidationIssue(
                    sheet=sheet,
                    row=row,
                    field=field,
                    issue_type=IssueType.INVALID_ID,
                    severity=Severity.ERROR,
                    value=item,
                    message=f"NCBITaxon:{taxon_id} not found or API error",
                )
            )
            return issues

        # Check if this taxon is related to the expected species
        expected_species = context.get(self.species_field)
        if expected_species:
            expected_species_id = parse_ncbi_taxon_curie(str(expected_species))
            if expected_species_id:
                # Get species ancestor of this taxon
                this_species = data.get("species_taxon_id", "")

                # A taxon is "related" if:
                # 1. Its species_taxon_id matches expected, OR
                # 2. It IS the expected species (rank=species and id matches)
                is_related = this_species == expected_species_id or taxon_id == expected_species_id

                if not is_related and this_species:
                    # This is a BOGUS cross-reference - completely unrelated organism
                    issues.append(
                        ValidationIssue(
                            sheet=sheet,
                            row=row,
                            field=field,
                            issue_type=IssueType.BOGUS_XREF,
                            severity=Severity.ERROR,
                            value=item,
                            expected=f"species_taxon_id={expected_species_id}",
                            actual=f"species_taxon_id={this_species}",
                            message=(
                                f"NCBITaxon:{taxon_id} belongs to species {this_species}, "
                                f"not {expected_species_id} - this is an unrelated organism"
                            ),
                            context={
                                "this_taxon_rank": data.get("rank"),
                                "this_taxon_species": this_species,
                                "expected_species": expected_species_id,
                            },
                        )
                    )
                elif not this_species and data.get("rank") not in ("species", "genus", ""):
                    # No species ancestor found - might be higher taxonomy
                    issues.append(
                        ValidationIssue(
                            sheet=sheet,
                            row=row,
                            field=field,
                            issue_type=IssueType.BOGUS_XREF,
                            severity=Severity.WARNING,
                            value=item,
                            message=(
                                f"NCBITaxon:{taxon_id} has no species-level ancestor "
                                f"(rank={data.get('rank')}) - cannot verify relationship"
                            ),
                            context={"ncbi_data": data},
                        )
                    )

        return issues
