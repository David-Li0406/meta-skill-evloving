#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [[ -z "${HYPRLAND_INSTANCE_SIGNATURE:-}" && -x "$script_dir/hypr-instance.sh" ]]; then
  inst="$("$script_dir/hypr-instance.sh" 2>/dev/null || true)"
  if [[ -n "$inst" ]]; then
    export HYPRLAND_INSTANCE_SIGNATURE="$inst"
  fi
fi

workspace="${1:-}"
follow=0

if [[ -z "$workspace" ]]; then
  echo "usage: hypr-win-move <workspace-name> [--follow]" >&2
  exit 1
fi

shift || true
if [[ "${1:-}" == "--follow" ]]; then
  follow=1
fi

hyprctl dispatch movetoworkspace "name:${workspace}"
if [[ "$follow" -eq 1 ]]; then
  hyprctl dispatch workspace "name:${workspace}"
fi
