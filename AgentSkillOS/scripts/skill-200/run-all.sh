#!/bin/bash
# Run all eval modes for skill-200
set -e
cd "$(dirname "$0")"
for script in run-free-style.sh run-tree-free-style.sh run-dag-plan-{0..4}.sh run-free-specified.sh run-dag-specified-0.sh; do
    bash "$script" "$@"
done
