---
name: ghostty-configure
description: Ghosttyターミナルエミュレータの設定・カスタマイズを支援。テーマ、フォント、キーバインド、ウィンドウ設定など。「Ghostty」「ゴースティ」「ターミナル設定」などの依頼で起動。
allowed-tools:
  - Read
  - Write
  - StrReplace
  - Bash
  - WebSearch
model: claude-haiku-4-5-20251001
user-invocable: true
---

# Ghostty Configure スキル

このスキルは、Ghosttyターミナルエミュレータの設定・カスタマイズを支援します。

**IMPORTANT: このスキルを使用する際は、特に指定が無い限り日本語でユーザーとコミュニケーションを取ってください。**

## Ghosttyとは

Ghosttyは、速度、シンプルさ、合理的なデフォルト設定を重視したクロスプラットフォームのターミナルエミュレータです。テキストベースの設定ファイルで外観や動作を細かくカスタマイズできます。

## 設定ファイルの場所

### macOS
```
$HOME/Library/Application Support/com.mitchellh.ghostty/config
```

### Linux
```
$XDG_CONFIG_HOME/ghostty/config
（デフォルト: ~/.config/ghostty/config）
```

両方の場所にファイルが存在する場合、後から読み込まれたファイルが優先されます。

## 設定構文

Ghosttyは `key = value` 形式を使用します。

```plaintext
# コメントは # で記述
background = 282c34
foreground = ffffff
font-family = "JetBrains Mono"
```

- キーは大文字・小文字を区別
- 値はクォートあり/なし両方可能
- 空行は無視される

## 主要な設定オプション

### テーマ・外観

| オプション | 説明 | 例 |
|-----------|------|-----|
| `theme` | プリセットテーマを適用 | `theme = Builtin Solarized Light` |
| `background` | 背景色 | `background = 282c34` |
| `foreground` | 文字色 | `foreground = ffffff` |
| `background-opacity` | 背景の透明度（0.0-1.0） | `background-opacity = 0.9` |
| `background-blur-radius` | 背景のぼかし効果 | `background-blur-radius = 10` |
| `background-image` | 背景画像（v1.2+） | `background-image = /path/to/image.png` |

### フォント設定

| オプション | 説明 | 例 |
|-----------|------|-----|
| `font-family` | フォントファミリー | `font-family = "JetBrains Mono"` |
| `font-size` | フォントサイズ | `font-size = 14` |
| `font-style` | フォントスタイル | `font-style = bold` |
| `font-thicken` | フォントを太くする | `font-thicken = true` |
| `font-thicken-strength` | 太さの強度 | `font-thicken-strength = 1` |
| `font-feature` | OpenType機能 | `font-feature = -dlig` |

### ウィンドウ設定

| オプション | 説明 | 例 |
|-----------|------|-----|
| `window-padding-x` | 横方向のパディング | `window-padding-x = 10` |
| `window-padding-y` | 縦方向のパディング | `window-padding-y = 10` |
| `window-padding-balance` | パディングのバランス調整 | `window-padding-balance = true` |
| `window-decoration` | タイトルバー/ボーダーの表示 | `window-decoration = true` |
| `quick-terminal-size` | クイックターミナルのサイズ（v1.2+） | `quick-terminal-size = 80x24` |

### シェル統合

| オプション | 説明 | 例 |
|-----------|------|-----|
| `shell-integration` | シェル統合の有効化 | `shell-integration = true` |
| `shell-integration-features` | 有効にする機能 | `shell-integration-features = cursor,sudo,title` |

### カーソル設定

| オプション | 説明 | 例 |
|-----------|------|-----|
| `cursor-style` | カーソルスタイル | `cursor-style = block` |
| `cursor-style-blink` | カーソルの点滅 | `cursor-style-blink = false` |

### キーバインド

カスタムキーバインドを設定できます：

```plaintext
keybind = ctrl+z=close_surface
keybind = ctrl+shift+t=new_tab
keybind = ctrl+shift+n=new_window
```

### その他

| オプション | 説明 | 例 |
|-----------|------|-----|
| `confirm-close-surface` | 閉じる際の確認 | `confirm-close-surface = false` |
| `quit-after-last-window-closed` | 最後のウィンドウを閉じたら終了 | `quit-after-last-window-closed = true` |

## 設定のリロード

設定変更後、以下のショートカットでリロードできます：

- **macOS**: `Cmd + Shift + ,`
- **Linux**: `Ctrl + Shift + ,`

一部のオプションはGhosttyの再起動が必要です。

## v1.2の新機能（2025年）

- **コマンドパレット**: アクションへの素早いアクセス
- **クイックターミナルサイズ**: `quick-terminal-size`でデフォルトサイズを設定
- **背景画像**: `background-image`で背景画像を設定可能
- **SSH改善**: リモートシステム接続時のシェル統合機能が向上

## テーマの探し方

```bash
# 利用可能なビルトインテーマを確認
ghostty +list-themes

# テーマのプレビュー
ghostty +show-config --default | grep theme
```

## トラブルシューティング

### 設定が反映されない

1. 設定ファイルのパスが正しいか確認
2. 構文エラーがないか確認
3. リロード（Cmd/Ctrl + Shift + ,）を試す
4. Ghosttyを再起動

### フォントが表示されない

1. フォントがシステムにインストールされているか確認
2. フォント名が正確か確認（クォートで囲む）
3. `fc-list | grep "フォント名"` でフォント名を確認

### パフォーマンスの問題

```plaintext
# ハードウェアアクセラレーションの確認
# GPU使用状況を確認し、必要に応じて調整
```

## 公式ドキュメント

設定オプションの完全なリストは公式ドキュメントを参照：
https://ghostty.org/docs/config

## 設定ファイルの探索

**IMPORTANT**: スキル起動時には、必ず以下の手順で設定ファイルの場所を特定してください。

### 探索手順

1. 以下の候補パスを**すべて**確認（OSに関わらず全ての場所をチェック）：
   ```bash
   # macOS標準の場所
   test -f "$HOME/Library/Application Support/com.mitchellh.ghostty/config" && echo "Found: $HOME/Library/Application Support/com.mitchellh.ghostty/config"

   # XDG準拠（環境変数が設定されている場合）
   test -n "$XDG_CONFIG_HOME" && test -f "$XDG_CONFIG_HOME/ghostty/config" && echo "Found: $XDG_CONFIG_HOME/ghostty/config"

   # XDG準拠（デフォルト）- macOSでも使用される場合がある
   test -f "$HOME/.config/ghostty/config" && echo "Found: $HOME/.config/ghostty/config"
   ```

2. 見つかった設定ファイルの場所をユーザーに報告

3. 複数の場所にファイルが存在する場合：
   - 両方の場所を報告
   - Ghosttyは後から読み込まれたファイルを優先することを説明
   - どちらを編集するかユーザーに確認

4. ファイルが見つからない場合：
   - デフォルトの場所（macOSなら macOS の場所、Linuxなら `~/.config/ghostty/config`）を提案
   - 新規作成するか確認

## ワークフロー例

### 設定ファイルの確認・編集

1. 現在の設定を確認
2. 必要な変更を特定
3. 設定ファイルを編集
4. リロードして確認

### 新しいテーマの適用

```bash
# 1. 利用可能なテーマを確認
ghostty +list-themes

# 2. 設定ファイルでテーマを指定
theme = テーマ名
```

## 重要な注意事項

1. **バックアップ**: 大きな変更を加える前に設定ファイルをバックアップ
2. **構文チェック**: 設定ファイルの構文エラーはGhosttyの起動を妨げる可能性あり
3. **最新情報の確認**: Ghosttyは活発に開発されているため、最新の機能は公式ドキュメントを確認
4. **日本語でコミュニケーション**: 特に指定が無い限り、ユーザーとのやり取りは日本語で行う
