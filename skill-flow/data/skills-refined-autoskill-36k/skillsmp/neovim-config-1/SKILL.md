---
name: neovim-config
description: Neovim設定のヘルプ。プラグイン追加、キーマッピング設定、LazyVim設定の質問に使用。
allowed-tools: Read, Grep, Glob
---

# Neovim設定スキル

このdotfilesリポジトリのNeovim設定をサポートします。

## 設定構成

- **設定ディレクトリ**: `config/nvim/`
- **プラグインマネージャー**: Lazy.nvim
- **フレームワーク**: LazyVim

## ディレクトリ構造

```
config/nvim/
├── init.lua              # エントリーポイント
├── lua/
│   ├── config/
│   │   ├── lazy.lua      # Lazy.nvim初期化
│   │   ├── keymaps.lua   # カスタムキーマッピング
│   │   ├── options.lua   # Vimオプション
│   │   └── autocmds.lua  # 自動コマンド
│   └── plugins/
│       └── *.lua         # プラグイン設定
├── lazy-lock.json        # プラグインロックファイル
└── stylua.toml           # Luaフォーマッター設定
```

## 主要プラグイン

- LazyVim（設定フレームワーク）
- nvim-treesitter（構文解析）
- nvim-lspconfig + mason.nvim（LSP）
- blink.cmp（補完）
- tokyonight.nvim（カラースキーム）
- gitsigns.nvim（Git統合）
- flash.nvim（高速移動）
- which-key.nvim（キーバインド表示）

## プラグイン追加方法

`lua/plugins/`ディレクトリに新しい`.lua`ファイルを作成：

```lua
return {
  {
    "author/plugin-name",
    opts = {
      -- 設定オプション
    },
  },
}
```

## キーマッピング追加方法

`lua/config/keymaps.lua`に追記：

```lua
vim.keymap.set("n", "<leader>xx", function()
  -- アクション
end, { desc = "説明" })
```

## 参考リンク

- LazyVim公式: https://www.lazyvim.org/
- Lazy.nvim公式: https://lazy.folke.io/
