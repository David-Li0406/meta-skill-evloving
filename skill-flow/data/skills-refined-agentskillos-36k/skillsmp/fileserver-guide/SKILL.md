---
name: fileserver-guide
description: NixOS file server setup and configuration using Tailscale VPN, Samba/CIFS, NFS, and SFTP with security design and client access methods
---

# NixOS ファイルサーバ設計書

## 概要

NixOSをファイルサーバとしても活用するための設計案です。既存のNixOS環境を活かしながら、Tailscale VPNによるセキュアなリモートアクセスと高性能なファイルサーバ機能を追加します。

## 現在の環境

### 基盤となる設定
- NixOS 25.05ベース
- SSH接続有効（セキュリティ強化済み）
- Docker対応済み
- 外部ストレージ2つマウント済み
  - `/mnt/sda1`: ext4 (UUID: 71323b1e-e85e-4658-b2f1-ce64474bb85b)
  - `/mnt/sdb1`: ext4 (UUID: d002ced3-af30-411f-8d52-eb71b53ea6cf)
- ファイアウォール有効
- Tailscale VPN対応済み

## アーキテクチャ設計

### VPNネットワーク層

#### Tailscale統合
- **主要機能**: セキュアなリモートアクセス、ネットワーク分離
- **認証**: OAuth (Google/GitHub等) + MFA対応
- **特徴**:
  - WireGuardベースの高性能暗号化
  - NAT越え自動設定
  - Magic DNS機能
  - 細かいアクセス制御（ACL）

#### セキュリティ層
```
インターネット → Tailscale VPN → ファイルサーバ
              (認証済みのみ)
```

### プロトコル構成

#### SMB/CIFS (Samba) - メインファイル共有
- **用途**: Windows/macOS互換性、日常的なファイル共有
- **共有フォルダ**:
  - `public`: 一般的なファイル共有
  - `media`: 動画・音楽ファイル（読み取り専用）
  - `backup`: バックアップデータ（Time Machine対応）

#### NFS - 高速Linux間通信
- **用途**: Linux間の高速ファイル転送、Docker volume共有
- **共有フォルダ**:
  - `docker`: Docker volume用
  - `dev`: 開発用ファイル

#### SFTP/SCP - セキュア転送
- **用途**: リモートアクセス、セキュアなファイル転送
- **認証**: SSH鍵認証
- **VPN**: Tailscale経由でのみアクセス可能

### ストレージ構成

```
/mnt/sda1 (プライマリストレージ)
├── /shares/public      # パブリック共有
├── /shares/media       # メディアファイル
├── /shares/backup      # バックアップ
└── /shares/docker      # Docker volumes

/mnt/sdb1 (セカンダリストレージ/冗長化)
├── /backup/sda1-mirror # sda1のミラー
└── /shares/archive     # アーカイブ
```

## セキュリティ設計

### アクセス制御

#### VPNレベル
- **Tailscale ACL**: デバイス・ユーザー単位でのアクセス制御（Admin Consoleで管理）
- **Magic DNS**: デバイス名での簡単アクセス
- **Exit Node**: ファイルサーバ経由でのインターネットアクセス

ACL運用の詳細は `docs/72_tailscale_acl.md` を参照。

#### システムレベル
- **ユーザー管理**: 既存のmiyoshi_sユーザー + ファイルサーバ専用ユーザー
- **グループ権限**:
  - `fileserver`: ファイルサーバ管理
  - `media`: メディアファイルアクセス
  - `backup`: バックアップデータアクセス
- **ネットワーク制限**: Tailscale VPN経由のみアクセス許可

### 認証方式
- **VPN認証**: Tailscale OAuth (Google/GitHub等) + MFA
- **SMB**: ユーザー名/パスワード認証（VPN内）
- **NFS**: ホストベース認証（VPN内）
- **SFTP**: SSH鍵認証（VPN内）

### ファイアウォール設定
```nix
networking.firewall = {
  enable = true;
  # Tailscaleインターフェースを信頼済みとして設定
  trustedInterfaces = [ "tailscale0" ];

  # VPN経由のみ許可、外部アクセス無効
  allowedTCPPorts = [
    # SSH, SMB, NFSはTailscale経由のみアクセス可能
  ];
  allowedUDPPorts = [
    41641  # Tailscale
  ];
};

# Tailscale設定
services.tailscale = {
  enable = true;
  useRoutingFeatures = "server";  # Exit Node機能
};
```

## 実装計画

### ディレクトリ構成
```
nixos/
├── services/
│   ├── fileserver/
│   │   ├── default.nix          # メインモジュール
│   │   ├── samba.nix           # Samba設定
│   │   ├── nfs.nix             # NFS設定
│   │   ├── monitoring.nix      # 監視設定
│   │   └── backup.nix          # バックアップ設定
│   ├── tailscale/
│   │   ├── default.nix         # Tailscale基本設定
│   │   └── (ACLはAdmin Consoleで管理)
│   └── default.nix             # 既存（fileserver, tailscale追加）
└── storage/
    ├── default.nix             # ストレージ管理
    └── directories.nix         # ディレクトリ作成
```

### 実装ステップ
1. **Tailscale VPN設定**
   - Tailscaleサービス有効化
   - ファイアウォール設定更新
   - Exit Node機能設定

2. **基本ファイルサーバモジュール作成**
   - サービス設定の基盤構築
   - ディレクトリ自動作成機能

3. **Samba設定**
   - 基本共有フォルダ設定
   - ユーザー認証設定

4. **NFS設定**
   - 開発用共有設定
   - Docker volume共有

5. **セキュリティ強化**
   - VPNアクセス制御設定
   - ユーザー権限管理

6. **監視・バックアップ**
   - 基本監視の実装
   - 自動バックアップ設定

## 設定例

### Tailscale設定
```nix
# nixos/services/tailscale/default.nix
{ config, pkgs, ... }:

{
  # Tailscaleサービス有効化
  services.tailscale = {
    enable = true;
    useRoutingFeatures = "server";  # Exit Node機能
  };

  # ファイアウォール設定
  networking.firewall = {
    enable = true;
    trustedInterfaces = [ "tailscale0" ];
    allowedUDPPorts = [ 41641 ];  # Tailscale
  };

  # systemd-resolvedとの統合
  services.resolved.enable = true;

  # 自動接続サービス
  systemd.services.tailscale-autoconnect = {
    description = "Automatic connection to Tailscale";
    after = [ "network-pre.target" "tailscale.service" ];
    wants = [ "network-pre.target" "tailscale.service" ];
    wantedBy = [ "multi-user.target" ];

    serviceConfig.Type = "oneshot";

    script = with pkgs; ''
      sleep 2
      status="$(${tailscale}/bin/tailscale status -json | ${jq}/bin/jq -r .BackendState)"
      if [ $status = "Running" ]; then
        exit 0
      fi
      ${tailscale}/bin/tailscale up --accept-routes --advertise-exit-node
    '';
  };
}
```

### Samba設定
```nix
services.samba = {
  enable = true;
  securityType = "user";
  shares = {
    public = {
      path = "/mnt/sda1/shares/public";
      browseable = "yes";
      "read only" = "no";
    };
    media = {
      path = "/mnt/sda1/shares/media";
      browseable = "yes";
      "read only" = "yes";
    };
    backup = {
      path = "/mnt/sda1/shares/backup";
      browseable = "yes";
      "read only" = "no";
    };
  };
};
```

### NFS設定
```nix
services.nfs.server = {
  enable = true;
  exports = '''
    /mnt/sda1/shares/docker 192.168.1.0/24(rw,sync,no_subtree_check)
    /mnt/sda1/shares/dev 192.168.1.0/24(rw,sync,no_subtree_check)
  ''';
};
```

## セットアップ手順

### 初期セットアップ
```bash
# 1. 設定適用
sudo nixos-rebuild switch

# 2. Tailscale認証（初回のみ）
sudo tailscale up --accept-routes --advertise-exit-node
# → ブラウザでOAuth認証を実行

# 3. Tailscale ACL設定（Admin Console）
#  - SSHアクセスが必要ならSSHルールを追加
#  - このリポジトリではACLは管理しない

# 4. ディレクトリ作成（自動化予定）
sudo mkdir -p /mnt/sda1/shares/{public,media,backup,docker}
sudo mkdir -p /mnt/sdb1/{backup,shares/archive}

# 5. 権限設定
sudo chown -R miyoshi_s:users /mnt/sda1/shares
sudo chmod -R 755 /mnt/sda1/shares

# 6. Sambaユーザー追加
sudo smbpasswd -a miyoshi_s

# 7. Tailscale設定確認
tailscale status
tailscale netcheck
```

### 運用管理
```bash
# Tailscale状態確認
tailscale status
tailscale netcheck
systemctl status tailscaled

# サービス状態確認
systemctl status smbd nmbd
systemctl status nfs-server

# 接続確認
smbclient -L nixos.tail-scale.ts.net -U miyoshi_s
showmount -e nixos.tail-scale.ts.net

# ログ確認
journalctl -u tailscaled -f
journalctl -u smbd -f
journalctl -u nfs-server -f
```

## クライアント接続方法

### 前提条件
各クライアントデバイスでTailscaleに接続済みである必要があります。

```bash
# クライアントでTailscale接続
tailscale up
```

### macOS
```bash
# Finder → サーバへ接続
smb://nixos.tail-scale.ts.net/public

# または Magic DNS使用
smb://nixos/public
```

### Windows
```bash
# エクスプローラーのアドレスバー
\\nixos.tail-scale.ts.net\public

# または Magic DNS使用
\\nixos\public
```

### Linux
```bash
# SMB
sudo mount -t cifs //nixos.tail-scale.ts.net/public /mnt/fileserver -o username=miyoshi_s

# NFS
sudo mount -t nfs nixos.tail-scale.ts.net:/mnt/sda1/shares/docker /mnt/docker-data

# Magic DNS使用の場合
sudo mount -t cifs //nixos/public /mnt/fileserver -o username=miyoshi_s
sudo mount -t nfs nixos:/mnt/sda1/shares/docker /mnt/docker-data
```

## モニタリング & バックアップ

### 監視項目
- **VPN接続**: Tailscale接続状態とトラフィック
- **ディスク使用量**: ストレージ使用率監視
- **ネットワーク転送量**: VPN経由のファイル転送量
- **アクセスログ**: ユーザーアクセス履歴
- **サービス稼働状況**: SMB/NFS/SSH各サービスの状態

### バックアップ戦略
- **プライマリ → セカンダリ**: rsyncによる定期ミラーリング（sda1 → sdb1）
- **重要データ**: 外部バックアップ対応
- **スナップショット**: 定期的なデータスナップショット

## 拡張オプション

### Web管理インターフェース
- **Cockpit**: システム全体の管理UI（Tailscale経由）
- **File Browser**: Web経由でのファイル管理（Tailscale経由）
- **Nextcloud**: クラウドストレージ機能（Tailscale経由）
- **Tailscale Admin Console**: VPN管理とACL設定

### Exit Node機能
- **リモートアクセス**: ファイルサーバ経由でのインターネットアクセス
- **セキュアブラウジング**: 外出先からの安全なネット接続
- **地域制限回避**: 自宅IP経由でのサービス利用

### 高度な機能
- **ZFS**: データ整合性とスナップショット機能
- **Jellyfin**: メディアサーバ機能（Tailscale経由）
- **rsync daemon**: 効率的な同期サービス
- **Tailscale ACL**: 細かいアクセス制御とロール管理（Admin Console）

## トラブルシューティング

### よくある問題
1. **Tailscale接続できない**
   - OAuth認証の確認
   - ファイアウォール設定確認（UDP 41641）
   - `tailscale netcheck`でネットワーク診断

2. **SMB接続できない**
   - Tailscale接続状態確認
   - Magic DNS設定確認
   - ユーザー認証設定確認

3. **NFS接続できない**
   - Tailscale経由でのアクセス確認
   - exports設定確認
   - ネットワーク権限確認

4. **権限エラー**
   - ディレクトリ権限確認
   - グループ所属確認
   - Tailscale ACL設定確認（Admin Console）

### ログ確認コマンド
```bash
# Tailscale
journalctl -u tailscaled -n 50
tailscale status --verbose
tailscale netcheck

# Samba
journalctl -u smbd -n 50
journalctl -u nmbd -n 50

# NFS
journalctl -u nfs-server -n 50

# システム全体
dmesg | tail -50
```

## 参考資料

### NixOS関連
- [NixOS Manual - Samba](https://nixos.org/manual/nixos/stable/#module-services-samba)
- [NixOS Manual - NFS](https://nixos.org/manual/nixos/stable/#module-services-nfs)
- [NixOS Manual - Tailscale](https://nixos.org/manual/nixos/stable/#module-services-tailscale)

### Tailscale関連
- [Tailscale Documentation](https://tailscale.com/kb/)
- [Tailscale Magic DNS](https://tailscale.com/kb/1081/magicdns/)
- [Tailscale Exit Nodes](https://tailscale.com/kb/1103/exit-nodes/)
- [Tailscale ACL Documentation](https://tailscale.com/kb/1018/acls/)

### ファイルサーバ関連
- [Samba Documentation](https://www.samba.org/samba/docs/)
- [NFS Documentation](https://nfs.sourceforge.net/)

### セキュリティ
- [Tailscale Security](https://tailscale.com/security/)
- [NixOS Security](https://nixos.org/manual/nixos/stable/#sec-security)
