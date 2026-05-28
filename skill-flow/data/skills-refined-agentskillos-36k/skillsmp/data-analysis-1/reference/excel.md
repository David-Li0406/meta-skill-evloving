# Excel操作ガイド

## 目次
- 読み込み
- 書き込み
- 書式設定
- グラフ作成
- ピボットテーブル
- 数式操作

## 読み込み

### pandas（シンプル）

```python
import pandas as pd

# 基本読み込み
df = pd.read_excel("data.xlsx")

# シート指定
df = pd.read_excel("data.xlsx", sheet_name="Sheet1")

# 複数シート
dfs = pd.read_excel("data.xlsx", sheet_name=None)  # dict of DataFrames

# オプション指定
df = pd.read_excel(
    "data.xlsx",
    sheet_name="Sheet1",
    header=0,           # ヘッダー行
    skiprows=2,         # スキップ行数
    usecols="A:D",      # 使用する列
    dtype={"ID": str},  # 型指定
    na_values=["N/A"]   # NA値
)
```

### openpyxl（詳細制御）

```python
from openpyxl import load_workbook

def read_excel_detailed(path: str) -> dict:
    """詳細な読み込み"""
    wb = load_workbook(path, data_only=True)
    
    result = {}
    for sheet_name in wb.sheetnames:
        ws = wb[sheet_name]
        
        data = []
        for row in ws.iter_rows(values_only=True):
            data.append(list(row))
        
        result[sheet_name] = {
            "data": data,
            "dimensions": ws.dimensions,
            "max_row": ws.max_row,
            "max_col": ws.max_column
        }
    
    return result
```

## 書き込み

### pandas

```python
import pandas as pd

# 基本書き込み
df.to_excel("output.xlsx", index=False)

# 複数シート
with pd.ExcelWriter("output.xlsx", engine="openpyxl") as writer:
    df1.to_excel(writer, sheet_name="Data", index=False)
    df2.to_excel(writer, sheet_name="Summary", index=False)
```

### openpyxl

```python
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows

def write_excel(df: pd.DataFrame, path: str, sheet_name: str = "Sheet1"):
    """DataFrameをExcelに書き込み"""
    wb = Workbook()
    ws = wb.active
    ws.title = sheet_name
    
    for r in dataframe_to_rows(df, index=False, header=True):
        ws.append(r)
    
    wb.save(path)
```

## 書式設定

```python
from openpyxl import Workbook
from openpyxl.styles import (
    Font, Fill, PatternFill, Border, Side,
    Alignment, NamedStyle
)
from openpyxl.utils import get_column_letter

def format_excel(path: str):
    """書式設定を適用"""
    wb = Workbook()
    ws = wb.active
    
    # ヘッダースタイル
    header_font = Font(bold=True, color="FFFFFF")
    header_fill = PatternFill(start_color="4472C4", end_color="4472C4", fill_type="solid")
    header_alignment = Alignment(horizontal="center", vertical="center")
    
    # 罫線
    thin_border = Border(
        left=Side(style="thin"),
        right=Side(style="thin"),
        top=Side(style="thin"),
        bottom=Side(style="thin")
    )
    
    # サンプルデータ
    headers = ["ID", "名前", "金額", "日付"]
    data = [
        [1, "田中", 10000, "2025-01-15"],
        [2, "佐藤", 20000, "2025-01-16"],
    ]
    
    # ヘッダー書き込み
    for col, header in enumerate(headers, 1):
        cell = ws.cell(row=1, column=col, value=header)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = header_alignment
        cell.border = thin_border
    
    # データ書き込み
    for row_idx, row_data in enumerate(data, 2):
        for col_idx, value in enumerate(row_data, 1):
            cell = ws.cell(row=row_idx, column=col_idx, value=value)
            cell.border = thin_border
            
            # 数値は右寄せ
            if isinstance(value, (int, float)):
                cell.alignment = Alignment(horizontal="right")
                # 金額は通貨形式
                if col_idx == 3:
                    cell.number_format = '¥#,##0'
    
    # 列幅自動調整
    for col in range(1, len(headers) + 1):
        ws.column_dimensions[get_column_letter(col)].width = 15
    
    wb.save(path)
```

## グラフ作成

```python
from openpyxl import Workbook
from openpyxl.chart import BarChart, LineChart, PieChart, Reference

def create_chart(path: str):
    """グラフを作成"""
    wb = Workbook()
    ws = wb.active
    
    # サンプルデータ
    data = [
        ["月", "売上", "利益"],
        ["1月", 100, 30],
        ["2月", 120, 40],
        ["3月", 150, 50],
        ["4月", 130, 35],
    ]
    
    for row in data:
        ws.append(row)
    
    # 棒グラフ
    chart = BarChart()
    chart.title = "月次売上"
    chart.x_axis.title = "月"
    chart.y_axis.title = "金額"
    
    data_ref = Reference(ws, min_col=2, max_col=3, min_row=1, max_row=5)
    categories = Reference(ws, min_col=1, min_row=2, max_row=5)
    
    chart.add_data(data_ref, titles_from_data=True)
    chart.set_categories(categories)
    chart.shape = 4  # グラフの種類
    
    ws.add_chart(chart, "E2")
    
    # 折れ線グラフ
    line_chart = LineChart()
    line_chart.title = "売上推移"
    line_chart.add_data(data_ref, titles_from_data=True)
    line_chart.set_categories(categories)
    ws.add_chart(line_chart, "E17")
    
    wb.save(path)
```

## 数式操作

```python
from openpyxl import Workbook

def add_formulas(path: str):
    """数式を追加"""
    wb = Workbook()
    ws = wb.active
    
    # データ
    ws["A1"] = "項目"
    ws["B1"] = "金額"
    ws["A2"] = "売上"
    ws["B2"] = 100000
    ws["A3"] = "経費"
    ws["B3"] = 30000
    ws["A4"] = "利益"
    
    # 数式
    ws["B4"] = "=B2-B3"
    
    # SUM
    ws["A6"] = "合計"
    ws["B6"] = "=SUM(B2:B3)"
    
    # VLOOKUP例
    ws["D1"] = "検索値"
    ws["E1"] = "=VLOOKUP(D1,A2:B4,2,FALSE)"
    
    wb.save(path)
```

## 大容量ファイル処理

```python
from openpyxl import load_workbook

def read_large_excel(path: str, chunk_size: int = 1000):
    """大容量Excelを分割読み込み"""
    wb = load_workbook(path, read_only=True)
    ws = wb.active
    
    chunk = []
    for row in ws.iter_rows(values_only=True):
        chunk.append(row)
        
        if len(chunk) >= chunk_size:
            yield chunk
            chunk = []
    
    if chunk:
        yield chunk
    
    wb.close()
```

```python
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows

def write_large_excel(dataframes: list, path: str):
    """大容量データを効率的に書き込み"""
    wb = Workbook(write_only=True)
    
    for i, df in enumerate(dataframes):
        ws = wb.create_sheet(f"Sheet{i+1}")
        
        for r in dataframe_to_rows(df, index=False, header=True):
            ws.append(r)
    
    wb.save(path)
```
