#!/usr/bin/env python3
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import re
import secrets
import shlex
import shutil
import subprocess
import sys
import tempfile
import time
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


def _now() -> str:
    return datetime.now().isoformat(timespec="seconds")


def _eprint(msg: str) -> None:
    print(msg, file=sys.stderr)


def _skill_dir() -> Path:
    return Path(__file__).resolve().parents[1]


def _config_path() -> Path:
    return Path(__file__).resolve().with_name("cap_config.yaml")


def _read_simple_yaml_kv(path: Path) -> dict[str, str]:
    try:
        raw = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return {}
    except OSError:
        return {}

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


def _expand_path_from(base: Path, path: str) -> Path:
    p = Path(os.path.expanduser(path.strip()))
    if not p.is_absolute():
        p = (base / p).resolve()
    return p


def _parse_sources(raw: str) -> list[str]:
    s = (raw or "").strip()
    if not s:
        return []

    if s.lstrip().startswith("["):
        try:
            parsed = json.loads(s)
            if isinstance(parsed, list):
                out: list[str] = []
                for v in parsed:
                    if isinstance(v, str) and v.strip():
                        out.append(v.strip())
                return out
        except json.JSONDecodeError:
            pass

    parts = [p.strip() for p in s.split(",")]
    return [p for p in parts if p]


@dataclass(frozen=True)
class _Config:
    sources: list[Path]
    strategy: str
    state_file: Path
    auth_team_dir: Path | None
    auth_team_glob: str
    auth_strategy: str


def _load_config() -> _Config:
    skill_dir = _skill_dir()
    cfg = _read_simple_yaml_kv(_config_path())

    sources_raw = os.environ.get("CAP_SOURCES", "").strip() or cfg.get("sources", "").strip()
    strategy = os.environ.get("CAP_STRATEGY", "").strip() or cfg.get("strategy", "round_robin").strip()
    state_raw = os.environ.get("CAP_STATE_FILE", "").strip() or cfg.get("state_file", "share/state.json").strip()
    auth_team_dir_raw = (
        os.environ.get("CAP_AUTH_TEAM_DIR", "").strip()
        or os.environ.get("AUTH_TEAM_DIR", "").strip()
        or cfg.get("auth_team_dir", "").strip()
    )
    auth_team_glob = os.environ.get("CAP_AUTH_TEAM_GLOB", "").strip() or cfg.get("auth_team_glob", "*").strip()
    auth_strategy_raw = os.environ.get("CAP_AUTH_STRATEGY", "").strip() or cfg.get("auth_strategy", "balanced").strip()

    strategy = (strategy or "round_robin").strip().lower()
    if strategy not in {"round_robin", "hash"}:
        raise SystemExit(f"❌ unsupported strategy: {strategy!r} (use: round_robin|hash)")

    auth_strategy = (auth_strategy_raw or "balanced").strip().lower()
    if auth_strategy in {"least_used", "least-used"}:
        auth_strategy = "balanced"
    if auth_strategy in {"round_robin", "rr"}:
        # Avoid confusion with CODEX_HOME strategy naming.
        auth_strategy = "team_cycle"
    if auth_strategy not in {"balanced", "team_cycle"}:
        raise SystemExit(f"❌ unsupported auth_strategy: {auth_strategy_raw!r} (use: balanced|team_cycle)")

    sources_in = _parse_sources(sources_raw)
    sources: list[Path] = []
    for s in sources_in:
        try:
            p = _expand_path_from(skill_dir, s)
        except Exception:
            continue
        if p.is_dir():
            sources.append(p)

    if not sources:
        default = Path.home() / ".codex"
        if default.is_dir():
            sources = [default]
        else:
            raise SystemExit(
                "❌ no valid sources configured.\n"
                "   Set `sources:` in scripts/cap_config.yaml (or env CAP_SOURCES).\n"
                f"   Default fallback missing: {default}"
            )

    # Dedup while preserving order.
    uniq: list[Path] = []
    seen: set[str] = set()
    for p in sources:
        k = str(p)
        if k not in seen:
            seen.add(k)
            uniq.append(p)
    sources = uniq

    state_file = _expand_path_from(skill_dir, state_raw or "share/state.json")

    auth_team_dir: Path | None = None
    if auth_team_dir_raw:
        auth_team_dir = _expand_path_from(skill_dir, auth_team_dir_raw)

    auth_team_glob = auth_team_glob.strip() or "*"
    return _Config(
        sources=sources,
        strategy=strategy,
        state_file=state_file,
        auth_team_dir=auth_team_dir,
        auth_team_glob=auth_team_glob,
        auth_strategy=auth_strategy,
    )


def _lock_path(state_file: Path) -> Path:
    return state_file.with_suffix(state_file.suffix + ".lock")


def _read_state(path: Path) -> dict[str, object]:
    try:
        raw = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return {}
    except OSError:
        return {}
    try:
        data = json.loads(raw)
        return data if isinstance(data, dict) else {}
    except json.JSONDecodeError:
        return {}


def _write_state_atomic(path: Path, data: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    tmp.replace(path)


def _b64url_decode(s: str) -> bytes:
    raw = s.encode("utf-8")
    pad = b"=" * ((4 - (len(raw) % 4)) % 4)
    return base64.urlsafe_b64decode(raw + pad)


def _jwt_payload(token: str) -> dict[str, object] | None:
    parts = token.split(".")
    if len(parts) < 2:
        return None
    try:
        payload = _b64url_decode(parts[1]).decode("utf-8", errors="replace")
        data = json.loads(payload)
        return data if isinstance(data, dict) else None
    except Exception:
        return None


def _auth_meta(path: Path) -> dict[str, str]:
    try:
        raw = path.read_text(encoding="utf-8")
        data = json.loads(raw)
    except Exception:
        return {}
    if not isinstance(data, dict):
        return {}

    out: dict[str, str] = {}

    api_key = data.get("OPENAI_API_KEY")
    if isinstance(api_key, str) and api_key.strip():
        out["auth_type"] = "api_key"
        return out

    tokens = data.get("tokens")
    if not isinstance(tokens, dict):
        return out

    account_id = tokens.get("account_id")
    if isinstance(account_id, str) and account_id.strip():
        out["account_id"] = account_id.strip()

    id_token = tokens.get("id_token")
    if not isinstance(id_token, str) or not id_token.strip():
        return out

    payload = _jwt_payload(id_token)
    if not payload:
        return out

    email = payload.get("email")
    if isinstance(email, str) and email.strip():
        out["email"] = email.strip()

    auth = payload.get("https://api.openai.com/auth")
    if isinstance(auth, dict):
        plan = auth.get("chatgpt_plan_type")
        if isinstance(plan, str) and plan.strip():
            out["plan"] = plan.strip()

    return out


def _pick_round_robin(*, cfg: _Config) -> Path:
    lock_path = _lock_path(cfg.state_file)
    lock_path.parent.mkdir(parents=True, exist_ok=True)

    with lock_path.open("w", encoding="utf-8") as f:
        try:
            import fcntl

            fcntl.flock(f, fcntl.LOCK_EX)
        except Exception:
            pass

        state = _read_state(cfg.state_file)
        counter = state.get("counter", 0)
        try:
            counter_i = int(counter) if counter is not None else 0
        except Exception:
            counter_i = 0

        idx = counter_i % len(cfg.sources)
        counter_i += 1

        state["counter"] = counter_i
        state["updated_at"] = _now()
        _write_state_atomic(cfg.state_file, state)

        try:
            import fcntl

            fcntl.flock(f, fcntl.LOCK_UN)
        except Exception:
            pass

    return cfg.sources[idx]


def _pick_hash(*, cfg: _Config, worker: str) -> Path:
    h = hashlib.sha256(worker.encode("utf-8")).digest()
    n = int.from_bytes(h[:8], "big")
    idx = n % len(cfg.sources)
    return cfg.sources[idx]

def _sync_codex_home(src_root: Path, dst_root: Path) -> None:
    # Minimal copy of a CODEX_HOME template, excluding worker-local roots.
    exclude = {"sessions", "log", "history.jsonl"}
    src_root = src_root.expanduser()
    dst_root = dst_root.expanduser()
    if not src_root.is_dir():
        raise SystemExit(f"❌ source CODEX_HOME not found: {src_root}")
    dst_root.mkdir(parents=True, exist_ok=True)

    def safe_unlink(path: Path) -> None:
        try:
            if path.is_symlink() or path.is_file():
                path.unlink()
            else:
                shutil.rmtree(path)
        except FileNotFoundError:
            return

    def is_same_filetype(a: Path, b: Path) -> bool:
        try:
            if a.is_symlink() or b.is_symlink():
                return a.is_symlink() and b.is_symlink()
            if a.is_dir() and b.is_dir():
                return True
            if a.is_file() and b.is_file():
                return True
        except OSError:
            return False
        return False

    def sync_entry(src: Path, dst: Path) -> None:
        if dst.exists() and not is_same_filetype(src, dst):
            safe_unlink(dst)

        if src.is_symlink():
            try:
                target = os.readlink(src)
            except OSError:
                return
            if dst.exists():
                safe_unlink(dst)
            dst.symlink_to(target)
            return

        if src.is_dir():
            sync_dir(src, dst)
            return

        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)

    def sync_dir(src_dir: Path, dst_dir: Path) -> None:
        dst_dir.mkdir(parents=True, exist_ok=True)
        try:
            src_children = {p.name: p for p in src_dir.iterdir()}
        except OSError:
            return

        for name, src_child in src_children.items():
            sync_entry(src_child, dst_dir / name)

        try:
            for dst_child in dst_dir.iterdir():
                if dst_child.name not in src_children:
                    safe_unlink(dst_child)
        except OSError:
            return

    try:
        src_entries = {p.name: p for p in src_root.iterdir() if p.name not in exclude}
    except OSError as exc:
        raise SystemExit(f"❌ failed to list source CODEX_HOME: {exc}") from exc

    for name, src_entry in src_entries.items():
        sync_entry(src_entry, dst_root / name)

    # Delete extras in dst, but preserve excluded root items (worker-local)
    try:
        for dst_entry in dst_root.iterdir():
            if dst_entry.name in exclude:
                continue
            if dst_entry.name not in src_entries:
                safe_unlink(dst_entry)
    except OSError:
        pass

    (dst_root / "sessions").mkdir(parents=True, exist_ok=True)
    (dst_root / "log").mkdir(parents=True, exist_ok=True)


def _auth_candidates(cfg: _Config) -> list[Path]:
    if cfg.auth_team_dir is None:
        raise SystemExit(
            "❌ AUTH_TEAM directory is required for auth balancing.\n"
            "   Set `auth_team_dir:` in codex-account-pool/scripts/cap_config.yaml,\n"
            "   or export CAP_AUTH_TEAM_DIR=/abs/path/to/AUTH_TEAM (or AUTH_TEAM_DIR=...)."
        )
    if not cfg.auth_team_dir.is_dir():
        raise SystemExit(f"❌ auth_team_dir not found: {cfg.auth_team_dir}")

    pattern = cfg.auth_team_glob.strip() or "*"
    out: list[Path] = []
    state_file = cfg.state_file.resolve()
    try:
        for p in cfg.auth_team_dir.glob(pattern):
            try:
                if not p.is_file():
                    continue
            except OSError:
                continue
            try:
                if p.resolve() == state_file:
                    continue
            except OSError:
                pass
            if p.name.endswith(".lock") or p.name.endswith(".tmp"):
                continue
            if p.name in {".DS_Store"}:
                continue
            out.append(p.resolve())
    except OSError:
        pass

    if not out:
        raise SystemExit(f"❌ no auth candidates found under {cfg.auth_team_dir} (glob={pattern!r})")
    out.sort(key=lambda p: str(p))
    return out


def _cfg_with_auth_team_override(*, cfg: _Config, team_dir: Path | None, glob: str | None) -> _Config:
    return _Config(
        sources=cfg.sources,
        strategy=cfg.strategy,
        state_file=cfg.state_file,
        auth_team_dir=team_dir if team_dir is not None else cfg.auth_team_dir,
        auth_team_glob=(glob.strip() if isinstance(glob, str) and glob.strip() else cfg.auth_team_glob),
        auth_strategy=cfg.auth_strategy,
    )


def _pick_auth_balanced(*, cfg: _Config) -> Path:
    candidates = _auth_candidates(cfg)

    lock_path = _lock_path(cfg.state_file)
    lock_path.parent.mkdir(parents=True, exist_ok=True)

    with lock_path.open("w", encoding="utf-8") as f:
        try:
            import fcntl

            fcntl.flock(f, fcntl.LOCK_EX)
        except Exception:
            pass

        state = _read_state(cfg.state_file)
        raw_counts = state.get("auth_counts")
        counts_in: dict[str, int] = {}
        if isinstance(raw_counts, dict):
            for k, v in raw_counts.items():
                if not isinstance(k, str) or not k.strip():
                    continue
                try:
                    counts_in[k] = int(v) if v is not None else 0
                except Exception:
                    counts_in[k] = 0

        # Prune + normalize to current candidates only.
        counts: dict[str, int] = {}
        for p in candidates:
            key = str(p)
            counts[key] = max(0, counts_in.get(key, 0))

        min_count = min(counts.values())
        least_used = [p for p in candidates if counts[str(p)] == min_count]
        picked = secrets.choice(least_used)

        counts[str(picked)] = counts[str(picked)] + 1
        state["auth_counts"] = counts
        state["updated_at"] = _now()
        state["auth_updated_at"] = state["updated_at"]
        _write_state_atomic(cfg.state_file, state)

        try:
            import fcntl

            fcntl.flock(f, fcntl.LOCK_UN)
        except Exception:
            pass

    return picked


def _auth_key(path: Path) -> str:
    return str(path.resolve())


def _coerce_int(value: object, *, default: int = 0) -> int:
    try:
        return int(value) if value is not None else int(default)
    except Exception:
        return int(default)


def _sync_auth_order(*, state: dict[str, object], candidates: list[Path]) -> tuple[dict[str, int], list[Path]]:
    raw = state.get("auth_order")
    order_in: dict[str, int] = {}
    if isinstance(raw, dict):
        for k, v in raw.items():
            if not isinstance(k, str) or not k.strip():
                continue
            order_in[k] = max(0, _coerce_int(v, default=0))

    # Prune to current candidates and add missing candidates with new order ids.
    order: dict[str, int] = {}
    cand_keys = {_auth_key(p): p for p in candidates}
    for k in cand_keys:
        if k in order_in:
            order[k] = order_in[k]

    max_order = max(order.values(), default=0)
    for k in sorted(cand_keys.keys()):
        if k in order:
            continue
        max_order += 1
        order[k] = max_order

    ordered = sorted(candidates, key=lambda p: (order.get(_auth_key(p), 0), _auth_key(p)))
    state["auth_order"] = order
    state["auth_order_updated_at"] = _now()
    return order, ordered


def _pick_auth_team_cycle(*, cfg: _Config) -> Path:
    candidates = _auth_candidates(cfg)

    lock_path = _lock_path(cfg.state_file)
    lock_path.parent.mkdir(parents=True, exist_ok=True)

    with lock_path.open("w", encoding="utf-8") as f:
        try:
            import fcntl

            fcntl.flock(f, fcntl.LOCK_EX)
        except Exception:
            pass

        state = _read_state(cfg.state_file)
        _order, ordered = _sync_auth_order(state=state, candidates=candidates)

        current_raw = state.get("auth_current")
        current = current_raw.strip() if isinstance(current_raw, str) else ""
        if not current or not any(_auth_key(p) == current for p in ordered):
            current = _auth_key(ordered[0])
            state["auth_current"] = current
            state["auth_switched_at"] = _now()

        state["updated_at"] = _now()
        _write_state_atomic(cfg.state_file, state)

        try:
            import fcntl

            fcntl.flock(f, fcntl.LOCK_UN)
        except Exception:
            pass

    for p in ordered:
        if _auth_key(p) == current:
            return p
    # Fallback (should not happen).
    return ordered[0]


def _advance_auth_team_cycle(*, cfg: _Config) -> tuple[Path, Path]:
    candidates = _auth_candidates(cfg)

    lock_path = _lock_path(cfg.state_file)
    lock_path.parent.mkdir(parents=True, exist_ok=True)

    with lock_path.open("w", encoding="utf-8") as f:
        try:
            import fcntl

            fcntl.flock(f, fcntl.LOCK_EX)
        except Exception:
            pass

        state = _read_state(cfg.state_file)
        _order, ordered = _sync_auth_order(state=state, candidates=candidates)

        current_raw = state.get("auth_current")
        current = current_raw.strip() if isinstance(current_raw, str) else ""
        if not current or not any(_auth_key(p) == current for p in ordered):
            current = _auth_key(ordered[0])

        idx = 0
        for i, p in enumerate(ordered):
            if _auth_key(p) == current:
                idx = i
                break

        prev = ordered[idx]
        nxt = ordered[(idx + 1) % len(ordered)]

        state["auth_current"] = _auth_key(nxt)
        state["auth_switched_at"] = _now()
        state["updated_at"] = state["auth_switched_at"]
        _write_state_atomic(cfg.state_file, state)

        try:
            import fcntl

            fcntl.flock(f, fcntl.LOCK_UN)
        except Exception:
            pass

    return prev, nxt


def _dotted_path_segment(name: str) -> str | None:
    # Codex's `-c key=value` dotted-path parser does NOT support quoted segments.
    # That means keys that contain "." cannot be addressed safely.
    # Hyphens (e.g. fetch-md) are OK.
    if not name:
        return None
    if "." in name or "=" in name:
        return None
    if any(ch.isspace() for ch in name):
        return None
    return name


def _detect_mcp_server_names() -> list[str]:
    try:
        res = subprocess.run(
            ["codex", "mcp", "list"],
            check=False,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except FileNotFoundError:
        return []

    if res.returncode != 0 or not res.stdout.strip():
        return []

    lines = res.stdout.splitlines()
    names: list[str] = []
    for line in lines:
        s = line.strip()
        if not s:
            continue
        if s.startswith("Name ") or s.startswith("Name\t"):
            continue
        if set(s) <= {"-"}:
            continue
        # Expect first column is name.
        parts = s.split()
        if not parts:
            continue
        name = parts[0].strip()
        if name and name != "Name":
            names.append(name)

    # Dedup preserving order.
    out: list[str] = []
    seen: set[str] = set()
    for n in names:
        if n not in seen:
            seen.add(n)
            out.append(n)
    return out


def _build_codex_cmd_args() -> list[str]:
    # For `cap status`, we want startup to be as close to a normal user
    # invocation as possible. MCP is disabled by editing the temporary
    # CODEX_HOME config.toml, not by passing many `-c ...` flags.
    return ["codex"]


def _strip_mcp_servers_from_config(config_path: Path) -> bool:
    try:
        raw = config_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return False
    except OSError:
        return False

    lines = raw.splitlines(keepends=True)
    out: list[str] = []
    changed = False

    skipping = False
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("[") and stripped.endswith("]"):
            # Section header like: [mcp_servers.fetch-md]
            header = stripped[1:-1].strip()
            if header == "mcp_servers" or header.startswith("mcp_servers."):
                skipping = True
                changed = True
                continue
            skipping = False
        if skipping:
            changed = True
            continue
        out.append(line)

    if not changed:
        return False

    try:
        config_path.write_text("".join(out), encoding="utf-8")
        return True
    except OSError:
        return False


def _tmux_has(session: str) -> bool:
    res = subprocess.run(["tmux", "has-session", "-t", session], check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return res.returncode == 0


def _tmux_kill(session: str) -> None:
    subprocess.run(["tmux", "kill-session", "-t", session], check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def _tmux_capture(target: str, *, lines: int = 200) -> str:
    start = f"-{max(50, lines)}"
    res = subprocess.run(
        ["tmux", "capture-pane", "-p", "-t", target, "-S", start],
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
    )
    return res.stdout or ""


def _tmux_send_keys(target: str, *keys: str) -> None:
    subprocess.run(
        ["tmux", "send-keys", "-t", target, *keys],
        check=False,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def _tmux_type_line(target: str, text: str) -> None:
    _tmux_send_keys(target, text)


def _tmux_press_enter(target: str) -> None:
    _tmux_send_keys(target, "Enter")


def _strip_status_line(line: str) -> str:
    s = line.strip()
    if s.startswith("│"):
        s = s[1:]
    if s.endswith("│"):
        s = s[:-1]
    return s.strip()


def _parse_status(text: str) -> dict[str, str]:
    out: dict[str, str] = {}
    for raw in text.splitlines():
        line = _strip_status_line(raw)
        if not line:
            continue
        for key in ("Model:", "Directory:", "Approval:", "Sandbox:", "Agents.md:", "Account:", "Session:", "5h limit:", "Weekly limit:", "Context window:"):
            if key in line:
                val = line.split(key, 1)[1].strip()
                out[key[:-1].lower().replace(" ", "_")] = val
                break
    return out


def _extract_status_block(text: str) -> str:
    # Best-effort: find the last rendered /status "usage/status" card box and return it.
    #
    # Important: do NOT match the startup banner box (it contains Model/Directory too).
    lines = text.splitlines()
    anchors = (
        "Token usage",
        "Weekly limit:",
        "5h limit:",
        "Context window:",
        "Visit https://chatgpt.com/codex/settings/usage",
        "Account:",
    )
    last_idx: int | None = None
    for i, raw in enumerate(lines):
        if any(a in raw for a in anchors):
            last_idx = i
    if last_idx is None:
        return ""

    # Expand to nearest box borders.
    top = last_idx
    while top > 0 and not (lines[top].lstrip().startswith("╭") or lines[top].lstrip().startswith("┌")):
        top -= 1
    bot = last_idx
    while bot < len(lines) - 1 and not (lines[bot].lstrip().startswith("╰") or lines[bot].lstrip().startswith("└")):
        bot += 1
    return "\n".join(lines[top : bot + 1]).strip()


def _extract_status_tail(text: str) -> str:
    # Return the output starting from the most recent "/status" invocation
    # (including the command line itself), so we can ignore the startup banner.
    lines = text.splitlines()
    last_idx: int | None = None
    for i, raw in enumerate(lines):
        if "/status" in raw:
            last_idx = i
    if last_idx is None:
        return ""
    return "\n".join(lines[last_idx:]).rstrip()


def _status_block_score(block: str) -> int:
    # Prefer "richer" cards that include limits/bars. This is used to pick the
    # best snapshot if the UI is updating while we poll.
    score = 0
    for needle in (
        "Visit https://chatgpt.com/codex/settings/usage",
        "Model:",
        "Directory:",
        "Approval:",
        "Sandbox:",
        "Agents.md:",
        "Account:",
        "Session:",
        "Context window:",
        "5h limit:",
        "Weekly limit:",
    ):
        if needle in block:
            score += 1
    # Penalize the placeholder.
    if "data not available yet" in block.lower():
        score -= 2
    return score


def _status_block_complete(block: str) -> bool:
    # The user wants the real limits lines (with "% left"), not the placeholder
    # "data not available yet" card that can appear briefly after startup.
    parsed = _parse_status(block)
    return _percent_left(parsed.get("5h_limit")) is not None and _percent_left(parsed.get("weekly_limit")) is not None


def _find_codex_exit_code(text: str) -> int | None:
    for raw in text.splitlines():
        s = raw.strip()
        if s.startswith("[CODEX_EXIT]"):
            tail = s.split("[CODEX_EXIT]", 1)[1].strip()
            try:
                return int(tail.split()[0])
            except Exception:
                return None
    return None


def _status_for_auth_file(
    *,
    cfg: _Config,
    auth_file: Path,
    timeout_s: float,
    pre_send_wait_s: float,
    enter_delay_s: float,
    disable_mcp: bool,
) -> tuple[dict[str, str], str, int | None]:
    auth_file = auth_file.resolve()
    if not auth_file.is_file():
        raise SystemExit(f"❌ auth file not found: {auth_file}")

    home_src = cfg.sources[0]
    codex_args = _build_codex_cmd_args()
    codex_cmd = " ".join(shlex.quote(a) for a in codex_args)

    with tempfile.TemporaryDirectory(prefix="cap-status-one-") as tmp:
        tmp_root = Path(tmp).resolve()
        home = tmp_root / "home"
        _sync_codex_home(home_src, home)
        if disable_mcp:
            _strip_mcp_servers_from_config(home / "config.toml")

        shutil.copy2(auth_file, home / "auth.json")
        try:
            os.chmod(home / "auth.json", 0o600)
        except OSError:
            pass
        # Ensure we don't carry a pinned auth selector from the template home.
        # If `.auth_current_name` points at a non-existent auth file inside this
        # temp CODEX_HOME, Codex may show incomplete /status info.
        try:
            (home / ".auth_current_name").unlink(missing_ok=True)  # py>=3.8
        except TypeError:
            try:
                if (home / ".auth_current_name").exists():
                    (home / ".auth_current_name").unlink()
            except OSError:
                pass
        except OSError:
            pass

        prefix_raw = os.environ.get("CAP_STATUS_SESSION_PREFIX", "").strip()
        if prefix_raw:
            safe_prefix = re.sub(r"[^a-zA-Z0-9_-]+", "-", prefix_raw).strip("-") or "cap-status"
            session = f"{safe_prefix[:80]}-status"
        else:
            session = f"cap-status-one-{os.getpid()}"
        target = f"{session}:0.0"
        try:
            if _tmux_has(session):
                _tmux_kill(session)

            inner = (
                f"export CODEX_HOME={shlex.quote(str(home))}; "
                f"{codex_cmd}; "
                'echo "[CODEX_EXIT] $?"; '
                "sleep 120"
            )
            launch = f"bash -lc {shlex.quote(inner)}"
            res = subprocess.run(["tmux", "new-session", "-d", "-s", session, "-c", str(Path.cwd()), launch], check=False)
            if res.returncode != 0:
                raise SystemExit("❌ failed to start tmux session for status (is tmux installed?)")

            time.sleep(float(pre_send_wait_s))
            _tmux_type_line(target, "/status")
            time.sleep(float(enter_delay_s))
            _tmux_press_enter(target)

            captured = ""
            best_block = ""
            best_tail = ""
            best_score = -10_000
            deadline = time.time() + float(timeout_s)
            while time.time() < deadline:
                captured = _tmux_capture(target, lines=900)
                tail_now = _extract_status_tail(captured)
                if tail_now.strip():
                    best_tail = tail_now

                block_now = _extract_status_block(tail_now)
                if block_now:
                    score = _status_block_score(block_now)
                    if score > best_score:
                        best_score = score
                        best_block = block_now
                    if _status_block_complete(block_now):
                        break
                if _find_codex_exit_code(captured) is not None:
                    break
                time.sleep(0.2)

            tail = best_tail or _extract_status_tail(captured)
            block = best_block or _extract_status_block(tail) or ""
            parsed = _parse_status(block or tail or captured)
            exit_code = _find_codex_exit_code(captured or "")

            _tmux_type_line(target, "/exit")
            _tmux_press_enter(target)
            time.sleep(0.5)
            return parsed, (block or "").strip(), exit_code
        finally:
            _tmux_kill(session)


_PCT_LEFT_RE = re.compile(r"(?P<pct>[0-9]{1,3})%\s*left", re.IGNORECASE)


def _percent_left(raw: str | None) -> int | None:
    if not raw:
        return None
    m = _PCT_LEFT_RE.search(raw)
    if not m:
        return None
    try:
        return max(0, min(100, int(m.group("pct"))))
    except Exception:
        return None


def _read_json_or_fail(path: Path) -> dict[str, object]:
    try:
        raw = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        raise SystemExit(f"❌ file not found: {path}")
    except OSError as exc:
        raise SystemExit(f"❌ failed to read: {path} ({exc})") from exc
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"❌ invalid JSON: {path} ({exc})") from exc
    return data if isinstance(data, dict) else {}


def _read_yaml_or_json(path: Path) -> dict[str, object]:
    try:
        raw = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return {}
    except OSError:
        return {}

    raw_s = raw.strip()
    if not raw_s:
        return {}

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
        return {}

    return {}


def _cfg_get(cfg: dict[str, object], path: tuple[str, ...]) -> object:
    cur: object = cfg
    for key in path:
        if not isinstance(cur, dict):
            return None
        cur = cur.get(key)
    return cur


def _cfg_get_str(cfg: dict[str, object], *paths: tuple[str, ...], default: str = "") -> str:
    for p in paths:
        v = _cfg_get(cfg, p)
        if isinstance(v, str) and v.strip():
            return v.strip()
    return default


def _resolve_registry_path(registry_raw: str | None) -> Path:
    if isinstance(registry_raw, str) and registry_raw.strip():
        return Path(os.path.expanduser(registry_raw.strip())).resolve()

    env_reg = os.environ.get("AITWF_REGISTRY", "").strip()
    if env_reg:
        return Path(os.path.expanduser(env_reg)).resolve()

    env_dir = os.environ.get("AITWF_DIR", "").strip()
    if env_dir:
        return (Path(os.path.expanduser(env_dir)).resolve() / "registry.json").resolve()

    # Best-effort auto-detect sibling ai-team-workflow install.
    skills_dir = _skill_dir().parent
    atwf_skill = skills_dir / "ai-team-workflow"
    cfg_path = atwf_skill / "scripts" / "atwf_config.yaml"
    cfg = _read_yaml_or_json(cfg_path) if cfg_path.is_file() else {}
    share_dir = _cfg_get_str(cfg, ("share", "dir"), ("share_dir",), default="")
    if share_dir:
        p = Path(os.path.expanduser(share_dir))
        team_dir = p if p.is_absolute() else (atwf_skill / p).resolve()
    else:
        team_dir = atwf_skill / "share"
    return (team_dir / "registry.json").resolve()


def _load_team_members(registry: Path) -> list[dict[str, str]]:
    data = _read_json_or_fail(registry)
    raw_members = data.get("members")
    if not isinstance(raw_members, list):
        return []

    out: list[dict[str, str]] = []
    for m in raw_members:
        if not isinstance(m, dict):
            continue
        full = str(m.get("full", "")).strip()
        state_file = str(m.get("state_file", "")).strip()
        if not full:
            continue
        out.append({"full": full, "state_file": state_file})
    return out


def _resolve_twf() -> Path:
    override = os.environ.get("CAP_TWF", "").strip()
    if override:
        p = Path(os.path.expanduser(override)).resolve()
        if p.is_file():
            return p
        raise SystemExit(f"❌ CAP_TWF points to missing file: {p}")

    skills_dir = _skill_dir().parent
    sibling = skills_dir / "tmux-workflow" / "scripts" / "twf"
    if sibling.is_file():
        return sibling

    global_path = Path.home() / ".codex" / "skills" / "tmux-workflow" / "scripts" / "twf"
    if global_path.is_file():
        return global_path

    raise SystemExit("❌ tmux-workflow not found (set CAP_TWF=/path/to/twf)")


def _run_twf(twf: Path, args: list[str], *, state_dir: Path | None) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    if state_dir is not None:
        env["TWF_STATE_DIR"] = str(state_dir)
    return subprocess.run(["bash", str(twf), *args], check=False, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env)


def _state_dir_from_members(members: list[dict[str, str]]) -> Path | None:
    for m in members:
        raw = (m.get("state_file") or "").strip()
        if not raw:
            continue
        p = Path(os.path.expanduser(raw)).resolve()
        if p.is_file():
            return p.parent
    return None


def _any_worker_limit_hit(members: list[dict[str, str]], *, needle: str) -> bool:
    needle = needle.strip()
    if not needle:
        return False

    for m in members:
        full = (m.get("full") or "").strip()
        raw_state = (m.get("state_file") or "").strip()
        if not full or not raw_state:
            continue
        state_path = Path(os.path.expanduser(raw_state)).resolve()
        if not state_path.is_file():
            continue
        try:
            state = _read_state(state_path)
        except Exception:
            state = {}
        target = (
            str(state.get("tmux_target") or "").strip()
            or str(state.get("tmux_session") or "").strip()
            or full
        )
        if not target:
            continue
        if not _tmux_has(full):
            continue
        captured = _tmux_capture(target, lines=900)
        if needle in captured:
            return True
    return False


def _restart_team(
    *,
    members: list[dict[str, str]],
    message: str,
) -> None:
    twf = _resolve_twf()
    state_dir = _state_dir_from_members(members)
    # Stop only currently running sessions; then resume them.
    running: list[str] = []
    for m in members:
        full = (m.get("full") or "").strip()
        if not full:
            continue
        if _tmux_has(full):
            running.append(full)

    for full in running:
        res = _run_twf(twf, ["stop", full], state_dir=state_dir)
        if res.returncode != 0:
            _eprint(res.stderr.strip() or res.stdout.strip() or f"⚠️ twf stop failed: {full}")

    for full in running:
        res = _run_twf(twf, ["resume", full, "--no-tree"], state_dir=state_dir)
        if res.returncode != 0:
            _eprint(res.stderr.strip() or res.stdout.strip() or f"⚠️ twf resume failed: {full}")
            continue
        res2 = _run_twf(twf, ["send", full, message], state_dir=state_dir)
        if res2.returncode != 0:
            _eprint(res2.stderr.strip() or res2.stdout.strip() or f"⚠️ twf send failed: {full}")


def cmd_watch_team(args: argparse.Namespace) -> int:
    cfg0 = _load_config()
    team_dir = Path(os.path.expanduser(args.team_dir)).resolve()
    glob_pat = (args.glob or "").strip() or cfg0.auth_team_glob
    # Force team_cycle semantics for the watcher (the whole purpose is to
    # watch+advance a single shared auth pointer).
    cfg = _Config(
        sources=cfg0.sources,
        strategy=cfg0.strategy,
        state_file=cfg0.state_file,
        auth_team_dir=team_dir,
        auth_team_glob=glob_pat,
        auth_strategy="team_cycle",
    )

    registry = _resolve_registry_path(getattr(args, "registry", None))
    pause_marker = registry.parent / ".paused"
    interval_s = float(getattr(args, "interval", 180.0))
    grace_s = float(getattr(args, "grace", 300.0))
    max_retries = int(getattr(args, "max_retries", 10) or 10)
    needle = str(getattr(args, "needle", "") or "You've hit your usage limit.")

    msg = str(getattr(args, "message", "") or "").strip()
    if not msg:
        msg = "Task continues. If you are waiting for a reply, please ignore this message."

    while True:
        if pause_marker.exists():
            _eprint(f"⏸️ team paused ({pause_marker}); skipping rotation check")
            if bool(getattr(args, "once", False)):
                return 0
            time.sleep(max(5.0, interval_s))
            continue

        members = _load_team_members(registry)
        if not members:
            _eprint(f"⚠️ no members found in registry: {registry}")
            if bool(getattr(args, "once", False)):
                return 1
            time.sleep(max(5.0, interval_s))
            continue

        current_auth = _pick_auth_team_cycle(cfg=cfg)

        parsed: dict[str, str] | None = None
        last_block = ""
        last_exit: int | None = None
        for attempt in range(1, max_retries + 1):
            parsed_try, block_try, exit_code = _status_for_auth_file(
                cfg=cfg,
                auth_file=current_auth,
                timeout_s=float(getattr(args, "status_timeout", 12.0)),
                pre_send_wait_s=float(getattr(args, "pre_send_wait", 5.0)),
                enter_delay_s=float(getattr(args, "enter_delay", 0.5)),
                disable_mcp=bool(getattr(args, "disable_mcp", True)),
            )
            last_block = block_try
            last_exit = exit_code
            pct_5h = _percent_left(parsed_try.get("5h_limit"))
            pct_week = _percent_left(parsed_try.get("weekly_limit"))
            if pct_5h is not None and pct_week is not None:
                parsed = parsed_try
                break
            time.sleep(0.5)

        if parsed is None:
            _eprint("⚠️ status did not return usable limit lines after retries; rotating auth")
            if grace_s > 0:
                _eprint(f"⏳ grace period: {int(grace_s)}s")
                time.sleep(grace_s)
            prev, nxt = _advance_auth_team_cycle(cfg=cfg)
            _eprint(f"🔁 auth rotated (status unavailable): {prev.name} -> {nxt.name}")
            _restart_team(members=members, message=msg)
        else:
            pct_5h = _percent_left(parsed.get("5h_limit"))
            pct_week = _percent_left(parsed.get("weekly_limit"))
            assert pct_5h is not None and pct_week is not None

            if pct_5h == 0 or pct_week == 0:
                if _any_worker_limit_hit(members, needle=needle):
                    _eprint(f"⚠️ usage limit hit (5h={pct_5h}% weekly={pct_week}%). Rotating after {int(grace_s)}s grace...")
                    if grace_s > 0:
                        time.sleep(grace_s)
                    prev, nxt = _advance_auth_team_cycle(cfg=cfg)
                    _eprint(f"🔁 auth rotated: {prev.name} -> {nxt.name}")
                    _restart_team(members=members, message=msg)
                else:
                    _eprint(f"ℹ️ limits show 0% left but no worker shows the limit banner; skipping rotation this round")

        if bool(getattr(args, "once", False)):
            return 0
        time.sleep(max(5.0, interval_s))


def cmd_status(args: argparse.Namespace) -> int:
    team_dir = Path(os.path.expanduser(args.team_dir)).resolve()
    if not team_dir.is_dir():
        raise SystemExit(f"❌ team dir not found: {team_dir}")

    glob_pat = (args.glob or "").strip() or "auth.json*"
    try:
        candidates = [p.resolve() for p in team_dir.glob(glob_pat) if p.is_file()]
    except OSError:
        candidates = []

    # Filter common junk.
    candidates = [p for p in candidates if not (p.name.endswith(".lock") or p.name.endswith(".tmp") or p.name == ".DS_Store")]
    candidates.sort(key=lambda p: p.name)
    if not candidates:
        raise SystemExit(f"❌ no auth files found under {team_dir} (glob={glob_pat!r})")

    cfg = _load_config()
    home_src = cfg.sources[0]
    state = _read_state(cfg.state_file)
    raw_counts = state.get("auth_counts")
    counts: dict[str, int] = {}
    if isinstance(raw_counts, dict):
        for k, v in raw_counts.items():
            if not isinstance(k, str) or not k.strip():
                continue
            try:
                counts[k] = int(v) if v is not None else 0
            except Exception:
                counts[k] = 0

    codex_args = _build_codex_cmd_args()
    codex_cmd = " ".join(shlex.quote(a) for a in codex_args)

    results: list[tuple[Path, dict[str, str], str, str, str, int | None]] = []

    with tempfile.TemporaryDirectory(prefix="cap-status-") as tmp:
        tmp_root = Path(tmp).resolve()
        home = tmp_root / "home"
        _sync_codex_home(home_src, home)
        if bool(args.disable_mcp):
            _strip_mcp_servers_from_config(home / "config.toml")

        for i, auth_file in enumerate(candidates, start=1):
            # Install selected auth into the temp home.
            shutil.copy2(auth_file, home / "auth.json")
            try:
                os.chmod(home / "auth.json", 0o600)
            except OSError:
                pass
            try:
                (home / ".auth_current_name").unlink(missing_ok=True)  # py>=3.8
            except TypeError:
                try:
                    if (home / ".auth_current_name").exists():
                        (home / ".auth_current_name").unlink()
                except OSError:
                    pass
            except OSError:
                pass

            session = f"cap-status-{os.getpid()}-{i}"
            target = f"{session}:0.0"
            try:
                if _tmux_has(session):
                    _tmux_kill(session)

                # Keep the tmux session alive even if Codex exits quickly, so we can
                # capture errors without the tmux server disappearing mid-loop.
                inner = (
                    f"export CODEX_HOME={shlex.quote(str(home))}; "
                    f"{codex_cmd}; "
                    'echo "[CODEX_EXIT] $?"; '
                    "sleep 3600"
                )
                launch = f"bash -lc {shlex.quote(inner)}"
                res = subprocess.run(["tmux", "new-session", "-d", "-s", session, "-c", str(Path.cwd()), launch], check=False)
                if res.returncode != 0:
                    raise SystemExit("❌ failed to start tmux session for status (is tmux installed?)")

                # Mimic a human: wait for UI to settle, type /status, wait a bit,
                # then press Enter.
                time.sleep(float(args.pre_send_wait))
                before = _tmux_capture(target, lines=500)
                _tmux_type_line(target, "/status")
                time.sleep(float(args.enter_delay))
                _tmux_press_enter(target)

                # Poll until we get the richest /status card we can.
                captured = ""
                best_block = ""
                best_tail = ""
                best_score = -10_000
                deadline = time.time() + float(args.timeout)
                while time.time() < deadline:
                    captured = _tmux_capture(target, lines=800)
                    tail_now = _extract_status_tail(captured)
                    if tail_now.strip():
                        best_tail = tail_now

                    block_now = _extract_status_block(tail_now)
                    if block_now:
                        score = _status_block_score(block_now)
                        if score > best_score:
                            best_score = score
                            best_block = block_now
                        if _status_block_complete(block_now):
                            break
                    if _find_codex_exit_code(captured) is not None:
                        break
                    time.sleep(0.2)

                # Prefer the best status card we saw; fall back to the /status tail.
                tail = best_tail or _extract_status_tail(captured)
                block = best_block or _extract_status_block(tail) or ""
                parsed = _parse_status(block or tail or captured)
                results.append((auth_file, parsed, block or "", tail or "", captured or "", _find_codex_exit_code(captured or "")))

                _tmux_type_line(target, "/exit")
                _tmux_press_enter(target)
                # Give Codex a moment to quit.
                time.sleep(0.5)
            finally:
                _tmux_kill(session)

    # Print results.
    for auth_file, parsed, block, tail, captured, exit_code in results:
        # Delimiter per auth (the status card itself does not include the auth file name).
        print(f"--- {auth_file.name} ---")
        if block.strip():
            print(block.rstrip())
        elif tail.strip():
            # Minimal /status output (e.g. "100% context left")
            print(tail.rstrip())
        elif args.print_raw and (captured or "").strip():
            print(captured.rstrip())
        else:
            print("(no /status output captured; increase --timeout / --pre-send-wait)")
        if exit_code is not None and exit_code != 0:
            print(f"[codex_exit={exit_code}]")
        print()

    return 0


def cmd_where(_: argparse.Namespace) -> int:
    cfg = _load_config()
    print(f"skill_dir:  {str(_skill_dir())}")
    print(f"config:     {str(_config_path())}")
    print(f"strategy:   {cfg.strategy}")
    print(f"auth_strategy: {cfg.auth_strategy}")
    print(f"state_file: {str(cfg.state_file)}")
    print(f"auth_team_dir: {str(cfg.auth_team_dir) if cfg.auth_team_dir else ''}")
    print(f"auth_team_glob: {cfg.auth_team_glob}")
    print("sources:")
    for p in cfg.sources:
        print(f"  - {p}")
    return 0


def cmd_list(_: argparse.Namespace) -> int:
    cfg = _load_config()
    for p in cfg.sources:
        print(str(p))
    return 0


def cmd_pick(args: argparse.Namespace) -> int:
    cfg = _load_config()
    worker = (args.worker or "").strip()
    base = (args.base or "").strip()
    if not worker:
        raise SystemExit("❌ --worker is required")
    if not base:
        raise SystemExit("❌ --base is required")

    if cfg.strategy == "round_robin":
        picked = _pick_round_robin(cfg=cfg)
    else:
        picked = _pick_hash(cfg=cfg, worker=worker)

    if os.environ.get("CAP_DEBUG", "").strip():
        _eprint(f"ℹ️ pick strategy={cfg.strategy} worker={worker} base={base} -> {picked}")
    print(str(picked))
    return 0

def cmd_pick_auth(args: argparse.Namespace) -> int:
    cfg = _load_config()
    worker = (args.worker or "").strip()
    base = (args.base or "").strip()
    if not worker:
        raise SystemExit("❌ --worker is required")
    if not base:
        raise SystemExit("❌ --base is required")

    if cfg.auth_strategy == "team_cycle":
        picked = _pick_auth_team_cycle(cfg=cfg)
    else:
        picked = _pick_auth_balanced(cfg=cfg)
    if os.environ.get("CAP_DEBUG", "").strip():
        _eprint(f"ℹ️ pick-auth strategy={cfg.auth_strategy} worker={worker} base={base} -> {picked}")
    print(str(picked))
    return 0


def cmd_auth_current(args: argparse.Namespace) -> int:
    cfg0 = _load_config()
    team_dir = Path(os.path.expanduser(args.team_dir)).resolve() if (args.team_dir or "").strip() else None
    glob = (args.glob or "").strip() or None
    cfg = _cfg_with_auth_team_override(cfg=cfg0, team_dir=team_dir, glob=glob)
    if cfg.auth_team_dir is None:
        raise SystemExit("❌ auth_team_dir is required (pass --team-dir or set it in cap_config.yaml)")
    picked = _pick_auth_team_cycle(cfg=cfg)
    print(str(picked))
    return 0


def cmd_auth_advance(args: argparse.Namespace) -> int:
    cfg0 = _load_config()
    team_dir = Path(os.path.expanduser(args.team_dir)).resolve() if (args.team_dir or "").strip() else None
    glob = (args.glob or "").strip() or None
    cfg = _cfg_with_auth_team_override(cfg=cfg0, team_dir=team_dir, glob=glob)
    if cfg.auth_team_dir is None:
        raise SystemExit("❌ auth_team_dir is required (pass --team-dir or set it in cap_config.yaml)")
    _prev, nxt = _advance_auth_team_cycle(cfg=cfg)
    print(str(nxt))
    return 0


def cmd_reset_state(_: argparse.Namespace) -> int:
    cfg = _load_config()
    lock_path = _lock_path(cfg.state_file)
    lock_path.parent.mkdir(parents=True, exist_ok=True)

    with lock_path.open("w", encoding="utf-8") as f:
        try:
            import fcntl

            fcntl.flock(f, fcntl.LOCK_EX)
        except Exception:
            pass

        ts = _now()
        # Preserve long-lived auth ordering/rotation state by default so `twf stop`
        # (which auto calls `cap reset-state`) doesn't destroy team rotation order.
        prev = _read_state(cfg.state_file)
        state: dict[str, object] = {}
        for k in ("auth_order", "auth_current", "auth_order_updated_at", "auth_switched_at"):
            if k in prev:
                state[k] = prev[k]
        state["reset_at"] = ts
        state["updated_at"] = ts
        _write_state_atomic(cfg.state_file, state)

        try:
            import fcntl

            fcntl.flock(f, fcntl.LOCK_UN)
        except Exception:
            pass

    print(str(cfg.state_file))
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="cap", add_help=True)
    sub = p.add_subparsers(dest="cmd", required=True)

    sub.add_parser("where", help="print resolved config + sources")
    sub.add_parser("list", help="list source directories (one per line)")

    pick = sub.add_parser("pick", help="pick a CODEX_HOME source directory for a worker")
    pick.add_argument("--worker", required=True)
    pick.add_argument("--base", required=True)

    pick_auth = sub.add_parser("pick-auth", help="pick an auth file from AUTH_TEAM (balanced by least-used)")
    pick_auth.add_argument("--worker", required=True)
    pick_auth.add_argument("--base", required=True)

    auth_cur = sub.add_parser("auth-current", help="print current team auth (team_cycle ordering)")
    auth_cur.add_argument("--team-dir", default="", help="AUTH_TEAM dir override (default: config/env)")
    auth_cur.add_argument("--glob", default="", help="auth glob override (default: config/env)")

    auth_adv = sub.add_parser("auth-advance", help="advance to next team auth (team_cycle ordering)")
    auth_adv.add_argument("--team-dir", default="", help="AUTH_TEAM dir override (default: config/env)")
    auth_adv.add_argument("--glob", default="", help="auth glob override (default: config/env)")

    sub.add_parser("reset-state", help="reset the state file (auth/home counters)")

    watch = sub.add_parser("watch-team", help="watch usage for current auth and rotate whole team when limits are hit")
    watch.add_argument("team_dir", help="AUTH_TEAM directory containing auth files")
    watch.add_argument("--glob", default="auth.json*", help="file glob inside team_dir (default: auth.json*)")
    watch.add_argument("--registry", default="", help="ai-team registry.json path (default: auto-detect / env AITWF_*)")
    watch.add_argument("--interval", type=float, default=180.0, help="seconds between checks (default: 180)")
    watch.add_argument("--grace", type=float, default=300.0, help="seconds to wait before rotating (default: 300)")
    watch.add_argument("--max-retries", type=int, default=10, help="max status retries before rotating (default: 10)")
    watch.add_argument("--needle", default="You've hit your usage limit.", help="banner text to confirm a worker hit the limit")
    watch.add_argument("--message", default="", help="message to send after resume (English)")
    watch.add_argument("--once", action="store_true", help="run one check and exit")
    watch.add_argument("--status-timeout", type=float, default=12.0, help="seconds to wait for /status (default: 12)")
    watch.add_argument("--pre-send-wait", type=float, default=5.0, help="seconds to wait before typing /status (default: 5.0)")
    watch.add_argument("--enter-delay", type=float, default=0.5, help="seconds to wait before pressing Enter (default: 0.5)")
    watch.add_argument(
        "--disable-mcp",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="disable all MCP servers for faster startup by stripping mcp_servers from temp config.toml (default: enabled)",
    )

    status = sub.add_parser("status", help="inspect /status for every auth file under a team dir (tmux required)")
    status.add_argument("team_dir", help="AUTH_TEAM directory containing auth files (names unrestricted)")
    status.add_argument("--glob", default="", help="file glob inside team_dir (default: auth.json*)")
    status.add_argument("--timeout", default="12", help="seconds to wait per account (default: 12)")
    status.add_argument("--pre-send-wait", default="5.0", help="seconds to wait after starting Codex before typing /status (default: 5.0)")
    status.add_argument("--enter-delay", default="0.5", help="seconds to wait after typing /status before pressing Enter (default: 0.5)")
    status.add_argument(
        "--disable-mcp",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="disable all MCP servers for faster startup by stripping mcp_servers from temp config.toml (default: enabled)",
    )
    status.add_argument("--print-raw", action="store_true", help="also print the raw /status box for each account")
    return p


def main(argv: list[str]) -> int:
    p = build_parser()
    args = p.parse_args(argv)
    if args.cmd == "where":
        return cmd_where(args)
    if args.cmd == "list":
        return cmd_list(args)
    if args.cmd == "pick":
        return cmd_pick(args)
    if args.cmd == "pick-auth":
        return cmd_pick_auth(args)
    if args.cmd == "auth-current":
        return cmd_auth_current(args)
    if args.cmd == "auth-advance":
        return cmd_auth_advance(args)
    if args.cmd == "reset-state":
        return cmd_reset_state(args)
    if args.cmd == "watch-team":
        return cmd_watch_team(args)
    if args.cmd == "status":
        return cmd_status(args)
    raise SystemExit("unreachable")


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
