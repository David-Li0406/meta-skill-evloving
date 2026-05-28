"""Pure functions specs (turtle builders, SPARQL parsers, prompt builders)."""

import pytest

from script.clients import escape_sparql
from script.prompt_builders import (
    build_claim_relations_prompt,
    build_extraction_prompt,
    build_ref_claims_context,
    format_claim_line,
    format_ref_claim_line,
)
from script.sparql_parsers import (
    parse_extraction_concepts,
    parse_sparql_claims_result,
    parse_sparql_concept_results,
    parse_sparql_count_result,
    validate_claim_relations,
)
from script.turtle_builders import (
    build_cites_turtle,
    build_claim_turtle,
    build_concept_turtle,
    build_new_concept_turtle,
    build_relation_turtle,
    expand_prefixed_uri,
    format_uri_ref,
)

# --- URI and String Formatting ---

class TestFormatUriRef:
    @pytest.mark.parametrize("uri,expected", [
        ("https://example.org/x", "<https://example.org/x>"),
        ("paper:co_abc", "paper:co_abc"),
        ("http://example.org/x", "http://example.org/x"),  # only https gets brackets
    ])
    def test_format(self, uri, expected):
        assert format_uri_ref(uri) == expected


class TestExpandPrefixedUri:
    @pytest.mark.parametrize("uri,expected", [
        ("paper:co_abc", "https://kg.corca.ai/paper#co_abc"),
        ("paper:cl_xyz", "https://kg.corca.ai/paper#cl_xyz"),
        ("paper:pa_123", "https://kg.corca.ai/paper#pa_123"),
        ("https://kg.corca.ai/paper#co_abc", "https://kg.corca.ai/paper#co_abc"),
        ("https://example.org/other", "https://example.org/other"),
        ("unknown:prefix", "unknown:prefix"),  # non-paper prefix unchanged
    ])
    def test_expand(self, uri, expected):
        assert expand_prefixed_uri(uri) == expected


class TestEscapeSparql:
    @pytest.mark.parametrize("input,expected", [
        ("hello world", "hello world"),
        ('say "hello"', 'say \\"hello\\"'),
        ("line1\nline2", "line1\\nline2"),
        ("path\\file", "path\\\\file"),
        ('He said "hi"\nbye', 'He said \\"hi\\"\\nbye'),
        (None, ""),
    ])
    def test_escape(self, input, expected):
        assert escape_sparql(input) == expected


# --- Turtle Building ---

class TestBuildConceptTurtle:
    def test_full_uri(self):
        turtle = build_concept_turtle("https://kg.corca.ai/paper#co_abc", "A description")
        assert "<https://kg.corca.ai/paper#co_abc>" in turtle
        assert 'rdfs:comment "A description"' in turtle

    def test_prefixed_uri(self):
        turtle = build_concept_turtle("paper:co_abc", "Desc")
        assert "paper:co_abc rdfs:comment" in turtle


class TestBuildNewConceptTurtle:
    def test_minimal(self):
        turtle = build_new_concept_turtle("paper:co_1", "Attention")
        assert "paper:co_1 a paper:Concept" in turtle
        assert 'rdfs:label "Attention"' in turtle
        assert "rdfs:comment" not in turtle

    def test_with_description(self):
        turtle = build_new_concept_turtle("paper:co_1", "Attention", "A mechanism")
        assert 'rdfs:label "Attention"' in turtle
        assert 'rdfs:comment "A mechanism"' in turtle

    def test_with_paper_uri(self):
        turtle = build_new_concept_turtle(
            "paper:co_1", "Attention", paper_uri="https://kg.corca.ai/paper#pa_1"
        )
        assert "<https://kg.corca.ai/paper#pa_1> paper:about paper:co_1" in turtle


class TestBuildCitesTurtle:
    def test_full_uris(self):
        turtle = build_cites_turtle(
            "https://kg.corca.ai/paper#pa_1",
            "https://kg.corca.ai/paper#pa_2"
        )
        assert "<https://kg.corca.ai/paper#pa_1>" in turtle
        assert "paper:cites" in turtle

    def test_prefixed_uris(self):
        turtle = build_cites_turtle("paper:pa_1", "paper:pa_2")
        assert "paper:pa_1 paper:cites paper:pa_2" in turtle


class TestBuildRelationTurtle:
    @pytest.mark.parametrize("from_uri,rel,to_uri,expected", [
        ("paper:cl_1", "extends", "paper:cl_2", "paper:cl_1 paper:extends paper:cl_2"),
        ("https://x.org/c1", "broader", "https://x.org/c2", "<https://x.org/c1>"),
    ])
    def test_relation(self, from_uri, rel, to_uri, expected):
        turtle = build_relation_turtle(from_uri, rel, to_uri)
        assert expected in turtle


class TestBuildClaimTurtle:
    def test_basic_claim(self):
        turtle = build_claim_turtle("paper:cl_1", "paper:pa_1", "Claim text")
        assert "paper:cl_1 a paper:Claim" in turtle
        assert 'rdfs:label "Claim text"' in turtle
        assert "paper:pa_1 paper:hasClaim paper:cl_1" in turtle

    def test_with_concepts(self):
        turtle = build_claim_turtle("paper:cl_1", "paper:pa_1", "Text", ["paper:co_1", "paper:co_2"])
        assert "paper:cl_1 paper:regarding paper:co_1" in turtle
        assert "paper:cl_1 paper:regarding paper:co_2" in turtle

    def test_without_concepts(self):
        turtle = build_claim_turtle("paper:cl_1", "paper:pa_1", "Text", None)
        assert "paper:regarding" not in turtle


# --- SPARQL Result Parsing ---

class TestParseSparqlConceptResults:
    def test_empty(self):
        assert parse_sparql_concept_results([]) == []

    def test_parses_fields(self):
        results = [{
            'uri': {'value': 'https://example.org/c1'},
            'name': {'value': 'Concept'},
            'title': {'value': 'Paper'},
            'abstract': {'value': 'Abstract'},
        }]
        parsed = parse_sparql_concept_results(results)
        assert parsed[0]['uri'] == 'https://example.org/c1'
        assert parsed[0]['name'] == 'Concept'


class TestParseSparqlClaimsResult:
    def test_empty(self):
        assert parse_sparql_claims_result([]) == []

    def test_parses_claims(self):
        results = [
            {'claim': {'value': 'u1'}, 'text': {'value': 'C1'}},
            {'claim': {'value': 'u2'}, 'text': {'value': 'C2'}},
        ]
        parsed = parse_sparql_claims_result(results)
        assert len(parsed) == 2
        assert parsed[0] == {'uri': 'u1', 'text': 'C1'}


class TestParseSparqlCountResult:
    @pytest.mark.parametrize("results,expected", [
        ([{'count': {'value': '42'}}], 42),
        ([{'count': {'value': '0'}}], 0),
        ([], 0),
        ([{'other': {'value': '5'}}], 0),
    ])
    def test_count(self, results, expected):
        assert parse_sparql_count_result(results) == expected


# --- Prompt Building ---

class TestFormatClaimLine:
    def test_format(self):
        claim = {'uri': 'https://x.org/cl1', 'text': 'The model works'}
        assert format_claim_line(claim) == '- [https://x.org/cl1] "The model works"'


class TestFormatRefClaimLine:
    @pytest.mark.parametrize("ref,expected", [
        ({'claim_uri': 'u1', 'claim_text': 'C', 'paper_year': 2020}, '- [u1] (2020) "C"'),
        ({'claim_uri': 'u1', 'claim_text': 'C'}, '- [u1] "C"'),
        ({'claim_uri': 'u1', 'claim_text': 'C', 'paper_year': None}, '- [u1] "C"'),
    ])
    def test_format(self, ref, expected):
        assert format_ref_claim_line(ref) == expected


class TestBuildRefClaimsContext:
    def test_empty(self):
        assert build_ref_claims_context([]) == ""

    def test_formats_claims(self):
        claims = [{'claim_uri': 'u1', 'claim_text': 'Text'}]
        ctx = build_ref_claims_context(claims)
        assert "Claims from papers this paper cites:" in ctx
        assert '[u1] "Text"' in ctx

    def test_respects_limit(self):
        claims = [{'claim_uri': f'u{i}', 'claim_text': f'T{i}'} for i in range(30)]
        ctx = build_ref_claims_context(claims, limit=5)
        assert '[u4]' in ctx
        assert '[u5]' not in ctx


class TestBuildClaimRelationsPrompt:
    def test_includes_all_parts(self):
        prompt = build_claim_relations_prompt(
            [{'uri': 'u1', 'text': 'My claim'}],
            [{'claim_uri': 'r1', 'claim_text': 'Ref claim', 'paper_year': 2019}],
            2020, "DEFINITIONS"
        )
        assert '[u1] "My claim"' in prompt
        assert '[r1] (2019) "Ref claim"' in prompt
        assert "(2020)" in prompt
        assert "DEFINITIONS" in prompt

    def test_no_year_suffix_when_none(self):
        prompt = build_claim_relations_prompt(
            [{'uri': 'u', 'text': 't'}], [], None, "DEFS"
        )
        assert "This paper's claims:" in prompt


class TestBuildExtractionPrompt:
    def test_includes_paper_info(self):
        prompt = build_extraction_prompt("Title", "Abstract", 2021, "", "DEFS")
        assert "Title" in prompt
        assert "Abstract" in prompt
        assert "Year: 2021" in prompt

    def test_none_year_shows_unknown(self):
        prompt = build_extraction_prompt("T", "A", None, "", "DEFS")
        assert "Year: Unknown" in prompt

    def test_includes_ref_claims_context(self):
        prompt = build_extraction_prompt("T", "A", 2020, "\n\nRef claims here", "DEFS")
        assert "Ref claims here" in prompt

    def test_includes_structure(self):
        prompt = build_extraction_prompt("T", "A", 2020, "", "DEFS")
        assert "## Concepts" in prompt
        assert "## Claims" in prompt
        assert "broader" in prompt
        assert "regarding" in prompt


# --- Validation ---

class TestValidateClaimRelations:
    def test_valid_relations(self):
        relations = [
            {'from_uri': 'u1', 'type': 'extends', 'to_uri': 'r1'},
            {'from_uri': 'u2', 'type': 'supports', 'to_uri': 'r2'},
        ]
        valid, invalid = validate_claim_relations(relations, {'u1', 'u2'}, {'r1', 'r2'})
        assert len(valid) == 2
        assert invalid == 0
        assert valid[0] == {'from': 'u1', 'type': 'extends', 'to': 'r1'}

    def test_filters_invalid_uris(self):
        relations = [
            {'from_uri': 'u1', 'type': 'extends', 'to_uri': 'r1'},  # valid
            {'from_uri': 'bad', 'type': 'refutes', 'to_uri': 'r1'},  # bad from
            {'from_uri': 'u1', 'type': 'supports', 'to_uri': 'bad'},  # bad to
        ]
        valid, invalid = validate_claim_relations(relations, {'u1'}, {'r1'})
        assert len(valid) == 1
        assert invalid == 2

    def test_empty(self):
        valid, invalid = validate_claim_relations([], {'u1'}, {'r1'})
        assert valid == []
        assert invalid == 0


# --- Extraction Parsing ---

class TestParseExtractionConcepts:
    def test_empty(self):
        concepts, relations = parse_extraction_concepts([])
        assert concepts == {}
        assert relations == []

    def test_concept_without_relations(self):
        raw = [{'name': 'CNN', 'description': 'A neural network',
                'broader': None, 'partOf': None, 'dependsOn': None}]
        concepts, relations = parse_extraction_concepts(raw)
        assert concepts == {'CNN': 'A neural network'}
        assert relations == []

    def test_concept_with_relations(self):
        raw = [{'name': 'Attention', 'description': 'Mechanism',
                'broader': 'Mechanism', 'partOf': 'Transformer', 'dependsOn': None}]
        concepts, relations = parse_extraction_concepts(raw)
        assert len(relations) == 2
        assert {r['type'] for r in relations} == {'broader', 'partOf'}

    def test_multiple_concepts(self):
        raw = [
            {'name': 'A', 'description': 'DA', 'broader': None, 'partOf': None, 'dependsOn': None},
            {'name': 'B', 'description': 'DB', 'broader': 'A', 'partOf': None, 'dependsOn': None},
        ]
        concepts, relations = parse_extraction_concepts(raw)
        assert len(concepts) == 2
        assert len(relations) == 1

    def test_missing_description(self):
        raw = [{'name': 'X', 'broader': None, 'partOf': None, 'dependsOn': None}]
        concepts, _ = parse_extraction_concepts(raw)
        assert concepts == {'X': None}
