#!/bin/bash
TEMPLATE="$1"
KEY="$2"
OUT="$3"
jq "del(.parameters[\"${KEY}\"])" "$TEMPLATE" > "$OUT"
