#!/bin/bash
# Run eval: skill-200/free-specified
set -e
cd "$(dirname "$0")/../.."
python run.py cli \
    --config config/eval/skill-200/config-free-specified.yaml \
    --task config/eval/skill-200/batch-free-specified.yaml \
    "$@"
