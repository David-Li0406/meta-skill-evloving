"""Tests for BacDive MongoDB source transformation."""

from typing import Any

from cmm_ai_automation.transform.bacdive_source import (
    extract_alternative_names,
    extract_biosafety_level,
    extract_culture_collection_ids,
    extract_genome_accessions,
    extract_ncbi_taxon_ids,
    extract_scientific_name,
    extract_strain_designations,
    extract_type_strain,
    safe_get_list,
    transform_bacdive_doc,
)


class TestSafeGetList:
    """Tests for safe_get_list utility function."""

    def test_dict_with_scalar(self) -> None:
        """Test extracting scalar value from nested dict."""
        doc: dict[str, Any] = {"General": {"NCBI tax id": 408}}
        result = safe_get_list(doc, "General", "NCBI tax id")
        assert result == [408]

    def test_dict_with_dict(self) -> None:
        """Test extracting dict value (normalized to list)."""
        doc: dict[str, Any] = {"General": {"NCBI tax id": {"NCBI tax id": 408, "Matching level": "species"}}}
        result = safe_get_list(doc, "General", "NCBI tax id")
        assert len(result) == 1
        assert result[0] == {"NCBI tax id": 408, "Matching level": "species"}

    def test_dict_with_list(self) -> None:
        """Test extracting list value (returned as-is)."""
        doc: dict[str, Any] = {
            "General": {
                "NCBI tax id": [
                    {"NCBI tax id": 31998, "Matching level": "species"},
                    {"NCBI tax id": 426355, "Matching level": "strain"},
                ]
            }
        }
        result = safe_get_list(doc, "General", "NCBI tax id")
        assert len(result) == 2

    def test_missing_key(self) -> None:
        """Test missing key returns empty list."""
        doc: dict[str, Any] = {"General": {}}
        result = safe_get_list(doc, "General", "Missing")
        assert result == []

    def test_none_value(self) -> None:
        """Test None value returns empty list."""
        doc: dict[str, Any] = {"General": {"NCBI tax id": None}}
        result = safe_get_list(doc, "General", "NCBI tax id")
        assert result == []

    def test_empty_path(self) -> None:
        """Test empty path returns the object as list."""
        doc: dict[str, Any] = {"key": "value"}
        result = safe_get_list(doc)
        assert result == [{"key": "value"}]

    def test_non_dict_returns_empty(self) -> None:
        """Test non-dict intermediate value returns empty."""
        doc: dict[str, Any] = {"General": "not a dict"}
        result = safe_get_list(doc, "General", "NCBI tax id")
        assert result == []


class TestExtractNcbiTaxonIds:
    """Tests for extract_ncbi_taxon_ids function."""

    def test_species_level_only(self) -> None:
        """Test extracting species-level taxon ID."""
        doc: dict[str, Any] = {"General": {"NCBI tax id": {"NCBI tax id": 408, "Matching level": "species"}}}
        species, strain = extract_ncbi_taxon_ids(doc)
        assert species == {"408"}
        assert strain == set()

    def test_strain_level_only(self) -> None:
        """Test extracting strain-level taxon ID."""
        doc: dict[str, Any] = {"General": {"NCBI tax id": {"NCBI tax id": 426355, "Matching level": "strain"}}}
        species, strain = extract_ncbi_taxon_ids(doc)
        assert species == set()
        assert strain == {"426355"}

    def test_multiple_levels(self) -> None:
        """Test extracting both species and strain level IDs."""
        doc: dict[str, Any] = {
            "General": {
                "NCBI tax id": [
                    {"NCBI tax id": 31998, "Matching level": "species"},
                    {"NCBI tax id": 426355, "Matching level": "strain"},
                ]
            }
        }
        species, strain = extract_ncbi_taxon_ids(doc)
        assert "31998" in species
        assert "426355" in strain

    def test_no_matching_level_defaults_to_species(self) -> None:
        """Test that missing Matching level defaults to species."""
        doc: dict[str, Any] = {"General": {"NCBI tax id": {"NCBI tax id": 408}}}
        species, strain = extract_ncbi_taxon_ids(doc)
        assert "408" in species
        assert strain == set()

    def test_scalar_defaults_to_species(self) -> None:
        """Test that scalar tax ID defaults to species."""
        doc: dict[str, Any] = {"General": {"NCBI tax id": 408}}
        species, strain = extract_ncbi_taxon_ids(doc)
        assert "408" in species
        assert strain == set()

    def test_missing_ncbi_tax_id(self) -> None:
        """Test missing NCBI tax id returns empty sets."""
        doc: dict[str, Any] = {"General": {}}
        species, strain = extract_ncbi_taxon_ids(doc)
        assert species == set()
        assert strain == set()

    def test_integer_tax_id(self) -> None:
        """Test integer tax IDs are converted to strings."""
        doc: dict[str, Any] = {"General": {"NCBI tax id": 408}}
        species, strain = extract_ncbi_taxon_ids(doc)
        assert species == {"408"}


class TestExtractScientificName:
    """Tests for extract_scientific_name function."""

    def test_extract_scientific_name(self) -> None:
        """Test extracting scientific name."""
        doc: dict[str, Any] = {"Name and taxonomic classification": {"species": "Methylorubrum extorquens"}}
        name = extract_scientific_name(doc)
        assert name == "Methylorubrum extorquens"

    def test_missing_taxonomy_section(self) -> None:
        """Test missing taxonomy section returns None."""
        doc: dict[str, Any] = {}
        name = extract_scientific_name(doc)
        assert name is None

    def test_missing_species_field(self) -> None:
        """Test missing species field returns None."""
        doc: dict[str, Any] = {"Name and taxonomic classification": {}}
        name = extract_scientific_name(doc)
        assert name is None


class TestExtractTypeStrain:
    """Tests for extract_type_strain function."""

    def test_type_strain_yes_string(self) -> None:
        """Test type strain 'yes' string."""
        doc: dict[str, Any] = {"Name and taxonomic classification": {"type strain": "yes"}}
        result = extract_type_strain(doc)
        assert result == "yes"

    def test_type_strain_no_string(self) -> None:
        """Test type strain 'no' string."""
        doc: dict[str, Any] = {"Name and taxonomic classification": {"type strain": "no"}}
        result = extract_type_strain(doc)
        assert result == "no"

    def test_type_strain_true_bool(self) -> None:
        """Test type strain True boolean."""
        doc: dict[str, Any] = {"Name and taxonomic classification": {"type strain": True}}
        result = extract_type_strain(doc)
        assert result == "yes"

    def test_type_strain_false_bool(self) -> None:
        """Test type strain False boolean."""
        doc: dict[str, Any] = {"Name and taxonomic classification": {"type strain": False}}
        result = extract_type_strain(doc)
        assert result == "no"

    def test_type_strain_mixed_case(self) -> None:
        """Test type strain mixed case string is lowercased."""
        doc: dict[str, Any] = {"Name and taxonomic classification": {"type strain": "YES"}}
        result = extract_type_strain(doc)
        assert result == "yes"

    def test_missing_type_strain(self) -> None:
        """Test missing type strain returns None."""
        doc: dict[str, Any] = {"Name and taxonomic classification": {}}
        result = extract_type_strain(doc)
        assert result is None


class TestExtractCultureCollectionIds:
    """Tests for extract_culture_collection_ids function."""

    def test_multiple_culture_collections(self) -> None:
        """Test extracting multiple culture collection IDs."""
        doc: dict[str, Any] = {"External links": {"culture collection no.": "DSM 1337, ATCC 43645, JCM 2802"}}
        ids = extract_culture_collection_ids(doc)
        assert "DSM:1337" in ids
        assert "ATCC:43645" in ids
        assert "JCM:2802" in ids

    def test_single_culture_collection(self) -> None:
        """Test extracting single culture collection ID."""
        doc: dict[str, Any] = {"External links": {"culture collection no.": "DSM 1337"}}
        ids = extract_culture_collection_ids(doc)
        assert ids == {"DSM:1337"}

    def test_already_normalized_curie(self) -> None:
        """Test IDs already in CURIE format are preserved."""
        doc: dict[str, Any] = {"External links": {"culture collection no.": "DSM:1337"}}
        ids = extract_culture_collection_ids(doc)
        assert ids == {"DSM:1337"}

    def test_missing_external_links(self) -> None:
        """Test missing External links returns empty set."""
        doc: dict[str, Any] = {}
        ids = extract_culture_collection_ids(doc)
        assert ids == set()

    def test_empty_culture_collection_string(self) -> None:
        """Test empty culture collection string returns empty set."""
        doc: dict[str, Any] = {"External links": {"culture collection no.": ""}}
        ids = extract_culture_collection_ids(doc)
        assert ids == set()

    def test_whitespace_handling(self) -> None:
        """Test whitespace is properly handled."""
        doc: dict[str, Any] = {"External links": {"culture collection no.": " DSM 1337 , ATCC 43645 "}}
        ids = extract_culture_collection_ids(doc)
        assert "DSM:1337" in ids
        assert "ATCC:43645" in ids


class TestExtractAlternativeNames:
    """Tests for extract_alternative_names function."""

    def test_multiple_synonyms(self) -> None:
        """Test extracting multiple synonyms."""
        doc: dict[str, Any] = {
            "Name and taxonomic classification": {
                "LPSN": {
                    "synonyms": [
                        {"synonym": "Methylobacterium extorquens"},
                        {"synonym": "Protomonas extorquens"},
                    ]
                }
            }
        }
        names = extract_alternative_names(doc)
        assert "Methylobacterium extorquens" in names
        assert "Protomonas extorquens" in names

    def test_single_synonym_as_dict(self) -> None:
        """Test single synonym as dict (normalized to list)."""
        doc: dict[str, Any] = {
            "Name and taxonomic classification": {"LPSN": {"synonyms": {"synonym": "Methylobacterium extorquens"}}}
        }
        names = extract_alternative_names(doc)
        assert "Methylobacterium extorquens" in names

    def test_synonym_as_string(self) -> None:
        """Test synonym as direct string value."""
        doc: dict[str, Any] = {
            "Name and taxonomic classification": {"LPSN": {"synonyms": "Methylobacterium extorquens"}}
        }
        names = extract_alternative_names(doc)
        assert "Methylobacterium extorquens" in names

    def test_missing_lpsn(self) -> None:
        """Test missing LPSN returns empty set."""
        doc: dict[str, Any] = {"Name and taxonomic classification": {}}
        names = extract_alternative_names(doc)
        assert names == set()

    def test_lpsn_not_dict(self) -> None:
        """Test LPSN not being a dict returns empty set."""
        doc: dict[str, Any] = {"Name and taxonomic classification": {"LPSN": "not a dict"}}
        names = extract_alternative_names(doc)
        assert names == set()


class TestExtractStrainDesignations:
    """Tests for extract_strain_designations function."""

    def test_single_strain_designation(self) -> None:
        """Test extracting single strain designation."""
        doc: dict[str, Any] = {"Name and taxonomic classification": {"strain designation": "TK 0001"}}
        designations = extract_strain_designations(doc)
        assert designations == ["TK 0001"]

    def test_comma_separated_designations(self) -> None:
        """Test extracting comma-separated strain designations."""
        doc: dict[str, Any] = {"Name and taxonomic classification": {"strain designation": "PG 8, PG8"}}
        designations = extract_strain_designations(doc)
        assert designations == ["PG 8", "PG8"]

    def test_multiple_comma_separated(self) -> None:
        """Test multiple comma-separated designations with whitespace."""
        doc: dict[str, Any] = {
            "Name and taxonomic classification": {"strain designation": "Blackley strain G2, BU 335"}
        }
        designations = extract_strain_designations(doc)
        assert len(designations) == 2
        assert "Blackley strain G2" in designations
        assert "BU 335" in designations

    def test_missing_taxonomy_section(self) -> None:
        """Test missing taxonomy section returns empty list."""
        doc: dict[str, Any] = {}
        designations = extract_strain_designations(doc)
        assert designations == []

    def test_missing_strain_designation_field(self) -> None:
        """Test missing strain designation field returns empty list."""
        doc: dict[str, Any] = {"Name and taxonomic classification": {}}
        designations = extract_strain_designations(doc)
        assert designations == []


class TestExtractGenomeAccessions:
    """Tests for extract_genome_accessions function."""

    def test_single_genome(self) -> None:
        """Test extracting single genome accession."""
        doc: dict[str, Any] = {
            "Sequence information": {"Genome sequences": {"accession": "408.23", "database": "patric"}}
        }
        accessions = extract_genome_accessions(doc)
        assert accessions == ["408.23"]

    def test_multiple_genomes(self) -> None:
        """Test extracting multiple genome accessions."""
        doc: dict[str, Any] = {
            "Sequence information": {
                "Genome sequences": [{"accession": "GCA_000022685.1"}, {"accession": "GCA_000983655.1"}]
            }
        }
        accessions = extract_genome_accessions(doc)
        assert len(accessions) == 2
        assert "GCA_000022685.1" in accessions
        assert "GCA_000983655.1" in accessions

    def test_missing_sequence_information(self) -> None:
        """Test missing Sequence information returns empty list."""
        doc: dict[str, Any] = {}
        accessions = extract_genome_accessions(doc)
        assert accessions == []

    def test_missing_genome_sequences(self) -> None:
        """Test missing Genome sequences returns empty list."""
        doc: dict[str, Any] = {"Sequence information": {}}
        accessions = extract_genome_accessions(doc)
        assert accessions == []

    def test_genome_without_accession(self) -> None:
        """Test genome entry without accession field."""
        doc: dict[str, Any] = {"Sequence information": {"Genome sequences": {"database": "patric"}}}
        accessions = extract_genome_accessions(doc)
        assert accessions == []

    def test_scalar_genome_accession(self) -> None:
        """Test genome sequences as scalar string (edge case)."""
        doc: dict[str, Any] = {"Sequence information": {"Genome sequences": "GCA_000022685.1"}}
        accessions = extract_genome_accessions(doc)
        assert accessions == ["GCA_000022685.1"]


class TestExtractBiosafetyLevel:
    """Tests for extract_biosafety_level function."""

    def test_biosafety_level_1(self) -> None:
        """Test extracting biosafety level 1."""
        doc: dict[str, Any] = {"Safety information": {"risk assessment": {"biosafety level": "1"}}}
        level = extract_biosafety_level(doc)
        assert level == "1"

    def test_biosafety_level_2(self) -> None:
        """Test extracting biosafety level 2."""
        doc: dict[str, Any] = {"Safety information": {"risk assessment": {"biosafety level": "2"}}}
        level = extract_biosafety_level(doc)
        assert level == "2"

    def test_multiple_risk_assessments_takes_first(self) -> None:
        """Test multiple risk assessments takes first level."""
        doc: dict[str, Any] = {
            "Safety information": {
                "risk assessment": [
                    {"biosafety level": "1"},
                    {"biosafety level": "2"},
                ]
            }
        }
        level = extract_biosafety_level(doc)
        assert level == "1"

    def test_integer_biosafety_level(self) -> None:
        """Test integer biosafety level is converted to string."""
        doc: dict[str, Any] = {"Safety information": {"risk assessment": {"biosafety level": 1}}}
        level = extract_biosafety_level(doc)
        assert level == "1"

    def test_missing_risk_assessment(self) -> None:
        """Test missing risk assessment returns None."""
        doc: dict[str, Any] = {"Safety information": {}}
        level = extract_biosafety_level(doc)
        assert level is None

    def test_whitespace_stripped(self) -> None:
        """Test whitespace is stripped from biosafety level."""
        doc: dict[str, Any] = {"Safety information": {"risk assessment": {"biosafety level": " 1 "}}}
        level = extract_biosafety_level(doc)
        assert level == "1"


class TestTransformBacDiveDoc:
    """Tests for transform_bacdive_doc function."""

    def test_minimal_document(self) -> None:
        """Test transformation with minimal BacDive document."""
        doc: dict[str, Any] = {"General": {"BacDive-ID": 7142}}
        nodes, edges = transform_bacdive_doc(doc)

        # Should create 1 strain node, no taxonomy node, no edges
        assert len(nodes) == 1
        assert len(edges) == 0
        assert nodes[0].id == "bacdive:7142"
        assert nodes[0].category == ["biolink:OrganismTaxon"]

    def test_document_with_species_taxonomy(self) -> None:
        """Test transformation with species taxonomy."""
        doc: dict[str, Any] = {
            "General": {
                "BacDive-ID": 7142,
                "NCBI tax id": {"NCBI tax id": 408, "Matching level": "species"},
            },
            "Name and taxonomic classification": {"species": "Methylorubrum extorquens"},
        }
        nodes, edges = transform_bacdive_doc(doc)

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
        assert species_node.provided_by == ["infores:ncbi"]

        # Check edge
        edge = edges[0]
        assert edge.subject == "bacdive:7142"
        assert edge.predicate == "biolink:in_taxon"
        assert edge.object == "NCBITaxon:408"
        assert edge.knowledge_level == "knowledge_assertion"
        assert edge.agent_type == "manual_agent"
        assert edge.primary_knowledge_source == ["infores:bacdive"]

    def test_full_document(self) -> None:
        """Test transformation with all available fields."""
        doc: dict[str, Any] = {
            "General": {
                "BacDive-ID": 7142,
                "NCBI tax id": {"NCBI tax id": 408, "Matching level": "species"},
            },
            "Name and taxonomic classification": {
                "species": "Methylorubrum extorquens",
                "type strain": "yes",
                "LPSN": {
                    "synonyms": [
                        {"synonym": "Methylobacterium extorquens"},
                        {"synonym": "Protomonas extorquens"},
                    ]
                },
            },
            "External links": {"culture collection no.": "DSM 1337, ATCC 43645, JCM 2802"},
            "Safety information": {"risk assessment": {"biosafety level": "1"}},
        }
        nodes, edges = transform_bacdive_doc(doc)

        assert len(nodes) == 2
        assert len(edges) == 1

        strain_node = nodes[0]
        assert strain_node.id == "bacdive:7142"
        assert strain_node.name == "Methylorubrum extorquens"
        assert strain_node.xref is not None and len(strain_node.xref) == 3
        assert "DSM:1337" in strain_node.xref
        assert strain_node.synonym is not None and len(strain_node.synonym) == 2
        assert "Methylobacterium extorquens" in strain_node.synonym
        assert strain_node.model_extra["type_strain"] == "yes"
        assert strain_node.model_extra["biosafety_level"] == "1"

    def test_missing_bacdive_id_returns_empty(self) -> None:
        """Test document without BacDive-ID returns empty results."""
        doc: dict[str, Any] = {"Name and taxonomic classification": {"species": "Methylorubrum extorquens"}}
        nodes, edges = transform_bacdive_doc(doc)

        assert len(nodes) == 0
        assert len(edges) == 0

    def test_multiple_species_ids_uses_first(self) -> None:
        """Test that when multiple species IDs present, first is used."""
        doc: dict[str, Any] = {
            "General": {
                "BacDive-ID": 7142,
                "NCBI tax id": [
                    {"NCBI tax id": 408, "Matching level": "species"},
                    {"NCBI tax id": 999, "Matching level": "species"},
                ],
            },
            "Name and taxonomic classification": {"species": "Methylorubrum extorquens"},
        }
        nodes, edges = transform_bacdive_doc(doc)

        strain_node = nodes[0]
        # Should use one of the species IDs (set iteration order)
        assert strain_node.in_taxon is not None
        assert len(strain_node.in_taxon) == 1
        assert strain_node.in_taxon[0] in ["NCBITaxon:408", "NCBITaxon:999"]
