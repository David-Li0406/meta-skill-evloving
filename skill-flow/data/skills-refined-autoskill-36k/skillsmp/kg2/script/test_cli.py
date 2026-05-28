"""Integration tests for CLI commands using mock clients."""

import sys
from pathlib import Path

from script.collector import Collector
from script.mocks import (
    MockOpenAIClient,
    MockSemanticScholarClient,
    MockSparqlClient,
    create_test_paper,
)
from script.models import Config

# pytest may not be installed (optional for running tests manually)
try:
    import pytest  # noqa: E402
except ImportError:
    pytest = None  # type: ignore[assignment]

# Support direct execution
if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).parent.parent))


class TestInitCommand:
    """Tests for the init command."""

    def test_init_with_single_seed(self):
        """Initialize with a single seed paper."""
        paper = create_test_paper(
            id="abc123",
            title="Attention Is All You Need",
            year=2017,
            doi="10.1234/attention",
        )

        ss = MockSemanticScholarClient()
        ss.add_paper("DOI:10.1234/attention", paper)

        collector = Collector(
            db_path=":memory:",
            sparql_client=MockSparqlClient(),
            ss_client=ss,
        )

        collector.initialize(["DOI:10.1234/attention"])

        # Verify paper was saved
        assert collector.db.paper_exists("abc123")
        config = collector.db.load_config()
        assert config is not None
        assert config.seed_ids == ["DOI:10.1234/attention"]

    def test_init_with_multiple_seeds(self):
        """Initialize with multiple seed papers."""
        paper1 = create_test_paper(id="p1", title="Paper 1", year=2020)
        paper2 = create_test_paper(id="p2", title="Paper 2", year=2018)

        ss = MockSemanticScholarClient()
        ss.add_paper("DOI:10.1/p1", paper1)
        ss.add_paper("DOI:10.1/p2", paper2)

        collector = Collector(
            db_path=":memory:",
            sparql_client=MockSparqlClient(),
            ss_client=ss,
        )

        collector.initialize(["DOI:10.1/p1", "DOI:10.1/p2"])

        assert collector.db.paper_exists("p1")
        assert collector.db.paper_exists("p2")
        assert collector.db.count_papers() == 2

    def test_init_skips_not_found(self):
        """Papers not found are skipped."""
        paper = create_test_paper(id="found", title="Found Paper")

        ss = MockSemanticScholarClient()
        ss.add_paper("DOI:10.1/found", paper)
        ss.mark_not_found("DOI:10.1/missing")

        collector = Collector(
            db_path=":memory:",
            sparql_client=MockSparqlClient(),
            ss_client=ss,
        )

        collector.initialize(["DOI:10.1/found", "DOI:10.1/missing"])

        assert collector.db.paper_exists("found")
        assert not collector.db.paper_exists("missing")
        assert collector.db.count_papers() == 1

    def test_init_enqueues_neighbors(self):
        """References and citations are enqueued."""
        paper = create_test_paper(
            id="main",
            title="Main Paper",
            references=["ref1", "ref2"],
            citations=["cit1"],
        )

        ss = MockSemanticScholarClient()
        ss.add_paper("DOI:10.1/main", paper)

        collector = Collector(
            db_path=":memory:",
            sparql_client=MockSparqlClient(),
            ss_client=ss,
        )

        collector.initialize(["DOI:10.1/main"])

        stats = collector.db.stats()
        assert stats.queue.get('pending', 0) == 3  # ref1, ref2, cit1


class TestRunCommand:
    """Tests for the run command."""

    def test_run_processes_queue(self):
        """Run processes papers from the queue."""
        seed = create_test_paper(id="seed", title="Seed", references=["ref1"])
        ref = create_test_paper(id="ref1", title="Reference Paper")

        ss = MockSemanticScholarClient()
        ss.add_paper("DOI:10.1/seed", seed)
        ss.add_paper("ref1", ref)

        collector = Collector(
            db_path=":memory:",
            sparql_client=MockSparqlClient(),
            ss_client=ss,
        )

        collector.initialize(["DOI:10.1/seed"])
        collector.run(max_iterations=1)

        assert collector.db.paper_exists("ref1")
        assert collector.db.count_papers() == 2

    def test_run_skips_not_found(self):
        """Papers not found in API are skipped."""
        seed = create_test_paper(id="seed", title="Seed", references=["missing"])

        ss = MockSemanticScholarClient()
        ss.add_paper("DOI:10.1/seed", seed)
        ss.mark_not_found("missing")

        collector = Collector(
            db_path=":memory:",
            sparql_client=MockSparqlClient(),
            ss_client=ss,
        )

        collector.initialize(["DOI:10.1/seed"])
        collector.run(max_iterations=1)

        assert not collector.db.paper_exists("missing")
        stats = collector.db.stats()
        assert stats.queue.get('skipped', 0) == 1

    def test_run_respects_max_papers(self):
        """Run stops at max_papers."""
        seed = create_test_paper(
            id="seed", title="Seed",
            references=["r1", "r2", "r3", "r4", "r5"]
        )

        ss = MockSemanticScholarClient()
        ss.add_paper("DOI:10.1/seed", seed)
        for i in range(1, 6):
            ss.add_paper(f"r{i}", create_test_paper(id=f"r{i}", title=f"Ref {i}"))

        collector = Collector(
            db_path=":memory:",
            sparql_client=MockSparqlClient(),
            ss_client=ss,
        )

        config = Config(seed_ids=["DOI:10.1/seed"], max_papers=3)
        collector.initialize(["DOI:10.1/seed"], config=config)
        collector.run()

        assert collector.db.count_papers() == 3  # seed + 2 refs


class TestStatusCommand:
    """Tests for the status command."""

    def test_stats_returns_counts(self):
        """Stats returns paper and queue counts."""
        seed = create_test_paper(id="seed", title="Seed", references=["r1", "r2"])

        ss = MockSemanticScholarClient()
        ss.add_paper("DOI:10.1/seed", seed)

        collector = Collector(
            db_path=":memory:",
            sparql_client=MockSparqlClient(),
            ss_client=ss,
        )

        collector.initialize(["DOI:10.1/seed"])
        stats = collector.stats()

        assert stats['total_papers'] == 1
        assert stats['papers']['seed'] == 1
        assert stats['queue']['pending'] == 2


class TestEnrichCommand:
    """Tests for the enrich command."""

    def test_enrich_extracts_concepts(self):
        """Enrich extracts concepts from paper."""
        seed = create_test_paper(
            id="seed",
            title="Attention Is All You Need",
            abstract="We propose the Transformer architecture.",
        )

        ss = MockSemanticScholarClient()
        ss.add_paper("DOI:10.1/seed", seed)

        openai = MockOpenAIClient()
        openai.set_extraction_response(
            concepts=[
                {"name": "Transformer", "description": "A neural network architecture",
                 "broader": None, "partOf": None, "dependsOn": None},
            ],
            claims=[
                {"text": "Transformers achieve state-of-the-art results",
                 "regarding": ["Transformer"],
                 "extends": None, "refutes": None, "supports": None},
            ],
        )

        sparql = MockSparqlClient()

        collector = Collector(
            db_path=":memory:",
            sparql_client=sparql,
            ss_client=ss,
            openai_client=openai,
        )

        collector.initialize(["DOI:10.1/seed"])
        collector.enrich(max_papers=1)

        # Verify LLM was called
        assert len(openai.call_history) == 1
        assert openai.call_history[0]['schema_name'] == 'paper_extraction'

        # Verify paper marked as enriched
        stats = collector.db.stats()
        assert stats.enriched == 1

    def test_enrich_skips_no_abstract(self):
        """Papers without abstract are marked enriched but not processed."""
        seed = create_test_paper(id="seed", title="No Abstract", abstract=None)

        ss = MockSemanticScholarClient()
        ss.add_paper("DOI:10.1/seed", seed)

        openai = MockOpenAIClient()

        collector = Collector(
            db_path=":memory:",
            sparql_client=MockSparqlClient(),
            ss_client=ss,
            openai_client=openai,
        )

        collector.initialize(["DOI:10.1/seed"])
        collector.enrich(max_papers=1)

        # LLM should not be called
        assert len(openai.call_history) == 0

        # But paper should be marked enriched
        stats = collector.db.stats()
        assert stats.enriched == 1


class TestLinkCommand:
    """Tests for the link command."""

    def test_link_finds_relations(self):
        """Link finds relations between claims."""
        seed = create_test_paper(
            id="seed",
            title="Test Paper",
            abstract="Test abstract",
            references=["ref1"],
        )
        ref = create_test_paper(id="ref1", title="Reference")

        ss = MockSemanticScholarClient()
        ss.add_paper("DOI:10.1/seed", seed)
        ss.add_paper("ref1", ref)

        sparql = MockSparqlClient()
        # Add claims for the papers
        sparql.add_claim("paper:cl_1", {
            "paper_uri": "paper:pa_00000001",
            "text": "Our method improves performance",
        })
        sparql.add_claim("paper:cl_2", {
            "paper_uri": "paper:pa_00000002",
            "text": "Baseline achieves 80% accuracy",
        })

        openai = MockOpenAIClient()
        openai.set_relations_response([
            {"from_uri": "paper:cl_1", "type": "extends", "to_uri": "paper:cl_2"},
        ])

        collector = Collector(
            db_path=":memory:",
            sparql_client=sparql,
            ss_client=ss,
            openai_client=openai,
        )

        collector.initialize(["DOI:10.1/seed"])

        # Manually mark as enriched for testing
        collector.db.mark_enriched("seed")
        collector.db.commit()

        collector.link(max_papers=1)

        # Verify paper marked as link-checked
        stats = collector.db.stats()
        assert stats.linked == 1


class TestRunAutoResume:
    """Tests for run command's auto-resume behavior."""

    def test_run_resets_processing_before_run(self):
        """Run resets processing items to pending before collecting."""
        seed = create_test_paper(id="seed", title="Seed", references=["r1"])
        ref = create_test_paper(id="r1", title="Reference")

        ss = MockSemanticScholarClient()
        ss.add_paper("DOI:10.1/seed", seed)
        ss.add_paper("r1", ref)

        collector = Collector(
            db_path=":memory:",
            sparql_client=MockSparqlClient(),
            ss_client=ss,
        )

        collector.initialize(["DOI:10.1/seed"])

        # Manually set an item to processing (simulating interrupted state)
        collector.db.update_queue_status("r1", "processing")
        collector.db.commit()

        stats_before = collector.db.stats()
        assert stats_before.queue.get('processing', 0) == 1

        # Run should auto-resume and process the paper
        collector.resume()
        collector.run(max_iterations=1)

        # Paper should now be collected
        assert collector.db.paper_exists("r1")
        stats_after = collector.db.stats()
        assert stats_after.queue.get('processing', 0) == 0


# --- Run tests ---

if __name__ == '__main__':
    if pytest:
        pytest.main([__file__, '-v'])
    else:
        # Run tests without pytest
        import sys
        failed = 0
        passed = 0
        for name, cls in list(globals().items()):
            if isinstance(cls, type) and name.startswith('Test'):
                instance = cls()
                for method in dir(instance):
                    if method.startswith('test_'):
                        try:
                            getattr(instance, method)()
                            print(f"PASS: {name}.{method}")
                            passed += 1
                        except AssertionError as e:
                            print(f"FAIL: {name}.{method}: {e}")
                            failed += 1
                        except Exception as e:
                            print(f"ERROR: {name}.{method}: {e}")
                            failed += 1
        print(f"\n{passed} passed, {failed} failed")
        sys.exit(1 if failed else 0)
