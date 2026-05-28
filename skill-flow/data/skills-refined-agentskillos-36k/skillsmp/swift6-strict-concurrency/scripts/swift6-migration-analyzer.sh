#!/bin/bash

# Swift 6 Migration Analyzer
# Swift 5 プロジェクトを分析し、Swift 6 Strict Concurrency 移行に必要な作業を報告する

set -e

# カラー定義
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# ヘルプメッセージ
show_help() {
    echo "Swift 6 Migration Analyzer"
    echo ""
    echo "使用方法: $0 <project_path>"
    echo ""
    echo "オプション:"
    echo "  -h, --help     このヘルプメッセージを表示"
    echo "  -v, --verbose  詳細な出力を表示"
    echo ""
    echo "例:"
    echo "  $0 /path/to/MyApp"
    echo "  $0 ."
}

# 引数チェック
if [ "$1" = "-h" ] || [ "$1" = "--help" ]; then
    show_help
    exit 0
fi

if [ -z "$1" ]; then
    echo -e "${RED}エラー: プロジェクトパスを指定してください${NC}"
    show_help
    exit 1
fi

PROJECT_PATH="$1"
VERBOSE=false

if [ "$2" = "-v" ] || [ "$2" = "--verbose" ]; then
    VERBOSE=true
fi

if [ ! -d "$PROJECT_PATH" ]; then
    echo -e "${RED}エラー: ディレクトリが見つかりません: $PROJECT_PATH${NC}"
    exit 1
fi

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Swift 6 Migration Analyzer${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""
echo -e "分析対象: ${GREEN}$PROJECT_PATH${NC}"
echo ""

# Swift ファイルの総数
SWIFT_FILES=$(find "$PROJECT_PATH" -name "*.swift" -type f | grep -v ".build" | grep -v "DerivedData" | grep -v "Pods" | wc -l | tr -d ' ')
echo -e "${BLUE}Swift ファイル数:${NC} $SWIFT_FILES"
echo ""

echo -e "${YELLOW}========================================${NC}"
echo -e "${YELLOW}1. ObservableObject の使用状況${NC}"
echo -e "${YELLOW}========================================${NC}"

# ObservableObject を使用しているファイル
OBSERVABLE_OBJECT_FILES=$(find "$PROJECT_PATH" -name "*.swift" -type f | grep -v ".build" | grep -v "DerivedData" | grep -v "Pods" | xargs grep -l "ObservableObject" 2>/dev/null | wc -l | tr -d ' ')
echo -e "ObservableObject 使用ファイル数: ${RED}$OBSERVABLE_OBJECT_FILES${NC}"

if [ "$VERBOSE" = true ] && [ "$OBSERVABLE_OBJECT_FILES" -gt 0 ]; then
    echo -e "\n${BLUE}対象ファイル:${NC}"
    find "$PROJECT_PATH" -name "*.swift" -type f | grep -v ".build" | grep -v "DerivedData" | grep -v "Pods" | xargs grep -l "ObservableObject" 2>/dev/null | head -20
fi

# @Published の使用数
PUBLISHED_COUNT=$(find "$PROJECT_PATH" -name "*.swift" -type f | grep -v ".build" | grep -v "DerivedData" | grep -v "Pods" | xargs grep -c "@Published" 2>/dev/null | awk -F: '{sum += $2} END {print sum}')
echo -e "@Published 使用数: ${RED}${PUBLISHED_COUNT:-0}${NC}"

echo -e "\n${GREEN}推奨アクション:${NC} @Observable + @MainActor パターンに移行"
echo ""

echo -e "${YELLOW}========================================${NC}"
echo -e "${YELLOW}2. DispatchQueue の使用状況${NC}"
echo -e "${YELLOW}========================================${NC}"

# DispatchQueue を使用しているファイル
DISPATCH_QUEUE_FILES=$(find "$PROJECT_PATH" -name "*.swift" -type f | grep -v ".build" | grep -v "DerivedData" | grep -v "Pods" | xargs grep -l "DispatchQueue" 2>/dev/null | wc -l | tr -d ' ')
echo -e "DispatchQueue 使用ファイル数: ${RED}$DISPATCH_QUEUE_FILES${NC}"

# DispatchQueue.main の使用数
DISPATCH_MAIN_COUNT=$(find "$PROJECT_PATH" -name "*.swift" -type f | grep -v ".build" | grep -v "DerivedData" | grep -v "Pods" | xargs grep -c "DispatchQueue.main" 2>/dev/null | awk -F: '{sum += $2} END {print sum}')
echo -e "DispatchQueue.main 使用数: ${RED}${DISPATCH_MAIN_COUNT:-0}${NC}"

echo -e "\n${GREEN}推奨アクション:${NC} @MainActor または Actor に移行"
echo ""

echo -e "${YELLOW}========================================${NC}"
echo -e "${YELLOW}3. シングルトンパターンの検出${NC}"
echo -e "${YELLOW}========================================${NC}"

# static let shared パターン
SINGLETON_COUNT=$(find "$PROJECT_PATH" -name "*.swift" -type f | grep -v ".build" | grep -v "DerivedData" | grep -v "Pods" | xargs grep -c "static let shared" 2>/dev/null | awk -F: '{sum += $2} END {print sum}')
echo -e "シングルトン検出数: ${RED}${SINGLETON_COUNT:-0}${NC}"

if [ "$VERBOSE" = true ] && [ "${SINGLETON_COUNT:-0}" -gt 0 ]; then
    echo -e "\n${BLUE}対象ファイル:${NC}"
    find "$PROJECT_PATH" -name "*.swift" -type f | grep -v ".build" | grep -v "DerivedData" | grep -v "Pods" | xargs grep -l "static let shared" 2>/dev/null | head -20
fi

echo -e "\n${GREEN}推奨アクション:${NC} Actor パターンに移行を検討"
echo ""

echo -e "${YELLOW}========================================${NC}"
echo -e "${YELLOW}4. クラスの検出（非 Sendable 候補）${NC}"
echo -e "${YELLOW}========================================${NC}"

# class キーワードの使用
CLASS_COUNT=$(find "$PROJECT_PATH" -name "*.swift" -type f | grep -v ".build" | grep -v "DerivedData" | grep -v "Pods" | xargs grep -c "^class \|^final class \|^public class \|^public final class " 2>/dev/null | awk -F: '{sum += $2} END {print sum}')
echo -e "クラス定義数: ${YELLOW}${CLASS_COUNT:-0}${NC}"

# 既に Actor を使用しているファイル
ACTOR_FILES=$(find "$PROJECT_PATH" -name "*.swift" -type f | grep -v ".build" | grep -v "DerivedData" | grep -v "Pods" | xargs grep -l "^actor \|^public actor " 2>/dev/null | wc -l | tr -d ' ')
echo -e "Actor 使用ファイル数: ${GREEN}$ACTOR_FILES${NC}"

echo -e "\n${GREEN}推奨アクション:${NC} 共有可変状態を持つクラスは Actor に移行"
echo ""

echo -e "${YELLOW}========================================${NC}"
echo -e "${YELLOW}5. 既存の Concurrency 対応状況${NC}"
echo -e "${YELLOW}========================================${NC}"

# @MainActor の使用
MAINACTOR_COUNT=$(find "$PROJECT_PATH" -name "*.swift" -type f | grep -v ".build" | grep -v "DerivedData" | grep -v "Pods" | xargs grep -c "@MainActor" 2>/dev/null | awk -F: '{sum += $2} END {print sum}')
echo -e "@MainActor 使用数: ${GREEN}${MAINACTOR_COUNT:-0}${NC}"

# Sendable の使用
SENDABLE_COUNT=$(find "$PROJECT_PATH" -name "*.swift" -type f | grep -v ".build" | grep -v "DerivedData" | grep -v "Pods" | xargs grep -c ": Sendable\|: .*Sendable\|@unchecked Sendable" 2>/dev/null | awk -F: '{sum += $2} END {print sum}')
echo -e "Sendable 使用数: ${GREEN}${SENDABLE_COUNT:-0}${NC}"

# async/await の使用
ASYNC_COUNT=$(find "$PROJECT_PATH" -name "*.swift" -type f | grep -v ".build" | grep -v "DerivedData" | grep -v "Pods" | xargs grep -c "async \|await " 2>/dev/null | awk -F: '{sum += $2} END {print sum}')
echo -e "async/await 使用数: ${GREEN}${ASYNC_COUNT:-0}${NC}"

echo ""

echo -e "${YELLOW}========================================${NC}"
echo -e "${YELLOW}6. Completion Handler の検出${NC}"
echo -e "${YELLOW}========================================${NC}"

# completion handler パターン
COMPLETION_COUNT=$(find "$PROJECT_PATH" -name "*.swift" -type f | grep -v ".build" | grep -v "DerivedData" | grep -v "Pods" | xargs grep -c "completion:" 2>/dev/null | awk -F: '{sum += $2} END {print sum}')
echo -e "Completion Handler 使用数: ${YELLOW}${COMPLETION_COUNT:-0}${NC}"

echo -e "\n${GREEN}推奨アクション:${NC} async/await パターンに移行"
echo ""

echo -e "${YELLOW}========================================${NC}"
echo -e "${YELLOW}7. 潜在的な問題パターン${NC}"
echo -e "${YELLOW}========================================${NC}"

# NSLock の使用
NSLOCK_COUNT=$(find "$PROJECT_PATH" -name "*.swift" -type f | grep -v ".build" | grep -v "DerivedData" | grep -v "Pods" | xargs grep -c "NSLock" 2>/dev/null | awk -F: '{sum += $2} END {print sum}')
echo -e "NSLock 使用数: ${YELLOW}${NSLOCK_COUNT:-0}${NC} (Actor への移行を検討)"

# weak var delegate パターン
DELEGATE_COUNT=$(find "$PROJECT_PATH" -name "*.swift" -type f | grep -v ".build" | grep -v "DerivedData" | grep -v "Pods" | xargs grep -c "weak var.*delegate" 2>/dev/null | awk -F: '{sum += $2} END {print sum}')
echo -e "Delegate パターン数: ${YELLOW}${DELEGATE_COUNT:-0}${NC} (@MainActor Protocol への移行を検討)"

# NotificationCenter addObserver
NOTIFICATION_COUNT=$(find "$PROJECT_PATH" -name "*.swift" -type f | grep -v ".build" | grep -v "DerivedData" | grep -v "Pods" | xargs grep -c "addObserver" 2>/dev/null | awk -F: '{sum += $2} END {print sum}')
echo -e "NotificationCenter Observer 数: ${YELLOW}${NOTIFICATION_COUNT:-0}${NC} (AsyncSequence への移行を検討)"

echo ""

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}サマリー${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""
echo -e "移行優先度: ${RED}高${NC}"
echo -e "  - ObservableObject: ${OBSERVABLE_OBJECT_FILES} ファイル"
echo -e "  - シングルトン: ${SINGLETON_COUNT:-0} 箇所"
echo ""
echo -e "移行優先度: ${YELLOW}中${NC}"
echo -e "  - DispatchQueue: ${DISPATCH_QUEUE_FILES} ファイル"
echo -e "  - Completion Handler: ${COMPLETION_COUNT:-0} 箇所"
echo -e "  - Delegate: ${DELEGATE_COUNT:-0} 箇所"
echo ""
echo -e "移行優先度: ${GREEN}低${NC}"
echo -e "  - NSLock: ${NSLOCK_COUNT:-0} 箇所"
echo -e "  - NotificationCenter: ${NOTIFICATION_COUNT:-0} 箇所"
echo ""

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}推奨される次のステップ${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""
echo "1. Build Settings で SWIFT_STRICT_CONCURRENCY = targeted を設定"
echo "2. ObservableObject を @Observable + @MainActor に移行"
echo "3. シングルトンを Actor に変換"
echo "4. DispatchQueue を @MainActor に置き換え"
echo "5. SWIFT_STRICT_CONCURRENCY = complete に変更"
echo "6. 残りの警告を修正"
echo ""
echo -e "${GREEN}分析完了${NC}"
