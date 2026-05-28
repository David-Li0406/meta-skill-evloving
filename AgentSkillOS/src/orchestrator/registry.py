"""Engine registry — register and create execution engines by name.

Engines are auto-discovered via pkgutil scanning of the orchestrator package.
Each engine class declares an ``EngineMeta`` instance as its ``meta`` class
attribute so that adding a new engine only requires creating new files — no
edits to existing modules.
"""

from __future__ import annotations

import importlib
import pkgutil
import threading
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .base import ExecutionEngine

from .base import EngineMeta

_engines: dict[str, type] = {}
_registered = False
_lock = threading.Lock()

_DEFAULT_META = EngineMeta(label="")


def register_engine(name: str):
    """Class decorator to register an engine under *name*."""

    def decorator(cls: type) -> type:
        _engines[name] = cls
        return cls

    return decorator


def _ensure_registered() -> None:
    """Lazily auto-discover engine modules via pkgutil scanning."""
    global _registered
    if _registered:
        return
    with _lock:
        if _registered:
            return
        _registered = True
        import orchestrator as pkg
        for finder, name, ispkg in pkgutil.iter_modules(pkg.__path__):
            if ispkg:
                try:
                    importlib.import_module(f"orchestrator.{name}.engine")
                except (ImportError, ModuleNotFoundError):
                    pass


def _get_meta(name: str) -> EngineMeta:
    """Return the EngineMeta for *name*, falling back to _DEFAULT_META."""
    cls = _engines.get(name)
    if cls is None:
        return _DEFAULT_META
    return getattr(cls, "meta", _DEFAULT_META)


# ---------------------------------------------------------------------------
# Engine instantiation
# ---------------------------------------------------------------------------

def create_engine(name: str, **kwargs) -> "ExecutionEngine":
    """Instantiate a registered engine by name.

    If the engine class has a ``create()`` classmethod, delegates to it.
    Otherwise falls back to ``cls(**kwargs)``.
    """
    _ensure_registered()
    if name not in _engines:
        raise KeyError(
            f"Unknown engine '{name}'. Available: {sorted(_engines)}"
        )
    cls = _engines[name]
    create_fn = getattr(cls, "create", None)
    if create_fn:
        return create_fn(**kwargs)
    return cls(**kwargs)


def list_engines() -> list[str]:
    """Return sorted list of registered engine names."""
    _ensure_registered()
    return sorted(_engines.keys())


# ---------------------------------------------------------------------------
# UI hints — derived from EngineMeta
# ---------------------------------------------------------------------------

def get_engine_ui_hints(name: str) -> dict:
    """Return UI hints for *name*, falling back to safe defaults."""
    _ensure_registered()
    meta = _get_meta(name)
    return {
        "needs_planning": meta.initial_phase == "planning",
        "execution_visual": meta.execution_visual,
    }


# ---------------------------------------------------------------------------
# Display metadata — derived from EngineMeta
# ---------------------------------------------------------------------------

def list_review_engines() -> list[dict]:
    """Return engines visible in skill review UI."""
    _ensure_registered()
    result = []
    for name in sorted(_engines):
        meta = _get_meta(name)
        if meta.show_in_review:
            result.append({"id": name, "label": meta.label, "description": meta.description})
    return result


# ---------------------------------------------------------------------------
# Alias resolution — read from EngineMeta.aliases
# ---------------------------------------------------------------------------

def resolve_engine_alias(name: str) -> str:
    """Resolve an engine name or alias to its canonical registered name.

    Returns the input unchanged if it's already a registered engine name.
    """
    _ensure_registered()
    if name in _engines:
        return name
    for engine_name in _engines:
        meta = _get_meta(engine_name)
        if name in meta.aliases:
            return engine_name
    return name


# ---------------------------------------------------------------------------
# UI contributions — collect from engine class attributes
# ---------------------------------------------------------------------------

def get_all_engine_contributions() -> dict[str, dict]:
    """Collect ui_contribution dicts from all registered engine classes.

    Returns:
        Dict mapping contribution id to contribution dict.
    """
    _ensure_registered()
    contributions = {}
    for cls in _engines.values():
        contrib = getattr(cls, "ui_contribution", None)
        if contrib and "id" in contrib:
            contributions[contrib["id"]] = contrib
    return contributions


# ---------------------------------------------------------------------------
# Engine execution metadata — derived from EngineMeta
# ---------------------------------------------------------------------------

def get_engine_execution_meta(name: str) -> dict:
    """Return execution metadata for an engine (folder_mode, initial_phase)."""
    _ensure_registered()
    meta = _get_meta(name)
    return {
        "folder_mode": meta.folder_mode if meta.folder_mode is not None else name,
        "initial_phase": meta.initial_phase,
    }
