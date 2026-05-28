#!/usr/bin/env bash
set -euo pipefail

usage() {
  echo "usage: hypr-instance [--all]" >&2
}

all=0
case "${1:-}" in
  -a|--all)
    all=1
    shift
    ;;
  -h|--help)
    usage
    exit 0
    ;;
  "")
    ;;
  *)
    usage
    exit 1
    ;;
esac

declare -A seen=()
instances=()
preferred=""

add_instance() {
  local sig="$1"
  [[ -n "$sig" ]] || return 0
  if [[ -z "${seen[$sig]+x}" ]]; then
    seen["$sig"]=1
    instances+=("$sig")
  fi
}

has_socket() {
  local dir="$1"
  [[ -d "$dir" ]] || return 1
  local sock
  for sock in ".socket.sock" ".socket2.sock" "hyprland.sock" "hyprland.sock2"; do
    if [[ -S "$dir/$sock" ]]; then
      return 0
    fi
  done
  return 1
}

socket_mtime() {
  local dir="$1"
  local sock
  for sock in ".socket.sock" ".socket2.sock" "hyprland.sock" "hyprland.sock2"; do
    if [[ -S "$dir/$sock" ]]; then
      stat -c %Y "$dir/$sock" 2>/dev/null || printf '0\n'
      return 0
    fi
  done
  printf '0\n'
}

hypr_root="/tmp/hypr"
if [[ -n "${XDG_RUNTIME_DIR:-}" && -d "$XDG_RUNTIME_DIR/hypr" ]]; then
  hypr_root="$XDG_RUNTIME_DIR/hypr"
fi
if [[ -L "$hypr_root" ]]; then
  hypr_root="$(readlink -f "$hypr_root" 2>/dev/null || echo "$hypr_root")"
fi

if [[ -n "${HYPRLAND_INSTANCE_SIGNATURE:-}" ]]; then
  if has_socket "$hypr_root/$HYPRLAND_INSTANCE_SIGNATURE"; then
    if [[ "$all" -eq 0 ]]; then
      printf '%s\n' "$HYPRLAND_INSTANCE_SIGNATURE"
      exit 0
    fi
  fi
  add_instance "$HYPRLAND_INSTANCE_SIGNATURE"
fi

if command -v pgrep >/dev/null 2>&1; then
  while IFS= read -r pid; do
    env_file="/proc/$pid/environ"
    [[ -r "$env_file" ]] || continue
    if ! env_dump="$(tr '\0' '\n' < "$env_file" 2>/dev/null)"; then
      continue
    fi
    sig="$(printf '%s\n' "$env_dump" | awk -F= '$1=="HYPRLAND_INSTANCE_SIGNATURE"{print $2; exit}')"
    [[ -n "$sig" ]] || continue
    add_instance "$sig"
    if [[ -n "${WAYLAND_DISPLAY:-}" && -z "$preferred" ]]; then
      wd="$(printf '%s\n' "$env_dump" | awk -F= '$1=="WAYLAND_DISPLAY"{print $2; exit}')"
      if [[ -n "$wd" && "$wd" == "$WAYLAND_DISPLAY" ]]; then
        preferred="$sig"
      fi
    fi
  done < <(pgrep -x Hyprland 2>/dev/null || pgrep -f '[H]yprland' 2>/dev/null || true)
fi

if [[ -d "$hypr_root" ]]; then
  while IFS= read -r dir; do
    if has_socket "$dir"; then
      add_instance "$(basename "$dir")"
    fi
  done < <(find -L "$hypr_root" -mindepth 1 -maxdepth 1 -type d 2>/dev/null)
fi

if [[ "$all" -eq 1 ]]; then
  if [[ "${#instances[@]}" -eq 0 ]]; then
    exit 1
  fi
  printf '%s\n' "${instances[@]}"
  exit 0
fi

if [[ -n "$preferred" ]]; then
  printf '%s\n' "$preferred"
  exit 0
fi

if [[ "${#instances[@]}" -eq 0 ]]; then
  exit 1
fi

if [[ "${#instances[@]}" -eq 1 ]]; then
  printf '%s\n' "${instances[0]}"
  exit 0
fi

latest_sig=""
latest_mtime=0
for sig in "${instances[@]}"; do
  mtime="$(socket_mtime "$hypr_root/$sig")"
  if [[ "$mtime" -gt "$latest_mtime" ]]; then
    latest_mtime="$mtime"
    latest_sig="$sig"
  fi
done

if [[ -n "$latest_sig" ]]; then
  printf '%s\n' "$latest_sig"
else
  printf '%s\n' "${instances[0]}"
fi
