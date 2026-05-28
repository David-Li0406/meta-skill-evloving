#!/bin/bash
# Run eval: skill-1000/dag-plan-2
set -e
cd "$(dirname "$0")/../.."
python run.py cli \
    --config config/eval/skill-1000/config-dag-plan-2.yaml \
    --task config/eval/skill-1000/batch-dag-plan-2.yaml \
    "$@"
