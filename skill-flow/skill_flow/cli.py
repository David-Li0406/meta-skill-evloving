"""CLI entry point for SkillFlow index operations."""

import argparse
import json
import logging
from pathlib import Path

from skill_flow.config import Config, load_config
from skill_flow.corpus.loader import load_corpus
from skill_flow.index.builder import build_index
from skill_flow.index.encoder import Encoder
from skill_flow.models.core import SkillFlow
from skill_flow.pipeline.cli_pipeline import run_pipeline_command
from skill_flow.refiner import RefinerConfig, refine_library
from skill_flow.reranker.reranker import Reranker
from skill_flow.retriever.retriever import IndexSearcher
from skill_flow.selector.selector import Selector


def _build_index(args: argparse.Namespace, config: Config) -> None:
    corpus_path = Path(args.corpus_path or config.index.input_corpus_path)
    output_dir = Path(args.output_dir or config.index.output_index_path)

    skills = load_corpus(corpus_path)
    encoder = Encoder(config.models.retriever)
    build_index(
        skills, encoder, output_dir, batch_size=args.batch_size, corpus_path=corpus_path
    )


def _search(args: argparse.Namespace, config: Config) -> None:
    index_dir = Path(args.index_dir or config.index.output_index_path)
    encoder = Encoder(config.models.retriever)
    searcher = IndexSearcher(index_dir, encoder, config.models.retriever)

    rerank_enabled = (
        args.rerank if args.rerank is not None else config.models.reranker.enabled
    )
    reranker = Reranker(config.models.reranker) if rerank_enabled else None
    deep_reranker = (
        Reranker(config.models.deep_reranker)
        if reranker and config.models.deep_reranker.enabled
        else None
    )
    selector = (
        Selector(config.models.selector)
        if deep_reranker and config.models.selector.enabled
        else None
    )
    retriever = SkillFlow(searcher, reranker, deep_reranker, selector)

    results = retriever.search(args.query, top_k=args.top_k)
    for i, r in enumerate(results, 1):
        print(f"{i:>3}. [{r.score:.4f}] {r.key}")


def main() -> None:
    """Parse arguments and dispatch to the appropriate subcommand."""
    parser = argparse.ArgumentParser(
        prog="skillflow",
        description="SkillFlow index CLI",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    build_p = sub.add_parser("build-index", help="Build FAISS index from corpus")
    build_p.add_argument(
        "--config",
        default=None,
        help="Path to config JSON (default: skill_flow/config/default.json)",
    )
    build_p.add_argument("--corpus-path", default=None, help="Path to corpus directory")
    build_p.add_argument(
        "--output-dir", default=None, help="Directory for index artifacts"
    )
    build_p.add_argument(
        "--batch-size", type=int, default=256, help="Encoding batch size"
    )

    search_p = sub.add_parser("search", help="Search the FAISS index")
    search_p.add_argument("--config", default=None, help="Path to config JSON")
    search_p.add_argument("--index-dir", default=None, help="Index artifacts directory")
    search_p.add_argument("--query", required=True, help="Search query")
    search_p.add_argument("--top-k", type=int, default=10, help="Number of results")
    search_p.add_argument(
        "--rerank",
        action=argparse.BooleanOptionalAction,
        default=None,
        help="Enable/disable cross-encoder reranking (overrides config)",
    )

    pipeline_p = sub.add_parser(
        "pipeline", help="Process a task directory through the SkillFlow pipeline"
    )
    pipeline_p.add_argument("--config", default=None, help="Path to config JSON")
    pipeline_p.add_argument(
        "--tasks-dir", default=None, help="Task dir with instruction.md subdirs"
    )
    pipeline_p.add_argument("--output-dir", default=None, help="Output directory")
    pipeline_p.add_argument(
        "--max-tasks", type=int, default=0, help="Limit tasks (0=all)"
    )
    pipeline_p.add_argument(
        "--max-query-chars",
        type=int,
        default=0,
        help="Truncate queries (0=no limit)",
    )

    refine_p = sub.add_parser(
        "refine",
        help="SkillX-style cluster+merge+filter refinement of the skill library",
    )
    refine_p.add_argument(
        "--config",
        required=True,
        help="Path to RefinerConfig JSON (standalone, NOT the default Config)",
    )
    refine_p.add_argument(
        "--source-corpus-dir",
        default=None,
        help="Override RefinerConfig.source_corpus_dir",
    )
    refine_p.add_argument(
        "--source-index-dir",
        default=None,
        help="Override RefinerConfig.source_index_dir",
    )
    refine_p.add_argument(
        "--output-corpus",
        default=None,
        help="Override RefinerConfig.output_corpus_dir",
    )
    refine_p.add_argument(
        "--report-dir",
        default=None,
        help="Override RefinerConfig.report_dir",
    )

    args = parser.parse_args()
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )

    if args.command == "refine":
        _refine(args)
        return

    config_path = Path(args.config) if args.config else None
    config = load_config(config_path)

    if args.command == "build-index":
        _build_index(args, config)
    elif args.command == "search":
        _search(args, config)
    elif args.command == "pipeline":
        run_pipeline_command(args, config)


def _refine(args: argparse.Namespace) -> None:
    """Load a standalone RefinerConfig JSON and run refinement."""
    data = json.loads(Path(args.config).read_text(encoding="utf-8"))
    overrides: dict[str, str] = {}
    if args.source_corpus_dir:
        overrides["source_corpus_dir"] = args.source_corpus_dir
    if args.source_index_dir:
        overrides["source_index_dir"] = args.source_index_dir
    if args.output_corpus:
        overrides["output_corpus_dir"] = args.output_corpus
    if args.report_dir:
        overrides["report_dir"] = args.report_dir
    data.update(overrides)
    config = RefinerConfig.model_validate(data)
    report = refine_library(config)
    print(
        f"\n=== refine summary ===\n"
        f"  before:           {report.before_count}\n"
        f"  after:            {report.after_count}\n"
        f"  clusters:         {report.clusters_total}\n"
        f"  merged clusters:  {report.clusters_merged}\n"
        f"  merge failures:   {report.merge_failures}\n"
        f"  dropped (filter): {report.dropped_by_filter}\n"
        f"  kept singletons:  {report.kept_singletons}\n"
        f"  kept merged:      {report.kept_merged}\n"
        f"  elapsed:          {report.elapsed_sec}s",
    )


if __name__ == "__main__":
    main()
