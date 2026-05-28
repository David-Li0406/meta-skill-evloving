# to_pptx

2_htmls/ディレクトリのHTMLからPowerPointを生成する。

## 引数

`<filter>` (例: part1, part2) 省略時は全スライド

| 引数 | 説明 |
|------|------|
| `part1` | 第1部のスライドのみ生成 |
| `part2` | 第2部のスライドのみ生成 |
| `part3` | 第3部のスライドのみ生成 |
| `part4` | 第4部のスライドのみ生成 |
| `part5` | 第5部のスライドのみ生成 |
| 省略 | 全スライドを生成 |

複数指定も可能（例: `part1 part2`）

## 実行コマンド

```bash
# 全スライド
npm run to_pptx

# フィルター指定
npm run to_pptx -- <filter>
```

## 出力ファイル

`3_pptxs/` ディレクトリにPPTXファイルが生成される。

## 前提条件

- `npm install` が実行済みであること
- `2_htmls/` ディレクトリにHTMLファイルが存在すること

## トラブルシューティング

エラーが発生した場合：

1. `npm install` を実行
2. `npx playwright install chromium` を実行（Playwrightのセットアップ）
3. HTMLファイルの構文エラーを確認
