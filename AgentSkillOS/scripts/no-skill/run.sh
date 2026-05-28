#!/bin/bash
# Run eval: no-skill
set -e
cd "$(dirname "$0")/../.."
python run.py cli \
    --config config/eval/no-skill/config.yaml \
    --task config/eval/no-skill/batch.yaml \
    "$@"
