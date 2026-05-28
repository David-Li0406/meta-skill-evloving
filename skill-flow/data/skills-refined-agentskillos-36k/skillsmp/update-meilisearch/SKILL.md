---
name: update-meilisearch
description: "Meilisearchアップデートスキル。Dockerで最新版を確認し、更新があればバックアップ・データ移行を行いアップグレードする。"
---

# Meilisearch Update Skill

Meilisearchのバージョン確認・アップグレードを自動化するスキル。
**すべてのタスクはサブエージェントに委託して実行する。**

## 実行トリガー

以下のようなリクエストで起動:
- "Meilisearchをアップデートして"
- "Meilisearchの最新版を確認して"
- "/update-meilisearch"

## オーケストレーション方針

このスキルはマネージャーとして動作し、実際の作業はすべてサブエージェントに委託する。
各ステップで Task ツールを使用してサブエージェントを起動し、結果を受け取って次のステップに進む。

## ワークフロー

```
┌──────────────────────────────────────────────────────────────────┐
│ Step 1: バージョン確認（並列実行）                               │
│   → Bash エージェント x2                                        │
├──────────────────────────────────────────────────────────────────┤
│ Step 2: 更新判定・リリースノート確認                            │
│   → Bash エージェント                                           │
├──────────────────────────────────────────────────────────────────┤
│ Step 3: バックアップ作成                                         │
│   3-1. Meilisearch起動確認・起動                                 │
│   3-2. Dump作成（v1.32→v1.33のような互換性なしの場合）           │
│   3-3. Dumpファイルをホストにコピー                              │
│   → Bash エージェント                                           │
├──────────────────────────────────────────────────────────────────┤
│ Step 4: データ移行（互換性なしの場合）                           │
│   4-1. コンテナ停止・削除                                        │
│   4-2. ボリューム削除                                            │
│   4-3. 新しいボリューム作成                                      │
│   4-4. 新バージョンで --import-dump 付きで起動                   │
│   4-5. インポート完了後、一時コンテナを停止                      │
│   → Bash エージェント                                           │
├──────────────────────────────────────────────────────────────────┤
│ Step 5: docker-compose.yml 更新                                  │
│   → 直接 Edit ツールを使用                                      │
├──────────────────────────────────────────────────────────────────┤
│ Step 6: コンテナ再起動・検証                                     │
│   → Bash エージェント                                           │
├──────────────────────────────────────────────────────────────────┤
│ Step 7: ドキュメント更新                                         │
│   → 直接 Edit ツールを使用                                      │
└──────────────────────────────────────────────────────────────────┘
```

## サブエージェント委託詳細

### Step 1: バージョン確認

**並列で2つのBashエージェントを起動:**

```
Task 1-A: 現在のバージョン取得
- subagent_type: Bash
- prompt: |
    docker-compose.yml から現在のMeilisearchバージョンを取得してください。
    grep -o 'getmeili/meilisearch:v[0-9.]*' docker-compose.yml

Task 1-B: 最新バージョン取得
- subagent_type: Bash
- prompt: |
    GitHub APIからMeilisearchの最新バージョンを取得してください。
    curl -s https://api.github.com/repos/meilisearch/meilisearch/releases/latest | jq -r '.tag_name'
```

### Step 2: 更新判定

- 現在のバージョンと最新バージョンを比較
- 同じ場合: "最新版です" と報告して終了
- 異なる場合: リリースノートを確認して続行

```
Task 2: リリースノート確認
- subagent_type: Bash
- prompt: |
    Meilisearchの最新リリースノートを取得してください。
    curl -s https://api.github.com/repos/meilisearch/meilisearch/releases/latest | jq -r '.body' | head -80
```

### Step 3: バックアップ作成

```
Task 3-1: Meilisearch起動確認・起動
- subagent_type: Bash
- prompt: |
    Meilisearchが起動しているか確認し、起動していなければ起動してください。
    1. curl -s http://localhost:7700/health でヘルスチェック
    2. 起動していない場合: docker compose up -d meilisearch
    3. ヘルスチェックが通るまで待機（最大60秒）

Task 3-2: Dump作成
- subagent_type: Bash
- prompt: |
    MeilisearchのDumpを作成してください。
    1. curl -X POST -H "Authorization: Bearer development_master_key" http://localhost:7700/dumps
    2. タスク完了を確認: curl -H "Authorization: Bearer development_master_key" "http://localhost:7700/tasks?types=dumpCreation&limit=1"
    3. Dumpファイル名を確認: docker compose exec meilisearch ls /meili_data/dumps/

Task 3-3: Dumpファイルをホストにコピー
- subagent_type: Bash
- prompt: |
    DumpファイルをホストのFSにコピーしてください。
    1. mkdir -p .meilisearch/dumps
    2. docker compose cp meilisearch:/meili_data/dumps/<dump_file> .meilisearch/dumps/
```

### Step 4: データ移行（互換性なしの場合）

**重要: v1.32 → v1.33 のようにDumplessアップグレード非対応の場合のみ実行**

```
Task 4: データ移行
- subagent_type: Bash
- prompt: |
    Meilisearchのデータを新バージョンに移行してください。
    1. docker compose stop meilisearch && docker compose rm -f meilisearch
    2. docker volume rm thac_meilisearch_data
    3. docker volume create thac_meilisearch_data
    4. docker run --rm \
         -v thac_meilisearch_data:/meili_data \
         -v $(pwd)/.meilisearch/dumps:/dumps:ro \
         -e MEILI_MASTER_KEY=development_master_key \
         getmeili/meilisearch:v<新バージョン> \
         meilisearch --import-dump /dumps/<dump_file>
    5. インポート完了のログを確認後、Ctrl+C で一時コンテナを停止

    ※ --import-dump 付きで起動するとインポート後もMeilisearchが稼働し続けます
    ※ 一時コンテナなので停止してもデータは永続化されています
```

### Step 5: docker-compose.yml 更新

**直接 Edit ツールを使用:**
```yaml
# Before
image: getmeili/meilisearch:v<旧バージョン>

# After
image: getmeili/meilisearch:v<新バージョン>
```

### Step 6: コンテナ再起動・検証

```
Task 6: 再起動・検証
- subagent_type: Bash
- prompt: |
    Meilisearchを再起動して検証してください。
    1. docker compose up -d meilisearch
    2. ヘルスチェック待機（最大60秒）
    3. バージョン確認: curl -s -H "Authorization: Bearer development_master_key" http://localhost:7700/version | jq
    4. インデックス確認: curl -s -H "Authorization: Bearer development_master_key" http://localhost:7700/indexes | jq
```

### Step 7: ドキュメント更新

**直接 Edit ツールを使用:**
`.kiro/steering/meilisearch.md` のバージョン記載を更新

## 障害復旧

### 起動失敗（os error 11 - Resource temporarily unavailable）

バージョンアップグレード後にコンテナが起動しない場合の対処法:

```
Task: データ復旧
- subagent_type: Bash
- prompt: |
    Meilisearchの起動障害を復旧してください。
    1. docker compose stop meilisearch && docker compose rm -f meilisearch
    2. ボリュームを使用中のコンテナがあれば削除:
       docker ps -a --filter volume=thac_meilisearch_data -q | xargs -r docker rm -f
    3. docker volume rm thac_meilisearch_data
    4. docker volume create thac_meilisearch_data
    5. docker run --rm \
         -v thac_meilisearch_data:/meili_data \
         -v $(pwd)/.meilisearch/dumps:/dumps:ro \
         -e MEILI_MASTER_KEY=development_master_key \
         getmeili/meilisearch:v<現バージョン> \
         meilisearch --import-dump /dumps/meilisearch-dump.dump
    6. インポート完了確認後 Ctrl+C で停止
    7. docker compose up -d meilisearch
    8. ヘルスチェック確認: curl -s http://localhost:7700/health
```

この問題は以下の原因で発生します:
- バージョン間のデータベースフォーマット非互換
- 一時コンテナがボリュームをロックしたまま残存
- dump経由の移行が正常に完了していない

## 重要な注意事項

### バージョン互換性

| 移行パターン | 方法 |
|-------------|------|
| v1.12+ → v1.13+ (同一マイナー内) | Dumplessアップグレード（自動移行） |
| v1.32 → v1.33 | **Dump経由の移行が必要** |

### ロールバック手順

問題が発生した場合は Bash エージェントに以下を委託:
1. docker compose stop meilisearch
2. docker-compose.yml を元のバージョンに戻す
3. スナップショットから復元（必要な場合）
4. docker compose up -d meilisearch

## 環境変数

| 変数 | 説明 | デフォルト |
|-----|------|-----------|
| `MEILI_MASTER_KEY` | API認証キー | `development_master_key` |
| `MEILI_URL` | Meilisearch URL | `http://localhost:7700` |

## 関連ファイル

- `docker-compose.yml` - Meilisearchサービス定義
- `.kiro/steering/meilisearch.md` - Meilisearch設定ガイド
- `.meilisearch/dumps/` - Dumpファイル保存先
- `Makefile` - `logs-meilisearch`, `shell-meilisearch` コマンド

## 参考資料

- [Meilisearch Releases](https://github.com/meilisearch/meilisearch/releases)
- [Meilisearch Update Guide](https://www.meilisearch.com/docs/learn/update_and_migration/updating)
