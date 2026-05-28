"""Tests for chemicals_kgx_from_curies script."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from pathlib import Path

from cmm_ai_automation.scripts.chemicals_kgx_from_curies import (
    BIOLINK_CHEMICAL_ENTITY,
    BIOLINK_CHEMICAL_ROLE,
    ChemicalResult,
    export_kgx,
    parse_curie,
    read_chemicals_from_file,
    sample_entries,
)


class TestParseCurie:
    """Tests for parse_curie function."""

    def test_parse_chebi_curie(self) -> None:
        """Test parsing CHEBI CURIE."""
        prefix, local_id = parse_curie("CHEBI:17790")
        assert prefix == "CHEBI"
        assert local_id == "17790"

    def test_parse_pubchem_curie(self) -> None:
        """Test parsing PUBCHEM.COMPOUND CURIE."""
        prefix, local_id = parse_curie("PUBCHEM.COMPOUND:16217523")
        assert prefix == "PUBCHEM.COMPOUND"
        assert local_id == "16217523"

    def test_parse_curie_with_whitespace(self) -> None:
        """Test parsing CURIE with surrounding whitespace."""
        prefix, local_id = parse_curie("  CHEBI:17790  ")
        assert prefix == "CHEBI"
        assert local_id == "17790"

    def test_parse_invalid_curie_no_colon(self) -> None:
        """Test that invalid CURIE without colon raises ValueError."""
        with pytest.raises(ValueError, match="no colon"):
            parse_curie("CHEBI17790")

    def test_parse_doi_curie(self) -> None:
        """Test parsing doi CURIE (non-chemical but valid format)."""
        prefix, local_id = parse_curie("doi:10.1371/journal.pone.0062957")
        assert prefix == "doi"
        assert local_id == "10.1371/journal.pone.0062957"


class TestChemicalResult:
    """Tests for ChemicalResult dataclass."""

    def test_create_basic_result(self) -> None:
        """Test creating a basic ChemicalResult."""
        result = ChemicalResult(
            input_curie="CHEBI:17790",
            canonical_id="CHEBI:17790",
            name="methanol",
            formula="CH4O",
            mass=32.042,
        )
        assert result.input_curie == "CHEBI:17790"
        assert result.canonical_id == "CHEBI:17790"
        assert result.name == "methanol"
        assert result.formula == "CH4O"
        assert result.mass == 32.042
        assert result.category == BIOLINK_CHEMICAL_ENTITY

    def test_to_kgx_node_basic(self) -> None:
        """Test converting ChemicalResult to KGX node."""
        result = ChemicalResult(
            input_curie="CHEBI:17790",
            canonical_id="CHEBI:17790",
            name="methanol",
            formula="CH4O",
            mass=32.042,
            inchikey="OKKJLVBELUTLKV-UHFFFAOYSA-N",
        )
        node = result.to_kgx_node()

        assert node["id"] == "CHEBI:17790"
        assert node["category"] == [BIOLINK_CHEMICAL_ENTITY]  # List for KGX Sink
        assert node["name"] == "methanol"
        assert node["formula"] == "CH4O"
        assert node["mass"] == "32.042"  # String for TSV output
        assert node["inchikey"] == "OKKJLVBELUTLKV-UHFFFAOYSA-N"

    def test_to_kgx_node_with_cas_numbers(self) -> None:
        """Test that CAS numbers are converted to xrefs."""
        result = ChemicalResult(
            input_curie="CHEBI:17790",
            canonical_id="CHEBI:17790",
            name="methanol",
            cas_numbers=["67-56-1"],
        )
        node = result.to_kgx_node()

        assert "casrn:67-56-1" in node["xref"]

    def test_to_kgx_node_with_synonyms(self) -> None:
        """Test that synonyms are returned as a list."""
        result = ChemicalResult(
            input_curie="CHEBI:17790",
            canonical_id="CHEBI:17790",
            name="methanol",
            synonyms=["MeOH", "wood alcohol", "carbinol"],
        )
        node = result.to_kgx_node()

        assert "MeOH" in node["synonym"]
        assert "wood alcohol" in node["synonym"]
        assert isinstance(node["synonym"], list)  # Lists for KGX Sink

    def test_to_kgx_node_with_xrefs(self) -> None:
        """Test that xrefs are properly formatted."""
        result = ChemicalResult(
            input_curie="CHEBI:17790",
            canonical_id="CHEBI:17790",
            name="methanol",
            xrefs=["PUBCHEM.COMPOUND:887", "KEGG.COMPOUND:C00132"],
            cas_numbers=["67-56-1"],
        )
        node = result.to_kgx_node()

        # CAS should be added as xref
        assert "casrn:67-56-1" in node["xref"]
        assert "PUBCHEM.COMPOUND:887" in node["xref"]
        assert "KEGG.COMPOUND:C00132" in node["xref"]

    def test_to_kgx_node_empty_mass(self) -> None:
        """Test that None mass is omitted from output."""
        result = ChemicalResult(
            input_curie="CHEBI:17790",
            canonical_id="CHEBI:17790",
            name="methanol",
            mass=None,
        )
        node = result.to_kgx_node()

        assert "mass" not in node  # Empty fields are omitted

    def test_to_kgx_node_with_roles(self) -> None:
        """Test that roles are stored but not in node output."""
        result = ChemicalResult(
            input_curie="CHEBI:17790",
            canonical_id="CHEBI:17790",
            name="methanol",
            chebi_roles=[("CHEBI:33292", "fuel"), ("CHEBI:77746", "human metabolite")],
        )
        node = result.to_kgx_node()

        # Roles should not appear in node output (they go in edges and role nodes)
        assert "chebi_role" not in node


class TestSampleEntries:
    """Tests for sample_entries function."""

    def test_sample_n(self) -> None:
        """Test sampling N entries."""
        entries = [{"curie": f"CHEBI:{i}"} for i in range(100)]
        sampled = sample_entries(entries, sample_n=10)

        assert len(sampled) == 10
        # All sampled entries should be from original list
        for entry in sampled:
            assert entry in entries

    def test_sample_n_larger_than_list(self) -> None:
        """Test sampling more than available."""
        entries = [{"curie": f"CHEBI:{i}"} for i in range(5)]
        sampled = sample_entries(entries, sample_n=10)

        assert len(sampled) == 5

    def test_sample_fraction(self) -> None:
        """Test sampling by fraction."""
        entries = [{"curie": f"CHEBI:{i}"} for i in range(100)]
        sampled = sample_entries(entries, sample_fraction=0.1)

        assert len(sampled) == 10

    def test_sample_fraction_minimum_one(self) -> None:
        """Test that fraction sampling returns at least 1."""
        entries = [{"curie": f"CHEBI:{i}"} for i in range(100)]
        sampled = sample_entries(entries, sample_fraction=0.001)

        assert len(sampled) >= 1

    def test_no_sampling(self) -> None:
        """Test that no sampling returns original list."""
        entries = [{"curie": f"CHEBI:{i}"} for i in range(10)]
        sampled = sample_entries(entries)

        assert sampled == entries


class TestReadChemicalsFromFile:
    """Tests for read_chemicals_from_file function."""

    def test_read_tsv_file(self, tmp_path: Path) -> None:
        """Test reading TSV file."""
        test_file = tmp_path / "chemicals.tsv"
        test_file.write_text("id\tname\tcomments\nCHEBI:17790\tmethanol\ta fuel\nPUBCHEM.COMPOUND:887\tmethanol\t\n")

        entries = read_chemicals_from_file(test_file, "id")

        assert len(entries) == 2
        assert entries[0]["curie"] == "CHEBI:17790"
        assert entries[1]["curie"] == "PUBCHEM.COMPOUND:887"

    def test_read_with_name_field(self, tmp_path: Path) -> None:
        """Test reading with name field."""
        test_file = tmp_path / "chemicals.tsv"
        test_file.write_text("id\tchemical_name\nCHEBI:17790\tMethanol\n")

        entries = read_chemicals_from_file(test_file, "id", name_field="chemical_name")

        assert entries[0]["name"] == "Methanol"

    def test_read_with_comments_field(self, tmp_path: Path) -> None:
        """Test reading with comments field."""
        test_file = tmp_path / "chemicals.tsv"
        test_file.write_text("id\tnotes\nCHEBI:17790\tUsed as solvent\n")

        entries = read_chemicals_from_file(test_file, "id", comments_field="notes")

        assert entries[0]["comments"] == "Used as solvent"

    def test_read_skips_empty_ids(self, tmp_path: Path) -> None:
        """Test that empty IDs are skipped."""
        test_file = tmp_path / "chemicals.tsv"
        test_file.write_text("id\tname\nCHEBI:17790\tmethanol\n\tno_id\nCHEBI:31795\tmagnesium sulfate\n")

        entries = read_chemicals_from_file(test_file, "id")

        assert len(entries) == 2
        assert entries[0]["curie"] == "CHEBI:17790"
        assert entries[1]["curie"] == "CHEBI:31795"


class TestExportKgx:
    """Tests for export_kgx function."""

    def test_export_creates_files(self, tmp_path: Path) -> None:
        """Test that export_kgx creates both nodes and edges files."""
        results = [
            ChemicalResult(
                input_curie="CHEBI:17790",
                canonical_id="CHEBI:17790",
                name="methanol",
                formula="CH4O",
                mass=32.042,
                chebi_roles=[("CHEBI:33292", "fuel")],
            )
        ]

        node_count, edge_count = export_kgx(results, tmp_path)

        # node_count includes chemical + role nodes (2 total)
        assert node_count == 2  # 1 chemical + 1 role node
        assert edge_count == 1
        nodes_path = tmp_path / "chemicals_nodes.tsv"
        edges_path = tmp_path / "chemicals_edges.tsv"
        assert nodes_path.exists()
        assert edges_path.exists()

        nodes_content = nodes_path.read_text()
        assert "CHEBI:17790" in nodes_content
        assert "methanol" in nodes_content
        assert "CH4O" in nodes_content

    def test_export_includes_roles(self, tmp_path: Path) -> None:
        """Test that role nodes and edges are created."""
        results = [
            ChemicalResult(
                input_curie="CHEBI:17790",
                canonical_id="CHEBI:17790",
                name="methanol",
                chebi_roles=[("CHEBI:33292", "fuel"), ("CHEBI:77746", "human metabolite")],
            )
        ]

        chemical_count, edge_count = export_kgx(results, tmp_path)

        assert edge_count == 2  # Two role edges
        edges_content = (tmp_path / "chemicals_edges.tsv").read_text()
        assert "biolink:has_role" in edges_content
        assert "CHEBI:33292" in edges_content
        assert "CHEBI:77746" in edges_content

        # Role nodes should be in nodes file
        nodes_content = (tmp_path / "chemicals_nodes.tsv").read_text()
        assert BIOLINK_CHEMICAL_ROLE in nodes_content

    def test_export_has_provenance(self, tmp_path: Path) -> None:
        """Test that edges have proper provenance fields."""
        results = [
            ChemicalResult(
                input_curie="CHEBI:17790",
                canonical_id="CHEBI:17790",
                name="methanol",
                chebi_roles=[("CHEBI:33292", "fuel")],
            )
        ]

        export_kgx(results, tmp_path)

        edges_content = (tmp_path / "chemicals_edges.tsv").read_text()
        assert "knowledge_assertion" in edges_content
        assert "manual_agent" in edges_content
        assert "infores:cmm-ai-automation" in edges_content

    def test_export_no_edges_without_roles(self, tmp_path: Path) -> None:
        """Test that chemicals without roles produce no edges."""
        results = [
            ChemicalResult(
                input_curie="CHEBI:17790",
                canonical_id="CHEBI:17790",
                name="methanol",
                chebi_roles=[],
            )
        ]

        chemical_count, edge_count = export_kgx(results, tmp_path)

        assert edge_count == 0
