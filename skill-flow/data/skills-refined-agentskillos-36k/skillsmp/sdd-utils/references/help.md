# help - SDDワークフローヘルプ

## 実行内容

SDDワークフローの全体像を説明する。

## 出力例

```
## SDD (Spec Driven Development)

仕様書に基づいて段階的に実装を進める開発手法です。

### Phase構成
| Phase | 目的 | 主要コマンド |
|-------|------|-------------|
| 0 | プロジェクト方針 | /sdd:steering |
| 1 | タスク初期化・調査 | /sdd:init-task, /sdd:conduct-research |
| 2 | 要件・技術定義 | /sdd:define-requirements, /sdd:define-technical |
| 3 | 検証・明確化 | /sdd:clarify-spec, /sdd:quality-check |
| 4 | Phase構成決定 | /sdd:plan-phases |
| 5 | Phase詳細計画 | /sdd:breakdown-phase |
| 6 | 実装 | /sdd:implement-phase, /sdd:sync-spec |
| 7 | 検証 | /sdd:verify-phase |

### クイックスタート
1. /sdd:steering（初回のみ）
2. /sdd:init-task <説明>
3. 各コマンド完了時に次のアクションが案内されます

### 詳細情報
- ステアリングドキュメント: `.claude/skills/steering/SKILL.md`
- 仕様書: `specs/{taskname}/overview.md`
- sdd-webappダッシュボードで進捗可視化
```

## 関連コマンド

- `/sdd:steering` - プロジェクト方針定義
- `/sdd:init-task` - タスク初期化
- `/sdd:utils status` - ステータス確認
