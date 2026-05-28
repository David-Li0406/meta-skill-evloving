#!/bin/bash
# Run eval: skill-10000/dag-specified-0
set -e
cd "$(dirname "$0")/../.."
python run.py cli \
    --config config/eval/skill-10000/config-dag-specified-0.yaml \
    --task config/eval/skill-10000/batch-dag-specified-0.yaml \
    "$@"
