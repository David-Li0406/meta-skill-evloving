#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
参数化测试示例

演示如何使用 pytest.mark.parametrize 进行参数化测试，
减少重复代码，提高测试覆盖率。
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))
from api_client import APIClient


class TestLoginParametrize:
    """登录接口参数化测试"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        self.client = APIClient(base_url="http://localhost:5000")
        yield
        self.client.close()
    
    @pytest.mark.parametrize("username,password,expected_success", [
        # 正向场景
        ("admin", "admin123", True),
        
        # 异常场景 - 密码错误
        ("admin", "wrong_password", False),
        ("admin", "123456", False),
        
        # 异常场景 - 用户不存在
        ("not_exist", "admin123", False),
        ("unknown_user", "password", False),
        
        # 异常场景 - 空值
        ("", "admin123", False),
        ("admin", "", False),
        ("", "", False),
        
        # 边界场景 - 特殊字符
        ("admin'--", "admin123", False),
        ("admin", "admin123'--", False),
    ])
    def test_login_scenarios(self, username, password, expected_success):
        """登录场景参数化测试"""
        response = self.client.post("/login", json={
            "username": username,
            "password": password
        })
        
        if response.status_code == 422:
            # 参数校验失败
            assert not expected_success
        else:
            data = response.json()
            actual_success = data["code"] == 200
            assert actual_success == expected_success, \
                f"用户名={username}, 密码={password}, 期望={expected_success}, 实际={actual_success}"


class TestPaginationParametrize:
    """分页查询参数化测试"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        self.client = APIClient(base_url="http://localhost:5000")
        self.client.login()
        yield
        self.client.close()
    
    @pytest.mark.parametrize("page_num,page_size,expected_valid", [
        # 正常分页
        (1, 10, True),
        (1, 20, True),
        (2, 10, True),
        (1, 100, True),
        
        # 边界值
        (1, 1, True),
        (1, 500, True),  # 最大页大小
        
        # 异常值
        (0, 10, False),   # 页码为 0
        (-1, 10, False),  # 负数页码
        (1, 0, False),    # 页大小为 0
        (1, -1, False),   # 负数页大小
    ])
    def test_user_pagination(self, page_num, page_size, expected_valid):
        """用户列表分页参数化测试"""
        response = self.client.post("/user/queryByPage", json={
            "pageNum": page_num,
            "pageSize": page_size
        })
        
        if response.status_code == 422:
            assert not expected_valid
        else:
            data = response.json()
            if expected_valid:
                assert data["code"] == 200
                assert "list" in data["data"]
            else:
                # 无效参数应该返回错误或空结果
                pass


class TestUserCreateParametrize:
    """用户创建参数化测试"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        self.client = APIClient(base_url="http://localhost:5000")
        self.client.login()
        self.created_ids = []
        yield
        # 清理测试数据
        for id in self.created_ids:
            try:
                self.client.delete("/user/delete", params={"id": id})
            except Exception:
                pass
        self.client.close()
    
    @pytest.mark.parametrize("username,password,email,expected_valid,description", [
        # 正常数据
        ("test_user_001", "Test@123456", "test001@example.com", True, "正常创建"),
        ("test_user_002", "Password123!", "test002@example.com", True, "正常创建2"),
        
        # 用户名校验
        ("ab", "Test@123456", "test@example.com", False, "用户名太短"),
        ("a" * 65, "Test@123456", "test@example.com", False, "用户名太长"),
        ("", "Test@123456", "test@example.com", False, "用户名为空"),
        
        # 密码校验
        ("test_pwd_001", "123", "test@example.com", False, "密码太短"),
        ("test_pwd_002", "", "test@example.com", False, "密码为空"),
        
        # 邮箱校验
        ("test_email_001", "Test@123456", "invalid_email", False, "邮箱格式错误"),
        ("test_email_002", "Test@123456", "", True, "邮箱为空（可选字段）"),
    ])
    def test_create_user_validation(self, username, password, email, expected_valid, description):
        """用户创建参数校验测试"""
        response = self.client.post("/user/insert", json={
            "username": username,
            "password": password,
            "email": email if email else None,
            "status": 1
        })
        
        if response.status_code == 422:
            # 参数校验失败
            assert not expected_valid, f"{description}: 期望成功但参数校验失败"
        else:
            data = response.json()
            actual_valid = data["code"] == 200
            
            if actual_valid and data.get("data") and data["data"].get("id"):
                self.created_ids.append(data["data"]["id"])
            
            assert actual_valid == expected_valid, \
                f"{description}: 期望={expected_valid}, 实际={actual_valid}, msg={data.get('msg')}"


class TestStatusCodeParametrize:
    """HTTP 状态码参数化测试"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        self.client = APIClient(base_url="http://localhost:5000")
        self.client.login()
        yield
        self.client.close()
    
    @pytest.mark.parametrize("method,path,expected_status", [
        # 存在的接口
        ("GET", "/user/queryById?id=1", 200),
        ("POST", "/user/queryByPage", 200),
        
        # 不存在的接口
        ("GET", "/not_exist_api", 404),
        ("POST", "/not_exist_api", 404),
        
        # 方法不允许
        ("DELETE", "/login", 405),
        ("PUT", "/login", 405),
    ])
    def test_http_status_codes(self, method, path, expected_status):
        """HTTP 状态码测试"""
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


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
