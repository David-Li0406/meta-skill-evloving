# PowerPoint 的 Office Open XML 技術參考

**重要:開始之前請閱讀整份文件。** 關鍵的 XML 結構描述規則和格式要求貫穿全文。錯誤的實作可能會建立 PowerPoint 無法開啟的無效 PPTX 檔案。

## 技術指南

### 結構描述合規性
- **`<p:txBody>` 中的元素順序**:`<a:bodyPr>`、`<a:lstStyle>`、`<a:p>`
- **空白**:為具有前導/尾隨空格的 `<a:t>` 元素新增 `xml:space='preserve'`
- **Unicode**:在 ASCII 內容中跳脫字元:`"` 變成 `&#8220;`
- **圖片**:新增到 `ppt/media/`,在投影片 XML 中引用,設定尺寸以適應投影片邊界
- **關係**:為每張投影片的資源更新 `ppt/slides/_rels/slideN.xml.rels`
- **Dirty 屬性**:在 `<a:rPr>` 和 `<a:endParaRPr>` 元素中新增 `dirty="0"` 以表示乾淨狀態

## 簡報結構

### 基本投影片結構
```xml
<!-- ppt/slides/slide1.xml -->
<p:sld>
  <p:cSld>
    <p:spTree>
      <p:nvGrpSpPr>...</p:nvGrpSpPr>
      <p:grpSpPr>...</p:grpSpPr>
      <!-- 形狀放在這裡 -->
    </p:spTree>
  </p:cSld>
</p:sld>
```

### 文字方塊 / 帶文字的形狀
```xml
<p:sp>
  <p:nvSpPr>
    <p:cNvPr id="2" name="Title"/>
    <p:cNvSpPr>
      <a:spLocks noGrp="1"/>
    </p:cNvSpPr>
    <p:nvPr>
      <p:ph type="ctrTitle"/>
    </p:nvPr>
  </p:nvSpPr>
  <p:spPr>
    <a:xfrm>
      <a:off x="838200" y="365125"/>
      <a:ext cx="7772400" cy="1470025"/>
    </a:xfrm>
  </p:spPr>
  <p:txBody>
    <a:bodyPr/>
    <a:lstStyle/>
    <a:p>
      <a:r>
        <a:t>投影片標題</a:t>
      </a:r>
    </a:p>
  </p:txBody>
</p:sp>
```

### 文字格式化
```xml
<!-- 粗體 -->
<a:r>
  <a:rPr b="1"/>
  <a:t>粗體文字</a:t>
</a:r>

<!-- 斜體 -->
<a:r>
  <a:rPr i="1"/>
  <a:t>斜體文字</a:t>
</a:r>

<!-- 底線 -->
<a:r>
  <a:rPr u="sng"/>
  <a:t>底線文字</a:t>
</a:r>

<!-- 螢光標示 -->
<a:r>
  <a:rPr>
    <a:highlight>
      <a:srgbClr val="FFFF00"/>
    </a:highlight>
  </a:rPr>
  <a:t>螢光標示文字</a:t>
</a:r>

<!-- 字型和大小 -->
<a:r>
  <a:rPr sz="2400" typeface="Arial">
    <a:solidFill>
      <a:srgbClr val="FF0000"/>
    </a:solidFill>
  </a:rPr>
  <a:t>彩色 Arial 24pt</a:t>
</a:r>

<!-- 完整格式化範例 -->
<a:r>
  <a:rPr lang="en-US" sz="1400" b="1" dirty="0">
    <a:solidFill>
      <a:srgbClr val="FAFAFA"/>
    </a:solidFill>
  </a:rPr>
  <a:t>格式化文字</a:t>
</a:r>
```

### 清單
```xml
<!-- 項目符號清單 -->
<a:p>
  <a:pPr lvl="0">
    <a:buChar char="•"/>
  </a:pPr>
  <a:r>
    <a:t>第一個項目符號點</a:t>
  </a:r>
</a:p>

<!-- 編號清單 -->
<a:p>
  <a:pPr lvl="0">
    <a:buAutoNum type="arabicPeriod"/>
  </a:pPr>
  <a:r>
    <a:t>第一個編號項目</a:t>
  </a:r>
</a:p>

<!-- 第二層縮排 -->
<a:p>
  <a:pPr lvl="1">
    <a:buChar char="•"/>
  </a:pPr>
  <a:r>
    <a:t>縮排項目符號</a:t>
  </a:r>
</a:p>
```

### 形狀
```xml
<!-- 矩形 -->
<p:sp>
  <p:nvSpPr>
    <p:cNvPr id="3" name="Rectangle"/>
    <p:cNvSpPr/>
    <p:nvPr/>
  </p:nvSpPr>
  <p:spPr>
    <a:xfrm>
      <a:off x="1000000" y="1000000"/>
      <a:ext cx="3000000" cy="2000000"/>
    </a:xfrm>
    <a:prstGeom prst="rect">
      <a:avLst/>
    </a:prstGeom>
    <a:solidFill>
      <a:srgbClr val="FF0000"/>
    </a:solidFill>
    <a:ln w="25400">
      <a:solidFill>
        <a:srgbClr val="000000"/>
      </a:solidFill>
    </a:ln>
  </p:spPr>
</p:sp>

<!-- 圓角矩形 -->
<p:sp>
  <p:spPr>
    <a:prstGeom prst="roundRect">
      <a:avLst/>
    </a:prstGeom>
  </p:spPr>
</p:sp>

<!-- 圓形/橢圓形 -->
<p:sp>
  <p:spPr>
    <a:prstGeom prst="ellipse">
      <a:avLst/>
    </a:prstGeom>
  </p:spPr>
</p:sp>
```

### 圖片
```xml
<p:pic>
  <p:nvPicPr>
    <p:cNvPr id="4" name="Picture">
      <a:hlinkClick r:id="" action="ppaction://media"/>
    </p:cNvPr>
    <p:cNvPicPr>
      <a:picLocks noChangeAspect="1"/>
    </p:cNvPicPr>
    <p:nvPr/>
  </p:nvPicPr>
  <p:blipFill>
    <a:blip r:embed="rId2"/>
    <a:stretch>
      <a:fillRect/>
    </a:stretch>
  </p:blipFill>
  <p:spPr>
    <a:xfrm>
      <a:off x="1000000" y="1000000"/>
      <a:ext cx="3000000" cy="2000000"/>
    </a:xfrm>
    <a:prstGeom prst="rect">
      <a:avLst/>
    </a:prstGeom>
  </p:spPr>
</p:pic>
```

### 表格
```xml
<p:graphicFrame>
  <p:nvGraphicFramePr>
    <p:cNvPr id="5" name="Table"/>
    <p:cNvGraphicFramePr>
      <a:graphicFrameLocks noGrp="1"/>
    </p:cNvGraphicFramePr>
    <p:nvPr/>
  </p:nvGraphicFramePr>
  <p:xfrm>
    <a:off x="1000000" y="1000000"/>
    <a:ext cx="6000000" cy="2000000"/>
  </p:xfrm>
  <a:graphic>
    <a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/table">
      <a:tbl>
        <a:tblGrid>
          <a:gridCol w="3000000"/>
          <a:gridCol w="3000000"/>
        </a:tblGrid>
        <a:tr h="500000">
          <a:tc>
            <a:txBody>
              <a:bodyPr/>
              <a:lstStyle/>
              <a:p>
                <a:r>
                  <a:t>儲存格 1</a:t>
                </a:r>
              </a:p>
            </a:txBody>
          </a:tc>
          <a:tc>
            <a:txBody>
              <a:bodyPr/>
              <a:lstStyle/>
              <a:p>
                <a:r>
                  <a:t>儲存格 2</a:t>
                </a:r>
              </a:p>
            </a:txBody>
          </a:tc>
        </a:tr>
      </a:tbl>
    </a:graphicData>
  </a:graphic>
</p:graphicFrame>
```

### 投影片版面配置

```xml
<!-- 標題投影片版面配置 -->
<p:sp>
  <p:nvSpPr>
    <p:nvPr>
      <p:ph type="ctrTitle"/>
    </p:nvPr>
  </p:nvSpPr>
  <!-- 標題內容 -->
</p:sp>

<p:sp>
  <p:nvSpPr>
    <p:nvPr>
      <p:ph type="subTitle" idx="1"/>
    </p:nvPr>
  </p:nvSpPr>
  <!-- 副標題內容 -->
</p:sp>

<!-- 內容投影片版面配置 -->
<p:sp>
  <p:nvSpPr>
    <p:nvPr>
      <p:ph type="title"/>
    </p:nvPr>
  </p:nvSpPr>
  <!-- 投影片標題 -->
</p:sp>

<p:sp>
  <p:nvSpPr>
    <p:nvPr>
      <p:ph type="body" idx="1"/>
    </p:nvPr>
  </p:nvSpPr>
  <!-- 內容本文 -->
</p:sp>
```

## 檔案更新

新增內容時,更新這些檔案:

**`ppt/_rels/presentation.xml.rels`:**
```xml
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide" Target="slides/slide1.xml"/>
<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideMaster" Target="slideMasters/slideMaster1.xml"/>
```

**`ppt/slides/_rels/slide1.xml.rels`:**
```xml
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout" Target="../slideLayouts/slideLayout1.xml"/>
<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="../media/image1.png"/>
```

**`[Content_Types].xml`:**
```xml
<Default Extension="png" ContentType="image/png"/>
<Default Extension="jpg" ContentType="image/jpeg"/>
<Override PartName="/ppt/slides/slide1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/>
```

**`ppt/presentation.xml`:**
```xml
<p:sldIdLst>
  <p:sldId id="256" r:id="rId1"/>
  <p:sldId id="257" r:id="rId2"/>
</p:sldIdLst>
```

**`docProps/app.xml`:** 更新投影片數量和統計資料
```xml
<Slides>2</Slides>
<Paragraphs>10</Paragraphs>
<Words>50</Words>
```

## 投影片操作

### 新增新投影片
在簡報末尾新增投影片時:

1. **建立投影片檔案**(`ppt/slides/slideN.xml`)
2. **更新 `[Content_Types].xml`**:為新投影片新增 Override
3. **更新 `ppt/_rels/presentation.xml.rels`**:為新投影片新增關係
4. **更新 `ppt/presentation.xml`**:將投影片 ID 新增到 `<p:sldIdLst>`
5. **建立投影片關係**(`ppt/slides/_rels/slideN.xml.rels`)(如需要)
6. **更新 `docProps/app.xml`**:增加投影片數量並更新統計資料(如果存在)

### 複製投影片
1. 以新名稱複製來源投影片 XML 檔案
2. 更新新投影片中的所有 ID 使其唯一
3. 遵循上述「新增新投影片」步驟
4. **關鍵**:移除或更新 `_rels` 檔案中的任何備忘稿投影片引用
5. 移除對未使用媒體檔案的引用

### 重新排序投影片
1. **更新 `ppt/presentation.xml`**:重新排序 `<p:sldIdLst>` 中的 `<p:sldId>` 元素
2. `<p:sldId>` 元素的順序決定投影片順序
3. 保持投影片 ID 和關係 ID 不變

範例:
```xml
<!-- 原始順序 -->
<p:sldIdLst>
  <p:sldId id="256" r:id="rId2"/>
  <p:sldId id="257" r:id="rId3"/>
  <p:sldId id="258" r:id="rId4"/>
</p:sldIdLst>

<!-- 將投影片 3 移到位置 2 後 -->
<p:sldIdLst>
  <p:sldId id="256" r:id="rId2"/>
  <p:sldId id="258" r:id="rId4"/>
  <p:sldId id="257" r:id="rId3"/>
</p:sldIdLst>
```

### 刪除投影片
1. **從 `ppt/presentation.xml` 移除**:刪除 `<p:sldId>` 項目
2. **從 `ppt/_rels/presentation.xml.rels` 移除**:刪除關係
3. **從 `[Content_Types].xml` 移除**:刪除 Override 項目
4. **刪除檔案**:移除 `ppt/slides/slideN.xml` 和 `ppt/slides/_rels/slideN.xml.rels`
5. **更新 `docProps/app.xml`**:減少投影片數量並更新統計資料
6. **清理未使用的媒體**:從 `ppt/media/` 移除孤立的圖片

注意:不要重新編號剩餘投影片 - 保持其原始 ID 和檔名。


## 常見錯誤避免

- **編碼**:在 ASCII 內容中跳脫 unicode 字元:`"` 變成 `&#8220;`
- **圖片**:新增到 `ppt/media/` 並更新關係檔案
- **清單**:從清單標題省略項目符號
- **ID**:使用有效的十六進位值作為 UUID
- **主題**:檢查 `theme` 目錄中所有主題的顏色

## 基於範本簡報的驗證清單

### 打包前,始終:
- **清理未使用的資源**:移除未引用的媒體、字型和備忘稿目錄
- **修復 Content_Types.xml**:宣告套件中存在的所有投影片、版面配置和主題
- **修復關係 ID**:
   - 如果不使用嵌入字型,移除字型嵌入引用
- **移除損壞的引用**:檢查所有 `_rels` 檔案中對已刪除資源的引用

### 常見範本複製陷阱:
- 複製後多張投影片引用相同的備忘稿投影片
- 來自已不存在的範本投影片的圖片/媒體引用
- 未包含字型時的字型嵌入引用
- 版面配置 12-25 缺少 slideLayout 宣告
- docProps 目錄可能無法解壓縮 - 這是可選的