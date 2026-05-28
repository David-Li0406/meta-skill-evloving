#!/bin/bash
# Run eval: skill-10000/tree-free-style
set -e
cd "$(dirname "$0")/../.."
python run.py cli \
    --config config/eval/skill-10000/config-tree-free-style.yaml \
    --task config/eval/skill-10000/batch-tree-free-style.yaml \
    "$@"
