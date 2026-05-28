---
name: "toeic-app-expert"
description: "TOEIC単語アプリ開発のエキスパート。技術ドキュメントに基づき、アーキテクチャ、キャッシュ戦略、データフロー、開発ルールについて回答・支援します。実装やデバッグの際に呼び出してください。"
---

# TOEIC App Expert

このスキルは `toeic_website_ver2.0` プロジェクトの開発を支援するための専門知識を提供します。

## プロジェクト概要

TOEIC頻出重要単語を学習するWebアプリケーションです。
- **フレームワーク**: Next.js 16.1.0 (App Router)
- **UI**: React 19, TypeScript
- **AI生成**: Google Gemini (詳細解説生成)
- **キャッシュ**: Upstash Redis (L2), Next.js Data Cache (L1)
- **音声**: Google Cloud Text-to-Speech
- **データソース**: Vercel Blob (`word.txt`)

## アーキテクチャとデータフロー

### 単語詳細取得 (`getWordDetail`)
1. **L1 Cache**: Next.js Data Cache (`cacheLife("weeks")`)。ヒットすれば即返却。
2. **L2 Cache**: Upstash Redis (`WORD_CACHE_TTL_DAYS`日)。ヒットすれば即返却。
3. **L3 Generation**: Google Geminiで生成 -> 正規化 -> Redis保存 -> 返却。
   - 生成失敗時もRedis読み書きエラー時も、可能な限り動作を継続する。

### 音声生成 (`POST /api/tts`)
- クライアントからテキストを受け取り、Google TTS APIを叩いてBase64(MP3)を返す。
- エラーハンドリング: APIキー未設定時は500エラー。

## ディレクトリ構造

- `src/app`: Next.js App Router ページ
  - `/words/[word]`: 単語詳細 (Server Component)
  - `/study`: 学習モード
  - `/favorites`: お気に入り
  - `/review`: 復習モード
- `src/components`: UIコンポーネント
  - `features/`: 機能ごとのコンポーネント (words, study, review, favorites)
- `src/lib`: ユーティリティ
  - `actions.ts`: Server Actions (`getWordDetail`など)
  - `wordCache.ts`: Redisキャッシュロジック
  - `upstash.ts`: Redis接続

## 開発ルール

- **テスト**: 自動テストは利用しない。`npm run test`は実行しない。手動テストを行う。
- **Lint**: `npm run lint` を遵守。
- **環境変数**: `.env.local` で管理 (`GEMINI_API_KEY`, `TTS_API_KEY`, `UPSTASH_REDIS_REST_URL` 等)。
- **デプロイ**: Vercel (GitHub Actions経由)。Previewは自動、Productionは手動。

## よくあるタスク

- **単語データの更新**: Vercel Blobの `word.txt` を更新する。
- **コンポーネント追加**: `src/components/features` 配下に機能単位で配置する。
- **キャッシュ確認**: Redisのキーは `word:<lowercased>`。

このスキルは `.trae/documents/技術ドキュメント.md` の内容に基づいています。
