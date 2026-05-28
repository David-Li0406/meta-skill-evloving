#!/bin/bash

set -euo pipefail

SCRIPT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_ROOT}/.." && pwd)"
FORMAT_SCRIPT="${SCRIPT_ROOT}/swift-format.sh"

if [ ! -x "${FORMAT_SCRIPT}" ]; then
    echo "SwiftFormat: ${FORMAT_SCRIPT} is missing or not executable." >&2
    exit 1
fi

if ! command -v git >/dev/null 2>&1; then
    echo "SwiftFormat: git is not available; skipping formatting." >&2
    exit 0
fi

cd "${REPO_ROOT}"

declare -a CANDIDATES=()

append_candidates() {
    while IFS= read -r file; do
        [[ -z "${file}" ]] && continue
        CANDIDATES+=("${file}")
    done
}

# Unstaged tracked changes.
append_candidates < <(git diff --name-only --diff-filter=ACMR -- '*.swift' || true)

# Staged tracked changes (if HEAD exists).
if git rev-parse --verify HEAD >/dev/null 2>&1; then
    append_candidates < <(git diff --cached --name-only --diff-filter=ACMR -- '*.swift' || true)
fi

# Untracked files.
append_candidates < <(git ls-files --others --exclude-standard -- '*.swift' || true)

declare -a FILES=()

if [ "${#CANDIDATES[@]}" -gt 0 ]; then
    while IFS= read -r file; do
        [[ -z "${file}" ]] && continue
        [[ ! -f "${file}" ]] && continue
        FILES+=("${file}")
    done < <(printf '%s\n' "${CANDIDATES[@]}" | awk 'length' | sort -u)
fi

if [ "${#FILES[@]}" -eq 0 ]; then
    echo "SwiftFormat: no changed Swift files detected; skipping."
    exit 0
fi

echo "SwiftFormat: formatting ${#FILES[@]} changed file(s)."
"${FORMAT_SCRIPT}" "${FILES[@]}"
