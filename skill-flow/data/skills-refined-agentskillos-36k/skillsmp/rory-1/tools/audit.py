"""
Audit Logging for CMO Agent Ads Operations

Provides detailed audit trail for all advertising operations.
This is critical for tracking spend, changes, and debugging issues.
"""

import os
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any, Literal
from dataclasses import dataclass, asdict
from enum import Enum

try:
    import yaml
except ImportError:
    yaml = None


# ============================================================================
# Audit Event Types
# ============================================================================

class AuditEventType(Enum):
    """Types of auditable events."""
    # Read operations
    LIST_ACCOUNTS = "list_accounts"
    LIST_CAMPAIGNS = "list_campaigns"
    GET_CAMPAIGN = "get_campaign"
    GET_PERFORMANCE = "get_performance"
    RUN_QUERY = "run_query"

    # Write operations (higher risk)
    CREATE_CAMPAIGN = "create_campaign"
    UPDATE_CAMPAIGN = "update_campaign"
    UPDATE_STATUS = "update_status"
    UPDATE_BUDGET = "update_budget"
    DELETE_CAMPAIGN = "delete_campaign"

    # Safety events
    BUDGET_LIMIT_EXCEEDED = "budget_limit_exceeded"
    CONFIRMATION_REQUIRED = "confirmation_required"
    CONFIRMATION_RECEIVED = "confirmation_received"

    # System events
    CREDENTIALS_LOADED = "credentials_loaded"
    CREDENTIALS_MISSING = "credentials_missing"
    API_ERROR = "api_error"


class AuditSeverity(Enum):
    """Severity levels for audit events."""
    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


@dataclass
class AuditEvent:
    """Represents a single audit event."""
    timestamp: str
    event_type: str
    severity: str
    platform: str  # google_ads, linkedin_ads, meta_ads
    operation: str
    success: bool
    user_id: Optional[str] = None
    account_id: Optional[str] = None
    campaign_id: Optional[str] = None
    details: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None
    request_data: Optional[Dict[str, Any]] = None
    response_summary: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary, excluding None values."""
        return {k: v for k, v in asdict(self).items() if v is not None}

    def to_json(self) -> str:
        """Convert to JSON string."""
        return json.dumps(self.to_dict())


# ============================================================================
# Audit Logger Class
# ============================================================================

class AuditLogger:
    """
    Audit logger for ads operations.

    Logs to both file and standard logging for flexibility.
    """

    def __init__(
        self,
        log_dir: Optional[str] = None,
        log_file: str = "ads_audit.log",
        config_path: Optional[str] = None
    ):
        self.config = self._load_config(config_path)
        self.enabled = self.config.get("audit_trail", True)

        # Set up log directory
        if log_dir is None:
            log_dir = Path(__file__).parent.parent / "logs"
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)

        self.log_file = self.log_dir / log_file

        # Set up Python logger
        self.logger = logging.getLogger("cmo_agent.audit")
        self._setup_logger()

    def _load_config(self, config_path: Optional[str] = None) -> Dict[str, Any]:
        """Load logging configuration from ads_config.yaml."""
        if config_path is None:
            config_path = Path(__file__).parent / "ads_config.yaml"

        if yaml and Path(config_path).exists():
            with open(config_path, 'r') as f:
                full_config = yaml.safe_load(f)
                return full_config.get("logging", {})

        # Defaults
        return {
            "log_api_calls": True,
            "log_level": "INFO",
            "audit_trail": True
        }

    def _setup_logger(self):
        """Configure the Python logger."""
        log_level = getattr(
            logging,
            self.config.get("log_level", "INFO").upper(),
            logging.INFO
        )
        self.logger.setLevel(log_level)

        # File handler for audit log
        if not self.logger.handlers:
            file_handler = logging.FileHandler(self.log_file)
            file_handler.setLevel(log_level)

            # JSON formatter for structured logs
            formatter = logging.Formatter('%(message)s')
            file_handler.setFormatter(formatter)

            self.logger.addHandler(file_handler)

    def log(
        self,
        event_type: AuditEventType,
        platform: str,
        operation: str,
        success: bool,
        severity: AuditSeverity = AuditSeverity.INFO,
        account_id: Optional[str] = None,
        campaign_id: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
        error_message: Optional[str] = None,
        request_data: Optional[Dict[str, Any]] = None,
        response_summary: Optional[Dict[str, Any]] = None
    ):
        """
        Log an audit event.

        Args:
            event_type: Type of event
            platform: Ads platform (google_ads, linkedin_ads)
            operation: Description of operation
            success: Whether operation succeeded
            severity: Log severity level
            account_id: Ads account ID
            campaign_id: Campaign ID (if applicable)
            details: Additional details
            error_message: Error message if failed
            request_data: Sanitized request data (no secrets!)
            response_summary: Summary of response
        """
        if not self.enabled:
            return

        event = AuditEvent(
            timestamp=datetime.utcnow().isoformat() + "Z",
            event_type=event_type.value,
            severity=severity.value,
            platform=platform,
            operation=operation,
            success=success,
            account_id=account_id,
            campaign_id=campaign_id,
            details=details,
            error_message=error_message,
            request_data=self._sanitize_request(request_data),
            response_summary=response_summary
        )

        # Log based on severity
        log_method = getattr(self.logger, severity.value, self.logger.info)
        log_method(event.to_json())

    def _sanitize_request(
        self,
        request_data: Optional[Dict[str, Any]]
    ) -> Optional[Dict[str, Any]]:
        """Remove sensitive data from request before logging."""
        if request_data is None:
            return None

        sanitized = request_data.copy()

        # Fields to redact
        sensitive_fields = {
            "api_key", "access_token", "refresh_token", "client_secret",
            "password", "secret", "token", "authorization"
        }

        def redact(obj):
            if isinstance(obj, dict):
                return {
                    k: "[REDACTED]" if k.lower() in sensitive_fields else redact(v)
                    for k, v in obj.items()
                }
            elif isinstance(obj, list):
                return [redact(item) for item in obj]
            return obj

        return redact(sanitized)

    # =========================================================================
    # Convenience Methods
    # =========================================================================

    def log_campaign_created(
        self,
        platform: str,
        account_id: str,
        campaign_id: str,
        campaign_name: str,
        status: str,
        budget: float
    ):
        """Log successful campaign creation."""
        self.log(
            event_type=AuditEventType.CREATE_CAMPAIGN,
            platform=platform,
            operation=f"Created campaign '{campaign_name}'",
            success=True,
            severity=AuditSeverity.INFO,
            account_id=account_id,
            campaign_id=campaign_id,
            details={
                "campaign_name": campaign_name,
                "status": status,
                "daily_budget": budget
            }
        )

    def log_status_change(
        self,
        platform: str,
        campaign_id: str,
        old_status: str,
        new_status: str,
        confirmed: bool
    ):
        """Log campaign status change."""
        # Higher severity for activation
        severity = (
            AuditSeverity.WARNING if new_status in ("ENABLED", "ACTIVE")
            else AuditSeverity.INFO
        )

        self.log(
            event_type=AuditEventType.UPDATE_STATUS,
            platform=platform,
            operation=f"Status change: {old_status} → {new_status}",
            success=True,
            severity=severity,
            campaign_id=campaign_id,
            details={
                "old_status": old_status,
                "new_status": new_status,
                "user_confirmed": confirmed
            }
        )

    def log_budget_change(
        self,
        platform: str,
        campaign_id: str,
        old_budget: float,
        new_budget: float,
        confirmed: bool
    ):
        """Log budget change."""
        change_type = "increase" if new_budget > old_budget else "decrease"

        self.log(
            event_type=AuditEventType.UPDATE_BUDGET,
            platform=platform,
            operation=f"Budget {change_type}: ${old_budget:.2f} → ${new_budget:.2f}",
            success=True,
            severity=AuditSeverity.WARNING if change_type == "increase" else AuditSeverity.INFO,
            campaign_id=campaign_id,
            details={
                "old_budget": old_budget,
                "new_budget": new_budget,
                "change_type": change_type,
                "user_confirmed": confirmed
            }
        )

    def log_budget_limit_exceeded(
        self,
        platform: str,
        requested: float,
        maximum: float
    ):
        """Log when budget limit is exceeded."""
        self.log(
            event_type=AuditEventType.BUDGET_LIMIT_EXCEEDED,
            platform=platform,
            operation=f"Budget ${requested:.2f} exceeds limit ${maximum:.2f}",
            success=False,
            severity=AuditSeverity.WARNING,
            details={
                "requested_budget": requested,
                "maximum_allowed": maximum,
                "config_file": "tools/ads_config.yaml"
            }
        )

    def log_confirmation_required(
        self,
        platform: str,
        operation: str,
        reason: str
    ):
        """Log when confirmation is required."""
        self.log(
            event_type=AuditEventType.CONFIRMATION_REQUIRED,
            platform=platform,
            operation=operation,
            success=False,  # Operation not completed
            severity=AuditSeverity.INFO,
            details={"reason": reason}
        )

    def log_api_error(
        self,
        platform: str,
        operation: str,
        error_code: str,
        error_message: str
    ):
        """Log API error."""
        self.log(
            event_type=AuditEventType.API_ERROR,
            platform=platform,
            operation=operation,
            success=False,
            severity=AuditSeverity.ERROR,
            error_message=error_message,
            details={"error_code": error_code}
        )

    def log_query(
        self,
        platform: str,
        query: str,
        account_id: str,
        result_count: int
    ):
        """Log a query operation."""
        if not self.config.get("log_api_calls", True):
            return

        self.log(
            event_type=AuditEventType.RUN_QUERY,
            platform=platform,
            operation="Execute query",
            success=True,
            severity=AuditSeverity.DEBUG,
            account_id=account_id,
            details={
                "query_preview": query[:200] + "..." if len(query) > 200 else query,
                "result_count": result_count
            }
        )


# ============================================================================
# Global Audit Logger Instance
# ============================================================================

_audit_logger: Optional[AuditLogger] = None


def get_audit_logger() -> AuditLogger:
    """Get or create the global audit logger."""
    global _audit_logger
    if _audit_logger is None:
        _audit_logger = AuditLogger()
    return _audit_logger


def log_ads_event(
    event_type: AuditEventType,
    platform: str,
    operation: str,
    success: bool,
    **kwargs
):
    """Convenience function to log an ads event."""
    get_audit_logger().log(
        event_type=event_type,
        platform=platform,
        operation=operation,
        success=success,
        **kwargs
    )


# ============================================================================
# CLI for viewing audit logs
# ============================================================================

def main():
    """CLI for viewing and managing audit logs."""
    import argparse

    parser = argparse.ArgumentParser(description="View CMO Agent audit logs")
    parser.add_argument(
        "--tail",
        type=int,
        default=20,
        help="Show last N entries"
    )
    parser.add_argument(
        "--platform",
        choices=["google_ads", "linkedin_ads", "all"],
        default="all",
        help="Filter by platform"
    )
    parser.add_argument(
        "--severity",
        choices=["debug", "info", "warning", "error", "critical", "all"],
        default="all",
        help="Filter by severity"
    )
    parser.add_argument(
        "--errors-only",
        action="store_true",
        help="Show only failed operations"
    )

    args = parser.parse_args()

    log_file = Path(__file__).parent.parent / "logs" / "ads_audit.log"

    if not log_file.exists():
        print("No audit log found. Logs will be created when ads operations run.")
        return

    # Read and filter logs
    entries = []
    with open(log_file, 'r') as f:
        for line in f:
            try:
                entry = json.loads(line.strip())
                entries.append(entry)
            except json.JSONDecodeError:
                continue

    # Apply filters
    if args.platform != "all":
        entries = [e for e in entries if e.get("platform") == args.platform]

    if args.severity != "all":
        entries = [e for e in entries if e.get("severity") == args.severity]

    if args.errors_only:
        entries = [e for e in entries if not e.get("success", True)]

    # Get last N entries
    entries = entries[-args.tail:]

    # Display
    print(f"\n📋 Audit Log (last {len(entries)} entries)\n")
    print("-" * 80)

    for entry in entries:
        timestamp = entry.get("timestamp", "")[:19]
        severity = entry.get("severity", "info").upper()
        platform = entry.get("platform", "unknown")
        operation = entry.get("operation", "")
        success = "✅" if entry.get("success") else "❌"

        # Color based on severity
        if severity == "ERROR":
            print(f"{timestamp} [{severity}] {success} [{platform}] {operation}")
            if entry.get("error_message"):
                print(f"           └─ {entry['error_message']}")
        elif severity == "WARNING":
            print(f"{timestamp} [{severity}] {success} [{platform}] {operation}")
        else:
            print(f"{timestamp} [{severity}] {success} [{platform}] {operation}")

    print("-" * 80)
    print(f"\nLog file: {log_file}")


if __name__ == "__main__":
    main()
