# Iterate 交付物格式

## 路径与命名
- 目录：`iterate/<feature-kebab>/`
- 文件：
  - `<feature_snake>_gen.json`（建模设计元素）
  - `<feature_snake>_update.sql`（DDL 结构变更）
- 目录使用 kebab-case，文件前缀使用 snake_case；前缀与目录语义保持一致。
- 参考风格：`iterate/video-post-processing-variant-encrypt`。

## 建模设计元素 JSON
- 文件为 JSON 数组，每个元素表示一个可生成的模型元素。
- 通用字段：`tag`, `name`, `desc`；`package` 按需要填写（如无可留空或省略）。

### 常见 tag 与字段
- `cmd` / `qry` / `cli` / `payload` / `event`
  - 必填：`package`, `name`, `desc`
  - 字段：`requestFields`, `responseFields`（可为空数组）
- `de`（领域事件）
  - 必填：`package`, `name`, `desc`, `aggregates`, `entity`, `persist`
- `validator`
  - 必填：`package`, `name`, `desc`
- `api_payload`
  - 必填：`name`, `desc`（`package` 可省略）

### 字段说明
- `requestFields` / `responseFields`：数组元素格式为：
  - `name`：lowerCamelCase
  - `type`：Kotlin/JVM 类型或自定义类型，如 `String`、`Int`、`List<String>`
  - `desc`：可选说明
  - `nullable`：可选，布尔值
  - `defaultValue`：可选，字符串；`"\"HLS_AES_128\""`

## DDL 结构变更脚本
- 使用 MySQL DDL（`ALTER TABLE` / `CREATE TABLE`）。
- 每个变更前加 `--` 注释，说明意图。
- 新增列补充 `COMMENT`，枚举字段使用 `@Enum`/`@E` + `@Type`/`@T` 风格（如 `@Enum=...;@Type=EnumName`）。
- 如无结构变更，仍保留文件并写入 `-- no schema change`。

## 数据库注解（COMMENT）
- 注解写在表/列 COMMENT 中：`@Name` 或 `@Name=value`；多个注解用 `;` 分隔，注解片段会从最终注释文本中剔除。
- 主要影响：实体/枚举/关系/聚合生成、字段类型映射、懒加载与只读字段等。
- 完整注解清单与效果参见 `references/DB_ANNOTATIONS.md`。
- 示例：

```sql
COMMENT 'Order status @Type=OrderStatus; @Enum=0:NEW:New|1:PAID:Paid;'
```
