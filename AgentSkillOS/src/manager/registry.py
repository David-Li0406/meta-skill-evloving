"""Plugin registry — auto-discovery and config.yaml driven instance creation.

Manager modules are auto-discovered via pkgutil scanning of the manager package.
Each subpackage that contains a class decorated with @register_manager will be
found automatically — no manual imports needed.
"""
import importlib
import pkgutil
import threading
from typing import Type

_managers: dict[str, Type] = {}

# ===== Registration decorators =====

def register_manager(name: str):
    def decorator(cls):
        _managers[name] = cls
        return cls
    return decorator


# ===== Factory functions =====

def create_manager(name: str = None, **kwargs):
    """Create a Manager instance. name=None reads from config.yaml."""
    _ensure_registered()
    if name is None:
        from config import get_config
        name = get_config().manager
    if name not in _managers:
        raise KeyError(
            f"Unknown manager: '{name}'. Available: {list(_managers.keys())}"
        )
    return _managers[name](**kwargs)


def list_plugins() -> dict:
    """List all registered plugins."""
    _ensure_registered()
    return {
        "managers": list(_managers.keys()),
    }


# ===== UI contributions collection =====

def get_all_manager_contributions() -> dict[str, dict]:
    """Collect ui_contribution dicts from all registered manager classes.

    Returns:
        Dict mapping contribution id to contribution dict.
    """
    _ensure_registered()
    contributions = {}
    for cls in _managers.values():
        contrib = getattr(cls, "ui_contribution", None)
        if contrib and "id" in contrib:
            contributions[contrib["id"]] = contrib
    return contributions


# ===== Auto-discovery (lazy) =====

_registered = False
_lock = threading.Lock()


def _ensure_registered():
    global _registered
    if _registered:
        return
    with _lock:
        if _registered:
            return
        _registered = True
        import manager as pkg
        for finder, name, ispkg in pkgutil.iter_modules(pkg.__path__):
            if ispkg:
                try:
                    mod = importlib.import_module(f"manager.{name}")
                    # If the subpackage __init__ has a class with register_manager
                    # applied, it's already registered. If not, look for common
                    # class naming conventions.
                except (ImportError, ModuleNotFoundError):
                    pass
