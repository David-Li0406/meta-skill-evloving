from __future__ import annotations

import logging
from pathlib import Path

from src.humcp.decorator import tool

try:
    from markitdown import MarkItDown
except ImportError as err:
    raise ImportError(
        "markitdown is required for PDF to Markdown conversion. Install with: pip install 'markitdown[all]'"
    ) from err

logger = logging.getLogger("humcp.tools.pdf_to_markdown")


@tool()
async def convert_to_markdown(pdf_path: str) -> dict:
    """
    Convert a PDF file to Markdown format.

    Args:
        pdf_path: Path to the PDF file to convert.

    Returns:
        Success flag and markdown content or error message.
    """
    try:
        pdf_file = Path(pdf_path)
        if not pdf_file.exists():
            return {"success": False, "error": f"PDF file not found: {pdf_path}"}

        if pdf_file.suffix.lower() != ".pdf":
            return {"success": False, "error": f"File is not a PDF: {pdf_path}"}

        md = MarkItDown()
        logger.info("Converting PDF to markdown path=%s", pdf_file)
        result = md.convert(str(pdf_file))

        markdown_content = (
            result.text_content if hasattr(result, "text_content") else str(result)
        )

        logger.info("PDF conversion complete path=%s", pdf_file)
        return {"success": True, "data": {"markdown": markdown_content}}
    except Exception as e:
        logger.exception("Failed to convert PDF to markdown")
        return {"success": False, "error": str(e)}
