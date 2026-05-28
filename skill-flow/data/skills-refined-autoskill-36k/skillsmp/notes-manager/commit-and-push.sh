#!/bin/bash

# Script to commit and push notes changes using Jujutsu
# Usage: ./commit-and-push.sh "commit description"

if [ -z "$1" ]; then
  echo "Error: Please provide a commit description"
  echo "Usage: $0 \"commit description\""
  exit 1
fi

cd /Users/mthorning/Documents/Notes || exit 1

jj commit -m "$1"
jj bookmark set main -r @-
jj git push -b main
