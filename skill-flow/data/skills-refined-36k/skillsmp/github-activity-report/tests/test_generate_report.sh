#!/bin/bash

# テスト用スクリプト: generate_report.shの出力フォーマットを検証する

# set -e を使わない（テストカウンタの算術演算でエラーになるため）

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
SCRIPT_PATH="$PROJECT_DIR/scripts/generate_report.sh"
TEST_OUTPUT_DIR="$SCRIPT_DIR/tmp"
TEST_OUTPUT_FILE="$TEST_OUTPUT_DIR/github-activity.md"

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

    # モックリポジトリデータを作成
    cat > "$MOCK_DATA_DIR/repos.json" << 'EOF'
[
  {
    "name": "agent-skills",
    "full_name": "testuser/agent-skills",
    "private": false,
    "owner": { "login": "testuser" }
  },
  {
    "name": "private-project",
    "full_name": "testuser/private-project",
    "private": true,
    "owner": { "login": "testuser" }
  }
]
EOF

    # モックコミットデータを作成（agent-skills）
    cat > "$MOCK_DATA_DIR/commits_agent-skills.json" << 'EOF'
[
  {
    "sha": "47c199e1234567890abcdef",
    "commit": {
      "message": "add new feature",
      "author": {
        "date": "2026-01-23T10:30:00Z"
      }
    }
  },
  {
    "sha": "abc1234567890abcdef1234",
    "commit": {
      "message": "fix bug",
      "author": {
        "date": "2026-01-22T15:00:00Z"
      }
    }
  }
]
EOF

    # モックコミットデータを作成（private-project）
    cat > "$MOCK_DATA_DIR/commits_private-project.json" << 'EOF'
[
  {
    "sha": "def5678901234567890abc",
    "commit": {
      "message": "initial commit",
      "author": {
        "date": "2025-12-15T09:00:00Z"
      }
    }
  }
]
EOF
}

# クリーンアップ
cleanup() {
    rm -rf "$TEST_OUTPUT_DIR"
}

# テストヘルパー関数
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
    assert_file_exists "$SCRIPT_PATH" "generate_report.sh should exist"
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

# テスト3: モックモードでの出力形式確認
test_output_format_with_mock() {
    echo "=== Test: Output format with mock data ==="

    # モックモードでスクリプトを実行
    cd "$TEST_OUTPUT_DIR"
    MOCK_DATA_DIR="$MOCK_DATA_DIR" bash "$SCRIPT_PATH" --mock 2>/dev/null || true

    if [[ ! -f "$TEST_OUTPUT_FILE" ]]; then
        echo -e "${RED}✗ FAIL${NC}: Output file should be created"
        TESTS_FAILED=$((TESTS_FAILED + 1))
        return
    fi

    local content
    content=$(cat "$TEST_OUTPUT_FILE")

    # ヘッダーの確認
    assert_contains "$content" "# GitHub Activity Report" "Should have title"

    # サマリーセクションの確認
    assert_contains "$content" "## Summary" "Should have Summary section"
    assert_contains "$content" "Total Commits:" "Should show total commits"
    assert_contains "$content" "Repositories:" "Should show repository count"

    # タイムラインセクションの確認
    assert_contains "$content" "## Timeline" "Should have Timeline section"

    # 月セクションの確認
    assert_contains "$content" "### 2026-01" "Should have month section"

    # 日付エントリの確認
    assert_contains "$content" "#### 2026-01-23" "Should have date entry"

    # コミットエントリの確認
    assert_contains "$content" "agent-skills" "Should contain repository name"
    assert_contains "$content" "47c199e" "Should contain short commit hash"
}

# テスト4: 時系列ソートの確認
test_chronological_order() {
    echo "=== Test: Chronological order (newest first) ==="

    if [[ ! -f "$TEST_OUTPUT_FILE" ]]; then
        echo -e "${RED}✗ SKIP${NC}: Output file not found"
        TESTS_FAILED=$((TESTS_FAILED + 1))
        return
    fi

    local content
    content=$(cat "$TEST_OUTPUT_FILE")

    # 2026-01が2025-12より前に来ているか確認
    local pos_2026_01 pos_2025_12
    pos_2026_01=$(echo "$content" | grep -n "### 2026-01" | head -1 | cut -d: -f1)
    pos_2025_12=$(echo "$content" | grep -n "### 2025-12" | head -1 | cut -d: -f1)

    if [[ -n "$pos_2026_01" && -n "$pos_2025_12" && "$pos_2026_01" -lt "$pos_2025_12" ]]; then
        echo -e "${GREEN}✓ PASS${NC}: Newer months should appear before older months"
        TESTS_PASSED=$((TESTS_PASSED + 1))
    else
        echo -e "${RED}✗ FAIL${NC}: Newer months should appear before older months"
        TESTS_FAILED=$((TESTS_FAILED + 1))
    fi
}

# テスト5: プライベートリポジトリの表示
test_private_repo_indicator() {
    echo "=== Test: Private repository indicator ==="

    if [[ ! -f "$TEST_OUTPUT_FILE" ]]; then
        echo -e "${RED}✗ SKIP${NC}: Output file not found"
        TESTS_FAILED=$((TESTS_FAILED + 1))
        return
    fi

    local content
    content=$(cat "$TEST_OUTPUT_FILE")

    # public/privateの表示確認
    assert_contains "$content" "(public)" "Should show (public) for public repos"
    assert_contains "$content" "(private)" "Should show (private) for private repos"
}

# メイン実行
main() {
    echo "========================================"
    echo "Running tests for generate_report.sh"
    echo "========================================"
    echo ""

    setup

    test_script_exists
    echo ""
    test_script_executable
    echo ""
    test_output_format_with_mock
    echo ""
    test_chronological_order
    echo ""
    test_private_repo_indicator
    echo ""

    echo "========================================"
    echo "Test Results: $TESTS_PASSED passed, $TESTS_FAILED failed"
    echo "========================================"

    # cleanup

    if [[ $TESTS_FAILED -gt 0 ]]; then
        exit 1
    fi
}

main "$@"
