import logging
from typing import Any, Optional
import sys
from pathlib import Path

# Add lib to path for serena_deps access
lib_path = Path(__file__).parent.parent.parent
sys.path.insert(0, str(lib_path))

from serena_deps.sensai_shim import dump_pickle, load_pickle

log = logging.getLogger(__name__)


def load_cache(path: str, version: Any) -> Optional[Any]:
    data = load_pickle(path)
    if not isinstance(data, dict) or "__cache_version" not in data:
        log.info("Cache is outdated (expected version %s). Ignoring cache at %s", version, path)
        return None
    saved_version = data["__cache_version"]
    if saved_version != version:
        log.info("Cache is outdated (expected version %s, got %s). Ignoring cache at %s", version, saved_version, path)
        return None
    return data["obj"]


def save_cache(path: str, version: Any, obj: Any) -> None:
    data = {"__cache_version": version, "obj": obj}
    dump_pickle(data, path)
