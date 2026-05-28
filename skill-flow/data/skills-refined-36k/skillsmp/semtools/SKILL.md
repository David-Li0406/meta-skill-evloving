---
description: 自然言語でファイルの中身を検索したいときに使用する。semtoolsの使用ガイド。
---

# semtools - セマンティック検索 CLI

## コマンド一覧

| コマンド | 説明 | API |
|---------|------|-----|
| `search` | ローカルセマンティック検索 | 不要 |
| `workspace` | 大規模検索用のキャッシュ管理 | 不要 |
| `parse` | PDF/DOCX/PPTX → Markdown 変換 | LlamaParse API |

## search - セマンティック検索

grep の代わりにセマンティック（意味的）な検索ができる。キーワードが完全一致しなくても関連する内容を見つける。

```bash
# 基本的な使い方
search "検索クエリ" ファイルパス

# 進捗ファイルを検索
search "認証機能の実装" .agents/progress/*.md

# 距離しきい値を調整（小さいほど厳密）
search "API設計" docs/*.md --max-distance 0.3

# 前後の行数を指定
search "エラーハンドリング" src/*.ts --n-lines 5
```

### オプション

- `--max-distance <float>`: 類似度しきい値（デフォルト: 0.5、小さいほど厳密）
- `--n-lines <int>`: マッチ前後の行数（デフォルト: 3）

## workspace - 大規模検索

多数のファイルを頻繁に検索する場合、インデックスを作成して高速化する。

```bash
# インデックス作成
workspace index ./docs

# インデックスを使って検索
workspace search "クエリ" ./docs
```

## parse - ドキュメント変換

PDF、DOCX、PPTX を Markdown に変換する。LlamaParse API キーが必要。

```bash
# 変換
parse document.pdf
parse reports/*.docx
```

## パイプライン例

```bash
# PDF を変換してから検索
parse docs/*.pdf | xargs search "API endpoints"

# grep と組み合わせ
search "認証" src/*.ts | grep -v test
```

## 設定ファイル

`~/.semtools_config.json`:

```json
{
  "llama_cloud_api_key": "llx-..."
}
```

優先順位: CLI 引数 > 設定ファイル > 環境変数

## 参考

- https://github.com/run-llama/semtools
