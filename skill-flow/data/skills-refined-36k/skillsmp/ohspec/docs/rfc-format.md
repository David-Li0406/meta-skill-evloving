# RFC ID 格式说明

## 目录
- [格式定义](#格式定义)
- [组成部分](#组成部分)
- [目录结构](#目录结构)
- [生成逻辑](#生成逻辑)

---

## 格式定义

```
RFC-{YYYYMMDD}-{slug}-{hash4}
```

**示例**：`RFC-20260115-3d-audio-toggle-a3f2`

## 组成部分

| 部分 | 说明 | 示例 |
|------|------|------|
| YYYYMMDD | 创建日期 | 20260115 |
| slug | 需求关键词（≤30字符） | 3d-audio-toggle |
| hash4 | 4位哈希（保证唯一性） | a3f2 |

## 目录结构

```
.ohspec/rfcs/
├── RFC-20260115-3d-audio-toggle-a3f2/
│   ├── findings.json    ← 代码扫描结果
│   ├── progress.json    ← 执行时间线
│   └── rfc.md           ← 最终交付物
```

> 兼容（历史）：`.claude/ohspec/rfcs/` 仍可读取，但新产出默认写入 `.ohspec/rfcs/`（工具无关，便于多模型共用）。

## 生成逻辑

```python
def generate_rfc_id(requirement: str) -> str:
    date_part = datetime.now().strftime("%Y%m%d")
    slug = generate_slug(requirement, max_length=30)
    hash_input = f"{requirement}{datetime.now().isoformat()}"
    short_hash = hashlib.md5(hash_input.encode()).hexdigest()[:4]
    return f"RFC-{date_part}-{slug}-{short_hash}"
```

详细实现见 [implementation-guide.md](implementation-guide.md) Step 0。
