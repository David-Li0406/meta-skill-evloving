# API 接口测试教程

使用 pytest + httpx 进行 API 接口自动化测试的完整实践教程。从基础请求到复杂场景，配套可运行示例，循序渐进掌握 API 测试技能。

## 目录

- [教程简介](#教程简介)
- [快速开始](#快速开始)
- [学习路径](#学习路径)
- [入门级示例](#入门级示例)
- [中级示例](#中级示例)
- [高级示例](#高级示例)
- [最佳实践](#最佳实践)
- [常见问题FAQ](#常见问题faq)
- [快速参考](#快速参考)

---

## 教程简介

### 这个教程适合谁？

- 🎯 想学习 API 自动化测试的开发者
- 🎯 需要测试后端接口的 QA 工程师
- 🎯 想提高测试技能的全栈开发者
- 🎯 对 pytest + httpx 感兴趣的技术人员

### 你将学到什么？

✅ **基础技能**
- 使用 httpx 发送 HTTP 请求
- 编写 pytest 测试用例
- 验证响应状态码和数据

✅ **中级技能**
- 测试 CRUD 接口
- 处理认证和授权
- 参数化测试减少重复

✅ **高级技能**
- 数据驱动测试
- 接口契约验证
- 完整测试套件组织

### 教程特色

- 📚 **9个渐进式示例** - 从简单到复杂，循序渐进
- 🚀 **开箱即用** - 所有示例都可直接运行
- 💡 **实用导向** - 基于真实场景的测试案例
- 🎓 **配套练习** - 每个示例都有练习题巩固知识

---

## 快速开始

### 环境准备

**1. 安装依赖**

```bash
pip install pytest httpx
```

**2. 验证安装**

```bash
cd .codebuddy/skills/testing/api-testing/examples/tutorial
make help
```

### 运行第一个示例

```bash
# 方式1: 使用 make 命令
make 01

# 方式2: 直接运行
cd beginner/01_basic_request
python test_basic.py
```

**预期输出：**
```
✓ GET 请求成功
✓ POST 请求成功
✓ 响应状态码验证通过
...
✓ 测试完成!
```

---

## 学习路径

### 学习路线图

```
🟢 入门级 (1小时)           🟡 中级 (1.5小时)          🔴 高级 (2小时)
┌──────────────────┐      ┌──────────────────┐      ┌──────────────────┐
│  01 基础请求      │ ───> │  04 CRUD测试      │ ───> │  07 契约测试      │
│  ⏱️ 15分钟        │      │  ⏱️ 25分钟        │      │  ⏱️ 30分钟        │
└──────────────────┘      └──────────────────┘      └──────────────────┘
         │                         │                         │
         ▼                         ▼                         ▼
┌──────────────────┐      ┌──────────────────┐      ┌──────────────────┐
│  02 响应验证      │      │  05 参数化测试⭐   │      │  08 性能基准      │
│  ⏱️ 20分钟        │      │  ⏱️ 30分钟        │      │  ⏱️ 25分钟        │
└──────────────────┘      └──────────────────┘      └──────────────────┘
         │                         │                         │
         ▼                         ▼                         ▼
┌──────────────────┐      ┌──────────────────┐      ┌──────────────────┐
│  03 认证授权      │      │  06 数据驱动⭐     │      │  09 综合套件⭐     │
│  ⏱️ 20分钟        │      │  ⏱️ 30分钟        │      │  ⏱️ 45分钟        │
└──────────────────┘      └──────────────────┘      └──────────────────┘

⭐ = 重点示例
```

---

## 入门级示例

### 示例01：基础请求

**📝 学习目标**
- 使用 httpx 发送 GET/POST 请求
- 理解请求参数和请求体
- 获取响应数据

**⏱️ 预计时间：15分钟**

**🚀 运行命令**
```bash
make 01
```

**核心代码**
```python
import httpx

# GET 请求
response = httpx.get("http://localhost:5000/user/queryById", params={"id": 1})
print(response.json())

# POST 请求
response = httpx.post("http://localhost:5000/login", json={
    "username": "admin",
    "password": "admin123"
})
print(response.json())
```

**🎯 练习题**
1. 发送一个带查询参数的 GET 请求
2. 发送一个带 JSON 请求体的 POST 请求
3. 打印响应的状态码、头信息和内容

---

### 示例02：响应验证

**📝 学习目标**
- 验证 HTTP 状态码
- 验证响应 JSON 结构
- 使用 pytest 断言

**⏱️ 预计时间：20分钟**

**🚀 运行命令**
```bash
make 02
```

**核心代码**
```python
import pytest
import httpx

def test_response_validation():
    response = httpx.get("http://localhost:5000/user/queryById", params={"id": 1})
    
    # 验证状态码
    assert response.status_code == 200
    
    # 验证响应结构
    data = response.json()
    assert data["code"] == 200
    assert "data" in data
    
    # 验证数据字段
    user = data["data"]
    assert user["id"] == 1
    assert "username" in user
```

**🎯 练习题**
1. 验证响应时间小于 1 秒
2. 验证响应头中的 Content-Type
3. 验证列表响应的长度

---

### 示例03：认证授权

**📝 学习目标**
- 实现登录获取 Token
- 在请求头中携带 Token
- 测试未授权访问

**⏱️ 预计时间：20分钟**

**🚀 运行命令**
```bash
make 03
```

**核心代码**
```python
import httpx

class TestAuth:
    def setup_method(self):
        self.client = httpx.Client(base_url="http://localhost:5000")
        
    def test_login_and_access(self):
        # 登录获取 Token
        response = self.client.post("/login", json={
            "username": "admin",
            "password": "admin123"
        })
        token = response.json()["data"]["token"]
        
        # 携带 Token 访问
        self.client.headers["Authorization"] = f"Bearer {token}"
        response = self.client.get("/user/queryById", params={"id": 1})
        
        assert response.status_code == 200
        
    def teardown_method(self):
        self.client.close()
```

**🎯 练习题**
1. 测试错误密码登录
2. 测试无 Token 访问受保护接口
3. 测试 Token 过期场景

---

## 中级示例

### 示例04：CRUD 测试

**📝 学习目标**
- 测试创建（Create）接口
- 测试查询（Read）接口
- 测试更新（Update）接口
- 测试删除（Delete）接口
- 测试数据清理

**⏱️ 预计时间：25分钟**

**🚀 运行命令**
```bash
make 04
```

**核心代码**
```python
class TestCRUD:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.client = APIClient()
        self.client.login()
        self.created_ids = []
        yield
        # 清理测试数据
        for id in self.created_ids:
            self.client.delete(f"/project/delete", params={"id": id})
        self.client.close()
    
    def test_create(self):
        response = self.client.post("/project/insert", json={
            "name": "测试项目",
            "status": 1
        })
        assert response.json()["code"] == 200
        self.created_ids.append(response.json()["data"]["id"])
    
    def test_read(self):
        response = self.client.post("/project/queryByPage", json={
            "pageNum": 1,
            "pageSize": 10
        })
        assert response.json()["code"] == 200
        assert "list" in response.json()["data"]
```

**🎯 练习题**
1. 实现完整的 CRUD 测试流程
2. 测试创建重复数据
3. 测试删除不存在的数据

---

### 示例05：参数化测试 ⭐

> **⚠️ 重要示例** - 大幅减少重复代码！

**📝 学习目标**
- 使用 `@pytest.mark.parametrize`
- 一个测试方法覆盖多个场景
- 组织测试数据

**⏱️ 预计时间：30分钟**

**🚀 运行命令**
```bash
make 05
```

**核心代码**
```python
import pytest

class TestLoginParametrize:
    @pytest.mark.parametrize("username,password,expected", [
        ("admin", "admin123", True),      # 正确凭证
        ("admin", "wrong", False),         # 错误密码
        ("", "admin123", False),           # 空用户名
        ("admin", "", False),              # 空密码
        ("not_exist", "any", False),       # 用户不存在
    ])
    def test_login(self, username, password, expected):
        response = client.post("/login", json={
            "username": username,
            "password": password
        })
        actual = response.json()["code"] == 200
        assert actual == expected
```

**🎯 练习题**
1. 参数化测试分页参数（pageNum, pageSize）
2. 参数化测试字段校验（必填、长度、格式）
3. 使用 `ids` 参数给测试用例命名

---

### 示例06：数据驱动测试 ⭐

> **⭐ 重点示例** - 测试用例与数据分离！

**📝 学习目标**
- 从 JSON/YAML 文件加载测试数据
- 实现测试用例与数据分离
- 便于维护和扩展

**⏱️ 预计时间：30分钟**

**🚀 运行命令**
```bash
make 06
```

**核心代码**
```python
import json

# 从文件加载测试数据
def load_test_data(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

TEST_DATA = load_test_data("test_cases.json")

class TestDataDriven:
    @pytest.mark.parametrize("case", TEST_DATA, ids=lambda x: x["case_id"])
    def test_api(self, case):
        response = client.request(
            case["method"],
            case["path"],
            json=case.get("body"),
            params=case.get("params")
        )
        assert response.json()["code"] == case["expected_code"]
```

**测试数据文件示例 (test_cases.json)**
```json
[
  {
    "case_id": "TC_001",
    "case_name": "正常登录",
    "method": "POST",
    "path": "/login",
    "body": {"username": "admin", "password": "admin123"},
    "expected_code": 200
  },
  {
    "case_id": "TC_002",
    "case_name": "密码错误",
    "method": "POST",
    "path": "/login",
    "body": {"username": "admin", "password": "wrong"},
    "expected_code": 401
  }
]
```

**🎯 练习题**
1. 创建 YAML 格式的测试数据文件
2. 实现 CSV 格式数据加载
3. 添加测试数据校验

---

## 高级示例

### 示例07：契约测试

**📝 学习目标**
- 验证 OpenAPI/Swagger 规范
- 校验响应结构符合契约
- 检测接口变更

**⏱️ 预计时间：30分钟**

**🚀 运行命令**
```bash
make 07
```

**核心代码**
```python
def test_openapi_contract():
    # 获取 OpenAPI 规范
    spec = client.get("/openapi.json").json()
    
    # 验证接口存在
    assert "/login" in spec["paths"]
    assert "post" in spec["paths"]["/login"]
    
    # 验证响应结构
    login_spec = spec["paths"]["/login"]["post"]
    assert "responses" in login_spec
    assert "200" in login_spec["responses"]
```

---

### 示例08：性能基准

**📝 学习目标**
- 测量接口响应时间
- 设置性能基准
- 检测性能退化

**⏱️ 预计时间：25分钟**

**🚀 运行命令**
```bash
make 08
```

**核心代码**
```python
import time

def test_response_time():
    start = time.time()
    response = client.get("/user/queryById", params={"id": 1})
    elapsed = time.time() - start
    
    assert response.status_code == 200
    assert elapsed < 1.0, f"响应时间过长: {elapsed:.2f}s"

def test_concurrent_requests():
    """并发请求测试"""
    import concurrent.futures
    
    def make_request():
        return client.get("/user/queryById", params={"id": 1})
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(make_request) for _ in range(100)]
        results = [f.result() for f in futures]
    
    success_count = sum(1 for r in results if r.status_code == 200)
    assert success_count >= 95, f"成功率过低: {success_count}%"
```

---

### 示例09：综合测试套件 ⭐

> **⭐ 重点示例** - 综合运用所有技术！

**📝 学习目标**
- 组织大型测试项目
- 使用 pytest fixtures
- 生成测试报告
- CI/CD 集成

**⏱️ 预计时间：45分钟**

**🚀 运行命令**
```bash
make 09
```

**项目结构**
```
tests/
├── conftest.py          # 共享 fixtures
├── test_auth.py         # 认证测试
├── test_user.py         # 用户模块测试
├── test_project.py      # 项目模块测试
└── data/
    └── test_cases.json  # 测试数据
```

**conftest.py**
```python
import pytest
from api_client import APIClient

@pytest.fixture(scope="session")
def api_client():
    """会话级别的 API 客户端"""
    client = APIClient()
    client.login()
    yield client
    client.close()

@pytest.fixture
def clean_test_data(api_client):
    """测试数据清理 fixture"""
    created_ids = []
    yield created_ids
    for id in created_ids:
        api_client.delete(f"/user/delete", params={"id": id})
```

---

## 最佳实践

### 测试组织

```python
# ✅ 好的组织方式
class TestUserAPI:
    """用户模块测试"""
    
    # ========== 正向测试 ==========
    def test_create_user_success(self): ...
    def test_query_user_success(self): ...
    
    # ========== 异常测试 ==========
    def test_create_user_duplicate(self): ...
    def test_query_user_not_found(self): ...
    
    # ========== 边界测试 ==========
    def test_create_user_max_length(self): ...
```

### 断言策略

```python
# ✅ 完整的断言
def test_api_response(self):
    response = client.get("/user/queryById", params={"id": 1})
    
    # 1. 验证 HTTP 状态码
    assert response.status_code == 200
    
    # 2. 验证业务状态码
    data = response.json()
    assert data["code"] == 200
    
    # 3. 验证数据结构
    assert "data" in data
    assert data["data"] is not None
    
    # 4. 验证关键字段
    user = data["data"]
    assert user["id"] == 1
    assert "username" in user

# ❌ 不完整的断言
def test_api_response_bad(self):
    response = client.get("/user/queryById", params={"id": 1})
    assert response.status_code == 200  # 只验证状态码
```

### 数据隔离

```python
# ✅ 每个测试独立的数据
class TestUser:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.created_ids = []
        yield
        # 清理测试数据
        for id in self.created_ids:
            client.delete(f"/user/delete", params={"id": id})
    
    def test_create_user(self):
        response = client.post("/user/insert", json={
            "username": f"test_user_{uuid.uuid4().hex[:8]}",  # 唯一用户名
            "password": "Test@123456"
        })
        if response.json()["code"] == 200:
            self.created_ids.append(response.json()["data"]["id"])
```

---

## 常见问题FAQ

### Q1: 如何处理 Token 过期？

```python
class APIClient:
    def request(self, method, path, **kwargs):
        response = self.client.request(method, path, **kwargs)
        
        # Token 过期时自动重新登录
        if response.status_code == 401:
            self.login()
            response = self.client.request(method, path, **kwargs)
        
        return response
```

### Q2: 如何测试文件上传？

```python
def test_file_upload():
    with open("test.pdf", "rb") as f:
        response = client.post("/upload", files={"file": f})
    assert response.status_code == 200
```

### Q3: 如何并行执行测试？

```bash
# 安装 pytest-xdist
pip install pytest-xdist

# 并行执行
pytest tests/ -n auto
```

### Q4: 如何生成测试报告？

```bash
# 安装 pytest-html
pip install pytest-html

# 生成 HTML 报告
pytest tests/ --html=report.html
```

### Q5: 如何处理环境差异？

```python
import os

BASE_URL = os.getenv("API_BASE_URL", "http://localhost:5000")
USERNAME = os.getenv("API_USERNAME", "admin")
PASSWORD = os.getenv("API_PASSWORD", "admin123")

client = APIClient(base_url=BASE_URL)
client.login(USERNAME, PASSWORD)
```

---

## 快速参考

### pytest 常用命令

```bash
# 运行所有测试
pytest tests/ -v

# 运行指定文件
pytest tests/test_user.py -v

# 运行指定测试
pytest tests/test_user.py::TestUser::test_create -v

# 只运行失败的测试
pytest tests/ --lf

# 失败时停止
pytest tests/ -x

# 显示 print 输出
pytest tests/ -s

# 生成覆盖率报告
pytest tests/ --cov=app --cov-report=html
```

### httpx 常用方法

```python
import httpx

# 创建客户端
client = httpx.Client(base_url="http://localhost:5000", timeout=30)

# GET 请求
response = client.get("/path", params={"key": "value"})

# POST 请求
response = client.post("/path", json={"key": "value"})

# PUT 请求
response = client.put("/path", json={"key": "value"})

# DELETE 请求
response = client.delete("/path", params={"id": 1})

# 设置请求头
client.headers["Authorization"] = "Bearer token"

# 响应处理
response.status_code    # HTTP 状态码
response.json()         # JSON 响应
response.text           # 文本响应
response.headers        # 响应头
response.elapsed        # 响应时间

# 关闭客户端
client.close()
```

### 断言速查

```python
# 状态码
assert response.status_code == 200
assert response.status_code in [200, 201]

# JSON 响应
data = response.json()
assert data["code"] == 200
assert data["data"] is not None
assert "key" in data
assert isinstance(data["list"], list)
assert len(data["list"]) > 0

# 响应时间
assert response.elapsed.total_seconds() < 1.0
```

---

## 总结

恭喜你完成了 API 接口测试教程的学习！🎉

### 你现在掌握了：

✅ **基础技能**
- HTTP 请求发送
- 响应验证
- 认证处理

✅ **中级技能**
- CRUD 测试
- 参数化测试
- 数据驱动测试

✅ **高级技能**
- 契约测试
- 性能测试
- 测试套件组织

### 下一步行动

1. ✍️ **完成所有练习题** - 巩固知识
2. 🚀 **应用到实际项目** - 实践是最好的学习
3. 📖 **阅读 pytest 文档** - 深入了解高级特性
4. 🤝 **结合 CI/CD** - 实现自动化测试流水线

---

**祝你测试愉快！Happy Testing! 🧪**
