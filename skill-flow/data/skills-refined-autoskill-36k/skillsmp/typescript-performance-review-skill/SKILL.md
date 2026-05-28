---
name: typescript-performance-review-skill
description: TypeScript/Reactパフォーマンスレビュースキル。測定ファーストの最適化観点でコードをレビュー。フロントエンド（re-render、バンドルサイズ）、バックエンド（N+1、キャッシュ）、API（ペイロード、圧縮）のパフォーマンス問題を検出。「パフォーマンスレビュー」「速度改善」「最適化チェック」などのリクエスト時に使用。
---

# パフォーマンスレビュー

測定ファーストのパフォーマンス最適化観点でコードをレビューするスキル。

## 基本理念

- **測定してから最適化**: 推測ではなく実測に基づく
- **ボトルネック特定**: 最も影響の大きい部分から改善
- **ユーザー中心**: Core Web Vitals を重視

## チェック項目

### フロントエンド
- 不要な re-render 防止
- バンドルサイズ最適化
- 画像最適化
- Code splitting 実装
- キャッシュ戦略

### バックエンド
- N+1 クエリ問題なし
- 適切なキャッシュ
- 非同期処理活用
- メモリリーク防止
- データベース最適化

### API
- ペイロードサイズ最小化
- 圧縮適用
- ページネーション実装
- レート制限設定

## 重要度分類

| 重要度 | 内容 |
|:-|:-|
| Critical | ページロード > 3秒、APIレスポンス > 1秒、メモリリーク、CPU使用率 > 80% |
| High | バンドルサイズ > 1MB、不要なre-render、非効率クエリ、キャッシュ未実装 |
| Medium | 画像未最適化、軽微なパフォーマンス改善、モニタリング強化 |

## プロファイリングツール

### フロントエンド
- Chrome DevTools: Performance, Memory, Network
- React DevTools Profiler
- Lighthouse
- WebPageTest

### バックエンド
- Node.js: built-in profiler, clinic.js
- Database: EXPLAIN, query profiler
- APM: New Relic, DataDog

詳細なパターンは `references/performance-patterns.md` を参照。
