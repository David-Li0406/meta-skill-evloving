# 自动修复反馈循环

## 目录
- [概述](#概述)
- [执行时机](#执行时机)
- [自动修复类型](#自动修复类型)
- [重试预算机制](#重试预算机制)
- [修复流程](#修复流程)
- [集成到 precheck](#集成到-precheck)
- [输出格式](#输出格式)

---

## 概述

**目标**：在 precheck 阶段发现问题后，自动修复常见错误，减少人工干预，提升 RFC 首次通过率。

**执行者**：Auto-fix 子代理（由 precheck 触发）

**预期收益**：
- RFC 首次通过率从 60% 提升到 85%
- 人工干预减少 40%
- 修复-验证循环自动化

---

## 执行时机

在 precheck 阶段检测到可自动修复的问题时触发：

```
design → precheck → 发现问题 → auto-fix → 验证 → 通过/重试
```

---

## 自动修复类型

### 类型 1：格式错误修复

**检测规则**：场景标题不符合 Gherkin 格式

**错误示例**：
```markdown
### 场景1：启用 3D 音效
**场景**：启用 3D 音效
```

**自动修复**：
```markdown
#### Scenario: 启用 3D 音效
```

**修复逻辑**：
```python
def fix_scenario_format(content):
    # 修复标题格式
    content = re.sub(r'^###\s+场景\d*[:：]\s*', '#### Scenario: ', content, flags=re.MULTILINE)
    content = re.sub(r'^\*\*场景\*\*[:：]\s*', '#### Scenario: ', content, flags=re.MULTILINE)

    # 修复 GIVEN/WHEN/THEN 格式
    content = re.sub(r'前置条件[:：]\s*', '- **GIVEN** ', content)
    content = re.sub(r'操作[:：]\s*', '- **WHEN** ', content)
    content = re.sub(r'结果[:：]\s*', '- **THEN** ', content)

    return content
```

---

### 类型 2：缺失章节补充

**检测规则**：RFC 缺少必需章节

**缺失示例**：缺少 §4.5 可观测性

**自动修复**：
```markdown
### 4.5 可观测性（Observability）

**日志规范**：
- 关键操作记录 INFO 级别日志
- 错误场景记录 ERROR 级别日志
- 日志包含操作 ID、时间戳、结果

**监控指标**：
- 操作成功率（目标 > 99%）
- 操作延迟（p99 < 100ms）
- 错误率（目标 < 1%）

**告警策略**：
- 错误率 > 5% 触发告警
- p99 延迟 > 200ms 触发告警
```

**修复逻辑**：
```python
def fix_missing_section(rfc_content, missing_section):
    templates = {
        '4.1': generate_security_template(),
        '4.2': generate_reliability_template(),
        '4.3': generate_performance_template(),
        '4.4': generate_testability_template(),
        '4.5': generate_observability_template(),
        '4.6': generate_maintainability_template(),
        '4.7': generate_compatibility_template(),
        '4.8': generate_operability_template(),
    }

    template = templates.get(missing_section)
    if template:
        # 在 §4 章节末尾插入
        return insert_section(rfc_content, missing_section, template)
    return rfc_content
```

---

### 类型 3：模糊描述量化

**检测规则**：DFX 描述包含模糊词汇

**模糊示例**：
```markdown
- 性能良好
- 延迟低
- 需要权限
```

**自动修复**：
```markdown
- 性能指标：p99 延迟 < 50ms，吞吐量 > 1000 QPS
- 延迟要求：p99 < 50ms，p95 < 30ms
- 权限策略：需要 ohos.permission.MANAGE_AUDIO 权限
```

**修复逻辑**：
```python
def fix_vague_description(content, context):
    replacements = {
        r'性能(?:良好|优秀|不错)': f'性能指标：p99 延迟 < {infer_latency(context)}ms',
        r'延迟(?:低|小|短)': f'延迟要求：p99 < {infer_latency(context)}ms',
        r'需要权限(?!.*ohos\.permission)': f'权限策略：需要 {infer_permission(context)} 权限',
        r'数据加密(?!.*AES|RSA)': '数据保护：使用 AES-256 加密',
        r'异常处理(?!.*返回|抛出)': f'异常处理：返回错误码 {infer_error_code(context)}',
    }

    for pattern, replacement in replacements.items():
        content = re.sub(pattern, replacement, content)

    return content

def infer_latency(context):
    # 根据上下文推断合理的延迟值
    if 'real-time' in context or '实时' in context:
        return 10
    elif 'interactive' in context or '交互' in context:
        return 50
    else:
        return 100

def infer_permission(context):
    # 根据上下文推断权限名称
    keywords = {
        'audio': 'ohos.permission.MANAGE_AUDIO',
        'camera': 'ohos.permission.CAMERA',
        'location': 'ohos.permission.LOCATION',
    }
    for keyword, permission in keywords.items():
        if keyword in context.lower():
            return permission
    return 'ohos.permission.REQUIRED_PERMISSION'
```

---

### 类型 4：场景覆盖补全

**检测规则**：缺少必需的场景类型

**缺失示例**：缺少异常场景

**自动修复**：
```markdown
#### Scenario: 权限不足时启用 3D 音效失败

- **GIVEN** 用户没有 MANAGE_AUDIO 权限
- **WHEN** 调用 enable3DSound()
- **THEN** 返回错误码 401，提示权限不足
```

**修复逻辑**：
```python
def fix_missing_scenario(rfc_content, scenario_type, context):
    templates = {
        'exception': generate_exception_scenario(context),
        'boundary': generate_boundary_scenario(context),
        'unsupported': generate_unsupported_scenario(context),
    }

    template = templates.get(scenario_type)
    if template:
        # 在“场景规格”末尾插入
        return insert_scenario(rfc_content, template)
    return rfc_content

def generate_exception_scenario(context):
    # 根据上下文生成异常场景
    return f"""
#### Scenario: {context['feature']}失败（权限不足）

- **GIVEN** 用户没有 {context['permission']} 权限
- **WHEN** 调用 {context['api']}()
- **THEN** 返回错误码 401，提示权限不足
"""
```

---

## 重试预算机制

### 预算规则

- **最大重试次数**：3 次
- **每次重试**：修复 → 验证 → 记录
- **超过预算**：报告用户，需要人工干预

### 重试流程

```
第 1 次：precheck 发现问题 → auto-fix 修复 → precheck 验证
第 2 次：仍有问题 → auto-fix 修复 → precheck 验证
第 3 次：仍有问题 → auto-fix 修复 → precheck 验证
超过 3 次：报告用户，标记为"需要人工干预"
```

### 重试记录

```json
{
  "auto_fix": {
    "attempts": [
      {
        "attempt": 1,
        "timestamp": "2026-01-19T10:30:00Z",
        "issues_found": ["格式错误", "缺失章节"],
        "fixes_applied": ["修复场景格式", "补充可观测性章节"],
        "result": "部分通过"
      },
      {
        "attempt": 2,
        "timestamp": "2026-01-19T10:32:00Z",
        "issues_found": ["模糊描述"],
        "fixes_applied": ["量化性能指标"],
        "result": "通过"
      }
    ],
    "total_attempts": 2,
    "final_result": "success"
  }
}
```

---

## 修复流程

### 步骤 1：问题分类

将 precheck 发现的问题分类为：
- 可自动修复（类型 1-4）
- 需要人工干预（复杂逻辑错误、设计缺陷）

### 步骤 2：执行修复

对每个可自动修复的问题：
1. 读取 rfc.md
2. 应用修复逻辑
3. 写回 rfc.md
4. 记录修复操作

### 步骤 3：验证修复

重新运行 precheck：
- 通过 → 结束
- 仍有问题 → 检查重试预算
  - 未超过 → 返回步骤 2
  - 已超过 → 报告用户

### 步骤 4：记录结果

将修复过程写入 progress.json：
- 修复次数
- 修复内容
- 最终结果

---

## 集成到 precheck

### 修改 precheck 流程

```
原流程：
precheck → 发现问题 → 生成报告 → 结束

新流程：
precheck → 发现问题 → 判断是否可自动修复
├─ 可修复 → 调用 auto-fix → 验证 → 通过/重试
└─ 不可修复 → 生成报告 → 结束
```

### 触发条件

```python
def should_trigger_auto_fix(issues):
    auto_fixable_types = [
        'format_error',      # 格式错误
        'missing_section',   # 缺失章节
        'vague_description', # 模糊描述
        'missing_scenario',  # 场景缺失
    ]

    for issue in issues:
        if issue['type'] in auto_fixable_types:
            return True
    return False
```

---

## 输出格式

### progress.json 输出

```json
{
  "phases": {
    "precheck": {
      "status": "complete",
      "issues_found": 5,
      "auto_fix_triggered": true,
      "auto_fix_result": {
        "attempts": 2,
        "fixes_applied": [
          "修复 3 个场景格式错误",
          "补充可观测性章节",
          "量化 2 个模糊描述"
        ],
        "final_result": "success",
        "manual_intervention_needed": false
      }
    }
  }
}
```

### 修复报告

```markdown
# 自动修复报告

## 修复摘要
- 总问题数：5
- 自动修复：5
- 需要人工：0
- 重试次数：2

## 修复详情

### 第 1 次修复
**时间**：2026-01-19 10:30:00

**问题**：
1. 场景格式错误（3 处）
2. 缺失 §4.5 可观测性

**修复**：
1. 修复场景标题为 `#### Scenario:` 格式
2. 补充可观测性章节（日志、监控、告警）

**验证结果**：部分通过（仍有 1 个模糊描述）

### 第 2 次修复
**时间**：2026-01-19 10:32:00

**问题**：
1. 模糊描述："性能良好"

**修复**：
1. 量化为 "p99 延迟 < 50ms"

**验证结果**：通过

## 最终结果
✅ 所有问题已自动修复，RFC 通过预检
```

---

## 注意事项

1. **保守修复**：只修复明确可自动化的问题，避免误修复
2. **保留原意**：修复时保留原始语义，只改进表达
3. **记录详细**：所有修复操作必须记录，便于审计
4. **预算限制**：严格执行 3 次重试限制，避免无限循环
5. **人工兜底**：复杂问题必须交由人工处理

---

## 性能指标

**目标**：
- RFC 首次通过率：60% → 85%
- 人工干预率：40% → 20%
- 平均修复时间：< 2 分钟
- 修复准确率：> 95%
