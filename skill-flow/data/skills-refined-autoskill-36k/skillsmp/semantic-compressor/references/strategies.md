# 压缩策略

## 1. 技能描述压缩

### 触发词保留算法
```
1. 提取触发词(文件扩展名、动作动词、领域术语)
2. 移除填充词: "此技能"、"帮助你"、"允许用户"、"在...时使用"
3. 转换句子 → 带分隔符的关键词列表
4. 合并同义词: "create/make/generate" → "create"
5. 验证: 确保所有原始触发词仍然存在
```

### 压缩模式
| 模式 | 压缩前 | 压缩后 |
|---------|--------|-------|
| 被动 → 主动 | "can be used to edit" | "edit" |
| 冗长触发词 | "Use this when working with" | "用于:" |
| 冗余类别 | "file types including .pdf, .docx" | ".pdf/.docx" |
| 功能列表 | "supports X, Y, and Z" | "X/Y/Z" |

## 2. DICE 上下文压缩

### 丢弃规则
- 问候语: "Hi"、"Hello"、"Thanks"
- 确认: "Got it"、"Sure"、"I understand"
- 失败的尝试: 仅保留最终有效方法
- 重复: 仅保留首次提及
- 元评论: "让我想想..."、"我会尝试..."

### 隐式转换
```
显式: "用户说他们想构建 REST API"
隐式: goal=REST_API

显式: "用户更喜欢 Python 而非 JavaScript"
隐式: lang=Python

显式: "他们提到需要快速"
隐式: constraint=perf
```

### 合并模板
```
多轮决策:
  用户: "我们应该用 React 吗?"
  助手: "React 或 Vue 都可以"
  用户: "让我们用 React"
  → decision: framework=React

错误恢复:
  助手: [尝试 X，失败]
  助手: [尝试 Y，失败]
  助手: [尝试 Z，成功]
  → approach=Z (X,Y 失败)
```

### 提取模式
```yaml
facts:
  - type: requirement|decision|constraint|blocker
    key: short_identifier
    value: compressed_value
    confidence: high|medium|low
```

## 3. 分层输出压缩

### L0 超短(<15 tokens)
单个可操作的见解或决策。
```
输入: [500 字的数据库选项分析]
L0: "使用 PostgreSQL: 最适合 ACID + JSON 需求"
```

### L1 简短(<50 tokens)
关键发现为简洁列表。
```
L1: "数据库选择: PostgreSQL
    - ACID 合规 ✓
    - JSON 支持 ✓
    - 团队专业知识 ✓
    - 成本: ~$200/月"
```

### L2 标准(<200 tokens)
带上下文的结构化摘要。
```
L2: "## 建议: PostgreSQL

选择 PostgreSQL 而非 MongoDB(缺少 ACID)和 MySQL(JSON 较弱)。

关键因素:
1. 事务要求 → 需要 ACID
2. 半结构化数据 → 需要 JSON 列
3. 团队具有 Postgres 经验

权衡: 更高的运维复杂度 vs. 灵活性。

下一步: 配置 RDS 实例，估计 $200/月"
```

## 4. 代码压缩模式

### 仅签名
```python
# 压缩前
def calculate_total(items: List[Item], tax_rate: float = 0.1) -> float:
    """计算含税总价。"""
    subtotal = sum(item.price * item.quantity for item in items)
    return subtotal * (1 + tax_rate)

# 压缩后(仅签名)
def calculate_total(items: List[Item], tax_rate: float = 0.1) -> float: ...
```

### 接口模式
```python
# 仅提取公共 API
class OrderService:
    def create_order(self, items: List[Item]) -> Order: ...
    def get_order(self, order_id: str) -> Optional[Order]: ...
    def cancel_order(self, order_id: str) -> bool: ...
    # 私有方法已省略
```

### 增量模式
```diff
# 仅更改 + 最少上下文
class OrderService:
    # ... 未更改 ...
+   def refund_order(self, order_id: str, reason: str) -> Refund:
+       """新增: 处理订单退款。"""
+       ...
    # ... 未更改 ...
```

## 5. 文档压缩模式

### 目录模式
```
# 原始: 5000 字的技术规范
# 压缩后:
1. 概述 - 系统处理实时事件处理
2. 架构 - Kafka + Flink 管道
3. 数据模型 - 包含 12 个字段的事件模式
4. API - 用于摄取/查询的 REST 端点
5. 部署 - 带自动扩展的 K8s
6. 监控 - Prometheus + Grafana 仪表板
```

### 实体模式
```yaml
entities:
  systems: [Kafka, Flink, PostgreSQL, Redis]
  actions: [摄取、处理、存储、查询]
  constraints: [<100ms 延迟, 10k 事件/秒]
  stakeholders: [数据团队、平台团队]
relations:
  - Kafka → Flink: 流
  - Flink → PostgreSQL: 持久化
  - Redis: 缓存层
```

## 6. 压缩质量指标

### 信息保留分数
```
IRS = (压缩后关键事实 / 压缩前关键事实) * 100

目标:
- 技能描述: IRS > 95%
- 上下文交接: IRS > 85%
- 报告摘要: IRS > 80%
```

### 可操作性分数
```
AS = 保留的可操作项目 / 原始可操作项目

所有压缩应保持 AS = 100%
(压缩中永远不要丢失操作项目)
```
