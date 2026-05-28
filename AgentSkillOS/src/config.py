"""
Unified configuration loader.

Priority: CLI arguments > Environment variables (.env) > config.yaml

Sensitive information (API keys) must be configured in .env, not in yaml.
config.yaml is REQUIRED - no default values are used for global keys.
"""
import os
from dataclasses import dataclass, field, fields
from pathlib import Path
from typing import TypeVar

import yaml
from dotenv import load_dotenv

# ===== Project paths =====
PROJECT_ROOT = Path(__file__).parent.parent
load_dotenv(PROJECT_ROOT / ".env")

# ===== Required global keys in config.yaml =====
_GLOBAL_REQUIRED_KEYS = [
    "skill_group",
    "max_skills",
    "prune_enabled",
    "port",
    "manager",
    "orchestrator",
]

# Cache TTL lower bound (1 year)
MIN_CACHE_TTL_SECONDS = 31_536_000

# ===== Frozen dataclass schemas for plugin config =====

T = TypeVar("T")


@dataclass(frozen=True)
class RetryConfig:
    base_delay: float = 1.0
    max_retries: int = 3


@dataclass(frozen=True)
class TreeBuildConfig:
    max_workers: int = 4
    caching: bool = True
    num_retries: int = 3
    timeout: float = 600.0
    deterministic_prompts: bool = True
    discovery_seed: int = 42
    prompt_fingerprint_version: str = "v1"
    cache_observability: bool = True


@dataclass(frozen=True)
class TreeSearchConfig:
    max_parallel: int = 5
    temperature: float = 0.3
    timeout: float = 600.0
    caching: bool = True


# Layering config classes (defined before TreeManagerConfig to avoid forward references)
@dataclass(frozen=True)
class DormantSearchConfig:
    """Configuration for dormant skill search."""
    keyword_enabled: bool = True      # Enable keyword search
    cache_ttl: int = MIN_CACHE_TTL_SECONDS

    def __post_init__(self):
        """Clamp TTL to at least one year."""
        try:
            ttl = int(self.cache_ttl)
        except (TypeError, ValueError):
            ttl = MIN_CACHE_TTL_SECONDS
        if ttl < MIN_CACHE_TTL_SECONDS:
            ttl = MIN_CACHE_TTL_SECONDS
        object.__setattr__(self, "cache_ttl", ttl)


_VALID_LAYERING_MODES = {"disabled", "directory", "install-count"}


@dataclass(frozen=True)
class LayeringConfig:
    """Configuration for active/dormant skill layering strategy.

    mode controls how layering works:
    - "disabled": no layering (default)
    - "directory": dormant skills live in a separate directory
    - "install-count": dormant/active split based on install counts
    """
    mode: str = "disabled"            # "disabled" | "directory" | "install-count"
    dormant_skills_dir: str = ""      # path relative to project root, for mode=directory
    active_threshold: int = 50        # Top N skills to keep active (for mode=install-count)
    max_dormant_suggestions: int = 10 # Max dormant skills to suggest
    dormant_search: DormantSearchConfig = field(default_factory=DormantSearchConfig)
    installs_data_path: str = "tools/skills_downloader_from_skillssh/skills_scraped.json"

    def __post_init__(self):
        if self.mode not in _VALID_LAYERING_MODES:
            raise ValueError(
                f"Invalid layering mode: {self.mode!r}. "
                f"Must be one of {sorted(_VALID_LAYERING_MODES)}"
            )
        if self.mode == "directory" and not self.dormant_skills_dir:
            raise ValueError(
                "dormant_skills_dir is required when layering mode is 'directory'. "
                "Set managers.tree.layering.dormant_skills_dir in config.yaml."
            )

    @property
    def is_enabled(self) -> bool:
        return self.mode != "disabled"

    @property
    def is_directory_mode(self) -> bool:
        return self.mode == "directory"

    @property
    def is_install_count_mode(self) -> bool:
        return self.mode == "install-count"


@dataclass(frozen=True)
class TreeManagerConfig:
    branching_factor: int = 8
    max_depth: int = 6
    build: TreeBuildConfig = field(default_factory=TreeBuildConfig)
    search: TreeSearchConfig = field(default_factory=TreeSearchConfig)
    layering: LayeringConfig = field(default_factory=LayeringConfig)


def _default_runtime_model() -> str:
    """Get default runtime model from env or fallback to 'sonnet'."""
    return os.environ.get("ANTHROPIC_MODEL", "sonnet")


@dataclass(frozen=True)
class RuntimeConfig:
    """Shared runtime config for all orchestrators (maps to SkillClient params)."""
    model: str = field(default_factory=_default_runtime_model)
    execution_timeout: float = 0.0       # 0 = no timeout
    summary_max_length: int = 500


@dataclass(frozen=True)
class DagOrchestratorConfig:
    node_timeout: float = 3600.0
    max_concurrent: int = 6
    batch_auto_plan: int = 0  # Plan index for batch/headless mode (0=quality, 1=speed, 2=simplicity)
    runtime: RuntimeConfig = field(default_factory=RuntimeConfig)

    def __post_init__(self):
        if not (0 <= self.batch_auto_plan <= 2):
            raise ValueError(
                f"batch_auto_plan must be 0-2, got {self.batch_auto_plan}. "
                f"(0=quality, 1=speed, 2=simplicity)"
            )


@dataclass(frozen=True)
class FreestyleOrchestratorConfig:
    runtime: RuntimeConfig = field(default_factory=RuntimeConfig)


@dataclass(frozen=True)
class DirectOrchestratorConfig:
    runtime: RuntimeConfig = field(default_factory=RuntimeConfig)


@dataclass(frozen=True)
class VectorBuildConfig:
    batch_size: int = 100
    max_workers: int = 4
    caching: bool = True


@dataclass(frozen=True)
class VectorManagerConfig:
    top_k: int = 10
    collection_name: str = "skills"
    build: VectorBuildConfig = field(default_factory=VectorBuildConfig)


# Registry mapping plugin names to their config dataclass
@dataclass(frozen=True)
class DirectManagerConfig:
    """No configuration needed — directly provides all skills to agent."""
    pass


_MANAGER_SCHEMAS: dict[str, type] = {
    "tree": TreeManagerConfig,
    "vector": VectorManagerConfig,
    "direct": DirectManagerConfig,
}

_ORCHESTRATOR_SCHEMAS: dict[str, type] = {
    "dag": DagOrchestratorConfig,
    "free-style": FreestyleOrchestratorConfig,
    "no-skill": DirectOrchestratorConfig,
}


def _build_nested_dataclass(cls: type[T], raw: dict | None) -> T:
    """Recursively construct a frozen dataclass from a raw dict.

    Missing keys fall back to dataclass field defaults.
    Extra keys are silently ignored.
    """
    if raw is None:
        raw = {}

    kwargs = {}
    for f in fields(cls):
        if f.name not in raw:
            continue
        value = raw[f.name]
        # Check if the field type is itself a dataclass
        if hasattr(f.type, "__dataclass_fields__"):
            value = _build_nested_dataclass(f.type, value if isinstance(value, dict) else {})
        kwargs[f.name] = value

    return cls(**kwargs)


class Config:
    """
    Unified configuration loader. Priority: CLI > ENV > YAML

    Usage:
        cfg = get_config()
        cfg.skill_group          # global (from yaml)
        cfg.llm_model            # from .env
        cfg.manager_config()     # TreeManagerConfig (or other based on active manager)
        cfg.orchestrator_config()  # DagOrchestratorConfig (or other)
        cfg.core_retry()         # RetryConfig
    """

    _yaml_cache = None
    _instance = None
    _config_path = None

    def __init__(self, cli_args: dict = None, config_path: str = None):
        self._cli = cli_args or {}
        if config_path:
            Config._config_path = Path(config_path)
        if Config._yaml_cache is None:
            Config._yaml_cache = self._load_yaml()

    @classmethod
    def get_instance(cls, cli_args: dict = None, config_path: str = None) -> "Config":
        """Get singleton instance, optionally updating CLI args."""
        if cls._instance is None:
            cls._instance = cls(cli_args, config_path=config_path)
        elif cli_args:
            cls._instance._cli.update(cli_args)
        return cls._instance

    @classmethod
    def reset(cls):
        """Reset singleton (for testing)."""
        cls._instance = None
        cls._yaml_cache = None
        cls._config_path = None

    def _load_yaml(self) -> dict:
        """Load config.yaml with validation."""
        path = Config._config_path or (PROJECT_ROOT / "config" / "config.yaml")
        if not path.exists():
            raise FileNotFoundError(
                f"Configuration file not found: {path}\n"
                "Please copy config/config.yaml.example to config/config.yaml and modify as needed."
            )

        with open(path, encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}

        missing = [k for k in _GLOBAL_REQUIRED_KEYS if k not in data]
        if missing:
            raise ValueError(f"config.yaml missing required keys: {missing}")

        return data

    def _get(self, key: str, env_key: str = None):
        """Get a top-level config value with priority: CLI > ENV > yaml."""
        if key in self._cli and self._cli[key] is not None:
            return self._cli[key]
        if env_key and os.getenv(env_key):
            return os.getenv(env_key)
        if Config._yaml_cache and key in Config._yaml_cache:
            return Config._yaml_cache[key]
        raise KeyError(f"config.yaml missing required key: {key}")

    # ===== Nested config accessors =====

    def core_retry(self) -> RetryConfig:
        """Get shared retry configuration from core.retry block."""
        core = Config._yaml_cache.get("core", {}) if Config._yaml_cache else {}
        raw = core.get("retry", {})
        return _build_nested_dataclass(RetryConfig, raw)

    def manager_config(self, name: str = None) -> object:
        """Get manager plugin config as a frozen dataclass.

        Args:
            name: Manager name. Defaults to the active manager from config.
        """
        name = name or self.manager
        schema = _MANAGER_SCHEMAS.get(name)
        if schema is None:
            return None
        managers = Config._yaml_cache.get("managers", {}) if Config._yaml_cache else {}
        raw = managers.get(name, {})
        return _build_nested_dataclass(schema, raw)

    def orchestrator_config(self, name: str = None) -> object:
        """Get orchestrator plugin config as a frozen dataclass.

        Args:
            name: Orchestrator name. Defaults to the active orchestrator from config.
        """
        name = name or self._get("orchestrator")
        schema = _ORCHESTRATOR_SCHEMAS.get(name)
        if schema is None:
            return None
        orchestrators = Config._yaml_cache.get("orchestrators", {}) if Config._yaml_cache else {}
        raw = orchestrators.get(name, {})
        return _build_nested_dataclass(schema, raw)

    def layering_config(self) -> LayeringConfig:
        """Get layering configuration from managers.tree.layering."""
        managers = Config._yaml_cache.get("managers", {}) if Config._yaml_cache else {}
        tree_config = managers.get("tree", {})
        raw = tree_config.get("layering", {})

        # Detect legacy config: 'enabled' was replaced by 'mode' in the tri-state refactor
        if "enabled" in raw:
            raise ValueError(
                "The 'layering.enabled' field has been removed. "
                "Use 'layering.mode' instead:\n"
                "  mode: 'install-count'  (replaces enabled: true)\n"
                "  mode: 'directory'      (new directory-based layering)\n"
                "  mode: 'disabled'       (replaces enabled: false)\n"
                "Please update managers.tree.layering in config.yaml."
            )

        return _build_nested_dataclass(LayeringConfig, raw)

    # ===== Global properties =====

    @property
    def skill_group(self) -> str:
        return self._get("skill_group")

    @property
    def max_skills(self) -> int:
        return int(self._get("max_skills"))

    @property
    def prune_enabled(self) -> bool:
        val = self._get("prune_enabled", "PRUNE_ENABLED")
        if isinstance(val, bool):
            return val
        return str(val).lower() == "true"

    @property
    def port(self) -> int:
        return int(self._get("port"))

    @property
    def manager(self) -> str:
        return str(self._get("manager"))

    # ===== LLM Configuration (from .env only) =====

    @property
    def llm_model(self) -> str:
        return os.getenv("LLM_MODEL", "openai/gpt-4o-mini")

    @property
    def llm_base_url(self) -> str:
        return os.getenv("LLM_BASE_URL") or os.getenv("OPENAI_BASE_URL")

    @property
    def llm_api_key(self) -> str:
        return os.getenv("LLM_API_KEY") or os.getenv("OPENAI_API_KEY")

    @property
    def llm_max_retries(self) -> int:
        return int(os.getenv("LLM_MAX_RETRIES", "3"))

    # ===== Embedding Configuration (from .env only) =====

    @property
    def embedding_model(self) -> str:
        return os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")

    @property
    def embedding_base_url(self) -> str:
        return os.getenv("EMBEDDING_BASE_URL") or os.getenv("OPENAI_BASE_URL")

    @property
    def embedding_api_key(self) -> str:
        return os.getenv("EMBEDDING_API_KEY") or os.getenv("OPENAI_API_KEY")

    @property
    def embedding_batch_size(self) -> int:
        return int(os.getenv("EMBEDDING_BATCH_SIZE", "100"))

    @property
    def chroma_persist_dir(self) -> str:
        return os.getenv("CHROMA_PERSIST_DIR", "data/vector_stores")


# ===== Global config instance =====
def get_config(cli_args: dict = None, config_path: str = None) -> Config:
    """Get global config instance."""
    return Config.get_instance(cli_args, config_path=config_path)
