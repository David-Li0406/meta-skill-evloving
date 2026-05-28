# /ohspec:spike - 可行性验证阶段（可选）

## 命令说明
启动可行性验证阶段，由**原型师**专家负责通过探针验证技术可行性。

## 触发条件
- RFC metadata 中 `needs_spike: true`
- 或用户主动调用

## 使用方式
```bash
/ohspec:spike RFC-20240101-120000
```

## 工作流程

### 步骤1：读取 RFC
读取 RFC §1-§2，理解需要验证的内容：
```python
rfc_path = f".ohspec/rfcs/{RFC_ID}/rfc.md"
rfc_content = read_file(rfc_path)
```

### 步骤2：启动原型师 Subagent
使用 Task 工具启动独立上下文的 Subagent：

```python
Task(
    subagent_type="general-purpose",
    description="可行性验证阶段",
    prompt=f"""
你现在是 OHSpec 专家组的**原型师**。

## 你的 Persona
{读取 personas/extension/prototyper.md}

## 当前任务
RFC：{RFC_ID}
需要验证的内容：{从 RFC §2 提取不确定性}

## 工作目录
RFC 目录：{RFC_DIR}

## 你的任务
1. 设计探针验证方案
2. 执行探针验证（只读，不修改代码）
3. 收集性能数据
4. 输出可行性报告到 RFC §2

## 输出要求
- 更新 {RFC_DIR}/rfc.md §2.可行性报告
- 更新 {RFC_DIR}/findings.json（性能数据）
- 更新 {RFC_DIR}/progress.json

## 完成标准
- 技术可行性已验证
- 性能可行性已验证
- 风险已识别
""",
    model="sonnet"
)
```

### 步骤3：用户门禁
Subagent 完成后，向用户展示可行性报告：
```
可行性验证完成！

## 验证结果
- 技术可行性：✅ 可行 / ❌ 不可行
- 性能可行性：✅ 可行 / ⚠️ 有风险
- 资源可行性：✅ 可接受 / ❌ 超预算

## 性能数据
[展示性能基准测试结果]

## 风险评估
[展示识别的风险]

请确认：
✅ 可行性验证通过，继续设计
❌ 不可行，需要调整需求
```

### 步骤4：更新 RFC 状态
用户确认后，更新 RFC 状态：
```yaml
status: ANALYZED → SPIKE_DONE
next_phase: design
```

## 输出物
- `{RFC_DIR}/rfc.md` - §2.可行性报告（新增）
- `{RFC_DIR}/findings.json` - 性能基准数据（更新）
- `{RFC_DIR}/progress.json` - 验证过程记录（更新）

## 失败处理
如果验证不通过：
1. 记录失败原因到 progress.json
2. 标记 RFC 状态为 `SPIKE_FAILED`
3. 建议用户调整需求或放弃

## 下一步
- 验证通过 → `/ohspec:design`
- 验证失败 → 返回 `/ohspec:analyze` 调整需求
