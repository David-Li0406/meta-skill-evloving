---
name: chrome-extension-dev
description: Chrome拡張機能開発に関する包括的なガイド。ベストプラクティス、アンチパターンの回避、型安全性、Manifest V3への準拠をサポート。Claudeが以下のためにChrome拡張機能を扱う場合に使用：(1) 新規拡張機能の計画・作成、(2) 既存コードのデバッグ・修正、(3) セキュリティレビュー、(4) Manifest V2からV3への移行、(5) TypeScript型の問題解決。
license: MIT
---

# Chrome Extension Development Skill

このスキルは、安全で高性能なChrome拡張機能（Manifest V3）を開発するためのガイダンスを提供します。

## 重要な原則

Chrome拡張機能開発において、以下の原則を常に守ってください。

1.  **Manifest V3 準拠**: Service Workerベースのアーキテクチャを採用し、永続的なバックグラウンドページは使用しない。
2.  **非同期処理の徹底**: `chrome.runtime.lastError` のチェックが必要なコールバックAPIではなく、Promise（async/await）を使用する。
3.  **状態管理**: グローバル変数に依存せず、必ず `chrome.storage` API を使用して状態を永続化する。Service Workerはいつでも停止する可能性がある。
4.  **セキュリティ**: `innerHTML` の使用を避け、適切なCSPを設定する。ユーザー入力や外部データは必ずサニタイズまたは検証する。

## リファレンスガイド

詳細な情報は以下のリファレンスドキュメントを参照してください。

### [ベストプラクティス](references/best-practices.md)
Manifest V3の採用、状態管理、メッセージパッシング、セキュリティ対策、非同期処理の推奨パターンについて解説しています。
**使用タイミング**: 新規機能の実装前、コードレビュー時。

### [アンチパターン](references/anti-patterns.md)
避けるべき一般的な間違い（グローバル変数の使用、不適切なポート管理、Promiseとcallbackの混在など）と、その修正方法を解説しています。
**使用タイミング**: デバッグ時、コードの品質改善時。

### [型安全性](references/type-safety.md)
TypeScriptを使用した開発において、`@types/chrome` の活用方法、`chrome.storage` やメッセージパッシングの型安全な実装、Valibotを使用したランタイム検証について解説しています。
**使用タイミング**: TypeScriptでの実装時、データ検証ロジックの作成時。
