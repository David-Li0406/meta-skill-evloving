#!/bin/bash
# E2Eテストをデバッグモードで実行

set -e

echo "🎭 Running E2E tests in debug mode..."
npm run test:e2e:debug
