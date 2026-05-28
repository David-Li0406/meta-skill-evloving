"""Shared utilities for slideshow video agent."""

import os
import sys
import shutil
import time
from pathlib import Path
from typing import Optional, Callable, Any


def load_env() -> bool:
    """Load environment variables from .env file.

    Returns:
        True if .env file was found and loaded, False otherwise.
    """
    try:
        from dotenv import load_dotenv
    except ImportError:
        print("python-dotenv not installed. Run: pip install python-dotenv")
        return False

    # Search for .env in multiple locations
    env_paths = [
        Path.cwd() / ".env",
        Path(__file__).parent.parent.parent.parent.parent / ".env",  # Project root
    ]

    for env_path in env_paths:
        if env_path.exists():
            load_dotenv(env_path)
            return True

    return False


def get_fal_key() -> str:
    """Get FAL_KEY from environment, with helpful error if missing.

    Returns:
        The FAL_KEY API key string.

    Raises:
        EnvironmentError: If FAL_KEY is not set.
    """
    load_env()
    key = os.environ.get("FAL_KEY")
    if not key or key == "your-fal-api-key-here":
        raise EnvironmentError(
            "FAL_KEY not found or not configured.\n"
            "Please add your API key to .env file:\n"
            "  FAL_KEY=your-actual-api-key\n"
            "Get your key at: https://fal.ai/dashboard/keys"
        )
    return key


def get_anthropic_key() -> str:
    """Get ANTHROPIC_API_KEY from environment, with helpful error if missing.

    Returns:
        The Anthropic API key string.

    Raises:
        EnvironmentError: If ANTHROPIC_API_KEY is not set.
    """
    load_env()
    key = os.environ.get("ANTHROPIC_API_KEY")
    if not key or key.startswith("your-"):
        raise EnvironmentError(
            "ANTHROPIC_API_KEY not found or not configured.\n"
            "Please add your API key to .env file:\n"
            "  ANTHROPIC_API_KEY=sk-ant-...\n"
            "Get your key at: https://console.anthropic.com/"
        )
    return key


# Known FFmpeg installation paths (WinGet, manual installs)
FFMPEG_KNOWN_PATHS = [
    # WinGet installation path
    Path.home() / "AppData/Local/Microsoft/WinGet/Packages/Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe/ffmpeg-8.0.1-full_build/bin",
    # Common manual installation paths
    Path("C:/ffmpeg/bin"),
    Path("C:/Program Files/ffmpeg/bin"),
]


def _find_executable(name: str) -> Optional[str]:
    """Find executable in PATH or known locations.

    Args:
        name: Executable name (e.g., 'ffmpeg', 'ffprobe').

    Returns:
        Full path to executable or None if not found.
    """
    # First check PATH
    path = shutil.which(name)
    if path:
        return path

    # Check known installation paths
    for known_path in FFMPEG_KNOWN_PATHS:
        if known_path.exists():
            exe_path = known_path / f"{name}.exe"
            if exe_path.exists():
                return str(exe_path)

    return None


def check_ffmpeg() -> bool:
    """Check if FFmpeg is installed and accessible.

    Returns:
        True if FFmpeg is found in PATH or known locations, False otherwise.
    """
    return _find_executable("ffmpeg") is not None


def get_ffmpeg_path() -> str:
    """Get FFmpeg path or raise helpful error.

    Returns:
        Path to FFmpeg executable.

    Raises:
        EnvironmentError: If FFmpeg is not installed.
    """
    path = _find_executable("ffmpeg")
    if not path:
        raise EnvironmentError(
            "FFmpeg not found in PATH or known locations.\n"
            "Install FFmpeg:\n"
            "  Windows: Download from https://github.com/BtbN/FFmpeg-Builds/releases\n"
            "           Extract and add bin folder to PATH\n"
            "  Or: winget install ffmpeg\n"
            "  Or: choco install ffmpeg"
        )
    return path


def get_ffprobe_path() -> str:
    """Get ffprobe path or raise helpful error.

    Returns:
        Path to ffprobe executable.

    Raises:
        EnvironmentError: If ffprobe is not installed.
    """
    path = _find_executable("ffprobe")
    if not path:
        raise EnvironmentError(
            "ffprobe not found in PATH or known locations.\n"
            "ffprobe is typically installed with FFmpeg.\n"
            "Install FFmpeg to get ffprobe."
        )
    return path


def get_project_root() -> Path:
    """Get the project root directory.

    Returns:
        Path to project root (where .env and Reference Images are located).
    """
    # Try to find project root by looking for Reference Images folder
    candidates = [
        Path.cwd(),
        Path(__file__).parent.parent.parent.parent.parent,
    ]

    for path in candidates:
        if (path / "Reference Images").exists():
            return path

    # Fallback to cwd
    return Path.cwd()


def get_reference_images_dir() -> Path:
    """Get the Reference Images directory path.

    Returns:
        Path to Reference Images directory.

    Raises:
        FileNotFoundError: If Reference Images folder not found.
    """
    ref_dir = get_project_root() / "Reference Images"

    if ref_dir.exists():
        return ref_dir

    raise FileNotFoundError(
        "Reference Images folder not found.\n"
        "Expected at project root: Reference Images/"
    )


def list_reference_images() -> list[str]:
    """List available reference images.

    Returns:
        List of absolute paths to reference images.
    """
    try:
        ref_dir = get_reference_images_dir()
    except FileNotFoundError:
        return []

    images = []
    for ext in ["*.png", "*.jpg", "*.jpeg", "*.webp", "*.PNG", "*.JPG", "*.JPEG"]:
        images.extend(ref_dir.glob(ext))

    return [str(img) for img in sorted(images)]


def ensure_output_dirs(base_dir: str) -> dict[str, Path]:
    """Create output directory structure.

    Args:
        base_dir: Base directory for output.

    Returns:
        Dictionary mapping directory names to Path objects.
    """
    base = Path(base_dir)
    dirs = {
        "slides": base / "slides",
        "audio": base / "audio",
        "transitions": base / "transitions",
        "temp": base / "temp",
    }

    for d in dirs.values():
        d.mkdir(parents=True, exist_ok=True)

    return dirs


def cleanup_temp_dir(temp_dir: Path) -> None:
    """Clean up temporary directory.

    Args:
        temp_dir: Path to temporary directory to remove.
    """
    if temp_dir.exists():
        shutil.rmtree(temp_dir, ignore_errors=True)


def api_call_with_retry(
    func: Callable[..., Any],
    *args,
    max_retries: int = 3,
    initial_delay: float = 2.0,
    **kwargs
) -> Any:
    """Execute API call with exponential backoff retry.

    Args:
        func: Function to call.
        *args: Positional arguments for func.
        max_retries: Maximum number of retry attempts.
        initial_delay: Initial delay in seconds before first retry.
        **kwargs: Keyword arguments for func.

    Returns:
        Result from successful function call.

    Raises:
        Exception: If all retries fail, raises the last exception.
    """
    last_exception = None

    for attempt in range(max_retries):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            last_exception = e
            if attempt == max_retries - 1:
                raise

            wait_time = initial_delay * (2 ** attempt)
            print(f"API call failed (attempt {attempt + 1}/{max_retries}), "
                  f"retrying in {wait_time:.1f}s: {e}")
            time.sleep(wait_time)

    raise last_exception


def validate_prerequisites() -> dict[str, bool]:
    """Validate all prerequisites are met.

    Returns:
        Dictionary with validation results for each prerequisite.
    """
    results = {
        "fal_key": False,
        "anthropic_key": False,
        "ffmpeg": False,
        "ffprobe": False,
        "reference_images_dir": False,
    }

    try:
        get_fal_key()
        results["fal_key"] = True
    except EnvironmentError:
        pass

    try:
        get_anthropic_key()
        results["anthropic_key"] = True
    except EnvironmentError:
        pass

    results["ffmpeg"] = check_ffmpeg()
    results["ffprobe"] = _find_executable("ffprobe") is not None

    try:
        get_reference_images_dir()
        results["reference_images_dir"] = True
    except FileNotFoundError:
        pass

    return results


def print_prerequisites_status() -> bool:
    """Print status of all prerequisites.

    Returns:
        True if all prerequisites are met, False otherwise.
    """
    results = validate_prerequisites()

    print("Prerequisites Status:")
    print("-" * 40)

    status_symbols = {True: "[OK]", False: "[MISSING]"}

    print(f"  {status_symbols[results['fal_key']]} FAL_KEY in .env")
    print(f"  {status_symbols[results['anthropic_key']]} ANTHROPIC_API_KEY in .env")
    print(f"  {status_symbols[results['ffmpeg']]} FFmpeg installed")
    print(f"  {status_symbols[results['ffprobe']]} ffprobe installed")
    print(f"  {status_symbols[results['reference_images_dir']]} Reference Images folder")

    print("-" * 40)

    all_ok = all(results.values())
    if all_ok:
        print("All prerequisites met!")
    else:
        print("Some prerequisites missing. See above for details.")

    return all_ok
