#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [[ -z "${HYPRLAND_INSTANCE_SIGNATURE:-}" && -x "$script_dir/hypr-instance.sh" ]]; then
  inst="$("$script_dir/hypr-instance.sh" 2>/dev/null || true)"
  if [[ -n "$inst" ]]; then
    export HYPRLAND_INSTANCE_SIGNATURE="$inst"
  fi
fi

usage() {
  cat <<'EOF' >&2
usage: hypr-win-focus [--class REGEX] [--title REGEX] [--workspace NAME] [--icase] [--exec CMD]
EOF
}

class=""
title=""
workspace=""
icase=0
exec_cmd=""

while [[ "$#" -gt 0 ]]; do
  case "$1" in
    --class) class="${2:-}"; shift 2 ;;
    --title) title="${2:-}"; shift 2 ;;
    --workspace) workspace="${2:-}"; shift 2 ;;
    --icase) icase=1; shift ;;
    --exec) exec_cmd="${2:-}"; shift 2 ;;
    -h|--help) usage; exit 0 ;;
    *) echo "unknown arg: $1" >&2; usage; exit 1 ;;
  esac
done

if [[ -z "$class" && -z "$title" ]]; then
  usage
  exit 1
fi

python - "$class" "$title" "$workspace" "$icase" "$exec_cmd" <<'PY'
import json
import os
import re
import subprocess
import sys

cls = sys.argv[1]
title = sys.argv[2]
workspace = sys.argv[3]
icase = sys.argv[4] == "1"
exec_cmd = sys.argv[5]

flags = re.IGNORECASE if icase else 0

clients = json.loads(subprocess.check_output(["hyprctl", "-j", "clients"]))
addr = None
for c in clients:
    if workspace and c.get("workspace", {}).get("name") != workspace:
        continue
    if cls and not re.search(cls, c.get("class", "") or "", flags):
        continue
    if title and not re.search(title, c.get("title", "") or "", flags):
        continue
    addr = c.get("address")
    break

if addr:
    subprocess.run(["hyprctl", "dispatch", "focuswindow", f"address:{addr}"])
    raise SystemExit(0)

if exec_cmd:
    subprocess.run(["hyprctl", "dispatch", "exec", exec_cmd])
    raise SystemExit(0)

raise SystemExit(1)
PY
