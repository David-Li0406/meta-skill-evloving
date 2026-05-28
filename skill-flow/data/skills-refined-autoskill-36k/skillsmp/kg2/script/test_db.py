"""Database operations specs."""

import pytest

from script.db import Database
from script.models import Author, Config, Paper, Venue


@pytest.fixture
def db():
    """In-memory database for testing."""
    database = Database(":memory:")
    yield database
    database.close()


def paper(id="p1", status="collected", year=2023, refs=None, cites=None, title=None, **kw):
    """Create test paper with sensible defaults."""
    return Paper(
        id=id, title=title or f"Paper {id}", year=year,
        authors=[Author(name="Test Author")],
        references=refs or [], citations=cites or [], status=status, **kw
    )


class TestConfig:
    def test_save_and_retrieve(self, db):
        db.save_config("key", "value")
        assert db.get_config("key") == "value"

    def test_missing_key_returns_default(self, db):
        assert db.get_config("missing", "default") == "default"
        assert db.get_config("missing") is None

    def test_overwrite(self, db):
        db.save_config("key", "v1")
        db.save_config("key", "v2")
        assert db.get_config("key") == "v2"

    def test_complex_values(self, db):
        db.save_config("list", [1, 2, 3])
        db.save_config("dict", {"a": 1})
        assert db.get_config("list") == [1, 2, 3]
        assert db.get_config("dict") == {"a": 1}

    def test_full_config_roundtrip(self, db):
        config = Config(seed_ids=["a", "b"], max_papers=500)
        db.save_full_config(config)

        loaded = db.load_config()
        assert loaded.seed_ids == ["a", "b"]
        assert loaded.max_papers == 500

    def test_load_config_before_init_returns_none(self, db):
        assert db.load_config() is None


class TestPapers:
    def test_insert_and_load_roundtrip(self, db):
        p = paper(
            id="p1", title="Test", year=2020, doi="10.1/test",
            refs=["r1", "r2"], cites=["c1"]
        )
        db.insert_paper(p, "paper:pa_001")

        loaded = db.load_paper("p1")
        assert loaded.id == "p1"
        assert loaded.title == "Test"
        assert loaded.doi == "10.1/test"
        assert loaded.references == ["r1", "r2"]

    def test_exists(self, db):
        assert not db.paper_exists("p1")
        db.insert_paper(paper(), "uri")
        assert db.paper_exists("p1")

    def test_get_kg2_uri(self, db):
        assert db.get_kg2_uri("missing") is None
        db.insert_paper(paper(), "paper:pa_001")
        assert db.get_kg2_uri("p1") == "paper:pa_001"

    def test_load_missing_returns_none(self, db):
        assert db.load_paper("missing") is None

    def test_count(self, db):
        assert db.count_papers() == 0
        for i in range(3):
            db.insert_paper(paper(id=f"p{i}"), f"uri{i}")
        assert db.count_papers() == 3

    def test_get_seed_ids(self, db):
        db.insert_paper(paper(id="s1", status="seed"), "u1")
        db.insert_paper(paper(id="s2", status="seed"), "u2")
        db.insert_paper(paper(id="c1", status="collected"), "u3")
        assert db.get_seed_ids() == {"s1", "s2"}

    def test_get_collected_ids(self, db):
        db.insert_paper(paper(id="p1"), "u1")
        db.insert_paper(paper(id="p2"), "u2")
        assert db.get_collected_ids() == {"p1", "p2"}

    def test_venue_roundtrip(self, db):
        p = Paper(
            id="p1", title="T", authors=[Author(name="A")], year=2023,
            venue=Venue(name="NeurIPS", venue_id="v1", venue_type="conference")
        )
        db.insert_paper(p, "uri")

        loaded = db.load_paper("p1")
        assert loaded.venue.name == "NeurIPS"
        assert loaded.venue.venue_type == "conference"

    def test_paper_without_venue(self, db):
        db.insert_paper(paper(), "uri")
        assert db.load_paper("p1").venue is None


class TestQueue:
    def test_enqueue_and_exists(self, db):
        assert not db.queue_exists("p1")
        db.enqueue("p1", 0.8, "source", "reference")
        assert db.queue_exists("p1")

    def test_enqueue_skips_existing_paper(self, db):
        db.insert_paper(paper(), "uri")
        db.enqueue("p1", 0.8, "s", "ref")
        assert not db.queue_exists("p1")

    def test_enqueue_skips_duplicate(self, db):
        db.enqueue("p1", 0.8, "s1", "ref")
        db.enqueue("p1", 0.9, "s2", "cit")  # ignored
        assert db.next_candidate().score == 0.8

    def test_next_candidate_ordered_by_score(self, db):
        db.enqueue("low", 0.3, "s", "ref")
        db.enqueue("high", 0.9, "s", "ref")
        db.enqueue("med", 0.6, "s", "ref")
        assert db.next_candidate().id == "high"

    def test_next_candidate_empty_returns_none(self, db):
        assert db.next_candidate() is None

    def test_next_candidate_skips_non_pending(self, db):
        db.enqueue("p1", 0.9, "s", "ref")
        db.update_queue_status("p1", "processing")
        assert db.next_candidate() is None

    def test_update_status_with_skip_reason(self, db):
        db.enqueue("p1", 0.5, "s", "ref")
        db.update_queue_status("p1", "skipped", "not_found")
        assert db.stats().queue.get("skipped") == 1


class TestPendingCites:
    def test_add_and_get(self, db):
        db.add_pending_cites("c1", "cited")
        db.add_pending_cites("c2", "cited")
        assert set(db.get_pending_cites_to("cited")) == {"c1", "c2"}

    def test_get_empty(self, db):
        assert db.get_pending_cites_to("missing") == []

    def test_delete(self, db):
        db.add_pending_cites("citing", "cited")
        db.delete_pending_cites("citing", "cited")
        assert db.get_pending_cites_to("cited") == []

    def test_duplicate_ignored(self, db):
        db.add_pending_cites("c", "cited")
        db.add_pending_cites("c", "cited")
        assert db.get_pending_cites_to("cited") == ["c"]


class TestEnrichment:
    def test_next_unenriched_paper(self, db):
        db.insert_paper(paper(title="First"), "uri")
        row = db.next_unenriched_paper()
        assert row.title == "First"

    def test_next_unenriched_empty(self, db):
        assert db.next_unenriched_paper() is None

    def test_next_unenriched_skips_enriched(self, db):
        db.insert_paper(paper(), "uri")
        db.mark_enriched("p1")
        assert db.next_unenriched_paper() is None

    def test_next_unenriched_returns_oldest_first(self, db):
        db.insert_paper(paper(id="new", year=2023), "u1")
        db.insert_paper(paper(id="old", year=2018), "u2")
        assert db.next_unenriched_paper().id == "old"

    def test_mark_enriched(self, db):
        db.insert_paper(paper(), "uri")
        db.mark_enriched("p1")
        stats = db.stats()
        assert stats.enriched == 1
        assert stats.unenriched == 0

    def test_get_enriched_refs(self, db):
        db.insert_paper(paper(id="e", title="Enriched"), "u1")
        db.insert_paper(paper(id="n", title="Not"), "u2")
        db.mark_enriched("e")

        refs = db.get_enriched_refs(["e", "n", "missing"])
        assert len(refs) == 1
        assert refs[0].title == "Enriched"

    def test_get_enriched_refs_empty_input(self, db):
        assert db.get_enriched_refs([]) == []


class TestLinking:
    def test_next_unlinked_requires_enriched(self, db):
        db.insert_paper(paper(), "uri")
        assert db.next_unlinked_paper() is None  # not enriched

        db.mark_enriched("p1")
        assert db.next_unlinked_paper().id == "p1"

    def test_next_unlinked_skips_linked(self, db):
        db.insert_paper(paper(), "uri")
        db.mark_enriched("p1")
        db.mark_link_checked("p1")
        assert db.next_unlinked_paper() is None

    def test_mark_link_checked(self, db):
        db.insert_paper(paper(), "uri")
        db.mark_enriched("p1")
        db.mark_link_checked("p1")
        assert db.stats().linked == 1

    def test_reset_link_checked_for_citers(self, db):
        db.insert_paper(paper(refs=["cited_paper"]), "uri")
        db.mark_enriched("p1")
        db.mark_link_checked("p1")

        count = db.reset_link_checked_for_citers("cited_paper")
        assert count == 1
        assert db.next_unlinked_paper().id == "p1"

    def test_reset_link_checked_no_matches(self, db):
        db.insert_paper(paper(refs=[]), "uri")
        db.mark_enriched("p1")
        db.mark_link_checked("p1")
        assert db.reset_link_checked_for_citers("other") == 0


class TestStats:
    def test_empty_stats(self, db):
        stats = db.stats()
        assert stats.total_papers == 0
        assert stats.papers == {}
        assert stats.queue == {}

    def test_stats_with_data(self, db):
        db.insert_paper(paper(id="s", status="seed"), "u1")
        db.insert_paper(paper(id="c", status="collected"), "u2")
        db.mark_enriched("s")
        db.enqueue("q1", 0.5, "s", "ref")
        db.add_pending_cites("a", "b")

        stats = db.stats()
        assert stats.total_papers == 2
        assert stats.papers["seed"] == 1
        assert stats.queue["pending"] == 1
        assert stats.pending_cites == 1
        assert stats.enriched == 1


class TestResumeOperations:
    def test_reset_processing_to_pending(self, db):
        db.enqueue("p1", 0.5, "s", "ref")
        db.enqueue("p2", 0.6, "s", "ref")
        db.update_queue_status("p1", "processing")

        assert db.reset_processing_to_pending() == 1
        assert db.stats().queue.get("pending") == 2


class TestTransactions:
    def test_rollback(self, db):
        db.insert_paper(paper(), "uri")
        db.rollback()
        assert not db.paper_exists("p1")

    def test_commit_persists(self, db):
        db.insert_paper(paper(), "uri")
        db.commit()
        assert db.paper_exists("p1")
