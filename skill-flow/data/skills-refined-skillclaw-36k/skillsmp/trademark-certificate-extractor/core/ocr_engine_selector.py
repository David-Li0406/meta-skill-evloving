#!/usr/bin/env python3
"""
OCR Engine Selector Module

Intelligently selects and manages multiple OCR engines for optimal accuracy.
"""

import subprocess
import sys
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
from enum import Enum
import json


class OCREngine(Enum):
    """Available OCR engines"""
    TESSERACT = "tesseract"
    PADDLEOCR = "paddleocr"
    EASYOCR = "easyocr"
    GOOGLE_VISION = "google_vision"
    AZURE_VISION = "azure_vision"


class OCREngineSelector:
    """
    Manages multiple OCR engines and selects the best one based on
    image characteristics and availability
    """

    def __init__(self, preferred_engines: Optional[List[OCREngine]] = None):
        """
        Initialize OCR engine selector

        Args:
            preferred_engines: List of preferred engines in priority order
        """
        self.preferred_engines = preferred_engines or [
            OCREngine.PADDLEOCR,
            OCREngine.TESSERACT,
            OCREngine.EASYOCR,
        ]

        self.available_engines = self._detect_available_engines()
        self.engine_cache = {}

    def _detect_available_engines(self) -> Dict[OCREngine, bool]:
        """
        Detect which OCR engines are available on the system

        Returns:
            Dictionary mapping engine names to availability status
        """
        available = {}

        # Check Tesseract
        try:
            result = subprocess.run(['tesseract', '--version'],
                                  capture_output=True, text=True)
            available[OCREngine.TESSERACT] = result.returncode == 0
        except FileNotFoundError:
            available[OCREngine.TESSERACT] = False

        # Check PaddleOCR
        try:
            import paddleocr
            available[OCREngine.PADDLEOCR] = True
        except ImportError:
            available[OCREngine.PADDLEOCR] = False

        # Check EasyOCR
        try:
            import easyocr
            available[OCREngine.EASYOCR] = True
        except ImportError:
            available[OCREngine.EASYOCR] = False

        # Cloud services (check for API keys)
        available[OCREngine.GOOGLE_VISION] = self._check_google_vision_available()
        available[OCREngine.AZURE_VISION] = self._check_azure_vision_available()

        return available

    def _check_google_vision_available(self) -> bool:
        """Check if Google Vision API is available"""
        try:
            from google.cloud import vision
            import os
            return 'GOOGLE_APPLICATION_CREDENTIALS' in os.environ
        except ImportError:
            return False

    def _check_azure_vision_available(self) -> bool:
        """Check if Azure Vision API is available"""
        try:
            from azure.cognitiveservices.vision.computervision import ComputerVisionClient
            import os
            return 'AZURE_VISION_KEY' in os.environ and 'AZURE_VISION_ENDPOINT' in os.environ
        except ImportError:
            return False

    def select_engine(self, image_path: Path,
                     language: str = "chi_sim+eng",
                     quality_hint: Optional[str] = None) -> OCREngine:
        """
        Select the best OCR engine for the given image

        Args:
            image_path: Path to the image
            language: Language code(s) for OCR
            quality_hint: Hint about image quality ("high", "low", "medium")

        Returns:
            Selected OCR engine
        """
        # Check preferred engines in order
        for engine in self.preferred_engines:
            if self.available_engines.get(engine, False):
                # Special logic based on quality hint
                if quality_hint == "low":
                    # PaddleOCR and cloud services handle low quality better
                    if engine in [OCREngine.PADDLEOCR, OCREngine.GOOGLE_VISION,
                                OCREngine.AZURE_VISION]:
                        return engine
                elif quality_hint == "high":
                    # Tesseract is fast and accurate for high quality
                    if engine == OCREngine.TESSERACT:
                        return engine

                # Return first available engine
                return engine

        # Fallback to any available engine
        for engine, available in self.available_engines.items():
            if available:
                return engine

        raise RuntimeError("No OCR engine available")

    def extract_text(self, image_path: Path,
                     engine: Optional[OCREngine] = None,
                     language: str = "chi_sim+eng") -> Tuple[str, Dict[str, Any]]:
        """
        Extract text using specified or auto-selected engine

        Args:
            image_path: Path to the image
            engine: OCR engine to use (auto-select if None)
            language: Language code(s)

        Returns:
            Tuple of (extracted_text, metadata)
        """
        if engine is None:
            engine = self.select_engine(image_path, language)

        if not self.available_engines.get(engine, False):
            raise RuntimeError(f"OCR engine not available: {engine.value}")

        # Extract text using the selected engine
        if engine == OCREngine.TESSERACT:
            return self._extract_with_tesseract(image_path, language)
        elif engine == OCREngine.PADDLEOCR:
            return self._extract_with_paddleocr(image_path, language)
        elif engine == OCREngine.EASYOCR:
            return self._extract_with_easyocr(image_path, language)
        elif engine == OCREngine.GOOGLE_VISION:
            return self._extract_with_google_vision(image_path)
        elif engine == OCREngine.AZURE_VISION:
            return self._extract_with_azure_vision(image_path)
        else:
            raise ValueError(f"Unknown engine: {engine}")

    def _extract_with_tesseract(self, image_path: Path,
                               language: str) -> Tuple[str, Dict[str, Any]]:
        """Extract text using Tesseract OCR"""
        try:
            result = subprocess.run(
                ['tesseract', str(image_path), 'stdout', '-l', language],
                capture_output=True,
                text=True,
                check=True
            )

            metadata = {
                'engine': OCREngine.TESSERACT.value,
                'language': language,
                'confidence': None,  # Tesseract doesn't provide overall confidence easily
            }

            return (result.stdout, metadata)
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Tesseract OCR failed: {e}")

    def _extract_with_paddleocr(self, image_path: Path,
                               language: str) -> Tuple[str, Dict[str, Any]]:
        """Extract text using PaddleOCR"""
        try:
            from paddleocr import PaddleOCR

            # Initialize PaddleOCR
            lang_code = 'ch' if 'chi' in language else 'en'

            if OCREngine.PADDLEOCR not in self.engine_cache:
                self.engine_cache[OCREngine.PADDLEOCR] = PaddleOCR(
                    use_angle_cls=True,
                    lang=lang_code,
                    show_log=False
                )

            ocr = self.engine_cache[OCREngine.PADDLEOCR]

            # Run OCR
            result = ocr.ocr(str(image_path), cls=True)

            # Extract text and confidence
            lines = []
            confidences = []

            if result and result[0]:
                for line in result[0]:
                    if line:
                        text = line[1][0]
                        confidence = line[1][1]
                        lines.append(text)
                        confidences.append(confidence)

            avg_confidence = sum(confidences) / len(confidences) if confidences else 0.0

            metadata = {
                'engine': OCREngine.PADDLEOCR.value,
                'language': lang_code,
                'confidence': avg_confidence,
                'line_count': len(lines),
            }

            return ('\n'.join(lines), metadata)

        except Exception as e:
            raise RuntimeError(f"PaddleOCR failed: {e}")

    def _extract_with_easyocr(self, image_path: Path,
                             language: str) -> Tuple[str, Dict[str, Any]]:
        """Extract text using EasyOCR"""
        try:
            import easyocr

            # Map language codes
            lang_list = ['ch_sim', 'en'] if 'chi' in language else ['en']

            if OCREngine.EASYOCR not in self.engine_cache:
                self.engine_cache[OCREngine.EASYOCR] = easyocr.Reader(lang_list)

            reader = self.engine_cache[OCREngine.EASYOCR]

            # Run OCR
            result = reader.readtext(str(image_path))

            # Extract text and confidence
            lines = []
            confidences = []

            for detection in result:
                text = detection[1]
                confidence = detection[2]
                lines.append(text)
                confidences.append(confidence)

            avg_confidence = sum(confidences) / len(confidences) if confidences else 0.0

            metadata = {
                'engine': OCREngine.EASYOCR.value,
                'language': lang_list,
                'confidence': avg_confidence,
                'line_count': len(lines),
            }

            return ('\n'.join(lines), metadata)

        except Exception as e:
            raise RuntimeError(f"EasyOCR failed: {e}")

    def _extract_with_google_vision(self, image_path: Path) -> Tuple[str, Dict[str, Any]]:
        """Extract text using Google Cloud Vision API"""
        try:
            from google.cloud import vision

            client = vision.ImageAnnotatorClient()

            with open(image_path, 'rb') as image_file:
                content = image_file.read()

            image = vision.Image(content=content)
            response = client.text_detection(image=image)

            if response.error.message:
                raise RuntimeError(f"Google Vision API error: {response.error.message}")

            texts = response.text_annotations

            if texts:
                full_text = texts[0].description
                confidence = texts[0].confidence if hasattr(texts[0], 'confidence') else None
            else:
                full_text = ""
                confidence = 0.0

            metadata = {
                'engine': OCREngine.GOOGLE_VISION.value,
                'confidence': confidence,
            }

            return (full_text, metadata)

        except Exception as e:
            raise RuntimeError(f"Google Vision API failed: {e}")

    def _extract_with_azure_vision(self, image_path: Path) -> Tuple[str, Dict[str, Any]]:
        """Extract text using Azure Computer Vision API"""
        try:
            from azure.cognitiveservices.vision.computervision import ComputerVisionClient
            from msrest.authentication import CognitiveServicesCredentials
            import os
            import time

            subscription_key = os.environ['AZURE_VISION_KEY']
            endpoint = os.environ['AZURE_VISION_ENDPOINT']

            client = ComputerVisionClient(
                endpoint,
                CognitiveServicesCredentials(subscription_key)
            )

            with open(image_path, 'rb') as image_file:
                read_response = client.read_in_stream(image_file, raw=True)

            # Get operation location
            operation_location = read_response.headers["Operation-Location"]
            operation_id = operation_location.split("/")[-1]

            # Wait for result
            while True:
                result = client.get_read_result(operation_id)
                if result.status.lower() not in ['notstarted', 'running']:
                    break
                time.sleep(1)

            # Extract text
            lines = []
            if result.status.lower() == 'succeeded':
                for text_result in result.analyze_result.read_results:
                    for line in text_result.lines:
                        lines.append(line.text)

            metadata = {
                'engine': OCREngine.AZURE_VISION.value,
                'confidence': None,
            }

            return ('\n'.join(lines), metadata)

        except Exception as e:
            raise RuntimeError(f"Azure Vision API failed: {e}")

    def extract_with_voting(self, image_path: Path,
                           engines: Optional[List[OCREngine]] = None,
                           language: str = "chi_sim+eng") -> Tuple[str, Dict[str, Any]]:
        """
        Extract text using multiple engines and combine results via voting

        Args:
            image_path: Path to the image
            engines: List of engines to use (use all available if None)
            language: Language code(s)

        Returns:
            Tuple of (combined_text, metadata)
        """
        if engines is None:
            engines = [e for e, available in self.available_engines.items() if available]

        if len(engines) < 2:
            # Not enough engines for voting, use single engine
            engine = engines[0] if engines else self.select_engine(image_path, language)
            return self.extract_text(image_path, engine, language)

        # Extract with multiple engines
        results = []
        for engine in engines[:3]:  # Limit to 3 engines to avoid excessive API calls
            try:
                text, metadata = self.extract_text(image_path, engine, language)
                results.append({
                    'engine': engine,
                    'text': text,
                    'metadata': metadata,
                })
            except Exception as e:
                print(f"Warning: {engine.value} failed: {e}", file=sys.stderr)

        if not results:
            raise RuntimeError("All OCR engines failed")

        # Simple voting: use result with highest confidence
        best_result = max(results,
                         key=lambda r: r['metadata'].get('confidence', 0) or 0)

        combined_metadata = {
            'engines_used': [r['engine'].value for r in results],
            'selected_engine': best_result['engine'].value,
            'confidence': best_result['metadata'].get('confidence'),
            'voting_enabled': True,
        }

        return (best_result['text'], combined_metadata)

    def get_available_engines(self) -> List[OCREngine]:
        """Get list of available OCR engines"""
        return [engine for engine, available in self.available_engines.items() if available]

    def generate_engine_report(self) -> str:
        """Generate a report of available OCR engines"""
        report_lines = []
        report_lines.append("=" * 60)
        report_lines.append("OCR ENGINE AVAILABILITY REPORT")
        report_lines.append("=" * 60)
        report_lines.append("")

        for engine in OCREngine:
            available = self.available_engines.get(engine, False)
            status = "✓ Available" if available else "✗ Not Available"
            report_lines.append(f"{engine.value}: {status}")

        report_lines.append("")
        report_lines.append(f"Total available: {len(self.get_available_engines())}/{len(OCREngine)}")
        report_lines.append("=" * 60)

        return "\n".join(report_lines)


if __name__ == "__main__":
    # Test OCR engine selector
    selector = OCREngineSelector()

    print(selector.generate_engine_report())

    if len(sys.argv) > 1:
        img_path = Path(sys.argv[1])
        print(f"\nTesting OCR on: {img_path}")

        try:
            text, metadata = selector.extract_text(img_path)
            print(f"\nEngine used: {metadata['engine']}")
            print(f"Confidence: {metadata.get('confidence', 'N/A')}")
            print(f"\nExtracted text:\n{text[:500]}...")
        except Exception as e:
            print(f"Error: {e}")
