# =============================================================================
# Google ADK Agent Test Template - Faiston NEXO
# =============================================================================
# Usage: Copy and adapt for testing AI agents
# Framework: pytest + unittest.mock
# =============================================================================

import pytest
import json
from unittest.mock import MagicMock, AsyncMock, patch

# =============================================================================
# Fixtures
# =============================================================================


@pytest.fixture
def mock_agent():
    """
    Mock Google ADK Agent class.

    Usage:
        def test_agent(mock_agent):
            mock_agent.run.return_value = "response"
    """
    with patch("google.adk.agents.Agent") as mock:
        agent = MagicMock()
        mock.return_value = agent
        yield agent


@pytest.fixture
def mock_session_service():
    """
    Mock InMemorySessionService for session management.

    Usage:
        async def test_session(mock_session_service):
            session = await mock_session_service.create_session(...)
    """
    with patch("google.adk.sessions.InMemorySessionService") as mock:
        service = MagicMock()
        service.create_session = AsyncMock(return_value=MagicMock())
        mock.return_value = service
        yield service


@pytest.fixture
def mock_runner():
    """
    Mock Runner with async iteration for streaming responses.

    Usage:
        async def test_runner(mock_runner):
            async for event in mock_runner.run_async(...):
                ...
    """
    with patch("google.adk.runners.Runner") as mock:
        runner = MagicMock()
        mock.return_value = runner

        async def mock_run_async(*args, **kwargs):
            event = MagicMock()
            event.is_final_response.return_value = True
            event.content = MagicMock()
            event.content.parts = [MagicMock(text='{"result": "success"}')]
            yield event

        runner.run_async = mock_run_async
        yield runner


@pytest.fixture
def flashcard_response():
    """Deterministic flashcard response for testing."""
    return {
        "flashcards": [
            {
                "id": "card-1",
                "question": "What is Python?",
                "answer": "A programming language",
                "difficulty": "easy",
            },
            {
                "id": "card-2",
                "question": "What is React?",
                "answer": "A JavaScript library for building UIs",
                "difficulty": "medium",
            },
        ]
    }


@pytest.fixture
def mindmap_response():
    """Deterministic mind map response for testing."""
    return {
        "title": "Test Lesson",
        "nodes": [
            {
                "id": "root",
                "label": "Main Topic",
                "children": [
                    {"id": "child-1", "label": "Subtopic 1", "timestamp": 60},
                    {"id": "child-2", "label": "Subtopic 2", "timestamp": 120},
                ],
            }
        ],
        "generatedAt": "2025-01-01T00:00:00Z",
    }


@pytest.fixture
def sample_transcription():
    """Sample transcription for testing agent inputs."""
    return """
    Nesta aula vamos aprender sobre Python.
    Python é uma linguagem de programação de alto nível.
    É muito usada para ciência de dados e machine learning.
    Também é popular para desenvolvimento web com frameworks como Django e Flask.
    """


# =============================================================================
# Utility Function Tests
# =============================================================================


class TestJsonParsing:
    """Tests for JSON parsing utilities."""

    def test_extract_json_from_markdown(self):
        """Should extract JSON from markdown code block."""
        from server.agentcore.agents.utils import extract_json

        response = """
        Here is the result:
        ```json
        {"flashcards": [{"q": "Q1", "a": "A1"}]}
        ```
        """

        result = extract_json(response)
        assert '{"flashcards"' in result

    def test_extract_json_raw(self):
        """Should extract raw JSON without markdown."""
        from server.agentcore.agents.utils import extract_json

        response = '{"key": "value"}'
        result = extract_json(response)

        assert result == '{"key": "value"}'

    def test_parse_json_safe_valid(self):
        """Should parse valid JSON."""
        from server.agentcore.agents.utils import parse_json_safe

        result = parse_json_safe('{"key": "value"}')

        assert result == {"key": "value"}

    def test_parse_json_safe_invalid(self):
        """Should return error dict for invalid JSON."""
        from server.agentcore.agents.utils import parse_json_safe

        result = parse_json_safe("not json")

        assert "error" in result
        assert "raw_response" in result


# =============================================================================
# Agent Response Tests
# =============================================================================


class TestFlashcardsAgent:
    """Tests for FlashcardsAgent."""

    @pytest.mark.asyncio
    async def test_generate_returns_flashcards(self, flashcard_response):
        """Should return flashcards with correct structure."""
        with patch("google.adk.runners.Runner") as mock_runner_class:
            runner = MagicMock()
            mock_runner_class.return_value = runner

            async def mock_run(*args, **kwargs):
                event = MagicMock()
                event.is_final_response.return_value = True
                event.content.parts = [MagicMock(text=json.dumps(flashcard_response))]
                yield event

            runner.run_async = mock_run

            from server.agentcore.agents.flashcards_agent import FlashcardsAgent

            agent = FlashcardsAgent()
            result = await agent.generate(
                transcription="Test content",
                difficulty="medium",
                count=5,
            )

            assert "flashcards" in result
            assert len(result["flashcards"]) == 2

    @pytest.mark.asyncio
    async def test_handles_empty_response(self):
        """Should handle empty LLM response gracefully."""
        with patch("google.adk.runners.Runner") as mock_runner_class:
            runner = MagicMock()
            mock_runner_class.return_value = runner

            async def mock_run(*args, **kwargs):
                event = MagicMock()
                event.is_final_response.return_value = True
                event.content = None  # Empty response
                yield event

            runner.run_async = mock_run

            from server.agentcore.agents.flashcards_agent import FlashcardsAgent

            agent = FlashcardsAgent()
            result = await agent.generate(
                transcription="Test content",
                difficulty="medium",
                count=5,
            )

            # Should return empty flashcards or error, not crash
            assert isinstance(result, dict)


class TestMindMapAgent:
    """Tests for MindMapAgent."""

    @pytest.mark.asyncio
    async def test_generate_returns_nodes(self, mindmap_response):
        """Should return mind map with nodes."""
        with patch("google.adk.runners.Runner") as mock_runner_class:
            runner = MagicMock()
            mock_runner_class.return_value = runner

            async def mock_run(*args, **kwargs):
                event = MagicMock()
                event.is_final_response.return_value = True
                event.content.parts = [MagicMock(text=json.dumps(mindmap_response))]
                yield event

            runner.run_async = mock_run

            from server.agentcore.agents.mindmap_agent import MindMapAgent

            agent = MindMapAgent()
            result = await agent.generate(
                transcription="Test content",
                episode_title="Test Lesson",
            )

            assert "nodes" in result
            assert result["title"] == "Test Lesson"


class TestNEXOAgent:
    """Tests for NEXOAgent (AI Tutor)."""

    @pytest.mark.asyncio
    async def test_invoke_returns_response(self, sample_transcription):
        """Should return response based on transcription."""
        with patch("google.adk.runners.Runner") as mock_runner_class:
            runner = MagicMock()
            mock_runner_class.return_value = runner

            async def mock_run(*args, **kwargs):
                event = MagicMock()
                event.is_final_response.return_value = True
                event.content.parts = [
                    MagicMock(text="Python é uma linguagem de programação!")
                ]
                yield event

            runner.run_async = mock_run

            from server.agentcore.agents.nexo_agent import NEXOAgent

            agent = NEXOAgent()
            result = await agent.invoke(
                prompt=f"O que é Python?\n\nTranscrição: {sample_transcription}",
                user_id="test-user",
                session_id="test-session-123456789012345678901234",
            )

            assert isinstance(result, str)
            assert len(result) > 0


# =============================================================================
# Main Entrypoint Tests
# =============================================================================


class TestAgentCoreMain:
    """Tests for AgentCore main entrypoint."""

    def test_invoke_routes_to_correct_agent(self):
        """Should route action to correct agent."""
        with patch("server.agentcore.main.NEXOAgent") as mock_nexo, patch(
            "server.agentcore.main.FlashcardsAgent"
        ) as mock_flash:
            # Configure mocks
            nexo_instance = mock_nexo.return_value
            nexo_instance.invoke = AsyncMock(return_value="Response")

            flash_instance = mock_flash.return_value
            flash_instance.generate = AsyncMock(return_value={"flashcards": []})

            from server.agentcore.main import invoke

            # Test nexo_chat action
            payload = {
                "action": "nexo_chat",
                "question": "What is Python?",
                "transcription": "Test transcription",
            }
            context = MagicMock()
            context.session_id = "test-session-123456789012345678901234"

            result = invoke(payload, context)

            assert "answer" in result or "error" in result

    def test_invoke_handles_unknown_action(self):
        """Should return error for unknown action."""
        from server.agentcore.main import invoke

        payload = {"action": "unknown_action"}
        context = MagicMock()

        result = invoke(payload, context)

        assert "error" in result
        assert "unknown" in result["error"].lower()


# =============================================================================
# Integration Tests (with mocked LLM)
# =============================================================================


class TestAgentIntegration:
    """Integration tests with mocked LLM responses."""

    @pytest.mark.asyncio
    async def test_full_flashcard_flow(self, sample_transcription, flashcard_response):
        """Test complete flashcard generation flow."""
        with patch("google.adk.runners.Runner") as mock_runner_class:
            runner = MagicMock()
            mock_runner_class.return_value = runner

            async def mock_run(*args, **kwargs):
                event = MagicMock()
                event.is_final_response.return_value = True
                event.content.parts = [MagicMock(text=json.dumps(flashcard_response))]
                yield event

            runner.run_async = mock_run

            from server.agentcore.agents.flashcards_agent import FlashcardsAgent

            agent = FlashcardsAgent()
            result = await agent.generate(
                transcription=sample_transcription,
                difficulty="medium",
                count=5,
            )

            # Verify structure
            assert "flashcards" in result
            for card in result["flashcards"]:
                assert "question" in card
                assert "answer" in card

    @pytest.mark.asyncio
    async def test_conversation_flow(self, sample_transcription):
        """Test multi-turn conversation with NEXO."""
        responses = [
            "Python é uma linguagem de programação!",
            "Sim, Python é usado para machine learning.",
        ]
        response_iter = iter(responses)

        with patch("google.adk.runners.Runner") as mock_runner_class:
            runner = MagicMock()
            mock_runner_class.return_value = runner

            async def mock_run(*args, **kwargs):
                event = MagicMock()
                event.is_final_response.return_value = True
                event.content.parts = [MagicMock(text=next(response_iter))]
                yield event

            runner.run_async = mock_run

            from server.agentcore.agents.nexo_agent import NEXOAgent

            agent = NEXOAgent()

            # First question
            r1 = await agent.invoke(
                prompt=f"O que é Python?\n\n{sample_transcription}",
                user_id="test",
                session_id="test-session-123456789012345678901234",
            )
            assert "Python" in r1

            # Follow-up
            r2 = await agent.invoke(
                prompt=f"É usado para machine learning?\n\n{sample_transcription}",
                user_id="test",
                session_id="test-session-123456789012345678901234",
            )
            assert "machine learning" in r2.lower()
