#!/usr/bin/env python3
"""
Test Suite for Iterative Deep Research Feature

TDD 기반 테스트: OpenSpec 시나리오와 1:1 매핑
- ResearchState, AnalysisResult 데이터 클래스
- analyze_results() 함수
- deep_research() 재귀 로직
- CLI 파라미터 파싱
"""

import sys
import os
import unittest
import json
from unittest.mock import patch, MagicMock
from dataclasses import dataclass, field
from typing import List, Dict, Set, Any

# Add scripts directory to path
scripts_dir = os.path.dirname(os.path.abspath(__file__))
if scripts_dir not in sys.path:
    sys.path.insert(0, scripts_dir)


class TestResearchState(unittest.TestCase):
    """Test ResearchState dataclass.
    
    Scenario: ResearchState 초기화 및 상태 관리
    """

    def test_research_state_initialization(self):
        """ResearchState가 올바르게 초기화되어야 한다."""
        from run import ResearchState
        
        state = ResearchState(
            topic="AI trends 2026",
            session_id="test_session_001",
            depth=3,
            breadth=5,
        )
        
        self.assertEqual(state.topic, "AI trends 2026")
        self.assertEqual(state.session_id, "test_session_001")
        self.assertEqual(state.depth, 3)
        self.assertEqual(state.breadth, 5)
        self.assertEqual(state.learnings, [])
        self.assertEqual(state.directions, [])
        self.assertEqual(state.visited_urls, set())
        self.assertEqual(state.all_results, [])

    def test_research_state_with_existing_learnings(self):
        """ResearchState가 기존 learnings으로 초기화될 수 있어야 한다."""
        from run import ResearchState
        
        existing_learnings = ["AI는 2026년에 더 발전할 것", "GPT-5가 출시될 예정"]
        
        state = ResearchState(
            topic="AI trends",
            session_id="test_002",
            depth=2,
            breadth=3,
            learnings=existing_learnings,
        )
        
        self.assertEqual(len(state.learnings), 2)
        self.assertIn("AI는 2026년에 더 발전할 것", state.learnings)

    def test_research_state_tracks_visited_urls(self):
        """ResearchState가 방문한 URL을 추적해야 한다."""
        from run import ResearchState
        
        state = ResearchState(
            topic="test",
            session_id="test_003",
            depth=2,
            breadth=3,
            visited_urls={"https://example.com/1", "https://example.com/2"},
        )
        
        self.assertIn("https://example.com/1", state.visited_urls)
        self.assertEqual(len(state.visited_urls), 2)


class TestAnalysisResult(unittest.TestCase):
    """Test AnalysisResult dataclass.
    
    Scenario: AnalysisResult 구조 검증
    """

    def test_analysis_result_structure(self):
        """AnalysisResult가 올바른 구조를 가져야 한다."""
        from run import AnalysisResult
        
        result = AnalysisResult(
            learnings=["New insight 1", "New insight 2"],
            directions=["Follow-up question 1"],
            is_complete=False,
            confidence=0.6,
        )
        
        self.assertEqual(len(result.learnings), 2)
        self.assertEqual(len(result.directions), 1)
        self.assertFalse(result.is_complete)
        self.assertEqual(result.confidence, 0.6)

    def test_analysis_result_complete_state(self):
        """AnalysisResult가 완료 상태를 표현할 수 있어야 한다."""
        from run import AnalysisResult
        
        result = AnalysisResult(
            learnings=["Complete answer found"],
            directions=[],
            is_complete=True,
            confidence=0.95,
        )
        
        self.assertTrue(result.is_complete)
        self.assertGreaterEqual(result.confidence, 0.9)
        self.assertEqual(len(result.directions), 0)


class TestAnalyzeResults(unittest.TestCase):
    """Test analyze_results() function.
    
    Scenario: 결과 분석 및 Learnings/Directions 추출
    """

    def test_analyze_results_extracts_learnings(self):
        """analyze_results가 결과에서 learnings를 추출해야 한다."""
        from run import DeepResearch
        
        # Mock LLM response
        mock_llm_response = json.dumps({
            "learnings": ["Key insight 1", "Key insight 2"],
            "directions": ["What about X?", "How does Y work?"],
            "is_complete": False,
            "confidence": 0.5
        })
        
        mock_llm = MagicMock(return_value=mock_llm_response)
        researcher = DeepResearch(llm_callback=mock_llm)
        
        results = [{"step": 1, "query": "test", "snippets": ["content..."]}]
        analysis = researcher.analyze_results(
            topic="Test topic",
            results=results,
            existing_learnings=[]
        )
        
        self.assertIsNotNone(analysis)
        self.assertEqual(len(analysis.learnings), 2)
        self.assertEqual(len(analysis.directions), 2)
        self.assertFalse(analysis.is_complete)

    def test_analyze_results_with_high_confidence(self):
        """confidence가 높으면 is_complete가 True여야 한다."""
        from run import DeepResearch
        
        mock_llm_response = json.dumps({
            "learnings": ["Complete answer"],
            "directions": [],
            "is_complete": True,
            "confidence": 0.95
        })
        
        mock_llm = MagicMock(return_value=mock_llm_response)
        researcher = DeepResearch(llm_callback=mock_llm)
        
        results = [{"step": 1, "query": "test", "snippets": ["content..."]}]
        analysis = researcher.analyze_results(
            topic="Test topic",
            results=results,
            existing_learnings=[]
        )
        
        self.assertTrue(analysis.is_complete)
        self.assertGreaterEqual(analysis.confidence, 0.9)

    def test_analyze_results_handles_malformed_response(self):
        """잘못된 LLM 응답을 gracefully 처리해야 한다."""
        from run import DeepResearch
        
        mock_llm = MagicMock(return_value="This is not valid JSON")
        researcher = DeepResearch(llm_callback=mock_llm)
        
        results = [{"step": 1, "query": "test", "snippets": ["content..."]}]
        analysis = researcher.analyze_results(
            topic="Test topic",
            results=results,
            existing_learnings=[]
        )
        
        # Should return a default analysis with empty learnings
        self.assertIsNotNone(analysis)
        self.assertEqual(analysis.learnings, [])
        self.assertFalse(analysis.is_complete)


class TestSelectBestDirection(unittest.TestCase):
    """Test select_best_direction() function.
    
    Scenario: 최적 탐색 방향 선택
    """

    def test_select_best_direction_returns_first(self):
        """여러 방향 중 첫 번째를 선택해야 한다 (Phase 1)."""
        from run import DeepResearch
        
        mock_llm = MagicMock()
        researcher = DeepResearch(llm_callback=mock_llm)
        
        directions = ["Question A?", "Question B?", "Question C?"]
        selected = researcher.select_best_direction(directions)
        
        self.assertEqual(selected, "Question A?")

    def test_select_best_direction_empty_list(self):
        """빈 리스트에서는 None을 반환해야 한다."""
        from run import DeepResearch
        
        mock_llm = MagicMock()
        researcher = DeepResearch(llm_callback=mock_llm)
        
        selected = researcher.select_best_direction([])
        
        self.assertIsNone(selected)


class TestDeepResearchRecursion(unittest.TestCase):
    """Test deep_research() recursive logic.
    
    Scenario: 재귀적 깊이 탐색
    """

    def test_deep_research_single_depth(self):
        """depth=1일 때 한 번만 실행되어야 한다."""
        from run import DeepResearch, ResearchState
        
        # Mock dependencies
        mock_llm = MagicMock()
        researcher = DeepResearch(llm_callback=mock_llm)
        
        # Mock methods
        researcher.create_plan = MagicMock(return_value={
            "session_id": "test",
            "topic": "test",
            "plan": {"steps": [{"query": "test", "rationale": "test"}]}
        })
        researcher.execute_plan = MagicMock(return_value=[
            {"step": 1, "query": "test", "snippets": ["content"]}
        ])
        researcher.analyze_results = MagicMock(return_value=MagicMock(
            learnings=["Learned something"],
            directions=[],
            is_complete=True,
            confidence=0.9
        ))
        
        state = ResearchState(
            topic="Test topic",
            session_id="test_session",
            depth=1,
            breadth=3,
        )
        
        final_state = researcher.deep_research(state)
        
        self.assertIsNotNone(final_state)
        self.assertEqual(researcher.execute_plan.call_count, 1)

    def test_deep_research_multiple_depth(self):
        """depth=3일 때 최대 3번 재귀해야 한다."""
        from run import DeepResearch, ResearchState
        
        mock_llm = MagicMock()
        researcher = DeepResearch(llm_callback=mock_llm)
        
        call_count = {"value": 0}
        
        def mock_execute(session, max_urls_per_step=3):
            call_count["value"] += 1
            return [{"step": 1, "query": "test", "snippets": ["content"]}]
        
        def mock_analyze(topic, results, existing_learnings):
            # Complete only on 3rd iteration
            is_complete = call_count["value"] >= 3
            return MagicMock(
                learnings=[f"Learning {call_count['value']}"],
                directions=[] if is_complete else ["Next direction?"],
                is_complete=is_complete,
                confidence=0.9 if is_complete else 0.5
            )
        
        researcher.create_plan = MagicMock(return_value={
            "session_id": "test",
            "topic": "test", 
            "plan": {"steps": [{"query": "test", "rationale": "test"}]}
        })
        researcher.execute_plan = mock_execute
        researcher.analyze_results = mock_analyze
        
        state = ResearchState(
            topic="Test topic",
            session_id="test_session",
            depth=3,
            breadth=3,
        )
        
        final_state = researcher.deep_research(state)
        
        self.assertEqual(call_count["value"], 3)
        self.assertEqual(len(final_state.learnings), 3)

    def test_deep_research_early_exit_on_complete(self):
        """is_complete=True면 조기 종료해야 한다."""
        from run import DeepResearch, ResearchState
        
        mock_llm = MagicMock()
        researcher = DeepResearch(llm_callback=mock_llm)
        
        researcher.create_plan = MagicMock(return_value={
            "session_id": "test",
            "topic": "test",
            "plan": {"steps": [{"query": "test", "rationale": "test"}]}
        })
        researcher.execute_plan = MagicMock(return_value=[
            {"step": 1, "query": "test", "snippets": ["content"]}
        ])
        # First call returns complete
        researcher.analyze_results = MagicMock(return_value=MagicMock(
            learnings=["Complete answer"],
            directions=[],
            is_complete=True,
            confidence=0.95
        ))
        
        state = ResearchState(
            topic="Test topic",
            session_id="test_session",
            depth=5,  # High depth but should exit early
            breadth=3,
        )
        
        final_state = researcher.deep_research(state)
        
        # Should only execute once despite depth=5
        self.assertEqual(researcher.execute_plan.call_count, 1)

    def test_deep_research_respects_max_depth(self):
        """MAX_DEPTH(5)를 초과하지 않아야 한다."""
        from run import DeepResearch, ResearchState
        
        mock_llm = MagicMock()
        researcher = DeepResearch(llm_callback=mock_llm)
        
        call_count = {"value": 0}
        
        def mock_execute(session, max_urls_per_step=3):
            call_count["value"] += 1
            return [{"step": 1, "query": "test", "snippets": ["content"]}]
        
        researcher.create_plan = MagicMock(return_value={
            "session_id": "test",
            "topic": "test",
            "plan": {"steps": [{"query": "test", "rationale": "test"}]}
        })
        researcher.execute_plan = mock_execute
        researcher.analyze_results = MagicMock(return_value=MagicMock(
            learnings=["Keep going"],
            directions=["More questions?"],
            is_complete=False,
            confidence=0.3
        ))
        
        state = ResearchState(
            topic="Test topic",
            session_id="test_session",
            depth=10,  # Exceeds MAX_DEPTH
            breadth=3,
        )
        
        final_state = researcher.deep_research(state)
        
        # Should be capped at MAX_DEPTH (5)
        self.assertLessEqual(call_count["value"], 5)


class TestCLIParameters(unittest.TestCase):
    """Test CLI parameter parsing.
    
    Scenario: --breadth, --depth 파라미터 파싱 및 하위 호환성
    """

    def test_cli_breadth_depth_parsing(self):
        """--breadth와 --depth가 올바르게 파싱되어야 한다."""
        from run import create_argument_parser
        
        parser = create_argument_parser()
        args = parser.parse_args(["topic", "--breadth", "5", "--depth", "3"])
        
        self.assertEqual(args.topic, "topic")
        self.assertEqual(args.breadth, 5)
        self.assertEqual(args.depth, 3)

    def test_cli_depth_only_backward_compatible(self):
        """--depth만 지정 시 기존 동작(단일 패스)을 유지해야 한다."""
        from run import create_argument_parser
        
        parser = create_argument_parser()
        args = parser.parse_args(["topic", "--depth", "10"])
        
        self.assertEqual(args.depth, 10)
        # breadth가 없으면 depth를 URL 수로 해석 (하위 호환성)
        self.assertIsNone(args.breadth)

    def test_cli_default_values(self):
        """기본값이 올바르게 설정되어야 한다."""
        from run import create_argument_parser
        
        parser = create_argument_parser()
        args = parser.parse_args(["topic"])
        
        # Default: depth=2 (재귀 깊이), breadth=None (지정하지 않음)
        self.assertEqual(args.depth, 2)
        self.assertIsNone(args.breadth)

    def test_cli_check_only_mode(self):
        """--check-only 모드가 작동해야 한다."""
        from run import create_argument_parser
        
        parser = create_argument_parser()
        args = parser.parse_args(["--check-only"])
        
        self.assertTrue(args.check_only)
        self.assertIsNone(args.topic)


class TestLearningsManagement(unittest.TestCase):
    """Test learnings accumulation and limiting.
    
    Scenario: Learnings 누적 및 최대 개수 제한
    """

    def test_learnings_accumulation(self):
        """learnings가 각 단계에서 누적되어야 한다."""
        from run import ResearchState
        
        state = ResearchState(
            topic="test",
            session_id="test",
            depth=3,
            breadth=3,
            learnings=["Learning 1", "Learning 2"]
        )
        
        # Simulate adding more learnings
        new_learnings = ["Learning 3", "Learning 4"]
        state.learnings.extend(new_learnings)
        
        self.assertEqual(len(state.learnings), 4)

    def test_learnings_limited_to_max(self):
        """learnings가 최대 20개로 제한되어야 한다."""
        from run import limit_learnings
        
        learnings = [f"Learning {i}" for i in range(30)]
        limited = limit_learnings(learnings, max_count=20)
        
        self.assertEqual(len(limited), 20)
        # 최신 learnings가 유지되어야 함 (가장 마지막 20개)
        self.assertEqual(limited[-1], "Learning 29")


def run_iterative_tests():
    """Run all iterative research tests."""
    print("=" * 60)
    print("Iterative Deep Research - TDD Test Suite")
    print("=" * 60)

    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add test cases
    suite.addTests(loader.loadTestsFromTestCase(TestResearchState))
    suite.addTests(loader.loadTestsFromTestCase(TestAnalysisResult))
    suite.addTests(loader.loadTestsFromTestCase(TestAnalyzeResults))
    suite.addTests(loader.loadTestsFromTestCase(TestSelectBestDirection))
    suite.addTests(loader.loadTestsFromTestCase(TestDeepResearchRecursion))
    suite.addTests(loader.loadTestsFromTestCase(TestCLIParameters))
    suite.addTests(loader.loadTestsFromTestCase(TestLearningsManagement))

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(run_iterative_tests())
