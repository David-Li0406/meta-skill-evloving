# Codex Skill Documentation

This skill provides versatile Codex MCP integration for code review, technical research, documentation generation, and custom queries.

## Overview

The Codex skill acts as an intelligent intermediary between Claude Code and the Codex MCP server, automatically:
- Detecting use cases from natural language requests
- Gathering relevant project context
- Constructing optimized prompts
- Executing Codex queries
- Formatting and presenting results

## Use Cases

### 1. Code Review

Automatically reviews code changes with comprehensive security, design, and quality analysis.

**Triggers**:
- "codexでレビューして"
- "review with codex"
- "check code with codex"

**What it does**:
1. Gets git diff of current changes
2. Reads changed files
3. Detects project tech stack (package.json, etc.)
4. Reads design principles (CLAUDE.md)
5. Constructs detailed review prompt with:
   - Security analysis (SQL injection, XSS, CSRF, etc.)
   - Design principles (SOLID, DRY, KISS, YAGNI)
   - Code quality (naming, readability, maintainability)
   - Performance optimization
6. Executes Codex review
7. Presents results with priority levels (🔴🟡🟢)

**Example**:
```
User: "codexでレビューして"

Output:
# コードレビュー結果

## 🔴 セキュリティ（最優先）
### 1. SQLインジェクションリスク
**ファイル**: src/api/users.ts:45
**問題**: ユーザー入力を直接クエリに使用
**推奨**: パラメータバインディングを使用
...
```

### 2. Technical Research

Conducts deep technical research with project context.

**Triggers**:
- "〜を調査して"
- "research 〜"
- "investigate 〜"
- "ベストプラクティス"

**What it does**:
1. Identifies research topic from request
2. Checks project's current tech stack and versions
3. Finds existing similar implementations
4. Reads project constraints (CLAUDE.md)
5. Constructs research prompt with:
   - Best practices and recommended patterns
   - Security considerations
   - Implementation examples
   - Compatibility with current project
6. Executes Codex research
7. Presents structured results with code examples

**Example**:
```
User: "TypeScriptの依存性注入のベストプラクティスを調査"

Output:
# 技術調査結果: TypeScript依存性注入

## プロジェクトコンテキスト
- 現在の技術スタック: TypeScript 5.3, Node.js 20
- 既存パターン: コンストラクタインジェクション使用中

## ベストプラクティス
### 1. コンストラクタインジェクション
```typescript
class UserService {
  constructor(
    private userRepo: UserRepository,
    private logger: Logger
  ) {}
}
```
...
```

### 3. Documentation Generation

Generates comprehensive documentation from code.

**Triggers**:
- "ドキュメント生成"
- "generate docs"
- "API仕様"

**What it does**:
1. Reads target code files
2. Extracts function/class signatures
3. Identifies public APIs
4. Checks existing documentation style
5. Constructs documentation prompt
6. Generates Markdown documentation with:
   - Overview
   - API specifications (parameters, return values, exceptions)
   - Usage examples
   - Architecture diagrams (Mermaid)
7. Offers to save to docs/

**Example**:
```
User: "src/api/auth.tsのドキュメント生成"

Output:
# Authentication API Documentation

## Overview
This module provides authentication and authorization functionality...

## API Reference

### `login(credentials: LoginCredentials): Promise<AuthToken>`
Authenticates a user and returns an auth token.

**Parameters**:
- `credentials` (LoginCredentials): User credentials
  - `username` (string): Username
  - `password` (string): Password

**Returns**: `Promise<AuthToken>`
...
```

### 4. Custom Queries

Handles any custom technical question.

**Triggers**:
- "/codex 〜"
- "Codexで〜"
- "using Codex 〜"

**What it does**:
1. Takes user's custom prompt as-is
2. Optionally gathers context if file paths mentioned
3. Sends to Codex
4. Returns response

**Example**:
```
User: "Codexでこのエラーの原因を教えて: Cannot read property 'map' of undefined"

Output:
このエラーは、undefinedまたはnullの値に対してmapメソッドを呼び出そうとした際に発生します。

## 原因
...

## 解決方法
...
```

## Prompt Templates

### Code Review Template

```markdown
以下のコードの包括的なレビューを実施してください。

## 🎯 レビューの目的
このコード変更の技術的品質、セキュリティ、保守性を評価し、改善すべき点を特定する。

## 📋 コードコンテキスト
- **変更規模**: {changed_files}ファイル、+{added_lines}行、-{deleted_lines}行
- **主要変更ファイル**: {file_list}
- **プロジェクト技術スタック**: {tech_stack}
- **プロジェクト設計原則**: {claude_md_principles}

## 📂 変更内容
{git_diff_or_file_contents}

## 🔍 レビュー項目（優先度順）
### 🔴 最優先（セキュリティ・重大バグ）
1. セキュリティ脆弱性の有無
2. 重大なバグやロジックエラー

### 🟡 重要（設計・品質）
3. 設計原則の遵守（SOLID、DRY、KISS、YAGNI）
4. コード品質（命名、可読性、テスト）

### 🟢 参考（パフォーマンス・最適化）
5. パフォーマンス最適化の余地
6. その他改善提案

## 🎨 期待するレビュー形式
- [ ] 各観点のレビュー結果
- [ ] 重大な問題の具体的な指摘（ファイル名、行番号、問題点）
- [ ] 具体的な改善提案とコード例
- [ ] 総合評価（Approve / Request Changes / Comment）

レビュー結果を上記形式でまとめてください。
```

### Technical Research Template

```markdown
{topic}について技術調査を実施してください。

## 🎯 調査の目的
{auto_generated_purpose}

## 📋 プロジェクトコンテキスト
- **技術スタック**: {tech_stack}
- **既存実装**: {existing_patterns}
- **バージョン制約**: {version_constraints}
- **プロジェクト設計原則**: {claude_md_principles}

## 🔍 調査項目（優先度順）
### 🔴 最優先
1. {primary_research_question}
2. ベストプラクティスと推奨パターン
3. セキュリティ考慮事項

### 🟡 重要
4. 実装例とコードサンプル
5. 既存実装との整合性
6. パフォーマンス考慮事項

### 🟢 参考
7. 代替アプローチ
8. 制約事項と注意点
9. 関連ドキュメント

## 🎨 期待する回答形式
- [ ] 各調査項目の回答
- [ ] 具体的なコード例
- [ ] 実装手順
- [ ] 推奨事項と非推奨事項

調査結果をまとめてください。
```

### Documentation Generation Template

```markdown
以下のコードのドキュメントを生成してください。

## 🎯 ドキュメントの目的
{auto_generated_purpose}

## 📋 対象コード
{code_content}

## 📂 プロジェクトコンテキスト
- **技術スタック**: {tech_stack}
- **既存ドキュメントスタイル**: {existing_doc_style}

## 🔍 生成するドキュメント
### 必須項目
- [ ] 概要説明
- [ ] 主要な機能の説明
- [ ] API仕様（パラメータ、戻り値、例外）
- [ ] 使用例

### 推奨項目
- [ ] アーキテクチャ図（Mermaid形式）
- [ ] 設計判断の理由
- [ ] 制約事項と注意点

## 🎨 ドキュメント形式
- フォーマット: Markdown
- コード例: {language}
- 説明言語: {output_language}

ドキュメントを生成してください。
```

## Context Gathering Details

### Tech Stack Detection

Automatically detects from:
- `package.json` → Node.js/TypeScript (checks dependencies, devDependencies)
- `requirements.txt`, `pyproject.toml` → Python (checks installed packages)
- `Gemfile` → Ruby (checks gems)
- `go.mod` → Go (checks modules)
- `Cargo.toml` → Rust (checks dependencies)

### Project Principles Loading

Reads if exists:
- `CLAUDE.md` or `.claude/CLAUDE.md` → Project-specific guidelines
- `docs/ai/key-guideline.md` → Development guidelines
- `README.md` → Basic project information

### Existing Pattern Discovery

Uses Glob/Grep to find:
- Similar class/function implementations
- Test file patterns
- Naming conventions
- Architecture patterns

### Smart File Reading

- Skips binary files (images, compiled binaries, etc.)
- Respects `.gitignore` patterns
- Limits: max 10 files, max 1000 lines per file
- Warns if context exceeds limits

## Error Handling

### MCP Unavailable (Critical)

If `mcp__codex__codex` tool is not available:

```
❌ エラー: Codex MCPサーバーに接続できません

このスキルの実行には、Codex MCPサーバーの設定が必要です。

## セットアップ手順
1. Codex MCPサーバーをインストール
2. Claude Code の設定ファイルにMCPサーバーを追加
3. Claude Code を再起動

## 代替手段
- 手動でのコードレビューを実施
- 他の技術調査ツールを使用
```

Skill execution STOPS. No fallback provided.

### Invalid Parameters

If parameters are unclear:
- Ask user for clarification
- Suggest most likely interpretation
- Provide usage examples

### Codex API Errors

If Codex returns an error:
- Display error message
- Suggest troubleshooting steps
- Offer to retry with modified prompt

### Context Too Large

If gathered context exceeds limits:
- Warn user about size
- Ask to reduce scope or proceed anyway

## Best Practices

### For Code Reviews

1. **Stage or commit changes first** for clearer diffs
2. **Review one logical change at a time**
3. **Specify focus areas** when needed (e.g., "focus on security")
4. **Provide context** about design decisions

### For Technical Research

1. **Mention current versions** of relevant tech
2. **Specify constraints** (project requirements, limitations)
3. **Ask for code examples** in your project's language
4. **Reference existing code** for better context

### For Documentation

1. **Finalize code first** before generating docs
2. **Specify target audience** (API users, contributors, etc.)
3. **Review generated docs** for accuracy
4. **Keep docs in sync** with code changes

### For Custom Queries

1. **Be specific** about what you want to know
2. **Provide relevant code snippets** if applicable
3. **Mention constraints** or preferences
4. **Follow up** with clarifying questions

## Troubleshooting

### Skill Not Triggering

**Problem**: Skill doesn't activate on request.

**Solutions**:
- Use explicit keywords: "codexでレビュー", "codex review"
- Try `/codex` for explicit invocation
- Check skill is installed: `/skills list`
- Verify trigger keywords in SKILL.md

### Poor Response Quality

**Problem**: Codex responses are generic or unhelpful.

**Solutions**:
- Provide more specific requests
- Mention relevant files or code sections explicitly
- Add constraints (language, depth, format)
- Include project context manually if needed

### MCP Connection Errors

**Problem**: Cannot connect to Codex MCP server.

**Solutions**:
```bash
# Check MCP configuration
cat ~/.claude/settings.json | jq '.mcpServers.codex'

# Verify Codex is installed
which codex

# Test Codex manually
codex "Hello"

# Check MCP server logs
cat ~/.claude/logs/mcp-codex.log
```

### Context Too Large Warnings

**Problem**: Skill warns about large context size.

**Solutions**:
- Reduce scope (fewer files, smaller directories)
- Specify exact files instead of directories
- Use `scope: file` parameter
- Split into multiple smaller requests

## Advanced Usage

### Specifying Use Case Explicitly

```
# Instead of auto-detection
/codex review src/api/auth.ts

# Explicit use case
/codex research "GraphQL best practices"

# Custom prompt
/codex custom "Explain this error: ..."
```

### Controlling Scope

```
# File scope (default for specific files)
"codexでこのファイルをレビュー: src/api/auth.ts"

# Directory scope
"codexでsrc/api/ディレクトリをレビュー"

# Diff scope (default for general review)
"codexでレビューして"  # Uses git diff

# Project scope
"codexでプロジェクト全体のセキュリティを調査"
```

### Combining with Other Skills

```
# Use with git-operations-specialist
1. "git statusを確認"  # Uses git-operations-specialist
2. "codexでレビュー"    # Uses codex skill with git diff

# Use with file operations
1. Read specific files
2. "これらのファイルをcodexでレビュー"
```

## Integration

This skill integrates with:
- **Claude Code core tools**: Bash, Read, Glob, Grep, Write
- **git-operations-specialist skill**: For git operations
- **Codex MCP server**: For AI-powered analysis

## Limitations

1. **MCP Required**: Codex MCP server must be configured (no fallback)
2. **Context Size**: Limited to 10 files, 1000 lines each
3. **Language**: Prompts optimized for Japanese/English
4. **File Types**: Skips binary files

## Performance Tips

1. **Commit changes first** for faster diff reading
2. **Be specific** to reduce context gathering time
3. **Use file scope** for targeted analysis
4. **Cache frequent requests** mentally to refine prompts

## Related Documentation

- [Codex Plugin README](../../README.md)
- [SKILL.md](./SKILL.md) - Full skill definition
- [review-support-codex command](../../../../../.claude/commands/review-support-codex.md) - PR review integration
