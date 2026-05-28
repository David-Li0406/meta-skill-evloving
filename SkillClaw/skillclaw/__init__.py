"""Public package surface for SkillClaw.

Keep package import lightweight: callers that only need metadata or a single
symbol should not pull in the whole proxy/server stack at import time.
"""

from __future__ import annotations

from importlib import import_module
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .api_server import SkillClawAPIServer
    from .config import SkillClawConfig
    from .config_store import ConfigStore
    from .launcher import SkillClawLauncher
    from .skill_manager import SkillManager

__all__ = [
    "SkillClawConfig",
    "ConfigStore",
    "SkillClawAPIServer",
    "SkillManager",
    "SkillClawLauncher",
]


_EXPORT_MAP = {
    "SkillClawConfig": ("skillclaw.config", "SkillClawConfig"),
    "ConfigStore": ("skillclaw.config_store", "ConfigStore"),
    "SkillClawAPIServer": ("skillclaw.api_server", "SkillClawAPIServer"),
    "SkillManager": ("skillclaw.skill_manager", "SkillManager"),
    "SkillClawLauncher": ("skillclaw.launcher", "SkillClawLauncher"),
}


def __getattr__(name: str):
    target = _EXPORT_MAP.get(name)
    if target is None:
        raise AttributeError(f"module 'skillclaw' has no attribute {name!r}")
    module_name, attr_name = target
    value = getattr(import_module(module_name), attr_name)
    globals()[name] = value
    return value


def __dir__() -> list[str]:
    return sorted(list(globals().keys()) + __all__)
