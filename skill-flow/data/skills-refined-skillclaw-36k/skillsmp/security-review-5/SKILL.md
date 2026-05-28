---
name: security-review
description: RBAC/監査ログ/秘密情報/マルチテナント越境/LLMプロンプト注入の観点でレビューする。
---

## 使いどころ（トリガー例）

- 「セキュリティレビュー」「越境が不安」「監査ログ」「APIキー管理」

## 観点（最低限）

- 認証・認可（RBAC、tenant_id の確定、越境防止）
- 監査ログ（start/approve/reject/retry/cancel/download/delete が記録されるか）
- 秘密情報（暗号化保管、平文ログ禁止、`.env` 不可視化）
- storage（tenant別prefix、署名URLの権限チェック、有効期限）
- LLM（プロンプト注入・データ流出の防止、PII の扱い）
