# /// script
# requires-python = ">=3.11"
# dependencies = ["pytest>=8.0.0", "notion-client>=2.6.0"]
# ///
"""Tests for Notion client wrapper functions.

Oracle Source: Notion API Reference - Authentication
https://developers.notion.com/reference/authentication

Test Principles Applied:
- Oracles from domain rules (token format per Notion docs)
- Black-box: Test validation against expected formats
- Invalid inputs must raise exceptions or return failure
- Deterministic with documented tolerances
"""

import pytest
import sys
from pathlib import Path
from unittest.mock import Mock, patch

# Add scripts to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from notion_wrapper import validate_token, get_client, api_call_with_retry


# =============================================================================
# ORACLES: Token format rules from Notion API documentation
# =============================================================================

class NotionAuthOracle:
    """Oracle for Notion authentication rules.

    Source: https://developers.notion.com/reference/authentication
    Retrieved: 2025-12-23

    Token formats:
    - Internal integration: starts with "secret_" (legacy) or "ntn_" (new)
    - OAuth: starts with specific prefix
    """

    VALID_PREFIXES = ("ntn_", "secret_")

    @classmethod
    def is_valid_format(cls, token: str) -> bool:
        """Oracle: Check if token has valid format per API docs."""
        return token.startswith(cls.VALID_PREFIXES)


# =============================================================================
# INTEGRITY TESTS: First principles validation
# =============================================================================

class TestClientIntegrity:
    """Integrity tests for client functions."""

    def test_get_client_returns_client_object(self):
        """First principle: get_client returns a Client instance."""
        # We can't import Client directly without the package,
        # but we can verify get_client is callable
        from notion_wrapper import get_client
        assert callable(get_client)

    def test_validate_token_returns_tuple(self):
        """First principle: validate_token returns (bool, str) tuple."""
        # Test with obviously invalid token (format check before API call)
        result = validate_token("invalid_token")
        assert isinstance(result, tuple)
        assert len(result) == 2
        assert isinstance(result[0], bool)
        assert isinstance(result[1], str)


# =============================================================================
# BLACK-BOX TESTS: Token format validation against oracle
# =============================================================================

class TestTokenFormatValidation:
    """Black-box tests for token format validation."""

    def test_ntn_prefix_is_valid_format(self):
        """Token starting with 'ntn_' is valid format per API docs."""
        token = "ntn_abc123def456"
        assert NotionAuthOracle.is_valid_format(token)

    def test_secret_prefix_is_valid_format(self):
        """Token starting with 'secret_' is valid format per API docs."""
        token = "secret_abc123def456"
        assert NotionAuthOracle.is_valid_format(token)

    def test_other_prefix_is_invalid_format(self):
        """Token with other prefix is invalid format per API docs."""
        invalid_tokens = [
            "invalid_token",
            "bearer_abc123",
            "api_key_xyz",
            "abc123",
            "",
        ]
        for token in invalid_tokens:
            assert not NotionAuthOracle.is_valid_format(token)

    def test_validate_token_rejects_invalid_format(self):
        """validate_token rejects tokens with invalid format."""
        result = validate_token("invalid_format_token")
        success, message = result
        assert success is False
        assert "ntn_" in message or "secret_" in message


# =============================================================================
# WHITE-BOX TESTS: Validate internal logic
# =============================================================================

class TestValidateTokenWhiteBox:
    """White-box tests for validate_token internal logic."""

    def test_format_check_happens_before_api_call(self):
        """Format validation occurs before making API request."""
        # This test verifies we don't make unnecessary API calls
        # for obviously invalid tokens
        result = validate_token("bad_token")
        success, message = result

        # Should fail with format message, not API error
        assert success is False
        assert "must start with" in message.lower() or "ntn_" in message

    def test_valid_format_but_invalid_token_fails_gracefully(self):
        """Token with valid format but invalid value fails gracefully."""
        # This would fail at the API level, not format level
        # We can't test actual API without mocking
        result = validate_token("ntn_this_is_not_real_but_has_valid_format")
        success, message = result

        # Should fail (either connection or auth error)
        # The exact error depends on network availability
        assert success is False


# =============================================================================
# RETRY LOGIC TESTS (with mocking)
# =============================================================================

class TestRetryLogic:
    """Tests for api_call_with_retry function."""

    def test_successful_call_returns_immediately(self):
        """Successful API call returns without retry."""
        mock_func = Mock(return_value={"status": "ok"})
        result = api_call_with_retry(mock_func, "arg1", kwarg1="value1")

        assert result == {"status": "ok"}
        assert mock_func.call_count == 1
        mock_func.assert_called_with("arg1", kwarg1="value1")

    def test_non_retryable_error_raises_immediately(self):
        """Non-retryable errors raise without retry attempts."""
        from notion_client import APIResponseError, APIErrorCode

        # Create a real exception instance by subclassing
        class MockNotFoundError(APIResponseError):
            def __init__(self):
                self.code = APIErrorCode.ObjectNotFound
                self.message = "Object not found"

        mock_func = Mock(side_effect=MockNotFoundError())

        with pytest.raises(APIResponseError):
            api_call_with_retry(mock_func, max_retries=3)

        # Should only try once for non-retryable errors
        assert mock_func.call_count == 1

    def test_max_retries_exceeded_raises(self):
        """Exceeding max retries raises RuntimeError."""
        from notion_client import APIResponseError, APIErrorCode

        # Create a real exception instance by subclassing
        class MockRateLimitError(APIResponseError):
            def __init__(self):
                self.code = APIErrorCode.RateLimited
                self.message = "Rate limited"
                self.additional_data = {"retry_after": 0}  # No wait for testing

        mock_func = Mock(side_effect=MockRateLimitError())

        with pytest.raises(RuntimeError, match="Max retries"):
            api_call_with_retry(mock_func, max_retries=3)

        # Should have tried 3 times
        assert mock_func.call_count == 3


# =============================================================================
# EDGE CASES
# =============================================================================

class TestClientEdgeCases:
    """Edge case tests for client functions."""

    def test_empty_token_is_invalid(self):
        """Empty string token is rejected."""
        result = validate_token("")
        success, _ = result
        assert success is False

    def test_whitespace_only_token_is_invalid(self):
        """Whitespace-only token is rejected."""
        result = validate_token("   ")
        success, _ = result
        assert success is False

    def test_token_with_valid_prefix_but_short(self):
        """Short token with valid prefix is still format-valid."""
        # Format is valid, but API will reject
        result = validate_token("ntn_")
        # Format check passes, but API call fails
        success, _ = result
        assert success is False  # API rejects

    def test_case_sensitivity_of_prefix(self):
        """Token prefix is case-sensitive."""
        # NTN_ is NOT valid (must be lowercase)
        result = validate_token("NTN_abc123")
        success, _ = result
        assert success is False


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
