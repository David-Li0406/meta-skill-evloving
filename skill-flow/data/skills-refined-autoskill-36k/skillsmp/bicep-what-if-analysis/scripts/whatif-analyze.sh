#!/bin/bash
# Bicep what-if分析スクリプト（azd環境変数を活用）
# Usage: ./whatif-analyze.sh [--raw] [--debug] [--template <path>] [--parameters <key=value>]...
#
# 任意のazdプロジェクトで使用可能な汎用スクリプト。
# azdプロジェクトのルートディレクトリ（azure.yamlがある場所）で実行してください。

set -euo pipefail

# オプション解析
RAW_OUTPUT=false
DEBUG_MODE=false
TEMPLATE_FILE=""
EXTRA_PARAMS=()
while [[ $# -gt 0 ]]; do
  case $1 in
    --raw)
      RAW_OUTPUT=true
      shift
      ;;
    --debug)
      DEBUG_MODE=true
      shift
      ;;
    --template|-t)
      TEMPLATE_FILE="$2"
      shift 2
      ;;
    --parameters|-p)
      EXTRA_PARAMS+=("$2")
      shift 2
      ;;
    -h|--help)
      echo "Usage: $0 [--raw] [--debug] [--template <path>] [--parameters <key=value>]..."
      echo ""
      echo "Options:"
      echo "  --raw                  Output raw what-if results without filtering"
      echo "  --debug                Enable debug output (show parameters passed to az)"
      echo "  --template, -t <path>  Bicep template file (default: auto-detect from azure.yaml)"
      echo "  --parameters, -p <kv>  Additional parameters (can be specified multiple times)"
      echo "  -h, --help             Show this help message"
      echo ""
      echo "Examples:"
      echo "  $0                              # Auto-detect template, filtered output"
      echo "  $0 --raw                        # Raw output without noise filtering"
      echo "  $0 --debug                      # Show debug info for troubleshooting"
      echo "  $0 --template infra/main.bicep  # Explicit template path"
      echo "  $0 -p vmSize=Standard_D2s_v3 -p nodeCount=3"
      exit 0
      ;;
    *)
      echo "Error: Unknown option: $1" >&2
      echo "Use --help for usage information." >&2
      exit 1
      ;;
  esac
done

# ログ関数
log_info() { echo "[INFO] $*" >&2; }
log_error() { echo "[ERROR] $*" >&2; }
log_debug() { [[ "$DEBUG_MODE" == "true" ]] && echo "[DEBUG] $*" >&2 || true; }

# 依存コマンドチェック
require_command() {
  if ! command -v "$1" >/dev/null 2>&1; then
    log_error "Required command not found: $1"
    exit 1
  fi
}

# 一時ファイルのクリーンアップ
CLEANUP_FILES=()
cleanup() {
  for file in "${CLEANUP_FILES[@]}"; do
    rm -f "$file"
  done
}
trap cleanup EXIT

require_command azd
require_command az
require_command jq
PYTHON_BIN="$(command -v python3 || command -v python || true)"

# カレントディレクトリをazdプロジェクトルートとして扱う
PROJECT_ROOT="$(pwd)"

# azure.yamlの存在確認
if [[ ! -f "$PROJECT_ROOT/azure.yaml" ]]; then
  log_error "azure.yaml not found in current directory."
  log_error "Please run this script from your azd project root directory."
  exit 1
fi

# azdから環境変数を取得
log_debug "Loading environment variables from azd env"
AZD_ENV_OUTPUT=$(azd env get-values 2>&1) || {
  log_error "Failed to get azd environment values."
  log_error "Output: $AZD_ENV_OUTPUT"
  log_error "Make sure the environment is properly initialized with 'azd env refresh'."
  exit 1
}

# 環境変数を評価
eval "$AZD_ENV_OUTPUT" || {
  log_error "Failed to parse azd environment values."
  log_error "This may be due to special characters in the values."
  log_error "Raw output:"
  echo "$AZD_ENV_OUTPUT" >&2
  exit 1
}

# azdのエクスポート形式に合わせて環境変数を適用
export AZURE_LOCATION AZURE_ENV_NAME AZURE_RESOURCE_GROUP AZURE_SUBSCRIPTION_ID AZURE_TENANT_ID

# 必須変数チェック
if [[ -z "${AZURE_LOCATION:-}" ]]; then
  log_error "AZURE_LOCATION is not set. Run 'azd env refresh' first."
  exit 1
fi
if [[ -z "${AZURE_ENV_NAME:-}" ]]; then
  log_error "AZURE_ENV_NAME is not set. Run 'azd env refresh' first."
  exit 1
fi

# 環境ディレクトリの存在確認
if [[ ! -d "$PROJECT_ROOT/.azure/$AZURE_ENV_NAME" ]]; then
  log_error "Environment directory not found: .azure/$AZURE_ENV_NAME"
  log_error "The environment '$AZURE_ENV_NAME' may not be properly initialized."
  log_error "Run 'azd env new $AZURE_ENV_NAME' or 'azd env select <existing-env>'."
  exit 1
fi

# azure.yamlからinfra.pathを検出（デフォルト: ./infra）
INFRA_PATH=$(grep -E "^\s*path:" "$PROJECT_ROOT/azure.yaml" | head -1 | sed 's/.*path:\s*//' | tr -d '"' || echo "")
if [[ -z "$INFRA_PATH" ]]; then
  INFRA_PATH="./infra"
fi

AUTO_DETECTED_TEMPLATE=false

# テンプレートファイルの自動検出
if [[ -z "$TEMPLATE_FILE" ]]; then
  AUTO_DETECTED_TEMPLATE=true
  # main.bicepを探す
  if [[ -f "$PROJECT_ROOT/$INFRA_PATH/main.bicep" ]]; then
    TEMPLATE_FILE="$INFRA_PATH/main.bicep"
  elif [[ -f "$PROJECT_ROOT/infra/main.bicep" ]]; then
    TEMPLATE_FILE="infra/main.bicep"
  else
    log_error "Could not auto-detect Bicep template file."
    log_error "Use --template option to specify the path."
    exit 1
  fi
fi

log_info "=== Bicep What-If Analysis ==="
log_info "Project: $PROJECT_ROOT"
log_info "Environment: ${AZURE_ENV_NAME}"
log_info "Location: $AZURE_LOCATION"
log_info "Template: $TEMPLATE_FILE"
log_info "Resource Group: ${AZURE_RESOURCE_GROUP:-will be created}"
log_info ""

# パラメータファイルの自動検出（テンプレート自動検出時のみ）
PARAMETERS_FILE=""
if [[ "$AUTO_DETECTED_TEMPLATE" == "true" ]]; then
  if [[ -f "$PROJECT_ROOT/$INFRA_PATH/main.parameters.json" ]]; then
    PARAMETERS_FILE="$PROJECT_ROOT/$INFRA_PATH/main.parameters.json"
  elif [[ -f "$PROJECT_ROOT/infra/main.parameters.json" ]]; then
    PARAMETERS_FILE="$PROJECT_ROOT/infra/main.parameters.json"
  fi
fi
if [[ -n "$PARAMETERS_FILE" ]]; then
  log_debug "Using parameters file: $PARAMETERS_FILE"
fi

# Bicepテンプレートから許可されたパラメータ名を抽出
ALLOWED_PARAMS=$(grep -E "^\s*param\s+\w+" "$TEMPLATE_FILE" | sed 's/^\s*param \([a-zA-Z_][a-zA-Z0-9_]*\).*/\1/' || true)

# what-if引数を構築
WHATIF_ARGS=(
  --location "$AZURE_LOCATION"
  --template-file "$TEMPLATE_FILE"
)

if [[ -n "$PARAMETERS_FILE" ]]; then
  if [[ -z "$PYTHON_BIN" ]]; then
    log_error "python3 is required to expand parameters file placeholders."
    log_error "Install python3 or pass parameters explicitly with --parameters."
    exit 1
  fi
  PARAMS_TEMP=$(mktemp)
  PARAMS_ERR=$(mktemp)
  CLEANUP_FILES+=("$PARAMS_TEMP" "$PARAMS_ERR")
  if ! "$PYTHON_BIN" - "$PARAMETERS_FILE" <<'PY' > "$PARAMS_TEMP" 2> "$PARAMS_ERR"; then
"""Expand environment variable placeholders in a JSON parameters file."""
import json
import os
import re
import sys
from typing import Any

def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python expand_params.py <parameters.json>", file=sys.stderr)
        sys.exit(1)

    path = sys.argv[1]
    pattern = re.compile(r"\$\{([A-Z0-9_]+)(:([^}]*))?\}")

    def replace_value(value: str) -> str:
        def repl(match: re.Match[str]) -> str:
            key = match.group(1)
            default = match.group(3) or ""
            return os.environ.get(key, default)
        return pattern.sub(repl, value)

    def walk(obj: Any) -> Any:
        if isinstance(obj, dict):
            return {k: walk(v) for k, v in obj.items()}
        if isinstance(obj, list):
            return [walk(v) for v in obj]
        if isinstance(obj, str):
            return replace_value(obj)
        return obj

    try:
        with open(path, "r", encoding="utf-8") as handle:
            data = json.load(handle)
        json.dump(walk(data), sys.stdout)
    except FileNotFoundError:
        print(f"Error: File not found: {path}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in {path}: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
PY
    log_error "Failed to expand parameters file: $PARAMETERS_FILE"
    log_error "Error output:"
    cat "$PARAMS_ERR" >&2
    exit 1
  fi
  WHATIF_ARGS+=(--parameters "@$PARAMS_TEMP")
else
  WHATIF_ARGS+=(--parameters location="$AZURE_LOCATION")
  # AZURE_ENV_NAME を 'environment' / 'environmentName' パラメータにマッピング（存在する場合）
  if echo "$ALLOWED_PARAMS" | grep -qw "environment"; then
    WHATIF_ARGS+=(--parameters environment="$AZURE_ENV_NAME")
  fi
  if echo "$ALLOWED_PARAMS" | grep -qw "environmentName"; then
    WHATIF_ARGS+=(--parameters environmentName="$AZURE_ENV_NAME")
  fi

  # azd環境変数からBicepパラメータに一致するもののみを自動検出
  # Bicepで定義されたパラメータ名とマッチするものだけを渡す（出力変数を除外）
  while IFS='=' read -r key value; do
    [[ -z "$key" ]] && continue
    # クォートを除去
    value="${value%\"}"
    value="${value#\"}"
    # Bicepで定義されたパラメータのみ渡す
    if echo "$ALLOWED_PARAMS" | grep -qw "$key"; then
      # location と environment は既に設定済みなのでスキップ
      if [[ "$key" != "location" && "$key" != "environment" && "$key" != "environmentName" ]]; then
        WHATIF_ARGS+=(--parameters "$key=$value")
      fi
    fi
  done <<< "$AZD_ENV_OUTPUT"
fi

# 追加パラメータを追加
for param in "${EXTRA_PARAMS[@]}"; do
  WHATIF_ARGS+=(--parameters "$param")
done

# デバッグ: 渡すパラメータを表示
log_debug "What-if arguments:"
for arg in "${WHATIF_ARGS[@]}"; do
  log_debug "  $arg"
done

# 生出力モード
if [[ "$RAW_OUTPUT" == "true" ]]; then
  log_info "Running what-if (raw output)..."
  az deployment sub what-if "${WHATIF_ARGS[@]}"
  exit 0
fi

# フィルタリングモード
log_info "Running what-if with noise filtering..."

# 一時ファイルに出力（パイプ処理の問題を回避）
TEMP_FILE=$(mktemp)
TEMP_ERR=$(mktemp)
CLEANUP_FILES+=("$TEMP_FILE" "$TEMP_ERR")

# what-if実行（エラーも取る）
WHATIF_EXIT_CODE=0
az deployment sub what-if "${WHATIF_ARGS[@]}" --no-pretty-print --only-show-errors -o json > "$TEMP_FILE" 2> "$TEMP_ERR" || WHATIF_EXIT_CODE=$?

# エラーチェック
if [[ $WHATIF_EXIT_CODE -ne 0 ]]; then
  log_error "What-if analysis failed (exit code: $WHATIF_EXIT_CODE)"
  log_error ""
  log_error "Error output:"
  cat "$TEMP_ERR" >&2
  log_error ""
  log_error "Hint: Use --debug to see the parameters being passed."
  log_error "Hint: Use --raw to see raw Azure CLI output."
  exit $WHATIF_EXIT_CODE
fi

# 出力が空または無効なJSONの場合
if [[ ! -s "$TEMP_FILE" ]]; then
  log_error "What-if returned empty output."
  if [[ -s "$TEMP_ERR" ]]; then
    log_error "Stderr output:"
    cat "$TEMP_ERR" >&2
  fi
  exit 1
fi

# JSONバリデーション
if ! jq empty "$TEMP_FILE" 2>/dev/null; then
  log_error "What-if returned invalid JSON."
  log_error "Raw output (first 500 chars):"
  head -c 500 "$TEMP_FILE" >&2
  echo "" >&2
  exit 1
fi

# jqでフィルタリング
jq '
  # ノイズパターン（読み取り専用/動的な値）
  # 一般的なAzureリソースで共通するノイズプロパティ
  def is_noise: . as $path | $path | test("provisioningState|etag|principalId|clientId|tenantId|fqdn|azurePortalFQDN|nodeImageVersion|currentOrchestratorVersion|uniqueId|resourceGuid|powerState\\.code|identityProfile|createdAt|modifiedAt|createdBy|lastModifiedBy|systemData");

  # 破壊的変更パターン（リソースの再作成が必要になる可能性があるプロパティ）
  def is_destructive: . as $path | $path | test("networkPlugin|networkPluginMode|subnetId|vnetSubnetID|addressPrefixes|sku\\.name|sku\\.tier|sku\\.capacity|kind|location");

  # 変更をフィルタリング
  [.changes[]
  | select(.changeType != "NoChange" and .changeType != "NoEffect" and .changeType != "Ignore")
  | {
      resourceId: .resourceId,
      resourceType: (if .resourceId == null or (.resourceId | startswith("[")) then "dynamic" else (.resourceId | split("/") | .[-2] // "unknown") end),
      resourceName: (if .resourceId == null or (.resourceId | startswith("[")) then "dynamic" else (.resourceId | split("/") | .[-1] // "unknown") end),
      changeType: .changeType,
      unsupportedReason: .unsupportedReason,
      significantChanges: (
        if .delta == null then []
        else [.delta[] | select((.path | is_noise | not) and .propertyChangeType != "NoEffect")]
        end
      ),
      potentiallyDestructive: (
        if .delta == null then false
        else ([.delta[] | select(.path | is_destructive)] | length > 0)
        end
      )
    }
  | select((.significantChanges | length > 0) or .changeType == "Create" or .changeType == "Delete" or .changeType == "Unsupported")]
  | {
      summary: {
        total: length,
        create: [.[] | select(.changeType == "Create")] | length,
        modify: [.[] | select(.changeType == "Modify")] | length,
        delete: [.[] | select(.changeType == "Delete")] | length,
        unsupported: [.[] | select(.changeType == "Unsupported")] | length,
        potentiallyDestructive: [.[] | select(.potentiallyDestructive == true)] | length
      },
      changes: .
    }
' "$TEMP_FILE"

log_info ""
log_info "=== Analysis Complete ==="
log_info "Tip: Use 'jq .changes[]' to see individual changes"
log_info "Tip: Use 'jq .summary' to see only the summary"
