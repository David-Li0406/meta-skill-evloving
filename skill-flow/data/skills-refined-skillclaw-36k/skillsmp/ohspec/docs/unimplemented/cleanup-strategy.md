# OHSpec 清理策略体系

**版本**：v1.0
**更新时间**：2026-01-16
**适配项目**：OHSpec（需求分析与设计规范生成）

---

## 📋 快速参考

### 何时执行清理？

| 触发条件 | 清理层级 | 执行时间 | 优先级 |
|---------|---------|---------|--------|
| ✅ RFC 完成 | 层级2 | 立即 | 高 |
| ⚠️ Token达到50% | 层级3（黄色） | 立即 | 高 |
| ⚠️ Token达到70% | 层级3（橙色） | 立即 | 紧急 |
| 🔴 Token达到85% | 层级3（红色） | 立即 | 危急 |
| 📅 完成5个RFC | 层级4 | 计划执行 | 中 |
| 📅 每周日 | 层级7 | 定期执行 | 中 |
| 🎯 项目里程碑 | 层级4+9 | 计划执行 | 高 |

---

## 🔄 RFC完成清理（层级2）

### 执行时机
- ✅ RFC 状态变为"completed"（audit 阶段通过）
- ✅ 用户明确表示 RFC 完成
- ✅ 开始新 RFC 前

### 检查清单

#### ☐ 步骤1：生成 RFC 摘要
```markdown
创建文件：.claude/archive/rfc-[RFC-ID]-[YYYY-MM-DD].md

必须包含：
□ RFC 目标（1-2句话）
□ 关键决策（3-5条，来自 progress.json 的 decisions）
□ 最终交付物（RFC 文件路径、findings.json、progress.json）
□ 经验教训（2-3条，如新发现的模式、常见陷阱）
□ 相关文件索引（RFC ID、阶段、复杂度等级）
```

#### ☐ 步骤2：压缩 progress.json
```markdown
□ 将当前 RFC 的详细日志移到归档
□ 在 progress.json 中只保留摘要（<100字）
□ 更新 progress.json 的 completed_rfcs 字段
□ 清理 interactions 和 decisions 中的冗余信息
```

#### ☐ 步骤3：压缩 findings.json
```markdown
□ 将当前 RFC 的详细扫描结果移到 archived_rfcs
□ 保留关键信息：文件路径、模式识别、技术约束
□ 移除原始代码片段（保留文件位置引用）
□ 更新 findings.json 的 metadata.last_cleanup 字段
```

#### ☐ 步骤4：清理临时文件
```markdown
□ 删除 RFC 工作目录中的临时分析文件
□ 删除中间生成的 precheck 报告（保留最终 audit 报告）
□ 归档或删除过期的 spike 验证结果
□ 清理 .claude/ohspec/rfcs/[RFC-ID]/ 目录中的临时文件
```

#### ☐ 步骤5：更新索引
```markdown
□ 更新 .claude/rfc-index.md（RFC 列表和状态）
□ 如果涉及新技术栈，更新 .claude/tech-stack-index.md
□ 如果识别了新模式，更新 .claude/pattern-index.md
□ 如果涉及新子系统，更新 .claude/subsystem-index.md
```

### 验证
```markdown
□ RFC 摘要文件已创建
□ progress.json 大小 < 50KB
□ findings.json 大小 < 100KB
□ 临时文件已清理
□ 索引文件已更新
```

---

## ⚠️ Token阈值清理（层级3）

### 🟡 黄色警告（50% - 100k/200k）

#### 检查清单
```markdown
□ 归档最旧的已完成 RFC（保留最近3个）
□ 压缩 progress.json（只保留最近2个 RFC）
□ 压缩 findings.json（移除历史代码片段）
□ 清理所有临时搜索结果和中间分析文件
□ 更新 rfc-index.md
```

#### 预期效果
```markdown
□ 释放10-20%的token
□ 当前Token使用降至40%以下
□ 所有活跃 RFC 的上下文仍然完整
```

#### 具体操作

**1. 归档旧 RFC**
```markdown
# 查看已完成的 RFC
cat .claude/rfc-index.md | grep "completed"

# 选择最旧的 RFC（保留最近3个）
# 将其 findings.json 和 progress.json 移到 archive/
mv .claude/ohspec/rfcs/[OLD-RFC-ID]/ .claude/archive/
```

**2. 压缩 progress.json**
```markdown
# 保留结构，删除详细的 interactions 和 decisions
# 只保留：
# - current_phase
# - completed_phases
# - rfc_sections_completed
# - key_decisions（摘要）
# - risks（未解决的风险）
```

**3. 压缩 findings.json**
```markdown
# 移除代码片段，保留文件路径
# 保留：
# - related_files（文件路径列表）
# - patterns（识别的模式）
# - constraints（技术约束）
# - decisions（关键决策）
```

---

### 🟠 橙色警告（70% - 140k/200k）

#### 检查清单
```markdown
□ 归档所有已完成 RFC（只保留当前 RFC）
□ 压缩所有上下文摘要（只保留关键章节）
□ 清理所有临时文件
□ 生成会话摘要索引
□ 创建检查点（checkpoint）
```

#### 预期效果
```markdown
□ 释放20-30%的token
□ 当前Token使用降至50%以下
□ 当前 RFC 的上下文完整
□ 历史 RFC 可通过索引恢复
```

#### 具体操作

**1. 归档所有已完成 RFC**
```markdown
# 保留当前活跃 RFC，其他全部归档
for rfc in .claude/ohspec/rfcs/*/; do
  if [ "$(cat $rfc/progress.json | jq -r '.current_phase')" != "active" ]; then
    mv "$rfc" .claude/archive/
  fi
done
```

**2. 创建检查点**
```markdown
创建文件：.claude/checkpoint-[YYYY-MM-DD-HHmmss].json

包含：
{
  "timestamp": "2026-01-16T10:30:00Z",
  "phase": "design",
  "active_rfc": "RFC-20260116-xxx",
  "rfc_sections_completed": ["§1", "§2", "§3"],
  "token_usage": {
    "current": 140000,
    "max": 200000,
    "ratio": 0.70
  },
  "archived_rfcs": [
    "RFC-20260115-xxx",
    "RFC-20260114-xxx"
  ]
}
```

---

### 🔴 红色警告（85% - 170k/200k）

#### 检查清单
```markdown
□ 强制归档所有历史 RFC
□ 只保留当前 RFC 的最小上下文
□ 生成紧急恢复点
□ 创建完整的会话快照
□ 通知用户考虑开始新会话
```

#### 预期效果
```markdown
□ 释放30-40%的token
□ 当前Token使用降至55%以下
□ 紧急恢复点已创建
□ 用户已被通知
```

#### 具体操作

**1. 最小上下文模式**
```markdown
# 只保留当前 RFC 的必要信息
# progress.json 中只保留：
# - current_phase
# - rfc_sections_completed
# - current_subagent_id（用于 resume）

# findings.json 中只保留：
# - related_files（文件路径）
# - key_constraints（关键约束）
```

**2. 生成紧急恢复点**
```markdown
创建文件：.claude/emergency-checkpoint-[YYYY-MM-DD-HHmmss].json

包含完整的会话状态，用于新会话恢复
```

**3. 用户通知**
```markdown
⚠️ Token 使用率已达 85%，建议：
1. 使用 /ohspec:resume [RFC-ID] 在新会话中继续
2. 当前进度已保存到 emergency-checkpoint-xxx.json
3. 可安全切换会话，无数据丢失
```

---

## 📚 知识库提炼（层级4）

### 执行时机
- 完成5个 RFC 后
- 项目里程碑（如v1.0发布）
- 每月定期维护

### 检查清单

#### ☐ 步骤1：模式识别
```markdown
□ 分析所有已完成 RFC 的 findings.json
□ 识别重复出现的实现模式（出现≥3次）
□ 识别通用的可复用组件和接口设计
□ 识别常见的陷阱和解决方案
□ 识别项目特定的约定和规范
```

#### ☐ 步骤2：生成/更新项目知识库
```markdown
□ 创建或更新 .claude/project-knowledge.md
□ 添加"核心架构模式"章节
□ 添加"可复用组件索引"章节
□ 添加"常见陷阱"章节
□ 添加"项目约定"章节
□ 添加"技术栈决策"章节
```

#### ☐ 步骤3：清理冗余
```markdown
□ 删除已提炼到知识库的重复信息
□ 归档超过1个月的已完成 RFC
□ 只保留最近5个 RFC 的完整上下文
□ 更新所有索引文件
```

### 验证
```markdown
□ project-knowledge.md 已更新
□ 至少识别出3个可复用模式
□ 冗余信息已清理
□ 历史 RFC 已适当归档
```

---

## 📅 定期维护（层级7）

### 每周日执行

#### 检查清单
```markdown
□ 归档上周的 progress.json
□ 生成周摘要
□ 清理临时分析内容
□ 更新所有索引文件
□ 检查归档文件完整性
```

#### 文件操作
```markdown
□ 创建 .claude/archive/progress-[YYYY-MM-weekN].md
□ 压缩 progress.json（保留本周内容）
□ 更新 .claude/progress-digest.md
□ 验证所有索引文件可读
```

### 验证
```markdown
□ 上周日志已归档
□ 周摘要已生成
□ progress.json 大小 < 50KB
□ 所有索引文件已更新
```

---

## 🎯 里程碑清理（层级4+9）

### 执行时机
- 项目版本发布（如v1.0, v2.0）
- 重大功能完成
- 架构重构完成

### 检查清单

#### ☐ 步骤1：创建里程碑检查点
```markdown
□ 创建完整的会话快照
□ 包含所有活跃 RFC 的完整上下文
□ 标记为"里程碑检查点"
□ 永久保留（不自动清理）
```

#### ☐ 步骤2：提炼项目知识库
```markdown
□ 执行层级4知识库提炼
□ 生成里程碑总结文档
□ 记录重大技术决策
□ 记录经验教训
```

#### ☐ 步骤3：归档历史 RFC
```markdown
□ 归档所有已完成 RFC
□ 生成里程碑 RFC 清单
□ 更新所有索引文件
```

#### ☐ 步骤4：清理和重置
```markdown
□ 清理所有临时文件
□ 重置 progress.json
□ 准备下一阶段的工作环境
```

### 验证
```markdown
□ 里程碑检查点已创建
□ 项目知识库已更新
□ 历史 RFC 已归档
□ 工作环境已重置
```

---

## 🔍 Token使用监控

### 实时监控

#### 当前状态检查
```markdown
□ 总Token使用：_____ / 200000 (_____%)
□ 当前 RFC Token：_____
□ 历史 RFC Token：_____
□ 距离黄色警告：_____ token
```

#### 清理历史
```markdown
□ 最近清理时间：_____
□ 清理层级：_____
□ 释放Token：_____
□ 下次清理预计：_____
```

#### 归档统计
```markdown
□ 已归档 RFC：_____ 个
□ 归档文件大小：_____ MB
□ 可恢复 RFC：_____ 个
□ 最旧归档日期：_____
```

---

## 📊 清理效果评估

### 每次清理后填写

#### 清理前
```markdown
- Token使用：_____ / 200000 (_____%)
- progress.json 大小：_____ 字
- findings.json 大小：_____ 字
- 活跃 RFC 数：_____ 个
- 归档 RFC 数：_____ 个
```

#### 清理后
```markdown
- Token使用：_____ / 200000 (_____%)
- progress.json 大小：_____ 字
- findings.json 大小：_____ 字
- 活跃 RFC 数：_____ 个
- 归档 RFC 数：_____ 个
```

#### 效果
```markdown
- 释放Token：_____ (_____%)
- 减少日志大小：_____ 字
- 归档 RFC 数：_____ 个
- 清理耗时：_____ 分钟
```

---

## 🚨 紧急情况处理

### 场景1：Token即将耗尽（>90%）

#### 立即执行
```markdown
1. □ 创建紧急检查点
2. □ 归档所有历史 RFC
3. □ 只保留当前 RFC 的核心上下文
4. □ 通知用户考虑开始新会话
5. □ 记录紧急清理日志
```

### 场景2：清理过度，需要恢复

#### 恢复流程
```markdown
1. □ 列出可用检查点
2. □ 选择最近的检查点
3. □ 恢复活跃 RFC 的完整上下文
4. □ 重建索引
5. □ 验证恢复完整性
```

### 场景3：找不到历史 RFC 信息

#### 查找流程
```markdown
1. □ 查询 .claude/rfc-index.md
2. □ 查询 .claude/tech-stack-index.md
3. □ 搜索 .claude/archive/ 目录
4. □ 检查检查点文件
5. □ 如果仍未找到，记录缺失信息
```

---

## 📝 清理日志模板

### 每次清理后记录

```markdown
## 清理记录 - [YYYY-MM-DD HH:mm]

### 清理信息
- 触发条件：[RFC完成 / Token阈值 / 定期维护 / 里程碑]
- 清理层级：[层级1-9]
- 执行者：[自动 / 手动]

### 清理前状态
- Token使用：_____ / 200000 (_____%)
- progress.json 大小：_____ 字
- findings.json 大小：_____ 字
- 活跃 RFC 数：_____ 个
- 归档 RFC 数：_____ 个

### 执行的操作
- □ 归档 RFC：[列出 RFC ID]
- □ 压缩日志：[压缩比例]
- □ 清理临时文件：[文件数量]
- □ 更新索引：[更新的索引文件]
- □ 创建检查点：[是/否]

### 清理后状态
- Token使用：_____ / 200000 (_____%)
- progress.json 大小：_____ 字
- findings.json 大小：_____ 字
- 活跃 RFC 数：_____ 个
- 归档 RFC 数：_____ 个

### 效果评估
- 释放Token：_____ (_____%)
- 减少日志大小：_____ 字
- 归档 RFC 数：_____ 个
- 清理耗时：_____ 分钟

### 备注
[记录任何特殊情况或需要注意的事项]
```

---

## 🎓 最佳实践

### ✅ 推荐做法

1. **RFC完成立即清理**
   - 不要等待多个 RFC 累积
   - 及时归档可以保持上下文清晰

2. **定期检查Token使用**
   - 每开始新 RFC 前检查
   - 达到50%时主动清理，不要等到70%

3. **保持索引更新**
   - 每次清理后更新索引
   - 索引是快速恢复的关键

4. **重要 RFC 创建检查点**
   - 复杂 RFC 开始前创建检查点
   - 里程碑时创建永久检查点

5. **定期提炼知识库**
   - 不要等到 RFC 太多才提炼
   - 及时提炼可以提高复用率

### ❌ 避免做法

1. **不要过度清理**
   - 不要删除当前 RFC 相关的上下文
   - 不要清理高相关性的历史 RFC

2. **不要忽略索引**
   - 清理后必须更新索引
   - 没有索引的归档很难恢复

3. **不要跳过检查点**
   - 重大清理前必须创建检查点
   - 检查点是最后的保险

4. **不要手动删除归档**
   - 使用清理策略自动管理
   - 手动删除可能破坏索引

5. **不要忽略Token监控**
   - 定期检查Token使用情况
   - 不要等到红色警告才清理

---

## 📞 快速参考命令

### 检查当前状态
```markdown
1. 查看Token使用：检查系统提示中的token usage
2. 查看 RFC 列表：cat .claude/rfc-index.md
3. 查看活跃 RFC：cat .claude/ohspec/rfcs/*/progress.json | jq '.current_phase'
4. 查看归档统计：ls -lh .claude/archive/
```

### 执行清理
```markdown
1. RFC完成清理：按照"RFC完成清理"检查清单执行
2. Token阈值清理：按照对应警告级别的检查清单执行
3. 定期维护：按照"定期维护"检查清单执行
4. 紧急清理：按照"紧急情况处理"流程执行
```

### 恢复信息
```markdown
1. 查找 RFC：cat .claude/rfc-index.md
2. 查找技术栈：cat .claude/tech-stack-index.md
3. 查找模式：cat .claude/pattern-index.md
4. 恢复检查点：按照"紧急情况处理"中的恢复流程
```

---

## 🔗 与Token预算管理集成

### 自动触发机制

OHSpec 的调度员在每次阶段切换时必须：

1. **更新 progress.json 中的 token_usage**
   ```json
   {
     "token_usage": {
       "current": 100000,
       "max": 200000,
       "ratio": 0.50,
       "alert_level": "yellow",
       "alert_triggered_at": "2026-01-16T10:30:00Z"
     }
   }
   ```

2. **检查是否触发预警阈值**
   - 50% → 黄色警告，执行层级3黄色清理
   - 70% → 橙色警告，执行层级3橙色清理
   - 85% → 红色警告，执行层级3红色清理

3. **执行对应级别的处理动作**
   - 参考 config.yaml 中的 token_budget.actions

4. **记录压缩操作到 progress.json**
   ```json
   {
     "compression_actions": [
       {
         "action": "archive_old_rfcs",
         "timestamp": "2026-01-16T10:30:01Z",
         "rfcs_archived": ["RFC-20260115-xxx"]
       }
     ]
   }
   ```

### 与 Resume 模式集成

当触发红色预警后用户开启新会话：

1. 新会话调度员读取 emergency-checkpoint-xxx.json
2. 从 checkpoint 恢复执行状态
3. 从 current_phase 继续执行
4. 重置 token_usage.current 为 0

---

## 📋 文件结构规范

所有清理相关的工作文件必须写入项目本地 `.claude/` 目录：

```
<project>/.claude/
    ├── rfc-index.md                    ← RFC 列表和状态
    ├── tech-stack-index.md             ← 技术栈索引
    ├── pattern-index.md                ← 模式索引
    ├── subsystem-index.md              ← 子系统索引
    ├── project-knowledge.md            ← 项目知识库
    ├── progress-digest.md              ← 进度摘要
    ├── checkpoint-[timestamp].json     ← 检查点
    ├── emergency-checkpoint-[timestamp].json  ← 紧急检查点
    ├── archive/
    │   ├── rfc-[RFC-ID]-[date].md
    │   ├── progress-[YYYY-MM-weekN].md
    │   └── ...
    └── ohspec/
        ├── rfcs/
        │   └── [RFC-ID]/
        │       ├── rfc.md
        │       ├── findings.json
        │       ├── progress.json
        │       └── audit-report.md
        └── ...
```

---

## 🔄 清理流程图

```
RFC 完成
    ↓
执行层级2清理
    ├─ 生成 RFC 摘要
    ├─ 压缩 progress.json
    ├─ 压缩 findings.json
    ├─ 清理临时文件
    └─ 更新索引
    ↓
检查 Token 使用
    ├─ < 50% → 继续
    ├─ 50-70% → 执行黄色清理
    ├─ 70-85% → 执行橙色清理
    └─ > 85% → 执行红色清理
    ↓
完成5个RFC
    ↓
执行层级4清理
    ├─ 模式识别
    ├─ 更新知识库
    └─ 清理冗余
    ↓
每周日
    ↓
执行层级7清理
    ├─ 归档周日志
    ├─ 生成周摘要
    └─ 更新索引
    ↓
项目里程碑
    ↓
执行层级4+9清理
    ├─ 创建里程碑检查点
    ├─ 提炼知识库
    ├─ 归档历史RFC
    └─ 重置工作环境
```

---

## 📊 清理效果指标

### 关键指标

| 指标 | 目标 | 说明 |
|------|------|------|
| Token使用率 | < 50% | 保持充足的上下文空间 |
| progress.json 大小 | < 50KB | 保持日志精简 |
| findings.json 大小 | < 100KB | 保持扫描结果精简 |
| 活跃RFC数 | ≤ 3 | 避免上下文混乱 |
| 归档RFC数 | ≥ 5 | 保留足够的历史 |
| 索引更新频率 | 每次清理后 | 确保可恢复性 |

### 监控周期

- **实时监控**：每次阶段切换时检查Token使用
- **日监控**：每天检查一次Token使用率
- **周监控**：每周日执行定期维护
- **月监控**：每月评估清理效果

---

**文档版本**：v1.0
**最后更新**：2026-01-16
**配套文档**：token-budget.md、resume-mode.md、implementation-guide.md
