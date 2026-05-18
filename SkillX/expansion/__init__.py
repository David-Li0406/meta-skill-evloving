"""Expansion module for experience-guided skill exploration."""

from .base import BaseExpansionStrategy
from .explorer import ExperienceGuidedExplorer
from .task_generator import TaskGenerator, TaskSynthesizer
from .env_worker import (
    BaseEnvWorker,
    GenericEnvWorker,
    AppWorldEnvWorker,
)
from .strategies import (
    ExplorationStrategy,
    TaskObjective,
    RandomExplorationStrategy,
    ExperienceGuidedExplorationStrategy,
    ExperienceTracker,
    RealEnvironmentExplorationStrategy,
    ExperienceGuidedRealStrategy,
)
from .task_manager import (
    TaskSynthesisManager,
    TaskPostFilter,
    DuplicateFilter,
    ConfidenceFilter,
)
from .env_explorer import (
    EnvironmentExplorer,
    RealEnvironmentExplorer,
    SimulatedEnvironmentExplorer,
)

__all__ = [
    "BaseExpansionStrategy",
    "ExperienceGuidedExplorer",
    "TaskGenerator",
    "TaskSynthesizer",
    # Environment worker interfaces
    "BaseEnvWorker",
    "GenericEnvWorker",
    "AppWorldEnvWorker",
    # Abstracted task synthesis components (AgentEvolver style)
    "ExplorationStrategy",
    "TaskObjective",
    "RandomExplorationStrategy",
    "ExperienceGuidedExplorationStrategy",
    "ExperienceTracker",
    "RealEnvironmentExplorationStrategy",
    "ExperienceGuidedRealStrategy",
    "TaskSynthesisManager",
    "TaskPostFilter",
    "DuplicateFilter",
    "ConfidenceFilter",
    # Environment exploration
    "EnvironmentExplorer",
    "RealEnvironmentExplorer",
    "SimulatedEnvironmentExplorer",
]
