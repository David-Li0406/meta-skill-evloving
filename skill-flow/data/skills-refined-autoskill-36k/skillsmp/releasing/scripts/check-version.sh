#!/bin/bash
# バージョン重複チェックスクリプト
# Usage: ./check-version.sh 0.X.0

set -e

VERSION="${1:-}"

if [ -z "$VERSION" ]; then
  echo "Usage: $0 <version>"
  echo "Example: $0 0.10.0"
  exit 1
fi

# v プレフィックスを正規化
VERSION="${VERSION#v}"

echo "🔍 Checking version v${VERSION}..."
echo ""

# 現在のバージョンを確認
CURRENT_VERSION=$(cat package.json | grep '"version"' | head -1 | sed 's/.*: "\(.*\)".*/\1/')
echo "📦 Current package.json version: v${CURRENT_VERSION}"

# 既存リリースを確認
echo ""
echo "📋 Existing releases:"
gh release list --limit 10

# 重複チェック
echo ""
echo "🔍 Checking if v${VERSION} already exists..."

if gh release view "v${VERSION}" &>/dev/null; then
  echo ""
  echo "❌ ERROR: v${VERSION} already exists!"
  echo ""
  echo "💡 Suggestion: Did you mean v$(echo ${VERSION} | awk -F. '{print $1"."$2+1".0"}')?"
  exit 1
else
  echo "✅ v${VERSION} is available"
fi

# バージョン比較
echo ""
if [ "$CURRENT_VERSION" = "$VERSION" ]; then
  echo "✅ package.json version matches target version"
else
  echo "⚠️  package.json (v${CURRENT_VERSION}) differs from target (v${VERSION})"
  echo "   Run: npm version [patch|minor|major] --no-git-tag-version"
fi

echo ""
echo "🎉 Pre-release check complete!"
