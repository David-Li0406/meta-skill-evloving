#!/usr/bin/env bash
# Initialize a new Continuity Ledger in the current directory

LEDGER_FILE="CONTINUITY.md"

if [ -f "$LEDGER_FILE" ]; then
    echo "Ledger already exists."
    exit 0
fi

cat <<EOF > "$LEDGER_FILE"
# Continuity Ledger

## Project Goal

- **Objective**:
- **Success Criteria**:

## Context & Constraints

- **Tech Stack**:
- **Constraints**:

## Key Decisions

## Execution State

- **Done**:

- **Now**:

- **Next**:

## Open Questions (UNCONFIRMED)

## Working Set

- **Files**:

- **Commands**:

EOF

echo "Initialized $LEDGER_FILE"
