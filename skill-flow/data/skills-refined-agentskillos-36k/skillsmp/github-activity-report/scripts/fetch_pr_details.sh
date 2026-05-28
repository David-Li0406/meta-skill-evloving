#!/bin/bash

# GitHub PR Details Fetcher
# Organization/ユーザーのマージ済みPR詳細を取得し、JSONファイルに出力する
# Usage: ./fetch_pr_details.sh <org_name> [--mock]

set -e

# 引数チェック
if [[ -z "$1" ]]; then
    echo "Usage: $0 <org_name> [--mock]" >&2
    echo "  org_name: Organization名 または ユーザー名" >&2
    echo "  --mock: モックモードで実行（テスト用）" >&2
    exit 1
fi

ORG="$1"

# モックモードフラグ
MOCK_MODE=false
MOCK_DATA_DIR="${MOCK_DATA_DIR:-}"

# 環境変数からモックデータディレクトリが設定されている場合
if [[ -n "$MOCK_DATA_DIR" ]]; then
    MOCK_MODE=true
fi

# 引数処理
shift
while [[ $# -gt 0 ]]; do
    case $1 in
        --mock)
            MOCK_MODE=true
            shift
            ;;
        *)
            shift
            ;;
    esac
done

# 設定
ONE_YEAR_AGO=$(date -v-1y +%Y-%m-%d 2>/dev/null || date -d "1 year ago" +%Y-%m-%d)
TODAY=$(date +%Y-%m-%d)

# スクリプトのディレクトリを基準に出力先を決定
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
OUTPUT_DIR="${SKILL_DIR}/tests/tmp"
mkdir -p "$OUTPUT_DIR"
OUTPUT_FILE="${OUTPUT_DIR}/pr_details_${ORG}_${TODAY}.json"

# 一時ファイル
TEMP_DIR=$(mktemp -d)
trap "rm -rf $TEMP_DIR" EXIT

# ユーザー名を取得
get_username() {
    if [[ "$MOCK_MODE" == "true" && -f "$MOCK_DATA_DIR/user.json" ]]; then
        jq -r '.login' "$MOCK_DATA_DIR/user.json"
    else
        gh api /user --jq '.login'
    fi
}

# マージ済みPRを検索
search_merged_prs() {
    local user="$1"
    local query="is:pr is:merged author:${user} org:${ORG} merged:>=${ONE_YEAR_AGO}"

    if [[ "$MOCK_MODE" == "true" && -f "$MOCK_DATA_DIR/search_prs.json" ]]; then
        cat "$MOCK_DATA_DIR/search_prs.json"
    else
        gh api "search/issues?q=$(echo "$query" | jq -sRr @uri)&per_page=100&sort=updated&order=desc" \
            --paginate 2>/dev/null || echo '{"items":[]}'
    fi
}

# PRの詳細を取得
get_pr_details() {
    local repo="$1"
    local pr_number="$2"

    if [[ "$MOCK_MODE" == "true" && -f "$MOCK_DATA_DIR/pr_${pr_number}.json" ]]; then
        cat "$MOCK_DATA_DIR/pr_${pr_number}.json"
    else
        gh api "repos/${repo}/pulls/${pr_number}" 2>/dev/null || echo '{}'
    fi
}

# PRの変更ファイル一覧を取得
get_pr_files() {
    local repo="$1"
    local pr_number="$2"

    if [[ "$MOCK_MODE" == "true" && -f "$MOCK_DATA_DIR/pr_${pr_number}_files.json" ]]; then
        cat "$MOCK_DATA_DIR/pr_${pr_number}_files.json"
    else
        gh api "repos/${repo}/pulls/${pr_number}/files" --paginate 2>/dev/null | jq '[.[].filename]' || echo '[]'
    fi
}

# リリースPR/RevertPRをフィルタリング
is_excluded_pr() {
    local title="$1"

    # リリースPRを除外（Release, release, RELEASE で始まるもの）
    if echo "$title" | grep -qiE "^Release"; then
        return 0
    fi

    # RevertPRを除外
    if echo "$title" | grep -qE "^Revert "; then
        return 0
    fi

    return 1
}

# メイン処理
main() {
    echo "Fetching user information..." >&2
    local user
    user=$(get_username)
    echo "User: $user" >&2

    echo "Searching merged PRs in ${ORG}..." >&2
    local search_result
    search_result=$(search_merged_prs "$user")

    # PRアイテムを抽出
    local items
    items=$(echo "$search_result" | jq -c '.items // []')

    local total_count
    total_count=$(echo "$items" | jq 'length')
    echo "Found $total_count PRs (before filtering)" >&2

    # 結果を格納する配列
    echo "[]" > "$TEMP_DIR/results.json"

    local processed=0
    local filtered=0

    echo "$items" | jq -c '.[]' | while read -r pr; do
        local number title repo_url merged_at

        number=$(echo "$pr" | jq -r '.number')
        title=$(echo "$pr" | jq -r '.title')
        repo_url=$(echo "$pr" | jq -r '.repository_url')

        # リポジトリ名を抽出（https://api.github.com/repos/owner/repo -> owner/repo）
        local repo
        repo=$(echo "$repo_url" | sed 's|https://api.github.com/repos/||')

        # リリースPR/RevertPRを除外
        if is_excluded_pr "$title"; then
            echo "  Skipping (excluded): $title" >&2
            filtered=$((filtered + 1))
            continue
        fi

        echo "  Fetching PR #${number}: $title" >&2

        # PR詳細を取得
        local details
        details=$(get_pr_details "$repo" "$number")

        # ファイル一覧を取得
        local files
        files=$(get_pr_files "$repo" "$number")

        # 結果オブジェクトを作成
        local result
        result=$(jq -n \
            --arg number "$number" \
            --arg title "$title" \
            --arg repo "$repo" \
            --argjson details "$details" \
            --argjson files "$files" \
            '{
                number: ($number | tonumber),
                title: $title,
                repo: $repo,
                merged_at: $details.merged_at,
                html_url: $details.html_url,
                body: $details.body,
                additions: $details.additions,
                deletions: $details.deletions,
                changed_files: $details.changed_files,
                files: $files
            }')

        # 結果を追加
        jq --argjson new_pr "$result" '. += [$new_pr]' "$TEMP_DIR/results.json" > "$TEMP_DIR/results_new.json"
        mv "$TEMP_DIR/results_new.json" "$TEMP_DIR/results.json"

        processed=$((processed + 1))
    done

    # 日付順（新しい順）にソート
    jq 'sort_by(.merged_at) | reverse' "$TEMP_DIR/results.json" > "$OUTPUT_FILE"

    local final_count
    final_count=$(jq 'length' "$OUTPUT_FILE")

    echo "" >&2
    echo "Complete!" >&2
    echo "  Total PRs found: $total_count" >&2
    echo "  PRs after filtering: $final_count" >&2
    echo "  Output: $OUTPUT_FILE" >&2
}

main "$@"
