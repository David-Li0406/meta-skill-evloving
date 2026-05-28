---
name: xlsx
description: "全面的試算表建立、編輯和分析功能,支援公式、格式化、資料分析和視覺化。當 Claude 需要處理試算表(.xlsx、.xlsm、.csv、.tsv 等)進行:(1) 建立包含公式和格式的新試算表,(2) 讀取或分析資料,(3) 修改現有試算表同時保留公式,(4) 試算表中的資料分析和視覺化,或 (5) 重新計算公式時"
license: Proprietary. LICENSE.txt has complete terms
---

# 輸出要求

## 所有 Excel 檔案

### 零公式錯誤
- 每個 Excel 模型必須以零公式錯誤交付(#REF!、#DIV/0!、#VALUE!、#N/A、#NAME?)

### 保留現有範本(更新範本時)
- 修改檔案時,研究並精確匹配現有格式、樣式和慣例
- 切勿對已有既定模式的檔案強加標準化格式
- 現有範本慣例始終優先於這些指南

## 財務模型

### 色彩編碼標準
除非使用者或現有範本另有說明

#### 行業標準色彩慣例
- **藍色文字(RGB: 0,0,255)**:硬編碼輸入,以及使用者將為情境更改的數字
- **黑色文字(RGB: 0,0,0)**:所有公式和計算
- **綠色文字(RGB: 0,128,0)**:從同一工作簿內其他工作表提取的連結
- **紅色文字(RGB: 255,0,0)**:連結到其他檔案的外部連結
- **黃色背景(RGB: 255,255,0)**:需要注意的關鍵假設或需要更新的儲存格

### 數字格式標準

#### 必要格式規則
- **年份**:格式化為文字字串(例如,"2024" 而非 "2,024")
- **貨幣**:使用 $#,##0 格式;始終在標題中指定單位("Revenue ($mm)")
- **零值**:使用數字格式使所有零顯示為 "-",包括百分比(例如,"$#,##0;($#,##0);-")
- **百分比**:預設為 0.0% 格式(一位小數)
- **倍數**:估值倍數格式化為 0.0x(EV/EBITDA、P/E)
- **負數**:使用括號 (123) 而非減號 -123

### 公式建構規則

#### 假設放置
- 將所有假設(成長率、利潤率、倍數等)放在單獨的假設儲存格中
- 在公式中使用儲存格引用而非硬編碼值
- 範例:使用 =B5*(1+$B$6) 而非 =B5*1.05

#### 公式錯誤預防
- 驗證所有儲存格引用是否正確
- 檢查範圍中的差一錯誤
- 確保所有預測期間的公式一致
- 使用邊界情況測試(零值、負數)
- 驗證沒有非預期的循環引用

#### 硬編碼的文件要求
- 在旁邊的儲存格中註解(如果在表格末端)。格式:"Source: [系統/文件], [日期], [具體引用], [URL(如適用)]"
- 範例:
  - "Source: Company 10-K, FY2024, Page 45, Revenue Note, [SEC EDGAR URL]"
  - "Source: Company 10-Q, Q2 2025, Exhibit 99.1, [SEC EDGAR URL]"
  - "Source: Bloomberg Terminal, 8/15/2025, AAPL US Equity"
  - "Source: FactSet, 8/20/2025, Consensus Estimates Screen"

# XLSX 建立、編輯和分析

## 概述

使用者可能要求您建立、編輯或分析 .xlsx 檔案的內容。您有不同的工具和工作流程可用於不同的任務。

## 重要要求

**公式重新計算需要 LibreOffice**:您可以假設已安裝 LibreOffice,用於使用 `recalc.py` 腳本重新計算公式值。該腳本會在首次執行時自動設定 LibreOffice

## 讀取和分析資料

### 使用 pandas 進行資料分析
對於資料分析、視覺化和基本操作,使用 **pandas**,它提供強大的資料操作能力:

```python
import pandas as pd

# 讀取 Excel
df = pd.read_excel('file.xlsx')  # 預設:第一個工作表
all_sheets = pd.read_excel('file.xlsx', sheet_name=None)  # 所有工作表作為字典

# 分析
df.head()      # 預覽資料
df.info()      # 欄位資訊
df.describe()  # 統計資料

# 寫入 Excel
df.to_excel('output.xlsx', index=False)
```

## Excel 檔案工作流程

## 關鍵:使用公式,而非硬編碼值

**始終使用 Excel 公式,而非在 Python 中計算值後硬編碼。** 這確保試算表保持動態且可更新。

### ❌ 錯誤 - 硬編碼計算值
```python
# 不好:在 Python 中計算並硬編碼結果
total = df['Sales'].sum()
sheet['B10'] = total  # 硬編碼 5000

# 不好:在 Python 中計算成長率
growth = (df.iloc[-1]['Revenue'] - df.iloc[0]['Revenue']) / df.iloc[0]['Revenue']
sheet['C5'] = growth  # 硬編碼 0.15

# 不好:Python 計算平均值
avg = sum(values) / len(values)
sheet['D20'] = avg  # 硬編碼 42.5
```

### ✅ 正確 - 使用 Excel 公式
```python
# 好:讓 Excel 計算總和
sheet['B10'] = '=SUM(B2:B9)'

# 好:成長率作為 Excel 公式
sheet['C5'] = '=(C4-C2)/C2'

# 好:使用 Excel 函數計算平均值
sheet['D20'] = '=AVERAGE(D2:D19)'
```

這適用於所有計算 - 總計、百分比、比率、差異等。試算表應該能夠在來源資料變更時重新計算。

## 常見工作流程
1. **選擇工具**:pandas 用於資料,openpyxl 用於公式/格式化
2. **建立/載入**:建立新工作簿或載入現有檔案
3. **修改**:新增/編輯資料、公式和格式
4. **儲存**:寫入檔案
5. **重新計算公式(如果使用公式則為必要)**:使用 recalc.py 腳本
   ```bash
   python recalc.py output.xlsx
   ```
6. **驗證並修復任何錯誤**:
   - 腳本返回包含錯誤詳情的 JSON
   - 如果 `status` 為 `errors_found`,檢查 `error_summary` 以獲取特定錯誤類型和位置
   - 修復識別出的錯誤並再次重新計算
   - 常見要修復的錯誤:
     - `#REF!`:無效的儲存格引用
     - `#DIV/0!`:除以零
     - `#VALUE!`:公式中的資料類型錯誤
     - `#NAME?`:無法識別的公式名稱

### 建立新 Excel 檔案

```python
# 使用 openpyxl 處理公式和格式化
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment

wb = Workbook()
sheet = wb.active

# 新增資料
sheet['A1'] = 'Hello'
sheet['B1'] = 'World'
sheet.append(['Row', 'of', 'data'])

# 新增公式
sheet['B2'] = '=SUM(A1:A10)'

# 格式化
sheet['A1'].font = Font(bold=True, color='FF0000')
sheet['A1'].fill = PatternFill('solid', start_color='FFFF00')
sheet['A1'].alignment = Alignment(horizontal='center')

# 欄寬
sheet.column_dimensions['A'].width = 20

wb.save('output.xlsx')
```

### 編輯現有 Excel 檔案

```python
# 使用 openpyxl 保留公式和格式
from openpyxl import load_workbook

# 載入現有檔案
wb = load_workbook('existing.xlsx')
sheet = wb.active  # 或 wb['SheetName'] 指定特定工作表

# 處理多個工作表
for sheet_name in wb.sheetnames:
    sheet = wb[sheet_name]
    print(f"Sheet: {sheet_name}")

# 修改儲存格
sheet['A1'] = 'New Value'
sheet.insert_rows(2)  # 在位置 2 插入列
sheet.delete_cols(3)  # 刪除第 3 欄

# 新增工作表
new_sheet = wb.create_sheet('NewSheet')
new_sheet['A1'] = 'Data'

wb.save('modified.xlsx')
```

## 重新計算公式

openpyxl 建立或修改的 Excel 檔案包含作為字串的公式,但不包含計算值。使用提供的 `recalc.py` 腳本重新計算公式:

```bash
python recalc.py <excel_file> [timeout_seconds]
```

範例:
```bash
python recalc.py output.xlsx 30
```

該腳本:
- 在首次執行時自動設定 LibreOffice 巨集
- 重新計算所有工作表中的所有公式
- 掃描所有儲存格以查找 Excel 錯誤(#REF!、#DIV/0! 等)
- 返回包含詳細錯誤位置和計數的 JSON
- 在 Linux 和 macOS 上都可使用

## 公式驗證清單

確保公式正確運作的快速檢查:

### 基本驗證
- [ ] **測試 2-3 個樣本引用**:在建構完整模型之前驗證它們提取正確的值
- [ ] **欄位對應**:確認 Excel 欄位匹配(例如,第 64 欄 = BL,而非 BK)
- [ ] **列偏移**:記住 Excel 列是從 1 開始索引的(DataFrame 第 5 列 = Excel 第 6 列)

### 常見陷阱
- [ ] **NaN 處理**:使用 `pd.notna()` 檢查空值
- [ ] **最右側欄位**:FY 資料通常在第 50+ 欄
- [ ] **多個匹配**:搜尋所有出現,而非僅第一個
- [ ] **除以零**:在公式中使用 `/` 之前檢查分母(#DIV/0!)
- [ ] **錯誤引用**:驗證所有儲存格引用指向預期的儲存格(#REF!)
- [ ] **跨工作表引用**:使用正確格式(Sheet1!A1)連結工作表

### 公式測試策略
- [ ] **從小處開始**:在廣泛應用之前在 2-3 個儲存格上測試公式
- [ ] **驗證依賴關係**:檢查公式中引用的所有儲存格是否存在
- [ ] **測試邊界情況**:包括零值、負值和非常大的值

### 解讀 recalc.py 輸出
腳本返回包含錯誤詳情的 JSON:
```json
{
  "status": "success",           // 或 "errors_found"
  "total_errors": 0,              // 錯誤總數
  "total_formulas": 42,           // 檔案中的公式數量
  "error_summary": {              // 僅在發現錯誤時出現
    "#REF!": {
      "count": 2,
      "locations": ["Sheet1!B5", "Sheet1!C10"]
    }
  }
}
```

## 最佳實踐

### 函式庫選擇
- **pandas**:最適合資料分析、批次操作和簡單資料匯出
- **openpyxl**:最適合複雜格式化、公式和 Excel 特定功能

### 使用 openpyxl
- 儲存格索引從 1 開始(row=1, column=1 指的是儲存格 A1)
- 使用 `data_only=True` 讀取計算值:`load_workbook('file.xlsx', data_only=True)`
- **警告**:如果使用 `data_only=True` 開啟並儲存,公式會被值替換並永久遺失
- 對於大型檔案:使用 `read_only=True` 進行讀取或 `write_only=True` 進行寫入
- 公式被保留但不被計算 - 使用 recalc.py 更新值

### 使用 pandas
- 指定資料類型以避免推斷問題:`pd.read_excel('file.xlsx', dtype={'id': str})`
- 對於大型檔案,讀取特定欄位:`pd.read_excel('file.xlsx', usecols=['A', 'C', 'E'])`
- 正確處理日期:`pd.read_excel('file.xlsx', parse_dates=['date_column'])`

## 程式碼樣式指南
**重要**:為 Excel 操作產生 Python 程式碼時:
- 編寫簡潔的 Python 程式碼,不需要不必要的註解
- 避免冗長的變數名稱和多餘的操作
- 避免不必要的列印語句

**對於 Excel 檔案本身**:
- 為複雜公式或重要假設的儲存格新增註解
- 記錄硬編碼值的資料來源
- 包含關鍵計算和模型部分的說明