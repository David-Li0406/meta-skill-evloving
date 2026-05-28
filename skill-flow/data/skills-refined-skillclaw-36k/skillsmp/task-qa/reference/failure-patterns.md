# 失敗分類の実践例（10パターン）

QAテスト失敗時の分類判断に迷った場合の参考事例集。

---

## A: 実装ミス

### 例1: トークン検証エラー
**症状**: `TypeError: Cannot read property 'token' of undefined`
**判定**: **A: 実装ミス**（nullチェック漏れ）
**戻し先**: task-executer

### 例5: ユニットテスト失敗
**症状**: `pnpm test` で5件失敗
**判定**: **A: 実装ミス**
**戻し先**: task-executer

### 例6: Lintエラー
**症状**: `pnpm lint` でBiomeエラー10件
**判定**: **A: 実装ミス**（コーディング規約違反）
**戻し先**: task-executer

### 例8: ビルドエラー
**症状**: `pnpm build` でTypeScriptエラー
**判定**: **A: 実装ミス**（型エラー）
**戻し先**: task-executer

---

## B: 要件齟齬

### 例2: バリデーションエラーメッセージ不一致
**症状**: requirements.md「400エラー」、実装「422エラー」
**判定**: **B: 要件齟齬**（ステータスコード不明確）
**戻し先**: requirements.md修正 → task-executer

### 例9: AC間の矛盾
**症状**: AC1.2「即座削除」vs AC1.3「バッチ削除」
**判定**: **B: 要件齟齬**（AC間矛盾）
**戻し先**: requirements.md修正 → task-executer

---

## C: 設計不備

### 例3: トランザクション未実装
**症状**: 競合状態で整合性が保証されない
**判定**: **C: 設計不備**（トランザクション設計欠如）
**戻し先**: design.md修正 → task-executer

### 例10: DBスキーマ設計ミス
**症状**: インデックス不適切でパフォーマンス劣化
**判定**: **C: 設計不備**（スキーマ設計ミス）
**戻し先**: design.md修正 → task-executer

---

## D: 環境問題

### 例4: PostgreSQL接続エラー
**症状**: `Error: connect ECONNREFUSED 127.0.0.1:5432`
**判定**: **D: 環境問題**（コンテナ未起動）
**戻し先**: qa再実行（環境修復後）

### 例7: Playwright MCPタイムアウト
**症状**: `Timeout 30000ms exceeded`（ネットワーク遅延）
**判定**: **D: 環境問題**
**戻し先**: qa再実行
