#!/usr/bin/env bash

# @describe Example CLI tool
# @env EXAMPLE_FOLDER_PATH="examples/" Path to the examples folder
# @flag -v --verbose Enable verbose output
# @option -f --file Input file
# @option --repo[`_choice_skogai_repos`] <REPO> Optional repository
# @arg file![`_choice_files`] <FILE> Required name argument from the ./examples/ folder

main() {
  if [[ $argc_verbose ]]; then
    echo "PATH TO FILE: ${EXAMPLE_FOLDER_PATH}${argc_file}"
  else
    echo "path to file: ${EXAMPLE_FOLDER_PATH}${argc_file}"
  fi
}

_choice_files() {
  ls -1 "$EXAMPLE_FOLDER_PATH"
}

_choice_skogai_repos() {
  gh repo list skogai --json nameWithOwner --jq ".[].nameWithOwner"
}

eval "$(argc --argc-eval "$0" "$@")"
