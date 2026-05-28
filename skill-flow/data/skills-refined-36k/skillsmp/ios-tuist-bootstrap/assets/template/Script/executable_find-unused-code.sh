#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'

usage() {
  cat <<'EOF'
Usage: find-unused-code.sh [--include-design] [--help]
Default: excludes Design files that generate noisy reports.
  --include-design   include Design directory in the scan
  --help             show this help text
EOF
}

include_design=false
while [[ $# -gt 0 ]]; do
  case "$1" in
    --include-design) include_design=true ;;
    --help|-h) usage; exit 0 ;;
    *) echo "Unknown argument: $1" >&2; usage >&2; exit 1 ;;
  esac
  shift
done

exclude_args=(--report-exclude "**/Derived/*.swift")

if [[ "$include_design" == false ]]; then
  design_excludes=(
    "**/Design/*Theme*.swift"
    "**/Design/*Palette.swift"
    "**/Design/*Tokens.swift"
  )
  for pattern in "${design_excludes[@]}"; do
    exclude_args+=(--report-exclude "$pattern")
  done
fi

mise exec periphery -- periphery scan --clean-build --relative-results "${exclude_args[@]}" || {
  echo "periphery failed. If it's missing, install it with: mise install periphery" >&2
  exit 1
}
