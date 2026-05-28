#!/bin/bash

set -e

echo "🧪 Testing Pi CLI..."
echo ""

TEST_PROMPT="Hello, this is a test."
START_TIME=$(date +%s)

echo "🚀 Running pi command..."
OUTPUT=$(pi --print --model z-ai/glm4.7 --provider nvidia "$TEST_PROMPT" 2>&1)

END_TIME=$(date +%s)
DURATION=$((END_TIME - START_TIME))

echo "Output: $OUTPUT"
echo ""
echo "✅ Pi CLI works! Duration: ${DURATION}s"
