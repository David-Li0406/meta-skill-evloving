# CLI開発: コマンド仕様設計

CLI（Command Line Interface）開発における設計ドキュメントの作成ガイドです。

## 作成する設計ドキュメント

`docs/design/cli-specification.md` を作成:

- **コマンド概要**: コマンドの目的と基本的な使い方
- **コマンド構文**: `command [options] <arguments>`
- **引数**: 必須引数と任意引数の説明
- **オプション**: フラグとその動作
- **入出力例**: 具体的な使用例と期待される出力
- **エラーケース**: エラーメッセージと終了コード
- **使用例とユースケース**: 典型的な使用シナリオ

## 補助ツールと設定ファイル

- **--help 出力仕様**: ヘルプメッセージの設計
- **man ページ形式**: 詳細なドキュメント構造
- **CLIフレームワークのスキーマ**:
  - Node.js: `oclif`, `commander.js`
  - Go: `cobra`, `cli`
  - Rust: `clap`
  - Python: `argparse`, `click`

## テンプレート構成例

```markdown
# CLI仕様: [コマンド名]

## 概要

[コマンドの目的と基本的な使い方]

## 構文

\`\`\`
command [options] <arguments>
\`\`\`

## 引数

- `<arg1>`: [説明]
- `[arg2]`: [説明]（任意）

## オプション

- `-f, --flag`: [説明]
- `-o, --output <file>`: [説明]
- `-v, --verbose`: 詳細な出力を表示
- `-h, --help`: ヘルプメッセージを表示

## 使用例

### 基本的な使用

\`\`\`bash

# 最小限の実行例

command input.txt

# 期待される出力

Processing input.txt...
Done.
\`\`\`

### オプション付きの使用

\`\`\`bash

# 出力ファイルを指定

command -o output.txt input.txt

# 詳細モードで実行

command -v input.txt
\`\`\`

### 複合的な使用

\`\`\`bash

# 複数のオプションを組み合わせ

command -v -f -o output.txt input.txt
\`\`\`

## 期待される出力

### 通常出力

\`\`\`
Processing input.txt...

- Found 100 items
- Processed 100 items
  Done. Output written to output.txt
  \`\`\`

### 詳細モード出力

\`\`\`
[INFO] Starting process...
[DEBUG] Reading input.txt
[DEBUG] Found 100 items
[DEBUG] Processing item 1/100
...
[INFO] Done. Output written to output.txt
\`\`\`

## エラーケース

| エラー状況             | エラーメッセージ                            | 終了コード |
| ---------------------- | ------------------------------------------- | ---------- |
| ファイルが見つからない | `Error: File not found: input.txt`          | 1          |
| 権限エラー             | `Error: Permission denied: input.txt`       | 2          |
| 無効な引数             | `Error: Invalid argument: --invalid`        | 3          |
| 構文エラー             | `Error: Missing required argument: <input>` | 4          |

## 終了コード

- `0`: 正常終了
- `1`: ファイルエラー
- `2`: 権限エラー
- `3`: 無効な引数
- `4`: 構文エラー

## ユースケース

### ユースケース1: データ変換

\`\`\`bash

# JSON を CSV に変換

command convert --from json --to csv data.json -o data.csv
\`\`\`

### ユースケース2: バッチ処理

\`\`\`bash

# 複数ファイルを一括処理

command batch \*.txt -o output/
\`\`\`

### ユースケース3: パイプライン処理

\`\`\`bash

# 他のコマンドと組み合わせ

cat input.txt | command process | grep "ERROR"
\`\`\`
```

## --help 出力の設計

コマンドの `--help` オプションで表示される内容:

```
USAGE:
  command [OPTIONS] <INPUT>

DESCRIPTION:
  [コマンドの簡潔な説明]

ARGUMENTS:
  <INPUT>    Input file path

OPTIONS:
  -o, --output <FILE>    Output file path
  -f, --force            Force overwrite existing files
  -v, --verbose          Enable verbose output
  -h, --help             Print help information
  -V, --version          Print version information

EXAMPLES:
  command input.txt
  command -o output.txt input.txt
  command -v -f input.txt

For more information, see: https://example.com/docs/command
```

## CLIフレームワーク別の設定例

### Node.js (commander.js)

```javascript
const { program } = require("commander");

program
  .name("command")
  .description("[コマンドの説明]")
  .version("1.0.0")
  .argument("<input>", "Input file path")
  .option("-o, --output <file>", "Output file path")
  .option("-f, --force", "Force overwrite")
  .option("-v, --verbose", "Verbose output")
  .action((input, options) => {
    // 実装
  });

program.parse();
```

### Go (cobra)

```go
var rootCmd = &cobra.Command{
  Use:   "command <input>",
  Short: "[コマンドの簡潔な説明]",
  Long:  "[コマンドの詳細な説明]",
  Args:  cobra.ExactArgs(1),
  Run: func(cmd *cobra.Command, args []string) {
    // 実装
  },
}

func init() {
  rootCmd.Flags().StringP("output", "o", "", "Output file path")
  rootCmd.Flags().BoolP("force", "f", false, "Force overwrite")
  rootCmd.Flags().BoolP("verbose", "v", false, "Verbose output")
}
```

### Rust (clap)

```rust
use clap::Parser;

#[derive(Parser)]
#[command(name = "command")]
#[command(about = "[コマンドの説明]", long_about = None)]
struct Cli {
    /// Input file path
    input: String,

    /// Output file path
    #[arg(short, long)]
    output: Option<String>,

    /// Force overwrite
    #[arg(short, long)]
    force: bool,

    /// Verbose output
    #[arg(short, long)]
    verbose: bool,
}
```

### Python (click)

```python
import click

@click.command()
@click.argument('input', type=click.Path(exists=True))
@click.option('-o', '--output', type=click.Path(), help='Output file path')
@click.option('-f', '--force', is_flag=True, help='Force overwrite')
@click.option('-v', '--verbose', is_flag=True, help='Verbose output')
def command(input, output, force, verbose):
    """[コマンドの説明]"""
    # 実装
    pass
```

## テスト設計の考慮事項

CLIコマンドのテストで確認すべき項目:

1. **正常系テスト**

   - 基本的な実行が成功する
   - オプションが正しく動作する
   - 出力が期待通りである

2. **異常系テスト**

   - 不正な引数でエラーが返る
   - ファイルが存在しない場合のエラー処理
   - 権限エラーの処理

3. **境界値テスト**

   - 空ファイルの処理
   - 大容量ファイルの処理
   - 特殊文字を含むファイル名

4. **統合テスト**
   - パイプライン処理
   - 他のコマンドとの組み合わせ

## 設計チェックリスト

- [ ] コマンド名は直感的で覚えやすいか
- [ ] 必須引数と任意引数が明確に区別されているか
- [ ] オプションの短縮形と長縮形が提供されているか
- [ ] --help と --version オプションが実装されているか
- [ ] エラーメッセージが明確で実行可能なアドバイスを含むか
- [ ] 終了コードが適切に設計されているか
- [ ] UNIX哲学（一つのことをうまくやる）に従っているか
- [ ] 標準入力/標準出力/標準エラー出力が適切に使い分けられているか
