---
name: codex
description: Guide for using Codex CLI for code reviews and specs.
metadata:
  owner: user
  version: "0.1.0"
---

# Codex CLI 使い方（このリポジトリ向け）

このドキュメントは、Codex CLI を使ってコードレビューや仕様相談を行うための最小ガイドです。
コマンドは `codex --help` の出力に基づいています。

## 基本コマンド

### 1) インタラクティブに開始
```bash
codex
```

### 2) 初期プロンプト付きで開始
```bash
codex "このリポジトリのビルド手順を要約して"
```

### 3) 作業ディレクトリを指定
```bash
codex -C /path/to/Pyrope
```

### 4) モデルを指定
```bash
codex -m o3 "変更点のリスクを洗い出して"
```

### 5) Web検索を有効化（必要な場合）
```bash
codex --search "最新の .NET 10 の変更点を調べて"
```

### 6) セッション再開・分岐
```bash
codex resume --last
codex fork --last
```

### 7) 直前の提案差分を適用
```bash
codex apply
```

---

## コードレビュー用途

### 未コミットの変更をレビュー
```bash
codex review --uncommitted
```

### ベースブランチとの差分をレビュー
```bash
codex review --base main
```

### 特定コミットの変更をレビュー
```bash
codex review --commit <SHA>
```

### レビュー観点を追加
```bash
codex review --uncommitted "重大バグ/互換性/テスト漏れ/性能劣化の観点でレビュー"
```

---

## 仕様相談・設計相談用途

### 仕様書を前提に相談（インタラクティブ）
```bash
codex "prompt/SPEC.md と prompt/PLAN.md を参照して、X機能の追加方針を提案して"
```

### 仕様差分の影響分析
```bash
codex "prompt/SPEC.md を前提に、Yの仕様変更がテストに与える影響を整理して"
```

### 非対話での相談（スクリプト向け）
```bash
echo "prompt/SPEC.md を前提に最小実装の手順を箇条書きで" | codex exec -
```
