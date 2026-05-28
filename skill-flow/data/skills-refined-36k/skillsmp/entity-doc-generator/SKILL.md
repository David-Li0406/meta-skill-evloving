---
name: entity-doc-generator
description: 自動掃描 Java 專案中的 @Entity 類別，分析其結構並生成完整的實體規格文件。
license: MIT
---

# Entity Documentation Generator Skill

## 概述
自動掃描 Java 專案中的 @Entity 類別，分析其結構並生成完整的實體規格文件。

## 使用方式

### 基本用法
````bash
# 掃描特定 package 下的所有 Entity
生成 src/main/java/com/example/domain 下所有 Entity 的規格文件

# 掃描整個專案的 Entity
生成專案中所有 @Entity 類別的規格文件

# 只生成特定 Entity 的文件
生成 User Entity 的規格文件
````

## 實作步驟

### 1. 掃描階段
````bash
# 找出所有標註 @Entity 的 Java 檔案
find <target_path> -name "*.java" -type f -exec grep -l "@Entity" {} \;

# 或使用 grep 遞歸搜尋
grep -rl "@Entity" <target_path> --include="*.java"
````

### 2. 分析階段
對每個 Entity 檔案進行以下分析：

#### 2.1 基本資訊提取
- 類別名稱：從 `public class XXX` 提取
- Package 資訊：從 `package` 語句提取
- 類別註解：@Entity, @Table, @Aggregate 等

#### 2.2 欄位分析
````java
// 提取所有欄位及其註解
- @Id, @GeneratedValue
- @Column (name, nullable, length, unique)
- @Enumerated
- @Embedded
- @Version
- @CreatedDate, @LastModifiedDate
- @CreatedBy, @LastModifiedBy
````

#### 2.3 關聯關係分析
````java
- @OneToOne (mappedBy, cascade, fetch, orphanRemoval)
- @OneToMany (mappedBy, cascade, fetch, orphanRemoval)
- @ManyToOne (fetch, cascade)
- @ManyToMany (mappedBy, cascade, fetch)
- @JoinColumn, @JoinTable
````

#### 2.4 約束與索引
````java
- @Table(uniqueConstraints, indexes)
- @UniqueConstraint
- @Index
````

#### 2.5 方法分析
- 建構子（特別是 protected 無參建構子）
- Factory methods（靜態工廠方法）
- Business methods（公開業務方法）
- Getter/Setter（區分業務邏輯型與單純存取型）

### 3. 文件生成階段

為每個 Entity 生成包含以下章節的 Markdown 文件：
````markdown
# Entity 規格文件：<EntityName>

## 1. 基本資訊
- **Entity 名稱**：從類別名稱提取
- **Package**：從 package 語句提取
- **資料庫表名**：從 @Table(name="xxx") 提取，預設為類別名的蛇形命名
- **描述**：從 JavaDoc 提取
- **Aggregate Root**：檢查是否有 @AggregateRoot 或相關註解
- **建立日期**：從 Git 歷史或檔案時間戳提取

## 2. 身份標識
- **主鍵欄位**：標註 @Id 的欄位
- **主鍵類型**：欄位的 Java 類型
- **生成策略**：@GeneratedValue(strategy=XXX)
- **序列名稱**：如使用 SEQUENCE 策略
- **複合鍵**：檢查 @IdClass 或 @EmbeddedId

## 3. 欄位定義

| 欄位名稱 | Java 類型 | 資料庫欄位 | 必填 | 長度 | 預設值 | 說明 |
|---------|----------|-----------|-----|------|--------|------|
| 從欄位註解自動提取 | | | | | | 從 JavaDoc 提取 |

### Value Objects
列出所有 @Embedded 的值物件

## 4. 驗證規則

從以下註解提取：
- @NotNull, @NotBlank, @NotEmpty
- @Size(min, max)
- @Min, @Max
- @Pattern(regexp)
- @Email
- @Past, @Future
- @Positive, @PositiveOrZero
- 自定義驗證註解

## 5. 不變條件 (Invariants)

從業務方法中的驗證邏輯提取：
```java
// 尋找方法中的 if 條件、throw 語句
// 尋找 Objects.requireNonNull
// 尋找 Assert.xxx 語句
```

## 6. 關聯關係

| 關聯類型 | 目標 Entity | 映射欄位 | Fetch 策略 | Cascade 類型 | 說明 |
|---------|------------|---------|-----------|-------------|------|
| 從關聯註解提取 | | | | | |

## 7. 生命週期管理

### 建構方式
- 公開建構子
- 靜態工廠方法
- Builder pattern

### 狀態欄位
檢查是否有 status, state 等列舉型欄位

### 軟刪除
- deletedAt: 檢查 LocalDateTime/Instant 類型欄位
- deleted/isDeleted: 檢查 Boolean 類型欄位
- @SQLDelete, @Where 註解

### 版本控制
- @Version 註解的欄位

## 8. 持久化映射

### 表結構
```sql
-- 從 @Table, @Column 註解生成 CREATE TABLE 語句
```

### 索引定義
- 從 @Table(indexes={...}) 提取
- 從 @Index 註解提取

### 特殊類型映射
- @Type 註解
- @Convert 轉換器
- @Enumerated(EnumType.STRING/ORDINAL)
- @Lob

## 9. 領域行為

### 業務方法列表
列出所有非 getter/setter 的公開方法

| 方法名稱 | 參數 | 返回值 | 說明 |
|---------|------|--------|------|
| 從方法簽章提取 | | | 從 JavaDoc 提取 |

### 主要業務邏輯
提取關鍵方法的實作邏輯摘要

## 10. 領域事件

檢查方法中是否有：
- applicationEventPublisher.publishEvent(...)
- DomainEvents.publish(...)
- 返回 DomainEvent 列表

## 11. 審計與多租戶

### 審計欄位
- @CreatedDate, @LastModifiedDate
- @CreatedBy, @LastModifiedBy
- @EntityListeners(AuditingEntityListener.class)

### 多租戶
- tenantId 欄位
- @TenantId 註解
- @Filter 註解

## 12. API 契約對應

搜尋對應的 DTO 類別：
- <EntityName>Request
- <EntityName>Response
- <EntityName>DTO

列出欄位映射關係

## 13. 使用範例
```java
// 從測試檔案提取範例
// 搜尋 <EntityName>Test.java
// 搜尋 <EntityName>Repository 的使用
```

## 14. 注意事項與限制

列出：
- TODO, FIXME 註解
- @Deprecated 標記
- 特殊的業務約束註解

## 15. 變更歷史
```bash
# 從 Git 歷史提取
git log --follow --format="%ai %aN %s" -- <entity_file_path> | head -10
```

---
*此文件由 Entity Documentation Generator 自動生成*
*生成時間：<timestamp>*
````

## 4. 輸出格式

### 單一 Entity
生成單獨的 Markdown 檔案：
````
docs/entities/<EntityName>.md
````

### 多個 Entity
生成索引頁和個別文件：
````
docs/entities/
  ├── README.md              # 索引頁，列出所有 Entity
  ├── User.md
  ├── Order.md
  └── Product.md
````

## 進階功能

### 1. 關聯圖生成
使用 Mermaid 語法生成 Entity 關聯圖：
````mermaid
erDiagram
    User ||--o{ Order : places
    Order ||--|{ OrderItem : contains
    Product ||--o{ OrderItem : "ordered in"
````

### 2. 依賴分析
分析 Entity 之間的依賴關係：
- 直接引用
- Repository 依賴
- Service 層使用情況

### 3. 完整性檢查
檢查 Entity 是否遵循最佳實踐：
- [ ] 有 protected 無參建構子
- [ ] @Id 欄位存在
- [ ] equals() 和 hashCode() 正確實作
- [ ] toString() 方法存在
- [ ] 無公開的 setter（除非必要）
- [ ] 關聯使用 Set 而非 List（避免重複）

## 實作提示

### 使用正則表達式提取資訊
````bash
# 提取類別名稱
grep -oP '(?<=class\s)\w+' file.java

# 提取 @Table 的 name 屬性
grep -oP '(?<=@Table\(name\s=\s")[^"]+' file.java

# 提取所有欄位定義
grep -E '^\s*(private|protected|public)\s+\w+(<.*>)?\s+\w+\s*;' file.java
````

### 分析 JPA 註解
建立註解解析對照表：
````bash
# 主鍵相關
@Id → 主鍵欄位
@GeneratedValue(strategy = GenerationType.IDENTITY) → 自增
@GeneratedValue(strategy = GenerationType.SEQUENCE) → 序列
@GeneratedValue(strategy = GenerationType.UUID) → UUID

# 欄位映射
@Column(nullable = false) → 必填
@Column(length = 100) → 長度限制
@Column(unique = true) → 唯一約束
````

## 輸出範例

完整的輸出會類似：
````markdown
# Entity 規格文件：User

## 1. 基本資訊
- **Entity 名稱**：User
- **Package**：com.example.domain.user
- **資料庫表名**：users
- **描述**：系統使用者實體，代表註冊用戶
- **Aggregate Root**：是
- **建立日期**：2024-01-15

## 2. 身份標識
- **主鍵欄位**：id
- **主鍵類型**：Long
- **生成策略**：IDENTITY（資料庫自增）
- **業務鍵**：email（唯一）

## 3. 欄位定義

| 欄位名稱 | Java 類型 | 資料庫欄位 | 必填 | 長度 | 預設值 | 說明 |
|---------|----------|-----------|-----|------|--------|------|
| id | Long | id | ✓ | - | AUTO | 主鍵 |
| email | String | email | ✓ | 255 | - | 使用者電子郵件 |
| username | String | username | ✓ | 50 | - | 使用者名稱 |
| password | String | password | ✓ | 255 | - | 加密後密碼 |
| status | UserStatus | status | ✓ | - | ACTIVE | 帳號狀態 |
| createdAt | LocalDateTime | created_at | ✓ | - | now() | 建立時間 |

...（其他章節）
````

## 使用建議

1. **初次使用**：從小範圍開始，先生成單一 Entity 的文件檢視效果
2. **批次處理**：確認格式滿意後，再批次處理整個 package
3. **定期更新**：程式碼變更後重新生成，保持文件同步
4. **版本控制**：將生成的文件納入 Git 管理
5. **持續改進**：根據實際需求調整文件範本

## 注意事項

- 生成的文件是基於程式碼分析，部分業務邏輯需要人工補充
- JavaDoc 的完整性影響文件品質
- 複雜的業務規則可能需要額外說明
- 建議配合人工審查確保準確性