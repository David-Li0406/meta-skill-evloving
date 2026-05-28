---
name: app-development-flow
description: |
  App 開発の標準フロースキル。
  1.基盤做成 → 2.式様読取 → 3.設計 → 4.実装 → 5.テスト → 不足→循環
  の反復開発プロセスを定義。
version: 1.0.0
author: agentflow-team
triggers:
  - 開発フロー
  - 開発手順
  - アプリ開発
  - 実装手順
  - 設計から実装
tags:
  - workflow
  - development
  - agile
  - iteration
---

# App 開発標準フロー

## 全体フロー図

```
┌─────────────────────────────────────────────────────────┐
│                    App 開発フロー                        │
├─────────────────────────────────────────────────────────┤
│  ┌──────────┐                                           │
│  │ 1. 基盤  │ ─── テンプレートから骨架生成              │
│  │   做成   │     Docker/DB/API 基盤                    │
│  └────┬─────┘                                           │
│       ↓                                                 │
│  ┌──────────┐                                           │
│  │ 2. 式様  │ ─── ユーザー要件を分析                    │
│  │   読取   │     エンティティ・API 特定                │
│  └────┬─────┘                                           │
│       ↓                                                 │
│  ┌──────────┐                                           │
│  │ 3. 設計  │ ─── DB スキーマ・API 設計                 │
│  │          │     Pydantic スキーマ定義                 │
│  └────┬─────┘                                           │
│       ↓                                                 │
│  ┌──────────┐                                           │
│  │ 4. 実装  │ ─── Repository/Service/Router 実装       │
│  │          │     Alembic マイグレーション              │
│  └────┬─────┘                                           │
│       ↓                                                 │
│  ┌──────────┐     失敗                                  │
│  │ 5.テスト │ ─────────────┐                           │
│  │          │              │                            │
│  └────┬─────┘              │                            │
│       │ 成功               ↓                            │
│       │              ┌──────────┐                       │
│       │              │ 不足分析 │ ─→ 3. 設計 に戻る    │
│       ↓              └──────────┘                       │
│  ┌──────────┐                                           │
│  │ 完了     │                                           │
│  └──────────┘                                           │
└─────────────────────────────────────────────────────────┘
```

## フェーズ詳細

### 1. 基盤做成（Foundation）

**目的**: App の骨架を生成

**入力**:
- アプリ名、タイトル、説明
- DB 設定（名前、ユーザー、パスワード）
- オプション（Redis、履歴 DB、フロントエンド）

**出力**:
- `apps/{app_name}/` ディレクトリ一式

**手順**:
```bash
# 1. テンプレート生成
python -m agentflow.templates.template_manager generate \
  --template fullstack-app \
  --params '{"app_name": "xxx", ...}'

# 2. コンテナ起動確認
cd apps/xxx && docker-compose up -d

# 3. ヘルスチェック
curl http://localhost:8000/health
```

### 2. 式様読取（Requirements Analysis）

**目的**: ユーザー要件を構造化

**チェックリスト**:
- [ ] ユーザーストーリー一覧
- [ ] 主要エンティティ特定
- [ ] エンティティ間関係
- [ ] 必要 API エンドポイント
- [ ] 非機能要件（性能、セキュリティ）

### 3. 設計（Design）

**目的**: 技術設計

**成果物**:
1. **DB スキーマ** (`repositories/models.py`)
2. **API スキーマ** (`schemas/`)
3. **API エンドポイント設計** (`routers/`)

**設計パターン**:
```python
# Repository パターン
class EntityRepository:
    async def create(...) -> Entity
    async def find_by_id(id: UUID) -> Entity | None
    async def find_all(filters, pagination) -> list[Entity]
    async def update(id: UUID, data) -> Entity
    async def delete(id: UUID) -> bool

# Service パターン
class EntityService:
    def __init__(self, repo: EntityRepository):
        self.repo = repo
    async def process_business_logic(...) -> Result
```

### 4. 実装（Implementation）

**順序**:
1. `models.py` - エンティティ定義
2. `migrations/` - Alembic マイグレーション
3. `repositories/` - データアクセス層
4. `services/` - ビジネスロジック
5. `routers/` - API エンドポイント
6. `schemas/` - リクエスト/レスポンス

### 5. テスト（Testing）

**テスト種類**:
- 単体テスト: `tests/unit/`
- 統合テスト: `tests/integration/`
- E2E テスト: `tests/e2e/`

**実行**:
```bash
# 単体テスト
pytest tests/unit/ -v

# カバレッジ
pytest --cov=. --cov-report=html
```

### 不足分析・ループ

**トリガー**:
- テスト失敗
- 新規要件追加
- バグ発見

**対応**:
1. 原因分析
2. 影響範囲特定
3. 設計見直し（必要な場合）
4. 実装修正
5. 再テスト

## AI 助手への指示

新規 App 構築時、以下を確認してください：

1. **基盤做成前**: 必要なパラメータ（アプリ名、DB 設定等）
2. **式様読取時**: 主要エンティティと API エンドポイント
3. **設計時**: スキーマとモデルの妥当性
4. **実装時**: コード品質とベストプラクティス
5. **テスト時**: カバレッジと境界条件

不明点があれば、推測せずユーザーに確認してください。

