---
name: design-plan
description: "設計計画スキル。TDD開発前の設計フェーズを支援し、仕様ドキュメントを作成。Use when: 新機能・API・画面・インフラの設計、実装前の仕様策定を依頼された時。"
---

# 設計計画（Design Plan）

TDD開発を開始する前の設計フェーズを支援します。実装前に設計仕様を文書化し、この仕様を元にtest-driven-developmentスキルで実装を開始できる状態を作ります。

## ワークフロー

```
1. design-plan スキル実行
   ↓ 設計ドキュメント作成 (docs/design/ 配下)
2. 補助ツールでの設計レビュー
   ↓ Swagger UI, Storybook, Terraform plan 等で確認
3. test-driven-development スキル実行
   ↓ Red-Green-Refactor サイクル
4. 実装完了
```

## 開発タイプ別ガイド

開発タイプに応じた詳細ガイドを参照してください。

| 開発タイプ               | 基本補助ツール                                  | 詳細ガイド                                                                           |
| ------------------------ | ----------------------------------------------- | ------------------------------------------------------------------------------------ |
| **CLI開発**              | CLIフレームワーク (oclif, cobra, clap, click等) | [resources/cli_design_desc.md](./resources/cli_design_desc.md)                       |
| **API開発**              | **Swagger UI / OpenAPI Specification**          | [resources/api_design_desc.md](./resources/api_design_desc.md)                       |
| **画面開発**             | **Storybook**                                   | [resources/ui_design_desc.md](./resources/ui_design_desc.md)                         |
| **モバイルアプリ開発**   | Figma, React Native Storybook, Flutter DevTools | [resources/mobile_design_desc.md](./resources/mobile_design_desc.md)                 |
| **クラウドインフラ構築** | **Terraform / OpenTofu**                        | [resources/infrastructure_design_desc.md](./resources/infrastructure_design_desc.md) |

## 詳細情報

以下の詳細情報は [REFERENCE.md](./REFERENCE.md) を参照してください：

- 設計計画の目的と原則
- 設計フェーズの実施手順
- 設計ドキュメントの配置構造
- 設計品質チェックポイント
- 他のスキルとの連携
- 補助ツールの選定基準
- カスタマイズガイド
- 注意事項とFAQ

---

**次のステップ**: 設計完了後は [test-driven-development](../test-driven-development/SKILL.md) スキルで実装を開始してください。
