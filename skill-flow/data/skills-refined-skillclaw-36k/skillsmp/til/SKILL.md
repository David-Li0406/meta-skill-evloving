---
name: til
description: Today I Learned - セッションから知識・発見を抽出してObsidianデイリーノートに記録
user-invocable: true
allowed-tools:
  - Bash
  - Write
  - Read
---

# /til - 知識の記録

現在のClaude Codeセッションから得られた知識・発見をObsidianデイリーノートに記録します。

## 記録対象

- 技術的な学び（ツール、ライブラリ、言語の挙動）
- サービス固有の仕様（WinTicket、IRISなどの構成・設定）
- ドメイン知識（環境構成、サービス間の依存関係、命名規則）
- 設定値・パラメータの意味（なぜその値か、デフォルトは何か）
- トラブルシューティングの記録（原因と解決策）
- 「こうなっている」という事実の発見
- PRで扱ったリソースの構造・仕様
- 調査で判明したシステムの内部構造・命名規則

## 使い方

- `/til` - セッション全体から知識を抽出
- `/til [トピック]` - 特定のトピックに絞って抽出

## 処理フロー

### 1. 知識の抽出

現在のセッションの会話を分析し、記録すべき知識を特定。

### 2. Obsidian最適化

- 見出し: `## タイトル: サブタイトル`
- タグ: `#til/カテゴリ` 形式
- 内部リンク: 技術名、ツール名、サービス名を `[[リンク]]` 形式に

### 3. ファイル書き込み

保存先: `~/gh/github.com/ryosukesuto/obsidian-notes/01_Daily/YYYY-MM-DD.md`

```bash
DAILY_DIR="$HOME/gh/github.com/ryosukesuto/obsidian-notes/01_Daily"
DAILY_NOTE="$DAILY_DIR/$(date '+%Y-%m-%d').md"

if [ ! -d "$DAILY_DIR" ]; then
    mkdir -p "$DAILY_DIR"
fi

NEW_FILE=false
if [ ! -f "$DAILY_NOTE" ]; then
    echo "# $(date '+%Y-%m-%d')" > "$DAILY_NOTE"
    echo "" >> "$DAILY_NOTE"
    NEW_FILE=true
fi

if [ "$NEW_FILE" = false ]; then
    echo "" >> "$DAILY_NOTE"
    echo "---" >> "$DAILY_NOTE"
    echo "" >> "$DAILY_NOTE"
fi
```

## 出力形式テンプレート

```markdown
## WinTicket: Fastlyのactivate設定
#til/winticket #til/fastly #til/terraform

### 背景
stg.winticket.bet にアクセスすると「unknown domain」エラーが発生

### 調査
1. [[Terraform]]の設定ファイルを確認
2. 動作している api-stg.winticket.bet と比較

### 仕様・発見
| サービス | activate設定 | 状態 |
|----------|-------------|------|
| api-stg.winticket.bet | `true` | 動作 |
| stg.winticket.bet | 未設定 | 停止 |

### ポイント
- 新規Fastlyサービス作成時は `activate = true` を明示的に設定
```

## 注意事項

- 記録すべき内容がない場合は報告
- 事実の記録を重視。「こうすべき」より「こうなっている」を優先
