# リポジトリ構成

## ディレクトリ構造

```
dotfiles/
├── install.sh           # GNU Stowによるインストーラー
├── scripts/             # ユーティリティスクリプト
├── packages/            # 共通パッケージ（全OS）
│   ├── shell/           # シェル設定（.zshrc, .bashrc）
│   ├── nvim/            # Neovim設定
│   ├── git/             # Git設定
│   ├── claude/          # Claude Code設定、skills
│   ├── gemini/          # Gemini CLI設定
│   ├── mise/            # miseツール管理
│   ├── kitty/           # Kittyターミナル
│   ├── starship/        # Starshipプロンプト
│   ├── lazygit/         # Lazygit設定
│   ├── yazi/            # Yaziファイラー
│   └── ...
├── packages-darwin/     # macOS専用パッケージ
├── packages-linux/      # Linux専用パッケージ
└── lib/                 # 共有ライブラリ（Lua等）
```

## パッケージ構造の規則

各パッケージはホームディレクトリからの相対パスで構成:

```
packages/shell/
├── .zshrc              # → ~/.zshrc
├── .bashrc             # → ~/.bashrc
└── .config/
    └── shell/          # → ~/.config/shell/
        ├── common.sh
        ├── tools.sh
        └── os/
            ├── linux.sh
            └── darwin.sh
```

## 主要パッケージ

| パッケージ | 内容 |
|-----------|------|
| shell | シェル設定、環境変数、エイリアス |
| nvim | Neovim設定、プラグイン |
| claude | Claude Code設定、skills、hooks |
| gemini | Gemini CLI設定（統計オプトアウト等） |
| mise | ツールバージョン管理（yq等） |
| git | gitconfig、gitignore |

## OS固有パッケージ

- `packages-darwin/`: macOS専用（Homebrew等）
- `packages-linux/`: Linux専用

install.shが自動的にOSを検出して適切なパッケージを適用。
