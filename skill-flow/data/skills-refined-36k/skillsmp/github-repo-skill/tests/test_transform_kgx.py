"""Tests for KGX transformation module."""

import pytest
from pydantic import ValidationError

from cmm_ai_automation.transform.kgx import (
    KGXEdge,
    KGXNode,
    normalize_curie,
    split_list_field,
    transform_strain_row,
)


class TestKGXNode:
    """Tests for KGXNode model."""

    def test_minimal_node(self) -> None:
        """Test creating a node with only required fields."""
        node = KGXNode(
            id="bacdive:7142",
            category=["biolink:OrganismTaxon"],
        )
        assert node.id == "bacdive:7142"
        assert node.category == ["biolink:OrganismTaxon"]
        assert node.name is None
        assert node.provided_by is None

    def test_full_node(self) -> None:
        """Test creating a node with all common fields."""
        node = KGXNode(
            id="bacdive:7142",
            category=["biolink:OrganismTaxon"],
            name="Methylorubrum extorquens DSM 1337",
            description="Type strain",
            provided_by=["infores:bacdive"],
            xref=["DSM:1337", "ATCC:43645"],
            synonym=["AM-1", "Methylobacterium extorquens AM1"],
            in_taxon=["NCBITaxon:408"],
            in_taxon_label="Methylorubrum extorquens",
        )
        assert node.id == "bacdive:7142"
        assert node.name == "Methylorubrum extorquens DSM 1337"
        assert node.xref is not None and len(node.xref) == 2
        assert node.synonym is not None and len(node.synonym) == 2

    def test_custom_properties_allowed(self) -> None:
        """Test that custom properties are allowed (KGX lenient design)."""
        node = KGXNode(
            id="bacdive:7142",
            category=["biolink:OrganismTaxon"],
            type_strain="yes",  # Custom property
            biosafety_level="1",  # Custom property
        )
        assert node.model_extra["type_strain"] == "yes"
        assert node.model_extra["biosafety_level"] == "1"

    def test_missing_required_id_fails(self) -> None:
        """Test that missing id raises ValidationError."""
        with pytest.raises(ValidationError):
            KGXNode(category=["biolink:OrganismTaxon"])

    def test_missing_required_category_fails(self) -> None:
        """Test that missing category raises ValidationError."""
        with pytest.raises(ValidationError):
            KGXNode(id="bacdive:7142")

    def test_empty_category_fails(self) -> None:
        """Test that empty category list raises ValidationError."""
        with pytest.raises(ValidationError):
            KGXNode(id="bacdive:7142", category=[])


class TestKGXEdge:
    """Tests for KGXEdge model."""

    def test_minimal_edge(self) -> None:
        """Test creating an edge with only required fields."""
        edge = KGXEdge(
            subject="bacdive:7142",
            predicate="biolink:in_taxon",
            object="NCBITaxon:408",
            knowledge_level="knowledge_assertion",
            agent_type="manual_agent",
        )
        assert edge.subject == "bacdive:7142"
        assert edge.predicate == "biolink:in_taxon"
        assert edge.object == "NCBITaxon:408"
        assert edge.knowledge_level == "knowledge_assertion"
        assert edge.agent_type == "manual_agent"
        assert edge.id is None

    def test_full_edge(self) -> None:
        """Test creating an edge with all recommended fields."""
        edge = KGXEdge(
            id="edge_1",
            subject="bacdive:7142",
            predicate="biolink:in_taxon",
            object="NCBITaxon:408",
            knowledge_level="knowledge_assertion",
            agent_type="manual_agent",
            category=["biolink:Association"],
            primary_knowledge_source=["infores:bacdive"],
            aggregator_knowledge_source=["infores:kg-microbe"],
            publications=["PMID:12345678"],
        )
        assert edge.id == "edge_1"
        assert edge.primary_knowledge_source == ["infores:bacdive"]
        assert edge.publications == ["PMID:12345678"]

    @pytest.mark.parametrize(
        "knowledge_level",
        [
            "knowledge_assertion",
            "logical_entailment",
            "prediction",
            "statistical_association",
            "observation",
            "not_provided",
        ],
    )
    def test_valid_knowledge_levels(self, knowledge_level: str) -> None:
        """Test that all valid knowledge_level enum values are accepted."""
        edge = KGXEdge(
            subject="bacdive:7142",
            predicate="biolink:in_taxon",
            object="NCBITaxon:408",
            knowledge_level=knowledge_level,
            agent_type="manual_agent",
        )
        assert edge.knowledge_level == knowledge_level

    @pytest.mark.parametrize(
        "agent_type",
        [
            "manual_agent",
            "automated_agent",
            "data_analysis_pipeline",
            "computational_model",
            "text_mining_agent",
            "image_processing_agent",
            "manual_validation_of_automated_agent",
            "not_provided",
        ],
    )
    def test_valid_agent_types(self, agent_type: str) -> None:
        """Test that all valid agent_type enum values are accepted."""
        edge = KGXEdge(
            subject="bacdive:7142",
            predicate="biolink:in_taxon",
            object="NCBITaxon:408",
            knowledge_level="knowledge_assertion",
            agent_type=agent_type,
        )
        assert edge.agent_type == agent_type

    def test_invalid_knowledge_level_fails(self) -> None:
        """Test that invalid knowledge_level raises ValidationError."""
        with pytest.raises(ValidationError):
            KGXEdge(
                subject="bacdive:7142",
                predicate="biolink:in_taxon",
                object="NCBITaxon:408",
                knowledge_level="invalid_level",
                agent_type="manual_agent",
            )

    def test_invalid_agent_type_fails(self) -> None:
        """Test that invalid agent_type raises ValidationError."""
        with pytest.raises(ValidationError):
            KGXEdge(
                subject="bacdive:7142",
                predicate="biolink:in_taxon",
                object="NCBITaxon:408",
                knowledge_level="knowledge_assertion",
                agent_type="invalid_agent",
            )


class TestNormalizeCurie:
    """Tests for normalize_curie function."""

    @pytest.mark.parametrize(
        "prefix,local_id,expected",
        [
            ("bacdive", "7142", "bacdive:7142"),
            ("NCBITaxon", "408", "NCBITaxon:408"),
            ("DSM", "1337", "DSM:1337"),
            ("ATCC", "43645", "ATCC:43645"),
            ("infores", "bacdive", "infores:bacdive"),
        ],
    )
    def test_normalize_curie(self, prefix: str, local_id: str, expected: str) -> None:
        """Test CURIE normalization with various inputs."""
        assert normalize_curie(prefix, local_id) == expected


class TestSplitListField:
    """Tests for split_list_field function."""

    @pytest.mark.parametrize(
        "input_str,expected",
        [
            ("DSM:1337; ATCC:43645; JCM:2802", ["DSM:1337", "ATCC:43645", "JCM:2802"]),
            ("value1;value2;value3", ["value1", "value2", "value3"]),
            ("single", ["single"]),
            ("  spaces  ; around ; values  ", ["spaces", "around", "values"]),
            ("", []),
            (None, []),
            ("   ", []),
            ("value1;;value3", ["value1", "value3"]),  # Empty middle value
        ],
    )
    def test_split_list_field(self, input_str: str | None, expected: list[str]) -> None:
        """Test splitting delimited strings with various inputs."""
        assert split_list_field(input_str) == expected

    def test_custom_delimiter(self) -> None:
        """Test using custom delimiter."""
        result = split_list_field("a|b|c", delimiter="|")
        assert result == ["a", "b", "c"]


class TestTransformStrainRow:
    """Tests for transform_strain_row function."""

    def test_minimal_valid_row(self) -> None:
        """Test transformation with minimal required data."""
        row = {
            "bacdive_id_mam": "7142",
        }
        nodes, edges = transform_strain_row(row)

        # Should create 1 strain node, no taxonomy node, no edges
        assert len(nodes) == 1
        assert len(edges) == 0
        assert nodes[0].id == "bacdive:7142"
        assert nodes[0].category == ["biolink:OrganismTaxon"]

    def test_row_with_species_taxon(self) -> None:
        """Test transformation with species taxonomy."""
        row = {
            "bacdive_id_mam": "7142",
            "scientific_name_sub_or_mpj": "Methylorubrum extorquens",
            "ncbi_species_taxon_fresh_lookup": "408",
        }
        nodes, edges = transform_strain_row(row)

        # Should create 2 nodes (strain + species) and 1 edge
        assert len(nodes) == 2
        assert len(edges) == 1

        # Check strain node
        strain_node = nodes[0]
        assert strain_node.id == "bacdive:7142"
        assert strain_node.in_taxon == ["NCBITaxon:408"]
        assert strain_node.in_taxon_label == "Methylorubrum extorquens"

        # Check species node
        species_node = nodes[1]
        assert species_node.id == "NCBITaxon:408"
        assert species_node.name == "Methylorubrum extorquens"

        # Check edge
        edge = edges[0]
        assert edge.subject == "bacdive:7142"
        assert edge.predicate == "biolink:in_taxon"
        assert edge.object == "NCBITaxon:408"

    def test_full_strain_row(self) -> None:
        """Test transformation with all available fields."""
        row = {
            "bacdive_id_mam": "7142",
            "strain_id_sub_or_mpj": "DSM:1337",
            "scientific_name_sub_or_mpj": "Methylorubrum extorquens",
            "ncbi_species_taxon_fresh_lookup": "408",
            "type_strain_fresh_lookup": "yes",
            "biosafety_level_fresh_lookup": "1",
            "culture_collection_ids_sub_or_mpj": "DSM:1337; ATCC:43645; JCM:2802",
            "alternative_names_sub_or_mpj": "AM-1; Methylobacterium extorquens AM1",
            "availability_status_sub_or_mpj": "available",
        }
        nodes, edges = transform_strain_row(row)

        assert len(nodes) == 2
        assert len(edges) == 1

        strain_node = nodes[0]
        assert strain_node.id == "bacdive:7142"
        assert strain_node.name == "Methylorubrum extorquens DSM:1337"
        assert strain_node.xref == ["DSM:1337", "ATCC:43645", "JCM:2802"]
        assert strain_node.synonym == ["AM-1", "Methylobacterium extorquens AM1"]
        assert strain_node.model_extra["type_strain"] == "yes"
        assert strain_node.model_extra["biosafety_level"] == "1"
        assert strain_node.model_extra["availability_status"] == "available"

    def test_prefer_fresh_lookup_over_sub_or_mpj(self) -> None:
        """Test that fresh_lookup values are preferred over sub_or_mpj."""
        row = {
            "bacdive_id_mam": "7142",
            "species_taxon_id_sub_or_mpj": "999",  # Old value
            "ncbi_species_taxon_fresh_lookup": "408",  # Fresh value
            "type_strain_sub_or_mpj": "no",  # Old value
            "type_strain_fresh_lookup": "yes",  # Fresh value
        }
        nodes, edges = transform_strain_row(row)

        strain_node = nodes[0]
        assert strain_node.in_taxon == ["NCBITaxon:408"]  # Used fresh
        assert strain_node.model_extra["type_strain"] == "yes"  # Used fresh

    def test_fallback_to_sub_or_mpj(self) -> None:
        """Test fallback to sub_or_mpj when fresh_lookup not available."""
        row = {
            "bacdive_id_mam": "7142",
            "species_taxon_id_sub_or_mpj": "408",
            "biosafety_level_sub_or_mpj": "1",
        }
        nodes, edges = transform_strain_row(row)

        strain_node = nodes[0]
        assert strain_node.in_taxon == ["NCBITaxon:408"]
        assert strain_node.model_extra["biosafety_level"] == "1"

    def test_empty_bacdive_id_returns_empty(self) -> None:
        """Test that row without BacDive ID returns empty results."""
        row = {
            "bacdive_id_mam": "",
            "scientific_name_sub_or_mpj": "Methylorubrum extorquens",
        }
        nodes, edges = transform_strain_row(row)

        assert len(nodes) == 0
        assert len(edges) == 0

    def test_missing_bacdive_id_returns_empty(self) -> None:
        """Test that row without bacdive_id_mam key returns empty results."""
        row = {
            "scientific_name_sub_or_mpj": "Methylorubrum extorquens",
        }
        nodes, edges = transform_strain_row(row)

        assert len(nodes) == 0
        assert len(edges) == 0

    def test_name_construction_priority(self) -> None:
        """Test name construction uses scientific_name + strain_id when both present."""
        row = {
            "bacdive_id_mam": "7142",
            "scientific_name_sub_or_mpj": "Methylorubrum extorquens",
            "strain_id_sub_or_mpj": "DSM:1337",
        }
        nodes, edges = transform_strain_row(row)

        assert nodes[0].name == "Methylorubrum extorquens DSM:1337"

    def test_name_fallback_scientific_only(self) -> None:
        """Test name uses scientific_name when strain_id not present."""
        row = {
            "bacdive_id_mam": "7142",
            "scientific_name_sub_or_mpj": "Methylorubrum extorquens",
        }
        nodes, edges = transform_strain_row(row)

        assert nodes[0].name == "Methylorubrum extorquens"

    def test_name_fallback_strain_id_only(self) -> None:
        """Test name uses strain_id when scientific_name not present."""
        row = {
            "bacdive_id_mam": "7142",
            "strain_id_sub_or_mpj": "DSM:1337",
        }
        nodes, edges = transform_strain_row(row)

        assert nodes[0].name == "DSM:1337"

    def test_name_fallback_curie(self) -> None:
        """Test name uses CURIE when neither scientific_name nor strain_id present."""
        row = {
            "bacdive_id_mam": "7142",
        }
        nodes, edges = transform_strain_row(row)

        assert nodes[0].name == "bacdive:7142"

    def test_edge_has_required_provenance(self) -> None:
        """Test that edges have proper provenance fields."""
        row = {
            "bacdive_id_mam": "7142",
            "ncbi_species_taxon_fresh_lookup": "408",
        }
        nodes, edges = transform_strain_row(row)

        edge = edges[0]
        assert edge.knowledge_level == "knowledge_assertion"
        assert edge.agent_type == "manual_agent"
        assert edge.primary_knowledge_source == ["infores:bacdive"]
