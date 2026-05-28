#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(CDPATH= cd -- "$(dirname "$0")/.." && pwd)"
PYTHON_BIN="${PYTHON_BIN:-python3}"
VENV_DIR="${SKILLCLAW_VENV_DIR:-$ROOT_DIR/.venv}"
INSTALL_EXTRAS="${SKILLCLAW_INSTALL_EXTRAS:-evolve,sharing,server}"
RUN_SETUP=0
RUN_START=0

usage() {
  cat <<EOF
Usage: $(basename "$0") [--venv-dir PATH] [--python BIN] [--extras LIST] [--run-setup] [--run-start]

Installs SkillClaw from the current repository checkout into a local virtualenv.

Examples:
  bash scripts/install_skillclaw.sh
  bash scripts/install_skillclaw.sh --venv-dir ~/.venvs/skillclaw --run-setup
  bash scripts/install_skillclaw.sh --extras all --run-setup --run-start

Default install command:
  python -m pip install -e ".[evolve,sharing,server]"

After install you can run:
  skillclaw setup
  skillclaw start

If you also plan to use the agent evolve server, install OpenClaw separately:
  npm install -g openclaw
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --venv-dir)
      VENV_DIR="$2"
      shift 2
      ;;
    --python)
      PYTHON_BIN="$2"
      shift 2
      ;;
    --extras)
      INSTALL_EXTRAS="$2"
      shift 2
      ;;
    --run-setup)
      RUN_SETUP=1
      shift
      ;;
    --run-start)
      RUN_START=1
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown argument: $1" >&2
      usage >&2
      exit 2
      ;;
  esac
done

if ! command -v "$PYTHON_BIN" >/dev/null 2>&1; then
  echo "Python executable not found: $PYTHON_BIN" >&2
  exit 1
fi

echo "[install_skillclaw] repo root: $ROOT_DIR"
echo "[install_skillclaw] python: $PYTHON_BIN"
echo "[install_skillclaw] venv: $VENV_DIR"
echo "[install_skillclaw] extras: $INSTALL_EXTRAS"

cd "$ROOT_DIR"
"$PYTHON_BIN" -m venv "$VENV_DIR"
# shellcheck disable=SC1090
source "$VENV_DIR/bin/activate"

python -m pip install -U pip
python -m pip install -e ".[${INSTALL_EXTRAS}]"

echo
echo "[install_skillclaw] install complete"
echo "[install_skillclaw] activate with:"
echo "  source \"$VENV_DIR/bin/activate\""
echo "[install_skillclaw] next steps:"
echo "  skillclaw setup"
echo "  skillclaw start"

if [[ "$RUN_SETUP" -eq 1 ]]; then
  echo
  echo "[install_skillclaw] running: skillclaw setup"
  skillclaw setup
fi

if [[ "$RUN_START" -eq 1 ]]; then
  echo
  echo "[install_skillclaw] running: skillclaw start"
  skillclaw start
fi
