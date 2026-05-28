# Level 3: Complete Modules Examples

Production-ready modules with error handling, logging, tests. Includes code review, refactoring, and comprehensive testing tasks using `gpt-5.2-codex` model (auto-selected). Parallel execution with task decomposition.

---

## Example 1: HTTP Client Module

Complete HTTP client with retry logic, timeout handling, and interceptors.

### Command

```bash
memex-cli run --backend codex --stdin <<'EOF'
---TASK---
id: http-client
backend: codex
workdir: /home/user/lib
model: gpt-5.2-codex
timeout: 120
---CONTENT---
Python HTTP客户端封装：支持重试、超时、请求拦截器、响应拦截器
---END---
EOF
```

### Expected Output

```
▶ http-client (codex/gpt-5.2-codex)

```python
import requests
from typing import Optional, Dict, Callable
from functools import wraps
import time
import logging

logger = logging.getLogger(__name__)

class HTTPClient:
    """可配置的HTTP客户端"""

    def __init__(self, base_url: str = "", timeout: int = 30, max_retries: int = 3):
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.max_retries = max_retries
        self.session = requests.Session()

        # 拦截器列表
        self.request_interceptors = []
        self.response_interceptors = []

    def add_request_interceptor(self, func: Callable):
        """添加请求拦截器"""
        self.request_interceptors.append(func)

    def add_response_interceptor(self, func: Callable):
        """添加响应拦截器"""
        self.response_interceptors.append(func)

    def _apply_request_interceptors(self, method: str, url: str, **kwargs):
        """应用请求拦截器"""
        for interceptor in self.request_interceptors:
            method, url, kwargs = interceptor(method, url, **kwargs)
        return method, url, kwargs

    def _apply_response_interceptors(self, response):
        """应用响应拦截器"""
        for interceptor in self.response_interceptors:
            response = interceptor(response)
        return response

    def request(self, method: str, path: str, **kwargs):
        """发送HTTP请求（支持重试）"""
        url = f"{self.base_url}{path}" if self.base_url else path
        method, url, kwargs = self._apply_request_interceptors(method, url, **kwargs)

        last_error = None
        for attempt in range(self.max_retries):
            try:
                response = self.session.request(
                    method,
                    url,
                    timeout=self.timeout,
                    **kwargs
                )
                return self._apply_response_interceptors(response)

            except (requests.Timeout, requests.ConnectionError) as e:
                last_error = e
                logger.warning(f"Request failed (attempt {attempt + 1}/{self.max_retries}): {e}")
                if attempt < self.max_retries - 1:
                    time.sleep(2 ** attempt)  # 指数退避

        raise last_error

    def get(self, path: str, **kwargs):
        return self.request("GET", path, **kwargs)

    def post(self, path: str, **kwargs):
        return self.request("POST", path, **kwargs)

    def put(self, path: str, **kwargs):
        return self.request("PUT", path, **kwargs)

    def delete(self, path: str, **kwargs):
        return self.request("DELETE", path, **kwargs)
```

» 写入 http_client.py
✓ http-client 8.2s
```

### Usage

```python
from http_client import HTTPClient

# 创建客户端
client = HTTPClient(base_url="https://api.example.com", max_retries=3)

# 添加认证拦截器
def auth_interceptor(method, url, **kwargs):
    kwargs.setdefault('headers', {})['Authorization'] = 'Bearer TOKEN'
    return method, url, kwargs

client.add_request_interceptor(auth_interceptor)

# 发送请求
response = client.get("/users/123")
print(response.json())
```

### Customization Tips

- Add rate limiting: Track requests per second
- Support circuit breaker pattern
- Add request/response logging interceptor
- Cache GET responses with TTL

---

## Example 2: Database Helper Module

SQLite utility with connection pooling, transaction management, and query builder.

### Command

```bash
memex-cli run --backend codex --stdin <<'EOF'
---TASK---
id: db-helper
backend: codex
workdir: /home/user/lib
model: gpt-5.2-codex
timeout: 120
---CONTENT---
SQLite工具类：连接池管理、事务上下文、简单查询构建器、自动重连
---END---
EOF
```

### Expected Output

```
▶ db-helper (codex/gpt-5.2-codex)

```python
import sqlite3
from contextlib import contextmanager
from typing import List, Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

class DatabaseHelper:
    """SQLite数据库助手"""

    def __init__(self, db_path: str, pool_size: int = 5):
        self.db_path = db_path
        self.pool_size = pool_size
        self.connection_pool = []

    def _get_connection(self):
        """从连接池获取连接"""
        if self.connection_pool:
            return self.connection_pool.pop()
        return sqlite3.connect(self.db_path)

    def _return_connection(self, conn):
        """归还连接到池"""
        if len(self.connection_pool) < self.pool_size:
            self.connection_pool.append(conn)
        else:
            conn.close()

    @contextmanager
    def transaction(self):
        """事务上下文管理器"""
        conn = self._get_connection()
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            logger.error(f"Transaction failed: {e}")
            raise
        finally:
            self._return_connection(conn)

    def execute(self, query: str, params: tuple = ()) -> List[Dict]:
        """执行查询并返回结果"""
        with self.transaction() as conn:
            cursor = conn.execute(query, params)
            columns = [desc[0] for desc in cursor.description] if cursor.description else []
            return [dict(zip(columns, row)) for row in cursor.fetchall()]

    def execute_many(self, query: str, params_list: List[tuple]):
        """批量执行"""
        with self.transaction() as conn:
            conn.executemany(query, params_list)

    class QueryBuilder:
        """简单查询构建器"""

        def __init__(self, table: str):
            self.table = table
            self.where_clauses = []
            self.order_by = None
            self.limit_value = None

        def where(self, condition: str):
            self.where_clauses.append(condition)
            return self

        def order(self, column: str, desc: bool = False):
            self.order_by = f"{column} {'DESC' if desc else 'ASC'}"
            return self

        def limit(self, n: int):
            self.limit_value = n
            return self

        def build_select(self) -> str:
            query = f"SELECT * FROM {self.table}"
            if self.where_clauses:
                query += " WHERE " + " AND ".join(self.where_clauses)
            if self.order_by:
                query += f" ORDER BY {self.order_by}"
            if self.limit_value:
                query += f" LIMIT {self.limit_value}"
            return query
```

» 写入 db_helper.py
✓ db-helper 9.1s
```

### Usage

```python
from db_helper import DatabaseHelper

db = DatabaseHelper("app.db")

# 使用事务
with db.transaction() as conn:
    conn.execute("INSERT INTO users (name, email) VALUES (?, ?)", ("Alice", "alice@example.com"))

# 查询数据
users = db.execute("SELECT * FROM users WHERE age > ?", (18,))

# 使用查询构建器
query = db.QueryBuilder("users").where("age > 18").order("created_at", desc=True).limit(10)
results = db.execute(query.build_select())
```

---

## Code Quality Tasks

### Example 3: Code Review

Analyze existing code for security issues, performance bottlenecks, and improvement suggestions.

#### Command

```bash
memex-cli run --backend codex --stdin <<'EOF'
---TASK---
id: code-review
backend: codex
workdir: /home/user/project
model: gpt-5.2-codex
files: ./src/auth.py, ./src/user.py
files-mode: ref
---CONTENT---
审查这段代码：
1. 指出安全隐患（SQL注入、XSS、密码存储等）
2. 识别性能瓶颈（N+1查询、低效算法）
3. 提出改进建议（设计模式、代码结构）
---END---
EOF
```

#### Expected Output

```
▶ code-review (codex/gpt-5.2-codex)
  📄 src/auth.py (1.8KB)
  📄 src/user.py (2.1KB)

## 代码审查报告

### 安全问题 🔴

1. **auth.py:23** - SQL注入风险
   ```python
   # 当前代码
   query = f"SELECT * FROM users WHERE email = '{email}'"

   # 建议修改
   query = "SELECT * FROM users WHERE email = ?"
   cursor.execute(query, (email,))
   ```

2. **auth.py:45** - 密码明文存储
   ```python
   # 当前代码
   db.insert("users", {"password": password})

   # 建议修改
   import bcrypt
   hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
   db.insert("users", {"password": hashed})
   ```

### 性能问题 🟡

1. **user.py:67** - N+1查询问题
   ```python
   # 当前代码
   for user in users:
       user.posts = db.query(f"SELECT * FROM posts WHERE user_id = {user.id}")

   # 建议修改（使用JOIN或批量查询）
   user_ids = [u.id for u in users]
   posts = db.query("SELECT * FROM posts WHERE user_id IN (?)", user_ids)
   posts_by_user = group_by(posts, 'user_id')
   for user in users:
       user.posts = posts_by_user.get(user.id, [])
   ```

2. **auth.py:89** - 每次请求都查询数据库
   ```python
   # 建议添加缓存
   from functools import lru_cache

   @lru_cache(maxsize=100)
   def get_user_permissions(user_id):
       return db.query("SELECT * FROM permissions WHERE user_id = ?", (user_id,))
   ```

### 改进建议 💡

1. **auth.py** - 应用Repository模式分离数据访问逻辑
2. **user.py** - 添加输入验证装饰器
3. 全局 - 添加日志记录和错误监控
4. 全局 - 编写单元测试（当前覆盖率0%）

### 优先级

- 🔴 高优先级：修复SQL注入和密码存储（安全风险）
- 🟡 中优先级：优化N+1查询（性能影响）
- 💡 低优先级：架构改进（可维护性）

✓ code-review 5.2s
```

#### Customization Tips

- Add specific security checklist (OWASP Top 10)
- Check coding standards compliance (PEP 8, ESLint)
- Generate code complexity metrics (cyclomatic complexity)
- Suggest refactoring opportunities (code smells)

---

### Example 4: Refactoring

Improve code quality by applying design patterns, extracting common logic, and enhancing testability.

#### Command

```bash
memex-cli run --stdin <<'EOF'
---TASK---
id: refactor
backend: codex
workdir: /home/user/project
model: gpt-5.2-codex
files: ./src/legacy.py
files-mode: ref
---CONTENT---
重构这段代码：
1. 应用设计模式（如Strategy、Factory、Observer）
2. 提取公共逻辑，减少重复代码
3. 改善可测试性（依赖注入、接口抽象）
4. 改进错误处理和边界情况
---END---
EOF
```

#### Expected Output

```
▶ refactor (codex/gpt-5.2-codex)
  📄 src/legacy.py (3.5KB)

## 重构报告

### 原始代码问题

1. **God Object反模式** - `OrderProcessor`类承担过多职责（验证、计算、支付、通知）
2. **硬编码依赖** - 直接实例化第三方服务，难以测试
3. **重复代码** - 价格计算逻辑在3处重复
4. **缺少错误处理** - 支付失败时未回滚状态

### 重构后代码

```python
# payment_strategy.py - 策略模式
from abc import ABC, abstractmethod

class PaymentStrategy(ABC):
    @abstractmethod
    def process(self, amount: float) -> bool:
        pass

class CreditCardPayment(PaymentStrategy):
    def process(self, amount: float) -> bool:
        # 信用卡支付逻辑
        return True

class AlipayPayment(PaymentStrategy):
    def process(self, amount: float) -> bool:
        # 支付宝支付逻辑
        return True

# price_calculator.py - 提取公共逻辑
class PriceCalculator:
    """价格计算服务（单一职责）"""

    def __init__(self, tax_rate: float = 0.1):
        self.tax_rate = tax_rate

    def calculate_total(self, items: list) -> float:
        subtotal = sum(item.price * item.quantity for item in items)
        tax = subtotal * self.tax_rate
        return subtotal + tax

# order_processor.py - 依赖注入
class OrderProcessor:
    """订单处理器（依赖注入提升可测试性）"""

    def __init__(
        self,
        calculator: PriceCalculator,
        payment: PaymentStrategy,
        notifier: Notifier
    ):
        self.calculator = calculator
        self.payment = payment
        self.notifier = notifier

    def process_order(self, order: Order) -> bool:
        """处理订单（带错误处理）"""
        try:
            # 计算总价
            total = self.calculator.calculate_total(order.items)

            # 执行支付
            if not self.payment.process(total):
                raise PaymentError("Payment failed")

            # 更新状态
            order.status = "paid"
            order.save()

            # 发送通知
            self.notifier.notify(f"Order {order.id} completed")

            return True

        except Exception as e:
            # 回滚状态
            order.status = "failed"
            order.save()
            logger.error(f"Order processing failed: {e}")
            return False

# 使用示例（依赖注入）
calculator = PriceCalculator(tax_rate=0.1)
payment = CreditCardPayment()
notifier = EmailNotifier()

processor = OrderProcessor(calculator, payment, notifier)
processor.process_order(order)
```

### 改进总结

✓ 应用策略模式 - 支付方式可扩展
✓ 单一职责原则 - 每个类只负责一件事
✓ 依赖注入 - 易于单元测试（可mock依赖）
✓ 错误处理 - 支付失败时正确回滚

### 测试改进

重构后可以轻松编写单元测试：

```python
def test_order_processing():
    # Mock依赖
    mock_calculator = Mock(spec=PriceCalculator)
    mock_payment = Mock(spec=PaymentStrategy)
    mock_notifier = Mock(spec=Notifier)

    mock_calculator.calculate_total.return_value = 100.0
    mock_payment.process.return_value = True

    # 测试
    processor = OrderProcessor(mock_calculator, mock_payment, mock_notifier)
    result = processor.process_order(order)

    assert result == True
    mock_payment.process.assert_called_once_with(100.0)
```

✓ refactor 12.4s
```

#### Customization Tips

- Specify target design patterns in prompt
- Preserve backward compatibility (add migration guide)
- Generate refactoring checklist
- Include performance comparison (before/after)

---

### Example 5: Comprehensive Unit Testing

Write full test coverage for complex modules including edge cases and error scenarios.

#### Command

```bash
memex-cli run --stdin <<'EOF'
---TASK---
id: write-tests
backend: codex
workdir: /home/user/project
model: gpt-5.2-codex
files: ./src/calculator.py
files-mode: ref
---CONTENT---
为calculator.py编写完整pytest测试用例：
1. 覆盖所有公共方法（正常路径 + 边界情况）
2. 测试错误处理（异常、无效输入）
3. 使用参数化测试减少重复
4. 达到>90%代码覆盖率
---END---
EOF
```

#### Expected Output

```
▶ write-tests (codex/gpt-5.2-codex)
  📄 src/calculator.py (2.3KB)

```python
import pytest
from calculator import Calculator

class TestCalculator:
    """Calculator全面测试套件"""

    @pytest.fixture
    def calc(self):
        """测试夹具：每个测试前创建新实例"""
        return Calculator()

    # 正常路径测试
    def test_add_positive_numbers(self, calc):
        assert calc.add(2, 3) == 5

    def test_subtract_positive_numbers(self, calc):
        assert calc.subtract(5, 3) == 2

    def test_multiply(self, calc):
        assert calc.multiply(4, 3) == 12

    def test_divide(self, calc):
        assert calc.divide(10, 2) == 5.0

    # 边界情况测试
    def test_add_zero(self, calc):
        assert calc.add(5, 0) == 5

    def test_multiply_by_zero(self, calc):
        assert calc.multiply(5, 0) == 0

    def test_divide_by_one(self, calc):
        assert calc.divide(10, 1) == 10.0

    def test_add_negative_numbers(self, calc):
        assert calc.add(-5, -3) == -8

    # 错误处理测试
    def test_divide_by_zero_raises_error(self, calc):
        with pytest.raises(ZeroDivisionError):
            calc.divide(10, 0)

    def test_invalid_input_type(self, calc):
        with pytest.raises(TypeError):
            calc.add("5", 3)

    # 参数化测试（减少重复代码）
    @pytest.mark.parametrize("a,b,expected", [
        (0, 0, 0),
        (1, 1, 2),
        (-1, 1, 0),
        (100, 200, 300),
        (0.1, 0.2, pytest.approx(0.3)),  # 浮点数精度
    ])
    def test_add_parametrized(self, calc, a, b, expected):
        assert calc.add(a, b) == expected

    @pytest.mark.parametrize("a,b,expected", [
        (10, 2, 5.0),
        (7, 2, 3.5),
        (1, 3, pytest.approx(0.333, rel=1e-2)),
        (-10, 2, -5.0),
    ])
    def test_divide_parametrized(self, calc, a, b, expected):
        assert calc.divide(a, b) == expected

    # 高级功能测试
    def test_chain_operations(self, calc):
        """测试链式操作"""
        result = calc.add(5, 3)
        result = calc.multiply(result, 2)
        assert result == 16

    def test_precision(self, calc):
        """测试浮点数精度"""
        result = calc.divide(1, 3)
        assert abs(result - 0.333333) < 1e-5

    # 性能测试（可选）
    @pytest.mark.performance
    def test_add_performance(self, calc, benchmark):
        """基准测试：确保add操作足够快"""
        benchmark(calc.add, 1000000, 1)
```

» 写入 test_calculator.py
✓ write-tests 6.7s
```

#### Usage

```bash
# 运行所有测试
pytest test_calculator.py -v

# 生成覆盖率报告
pytest test_calculator.py --cov=calculator --cov-report=html

# 只运行参数化测试
pytest test_calculator.py -k "parametrized"

# 跳过性能测试
pytest test_calculator.py -m "not performance"
```

#### Customization Tips

- Add integration tests (database, API calls)
- Use `pytest-mock` for mocking dependencies
- Add property-based testing with `hypothesis`
- Generate test data with `faker`

---

## Example 6: Auto Task Decomposition + Dependency Analysis + Parallel Execution

This example demonstrates L3 full capabilities: automatic task decomposition, dependency analysis, and parallel execution.

### Single Task Input (Auto-Decomposed)

```bash
memex-cli run --backend codex --stdin <<'EOF'
---TASK---
id: cache-manager
backend: codex
model: gpt-5.2-codex
workdir: ./lib
timeout: 180
---CONTENT---
创建完整的缓存管理模块：
1. 缓存接口抽象 (cache/interface.py)
2. 内存缓存实现 (cache/memory.py)
3. Redis缓存实现 (cache/redis.py)
4. 缓存装饰器 (cache/decorators.py)
5. 完整单元测试 (tests/test_cache.py)

要求：
- 支持TTL过期
- 支持缓存穿透保护
- 线程安全
- 完整类型注解
---END---
EOF
```

### Auto-Decomposition Process

```
▶ Task Decomposition Analysis
  Input: 1 complex task
  Detected Components: 5 files
  Generated Subtasks: 5

  Decomposition Strategy:
  ┌──────────────────────────────────────────────────┐
  │ Original Task: cache-manager                      │
  │                                                   │
  │ Subtasks Generated:                               │
  │   1. cache-manager-interface (interface.py)       │
  │   2. cache-manager-memory (memory.py)             │
  │   3. cache-manager-redis (redis.py)               │
  │   4. cache-manager-decorators (decorators.py)     │
  │   5. cache-manager-tests (test_cache.py)          │
  └──────────────────────────────────────────────────┘
```

### Auto-Generated Dependency Graph

```
▶ Dependency Analysis
  Implicit Dependencies Detected:
    - memory.py imports interface.py
    - redis.py imports interface.py
    - decorators.py imports interface.py
    - test_cache.py imports all modules

  Generated DAG:

Phase 1: Foundation (No deps)
┌──────────────────────┐
│ cache-manager-       │
│ interface            │
│ (interface.py)       │
│ 2.8s                 │
└──────────┬───────────┘
           │
           ↓
Phase 2: Implementations (Parallel, depends on Phase 1)
┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐
│ cache-manager-   │  │ cache-manager-   │  │ cache-manager-   │
│ memory           │  │ redis            │  │ decorators       │
│ (memory.py)      │  │ (redis.py)       │  │ (decorators.py)  │
│ 3.2s             │  │ 3.5s             │  │ 2.9s             │
└────────┬─────────┘  └────────┬─────────┘  └────────┬─────────┘
         │                     │                     │
         └─────────────────────┼─────────────────────┘
                               ↓
Phase 3: Testing (Depends on Phase 2)
              ┌──────────────────────┐
              │ cache-manager-tests  │
              │ (test_cache.py)      │
              │ 4.1s                 │
              └──────────────────────┘
```

### Execution Output

```
▶ Executing cache-manager with auto-decomposition

▶ Phase 1: Foundation
  » cache-manager-interface

  ```python
  from abc import ABC, abstractmethod
  from typing import Any, Optional

  class CacheInterface(ABC):
      """缓存接口抽象"""

      @abstractmethod
      def get(self, key: str) -> Optional[Any]:
          """获取缓存值"""
          pass

      @abstractmethod
      def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
          """设置缓存值"""
          pass

      @abstractmethod
      def delete(self, key: str) -> bool:
          """删除缓存"""
          pass

      @abstractmethod
      def exists(self, key: str) -> bool:
          """检查键是否存在"""
          pass
  ```
  » 写入 cache/interface.py
  ✓ cache-manager-interface 2.8s

▶ Phase 2: Implementations (3 tasks parallel)
  » Executing 3 tasks in parallel...

  ✓ cache-manager-memory 3.2s
    » 写入 cache/memory.py
  ✓ cache-manager-redis 3.5s
    » 写入 cache/redis.py
  ✓ cache-manager-decorators 2.9s
    » 写入 cache/decorators.py

▶ Phase 3: Testing
  » cache-manager-tests
  ✓ cache-manager-tests 4.1s
    » 写入 tests/test_cache.py

═══════════════════════════════════════════════════════════
✓ cache-manager completed
  Subtasks: 5
  Total Time: 10.4s (vs 16.5s serial = 37% faster)
  Files Generated:
    - cache/interface.py
    - cache/memory.py
    - cache/redis.py
    - cache/decorators.py
    - tests/test_cache.py
═══════════════════════════════════════════════════════════
```

### Comparison: L2 vs L3 Execution

| Feature | L2 | L3 |
|---------|:--:|:--:|
| Dependency Analysis | ✅ | ✅ |
| Parallel Execution | ✅ | ✅ |
| **Task Decomposition** | ❌ | ✅ |
| Single task → Multiple files | ❌ | ✅ |
| Auto-detect implicit deps | ❌ | ✅ |

**L3 Key Advantage:** Single complex task is automatically decomposed into multiple subtasks with proper dependency ordering.

---

## Model Selection for Level 3

| Task Type | Model | Execution |
|-----------|-------|-----------|
| Standard modules | `gpt-5.2-codex` | Parallel with decomposition |
| Code review | `gpt-5.2-codex` | Parallel analysis |
| Large refactoring | `gpt-5.2` | Auto-decomposition + parallel |
| Comprehensive tests | `gpt-5.2-codex` | Parallel test generation |

**L3 Execution Features:**
- Automatic task decomposition (single task → multiple subtasks)
- Implicit dependency detection (import analysis)
- Parallel execution of independent subtasks
- Phase-based execution scheduling

**When to upgrade to Level 4**:
- Algorithm optimization needed
- Complex data structures required
- Performance-critical code (O(log n) complexity)

---

## Tips for Level 3 Tasks

1. **Use files-mode: ref** for code review/refactoring to include source code
2. **Set longer timeout**: 120-180s for complex modules
3. **Review generated code**: Check for security issues before production
4. **Add logging**: Include logging statements in production modules
5. **Write tests first**: Consider TDD approach for new modules

---

## Related Resources

- [references/complexity-guide.md](../references/complexity-guide.md) - Level 3 detailed guidance
- [examples/level2-utilities.md](./level2-utilities.md) - Simpler utilities
- [examples/level4-algorithms.md](./level4-algorithms.md) - Complex algorithms
- [skills/memex-cli/SKILL.md](../../memex-cli/SKILL.md) - Memex CLI usage
