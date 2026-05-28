"""
Unit tests for tools/audit.py - Audit logging for ads operations.

Tests cover:
- Audit event creation
- Log file writing
- Sensitive data sanitization
- Convenience logging methods
"""

import pytest
import json
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

sys.path.insert(0, str(Path(__file__).parent.parent / "tools"))

from audit import (
    AuditEventType,
    AuditSeverity,
    AuditEvent,
    AuditLogger,
    get_audit_logger,
    log_ads_event
)


# ============================================================================
# AuditEvent Tests
# ============================================================================

class TestAuditEvent:
    """Test AuditEvent dataclass."""

    def test_basic_event(self):
        """Test basic event creation."""
        event = AuditEvent(
            timestamp="2024-01-01T00:00:00Z",
            event_type="create_campaign",
            severity="info",
            platform="google_ads",
            operation="Create campaign",
            success=True
        )

        assert event.platform == "google_ads"
        assert event.success is True

    def test_to_dict_excludes_none(self):
        """Test to_dict excludes None values."""
        event = AuditEvent(
            timestamp="2024-01-01T00:00:00Z",
            event_type="create_campaign",
            severity="info",
            platform="google_ads",
            operation="Create campaign",
            success=True,
            campaign_id=None,  # Should be excluded
            details=None
        )

        result = event.to_dict()
        assert "campaign_id" not in result
        assert "details" not in result

    def test_to_json(self):
        """Test JSON serialization."""
        event = AuditEvent(
            timestamp="2024-01-01T00:00:00Z",
            event_type="create_campaign",
            severity="info",
            platform="google_ads",
            operation="Create campaign",
            success=True,
            campaign_id="12345"
        )

        json_str = event.to_json()
        parsed = json.loads(json_str)

        assert parsed["platform"] == "google_ads"
        assert parsed["campaign_id"] == "12345"


# ============================================================================
# AuditLogger Tests
# ============================================================================

class TestAuditLogger:
    """Test AuditLogger class."""

    @pytest.fixture
    def temp_log_dir(self, tmp_path):
        """Create temporary log directory."""
        log_dir = tmp_path / "logs"
        log_dir.mkdir()
        return log_dir

    @pytest.fixture
    def logger(self, temp_log_dir):
        """Create logger with temp directory."""
        return AuditLogger(log_dir=str(temp_log_dir))

    def test_logger_creates_log_file(self, temp_log_dir):
        """Test logger creates log file."""
        logger = AuditLogger(log_dir=str(temp_log_dir))

        logger.log(
            event_type=AuditEventType.CREATE_CAMPAIGN,
            platform="google_ads",
            operation="Test",
            success=True
        )

        log_file = temp_log_dir / "ads_audit.log"
        assert log_file.exists()

    def test_log_writes_json(self, logger, temp_log_dir):
        """Test log writes valid JSON."""
        logger.log(
            event_type=AuditEventType.CREATE_CAMPAIGN,
            platform="google_ads",
            operation="Create test campaign",
            success=True,
            campaign_id="12345"
        )

        log_file = temp_log_dir / "ads_audit.log"
        with open(log_file, 'r') as f:
            line = f.readline()
            parsed = json.loads(line)

        assert parsed["platform"] == "google_ads"
        assert parsed["campaign_id"] == "12345"

    def test_sanitize_removes_secrets(self, logger):
        """Test that sensitive data is sanitized."""
        request_data = {
            "campaign_name": "Test",
            "api_key": "secret-key-12345",
            "access_token": "bearer-token",
            "normal_field": "value"
        }

        sanitized = logger._sanitize_request(request_data)

        assert sanitized["campaign_name"] == "Test"
        assert sanitized["api_key"] == "[REDACTED]"
        assert sanitized["access_token"] == "[REDACTED]"
        assert sanitized["normal_field"] == "value"

    def test_sanitize_nested_dict(self, logger):
        """Test sanitization of nested dictionaries."""
        request_data = {
            "config": {
                "client_secret": "secret123",
                "name": "test"
            }
        }

        sanitized = logger._sanitize_request(request_data)

        assert sanitized["config"]["client_secret"] == "[REDACTED]"
        assert sanitized["config"]["name"] == "test"

    def test_disabled_logger_does_not_log(self, temp_log_dir):
        """Test that disabled logger does not write."""
        logger = AuditLogger(log_dir=str(temp_log_dir))
        logger.enabled = False

        logger.log(
            event_type=AuditEventType.CREATE_CAMPAIGN,
            platform="google_ads",
            operation="Test",
            success=True
        )

        log_file = temp_log_dir / "ads_audit.log"
        # File may exist but should be empty
        if log_file.exists():
            assert log_file.stat().st_size == 0


# ============================================================================
# Convenience Method Tests
# ============================================================================

class TestConvenienceMethods:
    """Test convenience logging methods."""

    @pytest.fixture
    def logger(self, tmp_path):
        """Create logger with temp directory."""
        log_dir = tmp_path / "logs"
        log_dir.mkdir()
        return AuditLogger(log_dir=str(log_dir))

    def test_log_campaign_created(self, logger, tmp_path):
        """Test campaign creation logging."""
        logger.log_campaign_created(
            platform="google_ads",
            account_id="123",
            campaign_id="456",
            campaign_name="Test Campaign",
            status="PAUSED",
            budget=100.0
        )

        log_file = tmp_path / "logs" / "ads_audit.log"
        with open(log_file, 'r') as f:
            entry = json.loads(f.readline())

        assert entry["event_type"] == "create_campaign"
        assert entry["details"]["campaign_name"] == "Test Campaign"
        assert entry["details"]["daily_budget"] == 100.0

    def test_log_status_change(self, logger, tmp_path):
        """Test status change logging."""
        logger.log_status_change(
            platform="linkedin_ads",
            campaign_id="789",
            old_status="DRAFT",
            new_status="ACTIVE",
            confirmed=True
        )

        log_file = tmp_path / "logs" / "ads_audit.log"
        with open(log_file, 'r') as f:
            entry = json.loads(f.readline())

        assert entry["event_type"] == "update_status"
        assert entry["severity"] == "warning"  # ACTIVE should be warning
        assert entry["details"]["new_status"] == "ACTIVE"

    def test_log_budget_change(self, logger, tmp_path):
        """Test budget change logging."""
        logger.log_budget_change(
            platform="google_ads",
            campaign_id="123",
            old_budget=50.0,
            new_budget=100.0,
            confirmed=True
        )

        log_file = tmp_path / "logs" / "ads_audit.log"
        with open(log_file, 'r') as f:
            entry = json.loads(f.readline())

        assert entry["event_type"] == "update_budget"
        assert entry["details"]["change_type"] == "increase"
        assert entry["severity"] == "warning"

    def test_log_budget_decrease(self, logger, tmp_path):
        """Test budget decrease logs as info, not warning."""
        logger.log_budget_change(
            platform="google_ads",
            campaign_id="123",
            old_budget=100.0,
            new_budget=50.0,
            confirmed=True
        )

        log_file = tmp_path / "logs" / "ads_audit.log"
        with open(log_file, 'r') as f:
            entry = json.loads(f.readline())

        assert entry["details"]["change_type"] == "decrease"
        assert entry["severity"] == "info"

    def test_log_budget_limit_exceeded(self, logger, tmp_path):
        """Test budget limit exceeded logging."""
        logger.log_budget_limit_exceeded(
            platform="google_ads",
            requested=500.0,
            maximum=100.0
        )

        log_file = tmp_path / "logs" / "ads_audit.log"
        with open(log_file, 'r') as f:
            entry = json.loads(f.readline())

        assert entry["event_type"] == "budget_limit_exceeded"
        assert entry["success"] is False
        assert entry["details"]["requested_budget"] == 500.0

    def test_log_api_error(self, logger, tmp_path):
        """Test API error logging."""
        logger.log_api_error(
            platform="linkedin_ads",
            operation="Create campaign",
            error_code="401",
            error_message="Unauthorized"
        )

        log_file = tmp_path / "logs" / "ads_audit.log"
        with open(log_file, 'r') as f:
            entry = json.loads(f.readline())

        assert entry["event_type"] == "api_error"
        assert entry["severity"] == "error"
        assert entry["error_message"] == "Unauthorized"


# ============================================================================
# Global Logger Tests
# ============================================================================

class TestGlobalLogger:
    """Test global logger singleton."""

    def test_get_audit_logger_returns_singleton(self):
        """Test get_audit_logger returns same instance."""
        # Reset global
        import audit
        audit._audit_logger = None

        logger1 = get_audit_logger()
        logger2 = get_audit_logger()

        assert logger1 is logger2

    def test_log_ads_event_uses_global_logger(self, tmp_path):
        """Test log_ads_event convenience function."""
        import audit
        audit._audit_logger = None

        # Create a logger with temp dir
        log_dir = tmp_path / "logs"
        log_dir.mkdir()
        audit._audit_logger = AuditLogger(log_dir=str(log_dir))

        log_ads_event(
            event_type=AuditEventType.LIST_CAMPAIGNS,
            platform="google_ads",
            operation="List campaigns",
            success=True
        )

        log_file = log_dir / "ads_audit.log"
        assert log_file.exists()
