#!/bin/bash
# Run eval: skill-200/dag-plan-2
set -e
cd "$(dirname "$0")/../.."
python run.py cli \
    --config config/eval/skill-200/config-dag-plan-2.yaml \
    --task config/eval/skill-200/batch-dag-plan-2.yaml \
    "$@"
