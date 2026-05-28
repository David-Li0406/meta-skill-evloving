---
name: api-testing
description: 使用 pytest + httpx 进行 API 接口自动化测试的工具包。支持 RESTful API 测试、JWT 认证、参数化测试、断言验证以及测试报告生成。
---

# API 接口自动化测试

要测试后端 API 接口，请编写原生的 Python pytest + httpx 脚本。

**可用辅助脚本**：
- `scripts/api_client.py` - API 客户端封装（支持认证、请求、响应处理）
- `scripts/with_backend.py` - 管理后端服务器生命周期

**务必先使用 `--help` 运行脚本** 以查看用法。在你先尝试直接运行脚本并确认必须定制之前，不要阅读源码。这些脚本可能非常庞大，会污染你的上下文窗口。

## 决策树：选择你的方法

```
用户任务 → 是否有 OpenAPI/Swagger 文档？
    ├─ 是 → 读取 /docs 或 /openapi.json 获取接口定义
    │         ├─ 成功 → 根据接口定义编写测试脚本
    │         └─ 失败 → 手动分析接口（见下）
    │
    └─ 否 → 后端服务是否已在运行？
        ├─ 否 → 运行：python scripts/with_backend.py --help
        │        然后使用该助手启动服务 + 编写测试脚本
        │
        └─ 是 → 先探测，后测试：
            1. 获取 OpenAPI 文档：GET /openapi.json
            2. 分析接口路径、方法、参数
            3. 编写测试用例覆盖正向/异常场景
            4. 执行测试并验证响应
```

## 项目服务配置

本项目的服务端口配置：

| 服务 | 地址 | 说明 |
|------|------|------|
| 后端 API | `http://localhost:5000` | FastAPI 服务 |
| API 文档 | `http://localhost:5000/docs` | Swagger UI |
| OpenAPI | `http://localhost:5000/openapi.json` | OpenAPI 规范 |

## 示例：使用 with_backend.py

要启动后端服务，先运行 `--help`，然后使用该助手：

**启动后端服务：**
```bash
python scripts/with_backend.py --server "python run.py" --port 5000 -- pytest tests/api/ -v
```

**指定工作目录：**
```bash
python scripts/with_backend.py \
  --server "python run.py" \
  --port 5000 \
  --cwd platform-fastapi-server \
  -- pytest tests/api/test_login.py -v
```

## 示例：使用 api_client.py

编写测试脚本时，使用封装好的 API 客户端：

```python
from scripts.api_client import APIClient

# 创建客户端
client = APIClient(base_url="http://localhost:5000")

# 登录获取 Token
client.login("admin", "admin123")

# 发送请求
response = client.get("/user/queryById", params={"id": 1})
assert response.status_code == 200

data = response.json()
assert data["code"] == 200
assert data["data"]["username"] == "admin"

# 关闭客户端
client.close()
```

## "先探测，后测试"模式

1. **获取接口文档**：
   ```python
   response = client.get("/openapi.json")
   api_spec = response.json()
   paths = api_spec["paths"]  # 所有接口路径
   ```

2. **分析接口定义**：
   ```python
   # 获取某个接口的详细信息
   login_spec = paths["/login"]["post"]
   request_body = login_spec["requestBody"]
   responses = login_spec["responses"]
   ```

3. **编写测试用例**：
   ```python
   def test_login_success():
       response = client.post("/login", json={
           "username": "admin",
           "password": "admin123"
       })
       assert response.json()["code"] == 200
   ```

## pytest 测试脚本模板

```python
# tests/api/test_user.py
import pytest
from scripts.api_client import APIClient

class TestUserAPI:
    """用户管理接口测试"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """测试前置：创建客户端并登录"""
        self.client = APIClient()
        self.client.login()
        yield
        self.client.close()
    
    # ========== 正向测试 ==========
    
    def test_query_user_list(self):
        """查询用户列表"""
        response = self.client.post("/user/queryByPage", json={
            "pageNum": 1,
            "pageSize": 10
        })
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200
        assert "list" in data["data"]
    
    # ========== 异常测试 ==========
    
    def test_query_user_not_found(self):
        """查询不存在的用户"""
        response = self.client.get("/user/queryById", params={"id": 99999})
        data = response.json()
        assert data["data"] is None or data["code"] != 200
    
    # ========== 参数化测试 ==========
    
    @pytest.mark.parametrize("username,password,expected", [
        ("admin", "admin123", True),      # 正确凭证
        ("admin", "wrong", False),         # 错误密码
        ("", "admin123", False),           # 空用户名
    ])
    def test_login_scenarios(self, username, password, expected):
        """登录场景参数化测试"""
        client = APIClient()
        response = client.post("/login", json={
            "username": username,
            "password": password
        })
        data = response.json()
        assert (data["code"] == 200) == expected
        client.close()
```

## 常见陷阱

❌ 忘记在请求头中添加 Token
✅ 使用 `client.login()` 自动管理 Token

❌ 硬编码测试数据导致用例相互依赖
✅ 每个测试用例独立创建和清理数据

❌ 只测试正向场景
✅ 覆盖正向、异常、边界值场景

❌ 忽略响应状态码，只检查业务 code
✅ 同时验证 HTTP 状态码和业务响应码

## 最佳实践

- **使用 fixture 管理客户端生命周期** - 避免重复创建/销毁客户端
- **参数化测试** - 使用 `@pytest.mark.parametrize` 减少重复代码
- **数据隔离** - 测试数据使用唯一标识，测试后清理
- **断言明确** - 验证状态码、响应结构、关键字段
- **分层组织** - 按模块组织测试文件，便于维护

## 测试执行命令

```bash
# 运行所有 API 测试
pytest tests/api/ -v

# 运行指定测试文件
pytest tests/api/test_login.py -v

# 运行指定测试类/方法
pytest tests/api/test_user.py::TestUserAPI::test_query_user_list -v

# 生成 HTML 报告
pytest tests/api/ -v --html=reports/api_report.html

# 并行执行
pytest tests/api/ -v -n auto

# 失败重试
pytest tests/api/ -v --reruns 2
```

## 参考文件

- **examples/** - 展示常见模式的示例：
  - `basic_crud_test.py` - 基础 CRUD 接口测试
  - `auth_test.py` - 认证授权测试
  - `parametrize_test.py` - 参数化测试示例
  - `data_driven_test.py` - 数据驱动测试

## 完整教程

**`examples/tutorial/`** - 9个渐进式示例，从入门到高级：

### 入门级（1小时）
| 示例 | 目录 | 学习内容 |
|-----|------|---------|
| 01 | `beginner/01_basic_request/` | GET/POST 请求、响应获取 |
| 02 | `beginner/02_response_validation/` | 状态码、JSON 结构验证 |
| 03 | `beginner/03_authentication/` | 登录、Token 认证 |

### 中级（1.5小时）
| 示例 | 目录 | 学习内容 |
|-----|------|---------|
| 04 | `intermediate/04_crud_testing/` | CRUD 接口测试、数据清理 |
| 05 ⭐ | `intermediate/05_parametrize/` | **参数化测试（重点）** |
| 06 ⭐ | `intermediate/06_data_driven/` | **数据驱动测试（重点）** |

### 高级（2小时）
| 示例 | 目录 | 学习内容 |
|-----|------|---------|
| 07 | `advanced/07_contract_testing/` | OpenAPI 契约验证 |
| 08 | `advanced/08_performance/` | 响应时间、并发测试 |
| 09 ⭐ | `advanced/09_comprehensive/` | **完整测试套件（重点）** |

### 运行教程

```bash
cd examples/tutorial

# 查看所有命令
make help

# 运行特定示例
make 01  # 基础请求
make 05  # 参数化测试（重点）
make 09  # 综合套件（重点）

# 运行所有示例
make all
```

### 核心知识点速查

**参数化测试（重要）：**
```python
@pytest.mark.parametrize("username,password,expected", [
    ("admin", "admin123", True),   # 正确凭证
    ("admin", "wrong", False),      # 错误密码
    ("", "admin123", False),        # 空用户名
])
def test_login(self, username, password, expected):
    response = client.post("/login", json={
        "username": username,
        "password": password
    })
    actual = response.json()["code"] == 200
    assert actual == expected
```

**数据驱动测试（重要）：**
```python
TEST_DATA = [
    {"case_id": "TC_001", "username": "admin", "password": "admin123", "expected": True},
    {"case_id": "TC_002", "username": "admin", "password": "wrong", "expected": False},
]

@pytest.mark.parametrize("case", TEST_DATA, ids=lambda x: x["case_id"])
def test_login(self, case):
    response = client.post("/login", json={
        "username": case["username"],
        "password": case["password"]
    })
    assert (response.json()["code"] == 200) == case["expected"]
```

**Fixture 数据清理：**
```python
@pytest.fixture
def cleanup_users(api_client):
    created_ids = []
    yield created_ids
    # 测试结束后自动清理
    for id in created_ids:
        api_client.delete(f"/user/delete", params={"id": id})
```

详细内容请查看 `examples/tutorial/README.md`。
