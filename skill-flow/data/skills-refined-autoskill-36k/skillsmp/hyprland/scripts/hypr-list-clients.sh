#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [[ -z "${HYPRLAND_INSTANCE_SIGNATURE:-}" && -x "$script_dir/hypr-instance.sh" ]]; then
  inst="$("$script_dir/hypr-instance.sh" 2>/dev/null || true)"
  if [[ -n "$inst" ]]; then
    export HYPRLAND_INSTANCE_SIGNATURE="$inst"
  fi
fi

python - <<'PY'
import json
import subprocess

clients = json.loads(subprocess.check_output(["hyprctl", "-j", "clients"]))
for c in clients:
    addr = c.get("address", "")
    ws = c.get("workspace", {}).get("name", "")
    klass = c.get("class", "")
    title = c.get("title", "")
    print(f"{addr}\t{ws}\t{klass}\t{title}")
PY
