# analyze 阶段 - 需求分析

## 概述

**目标**：理解用户需求，基于 Dispatcher **基线扫描（scan-of-record）**澄清歧义，输出 RFC §1-§2。  
默认不做全量扫描，仅在“证据缺口”触发时提出补扫请求。

**执行者**：需求分析师子代理

**输入**：用户需求、findings.json（含 confirmed.key_files + confirmed.facts）、progress.json（ASSESS 决策）

**输出**：RFC §1-§2、findings.json（澄清记录/风险/假设）

---

## 执行流程

### 步骤 1：读取上下文

读取必要的上下文文件：
- `progress.json` - 获取 ASSESS 阶段的工具/策略建议（供补扫时复用）
- `findings.json` - 获取 Dispatcher 基线扫描结果（scan-of-record）
- 用户需求原文

### 步骤 2：验证基线证据（强制，先于任何产出）

检查 `findings.confirmed.key_files` 是否满足：
- 数量：≥ 3
- 覆盖面：入口/配置/依赖（或测试/可观测）

**不满足则禁止进入澄清与写作**：直接返回 `blocked`，并给出补扫建议（模块/关键词/缺失角色）。  
> 目标是“基于证据提问与建模”，而不是“先写再补证据”。

同时检查 `findings.confirmed.facts`（项目事实提炼）：
- 建议：≥3（配置/存储/权限/错误码/线程模型/可观测等）
- MEDIUM/COMPLEX：事实缺失视为证据缺口，优先补齐再继续

### 步骤 3：需求澄清（必须先于产出）

基于基线证据，向用户提出选项式问题（如有必要）。  
**若存在未决问题，必须停止并等待用户澄清，不得进入设计或审查。**

> 记录到 findings.json 的 `working.pending_questions` 与 progress.json 的提问区。

**批次控制（用户体验门禁）**：
- 每轮最多 **5** 个问题（优先问 critical）
- 结构：第 1 轮只问“会改变契约/默认行为/兼容性/权限/多用户/外部依赖”的关键决策
- 用户可选“跳过剩余问题，先按默认推进”，但必须在 RFC 的“未决项”里标红，并在 audit 阶段视为阻断（不得 approve）

### 步骤 3.5：加载竞品分析（如需要）

检查 `progress.json` 中的 `needs_competitive_analysis` 标志：

```python
if progress.get("needs_competitive_analysis"):
    platforms = progress.get("competitive_platforms", ["android"])

    for platform in platforms:
        # 读取 knowledge-base 文档
        kb_path = f"knowledge-base/{platform}/"
        docs = []

        # 根据需求类型选择相关文档
        if "API" in requirement or "接口" in requirement:
            docs.append(f"{kb_path}api-design.md")
        if "架构" in requirement or "architecture" in requirement:
            docs.append(f"{kb_path}architecture.md")
        if "性能" in requirement or "performance" in requirement:
            docs.append(f"{kb_path}performance.md")
        if "安全" in requirement or "security" in requirement:
            docs.append(f"{kb_path}security.md")

        # 读取文档内容并提炼要点
        key_points = []
        for doc in docs:
            content = Read(doc)
            # 提炼 3-5 条关键要点（在子代理中完成）
            points = extract_key_points(content, max_points=5)
            key_points.extend(points)

        # 追加到 findings.json（只写摘要，不写完整文档）
        findings["competitive_analysis"] = {
            "platform": platform,
            "source": "local_knowledge_base",
            "key_points": key_points,  # 只包含要点，不包含完整文档
            "documents_referenced": docs  # 记录引用的文档路径
        }
```

**上下文监控**（重要）：
```python
# 在加载竞品分析前，检查当前上下文使用量
# 注意：这是伪代码，实际实现需要 Claude Code 提供上下文监控 API
current_usage_ratio = estimate_context_usage()

if current_usage_ratio > 0.70:  # 超过 70%
    # 跳过竞品分析，避免爆上下文
    findings["competitive_analysis"] = {
        "skipped": True,
        "reason": "上下文预算不足（已使用 > 70%），已跳过竞品分析"
    }
    # 记录到 progress.json
    progress["warnings"].append({
        "phase": "analyze",
        "type": "context_budget_exceeded",
        "message": "跳过竞品分析以避免上下文溢出"
    })
    return  # 跳过竞品分析
```

写入 findings.json：
```json
{
  "competitive_analysis": {
    "platform": "android",
    "source": "local_knowledge_base",
    "key_points": [
      "Android AudioManager 使用 requestAudioFocus() 管理音频焦点",
      "建议使用 AUDIOFOCUS_GAIN_TRANSIENT 处理短暂音频",
      "需要实现 OnAudioFocusChangeListener 处理焦点变化",
      "支持 AudioAttributes 定义音频用途和内容类型",
      "遵循 DUCK 模式降低其他音频音量而不是完全停止"
    ],
    "documents_referenced": [
      "knowledge-base/android/api-design.md"
    ]
  }
}
```

**Token 成本**：
- 完整文档：2000-3000 tokens/文档
- 提炼要点：200-300 tokens（5 条要点）
- **节省 90% 的上下文消耗**

### 步骤 4：生成 RFC §1-§2

根据扫描结果和用户反馈，生成：
- §1.1 元数据
- §1.2 背景
- §2.1 功能需求
- §2.2 约束条件

**模板锁定（强制）**：
- 只能在既有 `rfc.md`（由 `templates/rfc.md` 初始化）里“填空/增量更新”
- **禁止**：重排章节结构、另起“§1 需求概述/§2 现状分析”等自定义目录、自动生成“目录/TOC”、贴大量实现代码
- 若发现 `rfc.md` 不是模板骨架（例如开头不是 `# RFC:`），必须先退回到 init 阶段修复骨架（否则后续 precheck/audit 必然失败）

### 步骤 5：更新状态

更新 `progress.json`：
- `phases.analyze.status` = "complete"
- `phases.analyze.completed_at` = 当前时间
- 若存在未决问题，标记 gate 未通过并暂停流转
- 如触发补扫，记录补扫原因与范围（避免重复全量扫描）

---

## 注意事项

1. **不做重复全量扫描**：默认只消费 Dispatcher 基线扫描结果；缺口才补扫
2. **禁止假设**：找不到证据就阻断/补扫，不得编造设置键/接口/默认值
3. **澄清前置**：未决问题清零前不得进入设计/审查
