#!/usr/bin/env python3
"""
Confidence Scoring System

Provides confidence scores for extracted fields and flags for manual review.
"""

import re
from typing import Dict, Any, Tuple, Optional
from datetime import datetime
from enum import Enum


class ConfidenceLevel(Enum):
    """Confidence level enumeration"""
    HIGH = "high"          # >= 0.8
    MEDIUM = "medium"      # >= 0.5
    LOW = "low"            # < 0.5
    REQUIRES_REVIEW = "requires_review"  # < 0.3


class FieldType(Enum):
    """Field type enumeration for different validation rules"""
    REGISTRATION_NUMBER = "registration_number"
    REGISTRANT = "registrant"
    VALIDITY_PERIOD = "validity_period"
    CLASSIFICATION = "classification"
    SERIAL_NUMBER = "serial_number"
    GENERIC = "generic"


class ConfidenceScorer:
    """
    Analyzes extracted trademark data and assigns confidence scores
    to each field based on validation rules and pattern matching.
    """

    # Confidence thresholds
    THRESHOLD_HIGH = 0.8
    THRESHOLD_MEDIUM = 0.5
    THRESHOLD_REVIEW = 0.3

    # Pattern definitions for Chinese trademark certificates
    PATTERNS = {
        'registration_number': [
            r'^\d{7,10}$',  # Standard format: 7-10 digits
            r'^[A-Z]?\d{7,10}[A-Z]?$',  # With letter prefix/suffix
        ],
        'classification': [
            r'^[1-9]|[1-3]\d|4[0-5]$',  # International classification 1-45
            r'^第[一二三四五六七八九十\d]+类$',  # Chinese format
        ],
        'validity_period': [
            r'\d{4}[-/年]\d{1,2}[-/月]\d{1,2}日?',  # Date format
            r'\d{4}\.\d{1,2}\.\d{1,2}',  # Dot separated
        ],
        'registrant': [
            r'.{2,100}',  # 2-100 characters (company/person name)
        ],
    }

    def __init__(self, strict_mode: bool = False):
        """
        Initialize confidence scorer

        Args:
            strict_mode: If True, applies stricter validation rules
        """
        self.strict_mode = strict_mode
        self.validation_rules = self._initialize_validation_rules()

    def _initialize_validation_rules(self) -> Dict[str, Any]:
        """Initialize field validation rules"""
        return {
            'registration_number': {
                'required': True,
                'min_length': 7,
                'max_length': 15,
                'patterns': self.PATTERNS['registration_number'],
            },
            'registrant': {
                'required': True,
                'min_length': 2,
                'max_length': 100,
                'patterns': self.PATTERNS['registrant'],
            },
            'classification': {
                'required': True,
                'min_length': 1,
                'max_length': 10,
                'patterns': self.PATTERNS['classification'],
            },
            'validity_period': {
                'required': True,
                'min_length': 8,
                'max_length': 30,
                'patterns': self.PATTERNS['validity_period'],
            },
        }

    def score_field(self, field_name: str, value: str, ocr_confidence: Optional[float] = None) -> Tuple[float, str]:
        """
        Calculate confidence score for a single field

        Args:
            field_name: Name of the field (e.g., 'registration_number')
            value: Extracted value
            ocr_confidence: OCR engine confidence score (0-1)

        Returns:
            Tuple of (confidence_score, reason)
        """
        if not value or value.strip() == '':
            return (0.0, "Empty value")

        score = 0.0
        reasons = []

        # Base score from OCR confidence
        if ocr_confidence is not None:
            score += ocr_confidence * 0.3  # 30% weight
            reasons.append(f"OCR: {ocr_confidence:.2f}")
        else:
            score += 0.15  # Default base score

        # Get validation rules for this field
        rules = self.validation_rules.get(field_name, {})

        # Length validation (20% weight)
        min_len = rules.get('min_length', 0)
        max_len = rules.get('max_length', 1000)
        value_len = len(value.strip())

        if min_len <= value_len <= max_len:
            score += 0.2
            reasons.append("Length OK")
        else:
            reasons.append(f"Length issue: {value_len} (expected {min_len}-{max_len})")

        # Pattern matching (50% weight)
        patterns = rules.get('patterns', [])
        pattern_matched = False

        for pattern in patterns:
            if re.search(pattern, value.strip()):
                score += 0.5
                pattern_matched = True
                reasons.append("Pattern matched")
                break

        if not pattern_matched and patterns:
            reasons.append("No pattern match")

        # Field-specific validation
        if field_name == 'validity_period':
            date_score, date_reason = self._validate_date(value)
            score += date_score * 0.2  # Additional 20% for valid date
            reasons.append(date_reason)

        elif field_name == 'registration_number':
            # Check for common OCR errors (O vs 0, I vs 1, etc.)
            if self._has_common_ocr_errors(value):
                score *= 0.8
                reasons.append("Potential OCR confusion")

        # Normalize score to [0, 1]
        score = min(1.0, max(0.0, score))

        return (score, "; ".join(reasons))

    def _validate_date(self, date_str: str) -> Tuple[float, str]:
        """
        Validate date format and reasonableness

        Returns:
            Tuple of (score, reason)
        """
        date_formats = [
            '%Y-%m-%d',
            '%Y/%m/%d',
            '%Y.%m.%d',
            '%Y年%m月%d日',
        ]

        for fmt in date_formats:
            try:
                # Remove '日' if present
                clean_date = date_str.replace('日', '')
                parsed_date = datetime.strptime(clean_date, fmt)

                # Check if date is reasonable (between 1950 and 2100)
                if 1950 <= parsed_date.year <= 2100:
                    return (1.0, "Valid date")
                else:
                    return (0.3, f"Date out of range: {parsed_date.year}")
            except (ValueError, TypeError):
                continue

        return (0.0, "Invalid date format")

    def _has_common_ocr_errors(self, text: str) -> bool:
        """Check if text contains characters commonly confused in OCR"""
        # Characters that look similar
        confusing_pairs = [
            ('O', '0'), ('I', '1'), ('l', '1'), ('S', '5'),
            ('Z', '2'), ('B', '8'), ('G', '6'), ('Q', '0')
        ]

        for char1, char2 in confusing_pairs:
            if char1 in text or char2 in text:
                return True
        return False

    def score_extraction(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Score all fields in an extraction result

        Args:
            data: Dictionary with extracted fields

        Returns:
            Enhanced dictionary with confidence scores and flags
        """
        scored_data = data.copy()
        scores = {}
        requires_review = []
        overall_scores = []

        # Score each field
        field_mapping = {
            '注册号': 'registration_number',
            '注册人': 'registrant',
            '国际分类': 'classification',
            '有效期限': 'validity_period',
        }

        for chinese_name, english_name in field_mapping.items():
            value = data.get(chinese_name, '')
            ocr_confidence = data.get(f'{chinese_name}_ocr_confidence')

            score, reason = self.score_field(english_name, value, ocr_confidence)
            scores[chinese_name] = {
                'score': score,
                'reason': reason,
                'level': self._get_confidence_level(score).value,
            }

            overall_scores.append(score)

            # Flag for review if confidence is low
            if score < self.THRESHOLD_REVIEW:
                requires_review.append({
                    'field': chinese_name,
                    'value': value,
                    'score': score,
                    'reason': reason,
                })

        # Calculate overall confidence
        overall_confidence = sum(overall_scores) / len(overall_scores) if overall_scores else 0.0

        # Add confidence metadata
        scored_data['confidence_scores'] = scores
        scored_data['overall_confidence'] = overall_confidence
        scored_data['requires_manual_review'] = len(requires_review) > 0
        scored_data['review_flags'] = requires_review
        scored_data['confidence_level'] = self._get_confidence_level(overall_confidence).value

        return scored_data

    def _get_confidence_level(self, score: float) -> ConfidenceLevel:
        """Convert numeric score to confidence level"""
        if score >= self.THRESHOLD_HIGH:
            return ConfidenceLevel.HIGH
        elif score >= self.THRESHOLD_MEDIUM:
            return ConfidenceLevel.MEDIUM
        elif score >= self.THRESHOLD_REVIEW:
            return ConfidenceLevel.LOW
        else:
            return ConfidenceLevel.REQUIRES_REVIEW

    def generate_review_report(self, scored_data: Dict[str, Any]) -> str:
        """
        Generate a human-readable review report

        Args:
            scored_data: Data with confidence scores

        Returns:
            Formatted report string
        """
        report_lines = []
        report_lines.append("=" * 60)
        report_lines.append("CONFIDENCE REVIEW REPORT")
        report_lines.append("=" * 60)
        report_lines.append("")

        # Overall summary
        overall = scored_data.get('overall_confidence', 0)
        level = scored_data.get('confidence_level', 'unknown')
        report_lines.append(f"Overall Confidence: {overall:.2%} ({level.upper()})")
        report_lines.append(f"Manual Review Required: {'YES' if scored_data.get('requires_manual_review') else 'NO'}")
        report_lines.append("")

        # Field details
        report_lines.append("Field Confidence Scores:")
        report_lines.append("-" * 60)

        for field, info in scored_data.get('confidence_scores', {}).items():
            score = info['score']
            level = info['level']
            reason = info['reason']

            status_icon = "✓" if score >= self.THRESHOLD_HIGH else "⚠" if score >= self.THRESHOLD_MEDIUM else "✗"
            report_lines.append(f"{status_icon} {field}: {score:.2%} ({level})")
            report_lines.append(f"  Reason: {reason}")
            report_lines.append("")

        # Review flags
        if scored_data.get('review_flags'):
            report_lines.append("FIELDS REQUIRING REVIEW:")
            report_lines.append("-" * 60)
            for flag in scored_data['review_flags']:
                report_lines.append(f"• {flag['field']}: {flag['value']}")
                report_lines.append(f"  Score: {flag['score']:.2%}")
                report_lines.append(f"  Reason: {flag['reason']}")
                report_lines.append("")

        report_lines.append("=" * 60)

        return "\n".join(report_lines)


if __name__ == "__main__":
    # Test the confidence scorer
    scorer = ConfidenceScorer()

    test_data = {
        '注册号': '12345678',
        '注册人': '阿里巴巴集团控股有限公司',
        '国际分类': '35',
        '有效期限': '2025-12-31',
    }

    result = scorer.score_extraction(test_data)
    print(scorer.generate_review_report(result))
