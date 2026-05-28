#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [[ -z "${HYPRLAND_INSTANCE_SIGNATURE:-}" && -x "$script_dir/hypr-instance.sh" ]]; then
  inst="$("$script_dir/hypr-instance.sh" 2>/dev/null || true)"
  if [[ -n "$inst" ]]; then
    export HYPRLAND_INSTANCE_SIGNATURE="$inst"
  fi
fi

if ! command -v wofi >/dev/null 2>&1; then
  echo "wofi not installed" >&2
  exit 1
fi

selection="$(
  python - <<'PY' | wofi --show dmenu --prompt "Window"
import json
import subprocess

clients = json.loads(subprocess.check_output(["hyprctl", "-j", "clients"]))
for c in clients:
    addr = c.get("address", "")
    ws = c.get("workspace", {}).get("name", "")
    klass = c.get("class", "")
    title = c.get("title", "")
    print(f"{ws} | {klass} | {title} | {addr}")
PY
)"

if [[ -z "$selection" ]]; then
  exit 0
fi

addr="${selection##* | }"
if [[ -n "$addr" ]]; then
  hyprctl dispatch focuswindow "address:${addr}"
fi
