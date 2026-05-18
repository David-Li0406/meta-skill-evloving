"""AppWorld-specific extraction configuration."""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional


@dataclass
class AppWorldExtractionConfig:
    """Configuration for AppWorld skill extraction."""

    # Benchmark identifier
    benchmark: str = "appworld"

    # Skill type
    skill_type: str = "functional"

    # API prefix for AppWorld
    api_prefix: str = "apis."

    # Filter settings
    filter_threshold: float = 0.999

    # Extraction settings
    batch_size: int = 10
    max_concurrent: int = 5
    max_retries: int = 5

    # Tool summary settings
    max_feedback_length: int = 1500

    # Plan format
    plan_step_prefix: str = "# step"

    # Known apps in AppWorld
    known_apps: List[str] = field(default_factory=lambda: [
        "spotify", "venmo", "amazon", "gmail", "calendar",
        "contacts", "notes", "reminders", "supervisor"
    ])

    def get_api_pattern(self) -> str:
        """Get regex pattern for API calls."""
        return rf"{self.api_prefix}(\w+)\.(\w+)"

    def is_valid_api(self, api_name: str) -> bool:
        """Check if API name follows AppWorld convention."""
        return api_name.startswith(self.api_prefix)

    def extract_app_name(self, api_name: str) -> Optional[str]:
        """Extract app name from full API name."""
        if not api_name.startswith(self.api_prefix):
            return None
        parts = api_name[len(self.api_prefix):].split(".")
        return parts[0] if parts else None
