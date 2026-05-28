"""Tests for session module."""

import sys
import tempfile
from pathlib import Path
from unittest.mock import patch

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from session import SessionState, save_checkpoint


class TestSessionState:
    def test_create_session_state(self):
        session = SessionState(
            session_id="test-session",
            spec="# Test Spec\n\nContent here.",
            round=1,
            doc_type="tech",
            models=["gpt-4o", "gemini/gemini-2.0-flash"],
        )
        assert session.session_id == "test-session"
        assert session.round == 1
        assert session.doc_type == "tech"
        assert len(session.models) == 2

    def test_default_values(self):
        # Mutation: changing default values would fail these checks
        session = SessionState(
            session_id="defaults-test",
            spec="spec",
            round=1,
            doc_type="tech",
            models=["gpt-4o"],
        )
        # Verify default values are exactly as expected
        assert session.focus is None  # Not ""
        assert session.persona is None  # Not ""
        assert session.preserve_intent is False  # Not True
        assert session.created_at == ""  # Not None or other
        assert session.updated_at == ""  # Not None or other
        assert session.history == []  # Not None

    def test_session_with_optional_fields(self):
        session = SessionState(
            session_id="test",
            spec="spec",
            round=2,
            doc_type="prd",
            models=["gpt-4o"],
            focus="security",
            persona="security-engineer",
            preserve_intent=True,
        )
        assert session.focus == "security"
        assert session.persona == "security-engineer"
        assert session.preserve_intent is True

    def test_save_and_load_session(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            sessions_dir = Path(tmpdir) / "sessions"

            with patch("session.SESSIONS_DIR", sessions_dir):
                session = SessionState(
                    session_id="save-test",
                    spec="test spec content",
                    round=3,
                    doc_type="tech",
                    models=["gpt-4o"],
                    focus="performance",
                )
                session.save()

                # Verify file exists
                assert (sessions_dir / "save-test.json").exists()

                # Load and verify
                loaded = SessionState.load("save-test")
                assert loaded.session_id == "save-test"
                assert loaded.spec == "test spec content"
                assert loaded.round == 3
                assert loaded.focus == "performance"
                assert loaded.updated_at != ""

    def test_save_creates_nested_directories(self):
        # Mutation: parents=True → parents=False would fail when parent doesn't exist
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create a path with multiple non-existent parents
            sessions_dir = Path(tmpdir) / "deep" / "nested" / "sessions"

            with patch("session.SESSIONS_DIR", sessions_dir):
                session = SessionState(
                    session_id="nested-test",
                    spec="spec",
                    round=1,
                    doc_type="tech",
                    models=["gpt-4o"],
                )
                # This should create all parent directories
                session.save()
                assert (sessions_dir / "nested-test.json").exists()

    def test_load_nonexistent_session_raises(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            sessions_dir = Path(tmpdir) / "sessions"
            sessions_dir.mkdir()

            with patch("session.SESSIONS_DIR", sessions_dir):
                try:
                    SessionState.load("nonexistent")
                    assert False, "Should have raised FileNotFoundError"
                except FileNotFoundError as e:
                    assert "nonexistent" in str(e)

    def test_list_sessions_empty(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            sessions_dir = Path(tmpdir) / "sessions"

            with patch("session.SESSIONS_DIR", sessions_dir):
                sessions = SessionState.list_sessions()
                assert sessions == []

    def test_list_sessions_returns_sorted(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            sessions_dir = Path(tmpdir) / "sessions"
            sessions_dir.mkdir()

            with patch("session.SESSIONS_DIR", sessions_dir):
                # Create two sessions
                s1 = SessionState(
                    session_id="first",
                    spec="spec1",
                    round=1,
                    doc_type="prd",
                    models=["gpt-4o"],
                )
                s1.save()

                s2 = SessionState(
                    session_id="second",
                    spec="spec2",
                    round=2,
                    doc_type="tech",
                    models=["gemini/gemini-2.0-flash"],
                )
                s2.save()

                sessions = SessionState.list_sessions()
                assert len(sessions) == 2
                # Most recent first
                assert sessions[0]["id"] == "second"
                assert sessions[1]["id"] == "first"

    def test_list_sessions_dict_keys(self):
        # Mutation: changing dict keys would fail this test
        with tempfile.TemporaryDirectory() as tmpdir:
            sessions_dir = Path(tmpdir) / "sessions"
            sessions_dir.mkdir()

            with patch("session.SESSIONS_DIR", sessions_dir):
                s = SessionState(
                    session_id="test",
                    spec="spec",
                    round=5,
                    doc_type="tech",
                    models=["gpt-4o"],
                )
                s.save()

                sessions = SessionState.list_sessions()
                assert len(sessions) == 1
                session = sessions[0]
                # Verify exact keys
                assert "id" in session
                assert "round" in session
                assert "doc_type" in session
                assert "updated_at" in session
                # Verify values
                assert session["round"] == 5
                assert session["doc_type"] == "tech"

    def test_session_history_append(self):
        session = SessionState(
            session_id="history-test",
            spec="spec",
            round=1,
            doc_type="tech",
            models=["gpt-4o"],
        )
        assert session.history == []

        session.history.append(
            {
                "round": 1,
                "all_agreed": False,
                "models": [{"model": "gpt-4o", "agreed": False}],
            }
        )
        assert len(session.history) == 1
        assert session.history[0]["round"] == 1


class TestSaveCheckpoint:
    def test_save_checkpoint_creates_file(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            checkpoint_dir = Path(tmpdir) / "checkpoints"

            with patch("session.CHECKPOINTS_DIR", checkpoint_dir):
                save_checkpoint("# Test Spec", 1)

                assert (checkpoint_dir / "round-1.md").exists()
                content = (checkpoint_dir / "round-1.md").read_text()
                assert content == "# Test Spec"

    def test_save_checkpoint_with_session_id(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            checkpoint_dir = Path(tmpdir) / "checkpoints"

            with patch("session.CHECKPOINTS_DIR", checkpoint_dir):
                save_checkpoint("# Test Spec", 2, session_id="my-session")

                assert (checkpoint_dir / "my-session-round-2.md").exists()

    def test_save_checkpoint_creates_nested_directories(self):
        # Mutation: parents=True → parents=False would fail
        with tempfile.TemporaryDirectory() as tmpdir:
            checkpoint_dir = Path(tmpdir) / "deep" / "nested" / "checkpoints"

            with patch("session.CHECKPOINTS_DIR", checkpoint_dir):
                save_checkpoint("# Nested Spec", 3)
                assert (checkpoint_dir / "round-3.md").exists()

    def test_save_checkpoint_filename_format(self):
        # Mutation: wrong prefix/suffix format would fail
        with tempfile.TemporaryDirectory() as tmpdir:
            checkpoint_dir = Path(tmpdir) / "checkpoints"

            with patch("session.CHECKPOINTS_DIR", checkpoint_dir):
                save_checkpoint("spec", 5, session_id="test-session")
                # Should be exactly "test-session-round-5.md"
                expected = checkpoint_dir / "test-session-round-5.md"
                assert expected.exists()
                # Verify no other files created
                files = list(checkpoint_dir.glob("*.md"))
                assert len(files) == 1
                assert files[0].name == "test-session-round-5.md"

    def test_save_checkpoint_exist_ok(self):
        # Mutation: exist_ok=True → exist_ok=False would fail on second call
        with tempfile.TemporaryDirectory() as tmpdir:
            checkpoint_dir = Path(tmpdir) / "checkpoints"

            with patch("session.CHECKPOINTS_DIR", checkpoint_dir):
                save_checkpoint("spec v1", 1)
                # Second call with same directory should not fail
                save_checkpoint("spec v2", 2)
                assert (checkpoint_dir / "round-1.md").exists()
                assert (checkpoint_dir / "round-2.md").exists()


class TestListSessionsEdgeCases:
    def test_list_sessions_missing_updated_at(self):
        # Mutation: data.get("updated_at", "") → data.get("updated_at", "XXXX")
        import json

        with tempfile.TemporaryDirectory() as tmpdir:
            sessions_dir = Path(tmpdir) / "sessions"
            sessions_dir.mkdir()

            # Create session without updated_at field
            session_data = {
                "session_id": "old-session",
                "spec": "spec",
                "round": 1,
                "doc_type": "tech",
                "models": ["gpt-4o"],
                # Intentionally no updated_at
            }
            (sessions_dir / "old-session.json").write_text(json.dumps(session_data))

            with patch("session.SESSIONS_DIR", sessions_dir):
                sessions = SessionState.list_sessions()
                assert len(sessions) == 1
                # Default should be empty string, not "XXXX"
                assert sessions[0]["updated_at"] == ""

    def test_list_sessions_sorting_with_missing_updated_at(self):
        # Mutation: sorted(..., key=lambda x: x.get("updated_at", "")) default change
        import json

        with tempfile.TemporaryDirectory() as tmpdir:
            sessions_dir = Path(tmpdir) / "sessions"
            sessions_dir.mkdir()

            # Create two sessions - one with updated_at, one without
            # Empty string sorts before any date, so session without updated_at should be last
            session1 = {
                "session_id": "new-session",
                "spec": "spec",
                "round": 1,
                "doc_type": "tech",
                "models": ["gpt-4o"],
                "updated_at": "2024-01-15T12:00:00",
            }
            session2 = {
                "session_id": "old-session",
                "spec": "spec",
                "round": 1,
                "doc_type": "tech",
                "models": ["gpt-4o"],
                # No updated_at - should sort to end
            }
            (sessions_dir / "new-session.json").write_text(json.dumps(session1))
            (sessions_dir / "old-session.json").write_text(json.dumps(session2))

            with patch("session.SESSIONS_DIR", sessions_dir):
                sessions = SessionState.list_sessions()
                assert len(sessions) == 2
                # Session with date should come first (reverse=True means newer first)
                assert sessions[0]["id"] == "new-session"
                assert sessions[1]["id"] == "old-session"
