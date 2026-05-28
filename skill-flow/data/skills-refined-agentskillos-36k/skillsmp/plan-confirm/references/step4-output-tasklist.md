# 步骤4：创建 impl.md 并输出任务清单

## 创建 Record/impl.md

提案创建完成后，生成实现任务表：

```markdown
# 实现任务表

创建时间：{ISO8601}
项目根目录：{project_root}
plan_version：{plan_version}

## 任务清单

- [ ] {slot}: {任务描述} (proposal: {proposal_id}, 依赖: {依赖列表或"无"})
- [ ] {slot}: {任务描述} (proposal: {proposal_id}, 依赖: {依赖列表或"无"})

## 分组

### 阶段1（无依赖）
- {slot1}
- {slot2}

### 阶段2（依赖阶段1）
- {slot3}

### 阶段3（依赖阶段2）
- {slot4}
```

## 分组规则

1. **解析依赖关系**：从各提案的 `depends_on` 字段获取依赖
2. **拓扑排序**：按依赖关系分组
3. **同组可并发**：同一阶段内的任务无相互依赖，可并发执行

## 槽位命名规则

同一子代理多次调用时分配编号：
- python-agent-01, python-agent-02, python-agent-03
- rust-agent-01, rust-agent-02
- ui-agent-01

## 返回格式

创建完成后返回：

```yaml
status: success
impl_file: "Record/impl.md"
stages:
  - stage: 1
    slots: ["python-agent-01", "rust-agent-01"]
  - stage: 2
    slots: ["python-agent-02"]
  - stage: 3
    slots: ["ui-agent-01"]
summary: "已创建 impl.md，共 4 个任务分 3 个阶段"
```

## 输出任务清单（供用户查看）

```markdown
## 子代理任务清单

| 阶段 | 运行槽位 | 子代理 | proposal_id | 负责工作 | 依赖 |
|------|---------|-------|-------------|---------|------|
| 1 | python-agent-01 | python-agent | data-proc-python-agent | 数据处理模块 | 无 |
| 1 | rust-agent-01 | rust-agent | core-algo-rust-agent | 核心算法 | 无 |
| 2 | python-agent-02 | python-agent | api-impl-python-agent | API接口 | python-agent-01 |
| 3 | ui-agent-01 | ui-agent | frontend-ui-agent | 前端界面 | python-agent-02 |

## 执行说明

Claude 主对话将自动：
1. 按阶段并发调用编程子代理
2. 更新 impl.md 状态（打钩/删除线）
3. 阶段完成后自动进入下一阶段
4. 全部完成后调用 build-agent 编译
```

## impl.md 示例

```markdown
# 实现任务表

创建时间：2026-01-08T10:30:00+08:00
项目根目录：/home/user/my-project
plan_version：v1.0.0

## 任务清单

- [ ] python-agent-01: 数据处理模块 (proposal: data-proc-python-agent, 依赖: 无)
- [ ] rust-agent-01: 核心算法 (proposal: core-algo-rust-agent, 依赖: 无)
- [ ] python-agent-02: API接口 (proposal: api-impl-python-agent, 依赖: python-agent-01)
- [ ] ui-agent-01: 前端界面 (proposal: frontend-ui-agent, 依赖: python-agent-02)

## 分组

### 阶段1（无依赖）
- python-agent-01
- rust-agent-01

### 阶段2（依赖阶段1）
- python-agent-02

### 阶段3（依赖阶段2）
- ui-agent-01
```
