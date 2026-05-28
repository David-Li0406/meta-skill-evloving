# setup

プロジェクトの初期セットアップを行う。

## 手順

1. フォルダ作成
2. サンプルファイルをコピー
3. package.json生成（既存の場合は依存関係をマージ）
4. npm install 実行
5. npx playwright install chromium 実行
6. 完了メッセージを表示

## 実行内容

### 1. フォルダ作成

```bash
mkdir -p 1_mds 2_htmls 3_pptxs
```

### 2. サンプルファイルをコピー

`1_mds/` にサンプルMarkdownをコピー（存在しない場合のみ）:

```bash
cp <skill-path>/assets/1_mds/sample.md 1_mds/sample.md
```

### 3. package.json生成

既存のpackage.jsonがない場合は新規作成。
`dependencies` は `<skill-path>/assets/package.json` から読み取ってコピーする:

```json
{
  "name": "md2html2pptx-project",
  "version": "1.0.0",
  "scripts": {
    "to_html": "NODE_PATH=$PWD/node_modules node <skill-path>/assets/to_html.js",
    "preview": "NODE_PATH=$PWD/node_modules node <skill-path>/assets/preview.js",
    "to_pptx": "NODE_PATH=$PWD/node_modules node <skill-path>/assets/to_pptx.js",
    "clean_to_html_all": "rm -rf 2_htmls/* && for f in 1_mds/*.md; do npm run to_html -- \"$f\"; done"
  },
  "dependencies": "<skill-path>/assets/package.json の dependencies をコピー"
}
```

既存のpackage.jsonがある場合は、`<skill-path>/assets/package.json` の dependencies をマージする。

### 4. 依存関係インストール

```bash
npm install
```

### 5. Playwrightブラウザインストール

```bash
npx playwright install chromium
```

### 6. 完了メッセージ

```
✅ セットアップ完了！

📁 作成されたフォルダ:
   1_mds/    - Markdownファイルを置く (sample.md をコピー済み)
   2_htmls/  - 生成されたHTMLスライド
   3_pptxs/  - 生成されたPowerPoint

🚀 使い方:
   1. /md2html2pptx to_html 1_mds/sample.md  → HTMLスライド生成
   2. /md2html2pptx preview                  → ブラウザでプレビュー
   3. /md2html2pptx to_pptx                  → PowerPoint生成
```

## オプション: Full Setup

プロジェクトにスキルのassetsをコピーする場合:

```bash
cp -r <skill-path>/assets/html2pptx ./
cp -r <skill-path>/assets/md2html ./
cp <skill-path>/assets/to_html.js ./
cp <skill-path>/assets/preview.js ./
cp <skill-path>/assets/to_pptx.js ./
```

この場合、package.jsonのスクリプトを以下に変更:

```json
{
  "scripts": {
    "to_html": "node to_html.js",
    "preview": "node preview.js",
    "to_pptx": "node to_pptx.js"
  }
}
```

## トラブルシューティング

### Chromiumインストールエラー

```bash
npx playwright install chromium --with-deps
```

### node_modules関連エラー

```bash
rm -rf node_modules package-lock.json
npm install
```

### 権限エラー（macOS）

```bash
xattr -cr node_modules
```
