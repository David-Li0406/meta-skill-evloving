#!/bin/bash

# テスト用スクリプト: fetch_pr_details.shの出力フォーマットを検証する

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
SCRIPT_PATH="$PROJECT_DIR/scripts/fetch_pr_details.sh"
TEST_OUTPUT_DIR="$SCRIPT_DIR/tmp"

# カラー出力
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

# テスト用のモックデータディレクトリ
MOCK_DATA_DIR="$SCRIPT_DIR/mock_data"

# テスト結果カウンタ
TESTS_PASSED=0
TESTS_FAILED=0

# セットアップ
setup() {
    mkdir -p "$TEST_OUTPUT_DIR"
    mkdir -p "$MOCK_DATA_DIR"

    # モックユーザーデータを作成
    cat > "$MOCK_DATA_DIR/user.json" << 'EOF'
{
  "login": "testuser"
}
EOF

    # モックPR検索結果を作成（マージ済みPR一覧）
    cat > "$MOCK_DATA_DIR/search_prs.json" << 'EOF'
{
  "total_count": 4,
  "items": [
    {
      "number": 101,
      "title": "[機能A] 新しいボタンを追加",
      "state": "closed",
      "merged_at": "2026-01-15T10:00:00Z",
      "html_url": "https://github.com/test-org/repo1/pull/101",
      "user": { "login": "testuser" },
      "repository_url": "https://api.github.com/repos/test-org/repo1",
      "body": "## 概要\n新しいボタンを追加しました。"
    },
    {
      "number": 102,
      "title": "Release v1.0.0",
      "state": "closed",
      "merged_at": "2026-01-14T10:00:00Z",
      "html_url": "https://github.com/test-org/repo1/pull/102",
      "user": { "login": "testuser" },
      "repository_url": "https://api.github.com/repos/test-org/repo1",
      "body": "Release notes"
    },
    {
      "number": 103,
      "title": "Revert \"[機能A] 新しいボタンを追加\"",
      "state": "closed",
      "merged_at": "2026-01-13T10:00:00Z",
      "html_url": "https://github.com/test-org/repo1/pull/103",
      "user": { "login": "testuser" },
      "repository_url": "https://api.github.com/repos/test-org/repo1",
      "body": "Revert the button change"
    },
    {
      "number": 104,
      "title": "[機能B] フォーム改善",
      "state": "closed",
      "merged_at": "2025-12-20T10:00:00Z",
      "html_url": "https://github.com/test-org/repo2/pull/104",
      "user": { "login": "testuser" },
      "repository_url": "https://api.github.com/repos/test-org/repo2",
      "body": "フォームのUI改善"
    }
  ]
}
EOF

    # モックPR詳細データを作成（PR 101）
    cat > "$MOCK_DATA_DIR/pr_101.json" << 'EOF'
{
  "number": 101,
  "title": "[機能A] 新しいボタンを追加",
  "state": "closed",
  "merged_at": "2026-01-15T10:00:00Z",
  "html_url": "https://github.com/test-org/repo1/pull/101",
  "user": { "login": "testuser" },
  "body": "## 概要\n新しいボタンを追加しました。",
  "additions": 150,
  "deletions": 30,
  "changed_files": 5
}
EOF

    # モックPR詳細データを作成（PR 104）
    cat > "$MOCK_DATA_DIR/pr_104.json" << 'EOF'
{
  "number": 104,
  "title": "[機能B] フォーム改善",
  "state": "closed",
  "merged_at": "2025-12-20T10:00:00Z",
  "html_url": "https://github.com/test-org/repo2/pull/104",
  "user": { "login": "testuser" },
  "body": "フォームのUI改善",
  "additions": 200,
  "deletions": 50,
  "changed_files": 3
}
EOF

    # モックPRファイル一覧（PR 101）
    cat > "$MOCK_DATA_DIR/pr_101_files.json" << 'EOF'
[
  {"filename": "src/components/Button.tsx"},
  {"filename": "src/components/Button.test.tsx"},
  {"filename": "src/styles/button.css"}
]
EOF

    # モックPRファイル一覧（PR 104）
    cat > "$MOCK_DATA_DIR/pr_104_files.json" << 'EOF'
[
  {"filename": "src/features/form/Form.tsx"},
  {"filename": "src/features/form/Form.test.tsx"}
]
EOF
}

# クリーンアップ
cleanup() {
    rm -f "$TEST_OUTPUT_DIR/pr_details_test-org.json"
}

# テストヘルパー関数
assert_equals() {
    local actual="$1"
    local expected="$2"
    local test_name="$3"

    if [[ "$actual" == "$expected" ]]; then
        echo -e "${GREEN}✓ PASS${NC}: $test_name"
        TESTS_PASSED=$((TESTS_PASSED + 1))
    else
        echo -e "${RED}✗ FAIL${NC}: $test_name"
        echo "  Expected: $expected"
        echo "  Actual:   $actual"
        TESTS_FAILED=$((TESTS_FAILED + 1))
    fi
}

assert_contains() {
    local content="$1"
    local expected="$2"
    local test_name="$3"

    if echo "$content" | grep -qF "$expected"; then
        echo -e "${GREEN}✓ PASS${NC}: $test_name"
        TESTS_PASSED=$((TESTS_PASSED + 1))
    else
        echo -e "${RED}✗ FAIL${NC}: $test_name"
        echo "  Expected to contain: $expected"
        TESTS_FAILED=$((TESTS_FAILED + 1))
    fi
}

assert_not_contains() {
    local content="$1"
    local not_expected="$2"
    local test_name="$3"

    if ! echo "$content" | grep -qF "$not_expected"; then
        echo -e "${GREEN}✓ PASS${NC}: $test_name"
        TESTS_PASSED=$((TESTS_PASSED + 1))
    else
        echo -e "${RED}✗ FAIL${NC}: $test_name"
        echo "  Should NOT contain: $not_expected"
        TESTS_FAILED=$((TESTS_FAILED + 1))
    fi
}

assert_file_exists() {
    local file="$1"
    local test_name="$2"

    if [[ -f "$file" ]]; then
        echo -e "${GREEN}✓ PASS${NC}: $test_name"
        TESTS_PASSED=$((TESTS_PASSED + 1))
    else
        echo -e "${RED}✗ FAIL${NC}: $test_name"
        echo "  File not found: $file"
        TESTS_FAILED=$((TESTS_FAILED + 1))
    fi
}

# テスト1: スクリプトが存在するか
test_script_exists() {
    echo "=== Test: Script exists ==="
    assert_file_exists "$SCRIPT_PATH" "fetch_pr_details.sh should exist"
}

# テスト2: スクリプトが実行可能か
test_script_executable() {
    echo "=== Test: Script is executable ==="
    if [[ -x "$SCRIPT_PATH" ]]; then
        echo -e "${GREEN}✓ PASS${NC}: Script should be executable"
        TESTS_PASSED=$((TESTS_PASSED + 1))
    else
        echo -e "${RED}✗ FAIL${NC}: Script should be executable"
        TESTS_FAILED=$((TESTS_FAILED + 1))
    fi
}

# テスト3: 引数なしの場合のエラー
test_no_argument_error() {
    echo "=== Test: No argument error ==="

    local output
    output=$(bash "$SCRIPT_PATH" 2>&1) || true

    assert_contains "$output" "Usage:" "Should show usage message when no argument"
}

# テスト4: モックモードでの出力形式確認
test_output_format_with_mock() {
    echo "=== Test: Output format with mock data ==="

    cd "$TEST_OUTPUT_DIR"
    MOCK_DATA_DIR="$MOCK_DATA_DIR" bash "$SCRIPT_PATH" test-org --mock 2>/dev/null || true

    local output_file="$TEST_OUTPUT_DIR/pr_details_test-org.json"
    assert_file_exists "$output_file" "Output file should be created"

    if [[ ! -f "$output_file" ]]; then
        return
    fi

    local content
    content=$(cat "$output_file")

    # JSON形式の確認
    if jq empty "$output_file" 2>/dev/null; then
        echo -e "${GREEN}✓ PASS${NC}: Output should be valid JSON"
        TESTS_PASSED=$((TESTS_PASSED + 1))
    else
        echo -e "${RED}✗ FAIL${NC}: Output should be valid JSON"
        TESTS_FAILED=$((TESTS_FAILED + 1))
        return
    fi

    # 必要なフィールドの確認
    local has_title has_merged_at has_additions has_files
    has_title=$(jq '.[0] | has("title")' "$output_file")
    has_merged_at=$(jq '.[0] | has("merged_at")' "$output_file")
    has_additions=$(jq '.[0] | has("additions")' "$output_file")
    has_files=$(jq '.[0] | has("files")' "$output_file")

    assert_equals "$has_title" "true" "PR should have title field"
    assert_equals "$has_merged_at" "true" "PR should have merged_at field"
    assert_equals "$has_additions" "true" "PR should have additions field"
    assert_equals "$has_files" "true" "PR should have files field"
}

# テスト5: リリースPRとRevertが除外されるか
test_exclude_release_and_revert() {
    echo "=== Test: Exclude release and revert PRs ==="

    local output_file="$TEST_OUTPUT_DIR/pr_details_test-org.json"
    if [[ ! -f "$output_file" ]]; then
        echo -e "${RED}✗ SKIP${NC}: Output file not found"
        TESTS_FAILED=$((TESTS_FAILED + 1))
        return
    fi

    local content
    content=$(cat "$output_file")

    # リリースPRが除外されていることを確認
    assert_not_contains "$content" "Release v1.0.0" "Should exclude release PR"

    # RevertPRが除外されていることを確認
    assert_not_contains "$content" "Revert \"" "Should exclude revert PR"

    # 通常のPRは含まれていることを確認
    assert_contains "$content" "[機能A] 新しいボタンを追加" "Should include normal PR"
    assert_contains "$content" "[機能B] フォーム改善" "Should include normal PR"
}

# テスト6: PR数が正しいか（フィルタ後）
test_filtered_pr_count() {
    echo "=== Test: Filtered PR count ==="

    local output_file="$TEST_OUTPUT_DIR/pr_details_test-org.json"
    if [[ ! -f "$output_file" ]]; then
        echo -e "${RED}✗ SKIP${NC}: Output file not found"
        TESTS_FAILED=$((TESTS_FAILED + 1))
        return
    fi

    local count
    count=$(jq 'length' "$output_file")

    # 4件中2件（リリースとRevertを除外）
    assert_equals "$count" "2" "Should have 2 PRs after filtering"
}

# メイン実行
main() {
    echo "========================================"
    echo "Running tests for fetch_pr_details.sh"
    echo "========================================"
    echo ""

    setup

    test_script_exists
    echo ""
    test_script_executable
    echo ""
    test_no_argument_error
    echo ""
    test_output_format_with_mock
    echo ""
    test_exclude_release_and_revert
    echo ""
    test_filtered_pr_count
    echo ""

    cleanup

    echo "========================================"
    echo "Test Results: $TESTS_PASSED passed, $TESTS_FAILED failed"
    echo "========================================"

    if [[ $TESTS_FAILED -gt 0 ]]; then
        exit 1
    fi
}

main "$@"
