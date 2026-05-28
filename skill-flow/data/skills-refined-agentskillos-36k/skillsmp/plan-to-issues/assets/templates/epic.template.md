# [Epic] {機能名}: 実装計画と進行管理

## 背景 / 目的

- 機能名: {機能名}
- 設計方針の要点（抜粋）: {アーキテクチャ/選定理由/判断基準}

## スコープ

- コンポーネント: ComponentA, ComponentB
- サービス/ユーティリティ: ...
- 移行フェーズ: Phase1〜4

## サブ Issue（Tasklist）

> 使い方: まず下記チェックリストにタスク名だけを書き出し、作成後に GitHub の「Convert to sub-issues」（または「Create sub-issues」）を押して子 Issue 化してください。以降は進捗バーが自動更新され、親子リンク（tracked by）が自動で張られます。

- [ ] ComponentA: create/parse を実装
- [ ] ComponentA Utils: validate/transform を実装
- [ ] ComponentB: 型/ファクトリを実装
- [ ] Phase 1: 基本実装
- [ ] Phase 2: 既存コード移行
- [ ] Phase 3: テスト/ドキュメント
- [ ] Phase 4: 最適化/クリーンアップ
- [ ] テスト整備
- [ ] パフォーマンス検討
- [ ] セキュリティ/エラー対策
- [ ] ドキュメント更新

## 受け入れ条件（DoD）

- 子 Issue が全て Close
- 相互参照（エピック ⇄ 子）が揃っている
- ドキュメント/テストが最新
