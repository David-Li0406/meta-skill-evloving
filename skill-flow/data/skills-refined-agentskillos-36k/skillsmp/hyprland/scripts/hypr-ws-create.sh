#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [[ -z "${HYPRLAND_INSTANCE_SIGNATURE:-}" && -x "$script_dir/hypr-instance.sh" ]]; then
  inst="$("$script_dir/hypr-instance.sh" 2>/dev/null || true)"
  if [[ -n "$inst" ]]; then
    export HYPRLAND_INSTANCE_SIGNATURE="$inst"
  fi
fi

name="${1:-}"
if [[ -z "$name" ]]; then
  echo "usage: hypr-ws-create <workspace-name>" >&2
  exit 1
fi

hyprctl dispatch workspace "name:${name}"
