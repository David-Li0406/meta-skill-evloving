#!/usr/bin/env python3
"""
Enhanced Error Handling and Reporting System

Provides comprehensive error tracking, logging, and reporting capabilities.
"""

import sys
import traceback
import json
from pathlib import Path
from typing import Optional, Dict, Any, List
from datetime import datetime
from enum import Enum
import logging


class ErrorSeverity(Enum):
    """Error severity levels"""
    CRITICAL = "critical"  # System cannot continue
    ERROR = "error"        # Processing failed but can continue
    WARNING = "warning"    # Potential issue, processing succeeded
    INFO = "info"          # Informational message


class ErrorCategory(Enum):
    """Error categories for classification"""
    OCR_FAILURE = "ocr_failure"
    IMAGE_PROCESSING = "image_processing"
    FILE_ACCESS = "file_access"
    VALIDATION = "validation"
    EXTRACTION = "extraction"
    EXPORT = "export"
    SYSTEM = "system"
    UNKNOWN = "unknown"


class ExtractionError(Exception):
    """Custom exception for extraction errors"""

    def __init__(self, message: str, category: ErrorCategory = ErrorCategory.UNKNOWN,
                 severity: ErrorSeverity = ErrorSeverity.ERROR, context: Optional[Dict] = None):
        super().__init__(message)
        self.message = message
        self.category = category
        self.severity = severity
        self.context = context or {}
        self.timestamp = datetime.now()

    def to_dict(self) -> Dict[str, Any]:
        """Convert error to dictionary for logging"""
        return {
            'message': self.message,
            'category': self.category.value,
            'severity': self.severity.value,
            'context': self.context,
            'timestamp': self.timestamp.isoformat(),
        }


class ErrorHandler:
    """
    Centralized error handling and reporting system
    """

    def __init__(self, log_file: Optional[Path] = None, verbose: bool = True):
        """
        Initialize error handler

        Args:
            log_file: Path to log file (optional)
            verbose: If True, print errors to console
        """
        self.log_file = log_file
        self.verbose = verbose
        self.errors: List[ExtractionError] = []
        self.warnings: List[ExtractionError] = []

        # Setup logging
        self._setup_logging()

    def _setup_logging(self):
        """Setup Python logging"""
        log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

        handlers = []

        # Console handler
        if self.verbose:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(logging.DEBUG)
            console_handler.setFormatter(logging.Formatter(log_format))
            handlers.append(console_handler)

        # File handler
        if self.log_file:
            file_handler = logging.FileHandler(self.log_file, encoding='utf-8')
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(logging.Formatter(log_format))
            handlers.append(file_handler)

        # Configure logger
        self.logger = logging.getLogger('TrademarkExtractor')
        self.logger.setLevel(logging.DEBUG)
        self.logger.handlers = handlers
        self.logger.propagate = False

    def handle_error(self, error: Exception, category: ErrorCategory = ErrorCategory.UNKNOWN,
                     severity: ErrorSeverity = ErrorSeverity.ERROR, context: Optional[Dict] = None):
        """
        Handle and log an error

        Args:
            error: Exception object
            category: Error category
            severity: Error severity
            context: Additional context information
        """
        # Convert to ExtractionError if needed
        if isinstance(error, ExtractionError):
            extraction_error = error
        else:
            extraction_error = ExtractionError(
                message=str(error),
                category=category,
                severity=severity,
                context=context or {}
            )

        # Add stack trace to context
        extraction_error.context['traceback'] = traceback.format_exc()

        # Store error
        if severity in [ErrorSeverity.CRITICAL, ErrorSeverity.ERROR]:
            self.errors.append(extraction_error)
        elif severity == ErrorSeverity.WARNING:
            self.warnings.append(extraction_error)

        # Log error
        log_message = f"[{category.value.upper()}] {extraction_error.message}"

        if severity == ErrorSeverity.CRITICAL:
            self.logger.critical(log_message, extra=extraction_error.context)
        elif severity == ErrorSeverity.ERROR:
            self.logger.error(log_message, extra=extraction_error.context)
        elif severity == ErrorSeverity.WARNING:
            self.logger.warning(log_message, extra=extraction_error.context)
        else:
            self.logger.info(log_message, extra=extraction_error.context)

        # Print to console if verbose
        if self.verbose:
            self._print_error(extraction_error)

    def _print_error(self, error: ExtractionError):
        """Print error to console with formatting"""
        severity_colors = {
            ErrorSeverity.CRITICAL: '\033[91m',  # Red
            ErrorSeverity.ERROR: '\033[91m',     # Red
            ErrorSeverity.WARNING: '\033[93m',   # Yellow
            ErrorSeverity.INFO: '\033[94m',      # Blue
        }
        reset_color = '\033[0m'

        color = severity_colors.get(error.severity, '')
        print(f"{color}[{error.severity.value.upper()}] {error.category.value}: {error.message}{reset_color}",
              file=sys.stderr if error.severity in [ErrorSeverity.CRITICAL, ErrorSeverity.ERROR] else sys.stdout)

    def log_info(self, message: str, context: Optional[Dict] = None):
        """Log informational message"""
        self.logger.info(message, extra=context or {})
        if self.verbose:
            print(f"ℹ {message}")

    def log_warning(self, message: str, context: Optional[Dict] = None):
        """Log warning message"""
        warning = ExtractionError(message, category=ErrorCategory.UNKNOWN,
                                  severity=ErrorSeverity.WARNING, context=context)
        self.handle_error(warning, severity=ErrorSeverity.WARNING)

    def log_success(self, message: str):
        """Log success message"""
        if self.verbose:
            print(f"✓ {message}")
        self.logger.info(f"SUCCESS: {message}")

    def has_errors(self) -> bool:
        """Check if any errors were recorded"""
        return len(self.errors) > 0

    def has_critical_errors(self) -> bool:
        """Check if any critical errors were recorded"""
        return any(e.severity == ErrorSeverity.CRITICAL for e in self.errors)

    def get_error_summary(self) -> Dict[str, Any]:
        """Get summary of all errors and warnings"""
        return {
            'total_errors': len(self.errors),
            'total_warnings': len(self.warnings),
            'critical_errors': sum(1 for e in self.errors if e.severity == ErrorSeverity.CRITICAL),
            'errors_by_category': self._group_by_category(self.errors),
            'warnings_by_category': self._group_by_category(self.warnings),
        }

    def _group_by_category(self, error_list: List[ExtractionError]) -> Dict[str, int]:
        """Group errors by category"""
        groups = {}
        for error in error_list:
            category = error.category.value
            groups[category] = groups.get(category, 0) + 1
        return groups

    def generate_error_report(self, output_file: Optional[Path] = None) -> str:
        """
        Generate comprehensive error report

        Args:
            output_file: Optional path to save report

        Returns:
            Formatted report string
        """
        report_lines = []
        report_lines.append("=" * 80)
        report_lines.append("ERROR REPORT - TRADEMARK CERTIFICATE EXTRACTION")
        report_lines.append("=" * 80)
        report_lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report_lines.append("")

        # Summary
        summary = self.get_error_summary()
        report_lines.append("SUMMARY")
        report_lines.append("-" * 80)
        report_lines.append(f"Total Errors: {summary['total_errors']}")
        report_lines.append(f"Critical Errors: {summary['critical_errors']}")
        report_lines.append(f"Total Warnings: {summary['total_warnings']}")
        report_lines.append("")

        # Errors by category
        if summary['errors_by_category']:
            report_lines.append("Errors by Category:")
            for category, count in sorted(summary['errors_by_category'].items()):
                report_lines.append(f"  • {category}: {count}")
            report_lines.append("")

        # Detailed errors
        if self.errors:
            report_lines.append("DETAILED ERRORS")
            report_lines.append("-" * 80)
            for i, error in enumerate(self.errors, 1):
                report_lines.append(f"{i}. [{error.severity.value.upper()}] {error.category.value}")
                report_lines.append(f"   Time: {error.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
                report_lines.append(f"   Message: {error.message}")
                if error.context:
                    report_lines.append(f"   Context: {json.dumps(error.context, indent=6, ensure_ascii=False)}")
                report_lines.append("")

        # Warnings
        if self.warnings:
            report_lines.append("WARNINGS")
            report_lines.append("-" * 80)
            for i, warning in enumerate(self.warnings, 1):
                report_lines.append(f"{i}. {warning.message}")
                report_lines.append(f"   Time: {warning.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
                report_lines.append("")

        report_lines.append("=" * 80)

        report = "\n".join(report_lines)

        # Save to file if specified
        if output_file:
            output_file.write_text(report, encoding='utf-8')
            self.log_info(f"Error report saved to: {output_file}")

        return report

    def clear(self):
        """Clear all recorded errors and warnings"""
        self.errors.clear()
        self.warnings.clear()


# Global error handler instance
_global_handler: Optional[ErrorHandler] = None


def get_error_handler() -> ErrorHandler:
    """Get global error handler instance"""
    global _global_handler
    if _global_handler is None:
        _global_handler = ErrorHandler()
    return _global_handler


def set_error_handler(handler: ErrorHandler):
    """Set global error handler instance"""
    global _global_handler
    _global_handler = handler


if __name__ == "__main__":
    # Test error handler
    handler = ErrorHandler(verbose=True)

    # Test different error types
    handler.log_info("Starting test")
    handler.log_warning("This is a warning")

    try:
        raise ValueError("Test error")
    except Exception as e:
        handler.handle_error(e, category=ErrorCategory.VALIDATION,
                            severity=ErrorSeverity.ERROR,
                            context={'file': 'test.pdf'})

    handler.log_success("Test completed")

    # Generate report
    print("\n" + handler.generate_error_report())
