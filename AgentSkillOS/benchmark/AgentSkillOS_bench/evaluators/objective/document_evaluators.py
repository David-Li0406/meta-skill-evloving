"""
Document format evaluators for PPTX, DOCX, PDF files.
"""
from pathlib import Path
from typing import Dict, Any, Tuple, List
import re

from ...registry import evaluator
from ...utils.file_utils import resolve_path, extract_docx_text, extract_pptx_text


@evaluator("pptx_slide_count")
async def eval_pptx_slide_count(workspace: Path, op_args: Dict[str, Any],
                                value: Any = None, **kwargs) -> Tuple[bool, str]:
    """
    Check the number of slides in a PPTX file.

    op_args:
        path: Path to PPTX file
        operator: Comparison operator ("==", ">=", "<=", ">", "<") default: ">="
        expected: Expected slide count
    """
    try:
        from pptx import Presentation
    except ImportError:
        return False, "python-pptx package not installed"

    path = op_args["path"]
    operator = op_args.get("operator", ">=")
    expected = op_args["expected"]

    full_path = resolve_path(workspace, path)
    if full_path is None:
        return False, f"File not found: {path}"

    try:
        prs = Presentation(str(full_path))
        actual = len(prs.slides)
    except Exception as e:
        return False, f"Failed to read PPTX: {e}"

    if operator in ("==", "eq"):
        passed = actual == expected
    elif operator in (">=", "gte"):
        passed = actual >= expected
    elif operator in ("<=", "lte"):
        passed = actual <= expected
    elif operator in (">", "gt"):
        passed = actual > expected
    elif operator in ("<", "lt"):
        passed = actual < expected
    else:
        return False, f"Unknown operator: {operator}"

    if passed:
        return True, ""
    return False, f"PPTX has {actual} slides, expected {operator} {expected}"


@evaluator("pptx_content_check")
async def eval_pptx_content_check(workspace: Path, op_args: Dict[str, Any],
                                  value: Any = None, **kwargs) -> Tuple[bool, str]:
    """
    Check if PPTX contains specific text content.

    op_args:
        path: Path to PPTX file
        mode: "contains" | "regex" (default: inferred from value type)

    value:
        For "contains" mode: List of strings that must all be present
        For "regex" mode: Regex pattern string
    """
    path = op_args["path"]
    mode = op_args.get("mode")

    if mode is None:
        mode = "contains" if isinstance(value, list) else "regex"

    full_path = resolve_path(workspace, path)
    if full_path is None:
        return False, f"File not found: {path}"

    content = extract_pptx_text(full_path)
    if content is None:
        return False, f"Failed to read PPTX: {path}"

    if mode == "contains":
        if not isinstance(value, list):
            value = [value]
        missing = [s for s in value if s.lower() not in content.lower()]
        if not missing:
            return True, ""
        return False, f"Missing content in PPTX: {missing[:3]}"

    elif mode == "regex":
        pattern = value
        if re.search(pattern, content, re.IGNORECASE):
            return True, ""
        return False, f"Pattern '{pattern}' not found in PPTX"

    return False, f"Unknown mode: {mode}"


@evaluator("docx_heading_count")
async def eval_docx_heading_count(workspace: Path, op_args: Dict[str, Any],
                                  value: Any = None, **kwargs) -> Tuple[bool, str]:
    """
    Count headings in a DOCX file.

    op_args:
        path: Path to DOCX file
        heading_level: Optional specific level (1, 2, 3) or None for all headings
        operator: Comparison operator ("==", ">=", "<=", ">", "<") default: ">="
        expected: Expected heading count
    """
    try:
        from docx import Document
    except ImportError:
        return False, "python-docx package not installed"

    path = op_args["path"]
    heading_level = op_args.get("heading_level")
    operator = op_args.get("operator", ">=")
    expected = op_args["expected"]

    full_path = resolve_path(workspace, path)
    if full_path is None:
        return False, f"File not found: {path}"

    try:
        doc = Document(str(full_path))
        count = 0
        for para in doc.paragraphs:
            style_name = (para.style.name if para.style else "").lower()
            if "heading" in style_name:
                if heading_level is None:
                    count += 1
                elif f"heading {heading_level}" in style_name:
                    count += 1
    except Exception as e:
        return False, f"Failed to read DOCX: {e}"

    if operator in ("==", "eq"):
        passed = count == expected
    elif operator in (">=", "gte"):
        passed = count >= expected
    elif operator in ("<=", "lte"):
        passed = count <= expected
    elif operator in (">", "gt"):
        passed = count > expected
    elif operator in ("<", "lt"):
        passed = count < expected
    else:
        return False, f"Unknown operator: {operator}"

    level_str = f" (level {heading_level})" if heading_level else ""
    if passed:
        return True, ""
    return False, f"DOCX has {count} headings{level_str}, expected {operator} {expected}"


@evaluator("docx_content_check")
async def eval_docx_content_check(workspace: Path, op_args: Dict[str, Any],
                                  value: Any = None, **kwargs) -> Tuple[bool, str]:
    """
    Check if DOCX contains specific text content.

    op_args:
        path: Path to DOCX file
        mode: "contains" | "regex" (default: inferred from value type)

    value:
        For "contains" mode: List of strings that must all be present
        For "regex" mode: Regex pattern string
    """
    path = op_args["path"]
    mode = op_args.get("mode")

    if mode is None:
        mode = "contains" if isinstance(value, list) else "regex"

    full_path = resolve_path(workspace, path)
    if full_path is None:
        return False, f"File not found: {path}"

    content = extract_docx_text(full_path)
    if content is None:
        return False, f"Failed to read DOCX: {path}"

    if mode == "contains":
        if not isinstance(value, list):
            value = [value]
        missing = [s for s in value if s.lower() not in content.lower()]
        if not missing:
            return True, ""
        return False, f"Missing content in DOCX: {missing[:3]}"

    elif mode == "regex":
        pattern = value
        if re.search(pattern, content, re.IGNORECASE):
            return True, ""
        return False, f"Pattern '{pattern}' not found in DOCX"

    return False, f"Unknown mode: {mode}"


@evaluator("pdf_page_count")
async def eval_pdf_page_count(workspace: Path, op_args: Dict[str, Any],
                              value: Any = None, **kwargs) -> Tuple[bool, str]:
    """
    Check the number of pages in a PDF file.

    op_args:
        path: Path to PDF file
        operator: Comparison operator ("==", ">=", "<=", ">", "<") default: ">="
        expected: Expected page count
    """
    try:
        import fitz
    except ImportError:
        return False, "PyMuPDF (fitz) package not installed"

    path = op_args["path"]
    operator = op_args.get("operator", ">=")
    expected = op_args["expected"]

    full_path = resolve_path(workspace, path)
    if full_path is None:
        return False, f"File not found: {path}"

    try:
        doc = fitz.open(str(full_path))
        actual = doc.page_count
        doc.close()
    except Exception as e:
        return False, f"Failed to read PDF: {e}"

    if operator in ("==", "eq"):
        passed = actual == expected
    elif operator in (">=", "gte"):
        passed = actual >= expected
    elif operator in ("<=", "lte"):
        passed = actual <= expected
    elif operator in (">", "gt"):
        passed = actual > expected
    elif operator in ("<", "lt"):
        passed = actual < expected
    else:
        return False, f"Unknown operator: {operator}"

    if passed:
        return True, ""
    return False, f"PDF has {actual} pages, expected {operator} {expected}"


@evaluator("pdf_orientation")
async def eval_pdf_orientation(workspace: Path, op_args: Dict[str, Any],
                               value: Any = None, **kwargs) -> Tuple[bool, str]:
    """
    Check if PDF pages are in the expected orientation (landscape or portrait).

    op_args:
        path: Path to PDF file
        expected: Expected orientation - "landscape" (width > height) or "portrait" (height > width)
        check_all: If True, all pages must match (default). If False, only first page is checked.
        tolerance: Aspect ratio tolerance for square-ish pages (default: 0.05)

    Returns:
        (passed, message) where passed is True if orientation matches expected.
    """
    try:
        import fitz
    except ImportError:
        return False, "PyMuPDF (fitz) package not installed"

    path = op_args["path"]
    expected = op_args.get("expected", "landscape").lower()
    check_all = op_args.get("check_all", True)
    tolerance = op_args.get("tolerance", 0.05)

    if expected not in ("landscape", "portrait"):
        return False, f"Invalid expected orientation: {expected}. Must be 'landscape' or 'portrait'."

    full_path = resolve_path(workspace, path)
    if full_path is None:
        return False, f"File not found: {path}"

    try:
        doc = fitz.open(str(full_path))
        page_count = doc.page_count

        if page_count == 0:
            doc.close()
            return False, "PDF has no pages"

        mismatched_pages = []
        first_page_info = None

        pages_to_check = range(page_count) if check_all else range(1)

        for i in pages_to_check:
            page = doc[i]
            rect = page.rect
            width = rect.width
            height = rect.height

            # Determine actual orientation
            ratio = width / height if height > 0 else 0
            if abs(ratio - 1.0) <= tolerance:
                actual = "square"
            elif width > height:
                actual = "landscape"
            else:
                actual = "portrait"

            if i == 0:
                first_page_info = f"{width:.0f}x{height:.0f} ({actual})"

            # Check if matches expected
            if expected == "landscape" and actual != "landscape":
                mismatched_pages.append((i + 1, width, height, actual))
            elif expected == "portrait" and actual != "portrait":
                mismatched_pages.append((i + 1, width, height, actual))

        doc.close()

    except Exception as e:
        return False, f"Failed to read PDF: {e}"

    if not mismatched_pages:
        return True, f"All {page_count} pages are {expected} (first page: {first_page_info})"

    # Build failure message
    if check_all:
        sample = mismatched_pages[:3]
        details = ", ".join([f"page {p}: {w:.0f}x{h:.0f} ({o})" for p, w, h, o in sample])
        if len(mismatched_pages) > 3:
            details += f" ... and {len(mismatched_pages) - 3} more"
        return False, f"Expected {expected} but found: {details}"
    else:
        p, w, h, o = mismatched_pages[0]
        return False, f"First page is {o} ({w:.0f}x{h:.0f}), expected {expected}"


@evaluator("pdf_dimensions")
async def eval_pdf_dimensions(workspace: Path, op_args: Dict[str, Any],
                              value: Any = None, **kwargs) -> Tuple[bool, str]:
    """
    Check if PDF page dimensions match expected size (e.g., A0, A4, letter).

    op_args:
        path: Path to PDF file
        expected_size: Expected size name ("A0", "A1", "A2", "A3", "A4", "letter")
                       or dict with {"width": mm, "height": mm}
        tolerance_mm: Tolerance in millimeters (default: 100 for posters, 10 for documents)
        check_all: If True, all pages must match (default True). If False, only first page.
        allow_rotated: If True, accept rotated dimensions (width/height swapped) (default True)

    Returns:
        (passed, message) where passed is True if dimensions match expected.
    """
    try:
        import fitz
    except ImportError:
        return False, "PyMuPDF (fitz) package not installed"

    # Standard paper sizes in mm (width x height in portrait)
    PAPER_SIZES = {
        "A0": (841, 1189),
        "A1": (594, 841),
        "A2": (420, 594),
        "A3": (297, 420),
        "A4": (210, 297),
        "letter": (216, 279),
    }

    path = op_args["path"]
    expected_size = op_args.get("expected_size", "A0")
    check_all = op_args.get("check_all", True)
    allow_rotated = op_args.get("allow_rotated", True)

    # Get expected dimensions
    if isinstance(expected_size, dict):
        expected_w = expected_size["width"]
        expected_h = expected_size["height"]
        size_name = f"{expected_w}x{expected_h}mm"
    elif expected_size.upper() in PAPER_SIZES:
        expected_w, expected_h = PAPER_SIZES[expected_size.upper()]
        size_name = expected_size.upper()
    else:
        return False, f"Unknown paper size: {expected_size}"

    # Default tolerance: larger for posters (A0-A2), smaller for documents
    default_tolerance = 100 if expected_size.upper() in ("A0", "A1", "A2") else 10
    tolerance_mm = op_args.get("tolerance_mm", default_tolerance)

    full_path = resolve_path(workspace, path)
    if full_path is None:
        return False, f"File not found: {path}"

    try:
        doc = fitz.open(str(full_path))
        page_count = doc.page_count

        if page_count == 0:
            doc.close()
            return False, "PDF has no pages"

        mismatched_pages = []
        first_page_info = None

        pages_to_check = range(page_count) if check_all else range(1)

        for i in pages_to_check:
            page = doc[i]
            rect = page.rect
            # Convert from points to mm (72 points = 1 inch, 1 inch = 25.4mm)
            actual_w_mm = rect.width * 25.4 / 72
            actual_h_mm = rect.height * 25.4 / 72

            if i == 0:
                first_page_info = f"{actual_w_mm:.0f}x{actual_h_mm:.0f}mm"

            # Check dimensions (allowing for rotation if enabled)
            match_portrait = (abs(actual_w_mm - expected_w) <= tolerance_mm and
                            abs(actual_h_mm - expected_h) <= tolerance_mm)
            match_landscape = (abs(actual_w_mm - expected_h) <= tolerance_mm and
                             abs(actual_h_mm - expected_w) <= tolerance_mm)

            if match_portrait or (allow_rotated and match_landscape):
                continue
            else:
                mismatched_pages.append((i + 1, actual_w_mm, actual_h_mm))

        doc.close()

    except Exception as e:
        return False, f"Failed to read PDF: {e}"

    if not mismatched_pages:
        return True, f"PDF dimensions match {size_name} (first page: {first_page_info}, tolerance: ±{tolerance_mm}mm)"

    # Build failure message
    if check_all:
        sample = mismatched_pages[:3]
        details = ", ".join([f"page {p}: {w:.0f}x{h:.0f}mm" for p, w, h in sample])
        if len(mismatched_pages) > 3:
            details += f" ... and {len(mismatched_pages) - 3} more"
        return False, f"Expected {size_name} (±{tolerance_mm}mm) but found: {details}"
    else:
        p, w, h = mismatched_pages[0]
        return False, f"First page is {w:.0f}x{h:.0f}mm, expected {size_name} ({expected_w}x{expected_h}mm ±{tolerance_mm}mm)"
