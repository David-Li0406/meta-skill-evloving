"""Integration tests for complete KGX transformation pipeline."""

import json
import tempfile

from cmm_ai_automation.transform import (
    flatten_results,
    transform_bacdive_doc,
    write_kgx_jsonl,
)


class TestBacDivePipeline:
    """Integration tests for BacDive → KGX → JSON Lines pipeline."""

    def test_single_document_pipeline(self) -> None:
        """Test complete pipeline with single BacDive document."""
        # Input: BacDive MongoDB document
        bacdive_doc = {
            "General": {
                "BacDive-ID": 7142,
                "NCBI tax id": {"NCBI tax id": 408, "Matching level": "species"},
            },
            "Name and taxonomic classification": {
                "species": "Methylorubrum extorquens",
                "type strain": "yes",
            },
            "External links": {"culture collection no.": "DSM 1337, ATCC 43645"},
            "Safety information": {"risk assessment": {"biosafety level": "1"}},
        }

        # Step 1: Transform BacDive doc to KGX
        nodes, edges = transform_bacdive_doc(bacdive_doc)

        # Verify transformation
        assert len(nodes) == 2  # Strain + species
        assert len(edges) == 1  # in_taxon edge

        strain_node = nodes[0]
        assert strain_node.id == "bacdive:7142"
        assert strain_node.category == ["biolink:OrganismTaxon"]

        # Step 2: Write to JSON Lines
        with tempfile.TemporaryDirectory() as tmpdir:
            nodes_file, edges_file = write_kgx_jsonl(nodes, edges, tmpdir, "cmm_strains")

            # Verify files created
            assert nodes_file.exists()
            assert edges_file.exists()

            # Verify node content
            with nodes_file.open() as f:
                node_lines = f.readlines()
                assert len(node_lines) == 2

                # Parse and verify strain node
                strain_data = json.loads(node_lines[0])
                assert strain_data["id"] == "bacdive:7142"
                assert strain_data["category"] == ["biolink:OrganismTaxon"]
                assert "type_strain" in strain_data
                assert strain_data["type_strain"] == "yes"

            # Verify edge content
            with edges_file.open() as f:
                edge_lines = f.readlines()
                assert len(edge_lines) == 1

                edge_data = json.loads(edge_lines[0])
                assert edge_data["subject"] == "bacdive:7142"
                assert edge_data["predicate"] == "biolink:in_taxon"
                assert edge_data["object"] == "NCBITaxon:408"

    def test_multiple_documents_pipeline(self) -> None:
        """Test pipeline with multiple BacDive documents."""
        # Input: Multiple BacDive documents
        docs = [
            {
                "General": {
                    "BacDive-ID": 7142,
                    "NCBI tax id": {"NCBI tax id": 408, "Matching level": "species"},
                },
                "Name and taxonomic classification": {"species": "Methylorubrum extorquens"},
            },
            {
                "General": {
                    "BacDive-ID": 7143,
                    "NCBI tax id": {"NCBI tax id": 408, "Matching level": "species"},
                },
                "Name and taxonomic classification": {"species": "Methylorubrum extorquens"},
            },
        ]

        # Step 1: Transform all documents
        results = []
        for doc in docs:
            nodes, edges = transform_bacdive_doc(doc)
            results.append((nodes, edges))

        # Step 2: Flatten results
        all_nodes, all_edges = flatten_results(results)

        # Should have 4 nodes (2 strains + 2 species before deduplication)
        assert len(all_nodes) == 4
        # Should have 2 edges
        assert len(all_edges) == 2

        # Step 3: Write to files (with deduplication)
        with tempfile.TemporaryDirectory() as tmpdir:
            nodes_file, edges_file = write_kgx_jsonl(all_nodes, all_edges, tmpdir, "cmm_strains", deduplicate=True)

            # Verify deduplication happened
            with nodes_file.open() as f:
                node_lines = f.readlines()
                # Should have 3 nodes after deduplication (2 strains + 1 species)
                assert len(node_lines) == 3

                # Parse all nodes
                node_ids = [json.loads(line)["id"] for line in node_lines]
                assert "bacdive:7142" in node_ids
                assert "bacdive:7143" in node_ids
                assert "NCBITaxon:408" in node_ids

            # Verify edges
            with edges_file.open() as f:
                edge_lines = f.readlines()
                assert len(edge_lines) == 2

                # All edges should have generated IDs
                for line in edge_lines:
                    edge_data = json.loads(line)
                    assert "id" in edge_data
                    assert edge_data["id"].startswith("edge_")

    def test_empty_document_handling(self) -> None:
        """Test pipeline handles documents without required fields."""
        # Document missing BacDive-ID
        bad_doc = {"Name and taxonomic classification": {"species": "Methylorubrum extorquens"}}

        nodes, edges = transform_bacdive_doc(bad_doc)

        # Should return empty lists
        assert len(nodes) == 0
        assert len(edges) == 0

    def test_full_pipeline_preserves_all_data(self) -> None:
        """Test that full pipeline preserves all data fields."""
        doc = {
            "General": {
                "BacDive-ID": 7142,
                "NCBI tax id": {"NCBI tax id": 408, "Matching level": "species"},
            },
            "Name and taxonomic classification": {
                "species": "Methylorubrum extorquens",
                "type strain": "yes",
                "strain designation": "TK 0001",
                "LPSN": {
                    "synonyms": [
                        {"synonym": "Methylobacterium extorquens"},
                        {"synonym": "Protomonas extorquens"},
                    ]
                },
            },
            "External links": {"culture collection no.": "DSM 1337, ATCC 43645, JCM 2802"},
            "Safety information": {"risk assessment": {"biosafety level": "1"}},
            "Sequence information": {
                "Genome sequences": [{"accession": "GCA_000022685.1"}, {"accession": "408.23", "database": "patric"}]
            },
        }

        nodes, edges = transform_bacdive_doc(doc)

        with tempfile.TemporaryDirectory() as tmpdir:
            nodes_file, _ = write_kgx_jsonl(nodes, edges, tmpdir, "test")

            with nodes_file.open() as f:
                strain_line = f.readline()
                strain_data = json.loads(strain_line)

                # Verify all fields preserved
                assert strain_data["id"] == "bacdive:7142"
                assert strain_data["category"] == ["biolink:OrganismTaxon"]
                assert strain_data["in_taxon"] == ["NCBITaxon:408"]
                assert len(strain_data["xref"]) == 3
                assert "DSM:1337" in strain_data["xref"]
                assert len(strain_data["synonym"]) == 2
                assert "Methylobacterium extorquens" in strain_data["synonym"]
                assert strain_data["type_strain"] == "yes"
                assert strain_data["biosafety_level"] == "1"
                assert strain_data["strain_designation"] == ["TK 0001"]
                assert len(strain_data["has_genome"]) == 2
                assert "GCA_000022685.1" in strain_data["has_genome"]
                assert "408.23" in strain_data["has_genome"]


class TestEdgeToEdgePipeline:
    """Test that edges maintain proper provenance through pipeline."""

    def test_edge_provenance_preserved(self) -> None:
        """Test that edge provenance fields are preserved in output."""
        doc = {
            "General": {
                "BacDive-ID": 7142,
                "NCBI tax id": {"NCBI tax id": 408, "Matching level": "species"},
            },
        }

        nodes, edges = transform_bacdive_doc(doc)

        with tempfile.TemporaryDirectory() as tmpdir:
            _, edges_file = write_kgx_jsonl(nodes, edges, tmpdir, "test")

            with edges_file.open() as f:
                edge_data = json.loads(f.readline())

                # Verify provenance fields
                assert edge_data["knowledge_level"] == "knowledge_assertion"
                assert edge_data["agent_type"] == "manual_agent"
                assert edge_data["primary_knowledge_source"] == ["infores:bacdive"]
                # Should have generated ID
                assert "id" in edge_data
                assert edge_data["id"].startswith("edge_")
