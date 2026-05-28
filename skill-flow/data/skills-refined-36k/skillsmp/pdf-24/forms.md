**關鍵：您必須按順序完成這些步驟。不要跳過直接編寫程式碼。**

如果您需要填寫 PDF 表單，首先檢查 PDF 是否有可填寫的表單欄位。從此檔案的目錄執行此腳本：
`python scripts/check_fillable_fields <file.pdf>`，根據結果前往「可填寫欄位」或「不可填寫欄位」部分並遵循相應說明。

# 可填寫欄位
如果 PDF 有可填寫的表單欄位：
- 從此檔案的目錄執行此腳本：`python scripts/extract_form_field_info.py <input.pdf> <field_info.json>`。它會建立一個 JSON 檔案，包含此格式的欄位清單：
```
[
  {
    "field_id": (欄位的唯一 ID),
    "page": (頁碼，從 1 開始),
    "rect": ([左, 下, 右, 上] 邊界框，PDF 座標，y=0 是頁面底部),
    "type": ("text"、"checkbox"、"radio_group" 或 "choice"),
  },
  // 核取方塊有 "checked_value" 和 "unchecked_value" 屬性：
  {
    "field_id": (欄位的唯一 ID),
    "page": (頁碼，從 1 開始),
    "type": "checkbox",
    "checked_value": (將欄位設定為此值以勾選核取方塊),
    "unchecked_value": (將欄位設定為此值以取消勾選核取方塊),
  },
  // 單選按鈕群組有一個 "radio_options" 清單，包含可能的選項。
  {
    "field_id": (欄位的唯一 ID),
    "page": (頁碼，從 1 開始),
    "type": "radio_group",
    "radio_options": [
      {
        "value": (將欄位設定為此值以選擇此單選選項),
        "rect": (此選項的單選按鈕邊界框)
      },
      // 其他單選選項
    ]
  },
  // 多選欄位有一個 "choice_options" 清單，包含可能的選項：
  {
    "field_id": (欄位的唯一 ID),
    "page": (頁碼，從 1 開始),
    "type": "choice",
    "choice_options": [
      {
        "value": (將欄位設定為此值以選擇此選項),
        "text": (選項的顯示文字)
      },
      // 其他選擇選項
    ],
  }
]
```
- 使用此腳本將 PDF 轉換為 PNG（每頁一張圖片）（從此檔案的目錄執行）：
`python scripts/convert_pdf_to_images.py <file.pdf> <output_directory>`
然後分析圖片以確定每個表單欄位的用途（確保將邊界框 PDF 座標轉換為圖片座標）。
- 建立一個 `field_values.json` 檔案，使用此格式包含每個欄位要輸入的值：
```
[
  {
    "field_id": "last_name", // 必須與 `extract_form_field_info.py` 的 field_id 相符
    "description": "使用者的姓氏",
    "page": 1, // 必須與 field_info.json 中的 "page" 值相符
    "value": "Simpson"
  },
  {
    "field_id": "Checkbox12",
    "description": "如果使用者年滿 18 歲則勾選的核取方塊",
    "page": 1,
    "value": "/On" // 如果這是核取方塊，使用其 "checked_value" 值來勾選。如果是單選按鈕群組，使用 "radio_options" 中的其中一個 "value" 值。
  },
  // 更多欄位
]
```
- 從此檔案的目錄執行 `fill_fillable_fields.py` 腳本以建立已填寫的 PDF：
`python scripts/fill_fillable_fields.py <input pdf> <field_values.json> <output pdf>`
此腳本會驗證您提供的欄位 ID 和值是否有效；如果印出錯誤訊息，請更正相應的欄位並重試。

# 不可填寫欄位
如果 PDF 沒有可填寫的表單欄位，您需要視覺化地確定資料應該新增的位置並建立文字註解。請「完全」遵循以下步驟。您必須執行所有這些步驟以確保表單正確填寫。每個步驟的詳細資訊如下。
- 將 PDF 轉換為 PNG 圖片並確定欄位邊界框。
- 建立包含欄位資訊和顯示邊界框的驗證圖片的 JSON 檔案。
- 驗證邊界框。
- 使用邊界框填寫表單。

## 步驟 1：視覺分析（必要）
- 將 PDF 轉換為 PNG 圖片。從此檔案的目錄執行此腳本：
`python scripts/convert_pdf_to_images.py <file.pdf> <output_directory>`
腳本會為 PDF 中的每一頁建立一張 PNG 圖片。
- 仔細檢查每張 PNG 圖片並識別所有表單欄位和使用者應該輸入資料的區域。對於使用者應該輸入文字的每個表單欄位，確定表單欄位標籤和使用者應該輸入文字的區域的邊界框。標籤和輸入邊界框必須不相交；文字輸入框應該只包含應該輸入資料的區域。通常這個區域會緊鄰標籤的旁邊、上方或下方。輸入邊界框必須足夠高和寬以容納其文字。

以下是您可能會看到的一些表單結構範例：

*標籤在框內*
```
┌────────────────────────┐
│ 姓名:                   │
└────────────────────────┘
```
輸入區域應該在「姓名」標籤的右側並延伸到框的邊緣。

*標籤在線條前*
```
Email: _______________________
```
輸入區域應該在線條上方並包含其整個寬度。

*標籤在線條下*
```
_________________________
姓名
```
輸入區域應該在線條上方並包含線條的整個寬度。這在簽名和日期欄位中很常見。

*標籤在線條上*
```
請輸入任何特殊要求：
________________________________________________
```
輸入區域應該從標籤底部延伸到線條，並應包含線條的整個寬度。

*核取方塊*
```
您是美國公民嗎？是 □  否 □
```
對於核取方塊：
- 尋找小方框（□）- 這些是要定位的實際核取方塊。它們可能在標籤的左側或右側。
- 區分標籤文字（「是」、「否」）和可點擊的核取方塊方框。
- 輸入邊界框應該只覆蓋小方框，而不是文字標籤。

### 步驟 2：建立 fields.json 和驗證圖片（必要）
- 建立一個名為 `fields.json` 的檔案，包含此格式的表單欄位和邊界框資訊：
```
{
  "pages": [
    {
      "page_number": 1,
      "image_width": (第一頁圖片寬度，像素),
      "image_height": (第一頁圖片高度，像素),
    },
    {
      "page_number": 2,
      "image_width": (第二頁圖片寬度，像素),
      "image_height": (第二頁圖片高度，像素),
    }
    // 其他頁面
  ],
  "form_fields": [
    // 文字欄位範例。
    {
      "page_number": 1,
      "description": "使用者的姓氏應該在這裡輸入",
      // 邊界框為 [左, 上, 右, 下]。標籤和文字輸入的邊界框不應重疊。
      "field_label": "姓氏",
      "label_bounding_box": [30, 125, 95, 142],
      "entry_bounding_box": [100, 125, 280, 142],
      "entry_text": {
        "text": "Johnson", // 此文字將作為註解新增到 entry_bounding_box 位置
        "font_size": 14, // 選用，預設為 14
        "font_color": "000000", // 選用，RRGGBB 格式，預設為 000000（黑色）
      }
    },
    // 核取方塊範例。輸入邊界框要定位方框，不是文字
    {
      "page_number": 2,
      "description": "如果使用者年滿 18 歲則應勾選的核取方塊",
      "entry_bounding_box": [140, 525, 155, 540],  // 覆蓋核取方塊方框的小框
      "field_label": "是",
      "label_bounding_box": [100, 525, 132, 540],  // 包含「是」文字的框
      // 使用 "X" 勾選核取方塊。
      "entry_text": {
        "text": "X",
      }
    }
    // 其他表單欄位條目
  ]
}
```

從此檔案的目錄為每一頁執行此腳本以建立驗證圖片：
`python scripts/create_validation_image.py <page_number> <path_to_fields.json> <input_image_path> <output_image_path>

驗證圖片會在應該輸入文字的地方有紅色矩形，在標籤文字上有藍色矩形。

### 步驟 3：驗證邊界框（必要）
#### 自動相交檢查
- 透過使用 `check_bounding_boxes.py` 腳本檢查 fields.json 檔案，驗證沒有邊界框相交且輸入邊界框足夠高（從此檔案的目錄執行）：
`python scripts/check_bounding_boxes.py <JSON file>`

如果有錯誤，重新分析相關欄位，調整邊界框，並反覆修正直到沒有剩餘錯誤。記住：標籤（藍色）邊界框應該包含文字標籤，輸入（紅色）框不應該包含。

#### 手動圖片檢查
**關鍵：不要在視覺檢查驗證圖片之前繼續**
- 紅色矩形必須只覆蓋輸入區域
- 紅色矩形必須不包含任何文字
- 藍色矩形應該包含標籤文字
- 對於核取方塊：
  - 紅色矩形必須置中在核取方塊方框上
  - 藍色矩形應該覆蓋核取方塊的文字標籤

- 如果任何矩形看起來不對，修正 fields.json，重新產生驗證圖片，然後再次驗證。重複此過程直到邊界框完全準確。


### 步驟 4：將註解新增到 PDF
從此檔案的目錄執行此腳本，使用 fields.json 中的資訊建立已填寫的 PDF：
`python scripts/fill_pdf_form_with_annotations.py <input_pdf_path> <path_to_fields.json> <output_pdf_path>
