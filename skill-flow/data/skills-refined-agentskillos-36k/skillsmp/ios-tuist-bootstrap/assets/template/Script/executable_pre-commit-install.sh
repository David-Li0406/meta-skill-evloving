#!/bin/sh

# Installs the project's pre-commit hook unless running in CI.

set -eu

log() {
    printf '[pre-commit-install] %s\n' "$1"
}

if [ -n "${CI:-}" ]; then
    log "Detected CI environment (CI=TRUE); skipping pre-commit install."
    exit 0
fi

if ! git rev-parse --git-dir > /dev/null 2>&1; then
    log "Not inside a git repository; skipping pre-commit install."
    exit 0
fi

repo_root="$(git rev-parse --show-toplevel)"
cd "$repo_root"

if ! command -v pre-commit > /dev/null 2>&1; then
    log "pre-commit executable not found on PATH; skipping hook installation."
    exit 0
fi

log "Installing pre-commit hook into '.git/hooks'."
pre-commit install --install-hooks --overwrite
log "pre-commit hook installation complete."
