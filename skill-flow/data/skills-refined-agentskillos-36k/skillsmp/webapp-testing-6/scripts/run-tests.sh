#!/bin/bash
# Unified test runner for LucidData
# Usage: ./run-tests.sh [unit|e2e|all] [--coverage]

set -e  # Exit on error

TEST_TYPE=${1:-all}
COVERAGE_FLAG=${2:-}

echo "🧪 LucidData Test Runner"
echo "========================"
echo ""

case $TEST_TYPE in
  unit)
    echo "📋 Running unit and integration tests..."
    if [ "$COVERAGE_FLAG" = "--coverage" ]; then
      npm run test:coverage
    else
      npm run test:run
    fi
    ;;

  e2e)
    echo "🌐 Running end-to-end tests..."
    echo "⚠️  Make sure the dev server is running at http://localhost:3000"
    echo ""
    npm run test:e2e
    ;;

  all)
    echo "🚀 Running all test suites..."
    echo ""
    echo "📋 Step 1/2: Unit and integration tests"
    if [ "$COVERAGE_FLAG" = "--coverage" ]; then
      npm run test:coverage
    else
      npm run test:run
    fi

    echo ""
    echo "🌐 Step 2/2: End-to-end tests"
    echo "⚠️  Make sure the dev server is running at http://localhost:3000"
    echo ""
    npm run test:e2e
    ;;

  *)
    echo "❌ Invalid test type: $TEST_TYPE"
    echo ""
    echo "Usage: ./run-tests.sh [unit|e2e|all] [--coverage]"
    echo ""
    echo "Examples:"
    echo "  ./run-tests.sh unit              # Run unit/integration tests"
    echo "  ./run-tests.sh unit --coverage   # Run with coverage report"
    echo "  ./run-tests.sh e2e               # Run E2E tests"
    echo "  ./run-tests.sh all               # Run all tests"
    echo "  ./run-tests.sh all --coverage    # Run all tests with coverage"
    exit 1
    ;;
esac

echo ""
echo "✅ Test run complete!"
