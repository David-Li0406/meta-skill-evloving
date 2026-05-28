# 出力例

このファイルはドキュメント作成スキルの出力例です。

---

## 概念説明の例

```markdown
# SSH Agent

## TL;DR

- SSH agent は秘密鍵をメモリに保持し、パスフレーズの再入力を省略する
- `ssh-add` で鍵を登録、`SSH_AUTH_SOCK` 経由で SSH クライアントと通信
- 一度登録すれば、セッション中は何度でも認証に利用できる

## SSH Agent とは

SSH 認証に使用する秘密鍵をメモリ上で管理するデーモンプロセス。

## なぜ必要か

秘密鍵にパスフレーズを設定している場合、SSH 接続のたびに入力が必要になる。
SSH agent を使うと、一度だけパスフレーズを入力すれば以降は自動的に認証される。

## 仕組み

SSH agent は Unix ドメインソケットを通じて SSH クライアントと通信する。

\`\`\`mermaid
sequenceDiagram
    participant User
    participant SSH as ssh コマンド
    participant Agent as ssh-agent
    participant Server as リモートサーバー

    User->>Agent: ssh-add（鍵を登録）
    User->>SSH: ssh host
    SSH->>Agent: 署名を依頼
    Agent-->>SSH: 署名を返却
    SSH->>Server: 署名で認証
    Server-->>SSH: 認証成功
\`\`\`

## ユースケース

- **開発作業**: Git 操作で頻繁に SSH 認証が必要な場合
- **サーバー管理**: 複数のサーバーに SSH 接続する場合
- **devcontainer**: ホストの鍵をコンテナ内で使用する場合

## 参考資料

**参考**: [ssh-agent - OpenBSD manual pages](https://man.openbsd.org/ssh-agent)

> ssh-agent is a program to hold private keys used for public key authentication.

<!-- AI Agent Context
作成日: 2024-01-15
目的: SSH agent の基本概念を理解するためのドキュメント
-->
```

---

## 手順書の例

```markdown
# macOS で SSH 鍵を設定する方法

## 前提条件

- macOS 10.12.2 以降
- Terminal.app または iTerm2

## 手順

### 1. SSH 鍵を生成する

Ed25519 アルゴリズムで新しい鍵を生成する:

\`\`\`bash
ssh-keygen -t ed25519 -C "your_email@example.com"
\`\`\`

パスフレーズの入力を求められる。セキュリティのため設定を推奨。

### 2. SSH agent に鍵を登録する

Keychain に保存しながら登録:

\`\`\`bash
ssh-add --apple-use-keychain ~/.ssh/id_ed25519
\`\`\`

### 3. 公開鍵をサーバーに登録する

公開鍵をクリップボードにコピー:

\`\`\`bash
pbcopy < ~/.ssh/id_ed25519.pub
\`\`\`

GitHub の場合: Settings → SSH and GPG keys → New SSH key

## 確認方法

接続テストを実行:

\`\`\`bash
ssh -T git@github.com
\`\`\`

"Hi username!" と表示されれば成功。

## トラブルシューティング

### Permission denied (publickey)

**症状**: `Permission denied (publickey).` エラー

**原因**: 公開鍵がサーバーに登録されていない、または agent に鍵が登録されていない

**解決策**:

1. `ssh-add -l` で登録済みの鍵を確認
2. 公開鍵がサーバーに正しく登録されているか確認

## 参考資料

**参考**: [Generating a new SSH key - GitHub Docs](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent)

<!-- AI Agent Context
作成日: 2024-01-15
目的: macOS での SSH 鍵設定手順をまとめる
-->
```

---

## リファレンスの例

```markdown
# ssh-add コマンドリファレンス

## 概要

ssh-add は SSH agent に秘密鍵を追加・削除・一覧表示するコマンド。

## 基本コマンド

| コマンド | 説明 | 例 |
|----------|------|-----|
| `ssh-add [file]` | 鍵を追加 | `ssh-add ~/.ssh/id_ed25519` |
| `ssh-add -l` | 登録済み鍵の一覧 | - |
| `ssh-add -L` | 公開鍵を表示 | - |
| `ssh-add -d [file]` | 特定の鍵を削除 | `ssh-add -d ~/.ssh/id_rsa` |
| `ssh-add -D` | 全ての鍵を削除 | - |

## macOS 固有オプション

| オプション | 説明 |
|------------|------|
| `--apple-use-keychain` | パスフレーズを Keychain に保存して追加 |
| `--apple-load-keychain` | Keychain から鍵を読み込み |

## 参考資料

**参考**: [ssh-add(1) - OpenBSD manual pages](https://man.openbsd.org/ssh-add)

<!-- AI Agent Context
作成日: 2024-01-15
目的: ssh-add コマンドのクイックリファレンス
-->
```
