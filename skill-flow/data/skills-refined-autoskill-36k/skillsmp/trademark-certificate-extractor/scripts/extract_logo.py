#!/usr/bin/env python3
"""
Trademark logo extraction script

Extracts the trademark logo image from trademark registration certificates.
Supports both PDF and image formats.
Uses OpenCV for intelligent logo detection.
"""

import sys
import tempfile
from pathlib import Path
from typing import Tuple, Optional

try:
    import cv2
    import numpy as np
    from PIL import Image
except ImportError:
    print("Required libraries not installed. Please install: pip install opencv-python numpy Pillow", file=sys.stderr)
    sys.exit(1)


def extract_logo_from_image(image_path: Path, output_path: Path) -> bool:
    """
    Extract trademark logo from an image file using OpenCV detection

    Args:
        image_path: Path to the certificate image file
        output_path: Path to save the extracted logo

    Returns:
        True if successful, False otherwise
    """
    try:
        # 1. Load image with OpenCV
        img = cv2.imread(str(image_path))
        if img is None:
            print(f"Error: Could not read image {image_path}", file=sys.stderr)
            return False

        h_img, w_img = img.shape[:2]

        # 2. Preprocessing
        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Adaptive Thresholding (better for scanned docs with uneven lighting)
        binary = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                     cv2.THRESH_BINARY_INV, 25, 10)

        # Mask out borders to remove scanning artifacts or page borders
        margin_h = int(h_img * 0.05)
        margin_w = int(w_img * 0.05)
        binary[0:margin_h, :] = 0  # Top
        binary[h_img-margin_h:h_img, :] = 0  # Bottom
        binary[:, 0:margin_w] = 0  # Left
        binary[:, w_img-margin_w:w_img] = 0  # Right

        # 3. Morphological operations
        # Dilate to merge nearby text/graphics into single blocks
        # Use asymmetric kernel to favor horizontal merging (for text logos like PREGENE)
        kernel = np.ones((5, 20), np.uint8) 
        dilated = cv2.dilate(binary, kernel, iterations=2)

        # 4. Find contours
        # Use RETR_LIST to find all contours including nested ones
        contours, _ = cv2.findContours(dilated, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

        candidates = []
        
        # Define search region (typical trademark certificate layout)
        # Logo is usually below the header (emblem/title) and above the details
        # Typically in Y range [20%, 45%] - Moved start to 20% to avoid emblem (国徽)
        search_min_y = int(h_img * 0.20)
        search_max_y = int(h_img * 0.45)
        search_min_x = int(w_img * 0.10) # Start from 10%
        search_max_x = int(w_img * 0.90) # End at 90% to cover centered logos

        center_x = w_img // 2

        for cnt in contours:
            x, y, w, h = cv2.boundingRect(cnt)
            area = w * h
            
            # Filter candidates based on position and size
            if (search_min_x < x < search_max_x and
                search_min_y < y < search_max_y):
                
                # Size constraints:
                # Must be significant enough (>0.2% of page area)
                # Must not be too wide (like a full text line) -> w < 80% page width
                # Aspect ratio shouldn't be extreme (allow wider for text logos)
                aspect_ratio = w / float(h)
                
                if (area > (w_img * h_img * 0.002) and 
                    w < w_img * 0.8 and
                    0.2 < aspect_ratio < 8.0):
                    
                    # Score candidates
                    # Base score is area
                    score = area
                    
                    # Bonus for being horizontally centered
                    cnt_center_x = x + w // 2
                    dist_from_center = abs(cnt_center_x - center_x)
                    
                    # If within 15% of center, give a huge boost
                    if dist_from_center < (w_img * 0.15):
                        score *= 2.0
                    
                    candidates.append((x, y, w, h, score))

        # 5. Select best candidate
        if candidates:
            # Sort by score (descending)
            candidates.sort(key=lambda c: c[4], reverse=True)
            
            x, y, w, h, _ = candidates[0]
            
            # Add padding
            pad = 20
            x_crop = max(0, x - pad)
            y_crop = max(0, y - pad)
            w_crop = min(w_img - x_crop, w + 2*pad)
            h_crop = min(h_img - y_crop, h + 2*pad)
            
            # Crop
            logo_crop = img[y_crop:y_crop+h_crop, x_crop:x_crop+w_crop]
            
            # Save
            cv2.imwrite(str(output_path), logo_crop)
            print(f"Logo detected and extracted to: {output_path}")
            return True
            
        else:
            print("No logo candidate detected via OpenCV. Falling back to fixed crop.", file=sys.stderr)
            return fallback_crop(img, output_path)

    except Exception as e:
        print(f"Error extracting logo from {image_path}: {e}", file=sys.stderr)
        # Fallback in case of error
        try:
             return fallback_crop(cv2.imread(str(image_path)), output_path)
        except:
             return False

def fallback_crop(img, output_path: Path) -> bool:
    """Fallback method using hardcoded coordinates"""
    if img is None:
        return False
        
    h, w = img.shape[:2]
    
    # Default logo area - CENTERED & LOWERED
    logo_top = int(h * 0.20)  # Start lower to avoid emblem
    logo_left = int(w * 0.20)  # Start from 20%
    logo_right = int(w * 0.80) # End at 80% (Center focus)
    logo_bottom = int(h * 0.40) 
    
    crop = img[logo_top:logo_bottom, logo_left:logo_right]
    cv2.imwrite(str(output_path), crop)
    print(f"Logo extracted using fallback crop: {output_path}")
    return True



def extract_logo_from_pdf(pdf_path: Path, output_path: Path) -> bool:
    """
    Extract trademark logo from a PDF file

    Converts the first page of the PDF to an image, then extracts the logo.

    Args:
        pdf_path: Path to the PDF certificate file
        output_path: Path to save the extracted logo

    Returns:
        True if successful, False otherwise
    """
    try:
        # Import pdf2image
        from pdf2image import convert_from_path

        # Convert first page to image
        images = convert_from_path(str(pdf_path), dpi=300, first_page=1, last_page=1)

        if not images:
            print("Error: Could not convert PDF to image", file=sys.stderr)
            return False

        # Save first page as temporary image
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
            temp_path = Path(tmp.name)
            images[0].save(temp_path, 'PNG')

        # Extract logo from the image
        success = extract_logo_from_image(temp_path, output_path)

        # Clean up temp file
        temp_path.unlink()

        return success

    except ImportError:
        print("pdf2image not installed. Install with: pip install pdf2image", file=sys.stderr)
        return False
    except Exception as e:
        print(f"Error processing PDF {pdf_path}: {e}", file=sys.stderr)
        return False


def extract_logo(file_path: Path, output_path: Path = None) -> Path:
    """
    Extract trademark logo from a certificate file (PDF or image)

    Args:
        file_path: Path to the certificate file
        output_path: Optional path to save the logo (defaults to same directory as input)

    Returns:
        Path to the extracted logo file, or None if extraction failed
    """
    if not file_path.exists():
        print(f"File not found: {file_path}", file=sys.stderr)
        return None

    # Generate output path if not provided
    if output_path is None:
        output_path = file_path.parent / f"{file_path.stem}_logo.png"

    # Extract based on file type
    suffix = file_path.suffix.lower()

    if suffix == '.pdf':
        success = extract_logo_from_pdf(file_path, output_path)
    elif suffix in ['.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.tif']:
        success = extract_logo_from_image(file_path, output_path)
    else:
        print(f"Unsupported file type: {suffix}", file=sys.stderr)
        return None

    return output_path if success else None


def main():
    """Command-line interface for the logo extraction script"""
    if len(sys.argv) < 2:
        print("Usage: python extract_logo.py <file_path> [output_path]")
        print("Example: python extract_logo.py certificate.pdf")
        print("Example: python extract_logo.py certificate.png logo.png")
        sys.exit(1)

    file_path = Path(sys.argv[1])
    output_path = Path(sys.argv[2]) if len(sys.argv) > 2 else None

    result = extract_logo(file_path, output_path)

    if result:
        print(f"Successfully extracted logo to: {result}")
    else:
        print("Failed to extract logo", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
