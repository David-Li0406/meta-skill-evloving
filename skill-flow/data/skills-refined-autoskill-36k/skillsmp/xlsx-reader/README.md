# Excel Reader Skill

Excel (.xlsx) ファイルを読み込んで Markdown テーブル形式に変換するスキルです。

## ファイル構成

```
xlsx-reader/
├── SKILL.md           # メインスキル定義（Claude が読む）
├── README.md          # このファイル（人間向けドキュメント）
└── scripts/
    └── read_xlsx.py   # Excel 読み込み用 Python スクリプト
```

## インストール

### 前提条件

- WSL (Windows Subsystem for Linux)
- Python 3.x
- openpyxl パッケージ

### セットアップ

```bash
# openpyxl のインストール
wsl pip3 install openpyxl
```

## 使い方

Claude に以下のように依頼します：

```
「C:\Users\keita\repos\data.xlsx を読み込んで」
```

Claude が自動的に：
1. Windows パスを WSL パスに変換
2. スクリプトを実行してデータ抽出
3. Markdown テーブル形式で表示
4. 必要に応じて Markdown ファイルとして保存

## スクリプトの直接実行

```bash
# 基本的な使い方（全シート）
wsl python3 scripts/read_xlsx.py "/mnt/c/path/to/file.xlsx"

# 特定のシートのみ
wsl python3 scripts/read_xlsx.py "/mnt/c/path/to/file.xlsx" "Sheet1,Sheet2"

# 行数制限（各シート100行まで）
wsl python3 scripts/read_xlsx.py "/mnt/c/path/to/file.xlsx" "" 100

# 出力をファイルに保存
wsl python3 scripts/read_xlsx.py "/mnt/c/path/to/file.xlsx" > output.md
```

## 機能

### データ抽出

- ✅ 全シートの読み込み
- ✅ 特定シートの指定
- ✅ 行数制限
- ✅ セルの値取得
- ✅ 計算式の評価後の値

### Markdown 変換

- ✅ テーブル形式
- ✅ シートごとに見出し付き
- ✅ 行数・列数の情報
- ✅ 空シートの処理

### 制限事項

- ❌ セルの書式（色、フォントなど）
- ❌ 画像、グラフ、図形
- ❌ マクロの実行
- ❌ ピボットテーブル
- ❌ .xls 形式（旧Excel）

## 出力例

```markdown
# sales_data.xlsx

**Total Sheets:** 2

---

## Sheet: 2024年度売上

**Dimensions:** 13 rows × 4 columns

| 月 | 売上 | 目標 | 達成率 |
| --- | --- | --- | --- |
| 1月 | 1000000 | 950000 | 105% |
| 2月 | 1200000 | 1100000 | 109% |
| 3月 | 1500000 | 1300000 | 115% |
| ... | ... | ... | ... |

---

## Sheet: 商品別

**Dimensions:** 20 rows × 3 columns

| 商品名 | 数量 | 金額 |
| --- | --- | --- |
| 商品A | 100 | 500000 |
| 商品B | 150 | 750000 |
| ... | ... | ... |

---
```

## トラブルシューティング

### openpyxl が見つからない

```bash
wsl pip3 install openpyxl
```

### ファイルが開けない

**原因1: ファイルが開かれている**
- Excel でファイルを閉じる

**原因2: .xls 形式（旧Excel）**
- .xlsx 形式に保存し直す
- または pandas を使用

**原因3: ファイルが破損**
- Excel で開いて修復を試みる

### シートが見つからない

```bash
# まず全シートを確認
wsl python3 scripts/read_xlsx.py file.xlsx

# シート名を正確に指定（大文字小文字を区別）
wsl python3 scripts/read_xlsx.py file.xlsx "売上データ"
```

### メモリ不足

大きな Excel ファイルの場合：

```bash
# 行数を制限
wsl python3 scripts/read_xlsx.py large_file.xlsx "" 1000

# または特定のシートのみ
wsl python3 scripts/read_xlsx.py large_file.xlsx "Sheet1" 500
```

## 開発

### スクリプトの修正

`scripts/read_xlsx.py` を編集して機能を追加・修正できます。

### カスタマイズ例

#### 特定の範囲のみ読み込み

```python
# A1:D10 の範囲のみ
for row in sheet['A1':'D10']:
    for cell in row:
        print(cell.value)
```

#### セルの書式情報を取得

```python
from openpyxl import load_workbook

wb = load_workbook('file.xlsx')  # read_only=False
sheet = wb['Sheet1']
cell = sheet['A1']

# 書式情報
print(cell.font.color)
print(cell.fill.fgColor)
```

### テスト

```bash
# テスト用の Excel ファイルで動作確認
wsl python3 scripts/read_xlsx.py "/mnt/c/path/to/test.xlsx"
```

## パフォーマンス

### 処理時間の目安

| ファイルサイズ | 行数 | 処理時間 |
|--------------|------|---------|
| 小（< 1MB） | < 1,000 | < 1秒 |
| 中（1-10MB） | 1,000-10,000 | 1-5秒 |
| 大（> 10MB） | > 10,000 | 5-30秒 |

### 最適化

1. **read_only モード使用**（既に実装済み）
   - メモリ使用量削減
   - 読み込み速度向上

2. **行数制限**
   - 大きなファイルは部分的に読み込み

3. **不要なシートをスキップ**
   - 必要なシートのみ指定

## 関連スキル

- **csv-reader**: CSV ファイル用（Read ツールで対応可能）
- **docx-reader**: Word 文書用
- **pdf-reader**: PDF 文書用

## 使用ライブラリ

### openpyxl

- **機能**: Excel 2010+ (.xlsx) の読み書き
- **特徴**:
  - 純粋な Python 実装
  - 計算式の評価（data_only=True）
  - read_only モードでメモリ効率化
  - セル書式情報の取得も可能

### 代替ライブラリ

- **xlrd**: 旧形式 .xls 用
- **pandas**: データ分析・集計が必要な場合
- **pyexcel**: 複数形式対応

## Excel 形式の違い

| 形式 | 拡張子 | 推奨ツール |
|------|-------|-----------|
| Excel 2007+ | .xlsx | **openpyxl** |
| Excel 97-2003 | .xls | xlrd |
| CSV | .csv | Read tool |
| TSV | .tsv | Read tool |
| OpenDocument | .ods | pyexcel |

## ライセンス

このスキルは個人プロジェクト用です。

## バージョン

- **v1.0.0** (2026-01-06)
  - 初期リリース
  - 基本的な Excel 読み込み機能
  - Markdown テーブル変換
  - 複数シート対応
  - シート指定・行数制限機能
  - WSL環境での動作確認済み
