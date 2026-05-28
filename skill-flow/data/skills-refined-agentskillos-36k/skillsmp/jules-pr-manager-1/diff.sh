#!/bin/bash
ID1=$1
ID2=$2

if [ -z "$ID1" ]; then
  echo "Usage: $0 <id1> [id2]"
  exit 1
fi

if [ -z "$ID2" ]; then
  # Single PR diff
  gh pr diff "$ID1"
else
  # Compare two PRs
  gh pr diff "$ID1" > "$ID1.diff"
  gh pr diff "$ID2" > "$ID2.diff"
  diff -u "$ID1.diff" "$ID2.diff"
  rm "$ID1.diff" "$ID2.diff"
fi
