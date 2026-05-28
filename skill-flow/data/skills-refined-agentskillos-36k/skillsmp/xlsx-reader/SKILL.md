---
name: xlsx-reader
description: Reads Excel (.xlsx) files and converts to Markdown format. Handles multiple sheets and large tables. Use when needing to read Excel spreadsheets. Requires openpyxl package.
---

# Excel Reader

Excel (.xlsx) ファイルを読み込んで Markdown テーブル形式に変換するスキルです。

## クイックスタート

### 基本的な使い方

```bash
# WSL環境でPythonスクリプトを実行
wsl python3 scripts/read_xlsx.py "/mnt/c/path/to/file.xlsx"
```

### Markdown形式で保存

1. スクリプトでデータ抽出
2. Write ツールで .md ファイルに保存

## 前提条件

openpyxl パッケージが必要です：

```bash
wsl pip3 install openpyxl
```

## 使用例

### 例1: Excel ファイルを読み込んで表示

```
User: "data.xlsx を読み込んで"
Assistant:
1. Windowsパスを WSL パスに変換
2. wsl python3 scripts/read_xlsx.py を実行
3. 全シートの内容を Markdown テーブルで表示
```

### 例2: 特定のシートのみ読み込み

```
User: "data.xlsx の Sheet1 と Sheet2 だけ読み込んで"
Assistant:
1. スクリプトにシート名を指定して実行
2. 指定したシートのみ Markdown 化
```

### 例3: 大きなファイルの一部のみ読み込み

```
User: "data.xlsx の最初の100行だけ読み込んで"
Assistant:
1. max_rows パラメータを指定して実行
2. 各シートの先頭100行のみ抽出
```

## ワークフロー

### 単一ファイルの読み込み

1. ユーザーが Excel ファイルパスを指定
2. Windows パスを WSL パス形式に変換
3. `wsl python3 scripts/read_xlsx.py` を実行
4. Markdown テーブルとして表示または保存

### 複数シートの処理

1. 全シート名を取得
2. 各シートをテーブルに変換
3. シートごとに見出しを付けて整理

## 出力形式

### Markdown 構造

```markdown
# data.xlsx

**Total Sheets:** 3

---

## Sheet: Sheet1

**Dimensions:** 100 rows × 5 columns

| 列1 | 列2 | 列3 | 列4 | 列5 |
| --- | --- | --- | --- | --- |
| データ1 | データ2 | データ3 | データ4 | データ5 |
| ... | ... | ... | ... | ... |

---

## Sheet: Sheet2

**Dimensions:** 50 rows × 3 columns

| A | B | C |
| --- | --- | --- |
| 値1 | 値2 | 値3 |
| ... | ... | ... |

---
```

## スクリプト詳細

Python スクリプトは `scripts/read_xlsx.py` に配置されています。

**主な機能:**
- 複数シートの読み込み
- Markdown テーブル形式への変換
- シート指定
- 行数制限
- エラーハンドリング

**使い方:**
```bash
python scripts/read_xlsx.py <file_path> [sheet_names] [max_rows]

# 例
python scripts/read_xlsx.py data.xlsx
python scripts/read_xlsx.py data.xlsx 'Sheet1,Sheet2'
python scripts/read_xlsx.py data.xlsx 'Sheet1' 100
```

## 対応機能

- ✅ 複数シートの読み込み
- ✅ Markdown テーブル形式
- ✅ シート指定
- ✅ 行数制限
- ✅ セルの値取得（計算式の結果）
- ⚠️ セルの書式情報は失われる
- ⚠️ 画像・グラフは抽出不可
- ⚠️ マクロは実行されない

## 制限事項

- セルの書式（色、フォントなど）は失われます
- 画像、グラフ、図形は抽出されません
- マクロは実行されません
- 計算式は評価後の値のみ取得
- 非常に大きなファイルはメモリ制約に注意

## トラブルシューティング

### openpyxl がインストールされていない

```bash
wsl pip3 install openpyxl
```

### ファイルが開けない

- ファイルが Excel で開かれていないか確認
- .xlsx 形式か確認（.xls は非対応）
- ファイルのアクセス権限を確認
- ファイルが破損していないか確認

### メモリ不足エラー

大きな Excel ファイルの場合：
```bash
# 行数を制限して読み込み
python scripts/read_xlsx.py large_file.xlsx '' 1000
```

### シートが見つからない

- シート名が正確か確認（大文字小文字を区別）
- スペースや特殊文字に注意
- シート名をクォートで囲む

## パス変換

Windows パスから WSL パスへの変換：

- `C:\Users\...` → `/mnt/c/Users/...`
- `D:\Projects\...` → `/mnt/d/Projects/...`

## 使い分けガイド

| ファイル形式 | 推奨スキル | 理由 |
|-------------|----------|------|
| .xlsx (Excel) | **xlsx-reader** | Excelネイティブ |
| .xls (旧Excel) | pandas経由 | 別ツール必要 |
| .csv | 直接Read | テキストファイル |
| .tsv | 直接Read | テキストファイル |

## 高度な使い方

### 特定のシートのみ読み込み

```bash
# Sheet1 のみ
python scripts/read_xlsx.py data.xlsx 'Sheet1'

# 複数シート
python scripts/read_xlsx.py data.xlsx 'Sheet1,Sheet2,Sheet3'
```

### 大きなファイルのサンプリング

```bash
# 各シートの先頭100行のみ
python scripts/read_xlsx.py large_file.xlsx '' 100
```

### CSVとの違い

| 機能 | CSV | Excel (.xlsx) |
|------|-----|--------------|
| 複数シート | ❌ | ✅ |
| セル書式 | ❌ | ⚠️（失われる） |
| 数式 | ❌ | ✅（評価後の値） |
| ファイルサイズ | 小 | 大 |
| 読み込み速度 | 速 | やや遅 |

## 関連ツール

- **csv-reader**: CSV ファイル用（Read ツールで直接可能）
- **pandas**: より高度なデータ処理が必要な場合
- **xlrd**: 旧形式 .xls ファイル用

## バージョン履歴

- v1.0.0 (2026-01-06): 初期リリース
  - 基本的な Excel 読み込み機能
  - Markdown テーブル変換
  - 複数シート対応
  - WSL環境での動作
