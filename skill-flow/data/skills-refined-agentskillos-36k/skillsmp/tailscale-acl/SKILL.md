---
name: tailscale-acl
description: Tailscale ACL configuration guide for access control and SSH rules management via Admin Console
---

# Tailscale ACL 運用メモ

Tailscale ACLはTailnet全体に適用されるため、NixOS側の設定では管理しません。
設定はTailscale Admin Consoleで行います。

## 目的
- デバイス・ユーザー単位でアクセスを制御する
- Tailscale SSHの許可範囲を明確にする

## 設定場所
- Tailscale Admin Console → ACL

## 例: SSH許可ルール
```json
{
  "ssh": [
    {
      "action": "accept",
      "src": ["miyoshi_s"],
      "dst": ["nixos"],
      "users": ["miyoshi_s"]
    }
  ]
}
```

## 注意点
- 変更後はAdmin Console上で保存と適用を実行する
- ルールが適用されるまで数十秒かかることがある

## 参考
- https://tailscale.com/kb/1018/acls/
