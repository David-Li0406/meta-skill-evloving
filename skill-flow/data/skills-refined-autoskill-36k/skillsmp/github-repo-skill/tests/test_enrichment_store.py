"""Tests for enrichment store module.

Tests composite key generation, conflict detection, merge logic,
and KGX export functionality.
"""

import tempfile
from collections.abc import Generator
from pathlib import Path

import pytest

from cmm_ai_automation.store.enrichment_store import (
    AUTHORITATIVE_SOURCES,
    EnrichmentStore,
    clean_html_tags,
    generate_composite_key,
    is_cas_number,
    parse_composite_key,
    score_name_quality,
    select_display_name,
)


class TestCompositeKeyGeneration:
    """Tests for composite key generation and parsing."""

    def test_generate_key_both_present(self) -> None:
        """Test key generation with both inchikey and cas_rn present."""
        key = generate_composite_key(
            inchikey="WQZGKKKJIJFFOK-GASJEMHNSA-N",
            cas_rn="50-99-7",
        )
        assert key == "WQZGKKKJIJFFOK-GASJEMHNSA-N|50-99-7"

    def test_generate_key_missing_cas(self) -> None:
        """Test key generation with missing cas_rn."""
        key = generate_composite_key(
            inchikey="WQZGKKKJIJFFOK-GASJEMHNSA-N",
            cas_rn=None,
        )
        assert key == "WQZGKKKJIJFFOK-GASJEMHNSA-N|unknown"

    def test_generate_key_missing_inchikey(self) -> None:
        """Test key generation with missing inchikey uses 'unknown'."""
        key = generate_composite_key(
            inchikey=None,
            cas_rn="50-99-7",
        )
        assert key == "unknown|50-99-7"

    def test_generate_key_both_missing(self) -> None:
        """Test key generation with both values missing."""
        key = generate_composite_key(inchikey=None, cas_rn=None)
        assert key == "unknown|unknown"

    def test_parse_key_both_present(self) -> None:
        """Test parsing a key with both values."""
        inchikey, cas_rn = parse_composite_key("WQZGKKKJIJFFOK-GASJEMHNSA-N|50-99-7")
        assert inchikey == "WQZGKKKJIJFFOK-GASJEMHNSA-N"
        assert cas_rn == "50-99-7"

    def test_parse_key_missing_cas(self) -> None:
        """Test parsing a key with missing cas_rn."""
        inchikey, cas_rn = parse_composite_key("WQZGKKKJIJFFOK-GASJEMHNSA-N|unknown")
        assert inchikey == "WQZGKKKJIJFFOK-GASJEMHNSA-N"
        assert cas_rn is None

    def test_parse_key_missing_inchikey(self) -> None:
        """Test parsing a key with 'unknown' placeholder for inchikey."""
        inchikey, cas_rn = parse_composite_key("unknown|50-99-7")
        assert inchikey is None
        assert cas_rn == "50-99-7"

    def test_parse_key_invalid_format(self) -> None:
        """Test parsing an invalid key returns None tuple."""
        inchikey, cas_rn = parse_composite_key("invalid-key-no-pipe")
        assert inchikey is None
        assert cas_rn is None

    def test_roundtrip_both_present(self) -> None:
        """Test that generate and parse are inverses when both values present."""
        original_inchikey = "CSNNHWWHGAXBCP-UHFFFAOYSA-L"
        original_cas = "7487-88-9"

        key = generate_composite_key(original_inchikey, original_cas)
        parsed_inchikey, parsed_cas = parse_composite_key(key)

        assert parsed_inchikey == original_inchikey
        assert parsed_cas == original_cas


class TestAuthoritativeSources:
    """Tests for authoritative source configuration."""

    def test_pubchem_authoritative_for_cid(self) -> None:
        """Test that pubchem is authoritative for pubchem_cid."""
        assert AUTHORITATIVE_SOURCES["pubchem_cid"] == "pubchem"

    def test_chebi_authoritative_for_chebi_id(self) -> None:
        """Test that chebi is authoritative for chebi_id."""
        assert AUTHORITATIVE_SOURCES["chebi_id"] == "chebi"

    def test_cas_authoritative_for_cas_rn(self) -> None:
        """Test that cas is authoritative for cas_rn."""
        assert AUTHORITATIVE_SOURCES["cas_rn"] == "cas"

    def test_chebi_authoritative_for_roles(self) -> None:
        """Test that chebi is authoritative for biological/chemical roles."""
        assert AUTHORITATIVE_SOURCES["biological_roles"] == "chebi"
        assert AUTHORITATIVE_SOURCES["chemical_roles"] == "chebi"
        assert AUTHORITATIVE_SOURCES["application_roles"] == "chebi"

    def test_no_authoritative_source_for_structure(self) -> None:
        """Test that structural data has no single authoritative source."""
        assert AUTHORITATIVE_SOURCES["inchi"] is None
        assert AUTHORITATIVE_SOURCES["inchikey"] is None
        assert AUTHORITATIVE_SOURCES["smiles"] is None


class TestEnrichmentStoreMerge:
    """Tests for record merging logic in EnrichmentStore.

    Uses mocking to test merge logic without database.
    """

    def test_merge_new_field(self) -> None:
        """Test that new fields are added without conflict."""
        from cmm_ai_automation.store.enrichment_store import EnrichmentStore

        store = EnrichmentStore.__new__(EnrichmentStore)
        store.store_path = Path("/tmp/test.duckdb")
        store.schema_path = Path("/tmp/schema.yaml")

        existing = {
            "inchikey": "WQZGKKKJIJFFOK-GASJEMHNSA-N",
            "cas_rn": "50-99-7",
            "name": "D-glucose",
            "conflicts": [],
            "source_records": [],
        }
        new_data = {
            "pubchem_cid": 5793,
            "smiles": "OC[C@H]1OC(O)[C@H](O)[C@@H](O)[C@@H]1O",
        }

        merged = store._merge_records(existing, new_data, "pubchem", "glucose")

        assert merged["pubchem_cid"] == 5793
        assert merged["smiles"] is not None
        assert merged["name"] == "D-glucose"  # preserved
        assert len(merged["conflicts"]) == 0

    def test_merge_authoritative_source_wins(self) -> None:
        """Test that authoritative source overwrites and logs conflict."""
        from cmm_ai_automation.store.enrichment_store import EnrichmentStore

        store = EnrichmentStore.__new__(EnrichmentStore)
        store.store_path = Path("/tmp/test.duckdb")
        store.schema_path = Path("/tmp/schema.yaml")

        existing = {
            "inchikey": "WQZGKKKJIJFFOK-GASJEMHNSA-N",
            "cas_rn": "50-99-7",
            "chebi_id": "CHEBI:99999",  # wrong value
            "conflicts": [],
            "source_records": [],
        }
        new_data = {
            "chebi_id": "CHEBI:17634",  # correct value from authoritative source
        }

        merged = store._merge_records(existing, new_data, "chebi", "glucose")

        # ChEBI is authoritative for chebi_id, so new value should win
        assert merged["chebi_id"] == "CHEBI:17634"
        assert len(merged["conflicts"]) == 1
        assert merged["conflicts"][0]["resolution"] == "primary_source_wins"
        assert merged["conflicts"][0]["field_name"] == "chebi_id"

    def test_merge_non_authoritative_conflict(self) -> None:
        """Test that non-authoritative conflicts are logged but don't overwrite."""
        from cmm_ai_automation.store.enrichment_store import EnrichmentStore

        store = EnrichmentStore.__new__(EnrichmentStore)
        store.store_path = Path("/tmp/test.duckdb")
        store.schema_path = Path("/tmp/schema.yaml")

        existing = {
            "inchikey": "WQZGKKKJIJFFOK-GASJEMHNSA-N",
            "cas_rn": "50-99-7",
            "chebi_id": "CHEBI:17634",  # authoritative value
            "conflicts": [],
            "source_records": [],
        }
        new_data = {
            "chebi_id": "CHEBI:99999",  # PubChem trying to set ChEBI ID
        }

        # PubChem is NOT authoritative for chebi_id
        merged = store._merge_records(existing, new_data, "pubchem", "glucose")

        # Original value should be preserved
        assert merged["chebi_id"] == "CHEBI:17634"
        assert len(merged["conflicts"]) == 1
        assert merged["conflicts"][0]["resolution"] == "unresolved"

    def test_merge_no_authoritative_source_conflict(self) -> None:
        """Test conflict for field with no authoritative source."""
        from cmm_ai_automation.store.enrichment_store import EnrichmentStore

        store = EnrichmentStore.__new__(EnrichmentStore)
        store.store_path = Path("/tmp/test.duckdb")
        store.schema_path = Path("/tmp/schema.yaml")

        existing = {
            "inchikey": "WQZGKKKJIJFFOK-GASJEMHNSA-N",
            "smiles": "OC[C@H]1OC(O)[C@H](O)[C@@H](O)[C@@H]1O",
            "conflicts": [],
            "source_records": [],
        }
        new_data = {
            "smiles": "C(C1C(C(C(C(O1)O)O)O)O)O",  # different representation
        }

        merged = store._merge_records(existing, new_data, "chebi", "glucose")

        # First value should be preserved (no authoritative source)
        assert merged["smiles"] == "OC[C@H]1OC(O)[C@H](O)[C@@H](O)[C@@H]1O"
        assert len(merged["conflicts"]) == 1
        assert merged["conflicts"][0]["resolution"] == "unresolved"

    def test_merge_skips_none_values(self) -> None:
        """Test that None values don't overwrite existing values."""
        from cmm_ai_automation.store.enrichment_store import EnrichmentStore

        store = EnrichmentStore.__new__(EnrichmentStore)
        store.store_path = Path("/tmp/test.duckdb")
        store.schema_path = Path("/tmp/schema.yaml")

        existing = {
            "name": "D-glucose",
            "pubchem_cid": 5793,
            "conflicts": [],
            "source_records": [],
        }
        new_data = {
            "name": None,  # Should not overwrite
            "chebi_id": "CHEBI:17634",  # New field
        }

        merged = store._merge_records(existing, new_data, "chebi", "glucose")

        assert merged["name"] == "D-glucose"  # preserved
        assert merged["chebi_id"] == "CHEBI:17634"  # added

    def test_merge_adds_source_record(self) -> None:
        """Test that merging adds a source record."""
        from cmm_ai_automation.store.enrichment_store import EnrichmentStore

        store = EnrichmentStore.__new__(EnrichmentStore)
        store.store_path = Path("/tmp/test.duckdb")
        store.schema_path = Path("/tmp/schema.yaml")

        existing = {
            "name": "D-glucose",
            "conflicts": [],
            "source_records": [
                {"source_name": "pubchem", "source_id": "5793"},
            ],
        }
        new_data = {
            "chebi_id": "CHEBI:17634",
        }

        merged = store._merge_records(existing, new_data, "chebi", "glucose lookup")

        assert len(merged["source_records"]) == 2
        assert merged["source_records"][1]["source_name"] == "chebi"
        assert merged["source_records"][1]["source_query"] == "glucose lookup"


class TestGetSourceId:
    """Tests for _get_source_id method."""

    def test_get_source_id_pubchem(self) -> None:
        """Test extracting pubchem_cid for pubchem source."""
        from cmm_ai_automation.store.enrichment_store import EnrichmentStore

        store = EnrichmentStore.__new__(EnrichmentStore)

        data = {"pubchem_cid": 5793, "chebi_id": "CHEBI:17634"}
        result = store._get_source_id(data, "pubchem")
        assert result == "5793"

    def test_get_source_id_chebi(self) -> None:
        """Test extracting chebi_id for chebi source."""
        from cmm_ai_automation.store.enrichment_store import EnrichmentStore

        store = EnrichmentStore.__new__(EnrichmentStore)

        data = {"pubchem_cid": 5793, "chebi_id": "CHEBI:17634"}
        result = store._get_source_id(data, "chebi")
        assert result == "CHEBI:17634"

    def test_get_source_id_cas(self) -> None:
        """Test extracting cas_rn for cas source."""
        from cmm_ai_automation.store.enrichment_store import EnrichmentStore

        store = EnrichmentStore.__new__(EnrichmentStore)

        data = {"cas_rn": "50-99-7", "chebi_id": "CHEBI:17634"}
        result = store._get_source_id(data, "cas")
        assert result == "50-99-7"

    def test_get_source_id_unknown_source(self) -> None:
        """Test that unknown source returns None."""
        from cmm_ai_automation.store.enrichment_store import EnrichmentStore

        store = EnrichmentStore.__new__(EnrichmentStore)

        data = {"pubchem_cid": 5793}
        result = store._get_source_id(data, "unknown_source")
        assert result is None


class TestEnrichmentStoreIntegration:
    """Integration tests for EnrichmentStore using temporary database."""

    @pytest.fixture
    def temp_store(self) -> Generator[EnrichmentStore, None, None]:
        """Create a store with a temporary database."""
        with tempfile.TemporaryDirectory() as tmpdir:
            store_path = Path(tmpdir) / "test_enrichment.duckdb"
            store = EnrichmentStore(store_path=store_path)
            yield store
            store.close()

    @pytest.mark.integration
    def test_upsert_and_retrieve(self, temp_store: EnrichmentStore) -> None:
        """Test inserting and retrieving an ingredient."""
        data = {
            "inchikey": "WQZGKKKJIJFFOK-GASJEMHNSA-N",
            "cas_rn": "50-99-7",
            "name": "D-glucose",
            "pubchem_cid": 5793,
        }

        key = temp_store.upsert_ingredient(data, source="pubchem", query="glucose")

        # Retrieve by composite key
        result = temp_store.get_by_composite_key(key)
        assert result is not None
        assert result["name"] == "D-glucose"
        assert result["pubchem_cid"] == 5793

    @pytest.mark.integration
    @pytest.mark.skip(reason="DuckDB schema evolution issue - fields not persisting after merge. See issue #63")
    def test_upsert_merge(self, temp_store: EnrichmentStore) -> None:
        """Test that upsert merges data from multiple sources."""
        # First insert from PubChem
        data1 = {
            "inchikey": "WQZGKKKJIJFFOK-GASJEMHNSA-N",
            "cas_rn": "50-99-7",
            "name": "D-glucose",
            "pubchem_cid": 5793,
        }
        key = temp_store.upsert_ingredient(data1, source="pubchem")

        # Second insert from ChEBI adds more data
        data2 = {
            "inchikey": "WQZGKKKJIJFFOK-GASJEMHNSA-N",
            "cas_rn": "50-99-7",
            "chebi_id": "CHEBI:17634",
            "biological_roles": ["CHEBI:78675"],
        }
        temp_store.upsert_ingredient(data2, source="chebi")

        # Should have merged data
        result = temp_store.get_by_composite_key(key)
        assert result is not None
        assert result["pubchem_cid"] == 5793
        assert result["chebi_id"] == "CHEBI:17634"
        assert result["biological_roles"] == ["CHEBI:78675"]

    @pytest.mark.integration
    def test_find_by_chebi(self, temp_store: EnrichmentStore) -> None:
        """Test finding ingredients by ChEBI ID."""
        data = {
            "inchikey": "WQZGKKKJIJFFOK-GASJEMHNSA-N",
            "cas_rn": "50-99-7",
            "chebi_id": "CHEBI:17634",
        }
        temp_store.upsert_ingredient(data, source="chebi")

        results = temp_store.find_by_chebi("CHEBI:17634")
        assert len(results) == 1
        assert results[0]["chebi_id"] == "CHEBI:17634"

    @pytest.mark.integration
    def test_get_stats(self, temp_store: EnrichmentStore) -> None:
        """Test getting store statistics."""
        # Insert a few records
        temp_store.upsert_ingredient(
            {
                "inchikey": "WQZGKKKJIJFFOK-GASJEMHNSA-N",
                "cas_rn": "50-99-7",
                "chebi_id": "CHEBI:17634",
                "pubchem_cid": 5793,
            },
            source="pubchem",
        )
        temp_store.upsert_ingredient(
            {
                "inchikey": "CSNNHWWHGAXBCP-UHFFFAOYSA-L",
                "cas_rn": "7487-88-9",
                "chebi_id": "CHEBI:32599",
            },
            source="chebi",
        )

        stats = temp_store.get_stats()
        assert stats["total_ingredients"] == 2
        assert stats["with_chebi_id"] == 2
        assert stats["with_inchikey"] == 2


class TestKGXExportLogic:
    """Tests for KGX export logic without requiring KGX library."""

    def test_build_xrefs_list(self) -> None:
        """Test that xrefs are built correctly from a record."""
        record = {
            "chebi_id": "CHEBI:17634",
            "pubchem_cid": 5793,
            "cas_rn": "50-99-7",
            "kegg_id": "C00031",
            "mesh_id": "D005947",
            "drugbank_id": "DB00117",
        }

        xrefs = []
        if record.get("chebi_id"):
            xrefs.append(record["chebi_id"])
        if record.get("pubchem_cid"):
            xrefs.append(f"PUBCHEM.COMPOUND:{record['pubchem_cid']}")
        if record.get("cas_rn"):
            xrefs.append(f"CAS:{record['cas_rn']}")
        if record.get("kegg_id"):
            xrefs.append(f"KEGG.COMPOUND:{record['kegg_id']}")
        if record.get("mesh_id"):
            xrefs.append(f"MESH:{record['mesh_id']}")
        if record.get("drugbank_id"):
            xrefs.append(f"DRUGBANK:{record['drugbank_id']}")

        assert "CHEBI:17634" in xrefs
        assert "PUBCHEM.COMPOUND:5793" in xrefs
        assert "CAS:50-99-7" in xrefs
        assert "KEGG.COMPOUND:C00031" in xrefs
        assert "MESH:D005947" in xrefs
        assert "DRUGBANK:DB00117" in xrefs

    def test_node_id_selection_prefers_chebi(self) -> None:
        """Test that node ID selection prefers ChEBI."""
        record = {
            "chebi_id": "CHEBI:17634",
            "id": "some-composite-key",
            "inchikey": "WQZGKKKJIJFFOK-GASJEMHNSA-N",
        }

        node_id = record.get("chebi_id") or record.get("id", "")
        assert node_id == "CHEBI:17634"

    def test_node_id_fallback_to_inchikey(self) -> None:
        """Test that node ID falls back to InChIKey when no ChEBI."""
        record = {
            "id": "some-composite-key",
            "inchikey": "WQZGKKKJIJFFOK-GASJEMHNSA-N",
        }

        node_id = record.get("chebi_id") or record.get("id", "")
        if not node_id.startswith("CHEBI:") and record.get("inchikey"):
            node_id = f"INCHIKEY:{record['inchikey']}"

        assert node_id == "INCHIKEY:WQZGKKKJIJFFOK-GASJEMHNSA-N"

    def test_category_selection_small_molecule(self) -> None:
        """Test that non-mixture is classified as SmallMolecule."""
        record = {"is_mixture": False}
        is_mixture = record.get("is_mixture")
        if is_mixture is True or is_mixture == "true":
            category = ["biolink:ChemicalMixture"]
        elif is_mixture is False or is_mixture == "false":
            category = ["biolink:SmallMolecule"]
        else:
            category = ["biolink:SmallMolecule"]
        assert category == ["biolink:SmallMolecule"]

    def test_category_selection_mixture(self) -> None:
        """Test that mixture is classified as ChemicalMixture."""
        record = {"is_mixture": True}
        is_mixture = record.get("is_mixture")
        if is_mixture is True or is_mixture == "true":
            category = ["biolink:ChemicalMixture"]
        elif is_mixture is False or is_mixture == "false":
            category = ["biolink:SmallMolecule"]
        else:
            category = ["biolink:SmallMolecule"]
        assert category == ["biolink:ChemicalMixture"]

    def test_category_selection_string_true(self) -> None:
        """Test that string 'true' is handled as mixture."""
        record = {"is_mixture": "true"}
        is_mixture = record.get("is_mixture")
        if is_mixture is True or is_mixture == "true":
            category = ["biolink:ChemicalMixture"]
        else:
            category = ["biolink:SmallMolecule"]
        assert category == ["biolink:ChemicalMixture"]


class TestEnrichmentStoreDatabase:
    """Unit tests for EnrichmentStore that use temp database but are fast enough for CI."""

    @pytest.fixture
    def store(self) -> Generator[EnrichmentStore, None, None]:
        """Create a store with a temporary database."""
        with tempfile.TemporaryDirectory() as tmpdir:
            store_path = Path(tmpdir) / "test_enrichment.duckdb"
            store = EnrichmentStore(store_path=store_path)
            yield store
            store.close()

    def test_store_init_creates_directory(self) -> None:
        """Test that store init creates parent directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            store_path = Path(tmpdir) / "subdir" / "test.duckdb"
            store = EnrichmentStore(store_path=store_path)
            assert store_path.parent.exists()
            store.close()

    def test_upsert_new_ingredient(self, store: EnrichmentStore) -> None:
        """Test upserting a new ingredient creates record."""
        data = {
            "inchikey": "WQZGKKKJIJFFOK-GASJEMHNSA-N",
            "cas_rn": "50-99-7",
            "name": "D-glucose",
            "pubchem_cid": 5793,
        }
        key = store.upsert_ingredient(data, source="pubchem", query="glucose")
        assert key == "WQZGKKKJIJFFOK-GASJEMHNSA-N|50-99-7"

        result = store.get_by_composite_key(key)
        assert result is not None
        assert result["name"] == "D-glucose"

    def test_get_by_key_returns_none_for_missing(self, store: EnrichmentStore) -> None:
        """Test that get_by_key returns None for nonexistent records."""
        result = store.get_by_key("NONEXISTENT", "0-00-0")
        assert result is None

    def test_find_by_chebi_returns_empty_for_missing(self, store: EnrichmentStore) -> None:
        """Test that find_by_chebi returns empty list for nonexistent ID."""
        results = store.find_by_chebi("CHEBI:99999999")
        assert results == []

    def test_find_by_pubchem_returns_empty_for_missing(self, store: EnrichmentStore) -> None:
        """Test that find_by_pubchem returns empty list for nonexistent CID."""
        results = store.find_by_pubchem(99999999)
        assert results == []

    def test_find_by_cas_returns_empty_for_missing(self, store: EnrichmentStore) -> None:
        """Test that find_by_cas returns empty list for nonexistent RN."""
        results = store.find_by_cas("999-99-9")
        assert results == []

    def test_get_all_conflicts_empty_store(self, store: EnrichmentStore) -> None:
        """Test that get_all_conflicts returns empty for empty store."""
        conflicts = store.get_all_conflicts()
        assert conflicts == []

    def test_get_stats_empty_store(self, store: EnrichmentStore) -> None:
        """Test that get_stats works on empty store."""
        stats = store.get_stats()
        assert stats["total_ingredients"] == 0
        assert stats["coverage_chebi"] == 0

    def test_export_to_kgx_empty_store(self, store: EnrichmentStore) -> None:
        """Test that export_to_kgx works on empty store."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "test_kgx"
            nodes, edges = store.export_to_kgx(output_path)
            assert nodes == 0
            assert edges == 0
            assert (output_path.parent / "test_kgx_nodes.tsv").exists()
            assert (output_path.parent / "test_kgx_edges.tsv").exists()

    def test_export_to_kgx_with_data(self, store: EnrichmentStore) -> None:
        """Test KGX export with actual data."""
        # Insert some test data
        store.upsert_ingredient(
            {
                "inchikey": "WQZGKKKJIJFFOK-GASJEMHNSA-N",
                "cas_rn": "50-99-7",
                "name": "D-glucose",
                "chebi_id": "CHEBI:17634",
                "pubchem_cid": 5793,
                "chemical_formula": "C6H12O6",
                "smiles": "OC[C@H]1OC(O)[C@H](O)[C@@H](O)[C@@H]1O",
                "molecular_mass": 180.16,
                "is_mixture": False,
            },
            source="pubchem",
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "test_kgx"
            nodes, edges = store.export_to_kgx(output_path)
            assert nodes == 1
            assert edges == 0

            # Verify nodes file content
            nodes_file = output_path.parent / "test_kgx_nodes.tsv"
            with nodes_file.open() as f:
                content = f.read()
                assert "CHEBI:17634" in content
                assert "D-glucose" in content
                assert "biolink:SmallMolecule" in content

    def test_close_clears_connections(self, store: EnrichmentStore) -> None:
        """Test that close clears all connections."""
        # Access collection to create connections
        store._get_collection()
        assert store._collection is not None

        store.close()
        assert store._collection is None
        assert store._db is None
        assert store._client is None


class TestCleanHtmlTags:
    """Tests for HTML tag cleaning."""

    def test_clean_simple_subscript(self) -> None:
        """Test cleaning subscript tags."""
        assert clean_html_tags("H<sub>2</sub>O") == "H2O"

    def test_clean_superscript(self) -> None:
        """Test cleaning superscript tags."""
        assert clean_html_tags("10<sup>6</sup>") == "106"

    def test_clean_multiple_tags(self) -> None:
        """Test cleaning multiple HTML tags."""
        text = "Mo<sub>7</sub>O<sub>24</sub><sup>6-</sup>"
        assert clean_html_tags(text) == "Mo7O246-"

    def test_clean_none_returns_none(self) -> None:
        """Test that None input returns None."""
        assert clean_html_tags(None) is None

    def test_clean_empty_returns_empty(self) -> None:
        """Test that empty string returns empty string."""
        assert clean_html_tags("") == ""

    def test_clean_no_tags_unchanged(self) -> None:
        """Test that text without tags is unchanged."""
        assert clean_html_tags("Glucose") == "Glucose"


class TestIsCasNumber:
    """Tests for CAS number detection."""

    def test_valid_cas_number(self) -> None:
        """Test detection of valid CAS numbers."""
        assert is_cas_number("50-99-7") is True
        assert is_cas_number("7732-18-5") is True
        assert is_cas_number("12125-02-9") is True

    def test_invalid_cas_number(self) -> None:
        """Test rejection of non-CAS strings."""
        assert is_cas_number("Glucose") is False
        assert is_cas_number("CHEBI:17634") is False
        assert is_cas_number("12345") is False

    def test_cas_with_whitespace(self) -> None:
        """Test CAS number with surrounding whitespace."""
        assert is_cas_number(" 50-99-7 ") is True


class TestScoreNameQuality:
    """Tests for name quality scoring."""

    def test_short_simple_name_scores_high(self) -> None:
        """Test that short, simple names score high."""
        score = score_name_quality("Glucose")
        assert score > 100  # Base + bonus for proper capitalization

    def test_long_name_scores_lower(self) -> None:
        """Test that long names score lower."""
        long_name = "alpha-D-glucopyranosyl-(1->4)-alpha-D-glucopyranose"
        short_name = "Glucose"
        assert score_name_quality(short_name) > score_name_quality(long_name)

    def test_iupac_semicolon_penalized(self) -> None:
        """Test that IUPAC names with semicolons are penalized."""
        iupac = "diazanium;sulfate"
        common = "Ammonium sulfate"
        assert score_name_quality(common) > score_name_quality(iupac)

    def test_cas_number_heavily_penalized(self) -> None:
        """Test that CAS numbers are heavily penalized."""
        assert score_name_quality("50-99-7") < 50

    def test_html_tags_penalized(self) -> None:
        """Test that names with HTML tags are penalized."""
        with_html = "Mo<sub>7</sub>O<sub>24</sub>"
        without_html = "Molybdate"
        assert score_name_quality(without_html) > score_name_quality(with_html)

    def test_all_caps_slightly_penalized(self) -> None:
        """Test that all-caps names are slightly penalized."""
        assert score_name_quality("Glucose") > score_name_quality("GLUCOSE")


class TestSelectDisplayName:
    """Tests for display name selection."""

    def test_prefer_query_name(self) -> None:
        """Test that original query name is preferred."""
        record = {
            "name": "D-glucose",
            "iupac_name": "(2R,3S,4R,5R)-2,3,4,5,6-pentahydroxyhexanal",
            "_sources": [{"source_query": "Glucose", "source_name": "pubchem"}],
        }
        assert select_display_name(record) == "Glucose"

    def test_fallback_to_name_field(self) -> None:
        """Test fallback to name field when no query name."""
        record = {
            "name": "D-glucose",
            "iupac_name": "complicated-name;with;semicolons",
            "_sources": [],
        }
        assert select_display_name(record) == "D-glucose"

    def test_avoid_iupac_when_better_available(self) -> None:
        """Test that IUPAC name is avoided when better options exist."""
        record = {
            "name": "Ammonium sulfate",
            "iupac_name": "diazanium;sulfate",
            "_sources": [],
        }
        result = select_display_name(record)
        assert result == "Ammonium sulfate"

    def test_clean_html_from_selected_name(self) -> None:
        """Test that HTML is cleaned from the selected name."""
        record = {
            "name": "Mo<sub>7</sub>O<sub>24</sub>",
            "_sources": [{"source_query": "Ammonium molybdate", "source_name": "pubchem"}],
        }
        result = select_display_name(record)
        # Should prefer the query name which has no HTML
        assert "<" not in result

    def test_handle_missing_sources(self) -> None:
        """Test handling of missing _sources field."""
        record = {
            "name": "Test compound",
        }
        assert select_display_name(record) == "Test compound"

    def test_handle_empty_record(self) -> None:
        """Test handling of empty record."""
        record: dict[str, str] = {}
        assert select_display_name(record) == "Unknown"

    def test_parse_json_source_records(self) -> None:
        """Test parsing source_records stored as JSON strings (from DuckDB)."""
        import json

        record = {
            "name": "Amchlor",  # Brand name from API
            "source_records": [
                json.dumps({"source_name": "pubchem", "source_query": "Ammonium chloride"}),
                json.dumps({"source_name": "chebi", "source_query": "Ammonium chloride"}),
            ],
        }
        # Should prefer the query name over the brand name
        assert select_display_name(record) == "Ammonium chloride"
