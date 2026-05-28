#!/bin/bash
# Run eval: skill-200/tree-free-style
set -e
cd "$(dirname "$0")/../.."
python run.py cli \
    --config config/eval/skill-200/config-tree-free-style.yaml \
    --task config/eval/skill-200/batch-tree-free-style.yaml \
    "$@"
