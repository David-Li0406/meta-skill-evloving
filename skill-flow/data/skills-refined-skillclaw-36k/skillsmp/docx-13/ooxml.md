# Office Open XML 技術參考

**重要：開始前請閱讀整份文件。** 本文件涵蓋：
- [技術指南](#技術指南) - 結構描述合規規則和驗證要求
- [文件內容模式](#文件內容模式) - 標題、清單、表格、格式等的 XML 模式
- [Document Library（Python）](#document-library-python) - 建議用於 OOXML 操作的方法，具有自動基礎設施設定
- [追蹤修訂（紅線標記）](#追蹤修訂紅線標記) - 實作追蹤修訂的 XML 模式

## 技術指南

### 結構描述合規
- **`<w:pPr>` 中的元素順序**：`<w:pStyle>`、`<w:numPr>`、`<w:spacing>`、`<w:ind>`、`<w:jc>`
- **空白字元**：在有前後空白的 `<w:t>` 元素上新增 `xml:space='preserve'`
- **Unicode**：在 ASCII 內容中跳脫字元：`"` 變成 `&#8220;`
  - **字元編碼參考**：彎引號 `""` 變成 `&#8220;&#8221;`，撇號 `'` 變成 `&#8217;`，破折號 `—` 變成 `&#8212;`
- **追蹤修訂**：在 `<w:r>` 元素外部使用 `<w:del>` 和 `<w:ins>` 標籤，搭配 `w:author="Claude"`
  - **關鍵**：`<w:ins>` 以 `</w:ins>` 關閉，`<w:del>` 以 `</w:del>` 關閉 - 絕不混用
  - **RSID 必須是 8 位十六進位**：使用如 `00AB1234` 的值（只有 0-9、A-F 字元）
  - **trackRevisions 位置**：在 settings.xml 中的 `<w:proofState>` 之後新增 `<w:trackRevisions/>`
- **圖片**：新增至 `word/media/`，在 `document.xml` 中參照，設定尺寸以防止溢出

## 文件內容模式

### 基本結構
```xml
<w:p>
  <w:r><w:t>文字內容</w:t></w:r>
</w:p>
```

### 標題和樣式
```xml
<w:p>
  <w:pPr>
    <w:pStyle w:val="Title"/>
    <w:jc w:val="center"/>
  </w:pPr>
  <w:r><w:t>文件標題</w:t></w:r>
</w:p>

<w:p>
  <w:pPr><w:pStyle w:val="Heading2"/></w:pPr>
  <w:r><w:t>章節標題</w:t></w:r>
</w:p>
```

### 文字格式
```xml
<!-- 粗體 -->
<w:r><w:rPr><w:b/><w:bCs/></w:rPr><w:t>粗體</w:t></w:r>
<!-- 斜體 -->
<w:r><w:rPr><w:i/><w:iCs/></w:rPr><w:t>斜體</w:t></w:r>
<!-- 底線 -->
<w:r><w:rPr><w:u w:val="single"/></w:rPr><w:t>底線</w:t></w:r>
<!-- 螢光標記 -->
<w:r><w:rPr><w:highlight w:val="yellow"/></w:rPr><w:t>螢光標記</w:t></w:r>
```

### 清單
```xml
<!-- 編號清單 -->
<w:p>
  <w:pPr>
    <w:pStyle w:val="ListParagraph"/>
    <w:numPr><w:ilvl w:val="0"/><w:numId w:val="1"/></w:numPr>
    <w:spacing w:before="240"/>
  </w:pPr>
  <w:r><w:t>第一項</w:t></w:r>
</w:p>

<!-- 重新從 1 開始的編號清單 - 使用不同的 numId -->
<w:p>
  <w:pPr>
    <w:pStyle w:val="ListParagraph"/>
    <w:numPr><w:ilvl w:val="0"/><w:numId w:val="2"/></w:numPr>
    <w:spacing w:before="240"/>
  </w:pPr>
  <w:r><w:t>新清單第 1 項</w:t></w:r>
</w:p>

<!-- 項目符號清單（第 2 層級） -->
<w:p>
  <w:pPr>
    <w:pStyle w:val="ListParagraph"/>
    <w:numPr><w:ilvl w:val="1"/><w:numId w:val="1"/></w:numPr>
    <w:spacing w:before="240"/>
    <w:ind w:left="900"/>
  </w:pPr>
  <w:r><w:t>項目符號項目</w:t></w:r>
</w:p>
```

### 表格
```xml
<w:tbl>
  <w:tblPr>
    <w:tblStyle w:val="TableGrid"/>
    <w:tblW w:w="0" w:type="auto"/>
  </w:tblPr>
  <w:tblGrid>
    <w:gridCol w:w="4675"/><w:gridCol w:w="4675"/>
  </w:tblGrid>
  <w:tr>
    <w:tc>
      <w:tcPr><w:tcW w:w="4675" w:type="dxa"/></w:tcPr>
      <w:p><w:r><w:t>儲存格 1</w:t></w:r></w:p>
    </w:tc>
    <w:tc>
      <w:tcPr><w:tcW w:w="4675" w:type="dxa"/></w:tcPr>
      <w:p><w:r><w:t>儲存格 2</w:t></w:r></w:p>
    </w:tc>
  </w:tr>
</w:tbl>
```

### 版面配置
```xml
<!-- 新章節前的分頁符號（常見模式） -->
<w:p>
  <w:r>
    <w:br w:type="page"/>
  </w:r>
</w:p>
<w:p>
  <w:pPr>
    <w:pStyle w:val="Heading1"/>
  </w:pPr>
  <w:r>
    <w:t>新章節標題</w:t>
  </w:r>
</w:p>

<!-- 置中段落 -->
<w:p>
  <w:pPr>
    <w:spacing w:before="240" w:after="0"/>
    <w:jc w:val="center"/>
  </w:pPr>
  <w:r><w:t>置中文字</w:t></w:r>
</w:p>

<!-- 字型變更 - 段落層級（套用至所有 run） -->
<w:p>
  <w:pPr>
    <w:rPr><w:rFonts w:ascii="Courier New" w:hAnsi="Courier New"/></w:rPr>
  </w:pPr>
  <w:r><w:t>等寬文字</w:t></w:r>
</w:p>

<!-- 字型變更 - run 層級（僅限此文字） -->
<w:p>
  <w:r>
    <w:rPr><w:rFonts w:ascii="Courier New" w:hAnsi="Courier New"/></w:rPr>
    <w:t>此文字為 Courier New</w:t>
  </w:r>
  <w:r><w:t> 而此文字使用預設字型</w:t></w:r>
</w:p>
```

## 檔案更新

新增內容時，更新這些檔案：

**`word/_rels/document.xml.rels`：**
```xml
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/numbering" Target="numbering.xml"/>
<Relationship Id="rId5" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/image1.png"/>
```

**`[Content_Types].xml`：**
```xml
<Default Extension="png" ContentType="image/png"/>
<Override PartName="/word/numbering.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.numbering+xml"/>
```

### 圖片
**關鍵**：計算尺寸以防止頁面溢出並維持長寬比。

```xml
<!-- 最小必要結構 -->
<w:p>
  <w:r>
    <w:drawing>
      <wp:inline>
        <wp:extent cx="2743200" cy="1828800"/>
        <wp:docPr id="1" name="Picture 1"/>
        <a:graphic xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">
          <a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">
            <pic:pic xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">
              <pic:nvPicPr>
                <pic:cNvPr id="0" name="image1.png"/>
                <pic:cNvPicPr/>
              </pic:nvPicPr>
              <pic:blipFill>
                <a:blip r:embed="rId5"/>
                <!-- 新增以保持長寬比的延伸填充 -->
                <a:stretch>
                  <a:fillRect/>
                </a:stretch>
              </pic:blipFill>
              <pic:spPr>
                <a:xfrm>
                  <a:ext cx="2743200" cy="1828800"/>
                </a:xfrm>
                <a:prstGeom prst="rect"/>
              </pic:spPr>
            </pic:pic>
          </a:graphicData>
        </a:graphic>
      </wp:inline>
    </w:drawing>
  </w:r>
</w:p>
```

### 連結（超連結）

**重要**：所有超連結（內部和外部）都需要在 styles.xml 中定義 Hyperlink 樣式。沒有此樣式，連結會看起來像一般文字而非藍色底線的可點擊連結。

**外部連結：**
```xml
<!-- 在 document.xml 中 -->
<w:hyperlink r:id="rId5">
  <w:r>
    <w:rPr><w:rStyle w:val="Hyperlink"/></w:rPr>
    <w:t>連結文字</w:t>
  </w:r>
</w:hyperlink>

<!-- 在 word/_rels/document.xml.rels 中 -->
<Relationship Id="rId5" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink"
              Target="https://www.example.com/" TargetMode="External"/>
```

**內部連結：**

```xml
<!-- 連結至書籤 -->
<w:hyperlink w:anchor="myBookmark">
  <w:r>
    <w:rPr><w:rStyle w:val="Hyperlink"/></w:rPr>
    <w:t>連結文字</w:t>
  </w:r>
</w:hyperlink>

<!-- 書籤目標 -->
<w:bookmarkStart w:id="0" w:name="myBookmark"/>
<w:r><w:t>目標內容</w:t></w:r>
<w:bookmarkEnd w:id="0"/>
```

**Hyperlink 樣式（styles.xml 中必要）：**
```xml
<w:style w:type="character" w:styleId="Hyperlink">
  <w:name w:val="Hyperlink"/>
  <w:basedOn w:val="DefaultParagraphFont"/>
  <w:uiPriority w:val="99"/>
  <w:unhideWhenUsed/>
  <w:rPr>
    <w:color w:val="467886" w:themeColor="hyperlink"/>
    <w:u w:val="single"/>
  </w:rPr>
</w:style>
```

## Document Library（Python）

使用 `scripts/document.py` 中的 Document 類別來處理所有追蹤修訂和註解。它會自動處理基礎設施設定（people.xml、RSID、settings.xml、註解檔案、關聯、內容類型）。只有在函式庫不支援的複雜情況下才使用直接 XML 操作。

**處理 Unicode 和實體：**
- **搜尋**：實體表示法和 Unicode 字元都可以使用 - `contains="&#8220;Company"` 和 `contains="\u201cCompany"` 會找到相同的文字
- **替換**：使用實體（`&#8220;`）或 Unicode（`\u201c`）都可以 - 兩者都會根據檔案編碼適當轉換（ascii → 實體，utf-8 → Unicode）

### 初始化

**找到 docx skill 根目錄**（包含 `scripts/` 和 `ooxml/` 的目錄）：
```bash
# 搜尋 document.py 以找到 skill 根目錄
# 注意：這裡的 /mnt/skills 是範例；請檢查您的環境以確定實際位置
find /mnt/skills -name "document.py" -path "*/docx/scripts/*" 2>/dev/null | head -1
# 範例輸出：/mnt/skills/docx/scripts/document.py
# Skill 根目錄是：/mnt/skills/docx
```

**使用設定為 docx skill 根目錄的 PYTHONPATH 執行您的腳本**：
```bash
PYTHONPATH=/mnt/skills/docx python your_script.py
```

**在您的腳本中**，從 skill 根目錄匯入：
```python
from scripts.document import Document, DocxXMLEditor

# 基本初始化（自動建立暫存副本並設定基礎設施）
doc = Document('unpacked')

# 自訂作者和縮寫
doc = Document('unpacked', author="John Doe", initials="JD")

# 啟用追蹤修訂模式
doc = Document('unpacked', track_revisions=True)

# 指定自訂 RSID（如未提供則自動產生）
doc = Document('unpacked', rsid="07DC5ECB")
```

### 建立追蹤修訂

**關鍵**：只標記實際變更的文字。將所有未變更的文字保留在 `<w:del>`/`<w:ins>` 標籤之外。標記未變更的文字會使編輯看起來不專業且難以審查。

**屬性處理**：Document 類別會自動將屬性（w:id、w:date、w:rsidR、w:rsidDel、w16du:dateUtc、xml:space）注入新元素。保留原始文件中未變更的文字時，複製原始 `<w:r>` 元素及其現有屬性以維持文件完整性。

**方法選擇指南**：
- **為一般文字新增您自己的變更**：使用 `replace_node()` 搭配 `<w:del>`/`<w:ins>` 標籤，或使用 `suggest_deletion()` 移除整個 `<w:r>` 或 `<w:p>` 元素
- **部分修改另一位作者的追蹤修訂**：使用 `replace_node()` 將您的變更嵌套在他們的 `<w:ins>`/`<w:del>` 內
- **完全拒絕另一位作者的插入**：在 `<w:ins>` 元素上使用 `revert_insertion()`（不是 `suggest_deletion()`）
- **完全拒絕另一位作者的刪除**：在 `<w:del>` 元素上使用 `revert_deletion()` 以使用追蹤修訂還原已刪除的內容

```python
# 最小編輯 - 變更一個字："The report is monthly" → "The report is quarterly"
# 原始：<w:r w:rsidR="00AB12CD"><w:rPr><w:rFonts w:ascii="Calibri"/></w:rPr><w:t>The report is monthly</w:t></w:r>
node = doc["word/document.xml"].get_node(tag="w:r", contains="The report is monthly")
rpr = tags[0].toxml() if (tags := node.getElementsByTagName("w:rPr")) else ""
replacement = f'<w:r w:rsidR="00AB12CD">{rpr}<w:t>The report is </w:t></w:r><w:del><w:r>{rpr}<w:delText>monthly</w:delText></w:r></w:del><w:ins><w:r>{rpr}<w:t>quarterly</w:t></w:r></w:ins>'
doc["word/document.xml"].replace_node(node, replacement)

# 最小編輯 - 變更數字："within 30 days" → "within 45 days"
# 原始：<w:r w:rsidR="00XYZ789"><w:rPr><w:rFonts w:ascii="Calibri"/></w:rPr><w:t>within 30 days</w:t></w:r>
node = doc["word/document.xml"].get_node(tag="w:r", contains="within 30 days")
rpr = tags[0].toxml() if (tags := node.getElementsByTagName("w:rPr")) else ""
replacement = f'<w:r w:rsidR="00XYZ789">{rpr}<w:t>within </w:t></w:r><w:del><w:r>{rpr}<w:delText>30</w:delText></w:r></w:del><w:ins><w:r>{rpr}<w:t>45</w:t></w:r></w:ins><w:r w:rsidR="00XYZ789">{rpr}<w:t> days</w:t></w:r>'
doc["word/document.xml"].replace_node(node, replacement)

# 完全替換 - 即使替換所有文字也保留格式
node = doc["word/document.xml"].get_node(tag="w:r", contains="apple")
rpr = tags[0].toxml() if (tags := node.getElementsByTagName("w:rPr")) else ""
replacement = f'<w:del><w:r>{rpr}<w:delText>apple</w:delText></w:r></w:del><w:ins><w:r>{rpr}<w:t>banana orange</w:t></w:r></w:ins>'
doc["word/document.xml"].replace_node(node, replacement)

# 插入新內容（不需要屬性 - 自動注入）
node = doc["word/document.xml"].get_node(tag="w:r", contains="existing text")
doc["word/document.xml"].insert_after(node, '<w:ins><w:r><w:t>new text</w:t></w:r></w:ins>')

# 部分刪除另一位作者的插入
# 原始：<w:ins w:author="Jane Smith" w:date="..."><w:r><w:t>quarterly financial report</w:t></w:r></w:ins>
# 目標：只刪除 "financial" 使其變成 "quarterly report"
node = doc["word/document.xml"].get_node(tag="w:ins", attrs={"w:id": "5"})
# 重要：在外層 <w:ins> 上保留 w:author="Jane Smith" 以維持作者身份
replacement = '''<w:ins w:author="Jane Smith" w:date="2025-01-15T10:00:00Z">
  <w:r><w:t>quarterly </w:t></w:r>
  <w:del><w:r><w:delText>financial </w:delText></w:r></w:del>
  <w:r><w:t>report</w:t></w:r>
</w:ins>'''
doc["word/document.xml"].replace_node(node, replacement)

# 變更另一位作者插入的部分內容
# 原始：<w:ins w:author="Jane Smith"><w:r><w:t>in silence, safe and sound</w:t></w:r></w:ins>
# 目標：將 "safe and sound" 變更為 "soft and unbound"
node = doc["word/document.xml"].get_node(tag="w:ins", attrs={"w:id": "8"})
replacement = f'''<w:ins w:author="Jane Smith" w:date="2025-01-15T10:00:00Z">
  <w:r><w:t>in silence, </w:t></w:r>
</w:ins>
<w:ins>
  <w:r><w:t>soft and unbound</w:t></w:r>
</w:ins>
<w:ins w:author="Jane Smith" w:date="2025-01-15T10:00:00Z">
  <w:del><w:r><w:delText>safe and sound</w:delText></w:r></w:del>
</w:ins>'''
doc["word/document.xml"].replace_node(node, replacement)

# 刪除整個 run（只在刪除所有內容時使用；部分刪除請使用 replace_node）
node = doc["word/document.xml"].get_node(tag="w:r", contains="text to delete")
doc["word/document.xml"].suggest_deletion(node)

# 刪除整個段落（就地處理，適用於一般和編號清單段落）
para = doc["word/document.xml"].get_node(tag="w:p", contains="paragraph to delete")
doc["word/document.xml"].suggest_deletion(para)

# 新增編號清單項目
target_para = doc["word/document.xml"].get_node(tag="w:p", contains="existing list item")
pPr = tags[0].toxml() if (tags := target_para.getElementsByTagName("w:pPr")) else ""
new_item = f'<w:p>{pPr}<w:r><w:t>New item</w:t></w:r></w:p>'
tracked_para = DocxXMLEditor.suggest_paragraph(new_item)
doc["word/document.xml"].insert_after(target_para, tracked_para)
# 選擇性：在內容前新增間距段落以獲得更好的視覺分隔
# spacing = DocxXMLEditor.suggest_paragraph('<w:p><w:pPr><w:pStyle w:val="ListParagraph"/></w:pPr></w:p>')
# doc["word/document.xml"].insert_after(target_para, spacing + tracked_para)
```

### 新增註解

```python
# 新增跨越兩個現有追蹤修訂的註解
# 注意：w:id 是自動產生的。只有在您從 XML 檢查中知道 w:id 時才按 w:id 搜尋
start_node = doc["word/document.xml"].get_node(tag="w:del", attrs={"w:id": "1"})
end_node = doc["word/document.xml"].get_node(tag="w:ins", attrs={"w:id": "2"})
doc.add_comment(start=start_node, end=end_node, text="此變更的說明")

# 在段落上新增註解
para = doc["word/document.xml"].get_node(tag="w:p", contains="paragraph text")
doc.add_comment(start=para, end=para, text="此段落的註解")

# 在新建立的追蹤修訂上新增註解
# 首先建立追蹤修訂
node = doc["word/document.xml"].get_node(tag="w:r", contains="old")
new_nodes = doc["word/document.xml"].replace_node(
    node,
    '<w:del><w:r><w:delText>old</w:delText></w:r></w:del><w:ins><w:r><w:t>new</w:t></w:r></w:ins>'
)
# 然後在新建立的元素上新增註解
# new_nodes[0] 是 <w:del>，new_nodes[1] 是 <w:ins>
doc.add_comment(start=new_nodes[0], end=new_nodes[1], text="根據需求將 old 變更為 new")

# 回覆現有註解
doc.reply_to_comment(parent_comment_id=0, text="我同意此變更")
```

### 拒絕追蹤修訂

**重要**：使用 `revert_insertion()` 拒絕插入，使用 `revert_deletion()` 透過追蹤修訂還原刪除。`suggest_deletion()` 只用於一般未標記的內容。

```python
# 拒絕插入（將其包在刪除中）
# 當另一位作者插入您想刪除的文字時使用
ins = doc["word/document.xml"].get_node(tag="w:ins", attrs={"w:id": "5"})
nodes = doc["word/document.xml"].revert_insertion(ins)  # 回傳 [ins]

# 拒絕刪除（建立插入以還原已刪除的內容）
# 當另一位作者刪除您想還原的文字時使用
del_elem = doc["word/document.xml"].get_node(tag="w:del", attrs={"w:id": "3"})
nodes = doc["word/document.xml"].revert_deletion(del_elem)  # 回傳 [del_elem, new_ins]

# 拒絕段落中的所有插入
para = doc["word/document.xml"].get_node(tag="w:p", contains="paragraph text")
nodes = doc["word/document.xml"].revert_insertion(para)  # 回傳 [para]

# 拒絕段落中的所有刪除
para = doc["word/document.xml"].get_node(tag="w:p", contains="paragraph text")
nodes = doc["word/document.xml"].revert_deletion(para)  # 回傳 [para]
```

### 插入圖片

**關鍵**：Document 類別使用 `doc.unpacked_path` 的暫存副本。務必將圖片複製到此暫存目錄，而非原始解壓縮資料夾。

```python
from PIL import Image
import shutil, os

# 首先初始化文件
doc = Document('unpacked')

# 複製圖片並計算保持長寬比的全寬尺寸
media_dir = os.path.join(doc.unpacked_path, 'word/media')
os.makedirs(media_dir, exist_ok=True)
shutil.copy('image.png', os.path.join(media_dir, 'image1.png'))
img = Image.open(os.path.join(media_dir, 'image1.png'))
width_emus = int(6.5 * 914400)  # 6.5 英吋可用寬度，914400 EMU/英吋
height_emus = int(width_emus * img.size[1] / img.size[0])

# 新增關聯和內容類型
rels_editor = doc['word/_rels/document.xml.rels']
next_rid = rels_editor.get_next_rid()
rels_editor.append_to(rels_editor.dom.documentElement,
    f'<Relationship Id="{next_rid}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/image1.png"/>')
doc['[Content_Types].xml'].append_to(doc['[Content_Types].xml'].dom.documentElement,
    '<Default Extension="png" ContentType="image/png"/>')

# 插入圖片
node = doc["word/document.xml"].get_node(tag="w:p", line_number=100)
doc["word/document.xml"].insert_after(node, f'''<w:p>
  <w:r>
    <w:drawing>
      <wp:inline distT="0" distB="0" distL="0" distR="0">
        <wp:extent cx="{width_emus}" cy="{height_emus}"/>
        <wp:docPr id="1" name="Picture 1"/>
        <a:graphic xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">
          <a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">
            <pic:pic xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">
              <pic:nvPicPr><pic:cNvPr id="1" name="image1.png"/><pic:cNvPicPr/></pic:nvPicPr>
              <pic:blipFill><a:blip r:embed="{next_rid}"/><a:stretch><a:fillRect/></a:stretch></pic:blipFill>
              <pic:spPr><a:xfrm><a:ext cx="{width_emus}" cy="{height_emus}"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr>
            </pic:pic>
          </a:graphicData>
        </a:graphic>
      </wp:inline>
    </w:drawing>
  </w:r>
</w:p>''')
```

### 取得節點

```python
# 依文字內容
node = doc["word/document.xml"].get_node(tag="w:p", contains="specific text")

# 依行號範圍
para = doc["word/document.xml"].get_node(tag="w:p", line_number=range(100, 150))

# 依屬性
node = doc["word/document.xml"].get_node(tag="w:del", attrs={"w:id": "1"})

# 依確切行號（必須是標籤開始的行號）
para = doc["word/document.xml"].get_node(tag="w:p", line_number=42)

# 組合篩選條件
node = doc["word/document.xml"].get_node(tag="w:r", line_number=range(40, 60), contains="text")

# 當文字出現多次時消除歧義 - 新增行號範圍
node = doc["word/document.xml"].get_node(tag="w:r", contains="Section", line_number=range(2400, 2500))
```

### 儲存

```python
# 使用自動驗證儲存（複製回原始目錄）
doc.save()  # 預設驗證，驗證失敗時拋出錯誤

# 儲存到不同位置
doc.save('modified-unpacked')

# 跳過驗證（僅供除錯 - 在正式環境中需要這個表示 XML 有問題）
doc.save(validate=False)
```

### 直接 DOM 操作

對於函式庫未涵蓋的複雜情況：

```python
# 存取任何 XML 檔案
editor = doc["word/document.xml"]
editor = doc["word/comments.xml"]

# 直接 DOM 存取（defusedxml.minidom.Document）
node = doc["word/document.xml"].get_node(tag="w:p", line_number=5)
parent = node.parentNode
parent.removeChild(node)
parent.appendChild(node)  # 移到結尾

# 一般文件操作（無追蹤修訂）
old_node = doc["word/document.xml"].get_node(tag="w:p", contains="original text")
doc["word/document.xml"].replace_node(old_node, "<w:p><w:r><w:t>replacement text</w:t></w:r></w:p>")

# 多次插入 - 使用回傳值維持順序
node = doc["word/document.xml"].get_node(tag="w:r", line_number=100)
nodes = doc["word/document.xml"].insert_after(node, "<w:r><w:t>A</w:t></w:r>")
nodes = doc["word/document.xml"].insert_after(nodes[-1], "<w:r><w:t>B</w:t></w:r>")
nodes = doc["word/document.xml"].insert_after(nodes[-1], "<w:r><w:t>C</w:t></w:r>")
# 結果為：original_node, A, B, C
```

## 追蹤修訂（紅線標記）

**請使用上面的 Document 類別處理所有追蹤修訂。** 以下模式供建構替換 XML 字串時參考。

### 驗證規則
驗證器會檢查還原 Claude 變更後的文件文字是否與原始文件相符。這表示：
- **絕不修改另一位作者的 `<w:ins>` 或 `<w:del>` 標籤內的文字**
- **務必使用嵌套刪除**來移除另一位作者的插入
- **每個編輯都必須正確追蹤**使用 `<w:ins>` 或 `<w:del>` 標籤

### 追蹤修訂模式

**關鍵規則**：
1. 絕不修改另一位作者追蹤修訂內的內容。務必使用嵌套刪除。
2. **XML 結構**：務必將 `<w:del>` 和 `<w:ins>` 放在包含完整 `<w:r>` 元素的段落層級。絕不嵌套在 `<w:r>` 元素內 - 這會建立破壞文件處理的無效 XML。

**文字插入：**
```xml
<w:ins w:id="1" w:author="Claude" w:date="2025-07-30T23:05:00Z" w16du:dateUtc="2025-07-31T06:05:00Z">
  <w:r w:rsidR="00792858">
    <w:t>inserted text</w:t>
  </w:r>
</w:ins>
```

**文字刪除：**
```xml
<w:del w:id="2" w:author="Claude" w:date="2025-07-30T23:05:00Z" w16du:dateUtc="2025-07-31T06:05:00Z">
  <w:r w:rsidDel="00792858">
    <w:delText>deleted text</w:delText>
  </w:r>
</w:del>
```

**刪除另一位作者的插入（必須使用嵌套結構）：**
```xml
<!-- 在原始插入內嵌套刪除 -->
<w:ins w:author="Jane Smith" w:id="16">
  <w:del w:author="Claude" w:id="40">
    <w:r><w:delText>monthly</w:delText></w:r>
  </w:del>
</w:ins>
<w:ins w:author="Claude" w:id="41">
  <w:r><w:t>weekly</w:t></w:r>
</w:ins>
```

**還原另一位作者的刪除：**
```xml
<!-- 保持他們的刪除不變，在其後新增插入 -->
<w:del w:author="Jane Smith" w:id="50">
  <w:r><w:delText>within 30 days</w:delText></w:r>
</w:del>
<w:ins w:author="Claude" w:id="51">
  <w:r><w:t>within 30 days</w:t></w:r>
</w:ins>
```
