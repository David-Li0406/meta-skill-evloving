#!/bin/bash
NAME="$1"
PERCENT="$2"
cat <<EOF
{
  "name": "${NAME}",
  "expression": "random < ${PERCENT}",
  "tagColor": "BLUE"
}
EOF
