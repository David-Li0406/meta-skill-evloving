#!/bin/bash
# Run all eval configurations: no-skill + 3 tree sizes
set -e
cd "$(dirname "$0")"
bash no-skill/run.sh "$@"
for tree in skill-200 skill-1000 skill-10000; do
    bash "$tree/run-all.sh" "$@"
done
