"""Mock clients for testing without external dependencies."""
from __future__ import annotations

from typing import Any

from .exceptions import NotFoundError
from .models import Author, Paper


class MockSparqlClient:
    """Mock SPARQL client that stores data in memory.

    Usage:
        sparql = MockSparqlClient()
        sparql.add_paper("paper:pa_123", {"title": "Test Paper"})
        sparql.add_concept("paper:co_456", {"name": "Neural Network"})
    """

    def __init__(self):
        self.papers: dict[str, dict[str, Any]] = {}
        self.authors: dict[str, dict[str, Any]] = {}
        self.venues: dict[str, dict[str, Any]] = {}
        self.concepts: dict[str, dict[str, Any]] = {}
        self.claims: dict[str, dict[str, Any]] = {}
        self.triples: list[tuple] = []  # (subject, predicate, object)
        self._uri_counter = 0

    def query(self, sparql: str) -> list[dict[str, Any]]:
        """Execute SELECT query, return mock results."""
        sparql_lower = sparql.lower()

        # Handle COUNT queries
        if 'count(' in sparql_lower:
            if 'paper:concept' in sparql_lower:
                count = len(self.concepts)
                if 'filter not exists' in sparql_lower and 'rdfs:comment' in sparql_lower:
                    count = sum(1 for c in self.concepts.values() if not c.get('description'))
                return [{'count': {'value': str(count)}}]
            return [{'count': {'value': '0'}}]

        # Handle paper lookups
        if 'paper:doi' in sparql_lower:
            for uri, data in self.papers.items():
                if data.get('doi') and data['doi'] in sparql:
                    return [{'uri': {'value': uri}}]
            return []

        if 'paper:arxivid' in sparql_lower:
            for uri, data in self.papers.items():
                if data.get('arxiv_id') and data['arxiv_id'] in sparql:
                    return [{'uri': {'value': uri}}]
            return []

        if 'paper:semanticscholarid' in sparql_lower:
            for uri, data in self.papers.items():
                if data.get('s2_id') and data['s2_id'] in sparql:
                    return [{'uri': {'value': uri}}]
            return []

        # Handle author lookups
        if 'paper:orcidid' in sparql_lower:
            for uri, data in self.authors.items():
                if data.get('orcid') and data['orcid'] in sparql:
                    return [{'uri': {'value': uri}}]
            return []

        if 'paper:semanticscholarauthorid' in sparql_lower:
            for uri, data in self.authors.items():
                if data.get('author_id') and data['author_id'] in sparql:
                    return [{'uri': {'value': uri}}]
            return []

        # Handle venue lookups
        if 'paper:semanticscholarvenueid' in sparql_lower:
            for uri, data in self.venues.items():
                if data.get('venue_id') and data['venue_id'] in sparql:
                    return [{'uri': {'value': uri}}]
            return []

        if 'paper:venue' in sparql_lower and 'rdfs:label' in sparql_lower:
            for uri, data in self.venues.items():
                if data.get('name') and data['name'] in sparql:
                    return [{'uri': {'value': uri}}]
            return []

        # Handle concept lookups
        if 'paper:concept' in sparql_lower and 'rdfs:label' in sparql_lower:
            for uri, data in self.concepts.items():
                if data.get('name') and data['name'] in sparql:
                    result = {'uri': {'value': uri}}
                    if data.get('description'):
                        result['comment'] = {'value': data['description']}
                    return [result]
            return []

        # Handle concepts without description query
        if 'paper:concept' in sparql_lower and 'paper:about' in sparql_lower:
            results = []
            for uri, data in self.concepts.items():
                if not data.get('description') and data.get('paper_uri'):
                    paper = self.papers.get(data['paper_uri'], {})
                    if paper.get('abstract'):
                        results.append({
                            'uri': {'value': uri},
                            'name': {'value': data.get('name', '')},
                            'title': {'value': paper.get('title', '')},
                            'abstract': {'value': paper.get('abstract', '')},
                        })
            return results

        # Handle claims for paper query
        if 'paper:hasclaim' in sparql_lower:
            results = []
            for uri, data in self.claims.items():
                if data.get('paper_uri') and data['paper_uri'] in sparql:
                    results.append({
                        'claim': {'value': uri},
                        'text': {'value': data.get('text', '')},
                    })
            return results

        return []

    def ask(self, sparql: str) -> bool:
        """Execute ASK query."""
        # Check if URI exists
        for uri in list(self.papers.keys()) + list(self.authors.keys()) + \
                   list(self.venues.keys()) + list(self.concepts.keys()):
            if uri in sparql or uri.replace('paper:', 'https://kg.corca.ai/paper#') in sparql:
                return True
        return False

    def insert_turtle(self, turtle: str) -> None:
        """Insert Turtle data (no-op for mock, just record it)."""
        self.triples.append(('turtle', turtle))

    def insert_turtle_silent(self, turtle: str) -> bool:
        """Insert Turtle data, silently ignoring errors."""
        self.triples.append(('turtle', turtle))
        return True

    def uri_exists(self, uri: str) -> bool:
        """Check if URI exists."""
        all_uris = set(self.papers.keys()) | set(self.authors.keys()) | \
                   set(self.venues.keys()) | set(self.concepts.keys()) | \
                   set(self.claims.keys())
        return uri in all_uris

    def generate_uri(self, prefix: str) -> str:
        """Generate unique URI."""
        self._uri_counter += 1
        return f"paper:{prefix}_{self._uri_counter:08d}"

    # --- Helper methods for test setup ---

    def add_paper(self, uri: str, data: dict[str, Any]):
        """Add a paper to the mock store."""
        self.papers[uri] = data

    def add_author(self, uri: str, data: dict[str, Any]):
        """Add an author to the mock store."""
        self.authors[uri] = data

    def add_venue(self, uri: str, data: dict[str, Any]):
        """Add a venue to the mock store."""
        self.venues[uri] = data

    def add_concept(self, uri: str, data: dict[str, Any]):
        """Add a concept to the mock store."""
        self.concepts[uri] = data

    def add_claim(self, uri: str, data: dict[str, Any]):
        """Add a claim to the mock store."""
        self.claims[uri] = data


class MockSemanticScholarClient:
    """Mock Semantic Scholar client that returns predefined papers.

    Usage:
        ss = MockSemanticScholarClient()
        ss.add_paper("DOI:10.1234/test", Paper(id="abc", title="Test"))
        paper = ss.get_paper("DOI:10.1234/test")
    """

    def __init__(self):
        self.papers: dict[str, Paper] = {}
        self.not_found: set[str] = set()

    def get_paper(self, paper_id: str) -> Paper:
        """Fetch paper metadata."""
        if paper_id in self.not_found:
            raise NotFoundError(paper_id)
        if paper_id in self.papers:
            return self.papers[paper_id]
        # Return a default paper for any ID
        raise NotFoundError(paper_id)

    def add_paper(self, paper_id: str, paper: Paper):
        """Add a paper to the mock store."""
        self.papers[paper_id] = paper

    def mark_not_found(self, paper_id: str):
        """Mark a paper ID as not found."""
        self.not_found.add(paper_id)


class MockOpenAIClient:
    """Mock OpenAI client that returns predefined responses.

    Usage:
        openai = MockOpenAIClient()
        openai.set_extraction_response({"concepts": [...], "claims": [...]})
    """

    def __init__(self, embedding_dim: int = 1536):
        self.responses: dict[str, Any] = {}
        self.default_responses = {
            'paper_extraction': {
                'concepts': [],
                'claims': [],
            },
            'claim_relations': {
                'relations': [],
            },
            'concept_description': {
                'description': 'A test description.',
            },
        }
        self.call_history: list[dict[str, Any]] = []
        self._embedding_dim = embedding_dim

    def structured_completion(
        self,
        messages: list[dict[str, str]],
        schema: dict[str, Any],
        schema_name: str = "response",
    ) -> dict[str, Any]:
        """Get structured completion."""
        self.call_history.append({
            'messages': messages,
            'schema': schema,
            'schema_name': schema_name,
        })

        if schema_name in self.responses:
            return self.responses[schema_name]
        return self.default_responses.get(schema_name, {})

    def embed(self, text: str) -> list[float]:
        """Get mock embedding for a single text (deterministic based on text hash)."""
        return self._generate_embedding(text)

    def embed_batch(self, texts: list[str]) -> list[list[float]]:
        """Get mock embeddings for multiple texts."""
        return [self._generate_embedding(t) for t in texts]

    def embed_paper(self, title: str, abstract: str | None) -> list[float]:
        """Get mock embedding for a paper."""
        text = f"{title}\n\n{abstract}" if abstract else title
        return self.embed(text)

    def _generate_embedding(self, text: str) -> list[float]:
        """Generate deterministic embedding based on text hash."""
        import hashlib
        # Use hash to generate reproducible pseudo-random embedding
        h = hashlib.sha256(text.encode()).digest()
        # Convert bytes to floats in range [-1, 1]
        embedding = []
        for i in range(self._embedding_dim):
            byte_idx = i % len(h)
            val = (h[byte_idx] / 127.5) - 1.0  # Normalize to [-1, 1]
            embedding.append(val)
        return embedding

    def set_response(self, schema_name: str, response: dict[str, Any]):
        """Set response for a specific schema."""
        self.responses[schema_name] = response

    def set_extraction_response(self, concepts: list[dict], claims: list[dict]):
        """Set response for paper extraction."""
        self.responses['paper_extraction'] = {
            'concepts': concepts,
            'claims': claims,
        }

    def set_relations_response(self, relations: list[dict]):
        """Set response for claim relations."""
        self.responses['claim_relations'] = {
            'relations': relations,
        }

    def set_description_response(self, description: str):
        """Set response for concept description."""
        self.responses['concept_description'] = {
            'description': description,
        }


# --- Test Fixtures ---

def create_test_paper(
    id: str = "test123",
    title: str = "Test Paper",
    year: int = 2023,
    abstract: str = "This is a test abstract.",
    doi: str | None = None,
    arxiv_id: str | None = None,
    authors: list[Author] | None = None,
    references: list[str] | None = None,
    citations: list[str] | None = None,
) -> Paper:
    """Create a test paper with default values."""
    if authors is None:
        authors = [Author(name="Test Author", author_id="auth123")]
    return Paper(
        id=id,
        title=title,
        year=year,
        abstract=abstract,
        doi=doi,
        arxiv_id=arxiv_id,
        authors=authors,
        references=references or [],
        citations=citations or [],
        citation_count=10,
    )


def create_test_collector(
    with_openai: bool = False,
    papers: dict[str, Paper] | None = None,
):
    """Create a Collector with mock clients for testing.

    Usage:
        collector = create_test_collector()
        collector.initialize(["DOI:10.1234/test"])
    """
    # Import here to avoid circular imports
    from .collector import Collector

    sparql = MockSparqlClient()
    ss = MockSemanticScholarClient()
    openai = MockOpenAIClient() if with_openai else None

    # Add any predefined papers
    if papers:
        for paper_id, paper in papers.items():
            ss.add_paper(paper_id, paper)

    return Collector(
        db_path=":memory:",
        sparql_client=sparql,
        ss_client=ss,
        openai_client=openai,
    )
