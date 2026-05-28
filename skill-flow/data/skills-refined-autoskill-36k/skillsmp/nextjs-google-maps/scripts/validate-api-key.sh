#!/bin/bash
#
# Google Maps API キー検証スクリプト
# 使用方法: bash scripts/validate-api-key.sh [API_KEY]
#
# API キーが指定されない場合、環境変数から読み取ります:
#   NEXT_PUBLIC_GOOGLE_MAPS_API_KEY または GOOGLE_MAPS_API_KEY
#

set -e

# カラー定義
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# アイコン
CHECK="✓"
CROSS="✗"
WARN="⚠"
INFO="ℹ"

# ヘルパー関数
print_header() {
    echo -e "\n${BLUE}========================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}========================================${NC}\n"
}

print_success() {
    echo -e "${GREEN}${CHECK} $1${NC}"
}

print_error() {
    echo -e "${RED}${CROSS} $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}${WARN} $1${NC}"
}

print_info() {
    echo -e "${BLUE}${INFO} $1${NC}"
}

# API キーの取得
get_api_key() {
    if [ -n "$1" ]; then
        echo "$1"
    elif [ -n "$NEXT_PUBLIC_GOOGLE_MAPS_API_KEY" ]; then
        echo "$NEXT_PUBLIC_GOOGLE_MAPS_API_KEY"
    elif [ -n "$GOOGLE_MAPS_API_KEY" ]; then
        echo "$GOOGLE_MAPS_API_KEY"
    elif [ -f ".env.local" ]; then
        grep -E "^NEXT_PUBLIC_GOOGLE_MAPS_API_KEY=" .env.local | cut -d '=' -f2- | tr -d '"' | tr -d "'"
    else
        echo ""
    fi
}

# API キーのフォーマット検証
validate_key_format() {
    local key="$1"

    if [ -z "$key" ]; then
        print_error "API キーが見つかりません"
        echo ""
        echo "使用方法:"
        echo "  bash scripts/validate-api-key.sh YOUR_API_KEY"
        echo ""
        echo "または、以下の方法で設定してください:"
        echo "  1. 環境変数: export NEXT_PUBLIC_GOOGLE_MAPS_API_KEY=YOUR_KEY"
        echo "  2. .env.local ファイル: NEXT_PUBLIC_GOOGLE_MAPS_API_KEY=YOUR_KEY"
        return 1
    fi

    if [[ ! "$key" =~ ^AIza[A-Za-z0-9_-]{35}$ ]]; then
        print_warning "API キーの形式が標準的ではありません"
        print_info "通常の Google API キーは 'AIza' で始まり、39文字です"
    else
        print_success "API キーの形式は正しいです"
    fi

    return 0
}

# API のテスト
test_api() {
    local api_name="$1"
    local url="$2"
    local key="$3"

    local full_url="${url}&key=${key}"
    local response
    local http_code

    # API を呼び出し
    response=$(curl -s -w "\n%{http_code}" "$full_url" 2>/dev/null)
    http_code=$(echo "$response" | tail -n1)
    body=$(echo "$response" | sed '$d')

    if [ "$http_code" = "200" ]; then
        # レスポンスのステータスを確認
        if echo "$body" | grep -q '"status"\s*:\s*"OK"'; then
            print_success "${api_name}: 有効"
            return 0
        elif echo "$body" | grep -q '"status"\s*:\s*"ZERO_RESULTS"'; then
            print_success "${api_name}: 有効（結果なし）"
            return 0
        elif echo "$body" | grep -q '"status"\s*:\s*"REQUEST_DENIED"'; then
            print_error "${api_name}: API が有効化されていません"
            return 1
        elif echo "$body" | grep -q '"error_message"'; then
            local error_msg=$(echo "$body" | grep -o '"error_message"\s*:\s*"[^"]*"' | cut -d'"' -f4)
            print_error "${api_name}: エラー - ${error_msg}"
            return 1
        else
            print_warning "${api_name}: 不明なレスポンス"
            return 1
        fi
    else
        print_error "${api_name}: HTTP エラー (${http_code})"
        return 1
    fi
}

# メイン処理
main() {
    print_header "Google Maps API キー検証ツール"

    # API キーの取得
    API_KEY=$(get_api_key "$1")

    if ! validate_key_format "$API_KEY"; then
        exit 1
    fi

    # キーの最初と最後を表示（セキュリティのため中間は隠す）
    local key_preview="${API_KEY:0:8}...${API_KEY: -4}"
    print_info "検証対象のキー: ${key_preview}"

    echo ""
    print_header "API 有効化状態のテスト"

    # 各 API をテスト
    local geocoding_url="https://maps.googleapis.com/maps/api/geocode/json?address=Tokyo"
    local places_url="https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input=Tokyo&inputtype=textquery"
    local directions_url="https://maps.googleapis.com/maps/api/directions/json?origin=Tokyo&destination=Osaka"

    echo ""
    echo "1. Geocoding API:"
    test_api "Geocoding API" "$geocoding_url" "$API_KEY"

    echo ""
    echo "2. Places API:"
    test_api "Places API" "$places_url" "$API_KEY"

    echo ""
    echo "3. Directions API:"
    test_api "Directions API" "$directions_url" "$API_KEY"

    echo ""
    print_header "推奨事項"

    print_info "本番環境では以下の設定を確認してください:"
    echo ""
    echo "  1. API キーにリファラー制限を設定"
    echo "     - 開発: localhost:*"
    echo "     - 本番: https://your-domain.com/*"
    echo ""
    echo "  2. 使用する API のみに制限"
    echo "     - Maps JavaScript API"
    echo "     - Places API（オートコンプリート使用時）"
    echo "     - Directions API（ルート計算使用時）"
    echo "     - Geocoding API（住所変換使用時）"
    echo ""
    echo "  3. 使用量のアラートを設定"
    echo "     - Cloud Console で予算アラートを設定"
    echo ""
    echo "  4. 開発用と本番用で別の API キーを使用"
    echo ""

    print_info "詳細は Google Cloud Console で確認してください:"
    echo "  https://console.cloud.google.com/google/maps-apis/credentials"
}

# スクリプト実行
main "$@"
