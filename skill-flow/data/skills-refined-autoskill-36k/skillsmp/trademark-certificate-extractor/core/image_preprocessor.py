#!/usr/bin/env python3
"""
Image Preprocessing Module

Enhances image quality before OCR to improve accuracy.
"""

import cv2
import numpy as np
from pathlib import Path
from typing import Optional, Tuple, List
from enum import Enum


class PreprocessingMode(Enum):
    """Image preprocessing modes"""
    AUTO = "auto"              # Automatic selection based on image analysis
    SCANNED = "scanned"        # Optimized for scanned documents
    PHOTO = "photo"            # Optimized for photos of documents
    LOW_QUALITY = "low_quality"  # Aggressive processing for poor quality images
    MINIMAL = "minimal"        # Minimal processing for high-quality images


class ImagePreprocessor:
    """
    Preprocesses images to optimize OCR accuracy
    """

    def __init__(self, mode: PreprocessingMode = PreprocessingMode.AUTO):
        """
        Initialize image preprocessor

        Args:
            mode: Preprocessing mode
        """
        self.mode = mode

    def preprocess(self, image_path: Path, output_path: Optional[Path] = None) -> np.ndarray:
        """
        Preprocess an image for OCR

        Args:
            image_path: Path to input image
            output_path: Optional path to save preprocessed image

        Returns:
            Preprocessed image as numpy array
        """
        # Load image
        img = cv2.imread(str(image_path))
        if img is None:
            raise ValueError(f"Failed to load image: {image_path}")

        # Determine preprocessing mode
        mode = self.mode
        if mode == PreprocessingMode.AUTO:
            mode = self._detect_preprocessing_mode(img)

        # Apply preprocessing pipeline
        processed = self._apply_preprocessing_pipeline(img, mode)

        # Save if output path specified
        if output_path:
            cv2.imwrite(str(output_path), processed)

        return processed

    def _detect_preprocessing_mode(self, img: np.ndarray) -> PreprocessingMode:
        """
        Automatically detect best preprocessing mode based on image analysis

        Args:
            img: Input image

        Returns:
            Recommended preprocessing mode
        """
        # Calculate image quality metrics
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) if len(img.shape) == 3 else img

        # 1. Check brightness
        mean_brightness = np.mean(gray)

        # 2. Check contrast
        contrast = np.std(gray)

        # 3. Check sharpness (using Laplacian variance)
        laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()

        # 4. Check noise level
        noise_level = self._estimate_noise(gray)

        # Decision logic
        if laplacian_var < 50:  # Very blurry
            return PreprocessingMode.LOW_QUALITY
        elif noise_level > 10:  # High noise
            return PreprocessingMode.LOW_QUALITY
        elif contrast < 30:  # Low contrast
            return PreprocessingMode.SCANNED
        elif mean_brightness < 100 or mean_brightness > 200:  # Poor lighting
            return PreprocessingMode.PHOTO
        else:
            return PreprocessingMode.MINIMAL

    def _estimate_noise(self, gray: np.ndarray) -> float:
        """Estimate noise level in image using median absolute deviation"""
        h, w = gray.shape
        # Sample center region
        center_h, center_w = h // 4, w // 4
        roi = gray[center_h:3*center_h, center_w:3*center_w]

        # Calculate noise estimate
        sigma = np.median(np.abs(roi - np.median(roi)))
        return sigma

    def _apply_preprocessing_pipeline(self, img: np.ndarray, mode: PreprocessingMode) -> np.ndarray:
        """
        Apply preprocessing pipeline based on mode

        Args:
            img: Input image
            mode: Preprocessing mode

        Returns:
            Preprocessed image
        """
        if mode == PreprocessingMode.MINIMAL:
            return self._minimal_preprocessing(img)
        elif mode == PreprocessingMode.SCANNED:
            return self._scanned_document_preprocessing(img)
        elif mode == PreprocessingMode.PHOTO:
            return self._photo_preprocessing(img)
        elif mode == PreprocessingMode.LOW_QUALITY:
            return self._aggressive_preprocessing(img)
        else:
            return img

    def _minimal_preprocessing(self, img: np.ndarray) -> np.ndarray:
        """Minimal preprocessing for high-quality images"""
        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) if len(img.shape) == 3 else img

        # Slight sharpening
        kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
        sharpened = cv2.filter2D(gray, -1, kernel)

        return sharpened

    def _scanned_document_preprocessing(self, img: np.ndarray) -> np.ndarray:
        """Preprocessing optimized for scanned documents"""
        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) if len(img.shape) == 3 else img

        # 1. Denoise
        denoised = cv2.fastNlMeansDenoising(gray, h=10)

        # 2. Increase contrast with CLAHE
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        contrasted = clahe.apply(denoised)

        # 3. Deskew
        deskewed = self._deskew(contrasted)

        # 4. Binarization with adaptive threshold
        binary = cv2.adaptiveThreshold(
            deskewed, 255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY,
            11, 2
        )

        return binary

    def _photo_preprocessing(self, img: np.ndarray) -> np.ndarray:
        """Preprocessing optimized for photos of documents"""
        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) if len(img.shape) == 3 else img

        # 1. Denoise
        denoised = cv2.fastNlMeansDenoising(gray, h=10)

        # 2. Auto-adjust brightness and contrast
        adjusted = self._auto_adjust_brightness_contrast(denoised)

        # 3. Deskew
        deskewed = self._deskew(adjusted)

        # 4. Sharpen
        kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
        sharpened = cv2.filter2D(deskewed, -1, kernel)

        # 5. Adaptive threshold
        binary = cv2.adaptiveThreshold(
            sharpened, 255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY,
            15, 5
        )

        return binary

    def _aggressive_preprocessing(self, img: np.ndarray) -> np.ndarray:
        """Aggressive preprocessing for low-quality images"""
        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) if len(img.shape) == 3 else img

        # 1. Upscale
        h, w = gray.shape
        upscaled = cv2.resize(gray, (w * 2, h * 2), interpolation=cv2.INTER_CUBIC)

        # 2. Strong denoising
        denoised = cv2.fastNlMeansDenoising(upscaled, h=15)

        # 3. Morphological operations to remove noise
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
        opened = cv2.morphologyEx(denoised, cv2.MORPH_OPEN, kernel)

        # 4. Strong contrast enhancement
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
        contrasted = clahe.apply(opened)

        # 5. Deskew
        deskewed = self._deskew(contrasted)

        # 6. Strong sharpening
        kernel = np.array([[-2,-2,-2], [-2,17,-2], [-2,-2,-2]])
        sharpened = cv2.filter2D(deskewed, -1, kernel)

        # 7. Otsu's binarization
        _, binary = cv2.threshold(sharpened, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        return binary

    def _deskew(self, img: np.ndarray) -> np.ndarray:
        """
        Deskew image by detecting and correcting rotation

        Args:
            img: Input grayscale image

        Returns:
            Deskewed image
        """
        # Calculate skew angle
        coords = np.column_stack(np.where(img > 0))
        if len(coords) == 0:
            return img

        angle = cv2.minAreaRect(coords)[-1]

        # Adjust angle
        if angle < -45:
            angle = 90 + angle
        elif angle > 45:
            angle = angle - 90

        # Only correct if angle is significant (> 0.5 degrees)
        if abs(angle) < 0.5:
            return img

        # Rotate image
        h, w = img.shape
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        rotated = cv2.warpAffine(
            img, M, (w, h),
            flags=cv2.INTER_CUBIC,
            borderMode=cv2.BORDER_REPLICATE
        )

        return rotated

    def _auto_adjust_brightness_contrast(self, img: np.ndarray,
                                         clip_hist_percent: float = 1.0) -> np.ndarray:
        """
        Automatically adjust brightness and contrast

        Args:
            img: Input grayscale image
            clip_hist_percent: Percentage of histogram to clip

        Returns:
            Adjusted image
        """
        # Calculate histogram
        hist = cv2.calcHist([img], [0], None, [256], [0, 256])
        hist_size = len(hist)

        # Calculate cumulative distribution
        accumulator = []
        accumulator.append(float(hist[0]))
        for i in range(1, hist_size):
            accumulator.append(accumulator[i - 1] + float(hist[i]))

        # Find clip limits
        maximum = accumulator[-1]
        clip_hist_percent *= (maximum / 100.0)
        clip_hist_percent /= 2.0

        # Find minimum gray level
        minimum_gray = 0
        while accumulator[minimum_gray] < clip_hist_percent:
            minimum_gray += 1

        # Find maximum gray level
        maximum_gray = hist_size - 1
        while accumulator[maximum_gray] >= (maximum - clip_hist_percent):
            maximum_gray -= 1

        # Calculate alpha and beta
        alpha = 255 / (maximum_gray - minimum_gray)
        beta = -minimum_gray * alpha

        # Apply linear transformation
        adjusted = cv2.convertScaleAbs(img, alpha=alpha, beta=beta)

        return adjusted

    def batch_preprocess(self, image_paths: List[Path],
                        output_dir: Optional[Path] = None) -> List[np.ndarray]:
        """
        Preprocess multiple images

        Args:
            image_paths: List of image paths
            output_dir: Optional directory to save preprocessed images

        Returns:
            List of preprocessed images
        """
        results = []

        for img_path in image_paths:
            if output_dir:
                output_path = output_dir / f"{img_path.stem}_preprocessed{img_path.suffix}"
            else:
                output_path = None

            processed = self.preprocess(img_path, output_path)
            results.append(processed)

        return results


if __name__ == "__main__":
    # Test preprocessor
    import sys

    if len(sys.argv) < 2:
        print("Usage: python image_preprocessor.py <image_path>")
        sys.exit(1)

    preprocessor = ImagePreprocessor(mode=PreprocessingMode.AUTO)
    img_path = Path(sys.argv[1])
    output_path = img_path.parent / f"{img_path.stem}_preprocessed{img_path.suffix}"

    print(f"Preprocessing: {img_path}")
    processed = preprocessor.preprocess(img_path, output_path)
    print(f"Saved to: {output_path}")
