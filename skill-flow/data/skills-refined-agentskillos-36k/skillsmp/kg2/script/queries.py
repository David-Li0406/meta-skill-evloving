"""SPARQL queries for kg2 operations.

All SPARQL queries are centralized here for easier maintenance,
testing, and preventing injection vulnerabilities.
"""

from .clients import escape_sparql
from .turtle_builders import format_uri_ref

# --- Paper Queries ---

def find_paper_by_doi(doi: str) -> str:
    """Find paper URI by DOI."""
    return f'''
        PREFIX paper: <https://kg.corca.ai/paper#>
        SELECT ?uri WHERE {{ ?uri paper:doi "{doi}" }}
    '''


def find_paper_by_arxiv(arxiv_id: str) -> str:
    """Find paper URI by arXiv ID."""
    return f'''
        PREFIX paper: <https://kg.corca.ai/paper#>
        SELECT ?uri WHERE {{ ?uri paper:arxivId "{arxiv_id}" }}
    '''


def find_paper_by_s2_id(s2_id: str) -> str:
    """Find paper URI by Semantic Scholar ID."""
    return f'''
        PREFIX paper: <https://kg.corca.ai/paper#>
        SELECT ?uri WHERE {{ ?uri paper:semanticScholarId "{s2_id}" }}
    '''


# --- Author Queries ---

def find_author_by_orcid(orcid: str) -> str:
    """Find author URI by ORCID."""
    return f'''
        PREFIX paper: <https://kg.corca.ai/paper#>
        SELECT ?uri WHERE {{
            ?uri a paper:Author ;
                 paper:orcidId "{orcid}" .
        }}
    '''


def find_author_by_s2_id(author_id: str) -> str:
    """Find author URI by Semantic Scholar Author ID."""
    return f'''
        PREFIX paper: <https://kg.corca.ai/paper#>
        SELECT ?uri WHERE {{
            ?uri a paper:Author ;
                 paper:semanticScholarAuthorId "{author_id}" .
        }}
    '''


# --- Venue Queries ---

def find_venue_by_s2_id(venue_id: str) -> str:
    """Find venue URI by Semantic Scholar Venue ID."""
    return f'''
        PREFIX paper: <https://kg.corca.ai/paper#>
        SELECT ?uri WHERE {{
            ?uri a paper:Venue ;
                 paper:semanticScholarVenueId "{venue_id}" .
        }}
    '''


def find_venue_by_name(name: str) -> str:
    """Find venue URI by name."""
    return f'''
        PREFIX paper: <https://kg.corca.ai/paper#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        SELECT ?uri WHERE {{
            ?uri a paper:Venue ;
                 rdfs:label "{escape_sparql(name)}" .
        }}
    '''


# --- Concept Queries ---

def find_concept_by_name(name: str) -> str:
    """Find concept URI and check if it has a description."""
    return f'''
        PREFIX paper: <https://kg.corca.ai/paper#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        SELECT ?uri ?comment WHERE {{
            ?uri a paper:Concept ;
                 rdfs:label "{escape_sparql(name)}" .
            OPTIONAL {{ ?uri rdfs:comment ?comment }}
        }}
    '''


def count_concepts() -> str:
    """Count total concepts."""
    return '''
        PREFIX paper: <https://kg.corca.ai/paper#>
        SELECT (COUNT(?uri) as ?count) WHERE { ?uri a paper:Concept }
    '''


# --- Claim Queries ---

def get_claims_for_paper(paper_uri: str) -> str:
    """Get claims for a paper."""
    return f'''
        PREFIX paper: <https://kg.corca.ai/paper#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        SELECT ?claim ?text WHERE {{
            {format_uri_ref(paper_uri)} paper:hasClaim ?claim .
            ?claim rdfs:label ?text .
        }}
    '''


# --- Concept Context Queries (for deduplication) ---

def get_concepts_for_paper(paper_uri: str) -> str:
    """Get all concepts mentioned in a paper."""
    return f'''
        PREFIX paper: <https://kg.corca.ai/paper#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        SELECT ?uri ?label WHERE {{
            {format_uri_ref(paper_uri)} paper:about ?uri .
            ?uri a paper:Concept ;
                 rdfs:label ?label .
        }}
    '''


def get_concepts_for_papers(paper_uris: list[str]) -> str:
    """Get all concepts mentioned in multiple papers.

    Returns concepts with uri, label, and optionally comment.
    """
    if not paper_uris:
        return '''
            PREFIX paper: <https://kg.corca.ai/paper#>
            SELECT ?uri ?label ?comment WHERE { VALUES ?uri { } }
        '''

    values = ' '.join(format_uri_ref(uri) for uri in paper_uris)
    return f'''
        PREFIX paper: <https://kg.corca.ai/paper#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        SELECT DISTINCT ?uri ?label ?comment WHERE {{
            VALUES ?paper {{ {values} }}
            ?paper paper:about ?uri .
            ?uri a paper:Concept ;
                 rdfs:label ?label .
            OPTIONAL {{ ?uri rdfs:comment ?comment }}
        }}
    '''


def get_papers_for_concept(concept_uri: str) -> str:
    """Get all papers that mention a concept."""
    return f'''
        PREFIX paper: <https://kg.corca.ai/paper#>
        SELECT ?paper WHERE {{
            ?paper paper:about {format_uri_ref(concept_uri)} .
        }}
    '''


def get_related_papers(paper_uri: str) -> str:
    """Get papers related to this paper (references and citations).

    Returns papers that this paper cites or that cite this paper.
    """
    return f'''
        PREFIX paper: <https://kg.corca.ai/paper#>
        SELECT DISTINCT ?related WHERE {{
            {{
                {format_uri_ref(paper_uri)} paper:cites ?related .
            }} UNION {{
                ?related paper:cites {format_uri_ref(paper_uri)} .
            }}
        }}
    '''


def get_concept_context(concept_uri: str) -> str:
    """Get context for a concept: papers and their references.

    Returns the concept's papers and their related papers (1-hop).
    """
    return f'''
        PREFIX paper: <https://kg.corca.ai/paper#>
        SELECT ?paper ?related WHERE {{
            ?paper paper:about {format_uri_ref(concept_uri)} .
            OPTIONAL {{
                {{ ?paper paper:cites ?related . }}
                UNION
                {{ ?related paper:cites ?paper . }}
            }}
        }}
    '''


def get_all_concepts() -> str:
    """Get all concepts with their labels."""
    return '''
        PREFIX paper: <https://kg.corca.ai/paper#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        SELECT ?uri ?label WHERE {
            ?uri a paper:Concept ;
                 rdfs:label ?label .
        }
    '''


def get_concept_label(concept_uri: str) -> str:
    """Get label for a single concept."""
    return f'''
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        SELECT ?label WHERE {{ <{concept_uri}> rdfs:label ?label }}
    '''


def get_concept_description(concept_uri: str) -> str:
    """Get description (rdfs:comment) for a concept."""
    return f'''
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        SELECT ?comment WHERE {{ <{concept_uri}> rdfs:comment ?comment }}
    '''


# --- Concept Merge Queries ---

def merge_concepts_as_object(keep_uri: str, remove_uri: str) -> str:
    """Move all triples where remove_uri is the object to keep_uri.

    Example: ?paper paper:about remove_uri → ?paper paper:about keep_uri
    """
    keep_ref = format_uri_ref(keep_uri)
    remove_ref = format_uri_ref(remove_uri)
    return f'''
        DELETE {{ ?s ?p {remove_ref} }}
        INSERT {{ ?s ?p {keep_ref} }}
        WHERE {{ ?s ?p {remove_ref} }}
    '''


def merge_concepts_as_subject(keep_uri: str, remove_uri: str) -> str:
    """Move all triples where remove_uri is the subject to keep_uri.

    Example: remove_uri paper:relatedTo ?other → keep_uri paper:relatedTo ?other

    Excludes rdf:type, rdfs:label, rdfs:comment to avoid duplicating metadata.
    """
    keep_ref = format_uri_ref(keep_uri)
    remove_ref = format_uri_ref(remove_uri)
    return f'''
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        DELETE {{ {remove_ref} ?p ?o }}
        INSERT {{ {keep_ref} ?p ?o }}
        WHERE {{
            {remove_ref} ?p ?o .
            FILTER(?p NOT IN (rdf:type, rdfs:label, rdfs:comment))
        }}
    '''


def delete_concept(concept_uri: str) -> str:
    """Delete all remaining triples for a concept (cleanup after merge)."""
    concept_ref = format_uri_ref(concept_uri)
    return f'''
        DELETE WHERE {{ {concept_ref} ?p ?o }}
    '''


def get_concept_labels(concept_uri: str) -> str:
    """Get all labels for a concept."""
    return f'''
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        SELECT ?label WHERE {{
            {format_uri_ref(concept_uri)} rdfs:label ?label .
        }}
    '''


def add_alias_label(concept_uri: str, alias: str) -> str:
    """Add an alias label to a concept (for merged concept names)."""
    return f'''
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX paper: <https://kg.corca.ai/paper#>
        INSERT DATA {{
            {format_uri_ref(concept_uri)} paper:alias "{escape_sparql(alias)}" .
        }}
    '''


# --- Batch Deduplication Queries ---

def get_all_papers_with_metadata() -> str:
    """Get all papers with title and abstract for deduplication."""
    return '''
        PREFIX paper: <https://kg.corca.ai/paper#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        SELECT ?uri ?title ?abstract WHERE {
            ?uri a paper:Paper ;
                 rdfs:label ?title .
            OPTIONAL { ?uri paper:abstract ?abstract }
        }
    '''


def get_all_concepts_with_description() -> str:
    """Get all concepts with their names and descriptions."""
    return '''
        PREFIX paper: <https://kg.corca.ai/paper#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        SELECT ?uri ?label ?comment WHERE {
            ?uri a paper:Concept ;
                 rdfs:label ?label .
            OPTIONAL { ?uri rdfs:comment ?comment }
        }
    '''


def get_concepts_for_paper_with_details(paper_uri: str) -> str:
    """Get concepts for a paper with their descriptions."""
    return f'''
        PREFIX paper: <https://kg.corca.ai/paper#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        SELECT ?uri ?label ?comment WHERE {{
            {format_uri_ref(paper_uri)} paper:about ?uri .
            ?uri a paper:Concept ;
                 rdfs:label ?label .
            OPTIONAL {{ ?uri rdfs:comment ?comment }}
        }}
    '''


def get_citing_and_cited_papers(paper_uri: str) -> str:
    """Get papers that cite or are cited by the given paper (1-hop)."""
    return f'''
        PREFIX paper: <https://kg.corca.ai/paper#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        SELECT DISTINCT ?related ?title ?abstract WHERE {{
            {{
                {format_uri_ref(paper_uri)} paper:cites ?related .
            }} UNION {{
                ?related paper:cites {format_uri_ref(paper_uri)} .
            }}
            ?related rdfs:label ?title .
            OPTIONAL {{ ?related paper:abstract ?abstract }}
        }}
    '''


def get_2hop_cited_papers(paper_uri: str) -> str:
    """Get papers within 2 hops of citation (cites/cited-by chains)."""
    return f'''
        PREFIX paper: <https://kg.corca.ai/paper#>
        SELECT DISTINCT ?related WHERE {{
            {{
                # 1-hop: direct citations
                {format_uri_ref(paper_uri)} paper:cites ?related .
            }} UNION {{
                ?related paper:cites {format_uri_ref(paper_uri)} .
            }} UNION {{
                # 2-hop: citations of citations
                {format_uri_ref(paper_uri)} paper:cites ?mid .
                ?mid paper:cites ?related .
            }} UNION {{
                ?mid paper:cites {format_uri_ref(paper_uri)} .
                ?related paper:cites ?mid .
            }} UNION {{
                {format_uri_ref(paper_uri)} paper:cites ?mid .
                ?related paper:cites ?mid .
            }} UNION {{
                ?mid paper:cites {format_uri_ref(paper_uri)} .
                ?mid paper:cites ?related .
            }}
            FILTER(?related != {format_uri_ref(paper_uri)})
        }}
    '''


def get_same_author_papers(paper_uri: str) -> str:
    """Get other papers by the same author(s)."""
    return f'''
        PREFIX paper: <https://kg.corca.ai/paper#>
        SELECT DISTINCT ?related WHERE {{
            {format_uri_ref(paper_uri)} paper:author ?author .
            ?related paper:author ?author .
            FILTER(?related != {format_uri_ref(paper_uri)})
        }}
    '''


def get_concepts_for_papers_with_source(paper_uris: list[str]) -> str:
    """Get concepts from multiple papers with their source paper info.

    Returns concepts with uri, label, comment, and source paper title.
    Each concept may appear multiple times if it's in multiple papers.
    """
    if not paper_uris:
        return '''
            PREFIX paper: <https://kg.corca.ai/paper#>
            SELECT ?uri ?label ?comment ?paperTitle WHERE { VALUES ?uri { } }
        '''

    values = ' '.join(format_uri_ref(uri) for uri in paper_uris)
    return f'''
        PREFIX paper: <https://kg.corca.ai/paper#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        SELECT ?uri ?label ?comment ?paperTitle WHERE {{
            VALUES ?p {{ {values} }}
            ?p paper:about ?uri ;
               rdfs:label ?paperTitle .
            ?uri a paper:Concept ;
                 rdfs:label ?label .
            OPTIONAL {{ ?uri rdfs:comment ?comment }}
        }}
    '''


# Alias for backward compatibility
get_concepts_for_multiple_papers = get_concepts_for_papers
