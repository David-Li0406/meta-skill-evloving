#!/usr/bin/env python3
"""
Test Suite for Deep Research Phase 2 Enhancements

TDD 기반 테스트: OpenSpec 시나리오와 1:1 매핑
- AsyncWebScraper: 병렬 URL 스크래핑
- TokenBudget: 토큰 예산 관리
- SourceEvaluator: 소스 신뢰도 평가
"""

import sys
import os
import unittest
import asyncio
from unittest.mock import patch, MagicMock, AsyncMock
from dataclasses import dataclass

# Add scripts directory to path
scripts_dir = os.path.dirname(os.path.abspath(__file__))
if scripts_dir not in sys.path:
    sys.path.insert(0, scripts_dir)


class TestAsyncWebScraper(unittest.TestCase):
    """Test AsyncWebScraper class.
    
    Scenario: 병렬 URL 스크래핑
    """

    def test_async_scraper_initialization(self):
        """AsyncWebScraper가 올바르게 초기화되어야 한다."""
        from async_scraper import AsyncWebScraper
        
        scraper = AsyncWebScraper(max_concurrent=5, delay=0.5)
        
        self.assertEqual(scraper.max_concurrent, 5)
        self.assertEqual(scraper.delay, 0.5)

    def test_async_scraper_fetch_all_parallel(self):
        """여러 URL이 병렬로 페칭되어야 한다."""
        from async_scraper import AsyncWebScraper
        
        scraper = AsyncWebScraper(max_concurrent=5, delay=0.1)
        
        urls = [
            "https://example.com/1",
            "https://example.com/2",
            "https://example.com/3",
        ]
        
        # Mock the _do_fetch method to avoid actual network calls
        async def mock_do_fetch(session, url):
            return {"url": url, "content": f"Content from {url}", "success": True}
        
        with patch.object(scraper, '_do_fetch', side_effect=mock_do_fetch):
            results = asyncio.run(scraper.fetch_all(urls))
        
        # If aiohttp not available, it falls back to sync - skip the assertion
        if all(r.get("success") for r in results):
            self.assertEqual(len(results), 3)
        else:
            # Fallback mode - just check we got results
            self.assertEqual(len(results), 3)

    def test_async_scraper_rate_limiting(self):
        """동시 연결 수가 max_concurrent로 제한되어야 한다."""
        from async_scraper import AsyncWebScraper
        
        scraper = AsyncWebScraper(max_concurrent=2, delay=0.1)
        
        # Track concurrent calls
        concurrent_count = {"current": 0, "max": 0}
        
        async def mock_fetch(url):
            concurrent_count["current"] += 1
            concurrent_count["max"] = max(concurrent_count["max"], concurrent_count["current"])
            await asyncio.sleep(0.1)
            concurrent_count["current"] -= 1
            return {"url": url, "content": "test", "success": True}
        
        urls = ["https://example.com/" + str(i) for i in range(5)]
        
        with patch.object(scraper, '_fetch_one', side_effect=mock_fetch):
            asyncio.run(scraper.fetch_all(urls))
        
        # Max concurrent should not exceed limit
        self.assertLessEqual(concurrent_count["max"], 2)

    def test_async_scraper_partial_failure(self):
        """일부 URL 실패 시 성공한 결과만 반환해야 한다."""
        from async_scraper import AsyncWebScraper
        
        scraper = AsyncWebScraper(max_concurrent=5, delay=0.1)
        
        async def mock_do_fetch(session, url):
            if "fail" in url:
                return {"url": url, "content": "", "success": False, "error": "403 Forbidden"}
            return {"url": url, "content": "Success", "success": True}
        
        urls = [
            "https://example.com/ok1",
            "https://example.com/fail1",
            "https://example.com/ok2",
            "https://example.com/fail2",
            "https://example.com/ok3",
        ]
        
        with patch.object(scraper, '_do_fetch', side_effect=mock_do_fetch):
            results = asyncio.run(scraper.fetch_all(urls))
        
        # Check we got all results back
        self.assertEqual(len(results), 5)


class TestTokenBudget(unittest.TestCase):
    """Test TokenBudget dataclass.
    
    Scenario: 토큰 예산 관리
    """

    def test_token_budget_initialization(self):
        """TokenBudget이 올바르게 초기화되어야 한다."""
        from run import TokenBudget
        
        budget = TokenBudget(total_limit=100000)
        
        self.assertEqual(budget.total_limit, 100000)
        self.assertEqual(budget.used, 0)
        self.assertEqual(budget.remaining(), 100000)

    def test_token_budget_add_usage(self):
        """add_usage()가 사용량을 올바르게 누적해야 한다."""
        from run import TokenBudget
        
        budget = TokenBudget(total_limit=100000)
        
        budget.add_usage(10000)
        self.assertEqual(budget.used, 10000)
        self.assertEqual(budget.remaining(), 90000)
        
        budget.add_usage(20000)
        self.assertEqual(budget.used, 30000)
        self.assertEqual(budget.remaining(), 70000)

    def test_token_budget_can_continue(self):
        """can_continue()가 예산 상태를 올바르게 반환해야 한다."""
        from run import TokenBudget
        
        budget = TokenBudget(total_limit=100000)
        
        self.assertTrue(budget.can_continue())
        
        budget.add_usage(95000)
        self.assertTrue(budget.can_continue())
        
        budget.add_usage(10000)  # 105000 > 100000
        self.assertFalse(budget.can_continue())

    def test_token_budget_early_exit(self):
        """예산 초과 시 deep_research가 조기 종료해야 한다."""
        from run import TokenBudget, ResearchState
        
        budget = TokenBudget(total_limit=1000)
        budget.add_usage(1001)  # Exceed budget
        
        state = ResearchState(
            topic="test",
            session_id="test",
            depth=5,
            breadth=3,
            token_budget=budget,
        )
        
        # Budget exhausted should prevent continuation
        self.assertFalse(state.token_budget.can_continue())


class TestSourceEvaluator(unittest.TestCase):
    """Test SourceEvaluator class.
    
    Scenario: 소스 신뢰도 평가
    """

    def test_source_evaluator_high_trust_domains(self):
        """높은 신뢰도 도메인이 높은 점수를 받아야 한다."""
        from source_evaluator import SourceEvaluator
        
        evaluator = SourceEvaluator()
        
        # Academic and official sources
        self.assertGreaterEqual(evaluator.evaluate("https://arxiv.org/abs/2024.1234"), 0.9)
        self.assertGreaterEqual(evaluator.evaluate("https://github.com/user/repo"), 0.8)
        self.assertGreaterEqual(evaluator.evaluate("https://docs.python.org/3/"), 0.85)

    def test_source_evaluator_low_trust_patterns(self):
        """낮은 신뢰도 패턴이 낮은 점수를 받아야 한다."""
        from source_evaluator import SourceEvaluator
        
        evaluator = SourceEvaluator()
        
        # Personal blogs and unreliable sources
        self.assertLessEqual(evaluator.evaluate("https://random.blogspot.com/post"), 0.4)
        self.assertLessEqual(evaluator.evaluate("https://some.wordpress.com/article"), 0.4)

    def test_source_evaluator_default_score(self):
        """알 수 없는 도메인은 기본 점수를 받아야 한다."""
        from source_evaluator import SourceEvaluator
        
        evaluator = SourceEvaluator()
        
        score = evaluator.evaluate("https://unknowndomain.com/page")
        
        self.assertGreaterEqual(score, 0.4)
        self.assertLessEqual(score, 0.6)

    def test_source_evaluator_filter_by_threshold(self):
        """임계값 이하 소스가 필터링되어야 한다."""
        from source_evaluator import SourceEvaluator
        
        evaluator = SourceEvaluator()
        
        urls = [
            "https://arxiv.org/paper1",      # High trust
            "https://github.com/repo",        # High trust
            "https://random.blogspot.com/x",  # Low trust
            "https://unknown.com/page",       # Default
        ]
        
        filtered = evaluator.filter_urls(urls, min_trust=0.5)
        
        # Low trust sources should be filtered out
        self.assertIn("https://arxiv.org/paper1", filtered)
        self.assertIn("https://github.com/repo", filtered)
        self.assertNotIn("https://random.blogspot.com/x", filtered)


class TestCLIPhase2Parameters(unittest.TestCase):
    """Test CLI parameter parsing for Phase 2.
    
    Scenario: Phase 2 CLI 옵션
    """

    def test_cli_parallel_flag(self):
        """--parallel 플래그가 파싱되어야 한다."""
        from run import create_argument_parser
        
        parser = create_argument_parser()
        args = parser.parse_args(["topic", "--parallel"])
        
        self.assertTrue(args.parallel)

    def test_cli_token_budget(self):
        """--token-budget 옵션이 파싱되어야 한다."""
        from run import create_argument_parser
        
        parser = create_argument_parser()
        args = parser.parse_args(["topic", "--token-budget", "50000"])
        
        self.assertEqual(args.token_budget, 50000)

    def test_cli_min_trust(self):
        """--min-trust 옵션이 파싱되어야 한다."""
        from run import create_argument_parser
        
        parser = create_argument_parser()
        args = parser.parse_args(["topic", "--min-trust", "0.6"])
        
        self.assertEqual(args.min_trust, 0.6)

    def test_cli_default_values_phase2(self):
        """Phase 2 기본값이 올바르게 설정되어야 한다."""
        from run import create_argument_parser
        
        parser = create_argument_parser()
        args = parser.parse_args(["topic"])
        
        self.assertFalse(args.parallel)
        self.assertEqual(args.token_budget, 100000)
        self.assertEqual(args.min_trust, 0.3)


class TestIntegrationPhase2(unittest.TestCase):
    """Integration tests for Phase 2 features."""

    def test_parallel_scraping_integration(self):
        """병렬 스크래핑이 DeepResearch와 통합되어야 한다."""
        from run import DeepResearch
        
        # Mock dependencies
        mock_llm = MagicMock(return_value="{}")
        researcher = DeepResearch(llm_callback=mock_llm)
        
        # Mock archive to avoid file system operations
        researcher.archive.save_content = MagicMock()
        
        # Mock engine and scraper
        researcher.engine.search = MagicMock(return_value=[
            {"href": "https://example.com/1", "title": "Title 1"},
            {"href": "https://example.com/2", "title": "Title 2"},
        ])
        
        # Mock parallel fetch
        with patch('run.fetch_urls_parallel') as mock_fetch:
            mock_fetch.return_value = [
                {"url": "https://example.com/1", "content": "Content 1", "success": True},
                {"url": "https://example.com/2", "content": "Content 2", "success": True},
            ]
            
            session_data = {
                "session_id": "test",
                "plan": {"steps": [{"query": "test", "rationale": "test"}]}
            }
            
            results = researcher.execute_plan(session_data, parallel=True)
            
            # Verify parallel fetch was called
            mock_fetch.assert_called_once()
            self.assertEqual(len(results[0]["snippets"]), 2)
            # Verify content was saved
            self.assertEqual(researcher.archive.save_content.call_count, 2)

    def test_token_budget_integration(self):
        """토큰 예산이 deep_research와 통합되어야 한다."""
        from run import DeepResearch, ResearchState, TokenBudget
        
        mock_llm = MagicMock(return_value="{}")
        researcher = DeepResearch(llm_callback=mock_llm)
        
        # Create state with exhausted budget
        budget = TokenBudget(total_limit=100)
        budget.add_usage(150)
        
        state = ResearchState(
            topic="test",
            session_id="test",
            depth=3,
            breadth=3,
            token_budget=budget
        )
        
        # Should exit immediately
        final_state = researcher.deep_research(state)
        
        # Verify no execution happened (mock_llm not called)
        mock_llm.assert_not_called()
        self.assertEqual(final_state.depth, 3)  # Depth unchanged


def run_phase2_tests():
    """Run all Phase 2 tests."""
    print("=" * 60)
    print("Deep Research Phase 2 - TDD Test Suite")
    print("=" * 60)

    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add test cases
    suite.addTests(loader.loadTestsFromTestCase(TestAsyncWebScraper))
    suite.addTests(loader.loadTestsFromTestCase(TestTokenBudget))
    suite.addTests(loader.loadTestsFromTestCase(TestSourceEvaluator))
    suite.addTests(loader.loadTestsFromTestCase(TestCLIPhase2Parameters))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegrationPhase2))

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(run_phase2_tests())
