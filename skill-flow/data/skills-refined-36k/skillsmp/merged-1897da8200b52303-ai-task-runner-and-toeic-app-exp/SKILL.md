---
name: ai-task-runner-and-toeic-app-expert
description: Use this skill when you need to delegate tasks to external AI agents for implementation or research while also receiving expert support for TOEIC app development.
---

# AI Task Runner and TOEIC App Expert

このスキルは、外部のAIエージェントを実行するための機能と、TOEIC単語アプリ開発に関する専門知識を提供します。実装や調査の作業を別のAIエージェントに委譲し、TOEICアプリの開発を支援します。

## TOEIC App Overview

TOEIC頻出重要単語を学習するWebアプリケーションです。
- **フレームワーク**: Next.js
- **UI**: React, TypeScript
- **AI生成**: Google Gemini
- **キャッシュ**: Upstash Redis, Next.js Data Cache
- **音声**: Google Cloud Text-to-Speech
- **データソース**: Vercel Blob

## Architecture and Data Flow

### Word Detail Retrieval (`getWordDetail`)
1. **L1 Cache**: Next.js Data Cache。ヒットすれば即返却。
2. **L2 Cache**: Upstash Redis。ヒットすれば即返却。
3. **L3 Generation**: Google Geminiで生成し、Redisに保存。

### Voice Generation (`POST /api/tts`)
- クライアントからテキストを受け取り、Google TTS APIを使用して音声を生成。

## Development Rules

- **Testing**: 手動テストを行う。
- **Linting**: `npm run lint` を遵守。
- **Environment Variables**: `.env.local` で管理。

## Common Tasks

- **Update Word Data**: Vercel Blobのデータを更新。
- **Add Components**: `src/components/features` に機能単位で配置。

## AI Agent Task Runner

このスキルは外部のAIエージェントをコマンドラインで依頼し実行させるための機能を提供します。

### Supported AI Agents
- Gemini CLI
- Copilot CLI

### Basic Execution Method
エージェントへの作業は時間がかかることがあるため、以下のように実行します。

```bash
gemini --approval-mode=auto_edit -p "<Your task here>"
```

```bash
copilot --allow-all-tools --deny-tool 'shell(rm)' --deny-tool 'shell(git push)' -p "<Your task here>"
```

### Instructions for Task Delegation
- **具体的なタスクを指示する**: 一度出した指示の変更はできません。
- **文脈を含める**: タスクの実行に関する情報を与える必要があります。
- **適切な出力形式を指定する**: 調査結果が長くなる場合は中間ファイルに出力するなどの工夫をしましょう。

このスキルは、TOEICアプリの開発と外部AIエージェントのタスク実行を効率的に行うためのものです。