#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [[ -z "${HYPRLAND_INSTANCE_SIGNATURE:-}" && -x "$script_dir/hypr-instance.sh" ]]; then
  inst="$("$script_dir/hypr-instance.sh" 2>/dev/null || true)"
  if [[ -n "$inst" ]]; then
    export HYPRLAND_INSTANCE_SIGNATURE="$inst"
  fi
fi

if [[ -n "${HYPR_PROJECT_ROOTS:-}" ]]; then
  IFS=':' read -r -a project_roots <<<"$HYPR_PROJECT_ROOTS"
else
  project_roots=("$HOME/Code/self" "$HOME/Code/rcrai")
fi

project_arg="${1:-}"

if [[ -z "$project_arg" ]]; then
  if command -v wofi >/dev/null 2>&1; then
    project_arg="$(
      {
        for root in "${project_roots[@]}"; do
          [[ -d "$root" ]] || continue
          root_label="${root#$HOME/Code/}"
          if [[ "$root_label" == "$root" || -z "$root_label" ]]; then
            root_label="$(basename "$root")"
          fi
          find "$root" -mindepth 1 -maxdepth 1 -type d -printf '%f\n' 2>/dev/null \
            | sort \
            | sed "s#^#${root_label}/#"
        done
      } | sort | wofi --show dmenu --prompt "Project"
    )"
  else
    echo "missing project name and wofi not installed" >&2
    exit 1
  fi
fi

if [[ -z "$project_arg" ]]; then
  exit 0
fi

repo=""
if [[ "$project_arg" = /* ]]; then
  repo="$project_arg"
elif [[ "$project_arg" == *"/"* ]]; then
  repo="$HOME/Code/$project_arg"
else
  for root in "${project_roots[@]}"; do
    if [[ -d "$root/$project_arg" ]]; then
      repo="$root/$project_arg"
      break
    fi
  done
fi

if [[ -z "$repo" ]]; then
  repo="${project_roots[0]}/${project_arg}"
fi

if [[ ! -d "$repo" ]]; then
  echo "repo not found: $repo" >&2
  exit 1
fi

workspace="${HYPR_WORKSPACE_NAME:-$(basename "$repo")}"
term="${HYPR_WORKSPACE_TERM:-ghostty}"
codex_cmd="${HYPR_WORKSPACE_CODEX_CMD:-codex}"
codex_bin="${HYPR_WORKSPACE_CODEX_BIN:-$HOME/.npm-global/bin/codex}"
nvim_cmd="${HYPR_WORKSPACE_NVIM_CMD:-nvim}"
codex_args="${HYPR_WORKSPACE_CODEX_ARGS:---dangerously-bypass-approvals-and-sandbox}"
shell="${HYPR_WORKSPACE_SHELL:-zsh}"
path_prefix="${HYPR_WORKSPACE_PATH_PREFIX:-$HOME/.npm-global/bin:$HOME/.opencode/bin}"

if [[ -z "${HYPR_WORKSPACE_SHELL_ARGS:-}" ]]; then
  if [[ "$shell" == "bash" ]]; then
    shell_args="-lc"
  else
    shell_args="-lic"
  fi
else
  shell_args="$HYPR_WORKSPACE_SHELL_ARGS"
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
require_cmd "$nvim_cmd"

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

spawn_term "${workspace} Codex" "if [ -x $(printf %q "$codex_bin") ]; then $(printf %q "$codex_bin") $codex_args; elif command -v $codex_cmd >/dev/null 2>&1; then $codex_cmd $codex_args; else echo 'codex not found'; fi; exec $shell"
sleep 0.2
spawn_term "${workspace} Shell" "exec $shell"
sleep 0.2
spawn_term "${workspace} Nvim" "exec $nvim_cmd"
