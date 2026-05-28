#!/usr/bin/env python3
"""
Tests for the Memory Skill using OpenMemory.

This module tests the MemoryClient functionality using openmemory-py.
"""

import json
import os
import sys
from pathlib import Path

import pytest

# Add skill directory to path
SKILL_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SKILL_DIR))


class TestMemoryClient:
    """Test MemoryClient with real OpenMemory."""

    @pytest.fixture
    def memory_client(self, tmp_path):
        """Create MemoryClient with temp directory."""
        from scripts.memory_client import MemoryClient

        client = MemoryClient(user_id="test_user", working_dir=str(tmp_path))
        yield client
        client.close()

    def test_add_memory(self, memory_client):
        """Test adding a memory."""
        result = memory_client.add("Test memory content", tags=["test", "unit"])

        assert result["status"] == "success"
        assert result["content"] == "Test memory content"
        assert result["tags"] == ["test", "unit"]
        assert "id" in result

    def test_add_memory_without_tags(self, memory_client):
        """Test adding a memory without tags."""
        result = memory_client.add("Simple memory")

        assert result["status"] == "success"
        assert result["content"] == "Simple memory"

    def test_add_memory_with_metadata(self, memory_client):
        """Test adding a memory with metadata."""
        result = memory_client.add(
            "Memory with metadata",
            tags=["test"],
            metadata={"source": "test", "version": 1},
        )

        assert result["status"] == "success"

    def test_query_memory(self, memory_client):
        """Test querying memories."""
        # Add some memories
        memory_client.add("User prefers dark mode", tags=["preferences"])
        memory_client.add("User likes Python programming", tags=["skills"])

        # Query
        results = memory_client.query("dark mode")

        assert isinstance(results, list)
        assert len(results) >= 1
        # Check that the relevant memory is in results
        contents = [r["content"] for r in results]
        assert any("dark mode" in c for c in contents)

    def test_query_with_limit(self, memory_client):
        """Test querying with custom limit."""
        # Add multiple memories
        for i in range(5):
            memory_client.add(f"Test memory number {i}", tags=["test"])

        # Query with limit
        results = memory_client.query("memory", limit=3)

        assert isinstance(results, list)
        assert len(results) <= 3

    def test_delete_memory(self, memory_client):
        """Test deleting a memory."""
        # Add a memory
        result = memory_client.add("To be deleted")
        memory_id = result["id"]

        # Delete
        delete_result = memory_client.delete(memory_id)

        assert delete_result["status"] == "success"
        assert delete_result["deleted_id"] == memory_id

    def test_clear_memories(self, memory_client):
        """Test clearing all memories."""
        # Add memories
        memory_client.add("Memory 1")
        memory_client.add("Memory 2")

        # Clear
        result = memory_client.clear()

        assert result["status"] == "success"

    def test_context_manager(self, tmp_path):
        """Test using MemoryClient as context manager."""
        from scripts.memory_client import MemoryClient

        original_cwd = os.getcwd()

        with MemoryClient(user_id="context_test", working_dir=str(tmp_path)) as client:
            result = client.add("Context manager test")
            assert result["status"] == "success"

        # Working directory should be restored
        assert os.getcwd() == original_cwd


class TestCLI:
    """Test the CLI interface (run.py)."""

    def test_parse_tags(self):
        """Test tag parsing function."""
        from scripts import run

        # Test normal tags
        assert run.parse_tags("tag1,tag2,tag3") == ["tag1", "tag2", "tag3"]

        # Test with spaces
        assert run.parse_tags("tag1, tag2 , tag3") == ["tag1", "tag2", "tag3"]

        # Test None
        assert run.parse_tags(None) is None

        # Test empty string
        assert run.parse_tags("") is None

    def test_format_output(self):
        """Test output formatting."""
        from scripts import run

        data = {"key": "value", "number": 42}
        output = run.format_output(data)

        # Should be valid JSON
        parsed = json.loads(output)
        assert parsed["key"] == "value"
        assert parsed["number"] == 42

    def test_format_output_with_korean(self):
        """Test output formatting with Korean characters."""
        from scripts import run

        data = {"content": "한글 테스트", "tag": "태그"}
        output = run.format_output(data)

        # Should preserve Korean characters
        assert "한글 테스트" in output
        parsed = json.loads(output)
        assert parsed["content"] == "한글 테스트"


class TestConvenienceFunctions:
    """Test module-level convenience functions."""

    @pytest.fixture(autouse=True)
    def setup_client(self, tmp_path):
        """Set up a fresh client for each test."""
        from scripts import memory_client as mc

        # Reset singleton
        mc._client = None
        mc.MEMORY_DIR = tmp_path

        yield

        # Cleanup
        if mc._client:
            mc._client.close()
        mc._client = None

    def test_convenience_add(self):
        """Test convenience add function."""
        from scripts import memory_client

        result = memory_client.add("test content", tags=["tag1"])

        assert result["status"] == "success"
        assert result["content"] == "test content"

    def test_convenience_query(self):
        """Test convenience query function."""
        from scripts import memory_client

        memory_client.add("searchable content")
        results = memory_client.query("searchable")

        assert isinstance(results, list)


class TestIntegration:
    """Integration tests with real OpenMemory."""

    def test_full_workflow(self, tmp_path):
        """Test complete memory workflow."""
        from scripts.memory_client import MemoryClient

        with MemoryClient(
            user_id="integration_test", working_dir=str(tmp_path)
        ) as client:
            # Add memories
            m1 = client.add("User prefers dark mode", tags=["preferences", "ui"])
            m2 = client.add("User is learning Python", tags=["education"])
            m3 = client.add("Meeting at 3 PM tomorrow", tags=["calendar"])

            assert m1["status"] == "success"
            assert m2["status"] == "success"
            assert m3["status"] == "success"

            # Query
            results = client.query("dark mode")
            assert len(results) >= 1
            assert any("dark mode" in r["content"] for r in results)

            # Delete
            delete_result = client.delete(m3["id"])
            assert delete_result["status"] == "success"

    def test_korean_content(self, tmp_path):
        """Test handling Korean content."""
        from scripts.memory_client import MemoryClient

        with MemoryClient(user_id="korean_test", working_dir=str(tmp_path)) as client:
            # Add Korean content
            result = client.add(
                "사용자는 Python과 TypeScript 개발에 관심이 많습니다",
                tags=["관심분야", "프로그래밍"],
            )

            assert result["status"] == "success"

            # Query with Korean
            results = client.query("Python")
            assert isinstance(results, list)
            # OpenMemory should be able to find Korean content
            if len(results) > 0:
                assert any("Python" in r["content"] for r in results)

    def test_multiple_users(self, tmp_path):
        """Test memory isolation between users."""
        from scripts.memory_client import MemoryClient

        # User 1 adds memory
        with MemoryClient(user_id="user1", working_dir=str(tmp_path)) as client1:
            client1.add("User 1's secret memory")

        # User 2 adds memory
        with MemoryClient(user_id="user2", working_dir=str(tmp_path)) as client2:
            client2.add("User 2's secret memory")

            # User 2 should not see User 1's memory
            results = client2.query("User 1")
            # Results should be empty or not contain User 1's content
            user1_contents = [r for r in results if "User 1" in r.get("content", "")]
            # Ideally should be empty due to user isolation
            assert len(user1_contents) == 0 or len(results) == 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
