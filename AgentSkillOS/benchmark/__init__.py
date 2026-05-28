"""Benchmark registry with pkgutil auto-discovery.

Usage::

    from benchmark import get_benchmark, list_benchmarks, resolve_task_file

    bench = get_benchmark("AgentSkillOS_bench")
    task_path = resolve_task_file("AgentSkillOS_bench", "data_computation_task1.json")
"""

import importlib
import pkgutil
import threading
from pathlib import Path
from typing import Type, Optional

from .base import BenchmarkBase, BenchmarkMeta

_benchmarks: dict[str, Type[BenchmarkBase]] = {}

# ===== Registration decorator =====

def register_benchmark(name: str):
    """Class decorator that registers a BenchmarkBase subclass."""
    def decorator(cls: Type[BenchmarkBase]):
        _benchmarks[name] = cls
        return cls
    return decorator


# ===== Factory / query functions =====

def get_benchmark(name: str) -> BenchmarkBase:
    """Return an instance of the named benchmark."""
    _ensure_registered()
    if name not in _benchmarks:
        raise KeyError(
            f"Unknown benchmark: '{name}'. Available: {list(_benchmarks.keys())}"
        )
    return _benchmarks[name]()


def list_benchmarks() -> list[str]:
    """Return names of all discovered benchmarks."""
    _ensure_registered()
    return list(_benchmarks.keys())


def resolve_task_file(bench_name: str, task_filename: str) -> Path:
    """Resolve a task JSON file path within the named benchmark.

    Args:
        bench_name: Registered benchmark name.
        task_filename: Filename (e.g. ``data_computation_task1.json``).

    Returns:
        Absolute path to the task file.

    Raises:
        KeyError: If the benchmark is not registered.
        FileNotFoundError: If the task file does not exist.
    """
    bench = get_benchmark(bench_name)
    path = bench.tasks_dir / task_filename
    if not path.exists():
        raise FileNotFoundError(f"Task file not found: {path}")
    return path


# ===== Auto-discovery (lazy, thread-safe) =====

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
        import benchmark as pkg
        for finder, name, ispkg in pkgutil.iter_modules(pkg.__path__):
            if ispkg:
                try:
                    importlib.import_module(f"benchmark.{name}")
                except (ImportError, ModuleNotFoundError):
                    pass
