---
name: code-analysis
description: コード分析・移行のための包括的なスキルセット。静的分析、複雑度評価、依存関係マッピング、セキュリティスキャン、移行計画を提供。
version: "1.0.0"
triggers:
  - コード分析
  - 静的分析
  - 複雑度
  - 依存関係
  - セキュリティ
  - 移行
  - リファクタリング
requirements:
  - pydantic
tags:
  - code-analysis
  - migration
  - security
---

# コード分析・移行スキルパッケージ

## 概要

このスキルパッケージは、コードベースの分析と移行に必要な一連の機能を提供します。

## 含まれるスキル

### 1. RepoConnector（リポジトリ接続）
Git/SVNリポジトリに接続し、コードベース情報を取得します。

```python
from agentflow.skills.builtin.code_analysis import RepoConnector

connector = RepoConnector()
repo = await connector.connect(
    url="https://github.com/org/repo.git",
    branch="main",
)
```

### 2. StaticAnalyzer（静的分析）
コードの品質問題、バグ、セキュリティ問題を検出します。

```python
from agentflow.skills.builtin.code_analysis import StaticAnalyzer

analyzer = StaticAnalyzer()
result = await analyzer.analyze(files=repo.files)
```

**検出カテゴリ**:
- バグ
- コードスメル
- 脆弱性
- 重複
- スタイル違反

### 3. ComplexityScorer（複雑度評価）
コードの複雑度を評価し、リファクタリング優先度を提案します。

```python
from agentflow.skills.builtin.code_analysis import ComplexityScorer

scorer = ComplexityScorer(ccn_threshold=10)
report = await scorer.score(files=repo.files)
```

**メトリクス**:
- 循環的複雑度（CCN）
- 認知的複雑度
- コード行数（LOC）
- ネスト深度
- 保守性指数

### 4. DependencyMapper（依存関係マッピング）
依存関係を分析し、依存グラフを構築します。

```python
from agentflow.skills.builtin.code_analysis import DependencyMapper

mapper = DependencyMapper()
graph = await mapper.map_dependencies(include_external=True)
```

**出力**:
- 直接/間接依存
- 循環依存の検出
- 古い/脆弱な依存の特定

### 5. SecurityScanner（セキュリティスキャン）
セキュリティ脆弱性を検出します。

```python
from agentflow.skills.builtin.code_analysis import SecurityScanner

scanner = SecurityScanner()
report = await scanner.scan(scan_types=["sast", "dependency"])
```

**スキャンタイプ**:
- SAST（静的アプリケーションセキュリティテスト）
- 依存関係の脆弱性チェック
- 設定監査

### 6. MigrationPlanner（移行計画策定）
レガシーコードの移行計画を策定します。

```python
from agentflow.skills.builtin.code_analysis import MigrationPlanner

planner = MigrationPlanner()
plan = await planner.create_plan(
    source_stack={"language": "cobol"},
    target_stack={"language": "java", "framework": "spring-boot"},
)
```

**出力**:
- 移行戦略（段階的/一括/Strangler）
- フェーズ別計画
- リスク評価
- 緩和策

## ワークフロー

```
リポジトリ接続 → 静的分析 → 複雑度評価 → 依存関係分析 → セキュリティスキャン → 移行計画
      ↓            ↓           ↓            ↓              ↓              ↓
   コード取得    品質問題   ホットスポット   依存グラフ    脆弱性       移行計画
```

## 統合例

```python
from agentflow.skills.builtin.code_analysis import (
    RepoConnector,
    StaticAnalyzer,
    ComplexityScorer,
    SecurityScanner,
    MigrationPlanner,
)

# 1. リポジトリ接続
connector = RepoConnector()
repo = await connector.run({"url": "https://github.com/org/legacy.git"})

# 2. 分析実行
analyzer = StaticAnalyzer()
analysis = await analyzer.run({"files": repo.get("files", [])})

scorer = ComplexityScorer()
complexity = await scorer.run({"files": repo.get("files", [])})

scanner = SecurityScanner()
security = await scanner.run({"scan_types": ["sast", "dependency"]})

# 3. 移行計画
planner = MigrationPlanner()
plan = await planner.run({
    "source_stack": {"language": "cobol"},
    "target_stack": {"language": "java"},
    "analysis_results": {
        "total_loc": repo.get("total_lines", 0),
        "complexity_score": complexity.get("maintainability_index", 50) / 100,
        "security_issues": security.get("summary", {}).get("total_vulnerabilities", 0),
    },
})
```
