#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'USAGE'
Run a command in a separate gnome-terminal so the user can enter a sudo password.

Usage:
  run_sudo_gnome_terminal.sh -- <command> [args...]
  run_sudo_gnome_terminal.sh --cmd "<shell command>"
  run_sudo_gnome_terminal.sh --interactive -- <command> [args...]
  run_sudo_gnome_terminal.sh --interactive --cmd "<shell command>"
  run_sudo_gnome_terminal.sh --self-test
USAGE
}

self_test=0
interactive=0
cmd_mode=""
cmd_string=""
cmd_args=()

while [[ $# -gt 0 ]]; do
  case "$1" in
    --self-test)
      self_test=1
      shift
      ;;
    --cmd)
      shift
      cmd_string="${1:-}"
      cmd_mode="string"
      shift
      ;;
    --interactive|--tty)
      interactive=1
      shift
      ;;
    --)
      shift
      cmd_args=("$@")
      cmd_mode="args"
      break
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown option: $1" >&2
      usage >&2
      exit 64
      ;;
  esac
done

if (( self_test )); then
  if ! command -v gnome-terminal >/dev/null 2>&1; then
    echo "gnome-terminal not found" >&2
    exit 1
  fi
  echo "ok"
  exit 0
fi

if [[ -z "${DISPLAY:-}" && -z "${WAYLAND_DISPLAY:-}" ]]; then
  echo "No GUI display detected (DISPLAY/WAYLAND_DISPLAY not set)." >&2
  exit 1
fi

if ! command -v gnome-terminal >/dev/null 2>&1; then
  echo "gnome-terminal not found. Install it or use another sudo workflow." >&2
  exit 1
fi

case "$cmd_mode" in
  string)
    if [[ -z "$cmd_string" ]]; then
      echo "--cmd requires a non-empty command string." >&2
      exit 64
    fi
    ;;
  args)
    if [[ ${#cmd_args[@]} -eq 0 ]]; then
      echo "Command args required after --" >&2
      exit 64
    fi
    ;;
  *)
    echo "Must provide --cmd or -- <command>" >&2
    usage >&2
    exit 64
    ;;
esac

tmpdir=$(mktemp -d -t codex-sudo-gnome-terminal.XXXXXX)
out_file="$tmpdir/stdout"
err_file="$tmpdir/stderr"
status_file="$tmpdir/status"
log_file="$tmpdir/command.log"
inner_script="$tmpdir/inner.sh"
keep_logs="${CODEX_SUDO_TERMINAL_KEEP_LOGS:-}"

cleanup() {
  if [[ "$keep_logs" == "1" ]]; then
    echo "Codex sudo logs kept at $tmpdir" >&2
    return
  fi
  rm -rf "$tmpdir"
}
trap cleanup EXIT

if [[ "$cmd_mode" == "string" ]]; then
  display_cmd="$cmd_string"
else
  printf -v display_cmd '%q ' "${cmd_args[@]}"
  display_cmd="${display_cmd% }"
fi

cat > "$inner_script" <<'INNER'
#!/usr/bin/env bash
set -uo pipefail

out_file="${CODEX_OUT_FILE:-}"
err_file="${CODEX_ERR_FILE:-}"
status_file="${CODEX_STATUS_FILE:-}"
log_file="${CODEX_LOG_FILE:-}"
cmd_mode="${CODEX_CMD_MODE:-}"
cmd_string="${CODEX_CMD_STRING:-}"
cmd_display="${CODEX_CMD_DISPLAY:-}"
interactive="${CODEX_INTERACTIVE:-0}"

{
  echo "Codex privileged command:"
  echo "$cmd_display"
} > "$log_file"

color_title="\033[1;36m"
color_cmd="\033[1;33m"
color_reset="\033[0m"
printf '%b\n' "${color_title}Codex privileged command:${color_reset}"
printf '%b\n' "${color_cmd}${cmd_display}${color_reset}"
printf '\n'
echo "Codex: running privileged command in this terminal."
echo "If prompted, enter your password."

set +e
if [[ "$interactive" == "1" ]]; then
  if [[ "$cmd_mode" == "string" ]]; then
    bash -lc "$cmd_string" 2> >(tee "$err_file" >&2)
    rc=$?
  else
    "$@" 2> >(tee "$err_file" >&2)
    rc=$?
  fi
else
  if [[ "$cmd_mode" == "string" ]]; then
    bash -lc "$cmd_string" > >(tee "$out_file") 2> >(tee "$err_file" >&2)
    rc=$?
  else
    "$@" > >(tee "$out_file") 2> >(tee "$err_file" >&2)
    rc=$?
  fi
fi
printf "%s" "$rc" > "$status_file"
exit "$rc"
INNER

chmod +x "$inner_script"

export CODEX_OUT_FILE="$out_file"
export CODEX_ERR_FILE="$err_file"
export CODEX_STATUS_FILE="$status_file"
export CODEX_LOG_FILE="$log_file"
export CODEX_CMD_MODE="$cmd_mode"
export CODEX_CMD_STRING="$cmd_string"
export CODEX_CMD_DISPLAY="$display_cmd"
export CODEX_INTERACTIVE="$interactive"

term_title="${CODEX_SUDO_TERMINAL_TITLE:-Codex sudo}"

set +e
term_pid=""
term_rc=1

on_interrupt() {
  if [[ -n "$term_pid" ]] && kill -0 "$term_pid" 2>/dev/null; then
    kill "$term_pid" 2>/dev/null || true
    sleep 0.5
    if kill -0 "$term_pid" 2>/dev/null; then
      kill -9 "$term_pid" 2>/dev/null || true
    fi
  fi
  exit 130
}

trap on_interrupt INT TERM HUP

if [[ "$cmd_mode" == "string" ]]; then
  gnome-terminal --title "$term_title" --wait -- "$inner_script" &
  term_pid=$!
else
  gnome-terminal --title "$term_title" --wait -- "$inner_script" "${cmd_args[@]}" &
  term_pid=$!
fi

wait "$term_pid"
term_rc=$?

trap - INT TERM HUP
set -e

rc="$term_rc"
if [[ -f "$status_file" ]]; then
  rc=$(cat "$status_file")
fi

if [[ -f "$out_file" ]]; then
  cat "$out_file"
fi

if [[ -f "$err_file" ]]; then
  cat "$err_file" >&2
fi

exit "${rc:-1}"
