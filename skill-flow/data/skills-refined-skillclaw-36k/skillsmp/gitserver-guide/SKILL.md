---
name: gitserver-guide
description: Git SSH server setup and configuration on NixOS including bare repository management, SSH key authentication, and remote access
---

# Git SSH Server (NixOS)

このドキュメントでは、NixOS上でSSH経由でアクセス可能なGitベアリポジトリサーバーの設定と使用方法について説明します。

## 概要

NixOSの`services.gitserver`モジュールを使用して、SSH経由でアクセス可能なGitサーバーを簡単に構築できます。

### 主な機能

- **SSH公開鍵認証**: パスワード不要のセキュアな認証
- **自動リポジトリ初期化**: 宣言的な設定によるベアリポジトリの自動作成
- **制限されたシェル**: git-shellによる安全な環境
- **systemd統合**: サービスとして自動管理

## 設定方法

### 1. SSH鍵ペアの準備

アクセスするクライアントマシンでSSH鍵を生成します（既にある場合はスキップ）:

```bash
# Ed25519鍵を生成（推奨）
ssh-keygen -t ed25519 -C "your_email@example.com"

# または RSA鍵
ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
```

公開鍵を確認:

```bash
cat ~/.ssh/id_ed25519.pub
# または
cat ~/.ssh/id_rsa.pub
```

### 2. NixOS設定の追加

`nixos/configuration.nix`または別のモジュールファイルに以下を追加:

```nix
{
  services.gitserver = {
    # Gitサーバーを有効化
    enable = true;

    # アクセスを許可するSSH公開鍵
    authorizedKeys = [
      "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIExampleKey1 user@laptop"
      "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIExampleKey2 user@desktop"
    ];

    # 初期化するリポジトリ
    repositories = [
      "myproject.git"
      "dotfiles.git"
      "notes.git"
    ];
  };
}
```

### 3. 設定の適用

```bash
sudo nixos-rebuild switch --flake .#desktop
```

## 使用方法

### ローカルからのアクセス

NixOSマシン自体からアクセスする場合:

```bash
# ローカルパスで直接アクセス
git clone /var/lib/git/myproject.git

# またはSSH経由
git clone git@localhost:myproject.git
```

### リモートからのアクセス

他のマシンからSSH経由でアクセス:

```bash
# ホスト名を使用
git clone git@nixos-hostname:myproject.git

# IPアドレスを使用
git clone git@192.168.1.100:myproject.git

# Tailscale経由（Tailscaleを使用している場合）
git clone git@nixos-tailscale-name:myproject.git
```

### 既存プロジェクトをプッシュ

```bash
# ローカルにリポジトリがある場合
cd /path/to/local/project
git init
git add .
git commit -m "Initial commit"

# リモートを追加してプッシュ
git remote add origin git@nixos-hostname:myproject.git
git push -u origin main
```

### 新しいリポジトリの追加

#### 方法1: 設定ファイルで宣言的に追加

`configuration.nix`を編集:

```nix
services.gitserver.repositories = [
  "myproject.git"
  "dotfiles.git"
  "newrepo.git"  # 新規追加
];
```

設定を適用:

```bash
sudo nixos-rebuild switch --flake .#desktop
```

#### 方法2: 手動で作成

```bash
sudo -u git git init --bare /var/lib/git/newrepo.git
```

## トラブルシューティング

### SSHアクセステスト

```bash
# クライアントマシンから実行
ssh git@nixos-hostname

# 成功すると以下のメッセージが表示されます:
# fatal: Interactive git shell is not enabled.
# Connection to nixos-hostname closed.
```

このメッセージは正常です。git-shellは対話的アクセスを制限しています。

### リポジトリ一覧の確認

```bash
# NixOS上で実行
sudo ls -la /var/lib/git/
```

### SSH公開鍵の確認

```bash
# 登録された公開鍵を確認
sudo cat /var/lib/git/.ssh/authorized_keys
```

### 接続エラーの場合

```bash
# SSH詳細ログで診断
ssh -vvv git@nixos-hostname

# ファイアウォールの確認
sudo nix-instantiate --eval -E '(import <nixpkgs/nixos> {}).config.networking.firewall.allowedTCPPorts'
```

### サービスの状態確認

```bash
# Git初期化サービスの状態
systemctl status git-init-repos.service

# ログを確認
journalctl -u git-init-repos.service
```

## 設定オプション

### services.gitserver.enable

- **型**: boolean
- **デフォルト**: `false`
- **説明**: Git SSH サーバーを有効化

### services.gitserver.user

- **型**: string
- **デフォルト**: `"git"`
- **説明**: Gitリポジトリを管理するユーザー名

### services.gitserver.group

- **型**: string
- **デフォルト**: `"git"`
- **説明**: Gitリポジトリのグループ名

### services.gitserver.repoDir

- **型**: path
- **デフォルト**: `"/var/lib/git"`
- **説明**: ベアリポジトリの保存ディレクトリ

### services.gitserver.authorizedKeys

- **型**: listOf string
- **デフォルト**: `[]`
- **説明**: アクセスを許可するSSH公開鍵のリスト

**例**:
```nix
authorizedKeys = [
  "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIExampleKey user@host"
  "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQ... user@host"
];
```

### services.gitserver.repositories

- **型**: listOf string
- **デフォルト**: `[]`
- **説明**: 自動的に初期化するベアリポジトリ名のリスト

**例**:
```nix
repositories = [
  "myproject.git"
  "dotfiles.git"
  "website.git"
];
```

## セキュリティ

このGitサーバーは以下のセキュリティ対策を実装しています:

- ✅ パスワード認証無効（公開鍵認証のみ）
- ✅ rootログイン禁止
- ✅ git-shellによる制限されたシェル環境
- ✅ ユーザー権限の分離（gitユーザー専用）
- ✅ ファイアウォール設定（SSH port 22）

## バックアップと復元

### バックアップ

```bash
# 全リポジトリをアーカイブ
sudo tar czf git-backup-$(date +%Y%m%d).tar.gz /var/lib/git/

# 特定のリポジトリのみ
sudo tar czf myproject-backup.tar.gz /var/lib/git/myproject.git
```

### 復元

```bash
# アーカイブから復元
sudo tar xzf git-backup-20231225.tar.gz -C /

# 権限を修正
sudo chown -R git:git /var/lib/git/
```

### 自動バックアップ（推奨）

NixOSの`services.restic`や`services.borgbackup`と組み合わせて自動バックアップを設定できます。

## 高度な使用例

### Git Hooks

サーバーサイドフックを使用して、プッシュ時の自動処理を実装できます:

```bash
# post-receiveフックの例
sudo -u git tee /var/lib/git/myproject.git/hooks/post-receive << 'EOF'
#!/bin/sh
echo "Push received at $(date)"
# デプロイやビルドのコマンドをここに追加
EOF

sudo -u git chmod +x /var/lib/git/myproject.git/hooks/post-receive
```

### アクセス制御

複数のユーザーで異なるアクセス権限を管理したい場合は、[Gitolite](https://gitolite.com/)や[Gitea](https://gitea.io/)の使用を検討してください。

## 関連ドキュメント

- [NixOS SSH Configuration](https://nixos.wiki/wiki/SSH)
- [Git on the Server](https://git-scm.com/book/en/v2/Git-on-the-Server-Setting-Up-the-Server)
- [Tailscale Configuration](60_services.md) (プライベートネットワークでの使用)
