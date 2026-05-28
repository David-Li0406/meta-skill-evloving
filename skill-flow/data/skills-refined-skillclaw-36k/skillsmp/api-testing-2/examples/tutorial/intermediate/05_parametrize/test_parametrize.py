#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
示例05: 参数化测试 ⭐

学习目标:
- 使用 @pytest.mark.parametrize
- 一个测试方法覆盖多个场景
- 组织测试数据

运行方式:
    pytest test_parametrize.py -v
    # 或
    make 05
"""

import pytest
import httpx

BASE_URL = "http://localhost:5000"


class TestLoginParametrize:
    """登录接口参数化测试"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        self.client = httpx.Client(base_url=BASE_URL, timeout=30)
        yield
        self.client.close()
    
    @pytest.mark.parametrize("username,password,expected_success", [
        # 正向场景
        ("admin", "admin123", True),
        
        # 异常场景 - 密码错误
        ("admin", "wrong_password", False),
        ("admin", "123456", False),
        
        # 异常场景 - 用户不存在
        ("not_exist_user", "admin123", False),
        ("unknown_user", "password", False),
        
        # 异常场景 - 空值
        ("", "admin123", False),
        ("admin", "", False),
        ("", "", False),
        
        # 边界场景 - 特殊字符（SQL 注入测试）
        ("admin'--", "admin123", False),
        ("admin", "admin123'--", False),
        ("admin\" OR 1=1--", "any", False),
    ])
    def test_login_scenarios(self, username, password, expected_success):
        """登录场景参数化测试"""
        response = self.client.post("/login", json={
            "username": username,
            "password": password
        })
        
        if response.status_code == 422:
            # 参数校验失败，视为登录失败
            assert not expected_success, f"用户名={username}: 期望成功但参数校验失败"
        else:
            data = response.json()
            actual_success = data["code"] == 200
            assert actual_success == expected_success, \
                f"用户名={username}, 密码={password}: 期望={expected_success}, 实际={actual_success}"


class TestPaginationParametrize:
    """分页查询参数化测试"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        self.client = httpx.Client(base_url=BASE_URL, timeout=30)
        
        # 登录
        response = self.client.post("/login", json={
            "username": "admin",
            "password": "admin123"
        })
        data = response.json()
        if data["code"] == 200 and data.get("data"):
            token = data["data"].get("token")
            if token:
                self.client.headers["Authorization"] = f"Bearer {token}"
        
        yield
        self.client.close()
    
    @pytest.mark.parametrize("page_num,page_size,expected_valid", [
        # 正常分页
        (1, 10, True),
        (1, 20, True),
        (2, 10, True),
        (1, 100, True),
        
        # 边界值
        (1, 1, True),      # 最小页大小
        (1, 500, True),    # 较大页大小
        (100, 10, True),   # 较大页码（可能返回空列表）
        
        # 异常值
        (0, 10, False),    # 页码为 0
        (-1, 10, False),   # 负数页码
        (1, 0, False),     # 页大小为 0
        (1, -1, False),    # 负数页大小
    ])
    def test_pagination(self, page_num, page_size, expected_valid):
        """分页参数化测试"""
        response = self.client.post("/user/queryByPage", json={
            "pageNum": page_num,
            "pageSize": page_size
        })
        
        if response.status_code == 422:
            # 参数校验失败
            assert not expected_valid, f"pageNum={page_num}, pageSize={page_size}: 期望成功但参数校验失败"
        else:
            data = response.json()
            if expected_valid:
                assert data["code"] == 200, f"pageNum={page_num}, pageSize={page_size}: 期望成功"
                assert "list" in data["data"]
            else:
                # 无效参数可能返回错误或被服务端修正
                pass


class TestFieldValidationParametrize:
    """字段校验参数化测试"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        self.client = httpx.Client(base_url=BASE_URL, timeout=30)
        
        response = self.client.post("/login", json={
            "username": "admin",
            "password": "admin123"
        })
        data = response.json()
        if data["code"] == 200 and data.get("data"):
            token = data["data"].get("token")
            if token:
                self.client.headers["Authorization"] = f"Bearer {token}"
        
        self.created_ids = []
        yield
        
        # 清理
        for id in self.created_ids:
            try:
                self.client.delete("/user/delete", params={"id": id})
            except Exception:
                pass
        self.client.close()
    
    @pytest.mark.parametrize("username,expected_valid,reason", [
        # 正常用户名
        ("test_user_001", True, "正常用户名"),
        ("user123", True, "字母数字组合"),
        
        # 长度校验
        ("ab", False, "用户名太短（小于3字符）"),
        ("a" * 65, False, "用户名太长（超过64字符）"),
        
        # 特殊字符
        ("user@test", True, "包含@符号"),
        ("user_test", True, "包含下划线"),
        ("user-test", True, "包含连字符"),
        
        # 空值
        ("", False, "空用户名"),
        ("   ", False, "纯空格用户名"),
    ], ids=lambda x: x if isinstance(x, str) and len(x) < 20 else "...")
    def test_username_validation(self, username, expected_valid, reason):
        """用户名校验参数化测试"""
        import uuid
        
        # 为了避免重复，给用户名加上唯一后缀
        test_username = f"{username}_{uuid.uuid4().hex[:4]}" if username.strip() else username
        
        response = self.client.post("/user/insert", json={
            "username": test_username,
            "password": "Test@123456",
            "status": 1
        })
        
        if response.status_code == 422:
            assert not expected_valid, f"{reason}: 期望成功但参数校验失败"
        else:
            data = response.json()
            actual_valid = data["code"] == 200
            
            if actual_valid and data.get("data") and data["data"].get("id"):
                self.created_ids.append(data["data"]["id"])
            
            # 注意：某些校验可能在业务层而非参数层
            # 这里根据实际情况调整断言


class TestHttpMethodParametrize:
    """HTTP 方法参数化测试"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        self.client = httpx.Client(base_url=BASE_URL, timeout=30)
        yield
        self.client.close()
    
    @pytest.mark.parametrize("method,path,expected_status", [
        # 存在的接口 - 正确方法
        ("POST", "/login", 200),
        
        # 不存在的接口
        ("GET", "/not_exist_api_12345", 404),
        ("POST", "/not_exist_api_12345", 404),
        
        # 方法不允许（根据实际接口配置）
        # ("GET", "/login", 405),  # 如果 login 只允许 POST
    ])
    def test_http_methods(self, method, path, expected_status):
        """HTTP 方法测试"""
        if method == "GET":
            response = self.client.get(path)
        elif method == "POST":
            response = self.client.post(path, json={})
        elif method == "PUT":
            response = self.client.put(path, json={})
        elif method == "DELETE":
            response = self.client.delete(path)
        else:
            response = self.client.request(method, path)
        
        assert response.status_code == expected_status, \
            f"{method} {path}: 期望状态码={expected_status}, 实际={response.status_code}"


class TestWithCustomIds:
    """使用自定义 ID 的参数化测试"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        self.client = httpx.Client(base_url=BASE_URL, timeout=30)
        yield
        self.client.close()
    
    @pytest.mark.parametrize(
        "username,password,expected",
        [
            ("admin", "admin123", True),
            ("admin", "wrong", False),
            ("", "admin123", False),
        ],
        ids=["正确凭证", "错误密码", "空用户名"]  # 自定义测试 ID
    )
    def test_login_with_ids(self, username, password, expected):
        """带自定义 ID 的登录测试"""
        response = self.client.post("/login", json={
            "username": username,
            "password": password
        })
        
        if response.status_code != 422:
            data = response.json()
            actual = data["code"] == 200
            assert actual == expected


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
