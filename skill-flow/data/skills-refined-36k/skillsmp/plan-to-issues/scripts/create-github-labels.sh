#!/bin/sh
set -eu

# create-github-labels.sh
# 指定した GitHub リポジトリに共通ラベルを一括作成/更新します。
# 依存: gh (GitHub CLI)
# 使い方:
#   REPO=owner/repo ./scripts/create-github-labels.sh
# オプション:
#   DRY_RUN=1      変更を加えずに実行内容のみ表示
#   FORCE_UPDATE=1 既存ラベルに対して色/説明を上書き更新
#   REPO=...       対象リポジトリ（省略時はカレントの gh コンテキストから推定）

REPO=${REPO:-}
DRY_RUN=${DRY_RUN:-0}
FORCE_UPDATE=${FORCE_UPDATE:-0}

log() { printf '%s\n' "$*"; }
err() { printf 'Error: %s\n' "$*" >&2; }

require_cmd() {
  command -v "$1" >/dev/null 2>&1 || { err "$1 が見つかりません。インストールしてください。"; exit 1; }
}

usage() {
  cat <<EOF
Usage:
  REPO=owner/repo ./scripts/create-github-labels.sh [options]

Env options:
  REPO=owner/repo   対象リポジトリ（未指定時は gh から推定）
  DRY_RUN=1         ドライラン（実行内容のみ表示）
  FORCE_UPDATE=1    既存ラベルにも color/description を上書き
EOF
}

# 前提チェック
require_cmd gh

# REPO が未指定なら gh から推定
if [ -z "${REPO}" ]; then
  if gh repo view >/dev/null 2>&1; then
    REPO=$(gh repo view --json nameWithOwner --jq .nameWithOwner)
  else
    err "REPO=owner/repo を指定するか、git/gh で対象リポジトリにいる必要があります。"
    usage
    exit 1
  fi
fi

log "Target repo: ${REPO}"

# 既存ラベルの取得（名前のみ）
EXISTING_NAMES=$(gh label list --repo "${REPO}" --limit 300 --json name --jq '.[].name' 2>/dev/null || true)

exists() {
  echo "${EXISTING_NAMES}" | grep -Fx "$1" >/dev/null 2>&1
}

apply_label() {
  NAME=$1
  COLOR=$2
  DESC=$3

  if exists "${NAME}"; then
    if [ "${FORCE_UPDATE}" = "1" ]; then
      if [ "${DRY_RUN}" = "1" ]; then
        log "[DRY] update ${NAME} color=${COLOR} desc='${DESC}'"
      else
        gh label edit "${NAME}" \
          --repo "${REPO}" \
          --color "${COLOR}" \
          --description "${DESC}" >/dev/null
        log "updated: ${NAME}"
      fi
    else
      log "skip (exists): ${NAME}"
    fi
  else
    if [ "${DRY_RUN}" = "1" ]; then
      log "[DRY] create ${NAME} color=${COLOR} desc='${DESC}'"
    else
      # --force は同名があっても成功にするための冗長保険
      if gh label create "${NAME}" --repo "${REPO}" --color "${COLOR}" --description "${DESC}" --force >/dev/null 2>&1; then
        :
      else
        gh label create "${NAME}" --repo "${REPO}" --color "${COLOR}" --description "${DESC}" >/dev/null
      fi
      log "created: ${NAME}"
    fi
  fi
}

# ラベル定義（name,color,description）
# color は # を付けない 6 桁 HEX
cat <<'EOF_LABELS' | while IFS=, read -r NAME COLOR DESC; do
# 種別
type:epic,5319e7,エピック/親Issue
type:feature,1f6feb,新機能/機能追加
type:migration,d4c5f9,移行/リファクタリング
type:chore,8b949e,雑務/周辺整備
type:test,8e44ad,テスト関連
type:docs,0e8a16,ドキュメント関連

# 領域
area:frontend,fbca04,フロントエンド領域
area:server,7057ff,バックエンド/サーバ領域
area:shared,ededed,共有/横断領域

# 優先度
priority:P1,d73a4a,最優先（ブロッカー）
priority:P2,ff9f1a,高優先度
priority:P3,ffd37a,中優先度

# 規模
size:S,0e8a16,小（<0.5日）
size:M,2ea043,中（~1-2日）
size:L,3fb950,大（>2日）
EOF_LABELS
  # 空行/コメントをスキップ
  [ -z "${NAME}" ] && continue
  case "${NAME}" in
    \#*) continue;;
  esac
  apply_label "${NAME}" "${COLOR}" "${DESC}"
done

log "Done: labels processed for ${REPO}"
