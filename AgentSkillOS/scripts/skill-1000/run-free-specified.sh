#!/bin/bash
# Run eval: skill-1000/free-specified
set -e
cd "$(dirname "$0")/../.."
python run.py cli \
    --config config/eval/skill-1000/config-free-specified.yaml \
    --task config/eval/skill-1000/batch-free-specified.yaml \
    "$@"
