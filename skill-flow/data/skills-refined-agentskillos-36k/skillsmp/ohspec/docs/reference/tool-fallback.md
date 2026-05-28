# 智能工具回退策略

## 目录
- [概述](#概述)
- [ripgrep 性能优化](#ripgrep-性能优化)
- [当前状态](#当前状态)
- [设计方案](#设计方案)
- [实施步骤](#实施步骤)
- [示例场景](#示例场景)
- [成本收益分析](#成本收益分析)
- [实施建议](#实施建议)

---

## 概述

**问题背景**：
OHSpec 依赖 Grep、Glob、Task 等工具进行代码扫描和分析。在受限环境（权限不足、工具缺失、网络隔离）中，这些工具可能失败，导致整个工作流中断。

**目标**：
建立智能回退机制，当主要工具失败时，自动切换到替代方案，确保工作流在受限环境中仍能继续执行。

**预期收益**：
- 提升鲁棒性，在受限环境中仍能工作
- 减少因工具失败导致的任务中断
- 提供降级但可用的服务
- **性能优化**：使用 ripgrep 可将搜索速度提升 3-10 倍

---

## ripgrep 性能优化

### 为什么选择 ripgrep

**ripgrep (rg)** 是目前最快的代码搜索工具，由 Rust 编写，性能远超传统 grep。

**性能对比**（搜索 100MB 代码库）：
- **ripgrep**: ~0.5 秒（基准）
- **ag (The Silver Searcher)**: ~1.5 秒（3x 慢）
- **grep**: ~5 秒（10x 慢）
- **Grep 工具**: ~3 秒（6x 慢）

**核心优势**：
1. **速度最快**：并行搜索，SIMD 优化
2. **智能过滤**：自动忽略 .gitignore 文件
3. **开箱即用**：默认递归搜索，无需复杂参数
4. **跨平台**：支持 Linux、macOS、Windows

### 工具优先级策略

**新的搜索工具优先级**：

```
1. ripgrep (rg)     ← 最优先，性能最佳
2. ag               ← 次优，性能良好
3. Grep 工具        ← 集成工具，始终可用
4. bash grep        ← 系统自带，保底方案
5. find + cat       ← 最小实现，极端情况
```

### ripgrep 集成方案

#### 方案 1：推荐用户安装（首选）

**优势**：
- 用户获得最佳性能
- 不增加 SKILL 体积
- 用户可自行更新

**实施**：
在 SKILL.md 和 README.md 中添加安装指南：

```markdown
## 性能优化建议

为获得最佳性能，强烈建议安装 ripgrep：

**macOS**:
```bash
brew install ripgrep
```

**Ubuntu/Debian**:
```bash
sudo apt install ripgrep
```

**Windows**:
```bash
choco install ripgrep
# 或使用 scoop
scoop install ripgrep
```

**其他系统**：参考 https://github.com/BurntSushi/ripgrep#installation
```

#### 方案 2：内置 ripgrep 二进制（可选）

**优势**：
- 开箱即用，无需用户安装
- 确保所有用户都有最佳性能

**劣势**：
- 增加 SKILL 体积（~5-10MB）
- 需要维护多平台二进制（Linux x64/ARM、macOS x64/ARM、Windows x64）
- 更新需要同步

**实施**（最小化方案）：
```
.claude/ohspec/bin/
├── rg-linux-x64          # Linux x86_64（服务器 + WSL）
└── rg-windows-x64.exe    # Windows x86_64（开发者桌面）
```

**完整方案**（可选）：
```
.claude/ohspec/bin/
├── rg-linux-x64
├── rg-macos-arm64        # macOS Apple Silicon（M1/M2/M3）
└── rg-windows-x64.exe
```

**说明**：
- **最小化方案**（2 个二进制，~10MB）：覆盖 Linux 服务器 + Windows 开发者，macOS 用户需自行安装
- **完整方案**（3 个二进制，~15MB）：覆盖所有主流平台
- 版本：15.1.0（2025-01-15 发布）
- 下载地址：https://github.com/BurntSushi/ripgrep/releases/tag/15.1.0

**检测逻辑**：
```bash
# 1. 优先使用系统 ripgrep
if command -v rg &> /dev/null; then
    RG_CMD="rg"
    echo "✓ 使用系统 ripgrep"
# 2. 回退到内置 ripgrep
elif [ -f ".claude/ohspec/bin/ripgrep-$(uname -s)-$(uname -m)" ]; then
    RG_CMD=".claude/ohspec/bin/ripgrep-$(uname -s)-$(uname -m)"
    echo "✓ 使用内置 ripgrep"
# 3. 回退到其他工具
else
    RG_CMD=""
    echo "⚠ ripgrep 不可用，使用回退工具"
fi
```

#### 方案 3：混合方案（推荐）

**策略**：
1. 启动时检测 ripgrep 可用性
2. 如果不存在，首次提示用户安装（带一键安装命令）
3. 用户可选择"安装"、"稍后"或"跳过"
4. 记录用户选择，不再重复提示
5. 自动回退到次优工具

**用户体验**：
```
🚀 性能优化建议

检测到您尚未安装 ripgrep，这是目前最快的代码搜索工具。

安装 ripgrep 可将搜索速度提升 3-10 倍：
  macOS:   brew install ripgrep
  Ubuntu:  sudo apt install ripgrep
  Windows: choco install ripgrep

[1] 现在安装（推荐）
[2] 稍后安装
[3] 跳过（使用标准工具）

您的选择：_
```

**状态记录**（progress.json）：
```json
{
  "tool_preferences": {
    "ripgrep_prompt_shown": true,
    "user_choice": "skip",
    "timestamp": "2026-01-19T10:30:00Z",
    "fallback_tool": "grep"
  }
}
```

### 工具检测和选择流程

```
启动 ASSESS 阶段
    ↓
检测 ripgrep (rg)
    ├─ 可用 → 使用 ripgrep（记录到 progress.json）
    └─ 不可用 → 检测 ag
        ├─ 可用 → 使用 ag（记录 + 性能警告）
        └─ 不可用 → 使用 Grep 工具（记录 + 性能警告）
            └─ 失败 → 回退到 bash grep
                └─ 失败 → 回退到 find + cat
```

### 性能监控

在 progress.json 中记录性能数据：

```json
{
  "tool_performance": {
    "search_tool": "ripgrep",
    "version": "15.1.0",
    "total_searches": 15,
    "total_time_sec": 2.5,
    "avg_time_per_search_sec": 0.17,
    "estimated_time_with_grep_sec": 25,
    "time_saved_sec": 22.5,
    "speedup_ratio": 10.0
  }
}
```

---

## 当前状态

### 现有工具依赖

| 工具 | 用途 | 失败场景 |
|------|------|----------|
| Grep | 内容搜索 | 权限不足、文件过大、正则表达式不支持 |
| Glob | 文件查找 | 权限不足、路径过长、符号链接循环 |
| Task | 并行执行 | 资源限制、子代理启动失败 |
| Read | 文件读取 | 权限不足、文件锁定、编码错误 |

### 现有问题

1. **实现未完全接入**：流程文档已定义优先级与回退，但执行侧仍需落地
2. **错误传播**：单个工具失败可能导致阶段失败
3. **用户体验差**：用户需要手动解决环境问题后重试

---

## 设计方案

### 核心思路

**三层回退策略**：
1. **主要工具**（Primary）：性能最优，功能完整
2. **备用工具**（Fallback）：性能降级，功能受限但可用
3. **最小实现**（Minimal）：纯 Bash 实现，功能最小但保证可用

### 回退决策树

```
尝试主要工具
├─ 成功 → 返回结果
└─ 失败 → 记录错误
    ├─ 尝试备用工具
    │   ├─ 成功 → 返回结果 + 警告
    │   └─ 失败 → 记录错误
    │       ├─ 尝试最小实现
    │       │   ├─ 成功 → 返回结果 + 严重警告
    │       │   └─ 失败 → 报告用户，任务失败
```

### 工具回退映射

#### Grep 回退策略（更新：整合 ripgrep）

```yaml
primary: ripgrep (rg)
  - 功能：正则搜索、上下文行、多文件、智能过滤
  - 性能：最优（10x 于 grep）
  - 命令：rg "pattern" path/
  - 可用性：需安装

fallback_1: ag (The Silver Searcher)
  - 功能：正则搜索、多文件、智能过滤
  - 性能：优（3x 于 grep）
  - 命令：ag "pattern" path/
  - 可用性：需安装

fallback_2: Grep 工具
  - 功能：正则搜索、上下文行、多文件
  - 性能：良（集成工具）
  - 可用性：始终可用

fallback_3: Bash grep
  - 功能：基本正则、单文件
  - 性能：中等
  - 命令：grep -r "pattern" path/
  - 可用性：系统自带

minimal: Bash find + cat
  - 功能：字面量搜索
  - 性能：最差
  - 命令：find path/ -type f -exec grep -l "pattern" {} \;
  - 可用性：系统自带
```

#### Glob 回退策略

```yaml
primary: Glob 工具
  - 功能：复杂模式、递归、排除规则
  - 性能：最优

fallback: Bash find
  - 功能：基本模式、递归
  - 性能：中等
  - 命令：find path/ -name "*.js"

minimal: Bash ls + 手动过滤
  - 功能：单层目录
  - 性能：最差
  - 命令：ls path/*.js
```

#### Task 回退策略

```yaml
primary: Task 工具（并行执行）
  - 功能：并行、后台运行、结果收集
  - 性能：最优

fallback: 串行执行
  - 功能：顺序执行、无并行
  - 性能：中等
  - 实现：循环调用子代理

minimal: 单代理执行
  - 功能：单个代理完成所有任务
  - 性能：最差
  - 实现：合并所有任务到一个提示
```

---

## 实施步骤

### 步骤 1：定义回退接口

创建统一的工具接口，封装回退逻辑：

```python
# 伪代码
class ToolWithFallback:
    def execute(self, operation, **kwargs):
        strategies = self.get_strategies(operation)

        for strategy in strategies:
            try:
                result = strategy.execute(**kwargs)
                self.log_success(strategy.name)
                return result
            except Exception as e:
                self.log_failure(strategy.name, e)
                continue

        # 所有策略都失败
        raise ToolFailureError("所有回退策略都失败")

    def get_strategies(self, operation):
        # 返回 [primary, fallback, minimal]
        pass
```

### 步骤 2：实现各工具的回退策略

为每个工具实现三层策略：

```python
# Grep 回退实现
class GrepWithFallback(ToolWithFallback):
    def get_strategies(self, operation):
        return [
            GrepToolStrategy(),      # 主要工具
            BashGrepStrategy(),      # Bash grep
            FindCatStrategy(),       # find + cat
        ]

# Glob 回退实现
class GlobWithFallback(ToolWithFallback):
    def get_strategies(self, operation):
        return [
            GlobToolStrategy(),      # 主要工具
            BashFindStrategy(),      # Bash find
            BashLsStrategy(),        # Bash ls
        ]
```

### 步骤 3：集成到工作流

修改 workflows/assess.md、workflows/analyze.md，使用回退工具：

```markdown
### 步骤 1：统计文件数量（带回退）

尝试使用 Glob 工具：
- 成功 → 继续
- 失败 → 回退到 Bash find
- 仍失败 → 回退到 Bash ls（仅扫描顶层目录）

记录使用的策略到 progress.json。
```

### 步骤 4：记录回退事件

在 progress.json 中记录回退事件：

```json
{
  "tool_fallbacks": [
    {
      "timestamp": "2026-01-19T10:30:00Z",
      "tool": "Grep",
      "operation": "search_code",
      "primary_failed": true,
      "fallback_used": "bash_grep",
      "reason": "权限不足",
      "performance_impact": "2x slower"
    }
  ]
}
```

### 步骤 5：用户通知

当使用回退策略时，通知用户：

```
⚠️ 警告：Grep 工具失败，已回退到 Bash grep（性能降低 2 倍）
原因：权限不足
建议：检查文件权限或使用 sudo
```

---

## 示例场景

### 场景 1：Grep 权限不足

**问题**：扫描 /root/ 目录时权限不足

**回退流程**：
1. Grep 工具失败（Permission denied）
2. 回退到 Bash grep（仍失败）
3. 回退到 find + cat（跳过无权限文件，扫描可访问文件）
4. 返回部分结果 + 警告

**输出**：
```json
{
  "scan_result": {
    "files_scanned": 15,
    "files_skipped": 5,
    "matches": 8,
    "fallback_used": "find_cat",
    "warning": "5 个文件因权限不足被跳过"
  }
}
```

### 场景 2：Task 并行失败

**问题**：资源限制，无法启动 5 个并行子代理

**回退流程**：
1. Task 工具启动 5 个并行任务（失败，资源不足）
2. 回退到串行执行（成功，但耗时 5 倍）
3. 返回结果 + 性能警告

**输出**：
```json
{
  "scan_result": {
    "partitions_scanned": 5,
    "execution_mode": "serial",
    "duration_sec": 250,
    "expected_duration_sec": 50,
    "warning": "并行执行失败，已回退到串行模式（耗时 5 倍）"
  }
}
```

### 场景 3：Glob 符号链接循环

**问题**：项目中存在符号链接循环，Glob 工具陷入死循环

**回退流程**：
1. Glob 工具超时（30 秒无响应）
2. 回退到 Bash find（带 -L 参数避免循环）
3. 返回结果 + 警告

**输出**：
```json
{
  "scan_result": {
    "files_found": 42,
    "fallback_used": "bash_find",
    "warning": "检测到符号链接循环，已跳过"
  }
}
```

---

## 成本收益分析

### 实施成本

| 项目 | 工作量 | 说明 |
|------|--------|------|
| 设计回退接口 | 2 小时 | 定义统一接口和策略模式 |
| 实现 Grep 回退 | 1 小时 | 3 层策略实现 |
| 实现 Glob 回退 | 1 小时 | 3 层策略实现 |
| 实现 Task 回退 | 1.5 小时 | 串行和单代理模式 |
| 集成到工作流 | 1 小时 | 修改 assess.md、analyze.md |
| 测试和文档 | 1.5 小时 | 测试各种失败场景 |
| **总计** | **8 小时** | |

### 预期收益

| 收益 | 量化指标 | 说明 |
|------|----------|------|
| 鲁棒性提升 | 失败率从 15% 降到 3% | 在受限环境中仍能工作 |
| 用户体验改善 | 中断率降低 80% | 自动回退，无需人工干预 |
| 适用场景扩展 | 支持 5+ 种受限环境 | 权限不足、工具缺失、网络隔离等 |

### ROI 评估

- **投入**：8 小时开发 + 2 小时测试 = 10 小时
- **回报**：每次避免任务中断节省 30 分钟 × 预计每月 20 次 = 10 小时/月
- **ROI**：首月即可回本，长期收益显著

---

## 实施建议

### 优先级评估

**建议优先级**：P2（中）

**理由**：
- 不是所有用户都会遇到受限环境问题
- 现有工具在大多数环境中工作良好
- 但对于企业用户（防火墙、权限管理严格）价值很高

### 实施时机

**建议时机**：Phase 3 完成后，收到用户反馈"工具失败"问题时

**前置条件**：
- 现有工作流稳定运行
- 收集到足够的工具失败案例
- 明确最常见的失败场景

### 分阶段实施

**阶段 1（2 小时）**：
- 实现 Grep 回退（最常用）
- 验证回退机制可行性

**阶段 2（3 小时）**：
- 实现 Glob 和 Task 回退
- 集成到工作流

**阶段 3（3 小时）**：
- 完善日志和通知
- 编写测试用例

### 替代方案

如果不实施完整回退机制，可以考虑：

1. **文档化解决方案**：编写故障排查指南，指导用户解决环境问题
2. **环境检测**：启动时检测工具可用性，提前警告用户
3. **优雅降级**：只实现关键工具（Grep）的回退，其他工具失败时给出清晰错误信息

---

## 附录：回退策略速查表

| 工具 | 主要策略 | 备用策略 1 | 备用策略 2 | 最小策略 | 性能对比 |
|------|----------|-----------|-----------|----------|----------|
| Grep | ripgrep (rg) | ag | Grep 工具 / bash grep | find + cat | 1x / 3x / 6x / 10x |
| Glob | Glob 工具 | bash find | bash ls | - | 1x / 3x / 10x |
| Task | 并行执行 | 串行执行 | 单代理 | - | 1x / 5x / 10x |
| Read | Read 工具 | bash cat | bash head | - | 1x / 1.5x / 2x |

**性能说明**：
- Grep 工具链：ripgrep (最快) → ag (3x 慢) → Grep 工具 (6x 慢) → bash grep (10x 慢)
- 推荐优先安装 ripgrep 以获得最佳性能

---

**最后更新**：2026-01-19
**状态**：流程文档已接入（assess/analyze），实现侧待落地执行
