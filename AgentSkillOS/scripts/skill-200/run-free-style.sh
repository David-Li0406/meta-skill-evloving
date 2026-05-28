#!/bin/bash
# Run eval: skill-200/free-style
set -e
cd "$(dirname "$0")/../.."
python run.py cli \
    --config config/eval/skill-200/config-free-style.yaml \
    --task config/eval/skill-200/batch-free-style.yaml \
    "$@"
