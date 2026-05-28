#!/usr/bin/env python3
from __future__ import annotations

import argparse
import ctypes
import ctypes.util
import json
import os
import shlex
import select
import subprocess
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, Optional, Tuple


EXIT_OK = 0
EXIT_ERROR = 1
EXIT_TIMEOUT = 2


def eprint(*args: object) -> None:
    print(*args, file=sys.stderr)


def _env_float(*names: str, default: float) -> float:
    for name in names:
        raw = os.environ.get(name)
        if raw is None:
            continue
        try:
            value = float(raw)
        except ValueError:
            continue
        return max(0.0, value)
    return max(0.0, default)


def _realpath(path: Path) -> str:
    return str(path.expanduser().resolve())


def _load_json(path: Path) -> Dict[str, Any]:
    try:
        with path.open("r", encoding="utf-8-sig") as f:
            data = json.load(f)
        return data if isinstance(data, dict) else {}
    except Exception:
        return {}


def _atomic_write_json(path: Path, data: Dict[str, Any]) -> None:
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.parent.mkdir(parents=True, exist_ok=True)
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    tmp.replace(path)


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


def _parse_ts(ts: Any) -> Optional[datetime]:
    if not isinstance(ts, str):
        return None
    # e.g. "2025-12-22T02:55:11.921Z"
    if ts.endswith("Z"):
        ts = ts[:-1] + "+00:00"
    try:
        return datetime.fromisoformat(ts)
    except ValueError:
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

    if entry_type != "response_item":
        return None
    if payload.get("type") != "message":
        return None
    if payload.get("role") != "assistant":
        return None

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

    message = payload.get("message")
    if isinstance(message, str) and message.strip():
        return message.strip()
    return None


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


def _extract_session_meta(entry: Dict[str, Any]) -> Tuple[Optional[str], Optional[str]]:
    if entry.get("type") != "session_meta":
        return None, None
    payload = entry.get("payload") or {}
    if not isinstance(payload, dict):
        return None, None
    session_id = payload.get("id")
    cwd = payload.get("cwd")
    return (session_id if isinstance(session_id, str) else None, cwd if isinstance(cwd, str) else None)


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
            _sid, cwd = _extract_session_meta(entry)
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


def _tmux_cmd(args: list[str], *, input_text: Optional[str] = None) -> None:
    data = input_text.encode("utf-8") if input_text is not None else None
    subprocess.run(["tmux", *args], input=data, check=True)


def _capture_tail(tmux_target: str, *, lines: int = 60) -> str:
    resolved = _resolve_pane_target(tmux_target)
    try:
        return subprocess.check_output(
            ["tmux", "capture-pane", "-p", "-t", resolved, "-S", f"-{max(1, int(lines))}"],
            text=True,
            errors="ignore",
        )
    except Exception:
        return ""


def _wait_for_tui_idle(tmux_target: str, *, timeout_s: float = 30.0, poll_s: float = 0.5) -> None:
    """Best-effort: avoid injecting while Codex is streaming output (prone to lost/garbled keys)."""
    deadline = time.time() + max(0.0, timeout_s)
    while time.time() < deadline:
        tail = _capture_tail(tmux_target, lines=60)
        # Codex TUI renders a "Working (... • esc to interrupt)" status line while streaming.
        busy = ("Working (" in tail) and ("esc to interrupt" in tail)
        if not busy:
            return
        time.sleep(max(0.05, poll_s))


def _resolve_pane_target(tmux_target: str) -> str:
    """Return a stable tmux pane target for injection.

    Handles cases where:
    - tmux_target is already a pane_id (starts with '%'), or
    - tmux_target is a session name (targets active pane), or
    - users created additional windows/panes in the session.

    Preference order:
    1) any pane whose current command is `codex` OR whose start command includes `codex`
    2) active pane
    3) first pane in session
    """
    t = (tmux_target or "").strip()
    if not t:
        return tmux_target
    if t.startswith("%"):
        return t

    session = t.split(":", 1)[0] if ":" in t else t
    try:
        out = subprocess.check_output(
            [
                "tmux",
                "list-panes",
                "-t",
                session,
                "-F",
                "#{pane_id}\t#{pane_current_command}\t#{pane_start_command}\t#{pane_active}",
            ],
            text=True,
        )
    except Exception:
        return tmux_target

    panes: list[tuple[str, str, str, str]] = []
    for line in out.splitlines():
        parts = line.split("\t")
        if len(parts) != 4:
            continue
        pane_id, cmd, start_cmd, active = (p.strip() for p in parts)
        if pane_id:
            panes.append((pane_id, cmd, start_cmd, active))

    for pane_id, cmd, start_cmd, _active in panes:
        if cmd == "codex":
            return pane_id
        # Codex CLI entrypoint is often `node` (wrapper) rather than `codex`.
        tokens = start_cmd.replace('"', "").split()
        if "codex" in tokens:
            return pane_id
    for pane_id, _cmd, _start_cmd, active in panes:
        if active == "1":
            return pane_id
    return panes[0][0] if panes else tmux_target


def _send_enter(tmux_target: str) -> None:
    resolved = _resolve_pane_target(tmux_target)
    # Send an explicit carriage return to submit.
    _tmux_cmd(["send-keys", "-t", resolved, "C-m"])


def _send_escape(tmux_target: str) -> None:
    resolved = _resolve_pane_target(tmux_target)
    _tmux_cmd(["send-keys", "-t", resolved, "Escape"])


def _prepare_tui_for_paste(tmux_target: str) -> None:
    # Codex TUI sometimes needs a short settle time after ESC to avoid paste/submit glitches.
    try:
        _send_escape(tmux_target)
    except Exception:
        return
    time.sleep(0.5)


def _clear_input(tmux_target: str) -> None:
    """Clear Codex input buffer (Ctrl+U works in Codex TUI)."""
    resolved = _resolve_pane_target(tmux_target)
    try:
        _tmux_cmd(["send-keys", "-t", resolved, "C-u"])
        time.sleep(0.05)
        _tmux_cmd(["send-keys", "-t", resolved, "C-u"])
    except Exception:
        return


def _should_clear_input() -> bool:
    v = (os.environ.get("TWF_CLEAR_INPUT") or "").strip().lower()
    return v in {"1", "true", "yes", "y", "on"}


class _InotifyWatcher:
    _IN_MODIFY = 0x00000002
    _IN_ATTRIB = 0x00000004
    _IN_CLOSE_WRITE = 0x00000008
    _IN_DELETE_SELF = 0x00000400
    _IN_MOVED_SELF = 0x00000800

    def __init__(self) -> None:
        self._libc: Optional[ctypes.CDLL] = None
        self._fd: Optional[int] = None
        self._wd: Optional[int] = None
        self._path: Optional[Path] = None

    @classmethod
    def maybe_create(cls) -> Optional["_InotifyWatcher"]:
        mode = (os.environ.get("TWF_WATCH_MODE") or "auto").strip().lower()
        if mode in {"poll", "sleep", "interval", "0", "false", "off"}:
            return None
        if not sys.platform.startswith("linux"):
            return None

        watcher = cls()
        if watcher._init():
            return watcher

        if mode in {"inotify", "watch"}:
            eprint("⚠️  inotify unavailable, falling back to polling (set TWF_WATCH_MODE=poll to silence).")
        watcher.close()
        return None

    def _init(self) -> bool:
        try:
            libc_path = ctypes.util.find_library("c") or "libc.so.6"
            libc = ctypes.CDLL(libc_path, use_errno=True)
            self._libc = libc

            fd: int
            if hasattr(libc, "inotify_init1"):
                libc.inotify_init1.argtypes = [ctypes.c_int]
                libc.inotify_init1.restype = ctypes.c_int
                fd = int(libc.inotify_init1(os.O_NONBLOCK | os.O_CLOEXEC))
            else:
                libc.inotify_init.argtypes = []
                libc.inotify_init.restype = ctypes.c_int
                fd = int(libc.inotify_init())
                if fd < 0:
                    return False
                import fcntl

                flags = fcntl.fcntl(fd, fcntl.F_GETFL)
                fcntl.fcntl(fd, fcntl.F_SETFL, flags | os.O_NONBLOCK)
                flags = fcntl.fcntl(fd, fcntl.F_GETFD)
                fcntl.fcntl(fd, fcntl.F_SETFD, flags | fcntl.FD_CLOEXEC)

            if fd < 0:
                return False

            libc.inotify_add_watch.argtypes = [ctypes.c_int, ctypes.c_char_p, ctypes.c_uint32]
            libc.inotify_add_watch.restype = ctypes.c_int
            libc.inotify_rm_watch.argtypes = [ctypes.c_int, ctypes.c_int]
            libc.inotify_rm_watch.restype = ctypes.c_int

            self._fd = fd
            return True
        except Exception:
            return False

    def watch_path(self, path: Path) -> None:
        if not self._libc or self._fd is None:
            return
        if self._path == path and self._wd is not None:
            return

        if self._wd is not None:
            try:
                self._libc.inotify_rm_watch(self._fd, int(self._wd))
            except Exception:
                pass
            self._wd = None

        self._path = path
        if not path.exists():
            return

        mask = (
            self._IN_MODIFY
            | self._IN_CLOSE_WRITE
            | self._IN_ATTRIB
            | self._IN_MOVED_SELF
            | self._IN_DELETE_SELF
        )
        wd = int(self._libc.inotify_add_watch(self._fd, os.fsencode(str(path)), ctypes.c_uint32(mask)))
        if wd >= 0:
            self._wd = wd

    def wait(self, timeout_s: float) -> None:
        if self._fd is None or self._wd is None:
            if timeout_s > 0:
                time.sleep(timeout_s)
            return
        if timeout_s <= 0:
            return

        try:
            ready, _, _ = select.select([self._fd], [], [], timeout_s)
        except Exception:
            return
        if not ready:
            return

        # Drain events (we only use it as a wakeup mechanism).
        try:
            while True:
                os.read(self._fd, 4096)
        except BlockingIOError:
            pass
        except OSError:
            pass

    def close(self) -> None:
        if self._libc and self._fd is not None and self._wd is not None:
            try:
                self._libc.inotify_rm_watch(self._fd, int(self._wd))
            except Exception:
                pass
        self._wd = None
        if self._fd is not None:
            try:
                os.close(self._fd)
            except OSError:
                pass
        self._fd = None
        self._path = None
        self._libc = None


def _inject_text(tmux_target: str, text: str, *, submit_delay_s: float) -> None:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    resolved = _resolve_pane_target(tmux_target)
    # Use buffer paste for large/multiline to avoid argv limits.
    if "\n" in text or len(text) > 200:
        buf = f"twf-ask-{os.getpid()}"
        _tmux_cmd(["load-buffer", "-b", buf, "-"], input_text=text)
        try:
            # Avoid bracketed paste (-p): Codex TUI may treat it as a paste-burst and ignore immediate submits.
            # -r: keep LF as-is.
            _tmux_cmd(["paste-buffer", "-t", resolved, "-b", buf, "-r"])
        finally:
            subprocess.run(["tmux", "delete-buffer", "-b", buf], check=False)
    else:
        _tmux_cmd(["send-keys", "-t", resolved, "-l", text])

    if submit_delay_s > 0:
        time.sleep(submit_delay_s)
    _send_enter(tmux_target)


def _inject_text_only(tmux_target: str, text: str) -> None:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    resolved = _resolve_pane_target(tmux_target)
    # Use buffer paste for large/multiline to avoid argv limits.
    if "\n" in text or len(text) > 200:
        buf = f"twf-ask-{os.getpid()}"
        _tmux_cmd(["load-buffer", "-b", buf, "-"], input_text=text)
        try:
            # Avoid bracketed paste (-p): Codex TUI may treat it as a paste-burst and ignore immediate submits.
            # -r: keep LF as-is.
            _tmux_cmd(["paste-buffer", "-t", resolved, "-b", buf, "-r"])
        finally:
            subprocess.run(["tmux", "delete-buffer", "-b", buf], check=False)
    else:
        _tmux_cmd(["send-keys", "-t", resolved, "-l", text])


def _schedule_submit_nudges_bg(
    tmux_target: str, *, submit_delay_s: float, nudge_after_s: float, nudge_count: int
) -> None:
    if submit_delay_s < 0:
        submit_delay_s = 0.0
    if nudge_after_s < 0:
        nudge_after_s = 0.0
    if nudge_count < 0:
        nudge_count = 0

    resolved = _resolve_pane_target(tmux_target)
    parts: list[str] = []

    parts.append(
        " ; ".join(
            [
                f"sleep {submit_delay_s:.3f}",
                f"tmux send-keys -t {shlex.quote(resolved)} C-m",
            ]
        )
    )
    for i in range(nudge_count):
        parts.append(
            " ; ".join(
                [
                    f"sleep {nudge_after_s:.3f}",
                    f"tmux send-keys -t {shlex.quote(resolved)} C-m",
                ]
            )
        )
    script = " ; ".join(parts)
    subprocess.run(["tmux", "run-shell", "-b", script], check=True)


def _send_submit_nudges(tmux_target: str, *, base_time_s: float, after_s: float, count: int) -> None:
    if count <= 0:
        return
    if after_s < 0:
        after_s = 0.0
    for i in range(count):
        deadline = base_time_s + after_s * (i + 1)
        sleep_s = deadline - time.time()
        if sleep_s > 0:
            time.sleep(sleep_s)
        try:
            _send_enter(tmux_target)
        except Exception:
            pass


def _poll_for_reply(
    log_path: Path,
    offset: int,
    *,
    allow_rescan: bool,
    per_worker_root: bool,
    sessions_root: Path,
    expected_cwd_norm: str,
    sent_after_utc: datetime,
    timeout_s: float,
    poll_s: float,
    tmux_target: Optional[str],
) -> Tuple[Optional[str], Path, int]:
    deadline = time.time() + timeout_s
    current_path = log_path
    current_offset = offset
    watcher = _InotifyWatcher.maybe_create()
    if watcher is not None:
        watcher.watch_path(current_path)
    last_rescan = time.time()
    rescan_interval = min(2.0, max(0.2, timeout_s / 2.0 if timeout_s > 0 else 0.2))
    # Nudges are sent by a dedicated scheduler in main() to guarantee timing,
    # independent of log detection. Keep polling pure here.

    try:
        while True:
            if time.time() >= deadline:
                return None, current_path, current_offset

            try:
                size = current_path.stat().st_size
                if current_offset > size:
                    current_offset = size
            except OSError:
                pass

            try:
                with current_path.open("rb") as f:
                    f.seek(max(0, current_offset))
                    while True:
                        if time.time() >= deadline:
                            return None, current_path, current_offset

                        pos_before = f.tell()
                        raw = f.readline()
                        if not raw:
                            break

                        if not raw.endswith(b"\n"):
                            f.seek(pos_before)
                            break

                        current_offset = f.tell()
                        line = raw.decode("utf-8", errors="ignore").strip()
                        if not line:
                            continue
                        try:
                            entry = json.loads(line)
                        except json.JSONDecodeError:
                            continue
                        if not isinstance(entry, dict):
                            continue

                        ts = _parse_ts(entry.get("timestamp"))
                        if ts is not None and ts < sent_after_utc:
                            continue

                        msg = _extract_assistant_text(entry)
                        if msg is not None:
                            return msg, current_path, current_offset
            except OSError:
                pass

            now = time.time()
            if allow_rescan and now - last_rescan >= rescan_interval:
                if per_worker_root:
                    candidate = _scan_latest_log(sessions_root)
                else:
                    candidate = _find_log_for_cwd(expected_cwd_norm)
                if candidate and candidate.exists() and candidate != current_path:
                    current_path = candidate
                    current_offset = 0
                    if watcher is not None:
                        watcher.watch_path(current_path)
                last_rescan = now

            now = time.time()
            next_wakeup = deadline
            if allow_rescan:
                next_wakeup = min(next_wakeup, last_rescan + rescan_interval)

            if watcher is None:
                time.sleep(poll_s)
            else:
                watcher.wait(max(0.0, next_wakeup - now))
    finally:
        if watcher is not None:
            watcher.close()


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Send a prompt to Codex running in tmux and wait for the next reply from Codex session logs.")
    parser.add_argument("text", nargs="?", help="Prompt text. If omitted, read from stdin.")
    parser.add_argument("--session-file", default=os.environ.get("TWF_SESSION_FILE", ".codex-tmux-session.json"))
    parser.add_argument("--log", default=None, help="Force a specific Codex session .jsonl log file.")
    parser.add_argument("--timeout", type=float, default=float(os.environ.get("TWF_TIMEOUT", "3600")))
    parser.add_argument("--poll", type=float, default=float(os.environ.get("TWF_POLL_INTERVAL", "0.05")))
    parser.add_argument("--no-write-session", action="store_true", help="Do not update session file with discovered log binding.")
    parser.add_argument(
        "--send-only",
        action="store_true",
        help="Submit the message and exit without waiting for an assistant reply (no submit confirmation).",
    )
    args = parser.parse_args(argv[1:])

    text = args.text
    if text is None:
        text = sys.stdin.read()
    if not isinstance(text, str) or not text.strip():
        eprint("❌ Empty prompt.")
        return EXIT_ERROR

    session_file = Path(args.session_file).expanduser()
    session = _load_json(session_file) if session_file.exists() else {}

    tmux_target = (
        os.environ.get("TWF_TMUX_TARGET")
        or session.get("tmux_target")
        or session.get("tmux_session")
        # pane_id can go stale after tmux restarts/resume; keep as last fallback only.
        or session.get("pane_id")
    )
    if not tmux_target:
        eprint(f"❌ tmux target not configured. Run codex_up_tmux.sh first to create {session_file}.")
        return EXIT_ERROR

    expected_cwd_norm = _realpath(Path.cwd())

    per_worker_root = bool(session.get("codex_home") or session.get("codex_session_root"))
    sessions_root = _sessions_root_for_session(session)

    submit_delay = 1.5
    submit_nudge_after = 2.0
    submit_nudge_max = 3

    if args.send_only:
        try:
            _prepare_tui_for_paste(str(tmux_target))
            if _should_clear_input():
                _clear_input(str(tmux_target))
            _inject_text_only(str(tmux_target), text)
            _schedule_submit_nudges_bg(
                str(tmux_target),
                submit_delay_s=submit_delay,
                nudge_after_s=submit_nudge_after,
                nudge_count=submit_nudge_max,
            )
        except subprocess.CalledProcessError as exc:
            eprint(f"❌ tmux injection failed: {exc}")
            return EXIT_ERROR
        return EXIT_OK

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

    # If we just started a worker, the first session log may take a moment to appear.
    if (not args.log) and (not log_path or not log_path.exists()):
        wait_s = min(10.0, max(0.0, args.timeout))
        deadline = time.time() + wait_s
        while time.time() < deadline:
            time.sleep(min(0.5, max(0.05, args.poll)))
            if per_worker_root:
                log_path = _scan_latest_log(sessions_root)
            else:
                log_path = _find_log_for_cwd(expected_cwd_norm) or _scan_latest_log(sessions_root)
            if log_path and log_path.exists():
                break

    if not log_path or not log_path.exists():
        eprint(f"❌ Codex session log not found under {sessions_root}. Start Codex first, then retry.")
        return EXIT_ERROR

    try:
        offset = log_path.stat().st_size
    except OSError:
        offset = 0

    sent_after = datetime.now(timezone.utc) - timedelta(seconds=0.5)
    try:
        _wait_for_tui_idle(str(tmux_target), timeout_s=30.0, poll_s=0.5)
        _prepare_tui_for_paste(str(tmux_target))
        if _should_clear_input():
            _clear_input(str(tmux_target))
        _inject_text_only(str(tmux_target), text)
        _schedule_submit_nudges_bg(
            str(tmux_target),
            submit_delay_s=submit_delay,
            nudge_after_s=submit_nudge_after,
            nudge_count=submit_nudge_max,
        )
    except subprocess.CalledProcessError as exc:
        eprint(f"❌ tmux injection failed: {exc}")
        return EXIT_ERROR

    reply, used_log_path, _new_offset = _poll_for_reply(
        log_path,
        offset,
        allow_rescan=args.log is None,
        per_worker_root=per_worker_root,
        sessions_root=sessions_root,
        expected_cwd_norm=expected_cwd_norm,
        sent_after_utc=sent_after,
        timeout_s=max(0.0, args.timeout),
        poll_s=min(0.5, max(0.01, args.poll)),
        tmux_target=str(tmux_target) if tmux_target else None,
    )

    if reply is None:
        eprint("⏳ Timeout: no reply.")
        return EXIT_TIMEOUT

    if not args.no_write_session:
        try:
            data = _load_json(session_file) if session_file.exists() else {}
            data["codex_session_path"] = str(used_log_path)
            # Bind session_id if available (read from header)
            for entry in _read_first_lines(used_log_path, limit=10):
                sid, cwd = _extract_session_meta(entry)
                if sid:
                    data["codex_session_id"] = sid
                    data["codex_current_id"] = sid
                    data["codex_resume_from_id"] = sid
                if cwd:
                    data["work_dir"] = cwd
                    try:
                        data["work_dir_norm"] = _realpath(Path(cwd))
                    except Exception:
                        pass
                if sid or cwd:
                    break
            _atomic_write_json(session_file, data)
        except Exception:
            pass

    sys.stdout.write(reply)
    if not reply.endswith("\n"):
        sys.stdout.write("\n")
    sys.stdout.flush()
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main(sys.argv))
