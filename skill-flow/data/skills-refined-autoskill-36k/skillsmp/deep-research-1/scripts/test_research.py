#!/usr/bin/env python3
"""
Test suite for Deep Research Skill

Run: python test_research.py
"""

import sys
import os
import unittest
from unittest.mock import patch, MagicMock

# Add scripts directory to path
scripts_dir = os.path.dirname(os.path.abspath(__file__))
if scripts_dir not in sys.path:
    sys.path.insert(0, scripts_dir)


class TestLLMClient(unittest.TestCase):
    """Test cases for LLM client module."""

    def test_mock_response_json(self):
        """Test mock response returns valid JSON for plan requests."""
        from llm_client import mock_response

        response = mock_response("Create a JSON plan")

        import json

        data = json.loads(response)
        self.assertIn("steps", data)
        self.assertIsInstance(data["steps"], list)

    def test_mock_response_report(self):
        """Test mock response returns markdown for reports."""
        from llm_client import mock_response

        response = mock_response("Write a report")

        self.assertIn("Mock", response)
        self.assertIn("#", response)  # Has markdown headers

    def test_llm_complete_without_keys(self):
        """Test llm_complete falls back to mock without API keys."""
        from llm_client import llm_complete

        # Clear API keys
        with patch.dict(os.environ, {}, clear=True):
            response = llm_complete("Test prompt with JSON")

            # Should return mock response
            self.assertIn("steps", response.lower())


class TestSearchEngine(unittest.TestCase):
    """Test cases for search engine module."""

    def test_import(self):
        """Test search engine is importable."""
        import importlib.util

        spec = importlib.util.find_spec("search_engine")
        self.assertIsNotNone(spec, "search_engine module not found")

    def test_search_returns_list(self):
        """Test search returns a list."""
        from search_engine import SearchEngine

        with patch("search_engine.DDGS") as mock_ddgs:
            mock_instance = MagicMock()
            mock_ddgs.return_value = mock_instance
            mock_instance.text.return_value = [
                {"title": "Test", "href": "https://test.com", "body": "Test body"}
            ]

            engine = SearchEngine()
            results = engine.search("test query", max_results=1)

            self.assertIsInstance(results, list)


class TestWebScraper(unittest.TestCase):
    """Test cases for web scraper module."""

    def test_import(self):
        """Test scraper is importable."""
        import importlib.util

        spec = importlib.util.find_spec("scraper")
        self.assertIsNotNone(spec, "scraper module not found")

    def test_fetch_handles_error(self):
        """Test fetch_content handles errors gracefully."""
        from scraper import WebScraper

        scraper = WebScraper()

        # Invalid URL should return empty string
        result = scraper.fetch_content("invalid-url")
        self.assertEqual(result, "")


class TestDeepResearch(unittest.TestCase):
    """Test cases for DeepResearch class."""

    def test_create_plan_structure(self):
        """Test create_plan returns correct structure."""
        from run import DeepResearch

        def mock_llm(prompt):
            return '{"steps": [{"query": "test", "rationale": "test"}]}'

        with patch("run.SearchEngine"), patch("run.WebScraper"):
            researcher = DeepResearch(llm_callback=mock_llm)

            # Mock archive
            researcher.archive.create_session = MagicMock(return_value="test_session")

            result = researcher.create_plan("test topic")

            self.assertIn("session_id", result)
            self.assertIn("topic", result)
            self.assertIn("plan", result)
            self.assertIn("steps", result["plan"])

    def test_create_plan_fallback(self):
        """Test create_plan uses fallback on invalid LLM response."""
        from run import DeepResearch

        def mock_llm(prompt):
            return "invalid json response"

        with patch("run.SearchEngine"), patch("run.WebScraper"):
            researcher = DeepResearch(llm_callback=mock_llm)
            researcher.archive.create_session = MagicMock(return_value="test_session")

            result = researcher.create_plan("test topic")

            # Should have fallback plan
            self.assertIn("steps", result["plan"])
            self.assertEqual(len(result["plan"]["steps"]), 3)


class TestIntegration(unittest.TestCase):
    """Integration tests (may require network/API)."""

    @unittest.skipIf("--skip-network" in sys.argv, "Skipping network tests")
    def test_real_search(self):
        """Test actual search (requires network)."""
        from search_engine import SearchEngine

        engine = SearchEngine()
        results = engine.search("Python programming", max_results=2)

        self.assertIsInstance(results, list)
        # DuckDuckGo should return results
        if results:
            self.assertIn("title", results[0])
            self.assertIn("href", results[0])


def run_tests():
    """Run all tests."""
    print("=" * 60)
    print("Deep Research Skill - Test Suite")
    print("=" * 60)

    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add test cases
    suite.addTests(loader.loadTestsFromTestCase(TestLLMClient))
    suite.addTests(loader.loadTestsFromTestCase(TestSearchEngine))
    suite.addTests(loader.loadTestsFromTestCase(TestWebScraper))
    suite.addTests(loader.loadTestsFromTestCase(TestDeepResearch))

    # Add integration tests if not skipping
    if "--skip-network" not in sys.argv:
        suite.addTests(loader.loadTestsFromTestCase(TestIntegration))

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(run_tests())
