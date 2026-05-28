# SimpleSurvey Markdown 語法完整指南

本指南詳細說明 SimpleSurvey 系統支援的所有語法、題型變形及進階參數。每個題型都提供獨立的變形範例。

---

## 1. 全域設定 (YAML Frontmatter)

必須位於檔案最上方，使用 `---` 包裹。

### 基本配置

```yaml
---
title: "問卷標題"
---
```

### 完整配置範例

```yaml
---
title: "2026 年度使用者大調查"
hero_image: "https://example.com/banner.jpg"
layout: "one-per-page"
expiry_date: "2026-12-31"
quota_limit: 500
ga_id: "G-XXXXXXXXXX"
bot_protection: "cloudflare"
pages:
  thank_you:
    content: "<h1>感謝參與!</h1><p>您的意見對我們很重要。</p>"
    cta_button:
      text: "返回首頁"
      url: "https://mysite.com"
  closed:
    content: "問卷已截止，感謝您的關注。"
  terminated:
    content: "根據您的回答，問卷已提前結束。"
terms:
  label: "我已閱讀並同意個人資料保護聲明"
  content: "詳細條款內容..."
---
```

**參數說明**：

- `layout`: `"one-per-page"` (逐題顯示) 或 `"scroll"` (捲動顯示)
- `bot_protection`: `"cloudflare"`, `"recaptcha"`, `"none"`
- `expiry_date`: ISO8601 格式 (如 `2026-12-31`)
- `quota_limit`: 正整數

---

## 2. 歡迎區塊 (Welcome Section)

位於 YAML 之後、第一個題目之前，支援 Markdown。

```markdown
---
title: "滿意度調查"
---

歡迎參與我們的調查

感謝您撥冗填寫這份問卷，本問卷約需 **5 分鐘**。

您的意見將幫助我們改進服務品質！
---
### Q1. [Single] 您的年齡層?
...
```

---

## 3. 題目標題與旗標

### 基本格式

`### {ID}. [{Type}] {Title}`

```markdown
### Q1. [Single] 您的職業?
```

### 標題支援 HTML (`/H`)

```markdown
### Q2. [Intro] <b>重要公告</b>：請仔細閱讀 /H
```

### 題目支援圖片 (`/P`)

```markdown
### Q3. [Single] 請選擇您喜歡的顏色 /P
![色卡](https://example.com/colors.jpg)
- ( ) 紅色
- ( ) 藍色
```

### 同時支援 HTML 與圖片 (`/HP`)

```markdown
### Q4. [Single] 選擇您的<em>最愛</em>款式 /HP
![款式圖](https://example.com/styles.jpg)
- ( ) 款式 A
- ( ) 款式 B
```

> 注意：所有的 {type} 都有區分大小寫，如 OpenText 不是 Opentext、Single 不是 single。

---

## 4. 題目說明

### 單行引言 (Blockquote)

```markdown
### Q5. [Text] 您的電子郵件
> 我們將透過此信箱發送抽獎通知
{{ format: "email" }}
```

### 多行引言

```markdown
### Q6. [Textarea] 您的建議
> 請告訴我們您的想法。
> 您的回饋對我們非常重要。
{{ rows: 5 }}
```

### 區塊描述 (`>>>`) - 保留格式與換行

```markdown
### Q7. [Intro] 問卷須知
>>>
本問卷分為三個部分：
1. 基本資料（約 1 分鐘）
2. 使用體驗（約 3 分鐘）
3. 未來期待（約 1 分鐘）

請依您的真實感受填寫。
>>>
```

---

## 5. 題型詳細範例

### 5.1 單選題 [Single]

#### 範例 1：基本單選（無圖片、無跳題）

```markdown
### Q1. [Single] 您的性別?
- ( ) 男性
- ( ) 女性
- ( ) 不願透露
```

#### 範例 2：選項帶圖片

```markdown
### Q2. [Single] 您喜歡哪種風格?
- ( ) ![現代風](https://example.com/modern.jpg) 現代簡約
- ( ) ![古典風](https://example.com/classic.jpg) 古典華麗
- ( ) ![工業風](https://example.com/industrial.jpg) 工業粗獷
```

#### 範例 3：單選搭配跳題邏輯

```markdown
### Q3. [Single] 您是否使用過我們的產品?
- ( ) 是 -> Q5
- ( ) 否
```

#### 範例 4：單選搭配終止邏輯

```markdown
### Q4. [Single] 您是否年滿 18 歲?
- ( ) 是
- ( ) 否 -> TERMINATE
```

#### 範例 5：單選搭配「其他」自填欄位

```markdown
### Q5. [Single] 您的職業?
- ( ) 工程師
- ( ) 設計師
- ( ) 學生
- ( ) 其他 {{ open: true }}
```

#### 範例 6：組合範例（圖片 + 跳題 + 自填）

```markdown
### Q6. [Single] 您最常使用的交通工具?
- ( ) ![捷運](https://example.com/mrt.jpg) 捷運 -> Q_METRO
- ( ) ![公車](https://example.com/bus.jpg) 公車 -> Q_BUS
- ( ) ![機車](https://example.com/scooter.jpg) 機車
- ( ) 其他 {{ open: true }}
```

#### Config 參數

```markdown
### Q7. [Single] 您喜歡的水果? (選項隨機排序)
{{ random: true }}
- ( ) 蘋果
- ( ) 香蕉
- ( ) 橘子
```

---

### 5.2 複選題 [Multi]

#### 範例 1：基本複選

```markdown
### Q8. [Multi] 您感興趣的主題? (可複選)
- [ ] 科技
- [ ] 旅遊
- [ ] 美食
- [ ] 運動
```

#### 範例 2：複選搭配選項圖片

```markdown
### Q9. [Multi] 您想參加的活動? (可複選)
- [ ] ![演唱會](https://example.com/concert.jpg) 演唱會
- [ ] ![展覽](https://example.com/exhibition.jpg) 展覽
- [ ] ![工作坊](https://example.com/workshop.jpg) 工作坊
```

#### 範例 3：複選搭配排他選項

```markdown
### Q10. [Multi] 您遇到的問題? (可複選)
- [ ] 速度太慢
- [ ] 介面不直覺
- [ ] 功能不足
- [ ] 以上皆非 {{ exclusive: true }}
```

#### 範例 4：限制選取數量

```markdown
### Q11. [Multi] 請選擇 2-3 項您最看重的因素
{{ min: 2, max: 3 }}
- [ ] 價格
- [ ] 品質
- [ ] 服務
- [ ] 品牌
- [ ] 便利性
```

#### 範例 5：隨機排序

```markdown
### Q12. [Multi] 您常用的社交平台?
{{ random: true }}
- [ ] Facebook
- [ ] Instagram
- [ ] Twitter
- [ ] LinkedIn
```

#### 範例 6：組合範例（圖片 + 數量限制 + 排他）

```markdown
### Q13. [Multi] 您想收到的禮物? (最多選 2 項)
{{ min: 1, max: 2 }}
- [ ] ![禮券](https://example.com/voucher.jpg) 購物禮券
- [ ] ![3C](https://example.com/gadget.jpg) 3C 產品
- [ ] ![書籍](https://example.com/book.jpg) 書籍
- [ ] 以上都不需要 {{ exclusive: true }}
```

---

### 5.3 矩陣題 [MatrixSingle] & [MatrixMulti]

#### 範例 1：單選矩陣（基本）

```markdown
### Q14. [MatrixSingle] 請評價以下服務項目
- Row: 客服態度
- Row: 處理速度
- Row: 問題解決能力
- Options: 非常滿意, 滿意, 普通, 不滿意
```

#### 範例 2：複選矩陣

```markdown
### Q15. [MatrixMulti] 您在不同時段可以參加的活動?
- Row: 星期一
- Row: 星期二
- Row: 星期三
- Options: 早上, 中午, 下午, 晚上
```

#### 範例 3：複選矩陣搭配每行上限

```markdown
### Q16. [MatrixMulti] 您的課程時段偏好? (每天最多選 2 個時段)
{{ max_per_row: 2 }}
- Row: 星期一
- Row: 星期二
- Row: 星期三
- Options: 09:00-12:00, 13:00-17:00, 18:00-21:00
```

---

### 5.4 評分題 [Rating]

#### 範例 1：基本星級評分

```markdown
### Q17. [Rating] 整體滿意度?
{{ max: 5 }}
```

#### 範例 2：愛心圖示

```markdown
### Q18. [Rating] 您有多喜歡這個產品?
{{ icon: "heart", max: 5 }}
```

#### 範例 3：搭配文字標籤

```markdown
### Q19. [Rating] 推薦意願?
{{ max: 10, labels: ["完全不推薦", "非常推薦"] }}
```

#### 範例 4：組合範例（愛心 + 10 分制 + 標籤）

```markdown
### Q20. [Rating] 您對我們的喜愛程度?
{{ icon: "heart", max: 10, labels: ["超討厭", "超喜歡"] }}
```

---

### 5.5 滑桿題 [Slider]

#### 範例 1：基本滑桿

```markdown
### Q21. [Slider] 您願意支付的價格範圍?
{{ min: 0, max: 1000, step: 50 }}
```

#### 範例 2：顯示即時數值

```markdown
### Q22. [Slider] NPS 推薦分數 (0-10)
{{ min: 0, max: 10, step: 1, show_value: true }}
```

#### 範例 3：搭配單位

```markdown
### Q23. [Slider] 您的預算?
{{ min: 1000, max: 50000, step: 1000, show_value: true }}
```

---

### 5.6 文字輸入 [Text]

#### 範例 1：基本文字輸入

```markdown
### Q24. [Text] 您的姓名?
{{ required: true }}
```

#### 範例 2：Email 格式驗證

```markdown
### Q25. [Text] 電子郵件
{{ format: "email", placeholder: "example@mail.com" }}
```

#### 範例 3：手機號碼驗證

```markdown
### Q26. [Text] 手機號碼
{{ format: "mobile", placeholder: "0912-345-678" }}
```

#### 範例 4：身分證字號驗證

```markdown
### Q27. [Text] 身分證字號
{{ format: "id_card" }}
```

#### 範例 5：網址驗證

```markdown
### Q28. [Text] 您的個人網站
{{ format: "url", placeholder: "https://yoursite.com" }}
```

#### 範例 6：字數限制

```markdown
### Q29. [Text] 推薦代碼 (8-12 字元)
{{ min_length: 8, max_length: 12 }}
```

---

### 5.7 多行文字 [Textarea]

#### 範例 1：基本多行輸入

```markdown
### Q30. [Textarea] 您的建議
{{ rows: 5 }}
```

#### 範例 2：必填且限制字數

```markdown
### Q31. [Textarea] 請詳述您的問題 (至少 20 字)
{{ required: true, min_length: 20, max_length: 500, rows: 8 }}
```

#### 範例 3：搭配 placeholder

```markdown
### Q32. [Textarea] 其他意見
{{ placeholder: "請輸入您的想法...", rows: 4 }}
```

---

### 5.8 數字輸入 [Number]

#### 範例 1：基本數字

```markdown
### Q33. [Number] 您的年齡?
{{ min: 0, max: 120 }}
```

#### 範例 2：搭配單位與間距

```markdown
### Q34. [Number] 每月預算 (元)
{{ min: 0, max: 100000, step: 1000, unit: "元" }}
```

#### 範例 3：必填

```markdown
### Q35. [Number] 家庭成員人數
{{ required: true, min: 1, max: 20 }}
```

---

### 5.9 排序題 [Sort]

#### 範例 1：基本排序

```markdown
### Q36. [Sort] 請依重要性排序以下因素
- [ ] 價格
- [ ] 品質
- [ ] 服務
- [ ] 速度
```

#### 範例 2：限制只排前 N 項

```markdown
### Q37. [Sort] 請選出並排序您最重視的 3 項
{{ limit_top: 3 }}
- [ ] 設計美觀
- [ ] 功能完整
- [ ] 操作簡易
- [ ] 執行效能
- [ ] 客服支援
```

---

### 5.10 日期選擇 [Date]

#### 範例 1：不限日期範圍

```markdown
### Q38. [Date] 您的生日?
{{ range: "all" }}
```

#### 範例 2：僅允許過去日期

```markdown
### Q39. [Date] 您的入職日期
{{ range: "past" }}
```

#### 範例 3：僅允許未來日期

```markdown
### Q40. [Date] 您希望的到貨日期
{{ range: "future" }}
```

---

### 5.11 特殊組件

#### [Check] - 單一核選框

```markdown
### Q41. [Check] 我同意訂閱電子報
{{ required: true }}
```

#### [Heading] - 分段標題

```markdown
### SEC1. [Heading] 第二部分：使用體驗
```

#### [Divider] - 分隔線

```markdown
### DIV1. [Divider] ---
```

#### [Intro] - 純資訊顯示

```markdown
### INFO1. [Intro] 接下來將詢問您的背景資料
> 所有資料僅供研究使用，絕不對外公開。
```

#### [OpenText] - 開放式留言區

```markdown
### NOTE1. [OpenText] 其他補充
> 如有任何想法，歡迎在此留言。
```

> 註：內容的每一行前面都要加上 ">" 標記，系統才會顯示在畫面上，空白行也一樣！

---

## 6. Config 參數完整對照表

| 參數            | 適用題型                      | 說明            | 範例                               |
| :-------------- | :---------------------------- | :-------------- | :--------------------------------- |
| `required`    | 所有題型                      | 必填            | `{{ required: true }}`           |
| `placeholder` | Text, Textarea                | 提示文字        | `{{ placeholder: "請輸入..." }}` |
| `format`      | Text                          | 格式驗證        | `{{ format: "email" }}`          |
| `min_length`  | Text, Textarea                | 最少字數        | `{{ min_length: 10 }}`           |
| `max_length`  | Text, Textarea                | 最多字數        | `{{ max_length: 200 }}`          |
| `rows`        | Textarea                      | 顯示行數        | `{{ rows: 5 }}`                  |
| `min`         | Number, Multi, Slider         | 最小值/最少選項 | `{{ min: 0 }}`                   |
| `max`         | Number, Multi, Rating, Slider | 最大值/最多選項 | `{{ max: 100 }}`                 |
| `step`        | Number, Slider                | 間距            | `{{ step: 5 }}`                  |
| `unit`        | Number                        | 單位            | `{{ unit: "元" }}`               |
| `random`      | Single, Multi                 | 隨機排序        | `{{ random: true }}`             |
| `max_per_row` | MatrixMulti                   | 每行最多選擇數  | `{{ max_per_row: 2 }}`           |
| `icon`        | Rating                        | 圖示類型        | `{{ icon: "heart" }}`            |
| `labels`      | Rating                        | 評分標籤        | `{{ labels: ["差", "好"] }}`     |
| `show_value`  | Slider                        | 顯示數值        | `{{ show_value: true }}`         |
| `limit_top`   | Sort                          | 限制排序前 N 項 | `{{ limit_top: 3 }}`             |
| `range`       | Date                          | 日期範圍        | `{{ range: "past" }}`            |

---

## 7. 跳題邏輯總結

僅 `[Single]` 選項支援跳題：

- `-> QID`: 跳至指定題目
- `-> TERMINATE`: 直接結束問卷

```markdown
### Q1. [Single] 您是會員嗎?
- ( ) 是 -> Q3
- ( ) 否

### Q2. [Text] 請輸入會員編號
{{ required: true }}

### Q3. [Single] 請評分
...
```
