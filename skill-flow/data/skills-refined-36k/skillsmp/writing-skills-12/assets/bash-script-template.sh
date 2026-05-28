#!/usr/bin/env bash

set -euo pipefail

function print_help() {
  echo "Usage: script-name [options]"
  echo
  echo "Description of what the script does."
  echo
  echo "Options:"
  echo
  echo "  --required <value>    Description of required flag."
  echo "  --optional <value>    Description of optional flag."
  echo "  --help                Show this help message and exit."
}

# Parse arguments
required_flag=""
optional_flag=""

while [[ $# -gt 0 ]]; do
  case "$1" in
  --help)
    print_help
    exit 0
    ;;
  --required)
    required_flag="$2"
    shift 2
    ;;
  --optional)
    optional_flag="$2"
    shift 2
    ;;
  *)
    echo "Error: Unknown option: $1" >&2
    echo >&2
    print_help >&2
    exit 1
    ;;
  esac
done

# Validate required arguments
if [[ -z "$required_flag" ]]; then
  echo "Error: --required is required" >&2
  echo >&2
  print_help >&2
  exit 1
fi

# TODO: Implement script
