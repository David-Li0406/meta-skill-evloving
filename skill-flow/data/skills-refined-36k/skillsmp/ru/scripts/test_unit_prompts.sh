#!/usr/bin/env bash
#
# Unit tests: Prompt generation (bd-prompt)
#
# Tests:
# - generate_digest_prompt
# - generate_review_prompt
#
# shellcheck disable=SC1091
# shellcheck disable=SC2317

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/test_framework.sh"

# Source functions
source_ru_function "generate_digest_prompt"
source_ru_function "generate_review_prompt"

test_generate_digest_prompt() {
    local test_name="generate_digest_prompt: outputs expected text"
    log_test_start "$test_name"

    local output
    output=$(generate_digest_prompt)

    assert_contains "$output" "repo-digest.md" "Should mention repo-digest.md"
    assert_contains "$output" "AGENTS.md" "Should mention AGENTS.md"

    log_test_pass "$test_name"
}

test_generate_review_prompt() {
    local test_name="generate_review_prompt: outputs structured prompt"
    log_test_start "$test_name"

    local items_json='[{"number":1,"title":"Bug"}]'
    local output
    output=$(generate_review_prompt "owner/repo" "/path/to/wt" "run-123" "$items_json")

    assert_contains "$output" "owner/repo" "Should contain repo name"
    assert_contains "$output" "/path/to/wt" "Should contain worktree path"
    assert_contains "$output" "run-123" "Should contain run ID"
    assert_contains "$output" "Bug" "Should contain work items"
    assert_contains "$output" "schema_version: 1" "Should contain schema version"

    log_test_pass "$test_name"
}

run_test test_generate_digest_prompt
run_test test_generate_review_prompt

print_results
