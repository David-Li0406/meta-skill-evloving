#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import shlex
import subprocess
import sys
import time
from functools import lru_cache
from concurrent.futures import ThreadPoolExecutor, as_completed
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any


DEFAULT_ROLES = ("pm", "arch", "prod", "dev", "qa", "ops", "coord", "liaison")
DEFAULT_ROLE_SCOPES: dict[str, str] = {
    "coord": "internal routing + escalation triage",
    "liaison": "user communication + clarifications",
    "pm": "overall delivery / milestone planning",
}
FULL_NAME_RE = re.compile(r"^.+-[0-9]{8}-[0-9]{6}-[0-9]+$")

_MSG_SEQ_FILE = "message_seq.json"
_MSG_ID_WIDTH = 6

_INBOX_DIR = "inbox"
_INBOX_UNREAD_DIR = "unread"
_INBOX_READ_DIR = "read"
_INBOX_OVERFLOW_DIR = "overflow"
_INBOX_MAX_UNREAD_DEFAULT = 15

_REQUESTS_DIR = "requests"
_REQUEST_META_FILE = "meta.json"
_REQUEST_RESPONSES_DIR = "responses"
_REQUEST_STATUS_OPEN = "open"
_REQUEST_STATUS_DONE = "done"
_REQUEST_STATUS_TIMED_OUT = "timed_out"
_REQUEST_TARGET_STATUS_PENDING = "pending"
_REQUEST_TARGET_STATUS_REPLIED = "replied"
_REQUEST_TARGET_STATUS_BLOCKED = "blocked"
_REQUEST_DEADLINE_DEFAULT_S = 3600.0
_REQUEST_BLOCK_SNOOZE_DEFAULT_S = 900.0  # 15 minutes

_STATE_DIR = "state"
_STATE_STATUS_WORKING = "working"
_STATE_STATUS_DRAINING = "draining"
_STATE_STATUS_IDLE = "idle"
_STATE_STATUSES = {_STATE_STATUS_WORKING, _STATE_STATUS_DRAINING, _STATE_STATUS_IDLE}

_DRIVE_MODE_RUNNING = "running"
_DRIVE_MODE_STANDBY = "standby"
_DRIVE_MODES = {_DRIVE_MODE_RUNNING, _DRIVE_MODE_STANDBY}

_STATE_INBOX_CHECK_INTERVAL_DEFAULT = 60.0
_STATE_IDLE_WAKE_DELAY_DEFAULT = 60.0
_STATE_WATCH_INTERVAL_DEFAULT = 60.0
_STATE_ACTIVITY_WINDOW_DEFAULT = 120.0
_STATE_ACTIVE_GRACE_PERIOD_DEFAULT = 180.0
_STATE_ACTIVITY_CAPTURE_LINES_DEFAULT = 200
_STATE_AUTO_ENTER_ENABLED_DEFAULT = True
_STATE_AUTO_ENTER_COOLDOWN_DEFAULT = 30.0
_STATE_AUTO_ENTER_TAIL_WINDOW_LINES_DEFAULT = 80
_STATE_AUTO_ENTER_PATTERNS_DEFAULT = ("3. No, and tell Codex what to do differently (esc)",)
_DRIVE_MODE_DEFAULT = _DRIVE_MODE_RUNNING
_DRIVE_DRIVER_ROLE_DEFAULT = "coord"
_DRIVE_BACKUP_ROLE_DEFAULT = "pm"
_DRIVE_COOLDOWN_DEFAULT = 600.0
_STATE_WORKING_STALE_THRESHOLD_DEFAULT = 180.0
_STATE_WORKING_ALERT_COOLDOWN_DEFAULT = 600.0
_STATE_WAKE_MESSAGE_DEFAULT = "INBOX wake: you have unread messages. Run: bash .codex/skills/ai-team-workflow/scripts/atwf inbox"
_STATE_REPLY_WAKE_MESSAGE_DEFAULT = "REPLY wake: you have pending reply-needed. Run: bash .codex/skills/ai-team-workflow/scripts/atwf reply-needed"


def _now() -> str:
    return datetime.now().isoformat(timespec="seconds")


def _parse_iso_dt(raw: str) -> datetime | None:
    s = (raw or "").strip()
    if not s:
        return None
    try:
        return datetime.fromisoformat(s)
    except Exception:
        return None


def _eprint(msg: str) -> None:
    print(msg, file=sys.stderr)


def _msg_seq_path(team_dir: Path) -> Path:
    return team_dir / _MSG_SEQ_FILE


def _format_msg_id(n: int) -> str:
    return str(max(0, int(n))).zfill(_MSG_ID_WIDTH)


def _next_msg_id(team_dir: Path) -> str:
    lock = team_dir / ".lock"
    seq_path = _msg_seq_path(team_dir)
    with _locked(lock):
        data = _read_json(seq_path)
        next_id_raw = data.get("next_id", 1)
        try:
            next_id = int(next_id_raw)
        except Exception:
            next_id = 1
        if next_id < 1:
            next_id = 1
        data.setdefault("created_at", _now())
        data["updated_at"] = _now()
        data["next_id"] = next_id + 1
        _write_json_atomic(seq_path, data)
    return _format_msg_id(next_id)


def _wrap_team_message(
    team_dir: Path,
    *,
    kind: str,
    sender_full: str,
    sender_role: str | None,
    to_full: str,
    body: str,
    msg_id: str | None = None,
) -> str:
    resolved_id = (msg_id or "").strip() or _next_msg_id(team_dir)
    kind_s = kind.strip() or "send"
    sender_full_s = sender_full.strip() or "unknown"
    to_full_s = to_full.strip() or "unknown"
    role_s = (sender_role or "").strip()
    role_part = f" role={role_s}" if role_s else ""
    header = f"[ATWF-MSG id={resolved_id} kind={kind_s} from={sender_full_s} to={to_full_s}{role_part} ts={_now()}]"
    body_s = (body or "").rstrip()
    if body_s:
        return f"{header}\n{body_s}\n[ATWF-END id={resolved_id}]\n"
    return f"{header}\n[ATWF-END id={resolved_id}]\n"


def _slugify(raw: str) -> str:
    s = re.sub(r"[^a-zA-Z0-9_-]+", "-", (raw or "").strip())
    s = "-".join(seg for seg in s.split("-") if seg)
    return s or "unknown"


def _inbox_root(team_dir: Path) -> Path:
    return team_dir / _INBOX_DIR


def _requests_root(team_dir: Path) -> Path:
    return team_dir / _REQUESTS_DIR


def _state_root(team_dir: Path) -> Path:
    return team_dir / _STATE_DIR


def _state_lock_path(team_dir: Path) -> Path:
    return _state_root(team_dir) / ".lock"


def _inbox_member_dir(team_dir: Path, *, base: str) -> Path:
    return _inbox_root(team_dir) / _slugify(base)


def _inbox_thread_dir(team_dir: Path, *, to_base: str, from_base: str, state: str) -> Path:
    state = state.strip().lower()
    if state not in {_INBOX_UNREAD_DIR, _INBOX_READ_DIR, _INBOX_OVERFLOW_DIR}:
        state = _INBOX_UNREAD_DIR
    return _inbox_member_dir(team_dir, base=to_base) / state / f"from-{_slugify(from_base)}"


def _inbox_message_path(team_dir: Path, *, to_base: str, from_base: str, state: str, msg_id: str) -> Path:
    return _inbox_thread_dir(team_dir, to_base=to_base, from_base=from_base, state=state) / f"{msg_id}.md"


def _request_dir(team_dir: Path, *, request_id: str) -> Path:
    return _requests_root(team_dir) / request_id.strip()


def _request_meta_path(team_dir: Path, *, request_id: str) -> Path:
    return _request_dir(team_dir, request_id=request_id) / _REQUEST_META_FILE


def _request_responses_dir(team_dir: Path, *, request_id: str) -> Path:
    return _request_dir(team_dir, request_id=request_id) / _REQUEST_RESPONSES_DIR


def _reply_drive_state_path(team_dir: Path) -> Path:
    return _state_root(team_dir) / "reply_drive.json"


def _expand_path(path: str) -> Path:
    p = Path(path).expanduser()
    if not p.is_absolute():
        p = (Path.cwd() / p).resolve()
    return p


def _expand_path_from(base: Path, path: str) -> Path:
    p = Path(path).expanduser()
    if not p.is_absolute():
        p = (base / p).resolve()
    return p


def _config_file() -> Path:
    return Path(__file__).resolve().with_name("atwf_config.yaml")


def _parse_simple_yaml_kv(raw: str) -> dict[str, str]:
    out: dict[str, str] = {}
    for line in raw.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if ":" not in stripped:
            continue
        key, value = stripped.split(":", 1)
        key = key.strip()
        if not key:
            continue
        value = value.strip()
        if not value:
            out[key] = ""
            continue
        if value[0] in {"'", '"'}:
            q = value[0]
            if value.endswith(q) and len(value) >= 2:
                out[key] = value[1:-1]
            else:
                out[key] = value[1:]
            continue
        if "#" in value:
            for i, ch in enumerate(value):
                if ch == "#" and (i == 0 or value[i - 1].isspace()):
                    value = value[:i].strip()
                    break
        out[key] = value.strip()
    return out


def _read_simple_yaml_kv(path: Path) -> dict[str, str]:
    try:
        raw = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return {}
    except OSError:
        return {}

    return _parse_simple_yaml_kv(raw)


def _read_yaml_or_json(path: Path) -> dict[str, Any]:
    try:
        raw = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return {}
    except OSError:
        return {}

    raw_s = raw.strip()
    if not raw_s:
        return {}

    # Config files may be provided as JSON (twf supports *.json fallback) or
    # YAML. Prefer JSON when it clearly looks like JSON.
    if raw_s.startswith("{"):
        try:
            parsed = json.loads(raw_s)
        except Exception:
            parsed = None
        if isinstance(parsed, dict):
            return parsed

    try:
        import yaml  # type: ignore

        parsed = yaml.safe_load(raw)
        if isinstance(parsed, dict):
            return parsed
    except Exception:
        pass

    # Best-effort fallback for environments without PyYAML or invalid YAML.
    return _parse_simple_yaml_kv(raw)


def _cfg_get(cfg: dict[str, Any], path: tuple[str, ...]) -> Any:
    cur: Any = cfg
    for key in path:
        if not isinstance(cur, dict):
            return None
        cur = cur.get(key)
    return cur


def _cfg_get_str(cfg: dict[str, Any], *paths: tuple[str, ...], default: str = "") -> str:
    for p in paths:
        v = _cfg_get(cfg, p)
        if isinstance(v, str):
            return v.strip()
    return default


@dataclass(frozen=True)
class TeamPolicy:
    root_role: str
    enabled_roles: frozenset[str]
    can_hire: dict[str, frozenset[str]]

    broadcast_allowed_roles: frozenset[str]
    broadcast_exclude_roles: frozenset[str]

    comm_allow_parent_child: bool
    comm_direct_allow: dict[str, frozenset[str]]
    comm_require_handoff: bool
    comm_handoff_creators: frozenset[str]


def _norm_role(raw: Any) -> str:
    if not isinstance(raw, str):
        return ""
    return raw.strip().lower()


def _role_set(raw: Any) -> set[str]:
    if isinstance(raw, str):
        parts = [p.strip() for p in raw.split(",")]
        return {p.lower() for p in parts if p}
    if isinstance(raw, list):
        out: set[str] = set()
        for item in raw:
            r = _norm_role(item)
            if r:
                out.add(r)
        return out
    return set()


def _available_template_roles() -> set[str]:
    td = _templates_dir()
    if not td.is_dir():
        return set()
    roles: set[str] = set()
    for p in td.glob("*.md"):
        if p.name == "command_rules.md":
            continue
        stem = p.stem.strip().lower()
        if stem:
            roles.add(stem)
    return roles


def _role_map(raw: Any) -> dict[str, set[str]]:
    if not isinstance(raw, dict):
        return {}
    out: dict[str, set[str]] = {}
    for k, v in raw.items():
        key = _norm_role(k)
        if not key:
            continue
        out[key] = _role_set(v)
    return out


@lru_cache(maxsize=1)
def _policy() -> TeamPolicy:
    cfg = _read_yaml_or_json(_config_file())

    templates = _available_template_roles()
    default_enabled = set(DEFAULT_ROLES) & templates if templates else set(DEFAULT_ROLES)

    enabled = _role_set(_cfg_get(cfg, ("team", "policy", "enabled_roles")))
    if not enabled:
        enabled = set(default_enabled)

    root_role = _norm_role(_cfg_get_str(cfg, ("team", "policy", "root_role"), default="coord")) or "coord"

    if enabled and root_role not in enabled:
        raise SystemExit(f"❌ policy.root_role={root_role!r} is not in enabled_roles")

    if templates:
        missing_templates = sorted(r for r in enabled if (td := (_templates_dir() / f"{r}.md")) and not td.is_file())
        if missing_templates:
            raise SystemExit(f"❌ enabled_roles missing templates/*.md: {', '.join(missing_templates)}")

    can_hire_raw = _role_map(_cfg_get(cfg, ("team", "policy", "can_hire")))
    can_hire: dict[str, frozenset[str]] = {}
    for parent_role, children in can_hire_raw.items():
        if parent_role not in enabled:
            continue
        filtered = {c for c in children if c in enabled}
        can_hire[parent_role] = frozenset(sorted(filtered))

    bc_allowed = _role_set(_cfg_get(cfg, ("team", "policy", "broadcast", "allowed_roles")))
    if not bc_allowed:
        bc_allowed = {root_role}
    bc_allowed = {r for r in bc_allowed if r in enabled}

    bc_exclude = _role_set(_cfg_get(cfg, ("team", "policy", "broadcast", "exclude_roles")))
    bc_exclude = {r for r in bc_exclude if r in enabled}

    comm_allow_parent_child = _cfg_get(cfg, ("team", "policy", "comm", "allow_parent_child"))
    if not isinstance(comm_allow_parent_child, bool):
        comm_allow_parent_child = True

    comm_require_handoff = _cfg_get(cfg, ("team", "policy", "comm", "require_handoff"))
    if not isinstance(comm_require_handoff, bool):
        comm_require_handoff = True

    handoff_creators = _role_set(_cfg_get(cfg, ("team", "policy", "comm", "handoff_creators")))
    if not handoff_creators:
        handoff_creators = {root_role}
    handoff_creators = {r for r in handoff_creators if r in enabled}

    direct_allow_raw = _role_map(_cfg_get(cfg, ("team", "policy", "comm", "direct_allow")))
    direct_allow: dict[str, set[str]] = {r: set() for r in enabled}
    for a, bs in direct_allow_raw.items():
        if a not in enabled:
            continue
        for b in bs:
            if b not in enabled:
                continue
            direct_allow.setdefault(a, set()).add(b)
            direct_allow.setdefault(b, set()).add(a)

    pairs_raw = _cfg_get(cfg, ("team", "policy", "comm", "direct_allow_pairs"))
    if isinstance(pairs_raw, list):
        for item in pairs_raw:
            if not isinstance(item, (list, tuple)) or len(item) != 2:
                continue
            a = _norm_role(item[0])
            b = _norm_role(item[1])
            if not a or not b or a not in enabled or b not in enabled:
                continue
            direct_allow.setdefault(a, set()).add(b)
            direct_allow.setdefault(b, set()).add(a)

    direct_allow_frozen: dict[str, frozenset[str]] = {}
    for r in enabled:
        direct_allow_frozen[r] = frozenset(sorted(direct_allow.get(r, set())))

    return TeamPolicy(
        root_role=root_role,
        enabled_roles=frozenset(sorted(enabled)),
        can_hire=can_hire,
        broadcast_allowed_roles=frozenset(sorted(bc_allowed)),
        broadcast_exclude_roles=frozenset(sorted(bc_exclude)),
        comm_allow_parent_child=bool(comm_allow_parent_child),
        comm_direct_allow=direct_allow_frozen,
        comm_require_handoff=bool(comm_require_handoff),
        comm_handoff_creators=frozenset(sorted(handoff_creators)),
    )


def _default_team_dir() -> Path:
    env_dir = os.environ.get("AITWF_DIR", "").strip()
    if env_dir:
        return _expand_path(env_dir)

    skill_dir = _skill_dir()
    cfg = _read_yaml_or_json(_config_file())
    share_dir = _cfg_get_str(cfg, ("share", "dir"), ("share_dir",))
    if share_dir:
        return _expand_path_from(skill_dir, share_dir)

    return skill_dir / "share"


def _paused_marker_path(team_dir: Path) -> Path:
    return team_dir / ".paused"


def _set_paused(team_dir: Path, *, reason: str) -> None:
    team_dir.mkdir(parents=True, exist_ok=True)
    content = f"paused_at: {_now()}\n"
    reason = reason.strip()
    if reason:
        content += f"reason: {reason}\n"
    _write_text_atomic(_paused_marker_path(team_dir), content)


def _clear_paused(team_dir: Path) -> None:
    try:
        _paused_marker_path(team_dir).unlink()
    except FileNotFoundError:
        return
    except OSError:
        return


def _read_optional_message(args: argparse.Namespace, *, attr: str) -> str:
    msg = str(getattr(args, attr, "") or "").strip()
    if msg:
        return msg
    stdin_msg = _forward_stdin()
    return (stdin_msg or "").strip()


def _registry_path(team_dir: Path) -> Path:
    override = os.environ.get("AITWF_REGISTRY", "").strip()
    return _expand_path(override) if override else team_dir / "registry.json"


def _skill_dir() -> Path:
    return Path(__file__).resolve().parents[1]


def _templates_dir() -> Path:
    return _skill_dir() / "templates"


def _resolve_twf() -> Path:
    override = os.environ.get("AITWF_TWF", "").strip()
    if override:
        p = _expand_path(override)
        if p.is_file():
            return p
        raise SystemExit(f"❌ AITWF_TWF points to missing file: {p}")

    skills_dir = _skill_dir().parent
    sibling = skills_dir / "tmux-workflow" / "scripts" / "twf"
    if sibling.is_file():
        return sibling

    global_path = Path.home() / ".codex" / "skills" / "tmux-workflow" / "scripts" / "twf"
    if global_path.is_file():
        return global_path

    raise SystemExit(
        "❌ tmux-workflow not found.\n"
        "   Expected `tmux-workflow/scripts/twf` next to this skill, or set AITWF_TWF=/path/to/twf."
    )


def _resolve_twf_config_path(twf: Path) -> Path | None:
    tmux_skill_dir = twf.resolve().parents[1]
    cfg_override = os.environ.get("TWF_CODEX_CMD_CONFIG", "").strip()
    if cfg_override:
        cfg_path = _expand_path(cfg_override)
    else:
        cfg_path = tmux_skill_dir / "scripts" / "twf_config.yaml"
        if not cfg_path.is_file():
            json_fallback = tmux_skill_dir / "scripts" / "twf_config.json"
            if json_fallback.is_file():
                cfg_path = json_fallback

    return cfg_path if cfg_path.is_file() else None


def _resolve_twf_state_dir(twf: Path) -> Path:
    # Mirror twf's state dir resolution (subset):
    # - env override: TWF_STATE_DIR
    # - config: scripts/twf_config.yaml (auto/global/manual)
    override = os.environ.get("TWF_STATE_DIR", "").strip()
    if override:
        return _expand_path(override)

    tmux_skill_dir = twf.resolve().parents[1]
    cfg_path = _resolve_twf_config_path(twf)
    cfg = _read_yaml_or_json(cfg_path) if cfg_path else {}

    mode = (_cfg_get_str(cfg, ("twf", "state_dir", "mode"), ("twf_state_dir_mode",), default="auto") or "auto").lower()
    if mode not in {"auto", "global", "manual"}:
        mode = "auto"

    if mode == "global":
        return Path.home() / ".twf"

    if mode == "manual":
        raw = _cfg_get_str(cfg, ("twf", "state_dir", "dir"), ("twf_state_dir",))
        if not raw:
            raise SystemExit(f"❌ twf_state_dir_mode=manual but twf_state_dir is empty in: {cfg_path}")
        return _expand_path(raw)

    return tmux_skill_dir / ".twf"


_TRUE_STRINGS = frozenset({"1", "true", "yes", "y", "on"})


def _as_bool(value: object, *, default: bool = False) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, int):
        return bool(value)
    if isinstance(value, str):
        return value.strip().lower() in _TRUE_STRINGS
    return default


def _cfg_get_boolish(cfg: dict[str, Any], *paths: tuple[str, ...], default: bool = False) -> bool:
    for p in paths:
        v = _cfg_get(cfg, p)
        if v is None:
            continue
        return _as_bool(v, default=default)
    return default


def _cfg_get_floatish(cfg: dict[str, Any], *paths: tuple[str, ...], default: float) -> float:
    for p in paths:
        v = _cfg_get(cfg, p)
        if v is None:
            continue
        try:
            return float(v)  # type: ignore[arg-type]
        except Exception:
            return float(default)
    return float(default)


def _cfg_get_intish(cfg: dict[str, Any], *paths: tuple[str, ...], default: int) -> int:
    for p in paths:
        v = _cfg_get(cfg, p)
        if v is None:
            continue
        try:
            return int(v)  # type: ignore[arg-type]
        except Exception:
            return int(default)
    return int(default)


def _cfg_get_boolish(cfg: dict[str, Any], *paths: tuple[str, ...], default: bool) -> bool:
    for p in paths:
        v = _cfg_get(cfg, p)
        if isinstance(v, bool):
            return v
        if v is None:
            continue
        if isinstance(v, (int, float)):
            return bool(v)
        if isinstance(v, str):
            s = v.strip().lower()
            if s in {"1", "true", "yes", "y", "on"}:
                return True
            if s in {"0", "false", "no", "n", "off"}:
                return False
    return bool(default)


def _cfg_get_str_list(cfg: dict[str, Any], path: tuple[str, ...], *, default: tuple[str, ...]) -> list[str]:
    v = _cfg_get(cfg, path)
    if isinstance(v, list):
        out: list[str] = []
        for item in v:
            if isinstance(item, str) and item.strip():
                out.append(item.strip())
        if out:
            return out
    if isinstance(v, str) and v.strip():
        return [v.strip()]
    return [s for s in default if s]


@lru_cache(maxsize=1)
def _inbox_max_unread_per_thread() -> int:
    cfg = _read_yaml_or_json(_config_file())
    n = _cfg_get_intish(cfg, ("team", "messaging", "inbox", "max_unread_per_thread"), default=_INBOX_MAX_UNREAD_DEFAULT)
    if n < 1:
        n = 1
    if n > 100:
        n = 100
    return n


@lru_cache(maxsize=1)
def _state_inbox_check_interval_s() -> float:
    cfg = _read_yaml_or_json(_config_file())
    n = _cfg_get_floatish(cfg, ("team", "state", "inbox_check_interval"), default=_STATE_INBOX_CHECK_INTERVAL_DEFAULT)
    if n < 5:
        n = 5.0
    if n > 3600:
        n = 3600.0
    return float(n)


@lru_cache(maxsize=1)
def _state_idle_wake_delay_s() -> float:
    cfg = _read_yaml_or_json(_config_file())
    n = _cfg_get_floatish(cfg, ("team", "state", "idle_wake_delay"), default=_STATE_IDLE_WAKE_DELAY_DEFAULT)
    if n < 5:
        n = 5.0
    if n > 3600:
        n = 3600.0
    return float(n)


@lru_cache(maxsize=1)
def _state_watch_interval_s() -> float:
    cfg = _read_yaml_or_json(_config_file())
    n = _cfg_get_floatish(cfg, ("team", "state", "watch_interval"), default=_STATE_WATCH_INTERVAL_DEFAULT)
    if n < 5:
        n = 5.0
    if n > 3600:
        n = 3600.0
    return float(n)


@lru_cache(maxsize=1)
def _state_activity_window_s() -> float:
    cfg = _read_yaml_or_json(_config_file())
    n = _cfg_get_floatish(cfg, ("team", "state", "activity_window"), default=_STATE_ACTIVITY_WINDOW_DEFAULT)
    if n < 10:
        n = 10.0
    if n > 3600:
        n = 3600.0
    return float(n)


@lru_cache(maxsize=1)
def _state_active_grace_period_s() -> float:
    cfg = _read_yaml_or_json(_config_file())
    n = _cfg_get_floatish(cfg, ("team", "state", "active_grace_period"), default=_STATE_ACTIVE_GRACE_PERIOD_DEFAULT)
    if n < 0:
        n = 0.0
    if n > 3600:
        n = 3600.0
    return float(n)


@lru_cache(maxsize=1)
def _state_activity_capture_lines() -> int:
    cfg = _read_yaml_or_json(_config_file())
    n = _cfg_get_intish(cfg, ("team", "state", "activity_capture_lines"), default=_STATE_ACTIVITY_CAPTURE_LINES_DEFAULT)
    if n < 20:
        n = 20
    if n > 5000:
        n = 5000
    return int(n)


@lru_cache(maxsize=1)
def _state_auto_enter_enabled() -> bool:
    cfg = _read_yaml_or_json(_config_file())
    return _cfg_get_boolish(cfg, ("team", "state", "auto_enter", "enabled"), default=_STATE_AUTO_ENTER_ENABLED_DEFAULT)


@lru_cache(maxsize=1)
def _state_auto_enter_cooldown_s() -> float:
    cfg = _read_yaml_or_json(_config_file())
    n = _cfg_get_floatish(cfg, ("team", "state", "auto_enter", "cooldown"), default=_STATE_AUTO_ENTER_COOLDOWN_DEFAULT)
    if n < 0:
        n = 0.0
    if n > 3600:
        n = 3600.0
    return float(n)


@lru_cache(maxsize=1)
def _state_auto_enter_tail_window_lines() -> int:
    cfg = _read_yaml_or_json(_config_file())
    n = _cfg_get_intish(cfg, ("team", "state", "auto_enter", "tail_window_lines"), default=_STATE_AUTO_ENTER_TAIL_WINDOW_LINES_DEFAULT)
    if n < 10:
        n = 10
    if n > 1000:
        n = 1000
    return int(n)


@lru_cache(maxsize=1)
def _state_auto_enter_patterns() -> list[str]:
    cfg = _read_yaml_or_json(_config_file())
    patterns = _cfg_get_str_list(cfg, ("team", "state", "auto_enter", "patterns"), default=_STATE_AUTO_ENTER_PATTERNS_DEFAULT)
    out: list[str] = []
    for p in patterns:
        s = (p or "").strip()
        if s and s not in out:
            out.append(s)
    return out


def _normalize_drive_mode(raw: str) -> str:
    s = (raw or "").strip().lower()
    if s in {"on", "enable", "enabled", "true", "1", "run", "running"}:
        return _DRIVE_MODE_RUNNING
    if s in {"off", "disable", "disabled", "false", "0", "standby", "idle"}:
        return _DRIVE_MODE_STANDBY
    return s


@lru_cache(maxsize=1)
def _drive_mode_config_default() -> str:
    cfg = _read_yaml_or_json(_config_file())
    raw_mode = _cfg_get_str(cfg, ("team", "drive", "mode"), default="")
    if raw_mode.strip():
        mode = _normalize_drive_mode(raw_mode)
        return mode if mode in _DRIVE_MODES else _DRIVE_MODE_DEFAULT
    enabled = _cfg_get_boolish(cfg, ("team", "drive", "enabled"), default=(True if _DRIVE_MODE_DEFAULT == _DRIVE_MODE_RUNNING else False))
    return _DRIVE_MODE_RUNNING if enabled else _DRIVE_MODE_STANDBY


def _drive_mode_config_hot() -> str:
    """
    Drive mode is controlled by config and must be hot-reloaded by the watcher.

    Requirement: only `team.drive.mode` is treated as authoritative and is re-read
    each watcher tick. Other config values remain cached and require watcher restart.
    """
    cfg = _read_yaml_or_json(_config_file())
    raw_mode = _cfg_get_str(cfg, ("team", "drive", "mode"), default="")
    if raw_mode.strip():
        mode = _normalize_drive_mode(raw_mode)
        return mode if mode in _DRIVE_MODES else _DRIVE_MODE_DEFAULT
    # Back-compat: older configs may use `team.drive.enabled`.
    return _drive_mode_config_default()


@lru_cache(maxsize=1)
def _drive_driver_role() -> str:
    cfg = _read_yaml_or_json(_config_file())
    role = _cfg_get_str(cfg, ("team", "drive", "driver_role"), default=_DRIVE_DRIVER_ROLE_DEFAULT)
    role = role.strip() or _policy().root_role
    return _require_role(role)


@lru_cache(maxsize=1)
def _drive_backup_role() -> str:
    cfg = _read_yaml_or_json(_config_file())
    role = _cfg_get_str(cfg, ("team", "drive", "backup_role"), default=_DRIVE_BACKUP_ROLE_DEFAULT)
    role = role.strip() or _DRIVE_BACKUP_ROLE_DEFAULT
    return _require_role(role)


@lru_cache(maxsize=1)
def _drive_cooldown_s() -> float:
    cfg = _read_yaml_or_json(_config_file())
    n = _cfg_get_floatish(cfg, ("team", "drive", "cooldown"), default=_DRIVE_COOLDOWN_DEFAULT)
    if n < 0:
        n = 0.0
    if n > 86400:
        n = 86400.0
    return float(n)


def _render_drive_template(template: str, *, iso_ts: str, msg_id: str) -> str:
    s = (template or "").replace("\r\n", "\n").replace("\r", "\n")
    s = s.replace("{{iso_ts}}", iso_ts)
    s = s.replace("{{msg_id}}", msg_id)
    s = s.replace("{{open_cmd}}", f"bash .codex/skills/ai-team-workflow/scripts/atwf inbox-open {msg_id}")
    return s


def _drive_message_body(*, iso_ts: str, msg_id: str) -> str:
    cfg = _read_yaml_or_json(_config_file())
    raw = _cfg_get_str(cfg, ("team", "drive", "message", "body"), default="")
    if raw.strip():
        return _render_drive_template(raw, iso_ts=iso_ts, msg_id=msg_id).rstrip() + "\n"
    default = (
        "[DRIVE] team stalled: ALL IDLE + INBOX EMPTY\n"
        "- detected_at: {{iso_ts}}\n"
        "- meaning: no one is driving work. This is an ABNORMAL STALL.\n"
        "\n"
        "1) Diagnose now:\n"
        "- atwf state\n"
        "- atwf list\n"
        "- atwf inbox (your own inbox)\n"
        "\n"
        'Summarize why the team reached "all idle + inbox empty", find the root cause, then re-drive the team back to work.\n'
    )
    return _render_drive_template(default, iso_ts=iso_ts, msg_id=msg_id)


def _drive_message_summary(*, iso_ts: str, msg_id: str) -> str:
    cfg = _read_yaml_or_json(_config_file())
    raw = _cfg_get_str(cfg, ("team", "drive", "message", "summary"), default="")
    if raw.strip():
        return _render_drive_template(raw, iso_ts=iso_ts, msg_id=msg_id).rstrip() + "\n"
    default = (
        "[DRIVE] team stalled: ALL IDLE + INBOX EMPTY\n"
        "inbox id={{msg_id}} (open: {{open_cmd}})\n"
        "Action: diagnose root cause, then re-drive the team back to work.\n"
    )
    return _render_drive_template(default, iso_ts=iso_ts, msg_id=msg_id)


@lru_cache(maxsize=1)
def _state_wake_message() -> str:
    cfg = _read_yaml_or_json(_config_file())
    msg = _cfg_get_str(cfg, ("team", "state", "wake_message"), default=_STATE_WAKE_MESSAGE_DEFAULT)
    return msg.strip() or _STATE_WAKE_MESSAGE_DEFAULT


@lru_cache(maxsize=1)
def _state_reply_wake_message() -> str:
    cfg = _read_yaml_or_json(_config_file())
    msg = _cfg_get_str(cfg, ("team", "state", "reply_wake_message"), default=_STATE_REPLY_WAKE_MESSAGE_DEFAULT)
    return msg.strip() or _STATE_REPLY_WAKE_MESSAGE_DEFAULT


@lru_cache(maxsize=1)
def _request_deadline_s() -> float:
    cfg = _read_yaml_or_json(_config_file())
    n = _cfg_get_floatish(cfg, ("team", "reply", "deadline"), default=_REQUEST_DEADLINE_DEFAULT_S)
    if n < 60:
        n = 60.0
    if n > 86400:
        n = 86400.0
    return float(n)


@lru_cache(maxsize=1)
def _request_block_snooze_default_s() -> float:
    cfg = _read_yaml_or_json(_config_file())
    n = _cfg_get_floatish(cfg, ("team", "reply", "blocked_snooze"), default=_REQUEST_BLOCK_SNOOZE_DEFAULT_S)
    if n < 30:
        n = 30.0
    if n > 86400:
        n = 86400.0
    return float(n)


@lru_cache(maxsize=1)
def _state_working_stale_threshold_s() -> float:
    cfg = _read_yaml_or_json(_config_file())
    n = _cfg_get_floatish(cfg, ("team", "state", "working_stale_threshold"), default=_STATE_WORKING_STALE_THRESHOLD_DEFAULT)
    if n < 30:
        n = 30.0
    if n > 3600:
        n = 3600.0
    return float(n)


@lru_cache(maxsize=1)
def _state_working_alert_cooldown_s() -> float:
    cfg = _read_yaml_or_json(_config_file())
    n = _cfg_get_floatish(cfg, ("team", "state", "working_alert_cooldown"), default=_STATE_WORKING_ALERT_COOLDOWN_DEFAULT)
    if n < 30:
        n = 30.0
    if n > 86400:
        n = 86400.0
    return float(n)


def _cap_watch_session_name(project_root: Path) -> str:
    base = re.sub(r"[^a-zA-Z0-9_-]+", "-", project_root.name or "project").strip("-") or "project"
    digest = hashlib.sha1(str(project_root).encode("utf-8")).hexdigest()[:8]
    # Keep it short-ish; tmux session names show up everywhere.
    return f"cap-watch-{base[:24]}-{digest}"


def _resolve_cap_cmd(*, twf: Path, twf_cfg: dict[str, Any]) -> Path | None:
    raw = os.environ.get("TWF_ACCOUNT_POOL_CMD", "").strip() or _cfg_get_str(
        twf_cfg,
        ("twf", "account_pool", "cmd"),
        ("twf_account_pool_cmd",),
        default="",
    )
    tmux_skill_dir = twf.resolve().parents[1]

    if raw:
        p = Path(os.path.expanduser(raw))
        if not p.is_absolute():
            p = (tmux_skill_dir / p).resolve()
        else:
            p = p.resolve()
        if p.is_file():
            return p

    skills_dir = tmux_skill_dir.parent
    sibling = skills_dir / "codex-account-pool" / "scripts" / "cap"
    if sibling.is_file():
        return sibling.resolve()

    global_path = Path.home() / ".codex" / "skills" / "codex-account-pool" / "scripts" / "cap"
    if global_path.is_file():
        return global_path.resolve()

    return None


def _normalize_auth_strategy(raw: str) -> str:
    s = (raw or "").strip().lower()
    if s in {"rr", "round_robin", "round-robin"}:
        return "team_cycle"
    if s in {"least_used", "least-used"}:
        return "balanced"
    return s


def _watch_idle_session_name(project_root: Path, *, team_dir: Path) -> str:
    base = re.sub(r"[^a-zA-Z0-9_-]+", "-", project_root.name or "project").strip("-") or "project"
    digest = hashlib.sha1(f"{project_root}|{team_dir}".encode("utf-8")).hexdigest()[:8]
    return f"atwf-watch-idle-{base[:20]}-{digest}"


def _restart_watch_idle_team(*, twf: Path, team_dir: Path, registry: Path) -> None:
    """
    Force-restart the `atwf watch-idle` sidecar so code/config changes take effect.
    """
    session = _watch_idle_session_name(_expected_project_root(), team_dir=team_dir)
    _tmux_kill_session(session)
    _ensure_watch_idle_team(twf=twf, team_dir=team_dir, registry=registry)


def _ensure_watch_idle_team(*, twf: Path, team_dir: Path, registry: Path) -> None:
    """
    Start a background `atwf watch-idle` tmux session.

    Behavior:
    - Runs forever as a sidecar.
    - Respects `share/.paused`: when paused, it sleeps and does nothing.
    """
    reg = _load_registry(registry)
    members = reg.get("members")
    if not isinstance(members, list) or not any(isinstance(m, dict) and str(m.get("full", "")).strip() for m in members):
        return

    session = _watch_idle_session_name(_expected_project_root(), team_dir=team_dir)
    if _tmux_running(session):
        return

    exports: list[str] = []
    exports.append(f"export AITWF_DIR={shlex.quote(str(team_dir))};")
    exports.append(f"export AITWF_TWF={shlex.quote(str(twf))};")

    cmd_parts = [
        "bash",
        ".codex/skills/ai-team-workflow/scripts/atwf",
        "watch-idle",
    ]
    cmd_line = " ".join(shlex.quote(p) for p in cmd_parts)
    launch = "".join(exports) + f"exec {cmd_line}"

    res = subprocess.run(
        ["tmux", "new-session", "-d", "-s", session, "-c", str(_expected_project_root()), "bash", "-lc", launch],
        check=False,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    if res.returncode != 0:
        _eprint(f"⚠️ failed to start atwf watch-idle tmux session: {session}")
        return
    _eprint(f"🛰️ atwf watch-idle started: {session}")


def _ensure_cap_watch_team(*, twf: Path, team_dir: Path, registry: Path) -> None:
    """
    Start a background `cap watch-team` tmux session when:
    - twf.account_pool.enabled=true
    - twf.account_pool.auth_team.strategy=team_cycle
    """
    reg = _load_registry(registry)
    members = reg.get("members")
    if not isinstance(members, list) or not any(isinstance(m, dict) and str(m.get("full", "")).strip() for m in members):
        return

    try:
        twf_cfg_path = _resolve_twf_config_path(twf)
        twf_cfg = _read_yaml_or_json(twf_cfg_path) if twf_cfg_path else {}
    except Exception:
        twf_cfg = {}

    enabled = _cfg_get_boolish(twf_cfg, ("twf", "account_pool", "enabled"), ("twf_use_account_pool",), default=False)
    if not enabled:
        return

    strategy_raw = _cfg_get_str(
        twf_cfg,
        ("twf", "account_pool", "auth_team", "strategy"),
        ("twf_auth_team_strategy",),
        default="",
    )
    strategy = _normalize_auth_strategy(strategy_raw)
    if strategy != "team_cycle":
        return

    watch_enabled = _cfg_get_boolish(twf_cfg, ("twf", "account_pool", "watch_team", "enabled"), default=True)
    if not watch_enabled:
        return

    auth_dir_raw = _cfg_get_str(
        twf_cfg,
        ("twf", "account_pool", "auth_team", "dir"),
        ("twf_auth_team_dir",),
        default="",
    )
    if not auth_dir_raw:
        _eprint("⚠️ account_pool enabled but auth_team.dir is empty; not starting cap watch-team")
        return
    auth_dir = _expand_path(auth_dir_raw)
    if not auth_dir.is_dir():
        _eprint(f"⚠️ auth_team.dir is not a directory: {auth_dir} (not starting cap watch-team)")
        return

    auth_glob = _cfg_get_str(
        twf_cfg,
        ("twf", "account_pool", "auth_team", "glob"),
        ("twf_auth_team_glob",),
        default="auth.json*",
    )

    interval = _cfg_get_floatish(twf_cfg, ("twf", "account_pool", "watch_team", "interval"), default=180.0)
    grace = _cfg_get_floatish(twf_cfg, ("twf", "account_pool", "watch_team", "grace"), default=300.0)
    max_retries = _cfg_get_intish(twf_cfg, ("twf", "account_pool", "watch_team", "max_retries"), default=10)
    needle = _cfg_get_str(
        twf_cfg,
        ("twf", "account_pool", "watch_team", "needle"),
        default="You've hit your usage limit.",
    )
    message = _cfg_get_str(
        twf_cfg,
        ("twf", "account_pool", "watch_team", "message"),
        default="Task continues. If you are waiting for a reply, please ignore this message.",
    )

    cap_cmd = _resolve_cap_cmd(twf=twf, twf_cfg=twf_cfg)
    if not cap_cmd:
        _eprint("⚠️ account_pool enabled but codex-account-pool/cap not found; not starting cap watch-team")
        return

    session = _cap_watch_session_name(_expected_project_root())
    if _tmux_running(session):
        return

    exports: list[str] = []
    exports.append(f"export CAP_STATUS_SESSION_PREFIX={shlex.quote(session)};")
    for k in ("CAP_STATE_FILE", "CAP_SOURCES", "CAP_STRATEGY"):
        v = os.environ.get(k, "").strip()
        if v:
            exports.append(f"export {k}={shlex.quote(v)};")

    cmd_parts = [
        "bash",
        str(cap_cmd),
        "watch-team",
        str(auth_dir),
        "--glob",
        auth_glob,
        "--registry",
        str(registry),
        "--interval",
        str(interval),
        "--grace",
        str(grace),
        "--max-retries",
        str(max_retries),
        "--needle",
        needle,
        "--message",
        message,
    ]
    cmd_line = " ".join(shlex.quote(p) for p in cmd_parts)
    launch = "".join(exports) + f"exec {cmd_line}"

    res = subprocess.run(
        ["tmux", "new-session", "-d", "-s", session, "-c", str(_expected_project_root()), "bash", "-lc", launch],
        check=False,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    if res.returncode != 0:
        _eprint(f"⚠️ failed to start cap watch-team tmux session: {session}")
        return
    _eprint(f"🛰️ cap watch-team started: {session}")


def _rm_tree(path: Path) -> None:
    try:
        shutil.rmtree(path)
    except FileNotFoundError:
        return
    except OSError:
        # Best effort.
        return


def _tmux_kill_session(name: str) -> None:
    name = (name or "").strip()
    if not name:
        return
    subprocess.run(["tmux", "kill-session", "-t", name], check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def cmd_reset(args: argparse.Namespace) -> int:
    """
    Reset current environment by deleting all local temp/state artifacts:
    - ai-team-workflow share dir (registry/task/design)
    - tmux-workflow workers for this project (tmux sessions, state files, worker homes)
    - codex-account-pool local state.json (optional)
    """
    expected_root = _expected_project_root()
    twf = _resolve_twf()
    # Stop the account-pool watcher early to avoid races during reset.
    watch_session = _cap_watch_session_name(expected_root)
    _tmux_kill_session(watch_session)
    _tmux_kill_session(f"{watch_session}-status")
    _tmux_kill_session(_watch_idle_session_name(expected_root, team_dir=_default_team_dir()))

    # 1) Stop/remove tmux-workflow workers for this project.
    state_dir = _resolve_twf_state_dir(twf)
    worker_candidates: list[tuple[Path, dict[str, Any]]] = []
    if state_dir.is_dir():
        for p in sorted(state_dir.glob("*.json")):
            try:
                data = _read_json(p)
            except SystemExit:
                continue
            if not data:
                continue
            if _state_file_matches_project(p, expected_root):
                worker_candidates.append((p, data))

    codex_workers_root = Path(os.environ.get("TWF_WORKERS_DIR", "") or (Path.home() / ".codex-workers")).expanduser().resolve()

    if args.dry_run:
        print(f"project_root: {expected_root}")
        print(f"twf_state_dir: {state_dir}")
        print(f"workers_matched: {len(worker_candidates)}")
        for p, data in worker_candidates:
            print(f"- state: {p}")
            tmux_session = str(data.get("tmux_session") or "").strip()
            codex_home = str(data.get("codex_home") or "").strip()
            if tmux_session:
                print(f"  tmux_session: {tmux_session}")
            if codex_home:
                print(f"  codex_home: {codex_home}")
        team_dir = _default_team_dir()
        print(f"ai_team_share_dir: {team_dir}")
        pool_state = (_skill_dir().parent / "codex-account-pool" / "share" / "state.json").resolve()
        print(f"cap_watch_session: {_cap_watch_session_name(expected_root)}")
        if getattr(args, "wipe_account_pool", False):
            print(f"cap_state: {pool_state}")
        else:
            print(f"cap_state: {pool_state} (preserved; pass --wipe-account-pool to delete)")
        return 0

    for p, data in worker_candidates:
        tmux_session = str(data.get("tmux_session") or "").strip()
        if tmux_session:
            _tmux_kill_session(tmux_session)

        codex_home_raw = str(data.get("codex_home") or "").strip()
        if codex_home_raw:
            try:
                codex_home = Path(codex_home_raw).expanduser().resolve()
                # Safety: only remove under codex_workers_root unless --force.
                if codex_workers_root == codex_home or codex_workers_root in codex_home.parents:
                    _rm_tree(codex_home)
                elif args.force:
                    _rm_tree(codex_home)
                else:
                    _eprint(f"⚠️ skip removing codex_home outside {codex_workers_root}: {codex_home}")
            except Exception:
                pass

        try:
            p.unlink()
        except FileNotFoundError:
            pass
        except OSError:
            pass

    # Remove stale lock file if present.
    try:
        (state_dir / ".lock").unlink()
    except Exception:
        pass

    # 2) Remove ai-team-workflow share dir (registry/task/design).
    team_dir = _default_team_dir()
    _rm_tree(team_dir)

    # 3) Optionally wipe local codex-account-pool state (per-project).
    if getattr(args, "wipe_account_pool", False):
        cap_share = _skill_dir().parent / "codex-account-pool" / "share"
        cap_state = cap_share / "state.json"
        cap_lock = cap_share / "state.json.lock"
        try:
            cap_state.unlink()
        except Exception:
            pass
        try:
            cap_lock.unlink()
        except Exception:
            pass
        # If share becomes empty, remove it.
        try:
            if cap_share.is_dir() and not any(cap_share.iterdir()):
                cap_share.rmdir()
        except Exception:
            pass

    _eprint("✅ reset complete")
    return 0


def _run(cmd: list[str], *, input_text: str | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        cmd,
        check=False,
        text=True,
        input=input_text,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def _run_twf(twf: Path, args: list[str], *, input_text: str | None = None) -> subprocess.CompletedProcess[str]:
    return _run(["bash", str(twf), *args], input_text=input_text)


def _require_role(role: str) -> str:
    r = role.strip().lower()
    enabled = _policy().enabled_roles
    if r not in enabled:
        raise SystemExit(f"❌ unsupported role: {role} (enabled: {', '.join(sorted(enabled))})")
    return r


def _require_full_name(name: str) -> str:
    n = name.strip()
    if not FULL_NAME_RE.match(n):
        raise SystemExit("❌ remove requires a full worker name like: <base>-YYYYmmdd-HHMMSS-<pid>")
    return n


def _base_name(role: str, label: str | None) -> str:
    if not label:
        return role
    clean = label.strip().replace(" ", "-")
    clean = "-".join([seg for seg in clean.split("-") if seg])
    if not clean:
        return role
    return f"{role}-{clean}"


def _read_json(path: Path) -> dict[str, Any]:
    try:
        raw = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return {}
    except OSError as e:
        raise SystemExit(f"❌ failed to read: {path} ({e})")
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        raise SystemExit(f"❌ invalid JSON: {path} ({e})")
    return data if isinstance(data, dict) else {}


def _write_json_atomic(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    tmp.replace(path)


@contextmanager
def _locked(lock_path: Path):
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    f = open(lock_path, "w", encoding="utf-8")
    try:
        import fcntl

        fcntl.flock(f, fcntl.LOCK_EX)
        yield
    finally:
        try:
            import fcntl

            fcntl.flock(f, fcntl.LOCK_UN)
        except Exception:
            pass
        f.close()


def _load_registry(registry: Path) -> dict[str, Any]:
    data = _read_json(registry)
    if not data:
        return {
            "version": 1,
            "created_at": _now(),
            "updated_at": _now(),
            "members": [],
            "permits": [],
        }
    if not isinstance(data.get("members"), list):
        data["members"] = []
    if not isinstance(data.get("permits"), list):
        data["permits"] = []
    if not isinstance(data.get("version"), int):
        data["version"] = 1
    if not isinstance(data.get("created_at"), str):
        data["created_at"] = _now()
    data["updated_at"] = _now()
    return data


def _find_member_index(data: dict[str, Any], full: str) -> int | None:
    members = data.get("members")
    if not isinstance(members, list):
        return None
    for i, m in enumerate(members):
        if isinstance(m, dict) and m.get("full") == full:
            return i
    return None


def _find_latest_member_by(data: dict[str, Any], *, role: str, base: str) -> dict[str, Any] | None:
    members = data.get("members")
    if not isinstance(members, list):
        return None
    matches = []
    for m in members:
        if not isinstance(m, dict):
            continue
        if str(m.get("role", "")).strip() != role:
            continue
        if str(m.get("base", "")).strip() != base:
            continue
        matches.append(m)
    if not matches:
        return None
    matches.sort(key=lambda m: str(m.get("updated_at", "")), reverse=True)
    return matches[0]


def _ensure_member(
    data: dict[str, Any],
    *,
    full: str,
    base: str | None = None,
    role: str | None = None,
    scope: str | None = None,
    parent: str | None = None,
    state_file: str | None = None,
) -> dict[str, Any]:
    members = data["members"]
    assert isinstance(members, list)

    idx = _find_member_index(data, full)
    if idx is None:
        m: dict[str, Any] = {
            "full": full,
            "base": base or "",
            "role": role or "",
            "scope": scope or "",
            "parent": parent,
            "children": [],
            "state_file": state_file or "",
            "created_at": _now(),
            "updated_at": _now(),
        }
        members.append(m)
        return m

    m = members[idx]
    if not isinstance(m, dict):
        m = {"full": full}
        members[idx] = m
    if base is not None:
        m["base"] = base
    if role is not None:
        m["role"] = role
    if scope is not None:
        m["scope"] = scope
    if parent is not None:
        m["parent"] = parent
    if state_file is not None:
        m["state_file"] = state_file
    if not isinstance(m.get("children"), list):
        m["children"] = []
    m["updated_at"] = _now()
    return m


def _add_child(data: dict[str, Any], *, parent_full: str, child_full: str) -> None:
    parent = _ensure_member(data, full=parent_full)
    children = parent.get("children")
    if not isinstance(children, list):
        children = []
    children = [c for c in children if isinstance(c, str) and c.strip()]
    if child_full not in children:
        children.append(child_full)
    parent["children"] = children
    parent["updated_at"] = _now()


def _resolve_member(data: dict[str, Any], name: str) -> dict[str, Any] | None:
    name = name.strip()
    members = data.get("members")
    if not isinstance(members, list):
        return None

    exact = [m for m in members if isinstance(m, dict) and m.get("full") == name]
    if exact:
        return exact[0]

    base_matches = [m for m in members if isinstance(m, dict) and m.get("base") == name]
    if not base_matches:
        return None
    base_matches.sort(key=lambda m: str(m.get("updated_at", "")), reverse=True)
    return base_matches[0]


def _resolve_latest_by_role(data: dict[str, Any], role: str) -> dict[str, Any] | None:
    role = role.strip()
    members = data.get("members")
    if not isinstance(members, list):
        return None
    matches = [m for m in members if isinstance(m, dict) and str(m.get("role", "")).strip() == role]
    if not matches:
        return None
    matches.sort(key=lambda m: str(m.get("updated_at", "")), reverse=True)
    return matches[0]


def _template_for_role(role: str) -> Path:
    role = _require_role(role)
    p = _templates_dir() / f"{role}.md"
    if not p.is_file():
        raise SystemExit(f"❌ missing template for role={role}: {p}")
    return p


def _render_template(raw: str, *, role: str, full: str, base: str, registry: Path, team_dir: Path) -> str:
    return (
        raw.replace("{{ROLE}}", role)
        .replace("{{FULL_NAME}}", full)
        .replace("{{BASE_NAME}}", base)
        .replace("{{REGISTRY_PATH}}", str(registry))
        .replace("{{TEAM_DIR}}", str(team_dir))
    )


def _ensure_registry_file(registry: Path, team_dir: Path) -> None:
    lock = team_dir / ".lock"
    with _locked(lock):
        data = _load_registry(registry)
        _write_json_atomic(registry, data)
    _eprint(f"✅ registry ready: {registry}")


def _prune_members_by(data: dict[str, Any], *, role: str, base: str, keep_full: str | None = None) -> None:
    members = data.get("members")
    if not isinstance(members, list) or not members:
        return

    role = role.strip()
    base = base.strip()
    keep = keep_full.strip() if isinstance(keep_full, str) and keep_full.strip() else None

    kept: list[Any] = []
    for m in members:
        if not isinstance(m, dict):
            kept.append(m)
            continue
        m_role = str(m.get("role", "")).strip()
        m_base = str(m.get("base", "")).strip()
        m_full = str(m.get("full", "")).strip()
        if m_role == role and m_base == base:
            if keep and m_full == keep:
                kept.append(m)
            continue
        kept.append(m)
    data["members"] = kept


def _member_state_file(m: dict[str, Any]) -> Path | None:
    raw = m.get("state_file")
    if not isinstance(raw, str):
        return None
    raw = raw.strip()
    if not raw:
        return None
    try:
        return _expand_path(raw)
    except Exception:
        return None


def _expected_project_root() -> Path:
    try:
        return _git_root()
    except SystemExit:
        return Path.cwd().resolve()


def _state_file_matches_project(state_file: Path, expected_root: Path) -> bool:
    data = _read_json(state_file)
    if not data:
        return False

    work_dir_norm = data.get("work_dir_norm")
    if isinstance(work_dir_norm, str) and work_dir_norm.strip():
        actual = Path(work_dir_norm.strip()).resolve()
    else:
        work_dir = data.get("work_dir")
        if not isinstance(work_dir, str) or not work_dir.strip():
            return False
        actual = Path(work_dir.strip()).resolve()

    expected = expected_root.resolve()
    return actual == expected or expected in actual.parents


def _write_text_atomic(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    payload = text if text.endswith("\n") else text + "\n"
    tmp.write_text(payload, encoding="utf-8")
    tmp.replace(path)


def _task_path(team_dir: Path) -> Path:
    return team_dir / "task.md"


def _design_dir(team_dir: Path) -> Path:
    return team_dir / "design"


def _design_summary_path(team_dir: Path) -> Path:
    return team_dir / "design.md"


def _ops_dir(team_dir: Path) -> Path:
    return team_dir / "ops"


def _ops_env_notes_path(team_dir: Path) -> Path:
    return _ops_dir(team_dir) / "env.md"


def _ops_host_deps_path(team_dir: Path) -> Path:
    return _ops_dir(team_dir) / "host-deps.md"


def _design_member_path(team_dir: Path, full: str) -> Path:
    safe = full.strip()
    if not safe:
        raise ValueError("full is required")
    return _design_dir(team_dir) / f"{safe}.md"


def _extract_task_file_from_text(task: str) -> str | None:
    raw = task.strip()
    if not raw:
        return None

    candidates = []
    if raw.startswith("任务描述：") or raw.startswith("任务描述:"):
        candidates.append(raw.split(":", 1)[1] if ":" in raw else raw.split("：", 1)[1])
    candidates.append(raw)

    for cand in candidates:
        p = cand.strip().strip('"').strip("'")
        if not p:
            continue
        if not p.startswith("/"):
            continue
        try:
            path = _expand_path(p)
        except Exception:
            continue
        if path.is_file():
            return str(path)
    return None


def _read_task_content(args: argparse.Namespace) -> tuple[str | None, str | None]:
    task_file = str(getattr(args, "task_file", "") or "").strip()
    task_text = str(getattr(args, "task", "") or "").strip()

    if not task_file and task_text:
        guessed = _extract_task_file_from_text(task_text)
        if guessed:
            task_file = guessed
            task_text = ""

    stdin_text = ""
    if not sys.stdin.isatty():
        stdin_text = sys.stdin.read().strip()

    if task_file:
        path = _expand_path(task_file)
        try:
            content = path.read_text(encoding="utf-8")
        except OSError as e:
            raise SystemExit(f"❌ failed to read task file: {path} ({e})")
        return content, str(path)

    if task_text:
        return task_text, None
    if stdin_text:
        return stdin_text, None
    return None, None


def _ensure_share_layout(team_dir: Path) -> None:
    team_dir.mkdir(parents=True, exist_ok=True)
    _design_dir(team_dir).mkdir(parents=True, exist_ok=True)
    _ops_dir(team_dir).mkdir(parents=True, exist_ok=True)
    _inbox_root(team_dir).mkdir(parents=True, exist_ok=True)
    _requests_root(team_dir).mkdir(parents=True, exist_ok=True)
    _state_root(team_dir).mkdir(parents=True, exist_ok=True)


def _inbox_summary(body: str) -> str:
    for line in (body or "").splitlines():
        s = line.strip()
        if s:
            return (s[:157] + "...") if len(s) > 160 else s
    return ""


def _agent_state_path(team_dir: Path, *, full: str) -> Path:
    return _state_root(team_dir) / f"{_slugify(full)}.json"


def _drive_state_path(team_dir: Path) -> Path:
    return _state_root(team_dir) / "drive.json"


def _default_drive_state(*, mode: str) -> dict[str, Any]:
    return {
        "version": 1,
        "created_at": _now(),
        "updated_at": _now(),
        "mode": _normalize_drive_mode(mode) if mode else _DRIVE_MODE_DEFAULT,
        "last_triggered_at": "",
        "last_msg_id": "",
        "last_reason": "",
        "last_driver_full": "",
    }


def _load_drive_state_unlocked(team_dir: Path, *, mode_default: str) -> dict[str, Any]:
    path = _drive_state_path(team_dir)
    data = _read_json(path) if path.is_file() else {}
    if not data:
        data = _default_drive_state(mode=mode_default)
        _write_json_atomic(path, data)
        return data

    data.setdefault("version", 1)
    data.setdefault("created_at", _now())
    data["updated_at"] = _now()
    data.setdefault("last_triggered_at", "")
    data.setdefault("last_msg_id", "")
    data.setdefault("last_reason", "")
    data.setdefault("last_driver_full", "")

    # Config is authoritative; keep the drive state's `mode` as an informational mirror.
    mode = _normalize_drive_mode(str(mode_default or ""))
    if mode not in _DRIVE_MODES:
        mode = _DRIVE_MODE_DEFAULT
    data["mode"] = mode
    return data


def _write_drive_state(team_dir: Path, *, update: dict[str, Any]) -> dict[str, Any]:
    lock = _state_lock_path(team_dir)
    with _locked(lock):
        _ensure_share_layout(team_dir)
        data = _load_drive_state_unlocked(team_dir, mode_default=_drive_mode_config_hot())
        for k, v in update.items():
            data[k] = v
        data["updated_at"] = _now()
        _write_json_atomic(_drive_state_path(team_dir), data)
        return data


def _set_drive_mode_config(mode: str) -> str:
    """
    Operator utility: update `team.drive.mode` in the config file in-place.
    This is intentionally conservative to preserve comments and other formatting.
    """
    mode = _normalize_drive_mode(mode)
    if mode not in _DRIVE_MODES:
        raise SystemExit(f"❌ invalid drive mode: {mode!r} (allowed: running|standby)")

    path = _config_file()
    try:
        raw = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        raise SystemExit(f"❌ config file missing: {path}")
    except OSError as e:
        raise SystemExit(f"❌ failed to read config file: {path} ({e})")

    lines = raw.splitlines(keepends=True)
    in_team = False
    team_indent: int | None = None
    in_drive = False
    drive_indent: int | None = None
    changed = False

    def leading_spaces(s: str) -> int:
        return len(s) - len(s.lstrip(" "))

    for i, line in enumerate(lines):
        stripped = line.lstrip(" ")
        if not stripped.strip() or stripped.lstrip().startswith("#"):
            continue
        indent = leading_spaces(line)
        key = stripped.split(":", 1)[0].strip()

        if not in_team:
            if key == "team" and stripped.startswith("team:"):
                in_team = True
                team_indent = indent
                in_drive = False
                drive_indent = None
            continue

        if team_indent is not None and indent <= team_indent and not stripped.startswith("-"):
            in_team = False
            in_drive = False
            drive_indent = None
            team_indent = None
            continue

        if not in_drive:
            if key == "drive" and stripped.startswith("drive:"):
                in_drive = True
                drive_indent = indent
            continue

        if drive_indent is not None and indent <= drive_indent and not stripped.startswith("-"):
            in_drive = False
            drive_indent = None
            continue

        if key != "mode" or not stripped.startswith("mode:"):
            continue

        suffix = ""
        if "#" in stripped:
            idx = stripped.find("#")
            suffix = " " + stripped[idx:].rstrip("\n")
        newline = "\n" if line.endswith("\n") else ""
        lines[i] = (" " * indent) + f"mode: {mode}" + suffix + newline
        changed = True
        break

    if not changed:
        raise SystemExit(f"❌ failed to locate `team.drive.mode` in config: {path}")

    new_raw = "".join(lines)
    try:
        _write_text_atomic(path, new_raw)
    except OSError as e:
        raise SystemExit(f"❌ failed to write config file: {path} ({e})")
    return mode


def _default_reply_drive_state() -> dict[str, Any]:
    return {
        "version": 1,
        "created_at": _now(),
        "updated_at": _now(),
        "last_triggered_at": "",
        "last_reason": "",
        "last_request_id": "",
        "last_target_base": "",
        "last_target_full": "",
    }


def _load_reply_drive_state_unlocked(team_dir: Path) -> dict[str, Any]:
    path = _reply_drive_state_path(team_dir)
    data = _read_json(path) if path.is_file() else {}
    if not data:
        data = _default_reply_drive_state()
        _write_json_atomic(path, data)
        return data

    data.setdefault("version", 1)
    data.setdefault("created_at", _now())
    data["updated_at"] = _now()
    data.setdefault("last_triggered_at", "")
    data.setdefault("last_reason", "")
    data.setdefault("last_request_id", "")
    data.setdefault("last_target_base", "")
    data.setdefault("last_target_full", "")
    return data


def _write_reply_drive_state(team_dir: Path, *, update: dict[str, Any]) -> dict[str, Any]:
    lock = _state_lock_path(team_dir)
    with _locked(lock):
        _ensure_share_layout(team_dir)
        data = _load_reply_drive_state_unlocked(team_dir)
        for k, v in update.items():
            data[k] = v
        data["updated_at"] = _now()
        _write_json_atomic(_reply_drive_state_path(team_dir), data)
        return data


def _normalize_agent_status(raw: str) -> str:
    s = (raw or "").strip().lower()
    if s in {"work", "working", "busy"}:
        return _STATE_STATUS_WORKING
    if s in {"drain", "draining"}:
        return _STATE_STATUS_DRAINING
    if s in {"idle", "standby"}:
        return _STATE_STATUS_IDLE
    return s


_DURATION_RE = re.compile(r"^([0-9]+(?:\\.[0-9]+)?)\\s*([a-zA-Z]+)?$")


def _parse_duration_seconds(raw: str, *, default_s: float) -> float:
    s = (raw or "").strip()
    if not s:
        return float(default_s)
    m = _DURATION_RE.match(s)
    if not m:
        return float(default_s)
    try:
        n = float(m.group(1))
    except Exception:
        return float(default_s)
    unit = (m.group(2) or "").strip().lower()
    if not unit:
        return float(n)
    if unit in {"s", "sec", "secs", "second", "seconds"}:
        return float(n)
    if unit in {"m", "min", "mins", "minute", "minutes"}:
        return float(n) * 60.0
    if unit in {"h", "hr", "hrs", "hour", "hours"}:
        return float(n) * 3600.0
    if unit in {"d", "day", "days"}:
        return float(n) * 86400.0
    return float(default_s)


def _default_agent_state(*, full: str, base: str, role: str) -> dict[str, Any]:
    return {
        "version": 1,
        "created_at": _now(),
        "updated_at": _now(),
        "full": full,
        "base": base,
        "role": role,
        "status": _STATE_STATUS_WORKING,
        "status_source": "init",
        "last_inbox_check_at": "",
        "last_inbox_unread": 0,
        "last_inbox_overflow": 0,
        "last_output_hash": "",
        "last_output_capture_at": "",
        "last_output_change_at": "",
        "auto_enter_last_sent_at": "",
        "auto_enter_last_reason": "",
        "auto_enter_count": 0,
        "idle_since": "",
        "idle_inbox_empty_at": "",
        "wakeup_scheduled_at": "",
        "wakeup_due_at": "",
        "wakeup_sent_at": "",
        "wakeup_reason": "",
        "stale_alert_sent_at": "",
        "stale_alert_msg_id": "",
        "stale_alert_reason": "",
    }


def _load_agent_state_unlocked(team_dir: Path, *, full: str, base: str, role: str) -> dict[str, Any]:
    path = _agent_state_path(team_dir, full=full)
    data = _read_json(path) if path.is_file() else {}
    if not data:
        data = _default_agent_state(full=full, base=base, role=role)
        _write_json_atomic(path, data)
        return data

    data.setdefault("version", 1)
    data.setdefault("created_at", _now())
    data.setdefault("full", full)
    data.setdefault("base", base)
    data.setdefault("role", role)
    data.setdefault("status", _STATE_STATUS_WORKING)
    data.setdefault("status_source", "init")
    data["updated_at"] = _now()

    status = _normalize_agent_status(str(data.get("status", "")))
    if status not in _STATE_STATUSES:
        status = _STATE_STATUS_WORKING
    data["status"] = status
    data.setdefault("last_output_hash", "")
    data.setdefault("last_output_capture_at", "")
    data.setdefault("last_output_change_at", "")
    data.setdefault("auto_enter_last_sent_at", "")
    data.setdefault("auto_enter_last_reason", "")
    data.setdefault("auto_enter_count", 0)
    return data


def _write_agent_state(team_dir: Path, *, full: str, base: str, role: str, update: dict[str, Any]) -> dict[str, Any]:
    lock = _state_lock_path(team_dir)
    with _locked(lock):
        _ensure_share_layout(team_dir)
        data = _load_agent_state_unlocked(team_dir, full=full, base=base, role=role)
        for k, v in update.items():
            data[k] = v
        data["updated_at"] = _now()
        _write_json_atomic(_agent_state_path(team_dir, full=full), data)
        return data


def _update_agent_state(
    team_dir: Path,
    *,
    full: str,
    base: str,
    role: str,
    updater,
) -> dict[str, Any]:
    lock = _state_lock_path(team_dir)
    with _locked(lock):
        _ensure_share_layout(team_dir)
        data = _load_agent_state_unlocked(team_dir, full=full, base=base, role=role)
        updater(data)
        data["updated_at"] = _now()
        _write_json_atomic(_agent_state_path(team_dir, full=full), data)
        return data


def _inbox_unread_stats(team_dir: Path, *, to_base: str) -> tuple[int, int, list[str]]:
    base_dir = _inbox_member_dir(team_dir, base=to_base)
    unread_root = base_dir / _INBOX_UNREAD_DIR
    overflow_root = base_dir / _INBOX_OVERFLOW_DIR

    unread = 0
    overflow = 0
    ids: list[tuple[int, str]] = []

    if unread_root.is_dir():
        for from_dir in unread_root.glob("from-*"):
            if not from_dir.is_dir():
                continue
            for n, stem, _p in _inbox_list_msgs(from_dir):
                unread += 1
                ids.append((n, stem))

    if overflow_root.is_dir():
        for from_dir in overflow_root.glob("from-*"):
            if not from_dir.is_dir():
                continue
            overflow += len(_inbox_list_msgs(from_dir))

    ids.sort(key=lambda t: t[0])
    return unread, overflow, [stem for _n, stem in ids]


def _inbox_pending_min_id(team_dir: Path, *, to_base: str) -> tuple[int, str]:
    """
    Return (min_numeric_id, min_id_str) across unread+overflow for a recipient base.
    If no pending messages exist, returns (0, "").
    """
    base_dir = _inbox_member_dir(team_dir, base=to_base)
    min_n: int | None = None
    min_s = ""

    for state in (_INBOX_UNREAD_DIR, _INBOX_OVERFLOW_DIR):
        root = base_dir / state
        if not root.is_dir():
            continue
        for from_dir in root.glob("from-*"):
            if not from_dir.is_dir():
                continue
            for p in from_dir.glob("*.md"):
                if not p.is_file():
                    continue
                stem = p.stem.strip()
                if not stem.isdigit():
                    continue
                try:
                    n = int(stem)
                except Exception:
                    continue
                if min_n is None or n < min_n:
                    min_n = n
                    min_s = stem

    if min_n is None:
        return 0, ""
    return int(min_n), min_s


def _inbox_message_created_at(team_dir: Path, *, to_base: str, msg_id: str) -> datetime | None:
    hit = _find_inbox_message_file(team_dir, to_base=to_base, msg_id=msg_id)
    if not hit:
        return None
    _state, _from_base, path = hit
    try:
        head = path.read_text(encoding="utf-8", errors="ignore").splitlines()[:40]
    except Exception:
        return None
    for line in head:
        s = line.strip()
        if s.startswith("- created_at:"):
            raw = s.split(":", 1)[1].strip()
            try:
                return datetime.fromisoformat(raw)
            except Exception:
                return None
    return None


def _inbox_list_msgs(dir_path: Path) -> list[tuple[int, str, Path]]:
    if not dir_path.is_dir():
        return []
    out: list[tuple[int, str, Path]] = []
    for p in dir_path.glob("*.md"):
        if not p.is_file():
            continue
        stem = p.stem.strip()
        if not stem.isdigit():
            continue
        try:
            n = int(stem)
        except Exception:
            continue
        out.append((n, stem, p))
    out.sort(key=lambda t: t[0])
    return out


def _inbox_enforce_unread_limit_unlocked(team_dir: Path, *, to_base: str, from_base: str, max_unread: int) -> None:
    if max_unread < 1:
        max_unread = 1
    unread_dir = _inbox_thread_dir(team_dir, to_base=to_base, from_base=from_base, state=_INBOX_UNREAD_DIR)
    entries = _inbox_list_msgs(unread_dir)
    if len(entries) <= max_unread:
        return

    overflow_dir = _inbox_thread_dir(team_dir, to_base=to_base, from_base=from_base, state=_INBOX_OVERFLOW_DIR)
    overflow_dir.mkdir(parents=True, exist_ok=True)

    # Move oldest unread into overflow so active unread stays bounded.
    excess = entries[: max(0, len(entries) - max_unread)]
    for _n, stem, p in excess:
        dst = overflow_dir / f"{stem}.md"
        try:
            p.replace(dst)
        except OSError:
            try:
                shutil.copy2(p, dst)
                p.unlink(missing_ok=True)  # type: ignore[call-arg]
            except Exception:
                pass


def _write_inbox_message_unlocked(
    team_dir: Path,
    *,
    msg_id: str,
    kind: str,
    from_full: str,
    from_base: str,
    from_role: str,
    to_full: str,
    to_base: str,
    to_role: str,
    body: str,
) -> Path:
    msg_id = msg_id.strip()
    if not msg_id:
        raise SystemExit("❌ inbox message id missing")

    kind_s = kind.strip() or "send"
    from_full_s = from_full.strip() or "unknown"
    from_base_s = from_base.strip() or from_full_s
    from_role_s = from_role.strip() or "?"
    to_full_s = to_full.strip() or "unknown"
    to_base_s = to_base.strip() or to_full_s
    to_role_s = to_role.strip() or "?"

    path = _inbox_message_path(
        team_dir,
        to_base=to_base_s,
        from_base=from_base_s,
        state=_INBOX_UNREAD_DIR,
        msg_id=msg_id,
    )

    summary = _inbox_summary(body)
    meta_lines = [
        f"# ATWF Inbox Message {msg_id}",
        "",
        f"- id: `{msg_id}`",
        f"- kind: `{kind_s}`",
        f"- created_at: {_now()}",
        f"- from: `{from_full_s}` (base `{from_base_s}` role `{from_role_s}`)",
        f"- to: `{to_full_s}` (base `{to_base_s}` role `{to_role_s}`)",
    ]
    if summary:
        meta_lines.append(f"- summary: {summary}")
    meta_lines.extend(["", "---", ""])

    body_s = (body or "").rstrip()
    payload = "\n".join(meta_lines) + (body_s + "\n" if body_s else "")
    _write_text_atomic(path, payload)
    return path


def _write_inbox_message(
    team_dir: Path,
    *,
    msg_id: str,
    kind: str,
    from_full: str,
    from_base: str,
    from_role: str,
    to_full: str,
    to_base: str,
    to_role: str,
    body: str,
) -> Path:
    lock = team_dir / ".lock"
    with _locked(lock):
        _ensure_share_layout(team_dir)
        path = _write_inbox_message_unlocked(
            team_dir,
            msg_id=msg_id,
            kind=kind,
            from_full=from_full,
            from_base=from_base,
            from_role=from_role,
            to_full=to_full,
            to_base=to_base,
            to_role=to_role,
            body=body,
        )
        _inbox_enforce_unread_limit_unlocked(
            team_dir,
            to_base=to_base,
            from_base=from_base,
            max_unread=_inbox_max_unread_per_thread(),
        )
        return path


def _find_inbox_message_file(team_dir: Path, *, to_base: str, msg_id: str) -> tuple[str, str, Path] | None:
    base_dir = _inbox_member_dir(team_dir, base=to_base)
    msg_id = msg_id.strip()
    if not msg_id:
        return None
    for state in (_INBOX_UNREAD_DIR, _INBOX_OVERFLOW_DIR, _INBOX_READ_DIR):
        state_dir = base_dir / state
        if not state_dir.is_dir():
            continue
        for from_dir in state_dir.glob("from-*"):
            if not from_dir.is_dir():
                continue
            p = from_dir / f"{msg_id}.md"
            if p.is_file():
                from_base = from_dir.name[len("from-") :]
                return state, from_base, p
    return None


def _mark_inbox_read(team_dir: Path, *, to_base: str, msg_id: str) -> Path | None:
    to_base = to_base.strip()
    msg_id = msg_id.strip()
    if not to_base or not msg_id:
        return None

    lock = team_dir / ".lock"
    with _locked(lock):
        hit = _find_inbox_message_file(team_dir, to_base=to_base, msg_id=msg_id)
        if not hit:
            return None
        state, from_base, src = hit
        if state == _INBOX_READ_DIR:
            return src

        dst = _inbox_message_path(
            team_dir,
            to_base=to_base,
            from_base=from_base,
            state=_INBOX_READ_DIR,
            msg_id=msg_id,
        )
        dst.parent.mkdir(parents=True, exist_ok=True)
        try:
            src.replace(dst)
        except OSError:
            try:
                shutil.copy2(src, dst)
                src.unlink(missing_ok=True)  # type: ignore[call-arg]
            except Exception:
                pass
        return dst if dst.is_file() else None


_REQUEST_ID_RE = re.compile(r"^[a-zA-Z0-9_-]+$")


def _request_response_path(team_dir: Path, *, request_id: str, target_base: str) -> Path:
    request_id = request_id.strip()
    if not request_id:
        raise SystemExit("❌ request id missing")
    return _request_responses_dir(team_dir, request_id=request_id) / f"{_slugify(target_base)}.md"


def _resolve_request_id(team_dir: Path, raw: str) -> str:
    s = (raw or "").strip()
    if not s:
        raise SystemExit("❌ request id missing")
    if _REQUEST_ID_RE.match(s) and _request_dir(team_dir, request_id=s).is_dir():
        return s
    if s.isdigit():
        alt = f"req-{s}"
        if _request_dir(team_dir, request_id=alt).is_dir():
            return alt
    if s.startswith("req-") and s[4:].isdigit():
        alt2 = s[4:]
        if _request_dir(team_dir, request_id=alt2).is_dir():
            return alt2
    return s


def _list_request_ids(team_dir: Path) -> list[str]:
    root = _requests_root(team_dir)
    if not root.is_dir():
        return []
    out: list[str] = []
    for p in root.iterdir():
        if p.is_dir():
            name = p.name.strip()
            if name:
                out.append(name)
    out.sort()
    return out


def _load_request_meta(team_dir: Path, *, request_id: str) -> dict[str, Any]:
    request_id = _resolve_request_id(team_dir, request_id)
    path = _request_meta_path(team_dir, request_id=request_id)
    data = _read_json(path) if path.is_file() else {}
    if not isinstance(data, dict) or not data:
        raise SystemExit(f"❌ request not found: {request_id}")
    data.setdefault("version", 1)
    data.setdefault("id", request_id)
    data.setdefault("created_at", "")
    data.setdefault("updated_at", "")
    status = str(data.get("status", "") or "").strip() or _REQUEST_STATUS_OPEN
    if status not in {_REQUEST_STATUS_OPEN, _REQUEST_STATUS_DONE, _REQUEST_STATUS_TIMED_OUT}:
        status = _REQUEST_STATUS_OPEN
    data["status"] = status
    targets = data.get("targets")
    if not isinstance(targets, dict):
        data["targets"] = {}
    return data


def _update_request_meta(team_dir: Path, *, request_id: str, updater) -> dict[str, Any]:
    request_id = _resolve_request_id(team_dir, request_id)
    lock = team_dir / ".lock"
    with _locked(lock):
        _ensure_share_layout(team_dir)
        path = _request_meta_path(team_dir, request_id=request_id)
        data = _read_json(path) if path.is_file() else {}
        if not isinstance(data, dict) or not data:
            raise SystemExit(f"❌ request not found: {request_id}")
        updater(data)
        data["updated_at"] = _now()
        _write_json_atomic(path, data)
        return data


def _request_all_replied(meta: dict[str, Any]) -> bool:
    targets = meta.get("targets")
    if not isinstance(targets, dict) or not targets:
        return False
    for _k, t in targets.items():
        if not isinstance(t, dict):
            return False
        if str(t.get("status", "")).strip() != _REQUEST_TARGET_STATUS_REPLIED:
            return False
    return True


def _render_request_result(team_dir: Path, meta: dict[str, Any], *, final_status: str) -> str:
    request_id = str(meta.get("id", "") or "").strip()
    topic = str(meta.get("topic", "") or "").strip()
    created_at = str(meta.get("created_at", "") or "").strip()
    deadline_at = str(meta.get("deadline_at", "") or "").strip()

    from_info = meta.get("from") if isinstance(meta.get("from"), dict) else {}
    from_base = str(from_info.get("base", "") or "").strip()
    from_role = str(from_info.get("role", "") or "").strip()
    from_full = str(from_info.get("full", "") or "").strip()

    meta_path = _request_meta_path(team_dir, request_id=request_id) if request_id else _requests_root(team_dir)
    responses_dir = _request_responses_dir(team_dir, request_id=request_id) if request_id else _requests_root(team_dir)

    lines: list[str] = []
    header = "[REPLY-NEEDED RESULT]"
    if final_status == _REQUEST_STATUS_TIMED_OUT:
        header += " timed_out"
    lines.append(header)
    if request_id:
        lines.append(f"- request_id: {request_id}")
    if topic:
        lines.append(f"- topic: {topic}")
    if from_base or from_full:
        lines.append(f"- from: {from_base or from_full} (role={from_role or '?'})")
    if created_at:
        lines.append(f"- created_at: {created_at}")
    if deadline_at:
        lines.append(f"- deadline_at: {deadline_at}")
    lines.append(f"- meta: `{meta_path}`")
    lines.append(f"- responses: `{responses_dir}`")

    targets = meta.get("targets")
    if not isinstance(targets, dict) or not targets:
        lines.append("- targets: (none)")
        return "\n".join(lines).rstrip() + "\n"

    replied: list[str] = []
    pending: list[str] = []
    for base, t in targets.items():
        if not isinstance(t, dict):
            pending.append(str(base))
            continue
        role = str(t.get("role", "") or "").strip() or "?"
        st = str(t.get("status", "") or "").strip() or _REQUEST_TARGET_STATUS_PENDING
        if st == _REQUEST_TARGET_STATUS_REPLIED:
            resp_file = str(t.get("response_file", "") or "").strip()
            resp_note = f" file={resp_file}" if resp_file else ""
            replied.append(f"{base} (role={role}){resp_note}")
            continue
        blocked_until = str(t.get("blocked_until", "") or "").strip()
        waiting_on = str(t.get("waiting_on", "") or "").strip()
        extra: list[str] = []
        if blocked_until:
            extra.append(f"blocked_until={blocked_until}")
        if waiting_on:
            extra.append(f"waiting_on={waiting_on}")
        extra_s = (" " + " ".join(extra)) if extra else ""
        pending.append(f"{base} (role={role} status={st}{extra_s})")

    if replied:
        lines.append("")
        lines.append("Replied:")
        for item in replied:
            lines.append(f"- {item}")
    if pending:
        lines.append("")
        lines.append("Pending:")
        for item in pending:
            lines.append(f"- {item}")

    return "\n".join(lines).rstrip() + "\n"


def _scan_reply_requests(
    team_dir: Path,
    *,
    now_dt: datetime,
) -> tuple[list[tuple[str, str]], bool, list[tuple[str, str, str, str]], dict[str, int]]:
    """
    Returns:
    - finalizable: [(request_id, final_status)] for requests that should be auto-finalized.
    - has_pending: whether any open request has any non-replied target.
    - due: [(request_id, target_base, target_role, target_status)] targets that are due (not replied, not snoozed).
    - waiters: {base -> count} reverse-dependency counts from waiting_on.
    """
    finalizable: list[tuple[str, str]] = []
    has_pending = False
    due: list[tuple[str, str, str, str]] = []
    waiters: dict[str, int] = {}

    for req_id in _list_request_ids(team_dir):
        meta_path = _request_meta_path(team_dir, request_id=req_id)
        if not meta_path.is_file():
            continue
        meta = _read_json(meta_path)
        if not isinstance(meta, dict) or not meta:
            continue
        if str(meta.get("status", "")).strip() != _REQUEST_STATUS_OPEN:
            continue

        targets = meta.get("targets")
        if not isinstance(targets, dict) or not targets:
            continue

        if _request_all_replied(meta):
            finalizable.append((req_id, _REQUEST_STATUS_DONE))
            continue

        deadline_dt = _parse_iso_dt(str(meta.get("deadline_at", "") or ""))
        if deadline_dt is not None and now_dt >= deadline_dt:
            finalizable.append((req_id, _REQUEST_STATUS_TIMED_OUT))
            continue

        for base, t in targets.items():
            if not isinstance(t, dict):
                has_pending = True
                due.append((req_id, str(base), "?", _REQUEST_TARGET_STATUS_PENDING))
                continue
            st = str(t.get("status", "") or "").strip() or _REQUEST_TARGET_STATUS_PENDING
            if st == _REQUEST_TARGET_STATUS_REPLIED:
                continue
            has_pending = True
            role = str(t.get("role", "") or "").strip() or "?"
            waiting_on = str(t.get("waiting_on", "") or "").strip()
            if waiting_on:
                waiters[waiting_on] = int(waiters.get(waiting_on, 0) or 0) + 1
            blocked_until = _parse_iso_dt(str(t.get("blocked_until", "") or ""))
            if blocked_until is not None and now_dt < blocked_until:
                continue
            due.append((req_id, str(base), role, st))

    return finalizable, has_pending, due, waiters


def _finalize_request(
    team_dir: Path,
    registry_data: dict[str, Any],
    *,
    request_id: str,
    msg_id: str,
    final_status: str,
    now_iso: str,
) -> bool:
    if final_status not in {_REQUEST_STATUS_DONE, _REQUEST_STATUS_TIMED_OUT}:
        return False

    now_dt = _parse_iso_dt(now_iso) or datetime.now()

    lock = team_dir / ".lock"
    with _locked(lock):
        meta_path = _request_meta_path(team_dir, request_id=request_id)
        meta = _read_json(meta_path) if meta_path.is_file() else {}
        if not isinstance(meta, dict) or not meta:
            return False
        if str(meta.get("status", "")).strip() != _REQUEST_STATUS_OPEN:
            return False
        if str(meta.get("final_msg_id", "") or "").strip():
            return False

        all_replied = _request_all_replied(meta)
        deadline_dt = _parse_iso_dt(str(meta.get("deadline_at", "") or ""))
        timed_out = deadline_dt is not None and now_dt >= deadline_dt and not all_replied

        if final_status == _REQUEST_STATUS_DONE and not all_replied:
            return False
        if final_status == _REQUEST_STATUS_TIMED_OUT and not timed_out:
            return False

        from_info = meta.get("from") if isinstance(meta.get("from"), dict) else {}
        to_base = str(from_info.get("base", "") or "").strip() or str(from_info.get("full", "") or "").strip()
        to_full = str(from_info.get("full", "") or "").strip()
        to_role = str(from_info.get("role", "") or "").strip() or "?"
        if to_base:
            m = _resolve_member(registry_data, to_base) or {}
            to_full = str(m.get("full", "")).strip() or to_full or to_base
            to_role = _member_role(m) or to_role

        if not to_base:
            return False

        body = _render_request_result(team_dir, meta, final_status=final_status)
        _write_inbox_message_unlocked(
            team_dir,
            msg_id=msg_id,
            kind="reply-needed-result",
            from_full="atwf-reply",
            from_base="atwf-reply",
            from_role="system",
            to_full=to_full or to_base,
            to_base=to_base,
            to_role=to_role,
            body=body,
        )
        _inbox_enforce_unread_limit_unlocked(team_dir, to_base=to_base, from_base="atwf-reply", max_unread=_inbox_max_unread_per_thread())

        meta["status"] = final_status
        meta["finalized_at"] = now_iso
        meta["final_msg_id"] = msg_id
        meta["updated_at"] = now_iso
        _write_json_atomic(meta_path, meta)
        return True


def _ensure_task_and_design_files(team_dir: Path, *, task_content: str | None, task_source: str | None) -> Path | None:
    _ensure_share_layout(team_dir)

    task_path = _task_path(team_dir)
    if task_content is not None:
        header = ""
        if task_source:
            header = (
                f"<!-- AITWF_TASK_SOURCE: {task_source} -->\n"
                f"<!-- AITWF_TASK_SAVED_AT: {_now()} -->\n\n"
            )
        _write_text_atomic(task_path, header + task_content.strip() + "\n")

    summary_path = _design_summary_path(team_dir)
    if not summary_path.exists():
        seed = "# Consolidated Design\n\n"
        if task_path.exists():
            seed += f"- Task: `{task_path}`\n\n"
        seed += "PM should consolidate module/team designs into this file.\n"
        _write_text_atomic(summary_path, seed)

    env_notes_path = _ops_env_notes_path(team_dir)
    if not env_notes_path.exists():
        seed = (
            "# Ops: Environment Notes\n\n"
            "## Policy (development-time)\n"
            "- Ops manages the project environment.\n"
            "- Ops can only operate local Docker (no remote hosts).\n"
            "- For a single project, all services must live in a single `docker-compose` file.\n"
            "- If anything must be installed on the host (e.g. `apt`, `brew`, `curl` download/unpack), it must be recorded in:\n"
            f"  - `{_ops_host_deps_path(team_dir)}`\n\n"
            "## Docker Compose\n"
            "- Keep one compose file for the whole project (commonly repo root `docker-compose.yml` or `compose.yaml`).\n"
            "- Prefer bind mounts + named volumes; avoid undocumented host paths.\n"
            "- Put secrets in `.env` (not committed) and document required keys.\n\n"
            "## Change Log\n"
            "- Record noteworthy environment changes here (date + what + why).\n"
        )
        _write_text_atomic(env_notes_path, seed)

    host_deps_path = _ops_host_deps_path(team_dir)
    if not host_deps_path.exists():
        seed = (
            "# Ops: Host Dependencies (must document)\n\n"
            "Record any dependencies installed outside Docker (OS-level installs, downloaded binaries, etc.).\n\n"
            "## APT (Linux)\n"
            "- (date) `sudo apt-get install ...`  # why\n\n"
            "## Brew (macOS)\n"
            "- (date) `brew install ...`  # why\n\n"
            "## Downloaded binaries\n"
            "- (date) url: ...  dest: ...  sha256: ...  # why\n"
        )
        _write_text_atomic(host_deps_path, seed)

    return task_path if task_path.exists() else None


def _design_seed(*, member: dict[str, Any], full: str, team_dir: Path) -> str:
    role = str(member.get("role", "")).strip()
    base = str(member.get("base", "")).strip()
    scope = str(member.get("scope", "")).strip()
    task_path = _task_path(team_dir)

    lines = [
        f"# Design: {full}",
        "",
        f"- role: `{role or '?'}`",
        f"- base: `{base or full}`",
        f"- scope: {scope or '(fill in)'}",
        f"- task: `{task_path}`" if task_path.exists() else "- task: (missing)",
        f"- created_at: {_now()}",
        "",
        "## Goal",
        "",
        "## Scope / Non-goals",
        "",
        "## Approach",
        "",
        "## Plan (steps)",
        "",
        "## Interfaces / Data",
        "",
        "## Testing / Verification",
        "",
        "## Risks / Rollback",
        "",
        "## Open Questions",
        "",
    ]
    return "\n".join(lines)


def _resolve_target_full(data: dict[str, Any], target: str) -> str | None:
    target = target.strip()
    if not target:
        return None

    m = _resolve_member(data, target)
    if m:
        full = str(m.get("full", "")).strip()
        return full or None

    maybe_role = target.lower()
    if maybe_role in _policy().enabled_roles:
        m2 = _resolve_latest_by_role(data, maybe_role)
        if m2:
            full = str(m2.get("full", "")).strip()
            return full or None

    if FULL_NAME_RE.match(target):
        return target

    return None


def _tmux_self_full() -> str | None:
    pane = os.environ.get("TMUX_PANE", "").strip()
    if pane:
        res = _run(["tmux", "display-message", "-p", "-t", pane, "#S"])
        if res.returncode == 0:
            name = res.stdout.strip()
            if name:
                return name

    res2 = _run(["tmux", "display-message", "-p", "#S"])
    if res2.returncode != 0:
        return None
    name2 = res2.stdout.strip()
    return name2 or None


def _resolve_actor_full(data: dict[str, Any], *, as_target: str | None) -> str:
    if as_target:
        full = _resolve_target_full(data, as_target)
        if not full:
            raise SystemExit(f"❌ --as target not found in registry: {as_target}")
        return full

    full = _tmux_self_full()
    if full:
        return full
    raise SystemExit("❌ this command must run inside tmux or pass --as <full|base|role>")


def _member_role(m: dict[str, Any] | None) -> str:
    if not isinstance(m, dict):
        return ""
    return str(m.get("role", "")).strip()


def _member_base(m: dict[str, Any] | None) -> str:
    if not isinstance(m, dict):
        return ""
    base = str(m.get("base", "")).strip()
    full = str(m.get("full", "")).strip()
    return base or full


def _is_direct_parent_child(data: dict[str, Any], a_full: str, b_full: str) -> bool:
    ma = _resolve_member(data, a_full)
    mb = _resolve_member(data, b_full)
    if not ma or not mb:
        return False
    pa = str(ma.get("parent", "")).strip() if isinstance(ma.get("parent"), str) else ""
    pb = str(mb.get("parent", "")).strip() if isinstance(mb.get("parent"), str) else ""
    return pa == b_full or pb == a_full


def _permit_allows(data: dict[str, Any], *, a_base: str, b_base: str) -> bool:
    permits = data.get("permits")
    if not isinstance(permits, list):
        return False
    a_base = a_base.strip()
    b_base = b_base.strip()
    if not a_base or not b_base:
        return False

    now = datetime.now()
    for p in permits:
        if not isinstance(p, dict):
            continue
        a = str(p.get("a", "")).strip()
        b = str(p.get("b", "")).strip()
        if not a or not b:
            continue
        if not ((a == a_base and b == b_base) or (a == b_base and b == a_base)):
            continue
        exp = str(p.get("expires_at", "")).strip()
        if exp:
            try:
                if datetime.fromisoformat(exp) <= now:
                    continue
            except Exception:
                # If expires_at is malformed, treat as non-expiring.
                pass
        return True
    return False


def _add_handoff_permit(
    data: dict[str, Any],
    *,
    a_base: str,
    b_base: str,
    created_by: str,
    created_by_role: str,
    reason: str,
    ttl_seconds: int | None,
) -> dict[str, Any]:
    permits = data.get("permits")
    if not isinstance(permits, list):
        permits = []
        data["permits"] = permits

    a_base = a_base.strip()
    b_base = b_base.strip()
    if not a_base or not b_base:
        raise SystemExit("❌ invalid handoff endpoints (missing base)")
    if a_base == b_base:
        raise SystemExit("❌ handoff endpoints must be different")

    now = datetime.now()
    created_at = now.isoformat(timespec="seconds")
    expires_at = ""
    if isinstance(ttl_seconds, int) and ttl_seconds > 0:
        expires_at = (now + timedelta(seconds=ttl_seconds)).isoformat(timespec="seconds")

    permit_id = f"handoff-{now.strftime('%Y%m%d-%H%M%S')}-{os.getpid()}-{len(permits) + 1}"
    payload: dict[str, Any] = {
        "id": permit_id,
        "a": a_base,
        "b": b_base,
        "created_by": created_by,
        "created_by_role": created_by_role,
        "created_at": created_at,
    }
    if expires_at:
        payload["expires_at"] = expires_at
    if reason.strip():
        payload["reason"] = reason.strip()
    permits.append(payload)
    return payload


def _comm_allowed(
    policy: TeamPolicy,
    data: dict[str, Any],
    *,
    actor_full: str,
    target_full: str,
) -> tuple[bool, str]:
    if actor_full == target_full:
        return True, "self"

    actor_m = _resolve_member(data, actor_full)
    target_m = _resolve_member(data, target_full)
    if not actor_m:
        return False, f"actor not registered: {actor_full}"
    if not target_m:
        return False, f"target not registered: {target_full}"

    actor_role = _member_role(actor_m)
    target_role = _member_role(target_m)
    if actor_role not in policy.enabled_roles:
        return False, f"actor role not enabled: {actor_role or '(missing)'}"
    if target_role not in policy.enabled_roles:
        return False, f"target role not enabled: {target_role or '(missing)'}"

    if policy.comm_allow_parent_child and _is_direct_parent_child(data, actor_full, target_full):
        return True, "parent-child"

    allowed_roles = policy.comm_direct_allow.get(actor_role, frozenset())
    if target_role in allowed_roles:
        return True, "direct-allow"

    if not policy.comm_require_handoff:
        return True, "handoff-not-required"

    actor_base = _member_base(actor_m)
    target_base = _member_base(target_m)
    if _permit_allows(data, a_base=actor_base, b_base=target_base):
        return True, "handoff-permit"

    return False, f"handoff required for {actor_role}->{target_role} (no permit)"


def _require_comm_allowed(
    policy: TeamPolicy,
    data: dict[str, Any],
    *,
    actor_full: str,
    target_full: str,
) -> None:
    ok, reason = _comm_allowed(policy, data, actor_full=actor_full, target_full=target_full)
    if ok:
        return
    root = policy.root_role
    raise SystemExit(
        "❌ communication not permitted by policy.\n"
        f"   actor:  {actor_full}\n"
        f"   target: {target_full}\n"
        f"   reason: {reason}\n"
        f"   hint: request a handoff via `{root}` (or run: atwf handoff --as {root} <from> <to> --reason \"...\")"
    )


def cmd_init(args: argparse.Namespace) -> int:
    team_dir = _default_team_dir()
    registry = _registry_path(team_dir)

    _ensure_registry_file(registry, team_dir)

    task_content, task_source = _read_task_content(args)
    task_path = _ensure_task_and_design_files(team_dir, task_content=task_content, task_source=task_source)

    if args.registry_only:
        if task_path:
            _eprint(f"✅ shared task saved: {task_path}")
        return 0

    twf = _resolve_twf()
    trio = _init_trio(
        twf=twf,
        registry=registry,
        team_dir=team_dir,
        force_new=bool(args.force_new),
        no_bootstrap=bool(args.no_bootstrap),
    )

    root_role = _policy().root_role
    pm_full = trio.get("pm", "")
    if not pm_full:
        raise SystemExit("❌ failed to resolve PM worker")

    root_full = trio.get(root_role, "")
    liaison_full = trio.get("liaison", "")
    _eprint("✅ initial team ready:")
    if pm_full:
        _eprint(f"   pm:      {pm_full}")
    if root_full:
        _eprint(f"   {root_role}:   {root_full}")
    if liaison_full:
        _eprint(f"   liaison: {liaison_full}")
    _eprint(f"   tip: enter a role via: atwf attach pm|{root_role}|liaison")

    # If account_pool is enabled in twf_config and team_cycle is selected,
    # start a background watcher that rotates the whole team when limits are hit.
    _ensure_cap_watch_team(twf=twf, team_dir=team_dir, registry=registry)
    _ensure_watch_idle_team(twf=twf, team_dir=team_dir, registry=registry)

    if task_path:
        msg = "[TASK]\n" f"Shared task file: {task_path}\n" "Please read it and proceed.\n"
        sender_full = root_full.strip() or "atwf-init"
        sender_m = _resolve_member(_load_registry(registry), sender_full) or {}
        from_role = _member_role(sender_m) or root_role
        from_base = _member_base(sender_m) or sender_full

        pm_m = _resolve_member(_load_registry(registry), pm_full) or {}
        to_role = _member_role(pm_m) or "pm"
        to_base = _member_base(pm_m) or pm_full

        msg_id = _next_msg_id(team_dir)
        _write_inbox_message(
            team_dir,
            msg_id=msg_id,
            kind="task",
            from_full=sender_full,
            from_base=from_base,
            from_role=from_role,
            to_full=pm_full,
            to_base=to_base,
            to_role=to_role,
            body=msg,
        )
        notice = f"[INBOX] id={msg_id}\nopen: atwf inbox-open {msg_id}\nack: atwf inbox-ack {msg_id}\n"
        wrapped = _wrap_team_message(
            team_dir,
            kind="task",
            sender_full=sender_full,
            sender_role=from_role or None,
            to_full=pm_full,
            body=notice,
            msg_id=msg_id,
        )
        res = _run_twf(twf, ["ask", pm_full, wrapped])
        sys.stdout.write(res.stdout)
        sys.stderr.write(res.stderr)
        return res.returncode

    _eprint("   next: atwf init \"任务描述：...\" (or: atwf init --task-file /abs/path).")
    return 0


def _init_trio(
    *,
    twf: Path,
    registry: Path,
    team_dir: Path,
    force_new: bool,
    no_bootstrap: bool,
) -> dict[str, str]:
    expected_root = _expected_project_root()

    policy = _policy()
    root_role = policy.root_role

    want_pm = "pm"
    want_liaison = "liaison"
    required = {root_role, want_pm, want_liaison}
    missing = sorted(r for r in required if r not in policy.enabled_roles)
    if missing:
        raise SystemExit(f"❌ init requires enabled_roles to include: {', '.join(missing)}")

    base_root = _base_name(root_role, "main")

    child_roles = [r for r in [want_pm, want_liaison] if r != root_role]
    for child_role in child_roles:
        if child_role not in policy.can_hire.get(root_role, frozenset()):
            raise SystemExit(f"❌ policy.can_hire: {root_role} cannot hire {child_role} (init needs it)")

    init_children: list[tuple[str, str, str]] = []
    for child_role in child_roles:
        init_children.append(
            (
                child_role,
                _base_name(child_role, "main"),
                DEFAULT_ROLE_SCOPES.get(child_role, ""),
            )
        )

    out: dict[str, str] = {}

    def reuse_full(*, role: str, base: str) -> str | None:
        data0 = _load_registry(registry)
        m0 = _find_latest_member_by(data0, role=role, base=base)
        if not m0:
            return None
        candidate = str(m0.get("full", "")).strip() or None
        state_file = _member_state_file(m0)
        if not (candidate and state_file and state_file.is_file() and _state_file_matches_project(state_file, expected_root)):
            return None
        if not _tmux_running(candidate):
            _run_twf(twf, ["resume", candidate, "--no-tree"])
        return candidate if _tmux_running(candidate) else None

    def prune_role_base(*, role: str, base: str, keep_full: str | None) -> None:
        lock = team_dir / ".lock"
        with _locked(lock):
            data1 = _load_registry(registry)
            _prune_members_by(data1, role=role, base=base, keep_full=keep_full)
            _write_json_atomic(registry, data1)

    def up_root(*, role: str, base: str, scope: str) -> tuple[str, Path]:
        prune_role_base(role=role, base=base, keep_full=None)
        full, session_path = _start_worker(twf, base=base, up_args=[])
        lock = team_dir / ".lock"
        with _locked(lock):
            data2 = _load_registry(registry)
            _ensure_member(
                data2,
                full=full,
                base=base,
                role=role,
                scope=scope,
                parent=None,
                state_file=str(session_path),
            )
            _write_json_atomic(registry, data2)
        if not no_bootstrap:
            _bootstrap_worker(twf, name=full, role=role, full=full, base=base, registry=registry, team_dir=team_dir)
        return full, session_path

    def spawn_child(*, parent_full: str, role: str, base: str, scope: str) -> tuple[str, Path]:
        prune_role_base(role=role, base=base, keep_full=None)
        full, session_path = _spawn_worker(twf, parent_full=parent_full, child_base=base, up_args=[])
        lock = team_dir / ".lock"
        with _locked(lock):
            data3 = _load_registry(registry)
            _ensure_member(
                data3,
                full=full,
                base=base,
                role=role,
                scope=scope,
                parent=parent_full,
                state_file=str(session_path),
            )
            _add_child(data3, parent_full=parent_full, child_full=full)
            _write_json_atomic(registry, data3)
        if not no_bootstrap:
            _bootstrap_worker(twf, name=full, role=role, full=full, base=base, registry=registry, team_dir=team_dir)
        return full, session_path

    # 1) Root role via up (single root).
    root_full: str | None = None
    if not force_new:
        root_full = reuse_full(role=root_role, base=base_root)
    if root_full:
        prune_role_base(role=root_role, base=base_root, keep_full=root_full)
        lock = team_dir / ".lock"
        with _locked(lock):
            data_root = _load_registry(registry)
            _ensure_member(data_root, full=root_full, base=base_root, role=root_role, scope=DEFAULT_ROLE_SCOPES.get(root_role, ""), parent=None)
            _write_json_atomic(registry, data_root)
        out[root_role] = root_full
    else:
        root_full, _ = up_root(role=root_role, base=base_root, scope=DEFAULT_ROLE_SCOPES.get(root_role, ""))
        out[root_role] = root_full

    # 2) Children under root (PM + Liaison).
    for role, base, scope in init_children:
        child_full: str | None = None
        if not force_new:
            child_full = reuse_full(role=role, base=base)
        if child_full:
            prune_role_base(role=role, base=base, keep_full=child_full)
            lock = team_dir / ".lock"
            with _locked(lock):
                data_child = _load_registry(registry)
                _ensure_member(data_child, full=child_full, base=base, role=role, scope=scope, parent=root_full)
                _add_child(data_child, parent_full=root_full, child_full=child_full)
                _write_json_atomic(registry, data_child)
            out[role] = child_full
            continue

        child_full, _ = spawn_child(parent_full=root_full, role=role, base=base, scope=scope)
        out[role] = child_full

    return out


def _start_worker(twf: Path, *, base: str, up_args: list[str]) -> tuple[str, Path]:
    res = _run_twf(twf, ["up", base, *up_args])
    if res.returncode != 0:
        raise SystemExit(res.stderr.strip() or f"❌ twf up failed (code {res.returncode})")
    session_file = res.stdout.strip()
    if not session_file:
        raise SystemExit("❌ twf up returned empty session file path")
    session_path = _expand_path(session_file)
    full = session_path.stem
    return full, session_path


def _spawn_worker(twf: Path, *, parent_full: str, child_base: str, up_args: list[str]) -> tuple[str, Path]:
    res = _run_twf(twf, ["spawn", parent_full, child_base, *up_args])
    if res.returncode != 0:
        raise SystemExit(res.stderr.strip() or f"❌ twf spawn failed (code {res.returncode})")
    session_file = res.stdout.strip()
    if not session_file:
        raise SystemExit("❌ twf spawn returned empty session file path")
    session_path = _expand_path(session_file)
    full = session_path.stem
    return full, session_path


def _bootstrap_worker(
    twf: Path,
    *,
    name: str,
    role: str,
    full: str,
    base: str,
    registry: Path,
    team_dir: Path,
) -> None:
    pieces: list[str] = []

    rules_path = _templates_dir() / "command_rules.md"
    if rules_path.is_file():
        rules_raw = rules_path.read_text(encoding="utf-8")
        pieces.append(_render_template(rules_raw, role=role, full=full, base=base, registry=registry, team_dir=team_dir).strip())

    template_path = _template_for_role(role)
    raw = template_path.read_text(encoding="utf-8")
    pieces.append(_render_template(raw, role=role, full=full, base=base, registry=registry, team_dir=team_dir).strip())

    msg = "\n\n---\n\n".join(pieces).strip() + "\n"
    msg_id = _next_msg_id(team_dir)
    _write_inbox_message(
        team_dir,
        msg_id=msg_id,
        kind="bootstrap",
        from_full="atwf-bootstrap",
        from_base="atwf",
        from_role="system",
        to_full=name,
        to_base=base,
        to_role=role,
        body=msg,
    )
    notice = (
        f"[BOOTSTRAP-INBOX] id={msg_id}\n"
        f"open: bash .codex/skills/ai-team-workflow/scripts/atwf inbox-open {msg_id}\n"
        f"ack:  bash .codex/skills/ai-team-workflow/scripts/atwf inbox-ack {msg_id}\n"
    )
    wrapped = _wrap_team_message(
        team_dir,
        kind="bootstrap",
        sender_full="atwf-bootstrap",
        sender_role=None,
        to_full=name,
        body=notice,
        msg_id=msg_id,
    )
    # Bootstrap should never block on a reply.
    res = _run_twf(twf, ["send", name, wrapped])
    if res.returncode != 0:
        _eprint(res.stderr.strip() or f"⚠️ twf send failed (code {res.returncode})")


def cmd_up(args: argparse.Namespace) -> int:
    twf = _resolve_twf()
    team_dir = _default_team_dir()
    registry = _registry_path(team_dir)
    role = _require_role(args.role)
    policy = _policy()
    if role != policy.root_role:
        raise SystemExit(f"❌ up only allowed for root_role={policy.root_role}. Use `atwf spawn` / `atwf spawn-self`.")

    data0 = _load_registry(registry)
    existing_roots = []
    for m in data0.get("members", []) if isinstance(data0.get("members"), list) else []:
        if not isinstance(m, dict):
            continue
        if str(m.get("role", "")).strip() != policy.root_role:
            continue
        parent = m.get("parent")
        parent_s = str(parent).strip() if isinstance(parent, str) else ""
        if not parent_s:
            existing_roots.append(str(m.get("full", "")).strip())
    if existing_roots:
        raise SystemExit(f"❌ root already exists in registry (use `atwf init` / `atwf resume`): {existing_roots[0]}")

    base = _base_name(role, args.label)

    full, session_path = _start_worker(twf, base=base, up_args=[])

    lock = team_dir / ".lock"
    with _locked(lock):
        data = _load_registry(registry)
        _ensure_member(
            data,
            full=full,
            base=base,
            role=role,
            scope=args.scope or "",
            parent=None,
            state_file=str(session_path),
        )
        _write_json_atomic(registry, data)

    if not args.no_bootstrap:
        _bootstrap_worker(
            twf,
            name=full,
            role=role,
            full=full,
            base=base,
            registry=registry,
            team_dir=team_dir,
        )

    _ensure_cap_watch_team(twf=twf, team_dir=team_dir, registry=registry)
    _ensure_watch_idle_team(twf=twf, team_dir=team_dir, registry=registry)

    print(full)
    return 0


def cmd_spawn(args: argparse.Namespace) -> int:
    twf = _resolve_twf()
    team_dir = _default_team_dir()
    registry = _registry_path(team_dir)

    parent_raw = args.parent_full.strip()
    if not parent_raw:
        raise SystemExit("❌ parent-full is required")

    data0 = _load_registry(registry)
    parent_full = _resolve_target_full(data0, parent_raw)
    if not parent_full:
        raise SystemExit(f"❌ parent not found in registry: {parent_raw}")

    role = _require_role(args.role)
    base = _base_name(role, args.label)

    parent_m = _resolve_member(data0, parent_full)
    if not parent_m:
        raise SystemExit(f"❌ parent not found in registry: {parent_full}")
    parent_role = str(parent_m.get("role", "")).strip()
    if not parent_role:
        raise SystemExit(f"❌ parent has no role recorded: {parent_full}")
    policy = _policy()
    allowed = policy.can_hire.get(parent_role, frozenset())
    if role not in allowed:
        raise SystemExit(
            f"❌ policy.can_hire: {parent_role} cannot hire {role}. "
            f"Allowed: {', '.join(sorted(allowed)) or '(none)'}"
        )

    full, session_path = _spawn_worker(twf, parent_full=parent_full, child_base=base, up_args=[])

    lock = team_dir / ".lock"
    with _locked(lock):
        data = _load_registry(registry)
        _ensure_member(
            data,
            full=full,
            base=base,
            role=role,
            scope=args.scope or "",
            parent=parent_full,
            state_file=str(session_path),
        )
        _add_child(data, parent_full=parent_full, child_full=full)
        _write_json_atomic(registry, data)

    if not args.no_bootstrap:
        _bootstrap_worker(
            twf,
            name=full,
            role=role,
            full=full,
            base=base,
            registry=registry,
            team_dir=team_dir,
        )

    _ensure_cap_watch_team(twf=twf, team_dir=team_dir, registry=registry)
    _ensure_watch_idle_team(twf=twf, team_dir=team_dir, registry=registry)

    print(full)
    return 0


def cmd_spawn_self(args: argparse.Namespace) -> int:
    res = _run(["tmux", "display-message", "-p", "#S"])
    if res.returncode != 0:
        raise SystemExit("❌ spawn-self must run inside tmux")
    parent_full = res.stdout.strip()
    if not parent_full:
        raise SystemExit("❌ failed to detect current tmux session name")

    ns = argparse.Namespace(
        parent_full=parent_full,
        role=args.role,
        label=args.label,
        scope=args.scope,
        no_bootstrap=args.no_bootstrap,
    )
    return cmd_spawn(ns)


def cmd_parent(args: argparse.Namespace) -> int:
    team_dir = _default_team_dir()
    registry = _registry_path(team_dir)
    data = _load_registry(registry)

    name = args.name.strip()
    if not name:
        raise SystemExit("❌ name is required")

    m = _resolve_member(data, name)
    if not m:
        raise SystemExit(f"❌ member not found in registry: {name}")

    parent = m.get("parent")
    parent_s = str(parent).strip() if isinstance(parent, str) else ""
    print(parent_s if parent_s else "(none)")
    return 0


def cmd_parent_self(_: argparse.Namespace) -> int:
    res = _run(["tmux", "display-message", "-p", "#S"])
    if res.returncode != 0:
        raise SystemExit("❌ parent-self must run inside tmux")
    name = res.stdout.strip()
    ns = argparse.Namespace(name=name)
    return cmd_parent(ns)


def cmd_children(args: argparse.Namespace) -> int:
    team_dir = _default_team_dir()
    registry = _registry_path(team_dir)
    data = _load_registry(registry)

    name = args.name.strip()
    if not name:
        raise SystemExit("❌ name is required")

    m = _resolve_member(data, name)
    if not m:
        raise SystemExit(f"❌ member not found in registry: {name}")

    children = m.get("children")
    if not isinstance(children, list):
        children = []
    out = [str(c).strip() for c in children if isinstance(c, str) and c.strip()]
    if not out:
        print("(none)")
        return 0
    print("\n".join(out))
    return 0


def cmd_children_self(_: argparse.Namespace) -> int:
    res = _run(["tmux", "display-message", "-p", "#S"])
    if res.returncode != 0:
        raise SystemExit("❌ children-self must run inside tmux")
    name = res.stdout.strip()
    ns = argparse.Namespace(name=name)
    return cmd_children(ns)


def _read_report_body(args_message: str | None) -> str:
    msg = args_message
    if msg is None:
        msg = _forward_stdin()
    msg = (msg or "").strip()
    if not msg:
        raise SystemExit("❌ report message missing (provide as arg or via stdin)")
    return msg


def _format_report(*, sender: dict[str, Any], to_full: str, body: str) -> str:
    role = str(sender.get("role", "")).strip()
    base = str(sender.get("base", "")).strip()
    full = str(sender.get("full", "")).strip()
    scope = str(sender.get("scope", "")).strip()
    ts = _now()

    header = [
        f"[REPORT] {ts}",
        f"from: {full} (role={role} base={base})",
        f"to:   {to_full}",
    ]
    if scope:
        header.append(f"scope: {scope}")
    header.append("---")
    return "\n".join(header) + "\n" + body.strip() + "\n"


def cmd_report_up(args: argparse.Namespace) -> int:
    team_dir = _default_team_dir()
    registry = _registry_path(team_dir)

    res = _run(["tmux", "display-message", "-p", "#S"])
    if res.returncode != 0:
        raise SystemExit("❌ report-up must run inside tmux")
    self_name = res.stdout.strip()
    if not self_name:
        raise SystemExit("❌ failed to detect current tmux session name")

    data = _load_registry(registry)
    sender = _resolve_member(data, self_name)
    if not sender:
        raise SystemExit(f"❌ current worker not found in registry: {self_name} (run: atwf register-self ...)")

    parent = sender.get("parent")
    parent_full = str(parent).strip() if isinstance(parent, str) else ""
    if not parent_full:
        raise SystemExit("❌ no parent recorded for this worker (root). Use report-to <coord|liaison|name> instead.")

    parent_m = _resolve_member(data, parent_full) or {}
    to_role = _member_role(parent_m)
    to_base = _member_base(parent_m) or parent_full

    body = _read_report_body(args.message)
    msg = _format_report(sender=sender, to_full=parent_full, body=body)

    from_role = str(sender.get("role", "")).strip()
    from_base = _member_base(sender) or self_name
    msg_id = _next_msg_id(team_dir)
    _write_inbox_message(
        team_dir,
        msg_id=msg_id,
        kind="report-up",
        from_full=self_name,
        from_base=from_base,
        from_role=from_role,
        to_full=parent_full,
        to_base=to_base,
        to_role=to_role,
        body=msg,
    )
    notice = f"[INBOX] id={msg_id}\nopen: atwf inbox-open {msg_id}\nack: atwf inbox-ack {msg_id}\n"
    wrapped = _wrap_team_message(
        team_dir,
        kind="report-up",
        sender_full=self_name,
        sender_role=from_role or None,
        to_full=parent_full,
        body=notice,
        msg_id=msg_id,
    )

    # Default: inbox-only delivery (no CLI injection). This avoids consuming the
    # recipient's Codex context. Recipients must poll inbox while working.
    if not bool(getattr(args, "wait", False)):
        print(msg_id)
        return 0

    # Exceptional: allow an explicit blocking request (CLI injection) when the
    # operator intentionally chooses to wait for a reply.
    twf = _resolve_twf()
    res2 = _run_twf(twf, ["ask", parent_full, wrapped])
    sys.stdout.write(res2.stdout)
    sys.stderr.write(res2.stderr)
    return res2.returncode


def cmd_report_to(args: argparse.Namespace) -> int:
    team_dir = _default_team_dir()
    registry = _registry_path(team_dir)

    target = args.target.strip()
    if not target:
        raise SystemExit("❌ target is required")

    data = _load_registry(registry)

    to_full = _resolve_target_full(data, target)
    if not to_full:
        raise SystemExit(f"❌ target not found in registry: {target}")

    self_name = _tmux_self_full()
    if not self_name:
        raise SystemExit("❌ report-to must run inside tmux")

    sender = _resolve_member(data, self_name)
    if not sender:
        raise SystemExit(f"❌ current worker not found in registry: {self_name} (run: atwf register-self ...)")

    policy = _policy()
    _require_comm_allowed(policy, data, actor_full=self_name, target_full=to_full)

    target_m = _resolve_member(data, to_full) or {}
    to_role = _member_role(target_m)
    to_base = _member_base(target_m) or to_full

    body = _read_report_body(args.message)
    msg = _format_report(sender=sender, to_full=to_full, body=body)

    from_role = str(sender.get("role", "")).strip()
    from_base = _member_base(sender) or self_name
    msg_id = _next_msg_id(team_dir)
    _write_inbox_message(
        team_dir,
        msg_id=msg_id,
        kind="report-to",
        from_full=self_name,
        from_base=from_base,
        from_role=from_role,
        to_full=to_full,
        to_base=to_base,
        to_role=to_role,
        body=msg,
    )
    notice = f"[INBOX] id={msg_id}\nopen: atwf inbox-open {msg_id}\nack: atwf inbox-ack {msg_id}\n"
    wrapped = _wrap_team_message(
        team_dir,
        kind="report-to",
        sender_full=self_name,
        sender_role=from_role or None,
        to_full=to_full,
        body=notice,
        msg_id=msg_id,
    )

    # Default: inbox-only delivery (no CLI injection).
    if not bool(getattr(args, "wait", False)):
        print(msg_id)
        return 0

    # Exceptional: blocking request (CLI injection) when --wait is used.
    twf = _resolve_twf()
    res2 = _run_twf(twf, ["ask", to_full, wrapped])
    sys.stdout.write(res2.stdout)
    sys.stderr.write(res2.stderr)
    return res2.returncode


def cmd_self(_: argparse.Namespace) -> int:
    res = _run(["tmux", "display-message", "-p", "#S"])
    if res.returncode != 0:
        raise SystemExit("❌ not inside tmux (or tmux unavailable)")
    print(res.stdout.strip())
    return 0


def cmd_register(args: argparse.Namespace) -> int:
    team_dir = _default_team_dir()
    registry = _registry_path(team_dir)

    full = args.full.strip()
    if not full:
        raise SystemExit("❌ full name is required")

    base = args.base.strip() if args.base else None
    role = _require_role(args.role) if args.role else None
    policy = _policy()

    lock = team_dir / ".lock"
    with _locked(lock):
        data = _load_registry(registry)
        existing = _resolve_member(data, full)
        existing_role = str(existing.get("role", "")).strip() if isinstance(existing, dict) else ""
        existing_parent = existing.get("parent") if isinstance(existing, dict) else None
        existing_parent_s = str(existing_parent).strip() if isinstance(existing_parent, str) else ""

        resolved_parent: str | None = None
        if args.parent is not None:
            parent_raw = str(args.parent).strip()
            if parent_raw:
                resolved_parent = _resolve_target_full(data, parent_raw) or (parent_raw if FULL_NAME_RE.match(parent_raw) else None)
                if not resolved_parent:
                    raise SystemExit(f"❌ parent not found in registry: {parent_raw}")
            else:
                resolved_parent = ""

        final_role = role or existing_role
        final_parent = existing_parent_s if args.parent is None else (resolved_parent or "")
        force = bool(getattr(args, "force", False))
        if final_role:
            if final_role == policy.root_role:
                if final_parent and not force:
                    raise SystemExit(f"❌ root_role={policy.root_role} cannot have a parent (use --force to override)")
            else:
                if not final_parent and not force:
                    raise SystemExit(
                        f"❌ non-root roles must have a parent (root_role={policy.root_role}). "
                        f"Use `atwf spawn`/`spawn-self` or pass --parent/--force."
                    )
                parent_m = _resolve_member(data, final_parent) if final_parent else None
                parent_role = _member_role(parent_m)
                allowed = policy.can_hire.get(parent_role, frozenset())
                if final_parent and (not parent_m or final_role not in allowed) and not force:
                    raise SystemExit(
                        f"❌ policy.can_hire: {parent_role or '(missing)'} cannot hire {final_role}. "
                        f"Allowed: {', '.join(sorted(allowed)) or '(none)'}"
                    )

        _ensure_member(
            data,
            full=full,
            base=base,
            role=role,
            scope=args.scope,
            parent=(resolved_parent if args.parent is not None else None),
            state_file=args.state_file,
        )
        if args.parent is not None and resolved_parent:
            _add_child(data, parent_full=resolved_parent, child_full=full)
        _write_json_atomic(registry, data)
    _eprint(f"✅ registered: {full}")
    return 0


def cmd_register_self(args: argparse.Namespace) -> int:
    res = _run(["tmux", "display-message", "-p", "#S"])
    if res.returncode != 0:
        raise SystemExit("❌ register-self must run inside tmux")
    full = res.stdout.strip()

    ns = argparse.Namespace(
        full=full,
        role=args.role,
        base=args.base,
        scope=args.scope,
        parent=args.parent,
        state_file=args.state_file,
        force=getattr(args, "force", False),
    )
    return cmd_register(ns)


def cmd_set_scope(args: argparse.Namespace) -> int:
    team_dir = _default_team_dir()
    registry = _registry_path(team_dir)

    name = args.name.strip()
    if not name:
        raise SystemExit("❌ name is required")
    scope = args.scope

    lock = team_dir / ".lock"
    with _locked(lock):
        data = _load_registry(registry)
        m = _resolve_member(data, name)
        if not m:
            raise SystemExit(f"❌ member not found in registry: {name}")
        full = str(m.get("full", "")).strip() or name
        _ensure_member(data, full=full, scope=scope)
        _write_json_atomic(registry, data)
    _eprint(f"✅ scope updated: {name}")
    return 0


def cmd_set_scope_self(args: argparse.Namespace) -> int:
    res = _run(["tmux", "display-message", "-p", "#S"])
    if res.returncode != 0:
        raise SystemExit("❌ set-scope-self must run inside tmux")
    name = res.stdout.strip()
    ns = argparse.Namespace(name=name, scope=args.scope)
    return cmd_set_scope(ns)


def cmd_list(_: argparse.Namespace) -> int:
    team_dir = _default_team_dir()
    registry = _registry_path(team_dir)
    data = _load_registry(registry)
    members = data.get("members", [])
    if not isinstance(members, list) or not members:
        print("(empty)")
        return 0

    def cell(v: Any) -> str:
        s = str(v) if v is not None else ""
        return " ".join(s.split())

    rows = []
    for m in members:
        if not isinstance(m, dict):
            continue
        rows.append(
            (
                cell(m.get("role", "")),
                cell(m.get("base", "")),
                cell(m.get("full", "")),
                cell(m.get("parent", "")),
                cell(m.get("scope", "")),
            )
        )

    widths = [0, 0, 0, 0, 0]
    for r in rows:
        for i, c in enumerate(r):
            widths[i] = max(widths[i], len(c))
    header = ("role", "base", "full", "parent", "scope")
    widths = [max(widths[i], len(header[i])) for i in range(5)]

    def fmt(r: tuple[str, str, str, str, str]) -> str:
        return "  ".join(r[i].ljust(widths[i]) for i in range(5))

    print(fmt(header))
    print(fmt(tuple("-" * w for w in widths)))  # type: ignore[arg-type]
    for r in rows:
        print(fmt(r))
    return 0


def cmd_where(_: argparse.Namespace) -> int:
    team_dir = _default_team_dir()
    registry = _registry_path(team_dir)
    print(str(team_dir))
    print(str(registry))
    return 0


def cmd_policy(_: argparse.Namespace) -> int:
    policy = _policy()
    print(f"config: {_config_file()}")
    print(f"root_role: {policy.root_role}")
    print(f"enabled_roles: {', '.join(sorted(policy.enabled_roles))}")

    print("can_hire:")
    for parent in sorted(policy.can_hire):
        kids = sorted(policy.can_hire.get(parent, frozenset()))
        print(f"  {parent}: {', '.join(kids) if kids else '(none)'}")

    print(f"broadcast.allowed_roles: {', '.join(sorted(policy.broadcast_allowed_roles)) or '(none)'}")
    print(f"broadcast.exclude_roles: {', '.join(sorted(policy.broadcast_exclude_roles)) or '(none)'}")

    print(f"comm.allow_parent_child: {policy.comm_allow_parent_child}")
    print(f"comm.require_handoff: {policy.comm_require_handoff}")
    print(f"comm.handoff_creators: {', '.join(sorted(policy.comm_handoff_creators)) or '(none)'}")

    print("comm.direct_allow:")
    for role in sorted(policy.enabled_roles):
        allowed = sorted(policy.comm_direct_allow.get(role, frozenset()))
        if not allowed:
            continue
        print(f"  {role}: {', '.join(allowed)}")
    return 0


def cmd_perms_self(_: argparse.Namespace) -> int:
    team_dir = _default_team_dir()
    registry = _registry_path(team_dir)
    data = _load_registry(registry)
    policy = _policy()

    self_full = _tmux_self_full()
    if not self_full:
        raise SystemExit("❌ perms-self must run inside tmux")

    self_m = _resolve_member(data, self_full)
    if not self_m:
        raise SystemExit(f"❌ current worker not found in registry: {self_full} (run: atwf register-self ...)")

    role = _member_role(self_m)
    base = _member_base(self_m)
    parent = str(self_m.get("parent", "")).strip() if isinstance(self_m.get("parent"), str) else ""

    print(f"full: {self_full}")
    print(f"role: {role or '(missing)'}")
    print(f"base: {base}")
    print(f"parent: {parent or '(none)'}")
    print(f"can_broadcast: {role in policy.broadcast_allowed_roles}")
    print(f"can_create_handoff: {role in policy.comm_handoff_creators}")
    print(f"can_hire: {', '.join(sorted(policy.can_hire.get(role, frozenset()))) or '(none)'}")
    print(f"direct_allow_roles: {', '.join(sorted(policy.comm_direct_allow.get(role, frozenset()))) or '(none)'}")

    peers: list[str] = []
    permits = data.get("permits")
    if isinstance(permits, list):
        for p in permits:
            if not isinstance(p, dict):
                continue
            a = str(p.get("a", "")).strip()
            b = str(p.get("b", "")).strip()
            if not a or not b:
                continue
            other = ""
            if a == base:
                other = b
            elif b == base:
                other = a
            if not other:
                continue
            exp = str(p.get("expires_at", "")).strip()
            if exp:
                try:
                    if datetime.fromisoformat(exp) <= datetime.now():
                        continue
                except Exception:
                    pass
            peers.append(other)
    uniq_peers = sorted({p for p in peers if p})
    print(f"active_handoff_peers: {', '.join(uniq_peers) if uniq_peers else '(none)'}")
    return 0


def cmd_handoff(args: argparse.Namespace) -> int:
    team_dir = _default_team_dir()
    registry = _registry_path(team_dir)
    policy = _policy()

    lock = team_dir / ".lock"
    dry_run = bool(getattr(args, "dry_run", False))
    permit: dict[str, Any] | None = None
    permit_exists = False
    with _locked(lock):
        data = _load_registry(registry)
        actor_full = _resolve_actor_full(data, as_target=getattr(args, "as_target", None))
        actor_m = _resolve_member(data, actor_full)
        if not actor_m:
            raise SystemExit(f"❌ actor not found in registry: {actor_full}")
        actor_role = _member_role(actor_m)
        if actor_role not in policy.comm_handoff_creators:
            raise SystemExit(
                "❌ handoff not permitted by policy.\n"
                f"   actor: {actor_full} (role={actor_role or '?'})\n"
                f"   allowed_roles: {', '.join(sorted(policy.comm_handoff_creators)) or '(none)'}"
            )

        a_full = _resolve_target_full(data, args.a)
        if not a_full:
            raise SystemExit(f"❌ member not found in registry: {args.a}")
        b_full = _resolve_target_full(data, args.b)
        if not b_full:
            raise SystemExit(f"❌ member not found in registry: {args.b}")
        a_m = _resolve_member(data, a_full)
        b_m = _resolve_member(data, b_full)
        if not a_m or not b_m:
            raise SystemExit("❌ handoff endpoints must be registered members")

        a_base = _member_base(a_m)
        b_base = _member_base(b_m)
        permit_exists = _permit_allows(data, a_base=a_base, b_base=b_base)
        if not permit_exists and not dry_run:
            permit = _add_handoff_permit(
                data,
                a_base=a_base,
                b_base=b_base,
                created_by=actor_full,
                created_by_role=actor_role,
                reason=str(getattr(args, "reason", "") or ""),
                ttl_seconds=(int(args.ttl) if getattr(args, "ttl", None) is not None else None),
            )
            _write_json_atomic(registry, data)

    if dry_run:
        print("dry_run: true")
        print(f"actor: {actor_full}")
        print(f"a: {a_full}")
        print(f"b: {b_full}")
        print(f"permit_exists: {str(permit_exists).lower()}")
        if not permit_exists:
            print("permit_id: (would-create)")
        return 0

    exp_s = ""
    if permit:
        exp_s = str(permit.get("expires_at", "")).strip()
    reason = str(getattr(args, "reason", "") or "").strip()
    reason_line = f"reason: {reason}\n" if reason else ""
    exp_line = f"expires_at: {exp_s}\n" if exp_s else ""

    msg_a = (
        "[HANDOFF]\n"
        f"creator: {actor_full} (role={actor_role or '?'})\n"
        f"peer: {b_base} ({b_full})\n"
        f"{reason_line}{exp_line}"
        "You are permitted to talk directly. Use:\n"
        f"- atwf send {b_base} \"...\"  # inbox-only by default; peer must poll inbox while working\n"
    )
    msg_b = (
        "[HANDOFF]\n"
        f"creator: {actor_full} (role={actor_role or '?'})\n"
        f"peer: {a_base} ({a_full})\n"
        f"{reason_line}{exp_line}"
        "Please reply directly to the requester (avoid relaying via coord).\n"
        "Use:\n"
        f"- atwf send {a_base} \"...\"  # inbox-only by default; peer must poll inbox while working\n"
    )

    handoff_id = _next_msg_id(team_dir)
    notice = f"[INBOX] id={handoff_id}\nopen: atwf inbox-open {handoff_id}\nack: atwf inbox-ack {handoff_id}\n"

    _write_inbox_message(
        team_dir,
        msg_id=handoff_id,
        kind="handoff",
        from_full=actor_full,
        from_base=_member_base(actor_m) or actor_full,
        from_role=actor_role or "?",
        to_full=a_full,
        to_base=a_base,
        to_role=_member_role(a_m) or "?",
        body=msg_a,
    )
    _write_inbox_message(
        team_dir,
        msg_id=handoff_id,
        kind="handoff",
        from_full=actor_full,
        from_base=_member_base(actor_m) or actor_full,
        from_role=actor_role or "?",
        to_full=b_full,
        to_base=b_base,
        to_role=_member_role(b_m) or "?",
        body=msg_b,
    )

    wrapped_a = _wrap_team_message(
        team_dir,
        kind="handoff",
        sender_full=actor_full,
        sender_role=actor_role or None,
        to_full=a_full,
        body=notice,
        msg_id=handoff_id,
    )
    wrapped_b = _wrap_team_message(
        team_dir,
        kind="handoff",
        sender_full=actor_full,
        sender_role=actor_role or None,
        to_full=b_full,
        body=notice,
        msg_id=handoff_id,
    )

    if bool(getattr(args, "notify", False)):
        twf = _resolve_twf()
        res_a = _run_twf(twf, ["send", a_full, wrapped_a])
        if res_a.returncode != 0:
            _eprint(res_a.stderr.strip() or f"⚠️ notify failed: {a_full}")
        res_b = _run_twf(twf, ["send", b_full, wrapped_b])
        if res_b.returncode != 0:
            _eprint(res_b.stderr.strip() or f"⚠️ notify failed: {b_full}")

    print(str(permit.get("id", "")) if permit else "(existing)")
    return 0


def _tmux_running(session: str) -> bool:
    if not session.strip():
        return False
    res = subprocess.run(["tmux", "has-session", "-t", session], check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return res.returncode == 0


def _tmux_capture_tail(session: str, *, lines: int) -> str | None:
    if not session.strip():
        return None
    n = int(lines) if int(lines) > 0 else 200
    start = f"-{n}"
    res = subprocess.run(
        ["tmux", "capture-pane", "-p", "-t", session, "-S", start],
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        text=True,
    )
    if res.returncode != 0:
        return None
    return res.stdout


def _tmux_send_enter(session: str) -> bool:
    if not session.strip():
        return False
    res = subprocess.run(
        ["tmux", "send-keys", "-t", session, "C-m"],
        check=False,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return res.returncode == 0


def _text_digest(raw: str) -> str:
    s = (raw or "").replace("\r\n", "\n").replace("\r", "\n")
    return hashlib.sha1(s.encode("utf-8", errors="ignore")).hexdigest()


def _tree_children(data: dict[str, Any]) -> dict[str, list[str]]:
    members = data.get("members", [])
    if not isinstance(members, list):
        return {}

    out: dict[str, list[str]] = {}

    for m in members:
        if not isinstance(m, dict):
            continue
        full = str(m.get("full", "")).strip()
        if not full:
            continue
        parent = m.get("parent")
        parent_full = str(parent).strip() if isinstance(parent, str) else ""
        if parent_full:
            out.setdefault(parent_full, []).append(full)

    # Merge explicit children lists (if present).
    for m in members:
        if not isinstance(m, dict):
            continue
        full = str(m.get("full", "")).strip()
        if not full:
            continue
        children = m.get("children")
        if not isinstance(children, list):
            continue
        for c in children:
            child = str(c).strip() if isinstance(c, str) else ""
            if not child:
                continue
            out.setdefault(full, []).append(child)

    # Dedup + stable sort.
    for k, v in list(out.items()):
        uniq: list[str] = []
        seen: set[str] = set()
        for child in v:
            if child not in seen:
                seen.add(child)
                uniq.append(child)
        out[k] = sorted(uniq)

    return out


def _tree_roots(data: dict[str, Any]) -> list[str]:
    members = data.get("members", [])
    if not isinstance(members, list):
        return []

    fulls = []
    for m in members:
        if not isinstance(m, dict):
            continue
        full = str(m.get("full", "")).strip()
        if full:
            fulls.append(full)

    known = set(fulls)
    roots = []
    for m in members:
        if not isinstance(m, dict):
            continue
        full = str(m.get("full", "")).strip()
        if not full:
            continue
        parent = m.get("parent")
        parent_full = str(parent).strip() if isinstance(parent, str) else ""
        if not parent_full or parent_full not in known:
            roots.append(full)

    # Stable-ish order by updated_at desc when available.
    def key(full: str) -> str:
        mm = _resolve_member(data, full)
        return str(mm.get("updated_at", "")) if mm else ""

    roots.sort(key=key, reverse=True)
    return roots


def cmd_tree(args: argparse.Namespace) -> int:
    team_dir = _default_team_dir()
    registry = _registry_path(team_dir)
    data = _load_registry(registry)

    members = data.get("members", [])
    if not isinstance(members, list) or not members:
        print("(empty)")
        return 0

    root_fulls: list[str]
    if getattr(args, "root", None):
        target = str(args.root).strip()
        if not target:
            raise SystemExit("❌ root is required")
        full = _resolve_target_full(data, target)
        if not full:
            raise SystemExit(f"❌ target not found in registry: {target}")
        root_fulls = [full]
    else:
        root_fulls = _tree_roots(data)

    children_map = _tree_children(data)
    visited: set[str] = set()

    def label(full: str) -> str:
        m = _resolve_member(data, full) or {}
        role = str(m.get("role", "")).strip()
        scope = str(m.get("scope", "")).strip()
        status = "running" if _tmux_running(full) else "stopped"
        parts = [f"[{role or '?'}]", full, f"({status})"]
        if scope:
            parts.append(f"- {scope}")
        return " ".join(parts)

    def walk(full: str, indent: str) -> None:
        if full in visited:
            print(f"{indent}{label(full)}  (cycle)")
            return
        visited.add(full)
        print(f"{indent}{label(full)}")
        for child in children_map.get(full, []):
            walk(child, indent + "  ")

    for i, root in enumerate(root_fulls):
        if i > 0:
            print("")
        walk(root, "")
    return 0


def cmd_design_path(args: argparse.Namespace) -> int:
    team_dir = _default_team_dir()
    registry = _registry_path(team_dir)
    data = _load_registry(registry)

    target = args.target.strip()
    if not target:
        raise SystemExit("❌ target is required")

    full = _resolve_target_full(data, target)
    if not full:
        raise SystemExit(f"❌ target not found in registry: {target}")

    print(str(_design_member_path(team_dir, full)))
    return 0


def cmd_design_init(args: argparse.Namespace) -> int:
    team_dir = _default_team_dir()
    registry = _registry_path(team_dir)
    data = _load_registry(registry)

    target = args.target.strip()
    if not target:
        raise SystemExit("❌ target is required")

    full = _resolve_target_full(data, target)
    if not full:
        raise SystemExit(f"❌ target not found in registry: {target}")

    _ensure_share_layout(team_dir)
    path = _design_member_path(team_dir, full)
    if path.exists() and not args.force:
        print(str(path))
        return 0

    m = _resolve_member(data, full) or {}
    _write_text_atomic(path, _design_seed(member=m, full=full, team_dir=team_dir))
    print(str(path))
    return 0


def cmd_design_init_self(args: argparse.Namespace) -> int:
    res = _run(["tmux", "display-message", "-p", "#S"])
    if res.returncode != 0:
        raise SystemExit("❌ design-init-self must run inside tmux")
    full = res.stdout.strip()
    if not full:
        raise SystemExit("❌ failed to detect current tmux session name")
    ns = argparse.Namespace(target=full, force=bool(args.force))
    return cmd_design_init(ns)


def _git_root() -> Path:
    # Prefer the "common" git dir so worktree commands behave consistently even
    # when invoked from inside a linked worktree (where --show-toplevel returns
    # the worktree path, not the project root).
    res = _run(["git", "rev-parse", "--git-common-dir"])
    if res.returncode == 0:
        raw = res.stdout.strip()
        if raw:
            common_dir = Path(raw)
            if not common_dir.is_absolute():
                common_dir = (Path.cwd() / common_dir).resolve()
            else:
                common_dir = common_dir.resolve()
            root = common_dir.parent.resolve()
            if root.is_dir():
                return root

    res = _run(["git", "rev-parse", "--show-toplevel"])
    if res.returncode != 0:
        raise SystemExit("❌ not a git repository (needed for worktree commands)")
    root = res.stdout.strip()
    if not root:
        raise SystemExit("❌ failed to detect git root")
    return Path(root).resolve()


def _worktrees_dir(git_root: Path) -> Path:
    return git_root / "worktree"


def _worktree_path(git_root: Path, full: str) -> Path:
    return _worktrees_dir(git_root) / full.strip()


def cmd_worktree_path(args: argparse.Namespace) -> int:
    team_dir = _default_team_dir()
    registry = _registry_path(team_dir)
    data = _load_registry(registry)

    target = args.target.strip()
    if not target:
        raise SystemExit("❌ target is required")

    full = _resolve_target_full(data, target)
    if not full:
        raise SystemExit(f"❌ target not found in registry: {target}")

    git_root = _git_root()
    print(str(_worktree_path(git_root, full)))
    return 0


def cmd_worktree_create(args: argparse.Namespace) -> int:
    team_dir = _default_team_dir()
    registry = _registry_path(team_dir)
    data = _load_registry(registry)

    target = args.target.strip()
    if not target:
        raise SystemExit("❌ target is required")

    full = _resolve_target_full(data, target)
    if not full:
        raise SystemExit(f"❌ target not found in registry: {target}")

    git_root = _git_root()
    wt_dir = _worktrees_dir(git_root)
    wt_dir.mkdir(parents=True, exist_ok=True)

    path = _worktree_path(git_root, full)
    base = (args.base or "HEAD").strip() or "HEAD"
    branch = (args.branch or full).strip() or full

    if path.exists():
        print(str(path))
        return 0

    res = _run(["git", "worktree", "add", "-b", branch, str(path), base])
    if res.returncode != 0:
        err = (res.stderr or "").strip()
        raise SystemExit(err or f"❌ git worktree add failed (code {res.returncode})")

    print(str(path))
    return 0


def cmd_worktree_create_self(args: argparse.Namespace) -> int:
    res = _run(["tmux", "display-message", "-p", "#S"])
    if res.returncode != 0:
        raise SystemExit("❌ worktree-create-self must run inside tmux")
    full = res.stdout.strip()
    if not full:
        raise SystemExit("❌ failed to detect current tmux session name")
    ns = argparse.Namespace(target=full, base=args.base, branch=args.branch)
    return cmd_worktree_create(ns)


def cmd_worktree_check_self(_: argparse.Namespace) -> int:
    res = _run(["tmux", "display-message", "-p", "#S"])
    if res.returncode != 0:
        raise SystemExit("❌ worktree-check-self must run inside tmux")
    full = res.stdout.strip()
    if not full:
        raise SystemExit("❌ failed to detect current tmux session name")

    git_root = _git_root()
    expected = _worktree_path(git_root, full).resolve()
    cwd = Path.cwd().resolve()

    if expected == cwd or expected in cwd.parents:
        print("OK")
        return 0

    _eprint("❌ not in your dedicated worktree")
    _eprint(f"   expected: {expected}")
    _eprint(f"   cwd:      {cwd}")
    _eprint(f"   fix:      bash .codex/skills/ai-team-workflow/scripts/atwf worktree-create-self && cd {expected}")
    return 1


def _members_by_role(data: dict[str, Any], role: str) -> list[str]:
    role = role.strip()
    members = data.get("members", [])
    if not isinstance(members, list):
        return []
    out = []
    for m in members:
        if not isinstance(m, dict):
            continue
        if str(m.get("role", "")).strip() != role:
            continue
        full = str(m.get("full", "")).strip()
        if full:
            out.append(full)
    return sorted(set(out))


def _subtree_fulls(data: dict[str, Any], root_full: str) -> list[str]:
    root_full = root_full.strip()
    if not root_full:
        return []
    children_map = _tree_children(data)
    out: list[str] = []
    seen: set[str] = set()
    stack = [root_full]
    while stack:
        cur = stack.pop()
        if cur in seen:
            continue
        seen.add(cur)
        out.append(cur)
        for child in children_map.get(cur, []):
            if child not in seen:
                stack.append(child)
    return out


def _all_member_fulls(data: dict[str, Any]) -> list[str]:
    members = data.get("members", [])
    if not isinstance(members, list):
        return []
    out: list[str] = []
    for m in members:
        if not isinstance(m, dict):
            continue
        full = str(m.get("full", "")).strip()
        if full:
            out.append(full)
    uniq: list[str] = []
    seen: set[str] = set()
    for full in out:
        if full not in seen:
            seen.add(full)
            uniq.append(full)
    return uniq


def _select_targets_for_team_op(
    data: dict[str, Any],
    *,
    targets: list[str] | None,
    role: str | None,
    subtree: str | None,
) -> list[str]:
    if role:
        return _members_by_role(data, role)

    if subtree:
        root = _resolve_target_full(data, subtree)
        if not root:
            raise SystemExit(f"❌ subtree root not found in registry: {subtree}")
        return _subtree_fulls(data, root)

    raw_targets = targets or []
    if raw_targets:
        resolved: list[str] = []
        for t in raw_targets:
            full = _resolve_target_full(data, str(t))
            if not full:
                raise SystemExit(f"❌ target not found in registry: {t}")
            resolved.append(full)
        uniq: list[str] = []
        seen: set[str] = set()
        for full in resolved:
            if full not in seen:
                seen.add(full)
                uniq.append(full)
        return uniq

    return _all_member_fulls(data)


def cmd_stop(args: argparse.Namespace) -> int:
    twf = _resolve_twf()
    team_dir = _default_team_dir()
    registry = _registry_path(team_dir)
    data = _load_registry(registry)

    targets = _select_targets_for_team_op(
        data,
        targets=getattr(args, "targets", None),
        role=getattr(args, "role", None),
        subtree=getattr(args, "subtree", None),
    )
    if not targets:
        print("(no targets)")
        return 0

    # Prefer stopping leaves first if a subtree is selected.
    if getattr(args, "subtree", None):
        targets = list(reversed(targets))

    if getattr(args, "dry_run", False):
        print("\n".join(targets))
        return 0

    failures: list[str] = []
    for full in targets:
        sys.stdout.write(f"--- stop {full} ---\n")
        res = _run_twf(twf, ["stop", full])
        sys.stdout.write(res.stdout)
        sys.stderr.write(res.stderr)
        if res.returncode != 0:
            failures.append(full)

    if failures:
        _eprint(f"❌ stop failures: {len(failures)} targets")
        return 1
    return 0


def cmd_pause(args: argparse.Namespace) -> int:
    """
    Human-facing pause:
    - writes a shared marker to disable watcher actions (`share/.paused`)
    - stops workers (same selection rules as `stop`)
    """
    team_dir = _default_team_dir()
    reason = _read_optional_message(args, attr="reason")
    _set_paused(team_dir, reason=reason)
    _eprint(f"⏸️ paused: {_paused_marker_path(team_dir)}")

    # Stop the watcher session so future updates are picked up on unpause.
    if not bool(getattr(args, "dry_run", False)):
        _tmux_kill_session(_watch_idle_session_name(_expected_project_root(), team_dir=team_dir))
    return cmd_stop(
        argparse.Namespace(
            targets=getattr(args, "targets", None),
            role=getattr(args, "role", None),
            subtree=getattr(args, "subtree", None),
            dry_run=getattr(args, "dry_run", False),
        )
    )


def cmd_resume(args: argparse.Namespace) -> int:
    twf = _resolve_twf()
    team_dir = _default_team_dir()
    registry = _registry_path(team_dir)
    data = _load_registry(registry)

    _ensure_cap_watch_team(twf=twf, team_dir=team_dir, registry=registry)
    _ensure_watch_idle_team(twf=twf, team_dir=team_dir, registry=registry)

    targets = _select_targets_for_team_op(
        data,
        targets=getattr(args, "targets", None),
        role=getattr(args, "role", None),
        subtree=getattr(args, "subtree", None),
    )
    if not targets:
        print("(no targets)")
        return 0

    if getattr(args, "dry_run", False):
        print("\n".join(targets))
        return 0

    failures: list[str] = []
    for full in targets:
        sys.stdout.write(f"--- resume {full} ---\n")
        res = _run_twf(twf, ["resume", full, "--no-tree"])
        sys.stdout.write(res.stdout)
        sys.stderr.write(res.stderr)
        if res.returncode != 0:
            failures.append(full)

    if failures:
        _eprint(f"❌ resume failures: {len(failures)} targets")
        return 1
    return 0


def cmd_unpause(args: argparse.Namespace) -> int:
    """
    Human-facing unpause:
    - clears the pause marker (`share/.paused`)
    - resumes workers (same selection rules as `resume`)
    - restarts watcher processes so updates take effect
    """
    twf = _resolve_twf()
    team_dir = _default_team_dir()
    registry = _registry_path(team_dir)
    data = _load_registry(registry)

    _clear_paused(team_dir)
    _eprint(f"▶️ unpaused: {_paused_marker_path(team_dir)}")

    if bool(getattr(args, "dry_run", False)):
        # In dry-run, do not change watcher state.
        pass
    else:
        _restart_watch_idle_team(twf=twf, team_dir=team_dir, registry=registry)

    targets = _select_targets_for_team_op(
        data,
        targets=getattr(args, "targets", None),
        role=getattr(args, "role", None),
        subtree=getattr(args, "subtree", None),
    )
    if not targets:
        print("(no targets)")
        return 0

    if getattr(args, "dry_run", False):
        print("\n".join(targets))
        return 0

    failures: list[str] = []
    for full in targets:
        sys.stdout.write(f"--- resume {full} ---\n")
        res = _run_twf(twf, ["resume", full, "--no-tree"])
        sys.stdout.write(res.stdout)
        sys.stderr.write(res.stderr)
        if res.returncode != 0:
            failures.append(full)

    if failures:
        _eprint(f"❌ resume failures: {len(failures)} targets")
        return 1
    return 0


def cmd_broadcast(args: argparse.Namespace) -> int:
    team_dir = _default_team_dir()
    registry = _registry_path(team_dir)
    data = _load_registry(registry)
    policy = _policy()

    # Hard constraint: require explicit intent via `atwf notice` / `atwf action`.
    # Members running inside their worker tmux sessions must not use legacy broadcast.
    self_full = _tmux_self_full()
    if self_full and _resolve_member(data, self_full):
        raise SystemExit("❌ use `atwf notice` or `atwf action` (legacy `broadcast` is disabled for team members)")

    actor_full = _resolve_actor_full(data, as_target=getattr(args, "as_target", None))
    actor_m = _resolve_member(data, actor_full)
    if not actor_m:
        raise SystemExit(f"❌ actor not found in registry: {actor_full}")
    actor_role = _member_role(actor_m)
    actor_base = _member_base(actor_m) or actor_full
    if actor_role not in policy.broadcast_allowed_roles:
        raise SystemExit(
            "❌ broadcast not permitted by policy.\n"
            f"   actor: {actor_full} (role={actor_role or '?'})\n"
            f"   allowed_roles: {', '.join(sorted(policy.broadcast_allowed_roles)) or '(none)'}"
        )

    msg = args.message
    if msg is None:
        msg = _forward_stdin()
    if msg is None:
        raise SystemExit("❌ message missing (use --message or pipe via stdin)")
    msg = msg.strip()
    if not msg:
        raise SystemExit("❌ empty message")

    targets: list[str] = []
    if args.role:
        targets = _members_by_role(data, args.role)
    elif args.subtree:
        root = _resolve_target_full(data, args.subtree)
        if not root:
            raise SystemExit(f"❌ subtree root not found in registry: {args.subtree}")
        targets = _subtree_fulls(data, root)
        if not bool(getattr(args, "include_excluded", False)) and policy.broadcast_exclude_roles:
            filtered: list[str] = []
            for full in targets:
                m = _resolve_member(data, full)
                if _member_role(m) in policy.broadcast_exclude_roles:
                    continue
                filtered.append(full)
            targets = filtered
    else:
        raw_targets = getattr(args, "targets", []) or []
        if not isinstance(raw_targets, list) or not raw_targets:
            raise SystemExit("❌ targets are required (or use --role/--subtree)")
        for t in raw_targets:
            full = _resolve_target_full(data, str(t))
            if not full:
                raise SystemExit(f"❌ target not found in registry: {t}")
            targets.append(full)

    if not targets:
        raise SystemExit("❌ no targets matched")

    uniq: list[str] = []
    seen: set[str] = set()
    for t in targets:
        if t == actor_full:
            continue
        if t not in seen:
            seen.add(t)
            uniq.append(t)

    bc_id = _next_msg_id(team_dir)
    notice = f"[INBOX] id={bc_id}\nopen: atwf inbox-open {bc_id}\nack: atwf inbox-ack {bc_id}\n"

    lock = team_dir / ".lock"
    with _locked(lock):
        _ensure_share_layout(team_dir)
        max_unread = _inbox_max_unread_per_thread()
        for full in uniq:
            m = _resolve_member(data, full) or {}
            to_role = _member_role(m)
            to_base = _member_base(m) or full
            _write_inbox_message_unlocked(
                team_dir,
                msg_id=bc_id,
                kind="broadcast",
                from_full=actor_full,
                from_base=actor_base,
                from_role=actor_role or "?",
                to_full=full,
                to_base=to_base,
                to_role=to_role or "?",
                body=msg,
            )
            _inbox_enforce_unread_limit_unlocked(
                team_dir,
                to_base=to_base,
                from_base=actor_base,
                max_unread=max_unread,
            )

    # Default: inbox-only delivery. We still write inbox entries for all
    # recipients, but we do NOT inject into their Codex CLIs unless explicitly
    # requested.
    if not bool(getattr(args, "notify", False)):
        print(bc_id)
        return 0

    twf = _resolve_twf()
    failures2: list[str] = []
    max_workers2 = min(16, max(1, len(uniq)))
    with ThreadPoolExecutor(max_workers=max_workers2) as pool:
        futures = {
            pool.submit(
                _run_twf,
                twf,
                [
                    "send",
                    full,
                    _wrap_team_message(
                        team_dir,
                        kind="broadcast",
                        sender_full=actor_full,
                        sender_role=actor_role or None,
                        to_full=full,
                        body=notice,
                        msg_id=bc_id,
                    ),
                ],
            ): full
            for full in uniq
        }
        for fut in as_completed(futures):
            full = futures[fut]
            sys.stdout.write(f"--- {full} ---\n")
            try:
                res = fut.result()
            except Exception as exc:
                sys.stderr.write(f"❌ broadcast notify failed: {full}: {exc}\n")
                failures2.append(full)
                continue
            sys.stdout.write(res.stdout)
            sys.stderr.write(res.stderr)
            if res.returncode != 0:
                failures2.append(full)

    if failures2:
        _eprint(f"❌ broadcast notify failures: {len(failures2)} targets")
        return 1
    return 0


def cmd_resolve(args: argparse.Namespace) -> int:
    team_dir = _default_team_dir()
    registry = _registry_path(team_dir)
    data = _load_registry(registry)

    target = args.target.strip()
    if not target:
        raise SystemExit("❌ target is required")

    full = _resolve_target_full(data, target)
    if not full:
        raise SystemExit(f"❌ target not found in registry: {target}")
    print(full)
    return 0


def cmd_attach(args: argparse.Namespace) -> int:
    team_dir = _default_team_dir()
    registry = _registry_path(team_dir)
    data = _load_registry(registry)

    target = args.target.strip()
    if not target:
        raise SystemExit("❌ target is required")

    full = _resolve_target_full(data, target)
    if not full:
        raise SystemExit(f"❌ target not found in registry: {target}")

    probe = subprocess.run(["tmux", "has-session", "-t", full], check=False)
    if probe.returncode != 0:
        raise SystemExit(f"❌ tmux session not found: {full} (maybe stopped; try: twf resume {full})")

    if os.environ.get("TMUX"):
        return subprocess.run(["tmux", "switch-client", "-t", full], check=False).returncode
    return subprocess.run(["tmux", "attach-session", "-t", full], check=False).returncode


@dataclass(frozen=True)
class _RouteHit:
    score: int
    role: str
    base: str
    full: str
    scope: str


def cmd_route(args: argparse.Namespace) -> int:
    team_dir = _default_team_dir()
    registry = _registry_path(team_dir)
    data = _load_registry(registry)
    members = data.get("members", [])
    if not isinstance(members, list):
        members = []

    query = (args.query or "").strip().lower()
    if not query:
        raise SystemExit("❌ query is required")

    role_filter = _require_role(args.role) if args.role else None

    hits: list[_RouteHit] = []
    for m in members:
        if not isinstance(m, dict):
            continue
        role = str(m.get("role", "")).strip()
        if role_filter and role != role_filter:
            continue
        base = str(m.get("base", "")).strip()
        full = str(m.get("full", "")).strip()
        scope = str(m.get("scope", "")).strip()

        hay_base = base.lower()
        hay_scope = scope.lower()
        score = 0
        if query == hay_base:
            score += 100
        if query in hay_base:
            score += 30
        if query in hay_scope:
            score += 20
        if query == role:
            score += 10
        if score <= 0:
            continue
        hits.append(_RouteHit(score=score, role=role, base=base, full=full, scope=scope))

    hits.sort(key=lambda h: (h.score, h.role, h.base, h.full), reverse=True)
    if not hits:
        print("(no match)")
        return 1

    for h in hits[: (args.limit or 5)]:
        print(f"{h.full}\t{h.role}\t{h.base}\t{h.scope}")
    return 0


def _forward_stdin() -> str | None:
    if sys.stdin.isatty():
        return None
    return sys.stdin.read()


def cmd_ask(args: argparse.Namespace) -> int:
    team_dir = _default_team_dir()
    registry = _registry_path(team_dir)
    data = _load_registry(registry)
    policy = _policy()

    actor_full = _resolve_actor_full(data, as_target=getattr(args, "as_target", None))
    actor_m = _resolve_member(data, actor_full)
    if not actor_m:
        raise SystemExit(f"❌ actor not found in registry: {actor_full} (run: atwf register-self ...)")
    actor_role = _member_role(actor_m)
    actor_base = _member_base(actor_m) or actor_full

    target = args.name.strip()
    if not target:
        raise SystemExit("❌ name is required")
    full = _resolve_target_full(data, target)
    if not full:
        raise SystemExit(f"❌ name not found in registry: {target} (use `atwf list` or `atwf up/spawn`)")

    target_m = _resolve_member(data, full) or {}
    to_role = _member_role(target_m)
    to_base = _member_base(target_m) or full

    _require_comm_allowed(policy, data, actor_full=actor_full, target_full=full)

    msg = args.message
    if msg is None:
        msg = _forward_stdin()
    if msg is None:
        raise SystemExit("❌ message missing (provide as arg or via stdin)")

    msg_id = _next_msg_id(team_dir)
    _write_inbox_message(
        team_dir,
        msg_id=msg_id,
        kind="ask",
        from_full=actor_full,
        from_base=actor_base,
        from_role=actor_role,
        to_full=full,
        to_base=to_base,
        to_role=to_role,
        body=msg,
    )
    notice = f"[INBOX] id={msg_id}\nopen: atwf inbox-open {msg_id}\nack: atwf inbox-ack {msg_id}\n"
    wrapped = _wrap_team_message(
        team_dir,
        kind="ask",
        sender_full=actor_full,
        sender_role=actor_role or None,
        to_full=full,
        body=notice,
        msg_id=msg_id,
    )

    # Default: inbox-only delivery (no CLI injection). Recipients must poll
    # inbox while working. This avoids consuming their Codex context.
    notify = bool(getattr(args, "notify", False))
    wait = bool(getattr(args, "wait", False))
    if wait and not notify:
        raise SystemExit("❌ --wait requires --notify (CLI injection)")
    if not notify:
        print(msg_id)
        return 0

    twf = _resolve_twf()
    twf_subcmd = "ask" if wait else "send"
    res = _run_twf(twf, [twf_subcmd, full, wrapped])
    sys.stdout.write(res.stdout)
    sys.stderr.write(res.stderr)
    return res.returncode


def cmd_send(args: argparse.Namespace) -> int:
    team_dir = _default_team_dir()
    registry = _registry_path(team_dir)
    data = _load_registry(registry)
    policy = _policy()

    # Hard constraint: require explicit intent via `atwf notice` / `atwf action`.
    # Members running inside their worker tmux sessions must not use legacy send.
    self_full = _tmux_self_full()
    if self_full and _resolve_member(data, self_full):
        raise SystemExit("❌ use `atwf notice <target>` or `atwf action <target>` (legacy `send` is disabled for team members)")

    actor_full = _resolve_actor_full(data, as_target=getattr(args, "as_target", None))
    actor_m = _resolve_member(data, actor_full)
    if not actor_m:
        raise SystemExit(f"❌ actor not found in registry: {actor_full} (run: atwf register-self ...)")
    actor_role = _member_role(actor_m)
    actor_base = _member_base(actor_m) or actor_full

    target = args.name.strip()
    if not target:
        raise SystemExit("❌ name is required")
    full = _resolve_target_full(data, target)
    if not full:
        raise SystemExit(f"❌ name not found in registry: {target} (use `atwf list` or `atwf up/spawn`)")

    target_m = _resolve_member(data, full) or {}
    to_role = _member_role(target_m)
    to_base = _member_base(target_m) or full

    _require_comm_allowed(policy, data, actor_full=actor_full, target_full=full)

    msg = args.message
    if msg is None:
        msg = _forward_stdin()
    if msg is None:
        raise SystemExit("❌ message missing (provide as arg or via stdin)")
    msg = msg.strip()
    if not msg:
        raise SystemExit("❌ empty message")

    msg_id = _next_msg_id(team_dir)
    _write_inbox_message(
        team_dir,
        msg_id=msg_id,
        kind="send",
        from_full=actor_full,
        from_base=actor_base,
        from_role=actor_role,
        to_full=full,
        to_base=to_base,
        to_role=to_role,
        body=msg,
    )
    notice = f"[INBOX] id={msg_id}\nopen: atwf inbox-open {msg_id}\nack: atwf inbox-ack {msg_id}\n"
    wrapped = _wrap_team_message(
        team_dir,
        kind="send",
        sender_full=actor_full,
        sender_role=actor_role or None,
        to_full=full,
        body=notice,
        msg_id=msg_id,
    )

    # Default: inbox-only delivery (no CLI injection).
    if not bool(getattr(args, "notify", False)):
        print(msg_id)
        return 0

    twf = _resolve_twf()
    res = _run_twf(twf, ["send", full, wrapped])
    sys.stdout.write(res.stdout)
    sys.stderr.write(res.stderr)
    return res.returncode


def _resolve_intent_targets(
    *,
    data: dict[str, Any],
    policy: TeamPolicy,
    actor_full: str,
    targets: list[str] | None,
    role: str | None,
    subtree: str | None,
    include_excluded: bool,
) -> tuple[list[str], bool]:
    """
    Resolve targets and whether this is a broadcast-style delivery.

    - For --role/--subtree: broadcast-style (policy.broadcast applies)
    - For explicit targets:
      - 1 target => direct (comm policy applies)
      - 2+ targets => broadcast-style (policy.broadcast applies)
    """
    resolved: list[str] = []

    if role:
        resolved = _members_by_role(data, role)
        is_broadcast = True
    elif subtree:
        root = _resolve_target_full(data, subtree)
        if not root:
            raise SystemExit(f"❌ subtree root not found in registry: {subtree}")
        resolved = _subtree_fulls(data, root)
        is_broadcast = True
        if not include_excluded and policy.broadcast_exclude_roles:
            filtered: list[str] = []
            for full in resolved:
                m = _resolve_member(data, full)
                if _member_role(m) in policy.broadcast_exclude_roles:
                    continue
                filtered.append(full)
            resolved = filtered
    else:
        raw = targets or []
        if not raw:
            raise SystemExit("❌ targets are required (or use --role/--subtree)")
        for t in raw:
            full = _resolve_target_full(data, str(t))
            if not full:
                raise SystemExit(f"❌ target not found in registry: {t}")
            resolved.append(full)
        is_broadcast = len({t for t in resolved if t}) > 1

    # De-dupe + drop self for broadcast-style deliveries.
    uniq: list[str] = []
    seen: set[str] = set()
    for full in resolved:
        if not full:
            continue
        if is_broadcast and full == actor_full:
            continue
        if full not in seen:
            seen.add(full)
            uniq.append(full)
    return uniq, is_broadcast


def _cmd_intent_message(args: argparse.Namespace, *, kind: str) -> int:
    """
    Deliver an inbox-backed message with an explicit intent kind:
    - kind=notice: FYI; recipients must not reply/ACK upward (use receipts to confirm read)
    - kind=action: instruction; no immediate ACK required; report-up only when done
    """
    team_dir = _default_team_dir()
    registry = _registry_path(team_dir)
    data = _load_registry(registry)
    policy = _policy()

    actor_full = _resolve_actor_full(data, as_target=getattr(args, "as_target", None))
    actor_m = _resolve_member(data, actor_full)
    if not actor_m:
        raise SystemExit(f"❌ actor not found in registry: {actor_full} (run: atwf register-self ...)")
    actor_role = _member_role(actor_m)
    actor_base = _member_base(actor_m) or actor_full

    msg = getattr(args, "message", None)
    if msg is None:
        msg = _forward_stdin()
    if msg is None:
        raise SystemExit("❌ message missing (use --message or pipe via stdin)")
    msg = str(msg).strip()
    if not msg:
        raise SystemExit("❌ empty message")

    targets, is_broadcast = _resolve_intent_targets(
        data=data,
        policy=policy,
        actor_full=actor_full,
        targets=getattr(args, "targets", None),
        role=getattr(args, "role", None),
        subtree=getattr(args, "subtree", None),
        include_excluded=bool(getattr(args, "include_excluded", False)),
    )
    if not targets:
        raise SystemExit("❌ no targets matched")

    if is_broadcast:
        if actor_role not in policy.broadcast_allowed_roles:
            raise SystemExit(
                "❌ broadcast not permitted by policy.\n"
                f"   actor: {actor_full} (role={actor_role or '?'})\n"
                f"   allowed_roles: {', '.join(sorted(policy.broadcast_allowed_roles)) or '(none)'}"
            )
    else:
        # Direct: enforce comm governance.
        _require_comm_allowed(policy, data, actor_full=actor_full, target_full=targets[0])

    msg_id = _next_msg_id(team_dir)
    inbox_notice = f"[INBOX] id={msg_id}\nopen: atwf inbox-open {msg_id}\nack: atwf inbox-ack {msg_id}\n"

    lock = team_dir / ".lock"
    with _locked(lock):
        _ensure_share_layout(team_dir)
        max_unread = _inbox_max_unread_per_thread()
        for full in targets:
            m = _resolve_member(data, full) or {}
            to_role = _member_role(m) or "?"
            to_base = _member_base(m) or full
            _write_inbox_message_unlocked(
                team_dir,
                msg_id=msg_id,
                kind=kind,
                from_full=actor_full,
                from_base=actor_base,
                from_role=actor_role or "?",
                to_full=full,
                to_base=to_base,
                to_role=to_role,
                body=msg,
            )
            _inbox_enforce_unread_limit_unlocked(
                team_dir,
                to_base=to_base,
                from_base=actor_base,
                max_unread=max_unread,
            )

    # Default: inbox-only delivery. CLI injection is discouraged.
    if not bool(getattr(args, "notify", False)):
        print(msg_id)
        return 0

    twf = _resolve_twf()
    if len(targets) == 1:
        wrapped = _wrap_team_message(
            team_dir,
            kind=kind,
            sender_full=actor_full,
            sender_role=actor_role or None,
            to_full=targets[0],
            body=inbox_notice,
            msg_id=msg_id,
        )
        res = _run_twf(twf, ["send", targets[0], wrapped])
        sys.stdout.write(res.stdout)
        sys.stderr.write(res.stderr)
        return res.returncode

    failures: list[str] = []
    max_workers = min(16, max(1, len(targets)))
    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        futures = {
            pool.submit(
                _run_twf,
                twf,
                [
                    "send",
                    full,
                    _wrap_team_message(
                        team_dir,
                        kind=kind,
                        sender_full=actor_full,
                        sender_role=actor_role or None,
                        to_full=full,
                        body=inbox_notice,
                        msg_id=msg_id,
                    ),
                ],
            ): full
            for full in targets
        }
        for fut in as_completed(futures):
            full = futures[fut]
            try:
                r = fut.result()
            except Exception:
                failures.append(full)
                continue
            if r.returncode != 0:
                failures.append(full)

    if failures:
        raise SystemExit(f"❌ notify failures: {len(failures)} targets")
    print(msg_id)
    return 0


def cmd_notice(args: argparse.Namespace) -> int:
    return _cmd_intent_message(args, kind="notice")


def cmd_action(args: argparse.Namespace) -> int:
    return _cmd_intent_message(args, kind="action")


def cmd_receipts(args: argparse.Namespace) -> int:
    """
    Query read receipts for a message id across recipients.

    Statuses:
    - unread: present under inbox/<to>/unread
    - overflow: present under inbox/<to>/overflow
    - read: present under inbox/<to>/read
    - missing: not present under inbox/<to> at all (not a recipient, or pruned)
    """
    team_dir = _default_team_dir()
    registry = _registry_path(team_dir)
    data = _load_registry(registry)

    msg_id = str(getattr(args, "msg_id", "") or "").strip()
    if not msg_id:
        raise SystemExit("❌ msg_id is required")

    targets = _select_targets_for_team_op(
        data,
        targets=getattr(args, "targets", None),
        role=getattr(args, "role", None),
        subtree=getattr(args, "subtree", None),
    )
    if not targets:
        print("(no targets)")
        return 0

    rows: list[tuple[str, str, str, str]] = []
    for full in targets:
        m = _resolve_member(data, full) or {}
        base = _member_base(m) or full
        role = _member_role(m) or "?"
        hit = _find_inbox_message_file(team_dir, to_base=base, msg_id=msg_id)
        status = "missing"
        if hit:
            state, _from_base, _path = hit
            status = state if state in {_INBOX_UNREAD_DIR, _INBOX_OVERFLOW_DIR, _INBOX_READ_DIR} else "missing"
        rows.append((status, role, base, full))

    order = {_INBOX_UNREAD_DIR: 0, _INBOX_OVERFLOW_DIR: 1, _INBOX_READ_DIR: 2, "missing": 3}
    rows.sort(key=lambda r: (order.get(r[0], 99), r[1], r[2], r[3]))
    for status, role, base, full in rows:
        print("\t".join([status, role, base, full]).rstrip())
    return 0


def cmd_gather(args: argparse.Namespace) -> int:
    """
    Create a reply-needed request to multiple targets.

    The request body is delivered to each target inbox; targets must use `atwf respond`
    (or `atwf respond --blocked`) to record their reply.
    The initiator only receives a single consolidated result when all replies arrive
    (or when the request times out).
    """
    team_dir = _default_team_dir()
    registry = _registry_path(team_dir)
    data = _load_registry(registry)
    policy = _policy()

    actor_full = _resolve_actor_full(data, as_target=getattr(args, "as_target", None))
    actor_m = _resolve_member(data, actor_full)
    if not actor_m:
        raise SystemExit(f"❌ actor not found in registry: {actor_full} (run: atwf register-self ...)")
    actor_role = _member_role(actor_m)
    actor_base = _member_base(actor_m) or actor_full

    targets_raw = [str(t).strip() for t in (getattr(args, "targets", None) or []) if str(t).strip()]
    if not targets_raw:
        raise SystemExit("❌ gather requires at least one target")

    msg = getattr(args, "message", None)
    if msg is None:
        msg = _forward_stdin()
    if msg is None:
        raise SystemExit("❌ message missing (provide as arg or via stdin)")
    msg = str(msg).rstrip()
    if not msg.strip():
        raise SystemExit("❌ empty message")

    topic = str(getattr(args, "topic", "") or "").strip()
    if not topic:
        # Use the first non-empty line as a default topic.
        topic = _inbox_summary(msg) or "reply-needed"

    deadline_s = _request_deadline_s()
    raw_deadline = str(getattr(args, "deadline", "") or "").strip()
    if raw_deadline:
        deadline_s = _parse_duration_seconds(raw_deadline, default_s=deadline_s)
    if deadline_s < 60:
        deadline_s = 60.0
    if deadline_s > 86400:
        deadline_s = 86400.0

    # Reserve IDs up front (avoid re-entrant locks).
    req_seq = _next_msg_id(team_dir)
    request_id = f"req-{req_seq}"

    resolved_targets: list[tuple[str, str, str]] = []
    seen_bases: set[str] = set()
    for raw in targets_raw:
        full = _resolve_target_full(data, raw)
        if not full:
            raise SystemExit(f"❌ target not found in registry: {raw} (use `atwf list`)")
        _require_comm_allowed(policy, data, actor_full=actor_full, target_full=full)
        m = _resolve_member(data, full) or {}
        base = _member_base(m) or full
        role = _member_role(m)
        if base == actor_base:
            continue
        if base in seen_bases:
            continue
        seen_bases.add(base)
        resolved_targets.append((full, base, role))

    if not resolved_targets:
        raise SystemExit("❌ gather has no valid targets after resolution/dedupe")

    notify_ids = [_next_msg_id(team_dir) for _full, _base, _role in resolved_targets]

    now_dt = datetime.now()
    created_at = now_dt.isoformat(timespec="seconds")
    deadline_at = (now_dt + timedelta(seconds=float(deadline_s))).isoformat(timespec="seconds")

    meta: dict[str, Any] = {
        "version": 1,
        "id": request_id,
        "created_at": created_at,
        "updated_at": created_at,
        "status": _REQUEST_STATUS_OPEN,
        "topic": topic,
        "message": msg,
        "deadline_s": float(deadline_s),
        "deadline_at": deadline_at,
        "from": {"full": actor_full, "base": actor_base, "role": actor_role},
        "targets": {},
        "finalized_at": "",
        "final_msg_id": "",
    }

    targets_meta: dict[str, Any] = {}
    for (full, base, role), notify_id in zip(resolved_targets, notify_ids, strict=True):
        targets_meta[base] = {
            "full": full,
            "base": base,
            "role": role,
            "status": _REQUEST_TARGET_STATUS_PENDING,
            "requested_at": created_at,
            "notify_msg_id": notify_id,
            "blocked_until": "",
            "blocked_reason": "",
            "waiting_on": "",
            "responded_at": "",
            "response_file": "",
        }
    meta["targets"] = targets_meta

    lock = team_dir / ".lock"
    with _locked(lock):
        _ensure_share_layout(team_dir)
        req_dir = _request_dir(team_dir, request_id=request_id)
        req_dir.mkdir(parents=True, exist_ok=True)
        _request_responses_dir(team_dir, request_id=request_id).mkdir(parents=True, exist_ok=True)

        _write_json_atomic(_request_meta_path(team_dir, request_id=request_id), meta)

        for (full, base, role), notify_id in zip(resolved_targets, notify_ids, strict=True):
            body = (
                f"[REPLY-NEEDED] request_id={request_id}\n"
                f"- topic: {topic}\n"
                f"- from: {actor_base} (role={actor_role or '?'})\n"
                f"- created_at: {created_at}\n"
                f"- deadline_at: {deadline_at}\n"
                "\n"
                "Respond (required):\n"
                f"- bash .codex/skills/ai-team-workflow/scripts/atwf respond {request_id} \"<your reply>\"\n"
                "\n"
                "If blocked, snooze reminders (default 15m):\n"
                f"- bash .codex/skills/ai-team-workflow/scripts/atwf respond {request_id} --blocked --snooze 15m --waiting-on <base> \"why blocked\"\n"
                "\n"
                "View pending reply-needed:\n"
                "- bash .codex/skills/ai-team-workflow/scripts/atwf reply-needed\n"
                "\n"
                "Message:\n"
                f"{msg.rstrip()}\n"
            )
            _write_inbox_message_unlocked(
                team_dir,
                msg_id=notify_id,
                kind="reply-needed",
                from_full=actor_full,
                from_base=actor_base,
                from_role=actor_role,
                to_full=full,
                to_base=base,
                to_role=role,
                body=body,
            )
            _inbox_enforce_unread_limit_unlocked(
                team_dir,
                to_base=base,
                from_base=actor_base,
                max_unread=_inbox_max_unread_per_thread(),
            )

    print(request_id)
    return 0


def cmd_respond(args: argparse.Namespace) -> int:
    """
    Record a reply-needed response for the current worker (or --as).

    - Normal reply: marks replied and writes a response file under requests/<id>/responses/.
    - --blocked: acknowledges the request but snoozes system reminders for a duration.
    """
    team_dir = _default_team_dir()
    registry = _registry_path(team_dir)
    data = _load_registry(registry)

    actor_full = _resolve_actor_full(data, as_target=getattr(args, "as_target", None))
    actor_m = _resolve_member(data, actor_full)
    if not actor_m:
        raise SystemExit(f"❌ actor not found in registry: {actor_full} (run: atwf register-self ...)")
    actor_role = _member_role(actor_m)
    actor_base = _member_base(actor_m) or actor_full

    request_id = _resolve_request_id(team_dir, str(getattr(args, "request_id", "") or ""))
    meta_path = _request_meta_path(team_dir, request_id=request_id)
    if not meta_path.is_file():
        raise SystemExit(f"❌ request not found: {request_id}")

    msg = getattr(args, "message", None)
    if msg is None:
        msg = _forward_stdin()
    msg = "" if msg is None else str(msg).rstrip()

    blocked = bool(getattr(args, "blocked", False))
    waiting_on = str(getattr(args, "waiting_on", "") or "").strip()
    raw_snooze = str(getattr(args, "snooze", "") or "").strip()
    snooze_s = _request_block_snooze_default_s()
    if raw_snooze:
        snooze_s = _parse_duration_seconds(raw_snooze, default_s=snooze_s)
    if snooze_s < 30:
        snooze_s = 30.0
    if snooze_s > 86400:
        snooze_s = 86400.0

    now_dt = datetime.now()
    now_iso = now_dt.isoformat(timespec="seconds")

    # Reserve a delivery msg id in case we need to finalize this request (avoid re-entrant locks).
    delivery_msg_id = _next_msg_id(team_dir)

    notify_msg_id = ""
    did_finalize = False
    blocked_until_out = ""

    lock = team_dir / ".lock"
    with _locked(lock):
        meta = _load_request_meta(team_dir, request_id=request_id)
        if str(meta.get("status", "")).strip() in {_REQUEST_STATUS_DONE, _REQUEST_STATUS_TIMED_OUT}:
            raise SystemExit(f"❌ request already finalized: {request_id} ({meta.get('status')})")

        targets = meta.get("targets")
        if not isinstance(targets, dict) or not targets:
            raise SystemExit(f"❌ request has no targets: {request_id}")

        key: str | None = None
        if actor_base in targets:
            key = actor_base
        else:
            for k, t in targets.items():
                if isinstance(t, dict) and str(t.get("full", "")).strip() == actor_full:
                    key = str(k)
                    break
        if not key or key not in targets or not isinstance(targets.get(key), dict):
            raise SystemExit(f"❌ you are not a target of request {request_id} (base={actor_base})")

        t = targets[key]
        notify_msg_id = str(t.get("notify_msg_id", "") or "").strip()

        if blocked:
            reason = msg.strip() or "(blocked)"
            blocked_until = (now_dt + timedelta(seconds=float(snooze_s))).isoformat(timespec="seconds")
            blocked_until_out = blocked_until
            t["status"] = _REQUEST_TARGET_STATUS_BLOCKED
            t["blocked_until"] = blocked_until
            t["blocked_reason"] = reason
            t["waiting_on"] = waiting_on
            t["responded_at"] = ""
            t["response_file"] = ""
        else:
            if not msg.strip():
                raise SystemExit("❌ reply body missing (provide as arg or via stdin)")
            resp_dir = _request_responses_dir(team_dir, request_id=request_id)
            resp_dir.mkdir(parents=True, exist_ok=True)
            resp_path = _request_response_path(team_dir, request_id=request_id, target_base=actor_base)
            payload = (
                f"# ATWF Reply-Needed Response\n\n"
                f"- request_id: `{request_id}`\n"
                f"- from: `{actor_full}` (base `{actor_base}` role `{actor_role or '?'}`)\n"
                f"- created_at: {now_iso}\n\n"
                "---\n\n"
                f"{msg.rstrip()}\n"
            )
            _write_text_atomic(resp_path, payload)

            rel = ""
            try:
                rel = str(resp_path.relative_to(team_dir))
            except Exception:
                rel = str(resp_path)

            t["status"] = _REQUEST_TARGET_STATUS_REPLIED
            t["responded_at"] = now_iso
            t["response_file"] = rel
            t["blocked_until"] = ""
            t["blocked_reason"] = ""
            t["waiting_on"] = ""

        meta["targets"] = targets
        meta["updated_at"] = now_iso

        # Finalize (single consolidated delivery) when complete or timed out.
        if not str(meta.get("final_msg_id", "") or "").strip():
            all_replied = _request_all_replied(meta)
            deadline_dt = _parse_iso_dt(str(meta.get("deadline_at", "") or ""))
            timed_out = (deadline_dt is not None and now_dt >= deadline_dt and not all_replied)
            if all_replied or timed_out:
                final_status = _REQUEST_STATUS_DONE if all_replied else _REQUEST_STATUS_TIMED_OUT

                from_info = meta.get("from") if isinstance(meta.get("from"), dict) else {}
                to_base = str(from_info.get("base", "") or "").strip() or str(from_info.get("full", "") or "").strip()
                to_full = str(from_info.get("full", "") or "").strip()
                to_role = str(from_info.get("role", "") or "").strip() or "?"
                # Prefer current registry for to_full/to_role if base exists.
                if to_base:
                    m = _resolve_member(data, to_base) or {}
                    to_full = str(m.get("full", "")).strip() or to_full or to_base
                    to_role = _member_role(m) or to_role

                if to_base:
                    body = _render_request_result(team_dir, meta, final_status=final_status)
                    _write_inbox_message_unlocked(
                        team_dir,
                        msg_id=delivery_msg_id,
                        kind="reply-needed-result",
                        from_full="atwf-reply",
                        from_base="atwf-reply",
                        from_role="system",
                        to_full=to_full or to_base,
                        to_base=to_base,
                        to_role=to_role,
                        body=body,
                    )
                    _inbox_enforce_unread_limit_unlocked(
                        team_dir,
                        to_base=to_base,
                        from_base="atwf-reply",
                        max_unread=_inbox_max_unread_per_thread(),
                    )
                    meta["status"] = final_status
                    meta["finalized_at"] = now_iso
                    meta["final_msg_id"] = delivery_msg_id
                    did_finalize = True

        _write_json_atomic(meta_path, meta)

    # Ack the original reply-needed notice (do this outside lock; it has its own lock).
    if notify_msg_id:
        _mark_inbox_read(team_dir, to_base=actor_base, msg_id=notify_msg_id)

    if blocked:
        print(f"{request_id}\tblocked\tuntil={blocked_until_out}".rstrip())
        return 0

    if did_finalize:
        print(f"{request_id}\treplied\tfinalized={delivery_msg_id}")
        return 0
    print(f"{request_id}\treplied")
    return 0


def cmd_reply_needed(args: argparse.Namespace) -> int:
    """
    List pending reply-needed requests for a target (self by default).
    """
    team_dir = _default_team_dir()
    registry = _registry_path(team_dir)
    data = _load_registry(registry)

    target = str(getattr(args, "target", "") or "").strip()
    if target:
        full = _resolve_target_full(data, target)
        if not full:
            raise SystemExit(f"❌ target not found in registry: {target}")
        m = _resolve_member(data, full) or {}
        to_base = _member_base(m) or full
    else:
        self_full = _tmux_self_full()
        if not self_full:
            raise SystemExit("❌ reply-needed must run inside tmux (or use: reply-needed --target <full|base|role>)")
        m = _resolve_member(data, self_full)
        if not m:
            raise SystemExit(f"❌ current worker not found in registry: {self_full}")
        to_base = _member_base(m) or self_full

    now_dt = datetime.now()
    rows: list[tuple[str, str, str, str, str]] = []

    for req_id in _list_request_ids(team_dir):
        meta_path = _request_meta_path(team_dir, request_id=req_id)
        if not meta_path.is_file():
            continue
        meta = _read_json(meta_path)
        if not isinstance(meta, dict) or not meta:
            continue
        if str(meta.get("status", "")).strip() != _REQUEST_STATUS_OPEN:
            continue
        targets = meta.get("targets")
        if not isinstance(targets, dict):
            continue
        t = targets.get(to_base)
        if not isinstance(t, dict):
            continue
        st = str(t.get("status", "") or "").strip() or _REQUEST_TARGET_STATUS_PENDING
        if st == _REQUEST_TARGET_STATUS_REPLIED:
            continue
        blocked_until = str(t.get("blocked_until", "") or "").strip()
        blocked_dt = _parse_iso_dt(blocked_until)
        if blocked_dt is not None and now_dt < blocked_dt:
            st = f"{st}(snoozed)"
        topic = str(meta.get("topic", "") or "").strip()
        from_info = meta.get("from") if isinstance(meta.get("from"), dict) else {}
        from_base = str(from_info.get("base", "") or "").strip()
        deadline_at = str(meta.get("deadline_at", "") or "").strip()
        rows.append((req_id, st, topic, from_base, deadline_at))

    if not rows:
        print("(none)")
        return 0

    rows.sort(key=lambda r: r[0])
    for req_id, st, topic, from_base, deadline_at in rows:
        print("\t".join([req_id, st, topic, from_base, deadline_at]).rstrip())
    return 0


def cmd_request(args: argparse.Namespace) -> int:
    team_dir = _default_team_dir()
    request_id = _resolve_request_id(team_dir, str(getattr(args, "request_id", "") or ""))
    meta = _load_request_meta(team_dir, request_id=request_id)
    print(_render_request_result(team_dir, meta, final_status=str(meta.get("status", "") or _REQUEST_STATUS_OPEN)))
    return 0


def cmd_pend(args: argparse.Namespace) -> int:
    twf = _resolve_twf()
    team_dir = _default_team_dir()
    registry = _registry_path(team_dir)
    data = _load_registry(registry)

    target = args.name.strip()
    if not target:
        raise SystemExit("❌ name is required")
    full = _resolve_target_full(data, target)
    if not full:
        raise SystemExit(f"❌ name not found in registry: {target} (use `atwf list`)")
    extra = [str(args.n)] if args.n is not None else []
    res = _run_twf(twf, ["pend", full, *extra])
    sys.stdout.write(res.stdout)
    sys.stderr.write(res.stderr)
    return res.returncode


def cmd_ping(args: argparse.Namespace) -> int:
    twf = _resolve_twf()
    team_dir = _default_team_dir()
    registry = _registry_path(team_dir)
    data = _load_registry(registry)

    target = args.name.strip()
    if not target:
        raise SystemExit("❌ name is required")
    full = _resolve_target_full(data, target)
    if not full:
        raise SystemExit(f"❌ name not found in registry: {target} (use `atwf list`)")
    res = _run_twf(twf, ["ping", full])
    sys.stdout.write(res.stdout)
    sys.stderr.write(res.stderr)
    return res.returncode


def cmd_state(args: argparse.Namespace) -> int:
    team_dir = _default_team_dir()
    registry = _registry_path(team_dir)
    data = _load_registry(registry)

    target = str(getattr(args, "target", "") or "").strip()
    members = data.get("members")
    if not isinstance(members, list):
        members = []

    def print_row(*cols: str) -> None:
        sys.stdout.write("\t".join(c or "" for c in cols) + "\n")

    if target:
        full = _resolve_target_full(data, target)
        if not full:
            raise SystemExit(f"❌ target not found in registry: {target}")
        m = _resolve_member(data, full) or {}
        base = _member_base(m) or full
        role = _member_role(m)
        path = _agent_state_path(team_dir, full=full)
        st = _read_json(path) if path.is_file() else {}
        status = _normalize_agent_status(str(st.get("status", ""))) if st else _STATE_STATUS_WORKING
        if status not in _STATE_STATUSES:
            status = _STATE_STATUS_WORKING
        updated_at = str(st.get("updated_at", "") or "")
        due_at = str(st.get("wakeup_due_at", "") or "")
        print_row(full, role, base, status, updated_at, due_at)
        return 0

    # Table for all members (stable ordering: role then updated_at then full)
    rows: list[tuple[str, str, str, str, str, str]] = []
    for m in members:
        if not isinstance(m, dict):
            continue
        full = str(m.get("full", "")).strip()
        if not full:
            continue
        base = _member_base(m) or full
        role = _member_role(m)
        path = _agent_state_path(team_dir, full=full)
        st = _read_json(path) if path.is_file() else {}
        status = _normalize_agent_status(str(st.get("status", ""))) if st else _STATE_STATUS_WORKING
        if status not in _STATE_STATUSES:
            status = _STATE_STATUS_WORKING
        updated_at = str(st.get("updated_at", "") or "")
        due_at = str(st.get("wakeup_due_at", "") or "")
        rows.append((role, updated_at, full, base, status, due_at))

    rows.sort(key=lambda r: (r[0], r[1], r[2]))
    print_row("full", "role", "base", "status", "updated_at", "wakeup_due_at")
    for role, updated_at, full, base, status, due_at in rows:
        print_row(full, role, base, status, updated_at, due_at)
    return 0


def cmd_state_self(args: argparse.Namespace) -> int:
    team_dir = _default_team_dir()
    registry = _registry_path(team_dir)
    data = _load_registry(registry)

    self_full = _tmux_self_full()
    if not self_full:
        raise SystemExit("❌ state-self must run inside tmux")
    m = _resolve_member(data, self_full)
    if not m:
        raise SystemExit(f"❌ current worker not found in registry: {self_full}")
    base = _member_base(m) or self_full
    role = _member_role(m)

    st = _update_agent_state(team_dir, full=self_full, base=base, role=role, updater=lambda _d: None)
    status = str(st.get("status", ""))
    updated_at = str(st.get("updated_at", ""))
    due_at = str(st.get("wakeup_due_at", ""))
    print("\t".join([self_full, role, base, status, updated_at, due_at]).rstrip())
    return 0


def cmd_state_set_self(args: argparse.Namespace) -> int:
    team_dir = _default_team_dir()
    registry = _registry_path(team_dir)
    data = _load_registry(registry)

    status_raw = str(args.status or "").strip()
    if not status_raw:
        raise SystemExit("❌ status is required")
    desired = _normalize_agent_status(status_raw)
    if desired not in _STATE_STATUSES:
        raise SystemExit(f"❌ invalid status: {status_raw} (allowed: working|draining|idle)")

    self_full = _tmux_self_full()
    if not self_full:
        raise SystemExit("❌ state-set-self must run inside tmux")
    m = _resolve_member(data, self_full)
    if not m:
        raise SystemExit(f"❌ current worker not found in registry: {self_full}")
    base = _member_base(m) or self_full
    role = _member_role(m)

    def set_status(state: dict[str, Any]) -> None:
        cur = _normalize_agent_status(str(state.get("status", ""))) or _STATE_STATUS_WORKING
        if cur not in _STATE_STATUSES:
            cur = _STATE_STATUS_WORKING
        now = _now()

        if desired == _STATE_STATUS_IDLE:
            if cur != _STATE_STATUS_DRAINING:
                raise SystemExit("❌ must set state to 'draining' before 'idle'")
            unread, overflow, ids = _inbox_unread_stats(team_dir, to_base=base)
            if unread or overflow:
                preview = ", ".join(ids[:10]) if ids else ""
                hint = f" ids: {preview}" if preview else ""
                raise SystemExit(
                    f"❌ inbox not empty (unread={unread} overflow={overflow}){hint} "
                    f"(run: bash .codex/skills/ai-team-workflow/scripts/atwf inbox)"
                )
            state["idle_since"] = now
            state["idle_inbox_empty_at"] = now
        elif desired == _STATE_STATUS_DRAINING:
            state["idle_since"] = ""
            state["idle_inbox_empty_at"] = ""
        elif desired == _STATE_STATUS_WORKING:
            state["idle_since"] = ""
            state["idle_inbox_empty_at"] = ""

        # Clear any pending wake scheduling when state changes.
        state["wakeup_scheduled_at"] = ""
        state["wakeup_due_at"] = ""
        state["wakeup_reason"] = ""
        if desired != _STATE_STATUS_WORKING:
            # keep historical wake_sent_at for debugging
            pass
        state["status"] = desired

    st = _update_agent_state(team_dir, full=self_full, base=base, role=role, updater=set_status)
    print(str(st.get("status", "")))
    return 0


def cmd_state_set(args: argparse.Namespace) -> int:
    team_dir = _default_team_dir()
    registry = _registry_path(team_dir)
    data = _load_registry(registry)

    target = str(getattr(args, "target", "") or "").strip()
    if not target:
        raise SystemExit("❌ target is required")
    full = _resolve_target_full(data, target)
    if not full:
        raise SystemExit(f"❌ target not found in registry: {target}")
    m = _resolve_member(data, full) or {}
    base = _member_base(m) or full
    role = _member_role(m)

    status_raw = str(args.status or "").strip()
    if not status_raw:
        raise SystemExit("❌ status is required")
    desired = _normalize_agent_status(status_raw)
    if desired not in _STATE_STATUSES:
        raise SystemExit(f"❌ invalid status: {status_raw} (allowed: working|draining|idle)")

    force = bool(getattr(args, "force", False))
    if desired in {_STATE_STATUS_IDLE, _STATE_STATUS_DRAINING} and not force:
        raise SystemExit("❌ only the worker can set draining/idle (use --force for operator override)")

    st = _update_agent_state(team_dir, full=full, base=base, role=role, updater=lambda s: s.__setitem__("status", desired))
    print(str(st.get("status", "")))
    return 0


def cmd_drive(args: argparse.Namespace) -> int:
    """
    Drive loop mode (human-controlled):
    - running: watcher treats all-idle + inbox-empty as an abnormal stall and wakes the driver
    - standby: allow the whole team to be idle with empty inbox (no drive nudge)
    """
    team_dir = _default_team_dir()

    mode_raw = str(getattr(args, "mode", "") or "").strip()
    if not mode_raw:
        mode = _drive_mode_config_hot()
        lock = _state_lock_path(team_dir)
        with _locked(lock):
            _ensure_share_layout(team_dir)
            data = _load_drive_state_unlocked(team_dir, mode_default=mode)
        print("\t".join([mode, str(data.get("last_triggered_at", "")), str(data.get("last_msg_id", ""))]).rstrip())
        return 0

    mode = _normalize_drive_mode(mode_raw)
    if mode not in _DRIVE_MODES:
        raise SystemExit(f"❌ invalid drive mode: {mode_raw!r} (allowed: running|standby)")

    # Config is authoritative; prevent team members from switching mode in-worker.
    registry = _registry_path(team_dir)
    data = _load_registry(registry)
    self_full = _tmux_self_full()
    if self_full and _resolve_member(data, self_full):
        raise SystemExit(
            "❌ drive mode is user/operator-only.\n"
            f"   workers must NOT edit: {_config_file()}\n"
            "   workers must NOT change drive mode."
        )

    print(_set_drive_mode_config(mode))
    return 0


def cmd_watch_idle(args: argparse.Namespace) -> int:
    """
    Operator-side watcher:
    - polls inbox + derives working/idle from tmux pane activity (output hash)
    - if a member is `idle` and has pending inbox, schedule a wakeup
    - when due, inject a short wake message and record wakeup_sent_at (grace keeps it active)
    """
    twf = _resolve_twf()
    team_dir = _default_team_dir()
    registry = _registry_path(team_dir)

    interval_s = float(getattr(args, "interval", None) or _state_watch_interval_s())
    delay_s = float(getattr(args, "delay", None) or _state_idle_wake_delay_s())
    activity_window_s = _state_activity_window_s()
    grace_s = _state_active_grace_period_s()
    capture_lines = _state_activity_capture_lines()
    auto_enter_enabled = _state_auto_enter_enabled()
    auto_enter_cooldown_s = _state_auto_enter_cooldown_s()
    auto_enter_tail_lines = _state_auto_enter_tail_window_lines()
    auto_enter_patterns = _state_auto_enter_patterns() if auto_enter_enabled else []
    message = str(getattr(args, "message", "") or "").strip() or _state_wake_message()
    reply_message = _state_reply_wake_message()
    stale_s = float(getattr(args, "working_stale", None) or _state_working_stale_threshold_s())
    cooldown_s = float(getattr(args, "alert_cooldown", None) or _state_working_alert_cooldown_s())
    once = bool(getattr(args, "once", False))
    dry_run = bool(getattr(args, "dry_run", False))

    def parse_iso(raw: str) -> datetime | None:
        s = (raw or "").strip()
        if not s:
            return None
        try:
            return datetime.fromisoformat(s)
        except Exception:
            return None

    def iso(dt: datetime) -> str:
        return dt.isoformat(timespec="seconds")

    def parse_dt(raw: str) -> datetime | None:
        s = (raw or "").strip()
        if not s:
            return None
        try:
            return datetime.fromisoformat(s)
        except Exception:
            return None

    while True:
        if _paused_marker_path(team_dir).is_file():
            if once:
                return 0
            time_sleep = max(1.0, interval_s)
            time.sleep(time_sleep)
            continue

        data = _load_registry(registry)
        members = data.get("members")
        if not isinstance(members, list):
            members = []

        now_dt = datetime.now()
        now_iso_tick = iso(now_dt)
        drive_mode = _drive_mode_config_hot()
        policy = _policy()
        coord_m = _resolve_latest_by_role(data, policy.root_role)
        coord_full = str(coord_m.get("full", "")).strip() if isinstance(coord_m, dict) else ""
        coord_base = _member_base(coord_m) if isinstance(coord_m, dict) else ""

        member_count = 0
        all_idle = True
        any_pending = False

        for m in members:
            if not isinstance(m, dict):
                continue
            full = str(m.get("full", "")).strip()
            if not full:
                continue
            base = _member_base(m) or full
            role = _member_role(m)

            # Read (or create) state lazily.
            path = _agent_state_path(team_dir, full=full)
            if path.is_file():
                st = _read_json(path)
            else:
                st = _write_agent_state(team_dir, full=full, base=base, role=role, update={})

            prev_status = _normalize_agent_status(str(st.get("status", ""))) or _STATE_STATUS_WORKING
            if prev_status not in _STATE_STATUSES:
                prev_status = _STATE_STATUS_WORKING

            unread, overflow, ids = _inbox_unread_stats(team_dir, to_base=base)
            pending = unread + overflow

            # Derive working/idle from tmux pane activity + grace after wake injection.
            now_iso = now_iso_tick
            last_output_change_dt = parse_dt(str(st.get("last_output_change_at", "") or ""))
            output_update: dict[str, Any] = {}
            auto_update: dict[str, Any] = {}
            if _tmux_running(full):
                tail = _tmux_capture_tail(full, lines=capture_lines)
                if tail is not None:
                    digest = _text_digest(tail)
                    prev_digest = str(st.get("last_output_hash", "") or "")
                    if digest != prev_digest or last_output_change_dt is None:
                        last_output_change_dt = now_dt
                    output_update = {
                        "last_output_hash": digest,
                        "last_output_capture_at": now_iso,
                        "last_output_change_at": iso(last_output_change_dt),
                    }
                    if auto_enter_enabled and auto_enter_patterns and not dry_run:
                        tail_lines = tail.splitlines()
                        window = "\n".join(tail_lines[-max(1, int(auto_enter_tail_lines)) :])
                        matched = ""
                        for pat in auto_enter_patterns:
                            if pat and pat in window:
                                matched = pat
                                break
                        if matched:
                            last_sent_dt = parse_dt(str(st.get("auto_enter_last_sent_at", "") or ""))
                            age_s = (now_dt - last_sent_dt).total_seconds() if last_sent_dt else None
                            if age_s is None or age_s >= max(0.0, auto_enter_cooldown_s):
                                if _tmux_send_enter(full):
                                    auto_update = {
                                        "auto_enter_last_sent_at": now_iso,
                                        "auto_enter_last_reason": matched,
                                        "auto_enter_count": int(st.get("auto_enter_count", 0) or 0) + 1,
                                    }
                                else:
                                    auto_update = {
                                        "auto_enter_last_sent_at": now_iso,
                                        "auto_enter_last_reason": matched,
                                    }
            wake_dt = parse_dt(str(st.get("wakeup_sent_at", "") or ""))
            active = False
            if last_output_change_dt is not None:
                active = (now_dt - last_output_change_dt).total_seconds() <= max(0.0, activity_window_s)
            if not active and wake_dt is not None and grace_s > 0:
                active = (now_dt - wake_dt).total_seconds() <= max(0.0, grace_s)

            status = _STATE_STATUS_WORKING if active else _STATE_STATUS_IDLE
            status_update: dict[str, Any] = {
                "status": status,
                "status_source": "watch",
                "last_inbox_unread": unread,
                "last_inbox_overflow": overflow,
            }
            if status == _STATE_STATUS_IDLE:
                if prev_status != _STATE_STATUS_IDLE:
                    status_update["idle_since"] = now_iso
                status_update["idle_inbox_empty_at"] = now_iso if pending == 0 else ""
            else:
                status_update["idle_since"] = ""
                status_update["idle_inbox_empty_at"] = ""
                status_update["wakeup_scheduled_at"] = ""
                status_update["wakeup_due_at"] = ""
                status_update["wakeup_reason"] = ""

            if not dry_run:
                st = _write_agent_state(team_dir, full=full, base=base, role=role, update={**output_update, **auto_update, **status_update})
            else:
                st = {**st, **output_update, **auto_update, **status_update}

            member_count += 1
            if pending > 0:
                any_pending = True
            if status != _STATE_STATUS_IDLE:
                all_idle = False

            # Working stale inbox governance:
            # If the worker is working and has pending inbox messages older than N seconds,
            # write an inbox-only alert to coord (cooldown applies).
            if (
                coord_full
                and coord_base
                and status == _STATE_STATUS_WORKING
                and not dry_run
                and full != coord_full
            ):
                if pending > 0:
                    _min_n, min_id = _inbox_pending_min_id(team_dir, to_base=base)
                    created = _inbox_message_created_at(team_dir, to_base=base, msg_id=min_id) if min_id else None
                    if created is not None:
                        age_s = (now_dt - created).total_seconds()
                        last_check_dt = parse_dt(str(st.get("last_inbox_check_at", "") or ""))
                        check_age_s = (now_dt - last_check_dt).total_seconds() if last_check_dt else None

                        last_alert_dt = parse_dt(str(st.get("stale_alert_sent_at", "") or ""))
                        alert_age_s = (now_dt - last_alert_dt).total_seconds() if last_alert_dt else None
                        should_alert = age_s >= max(1.0, stale_s)
                        # If we just woke the worker, give them a grace period before alerting.
                        if should_alert and wake_dt is not None and grace_s > 0:
                            wake_age_s = (now_dt - wake_dt).total_seconds()
                            if wake_age_s < max(1.0, grace_s):
                                should_alert = False
                        if should_alert and check_age_s is not None:
                            should_alert = should_alert and check_age_s >= max(1.0, stale_s)
                        if should_alert and alert_age_s is not None:
                            should_alert = should_alert and alert_age_s >= max(1.0, cooldown_s)

                        if should_alert:
                            msg_id = _next_msg_id(team_dir)
                            body = (
                                "[ALERT] stale inbox while working\n"
                                f"- worker: {full} (role={role or '?'}, base={base})\n"
                                f"- status: working\n"
                                f"- pending: unread={unread} overflow={overflow}\n"
                                f"- oldest_id: {min_id} age_s={int(age_s)}\n"
                                f"- last_inbox_check_at: {str(st.get('last_inbox_check_at','') or '(never)')}\n"
                                "Suggested action:\n"
                                f"- Ask the worker to run: bash .codex/skills/ai-team-workflow/scripts/atwf inbox\n"
                                "- If they are stuck, re-scope or pause/unpause that worker.\n"
                            )
                            _write_inbox_message(
                                team_dir,
                                msg_id=msg_id,
                                kind="alert-stale-inbox",
                                from_full="atwf-watch",
                                from_base="atwf-watch",
                                from_role="system",
                                to_full=coord_full,
                                to_base=coord_base,
                                to_role=policy.root_role,
                                body=body,
                            )
                            # Also inject a short notice into coord's CLI so the coordinator
                            # sees governance alerts even if they aren't polling inbox.
                            short = (
                                "[ALERT] stale inbox while working\n"
                                f"worker={base} role={role or '?'} pending={unread}+{overflow} "
                                f"oldest={min_id} age_s={int(age_s)}\n"
                                f"inbox id={msg_id} (run: atwf inbox-open {msg_id} --target coord)\n"
                            )
                            wrapped = _wrap_team_message(
                                team_dir,
                                kind="alert-stale-inbox",
                                sender_full="atwf-watch",
                                sender_role="system",
                                to_full=coord_full,
                                body=short,
                                msg_id=msg_id,
                            )
                            _run_twf(twf, ["send", coord_full, wrapped])
                            _write_agent_state(
                                team_dir,
                                full=full,
                                base=base,
                                role=role,
                                update={
                                    "stale_alert_sent_at": _now(),
                                    "stale_alert_msg_id": msg_id,
                                    "stale_alert_reason": f"pending:{unread}+{overflow} oldest:{min_id} age_s:{int(age_s)}",
                                },
                            )

            # Clear stale wake scheduling when not idle.
            if status != _STATE_STATUS_IDLE:
                if st.get("wakeup_due_at") or st.get("wakeup_scheduled_at") or st.get("wakeup_reason"):
                    if not dry_run:
                        _write_agent_state(
                            team_dir,
                            full=full,
                            base=base,
                            role=role,
                            update={"wakeup_scheduled_at": "", "wakeup_due_at": "", "wakeup_reason": ""},
                        )
                continue

            unread, overflow, ids = _inbox_unread_stats(team_dir, to_base=base)
            pending = unread + overflow
            if pending == 0:
                if st.get("wakeup_due_at") or st.get("wakeup_scheduled_at") or st.get("wakeup_reason"):
                    if not dry_run:
                        _write_agent_state(
                            team_dir,
                            full=full,
                            base=base,
                            role=role,
                            update={"wakeup_scheduled_at": "", "wakeup_due_at": "", "wakeup_reason": ""},
                        )
                continue

            due_dt = parse_iso(str(st.get("wakeup_due_at", "")))
            if due_dt is None:
                due_dt = now_dt + timedelta(seconds=max(1.0, delay_s))
                if not dry_run:
                    _write_agent_state(
                        team_dir,
                        full=full,
                        base=base,
                        role=role,
                        update={
                            "wakeup_scheduled_at": iso(now_dt),
                            "wakeup_due_at": iso(due_dt),
                            "wakeup_reason": f"inbox_pending:{unread}+{overflow}",
                        },
                    )
                continue

            if now_dt < due_dt:
                continue

            # Due: re-check state + inbox before sending.
            st2 = _read_json(path) if path.is_file() else {}
            status2 = _normalize_agent_status(str(st2.get("status", ""))) or _STATE_STATUS_WORKING
            if status2 != _STATE_STATUS_IDLE:
                continue
            unread2, overflow2, _ids2 = _inbox_unread_stats(team_dir, to_base=base)
            pending2 = unread2 + overflow2
            if pending2 == 0:
                continue

            if not _tmux_running(full):
                # Keep due; we'll try again on next tick.
                continue

            if not dry_run:
                _write_agent_state(
                    team_dir,
                    full=full,
                    base=base,
                    role=role,
                    update={
                        "status": _STATE_STATUS_WORKING,
                        "wakeup_sent_at": _now(),
                        "wakeup_scheduled_at": "",
                        "wakeup_due_at": "",
                        "wakeup_reason": f"inbox_pending:{unread2}+{overflow2}",
                        "idle_since": "",
                        "idle_inbox_empty_at": "",
                        "last_inbox_unread": unread2,
                        "last_inbox_overflow": overflow2,
                    },
                )
                # Minimal wake: no body, just a reminder to read inbox.
                _run_twf(twf, ["send", full, message])

        # Auto-finalize reply-needed requests (single consolidated delivery).
        if not dry_run:
            finalizable, _has_pending_replies, _due_targets, _waiters = _scan_reply_requests(team_dir, now_dt=now_dt)
            for req_id, final_status in finalizable:
                msg_id = _next_msg_id(team_dir)
                if _finalize_request(
                    team_dir,
                    data,
                    request_id=req_id,
                    msg_id=msg_id,
                    final_status=final_status,
                    now_iso=now_iso_tick,
                ):
                    # We wrote a new inbox message; treat as pending to avoid drive on this tick.
                    any_pending = True

        # Reply-drive: if the whole team is idle and all inboxes are empty, but reply-needed
        # requests are pending, wake the best "debtor" instead of driving coord.
        suppress_drive = False
        if (
            member_count > 0
            and all_idle
            and not any_pending
            and not dry_run
            and drive_mode == _DRIVE_MODE_RUNNING
        ):
            _finalizable2, has_pending_replies, due_targets, waiters = _scan_reply_requests(team_dir, now_dt=now_dt)
            if has_pending_replies:
                # If nothing is due (everyone snoozed), suppress drive (standby-like behavior).
                if not due_targets:
                    suppress_drive = True
                else:
                    running: list[tuple[int, str, str, str]] = []
                    # (priority, request_id, base, full)
                    for req_id, base, role, st in due_targets:
                        m = _resolve_member(data, base) or {}
                        full = str(m.get("full", "")).strip()
                        if full and _tmux_running(full):
                            prio = int(waiters.get(base, 0) or 0)
                            running.append((prio, req_id, base, full))
                    # If at least one due target is runnable, suppress drive and let reply-drive handle it.
                    if running:
                        suppress_drive = True

                        cooldown_drive_s = _drive_cooldown_s()
                        lock2 = _state_lock_path(team_dir)
                        with _locked(lock2):
                            _ensure_share_layout(team_dir)
                            reply_state = _load_reply_drive_state_unlocked(team_dir)
                        last_reply_dt = parse_dt(str(reply_state.get("last_triggered_at", "") or ""))
                        allow = last_reply_dt is None or (now_dt - last_reply_dt).total_seconds() >= max(0.0, cooldown_drive_s)

                        if allow:
                            running.sort(key=lambda t: (-t[0], t[1], t[2]))
                            _prio, rid, base, full = running[0]
                            role = _member_role(_resolve_member(data, full) or {}) or "?"
                            if full and _tmux_running(full):
                                if not dry_run:
                                    _write_agent_state(
                                        team_dir,
                                        full=full,
                                        base=base,
                                        role=role,
                                        update={
                                            "status": _STATE_STATUS_WORKING,
                                            "wakeup_sent_at": now_iso_tick,
                                            "wakeup_reason": f"reply-needed:{rid}",
                                            "idle_since": "",
                                            "idle_inbox_empty_at": "",
                                        },
                                    )
                                _run_twf(twf, ["send", full, reply_message])
                                _write_reply_drive_state(
                                    team_dir,
                                    update={
                                        "last_triggered_at": now_iso_tick,
                                        "last_reason": "all_idle_inbox_empty_reply_pending",
                                        "last_request_id": rid,
                                        "last_target_base": base,
                                        "last_target_full": full,
                                    },
                                )
                    else:
                        # Due replies exist but no runnable tmux target; allow normal drive to intervene.
                        suppress_drive = False

        # Drive loop (anti-stall): if the whole team is idle and all inboxes are empty,
        # wake a single driver to re-kickoff work (only when drive mode is running).
        if (
            member_count > 0
            and all_idle
            and not any_pending
            and not dry_run
            and drive_mode == _DRIVE_MODE_RUNNING
            and not suppress_drive
        ):
            cooldown_drive_s = _drive_cooldown_s()
            driver_role = _drive_driver_role()
            backup_role = _drive_backup_role()

            lock = _state_lock_path(team_dir)
            with _locked(lock):
                _ensure_share_layout(team_dir)
                drive_state = _load_drive_state_unlocked(team_dir, mode_default=drive_mode)
            last_drive_dt = parse_dt(str(drive_state.get("last_triggered_at", "") or ""))
            if last_drive_dt is None or (now_dt - last_drive_dt).total_seconds() >= max(0.0, cooldown_drive_s):
                driver_m = _resolve_latest_by_role(data, driver_role)
                driver_full = str(driver_m.get("full", "")).strip() if isinstance(driver_m, dict) else ""
                driver_base = _member_base(driver_m) if isinstance(driver_m, dict) else ""
                driver_base = driver_base or driver_full

                target_full = driver_full
                target_role = driver_role
                target_base = driver_base
                if target_full and not _tmux_running(target_full):
                    backup_m = _resolve_latest_by_role(data, backup_role)
                    backup_full = str(backup_m.get("full", "")).strip() if isinstance(backup_m, dict) else ""
                    backup_base = _member_base(backup_m) if isinstance(backup_m, dict) else ""
                    if backup_full and _tmux_running(backup_full):
                        target_full = backup_full
                        target_role = backup_role
                        target_base = backup_base or backup_full

                if target_full:
                    msg_id = _next_msg_id(team_dir)
                    body = _drive_message_body(iso_ts=now_iso_tick, msg_id=msg_id)
                    _write_inbox_message(
                        team_dir,
                        msg_id=msg_id,
                        kind="drive",
                        from_full="atwf-drive",
                        from_base="atwf-drive",
                        from_role="system",
                        to_full=target_full,
                        to_base=target_base,
                        to_role=target_role,
                        body=body,
                    )
                    short = _drive_message_summary(iso_ts=now_iso_tick, msg_id=msg_id)
                    wrapped = _wrap_team_message(
                        team_dir,
                        kind="drive",
                        sender_full="atwf-drive",
                        sender_role="system",
                        to_full=target_full,
                        body=short,
                        msg_id=msg_id,
                    )
                    _run_twf(twf, ["send", target_full, wrapped])
                    _write_drive_state(
                        team_dir,
                        update={
                            "last_triggered_at": now_iso_tick,
                            "last_msg_id": msg_id,
                            "last_reason": "all_idle_inbox_empty",
                            "last_driver_full": target_full,
                        },
                    )

        if once:
            return 0
        time_sleep = max(1.0, interval_s)
        time.sleep(time_sleep)


def cmd_inbox(args: argparse.Namespace) -> int:
    team_dir = _default_team_dir()
    registry = _registry_path(team_dir)
    data = _load_registry(registry)

    target = str(getattr(args, "target", "") or "").strip()
    is_self = False
    if target:
        full = _resolve_target_full(data, target)
        if not full:
            raise SystemExit(f"❌ target not found in registry: {target}")
        m = _resolve_member(data, full) or {}
        to_base = _member_base(m) or full
    else:
        self_full = _tmux_self_full()
        if not self_full:
            raise SystemExit("❌ inbox must run inside tmux (or use: inbox --target <full|base|role>)")
        m = _resolve_member(data, self_full)
        if not m:
            raise SystemExit(f"❌ current worker not found in registry: {self_full}")
        to_base = _member_base(m) or self_full
        is_self = True

    base_dir = _inbox_member_dir(team_dir, base=to_base)
    unread_root = base_dir / _INBOX_UNREAD_DIR
    overflow_root = base_dir / _INBOX_OVERFLOW_DIR

    rows: list[tuple[int, str, str, str, str, str]] = []

    def parse_meta(path: Path) -> tuple[str, str]:
        kind = ""
        summary = ""
        try:
            head = path.read_text(encoding="utf-8", errors="ignore").splitlines()[:40]
        except Exception:
            return kind, summary
        for line in head:
            s = line.strip()
            if s.startswith("- kind:"):
                kind = s.split(":", 1)[1].strip().strip("`")
            elif s.startswith("- summary:"):
                summary = s.split(":", 1)[1].strip()
        return kind, summary

    if unread_root.is_dir():
        for from_dir in sorted([p for p in unread_root.glob("from-*") if p.is_dir()]):
            from_base = from_dir.name[len("from-") :]
            for n, stem, p in _inbox_list_msgs(from_dir):
                kind, summary = parse_meta(p)
                rows.append((n, stem, from_base, kind, summary, _INBOX_UNREAD_DIR))

    if overflow_root.is_dir():
        for from_dir in sorted([p for p in overflow_root.glob("from-*") if p.is_dir()]):
            from_base = from_dir.name[len("from-") :]
            for n, stem, p in _inbox_list_msgs(from_dir):
                kind, summary = parse_meta(p)
                rows.append((n, stem, from_base, kind, summary, _INBOX_OVERFLOW_DIR))

    rows.sort(key=lambda r: r[0])
    if not rows:
        print("(empty)")
        return 0

    for _n, msg_id, from_base, kind, summary, state in rows:
        parts = [msg_id, from_base]
        parts.append(kind or "?")
        if summary:
            parts.append(summary)
        if state != _INBOX_UNREAD_DIR:
            parts.append(state)
        print("\t".join(parts))

    if is_self:
        self_full = _tmux_self_full() or ""
        if self_full and isinstance(m, dict):
            base = _member_base(m) or self_full
            role = _member_role(m)
            unread, overflow, _ids = _inbox_unread_stats(team_dir, to_base=base)
            _update_agent_state(
                team_dir,
                full=self_full,
                base=base,
                role=role,
                updater=lambda s: (
                    s.__setitem__("last_inbox_check_at", _now()),
                    s.__setitem__("last_inbox_unread", unread),
                    s.__setitem__("last_inbox_overflow", overflow),
                ),
            )
    return 0


def cmd_inbox_open(args: argparse.Namespace) -> int:
    team_dir = _default_team_dir()
    registry = _registry_path(team_dir)
    data = _load_registry(registry)

    msg_id = str(args.msg_id or "").strip()
    if not msg_id:
        raise SystemExit("❌ msg_id is required")

    target = str(getattr(args, "target", "") or "").strip()
    if target:
        full = _resolve_target_full(data, target)
        if not full:
            raise SystemExit(f"❌ target not found in registry: {target}")
        m = _resolve_member(data, full) or {}
        to_base = _member_base(m) or full
    else:
        self_full = _tmux_self_full()
        if not self_full:
            raise SystemExit("❌ inbox-open must run inside tmux (or use: inbox-open --target <full|base|role> <id>)")
        m = _resolve_member(data, self_full)
        if not m:
            raise SystemExit(f"❌ current worker not found in registry: {self_full}")
        to_base = _member_base(m) or self_full

    hit = _find_inbox_message_file(team_dir, to_base=to_base, msg_id=msg_id)
    if not hit:
        raise SystemExit(f"❌ message not found in inbox: {msg_id}")
    _state, _from_base, path = hit
    content = path.read_text(encoding="utf-8", errors="ignore")
    sys.stdout.write(content)
    if content and not content.endswith("\n"):
        sys.stdout.write("\n")

    # Update "last_inbox_check_at" for self only.
    if not target:
        self_full = _tmux_self_full() or ""
        if self_full and isinstance(m, dict):
            base = _member_base(m) or self_full
            role = _member_role(m)
            unread, overflow, _ids = _inbox_unread_stats(team_dir, to_base=base)
            _update_agent_state(
                team_dir,
                full=self_full,
                base=base,
                role=role,
                updater=lambda s: (
                    s.__setitem__("last_inbox_check_at", _now()),
                    s.__setitem__("last_inbox_unread", unread),
                    s.__setitem__("last_inbox_overflow", overflow),
                ),
            )
    return 0


def cmd_inbox_ack(args: argparse.Namespace) -> int:
    team_dir = _default_team_dir()
    registry = _registry_path(team_dir)
    data = _load_registry(registry)

    msg_id = str(args.msg_id or "").strip()
    if not msg_id:
        raise SystemExit("❌ msg_id is required")

    self_full = _tmux_self_full()
    if not self_full:
        raise SystemExit("❌ inbox-ack must run inside tmux")
    m = _resolve_member(data, self_full)
    if not m:
        raise SystemExit(f"❌ current worker not found in registry: {self_full}")
    to_base = _member_base(m) or self_full

    moved = _mark_inbox_read(team_dir, to_base=to_base, msg_id=msg_id)
    if not moved:
        raise SystemExit(f"❌ message not found: {msg_id}")
    print("OK")

    unread, overflow, _ids = _inbox_unread_stats(team_dir, to_base=to_base)
    _update_agent_state(
        team_dir,
        full=self_full,
        base=to_base,
        role=_member_role(m),
        updater=lambda s: (
            s.__setitem__("last_inbox_check_at", _now()),
            s.__setitem__("last_inbox_unread", unread),
            s.__setitem__("last_inbox_overflow", overflow),
        ),
    )
    return 0


def cmd_inbox_pending(args: argparse.Namespace) -> int:
    team_dir = _default_team_dir()
    registry = _registry_path(team_dir)
    data = _load_registry(registry)

    actor_full = _resolve_actor_full(data, as_target=getattr(args, "as_target", None))
    actor_m = _resolve_member(data, actor_full)
    if not actor_m:
        raise SystemExit(f"❌ actor not found in registry: {actor_full}")
    from_base = _member_base(actor_m) or actor_full

    target = str(args.target or "").strip()
    if not target:
        raise SystemExit("❌ target is required")
    target_full = _resolve_target_full(data, target)
    if not target_full:
        raise SystemExit(f"❌ target not found in registry: {target}")
    target_m = _resolve_member(data, target_full) or {}
    to_base = _member_base(target_m) or target_full

    unread_dir = _inbox_thread_dir(team_dir, to_base=to_base, from_base=from_base, state=_INBOX_UNREAD_DIR)
    overflow_dir = _inbox_thread_dir(team_dir, to_base=to_base, from_base=from_base, state=_INBOX_OVERFLOW_DIR)

    unread = len(_inbox_list_msgs(unread_dir))
    overflow = len(_inbox_list_msgs(overflow_dir))
    print(f"unread={unread} overflow={overflow}")
    return 0


def cmd_bootstrap(args: argparse.Namespace) -> int:
    twf = _resolve_twf()
    team_dir = _default_team_dir()
    registry = _registry_path(team_dir)
    role = _require_role(args.role)

    target = args.name.strip()
    if not target:
        raise SystemExit("❌ name is required")

    data = _load_registry(registry)
    full = _resolve_target_full(data, target)
    if not full:
        raise SystemExit(f"❌ name not found in registry: {target} (use `atwf list`)")
    m = _resolve_member(data, full)
    base = str(m.get("base") or "").strip() if m else ""
    base = base or full

    _bootstrap_worker(twf, name=full, role=role, full=full, base=base, registry=registry, team_dir=team_dir)
    _eprint(f"✅ bootstrapped: {full} as {role}")
    return 0


def cmd_remove(args: argparse.Namespace) -> int:
    twf = _resolve_twf()
    team_dir = _default_team_dir()
    registry = _registry_path(team_dir)

    pm_full = _require_full_name(args.pm_full)

    lock = team_dir / ".lock"
    with _locked(lock):
        data = _load_registry(registry)
        pm = _resolve_member(data, pm_full)
        if not pm:
            raise SystemExit(f"❌ pm not found in registry: {pm_full}")
        role = str(pm.get("role", "")).strip()
        if role != "pm":
            raise SystemExit(f"❌ remove only supports PM. Provided worker role={role!r} full={pm_full}")

        members = data.get("members", [])
        if not isinstance(members, list) or not members:
            _eprint("ℹ️ registry has no members; nothing to remove")
            return 0

        to_remove: list[str] = []
        for m in members:
            if not isinstance(m, dict):
                continue
            full = str(m.get("full", "")).strip()
            if not full or not FULL_NAME_RE.match(full):
                continue
            to_remove.append(full)

    # Remove everything recorded in the registry (team disband), with PM last.
    uniq: list[str] = []
    seen: set[str] = set()
    for full in to_remove:
        if full not in seen:
            seen.add(full)
            uniq.append(full)

    uniq_no_pm = [n for n in uniq if n != pm_full]
    ordered = uniq_no_pm + [pm_full] if pm_full in seen else uniq_no_pm

    if args.dry_run:
        print("\n".join(ordered))
        return 0

    failed: list[str] = []
    for full in ordered:
        res = _run_twf(twf, ["remove", full, "--no-recursive"])
        if res.returncode != 0:
            failed.append(full)
            err = (res.stderr or "").strip()
            _eprint(f"⚠️ twf remove failed for {full}: {err or res.stdout.strip()}")

    with _locked(lock):
        data = _load_registry(registry)
        data["members"] = []
        data["updated_at"] = _now()
        _write_json_atomic(registry, data)

    if failed:
        _eprint(f"❌ team disband completed with failures: {len(failed)} workers (see stderr)")
        return 1
    _eprint("✅ team disbanded (registry cleared)")
    return 0


def build_parser() -> argparse.ArgumentParser:
    enabled_roles = sorted(_policy().enabled_roles)
    p = argparse.ArgumentParser(prog="atwf", add_help=True)
    sub = p.add_subparsers(dest="cmd", required=True)

    init = sub.add_parser("init", help="init registry and start initial team (root_role + pm + liaison)")
    init.add_argument("task", nargs="?", help="task description (saved to share/task.md); or pipe via stdin")
    init.add_argument("--task-file", help="task file path to copy into share/task.md")
    init.add_argument("--registry-only", action="store_true", help="only create registry, do not start workers")
    init.add_argument("--force-new", action="store_true", help="always start a fresh trio (even if one exists)")
    init.add_argument("--no-bootstrap", action="store_true", help="skip sending role templates on creation")

    reset = sub.add_parser("reset", help="reset local environment (delete worker state + share; preserve account pool by default)")
    reset.add_argument("--dry-run", action="store_true", help="print what would be deleted, without deleting")
    reset.add_argument("--force", action="store_true", help="also delete codex_home paths outside ~/.codex-workers (dangerous)")
    reset.add_argument("--wipe-account-pool", action="store_true", help="also delete local account pool state.json (resets auth ordering/pointer)")

    up = sub.add_parser("up", help="start a new worker (root_role only; twf up) + register + bootstrap")
    up.add_argument("role")
    up.add_argument("label", nargs="?")
    up.add_argument("--scope", default="")
    up.add_argument("--no-bootstrap", action="store_true")

    sp = sub.add_parser("spawn", help="spawn a child worker (twf spawn) + register + bootstrap")
    sp.add_argument("parent_full")
    sp.add_argument("role")
    sp.add_argument("label", nargs="?")
    sp.add_argument("--scope", default="")
    sp.add_argument("--no-bootstrap", action="store_true")

    sps = sub.add_parser("spawn-self", help="spawn a child worker from the current tmux session")
    sps.add_argument("role")
    sps.add_argument("label", nargs="?")
    sps.add_argument("--scope", default="")
    sps.add_argument("--no-bootstrap", action="store_true")

    parent = sub.add_parser("parent", help="print a member's parent (lookup by full or base)")
    parent.add_argument("name")

    sub.add_parser("parent-self", help="print current worker's parent (inside tmux)")

    children = sub.add_parser("children", help="print a member's children (lookup by full or base)")
    children.add_argument("name")

    sub.add_parser("children-self", help="print current worker's children (inside tmux)")

    rup = sub.add_parser("report-up", help="send a completion/progress report to your parent (inside tmux)")
    rup.add_argument("message", nargs="?")
    rup.add_argument("--wait", action="store_true", help="wait for a reply (uses twf ask)")

    rto = sub.add_parser("report-to", help="send a report to a target member or role (inside tmux)")
    rto.add_argument("target", help="full|base|role (see `atwf policy` for enabled roles)")
    rto.add_argument("message", nargs="?")
    rto.add_argument("--wait", action="store_true", help="wait for a reply (uses twf ask)")

    sub.add_parser("self", help="print current tmux session name")

    reg = sub.add_parser("register", help="upsert a member into registry.json")
    reg.add_argument("full")
    reg.add_argument("--role", choices=enabled_roles)
    reg.add_argument("--base")
    reg.add_argument("--scope")
    reg.add_argument("--parent")
    reg.add_argument("--state-file")
    reg.add_argument("--force", action="store_true", help="bypass root/parent policy checks (registry repair)")

    regself = sub.add_parser("register-self", help="register current tmux session into registry.json")
    regself.add_argument("--role", required=True, choices=enabled_roles)
    regself.add_argument("--base")
    regself.add_argument("--scope")
    regself.add_argument("--parent")
    regself.add_argument("--state-file")
    regself.add_argument("--force", action="store_true", help="bypass root/parent policy checks (registry repair)")

    ss = sub.add_parser("set-scope", help="update scope for a member (lookup by full or base)")
    ss.add_argument("name")
    ss.add_argument("scope")

    sss = sub.add_parser("set-scope-self", help="update scope for current tmux session")
    sss.add_argument("scope")

    sub.add_parser("list", help="print registry table")

    sub.add_parser("where", help="print resolved shared dirs (team_dir + registry)")

    sub.add_parser("policy", help="print resolved team policy (hard constraints)")

    sub.add_parser("perms-self", help="print current worker permissions (inside tmux)")

    tree = sub.add_parser("tree", help="print org tree from registry (parent/children)")
    tree.add_argument("root", nargs="?", help="optional root: full|base|role")

    dpath = sub.add_parser("design-path", help="print the per-member design doc path under share/design/")
    dpath.add_argument("target", help="full|base|role")

    dinit = sub.add_parser("design-init", help="create a design doc stub under share/design/ (non-destructive by default)")
    dinit.add_argument("target", help="full|base|role")
    dinit.add_argument("--force", action="store_true", help="overwrite if exists")

    dself = sub.add_parser("design-init-self", help="create a design doc stub for the current tmux worker")
    dself.add_argument("--force", action="store_true", help="overwrite if exists")

    wtp = sub.add_parser("worktree-path", help="print the dedicated git worktree path for a worker")
    wtp.add_argument("target", help="full|base|role")

    wtc = sub.add_parser("worktree-create", help="create a dedicated git worktree under <git-root>/worktree/<full>")
    wtc.add_argument("target", help="full|base|role")
    wtc.add_argument("--base", default="HEAD", help="base ref/branch/commit (default: HEAD)")
    wtc.add_argument("--branch", default="", help="branch name to create for the worktree (default: <full>)")

    wtcs = sub.add_parser("worktree-create-self", help="create a dedicated git worktree for the current tmux worker")
    wtcs.add_argument("--base", default="HEAD", help="base ref/branch/commit (default: HEAD)")
    wtcs.add_argument("--branch", default="", help="branch name to create for the worktree (default: <full>)")

    sub.add_parser("worktree-check-self", help="ensure you are working inside your dedicated worktree (inside tmux)")

    stop = sub.add_parser("stop", help="stop Codex tmux workers (default: whole team)")
    stop.add_argument("targets", nargs="*", help="optional targets (full|base|role)")
    stop.add_argument("--role", choices=enabled_roles, help="stop all members of a role")
    stop.add_argument("--subtree", help="stop all members under a root (full|base|role)")
    stop.add_argument("--dry-run", action="store_true", help="print what would be stopped")

    resume = sub.add_parser("resume", help="resume Codex tmux workers (default: whole team)")
    resume.add_argument("targets", nargs="*", help="optional targets (full|base|role)")
    resume.add_argument("--role", choices=enabled_roles, help="resume all members of a role")
    resume.add_argument("--subtree", help="resume all members under a root (full|base|role)")
    resume.add_argument("--dry-run", action="store_true", help="print what would be resumed")

    pause = sub.add_parser("pause", help="pause workers and disable watcher actions (recommended for humans)")
    pause.add_argument("targets", nargs="*", help="optional targets (full|base|role)")
    pause.add_argument("--role", choices=enabled_roles, help="pause all members of a role")
    pause.add_argument("--subtree", help="pause all members under a root (full|base|role)")
    pause.add_argument("--dry-run", action="store_true", help="print what would be paused (still writes marker)")
    pause.add_argument("--reason", default="", help="optional pause reason (if omitted, read stdin)")

    unpause = sub.add_parser("unpause", help="unpause workers (resume) without restarting watcher")
    unpause.add_argument("targets", nargs="*", help="optional targets (full|base|role)")
    unpause.add_argument("--role", choices=enabled_roles, help="unpause all members of a role")
    unpause.add_argument("--subtree", help="unpause all members under a root (full|base|role)")
    unpause.add_argument("--dry-run", action="store_true", help="print what would be resumed")

    bc = sub.add_parser("broadcast", help="send the same message to multiple workers (sequential)")
    bc.add_argument("targets", nargs="*", help="targets (full|base|role). Ignored when --role/--subtree is used.")
    bc.add_argument("--role", choices=enabled_roles, help="broadcast to all members of a role")
    bc.add_argument("--subtree", help="broadcast to all members under a root (full|base|role)")
    bc.add_argument("--message", default=None, help="message text (if omitted, read stdin)")
    bc.add_argument("--as", dest="as_target", default=None, help="actor (full|base|role); required outside tmux")
    bc.add_argument("--include-excluded", action="store_true", help="include excluded roles when using --subtree")
    bc.add_argument("--notify", action="store_true", help="also inject a short inbox notice into recipients' CLIs (discouraged)")

    notice = sub.add_parser("notice", help="send a notice (FYI, no reply expected; supports stdin)")
    notice.add_argument("targets", nargs="*", help="targets (full|base|role). Ignored when --role/--subtree is used.")
    notice.add_argument("--role", choices=enabled_roles, help="notice all members of a role")
    notice.add_argument("--subtree", help="notice all members under a root (full|base|role)")
    notice.add_argument("--message", default=None, help="message text (if omitted, read stdin)")
    notice.add_argument("--as", dest="as_target", default=None, help="actor (full|base|role); required outside tmux")
    notice.add_argument("--include-excluded", action="store_true", help="include excluded roles when using --subtree")
    notice.add_argument("--notify", action="store_true", help="also inject inbox notice into recipient CLIs (discouraged)")

    action = sub.add_parser("action", help="send an action/instruction (no immediate ACK; supports stdin)")
    action.add_argument("targets", nargs="*", help="targets (full|base|role). Ignored when --role/--subtree is used.")
    action.add_argument("--role", choices=enabled_roles, help="send an action to all members of a role")
    action.add_argument("--subtree", help="send an action to all members under a root (full|base|role)")
    action.add_argument("--message", default=None, help="message text (if omitted, read stdin)")
    action.add_argument("--as", dest="as_target", default=None, help="actor (full|base|role); required outside tmux")
    action.add_argument("--include-excluded", action="store_true", help="include excluded roles when using --subtree")
    action.add_argument("--notify", action="store_true", help="also inject inbox notice into recipient CLIs (discouraged)")

    resolve = sub.add_parser("resolve", help="resolve a target to full tmux session name (full|base|role)")
    resolve.add_argument("target")

    attach = sub.add_parser("attach", help="enter a worker tmux session (full|base|role)")
    attach.add_argument("target")

    route = sub.add_parser("route", help="find best owner(s) for a query")
    route.add_argument("query")
    route.add_argument("--role", choices=enabled_roles)
    route.add_argument("--limit", type=int, default=5)

    ask = sub.add_parser("ask", help="twf ask wrapper (supports stdin)")
    ask.add_argument("name")
    ask.add_argument("message", nargs="?")
    ask.add_argument("--as", dest="as_target", default=None, help="actor (full|base|role); required outside tmux")
    ask.add_argument("--notify", action="store_true", help="inject inbox notice into recipient CLI (discouraged)")
    ask.add_argument("--wait", action="store_true", help="wait for reply (implies CLI injection; requires --notify)")

    send = sub.add_parser("send", help="twf send wrapper with policy checks (supports stdin)")
    send.add_argument("name")
    send.add_argument("message", nargs="?")
    send.add_argument("--as", dest="as_target", default=None, help="actor (full|base|role); required outside tmux")
    send.add_argument("--notify", action="store_true", help="also inject inbox notice into recipient CLI (discouraged)")

    gather = sub.add_parser("gather", help="create a reply-needed request to multiple targets (supports stdin)")
    gather.add_argument("targets", nargs="+", help="targets (full|base|role)")
    gather.add_argument("--message", default=None, help="message text (if omitted, read stdin)")
    gather.add_argument("--topic", default="", help="request topic/title (default: first non-empty line)")
    gather.add_argument("--deadline", default="", help="deadline duration (default: config; e.g. 1h, 30m, 900s)")
    gather.add_argument("--as", dest="as_target", default=None, help="actor (full|base|role); required outside tmux")

    respond = sub.add_parser("respond", help="reply to a reply-needed request (supports stdin)")
    respond.add_argument("request_id", help="request id (e.g. req-000123)")
    respond.add_argument("message", nargs="?")
    respond.add_argument("--blocked", action="store_true", help="acknowledge but block/snooze reminders")
    respond.add_argument("--snooze", default="", help="snooze duration for --blocked (default: config; e.g. 15m)")
    respond.add_argument("--waiting-on", default="", help="who you are waiting on (base name, optional)")
    respond.add_argument("--as", dest="as_target", default=None, help="actor (full|base|role); required outside tmux")

    reply_needed = sub.add_parser("reply-needed", help="list pending reply-needed requests (self by default)")
    reply_needed.add_argument("--target", default="", help="optional target to inspect (full|base|role)")

    request = sub.add_parser("request", help="show request status/paths")
    request.add_argument("request_id")

    receipts = sub.add_parser("receipts", help="query read receipts for a msg id across recipients")
    receipts.add_argument("msg_id")
    receipts.add_argument("targets", nargs="*", help="optional targets (full|base|role); default: all members")
    receipts.add_argument("--role", choices=enabled_roles, help="limit to a role")
    receipts.add_argument("--subtree", help="limit to a subtree under a root (full|base|role)")

    handoff = sub.add_parser("handoff", help="create a handoff/permit so two members can talk directly")
    handoff.add_argument("a", help="member A (full|base|role)")
    handoff.add_argument("b", help="member B (full|base|role)")
    handoff.add_argument("--as", dest="as_target", default=None, help="creator (full|base|role); required outside tmux")
    handoff.add_argument("--reason", default="", help="handoff reason (optional)")
    handoff.add_argument("--ttl", type=int, default=None, help="permit ttl in seconds (optional)")
    handoff.add_argument("--dry-run", action="store_true", help="do not write/send; print what would happen")
    handoff.add_argument("--notify", action="store_true", help="also inject inbox notice into both CLIs (discouraged)")

    pend = sub.add_parser("pend", help="twf pend wrapper")
    pend.add_argument("name")
    pend.add_argument("n", nargs="?", type=int)

    ping = sub.add_parser("ping", help="twf ping wrapper")
    ping.add_argument("name")

    drive = sub.add_parser("drive", help="get/set drive mode (running|standby)")
    drive.add_argument("mode", nargs="?", default="", help="running|standby")

    state = sub.add_parser("state", help="print agent state table (or one target)")
    state.add_argument("target", nargs="?", default="", help="optional target (full|base|role)")

    sub.add_parser("state-self", help="print current worker state (inside tmux)")

    state_set_self = sub.add_parser("state-set-self", help="set current worker state (inside tmux)")
    state_set_self.add_argument("status", help="working|draining|idle")

    state_set = sub.add_parser("state-set", help="operator: set a worker state (use --force for draining/idle)")
    state_set.add_argument("target", help="target member (full|base|role)")
    state_set.add_argument("status", help="working|draining|idle")
    state_set.add_argument("--force", action="store_true", help="allow setting draining/idle for other workers")

    watch_idle = sub.add_parser("watch-idle", help="operator: wake idle workers when inbox has unread messages")
    watch_idle.add_argument("--interval", type=float, default=None, help="poll interval seconds (default: config)")
    watch_idle.add_argument("--delay", type=float, default=None, help="wake delay seconds (default: config)")
    watch_idle.add_argument("--message", default="", help="wake message injected into Codex TUI (default: config)")
    watch_idle.add_argument("--working-stale", type=float, default=None, help="alert coord if a working worker has pending inbox older than N seconds (default: config)")
    watch_idle.add_argument("--alert-cooldown", type=float, default=None, help="minimum seconds between alerts per worker (default: config)")
    watch_idle.add_argument("--once", action="store_true", help="run one tick then exit")
    watch_idle.add_argument("--dry-run", action="store_true", help="do not write/send; print nothing, but still polls")

    inbox = sub.add_parser("inbox", help="list unread inbox messages (self by default)")
    inbox.add_argument("--target", default="", help="optional target inbox to inspect (full|base|role)")

    inbox_open = sub.add_parser("inbox-open", help="print a message body from inbox by id (self by default)")
    inbox_open.add_argument("msg_id")
    inbox_open.add_argument("--target", default="", help="optional target inbox to inspect (full|base|role)")

    inbox_ack = sub.add_parser("inbox-ack", help="mark an inbox message as read (self only)")
    inbox_ack.add_argument("msg_id")

    inbox_pending = sub.add_parser("inbox-pending", help="count pending messages you sent to a target")
    inbox_pending.add_argument("target", help="target member (full|base|role)")
    inbox_pending.add_argument("--as", dest="as_target", default=None, help="actor (full|base|role); required outside tmux")

    boot = sub.add_parser("bootstrap", help="send the role prompt template to a worker")
    boot.add_argument("name")
    boot.add_argument("role", choices=enabled_roles)

    return p


def main(argv: list[str]) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.cmd == "init":
        return cmd_init(args)
    if args.cmd == "reset":
        return cmd_reset(args)
    if args.cmd == "up":
        return cmd_up(args)
    if args.cmd == "spawn":
        return cmd_spawn(args)
    if args.cmd == "spawn-self":
        return cmd_spawn_self(args)
    if args.cmd == "parent":
        return cmd_parent(args)
    if args.cmd == "parent-self":
        return cmd_parent_self(args)
    if args.cmd == "children":
        return cmd_children(args)
    if args.cmd == "children-self":
        return cmd_children_self(args)
    if args.cmd == "report-up":
        return cmd_report_up(args)
    if args.cmd == "report-to":
        return cmd_report_to(args)
    if args.cmd == "self":
        return cmd_self(args)
    if args.cmd == "register":
        return cmd_register(args)
    if args.cmd == "register-self":
        return cmd_register_self(args)
    if args.cmd == "set-scope":
        return cmd_set_scope(args)
    if args.cmd == "set-scope-self":
        return cmd_set_scope_self(args)
    if args.cmd == "list":
        return cmd_list(args)
    if args.cmd == "where":
        return cmd_where(args)
    if args.cmd == "policy":
        return cmd_policy(args)
    if args.cmd == "perms-self":
        return cmd_perms_self(args)
    if args.cmd == "tree":
        return cmd_tree(args)
    if args.cmd == "design-path":
        return cmd_design_path(args)
    if args.cmd == "design-init":
        return cmd_design_init(args)
    if args.cmd == "design-init-self":
        return cmd_design_init_self(args)
    if args.cmd == "worktree-path":
        return cmd_worktree_path(args)
    if args.cmd == "worktree-create":
        return cmd_worktree_create(args)
    if args.cmd == "worktree-create-self":
        return cmd_worktree_create_self(args)
    if args.cmd == "worktree-check-self":
        return cmd_worktree_check_self(args)
    if args.cmd == "stop":
        return cmd_stop(args)
    if args.cmd == "resume":
        return cmd_resume(args)
    if args.cmd == "pause":
        return cmd_pause(args)
    if args.cmd == "unpause":
        return cmd_unpause(args)
    if args.cmd == "broadcast":
        return cmd_broadcast(args)
    if args.cmd == "notice":
        return cmd_notice(args)
    if args.cmd == "action":
        return cmd_action(args)
    if args.cmd == "resolve":
        return cmd_resolve(args)
    if args.cmd == "attach":
        return cmd_attach(args)
    if args.cmd == "route":
        return cmd_route(args)
    if args.cmd == "ask":
        return cmd_ask(args)
    if args.cmd == "send":
        return cmd_send(args)
    if args.cmd == "gather":
        return cmd_gather(args)
    if args.cmd == "respond":
        return cmd_respond(args)
    if args.cmd == "reply-needed":
        return cmd_reply_needed(args)
    if args.cmd == "request":
        return cmd_request(args)
    if args.cmd == "receipts":
        return cmd_receipts(args)
    if args.cmd == "handoff":
        return cmd_handoff(args)
    if args.cmd == "pend":
        return cmd_pend(args)
    if args.cmd == "ping":
        return cmd_ping(args)
    if args.cmd == "drive":
        return cmd_drive(args)
    if args.cmd == "state":
        return cmd_state(args)
    if args.cmd == "state-self":
        return cmd_state_self(args)
    if args.cmd == "state-set-self":
        return cmd_state_set_self(args)
    if args.cmd == "state-set":
        return cmd_state_set(args)
    if args.cmd == "watch-idle":
        return cmd_watch_idle(args)
    if args.cmd == "inbox":
        return cmd_inbox(args)
    if args.cmd == "inbox-open":
        return cmd_inbox_open(args)
    if args.cmd == "inbox-ack":
        return cmd_inbox_ack(args)
    if args.cmd == "inbox-pending":
        return cmd_inbox_pending(args)
    if args.cmd == "bootstrap":
        return cmd_bootstrap(args)

    raise SystemExit("❌ unreachable")


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
