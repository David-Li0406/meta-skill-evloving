"""LiteLLM disk cache initialization."""

import threading

from config import PROJECT_ROOT, MIN_CACHE_TTL_SECONDS

_cache_lock = threading.Lock()
_cache_initialized = False


def ensure_cache():
    """Ensure LiteLLM disk cache is initialized (thread-safe)."""
    global _cache_initialized
    if _cache_initialized:
        return
    with _cache_lock:
        if _cache_initialized:  # double-check
            return
        try:
            import litellm
            cache_dir = PROJECT_ROOT / ".cache" / "litellm"
            cache_dir.mkdir(parents=True, exist_ok=True)
            litellm.cache = litellm.Cache(
                type="disk",
                disk_cache_dir=str(cache_dir),
                ttl=MIN_CACHE_TTL_SECONDS,  # at least one year
            )
            # litellm DiskCache doesn't expose size_limit param;
            # default 1GB is insufficient when embedding entries (~3.8MB each)
            # coexist with completion entries, causing premature eviction.
            litellm.cache.cache.disk_cache.reset('size_limit', int(20e9))  # 20GB
            litellm.enable_cache()
            _cache_initialized = True
        except Exception as e:
            from rich.console import Console
            Console(stderr=True).print(f"[yellow]Warning: LiteLLM cache init failed: {e}[/yellow]")
