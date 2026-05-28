# RFC 注册表集成指南

> 文档版本: 1.0.0
> 最后更新: 2026-01-16
> 相关文件: `docs/unimplemented/rfc-registry.json`

---

## 概述

本文档说明如何将 RFC 注册表与 OHSpec 项目的其他组件集成，包括自动化更新、数据同步和工作流集成。

## 架构集成

### 整体架构

```
┌─────────────────────────────────────────────────────────────┐
│                    RFC 注册表 (rfc-registry.json)           │
│  - RFC 列表和元数据                                          │
│  - 状态定义和转换规则                                        │
│  - 标签分类体系                                              │
│  - 统计和分析                                                │
└────────┬──────────────────────────────────────────────────┬──┘
         │                                                  │
         ├─→ RFC 文档 (rfc.md)                             │
         │   - 需求和设计                                  │
         │   - 契约和 DFX 约束                             │
         │                                                  │
         ├─→ 进度跟踪 (progress.json)                      │
         │   - 状态机                                      │
         │   - 阶段进度                                    │
         │   - 性能指标                                    │
         │                                                  │
         ├─→ 代码扫描 (findings.json)                      │
         │   - 已确认的决策                                │
         │   - 关键文件                                    │
         │   - 依赖关系                                    │
         │                                                  │
         ├─→ 项目知识库 (project-knowledge.json)           │
         │   - 可复用模式                                  │
         │   - 历史决策                                    │
         │   - DFX 模板                                    │
         │                                                  │
         └─→ 上下文包 (context-pack.json)                 │
             - L0 元数据                                   │
             - L1 决策                                     │
             - L2 摘要                                     │
             - L3 引用                                     │
```

### 数据流

```
创建 RFC
  ↓
初始化文件 (rfc.md, findings.json, progress.json)
  ↓
添加到注册表 (status: draft)
  ↓
执行分析阶段 (status: analyzing)
  ├─→ 更新 findings.json
  ├─→ 更新 progress.json
  └─→ 更新注册表统计
  ↓
执行设计阶段 (status: designing)
  ├─→ 更新 rfc.md
  ├─→ 更新 findings.json
  └─→ 更新注册表统计
  ↓
执行预检阶段 (status: prechecking)
  ├─→ 验证 rfc.md 结构
  └─→ 更新注册表统计
  ↓
执行审核阶段 (status: auditing)
  ├─→ 生成审查报告
  └─→ 更新注册表统计
  ↓
批准或拒绝 (status: approved/rejected)
  ├─→ 更新注册表状态
  ├─→ 提炼到项目知识库
  └─→ 更新统计汇总
  ↓
归档 (status: archived)
  └─→ 备份 RFC 文件
```

## 自动化更新规则

### 1. 状态转换自动化

**触发条件**:
- RFC 文档状态标记变更
- progress.json 状态机转换
- 审核决策确认

**更新逻辑**:
```python
def update_rfc_status(rfc_id, new_status):
    # 验证状态转换合法性
    current_status = registry[rfc_id]['status']
    allowed_transitions = status_definitions[current_status]['transitions_to']

    if new_status not in allowed_transitions:
        raise ValueError(f"Invalid transition: {current_status} -> {new_status}")

    # 更新注册表
    registry[rfc_id]['status'] = new_status
    registry[rfc_id]['updated_at'] = now()

    # 更新统计
    update_statistics(registry)

    # 同步到 progress.json
    sync_to_progress_json(rfc_id, new_status)
```

### 2. 统计汇总自动化

**更新时机**:
- RFC 创建时
- RFC 状态变更时
- RFC 标签变更时
- 每日定时更新

**更新逻辑**:
```python
def update_statistics(registry):
    stats = {
        'total_count': len(registry['rfcs']),
        'status_summary': {},
        'priority_summary': {},
        'complexity_summary': {}
    }

    for rfc in registry['rfcs']:
        # 按状态统计
        status = rfc['status']
        stats['status_summary'][status] = stats['status_summary'].get(status, 0) + 1

        # 按优先级统计
        priority = rfc['tags']['priority']
        stats['priority_summary'][priority] = stats['priority_summary'].get(priority, 0) + 1

        # 按复杂度统计
        complexity = rfc['tags']['complexity']
        stats['complexity_summary'][complexity] = stats['complexity_summary'].get(complexity, 0) + 1

    registry['meta'].update(stats)
```

### 3. 标签自动推断

**规则**:

| 条件 | 自动标签 |
|------|---------|
| 涉及多个平台 | platform: cross-platform |
| 影响多个模块 | complexity: complex |
| 修复已知问题 | type: bugfix |
| 改进现有功能 | type: enhancement |
| 包含 API 变更 | risk: breaking-change |
| 依赖其他 RFC | dependency: blocked-by |

**实现**:
```python
def infer_tags(rfc):
    tags = rfc.get('tags', {})

    # 推断复杂度
    if len(rfc['related_rfcs']) > 2:
        tags['complexity'] = 'complex'

    # 推断风险
    if 'breaking-change' in rfc.get('notes', ''):
        tags['risk'] = 'breaking-change'

    # 推断依赖
    if any(r['relationship'] == 'blocked-by' for r in rfc['related_rfcs']):
        tags['dependency'] = 'blocked-by'

    return tags
```

## 工作流集成

### 1. 创建 RFC 工作流

**步骤**:

```yaml
Step 1: 生成 RFC ID
  Input: 用户需求
  Output: RFC-YYYYMMDD-slug-hash4
  Tool: rfc_id_generator

Step 2: 初始化 RFC 目录
  Input: RFC ID
  Output: rfcs/{RFC_ID}/ 目录
  Files:
    - rfc.md (使用 rfc-minimal.md 模板)
    - findings.json (使用 findings.json 模板)
    - progress.json (使用 progress.json 模板)

Step 3: 添加到注册表
  Input: RFC 元数据
  Output: 注册表条目
  Action:
    - 添加 RFC 到 rfcs 数组
    - 更新统计汇总
    - 设置 status: draft

Step 4: 启动分析阶段
  Input: RFC ID
  Output: 分析结果
  Action:
    - 更新 status: analyzing
    - 执行代码扫描
    - 更新 findings.json
    - 更新 progress.json
```

### 2. 状态转换工作流

**从 ANALYZING 到 DESIGNING**:

```yaml
Precondition:
  - RFC 处于 ANALYZING 状态
  - findings.json 已完成
  - 需求已确认

Action:
  1. 验证 findings.json 完整性
  2. 更新 rfc.md §1-§2
  3. 更新 progress.json 状态
  4. 更新注册表状态
  5. 更新统计汇总

Postcondition:
  - RFC 处于 DESIGNING 状态
  - rfc.md §3-§5 待填充
  - 设计阶段可开始
```

### 3. 批准工作流

**从 AUDITING 到 APPROVED**:

```yaml
Precondition:
  - RFC 处于 AUDITING 状态
  - 审查报告已生成
  - 审查评分 >= 90

Action:
  1. 验证审查报告
  2. 更新 progress.json 审核结果
  3. 更新注册表状态为 APPROVED
  4. 提炼到项目知识库
  5. 更新统计汇总
  6. 发送通知

Postcondition:
  - RFC 处于 APPROVED 状态
  - 可进入实现阶段
  - 知识已积累到项目库
```

## 数据同步规则

### 1. 与 progress.json 同步

**同步方向**: 双向

**同步字段**:

| 注册表字段 | progress.json 字段 | 同步方向 |
|-----------|------------------|--------|
| status | state_machine.current_state | ← → |
| progress.completion_percentage | meta.completion | ← → |
| progress.current_phase | current.phase | ← → |
| progress.phases_completed | phases[*].status | ← |

**同步时机**:
- RFC 状态变更时
- 阶段完成时
- 每 5 分钟定时同步

**冲突解决**:
- progress.json 优先（实时性更强）
- 冲突时记录到审计日志
- 手动审查后确认

### 2. 与 findings.json 同步

**同步方向**: 单向（findings → registry）

**同步字段**:

| findings.json 字段 | 注册表字段 | 映射规则 |
|------------------|-----------|--------|
| confirmed.decisions | tags | 提取关键决策 |
| confirmed.constraints | metadata | 提取约束条件 |
| confirmed.key_files | links | 更新关键文件 |
| confirmed.dependencies | related_rfcs | 推断依赖关系 |

**同步时机**:
- findings.json 更新时
- 阶段转换时
- 每 10 分钟定时同步

### 3. 与 rfc.md 同步

**同步方向**: 单向（rfc.md → registry）

**同步字段**:

| rfc.md 字段 | 注册表字段 | 映射规则 |
|-----------|-----------|--------|
| 状态标记 | status | 提取状态 |
| §1.1 元数据 | metadata | 提取元数据 |
| §2.1 需求 | description | 更新描述 |
| §3.4 场景 | metadata.scenarios | 统计场景数 |
| §4 DFX | tags.risk | 推断风险 |

**同步时机**:
- rfc.md 保存时
- 每 15 分钟定时同步

## 查询和报告集成

### 1. 预定义查询实现

**查询引擎**:

```python
class RFCQuery:
    def __init__(self, registry):
        self.registry = registry
        self.predefined = registry['queries']['predefined']

    def execute(self, query_id, filters=None):
        # 获取预定义查询
        query = next(q for q in self.predefined if q['id'] == query_id)

        # 合并过滤条件
        combined_filters = {**query['filter'], **(filters or {})}

        # 执行查询
        results = self._filter_rfcs(combined_filters)

        return results

    def _filter_rfcs(self, filters):
        results = []
        for rfc in self.registry['rfcs']:
            if self._matches_filters(rfc, filters):
                results.append(rfc)
        return results

    def _matches_filters(self, rfc, filters):
        for key, values in filters.items():
            if key.startswith('tags.'):
                tag_name = key.split('.')[1]
                if rfc['tags'].get(tag_name) not in values:
                    return False
            else:
                if rfc.get(key) not in values:
                    return False
        return True
```

### 2. 报告生成实现

**报告生成器**:

```python
class RFCReportGenerator:
    def __init__(self, registry):
        self.registry = registry
        self.reports = registry['export']['reports']

    def generate(self, report_id, format='json'):
        # 获取报告模板
        report = next(r for r in self.reports if r['id'] == report_id)

        # 提取字段
        data = self._extract_fields(report['fields'])

        # 格式化输出
        if format == 'json':
            return json.dumps(data, indent=2)
        elif format == 'csv':
            return self._to_csv(data)
        elif format == 'markdown':
            return self._to_markdown(data)
        elif format == 'html':
            return self._to_html(data)

    def _extract_fields(self, fields):
        results = []
        for rfc in self.registry['rfcs']:
            row = {}
            for field in fields:
                row[field] = self._get_field_value(rfc, field)
            results.append(row)
        return results

    def _get_field_value(self, rfc, field):
        if '.' in field:
            parts = field.split('.')
            value = rfc
            for part in parts:
                value = value.get(part, {})
            return value
        else:
            return rfc.get(field)
```

## 监控和告警

### 1. 关键指标

**监控指标**:

| 指标 | 阈值 | 告警级别 |
|------|------|--------|
| 活跃 RFC 数 | > 50 | 警告 |
| 被阻塞 RFC 数 | > 5 | 警告 |
| 高风险 RFC 数 | > 3 | 严重 |
| 平均审核时间 | > 7 天 | 警告 |
| 拒绝率 | > 20% | 警告 |

### 2. 告警规则

**规则示例**:

```yaml
Alert: HighBlockedRFCCount
  Condition: count(status='analyzing' AND tags.dependency='blocked-by') > 5
  Severity: WARNING
  Action: 通知项目经理

Alert: HighRiskRFCApproved
  Condition: status='approved' AND tags.risk='high-risk'
  Severity: CRITICAL
  Action: 通知技术负责人

Alert: StaleRFC
  Condition: status='draft' AND updated_at < 30 days ago
  Severity: INFO
  Action: 发送提醒邮件
```

## 性能优化

### 1. 索引策略

**建议索引**:

```python
# 按状态索引
index_by_status = {}
for rfc in registry['rfcs']:
    status = rfc['status']
    if status not in index_by_status:
        index_by_status[status] = []
    index_by_status[status].append(rfc['id'])

# 按优先级索引
index_by_priority = {}
for rfc in registry['rfcs']:
    priority = rfc['tags']['priority']
    if priority not in index_by_priority:
        index_by_priority[priority] = []
    index_by_priority[priority].append(rfc['id'])

# 按所有者索引
index_by_owner = {}
for rfc in registry['rfcs']:
    owner = rfc['owner']
    if owner not in index_by_owner:
        index_by_owner[owner] = []
    index_by_owner[owner].append(rfc['id'])
```

### 2. 缓存策略

**缓存层次**:

| 层次 | 内容 | TTL | 更新触发 |
|------|------|-----|--------|
| L1 | 统计汇总 | 5 分钟 | 状态变更 |
| L2 | 预定义查询结果 | 10 分钟 | 状态变更 |
| L3 | 报告缓存 | 1 小时 | 手动刷新 |

### 3. 分页策略

**分页参数**:

```python
def paginate_rfcs(registry, page=1, page_size=20, sort_by='updated_at'):
    rfcs = registry['rfcs']

    # 排序
    rfcs = sorted(rfcs, key=lambda r: r.get(sort_by), reverse=True)

    # 分页
    start = (page - 1) * page_size
    end = start + page_size

    return {
        'data': rfcs[start:end],
        'total': len(rfcs),
        'page': page,
        'page_size': page_size,
        'total_pages': (len(rfcs) + page_size - 1) // page_size
    }
```

## 错误处理

### 1. 常见错误

**错误类型**:

| 错误 | 原因 | 处理方案 |
|------|------|--------|
| InvalidStateTransition | 非法状态转换 | 验证转换规则 |
| MissingRequiredField | 缺少必填字段 | 提示用户补充 |
| DuplicateRFCID | RFC ID 重复 | 重新生成 ID |
| SyncConflict | 数据同步冲突 | 手动审查后确认 |
| CorruptedData | 数据损坏 | 从备份恢复 |

### 2. 恢复策略

**恢复流程**:

```python
def recover_from_error(error_type, rfc_id):
    if error_type == 'SyncConflict':
        # 从备份恢复
        backup = load_backup(rfc_id)
        registry[rfc_id] = backup
        log_recovery('SyncConflict', rfc_id, backup)

    elif error_type == 'CorruptedData':
        # 从最近的检查点恢复
        checkpoint = load_latest_checkpoint(rfc_id)
        registry[rfc_id] = checkpoint
        log_recovery('CorruptedData', rfc_id, checkpoint)

    elif error_type == 'InvalidStateTransition':
        # 回滚到上一个有效状态
        previous_state = registry[rfc_id]['previous_state']
        registry[rfc_id]['status'] = previous_state
        log_recovery('InvalidStateTransition', rfc_id, previous_state)
```

## 版本控制

### 1. 注册表版本管理

**版本策略**:

```yaml
Version: 1.0.0
  - 初始版本
  - 8 个状态定义
  - 7 个标签分类
  - 6 个预定义查询
  - 4 个报告模板

Version: 1.1.0 (计划)
  - 添加自定义标签支持
  - 添加 RFC 模板
  - 添加工作流自动化

Version: 2.0.0 (计划)
  - 支持 RFC 版本管理
  - 支持 RFC 分支和合并
  - 支持协作编辑
```

### 2. 向后兼容性

**兼容性规则**:

- 新增字段: 可选，默认值为 null
- 删除字段: 标记为 deprecated，保留 1 个版本
- 修改字段: 创建新字段，保留旧字段用于兼容

## 相关文档

- [RFC 注册表使用指南](rfc-registry-guide.md)
- [RFC 格式说明](rfc-format.md)
- [进度跟踪](../templates/progress.json)
- [代码扫描结果](../templates/findings.json)
- [项目知识库](../templates/project-knowledge.json)

## 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| 1.0.0 | 2026-01-16 | 初始版本 |

---

**最后更新**: 2026-01-16
**维护者**: OHSpec 项目团队
