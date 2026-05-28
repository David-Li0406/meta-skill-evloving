#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [[ -z "${HYPRLAND_INSTANCE_SIGNATURE:-}" && -x "$script_dir/hypr-instance.sh" ]]; then
  inst="$("$script_dir/hypr-instance.sh" 2>/dev/null || true)"
  if [[ -n "$inst" ]]; then
    export HYPRLAND_INSTANCE_SIGNATURE="$inst"
  fi
fi

if [[ "$#" -eq 0 ]]; then
  echo "usage: hypr-ws-close <workspace-name> [workspace-name...]" >&2
  exit 1
fi

python - "$@" <<'PY'
import json
import os
import signal
import subprocess
import sys
import time

targets = set(sys.argv[1:])
if not targets:
    raise SystemExit(1)

clients = json.loads(subprocess.check_output(["hyprctl", "-j", "clients"]))
addresses = [
    c.get("address")
    for c in clients
    if c.get("workspace", {}).get("name") in targets
]

for addr in addresses:
    if not addr:
        continue
    subprocess.run(["hyprctl", "dispatch", "closewindow", f"address:{addr}"])

for addr in addresses:
    if not addr:
        continue
    subprocess.run(["hyprctl", "dispatch", "focuswindow", f"address:{addr}"])
    subprocess.run(["hyprctl", "dispatch", "killactive"])

clients = json.loads(subprocess.check_output(["hyprctl", "-j", "clients"]))
pids = [
    c.get("pid")
    for c in clients
    if c.get("workspace", {}).get("name") in targets and c.get("pid")
]

for pid in pids:
    try:
        os.kill(pid, signal.SIGTERM)
    except ProcessLookupError:
        pass

time.sleep(0.2)

clients = json.loads(subprocess.check_output(["hyprctl", "-j", "clients"]))
for c in clients:
    if c.get("workspace", {}).get("name") in targets and c.get("pid"):
        try:
            os.kill(c["pid"], signal.SIGKILL)
        except ProcessLookupError:
            pass

fallback = os.environ.get("HYPR_WS_FALLBACK", "1").strip()
if fallback and fallback.lower() not in {"none", "off", "false"}:
    subprocess.run(["hyprctl", "dispatch", "workspace", fallback])

history = os.path.expanduser("~/.cache/hypr-launcher/workspaces.txt")
if os.path.exists(history):
    with open(history, "r", encoding="utf-8") as fh:
        lines = [line.rstrip("\n") for line in fh]
    lines = [line for line in lines if line and line not in targets]
    with open(history, "w", encoding="utf-8") as fh:
        for line in lines:
            fh.write(line + "\n")
PY
