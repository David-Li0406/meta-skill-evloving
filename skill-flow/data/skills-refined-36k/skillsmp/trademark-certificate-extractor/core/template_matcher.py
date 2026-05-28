#!/usr/bin/env python3
"""
Template Matcher Module

Detects and matches trademark certificate templates for optimized extraction.
"""

import cv2
import numpy as np
from pathlib import Path
from typing import Dict, Any, Optional, List, Tuple
from enum import Enum
import json


class CertificateRegion(Enum):
    """Certificate regions for template matching"""
    HEADER = "header"
    LOGO_AREA = "logo_area"
    REGISTRATION_NUMBER = "registration_number"
    REGISTRANT = "registrant"
    CLASSIFICATION = "classification"
    VALIDITY_PERIOD = "validity_period"
    SEAL = "seal"


class TemplateType(Enum):
    """Known certificate template types"""
    CHINA_TRADEMARK_2019 = "china_trademark_2019"
    CHINA_TRADEMARK_2014 = "china_trademark_2014"
    CHINA_TRADEMARK_PRE2014 = "china_trademark_pre2014"
    US_TRADEMARK = "us_trademark"
    EU_TRADEMARK = "eu_trademark"
    UNKNOWN = "unknown"


class TemplateMatcher:
    """
    Matches trademark certificates against known templates to optimize extraction
    """

    def __init__(self, templates_dir: Optional[Path] = None):
        """
        Initialize template matcher

        Args:
            templates_dir: Directory containing template definitions
        """
        self.templates_dir = templates_dir or Path(__file__).parent / "templates"
        self.templates = self._load_templates()

    def _load_templates(self) -> Dict[str, Any]:
        """
        Load template definitions

        Returns:
            Dictionary of template configurations
        """
        # Define standard Chinese trademark certificate templates
        templates = {
            TemplateType.CHINA_TRADEMARK_2019.value: {
                'name': '中国商标注册证（2019年后）',
                'identifier_text': ['中华人民共和国国家知识产权局', '商标注册证'],
                'regions': {
                    CertificateRegion.HEADER.value: {
                        'y_start': 0.0,
                        'y_end': 0.15,
                        'x_start': 0.0,
                        'x_end': 1.0,
                    },
                    CertificateRegion.LOGO_AREA.value: {
                        'y_start': 0.20,
                        'y_end': 0.45,
                        'x_start': 0.15,
                        'x_end': 0.85,
                    },
                    CertificateRegion.REGISTRATION_NUMBER.value: {
                        'y_start': 0.05,
                        'y_end': 0.12,
                        'x_start': 0.70,
                        'x_end': 1.0,
                    },
                    CertificateRegion.REGISTRANT.value: {
                        'y_start': 0.50,
                        'y_end': 0.65,
                        'x_start': 0.20,
                        'x_end': 0.85,
                    },
                    CertificateRegion.CLASSIFICATION.value: {
                        'y_start': 0.48,
                        'y_end': 0.55,
                        'x_start': 0.20,
                        'x_end': 0.50,
                    },
                    CertificateRegion.VALIDITY_PERIOD.value: {
                        'y_start': 0.68,
                        'y_end': 0.75,
                        'x_start': 0.20,
                        'x_end': 0.85,
                    },
                    CertificateRegion.SEAL.value: {
                        'y_start': 0.75,
                        'y_end': 0.95,
                        'x_start': 0.60,
                        'x_end': 0.95,
                    },
                },
                'field_labels': {
                    '注册号': ['第', '号'],
                    '注册人': ['注册人名义', '商标注册人'],
                    '国际分类': ['国际分类', '类别'],
                    '有效期限': ['有效期限', '专用权期限'],
                }
            },
            TemplateType.CHINA_TRADEMARK_2014.value: {
                'name': '中国商标注册证（2014-2019）',
                'identifier_text': ['中华人民共和国国家工商行政管理总局', '商标注册证'],
                'regions': {
                    CertificateRegion.LOGO_AREA.value: {
                        'y_start': 0.22,
                        'y_end': 0.45,
                        'x_start': 0.15,
                        'x_end': 0.85,
                    },
                    CertificateRegion.REGISTRATION_NUMBER.value: {
                        'y_start': 0.05,
                        'y_end': 0.12,
                        'x_start': 0.65,
                        'x_end': 1.0,
                    },
                },
                'field_labels': {
                    '注册号': ['第', '号'],
                    '注册人': ['注册人名义'],
                    '国际分类': ['国际分类'],
                    '有效期限': ['有效期限'],
                }
            },
            TemplateType.CHINA_TRADEMARK_PRE2014.value: {
                'name': '中国商标注册证（2014年前）',
                'identifier_text': ['中华人民共和国国家工商行政管理总局商标局', '商标注册证'],
                'regions': {
                    CertificateRegion.LOGO_AREA.value: {
                        'y_start': 0.25,
                        'y_end': 0.50,
                        'x_start': 0.20,
                        'x_end': 0.80,
                    },
                },
                'field_labels': {
                    '注册号': ['注册号'],
                    '注册人': ['注册人'],
                    '国际分类': ['类别'],
                    '有效期限': ['有效期限'],
                }
            },
        }

        return templates

    def detect_template(self, image_path: Path, ocr_text: Optional[str] = None) -> Tuple[TemplateType, float]:
        """
        Detect which template matches the certificate

        Args:
            image_path: Path to certificate image
            ocr_text: Optional OCR text from the certificate

        Returns:
            Tuple of (template_type, confidence_score)
        """
        img = cv2.imread(str(image_path))
        if img is None:
            return (TemplateType.UNKNOWN, 0.0)

        best_match = TemplateType.UNKNOWN
        best_score = 0.0

        # Try text-based matching first if OCR text available
        if ocr_text:
            for template_type, template_config in self.templates.items():
                score = self._match_by_text(ocr_text, template_config)
                if score > best_score:
                    best_score = score
                    best_match = TemplateType(template_type)

        # If no confident match, try image-based matching
        if best_score < 0.7:
            for template_type, template_config in self.templates.items():
                score = self._match_by_image(img, template_config)
                if score > best_score:
                    best_score = score
                    best_match = TemplateType(template_type)

        return (best_match, best_score)

    def _match_by_text(self, ocr_text: str, template_config: Dict) -> float:
        """
        Match template by searching for identifier text

        Args:
            ocr_text: OCR text from certificate
            template_config: Template configuration

        Returns:
            Confidence score (0-1)
        """
        identifier_texts = template_config.get('identifier_text', [])

        matches = 0
        for identifier in identifier_texts:
            if identifier in ocr_text:
                matches += 1

        score = matches / len(identifier_texts) if identifier_texts else 0.0
        return score

    def _match_by_image(self, img: np.ndarray, template_config: Dict) -> float:
        """
        Match template by analyzing image structure

        Args:
            img: Certificate image
            template_config: Template configuration

        Returns:
            Confidence score (0-1)
        """
        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) if len(img.shape) == 3 else img
        h, w = gray.shape

        # Check for expected regions
        regions = template_config.get('regions', {})
        if not regions:
            return 0.0

        # Simple heuristic: check if key regions have content
        score = 0.0
        total_regions = 0

        for region_name, region_coords in regions.items():
            y_start = int(h * region_coords['y_start'])
            y_end = int(h * region_coords['y_end'])
            x_start = int(w * region_coords['x_start'])
            x_end = int(w * region_coords['x_end'])

            roi = gray[y_start:y_end, x_start:x_end]

            # Check if region has content (not mostly white/empty)
            mean_intensity = np.mean(roi)
            if 50 < mean_intensity < 200:  # Has some content
                score += 1.0

            total_regions += 1

        return score / total_regions if total_regions > 0 else 0.0

    def get_extraction_regions(self, template_type: TemplateType,
                               image_shape: Tuple[int, int]) -> Dict[str, Dict[str, int]]:
        """
        Get pixel coordinates for extraction regions based on template

        Args:
            template_type: Detected template type
            image_shape: (height, width) of the image

        Returns:
            Dictionary mapping region names to pixel coordinates
        """
        h, w = image_shape

        template_config = self.templates.get(template_type.value, {})
        regions = template_config.get('regions', {})

        pixel_regions = {}
        for region_name, region_coords in regions.items():
            pixel_regions[region_name] = {
                'y_start': int(h * region_coords['y_start']),
                'y_end': int(h * region_coords['y_end']),
                'x_start': int(w * region_coords['x_start']),
                'x_end': int(w * region_coords['x_end']),
            }

        return pixel_regions

    def get_field_labels(self, template_type: TemplateType) -> Dict[str, List[str]]:
        """
        Get field label variations for the template

        Args:
            template_type: Template type

        Returns:
            Dictionary mapping field names to possible label texts
        """
        template_config = self.templates.get(template_type.value, {})
        return template_config.get('field_labels', {})

    def extract_region(self, image_path: Path, region: CertificateRegion,
                      template_type: TemplateType) -> Optional[np.ndarray]:
        """
        Extract a specific region from the certificate

        Args:
            image_path: Path to certificate image
            region: Region to extract
            template_type: Detected template type

        Returns:
            Extracted region as numpy array or None
        """
        img = cv2.imread(str(image_path))
        if img is None:
            return None

        h, w = img.shape[:2]
        regions = self.get_extraction_regions(template_type, (h, w))

        if region.value not in regions:
            return None

        coords = regions[region.value]
        extracted = img[coords['y_start']:coords['y_end'],
                       coords['x_start']:coords['x_end']]

        return extracted

    def generate_template_report(self, image_path: Path,
                                ocr_text: Optional[str] = None) -> str:
        """
        Generate a template detection report

        Args:
            image_path: Path to certificate image
            ocr_text: Optional OCR text

        Returns:
            Formatted report string
        """
        template_type, confidence = self.detect_template(image_path, ocr_text)

        report_lines = []
        report_lines.append("=" * 60)
        report_lines.append("TEMPLATE DETECTION REPORT")
        report_lines.append("=" * 60)
        report_lines.append(f"Image: {image_path.name}")
        report_lines.append("")

        if template_type == TemplateType.UNKNOWN:
            report_lines.append("❌ No matching template detected")
            report_lines.append(f"Confidence: {confidence:.2%}")
        else:
            template_config = self.templates.get(template_type.value, {})
            report_lines.append(f"✓ Detected: {template_config.get('name', template_type.value)}")
            report_lines.append(f"Confidence: {confidence:.2%}")
            report_lines.append("")

            report_lines.append("Extraction Regions:")
            img = cv2.imread(str(image_path))
            if img is not None:
                regions = self.get_extraction_regions(template_type, img.shape[:2])
                for region_name, coords in regions.items():
                    report_lines.append(f"  • {region_name}:")
                    report_lines.append(f"    Y: {coords['y_start']}-{coords['y_end']}")
                    report_lines.append(f"    X: {coords['x_start']}-{coords['x_end']}")

        report_lines.append("=" * 60)
        return "\n".join(report_lines)


if __name__ == "__main__":
    # Test template matcher
    import sys

    if len(sys.argv) < 2:
        print("Usage: python template_matcher.py <certificate_image>")
        sys.exit(1)

    matcher = TemplateMatcher()
    img_path = Path(sys.argv[1])

    print(matcher.generate_template_report(img_path))
