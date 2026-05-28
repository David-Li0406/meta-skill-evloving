# to_html

MarkdownファイルからHTMLスライドを生成する。

## 引数

`<mds-file>` (例: 1_mds/part1.md)

## 実行コマンド

```bash
npm run to_html -- <mds-file>
```

## 使用例

```bash
# 基本的な使い方
npm run to_html -- 1_mds/sample.md

# 出力先を指定
npm run to_html -- 1_mds/sample.md --output 2_htmls

# ファイル名プレフィックスを指定
npm run to_html -- 1_mds/sample.md --prefix slide

# ドライラン（ファイルを書き込まずに確認）
npm run to_html -- 1_mds/sample.md --dry-run
```

## Markdown記法

[README.md](../README.md) の「Markdown記法」セクションを参照。
