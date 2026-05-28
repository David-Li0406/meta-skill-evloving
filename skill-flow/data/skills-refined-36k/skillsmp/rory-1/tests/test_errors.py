"""
Unit tests for tools/errors.py - Error handling and recovery guidance.

Tests cover:
- Error categorization
- Recovery guidance lookup
- Error formatting
- User-friendly message generation
"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "tools"))

from errors import (
    ErrorCategory,
    RecoveryGuidance,
    RECOVERY_GUIDES,
    format_error,
    format_missing_credential_error,
    format_budget_error,
    format_error_message
)


# ============================================================================
# Recovery Guides Structure Tests
# ============================================================================

class TestRecoveryGuides:
    """Test recovery guide structure and coverage."""

    def test_all_services_have_guides(self):
        """Test that all expected services have recovery guides."""
        expected_services = [
            "apollo", "firecrawl", "clearbit",
            "google_ads", "linkedin_ads", "proxycurl"
        ]
        for service in expected_services:
            assert service in RECOVERY_GUIDES, f"Missing guides for {service}"

    def test_common_errors_covered(self):
        """Test that common error codes are covered."""
        common_codes = ["401", "403", "429", "missing_credential"]

        for service, guides in RECOVERY_GUIDES.items():
            for code in common_codes:
                # Not all services have all codes, but auth errors should be covered
                if code in ["401", "missing_credential"]:
                    assert code in guides or "AUTHENTICATION_ERROR" in guides, \
                        f"{service} missing handler for {code}"

    def test_recovery_guidance_has_required_fields(self):
        """Test all RecoveryGuidance objects have required fields."""
        for service, guides in RECOVERY_GUIDES.items():
            for code, guidance in guides.items():
                assert guidance.summary, f"{service}/{code} missing summary"
                assert guidance.steps, f"{service}/{code} missing steps"
                assert len(guidance.steps) > 0, f"{service}/{code} has empty steps"


# ============================================================================
# Error Formatting Tests
# ============================================================================

class TestFormatError:
    """Test error formatting functions."""

    def test_format_known_error(self):
        """Test formatting a known error code."""
        result = format_error(
            service="apollo",
            error_code="401",
            original_message="Unauthorized"
        )

        assert result["error"] is True
        assert result["service"] == "apollo"
        assert result["code"] == "401"
        assert "recovery" in result
        assert "steps" in result["recovery"]

    def test_format_unknown_error(self):
        """Test formatting an unknown error code."""
        result = format_error(
            service="apollo",
            error_code="999",
            original_message="Something went wrong"
        )

        assert result["error"] is True
        assert result["message"] == "Something went wrong"

    def test_format_error_includes_context(self):
        """Test that context is included in formatted error."""
        result = format_error(
            service="google_ads",
            error_code="QUOTA_ERROR",
            context={"customer_id": "123456"}
        )

        assert "context" in result
        assert result["context"]["customer_id"] == "123456"

    def test_format_error_categorizes_correctly(self):
        """Test error categorization."""
        auth_error = format_error("apollo", "401")
        assert auth_error["category"] == ErrorCategory.AUTHENTICATION.value

        rate_error = format_error("apollo", "429")
        assert rate_error["category"] == ErrorCategory.RATE_LIMIT.value

        budget_error = format_error("google_ads", "BUDGET_EXCEEDED")
        assert budget_error["category"] == ErrorCategory.BUDGET.value


class TestFormatMissingCredentialError:
    """Test missing credential error formatting."""

    def test_apollo_missing_credential(self):
        """Test Apollo missing credential error."""
        result = format_missing_credential_error("apollo")

        assert result["error"] is True
        assert result["code"] == "missing_credential"
        assert "recovery" in result
        assert any("apollo.io" in step.lower() for step in result["recovery"]["steps"])

    def test_google_ads_missing_credential(self):
        """Test Google Ads missing credential error."""
        result = format_missing_credential_error("google_ads")

        assert "recovery" in result
        # Should mention setup guide
        assert any("google-ads.md" in step for step in result["recovery"]["steps"])


class TestFormatBudgetError:
    """Test budget limit error formatting."""

    def test_budget_error_includes_amounts(self):
        """Test budget error includes requested and maximum amounts."""
        result = format_budget_error(
            service="google_ads",
            requested=500.0,
            maximum=100.0
        )

        assert result["error"] is True
        assert "$500" in result["message"]
        assert "$100" in result["message"]
        assert result["context"]["requested"] == 500.0
        assert result["context"]["maximum"] == 100.0


# ============================================================================
# User-Friendly Message Tests
# ============================================================================

class TestFormatErrorMessage:
    """Test user-friendly message formatting."""

    def test_basic_message_formatting(self):
        """Test basic error message formatting."""
        error = format_error("apollo", "401")
        message = format_error_message(error)

        assert "Error" in message or "error" in message.lower()
        assert "fix" in message.lower() or "How to" in message

    def test_includes_recovery_steps(self):
        """Test message includes recovery steps."""
        error = format_error("firecrawl", "401")
        message = format_error_message(error)

        # Should have numbered steps
        assert "1." in message
        assert "firecrawl" in message.lower()

    def test_includes_documentation_link(self):
        """Test message includes documentation link when available."""
        error = format_error("google_ads", "AUTHENTICATION_ERROR")
        message = format_error_message(error)

        if error.get("recovery", {}).get("documentation"):
            assert "Documentation" in message or "http" in message

    def test_includes_retry_time(self):
        """Test message includes retry time for rate limits."""
        error = format_error("apollo", "429")
        message = format_error_message(error)

        if error.get("recovery", {}).get("retry_after_seconds"):
            assert "Retry" in message or "seconds" in message


# ============================================================================
# Edge Cases
# ============================================================================

class TestEdgeCases:
    """Test edge cases in error handling."""

    def test_unknown_service(self):
        """Test handling of unknown service."""
        result = format_error(
            service="unknown_service",
            error_code="500",
            original_message="Server error"
        )

        assert result["error"] is True
        assert result["service"] == "unknown_service"
        # Should still categorize as unknown
        assert result["category"] == ErrorCategory.UNKNOWN.value

    def test_empty_original_message(self):
        """Test handling of empty original message."""
        result = format_error("apollo", "401", original_message="")

        # Should use recovery summary as message
        assert result["message"]
        assert len(result["message"]) > 0

    def test_error_code_as_int(self):
        """Test error code as integer is handled."""
        result = format_error("firecrawl", 401)

        # Should convert to string
        assert result["code"] == "401"
