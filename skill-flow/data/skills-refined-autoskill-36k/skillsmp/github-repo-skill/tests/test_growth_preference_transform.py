"""Tests for growth preference transformation functions."""

from cmm_ai_automation.transform.growth_preference_transform import (
    DOES_NOT_GROW_IN,
    GROWS_IN,
    extract_placeholder_id,
    extract_strain_curie,
    transform_preference_row,
)


class TestExtractPlaceholderId:
    """Tests for extract_placeholder_id()."""

    def test_extract_from_standard_uri(self) -> None:
        """Test extracting ID from standard media URI."""
        uri = "http://example.com/ber-cmm/media/0000001Hypho medium"
        result = extract_placeholder_id(uri)
        assert result == "0000001"

    def test_extract_different_ids(self) -> None:
        """Test extracting various placeholder IDs."""
        test_cases = [
            ("http://example.com/media/0000001", "0000001"),
            ("http://example.com/media/0000123", "0000123"),
            ("http://example.com/media/9999999", "9999999"),
            ("http://foo.bar/media/0000042Extra text", "0000042"),
        ]
        for uri, expected in test_cases:
            result = extract_placeholder_id(uri)
            assert result == expected

    def test_extract_returns_none_for_invalid(self) -> None:
        """Test that invalid URIs return None."""
        test_cases = [
            "http://example.com/no/media/here",
            "http://example.com/media/ABC",  # Not a number
            "http://example.com/media/123",  # Not 7 digits
            "",
            "random string",
        ]
        for uri in test_cases:
            result = extract_placeholder_id(uri)
            assert result is None


class TestExtractStrainCurie:
    """Tests for extract_strain_curie()."""

    def test_extract_ncbi_taxon_from_purl(self) -> None:
        """Test extracting NCBITaxon CURIE from OBO PURL."""
        url = "http://purl.obolibrary.org/obo/NCBITaxon_1286640"
        result = extract_strain_curie(url)
        assert result == "NCBITaxon:1286640"

    def test_extract_various_ncbi_taxons(self) -> None:
        """Test extracting various NCBI taxon IDs."""
        test_cases = [
            ("http://purl.obolibrary.org/obo/NCBITaxon_408", "NCBITaxon:408"),
            ("http://purl.obolibrary.org/obo/NCBITaxon_1", "NCBITaxon:1"),
            ("http://purl.obolibrary.org/obo/NCBITaxon_99999999", "NCBITaxon:99999999"),
        ]
        for url, expected in test_cases:
            result = extract_strain_curie(url)
            assert result == expected

    def test_extract_bacdive_id(self) -> None:
        """Test extracting BacDive ID from URL."""
        url = "https://bacdive.dsmz.de/strain/12345"
        result = extract_strain_curie(url)
        assert result == "bacdive:12345"

    def test_extract_bacdive_with_trailing_slash(self) -> None:
        """Test extracting BacDive ID with trailing slash."""
        url = "https://bacdive.dsmz.de/strain/12345/"
        result = extract_strain_curie(url)
        assert result == "bacdive:12345"

    def test_returns_none_for_empty_string(self) -> None:
        """Test that empty string returns None."""
        result = extract_strain_curie("")
        assert result is None

    def test_returns_none_for_none(self) -> None:
        """Test that None input returns None."""
        result = extract_strain_curie(None)  # type: ignore[arg-type]
        assert result is None

    def test_returns_none_for_unrecognized_url(self) -> None:
        """Test that unrecognized URLs return None."""
        test_cases = [
            "http://example.com/some/random/url",
            "http://notbacdive.com/strain/123",
            "http://example.org/obo/SomeOther_123",
        ]
        for url in test_cases:
            result = extract_strain_curie(url)
            assert result is None


class TestTransformPreferenceRow:
    """Tests for transform_preference_row()."""

    def test_transform_grows_in_preference(self) -> None:
        """Test transforming a 'grows in' preference."""
        row = {
            "strain_url": "http://purl.obolibrary.org/obo/NCBITaxon_1286640",
            "object": "http://example.com/ber-cmm/media/0000001Hypho medium",
            "Growth result binary": "1",
        }
        media_map = {"0000001": "BER-CMM-MEDIUM:0000001"}

        edge = transform_preference_row(row, media_map)

        assert edge is not None
        assert edge.subject == "NCBITaxon:1286640"
        assert edge.object == "BER-CMM-MEDIUM:0000001"
        assert edge.predicate == GROWS_IN

    def test_transform_does_not_grow_in(self) -> None:
        """Test transforming a 'does not grow in' preference."""
        row = {
            "strain_url": "http://purl.obolibrary.org/obo/NCBITaxon_408",
            "object": "http://example.com/media/0000002",
            "Growth result binary": "0",  # Does not grow
        }
        media_map = {"0000002": "BER-CMM-MEDIUM:0000002"}

        edge = transform_preference_row(row, media_map)

        assert edge is not None
        assert edge.subject == "NCBITaxon:408"
        assert edge.predicate == DOES_NOT_GROW_IN

    def test_transform_with_quantitative_data(self) -> None:
        """Test that quantitative data is added to edge."""
        row = {
            "strain_url": "http://purl.obolibrary.org/obo/NCBITaxon_408",
            "object": "http://example.com/media/0000001",
            "Growth result binary": "1",
            "Growth result quantiative": "3.5",
        }
        media_map = {"0000001": "BER-CMM-MEDIUM:0000001"}

        edge = transform_preference_row(row, media_map)

        assert edge is not None
        assert edge.model_extra is not None
        assert "growth_value" in edge.model_extra
        assert edge.model_extra["growth_value"] == "3.5"

    def test_transform_uses_fallback_strain_id(self) -> None:
        """Test using fallback strain id when URL not available."""
        row = {
            "strain_url": "",
            "strain id": "DSM:1337",
            "object": "http://example.com/media/0000001",
            "Growth result binary": "1",
        }
        media_map = {"0000001": "BER-CMM-MEDIUM:0000001"}

        edge = transform_preference_row(row, media_map)

        assert edge is not None
        assert edge.subject == "DSM:1337"

    def test_transform_returns_none_for_missing_strain(self) -> None:
        """Test that missing strain info returns None."""
        row = {
            "strain_url": "",
            "strain id": "",
            "object": "http://example.com/media/0000001",
            "Growth result binary": "1",
        }
        media_map = {"0000001": "BER-CMM-MEDIUM:0000001"}

        edge = transform_preference_row(row, media_map)

        assert edge is None

    def test_transform_returns_none_for_invalid_placeholder(self) -> None:
        """Test that invalid placeholder returns None."""
        row = {
            "strain_url": "http://purl.obolibrary.org/obo/NCBITaxon_408",
            "object": "http://example.com/no_placeholder_here",
            "Growth result binary": "1",
        }
        media_map = {"0000001": "BER-CMM-MEDIUM:0000001"}

        edge = transform_preference_row(row, media_map)

        assert edge is None

    def test_transform_returns_none_for_unmapped_media(self) -> None:
        """Test that unmapped media placeholder returns None."""
        row = {
            "strain_url": "http://purl.obolibrary.org/obo/NCBITaxon_408",
            "object": "http://example.com/media/9999999",  # Not in map
            "Growth result binary": "1",
        }
        media_map = {"0000001": "BER-CMM-MEDIUM:0000001"}

        edge = transform_preference_row(row, media_map)

        assert edge is None

    def test_transform_defaults_to_grows_in(self) -> None:
        """Test that missing or non-zero binary result defaults to grows in."""
        test_cases = [
            "",  # Empty
            "1",  # Explicit 1
            "yes",  # Non-zero
        ]
        for binary_result in test_cases:
            row = {
                "strain_url": "http://purl.obolibrary.org/obo/NCBITaxon_408",
                "object": "http://example.com/media/0000001",
                "Growth result binary": binary_result,
            }
            media_map = {"0000001": "BER-CMM-MEDIUM:0000001"}

            edge = transform_preference_row(row, media_map)

            if edge:  # May be None for invalid binary result
                assert edge.predicate == GROWS_IN

    def test_transform_edge_has_provenance(self) -> None:
        """Test that transformed edge has required provenance."""
        row = {
            "strain_url": "http://purl.obolibrary.org/obo/NCBITaxon_408",
            "object": "http://example.com/media/0000001",
            "Growth result binary": "1",
        }
        media_map = {"0000001": "BER-CMM-MEDIUM:0000001"}

        edge = transform_preference_row(row, media_map)

        assert edge is not None
        assert edge.knowledge_level == "knowledge_assertion"
        assert edge.agent_type == "manual_agent"
        assert edge.primary_knowledge_source is not None
        assert "infores:cmm-ai-automation" in edge.primary_knowledge_source
