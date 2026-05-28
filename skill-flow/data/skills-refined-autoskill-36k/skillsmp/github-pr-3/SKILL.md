---
description: GitHub PR操作のユーティリティ。レビューコメントの取得・返信、未解決スレッドの管理など。octokit/simple-gitを使用した効率的なPR操作を提供する。
---

GitHub Pull Request の操作を効率化するユーティリティ集。

いずれも `${CLAUDE_PLUGIN_ROOT}/skills/github-pr/scripts/<scriptName>` に配置されている。

| スクリプト | 説明 |
|-----------|------|
| `get-unresolved-threads.ts` | 未解決スレッドID一覧を取得 |
| `get-comments-by-thread.ts` | スレッドIDからコメント詳細を取得 |
| `reply-to-thread.ts` | スレッドに返信 |
| `get-ci-status.ts` | PRのCI状態を取得 |

使用する際は `<script> --help` を実行し、使い方を把握してから使用すること。
