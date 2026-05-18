"""Exploration strategies for task synthesis.

Available strategies:
- RandomExplorationStrategy: LLM-simulated random exploration
- ExperienceGuidedExplorationStrategy: LLM-simulated experience-guided exploration
- RealEnvironmentExplorationStrategy: Real environment exploration via EnvClient
- ExperienceGuidedRealStrategy: Experience-guided real environment exploration
"""

from .base import ExplorationStrategy, TaskObjective
from .random import RandomExplorationStrategy
from .experience_guided import (
    ExperienceGuidedExplorationStrategy,
    ExperienceTracker,
)
from .real_env import (
    RealEnvironmentExplorationStrategy,
    ExperienceGuidedRealStrategy,
)

__all__ = [
    "ExplorationStrategy",
    "TaskObjective",
    "RandomExplorationStrategy",
    "ExperienceGuidedExplorationStrategy",
    "ExperienceTracker",
    "RealEnvironmentExplorationStrategy",
    "ExperienceGuidedRealStrategy",
]
