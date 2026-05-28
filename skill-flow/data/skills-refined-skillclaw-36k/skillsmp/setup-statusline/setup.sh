#!/bin/bash

set -e

# カラー定義
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# ヘルプメッセージ
show_help() {
    cat << EOF
Claude Code ステータスライン設定スクリプト

使用方法:
  $0 [OPTIONS]

オプション:
  --help    このヘルプメッセージを表示

説明:
  このスクリプトは Claude Code のステータスライン表示を自動設定します。
  以下の処理を実行します:
    1. jq コマンドのインストール確認
    2. ~/.claude/ ディレクトリの確認/作成
    3. ~/.claude/settings.json に statusLine 設定を追加（既存設定は保持）
    4. ~/.claude/statusline.sh スクリプトを作成

前提条件:
  - jq コマンドがインストールされている必要があります
    macOS:        brew install jq
    Ubuntu/Debian: sudo apt-get install jq
    Fedora/RHEL:  sudo dnf install jq

設定内容:
  - ディレクトリ名（青色）
  - Git ブランチ名（括弧内）
  - モデル名（角括弧内）
  - トークン情報（合計、入力、出力、キャッシュ）

例:
  $0
EOF
}

# jq のインストール確認
check_jq_installed() {
    echo -e "${BLUE}前提条件をチェック中...${NC}"

    if ! command -v jq &> /dev/null; then
        echo -e "${RED}❌ jq が見つかりません${NC}"
        echo ""
        echo "jq をインストールしてください:"
        echo "  macOS:         brew install jq"
        echo "  Ubuntu/Debian: sudo apt-get install jq"
        echo "  Fedora/RHEL:   sudo dnf install jq"
        echo ""
        exit 1
    fi

    echo -e "${GREEN}✅ jq が見つかりました${NC}"
}

# ~/.claude/ ディレクトリの確認/作成
check_claude_dir() {
    local CLAUDE_DIR="$HOME/.claude"

    echo -e "${BLUE}Claude ディレクトリをチェック中...${NC}"

    if [ ! -d "$CLAUDE_DIR" ]; then
        echo -e "${YELLOW}~/.claude/ ディレクトリが見つかりません。作成します...${NC}"
        mkdir -p "$CLAUDE_DIR" || {
            echo -e "${RED}❌ ~/.claude/ ディレクトリの作成に失敗しました${NC}"
            exit 1
        }
        echo -e "${GREEN}✅ ~/.claude/ ディレクトリを作成しました${NC}"
    else
        echo -e "${GREEN}✅ ~/.claude/ ディレクトリが見つかりました${NC}"
    fi
}

# settings.json のマージ
merge_settings() {
    local SETTINGS_FILE="$HOME/.claude/settings.json"
    local STATUSLINE_CONFIG='{"type":"command","command":"~/.claude/statusline.sh","padding":0}'

    echo -e "${BLUE}settings.json を更新中...${NC}"

    if [ -f "$SETTINGS_FILE" ]; then
        # バックアップ作成
        cp "$SETTINGS_FILE" "$SETTINGS_FILE.backup"
        echo -e "${YELLOW}既存の設定をバックアップしました: $SETTINGS_FILE.backup${NC}"

        # JSON をマージ
        jq ". + {\"statusLine\": $STATUSLINE_CONFIG}" "$SETTINGS_FILE" > "$SETTINGS_FILE.tmp"
        mv "$SETTINGS_FILE.tmp" "$SETTINGS_FILE"
        echo -e "${GREEN}✅ settings.json を更新しました（既存設定は保持）${NC}"
    else
        # 新規作成
        echo "{\"statusLine\": $STATUSLINE_CONFIG}" | jq '.' > "$SETTINGS_FILE"
        echo -e "${GREEN}✅ settings.json を新規作成しました${NC}"
    fi
}

# statusline.sh の作成
create_statusline_script() {
    local SCRIPT_FILE="$HOME/.claude/statusline.sh"

    echo -e "${BLUE}statusline.sh を作成中...${NC}"

    # 既存ファイルのバックアップ
    if [ -f "$SCRIPT_FILE" ]; then
        cp "$SCRIPT_FILE" "$SCRIPT_FILE.backup"
        echo -e "${YELLOW}既存のスクリプトをバックアップしました: $SCRIPT_FILE.backup${NC}"
    fi

    # スクリプト作成
    cat > "$SCRIPT_FILE" << 'EOF'
#!/bin/bash

input=$(cat)

current_dir=$(echo "$input" | jq -r '.workspace.current_dir')
model_name=$(echo "$input" | jq -r '.model.display_name')

# Git ブランチ情報を取得
git_branch=""
if [ -d "$current_dir/.git" ] || git -C "$current_dir" rev-parse --git-dir > /dev/null 2>&1; then
    git_branch=$(git -C "$current_dir" branch --show-current 2>/dev/null)
    if [ -n "$git_branch" ]; then
        git_branch=" ($git_branch)"
    fi
fi

# トークン情報を取得
usage=$(echo "$input" | jq '.context_window.current_usage')
token_info=""

if [ "$usage" != "null" ]; then
    input_tokens=$(echo "$usage" | jq -r '.input_tokens // 0')
    output_tokens=$(echo "$usage" | jq -r '.output_tokens // 0')
    cache_creation=$(echo "$usage" | jq -r '.cache_creation_input_tokens // 0')
    cache_read=$(echo "$usage" | jq -r '.cache_read_input_tokens // 0')

    # 合計トークン数を計算
    total=$((input_tokens + output_tokens + cache_creation + cache_read))

    # トークン数を K (千) 単位で表示
    if [ $total -gt 1000 ]; then
        # awk で小数点1桁まで表示
        total_display=$(awk "BEGIN {printf \"%.1f\", $total / 1000}")"K"
    else
        total_display="$total"
    fi

    token_info=" | 📊 ${total_display} (In:${input_tokens} Out:${output_tokens} Cache:${cache_read})"
fi

printf "\033[36m%s\033[0m\033[2m%s [%s]%s\033[0m" \
    "$(basename "$current_dir")" \
    "$git_branch" \
    "$model_name" \
    "$token_info"
EOF

    # 実行権限付与
    chmod +x "$SCRIPT_FILE"
    echo -e "${GREEN}✅ statusline.sh を作成しました（実行権限付与済み）${NC}"
}

# メイン処理
main() {
    # --help オプションのチェック
    if [ "$1" == "--help" ]; then
        show_help
        exit 0
    fi

    echo -e "${GREEN}========================================${NC}"
    echo -e "${GREEN}Claude Code ステータスライン設定${NC}"
    echo -e "${GREEN}========================================${NC}"
    echo ""

    # 各処理を実行
    check_jq_installed
    echo ""

    check_claude_dir
    echo ""

    merge_settings
    echo ""

    create_statusline_script
    echo ""

    echo -e "${GREEN}========================================${NC}"
    echo -e "${GREEN}✅ セットアップが完了しました！${NC}"
    echo -e "${GREEN}========================================${NC}"
    echo ""
    echo -e "次回 Claude Code を起動すると、ステータスラインが表示されます。"
    echo ""
    echo -e "表示例:"
    echo -e "  ${BLUE}skillth${NC}${YELLOW} (feature/setup-statusline)${NC} [Sonnet] | 📊 38.8K (In:37442 Out:0 Cache:0)"
    echo ""
}

# スクリプト実行
main "$@"
