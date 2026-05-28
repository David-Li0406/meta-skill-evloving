#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import sys
from collections import deque
from pathlib import Path
from typing import Any, Deque, Dict, Iterable, Optional, Tuple


EXIT_OK = 0
EXIT_ERROR = 1
EXIT_NO_REPLY = 2


def eprint(*args: object) -> None:
    print(*args, file=sys.stderr)


def _realpath(path: Path) -> str:
    return str(path.expanduser().resolve())


def _sessions_root() -> Path:
    if os.environ.get("TWF_CODEX_SESSION_ROOT"):
        return Path(os.environ["TWF_CODEX_SESSION_ROOT"]).expanduser()
    if os.environ.get("CODEX_SESSION_ROOT"):
        return Path(os.environ["CODEX_SESSION_ROOT"]).expanduser()
    if os.environ.get("CODEX_HOME"):
        return Path(os.environ["CODEX_HOME"]).expanduser() / "sessions"
    return Path.home() / ".codex" / "sessions"


def _sessions_root_for_session(session: Dict[str, Any]) -> Path:
    value = session.get("codex_session_root")
    if isinstance(value, str) and value.strip():
        return Path(value).expanduser()

    codex_home = session.get("codex_home")
    if isinstance(codex_home, str) and codex_home.strip():
        return Path(codex_home).expanduser() / "sessions"

    return _sessions_root()


def _load_json(path: Path) -> Dict[str, Any]:
    try:
        with path.open("r", encoding="utf-8-sig") as f:
            data = json.load(f)
        return data if isinstance(data, dict) else {}
    except Exception:
        return {}


def _read_first_lines(path: Path, limit: int = 50) -> Iterable[Dict[str, Any]]:
    try:
        with path.open("r", encoding="utf-8", errors="ignore") as f:
            for _ in range(limit):
                line = f.readline()
                if not line:
                    break
                line = line.strip()
                if not line:
                    continue
                try:
                    entry = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if isinstance(entry, dict):
                    yield entry
    except OSError:
        return


def _extract_session_cwd(entry: Dict[str, Any]) -> Optional[str]:
    if entry.get("type") != "session_meta":
        return None
    payload = entry.get("payload") or {}
    if not isinstance(payload, dict):
        return None
    cwd = payload.get("cwd")
    return cwd if isinstance(cwd, str) else None


def _find_log_for_cwd(expected_cwd_norm: str) -> Optional[Path]:
    root = _sessions_root()
    if not root.exists():
        return None

    best: Optional[Path] = None
    best_mtime = -1.0

    for path in root.glob("**/*.jsonl"):
        if not path.is_file():
            continue
        try:
            mtime = path.stat().st_mtime
        except OSError:
            continue
        if mtime < best_mtime:
            continue

        found_cwd = None
        for entry in _read_first_lines(path, limit=5):
            cwd = _extract_session_cwd(entry)
            if cwd:
                found_cwd = cwd
                break
        if not found_cwd:
            continue

        try:
            found_norm = _realpath(Path(found_cwd))
        except Exception:
            found_norm = found_cwd
        if found_norm != expected_cwd_norm:
            continue

        best = path
        best_mtime = mtime

    return best


def _scan_latest_log(root: Path) -> Optional[Path]:
    if not root.exists():
        return None

    latest: Optional[Path] = None
    latest_mtime = -1.0

    for path in root.glob("**/*.jsonl"):
        if not path.is_file():
            continue
        try:
            mtime = path.stat().st_mtime
        except OSError:
            continue
        if mtime >= latest_mtime:
            latest = path
            latest_mtime = mtime

    return latest


def _extract_user_text(entry: Dict[str, Any]) -> Optional[str]:
    entry_type = entry.get("type")
    payload = entry.get("payload") or {}
    if not isinstance(payload, dict):
        return None

    if entry_type == "event_msg" and payload.get("type") == "user_message":
        msg = payload.get("message")
        if isinstance(msg, str) and msg.strip():
            return msg.strip()
        return None

    if entry_type == "response_item" and payload.get("type") == "message" and payload.get("role") == "user":
        content = payload.get("content") or []
        if isinstance(content, list):
            texts = []
            for item in content:
                if not isinstance(item, dict):
                    continue
                if item.get("type") == "input_text":
                    text = item.get("text")
                    if isinstance(text, str) and text:
                        texts.append(text)
            if texts:
                return "\n".join(texts).strip()
    return None


def _extract_assistant_text(entry: Dict[str, Any]) -> Optional[str]:
    entry_type = entry.get("type")
    payload = entry.get("payload") or {}
    if not isinstance(payload, dict):
        return None

    if entry_type == "event_msg" and payload.get("type") == "agent_message":
        msg = payload.get("message")
        if isinstance(msg, str) and msg.strip():
            return msg.strip()
        return None

    if entry_type == "response_item" and payload.get("type") == "message" and payload.get("role") == "assistant":
        content = payload.get("content") or []
        if isinstance(content, list):
            texts = []
            for item in content:
                if not isinstance(item, dict):
                    continue
                if item.get("type") == "output_text":
                    text = item.get("text")
                    if isinstance(text, str) and text:
                        texts.append(text)
            if texts:
                return "\n".join(texts).strip()
        msg = payload.get("message")
        if isinstance(msg, str) and msg.strip():
            return msg.strip()
    return None


def _latest_conversations(log_path: Path, n: int) -> list[Tuple[str, str]]:
    conversations: Deque[Tuple[str, str]] = deque(maxlen=n)
    pending_q: Optional[str] = None

    try:
        with log_path.open("r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    entry = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if not isinstance(entry, dict):
                    continue
                q = _extract_user_text(entry)
                if q:
                    pending_q = q
                a = _extract_assistant_text(entry)
                if a and pending_q is not None:
                    conversations.append((pending_q, a))
                    pending_q = None
    except OSError:
        return []

    return list(conversations)


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Print latest Codex replies from session logs.")
    parser.add_argument("n", nargs="?", default="1", help="Number of Q/A rounds to show (default: 1).")
    parser.add_argument("--session-file", default=os.environ.get("TWF_SESSION_FILE", ".codex-tmux-session.json"))
    parser.add_argument("--log", default=None, help="Force a specific Codex session .jsonl log file.")
    args = parser.parse_args(argv[1:])

    try:
        n = max(1, int(args.n))
    except ValueError:
        eprint("Usage: codex_pend.py [N]")
        return EXIT_ERROR

    session_file = Path(args.session_file).expanduser()
    session = _load_json(session_file) if session_file.exists() else {}

    expected_cwd_norm = _realpath(Path.cwd())
    per_worker_root = bool(session.get("codex_home") or session.get("codex_session_root"))
    sessions_root = _sessions_root_for_session(session)

    log_path: Optional[Path]
    if args.log:
        log_path = Path(args.log).expanduser()
    else:
        bound = session.get("codex_session_path")
        log_path = Path(bound).expanduser() if isinstance(bound, str) and bound else None

    if not log_path or not log_path.exists():
        if per_worker_root:
            log_path = _scan_latest_log(sessions_root)
        else:
            log_path = _find_log_for_cwd(expected_cwd_norm) or _scan_latest_log(sessions_root)

    if not log_path or not log_path.exists():
        eprint(f"❌ Codex session log not found under {sessions_root}.")
        return EXIT_ERROR

    conversations = _latest_conversations(log_path, n=n)
    # If a bound log exists but yields no reply, try the latest log under the same root (rotation / new session).
    if not conversations and not args.log:
        latest = _scan_latest_log(sessions_root)
        if latest and latest != log_path:
            log_path = latest
            conversations = _latest_conversations(log_path, n=n)
    if not conversations:
        eprint("No reply available.")
        return EXIT_NO_REPLY

    if n == 1:
        sys.stdout.write(conversations[-1][1])
        if not conversations[-1][1].endswith("\n"):
            sys.stdout.write("\n")
        return EXIT_OK

    for i, (q, a) in enumerate(conversations):
        if q:
            print(f"Q: {q}")
        print(f"A: {a}")
        if i < len(conversations) - 1:
            print("---")
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main(sys.argv))
