---
name: subagent-review
description: PRのコードレビューをCodexサブエージェントに依頼する。ユーザーがレビュー依頼/コード確認/「review」と言及したときに使う。
allowed-tools: Bash
---

# サブエージェントレビュー

このスキルは、外部のAIエージェント（Codex または Gemini）にコードレビューを委譲する。
**デフォルトは Codex CLI** を使用する。

## 手順

ユーザーがレビューを依頼した場合（例:「PR #123レビューして」「これレビューして」）は次の手順で進める。

1.  **PR番号を特定**:

    - ユーザーが番号を指定していればそれを使う
    - 指定がなければ `gh pr view --json number -q .number` で現在のPR番号を取得する

2.  **レビュワーを選択**:

    - **デフォルト**: Codex CLI
    - ユーザーが「Gemini」を指定した場合: Gemini CLI

3.  **サブエージェントを呼び出す**:

    ### Codex（デフォルト）

    ```bash
    # 結果は stdout に返す（ファイル経由にしない）
    codex exec -s workspace-write -c 'sandbox_permissions=["disk-full-read-access"]' \
      --output-last-message - \
      "/review <PR_NUMBER>"
    ```

    ### Gemini（ユーザー指定時）

    ```bash
    gemini "/review <PR_NUMBER>" --yolo
    ```

4.  **報告**:
    - レビュー依頼を送ったことをユーザーに伝える
    - **結果は標準出力で返る**（必要ならユーザーが任意のファイルにリダイレクトして保存する）
    - PRへの自動投稿は行われない（ユーザーが必要に応じて手動で投稿する）
