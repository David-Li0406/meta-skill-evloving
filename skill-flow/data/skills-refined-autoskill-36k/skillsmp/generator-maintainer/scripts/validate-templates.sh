#!/bin/bash
# テンプレートファイル存在確認スクリプト

CONFIG_FILE="scripts/generate/config.json"
TEMPLATE_DIR="scripts/generate/templates"

echo "Validating templates..."

# config.jsonで定義されたテンプレートファイルが存在するか確認
# (簡易版: 実際にはjqでパースして確認)

if [ ! -d "$TEMPLATE_DIR" ]; then
  echo "ERROR: Template directory not found: $TEMPLATE_DIR"
  exit 1
fi

echo "✓ Templates directory exists"
exit 0
