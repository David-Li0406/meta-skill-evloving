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
repo="${2:-}"
shift 2 || true

if [[ -z "$workspace" || -z "$repo" ]]; then
  echo "usage: hypr-ws-open-terms <workspace> <dir> [Title::Command]..." >&2
  echo "or set HYPR_WS_TERMS=\"Title::Command|Title::Command\"" >&2
  exit 1
fi

if [[ ! -d "$repo" ]]; then
  echo "repo not found: $repo" >&2
  exit 1
fi

term="${HYPR_WS_TERM:-ghostty}"
shell="${HYPR_WS_SHELL:-zsh}"
path_prefix="${HYPR_WS_PATH_PREFIX:-$HOME/.npm-global/bin:$HOME/.opencode/bin}"

if [[ -z "${HYPR_WS_SHELL_ARGS:-}" ]]; then
  if [[ "$shell" == "bash" ]]; then
    shell_args="-lc"
  else
    shell_args="-lic"
  fi
else
  shell_args="$HYPR_WS_SHELL_ARGS"
fi

if [[ "$#" -gt 0 ]]; then
  terms=("$@")
elif [[ -n "${HYPR_WS_TERMS:-}" ]]; then
  IFS='|' read -r -a terms <<<"$HYPR_WS_TERMS"
else
  terms=("Shell::${shell}")
fi

require_cmd() {
  local cmd="$1"
  if ! command -v "$cmd" >/dev/null 2>&1; then
    echo "missing command: $cmd" >&2
    return 1
  fi
}

require_cmd hyprctl
require_cmd "$term"

hypr_instance() {
  if [[ -n "${HYPRLAND_INSTANCE_SIGNATURE:-}" ]]; then
    printf '%s\n' "$HYPRLAND_INSTANCE_SIGNATURE"
    return 0
  fi

  if [[ -x "$script_dir/hypr-instance.sh" ]]; then
    "$script_dir/hypr-instance.sh" 2>/dev/null || true
  fi
}

hypr() {
  local inst
  inst="$(hypr_instance || true)"
  if [[ -n "$inst" ]]; then
    hyprctl --instance "$inst" "$@"
  else
    hyprctl "$@"
  fi
}

spawn_term() {
  local title="$1"
  local snippet="$2"
  local repo_quoted shell_cmd path_prefix_quoted

  repo_quoted="$(printf %q "$repo")"
  path_prefix_quoted="$(printf %q "$path_prefix")"
  shell_cmd="export PATH=${path_prefix_quoted}:\$PATH; cd $repo_quoted; printf '\033]0;${title}\007'; ${snippet}"
  hypr dispatch exec "$term -e $shell $shell_args $(printf %q "$shell_cmd")"
}

hypr dispatch workspace "name:${workspace}"

for item in "${terms[@]}"; do
  if [[ "$item" == *"::"* ]]; then
    title="${item%%::*}"
    cmd="${item#*::}"
  else
    title="$item"
    cmd="$item"
  fi
  if [[ -z "$cmd" ]]; then
    cmd="$shell"
  fi
  spawn_term "${workspace} ${title}" "$cmd"
  sleep 0.15
done
