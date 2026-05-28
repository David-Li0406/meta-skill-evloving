#!/bin/bash

# GitHub Activity Report Generator
# 過去1年間のGitHub活動（コミット履歴）を時系列でMarkdownファイルに出力する

set -e

# 設定
OUTPUT_FILE="github-activity.md"
ONE_YEAR_AGO=$(date -v-1y +%Y-%m-%dT00:00:00Z 2>/dev/null || date -d "1 year ago" +%Y-%m-%dT00:00:00Z)
TODAY=$(date +%Y-%m-%d)

# モックモードフラグ（環境変数を保持）
MOCK_MODE=false
MOCK_DATA_DIR="${MOCK_DATA_DIR:-}"

# 環境変数からモックデータディレクトリが設定されている場合
if [[ -n "$MOCK_DATA_DIR" ]]; then
    MOCK_MODE=true
fi

# 引数処理
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

# 一時ファイル
TEMP_DIR=$(mktemp -d)
COMMITS_FILE="$TEMP_DIR/all_commits.json"
trap "rm -rf $TEMP_DIR" EXIT

# リポジトリ一覧を取得
get_repos() {
    if [[ "$MOCK_MODE" == "true" && -f "$MOCK_DATA_DIR/repos.json" ]]; then
        cat "$MOCK_DATA_DIR/repos.json"
    else
        gh api /user/repos \
            --paginate \
            -q '.[] | {name: .name, full_name: .full_name, private: .private, owner: .owner.login}' \
            2>/dev/null | jq -s '.'
    fi
}

# 特定リポジトリのコミットを取得
get_commits() {
    local repo_name="$1"
    local full_name="$2"
    local is_private="$3"

    if [[ "$MOCK_MODE" == "true" && -f "$MOCK_DATA_DIR/commits_${repo_name}.json" ]]; then
        cat "$MOCK_DATA_DIR/commits_${repo_name}.json" | jq --arg repo "$repo_name" --arg private "$is_private" \
            '[.[] | {
                sha: .sha[0:7],
                message: (.commit.message | split("\n")[0]),
                date: .commit.author.date,
                repo: $repo,
                private: ($private == "true")
            }]'
    else
        gh api "repos/${full_name}/commits?since=${ONE_YEAR_AGO}&per_page=100" \
            --paginate \
            2>/dev/null | jq --arg repo "$repo_name" --arg private "$is_private" \
            '[.[] | {
                sha: .sha[0:7],
                message: (.commit.message | split("\n")[0]),
                date: .commit.author.date,
                repo: $repo,
                private: ($private == "true")
            }]' 2>/dev/null || echo "[]"
    fi
}

# メイン処理
main() {
    echo "Fetching repositories..." >&2

    # リポジトリ一覧を取得
    local repos
    repos=$(get_repos)

    # すべてのコミットを収集
    echo "[]" > "$COMMITS_FILE"

    local repo_count=0
    while read -r repo; do
        local name full_name is_private
        name=$(echo "$repo" | jq -r '.name')
        full_name=$(echo "$repo" | jq -r '.full_name')
        is_private=$(echo "$repo" | jq -r '.private')

        echo "Fetching commits from $name..." >&2

        local commits
        commits=$(get_commits "$name" "$full_name" "$is_private")

        # 既存のコミットとマージ
        jq -s '.[0] + .[1]' "$COMMITS_FILE" <(echo "$commits") > "$TEMP_DIR/merged.json"
        mv "$TEMP_DIR/merged.json" "$COMMITS_FILE"

        repo_count=$((repo_count + 1))
    done < <(echo "$repos" | jq -c '.[]')

    # コミットを日付順（新しい順）にソート
    local sorted_commits
    sorted_commits=$(jq 'sort_by(.date) | reverse' "$COMMITS_FILE")

    # 統計情報を計算
    local total_commits
    total_commits=$(echo "$sorted_commits" | jq 'length')
    local repo_names
    repo_names=$(echo "$sorted_commits" | jq -r '[.[].repo] | unique | length')

    # Markdownを生成
    {
        echo "# GitHub Activity Report (${ONE_YEAR_AGO%T*} 〜 ${TODAY})"
        echo ""
        echo "## Summary"
        echo "- Total Commits: $total_commits"
        echo "- Repositories: $repo_names"
        echo ""
        echo "## Timeline"
        echo ""

        local current_month=""
        local current_date=""

        echo "$sorted_commits" | jq -c '.[]' | while read -r commit; do
            local date sha message repo is_private visibility
            date=$(echo "$commit" | jq -r '.date')
            sha=$(echo "$commit" | jq -r '.sha')
            message=$(echo "$commit" | jq -r '.message')
            repo=$(echo "$commit" | jq -r '.repo')
            is_private=$(echo "$commit" | jq -r '.private')

            # visibility設定
            if [[ "$is_private" == "true" ]]; then
                visibility="private"
            else
                visibility="public"
            fi

            # 月を抽出 (YYYY-MM)
            local month="${date:0:7}"
            # 日付を抽出 (YYYY-MM-DD)
            local day="${date:0:10}"

            # 月が変わったらヘッダーを出力
            if [[ "$month" != "$current_month" ]]; then
                echo ""
                echo "### $month"
                current_month="$month"
                current_date="" # 月が変わったら日付もリセット
            fi

            # 日付が変わったらヘッダーを出力
            if [[ "$day" != "$current_date" ]]; then
                echo ""
                echo "#### $day"
                current_date="$day"
            fi

            # コミットエントリを出力
            echo "- **$repo** ($visibility): $message - \`$sha\`"
        done
    } > "$OUTPUT_FILE"

    echo "" >&2
    echo "Report generated: $OUTPUT_FILE" >&2
    echo "Total commits: $total_commits" >&2
}

main "$@"
