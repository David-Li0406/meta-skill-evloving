"""
Trademark Certificate Extractor - Enhanced Core Module

This module provides enhanced functionality for extracting and processing
trademark certificate information with confidence scoring, error handling,
and advanced features.
"""

__version__ = "2.0.0"
__author__ = "Enhanced with Claude"

from .confidence import ConfidenceScorer
from .error_handler import ErrorHandler, ExtractionError
from .expiry_checker import ExpiryChecker
from .image_preprocessor import ImagePreprocessor
from .progress_tracker import ProgressTracker
from .template_matcher import TemplateMatcher
from .ocr_engine_selector import OCREngineSelector
from .export_manager import ExportManager
from .history_tracker import HistoryTracker
from .dashboard_generator import DashboardGenerator

__all__ = [
    'ConfidenceScorer',
    'ErrorHandler',
    'ExtractionError',
    'ExpiryChecker',
    'ImagePreprocessor',
    'ProgressTracker',
    'TemplateMatcher',
    'OCREngineSelector',
    'ExportManager',
    'HistoryTracker',
    'DashboardGenerator',
]
