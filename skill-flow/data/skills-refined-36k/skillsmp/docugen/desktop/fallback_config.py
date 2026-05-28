"""Configuration for accessibility API fallback mechanism."""

import os
from dataclasses import dataclass, field
from typing import Dict


@dataclass
class FallbackConfig:
    """Configuration for fallback behavior when accessibility APIs fail."""

    timeout_ms: int = 100
    retry_strategy: str = "exponential_backoff"  # none, immediate, exponential_backoff
    permission_handling: str = "auto_fallback"  # auto_fallback, prompt_user, fail
    cache_ttl_seconds: int = 300
    max_retries: int = 2
    visual_fallback_enabled: bool = True
    app_specific_rules: Dict[str, Dict] = field(default_factory=dict)

    @classmethod
    def from_env(cls) -> "FallbackConfig":
        """Load configuration from environment variables with defaults."""
        return cls(
            timeout_ms=int(os.getenv("FALLBACK_TIMEOUT_MS", "100")),
            retry_strategy=os.getenv("FALLBACK_RETRY_STRATEGY", "exponential_backoff"),
            permission_handling=os.getenv("FALLBACK_PERMISSION_HANDLING", "auto_fallback"),
            cache_ttl_seconds=int(os.getenv("FALLBACK_CACHE_TTL", "300")),
            max_retries=int(os.getenv("FALLBACK_MAX_RETRIES", "2")),
            visual_fallback_enabled=os.getenv("FALLBACK_VISUAL_ENABLED", "true").lower() == "true",
        )
