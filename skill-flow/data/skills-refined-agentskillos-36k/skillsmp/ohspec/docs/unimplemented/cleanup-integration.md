# 清理策略与Token预算管理集成指南

**版本**：v1.0
**更新时间**：2026-01-16
**目的**：说明 cleanup-strategy.md 与 token-budget.md 的集成方式

---

## 📌 核心集成原则

### 1. 自动触发机制

清理策略通过Token预算管理自动触发：

```
Token使用监控（实时）
    ↓
达到阈值（50% / 70% / 85%）
    ↓
调度员检测到预警
    ↓
自动执行对应清理层级
    ↓
更新 progress.json 和 findings.json
    ↓
继续执行 RFC
```

### 2. 三级预警与清理层级的映射

| Token阈值 | 预警级别 | 清理层级 | 主要动作 |
|----------|---------|---------|---------|
| 50% | 🟡 黄色 | 层级3黄色 | 归档旧RFC、压缩日志 |
| 70% | 🟠 橙色 | 层级3橙色 | 只保留当前RFC、创建检查点 |
| 85% | 🔴 红色 | 层级3红色 | 最小上下文、建议新会话 |

### 3. 优先级规则

```
紧急清理（Token > 85%）
    ↓ 优先级最高
中等清理（Token 50-85%）
    ↓
定期清理（每周日）
    ↓
RFC完成清理（层级2）
    ↓ 优先级最低
知识库提炼（层级4）
```

---

## 🔄 调度员职责（集成点）

### 每次阶段切换时的操作流程

```
1. 阶段执行完成
    ↓
2. 更新 progress.json
    ├─ current_phase
    ├─ completed_phases
    └─ rfc_sections_completed
    ↓
3. 计算 Token 使用率
    ├─ current_tokens = 系统报告的token使用
    ├─ max_tokens = 200000（来自config.yaml）
    └─ ratio = current_tokens / max_tokens
    ↓
4. 检查是否触发预警
    ├─ IF ratio >= 0.85 → 执行红色清理
    ├─ ELSE IF ratio >= 0.70 → 执行橙色清理
    ├─ ELSE IF ratio >= 0.50 → 执行黄色清理
    └─ ELSE → 继续正常流程
    ↓
5. 执行清理（如需要）
    ├─ 调用对应清理层级的检查清单
    ├─ 更新 progress.json 的 compression_actions
    └─ 记录清理日志
    ↓
6. 继续执行下一阶段
```

### progress.json 中的Token使用字段

```json
{
  "token_usage": {
    "current": 100000,
    "max": 200000,
    "ratio": 0.50,
    "alert_level": "yellow",
    "alert_triggered_at": "2026-01-16T10:30:00Z",
    "last_cleanup": {
      "timestamp": "2026-01-16T10:30:01Z",
      "level": "yellow",
      "actions": [
        "archive_old_rfcs",
        "compress_findings"
      ]
    }
  }
}
```

---

## 📊 清理动作详细说明

### 黄色清理（50%）- 预防性清理

**触发条件**：`token_usage.ratio >= 0.50`

**执行步骤**：

1. **归档旧RFC**
   ```markdown
   # 查看已完成的RFC列表
   cat .claude/rfc-index.md | grep "completed"

   # 保留最近3个，其他归档
   # 移动到 .claude/archive/
   ```

2. **压缩findings.json**
   ```json
   {
     "related_files": ["file1.cpp", "file2.h"],  // 保留
     "patterns": [...],                          // 保留
     "constraints": [...],                       // 保留
     "code_snippets": []                         // 删除
   }
   ```

3. **压缩progress.json**
   ```json
   {
     "current_phase": "design",                  // 保留
     "completed_phases": ["analyze"],            // 保留
     "interactions": []                          // 删除详细内容
   }
   ```

**预期效果**：释放 10-20% token，使用率降至 40% 以下

**调度员代码示例**：
```python
def handle_yellow_alert(progress_json, findings_json):
    # 1. 归档旧RFC
    archive_old_rfcs(keep_recent=3)

    # 2. 压缩findings
    compress_findings(remove_code_snippets=True)

    # 3. 压缩progress
    compress_progress(keep_recent_phases=2)

    # 4. 更新progress.json
    progress_json['token_usage']['alert_level'] = 'yellow'
    progress_json['token_usage']['last_cleanup'] = {
        'timestamp': now(),
        'level': 'yellow',
        'actions': ['archive_old_rfcs', 'compress_findings', 'compress_progress']
    }

    return progress_json
```

---

### 橙色清理（70%）- 激进清理

**触发条件**：`token_usage.ratio >= 0.70`

**执行步骤**：

1. **只保留当前RFC**
   ```markdown
   # 归档所有已完成的RFC
   for rfc in .claude/ohspec/rfcs/*/; do
     if [ "$(cat $rfc/progress.json | jq -r '.current_phase')" != "active" ]; then
       mv "$rfc" .claude/archive/
     fi
   done
   ```

2. **创建检查点**
   ```json
   {
     "timestamp": "2026-01-16T10:30:00Z",
     "checkpoint_type": "orange_alert",
     "phase": "design",
     "active_rfc": "RFC-20260116-xxx",
     "rfc_sections_completed": ["§1", "§2", "§3"],
     "token_usage": {
       "current": 140000,
       "max": 200000,
       "ratio": 0.70
     },
     "archived_rfcs": ["RFC-20260115-xxx", "RFC-20260114-xxx"],
     "recovery_instructions": "使用此检查点恢复上下文"
   }
   ```

3. **清理历史交互**
   ```json
   {
     "interactions": [],  // 删除所有历史交互
     "decisions": []      // 只保留关键决策摘要
   }
   ```

**预期效果**：释放 20-30% token，使用率降至 50% 以下

**调度员代码示例**：
```python
def handle_orange_alert(progress_json, findings_json):
    # 1. 归档所有已完成RFC
    archive_all_completed_rfcs()

    # 2. 创建检查点
    checkpoint = create_checkpoint(
        checkpoint_type='orange_alert',
        phase=progress_json['current_phase'],
        active_rfc=progress_json['active_rfc'],
        rfc_sections=progress_json['rfc_sections_completed']
    )
    save_checkpoint(checkpoint)

    # 3. 清理历史交互
    progress_json['interactions'] = []
    progress_json['decisions'] = extract_key_decisions(progress_json['decisions'])

    # 4. 更新progress.json
    progress_json['token_usage']['alert_level'] = 'orange'
    progress_json['token_usage']['checkpoint'] = checkpoint['id']

    return progress_json
```

---

### 红色清理（85%）- 紧急清理

**触发条件**：`token_usage.ratio >= 0.85`

**执行步骤**：

1. **最小上下文模式**
   ```json
   {
     "current_phase": "design",
     "rfc_sections_completed": ["§1", "§2", "§3"],
     "current_subagent_id": "subagent-xxx",
     "active_rfc": "RFC-20260116-xxx"
   }
   ```

2. **生成紧急恢复点**
   ```json
   {
     "timestamp": "2026-01-16T10:30:00Z",
     "checkpoint_type": "emergency",
     "severity": "critical",
     "complete_state": {
       // 完整的会话状态，用于新会话恢复
     },
     "recovery_instructions": "在新会话中使用 /ohspec:resume [RFC-ID]"
   }
   ```

3. **用户通知**
   ```
   ⚠️ Token 使用率已达 85%，建议：
   1. 使用 /ohspec:resume RFC-20260116-xxx 在新会话中继续
   2. 当前进度已保存到 emergency-checkpoint-xxx.json
   3. 可安全切换会话，无数据丢失
   ```

**预期效果**：释放 30-40% token，使用率降至 55% 以下

**调度员代码示例**：
```python
def handle_red_alert(progress_json, findings_json):
    # 1. 创建最小上下文
    minimal_context = {
        'current_phase': progress_json['current_phase'],
        'rfc_sections_completed': progress_json['rfc_sections_completed'],
        'current_subagent_id': progress_json['current_subagent_id'],
        'active_rfc': progress_json['active_rfc']
    }

    # 2. 生成紧急恢复点
    emergency_checkpoint = create_checkpoint(
        checkpoint_type='emergency',
        severity='critical',
        complete_state=progress_json,
        minimal_context=minimal_context
    )
    save_checkpoint(emergency_checkpoint)

    # 3. 更新progress.json为最小模式
    progress_json = minimal_context
    progress_json['token_usage']['alert_level'] = 'red'
    progress_json['token_usage']['emergency_checkpoint'] = emergency_checkpoint['id']

    # 4. 通知用户
    notify_user_red_alert(emergency_checkpoint['id'])

    return progress_json
```

---

## 🔗 与Resume模式的集成

### 新会话恢复流程

```
用户在新会话中执行：
/ohspec:resume RFC-20260116-xxx
    ↓
调度员读取 emergency-checkpoint-xxx.json
    ↓
恢复完整的会话状态
    ↓
从 current_phase 继续执行
    ↓
重置 token_usage.current 为 0
    ↓
继续执行RFC
```

### 恢复检查清单

```markdown
□ 读取检查点文件
□ 验证检查点完整性
□ 恢复 progress.json
□ 恢复 findings.json
□ 恢复 rfc.md
□ 验证RFC状态一致性
□ 重置Token计数器
□ 继续执行下一阶段
```

---

## 📋 集成配置（config.yaml）

```yaml
# Token预算管理
token_budget:
  max_tokens: 200000

  # 三级预警阈值
  thresholds:
    yellow: 0.50
    orange: 0.70
    red: 0.85

  # 各级别处理策略
  actions:
    yellow:
      - "archive_old_rfcs"
      - "compress_findings"
      - "compress_progress"
    orange:
      - "archive_all_completed_rfcs"
      - "create_checkpoint"
      - "cleanup_interactions"
    red:
      - "minimal_context_mode"
      - "create_emergency_checkpoint"
      - "notify_user"

  # 上下文压缩策略
  compression:
    preserve:
      - "current_phase"
      - "rfc_sections_completed"
      - "key_decisions"
      - "active_rfc"
    compressible:
      - "code_snippets"
      - "interactions"
      - "completed_phases_details"
      - "historical_decisions"

# 清理策略配置
cleanup_strategy:
  # 层级2：RFC完成清理
  level_2:
    trigger: "rfc_completed"
    actions:
      - "generate_rfc_summary"
      - "compress_progress"
      - "compress_findings"
      - "cleanup_temp_files"
      - "update_indices"

  # 层级3：Token阈值清理
  level_3:
    trigger: "token_threshold"
    yellow:
      - "archive_old_rfcs"
      - "compress_findings"
    orange:
      - "archive_all_completed_rfcs"
      - "create_checkpoint"
    red:
      - "minimal_context_mode"
      - "create_emergency_checkpoint"

  # 层级4：知识库提炼
  level_4:
    trigger: "completed_rfcs >= 5"
    actions:
      - "identify_patterns"
      - "update_knowledge_base"
      - "cleanup_redundancy"

  # 层级7：定期维护
  level_7:
    trigger: "weekly"
    schedule: "every_sunday"
    actions:
      - "archive_weekly_logs"
      - "generate_summary"
      - "update_indices"

# 监控配置
monitoring:
  token_check_frequency: "every_phase_switch"
  cleanup_log_path: ".claude/cleanup-log.md"
  checkpoint_retention: "permanent"
  archive_retention: "90_days"
```

---

## 🚀 实施步骤

### 第1步：初始化清理机制

```markdown
1. 创建 .claude/rfc-index.md
   - 记录所有RFC的ID、状态、创建时间

2. 创建 .claude/cleanup-log.md
   - 记录所有清理操作

3. 创建 .claude/archive/ 目录
   - 存放归档的RFC和日志

4. 更新 config.yaml
   - 添加token_budget配置
   - 添加cleanup_strategy配置
```

### 第2步：集成到调度员

```markdown
1. 在调度员的阶段切换逻辑中添加：
   - Token使用率计算
   - 预警阈值检查
   - 清理动作执行

2. 更新 progress.json 的结构：
   - 添加 token_usage 字段
   - 添加 compression_actions 字段
   - 添加 checkpoint 字段

3. 实现清理函数：
   - archive_old_rfcs()
   - compress_findings()
   - compress_progress()
   - create_checkpoint()
   - handle_yellow_alert()
   - handle_orange_alert()
   - handle_red_alert()
```

### 第3步：测试和验证

```markdown
1. 单元测试：
   - 测试Token计算逻辑
   - 测试预警触发条件
   - 测试清理动作

2. 集成测试：
   - 模拟Token逐步增长
   - 验证各级别清理效果
   - 验证恢复流程

3. 端到端测试：
   - 完整的RFC流程
   - 多个RFC的清理
   - 紧急恢复场景
```

### 第4步：文档和培训

```markdown
1. 更新文档：
   - cleanup-strategy.md（已完成）
   - cleanup-integration.md（本文档）
   - 调度员实现指南

2. 创建运维手册：
   - 清理操作手册
   - 故障排查指南
   - 恢复流程指南
```

---

## 📊 监控和报告

### 清理效果指标

```markdown
## 清理效果报告 - [YYYY-MM-DD]

### Token使用趋势
- 清理前：_____ / 200000 (_____%)
- 清理后：_____ / 200000 (_____%)
- 释放比例：_____%

### 文件大小变化
- progress.json：_____ → _____ (减少 _____%)
- findings.json：_____ → _____ (减少 _____%)

### 清理操作统计
- 执行清理次数：_____
- 归档RFC数：_____
- 创建检查点数：_____
- 平均清理耗时：_____ 分钟

### 恢复能力
- 可恢复RFC数：_____
- 最旧归档日期：_____
- 检查点完整性：_____
```

### 监控仪表板

```markdown
# Token使用监控仪表板

## 实时状态
- 当前Token使用：_____ / 200000
- 使用率：_____%
- 预警级别：[正常 / 黄色 / 橙色 / 红色]

## 清理历史（最近7天）
| 日期 | 触发条件 | 清理层级 | 释放Token | 耗时 |
|------|---------|---------|----------|------|
| ... | ... | ... | ... | ... |

## 活跃RFC
| RFC ID | 状态 | 创建时间 | Token占用 |
|--------|------|---------|----------|
| ... | ... | ... | ... |

## 归档统计
- 已归档RFC：_____ 个
- 归档文件大小：_____ MB
- 最旧归档：_____ 天前
```

---

## 🔍 故障排查

### 问题1：清理后Token仍未下降

**原因分析**：
- 清理动作未完全执行
- 新的RFC上下文加载
- Token计算有误

**解决方案**：
```markdown
1. 检查清理日志：cat .claude/cleanup-log.md
2. 验证清理动作：
   - 检查archive目录是否有新文件
   - 检查progress.json是否被压缩
   - 检查findings.json是否被压缩
3. 手动执行清理：按照清理检查清单重新执行
4. 重新计算Token使用率
```

### 问题2：无法恢复RFC

**原因分析**：
- 检查点文件损坏
- 索引文件不完整
- 归档文件丢失

**解决方案**：
```markdown
1. 查看可用检查点：ls -la .claude/checkpoint-*.json
2. 查看RFC索引：cat .claude/rfc-index.md
3. 查看归档目录：ls -la .claude/archive/
4. 如果找到检查点，按照恢复流程执行
5. 如果检查点丢失，记录缺失信息并通知用户
```

### 问题3：清理过度，丢失重要信息

**原因分析**：
- 清理策略过于激进
- 误删了活跃RFC的上下文
- 索引未及时更新

**解决方案**：
```markdown
1. 立即停止清理操作
2. 查看最近的检查点：ls -lt .claude/checkpoint-*.json | head -1
3. 从检查点恢复：按照恢复流程执行
4. 验证恢复完整性
5. 调整清理策略，避免过度清理
```

---

## 📞 快速参考

### 调度员集成检查清单

```markdown
□ 在阶段切换时计算Token使用率
□ 检查是否触发预警阈值
□ 执行对应级别的清理动作
□ 更新progress.json的token_usage字段
□ 记录清理操作到cleanup-log.md
□ 验证清理效果
□ 继续执行下一阶段
```

### 用户操作检查清单

```markdown
□ 定期检查Token使用率
□ 收到预警时查看清理日志
□ 收到红色警告时准备新会话
□ 使用 /ohspec:resume 恢复RFC
□ 验证恢复后的RFC状态
```

---

**文档版本**：v1.0
**最后更新**：2026-01-16
**相关文档**：cleanup-strategy.md、token-budget.md、resume-mode.md
