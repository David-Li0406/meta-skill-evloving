#!/bin/bash
# ユニットテストをUIモードで実行（デバッグ用）

set -e

echo "🧪 Running unit tests in UI mode..."
npm run test:ui
