"""Main collector implementation - thin coordinator for paper collection."""

from __future__ import annotations

import logging
import os
import time
from pathlib import Path

from . import queries
from .clients import (
    ArxivClient,
    CrossRefClient,
    DOIScraperClient,
    OpenAIClient,
    OpenAlexClient,
    SemanticScholarClient,
    SparqlClient,
)
from .constants import BACKOFF_MAX_INIT, BACKOFF_MAX_RUN, DEFAULT_EMBEDDING_MODEL, Backoff
from .db import Database
from .embeddings import compute_centroid
from .enrichment import Enricher
from .exceptions import NoAuthorsError, NotFoundError, RateLimitError, SparqlError, TemporaryError
from .kg2_writer import KG2Writer
from .linking import Linker
from .models import Config, Paper, PaperStatus, QueueStatus, Relation
from .scoring import compute_score, estimate_score
from .sparql_parsers import parse_sparql_count_result

logger = logging.getLogger(__name__)


def load_env(env_path: str | Path) -> dict[str, str]:
    """Load .env file into dict."""
    env = {}
    path = Path(env_path)
    if path.exists():
        for line in path.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, _, value = line.partition('=')
                env[key.strip()] = value.strip().strip('"').strip("'")
    return env


class Collector:
    """Paper collector - coordinates paper collection and enrichment.

    Usage:
        collector = Collector("./papers.db")
        collector.initialize(["DOI:10.1234/a", "ARXIV:1706.03762"])
        collector.run()

    For testing, inject mock clients:
        collector = Collector(
            db_path=":memory:",
            sparql_client=MockSparqlClient(),
            ss_client=MockSemanticScholarClient(),
        )
    """

    def __init__(self, db_path: str, api_key: str | None = None,
                 repo: str = "kg2",
                 # Optional client injection for testing
                 sparql_client: SparqlClient | None = None,
                 ss_client: SemanticScholarClient | None = None,
                 openai_client: OpenAIClient | None = None,
                 arxiv_client: ArxivClient | None = None,
                 crossref_client: CrossRefClient | None = None,
                 openalex_client: OpenAlexClient | None = None,
                 doi_scraper_client: DOIScraperClient | None = None):
        """Initialize collector with optional client injection for testing."""
        self.db = Database(db_path)

        # Load API keys from .env and environment
        script_dir = Path(__file__).parent
        env = load_env(script_dir / ".env")

        def get_key(name: str) -> str | None:
            return env.get(name) or os.environ.get(name)

        s2_key = api_key or get_key('S2_API_KEY')
        openai_key = get_key('OPENAI_API_KEY')
        polite_email = get_key('POLITE_EMAIL')

        # Initialize clients (injected or default)
        self.sparql = sparql_client or SparqlClient(repo)
        self.ss = ss_client or SemanticScholarClient(s2_key)
        self.openai = openai_client or (OpenAIClient(openai_key) if openai_key else None)
        self.arxiv = arxiv_client or ArxivClient()
        self.crossref = crossref_client or CrossRefClient(email=polite_email)
        self.openalex = openalex_client or OpenAlexClient(email=polite_email)
        self.doi_scraper = doi_scraper_client or DOIScraperClient()

        # Initialize specialized modules
        self.kg2_writer = KG2Writer(self.sparql, self.db)
        self.enricher = Enricher(self.sparql, self.db, self.openai)
        self.linker = Linker(self.sparql, self.db, self.openai)

    def close(self):
        """Close database connection."""
        self.db.close()

    # --- Initialization ---

    def initialize(self, seed_ids: list[str], config: Config | None = None):
        """Initialize collection with seed papers.

        Args:
            seed_ids: List of seed paper IDs (DOI:xxx, ARXIV:xxx, etc.)
            config: Optional collection configuration
        """
        if config is None:
            config = Config(seed_ids=seed_ids)
        else:
            config.seed_ids = seed_ids

        self.db.save_full_config(config)

        seed_papers = self._fetch_seed_papers(seed_ids)
        self.db.commit()

        self._compute_seed_embeddings(seed_papers)

        for paper in seed_papers:
            self._enqueue_neighbors(paper)

        self.db.commit()
        logger.info("Initialized with %d seeds", len(seed_papers))

    def _fetch_seed_papers(self, seed_ids: list[str]) -> list[Paper]:
        """Fetch and store seed papers."""
        seed_papers = []
        backoff = Backoff(maximum=BACKOFF_MAX_INIT)

        for seed_id in seed_ids:
            paper = self._fetch_seed_paper(seed_id, backoff)
            if paper:
                seed_papers.append(paper)

        return seed_papers

    def _fetch_seed_paper(self, seed_id: str, backoff: Backoff) -> Paper | None:
        """Fetch a single seed paper with retry logic."""
        logger.info("Fetching seed: %s", seed_id)

        while True:
            try:
                paper = self.ss.get_paper(seed_id)
                break
            except NotFoundError:
                logger.warning("  Skipping: not found")
                return None
            except RateLimitError:
                backoff.wait("Rate limited")

        if not paper.authors:
            raise NoAuthorsError(seed_id)

        self._fill_abstract_from_fallbacks(paper)
        paper.status = PaperStatus.SEED

        kg2_uri = self.kg2_writer.insert_paper(paper)
        self.db.insert_paper(paper, kg2_uri)
        logger.info("  -> %s...", paper.title[:60])

        return paper

    def _compute_seed_embeddings(self, seed_papers: list[Paper]) -> None:
        """Compute and store seed paper embeddings and centroid."""
        if not self.openai or not seed_papers:
            return

        logger.info("Computing seed embeddings...")
        seed_embeddings = []

        for paper in seed_papers:
            try:
                emb = self.openai.embed_paper(paper.title, paper.abstract)
                self.db.save_paper_embedding(paper.id, emb, DEFAULT_EMBEDDING_MODEL)
                seed_embeddings.append(emb)
                logger.info("  -> embedded: %s...", paper.title[:40])
            except Exception as e:
                logger.warning("  -> failed to embed %s: %s", paper.id, e)

        if seed_embeddings:
            centroid = compute_centroid(seed_embeddings)
            self.db.save_seed_centroid(
                centroid, DEFAULT_EMBEDDING_MODEL, [p.id for p in seed_papers]
            )
            logger.info("Saved seed centroid from %d embeddings", len(seed_embeddings))

        self.db.commit()

    def resume(self):
        """Resume interrupted collection."""
        count = self.db.reset_processing_to_pending()
        self.db.commit()
        logger.info("Resumed: reset %d processing items to pending", count)

    # --- Main Loop ---

    def run(self, max_iterations: int | None = None):
        """Run collection.

        Args:
            max_iterations: Max iterations (None = until max_papers)
        """
        config = self.db.load_config()
        if config is None:
            raise RuntimeError("Not initialized. Run initialize() first.")

        total = self.db.count_papers()
        logger.info("Starting collection (papers: %d/%d)...", total, config.max_papers)

        # Load seed centroid for semantic scoring
        centroid_data = self.db.get_seed_centroid()
        seed_centroid = centroid_data[0] if centroid_data else None
        if seed_centroid:
            logger.info("Using seed centroid for semantic scoring")
        elif self.openai:
            logger.info("No seed centroid found - semantic scoring disabled")

        iterations = 0
        backoff = Backoff(maximum=BACKOFF_MAX_RUN)

        while True:
            # Check termination conditions
            if max_iterations and iterations >= max_iterations:
                break
            total = self.db.count_papers()
            if total >= config.max_papers:
                logger.info("Reached max_papers (%d)", config.max_papers)
                break

            # Get next candidate
            candidate = self.db.next_candidate()
            if not candidate:
                logger.info("Queue empty")
                break

            paper_id = candidate.id
            source_id = candidate.source_id
            relation = candidate.relation

            logger.info("Fetching: %s...", paper_id)

            # Mark as processing
            self.db.update_queue_status(paper_id, QueueStatus.PROCESSING)
            self.db.commit()

            # Fetch from API
            try:
                paper = self.ss.get_paper(paper_id)
                backoff.reset()
            except NotFoundError:
                logger.info("  -> skipped: not found")
                self.db.update_queue_status(paper_id, QueueStatus.SKIPPED, 'not_found')
                self.db.commit()
                continue
            except RateLimitError:
                self.db.update_queue_status(paper_id, QueueStatus.PENDING)
                self.db.commit()
                backoff.wait("Rate limited")
                continue
            except TemporaryError as e:
                self.db.update_queue_status(paper_id, QueueStatus.PENDING)
                self.db.commit()
                backoff.wait(str(e))
                continue

            # Filter: no authors
            if not paper.authors:
                logger.info("  -> skipped: no authors")
                self.db.update_queue_status(paper_id, QueueStatus.SKIPPED, 'no_authors')
                self.db.commit()
                continue

            # Fill abstract from fallback sources if missing
            self._fill_abstract_from_fallbacks(paper)

            # Compute paper embedding for semantic scoring
            paper_embedding = None
            if self.openai and seed_centroid:
                try:
                    paper_embedding = self.openai.embed_paper(paper.title, paper.abstract)
                except Exception as e:
                    logger.debug("  -> embedding failed: %s", e)

            # Compute score
            seed_ids = self.db.get_seed_ids()
            collected_ids = self.db.get_collected_ids()
            actual_score = compute_score(
                paper, seed_ids, collected_ids,
                source_id=source_id, relation=relation,
                paper_embedding=paper_embedding, seed_centroid=seed_centroid
            )

            # Insert to kg2 and database
            try:
                kg2_uri = self.kg2_writer.insert_paper(paper)
            except SparqlError as e:
                logger.warning("SPARQL error: %s", e)
                self.db.update_queue_status(paper_id, QueueStatus.SKIPPED, 'sparql_error')
                self.db.commit()
                continue

            self.db.insert_paper(paper, kg2_uri)
            self.db.update_queue_status(paper_id, QueueStatus.DONE)

            # Save paper embedding for later use in linking
            if paper_embedding:
                self.db.save_paper_embedding(paper.id, paper_embedding, DEFAULT_EMBEDDING_MODEL)

            # Enqueue neighbors
            self._enqueue_neighbors(paper)

            self.db.commit()
            iterations += 1

            logger.info("[%d/%d] %s... (score=%.2f)",
                        total + 1, config.max_papers, paper.title[:50], actual_score)

        stats = self.db.stats()
        logger.info("Done. Papers: %d, Queue: pending=%d, done=%d, skipped=%d",
                    stats.total_papers, stats.queue.get('pending', 0),
                    stats.queue.get('done', 0), stats.queue.get('skipped', 0))

    def _enqueue_neighbors(self, paper: Paper):
        """Enqueue paper's neighbors."""
        for ref_id in paper.references:
            score = estimate_score(paper, Relation.REFERENCE)
            self.db.enqueue(ref_id, score, paper.id, Relation.REFERENCE)

        for cit_id in paper.citations:
            score = estimate_score(paper, Relation.CITATION)
            self.db.enqueue(cit_id, score, paper.id, Relation.CITATION)

    def _try_abstract_sources(self, arxiv_id: str | None, doi: str | None,
                               title: str | None = None) -> tuple[str | None, str | None]:
        """Try to fetch abstract from fallback sources.

        Tries arXiv first (if arxiv_id provided), then CrossRef, OpenAlex,
        DOI scraper, and DBLP search for JMLR papers.

        Args:
            arxiv_id: arXiv ID (optional)
            doi: DOI (optional)
            title: Paper title for DBLP search (optional)

        Returns:
            Tuple of (abstract, source_name) or (None, None) if not found
        """
        sources = [
            (arxiv_id, lambda aid: self.arxiv.get_abstract(aid), "arXiv"),
            (doi, lambda d: self.crossref.get_abstract(d), "CrossRef"),
            (doi, lambda d: self.openalex.get_abstract(d), "OpenAlex"),
            (doi, lambda d: self.doi_scraper.get_abstract(d), "publisher page"),
            (title, lambda t: self.doi_scraper.search_dblp_for_jmlr(t), "JMLR via DBLP"),
        ]
        for identifier, fetcher, source in sources:
            if identifier:
                abstract = fetcher(identifier)
                if abstract:
                    return abstract, source
        return None, None

    def _fill_abstract_from_fallbacks(self, paper: Paper) -> bool:
        """Fill paper's abstract from fallback sources if missing.

        Tries: arXiv, CrossRef, OpenAlex, DOI scraper, DBLP.
        Modifies paper in place.

        Returns:
            True if abstract was found
        """
        if paper.abstract:
            return False

        abstract, source = self._try_abstract_sources(paper.arxiv_id, paper.doi)
        if abstract:
            paper.abstract = abstract
            logger.info("  -> fetched abstract from %s", source)
            return True
        return False

    def fetch_contexts(self, max_papers: int | None = None,
                        watch: bool = False, poll_interval: int = 10) -> int:
        """Fetch citation contexts for papers.

        Citation contexts include:
        - intents: why a paper is cited (background, methodology, result)
        - contexts: text snippets where the citation occurs

        Args:
            max_papers: Maximum papers to process (None = all pending)
            watch: If True, poll for new papers instead of exiting
            poll_interval: Seconds between polls when watching

        Returns:
            Number of papers processed
        """
        processed = 0
        backoff = Backoff(maximum=BACKOFF_MAX_RUN)

        while True:
            if max_papers and processed >= max_papers:
                break

            # Get papers needing context fetch
            paper_ids = self.db.get_papers_needing_contexts(limit=1)
            if not paper_ids:
                if watch:
                    logger.info("Waiting for papers needing contexts... (poll every %ds)",
                               poll_interval)
                    time.sleep(poll_interval)
                    continue
                else:
                    break

            paper_id = paper_ids[0]
            logger.info("Fetching contexts for: %s...", paper_id[:20])

            try:
                contexts = self.ss.get_citation_contexts(paper_id)
                backoff.reset()

                saved = self.db.save_citation_contexts(paper_id, contexts)
                self.db.mark_contexts_fetched(paper_id)
                self.db.commit()

                processed += 1
                logger.info("  -> saved %d citation contexts", saved)

            except NotFoundError:
                logger.info("  -> not found, skipping")
                self.db.mark_contexts_fetched(paper_id)
                self.db.commit()
            except RateLimitError:
                backoff.wait("Rate limited")
            except TemporaryError as e:
                backoff.wait(str(e))

        logger.info("Fetched contexts for %d papers", processed)
        return processed

    def backfill_abstracts(self, max_papers: int | None = None) -> tuple[int, int]:
        """Backfill abstracts for papers missing them.

        Args:
            max_papers: Maximum papers to process (None = all)

        Returns:
            Tuple of (papers_checked, abstracts_found)
        """
        checked = 0
        found = 0

        for row in self.db.iter_papers_without_abstract():
            if max_papers and checked >= max_papers:
                break

            logger.info("Checking: %s...", row['title'][:50])
            checked += 1

            abstract, source = self._try_abstract_sources(
                row['arxiv_id'], row['doi'], row['title']
            )
            if abstract:
                logger.info("  -> found via %s", source)
                self.db.update_abstract(row['id'], abstract)
                self.db.commit()
                found += 1

        logger.info("Checked %d papers, found %d abstracts", checked, found)
        return checked, found

    # --- Delegated Methods ---

    def enrich(self, max_papers: int | None = None,
               watch: bool = False, poll_interval: int = 10,
               parallel: bool = False):
        """Enrich papers with LLM-extracted concepts and claims."""
        return self.enricher.enrich(max_papers, watch, poll_interval, parallel)

    def link(self, max_papers: int | None = None,
             watch: bool = False, poll_interval: int = 10,
             parallel: bool = False):
        """Find missed claim relations for enriched papers."""
        return self.linker.link(max_papers, watch, poll_interval, parallel)

    # --- Statistics ---

    def stats(self) -> dict:
        """Get collection statistics."""
        return self.db.stats().to_dict()

    def concept_stats(self) -> dict:
        """Get concept statistics from kg2."""
        results = self.sparql.query(queries.count_concepts())
        total = parse_sparql_count_result(results)
        return {'total': total}
