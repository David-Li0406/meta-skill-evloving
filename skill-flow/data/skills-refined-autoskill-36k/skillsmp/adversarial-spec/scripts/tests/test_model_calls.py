"""Tests for model calling logic with mocked API responses."""

import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from models import (
    CostTracker,
    ModelResponse,
    call_models_parallel,
    call_single_model,
)


class MockUsage:
    def __init__(self, prompt_tokens=100, completion_tokens=50):
        self.prompt_tokens = prompt_tokens
        self.completion_tokens = completion_tokens


class MockChoice:
    def __init__(self, content):
        self.message = MagicMock()
        self.message.content = content


class MockResponse:
    def __init__(self, content, prompt_tokens=100, completion_tokens=50):
        self.choices = [MockChoice(content)]
        self.usage = MockUsage(prompt_tokens, completion_tokens)


class TestCallSingleModel:
    @patch("models.completion")
    @patch("models.cost_tracker", CostTracker())
    def test_returns_model_response_on_success(self, mock_completion):
        mock_completion.return_value = MockResponse(
            "Here is my critique.\n\n[SPEC]\n# Revised Spec\n[/SPEC]"
        )

        result = call_single_model(
            model="gpt-4o",
            spec="# Original Spec",
            round_num=1,
            doc_type="tech",
        )

        assert isinstance(result, ModelResponse)
        assert result.model == "gpt-4o"
        assert result.agreed is False
        assert result.spec == "# Revised Spec"
        assert result.error is None
        assert result.input_tokens == 100
        assert result.output_tokens == 50

    @patch("models.completion")
    @patch("models.cost_tracker", CostTracker())
    def test_detects_agreement(self, mock_completion):
        mock_completion.return_value = MockResponse(
            "This spec looks complete. [AGREE]\n\n[SPEC]\n# Final Spec\n[/SPEC]"
        )

        result = call_single_model(
            model="gpt-4o",
            spec="# Spec",
            round_num=2,
            doc_type="tech",
        )

        assert result.agreed is True
        assert result.spec == "# Final Spec"

    @patch("models.completion")
    @patch("models.cost_tracker", CostTracker())
    def test_handles_api_error_with_retry(self, mock_completion):
        mock_completion.side_effect = Exception("API timeout")

        result = call_single_model(
            model="gpt-4o",
            spec="# Spec",
            round_num=1,
            doc_type="tech",
        )

        assert result.error is not None
        assert "API timeout" in result.error
        assert result.agreed is False
        # Should have retried 3 times
        assert mock_completion.call_count == 3

    @patch("models.completion")
    @patch("models.cost_tracker", CostTracker())
    def test_recovers_on_second_retry(self, mock_completion):
        # First call fails, second succeeds
        mock_completion.side_effect = [
            Exception("Temporary error"),
            MockResponse("[AGREE]\n[SPEC]\n# Spec\n[/SPEC]"),
        ]

        result = call_single_model(
            model="gpt-4o",
            spec="# Spec",
            round_num=1,
            doc_type="tech",
        )

        assert result.error is None
        assert result.agreed is True
        assert mock_completion.call_count == 2

    @patch("models.completion")
    @patch("models.cost_tracker", CostTracker())
    def test_includes_focus_in_prompt(self, mock_completion):
        mock_completion.return_value = MockResponse("[AGREE]\n[SPEC]\n# Spec\n[/SPEC]")

        call_single_model(
            model="gpt-4o",
            spec="# Spec",
            round_num=1,
            doc_type="tech",
            focus="security",
        )

        # Check that the user message includes security focus
        call_args = mock_completion.call_args
        messages = call_args.kwargs["messages"]
        user_message = messages[1]["content"]
        assert "SECURITY" in user_message

    @patch("models.completion")
    @patch("models.cost_tracker", CostTracker())
    def test_includes_preserve_intent_prompt(self, mock_completion):
        mock_completion.return_value = MockResponse("[AGREE]\n[SPEC]\n# Spec\n[/SPEC]")

        call_single_model(
            model="gpt-4o",
            spec="# Spec",
            round_num=1,
            doc_type="tech",
            preserve_intent=True,
        )

        call_args = mock_completion.call_args
        messages = call_args.kwargs["messages"]
        user_message = messages[1]["content"]
        assert "PRESERVE ORIGINAL INTENT" in user_message

    @patch("models.completion")
    @patch("models.cost_tracker", CostTracker())
    def test_uses_press_prompt_when_press_true(self, mock_completion):
        mock_completion.return_value = MockResponse("[AGREE]\n[SPEC]\n# Spec\n[/SPEC]")

        call_single_model(
            model="gpt-4o",
            spec="# Spec",
            round_num=2,
            doc_type="tech",
            press=True,
        )

        call_args = mock_completion.call_args
        messages = call_args.kwargs["messages"]
        user_message = messages[1]["content"]
        assert "confirm your agreement" in user_message

    @patch("models.completion")
    @patch("models.cost_tracker", CostTracker())
    def test_bedrock_mode_adds_prefix(self, mock_completion):
        mock_completion.return_value = MockResponse("[AGREE]\n[SPEC]\n# Spec\n[/SPEC]")

        call_single_model(
            model="anthropic.claude-3-sonnet",
            spec="# Spec",
            round_num=1,
            doc_type="tech",
            bedrock_mode=True,
            bedrock_region="us-east-1",
        )

        call_args = mock_completion.call_args
        # Model should have bedrock/ prefix
        assert call_args.kwargs["model"] == "bedrock/anthropic.claude-3-sonnet"


class TestCallModelsParallel:
    @patch("models.completion")
    @patch("models.cost_tracker", CostTracker())
    def test_calls_multiple_models(self, mock_completion):
        mock_completion.return_value = MockResponse(
            "Critique here.\n[SPEC]\n# Revised\n[/SPEC]"
        )

        results = call_models_parallel(
            models=["gpt-4o", "gemini/gemini-2.0-flash"],
            spec="# Spec",
            round_num=1,
            doc_type="tech",
        )

        assert len(results) == 2
        # Each model should have been called
        assert mock_completion.call_count == 2

    @patch("models.completion")
    @patch("models.cost_tracker", CostTracker())
    def test_handles_mixed_results(self, mock_completion):
        # First model agrees, second critiques
        def side_effect(*args, **kwargs):
            model = kwargs.get("model", args[0] if args else "")
            if "gpt" in model:
                return MockResponse("[AGREE]\n[SPEC]\n# Final\n[/SPEC]")
            else:
                return MockResponse("Issues found.\n[SPEC]\n# Revised\n[/SPEC]")

        mock_completion.side_effect = side_effect

        results = call_models_parallel(
            models=["gpt-4o", "gemini/gemini-2.0-flash"],
            spec="# Spec",
            round_num=1,
            doc_type="tech",
        )

        agreed_count = sum(1 for r in results if r.agreed)
        assert agreed_count == 1

    @patch("models.completion")
    @patch("models.cost_tracker", CostTracker())
    def test_one_model_error_others_succeed(self, mock_completion):
        # Use model name to determine behavior (deterministic in parallel)
        def side_effect(*args, **kwargs):
            model = kwargs.get("model", "")
            if "fail" in model:
                raise Exception("API error")
            return MockResponse("[AGREE]\n[SPEC]\n# Spec\n[/SPEC]")

        mock_completion.side_effect = side_effect

        results = call_models_parallel(
            models=["model-fail", "model-succeed"],
            spec="# Spec",
            round_num=1,
            doc_type="tech",
        )

        errors = [r for r in results if r.error]
        successes = [r for r in results if not r.error]
        assert len(errors) == 1
        assert len(successes) == 1
        assert errors[0].model == "model-fail"
        assert successes[0].model == "model-succeed"


class TestCostTrackerIntegration:
    @patch("models.completion")
    def test_cost_accumulates_across_calls(self, mock_completion):
        tracker = CostTracker()

        with patch("models.cost_tracker", tracker):
            mock_completion.return_value = MockResponse(
                "[AGREE]\n[SPEC]\n# Spec\n[/SPEC]",
                prompt_tokens=1000,
                completion_tokens=500,
            )

            call_single_model(
                model="gpt-4o",
                spec="# Spec",
                round_num=1,
                doc_type="tech",
            )

            call_single_model(
                model="gpt-4o",
                spec="# Spec",
                round_num=2,
                doc_type="tech",
            )

        assert tracker.total_input_tokens == 2000
        assert tracker.total_output_tokens == 1000
        assert tracker.total_cost > 0
        assert "gpt-4o" in tracker.by_model


class TestCodexModelPath:
    @patch("models.CODEX_AVAILABLE", False)
    @patch("models.cost_tracker", CostTracker())
    def test_codex_unavailable_returns_error(self):
        result = call_single_model(
            model="codex/gpt-5.2-codex",
            spec="# Spec",
            round_num=1,
            doc_type="tech",
        )

        assert result.error is not None
        assert "Codex CLI not found" in result.error
