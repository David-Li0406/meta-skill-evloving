"""Tests for KGX file writer module."""

import json
import tempfile
from pathlib import Path

from cmm_ai_automation.transform.kgx import KGXEdge, KGXNode
from cmm_ai_automation.transform.writer import (
    deduplicate_nodes,
    flatten_results,
    generate_edge_id,
    write_kgx_jsonl,
)


class TestDeduplicateNodes:
    """Tests for deduplicate_nodes function."""

    def test_no_duplicates(self) -> None:
        """Test that unique nodes are preserved."""
        nodes = [
            KGXNode(
                id="bacdive:1",
                category=["biolink:OrganismTaxon"],
            ),
            KGXNode(
                id="bacdive:2",
                category=["biolink:OrganismTaxon"],
            ),
        ]
        result = deduplicate_nodes(nodes)
        assert len(result) == 2

    def test_duplicate_nodes_merged(self) -> None:
        """Test that duplicate nodes are merged."""
        nodes = [
            KGXNode(
                id="NCBITaxon:408",
                category=["biolink:OrganismTaxon"],
                name="Methylorubrum extorquens",
                provided_by=["infores:ncbi"],
            ),
            KGXNode(
                id="NCBITaxon:408",
                category=["biolink:OrganismTaxon"],
                name="Methylorubrum extorquens",
                provided_by=["infores:bacdive"],
            ),
        ]
        result = deduplicate_nodes(nodes)

        assert len(result) == 1
        assert result[0].id == "NCBITaxon:408"
        provided = result[0].provided_by or []
        assert sorted(provided) == ["infores:bacdive", "infores:ncbi"]

    def test_list_fields_combined(self) -> None:
        """Test that list fields from duplicates are combined."""
        nodes = [
            KGXNode(
                id="bacdive:1",
                category=["biolink:OrganismTaxon"],
                xref=["DSM:1337", "ATCC:43645"],
            ),
            KGXNode(
                id="bacdive:1",
                category=["biolink:OrganismTaxon"],
                xref=["JCM:2802", "ATCC:43645"],  # ATCC duplicate
            ),
        ]
        result = deduplicate_nodes(nodes)

        assert len(result) == 1
        # Should have 3 unique xrefs (ATCC not duplicated)
        xref = result[0].xref or []
        assert len(xref) == 3
        assert "DSM:1337" in xref
        assert "ATCC:43645" in xref
        assert "JCM:2802" in xref

    def test_missing_fields_added(self) -> None:
        """Test that missing fields from one node are added."""
        nodes = [
            KGXNode(
                id="bacdive:1",
                category=["biolink:OrganismTaxon"],
                name="Strain 1",
            ),
            KGXNode(
                id="bacdive:1",
                category=["biolink:OrganismTaxon"],
                description="A bacterial strain",
            ),
        ]
        result = deduplicate_nodes(nodes)

        assert len(result) == 1
        assert result[0].name == "Strain 1"
        assert result[0].description == "A bacterial strain"

    def test_empty_list(self) -> None:
        """Test deduplication with empty list."""
        result = deduplicate_nodes([])
        assert result == []


class TestGenerateEdgeId:
    """Tests for generate_edge_id function."""

    def test_generates_deterministic_id(self) -> None:
        """Test that same edge generates same ID."""
        edge1 = KGXEdge(
            subject="bacdive:7142",
            predicate="biolink:in_taxon",
            object="NCBITaxon:408",
            knowledge_level="knowledge_assertion",
            agent_type="manual_agent",
        )
        edge2 = KGXEdge(
            subject="bacdive:7142",
            predicate="biolink:in_taxon",
            object="NCBITaxon:408",
            knowledge_level="knowledge_assertion",
            agent_type="manual_agent",
        )

        id1 = generate_edge_id(edge1)
        id2 = generate_edge_id(edge2)

        assert id1 == id2
        assert id1.startswith("edge_")

    def test_different_edges_different_ids(self) -> None:
        """Test that different edges generate different IDs."""
        edge1 = KGXEdge(
            subject="bacdive:7142",
            predicate="biolink:in_taxon",
            object="NCBITaxon:408",
            knowledge_level="knowledge_assertion",
            agent_type="manual_agent",
        )
        edge2 = KGXEdge(
            subject="bacdive:7143",  # Different subject
            predicate="biolink:in_taxon",
            object="NCBITaxon:408",
            knowledge_level="knowledge_assertion",
            agent_type="manual_agent",
        )

        id1 = generate_edge_id(edge1)
        id2 = generate_edge_id(edge2)

        assert id1 != id2

    def test_id_format(self) -> None:
        """Test that generated ID has expected format."""
        edge = KGXEdge(
            subject="bacdive:7142",
            predicate="biolink:in_taxon",
            object="NCBITaxon:408",
            knowledge_level="knowledge_assertion",
            agent_type="manual_agent",
        )

        edge_id = generate_edge_id(edge)

        assert edge_id.startswith("edge_")
        # SHA256 produces 64 hex chars + "edge_" prefix = 69 chars total
        assert len(edge_id) == 69


class TestFlattenResults:
    """Tests for flatten_results function."""

    def test_flatten_single_result(self) -> None:
        """Test flattening single result tuple."""
        results: list[tuple[list[KGXNode], list[KGXEdge]]] = [
            (
                [KGXNode(id="bacdive:1", category=["biolink:OrganismTaxon"])],
                [
                    KGXEdge(
                        subject="bacdive:1",
                        predicate="biolink:in_taxon",
                        object="NCBITaxon:1",
                        knowledge_level="knowledge_assertion",
                        agent_type="manual_agent",
                    )
                ],
            ),
        ]

        nodes, edges = flatten_results(results)

        assert len(nodes) == 1
        assert len(edges) == 1

    def test_flatten_multiple_results(self) -> None:
        """Test flattening multiple result tuples."""
        results: list[tuple[list[KGXNode], list[KGXEdge]]] = [
            (
                [KGXNode(id="bacdive:1", category=["biolink:OrganismTaxon"])],
                [
                    KGXEdge(
                        subject="bacdive:1",
                        predicate="biolink:in_taxon",
                        object="NCBITaxon:1",
                        knowledge_level="knowledge_assertion",
                        agent_type="manual_agent",
                    )
                ],
            ),
            (
                [KGXNode(id="bacdive:2", category=["biolink:OrganismTaxon"])],
                [
                    KGXEdge(
                        subject="bacdive:2",
                        predicate="biolink:in_taxon",
                        object="NCBITaxon:2",
                        knowledge_level="knowledge_assertion",
                        agent_type="manual_agent",
                    )
                ],
            ),
        ]

        nodes, edges = flatten_results(results)

        assert len(nodes) == 2
        assert len(edges) == 2
        assert nodes[0].id == "bacdive:1"
        assert nodes[1].id == "bacdive:2"

    def test_flatten_empty_results(self) -> None:
        """Test flattening with no results."""
        nodes, edges = flatten_results([])

        assert len(nodes) == 0
        assert len(edges) == 0

    def test_flatten_with_empty_tuples(self) -> None:
        """Test flattening with empty node/edge lists."""
        results: list[tuple[list[KGXNode], list[KGXEdge]]] = [
            ([], []),
            (
                [KGXNode(id="bacdive:1", category=["biolink:OrganismTaxon"])],
                [],
            ),
        ]

        nodes, edges = flatten_results(results)

        assert len(nodes) == 1
        assert len(edges) == 0


class TestWriteKgxJsonl:
    """Tests for write_kgx_jsonl function."""

    def test_write_basic_files(self) -> None:
        """Test writing basic nodes and edges to JSON Lines."""
        nodes = [
            KGXNode(
                id="bacdive:7142",
                category=["biolink:OrganismTaxon"],
                name="Methylorubrum extorquens",
            )
        ]
        edges = [
            KGXEdge(
                subject="bacdive:7142",
                predicate="biolink:in_taxon",
                object="NCBITaxon:408",
                knowledge_level="knowledge_assertion",
                agent_type="manual_agent",
            )
        ]

        with tempfile.TemporaryDirectory() as tmpdir:
            nodes_file, edges_file = write_kgx_jsonl(nodes, edges, tmpdir, "test")

            assert nodes_file.exists()
            assert edges_file.exists()
            assert nodes_file.name == "test_nodes.jsonl"
            assert edges_file.name == "test_edges.jsonl"

            # Verify file contents
            with nodes_file.open() as f:
                lines = f.readlines()
                assert len(lines) == 1
                node_data = json.loads(lines[0])
                assert node_data["id"] == "bacdive:7142"
                assert node_data["name"] == "Methylorubrum extorquens"

            with edges_file.open() as f:
                lines = f.readlines()
                assert len(lines) == 1
                edge_data = json.loads(lines[0])
                assert edge_data["subject"] == "bacdive:7142"
                assert edge_data["predicate"] == "biolink:in_taxon"

    def test_write_with_deduplication(self) -> None:
        """Test that nodes are deduplicated by default."""
        nodes = [
            KGXNode(
                id="NCBITaxon:408",
                category=["biolink:OrganismTaxon"],
                provided_by=["infores:ncbi"],
            ),
            KGXNode(
                id="NCBITaxon:408",
                category=["biolink:OrganismTaxon"],
                provided_by=["infores:bacdive"],
            ),
        ]

        with tempfile.TemporaryDirectory() as tmpdir:
            nodes_file, _ = write_kgx_jsonl(nodes, [], tmpdir, "test", deduplicate=True)

            with nodes_file.open() as f:
                lines = f.readlines()
                # Should have only 1 node after deduplication
                assert len(lines) == 1
                node_data = json.loads(lines[0])
                # Should have both provided_by values
                assert len(node_data["provided_by"]) == 2

    def test_write_without_deduplication(self) -> None:
        """Test writing without deduplication."""
        nodes = [
            KGXNode(
                id="NCBITaxon:408",
                category=["biolink:OrganismTaxon"],
                provided_by=["infores:ncbi"],
            ),
            KGXNode(
                id="NCBITaxon:408",
                category=["biolink:OrganismTaxon"],
                provided_by=["infores:bacdive"],
            ),
        ]

        with tempfile.TemporaryDirectory() as tmpdir:
            nodes_file, _ = write_kgx_jsonl(nodes, [], tmpdir, "test", deduplicate=False)

            with nodes_file.open() as f:
                lines = f.readlines()
                # Should have 2 nodes without deduplication
                assert len(lines) == 2

    def test_write_with_edge_id_generation(self) -> None:
        """Test that edge IDs are generated by default."""
        edges = [
            KGXEdge(
                subject="bacdive:7142",
                predicate="biolink:in_taxon",
                object="NCBITaxon:408",
                knowledge_level="knowledge_assertion",
                agent_type="manual_agent",
            )
        ]

        with tempfile.TemporaryDirectory() as tmpdir:
            _, edges_file = write_kgx_jsonl([], edges, tmpdir, "test", generate_ids=True)

            with edges_file.open() as f:
                lines = f.readlines()
                edge_data = json.loads(lines[0])
                assert "id" in edge_data
                assert edge_data["id"].startswith("edge_")

    def test_write_without_edge_id_generation(self) -> None:
        """Test writing without edge ID generation."""
        edges = [
            KGXEdge(
                subject="bacdive:7142",
                predicate="biolink:in_taxon",
                object="NCBITaxon:408",
                knowledge_level="knowledge_assertion",
                agent_type="manual_agent",
            )
        ]

        with tempfile.TemporaryDirectory() as tmpdir:
            _, edges_file = write_kgx_jsonl([], edges, tmpdir, "test", generate_ids=False)

            with edges_file.open() as f:
                lines = f.readlines()
                edge_data = json.loads(lines[0])
                # Should not have ID field
                assert "id" not in edge_data

    def test_write_creates_directory(self) -> None:
        """Test that output directory is created if it doesn't exist."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir) / "nested" / "output"
            nodes = [KGXNode(id="bacdive:1", category=["biolink:OrganismTaxon"])]

            nodes_file, _ = write_kgx_jsonl(nodes, [], output_dir, "test")

            assert output_dir.exists()
            assert nodes_file.parent == output_dir

    def test_write_multiple_nodes_and_edges(self) -> None:
        """Test writing multiple nodes and edges."""
        nodes = [
            KGXNode(id="bacdive:1", category=["biolink:OrganismTaxon"]),
            KGXNode(id="bacdive:2", category=["biolink:OrganismTaxon"]),
            KGXNode(id="NCBITaxon:1", category=["biolink:OrganismTaxon"]),
        ]
        edges = [
            KGXEdge(
                subject="bacdive:1",
                predicate="biolink:in_taxon",
                object="NCBITaxon:1",
                knowledge_level="knowledge_assertion",
                agent_type="manual_agent",
            ),
            KGXEdge(
                subject="bacdive:2",
                predicate="biolink:in_taxon",
                object="NCBITaxon:1",
                knowledge_level="knowledge_assertion",
                agent_type="manual_agent",
            ),
        ]

        with tempfile.TemporaryDirectory() as tmpdir:
            nodes_file, edges_file = write_kgx_jsonl(nodes, edges, tmpdir, "test")

            with nodes_file.open() as f:
                assert len(f.readlines()) == 3

            with edges_file.open() as f:
                assert len(f.readlines()) == 2

    def test_json_format_preserves_all_fields(self) -> None:
        """Test that JSON Lines format preserves all node/edge fields."""
        nodes = [
            KGXNode(
                id="bacdive:7142",
                category=["biolink:OrganismTaxon"],
                name="Methylorubrum extorquens",
                xref=["DSM:1337", "ATCC:43645"],
                synonym=["AM-1"],
                in_taxon=["NCBITaxon:408"],
                in_taxon_label="Methylorubrum extorquens",
                provided_by=["infores:bacdive"],
                type_strain="yes",  # Custom property
                biosafety_level="1",  # Custom property
            )
        ]

        with tempfile.TemporaryDirectory() as tmpdir:
            nodes_file, _ = write_kgx_jsonl(nodes, [], tmpdir, "test")

            with nodes_file.open() as f:
                node_data = json.loads(f.readline())
                # Check all standard fields present
                assert node_data["id"] == "bacdive:7142"
                assert node_data["category"] == ["biolink:OrganismTaxon"]
                assert node_data["name"] == "Methylorubrum extorquens"
                assert node_data["xref"] == ["DSM:1337", "ATCC:43645"]
                assert node_data["synonym"] == ["AM-1"]
                assert node_data["in_taxon"] == ["NCBITaxon:408"]
                # Check custom properties preserved
                assert node_data["type_strain"] == "yes"
                assert node_data["biosafety_level"] == "1"
