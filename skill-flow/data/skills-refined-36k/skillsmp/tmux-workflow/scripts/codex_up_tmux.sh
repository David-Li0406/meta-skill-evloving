#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

usage() {
  cat <<'USAGE' >&2
Usage:
  codex_up_tmux.sh [--session NAME] [--session-file PATH] [--cmd "codex ..."] [--attach]

Defaults:
  - session-file: ./.codex-tmux-session.json
  - session name: codex-<sha1(realpath(cwd))[:10]>
  - cmd:         codex -c disable_paste_burst=true --sandbox danger-full-access -m <model> --config model_reasoning_effort="<effort>"

Environment:
  TWF_SESSION_FILE      Override session file path
  TWF_TMUX_SESSION      Override tmux session name
  TWF_CODEX_CMD         Override codex command
  TWF_CODEX_PROFILE     Optional codex profile (adds `-p <profile>`)
  TWF_CODEX_CMD_CONFIG  Override YAML config path (default: scripts/twf_config.yaml)
  TWF_WORKERS_DIR       Per-worker CODEX_HOME base dir (default: ~/.codex-workers)
  TWF_CODEX_HOME_SRC    Source CODEX_HOME to copy from (default: ~/.codex)
  TWF_AUTH_SRC          Optional auth file to copy into worker as `auth.json` (overrides synced auth.json)
USAGE
}

config_file="${TWF_CODEX_CMD_CONFIG:-$script_dir/twf_config.yaml}"
if [[ -z "${TWF_CODEX_CMD_CONFIG:-}" && ! -f "$config_file" && -f "$script_dir/twf_config.json" ]]; then
  config_file="$script_dir/twf_config.json"
fi

build_default_codex_cmd() {
  python3 - "$config_file" <<'PY'
import json
import shlex
import sys
from pathlib import Path

cfg_path = Path(sys.argv[1]).expanduser()
raw = ""
try:
    if cfg_path.exists():
        raw = cfg_path.read_text(encoding="utf-8")
except Exception:
    raw = ""

def parse_yaml(text: str) -> dict:
    out: dict[str, str] = {}
    for line in text.splitlines():
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
            # strip inline comment (only when it starts a token)
            for i, ch in enumerate(value):
                if ch == "#" and (i == 0 or value[i - 1].isspace()):
                    value = value[:i].strip()
                    break
        out[key] = value.strip()
    return out

def load_cfg(text: str) -> dict:
    raw_s = text.strip()
    if not raw_s:
        return {}

    if raw_s.startswith("{"):
        try:
            data = json.loads(raw_s)
        except Exception:
            data = None
        if isinstance(data, dict):
            return data

    try:
        import yaml  # type: ignore

        data = yaml.safe_load(text)
        if isinstance(data, dict):
            return data
    except Exception:
        pass

    return parse_yaml(text)

cfg = load_cfg(raw)

def get_path(data: dict, path: list[str]):
    cur = data
    for k in path:
        if not isinstance(cur, dict):
            return None
        cur = cur.get(k)
    return cur

def get_str(*paths: list[str], default: str = "") -> str:
    for p in paths:
        v = get_path(cfg, p)
        if isinstance(v, str):
            return v.strip()
    return default

model = get_str(["codex", "model"], ["model"], default="gpt-5.2")
effort = get_str(["codex", "model_reasoning_effort"], ["model_reasoning_effort"], default="xhigh")

model = model.strip()
effort = effort.strip()

args: list[str] = [
    "codex",
    "-c",
    "disable_paste_burst=true",
    "--sandbox",
    "danger-full-access",
]

if model:
    args.extend(["-m", model])
if effort:
    args.extend(["--config", f'model_reasoning_effort="{effort}"'])

print(" ".join(shlex.quote(a) for a in args))
PY
}

session_file="${TWF_SESSION_FILE:-.codex-tmux-session.json}"
tmux_session="${TWF_TMUX_SESSION:-}"
codex_cmd="${TWF_CODEX_CMD:-}"
attach=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    --session|-s)
      tmux_session="${2:-}"; shift 2 ;;
    --session-file|-f)
      session_file="${2:-}"; shift 2 ;;
    --cmd)
      codex_cmd="${2:-}"; shift 2 ;;
    --attach)
      attach=1; shift ;;
    -h|--help)
      usage; exit 0 ;;
    *)
      echo "Unknown arg: $1" >&2
      usage
      exit 1 ;;
  esac
done

if [[ -z "$codex_cmd" ]]; then
  codex_cmd="$(build_default_codex_cmd)"
fi

profile="${TWF_CODEX_PROFILE:-}"
if [[ -n "$profile" ]]; then
  codex_cmd="$(python3 - "$profile" "$codex_cmd" <<'PY'
import shlex
import sys

profile = sys.argv[1].strip()
cmd = sys.argv[2]

try:
    parts = shlex.split(cmd)
except Exception:
    print(cmd)
    raise SystemExit(0)

if not parts or parts[0] != "codex":
    print(cmd)
    raise SystemExit(0)

if "-p" in parts or "--profile" in parts:
    print(cmd)
    raise SystemExit(0)

parts = [parts[0], "-p", profile] + parts[1:]
print(" ".join(shlex.quote(p) for p in parts))
PY
)"
fi

work_dir="$PWD"
work_dir_norm="$(python3 -c 'import os,sys; print(os.path.realpath(sys.argv[1]))' "$work_dir")"

if [[ -z "$tmux_session" ]]; then
  hash="$(python3 -c 'import hashlib,sys; print(hashlib.sha1(sys.argv[1].encode()).hexdigest()[:10])' "$work_dir_norm")"
  tmux_session="codex-$hash"
fi

# Per-worker CODEX_HOME isolation: ~/.codex-workers/<worker_id>
worker_id="$tmux_session"
codex_workers_dir="${TWF_WORKERS_DIR:-$HOME/.codex-workers}"
codex_home_src="${TWF_CODEX_HOME_SRC:-$HOME/.codex}"
auth_src="${TWF_AUTH_SRC:-}"
worker_home="$codex_workers_dir/$worker_id"
worker_sessions_root="$worker_home/sessions"

echo "🔧 Syncing CODEX_HOME -> $worker_home (excluding sessions/log/history.jsonl)" >&2
python3 "$script_dir/sync_codex_home.py" --src "$codex_home_src" --dst "$worker_home"

if [[ -n "$auth_src" ]]; then
  if [[ ! -f "$auth_src" ]]; then
    echo "❌ TWF_AUTH_SRC not found (expected file): $auth_src" >&2
    exit 1
  fi
  cp -f "$auth_src" "$worker_home/auth.json"
  chmod 600 "$worker_home/auth.json" >/dev/null 2>&1 || true
  # Ensure we don't carry a pinned auth selector from the template.
  rm -f "$worker_home/.auth_current_name" >/dev/null 2>&1 || true
fi

tmux_target="${tmux_session}:0.0"

if tmux has-session -t "$tmux_session" >/dev/null 2>&1; then
  echo "ℹ️  Reusing tmux session: $tmux_session" >&2
else
  echo "🚀 Starting tmux session: $tmux_session" >&2
  quoted_worker_home="$(python3 -c 'import shlex,sys; print(shlex.quote(sys.argv[1]))' "$worker_home")"
  tmux new-session -d -s "$tmux_session" -c "$work_dir" "env CODEX_HOME=$quoted_worker_home $codex_cmd"
fi

tmux set-environment -t "$tmux_session" CODEX_HOME "$worker_home" >/dev/null 2>&1 || true

pane_id="$(tmux display-message -p -t "$tmux_target" '#{pane_id}' 2>/dev/null || true)"

python3 - "$session_file" "$tmux_session" "$tmux_target" "$pane_id" "$work_dir" "$work_dir_norm" "$codex_cmd" "$worker_id" "$worker_home" "$worker_sessions_root" "$codex_home_src" "$auth_src" <<'PY'
import json
import sys
from datetime import datetime
from pathlib import Path

session_file = Path(sys.argv[1]).expanduser()
tmux_session = sys.argv[2]
tmux_target = sys.argv[3]
pane_id = sys.argv[4] or None
work_dir = sys.argv[5]
work_dir_norm = sys.argv[6]
codex_cmd = sys.argv[7]
worker_id = sys.argv[8]
codex_home = sys.argv[9]
sessions_root = sys.argv[10]
codex_home_src = sys.argv[11]
auth_src = sys.argv[12] or ""

def load_json(path: Path) -> dict:
    try:
        if path.exists():
            with path.open("r", encoding="utf-8-sig") as f:
                data = json.load(f)
            if isinstance(data, dict):
                return data
    except Exception:
        pass
    return {}

def scan_latest_log(root: Path):
    if not root.exists():
        return None
    latest = None
    latest_mtime = -1.0
    for p in root.glob("**/*.jsonl"):
        if not p.is_file():
            continue
        try:
            mtime = p.stat().st_mtime
        except OSError:
            continue
        if mtime >= latest_mtime:
            latest = p
            latest_mtime = mtime
    return latest

def read_session_id(log_path: Path):
    try:
        with log_path.open("r", encoding="utf-8", errors="ignore") as f:
            head = f.readline().strip()
    except OSError:
        return None
    if not head:
        return None
    try:
        entry = json.loads(head)
    except Exception:
        return None
    if not isinstance(entry, dict) or entry.get("type") != "session_meta":
        return None
    payload = entry.get("payload") or {}
    if not isinstance(payload, dict):
        return None
    sid = payload.get("id")
    return sid if isinstance(sid, str) else None

data = load_json(session_file)

data.update(
    {
        "terminal": "tmux",
        "tmux_session": tmux_session,
        "tmux_target": tmux_target,
        "pane_id": pane_id,
        "work_dir": work_dir,
        "work_dir_norm": work_dir_norm,
        "worker_id": worker_id,
        "codex_home": codex_home,
        "codex_home_src": codex_home_src,
        "auth_src": auth_src,
        "codex_session_root": sessions_root,
        "active": True,
        "started_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "codex_start_cmd": codex_cmd,
    }
)

latest = scan_latest_log(Path(sessions_root))
if latest:
    data["codex_session_path"] = str(latest)
    sid = read_session_id(latest)
    if sid:
        data["codex_session_id"] = sid
        data["codex_current_id"] = sid
        data["codex_resume_from_id"] = sid

tmp = session_file.with_suffix(session_file.suffix + ".tmp")
tmp.parent.mkdir(parents=True, exist_ok=True)
tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
tmp.replace(session_file)
print(json.dumps({"tmux_session": data["tmux_session"], "tmux_target": data["tmux_target"]}))
PY

if [[ "$attach" -eq 1 ]]; then
  tmux attach -t "$tmux_session"
fi
