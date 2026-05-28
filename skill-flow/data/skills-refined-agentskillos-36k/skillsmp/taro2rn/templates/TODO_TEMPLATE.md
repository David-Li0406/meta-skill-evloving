# Taro → React Native 转换进度

> **重要**: 开始工作前请先阅读本文档，了解项目配置和当前进度。

---

## 一、项目配置

| 配置项 | 值 |
| ------ | -- |
| 项目名称 | {{PROJECT_NAME}} |
| 设计稿宽度 | {{DESIGN_WIDTH}} |
| RN 应用路径 | {{RN_APP_PATH}} |
| rpx 文件路径 | {{RPX_FILE_PATH}} |

**转换规则**: `.claude/skills/taro2rn/core/TRANSFORM_RULES.md`

---

## 二、任务进度

### ✅ 已完成

- [x] 项目初始化 - {{INIT_DATE}}

### 🔄 进行中

- [ ] 待添加

### ⏳ 待执行

- [ ] 待添加

---

## 三、更新日志

| 日期 | 更新内容 |
| ---- | -------- |
| {{INIT_DATE}} | 创建 taro2rnTODO.md |

---

## 四、转换工作流

1. 阅读本文档 → 了解项目配置和进度
2. 认领任务 → 在任务后标注进行中
3. 参考转换规则 → `core/TRANSFORM_RULES.md`
4. 遇到问题 → 查阅 `core/KNOWN_ISSUES.md`
5. 更新本文档 → 标记完成，添加日志

---

## 五、注意事项

### 样式转换

- 设计稿宽度 **{{DESIGN_WIDTH}}** → 使用 `rpx()` 或 `rpx{{DESIGN_WIDTH}}()`
- rpx 函数位置: `{{RPX_FILE_PATH}}`

### 原生依赖

安装新依赖后：
```bash
cd {{RN_APP_PATH}}/ios && pod install
```
