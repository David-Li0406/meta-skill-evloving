"""Shared utilities for PowerPoint agent."""

import os
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
    """Create output directory structure for PowerPoint generation.

    Args:
        base_dir: Base directory for output.

    Returns:
        Dictionary mapping directory names to Path objects.
    """
    base = Path(base_dir)
    dirs = {
        "slides": base / "slides",
        "temp": base / "temp",
    }

    for d in dirs.values():
        d.mkdir(parents=True, exist_ok=True)

    return dirs


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
        "reference_images_dir": False,
        "python_pptx": False,
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

    try:
        get_reference_images_dir()
        results["reference_images_dir"] = True
    except FileNotFoundError:
        pass

    try:
        import pptx
        results["python_pptx"] = True
    except ImportError:
        pass

    return results


def print_prerequisites_status() -> bool:
    """Print status of all prerequisites.

    Returns:
        True if all required prerequisites are met, False otherwise.
    """
    results = validate_prerequisites()

    print("Prerequisites Status:")
    print("-" * 40)

    status_symbols = {True: "[OK]", False: "[MISSING]"}

    print(f"  {status_symbols[results['fal_key']]} FAL_KEY in .env")
    print(f"  {status_symbols[results['anthropic_key']]} ANTHROPIC_API_KEY in .env (optional, for validation)")
    print(f"  {status_symbols[results['python_pptx']]} python-pptx installed")
    print(f"  {status_symbols[results['reference_images_dir']]} Reference Images folder")

    print("-" * 40)

    # Only fal_key and python_pptx are required
    required_ok = results["fal_key"] and results["python_pptx"]
    if required_ok:
        print("All required prerequisites met!")
    else:
        print("Some required prerequisites missing. See above for details.")

    return required_ok
