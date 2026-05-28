# 分级上下文传递机制

本文档定义 Subagent 间上下文传递的分级模型和压缩策略。

---

## 分级定义

| 级别 | 内容 | Token 预算 | 传递时机 |
|------|------|-----------|---------|
| L0 | 核心元数据 | ~100 | 必传 |
| L1 | 关键决策 | ~300 | 必传 |
| L2 | 扫描摘要 | ~500 | 按需 |
| L3 | 详细分析 | ~2000+ | 按需读取 |

---

## 各级别内容说明

### L0: 核心元数据 (~100 tokens)

最小必需信息，任何 Subagent 调用都必须包含。

```json
{
  "rfc_id": "RFC-20260116-audio-toggle-a3f2",
  "phase": "design",
  "intent": "为音频服务增加 3D 音效开关",
  "complexity": "MEDIUM"
}
```

**包含字段**:
- `rfc_id`: RFC 标识符
- `phase`: 当前阶段
- `intent`: 一句话需求描述
- `complexity`: 复杂度级别

### L1: 关键决策 (~300 tokens)

已确认的技术决策、约束与“项目事实”（scan-of-record 提炼），影响后续设计的核心信息。

```json
{
  "decisions": [
    {"id": "D001", "decision": "使用 WebAudio API", "rationale": "原生支持，无额外依赖"}
  ],
  "facts": [
    {"id": "FACT-001", "fact": "配置项通过 Settings DB 读取并监听变更", "evidence": ["main@HEAD:path#Lline"]}
  ],
  "constraints": {
    "technical": ["需兼容 Chrome 90+"],
    "scope": ["不支持 IE11"]
  }
}
```

**包含字段**:
- `decisions`: 已确认的技术决策
- `facts`: 项目事实（必须可追溯到锚点）
- `constraints`: 技术/业务/范围约束

### L2: 扫描摘要 (~500 tokens)

代码扫描的关键发现，按需传递。

```json
{
  "key_files": [
    {"path": "main@HEAD:src/audio/service.ts#L1", "role": "entry"},
    {"path": "main@HEAD:src/audio/config.ts#L1", "role": "config"}
  ],
  "dependencies": {
    "internal": ["AudioManager"],
    "external": ["howler@2.2.0"]
  }
}
```

**包含字段**:
- `key_files`: 关键文件列表（路径 + 角色）
- `dependencies`: 内部/外部依赖

### L3: 详细分析 (~2000+ tokens)

完整扫描结果，不直接传递，通过文件路径引用。

```json
{
  "file_ref": "{rfc_dir}/findings.json",
  "sections": ["working.scan_results", "references"]
}
```

**访问方式**: Subagent 按需读取 `findings.json` 指定分区。

---

## 压缩策略

### minimal: 仅 L0

适用场景：简单任务、快速模式、Token 紧张时。

```json
{
  "strategy": "minimal",
  "content": { /* L0 */ }
}
```

### standard: L0 + L1 + L2

适用场景：标准流程、大多数阶段转换。

```json
{
  "strategy": "standard",
  "content": {
    /* L0 */,
    /* L1 */,
    /* L2 */
  }
}
```

### full: L0 + L1 + L2 + L3

适用场景：复杂任务、需要完整上下文、审查阶段。

```json
{
  "strategy": "full",
  "content": {
    /* L0 */,
    /* L1 */,
    /* L2 */
  },
  "file_refs": {
    "findings": "{rfc_dir}/findings.json",
    "rfc": "{rfc_dir}/rfc.md"
  }
}
```

---

## 重要性评分机制

### 评分算法

基于相关性的重要性评分用于动态调整上下文压缩级别。评分算法综合考虑内容的依赖关系、技术栈相关性、时间新鲜度和被引用程度。

**评分公式**：

```
总分 = 直接依赖×5 + 技术栈相关×3 + 时间相关×2 + 被引用次数×4
```

### 评分维度详解

#### 1. 直接依赖（权重：5）

**定义**：内容被其他内容直接引用或依赖的次数。

**计算方法**：
- 统计该内容在 `confirmed.dependencies` 中被引用的次数
- 统计该内容在 `confirmed.key_files` 中作为依赖被列出的次数
- 统计该内容在 `confirmed.decisions` 中被直接引用的次数

**示例**：
```json
{
  "path": "src/audio/service.ts",
  "direct_dependencies": 3,
  "score_contribution": 3 * 5 = 15
}
```

**权重说明**：权重最高（5），因为直接依赖最能反映内容的核心重要性。

#### 2. 技术栈相关（权重：3）

**定义**：内容与当前项目技术栈的相关程度。

**计算方法**：
- 检查内容是否涉及项目的核心技术栈（如框架、语言、关键库）
- 相关：1 分；不相关：0 分
- 高度相关（如当前阶段的关键技术）：2 分

**示例**：
```json
{
  "path": "src/audio/config.ts",
  "tech_stack_relevance": 2,
  "score_contribution": 2 * 3 = 6,
  "reason": "涉及项目核心的音频配置系统"
}
```

**权重说明**：权重中等（3），因为技术栈相关性影响内容对当前任务的适用性。

#### 3. 时间相关（权重：2）

**定义**：内容的新鲜度或与当前阶段的时间距离。

**计算方法**：
- 计算内容最后修改时间与当前时间的差距
- 最近 7 天内修改：2 分
- 最近 30 天内修改：1 分
- 30 天以上未修改：0 分

**示例**：
```json
{
  "path": "src/audio/service.ts",
  "last_modified": "2026-01-15T10:30:00Z",
  "time_relevance": 2,
  "score_contribution": 2 * 2 = 4,
  "reason": "最近修改，反映最新的实现状态"
}
```

**权重说明**：权重较低（2），因为时间相关性不如依赖关系稳定，但仍需考虑。

#### 4. 被引用次数（权重：4）

**定义**：内容在文档、代码或决策中被引用的总次数。

**计算方法**：
- 统计内容在 RFC 文档中被引用的次数
- 统计内容在其他 findings 中被引用的次数
- 统计内容在决策记录中被提及的次数

**示例**：
```json
{
  "path": "src/audio/service.ts",
  "reference_count": 5,
  "score_contribution": 5 * 4 = 20,
  "reason": "在多个决策和设计文档中被引用"
}
```

**权重说明**：权重较高（4），因为被引用次数反映了内容的广泛影响力。

### 评分范围和含义

**评分说明**：评分是相对的，用于比较不同内容的重要性。在实际应用中，通常计算所有内容的评分后，按相对排名确定压缩策略。

#### 评分分布和策略映射

| 相对排名 | 评分特征 | 压缩策略 | 说明 |
|---------|---------|---------|------|
| 前 20% | 最高分 | full | 必须包含所有级别，完整传递 |
| 前 50% | 较高分 | standard | 包含 L0+L1+L2，满足大多数需求 |
| 后 50% | 较低分 | minimal | 仅包含 L0，其他内容按需加载 |

#### 绝对评分参考

基于以下假设的绝对评分范围（仅供参考）：
- 直接依赖最多 8 个（权重 5）→ 最多 40 分
- 技术栈相关最多 2 分（权重 3）→ 最多 6 分
- 时间相关最多 2 分（权重 2）→ 最多 4 分
- 被引用最多 12 次（权重 4）→ 最多 48 分
- **理论最大分数**：约 100 分

| 绝对评分范围 | 含义 | 压缩策略 | 说明 |
|-------------|------|---------|------|
| 80-100 | 极高重要性 | full | 必须包含所有级别，完整传递 |
| 50-79 | 高重要性 | standard | 包含 L0+L1+L2，满足大多数需求 |
| 20-49 | 中等重要性 | standard | 包含 L0+L1+L2，可选择性压缩 L2 |
| 1-19 | 低重要性 | minimal | 仅包含 L0，其他内容按需加载 |
| 0 | 极低重要性 | minimal | 仅包含 L0，可考虑归档 |

### 评分算法实现

```python
from datetime import datetime, timedelta
import json

def calculate_importance_score(
    content_item: dict,
    findings: dict,
    rfc_dir: str
) -> dict:
    """
    计算内容的重要性评分

    参数:
        content_item: 内容项（如文件、决策等）
        findings: findings.json 内容
        rfc_dir: RFC 目录路径

    返回:
        包含评分和各维度贡献的字典
    """
    score = 0
    contributions = {}

    # 维度1：直接依赖（权重×5）
    direct_deps = count_direct_dependencies(content_item, findings)
    direct_dep_score = direct_deps * 5
    contributions["direct_dependencies"] = {
        "count": direct_deps,
        "weight": 5,
        "score": direct_dep_score
    }
    score += direct_dep_score

    # 维度2：技术栈相关（权重×3）
    tech_relevance = assess_tech_stack_relevance(content_item, findings)
    tech_score = tech_relevance * 3
    contributions["tech_stack_relevance"] = {
        "relevance": tech_relevance,
        "weight": 3,
        "score": tech_score
    }
    score += tech_score

    # 维度3：时间相关（权重×2）
    time_relevance = assess_time_relevance(content_item)
    time_score = time_relevance * 2
    contributions["time_relevance"] = {
        "relevance": time_relevance,
        "weight": 2,
        "score": time_score
    }
    score += time_score

    # 维度4：被引用次数（权重×4）
    ref_count = count_references(content_item, findings, rfc_dir)
    ref_score = ref_count * 4
    contributions["reference_count"] = {
        "count": ref_count,
        "weight": 4,
        "score": ref_score
    }
    score += ref_score

    return {
        "total_score": score,
        "contributions": contributions,
        "compression_strategy": determine_strategy(score),
        "calculated_at": datetime.now().isoformat()
    }


def count_direct_dependencies(content_item: dict, findings: dict) -> int:
    """统计直接依赖次数"""
    count = 0
    item_id = content_item.get("id") or content_item.get("path")

    # 检查 confirmed.dependencies
    for dep_list in findings.get("confirmed", {}).get("dependencies", {}).values():
        if isinstance(dep_list, list):
            count += sum(1 for dep in dep_list if dep.get("id") == item_id or dep.get("path") == item_id)

    # 检查 confirmed.decisions 中的引用
    for decision in findings.get("confirmed", {}).get("decisions", []):
        if item_id in str(decision):
            count += 1

    return count


def assess_tech_stack_relevance(content_item: dict, findings: dict) -> int:
    """评估技术栈相关性"""
    # 获取项目技术栈关键词
    tech_keywords = findings.get("dispatcher", {}).get("tech_stack", [])
    content_text = json.dumps(content_item)

    # 计算匹配度
    matches = sum(1 for keyword in tech_keywords if keyword.lower() in content_text.lower())

    if matches >= 2:
        return 2  # 高度相关
    elif matches == 1:
        return 1  # 相关
    else:
        return 0  # 不相关


def assess_time_relevance(content_item: dict) -> int:
    """评估时间相关性"""
    last_modified = content_item.get("last_modified")
    if not last_modified:
        return 0

    try:
        modified_time = datetime.fromisoformat(last_modified)
        days_ago = (datetime.now() - modified_time).days

        if days_ago <= 7:
            return 2  # 最近 7 天
        elif days_ago <= 30:
            return 1  # 最近 30 天
        else:
            return 0  # 30 天以上
    except (ValueError, TypeError):
        return 0


def count_references(content_item: dict, findings: dict, rfc_dir: str) -> int:
    """统计被引用次数"""
    count = 0
    item_id = content_item.get("id") or content_item.get("path")
    search_text = json.dumps(findings)

    # 计算在 findings 中的引用次数
    count += search_text.count(item_id)

    # 如果有 RFC 文件，也统计其中的引用
    try:
        with open(f"{rfc_dir}/rfc.md", 'r', encoding='utf-8') as f:
            rfc_content = f.read()
            count += rfc_content.count(item_id)
    except (FileNotFoundError, IOError):
        pass

    return count


def determine_strategy(score: int) -> str:
    """根据评分确定压缩策略"""
    if score >= 90:
        return "full"
    elif score >= 50:
        return "standard"
    else:
        return "minimal"
```

### 动态压缩策略调整

#### 调整规则

1. **初始策略选择**：根据阶段推荐策略（见下表）选择基础策略
2. **评分调整**：计算关键内容的重要性评分
3. **策略升级**：如果评分 ≥ 90，升级到 full 策略
4. **策略降级**：如果评分 < 50 且 Token 预算紧张，降级到 minimal 策略

#### 调整流程

```python
def adjust_compression_strategy(
    base_strategy: str,
    importance_scores: dict,
    token_budget_ratio: float
) -> str:
    """
    根据重要性评分和 Token 预算动态调整压缩策略

    参数:
        base_strategy: 基础策略（来自阶段推荐）
        importance_scores: 各内容的重要性评分
        token_budget_ratio: Token 使用率（0-1）

    返回:
        调整后的压缩策略
    """
    # 计算平均评分
    avg_score = sum(s.get("total_score", 0) for s in importance_scores.values()) / len(importance_scores) if importance_scores else 0

    # 策略升级：高评分且 Token 充足
    if avg_score >= 90 and token_budget_ratio < 0.7:
        return "full"

    # 策略降级：低评分且 Token 紧张
    if avg_score < 50 and token_budget_ratio > 0.7:
        return "minimal"

    # 保持基础策略
    return base_strategy
```

### 应用场景

#### 场景1：设计阶段的上下文传递

```python
# 从 analyze 阶段转换到 design 阶段
findings = load_findings(rfc_dir)

# 计算关键文件的重要性评分
key_files_scores = {}
for file_info in findings["confirmed"]["key_files"]:
    score_result = calculate_importance_score(file_info, findings, rfc_dir)
    key_files_scores[file_info["path"]] = score_result

# 根据评分调整压缩策略
base_strategy = "standard"  # 设计阶段推荐策略
adjusted_strategy = adjust_compression_strategy(
    base_strategy,
    key_files_scores,
    token_budget_ratio=0.6
)

# 构建上下文包
context_pack = build_context_pack(rfc_dir, adjusted_strategy)
```

#### 场景2：Token 预算紧张时的智能压缩

```python
# 当 Token 使用率达到 70% 时
if token_usage_ratio >= 0.7:
    # 计算所有内容的重要性评分
    all_scores = {}
    for item in findings["confirmed"]["key_files"]:
        score = calculate_importance_score(item, findings, rfc_dir)
        all_scores[item["path"]] = score

    # 只保留高分内容（≥70）
    high_importance_items = {
        path: score for path, score in all_scores.items()
        if score["total_score"] >= 70
    }

    # 使用 minimal 策略，仅传递高分内容
    compressed_pack = build_minimal_context(high_importance_items)
```

---

## 与 findings.json 分区的映射

| 级别 | findings.json 分区 |
|------|-------------------|
| L0 | `meta` + `requirement.intent` + `dispatcher.complexity` |
| L1 | `confirmed.decisions` + `confirmed.constraints` |
| L2 | `confirmed.key_files` + `confirmed.dependencies` |
| L3 | `working.*` + `references` |

---

## 使用示例

### Orchestrator 构建上下文包

```python
def build_context_pack(rfc_dir: str, strategy: str = "standard") -> dict:
    """
    根据策略构建上下文包

    参数:
        rfc_dir: RFC 目录路径
        strategy: 压缩策略 (minimal/standard/full)

    返回:
        上下文包字典
    """
    import json

    with open(f"{rfc_dir}/findings.json", 'r') as f:
        findings = json.load(f)

    # L0: 必传
    pack = {
        "rfc_id": findings["meta"]["rfc_id"],
        "phase": findings["working"]["phase"],
        "intent": findings["requirement"]["intent"],
        "complexity": findings["dispatcher"]["complexity"]
    }

    if strategy == "minimal":
        return {"strategy": "minimal", "content": pack}

    # L1: 关键决策
    pack["decisions"] = findings["confirmed"]["decisions"]
    pack["constraints"] = findings["confirmed"]["constraints"]

    # L2: 扫描摘要
    pack["key_files"] = findings["confirmed"]["key_files"]
    pack["dependencies"] = findings["confirmed"]["dependencies"]

    if strategy == "standard":
        return {"strategy": "standard", "content": pack}

    # L3: 文件引用
    return {
        "strategy": "full",
        "content": pack,
        "file_refs": {
            "findings": f"{rfc_dir}/findings.json",
            "rfc": f"{rfc_dir}/rfc.md"
        }
    }
```

### Subagent 接收上下文

```python
def load_context(context_pack: dict, rfc_dir: str) -> dict:
    """
    Subagent 加载上下文

    参数:
        context_pack: 上下文包
        rfc_dir: RFC 目录路径

    返回:
        完整上下文
    """
    import json

    context = context_pack["content"].copy()

    # 如果是 full 策略，按需加载文件
    if context_pack.get("strategy") == "full":
        file_refs = context_pack.get("file_refs", {})
        if "findings" in file_refs:
            with open(file_refs["findings"], 'r') as f:
                context["_findings"] = json.load(f)

    return context
```

---

## 阶段推荐策略

| 阶段 | 推荐策略 | 说明 |
|------|---------|------|
| dispatcher | minimal | 初始扫描，无历史上下文 |
| requirement | standard | 需要决策和约束 |
| design | standard | 需要文件和依赖信息 |
| audit | full | 需要完整上下文进行审查 |
| resume | full | 恢复时需要完整状态 |
