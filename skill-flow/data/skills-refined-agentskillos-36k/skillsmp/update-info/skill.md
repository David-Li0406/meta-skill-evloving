---
name: update-info
description: ポートフォリオサイトの情報を最新に更新する
args: "[--ci] CIモード：承認プロセスをスキップして自動実行"
---

# HP情報更新スキル

このスキルは、ポートフォリオサイト（hirokidaichi.github.io）の各セクションの情報を最新に更新します。

## 実行モード

- **通常モード** (デフォルト): 更新内容をユーザーに確認し、承認を得てからコミット
- **CIモード** (`--ci`): GitHub Actions用。承認プロセスをスキップし、変更があれば自動でブランチ作成・コミット

CIモードで実行する場合:
```bash
/update-info --ci
```

## 実行フロー

### 1. 最終更新日時の確認

`data/UPDATED_AT.md` ファイルを読み込んで、最終更新日時を取得します。
- ファイルが存在しない場合は、新規作成します（初回実行時）
- フォーマット: `YYYY-MM-DD HH:MM:SS`

### 2. 各セクションの並列更新

以下のmarkdownファイルを**並列**で更新します（Taskツールを使用）:

#### a. NewsPicks記事 (`data/_newspicks.md`)
- agent-browserで https://newspicks.com/topics/dx/ にアクセス
- UPDATED_AT以降の新しい記事を抽出
- 既存の_newspicks.mdに新しい記事を追加（重複チェック）
- エラーが発生しても他のタスクは続行

#### b. Podcast情報 (`data/_podcast.md`)
- 関連するポッドキャストサイトをチェック
- 新しいエピソード情報を取得
- _podcast.mdを更新

#### c. Slides情報 (`data/_slides.md`)
- SlideShareやSpeakerDeckなどから最新のスライドを取得
- _slides.mdを更新

#### d. Event情報 (`data/_event.md`)
- イベント登壇情報を確認
- _event.mdを更新

#### e. Interview記事 (`data/_interview.md`)
- 新しいインタビュー記事を検索
- _interview.mdを更新

#### f. Note記事（既存APIを活用）
- `getNoteArticles()`関数は既にpages/index.tsxに存在
- Note APIから最新記事を取得して確認

#### g. Qiita記事（既存APIを活用）
- `getQiitaArticles()`関数は既にpages/index.tsxに存在
- Qiita APIから最新記事を取得して確認

### 3. 更新内容の確認と承認

**通常モードの場合:**
- 各ファイルの更新差分を表示
- ユーザーに承認を求める
- 承認された場合のみ、次のステップに進む

**CIモード (`--ci`) の場合:**
- 承認プロセスをスキップ
- 変更があれば自動で次のステップに進む
- 変更がなければ「更新なし」として終了

### 4. ファイルの更新とコミット

**通常モードの場合:**
承認後:
1. 各markdownファイルを更新
2. `data/UPDATED_AT.md`を現在時刻で更新
3. 変更をgit add
4. コミットメッセージを自動生成
5. ユーザーに確認後、コミット

**CIモード (`--ci`) の場合:**
1. 新しいブランチを作成: `auto-update/YYYY-MM-DD`
2. 各markdownファイルを更新
3. `data/UPDATED_AT.md`を現在時刻で更新
4. 変更をgit add
5. コミットメッセージを自動生成してコミット
6. ブランチをpush
7. `gh pr create` でPRを作成（タイトル: "Auto-update: サイト情報の自動更新 YYYY-MM-DD"）
8. PRのURLを出力して終了

## 重要な注意事項

- **エラーハンドリング**: 個別のタスクがエラーになっても他のタスクは継続
- **並列実行**: 各markdownファイルごとに並列でTaskツールを実行
- **agent-browser使用**: Webサイトからのスクレイピングにはagent-browserを必須で使用
- **承認プロセス**: 必ず更新内容をユーザーに見せて承認を得る

## 使用するツール

- Read: ファイル読み込み
- Write/Edit: ファイル更新
- Task: 並列実行（subagent_type: "general-purpose"）
- agent-browser: Webサイトからの情報取得（Bashツール経由）
- Bash: git操作、agent-browser実行
- AskUserQuestion: 承認プロセス

## 実装例

```typescript
// 並列実行のイメージ
const tasks = [
  { file: '_newspicks.md', url: 'https://newspicks.com/topics/dx/' },
  { file: '_podcast.md', source: 'podcast-sites' },
  { file: '_slides.md', source: 'slide-sharing-sites' },
  // ...
];

// 各タスクを並列で実行（一つのメッセージで複数のTask tool callを送信）
```

## 初回セットアップ

初回実行時は `data/UPDATED_AT.md` を作成:
```
2026-01-14 16:30:00
```
