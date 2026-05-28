"""Tests for OLS client data structures."""

from cmm_ai_automation.clients.ols import ChEBITerm, OLSSearchResult


class TestChEBITerm:
    """Tests for ChEBITerm dataclass."""

    def test_create_minimal_term(self) -> None:
        """Test creating ChEBI term with minimal fields."""
        term = ChEBITerm(chebi_id="CHEBI:17634")
        assert term.chebi_id == "CHEBI:17634"
        assert term.label is None
        assert term.description is None
        assert term.synonyms == []
        assert term.is_obsolete is False

    def test_create_full_term(self) -> None:
        """Test creating ChEBI term with all fields."""
        term = ChEBITerm(
            chebi_id="CHEBI:17634",
            label="D-glucose",
            description="A glucose with D-configuration",
            synonyms=["glucose", "dextrose", "grape sugar"],
            inchikey="WQZGKKKJIJFFOK-GASJEMHNSA-N",
            inchi="InChI=1S/C6H12O6/c7-1-2-3(8)4(9)5(10)6(11)12-2/h2-11H,1H2/t2-,3-,4+,5-,6+/m1/s1",
            smiles="OC[C@H]1OC(O)[C@H](O)[C@@H](O)[C@@H]1O",
            formula="C6H12O6",
            mass=180.156,
            charge=0,
            star=3,
            is_obsolete=False,
            parent_ids=["CHEBI:4167"],
            has_role=["CHEBI:26191", "CHEBI:35381"],
            has_functional_parent=["CHEBI:5686"],
            xrefs={"KEGG": ["C00031"], "CAS": ["50-99-7"]},
        )

        assert term.chebi_id == "CHEBI:17634"
        assert term.label == "D-glucose"
        assert term.description == "A glucose with D-configuration"
        assert len(term.synonyms) == 3
        assert "glucose" in term.synonyms
        assert term.inchikey == "WQZGKKKJIJFFOK-GASJEMHNSA-N"
        assert term.formula == "C6H12O6"
        assert term.mass == 180.156
        assert term.charge == 0
        assert term.star == 3
        assert term.is_obsolete is False
        assert "CHEBI:4167" in term.parent_ids
        assert len(term.has_role) == 2
        assert term.xrefs["KEGG"] == ["C00031"]

    def test_to_dict_minimal(self) -> None:
        """Test converting minimal term to dictionary."""
        term = ChEBITerm(chebi_id="CHEBI:12345")
        d = term.to_dict()

        assert d["chebi_id"] == "CHEBI:12345"
        assert d["label"] is None
        assert d["synonyms"] == []
        assert d["parent_ids"] == []
        assert d["xrefs"] == {}

    def test_to_dict_full(self) -> None:
        """Test converting full term to dictionary."""
        term = ChEBITerm(
            chebi_id="CHEBI:17634",
            label="D-glucose",
            synonyms=["glucose", "dextrose"],
            formula="C6H12O6",
            mass=180.156,
            charge=0,
            star=3,
            parent_ids=["CHEBI:4167"],
            xrefs={"KEGG": ["C00031"]},
        )
        d = term.to_dict()

        assert d["chebi_id"] == "CHEBI:17634"
        assert d["label"] == "D-glucose"
        assert d["synonyms"] == ["glucose", "dextrose"]
        assert d["formula"] == "C6H12O6"
        assert d["mass"] == 180.156
        assert d["charge"] == 0
        assert d["star"] == 3
        assert d["parent_ids"] == ["CHEBI:4167"]
        assert d["xrefs"] == {"KEGG": ["C00031"]}

    def test_obsolete_term(self) -> None:
        """Test marking term as obsolete."""
        term = ChEBITerm(chebi_id="CHEBI:99999", is_obsolete=True)
        assert term.is_obsolete is True

        d = term.to_dict()
        assert d["is_obsolete"] is True

    def test_term_with_multiple_parents(self) -> None:
        """Test term with multiple parent IDs."""
        term = ChEBITerm(
            chebi_id="CHEBI:12345",
            parent_ids=["CHEBI:1", "CHEBI:2", "CHEBI:3"],
        )
        assert len(term.parent_ids) == 3
        assert "CHEBI:1" in term.parent_ids
        assert "CHEBI:2" in term.parent_ids
        assert "CHEBI:3" in term.parent_ids

    def test_term_with_roles(self) -> None:
        """Test term with role classifications."""
        term = ChEBITerm(
            chebi_id="CHEBI:12345",
            has_role=["CHEBI:role1", "CHEBI:role2"],
            has_functional_parent=["CHEBI:fp1"],
        )
        assert len(term.has_role) == 2
        assert len(term.has_functional_parent) == 1

    def test_term_with_xrefs(self) -> None:
        """Test term with cross-references to other databases."""
        term = ChEBITerm(
            chebi_id="CHEBI:12345",
            xrefs={
                "KEGG": ["C00031", "C00032"],
                "CAS": ["50-99-7"],
                "PubChem": ["5793"],
            },
        )
        assert len(term.xrefs) == 3
        assert len(term.xrefs["KEGG"]) == 2
        assert term.xrefs["CAS"] == ["50-99-7"]


class TestOLSSearchResult:
    """Tests for OLSSearchResult dataclass."""

    def test_create_minimal_result(self) -> None:
        """Test creating search result with minimal fields."""
        result = OLSSearchResult(
            iri="http://purl.obolibrary.org/obo/CHEBI_17634",
            label=None,
            short_form="CHEBI_17634",
            ontology_name="chebi",
        )
        assert result.iri == "http://purl.obolibrary.org/obo/CHEBI_17634"
        assert result.label is None
        assert result.short_form == "CHEBI_17634"
        assert result.ontology_name == "chebi"
        assert result.description is None
        assert result.is_obsolete is False

    def test_create_full_result(self) -> None:
        """Test creating search result with all fields."""
        result = OLSSearchResult(
            iri="http://purl.obolibrary.org/obo/CHEBI_17634",
            label="D-glucose",
            short_form="CHEBI_17634",
            ontology_name="chebi",
            description="A glucose with D-configuration",
            is_obsolete=False,
        )
        assert result.label == "D-glucose"
        assert result.description == "A glucose with D-configuration"
        assert result.is_obsolete is False

    def test_curie_property(self) -> None:
        """Test curie property converts short_form to CURIE format."""
        result = OLSSearchResult(
            iri="http://example.org",
            label="Test",
            short_form="CHEBI_17634",
            ontology_name="chebi",
        )
        assert result.curie == "CHEBI:17634"

    def test_curie_with_different_ontologies(self) -> None:
        """Test CURIE conversion for different ontologies."""
        test_cases = [
            ("CHEBI_17634", "CHEBI:17634"),
            ("GO_0008150", "GO:0008150"),
            ("NCBITaxon_9606", "NCBITaxon:9606"),
            ("UBERON_0000955", "UBERON:0000955"),
        ]
        for short_form, expected_curie in test_cases:
            result = OLSSearchResult(
                iri="http://example.org",
                label="Test",
                short_form=short_form,
                ontology_name="test",
            )
            assert result.curie == expected_curie

    def test_obsolete_result(self) -> None:
        """Test marking search result as obsolete."""
        result = OLSSearchResult(
            iri="http://example.org",
            label="Obsolete term",
            short_form="CHEBI_99999",
            ontology_name="chebi",
            is_obsolete=True,
        )
        assert result.is_obsolete is True

    def test_result_from_different_ontologies(self) -> None:
        """Test search results from different ontologies."""
        ontologies = ["chebi", "go", "uberon", "ncbitaxon", "pr"]
        for onto in ontologies:
            result = OLSSearchResult(
                iri=f"http://purl.obolibrary.org/obo/{onto.upper()}_12345",
                label="Test term",
                short_form=f"{onto.upper()}_12345",
                ontology_name=onto,
            )
            assert result.ontology_name == onto
            assert onto.upper() in result.curie

    def test_result_with_long_description(self) -> None:
        """Test search result with long description."""
        long_desc = "This is a very long description " * 20
        result = OLSSearchResult(
            iri="http://example.org",
            label="Test",
            short_form="CHEBI_12345",
            ontology_name="chebi",
            description=long_desc,
        )
        assert result.description == long_desc
        assert len(result.description) > 100
