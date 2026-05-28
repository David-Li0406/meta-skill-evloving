# memex-cli Decision Rules Cheatsheet

1 页速查卡，用于工作流快速决策，**无需脚本计算**。

---

## 📋 并行执行规则（3 秒决策）

| 场景 | 判断 | 配置 |
|------|------|------|
| **任务完全独立** | 无数据依赖 | 无 dependencies 参数 → 并行 |
| **任务有依赖链** | A → B → C | B: dependencies: A; C: dependencies: B |
| **任务同依赖** | A,B 都依赖 C | A: dependencies: C; B: dependencies: C → A,B 并行 |
| **混合场景** | 部分独立，部分依赖 | 分波次：Wave 1 并行，Wave 2 依赖 Wave 1 |

**反模式：**
- ❌ 过度细分（>10 个小任务）
- ❌ 过度串行（>3 层依赖链）

---

## 📂 文件引用规则（2 秒决策）

| 文件特征 | files-mode | 示例 |
|---------|-----------|------|
| **单个小文档** (< 50 KB) | `embed` | `config.json`, `requirements.md` |
| **Glob 模式** (`**/`) | `ref` | `src/**/*.py`, `docs/**/*.md` |
| **多个文件** (> 3 个) | `ref` | `file1.md,file2.md,file3.md,file4.md` |
| **数据文件** (.sql, .csv, .log) | `ref` | `database_dump.sql`, `logs/*.log` |
| **二进制文件** (.png, .pdf) | `ref` | `mockups/*.png` |
| **混合/不确定** | `auto` | `./` (项目根目录) |

**快速口诀：**
- 单小用 embed
- Glob 用 ref
- 多文件用 ref
- 不确定用 auto

---

## 🎯 工作流阶段配置表

| 阶段 | 文件模式 | 并行模式 | 示例 |
|------|---------|---------|------|
| **需求分析** | embed (单文档) | 串行 | requirements_draft.md |
| **设计文档** | embed (2-3 文档) | 并行 | architecture.md, api-spec.md 并行 |
| **代码开发** | ref (多文档) | 波次并行 | docs/**/*.md → ref |
| **测试生成** | ref (源码) | 依赖开发 | src/**/*.py → ref, dependencies: develop |
| **代码审查** | ref (Glob) | 并行 | src/**/*.py → ref |

---

## ⚠️ 错误处理速查

| 错误类型 | 处理策略 | 配置 |
|---------|---------|------|
| **Skill 失败** | 重试 2 次 → 降级 | 3s 间隔，fallback to memex-cli |
| **Context 超限** | 切换 ref | files-mode: embed → ref |
| **Rate Limit** | 等待 60s | 重试或切换 backend |
| **并行部分失败** | 仅重试失败 | 保留成功任务结果 |
| **Timeout** | 指数退避 | 2s → 4s → 8s |

---

## 🔢 规则总数统计

- **并行规则**: 3 条
- **文件引用规则**: 2 条
- **错误处理规则**: 5 条
- **总计**: 10 条核心规则

**目标决策时间**: < 5 秒

---

## 📖 使用说明

### 步骤 1: 识别阶段
确定当前处于哪个工作流阶段（需求/设计/开发/测试）

### 步骤 2: 查表配置
根据"工作流阶段配置表"直接应用配置

### 步骤 3: 特殊情况
如遇特殊场景，参考"并行执行规则"和"文件引用规则"

**示例：**
```
当前阶段: 代码开发
查表 → 文件模式: ref (docs/**/*.md)
查表 → 并行模式: 波次并行
配置完成 ✓
```

---

## 🚀 快速模板

### 模板 1: 并行文档生成
```bash
memex-cli run --stdin <<EOF
---TASK---
id: doc-architecture-$RUN_ID
backend: claude
workdir: .
files: requirements.md
files-mode: embed
---CONTENT---
生成架构文档
---END---

---TASK---
id: doc-api-$RUN_ID
backend: claude
workdir: .
files: requirements.md
files-mode: embed
---CONTENT---
生成 API 文档
---END---
EOF
```

### 模板 2: 依赖开发
```bash
memex-cli run --stdin <<EOF
---TASK---
id: implement-$RUN_ID
backend: codex
workdir: .
files: docs/**/*.md
files-mode: ref
---CONTENT---
实现代码
---END---

---TASK---
id: test-$RUN_ID
backend: codex
workdir: .
dependencies: implement-$RUN_ID
files: src/**/*.py
files-mode: ref
---CONTENT---
生成测试
---END---
EOF
```

---

## 📊 决策流程图（ASCII）

```
┌─────────────────┐
│  开始新任务     │
└────────┬────────┘
         │
    ┌────▼────┐
    │ 任务独立? │
    └────┬────┘
         │
    YES  │  NO
    ┌────▼────┐    ┌─────────────┐
    │  并行   │    │ dependencies │
    └─────────┘    └──────┬──────┘
         │                │
    ┌────▼────────────────▼────┐
    │  文件数量/类型?          │
    └────┬────────────────┬────┘
         │                │
    单/小 │  Glob/多       │
    ┌────▼────┐      ┌────▼────┐
    │  embed  │      │   ref   │
    └─────────┘      └─────────┘
         │                │
    ┌────▼────────────────▼────┐
    │   生成 task 配置         │
    └─────────────────────────┘
```

---

## 💡 记忆口诀

**并行口诀：**
> 独立并行，依赖串行，同依赖可并行

**文件口诀：**
> 单小 embed，Glob ref，多文件 ref，不确定 auto

**错误口诀：**
> Skill 重试降级，Context 切 ref，Rate 等待换端，并行仅重试失败

---

## ✅ 检查清单

使用前快速检查（5 秒）：

- [ ] 任务关系已明确（独立/依赖/同依赖）
- [ ] 文件类型已识别（单/多/Glob/二进制）
- [ ] 错误处理策略已配置（重试/降级/切换）

**检查通过 → 开始编写配置**
