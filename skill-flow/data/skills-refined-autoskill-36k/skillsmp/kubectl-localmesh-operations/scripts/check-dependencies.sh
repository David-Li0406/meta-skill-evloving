#!/bin/bash
# kubectl-localmesh 依存関係チェックスクリプト

set -e

echo "==================================="
echo "kubectl-localmesh 依存関係チェック"
echo "==================================="
echo ""

exit_code=0

# kubectl
echo "【kubectl】"
if ! command -v kubectl &> /dev/null; then
    echo "❌ kubectl が見つかりません"
    echo "   インストール方法: https://kubernetes.io/docs/tasks/tools/"
    exit_code=1
else
    version=$(kubectl version --client --short 2>/dev/null || kubectl version --client 2>&1 | head -n 1)
    echo "✅ kubectl: $version"
fi
echo ""

# envoy
echo "【envoy】"
if ! command -v envoy &> /dev/null; then
    echo "❌ envoy が見つかりません"
    echo "   macOS: brew install envoy"
    echo "   Linux: https://www.envoyproxy.io/docs/envoy/latest/start/install"
    exit_code=1
else
    version=$(envoy --version 2>&1 | head -n 1)
    echo "✅ envoy: $version"
fi
echo ""

# bash
echo "【bash】"
if ! command -v bash &> /dev/null; then
    echo "❌ bash が見つかりません"
    exit_code=1
else
    version=$(bash --version | head -n 1)
    echo "✅ bash: $version"
fi
echo ""

# kubeconfig確認（オプション）
echo "【Kubernetes接続確認（オプション）】"
if kubectl cluster-info &> /dev/null; then
    context=$(kubectl config current-context 2>/dev/null)
    echo "✅ Kubernetesクラスタに接続可能"
    echo "   現在のコンテキスト: $context"
else
    echo "⚠️  Kubernetesクラスタに接続できません"
    echo "   kubectl-localmeshの起動時にエラーになる可能性があります"
    echo "   （オフラインモードでのEnvoy設定ダンプは可能）"
fi
echo ""

# GCP関連の依存関係（オプション - SSH Bastion使用時のみ必要）
echo "【GCP関連（オプション - SSH Bastion使用時のみ）】"
echo "ℹ️  GCP SSH Bastion経由のDB接続を使用する場合に必要です"
echo ""

# gcloud CLIの確認
echo "  - gcloud CLI"
if ! command -v gcloud &> /dev/null; then
    echo "    ⚠️  gcloud コマンドが見つかりません"
    echo "       インストール方法: https://cloud.google.com/sdk/docs/install"
else
    version=$(gcloud version 2>&1 | head -n 1)
    echo "    ✅ gcloud: $version"
fi
echo ""

# Application Default Credentials確認
echo "  - Application Default Credentials (ADC)"
if [ -n "$GOOGLE_APPLICATION_CREDENTIALS" ]; then
    if [ -f "$GOOGLE_APPLICATION_CREDENTIALS" ]; then
        echo "    ✅ 環境変数GOOGLE_APPLICATION_CREDENTIALSが設定されています"
        echo "       ファイル: $GOOGLE_APPLICATION_CREDENTIALS"
    else
        echo "    ⚠️  GOOGLE_APPLICATION_CREDENTIALSが設定されていますが、ファイルが存在しません"
        echo "       ファイル: $GOOGLE_APPLICATION_CREDENTIALS"
    fi
elif [ -f "$HOME/.config/gcloud/application_default_credentials.json" ]; then
    echo "    ✅ Application Default Credentialsが設定されています"
    echo "       ファイル: $HOME/.config/gcloud/application_default_credentials.json"
else
    echo "    ⚠️  Application Default Credentialsが見つかりません"
    echo "       設定方法: gcloud auth application-default login"
fi
echo ""

# 結果サマリー
echo "==================================="
if [ $exit_code -eq 0 ]; then
    echo "✅ すべての依存関係が満たされています"
    echo ""
    echo "次のステップ:"
    echo "  sudo ./bin/kubectl-localmesh -f services.yaml"
else
    echo "❌ 必須の依存関係が不足しています"
    echo "   上記のインストール方法を参照してください"
fi
echo "==================================="

exit $exit_code
