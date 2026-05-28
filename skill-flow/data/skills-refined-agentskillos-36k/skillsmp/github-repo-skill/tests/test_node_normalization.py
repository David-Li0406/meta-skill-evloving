"""Tests for NodeNormalization client."""

import pytest

from cmm_ai_automation.clients.node_normalization import (
    NodeNormalizationClient,
    NormalizationError,
    NormalizedNode,
)


class TestNodeNormalizationClient:
    """Tests for NodeNormalizationClient."""

    @pytest.fixture
    def client(self) -> NodeNormalizationClient:
        """Create a NodeNormalization client for testing."""
        return NodeNormalizationClient()

    @pytest.mark.integration
    def test_normalize_chebi(self, client: NodeNormalizationClient) -> None:
        """Test normalizing a ChEBI ID (glucose)."""
        result = client.normalize("CHEBI:17634")

        assert isinstance(result, NormalizedNode)
        assert result.query_id == "CHEBI:17634"
        assert "CHEBI" in result.equivalent_ids
        # Note: CHEBI:17634 (D-glucose) may not have PubChem cross-references
        # in the Node Normalization service. The service uses CHEBI:4167
        # (D-glucopyranose) as the canonical ID for PUBCHEM.COMPOUND:5793

    @pytest.mark.integration
    def test_normalize_by_chebi_helper(self, client: NodeNormalizationClient) -> None:
        """Test normalize_by_chebi helper method."""
        # Test with just the ID number
        result = client.normalize_by_chebi("17634")
        assert isinstance(result, NormalizedNode)

        # Test with CHEBI: prefix
        result2 = client.normalize_by_chebi("CHEBI:17634")
        assert isinstance(result2, NormalizedNode)

        # Test with integer
        result3 = client.normalize_by_chebi(17634)
        assert isinstance(result3, NormalizedNode)

    @pytest.mark.integration
    def test_normalize_pubchem(self, client: NodeNormalizationClient) -> None:
        """Test normalizing a PubChem CID (glucose - 5793)."""
        result = client.normalize_by_pubchem(5793)

        assert isinstance(result, NormalizedNode)
        # Should find ChEBI equivalents
        chebi_ids = result.get_chebi_ids()
        assert len(chebi_ids) > 0

    @pytest.mark.integration
    def test_normalize_inchikey(self, client: NodeNormalizationClient) -> None:
        """Test normalizing an InChIKey (glucose)."""
        # D-glucose InChIKey
        inchikey = "WQZGKKKJIJFFOK-GASJEMHNSA-N"
        result = client.normalize_by_inchikey(inchikey)

        assert isinstance(result, NormalizedNode)
        assert result.inchikey == inchikey

    @pytest.mark.integration
    def test_normalize_cas(self, client: NodeNormalizationClient) -> None:
        """Test normalizing a CAS Registry Number."""
        # Glucose CAS
        result = client.normalize_by_cas("50-99-7")

        assert isinstance(result, NormalizedNode)
        assert result.cas_rn == "50-99-7"

    @pytest.mark.integration
    def test_normalize_not_found(self, client: NodeNormalizationClient) -> None:
        """Test normalizing a nonexistent identifier."""
        result = client.normalize("CHEBI:999999999")

        assert isinstance(result, NormalizationError)
        assert result.error_code == "NOT_FOUND"

    @pytest.mark.integration
    def test_normalize_batch(self, client: NodeNormalizationClient) -> None:
        """Test batch normalization."""
        curies = ["CHEBI:17634", "PUBCHEM.COMPOUND:5793", "CHEBI:999999999"]
        results = client.normalize_batch(curies)

        assert len(results) == 3
        # First two should succeed
        assert isinstance(results["CHEBI:17634"], NormalizedNode)
        assert isinstance(results["PUBCHEM.COMPOUND:5793"], NormalizedNode)
        # Third should fail
        assert isinstance(results["CHEBI:999999999"], NormalizationError)

    @pytest.mark.integration
    def test_cross_references_comprehensive(self, client: NodeNormalizationClient) -> None:
        """Test that we get comprehensive cross-references."""
        # Use Fe(III)-EDTA which has good cross-references
        result = client.normalize("CHEBI:32599")

        assert isinstance(result, NormalizedNode)

        # Check various ID types are present
        assert len(result.equivalent_ids) > 0

        # Should have labels
        assert result.canonical_label is not None or len(result.all_labels) > 0

    def test_normalized_node_to_dict(self) -> None:
        """Test NormalizedNode serialization."""
        node = NormalizedNode(
            canonical_id="CHEBI:17634",
            canonical_label="D-glucose",
            query_id="PUBCHEM.COMPOUND:5793",
            equivalent_ids={
                "CHEBI": ["CHEBI:17634"],
                "PUBCHEM.COMPOUND": ["PUBCHEM.COMPOUND:5793"],
            },
            inchikey="WQZGKKKJIJFFOK-GASJEMHNSA-N",
            cas_rn="50-99-7",
            all_labels=["D-glucose", "glucose"],
        )

        d = node.to_dict()
        assert d["canonical_id"] == "CHEBI:17634"
        assert d["canonical_label"] == "D-glucose"
        assert d["inchikey"] == "WQZGKKKJIJFFOK-GASJEMHNSA-N"
        assert d["cas_rn"] == "50-99-7"
        assert "CHEBI" in d["equivalent_ids"]

    def test_get_ids_helpers(self) -> None:
        """Test helper methods for extracting specific ID types."""
        node = NormalizedNode(
            canonical_id="CHEBI:17634",
            canonical_label="D-glucose",
            query_id="CHEBI:17634",
            equivalent_ids={
                "CHEBI": ["CHEBI:17634", "CHEBI:4167"],
                "PUBCHEM.COMPOUND": ["PUBCHEM.COMPOUND:5793"],
                "MESH": ["MESH:D005947"],
                "DRUGBANK": ["DRUGBANK:DB00117"],
                "KEGG.COMPOUND": ["KEGG.COMPOUND:C00031"],
                "CHEMBL.COMPOUND": ["CHEMBL.COMPOUND:CHEMBL1222250"],
                "UNII": ["UNII:5SL0G7R0OK"],
            },
        )

        assert node.get_pubchem_cids() == [5793]
        assert "17634" in node.get_chebi_ids()
        assert "D005947" in node.get_mesh_ids()
        assert "DB00117" in node.get_drugbank_ids()
        assert "C00031" in node.get_kegg_ids()
        assert "CHEMBL1222250" in node.get_chembl_ids()
        assert node.get_unii() == "5SL0G7R0OK"

    def test_empty_batch(self, client: NodeNormalizationClient) -> None:
        """Test batch normalization with empty list."""
        results = client.normalize_batch([])
        assert results == {}
