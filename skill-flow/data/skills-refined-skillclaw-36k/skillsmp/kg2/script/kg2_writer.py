"""KG2 write operations for papers, authors, venues, and citations."""
from __future__ import annotations

import contextlib

from . import queries
from .clients import SparqlClient, escape_sparql
from .constants import TURTLE_PREFIXES
from .db import Database
from .exceptions import SparqlError
from .models import Author, Paper, Venue
from .turtle_builders import build_cites_turtle, format_uri_ref


def _end_turtle_statement(lines: list[str]) -> None:
    """Replace trailing semicolon with period to end Turtle statement."""
    if lines and lines[-1].endswith(' ;'):
        lines[-1] = lines[-1][:-2] + ' .'


class KG2Writer:
    """Handles writing papers, authors, venues to KG2."""

    def __init__(self, sparql: SparqlClient, db: Database):
        self.sparql = sparql
        self.db = db

    def _query_uri(self, query: str) -> str | None:
        """Execute query and return first URI if found."""
        results = self.sparql.query(query)
        return results[0]['uri']['value'] if results else None

    def insert_paper(self, paper: Paper) -> str:
        """Insert paper to kg2. Returns URI."""
        # Check for existing paper
        existing_uri = self._find_existing_paper(paper)
        if existing_uri:
            return existing_uri

        # Generate new URI
        paper_uri = self.sparql.generate_uri("pa")

        # Prepare Author/Venue URIs
        author_uris = [self._ensure_author(a) for a in paper.authors]
        venue_uri = self._ensure_venue(paper.venue) if paper.venue else None

        # Build and insert Turtle
        turtle = self._build_paper_turtle(paper, paper_uri, author_uris, venue_uri)
        self.sparql.insert_turtle(turtle)

        # Process citations
        self._process_citations(paper, paper_uri)

        return paper_uri

    def _find_existing_paper(self, paper: Paper) -> str | None:
        """Find existing paper URI in kg2."""
        if paper.doi and (uri := self._query_uri(queries.find_paper_by_doi(paper.doi))):
            return uri
        if paper.arxiv_id and (uri := self._query_uri(queries.find_paper_by_arxiv(paper.arxiv_id))):
            return uri
        return self._query_uri(queries.find_paper_by_s2_id(paper.id))

    def _ensure_author(self, author: Author) -> str:
        """Get or create Author URI."""
        if author.orcid and (uri := self._query_uri(queries.find_author_by_orcid(author.orcid))):
            return uri
        if author.author_id and (uri := self._query_uri(queries.find_author_by_s2_id(author.author_id))):
            return uri
        return self.sparql.generate_uri("au")

    def _ensure_venue(self, venue: Venue) -> str:
        """Get or create Venue URI."""
        if venue.venue_id and (uri := self._query_uri(queries.find_venue_by_s2_id(venue.venue_id))):
            return uri
        return self._query_uri(queries.find_venue_by_name(venue.name)) or self.sparql.generate_uri("ve")

    def _build_paper_turtle(self, paper: Paper, paper_uri: str,
                            author_uris: list[str], venue_uri: str | None) -> str:
        """Build Turtle for Paper + Author + Venue."""
        lines = [TURTLE_PREFIXES, ""]

        # Authors (only new ones - prefixed URIs indicate newly generated)
        for i, author in enumerate(paper.authors):
            uri = author_uris[i]
            if not uri.startswith("https://"):
                lines.append(f'{uri} a paper:Author ;')
                lines.append(f'    rdfs:label "{escape_sparql(author.name)}" ;')
                if author.author_id:
                    lines.append(f'    paper:semanticScholarAuthorId "{author.author_id}" ;')
                if author.orcid:
                    lines.append(f'    paper:orcidId "{author.orcid}" ;')
                _end_turtle_statement(lines)
                lines.append("")

        # Venue (only new - prefixed URIs indicate newly generated)
        venue = paper.venue
        if venue and venue_uri and not venue_uri.startswith("https://"):
            lines.append(f'{venue_uri} a paper:Venue ;')
            lines.append(f'    rdfs:label "{escape_sparql(venue.name)}" ;')
            if venue.venue_id:
                lines.append(f'    paper:semanticScholarVenueId "{venue.venue_id}" ;')
            if venue.venue_type:
                lines.append(f'    paper:venueType "{venue.venue_type}" ;')
            _end_turtle_statement(lines)
            lines.append("")

        # Paper
        lines.append(f'{paper_uri} a paper:Paper ;')
        lines.append(f'    rdfs:label "{escape_sparql(paper.title)}" ;')
        lines.append(f'    paper:semanticScholarId "{paper.id}" ;')

        if paper.doi:
            lines.append(f'    paper:doi "{paper.doi}" ;')
        if paper.arxiv_id:
            lines.append(f'    paper:arxivId "{paper.arxiv_id}" ;')
        if paper.year:
            lines.append(f'    paper:year {paper.year} ;')
        if paper.abstract:
            lines.append(f'    paper:abstract "{escape_sparql(paper.abstract)}" ;')

        # primaryAuthor (first) and co-authors
        lines.append(f'    paper:primaryAuthor {format_uri_ref(author_uris[0])} ;')
        for uri in author_uris[1:]:
            lines.append(f'    paper:author {format_uri_ref(uri)} ;')

        if venue_uri:
            lines.append(f'    paper:publishedIn {format_uri_ref(venue_uri)} ;')

        _end_turtle_statement(lines)

        return '\n'.join(lines)

    def _process_citations(self, paper: Paper, paper_uri: str):
        """Process citation relationships."""
        # This paper's references
        for ref_id in paper.references:
            ref_kg2_uri = self.db.get_kg2_uri(ref_id)
            if ref_kg2_uri:
                self._add_cites(paper_uri, ref_kg2_uri)
            else:
                self.db.add_pending_cites(paper.id, ref_id)

        # Pending cites waiting for this paper
        pending = self.db.get_pending_cites_to(paper.id)
        for citing_id in pending:
            citing_uri = self.db.get_kg2_uri(citing_id)
            if citing_uri:
                self._add_cites(citing_uri, paper_uri)
                self.db.delete_pending_cites(citing_id, paper.id)

    def _add_cites(self, citing_uri: str, cited_uri: str):
        """Add cites relationship."""
        with contextlib.suppress(SparqlError):
            self.sparql.insert_turtle(build_cites_turtle(citing_uri, cited_uri))
