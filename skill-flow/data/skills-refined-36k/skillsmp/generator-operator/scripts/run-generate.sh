#!/bin/bash
# npm run generate実行ラッパー

CATEGORY=$1
SUBTYPE=$2
SERVICE=$3
SECTION=$4
NAME=$5

echo "Generating file with npm run generate..."

# パラメータに応じてコマンドを構築
if [ "$CATEGORY" = "ui" ]; then
  npm run generate -- \
    --category "$CATEGORY" \
    --ui-type "$SUBTYPE" \
    --service "$SERVICE" \
    --section "$SECTION" \
    --name "$NAME"
elif [ "$CATEGORY" = "documents" ]; then
  npm run generate -- \
    --category "$CATEGORY" \
    --document-type "$SUBTYPE" \
    --service "$SERVICE" \
    --section "$SECTION" \
    --name "$NAME"
else
  npm run generate -- \
    --category "$CATEGORY" \
    --service "$SERVICE" \
    --section "$SECTION" \
    --name "$NAME"
fi
