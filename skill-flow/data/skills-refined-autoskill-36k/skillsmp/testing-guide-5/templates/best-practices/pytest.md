# pytest 最佳实践

Python 测试框架的质量约束和最佳实践。

---

## 项目配置

### pyproject.toml（推荐）

```toml
[tool.pytest.ini_options]
# 测试目录
testpaths = ["tests"]

# 文件匹配
python_files = ["test_*.py", "*_test.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]

# 默认选项
addopts = [
    "-v",                    # 详细输出
    "--strict-markers",      # 严格标记检查
    "--tb=short",            # 简短回溯
    "-ra",                   # 显示所有非通过测试的摘要
]

# 标记定义
markers = [
    "slow: 标记慢速测试",
    "integration: 集成测试",
    "unit: 单元测试",
]

# 最小版本
minversion = "7.0"

# 过滤警告
filterwarnings = [
    "error",                          # 将警告视为错误
    "ignore::DeprecationWarning",     # 忽略弃用警告
]

[tool.coverage.run]
source = ["src"]
branch = true
omit = [
    "*/tests/*",
    "*/__init__.py",
]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise NotImplementedError",
    "if TYPE_CHECKING:",
]
fail_under = 80
show_missing = true
```

### pytest.ini（传统方式）

```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = -v --strict-markers --tb=short
markers =
    slow: 慢速测试
    integration: 集成测试
```

---

## 测试结构规范

### 目录组织

```
project/
├── src/
│   └── myapp/
│       ├── __init__.py
│       ├── services/
│       │   └── user_service.py
│       └── utils/
│           └── validators.py
├── tests/
│   ├── conftest.py              # 共享 fixtures
│   ├── unit/                    # 单元测试
│   │   ├── conftest.py
│   │   ├── test_user_service.py
│   │   └── test_validators.py
│   ├── integration/             # 集成测试
│   │   ├── conftest.py
│   │   └── test_api.py
│   └── e2e/                     # 端到端测试
│       └── test_workflows.py
├── pyproject.toml
└── conftest.py                  # 根级 fixtures
```

### 测试文件结构

```python
# tests/unit/test_user_service.py
"""UserService 单元测试"""

import pytest
from myapp.services.user_service import UserService
from myapp.exceptions import UserNotFoundError, DuplicateEmailError


class TestUserServiceCreateUser:
    """createUser 方法测试"""

    def test_应该创建用户并返回用户对象(self, user_service, mock_db):
        """正常创建用户"""
        # Arrange
        user_data = {"email": "test@example.com", "name": "Test"}

        # Act
        result = user_service.create_user(user_data)

        # Assert
        assert result["email"] == "test@example.com"
        assert result["name"] == "Test"
        assert "id" in result
        mock_db.insert.assert_called_once()

    def test_应该拒绝重复的邮箱(self, user_service, mock_db):
        """邮箱重复时抛出异常"""
        mock_db.find_one.return_value = {"id": "1", "email": "test@example.com"}

        with pytest.raises(DuplicateEmailError, match="邮箱已存在"):
            user_service.create_user({"email": "test@example.com"})

    def test_应该处理数据库错误(self, user_service, mock_db):
        """数据库错误时抛出异常"""
        mock_db.insert.side_effect = Exception("DB Error")

        with pytest.raises(Exception, match="DB Error"):
            user_service.create_user({"email": "test@example.com"})


class TestUserServiceGetUser:
    """getUser 方法测试"""

    def test_应该返回用户当用户存在时(self, user_service, mock_db):
        mock_db.find_one.return_value = {"id": "1", "name": "Test"}

        result = user_service.get_user("1")

        assert result["name"] == "Test"

    def test_应该返回None当用户不存在时(self, user_service, mock_db):
        mock_db.find_one.return_value = None

        result = user_service.get_user("999")

        assert result is None
```

---

## 断言最佳实践

### 推荐的断言方式

```python
# ✅ 具体值断言
assert result["status"] == "success"
assert result["count"] == 5
assert user.name == "Test User"

# ✅ 近似值断言（浮点数）
assert result == pytest.approx(3.14, rel=1e-2)
assert values == pytest.approx([0.1, 0.2, 0.3], abs=0.01)

# ✅ 集合断言
assert "apple" in result["items"]
assert len(result["items"]) == 3
assert set(result["items"]) == {"apple", "banana", "orange"}

# ✅ 字典断言
assert result == {"id": "1", "name": "Test"}
assert result.items() >= {"name": "Test"}.items()  # 包含检查

# ✅ 异常断言
with pytest.raises(ValueError):
    validate(None)

with pytest.raises(ValueError, match="must be positive"):
    validate(-1)

with pytest.raises(ValueError) as exc_info:
    validate(-1)
assert "positive" in str(exc_info.value)

# ✅ 警告断言
with pytest.warns(DeprecationWarning):
    deprecated_function()

# ✅ 类型断言
assert isinstance(result, User)
assert hasattr(result, "email")
```

### 禁止的断言方式

```python
# ❌ 弱断言
assert result is not None
assert result  # truthy 检查
assert bool(result)
assert result != None  # 应该用 is not None

# ❌ 没有断言
def test_something():
    result = do_something()
    # 没有 assert！

# ❌ 断言过于宽松
assert type(result) == dict  # 应该检查内容
assert len(result) > 0       # 应该检查具体值
```

---

## Fixtures 最佳实践

### 基础 Fixtures

```python
# conftest.py
import pytest
from unittest.mock import Mock, MagicMock

@pytest.fixture
def mock_db():
    """数据库 Mock"""
    db = Mock()
    db.find_one.return_value = None
    db.find_many.return_value = []
    db.insert.return_value = {"id": "new-id"}
    return db

@pytest.fixture
def user_service(mock_db):
    """UserService 实例"""
    from myapp.services.user_service import UserService
    return UserService(db=mock_db)

@pytest.fixture
def sample_user():
    """示例用户数据"""
    return {
        "id": "user-1",
        "email": "test@example.com",
        "name": "Test User",
        "role": "user",
    }
```

### Fixture 作用域

```python
# function - 每个测试函数执行一次（默认）
@pytest.fixture
def fresh_data():
    return {"count": 0}

# class - 每个测试类执行一次
@pytest.fixture(scope="class")
def db_connection():
    conn = create_connection()
    yield conn
    conn.close()

# module - 每个测试模块执行一次
@pytest.fixture(scope="module")
def expensive_resource():
    resource = create_expensive_resource()
    yield resource
    resource.cleanup()

# session - 整个测试会话执行一次
@pytest.fixture(scope="session")
def docker_container():
    container = start_container()
    yield container
    container.stop()
```

### Fixture 工厂

```python
@pytest.fixture
def create_user():
    """用户工厂 fixture"""
    created_users = []

    def _create_user(email="test@example.com", name="Test", **kwargs):
        user = {
            "id": f"user-{len(created_users) + 1}",
            "email": email,
            "name": name,
            **kwargs,
        }
        created_users.append(user)
        return user

    yield _create_user

    # 清理
    for user in created_users:
        # cleanup logic
        pass

# 使用
def test_multiple_users(create_user):
    user1 = create_user(email="user1@example.com")
    user2 = create_user(email="user2@example.com")
    admin = create_user(email="admin@example.com", role="admin")

    assert user1["email"] != user2["email"]
```

### Fixture 参数化

```python
@pytest.fixture(params=["sqlite", "postgresql", "mysql"])
def database(request):
    """参数化数据库 fixture"""
    db_type = request.param
    db = create_database(db_type)
    yield db
    db.cleanup()

# 使用此 fixture 的测试会运行 3 次
def test_query(database):
    result = database.query("SELECT 1")
    assert result is not None
```

---

## Mock 最佳实践

### 使用 unittest.mock

```python
from unittest.mock import Mock, MagicMock, patch, call

# 创建 Mock
mock_service = Mock()
mock_service.get_user.return_value = {"id": "1", "name": "Test"}

# MagicMock（支持魔术方法）
mock_dict = MagicMock()
mock_dict["key"] = "value"
mock_dict.__len__.return_value = 1

# 设置返回值
mock_fn = Mock()
mock_fn.return_value = "result"
mock_fn.side_effect = [1, 2, 3]  # 依次返回
mock_fn.side_effect = ValueError("error")  # 抛出异常

# 验证调用
mock_fn("arg1", "arg2")
mock_fn.assert_called()
mock_fn.assert_called_once()
mock_fn.assert_called_with("arg1", "arg2")
mock_fn.assert_called_once_with("arg1", "arg2")
assert mock_fn.call_count == 1
assert mock_fn.call_args == call("arg1", "arg2")
assert mock_fn.call_args_list == [call("arg1", "arg2")]
```

### 使用 patch

```python
from unittest.mock import patch

# 作为装饰器
@patch("myapp.services.user_service.send_email")
def test_create_user_sends_email(mock_send_email, user_service):
    user_service.create_user({"email": "test@example.com"})
    mock_send_email.assert_called_once()

# 作为上下文管理器
def test_with_patch():
    with patch("myapp.services.external_api.fetch") as mock_fetch:
        mock_fetch.return_value = {"data": "mocked"}
        result = my_function()
        assert result == {"data": "mocked"}

# patch 对象属性
@patch.object(UserService, "validate_email", return_value=True)
def test_with_patched_method(mock_validate):
    # ...
    pass

# patch 字典
@patch.dict("os.environ", {"API_KEY": "test-key"})
def test_with_env():
    import os
    assert os.environ["API_KEY"] == "test-key"
```

### 使用 pytest-mock

```python
# 安装: pip install pytest-mock

def test_with_mocker(mocker):
    # mocker 是 pytest-mock 提供的 fixture
    mock_fn = mocker.patch("myapp.services.external_api.fetch")
    mock_fn.return_value = {"data": "mocked"}

    result = my_function()

    assert result == {"data": "mocked"}
    mock_fn.assert_called_once()

def test_spy(mocker):
    # spy 真实对象
    spy = mocker.spy(user_service, "validate_email")

    user_service.create_user({"email": "test@example.com"})

    spy.assert_called_with("test@example.com")
```

---

## 参数化测试

```python
# 基础参数化
@pytest.mark.parametrize("input,expected", [
    ("test@example.com", True),
    ("invalid", False),
    ("", False),
    ("user@domain.org", True),
])
def test_validate_email(input, expected):
    assert validate_email(input) == expected

# 多参数
@pytest.mark.parametrize("a,b,expected", [
    (1, 2, 3),
    (0, 0, 0),
    (-1, 1, 0),
    (100, 200, 300),
])
def test_add(a, b, expected):
    assert add(a, b) == expected

# 使用 ids 提高可读性
@pytest.mark.parametrize("email,valid", [
    pytest.param("test@example.com", True, id="valid_email"),
    pytest.param("invalid", False, id="no_at_sign"),
    pytest.param("", False, id="empty_string"),
], ids=str)
def test_validate_email_with_ids(email, valid):
    assert validate_email(email) == valid

# 参数化 fixture
@pytest.fixture(params=[
    pytest.param("admin", id="admin_role"),
    pytest.param("user", id="user_role"),
    pytest.param("guest", id="guest_role"),
])
def user_role(request):
    return request.param

def test_permissions(user_role):
    user = create_user(role=user_role)
    # 测试会运行 3 次
```

### 组合参数化

```python
@pytest.mark.parametrize("x", [1, 2])
@pytest.mark.parametrize("y", [10, 20])
def test_combinations(x, y):
    # 测试会运行 4 次: (1,10), (1,20), (2,10), (2,20)
    assert x + y > 0
```

---

## 异步测试

```python
# 安装: pip install pytest-asyncio

import pytest

# 标记异步测试
@pytest.mark.asyncio
async def test_async_function():
    result = await async_fetch_data()
    assert result["status"] == "success"

# 异步 fixture
@pytest.fixture
async def async_client():
    async with AsyncClient() as client:
        yield client

@pytest.mark.asyncio
async def test_with_async_client(async_client):
    response = await async_client.get("/api/users")
    assert response.status_code == 200

# 配置 asyncio mode
# pyproject.toml
[tool.pytest.ini_options]
asyncio_mode = "auto"  # 自动标记异步测试
```

---

## 测试数据库

### 使用事务回滚

```python
@pytest.fixture
def db_session():
    """数据库会话（事务回滚）"""
    session = SessionLocal()
    session.begin_nested()  # 开始嵌套事务

    yield session

    session.rollback()  # 回滚所有更改
    session.close()

def test_create_user(db_session):
    user = User(email="test@example.com")
    db_session.add(user)
    db_session.flush()

    assert user.id is not None
    # 测试结束后自动回滚
```

### 使用测试数据库

```python
@pytest.fixture(scope="session")
def test_db():
    """创建测试数据库"""
    # 创建测试数据库
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)

    yield engine

    engine.dispose()

@pytest.fixture
def db_session(test_db):
    """每个测试的数据库会话"""
    Session = sessionmaker(bind=test_db)
    session = Session()

    yield session

    session.rollback()
    session.close()
```

---

## 运行命令

```bash
# 基础命令
pytest                              # 运行所有测试
pytest tests/unit/                  # 运行特定目录
pytest tests/unit/test_user.py     # 运行特定文件
pytest tests/unit/test_user.py::test_create  # 运行特定测试

# 匹配测试名
pytest -k "create"                  # 匹配包含 "create" 的测试
pytest -k "create and not delete"   # 组合匹配

# 标记筛选
pytest -m "unit"                    # 运行标记为 unit 的测试
pytest -m "not slow"                # 排除 slow 标记

# 覆盖率
pytest --cov=src                    # 覆盖率报告
pytest --cov=src --cov-report=html  # HTML 报告
pytest --cov=src --cov-fail-under=80  # 覆盖率门槛

# 并行运行（需要 pytest-xdist）
pytest -n auto                      # 自动检测 CPU 核心数
pytest -n 4                         # 使用 4 个进程

# 调试
pytest -v                           # 详细输出
pytest -vv                          # 更详细输出
pytest -s                           # 显示 print 输出
pytest --pdb                        # 失败时进入调试器
pytest --pdb-first                  # 第一个失败时进入调试器
pytest -x                           # 第一个失败后停止
pytest --lf                         # 只运行上次失败的测试
pytest --ff                         # 先运行上次失败的测试

# 报告
pytest --tb=short                   # 简短回溯
pytest --tb=long                    # 完整回溯
pytest --tb=no                      # 无回溯
pytest -ra                          # 显示所有非通过测试摘要
```

---

## 常用插件

```toml
# pyproject.toml
[project.optional-dependencies]
test = [
    "pytest>=7.0",
    "pytest-cov",        # 覆盖率
    "pytest-asyncio",    # 异步测试
    "pytest-mock",       # Mock 增强
    "pytest-xdist",      # 并行运行
    "pytest-timeout",    # 超时控制
    "pytest-randomly",   # 随机顺序
    "pytest-sugar",      # 美化输出
    "pytest-env",        # 环境变量
    "factory-boy",       # 测试数据工厂
    "faker",             # 假数据生成
    "freezegun",         # 时间冻结
    "responses",         # HTTP Mock
    "httpx",             # 异步 HTTP 测试
]
```

### 时间冻结

```python
from freezegun import freeze_time

@freeze_time("2024-01-01")
def test_with_frozen_time():
    from datetime import datetime
    assert datetime.now() == datetime(2024, 1, 1)

@freeze_time("2024-01-01")
class TestWithFrozenTime:
    def test_something(self):
        # 整个类都使用冻结的时间
        pass
```

### HTTP Mock

```python
import responses

@responses.activate
def test_api_call():
    responses.add(
        responses.GET,
        "https://api.example.com/users/1",
        json={"id": 1, "name": "Test"},
        status=200,
    )

    result = fetch_user(1)

    assert result["name"] == "Test"
    assert len(responses.calls) == 1
```
