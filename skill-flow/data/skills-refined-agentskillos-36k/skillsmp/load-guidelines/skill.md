---
name: load-guidelines
description: ガイドライン自動読み込み - プロジェクトの技術スタックを検出し、必要なガイドラインのみをセッションに適用。トークン節約。
---

# プロジェクト適応型ガイドライン読み込み

## 使用方法

```
/load-guidelines        # サマリーのみ（軽量、推奨）
/load-guidelines full   # サマリー + 詳細ガイドライン
```

> **⚠️ トークン節約注意**
> - デフォルト（サマリーのみ）を推奨。ほとんどの作業はサマリーで十分
> - `full`オプションは追加で約5,500トークン消費
> - 詳細なコード例が必要な場合はContext7を活用

## 使用タイミング

- 開発作業開始時（プロジェクトモード）
- Skill実行時（Skillモード - requires-guidelines自動読み込み）

---

## モード1: プロジェクト検出（セッション開始時）

### Step 1: 技術スタック検出

以下のファイル存在を確認:

| ファイル | 判定 |
|---------|------|
| `package.json` + next依存 | Next.js |
| `package.json` + react依存 | React |
| `package.json` + typescript依存 | TypeScript |
| `go.mod` | Go |
| `*.tf` | Terraform |
| `Dockerfile` / `docker-compose.yml` | Docker |
| `serverless.yml` / `template.yaml` | Lambda |
| `kubernetes/` / `k8s/` | Kubernetes |

### Step 2: ガイドライン読み込み（2段階）

#### デフォルト: サマリーのみ（~2,500トークン）

検出された技術スタックに応じてサマリーを読み込む:

| 条件 | サマリー |
|-----|---------|
| 共通（必須） | `~/.claude/guidelines/summaries/common-summary.md` |
| TypeScript | `~/.claude/guidelines/summaries/typescript-summary.md` |
| Next.js/React | `~/.claude/guidelines/summaries/nextjs-react-summary.md` |
| Go | `~/.claude/guidelines/summaries/golang-summary.md` |

#### `full` オプション: 詳細ガイドライン追加（+~5,500トークン）

サマリーに加えて詳細ガイドラインを読み込む:

**共通:**
- `~/.claude/guidelines/common/claude-code-tips.md`
- `~/.claude/guidelines/common/code-quality-design.md`
- `~/.claude/guidelines/common/development-process.md`

**言語別（検出時のみ）:**

| 条件 | ガイドライン |
|-----|-------------|
| TypeScript | `~/.claude/guidelines/languages/typescript.md` |
| Next.js/React | `~/.claude/guidelines/languages/nextjs-react.md` |
| Go | `~/.claude/guidelines/languages/golang.md` |

**インフラ（検出時のみ）:**

| 条件 | ガイドライン |
|-----|-------------|
| Terraform | `~/.claude/guidelines/infrastructure/terraform.md` |
| Lambda | `~/.claude/guidelines/infrastructure/aws-lambda.md` |
| ECS/Fargate | `~/.claude/guidelines/infrastructure/aws-ecs-fargate.md` |
| EKS/K8s | `~/.claude/guidelines/infrastructure/aws-eks.md` |
| EC2 | `~/.claude/guidelines/infrastructure/aws-ec2.md` |

### Step 3: 結果報告

検出結果を報告し、**検出された言語名を記憶**:
- 検出言語: go, ts, react など（カンマ区切り）
- 共通のみの場合: common
- モード: summary | full

---

## モード2: Skill連携（requires-guidelines）

### 概要

Skillのフロントマターに`requires-guidelines`が定義されている場合、そのSkill実行時に関連ガイドラインを自動読み込み。

### Skillフロントマター例

```yaml
---
name: typescript-backend
description: TypeScriptバックエンド開発
requires-guidelines:
  - typescript
  - common
---
```

### ガイドライン識別子マッピング

**共通**: `common` → `common/*.md`

**言語別**:
| 識別子 | パス |
|--------|------|
| `typescript` | `languages/typescript.md` |
| `golang` | `languages/golang.md` |
| `nextjs-react` | `languages/nextjs-react.md` |
| `tailwind` | `languages/tailwind.md` |
| `shadcn` | `languages/shadcn.md` |

**インフラ**: `terraform`, `kubernetes` → `infrastructure/`

**設計**: `clean-architecture`, `ddd` → `design/`

**アーカイブ**: `microservices-kubernetes`, `ui-ux`, `requirements-engineering` → `guidelines-archive/`

### 自動読み込みフロー

1. Skill呼び出し時、フロントマターの`requires-guidelines`を確認
2. 未読み込みのガイドラインがあれば読み込み
3. 既に読み込み済みならスキップ（重複防止）

---

## ガイドライン一覧

### common（共通）
- `claude-code-tips.md` - Claude Code活用法
- `code-quality-design.md` - コード品質
- `development-process.md` - 開発プロセス
- `error-handling-patterns.md` - エラーハンドリング
- `testing-guidelines.md` - テスト指針
- `type-safety-principles.md` - 型安全性

### languages（言語）
- `typescript.md` - TypeScript
- `golang.md` - Go
- `nextjs-react.md` - Next.js/React

### infrastructure（インフラ）
- `terraform.md` - Terraform
- `aws-eks.md` - EKS/Kubernetes
- `aws-ecs-fargate.md` - ECS/Fargate
- `aws-lambda.md` - Lambda
- `aws-ec2.md` - EC2

### design（設計）
- `clean-architecture.md` - クリーンアーキテクチャ
- `domain-driven-design.md` - DDD
- `microservices-kubernetes.md` - マイクロサービス
- `ui-ux-guidelines.md` - UI/UX

---

## 使用例

### セッション開始時（推奨）
```
/load-guidelines
→ プロジェクト検出 → サマリーのみ読み込み（軽量）
→ 出力: "guidelines(ts,react) [summary]"
```

### 詳細が必要な場合
```
/load-guidelines full
→ プロジェクト検出 → サマリー + 詳細ガイドライン読み込み
→ 出力: "guidelines(ts,react) [full]"
```

### Skill実行時（自動）
```
/review でsecurity-error-reviewスキル実行
→ requires-guidelines: [common] を確認
→ common未読み込みなら common-summary.md を読み込み
```

### 実装中に詳細が必要になった場合
```
（サマリー読み込み済みの状態で）
/load-guidelines full
→ 未読み込みの詳細ガイドラインのみ追加読み込み
```
