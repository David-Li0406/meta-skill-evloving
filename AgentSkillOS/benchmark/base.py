"""Base class and metadata for benchmark plugins."""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional


@dataclass
class BenchmarkMeta:
    """Metadata describing a benchmark plugin."""

    label: str
    description: str = ""
    task_count: int = 0
    categories: list[str] = field(default_factory=list)


class BenchmarkBase:
    """Abstract base for benchmark plugins.

    Subclasses must set the ``meta`` class attribute and be decorated
    with ``@register_benchmark(name)`` so the registry can discover them.
    """

    meta: BenchmarkMeta

    def __init__(self) -> None:
        # root is the directory containing *this* subclass's __init__.py
        self.root: Path = Path(self.__class__.__module__.replace(".", "/")).parent
        # Fallback: use the package file directly
        mod = __import__(self.__class__.__module__)
        for part in self.__class__.__module__.split(".")[1:]:
            mod = getattr(mod, part)
        if hasattr(mod, "__file__") and mod.__file__:
            self.root = Path(mod.__file__).resolve().parent

    @property
    def tasks_dir(self) -> Path:
        return self.root / "tasks"

    @property
    def task_data_dir(self) -> Path:
        return self.root / "task_data"

    def resolve_task_data(self, task_id: str) -> Optional[Path]:
        """Return the task_data subdirectory for *task_id*, or None."""
        p = self.task_data_dir / task_id
        return p if p.is_dir() else None
