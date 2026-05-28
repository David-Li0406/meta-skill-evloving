#!/bin/bash
# Run eval: skill-1000/tree-free-style
set -e
cd "$(dirname "$0")/../.."
python run.py cli \
    --config config/eval/skill-1000/config-tree-free-style.yaml \
    --task config/eval/skill-1000/batch-tree-free-style.yaml \
    "$@"
