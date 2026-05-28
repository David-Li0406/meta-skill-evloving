#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import shlex
import shutil
import subprocess
import sys
import threading
from dataclasses import dataclass
from pathlib import Path
from queue import Queue
from typing import Any
from urllib.parse import quote_from_bytes, unquote, urlparse, urlunparse


def _eprint(msg: str) -> None:
    print(msg, file=sys.stderr)


def _file_uri(path: Path) -> str:
    p = Path(path).expanduser().resolve()
    raw = p.as_posix().encode("utf-8")
    return urlunparse(("file", "", quote_from_bytes(raw), "", "", ""))


def _path_from_uri(uri: str) -> Path:
    parsed = urlparse(uri)
    if parsed.scheme != "file":
        raise ValueError(f"unsupported uri scheme: {uri!r}")
    return Path(os.path.normpath(unquote(parsed.path)))


def _git_toplevel(cwd: Path) -> Path | None:
    try:
        res = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            cwd=str(cwd),
            capture_output=True,
            text=True,
            check=False,
        )
    except OSError:
        return None
    if res.returncode != 0:
        return None
    out = (res.stdout or "").strip()
    return Path(out).resolve() if out else None


def _resolve_langserver(*, venv: str) -> list[str]:
    exe = shutil.which("pyright-langserver")
    if exe:
        return [exe]

    if venv:
        venv_path = Path(venv).expanduser()
        if venv_path.is_dir():
            cand = venv_path / "bin" / "pyright-langserver"
            if cand.is_file():
                return [str(cand)]
            py = venv_path / "bin" / "python"
            if py.is_file():
                return [str(py), "-m", "pyright.langserver"]

    raise SystemExit(
        "❌ pyright-langserver not found.\n"
        "   Install `pyright` into your environment, e.g.\n"
        "   - pip install pyright\n"
        "   Or point to your venv:\n"
        "   - --venv <venv_dir>\n"
    )


@dataclass(frozen=True)
class LspLocation:
    uri: str
    line0: int
    character0: int

    def to_display(self) -> str:
        p = _path_from_uri(self.uri)
        return f"{p}:{self.line0 + 1}:{self.character0 + 1}"


class LspTransport:
    def __init__(self, proc: subprocess.Popen[bytes]):
        self._proc = proc
        self._lock = threading.Lock()
        self._next_id = 1
        self._pending: dict[int, Queue[dict[str, Any]]] = {}
        self._reader = threading.Thread(target=self._read_loop, daemon=True)
        self._reader.start()

    def close(self) -> None:
        try:
            if self._proc.stdin:
                self._proc.stdin.close()
        except Exception:
            pass
        try:
            self._proc.terminate()
        except Exception:
            pass
        try:
            self._proc.wait(timeout=2)
        except Exception:
            try:
                self._proc.kill()
            except Exception:
                pass

    def notify(self, method: str, params: dict[str, Any] | None = None) -> None:
        msg: dict[str, Any] = {"jsonrpc": "2.0", "method": method}
        if params is not None:
            msg["params"] = params
        self._send(msg)

    def request(self, method: str, params: dict[str, Any] | None = None, *, timeout_s: float = 60.0) -> Any:
        with self._lock:
            req_id = self._next_id
            self._next_id += 1
            q: Queue[dict[str, Any]] = Queue()
            self._pending[req_id] = q

        msg: dict[str, Any] = {"jsonrpc": "2.0", "id": req_id, "method": method}
        if params is not None:
            msg["params"] = params
        self._send(msg)

        try:
            resp = q.get(timeout=timeout_s)
        except Exception as e:
            raise TimeoutError(f"timeout waiting for {method} response") from e
        if "error" in resp:
            raise RuntimeError(resp["error"])
        return resp.get("result")

    def _send(self, payload: dict[str, Any]) -> None:
        raw = json.dumps(payload, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
        header = f"Content-Length: {len(raw)}\r\n\r\n".encode("ascii")
        if not self._proc.stdin:
            raise RuntimeError("stdin closed")
        self._proc.stdin.write(header)
        self._proc.stdin.write(raw)
        self._proc.stdin.flush()

    def _read_headers(self) -> int:
        if not self._proc.stdout:
            raise RuntimeError("stdout closed")
        content_len: int | None = None
        while True:
            line = self._proc.stdout.readline()
            if not line:
                raise EOFError("LSP server stdout closed")
            if line in {b"\r\n", b"\n"}:
                break
            if line.lower().startswith(b"content-length:"):
                try:
                    content_len = int(line.split(b":", 1)[1].strip())
                except Exception:
                    content_len = None
        if content_len is None:
            raise ValueError("missing Content-Length header")
        return content_len

    def _read_loop(self) -> None:
        while True:
            try:
                n = self._read_headers()
                if not self._proc.stdout:
                    return
                body = self._proc.stdout.read(n)
                if not body:
                    return
                msg = json.loads(body.decode("utf-8"))
            except Exception:
                return

            if isinstance(msg, dict) and "id" in msg:
                req_id = msg.get("id")
                if isinstance(req_id, int):
                    with self._lock:
                        q = self._pending.pop(req_id, None)
                    if q is not None:
                        q.put(msg)
                continue

            # Ignore notifications.


def _start_pyright_server(*, cwd: Path, venv: str) -> LspTransport:
    argv = _resolve_langserver(venv=venv) + ["--stdio"]
    _eprint(f"ℹ️ starting pyright LSP: {shlex.join(argv)} (cwd={cwd})")
    proc = subprocess.Popen(
        argv,
        cwd=str(cwd),
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
    )
    return LspTransport(proc)


def _initialize(client: LspTransport, *, root: Path) -> None:
    root_uri = _file_uri(root)
    params = {
        "processId": os.getpid(),
        "rootUri": root_uri,
        "capabilities": {},
        "clientInfo": {"name": "pyright-lsp-tool"},
        "workspaceFolders": [{"uri": root_uri, "name": root.name}],
    }
    client.request("initialize", params, timeout_s=120.0)
    client.notify("initialized", {})


def _did_open(client: LspTransport, *, path: Path, version: int = 1) -> str:
    uri = _file_uri(path)
    text = path.read_text(encoding="utf-8")
    client.notify(
        "textDocument/didOpen",
        {
            "textDocument": {
                "uri": uri,
                "languageId": "python",
                "version": version,
                "text": text,
            }
        },
    )
    return uri


def _did_close(client: LspTransport, *, uri: str) -> None:
    client.notify("textDocument/didClose", {"textDocument": {"uri": uri}})


def _refs(client: LspTransport, *, uri: str, line0: int, character0: int) -> list[LspLocation]:
    res = client.request(
        "textDocument/references",
        {
            "textDocument": {"uri": uri},
            "position": {"line": line0, "character": character0},
            "context": {"includeDeclaration": False},
        },
        timeout_s=120.0,
    )
    out: list[LspLocation] = []
    if isinstance(res, list):
        for item in res:
            if not isinstance(item, dict):
                continue
            u = item.get("uri")
            r = item.get("range")
            if not isinstance(u, str) or not isinstance(r, dict):
                continue
            start = r.get("start")
            if not isinstance(start, dict):
                continue
            line = start.get("line")
            ch = start.get("character")
            if isinstance(line, int) and isinstance(ch, int):
                out.append(LspLocation(u, line, ch))
    return out


def _parse_loc(s: str) -> tuple[Path, int, int]:
    # path:line:col (1-based), allow optional # separator.
    if "#" in s:
        path_s, rest = s.split("#", 1)
    else:
        path_s, rest = s, ""
    if rest:
        parts = rest.split(":")
    else:
        parts = path_s.split(":")
        if len(parts) >= 3:
            path_s = ":".join(parts[:-2])
            parts = parts[-2:]
        else:
            raise ValueError("location must be path:line:col")

    if len(parts) != 2:
        raise ValueError("location must be path:line:col")
    line = int(parts[0])
    col = int(parts[1])
    if line <= 0 or col <= 0:
        raise ValueError("line/col must be 1-based positive integers")
    return Path(path_s), line - 1, col - 1


def cmd_refs(args: argparse.Namespace) -> int:
    cwd = Path.cwd()
    root = Path(args.root).expanduser().resolve() if args.root else (_git_toplevel(cwd) or cwd)

    file_path, line0, col0 = _parse_loc(args.location)
    if not file_path.is_absolute():
        file_path = (Path.cwd() / file_path).resolve()
    if not file_path.is_file():
        raise SystemExit(f"❌ file not found: {file_path}")

    client = _start_pyright_server(cwd=root, venv=args.venv)
    try:
        _initialize(client, root=root)
        uri = _did_open(client, path=file_path)
        try:
            locs = _refs(client, uri=uri, line0=line0, character0=col0)
        finally:
            _did_close(client, uri=uri)
    finally:
        client.close()

    uniq = sorted({loc.to_display() for loc in locs})
    try:
        for line in uniq:
            print(line)
    except BrokenPipeError:
        return 0
    return 0


def cmd_repl(args: argparse.Namespace) -> int:
    cwd = Path.cwd()
    root = Path(args.root).expanduser().resolve() if args.root else (_git_toplevel(cwd) or cwd)

    client = _start_pyright_server(cwd=root, venv=args.venv)
    try:
        _initialize(client, root=root)
        _eprint("✅ pyright LSP ready. Commands: refs <path:line:col> | exit")
        version = 1
        while True:
            try:
                raw = input("pyright> ").strip()
            except EOFError:
                break
            if not raw:
                continue
            if raw in {"exit", "quit"}:
                break
            if raw.startswith("refs "):
                loc_s = raw[len("refs ") :].strip()
                try:
                    file_path, line0, col0 = _parse_loc(loc_s)
                except Exception as e:
                    _eprint(f"❌ invalid location: {e}")
                    continue
                if not file_path.is_absolute():
                    file_path = (Path.cwd() / file_path).resolve()
                if not file_path.is_file():
                    _eprint(f"❌ file not found: {file_path}")
                    continue
                uri = _did_open(client, path=file_path, version=version)
                version += 1
                try:
                    locs = _refs(client, uri=uri, line0=line0, character0=col0)
                except Exception as e:
                    _eprint(f"❌ refs failed: {e}")
                    continue
                finally:
                    _did_close(client, uri=uri)
                uniq = sorted({loc.to_display() for loc in locs})
                for line in uniq:
                    print(line)
                continue
            _eprint("❌ unknown command. Use: refs <path:line:col> | exit")
    finally:
        client.close()

    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="pyright_lsp_tool", add_help=True)
    p.add_argument("--root", default="", help="project root (default: git toplevel or cwd)")
    p.add_argument("--venv", default="", help="optional venv dir to locate pyright-langserver")
    sub = p.add_subparsers(dest="cmd", required=True)

    refs = sub.add_parser("refs", help="find references at a file position (path:line:col, 1-based)")
    refs.add_argument("location")

    sub.add_parser("repl", help="interactive session (keeps server warm)")
    return p


def main(argv: list[str]) -> int:
    args = build_parser().parse_args(argv)
    if args.cmd == "refs":
        return cmd_refs(args)
    if args.cmd == "repl":
        return cmd_repl(args)
    raise SystemExit("unreachable")


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

