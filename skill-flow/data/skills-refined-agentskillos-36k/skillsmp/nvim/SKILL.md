---
name: nvim
description: Neovim/LazyVim configuration assistant for this repository
---

# Neovim/LazyVim Configuration Assistant

このリポジトリのNeovim (LazyVim) 設定に関する質問に回答します。

## 手順

1. **まず `nvim/LAZYVIM_REFERENCE.md` を読む** - LazyVimの規約とこのリポジトリの設定パターン
2. **次に該当する `lua/plugins/*.lua` を確認** - 既存のプラグイン設定
3. **上記で解決しない場合のみWeb検索** - 新プラグインの追加、詳細なAPI、エラー対応

## ファイル構成

```
nvim/
├── init.lua                    # エントリーポイント
├── lua/config/
│   ├── lazy.lua                # LazyVim + Extras設定
│   ├── options.lua             # vim.opt設定
│   └── keymaps.lua             # カスタムキーマップ
└── lua/plugins/                # プラグイン設定（*.lua を参照）
```

## 回答時の注意

- LazyVimの規約に従った設定を提案する
- 既存の設定スタイル（opts, keys, cmd パターン）に合わせる
- プラグイン追加時は `lua/plugins/` に新ファイルを作成
