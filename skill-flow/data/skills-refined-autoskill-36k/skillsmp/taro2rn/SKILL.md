---
name: taro2rn
description:
    Taro 代码转换为 React Native，自动读取转换规则并引导完成转换任务
---

# Taro to React Native 转换

将 Taro 小程序代码转换为 React Native 代码的完整工具包。

## 快速开始

### 第一步：处理 taro2rnTODO.md

检查项目根目录是否存在 `taro2rnTODO.md`：、

| 情况 | 操作 |
| ---- | ---- |
| **存在** | 直接读取，了解当前进度，跳至第二步 |
| **不存在** | 执行初始化流程（见下方） |

#### 初始化流程（仅当文件不存在时执行）

1. **询问用户配置**（使用 AskUserQuestion 工具）：

| 配置项 | 默认值 | 说明 |
| ------ | ------ | ---- |
| 项目名称 | 当前目录名 | 用于标识项目 |
| 设计稿宽度 | 750 | 750 或 1242 |
| RN 应用路径 | . | React Native 应用相对路径 |

2. **基于模板生成 taro2rnTODO.md**：
   - 读取 `templates/TODO_TEMPLATE.md`
   - 替换占位符：
     - `{{PROJECT_NAME}}` → 项目名称
     - `{{DESIGN_WIDTH}}` → 设计稿宽度
     - `{{RN_APP_PATH}}` → RN 应用路径
     - `{{RPX_FILE_PATH}}` → `src/utils/rpx.ts`（固定值）
     - `{{INIT_DATE}}` → 当前日期（YYYY-MM-DD）
   - 写入项目根目录 `taro2rnTODO.md`

### 第二步：执行转换

1. 按照 [TRANSFORM_RULES.md](core/TRANSFORM_RULES.md) 转换组件
2. 遇到问题查阅 [KNOWN_ISSUES.md](core/KNOWN_ISSUES.md)
3. 若本地文档未覆盖，查阅官方文档：[Taro](https://docs.taro.zone/docs/) | [React Native](https://reactnative.dev/docs/getting-started)
4. 完成后更新 `taro2rnTODO.md`

## 文档结构

```
taro2rn/
├── SKILL.md                 # 入口文档
├── core/
│   ├── TRANSFORM_RULES.md   # 转换规则
│   └── KNOWN_ISSUES.md      # 已知问题（含 Monorepo 附录）
└── templates/
    └── TODO_TEMPLATE.md     # 项目进度模板
```

## 转换规则

[core/TRANSFORM_RULES.md](core/TRANSFORM_RULES.md) 包含：

| 章节 | 内容 |
| ---- | ---- |
| 一、组件映射 | View、Text、Image、Input、ScrollView 等 |
| 二、API 映射 | 路由、存储、网络请求、UI 反馈 |
| 三、生命周期 | useDidShow、useRouter、下拉刷新 |
| 四、样式转换 | rpx 单位、Flex、文字、边框 |
| 五、平台代码 | Platform.OS、平台特定文件 |
| 六、事件处理 | 事件对象、阻止冒泡 |
| 七、特殊组件 | Portal、RichText、WebView |
| 八、导入汇总 | Taro → RN 导入对照 |
| 九、IM 布局 | 键盘避让、消息列表 |

## 转换工作流

```
1. 处理 taro2rnTODO.md → 初始化或读取现有进度
2. 确认设计稿标准     → 750 用 rpx()，1242 用 rpx1242()
3. 读取 Taro 源码     → 分析组件结构
4. 应用转换规则       → 参考 TRANSFORM_RULES.md
5. 处理特殊情况       → 查阅 KNOWN_ISSUES.md
6. 更新 taro2rnTODO.md → 标记完成
```
