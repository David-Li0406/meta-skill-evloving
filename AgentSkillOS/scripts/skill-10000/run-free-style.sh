#!/bin/bash
# Run eval: skill-10000/free-style
set -e
cd "$(dirname "$0")/../.."
python run.py cli \
    --config config/eval/skill-10000/config-free-style.yaml \
    --task config/eval/skill-10000/batch-free-style.yaml \
    "$@"
