#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$SCRIPT_DIR/.venv"
VENV_PY="$VENV_DIR/bin/python"
VENV_BIN="$VENV_DIR/bin"

DEFAULT_CIPHEY_VERSION="5.14.0"

print_help() {
  cat <<'EOF'
Usage:
  ciphey.sh [--runner <uv|docker|auto>] [--] <ciphey-args...>

Common examples:
  ciphey.sh --text "aGVsbG8gbXkgbmFtZSBpcyBiZWU="
  ciphey.sh --file ./cipher.txt
  echo "aGVsbG8=" | ciphey.sh

Runner behavior:
  - Default runner is uv-first; if Ciphey cannot be installed on this platform, falls back to Docker.

Environment variables:
  - CIPHEY_RUNNER_MODE=uv|docker|auto (default: auto)
  - CIPHEY_VERSION=<version>         (default: 5.14.0)
  - CIPHEY_DOCKER_IMAGE=<image>      (default: remnux/ciphey)
EOF
}

ensure_uv() {
  if command -v uv >/dev/null 2>&1; then
    return 0
  fi

  if ! command -v curl >/dev/null 2>&1; then
    echo "error: uv is not installed and curl is missing; install uv manually, or install curl and re-run." >&2
    return 1
  fi

  echo "Installing uv..." >&2
  curl -LsSf https://astral.sh/uv/install.sh | sh

  export PATH="$HOME/.local/bin:$HOME/.cargo/bin:$PATH"

  if ! command -v uv >/dev/null 2>&1; then
    echo "error: uv install finished but 'uv' is not on PATH." >&2
    echo "hint: add ~/.local/bin to PATH (then restart your shell) and re-run." >&2
    return 1
  fi
}

ensure_venv() {
  if [[ -x "$VENV_PY" ]]; then
    return 0
  fi

  echo "Creating venv: $VENV_DIR (Python 3.9)" >&2
  if uv venv -p 3.9 "$VENV_DIR"; then
    return 0
  fi

  echo "uv venv failed; trying to install Python 3.9 via uv..." >&2
  uv python install 3.9
  uv venv -p 3.9 "$VENV_DIR"
}

ensure_ciphey() {
  local version="${CIPHEY_VERSION:-$DEFAULT_CIPHEY_VERSION}"

  if "$VENV_PY" -c "import ciphey, cipheycore" >/dev/null 2>&1; then
    return 0
  fi

  echo "Installing Ciphey into venv (ciphey==$version)..." >&2
  if ! uv pip install --python "$VENV_PY" "ciphey==$version"; then
    echo "error: failed to install ciphey==$version via uv/pip." >&2
    return 1
  fi

  if ! "$VENV_PY" -c "import ciphey, cipheycore" >/dev/null 2>&1; then
    echo "error: Ciphey installed but failed to import (cipheycore likely unsupported on this platform)." >&2
    return 1
  fi
}

run_uv() {
  ensure_uv
  ensure_venv
  ensure_ciphey

  if [[ ! -x "$VENV_BIN/ciphey" ]]; then
    echo "error: expected Ciphey executable at $VENV_BIN/ciphey but it was not found." >&2
    return 1
  fi

  "$VENV_BIN/ciphey" "$@"
}

resolve_abs_file() {
  local caller_dir="$1"
  local path="$2"

  if [[ "$path" != /* ]]; then
    path="$caller_dir/$path"
  fi

  local dir
  dir="$(cd "$(dirname "$path")" && pwd)"
  echo "$dir/$(basename "$path")"
}

run_docker() {
  local caller_dir="$1"
  shift

  local image="${CIPHEY_DOCKER_IMAGE:-remnux/ciphey}"

  if ! command -v docker >/dev/null 2>&1; then
    echo "error: docker is not installed; cannot use Docker runner." >&2
    return 1
  fi

  local mount_dir=""
  local -a ciphey_args=()

  while [[ $# -gt 0 ]]; do
    case "$1" in
      -f|--file)
        if [[ $# -lt 2 ]]; then
          echo "error: missing value for $1" >&2
          return 2
        fi
        local host_file
        host_file="$(resolve_abs_file "$caller_dir" "$2")"
        if [[ ! -f "$host_file" ]]; then
          echo "error: file not found: $2" >&2
          return 2
        fi
        mount_dir="$(cd "$(dirname "$host_file")" && pwd)"
        ciphey_args+=("-f" "/work/$(basename "$host_file")")
        shift 2
        ;;
      --file=*)
        local host_file
        host_file="$(resolve_abs_file "$caller_dir" "${1#*=}")"
        if [[ ! -f "$host_file" ]]; then
          echo "error: file not found: ${1#*=}" >&2
          return 2
        fi
        mount_dir="$(cd "$(dirname "$host_file")" && pwd)"
        ciphey_args+=("-f" "/work/$(basename "$host_file")")
        shift
        ;;
      *)
        ciphey_args+=("$1")
        shift
        ;;
    esac
  done

  local -a docker_args=(--rm -i)
  if [[ -n "$mount_dir" ]]; then
    docker_args+=("-v" "$mount_dir:/work:ro" "-w" "/work")
  fi

  docker run "${docker_args[@]}" "$image" "${ciphey_args[@]}"
}

main() {
  local runner="${CIPHEY_RUNNER_MODE:-auto}"

  if [[ $# -eq 0 ]]; then
    print_help
    exit 2
  fi

  local -a args=()
  while [[ $# -gt 0 ]]; do
    case "$1" in
      -h|--help)
        print_help
        exit 0
        ;;
      --runner)
        if [[ $# -lt 2 ]]; then
          echo "error: --runner requires a value: uv|docker|auto" >&2
          exit 2
        fi
        runner="$2"
        shift 2
        ;;
      --runner=*)
        runner="${1#*=}"
        shift
        ;;
      --)
        shift
        args+=("$@")
        break
        ;;
      *)
        args+=("$1")
        shift
        ;;
    esac
  done

  local caller_dir="$PWD"
  cd "$SCRIPT_DIR"

  case "$runner" in
    uv)
      run_uv "${args[@]}"
      ;;
    docker)
      run_docker "$caller_dir" "${args[@]}"
      ;;
    auto)
      if run_uv "${args[@]}"; then
        return 0
      fi
      echo "uv runner failed; falling back to Docker..." >&2
      run_docker "$caller_dir" "${args[@]}"
      ;;
    *)
      echo "error: invalid runner: $runner (expected: uv|docker|auto)" >&2
      exit 2
      ;;
  esac
}

if [[ "${BASH_SOURCE[0]}" == "$0" ]]; then
  main "$@"
fi

