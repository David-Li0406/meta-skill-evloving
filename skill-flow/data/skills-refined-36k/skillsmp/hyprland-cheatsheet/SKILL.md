---
name: hyprland-cheatsheet
description: Hyprland window manager shortcuts including window navigation, workspace management, media keys, and configuration files
---

# Hyprland チートシート

## 基本操作

| キー | 動作 |
|------|------|
| `Super + Return` | ターミナル（Alacritty）を開く |
| `Super + Shift + Q` | アクティブウィンドウを閉じる |
| `Super + Shift + M` | Hyprlandを終了（ログアウト） |
| `Super + Shift + E` | ファイルマネージャー（Thunar）を開く |
| `Super + Shift + L` | スクリーンロック |

## アプリケーションランチャー

| キー | 動作 |
|------|------|
| `Super + Space` | wofi ランチャー |

## ウィンドウ操作

| キー | 動作 |
|------|------|
| `⌘ (Super) + Shift + V` | クリップボード履歴から貼り付け（Hyprland バインドは `Alt + Shift + V`） |
| `Win（物理Super） + Shift + V` | フローティングモード切替 |
| `Super + Shift + P` | 疑似タイル |
| `Super + J` | 分割方向切替 |

## フォーカス移動

### 矢印キー
| キー | 動作 |
|------|------|
| `Super + ←` | 左のウィンドウにフォーカス |
| `Super + →` | 右のウィンドウにフォーカス |
| `Super + ↑` | 上のウィンドウにフォーカス |
| `Super + ↓` | 下のウィンドウにフォーカス |

### Vimキー
| キー | 動作 |
|------|------|
| `Super + h` | 左のウィンドウにフォーカス |
| `Super + l` | 右のウィンドウにフォーカス |
| `Super + k` | 上のウィンドウにフォーカス |
| `Super + j` | 下のウィンドウにフォーカス |

## ワークスペース操作

| キー | 動作 |
|------|------|
| `Super + 1-9,0` | ワークスペース 1-10 に切り替え |
| `Super + Shift + 1-9,0` | アクティブウィンドウをワークスペース 1-10 に移動 |
| `Super + マウスホイール上` | 前のワークスペース |
| `Super + マウスホイール下` | 次のワークスペース |

## マウス操作

| キー | 動作 |
|------|------|
| `Super + 左クリックドラッグ` | ウィンドウを移動 |
| `Super + 右クリックドラッグ` | ウィンドウをリサイズ |

## スクリーンショット

| キー | 動作 |
|------|------|
| `Print` | 範囲選択スクリーンショット（クリップボードに保存） |
| `Shift + Print` | 全画面スクリーンショット（クリップボードに保存） |

## メディアキー

| キー | 動作 |
|------|------|
| `音量+` | 音量を上げる |
| `音量-` | 音量を下げる |
| `ミュート` | 消音切替 |
| `再生/一時停止` | メディア再生/一時停止 |
| `次の曲` | 次のトラック |
| `前の曲` | 前のトラック |

## 画面輝度

| キー | 動作 |
|------|------|
| `輝度+` | 画面輝度を上げる（+10%） |
| `輝度-` | 画面輝度を下げる（-10%） |

## 自動起動アプリケーション

- Waybar（ステータスバー）
- Dunst（通知デーモン）
- Hyprpaper（壁紙）
- Fcitx5（日本語入力）
- Gammastep（ブルーライトフィルター）

## ターミナルコマンド

| コマンド | 動作 |
|----------|------|
| `hyprctl dispatch exit` | Hyprlandを終了 |
| `hyprctl clients` | アクティブなウィンドウ一覧 |
| `hyprctl workspaces` | ワークスペース一覧 |
| `hyprctl reload` | 設定をリロード |

## 設定ファイル

- メイン設定: `/etc/xdg/hypr/hyprland.conf`
- Waybar設定: `/etc/xdg/waybar/config`
- Dunst設定: `/etc/xdg/dunst/dunstrc`

## テーマと見た目の調整

- Waybar: `nixos/desktop/hyprland/waybar.nix` でモジュール構成・Catppuccin配色を管理。`style.css` 内の `@define-color` を変更すると一括で色が切り替わります。
- ウィンドウ装飾: `nixos/desktop/hyprland/config.nix` の `decoration`・`general` ブロックで丸み・ブラー・ボーダー色を制御。
- 壁紙: `nixos/desktop/hyprland/wallpaper.nix` がグラデーション壁紙を自動生成します。別画像に差し替える場合は `preload`/`wallpaper` 行を書き換え。
- ランチャー: `nixos/desktop/hyprland/wofi.nix` でサイズやフォント、ハイライト色を変更可能。

## リロードのショートカット

- Waybar を再起動: `systemctl --user restart waybar`
- Hyprland 設定反映: `hyprctl reload`
- Wofi テーマ確認: `wofi --show drun` を都度実行してプレビュー
