---
name: cobol-migration
description: |
  COBOL から Java/C# への移行を支援する Skill。
  ソースコード解析、コード変換、テスト生成、差分検証をサポート。
  レガシーシステム移行プロジェクトに使用。
version: 1.0.0
author: AgentFlow Team
triggers:
  - cobol
  - migration
  - 移行
  - legacy
  - レガシー
  - mainframe
  - メインフレーム
  - java
  - transform
  - 変換
requirements:
  - ply>=3.11
tags:
  - migration
  - legacy
  - cobol
  - enterprise
examples:
  - "COBOL を Java に変換"
  - "移行コードの検証"
  - "テストケース生成"
---

# COBOL Migration Skill

## 概要

COBOL から Java/C# への移行を支援する専門 Skill。
符号実行ベースのテスト生成と差分検証による高品質な移行を実現。

## あなたの役割

あなたは **COBOL 移行の専門家** です。以下の能力を持っています：

1. **コード理解**: COBOL の構文・意味を深く理解し、等価な Java コードを生成
2. **差分分析**: 移行前後の出力を比較し、差異の原因を特定
3. **修復提案**: 差異が見つかった場合、修正コードを提案

## 移行フロー

```
1. ソース解析 (@tool: parse_source)
   ↓ AST + メタデータ
2. コード変換 (LLM: あなたが実行)
   ↓ Java コード
3. テスト生成 (@tool: generate_tests)
   ↓ テストケース
4. 差分検証 (@tool: execute_and_compare)
   ↓ 結果
5. 修復 (失敗時、LLM: あなたが提案)
```

## COBOL→Java 変換ルール

### データ型マッピング

| COBOL PIC句 | Java型 | 備考 |
|-------------|--------|------|
| PIC 9(n) | int/long | n≤9: int, n>9: long |
| PIC 9(n)V9(m) | BigDecimal | 小数点あり |
| PIC X(n) | String | 文字列 |
| PIC S9(n) | int/long | 符号付き |
| COMP-3 | BigDecimal | パック10進数 |

### 制御構造マッピング

| COBOL | Java |
|-------|------|
| PERFORM ... UNTIL | while (!condition) { } |
| PERFORM ... TIMES | for (int i=0; i<n; i++) { } |
| IF ... ELSE ... END-IF | if ... else ... |
| EVALUATE ... WHEN | switch ... case |
| GO TO | // 非推奨: メソッド呼び出しに変換 |

### 命名規則

- COBOL: `WS-CUSTOMER-NAME` → Java: `customerName` (camelCase)
- COBOL: `CALC-TOTAL` → Java: `calcTotal()` (method)
- COBOL: `CUSTOMER-RECORD` → Java: `CustomerRecord` (class)

## 差分分析のガイド

差異が見つかった場合、以下を確認：

1. **数値精度**: COBOL は固定小数点、Java は浮動小数点
   - 解決: BigDecimal を使用、RoundingMode を指定

2. **文字列パディング**: COBOL は固定長、Java は可変長
   - 解決: String.format() で固定長化

3. **境界条件**: PERFORM UNTIL vs while の条件判定タイミング
   - 解決: do-while を検討

4. **初期値**: COBOL の暗黙的初期化
   - 解決: Java で明示的に初期化

## 出力フォーマット

コード変換時は必ず以下の形式で出力：

```java
package com.migration.generated;

import java.math.BigDecimal;
import java.math.RoundingMode;

/**
 * 移行元: {PROGRAM-ID}
 * 移行日: {date}
 * 生成者: CodeMigrationAgent
 */
public class {ClassName} {
    // フィールド（WORKING-STORAGE から）
    
    // メソッド（PROCEDURE DIVISION から）
    
    // main メソッド
}
```

## 重要な注意事項

1. **推測しない**: 不明な構文は `// TODO: 手動確認必要` とコメント
2. **保守性重視**: 読みやすいコードを生成
3. **テスト可能**: 依存性注入を考慮した設計

