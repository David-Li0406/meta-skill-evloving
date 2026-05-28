#!/usr/bin/env python3
"""Citation Network Paper Collector CLI."""

import logging
import multiprocessing
import os
import sys
from pathlib import Path

import click

# Support direct execution: add parent to path so relative imports work
if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).parent.parent))

from script.collector import Collector  # noqa: E402
from script.models import Config  # noqa: E402

DEFAULT_DB = "./papers.db"


@click.group()
@click.option("--db", default=DEFAULT_DB, help="SQLite database path")
@click.option("--api-key", default=None, help="Semantic Scholar API key")
@click.option("--repo", default="kg2", help="GraphDB repository name")
@click.option("--quiet", "-q", is_flag=True, help="Suppress progress output")
@click.pass_context
def cli(ctx, db, api_key, repo, quiet):
    """Citation Network Paper Collector."""
    ctx.ensure_object(dict)
    ctx.obj["db"] = db
    ctx.obj["api_key"] = api_key
    ctx.obj["repo"] = repo

    # Configure logging once at startup
    level = logging.WARNING if quiet else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(message)s",
        handlers=[logging.StreamHandler(sys.stdout)]
    )


@cli.command()
@click.option("--seeds", "-s", multiple=True, required=True,
              help="Seed paper IDs (DOI:xxx, ARXIV:xxx, etc.)")
@click.option("--max-papers", default=500, help="Maximum papers to collect")
@click.pass_context
def init(ctx, seeds, max_papers):
    """Initialize collection with seed papers."""
    config = Config(
        seed_ids=list(seeds),
        max_papers=max_papers,
    )
    collector = Collector(ctx.obj["db"], api_key=ctx.obj["api_key"],
                          repo=ctx.obj["repo"])
    try:
        collector.initialize(list(seeds), config)
    finally:
        collector.close()


@cli.command()
@click.option("--max", "max_iterations", type=int, default=None,
              help="Maximum iterations (default: until max_papers)")
@click.pass_context
def run(ctx, max_iterations):
    """Run collection (auto-resumes interrupted state)."""
    collector = Collector(ctx.obj["db"], api_key=ctx.obj["api_key"],
                          repo=ctx.obj["repo"])
    try:
        collector.resume()
        collector.run(max_iterations=max_iterations)
    finally:
        collector.close()


@cli.command()
@click.pass_context
def status(ctx):
    """Show collection status."""
    collector = Collector(ctx.obj["db"], repo=ctx.obj["repo"])
    try:
        stats = collector.stats()

        click.echo("Papers:")
        for st, count in stats['papers'].items():
            click.echo(f"  {st}: {count}")
        click.echo(f"  total: {stats['total_papers']}")

        click.echo("\nEnrichment:")
        click.echo(f"  enriched: {stats['enriched']}")
        click.echo(f"  unenriched: {stats['unenriched']}")

        click.echo("\nLinking:")
        click.echo(f"  linked: {stats['linked']}")
        click.echo(f"  unlinked: {stats['unlinked']}")

        click.echo("\nCitation Contexts:")
        click.echo(f"  fetched: {stats.get('contexts_fetched', 0)}")
        click.echo(f"  pending: {stats.get('contexts_pending', 0)}")

        click.echo("\nQueue:")
        for st, count in stats['queue'].items():
            click.echo(f"  {st}: {count}")

        click.echo(f"\nPending cites: {stats['pending_cites']}")

        concept_stats = collector.concept_stats()
        click.echo(f"\nConcepts: {concept_stats['total']}")

        config = collector.db.load_config()
        if config:
            click.echo("\nConfig:")
            click.echo(f"  max_papers: {config.max_papers}")
    finally:
        collector.close()


def _run_worker(task: str, db: str, repo: str, max_papers: int | None,
                watch: bool, poll: int, worker_id: int, quiet: bool):
    """Generic worker process for parallel enrichment or linking."""
    level = logging.WARNING if quiet else logging.INFO
    logging.basicConfig(
        level=level,
        format=f"[{task}-{worker_id}] %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)],
        force=True,
    )

    collector = Collector(db, repo=repo)
    try:
        method = getattr(collector, task)
        method(max_papers=max_papers, watch=watch, poll_interval=poll, parallel=True)
    finally:
        collector.close()


def _run_parallel_or_single(task: str, ctx, max_papers, watch, poll, workers):
    """Run a task with optional parallel workers."""
    db = ctx.obj["db"]
    repo = ctx.obj["repo"]
    quiet = logging.getLogger().level >= logging.WARNING

    if workers > 1:
        processes = [
            multiprocessing.Process(
                target=_run_worker,
                args=(task, db, repo, max_papers, watch, poll, i, quiet)
            )
            for i in range(workers)
        ]
        for p in processes:
            p.start()
        try:
            for p in processes:
                p.join()
        except KeyboardInterrupt:
            click.echo("\nStopping workers...")
            for p in processes:
                p.terminate()
            for p in processes:
                p.join()
    else:
        collector = Collector(db, repo=repo)
        try:
            getattr(collector, task)(max_papers=max_papers, watch=watch, poll_interval=poll)
        finally:
            collector.close()


@cli.command()
@click.option("--max", "max_papers", type=int, default=None,
              help="Maximum papers to enrich (default: all)")
@click.option("--watch", "-w", is_flag=True,
              help="Watch for new papers instead of exiting")
@click.option("--poll", default=10, help="Poll interval in seconds when watching")
@click.option("--workers", default=1, help="Number of parallel workers")
@click.pass_context
def enrich(ctx, max_papers, watch, poll, workers):
    """Enrich papers with LLM-extracted concepts and claims."""
    _run_parallel_or_single("enrich", ctx, max_papers, watch, poll, workers)


@cli.command()
@click.option("--max", "max_papers", type=int, default=None,
              help="Maximum papers to process (default: all)")
@click.option("--watch", "-w", is_flag=True,
              help="Watch for enriched papers instead of exiting")
@click.option("--poll", default=10, help="Poll interval in seconds when watching")
@click.option("--workers", default=1, help="Number of parallel workers")
@click.pass_context
def link(ctx, max_papers, watch, poll, workers):
    """Find missed claim relations between papers."""
    _run_parallel_or_single("link", ctx, max_papers, watch, poll, workers)


@cli.command("backfill-abstracts")
@click.option("--max", "max_papers", type=int, default=None,
              help="Maximum papers to check (default: all)")
@click.pass_context
def backfill_abstracts(ctx, max_papers):
    """Backfill missing abstracts from arXiv and CrossRef."""
    collector = Collector(ctx.obj["db"], repo=ctx.obj["repo"])
    try:
        checked, found = collector.backfill_abstracts(max_papers=max_papers)
        click.echo(f"Done: checked {checked} papers, found {found} abstracts")
    finally:
        collector.close()


@cli.command("fetch-contexts")
@click.option("--max", "max_papers", type=int, default=None,
              help="Maximum papers to process (default: all)")
@click.option("--watch", "-w", is_flag=True,
              help="Watch for new papers instead of exiting")
@click.option("--poll", default=10, help="Poll interval in seconds when watching")
@click.pass_context
def fetch_contexts(ctx, max_papers, watch, poll):
    """Fetch citation contexts from Semantic Scholar.

    Citation contexts include:
    - intents: why a paper is cited (background, methodology, result)
    - contexts: text snippets where the citation occurs

    These are used to improve claim relation detection in the link step.
    """
    collector = Collector(ctx.obj["db"], api_key=ctx.obj["api_key"],
                          repo=ctx.obj["repo"])
    try:
        processed = collector.fetch_contexts(max_papers=max_papers, watch=watch,
                                             poll_interval=poll)
        click.echo(f"Done: fetched contexts for {processed} papers")
    finally:
        collector.close()


@cli.command("organize-concepts")
@click.option("--skip-llm", is_flag=True,
              help="Only auto-merge (>= 0.95 similarity), skip LLM analysis")
@click.option("--workers", "-w", default=1, type=int,
              help="Number of parallel workers for cluster processing (default: 1)")
@click.option("--cache-stats", is_flag=True,
              help="Show embedding cache statistics")
@click.pass_context
def organize_concepts(ctx, skip_llm, workers, cache_stats):
    """Organize concepts: merge duplicates and add missing relations.

    Analyzes concept pairs by embedding similarity:
    1. Auto-merge: pairs with similarity >= 0.95 are merged immediately
    2. LLM analysis: pairs with similarity 0.88-0.95 are analyzed by LLM
       - Same concept: merged
       - Related (broader/partOf/dependsOn): relation added
       - Unrelated: skipped

    Use --skip-llm to only do auto-merge (faster, but misses relations).
    """
    from script.batch_dedup import GlobalConceptDeduplicator
    from script.clients import OpenAIClient, SparqlClient
    from script.embedding_cache import EmbeddingCache

    # Get OpenAI API key
    openai_key = os.environ.get("OPENAI_API_KEY")
    if not openai_key:
        from dotenv import load_dotenv
        load_dotenv()
        openai_key = os.environ.get("OPENAI_API_KEY")

    if not openai_key:
        click.echo("Error: OPENAI_API_KEY environment variable not set", err=True)
        sys.exit(1)

    # Initialize clients
    sparql = SparqlClient(repo=ctx.obj["repo"])
    openai = OpenAIClient(api_key=openai_key)
    cache = EmbeddingCache(openai)

    # Show cache stats if requested
    if cache_stats:
        stats = cache.stats()
        click.echo(f"Embedding cache: {stats['count']} entries, "
                  f"{stats['size_bytes'] / 1024:.1f} KB")
        return

    # Initialize and run deduplicator
    dedup = GlobalConceptDeduplicator(
        sparql=sparql,
        openai=openai,
        embedding_cache=cache,
    )

    auto_merged, llm_merged, relations_added = dedup.run(skip_llm=skip_llm, workers=workers)

    click.echo(f"\nDone: {auto_merged} auto-merged, {llm_merged} LLM-merged, {relations_added} relations added")


def main():
    """Entry point."""
    try:
        cli()
    except KeyboardInterrupt:
        click.echo("\nInterrupted")
        sys.exit(130)


if __name__ == "__main__":
    main()
