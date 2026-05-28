#!/usr/bin/env python3
"""
Unit tests for AgentEvaluator class
Tests the enhanced agent evaluation logic with file patterns, intent patterns, and priority-based activation.
Test cases are dynamically loaded from agent_evaluator_test_cases.md
"""

import unittest
import json
import sys
import os
import re
from unittest.mock import patch, MagicMock
from io import StringIO
from typing import Dict, List, Any

# Add the scripts directory to the path so we can import the module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agent_evaluator import AgentEvaluator, main


class MarkdownTestLoader:
    """Load test cases from Markdown file and convert to test data."""

    def __init__(self, markdown_file: str):
        self.markdown_file = markdown_file
        self.test_cases = {}
        self._load_test_cases()

    def _load_test_cases(self):
        """Parse the Markdown file and extract test cases."""
        if not os.path.exists(self.markdown_file):
            raise FileNotFoundError(f"Test cases file not found: {self.markdown_file}")

        with open(self.markdown_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Split by main headers (##)
        sections = re.split(r'^##\s+', content, flags=re.MULTILINE)[1:]

        for section in sections:
            if not section.strip():
                continue

            lines = section.strip().split('\n')
            section_title = lines[0].strip()

            # Parse test cases within this section
            test_cases = self._parse_section_test_cases(lines[1:])
            if test_cases:
                self.test_cases[section_title] = test_cases

    def _parse_section_test_cases(self, lines: List[str]) -> List[Dict[str, Any]]:
        """Parse test cases from a section."""
        test_cases = []
        current_test = None

        for line in lines:
            line = line.strip()
            if not line:
                continue

            # Start of new test case
            if line.startswith('### '):
                if current_test:
                    test_cases.append(current_test)
                current_test = {
                    'title': line[4:].strip(),
                    'description': '',
                    'input': {},
                    'expected': {}
                }
            elif line.startswith('- **Description**:'):
                if current_test:
                    current_test['description'] = line[18:].strip()
            elif line.startswith('- **Input**:'):
                input_data = line[12:].strip()
                if current_test:
                    current_test['input'] = self._parse_input(input_data)
            elif line.startswith('- **Expected**:'):
                expected_data = line[15:].strip()
                if current_test:
                    current_test['expected'] = self._parse_expected(expected_data)
            elif line.startswith('- **Test Cases**:'):
                # Handle list of test cases
                continue
            elif line.startswith('  - '):
                # Individual test case in list
                if current_test and 'test_cases' not in current_test:
                    current_test['test_cases'] = []
                if current_test:
                    current_test['test_cases'].append(line[4:].strip())

        if current_test:
            test_cases.append(current_test)

        return test_cases

    def _parse_input(self, input_str: str) -> Dict[str, Any]:
        """Parse input data from test case."""
        result = {}
        if '`' in input_str:
            # Extract quoted strings
            matches = re.findall(r'`([^`]+)`', input_str)
            if matches:
                result['query'] = matches[0]
            if len(matches) > 1:
                result['file_path'] = matches[1]
        else:
            result['query'] = input_str.strip('"')
        return result

    def _parse_expected(self, expected_str: str) -> Dict[str, Any]:
        """Parse expected results from test case."""
        result = {}
        lines = expected_str.split('\n')
        for line in lines:
            line = line.strip()
            if not line:
                continue
            if ':' in line:
                key, value = line.split(':', 1)
                key = key.strip().lower().replace(' ', '_')
                value = value.strip()
                result[key] = value
        return result

    def get_test_cases(self) -> Dict[str, List[Dict[str, Any]]]:
        """Get all loaded test cases."""
        return self.test_cases


class TestAgentEvaluator(unittest.TestCase):
    """Test cases for the AgentEvaluator class."""

    def setUp(self):
        """Set up test fixtures."""
        self.evaluator = AgentEvaluator()

    def _run_test_case(self, test_case: Dict[str, Any]):
        """Run a single test case from the Markdown file."""
        input_data = test_case.get('input', {})
        expected = test_case.get('expected', {})

        query = input_data.get('query', '')
        file_path = input_data.get('file_path')

        # Run the evaluation
        result = self.evaluator.evaluate_query(query, file_path)

        # Check expectations
        for key, expected_value in expected.items():
            if key == 'activated_agents':
                if expected_value == 'empty':
                    self.assertEqual(len(result['activated_agents']), 0)
                else:
                    # Parse expected agent names
                    expected_agents = [name.strip() for name in expected_value.split(',')]
                    for agent in expected_agents:
                        self.assertIn(agent, result['activated_agents'])
            elif key == 'required_agents':
                if expected_value == 'empty':
                    self.assertEqual(len(result['required_agents']), 0)
                else:
                    expected_agents = [name.strip() for name in expected_value.split('and')]
                    for agent in expected_agents:
                        self.assertIn(agent, result['required_agents'])
            elif key == 'additional_context':
                if expected_value == 'empty':
                    self.assertEqual(result['additional_context'], '')
                else:
                    self.assertIn(expected_value, result['additional_context'])
            elif key == 'file_path':
                self.assertEqual(result['file_path'], expected_value)
            elif key == 'priority':
                # Check specific agent priority
                agent_name = expected.get('agent_name', '')
                if agent_name:
                    agent_eval = result['evaluations'].get(agent_name, {})
                    self.assertEqual(agent_eval.get('priority'), expected_value)
            elif key == 'keyword_matches':
                if '>' in expected_value:
                    _, threshold = expected_value.split('>')
                    agent_name = expected.get('agent_name', '')
                    if agent_name:
                        agent_eval = result['evaluations'].get(agent_name, {})
                        self.assertGreater(agent_eval.get('keyword_matches', 0), int(threshold))
            elif key == 'relevance_score':
                if '>=' in expected_value:
                    _, threshold = expected_value.split('>=')
                    agent_name = expected.get('agent_name', '')
                    if agent_name:
                        agent_eval = result['evaluations'].get(agent_name, {})
                        self.assertGreaterEqual(agent_eval.get('relevance_score', 0), int(threshold))
            elif key == 'yes_no':
                agent_name = expected.get('agent_name', '')
                if agent_name:
                    agent_eval = result['evaluations'].get(agent_name, {})
                    self.assertEqual(agent_eval.get('yes_no'), expected_value)

    @classmethod
    def _create_dynamic_tests(cls):
        """Create dynamic test methods from loaded test cases."""
        for section_name, test_cases in cls.test_cases.items():
            for test_case in test_cases:
                test_method_name = f"test_{section_name.lower().replace(' ', '_').replace('-', '_')}_{test_case['title'].lower().replace(' ', '_').replace('-', '_')}"

                # Create the test method
                def dynamic_test(self, test_case=test_case):
                    self._run_test_case(test_case)

                # Set the method name and docstring
                dynamic_test.__name__ = test_method_name
                dynamic_test.__doc__ = test_case.get('description', f"Dynamic test: {test_case['title']}")

                # Add the method to the class
                setattr(cls, test_method_name, dynamic_test)

    def test_initialization(self):
        """Test that AgentEvaluator initializes with correct agent definitions."""
        self.assertIsInstance(self.evaluator.agents, dict)
        self.assertEqual(len(self.evaluator.agents), 8)

        # Check that all agents have required fields
        required_fields = ["description", "keywords", "file_patterns", "intent_patterns", "priority", "relevance_score"]
        for agent_name, agent_data in self.evaluator.agents.items():
            for field in required_fields:
                self.assertIn(field, agent_data, f"Agent {agent_name} missing field: {field}")

    def test_match_file_patterns_basic(self):
        """Test basic file pattern matching."""
        # Test exact match
        self.assertTrue(self.evaluator.match_file_patterns("test.md", ["*.md"]))
        self.assertFalse(self.evaluator.match_file_patterns("test.txt", ["*.md"]))

        # Test directory patterns
        self.assertTrue(self.evaluator.match_file_patterns("docs/README.md", ["docs/**"]))
        self.assertFalse(self.evaluator.match_file_patterns("src/README.md", ["docs/**"]))

        # Test globstar patterns
        self.assertTrue(self.evaluator.match_file_patterns("src/components/Button.tsx", ["src/**"]))
        self.assertTrue(self.evaluator.match_file_patterns("src/utils/helpers.ts", ["src/**"]))

    def test_match_file_patterns_edge_cases(self):
        """Test file pattern matching edge cases."""
        # Empty patterns
        self.assertFalse(self.evaluator.match_file_patterns("test.md", []))
        self.assertFalse(self.evaluator.match_file_patterns("", ["*.md"]))
        self.assertFalse(self.evaluator.match_file_patterns("test.md", [""]))

        # Invalid regex patterns (should be handled gracefully)
        self.assertFalse(self.evaluator.match_file_patterns("test.md", ["[invalid"]))

    def test_match_intent_patterns_basic(self):
        """Test basic intent pattern matching."""
        # Test simple pattern
        self.assertTrue(self.evaluator.match_intent_patterns("create a diagram", [r"\b(create|generate)\b.*\b(diagram)\b"]))
        self.assertFalse(self.evaluator.match_intent_patterns("draw a picture", [r"\b(create|generate)\b.*\b(diagram)\b"]))

        # Test case insensitive
        self.assertTrue(self.evaluator.match_intent_patterns("CREATE A DIAGRAM", [r"\b(create|generate)\b.*\b(diagram)\b"]))

    def test_match_intent_patterns_edge_cases(self):
        """Test intent pattern matching edge cases."""
        # Empty patterns
        self.assertFalse(self.evaluator.match_intent_patterns("test query", []))
        self.assertFalse(self.evaluator.match_intent_patterns("", [r"\btest\b"]))
        self.assertFalse(self.evaluator.match_intent_patterns("test query", [""]))

        # Invalid regex patterns (should be handled gracefully)
        self.assertFalse(self.evaluator.match_intent_patterns("test query", ["[invalid"]))

    def test_evaluate_query_keyword_matching(self):
        """Test keyword-based agent activation."""
        result = self.evaluator.evaluate_query("commit my changes to git")

        # Git-Committer should be activated
        self.assertIn("Git-Committer", result["activated_agents"])
        self.assertIn("Git-Committer", result["required_agents"])
        self.assertEqual(result["evaluations"]["Git-Committer"]["keyword_matches"], 2)
        self.assertEqual(result["evaluations"]["Git-Committer"]["yes_no"], "YES")

    def test_evaluate_query_intent_matching(self):
        """Test intent pattern-based agent activation."""
        result = self.evaluator.evaluate_query("create a flowchart for my application")

        # Mermaid-Agent should be activated via intent pattern
        mermaid_eval = result["evaluations"]["Mermaid-Agent"]
        self.assertEqual(mermaid_eval["intent_matches"], 1)
        self.assertEqual(mermaid_eval["yes_no"], "YES")

    def test_evaluate_query_file_matching(self):
        """Test file pattern-based agent activation."""
        result = self.evaluator.evaluate_query("create new instruction file", "instructions/new-feature.instructions.md")

        # Instruction-Writer should be activated via file pattern
        instruction_eval = result["evaluations"]["Instruction-Writer"]
        self.assertEqual(instruction_eval["file_matches"], 1)
        self.assertEqual(instruction_eval["yes_no"], "YES")

    def test_evaluate_query_combined_matching(self):
        """Test combined keyword, intent, and file pattern matching."""
        result = self.evaluator.evaluate_query("create a new instruction file", "instructions/setup.instructions.md")

        instruction_eval = result["evaluations"]["Instruction-Writer"]
        self.assertEqual(instruction_eval["keyword_matches"], 2)  # "instruction", "file"
        self.assertEqual(instruction_eval["intent_matches"], 1)   # matches intent pattern
        self.assertEqual(instruction_eval["file_matches"], 1)     # matches file pattern
        self.assertEqual(instruction_eval["relevance_score"], 10) # Max score
        self.assertEqual(instruction_eval["yes_no"], "YES")

    def test_evaluate_query_priority_thresholds(self):
        """Test that different priorities have different activation thresholds."""
        # High priority agent with moderate score should activate
        result = self.evaluator.evaluate_query("create a diagram")  # Should trigger Mermaid-Agent

        mermaid_eval = result["evaluations"]["Mermaid-Agent"]
        # Should activate even with moderate score due to high priority
        self.assertEqual(mermaid_eval["priority"], "high")
        self.assertGreaterEqual(mermaid_eval["relevance_score"], 4)
        self.assertEqual(mermaid_eval["yes_no"], "YES")

    def test_evaluate_query_no_activation(self):
        """Test query that should not activate any agents."""
        result = self.evaluator.evaluate_query("what is the weather today")

        self.assertEqual(len(result["activated_agents"]), 0)
        self.assertEqual(len(result["required_agents"]), 0)
        self.assertEqual(len(result["suggested_agents"]), 0)
        self.assertEqual(result["additional_context"], "")

    def test_evaluate_query_with_file_path(self):
        """Test evaluation with file path parameter."""
        result = self.evaluator.evaluate_query("update documentation", "README.md")

        # Should include file_path in result
        self.assertEqual(result["file_path"], "README.md")

        # Diataxis-Documentation-Expert should be activated via file pattern
        diataxis_eval = result["evaluations"]["Diataxis-Documentation-Expert"]
        self.assertEqual(diataxis_eval["file_matches"], 1)

    def test_evaluate_query_structured_output(self):
        """Test that structured output is generated correctly."""
        result = self.evaluator.evaluate_query("commit changes")

        self.assertIn("additional_context", result)
        self.assertIn("IMPORTANT GUIDELINES:", result["additional_context"])
        self.assertIn("Git Committer", result["additional_context"])

    def test_generate_reasoning_high_relevance(self):
        """Test reasoning generation for high relevance scores."""
        reasoning = self.evaluator._generate_reasoning("Test-Agent", 9, 2, 1, 1)
        self.assertIn("High relevance (9/10)", reasoning)
        self.assertIn("strong match", reasoning)
        self.assertIn("keywords (2)", reasoning)
        self.assertIn("intent pattern", reasoning)
        self.assertIn("file pattern", reasoning)

    def test_generate_reasoning_moderate_relevance(self):
        """Test reasoning generation for moderate relevance scores."""
        reasoning = self.evaluator._generate_reasoning("Test-Agent", 6, 1, 0, 0)
        self.assertIn("Moderate relevance (6/10)", reasoning)
        self.assertIn("keywords (1)", reasoning)

    def test_generate_reasoning_low_relevance(self):
        """Test reasoning generation for low relevance scores."""
        reasoning = self.evaluator._generate_reasoning("Test-Agent", 2, 0, 0, 0)
        self.assertIn("Low relevance (2/10)", reasoning)
        self.assertIn("minimal overlap", reasoning)

    def test_special_git_committer_activation(self):
        """Test that Git-Committer activates on any keyword match."""
        result = self.evaluator.evaluate_query("git status")

        git_eval = result["evaluations"]["Git-Committer"]
        self.assertEqual(git_eval["keyword_matches"], 1)  # "git"
        self.assertEqual(git_eval["yes_no"], "YES")  # Special case activation

    def test_context_aware_boosts(self):
        """Test context-aware scoring boosts."""
        # Test "create" boost for creation agents
        result = self.evaluator.evaluate_query("create a custom agent")

        meta_eval = result["evaluations"]["Meta-Agent"]
        # Should get boost due to "create" + agent keywords
        self.assertGreaterEqual(meta_eval["relevance_score"], 5)

    @patch('sys.stdout', new_callable=StringIO)
    def test_main_function_success(self, mock_stdout):
        """Test main function with valid arguments."""
        test_args = ['agent_evaluator.py', 'test query']
        with patch('sys.argv', test_args):
            main()

        output = mock_stdout.getvalue()
        result = json.loads(output)
        self.assertIn('query', result)
        self.assertEqual(result['query'], 'test query')

    @patch('sys.stdout', new_callable=StringIO)
    def test_main_function_with_file_path(self, mock_stdout):
        """Test main function with file path argument."""
        test_args = ['agent_evaluator.py', 'create instructions', 'instructions/test.instructions.md']
        with patch('sys.argv', test_args):
            main()

        output = mock_stdout.getvalue()
        result = json.loads(output)
        self.assertEqual(result['file_path'], 'instructions/test.instructions.md')

    @patch('sys.stdout', new_callable=StringIO)
    def test_main_function_no_args(self, mock_stdout):
        """Test main function with no arguments."""
        test_args = ['agent_evaluator.py']
        with patch('sys.argv', test_args), self.assertRaises(SystemExit) as cm:
            main()

        # Should exit with code 1
        self.assertEqual(cm.exception.code, 1)

        output = mock_stdout.getvalue()
        error_result = json.loads(output)
        self.assertIn('error', error_result)

    def test_agent_priority_distribution(self):
        """Test that agents have appropriate priority distribution."""
        priorities = {}
        for agent_data in self.evaluator.agents.values():
            priority = agent_data["priority"]
            priorities[priority] = priorities.get(priority, 0) + 1

        # Should have mix of priorities
        self.assertGreater(priorities.get("critical", 0), 0)  # At least Git-Committer
        self.assertGreater(priorities.get("high", 0), 0)     # Several high priority
        self.assertGreater(priorities.get("medium", 0), 0)   # Some medium priority
        self.assertGreater(priorities.get("low", 0), 0)      # At least Knowledge-Graph

    def test_required_vs_suggested_separation(self):
        """Test that required and suggested agents are separated correctly."""
        result = self.evaluator.evaluate_query("create a flowchart and commit changes")

        # Should have both Mermaid-Agent (high) and Git-Committer (critical) as required
        self.assertIn("Mermaid-Agent", result["required_agents"])
        self.assertIn("Git-Committer", result["required_agents"])

        # Should not have them in suggested
        self.assertNotIn("Mermaid-Agent", result["suggested_agents"])
        self.assertNotIn("Git-Committer", result["suggested_agents"])

    def test_generate_reasoning_high_relevance(self):
        """Test reasoning generation for high relevance scores."""
        reasoning = self.evaluator._generate_reasoning("Test-Agent", 9, 2, 1, 1)
        self.assertIn("High relevance (9/10)", reasoning)
        self.assertIn("strong match", reasoning)
        self.assertIn("keywords (2)", reasoning)
        self.assertIn("intent pattern", reasoning)
        self.assertIn("file pattern", reasoning)

    def test_generate_reasoning_moderate_relevance(self):
        """Test reasoning generation for moderate relevance scores."""
        reasoning = self.evaluator._generate_reasoning("Test-Agent", 6, 1, 0, 0)
        self.assertIn("Moderate relevance (6/10)", reasoning)
        self.assertIn("keywords (1)", reasoning)

    def test_generate_reasoning_low_relevance(self):
        """Test reasoning generation for low relevance scores."""
        reasoning = self.evaluator._generate_reasoning("Test-Agent", 2, 0, 0, 0)
        self.assertIn("Low relevance (2/10)", reasoning)
        self.assertIn("minimal overlap", reasoning)



# Dynamically add test cases from Markdown file
try:
    test_cases_file = os.path.join(os.path.dirname(__file__), 'agent_evaluator.test-cases.md')
    loader = MarkdownTestLoader(test_cases_file)
    test_cases = loader.get_test_cases()

    for section_name, cases in test_cases.items():
        for test_case in cases:
            # Create a valid method name
            safe_section = section_name.lower().replace(' ', '_').replace('-', '_')
            safe_title = test_case['title'].lower().replace(' ', '_').replace('-', '_')
            test_method_name = f"test_{safe_section}_{safe_title}"

            # Create the test method
            def dynamic_test(self, test_case=test_case):
                self._run_test_case(test_case)

            # Set the method name and docstring
            dynamic_test.__name__ = test_method_name
            dynamic_test.__doc__ = test_case.get('description', f"Dynamic test: {test_case['title']}")

            # Add the method to the class
            setattr(TestAgentEvaluator, test_method_name, dynamic_test)
except Exception as e:
    print(f"Error loading dynamic tests: {e}")

if __name__ == '__main__':
    unittest.main()
