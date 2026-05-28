"""
File-to-image converters for LLM judge visual evaluation.

Converts PPTX, DOCX, HTML, PDF, and video files into PNG screenshots so that
the LLM judge can evaluate the *rendered visual output*, not raw source code.

Dependencies (all in skill_bench env):
    - PyMuPDF (fitz)       — PDF → images
    - playwright           — HTML rendering / screenshots
    - libreoffice (system) — DOCX/PPTX → PDF conversion (preserves styles & images)
    - opencv-python        — Video → key frame extraction
    - ffprobe (system)     — Video metadata extraction
"""
import asyncio
import shutil
import subprocess
import sys
import json
import tempfile
import uuid
from pathlib import Path
from typing import List, Optional, Dict, Any

# Max pages to render (avoids token explosion for long documents)
MAX_PAGES = 20
MAX_VIDEO_FRAMES = 30  # Fixed uniform sampling: first + last + evenly spaced middle frames

RENDERS_DIR_NAME = "_eval_renders"

# Shared image size limit — longest edge for images fed to LLM judges
MAX_IMAGE_EDGE = 1080


def resize_safe_image(
    image_path: Path,
    max_edge: int = MAX_IMAGE_EDGE,
    out_dir: Optional[Path] = None,
) -> Optional[Path]:
    """Resize an image so its longest edge is at most *max_edge* pixels.

    Handles decompression-bomb-sized images safely.  GIF files are returned
    unchanged to preserve animation.

    Args:
        image_path: Source image path.
        max_edge: Maximum longest edge in pixels.
        out_dir: Directory for the resized copy.  Defaults to the same
                 directory as *image_path*.

    Returns:
        Path to the (possibly new) image, or ``None`` if unreadable.
    """
    if image_path.suffix.lower() == ".gif":
        return image_path

    try:
        from PIL import Image
        # Disable PIL's built-in bomb check — we handle oversized images ourselves.
        Image.MAX_IMAGE_PIXELS = None

        with Image.open(image_path) as img:
            w, h = img.size
            longest = max(w, h)
            if longest <= max_edge:
                return image_path

            scale = max_edge / longest
            new_w = max(1, int(w * scale))
            new_h = max(1, int(h * scale))

            dest_dir = out_dir or image_path.parent
            dest_dir.mkdir(parents=True, exist_ok=True)
            out_path = dest_dir / f"{image_path.stem}_resized{image_path.suffix}"

            resized = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
            resized.save(str(out_path))
            print(f"  [resize] {image_path.name}: {w}x{h} -> {new_w}x{new_h}")
            return out_path
    except Exception as e:
        print(f"  [resize] Skipping unreadable image {image_path.name}: {e}")
        return None


def cleanup_renders(workspace: Path) -> int:
    """Remove all _eval_renders directories under workspace.

    Returns number of directories removed.
    """
    count = 0
    for renders_dir in workspace.rglob(RENDERS_DIR_NAME):
        if renders_dir.is_dir():
            shutil.rmtree(renders_dir, ignore_errors=True)
            count += 1
    return count

# Cache for video metadata (file_path -> metadata_dict)
_video_metadata_cache: Dict[str, Dict[str, Any]] = {}

# Cache for DOCX page count (file_path -> page_count), populated during rendering
_docx_page_count_cache: Dict[str, int] = {}


def get_video_metadata(file_path: Path) -> Optional[Dict[str, Any]]:
    """Get cached video metadata for a file.

    Returns dict with keys: width, height, fps, duration, frame_count, codec, bitrate
    Returns None if metadata not available.
    """
    return _video_metadata_cache.get(str(file_path))


def get_video_metadata_summary(file_path: Path) -> Optional[str]:
    """Get a human-readable summary of video metadata for LLM evaluation.

    Returns a formatted string suitable for including in LLM prompts.
    """
    meta = get_video_metadata(file_path)
    if not meta:
        return None

    lines = ["Video Technical Metadata:"]
    lines.append(f"  - Resolution: {meta.get('width', '?')}x{meta.get('height', '?')} pixels")
    lines.append(f"  - Frame rate: {meta.get('fps', '?')} fps")
    lines.append(f"  - Duration: {meta.get('duration', '?')} seconds")
    lines.append(f"  - Total frames: {meta.get('frame_count', '?')}")
    if meta.get('codec'):
        lines.append(f"  - Codec: {meta.get('codec')}")
    if meta.get('bitrate'):
        lines.append(f"  - Bitrate: {meta.get('bitrate')} kbps")
    if meta.get('encoder'):
        lines.append(f"  - Encoder: {meta.get('encoder')}")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

async def render_to_images(file_path: Path, out_dir: Optional[Path] = None) -> List[Path]:
    """Render a file to a list of PNG screenshot paths.

    Supports: .pdf, .html, .pptx, .docx, .mp4, .avi, .mov, .webm
    Unsupported formats return an empty list.

    Args:
        file_path: Path to the file to render.
        out_dir: Base directory for rendered output.  When ``None`` (default),
                 images are saved under ``{file_path.parent}/_eval_renders/{stem}``.
                 When provided, images are saved under ``{out_dir}/{stem}``.
    """
    suffix = file_path.suffix.lower()
    renderers = {
        ".pdf": _render_pdf,
        ".html": _render_html,
        ".htm": _render_html,
        ".pptx": _render_pptx,
        ".docx": _render_docx,
        ".mp4": _render_video,
        ".avi": _render_video,
        ".mov": _render_video,
        ".webm": _render_video,
    }
    renderer = renderers.get(suffix)
    if renderer is None:
        return []

    # Prepare output directory (per-file subdirectory to avoid collisions)
    if out_dir is None:
        out_dir = file_path.parent / RENDERS_DIR_NAME / file_path.stem
    else:
        out_dir = out_dir / file_path.stem
    if out_dir.exists():
        shutil.rmtree(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    try:
        return await renderer(file_path, out_dir)
    except Exception as e:
        print(f"  [file_converters] Failed to render {file_path.name}: {e}")
        return []


# ---------------------------------------------------------------------------
# PDF → images  (PyMuPDF)
# ---------------------------------------------------------------------------

async def _render_pdf(file_path: Path, out_dir: Path) -> List[Path]:
    def _convert():
        import fitz
        doc = fitz.open(str(file_path))
        paths = []
        for i, page in enumerate(doc):
            if i >= MAX_PAGES:
                break
            pix = page.get_pixmap(dpi=150)
            out = out_dir / f"{file_path.stem}_page_{i + 1:03d}.png"
            pix.save(str(out))
            paths.append(out)
        doc.close()
        return paths

    return await asyncio.to_thread(_convert)


# ---------------------------------------------------------------------------
# HTML → screenshot  (playwright)
# ---------------------------------------------------------------------------

async def _render_html(file_path: Path, out_dir: Path) -> List[Path]:
    def _capture():
        from playwright.sync_api import sync_playwright

        out_gif = out_dir / f"{file_path.stem}.gif"

        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page(
                viewport={"width": 1280, "height": 800},
                device_scale_factor=2,  # 2x resolution for sharper screenshots
            )
            page.goto(f"file://{file_path.resolve()}", wait_until="networkidle")

            # Wait for initial animations
            page.wait_for_timeout(1500)

            # Get page height for scrolling
            page_height = page.evaluate("document.body.scrollHeight")
            scroll_step = 600  # Scroll 600px each step

            # Collect frames for GIF while scrolling
            frame_paths = []

            # Capture initial frame at top
            frame_path = out_dir / f"frame_000.png"
            page.screenshot(path=str(frame_path))
            frame_paths.append(frame_path)

            # Scroll down incrementally and capture frames
            current_scroll = 0
            frame_idx = 1
            while current_scroll < page_height:
                current_scroll += scroll_step
                page.evaluate(f"window.scrollTo(0, {current_scroll})")
                page.wait_for_timeout(400)  # Wait for animations

                frame_path = out_dir / f"frame_{frame_idx:03d}.png"
                page.screenshot(path=str(frame_path))
                frame_paths.append(frame_path)
                frame_idx += 1

            # Scroll to bottom
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            page.wait_for_timeout(500)
            frame_path = out_dir / f"frame_{frame_idx:03d}.png"
            page.screenshot(path=str(frame_path))
            frame_paths.append(frame_path)
            frame_idx += 1

            # Pause at bottom
            for _ in range(2):
                frame_paths.append(frame_path)  # Duplicate last frame for pause

            # Capture full-page PNG (OpenAI only sees first GIF frame)
            full_page_path = out_dir / f"{file_path.stem}_full.png"
            page.evaluate("window.scrollTo(0, 0)")
            page.wait_for_timeout(300)
            page.screenshot(path=str(full_page_path), full_page=True)

            browser.close()

        # Create GIF from frames using Pillow
        try:
            from PIL import Image

            # Read first frame to determine scaling ratio (max longest edge 1080px)
            first_img = Image.open(frame_paths[0])
            orig_w, orig_h = first_img.size
            longest = max(orig_w, orig_h)
            if longest > 1080:
                scale = 1080 / longest
                target_w = int(orig_w * scale)
                target_h = int(orig_h * scale)
            else:
                target_w, target_h = orig_w, orig_h
            first_img.close()

            images = []
            for fp in frame_paths:
                img = Image.open(fp)
                img = img.resize((target_w, target_h), Image.Resampling.LANCZOS)
                images.append(img)

            if images:
                images[0].save(
                    str(out_gif),
                    save_all=True,
                    append_images=images[1:],
                    duration=500,  # 500ms per frame
                    loop=0  # Loop forever
                )

            # Clean up individual frame files
            for fp in set(frame_paths):
                if fp.exists():
                    fp.unlink()

        except ImportError:
            print("  [file_converters] Pillow not available, skipping GIF generation")
        except Exception as e:
            print(f"  [file_converters] GIF generation failed: {e}")

        results = []
        if out_gif.exists():
            results.append(out_gif)
        if full_page_path.exists():
            results.append(full_page_path)
        return results

    return await asyncio.to_thread(_capture)


# ---------------------------------------------------------------------------
# LibreOffice conversion helper (for DOCX/PPTX → PDF)
# ---------------------------------------------------------------------------

def _find_libreoffice() -> Optional[str]:
    """Find the LibreOffice binary path, checking platform-appropriate locations."""
    if sys.platform == "darwin":
        mac_path = "/Applications/LibreOffice.app/Contents/MacOS/soffice"
        if Path(mac_path).is_file():
            return mac_path
        for name in ("soffice", "libreoffice"):
            found = shutil.which(name)
            if found:
                return found
    else:
        for name in ("libreoffice", "soffice"):
            found = shutil.which(name)
            if found:
                return found
    return None


def _convert_to_pdf_libreoffice(file_path: Path, out_dir: Path) -> Optional[Path]:
    """Convert DOCX/PPTX to PDF using LibreOffice.

    This preserves all styles, images, and formatting that would be lost
    with python-docx/pptx → HTML conversion.

    Uses a unique temporary user profile to avoid conflicts when running
    multiple LibreOffice instances concurrently.

    Returns the PDF path on success, None on failure.
    """
    pdf_path = out_dir / f"{file_path.stem}.pdf"

    # Create a unique temporary directory for LibreOffice user profile
    # This prevents conflicts when multiple conversions run in parallel
    tmp_profile = None

    lo_bin = _find_libreoffice()
    if lo_bin is None:
        if sys.platform == "darwin":
            print("  [file_converters] LibreOffice not installed. Install from https://www.libreoffice.org/ or: brew install --cask libreoffice")
        else:
            print("  [file_converters] LibreOffice not installed. Install with: sudo apt install libreoffice")
        return None

    try:
        tmp_profile = tempfile.mkdtemp(prefix=f"lo_profile_{uuid.uuid4().hex[:8]}_")

        result = subprocess.run(
            [
                lo_bin,
                "--headless",
                f"-env:UserInstallation=file://{tmp_profile}",
                "--convert-to", "pdf",
                "--outdir", str(out_dir),
                str(file_path)
            ],
            capture_output=True,
            text=True,
            timeout=120,  # 2 minutes timeout for large files
        )

        if result.returncode != 0:
            print(f"  [file_converters] LibreOffice conversion failed: {result.stderr}")
            return None

        if not pdf_path.exists():
            print(f"  [file_converters] PDF not created at expected path: {pdf_path}")
            return None

        return pdf_path

    except FileNotFoundError:
        if sys.platform == "darwin":
            print("  [file_converters] LibreOffice not installed. Install from https://www.libreoffice.org/ or: brew install --cask libreoffice")
        else:
            print("  [file_converters] LibreOffice not installed. Install with: sudo apt install libreoffice")
        return None
    except subprocess.TimeoutExpired:
        print("  [file_converters] LibreOffice conversion timed out")
        return None
    except Exception as e:
        print(f"  [file_converters] LibreOffice conversion error: {e}")
        return None
    finally:
        # Clean up temporary profile directory
        if tmp_profile:
            try:
                shutil.rmtree(tmp_profile, ignore_errors=True)
            except Exception:
                pass


def _render_pdf_pages(pdf_path: Path, out_dir: Path, stem: str, dpi: int = 150) -> List[Path]:
    """Render PDF pages to PNG images using PyMuPDF.

    Args:
        pdf_path: Path to the PDF file
        out_dir: Output directory for PNG files
        stem: Base name for output files
        dpi: Resolution for rendering (default 150)

    Returns:
        List of PNG file paths
    """
    import fitz

    doc = fitz.open(str(pdf_path))
    paths = []

    for i, page in enumerate(doc):
        if i >= MAX_PAGES:
            break
        pix = page.get_pixmap(dpi=dpi)
        out = out_dir / f"{stem}_page_{i + 1:03d}.png"
        pix.save(str(out))
        paths.append(out)

    doc.close()
    return paths


# ---------------------------------------------------------------------------
# PPTX → images  (LibreOffice → PDF → PyMuPDF)
# ---------------------------------------------------------------------------

async def _render_pptx(file_path: Path, out_dir: Path) -> List[Path]:
    """Render PPTX to images using LibreOffice for high-fidelity conversion."""
    def _convert():
        # Step 1: Convert PPTX to PDF using LibreOffice
        pdf_path = _convert_to_pdf_libreoffice(file_path, out_dir)
        if pdf_path is None:
            return []

        # Step 2: Render PDF pages to PNG
        paths = _render_pdf_pages(pdf_path, out_dir, file_path.stem, dpi=150)

        # Clean up intermediate PDF
        try:
            pdf_path.unlink()
        except Exception:
            pass

        return paths

    return await asyncio.to_thread(_convert)


# ---------------------------------------------------------------------------
# DOCX → images  (LibreOffice → PDF → PyMuPDF)
# ---------------------------------------------------------------------------

async def _render_docx(file_path: Path, out_dir: Path) -> List[Path]:
    """Render DOCX to images using LibreOffice for high-fidelity conversion."""
    def _convert():
        # Step 1: Convert DOCX to PDF using LibreOffice
        pdf_path = _convert_to_pdf_libreoffice(file_path, out_dir)
        if pdf_path is None:
            return []

        # Record page count from intermediate PDF for metadata
        try:
            import fitz
            doc = fitz.open(str(pdf_path))
            _docx_page_count_cache[str(file_path)] = len(doc)
            doc.close()
        except Exception:
            pass

        # Step 2: Render PDF pages to PNG
        paths = _render_pdf_pages(pdf_path, out_dir, file_path.stem, dpi=150)

        # Clean up intermediate PDF
        try:
            pdf_path.unlink()
        except Exception:
            pass

        return paths

    return await asyncio.to_thread(_convert)


# ---------------------------------------------------------------------------
# Video → key frames  (OpenCV) + metadata extraction (ffprobe)
# ---------------------------------------------------------------------------

def _extract_video_metadata(file_path: Path) -> Dict[str, Any]:
    """Extract video metadata using ffprobe.

    Returns dict with: width, height, fps, duration, frame_count, codec, bitrate, encoder
    """
    try:
        cmd = [
            "ffprobe", "-v", "quiet",
            "-print_format", "json",
            "-show_format", "-show_streams",
            str(file_path)
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if result.returncode != 0:
            return {}

        data = json.loads(result.stdout)
        meta = {}

        # Find video stream
        for stream in data.get("streams", []):
            if stream.get("codec_type") == "video":
                meta["width"] = stream.get("width")
                meta["height"] = stream.get("height")
                meta["codec"] = stream.get("codec_name")
                meta["frame_count"] = int(stream.get("nb_frames", 0)) or None

                # Parse frame rate (e.g., "60/1" or "30000/1001")
                fps_str = stream.get("r_frame_rate", "")
                if "/" in fps_str:
                    num, den = fps_str.split("/")
                    try:
                        meta["fps"] = round(float(num) / float(den), 2)
                    except (ValueError, ZeroDivisionError):
                        pass

                # Duration from stream
                if stream.get("duration"):
                    meta["duration"] = round(float(stream["duration"]), 2)

                # Bitrate from stream (in kbps)
                if stream.get("bit_rate"):
                    meta["bitrate"] = round(int(stream["bit_rate"]) / 1000, 1)

                break

        # Get encoder info from format tags
        fmt = data.get("format", {})
        tags = fmt.get("tags", {})
        if tags.get("comment"):
            meta["encoder"] = tags["comment"]
        elif tags.get("encoder"):
            meta["encoder"] = tags["encoder"]

        # Fallback duration from format
        if not meta.get("duration") and fmt.get("duration"):
            meta["duration"] = round(float(fmt["duration"]), 2)

        return meta

    except Exception as e:
        print(f"  [file_converters] Failed to extract video metadata: {e}")
        return {}


async def _render_video(file_path: Path, out_dir: Path) -> List[Path]:
    """Extract up to N uniformly sampled frames from a video file and cache metadata."""
    def _convert():
        import cv2

        # Extract and cache metadata first
        meta = _extract_video_metadata(file_path)
        if meta:
            _video_metadata_cache[str(file_path)] = meta

        cap = cv2.VideoCapture(str(file_path))
        if not cap.isOpened():
            return []

        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        if total_frames <= 0:
            cap.release()
            return []

        # Uniformly sample up to MAX_VIDEO_FRAMES frames, always including
        # the first and last frame for complete coverage of the video.
        num_frames = min(MAX_VIDEO_FRAMES, total_frames)
        if num_frames <= 1:
            sample_indices = [0]
        else:
            sample_indices = [
                round(i * (total_frames - 1) / (num_frames - 1))
                for i in range(num_frames)
            ]

        paths = []
        for frame_idx in sample_indices:
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
            ret, frame = cap.read()
            if not ret:
                break
            out = out_dir / f"{file_path.stem}_frame_{len(paths) + 1:04d}.png"
            cv2.imwrite(str(out), frame)
            paths.append(out)

        cap.release()
        return paths

    return await asyncio.to_thread(_convert)


# ---------------------------------------------------------------------------
# File metadata extraction
# ---------------------------------------------------------------------------

def get_file_metadata_summary(file_path: Path) -> Optional[str]:
    """Return a human-readable metadata summary for images, PDFs, PPTX, and DOCX.

    Similar to ``get_video_metadata_summary()`` but for non-video files.
    Returns None for unsupported file types or on failure.
    """
    suffix = file_path.suffix.lower()
    try:
        if suffix in (".png", ".jpg", ".jpeg", ".webp", ".bmp", ".gif"):
            from PIL import Image
            with Image.open(file_path) as img:
                w, h = img.size
                fmt = img.format or suffix.lstrip(".").upper()
            lines = [
                "Image Metadata:",
                f"  - Original resolution: {w}x{h} pixels",
                f"  - Format: {fmt}",
            ]
            return "\n".join(lines)

        if suffix == ".pdf":
            import fitz
            doc = fitz.open(str(file_path))
            page_count = len(doc)
            if page_count > 0:
                page = doc[0]
                # Convert points to mm (1 pt = 25.4/72 mm)
                w_mm = round(page.rect.width * 25.4 / 72)
                h_mm = round(page.rect.height * 25.4 / 72)
                orientation = "Portrait" if h_mm >= w_mm else "Landscape"
                size_str = f"{w_mm}x{h_mm} mm ({orientation})"
            else:
                size_str = "unknown"
            doc.close()
            lines = [
                "PDF Metadata:",
                f"  - Page count: {page_count}",
                f"  - Page size: {size_str}",
            ]
            return "\n".join(lines)

        if suffix == ".pptx":
            from pptx import Presentation
            prs = Presentation(str(file_path))
            slide_count = len(prs.slides)
            w_mm = round(prs.slide_width / 914400 * 25.4)  # EMU → inches → mm
            h_mm = round(prs.slide_height / 914400 * 25.4)
            lines = [
                "PPTX Metadata:",
                f"  - Slide count: {slide_count}",
                f"  - Slide size: {w_mm}x{h_mm} mm",
            ]
            return "\n".join(lines)

        if suffix == ".docx":
            page_count = _docx_page_count_cache.get(str(file_path))
            if page_count is not None:
                lines = [
                    "DOCX Metadata:",
                    f"  - Page count: {page_count}",
                ]
                return "\n".join(lines)
            return None

    except Exception:
        return None

    return None


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _escape(text: str) -> str:
    """Escape HTML special characters."""
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )
