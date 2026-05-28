# 压缩示例

## 技能描述示例

### 示例 1: 文档处理技能
```
压缩前 (89 tokens):
"此技能提供全面的文档创建、编辑和分析能力，完全支持修订跟踪、注释、格式保留和文本提取。当 Claude 需要以 .docx 格式处理专业文档时使用此技能，用于以下任何任务:从零开始创建新文档、修改或编辑现有内容、使用修订跟踪和版本历史，或向文档添加注释和批注。"

压缩后 (24 tokens):
"Word (.docx) 处理器: 创建/编辑/分析。特性: 修订跟踪、注释、格式。触发词: document, docx, Word, report, edit document"

比例: 3.7:1
```

### 示例 2: 数据分析技能
```
压缩前 (67 tokens):
"此技能使用户能够执行数据分析任务，包括读取 CSV 和 Excel 文件、执行统计计算、创建可视化以及生成报告。当用户询问分析数据、创建图表或处理电子表格时应触发此技能。"

压缩后 (19 tokens):
"数据分析: CSV/Excel → 统计/可视化/报告。
触发词: analyze data, chart, spreadsheet, statistics, plot"

比例: 3.5:1
```

## 上下文压缩示例

### 示例 1: 多轮开发对话
```
压缩前 (312 tokens):
用户: "你好!我正在做一个新项目，需要一些帮助。"
助手: "当然!我很乐意帮忙。你在做什么类型的项目?"
用户: "我正在构建一个任务管理 web 应用。类似 Todoist 但更简单。"
助手: "好主意!你在想使用什么技术栈?"
用户: "我在想前端用 React，但我不确定后端用什么。你推荐什么?"
助手: "对于任务管理应用，你有几个不错的选择。带 Express 的 Node.js 很流行，而且全用 JavaScript。带 FastAPI 的 Python 是另一个不错的选择，如果你更喜欢 Python。Django 功能更全面。"
用户: "让我们用 FastAPI，因为我更熟悉 Python。"
助手: "极好的选择!FastAPI 速度快，文档很好，会自动生成 API 文档。我们应该从数据模型开始吗?"
用户: "是的，但我还需要用户认证。我们可以用 JWT 吗?"
助手: "当然可以!JWT 非常适合。我们还需要设置密码哈希。"

压缩后 (52 tokens) - DICE 格式:
[目标] 构建任务管理 web 应用(Todoist 简化版)
[状态] 技术栈已定: React 前端 + FastAPI 后端
[约束] 用户更熟悉 Python > JS；需要认证
[决策] JWT 用于认证，FastAPI 用于后端
[下一步] 设计数据模型，然后实现 JWT 认证

比例: 6:1
```

### 示例 2: 调试会话
```
压缩前 (198 tokens):
用户: "我的 API 有时返回 500 错误"
助手: "让我帮忙调试。你能分享错误日志吗?"
用户: "这是追踪: [长追踪信息]"
助手: "我看到数据库连接错误。你在使用连接池吗?"
用户: "不确定，让我检查...不，我每次请求都创建新连接"
助手: "这可能就是问题。负载下，你会耗尽连接。"
用户: "怎么修复?"
助手: "使用 SQLAlchemy 的连接池。设置 pool_size=5, max_overflow=10"
用户: "修复了!但现在查询很慢"
助手: "让我们添加查询日志来识别慢查询"

压缩后 (41 tokens) - DICE 格式:
[目标] 修复 API 500 错误
[状态] 根本原因: DB 连接耗尽(无连接池)
[已修复] 添加 SQLAlchemy 池(size=5, overflow=10)
[新问题] 慢查询已识别
[下一步] 添加查询日志，优化慢查询

比例: 4.8:1
```

## 输出压缩示例

### 示例 1: 代码审查分析
```
压缩前 (L2 - 180 tokens):
"代码审查发现了几个问题。首先，用户搜索函数中存在潜在的 SQL 注入漏洞，用户输入直接连接到查询字符串中。其次，错误处理不一致 - 有些函数在错误时返回 None，而其他函数抛出异常。第三，认证中间件中存在大量代码重复，可以重构。第四，几个函数超过 50 行，应该分解。最后，测试覆盖率只有 45%，没有边缘情况测试。应该优先立即修复 SQL 注入，然后标准化错误处理，再解决代码质量问题。"

L1 (48 tokens):
"严重: user_search 中的 SQL 注入(立即修复)
高: 不一致的错误处理(None vs 异常)
中: 认证中间件重复，长函数
低: 45% 测试覆盖率，无边缘情况测试
行动: SQLi 修复 → 错误标准化 → 重构"

L0 (12 tokens):
"严重: 立即修复 user_search 中的 SQL 注入"

比例: L2→L1 = 3.75:1, L2→L0 = 15:1
```

### 示例 2: 研究总结
```
压缩前 (L2 - 156 tokens):
"分析了项目的三个数据库选项。PostgreSQL 提供强大的 ACID 合规性、出色的 JSON 支持，团队具有现有专业知识。成本估计 RDS 上 $200/月。MongoDB 提供灵活的模式和水平扩展，但缺少财务数据所需的事务支持。成本估计 $180/月。MySQL 成本效益高，$120/月，但 JSON 支持较弱，团队需要培训。建议: PostgreSQL，尽管成本较高，但由于事务要求和团队熟悉度。JSON 列支持将处理我们的半结构化元数据需求。"

L1 (38 tokens):
"数据库比较:
- PostgreSQL: ACID ✓，JSON ✓，团队经验 ✓，$200/月 → 推荐
- MongoDB: 灵活但无 ACID ×，$180/月
- MySQL: 便宜 $120/月但 JSON 弱，需要培训"

L0 (9 tokens):
"使用 PostgreSQL: ACID + JSON + 团队专业知识"

比例: L2→L1 = 4.1:1, L2→L0 = 17.3:1
```

## 代码压缩示例

### 仅签名模式
```python
# 压缩前 (142 tokens)
class UserService:
    def __init__(self, db: Database, cache: Redis):
        self.db = db
        self.cache = cache
        self.logger = logging.getLogger(__name__)

    def get_user(self, user_id: str) -> Optional[User]:
        """通过 ID 获取用户，首先检查缓存。"""
        cached = self.cache.get(f"user:{user_id}")
        if cached:
            return User.from_json(cached)
        user = self.db.query(User).filter_by(id=user_id).first()
        if user:
            self.cache.set(f"user:{user_id}", user.to_json(), ex=3600)
        return user

    def create_user(self, email: str, name: str) -> User:
        """创建新用户并进行邮箱验证。"""
        if not self._validate_email(email):
            raise ValueError("无效邮箱")
        user = User(email=email, name=name)
        self.db.add(user)
        self.db.commit()
        return user

# 压缩后 (38 tokens)
class UserService:
    def __init__(self, db: Database, cache: Redis): ...
    def get_user(self, user_id: str) -> Optional[User]: ...
    def create_user(self, email: str, name: str) -> User: ...

比例: 3.7:1
```

### 接口 + 文档字符串模式
```python
# 压缩后 (52 tokens) - 保留意图
class UserService:
    """带有 Redis 缓存的用户 CRUD。"""
    def __init__(self, db: Database, cache: Redis): ...
    def get_user(self, user_id: str) -> Optional[User]:
        """获取用户，缓存优先(1小时 TTL)。"""
    def create_user(self, email: str, name: str) -> User:
        """创建用户并进行邮箱验证。"""

比例: 2.7:1 (保留更多上下文)
```

## 文档压缩示例

### 目录模式
```
压缩前: 3200字的 API 文档

压缩后 (67 tokens):
# API 文档摘要
1. 认证 - JWT 不记名令牌，1小时过期
2. 用户 - CRUD 端点，支持分页
3. 任务 - 创建/更新/删除，批量操作可用
4. Webhooks - 事件订阅，重试策略 3 次
5. 速率限制 - 每个 API 密钥 1000 请求/小时
6. 错误 - 标准 HTTP 代码，body 中的 error_code
```

### 实体关系模式
```yaml
# 压缩前: 2500字的系统架构文档

# 压缩后 (45 tokens):
entities:
  services: [api-gateway, user-svc, task-svc, notification-svc]
  data: [PostgreSQL, Redis, S3]
  infra: [K8s, ALB, CloudWatch]
flow:
  request → gateway → service → db
  async: service → queue → notification
deps:
  user-svc → PostgreSQL, Redis
  task-svc → PostgreSQL, S3
```
