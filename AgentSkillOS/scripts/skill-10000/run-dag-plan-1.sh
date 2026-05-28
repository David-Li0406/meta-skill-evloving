#!/bin/bash
# Run eval: skill-10000/dag-plan-1
set -e
cd "$(dirname "$0")/../.."
python run.py cli \
    --config config/eval/skill-10000/config-dag-plan-1.yaml \
    --task config/eval/skill-10000/batch-dag-plan-1.yaml \
    "$@"
