#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
示例03: 认证授权

学习目标:
- 实现登录获取 Token
- 在请求头中携带 Token
- 测试未授权访问

运行方式:
    pytest test_auth.py -v
    # 或
    make 03
"""

import pytest
import httpx

BASE_URL = "http://localhost:5000"


class TestLogin:
    """登录测试"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        self.client = httpx.Client(base_url=BASE_URL, timeout=30)
        yield
        self.client.close()
    
    def test_login_success(self):
        """正常登录"""
        response = self.client.post("/login", json={
            "username": "admin",
            "password": "admin123"
        })
        
        assert response.status_code == 200
        
        data = response.json()
        assert data["code"] == 200, f"登录失败: {data.get('msg')}"
        assert data["data"] is not None
        assert data["data"].get("token"), "Token 不应为空"
        
        # Token 格式检查（JWT 通常是三段式）
        token = data["data"]["token"]
        assert len(token) > 20, "Token 长度异常"
    
    def test_login_wrong_password(self):
        """密码错误"""
        response = self.client.post("/login", json={
            "username": "admin",
            "password": "wrong_password"
        })
        
        data = response.json()
        assert data["code"] != 200, "密码错误应登录失败"
    
    def test_login_user_not_exist(self):
        """用户不存在"""
        response = self.client.post("/login", json={
            "username": "not_exist_user_12345",
            "password": "any_password"
        })
        
        data = response.json()
        assert data["code"] != 200, "用户不存在应登录失败"
    
    def test_login_empty_credentials(self):
        """空凭证"""
        # 空用户名
        response = self.client.post("/login", json={
            "username": "",
            "password": "admin123"
        })
        if response.status_code != 422:
            data = response.json()
            assert data["code"] != 200
        
        # 空密码
        response = self.client.post("/login", json={
            "username": "admin",
            "password": ""
        })
        if response.status_code != 422:
            data = response.json()
            assert data["code"] != 200


class TestTokenAuth:
    """Token 认证测试"""
    
    @pytest.fixture
    def auth_client(self):
        """已认证的客户端"""
        client = httpx.Client(base_url=BASE_URL, timeout=30)
        
        # 登录获取 Token
        response = client.post("/login", json={
            "username": "admin",
            "password": "admin123"
        })
        
        data = response.json()
        if data["code"] == 200 and data.get("data"):
            token = data["data"].get("token")
            if token:
                client.headers["Authorization"] = f"Bearer {token}"
        
        yield client
        client.close()
    
    @pytest.fixture
    def unauth_client(self):
        """未认证的客户端"""
        client = httpx.Client(base_url=BASE_URL, timeout=30)
        yield client
        client.close()
    
    def test_access_with_token(self, auth_client):
        """携带 Token 访问"""
        response = auth_client.post("/user/queryByPage", json={
            "pageNum": 1,
            "pageSize": 10
        })
        
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200, f"携带 Token 访问失败: {data.get('msg')}"
    
    def test_access_without_token(self, unauth_client):
        """不携带 Token 访问"""
        response = unauth_client.post("/user/queryByPage", json={
            "pageNum": 1,
            "pageSize": 10
        })
        
        # 应返回未授权错误
        if response.status_code == 401:
            pass  # HTTP 401
        elif response.status_code == 200:
            data = response.json()
            assert data["code"] in [401, 403, 500], "未授权应返回错误码"
    
    def test_access_with_invalid_token(self, unauth_client):
        """使用无效 Token 访问"""
        unauth_client.headers["Authorization"] = "Bearer invalid_token_12345"
        
        response = unauth_client.post("/user/queryByPage", json={
            "pageNum": 1,
            "pageSize": 10
        })
        
        # 应返回认证失败
        if response.status_code in [401, 403]:
            pass
        elif response.status_code == 200:
            data = response.json()
            assert data["code"] != 200, "无效 Token 应认证失败"
    
    def test_access_with_malformed_token(self, unauth_client):
        """使用格式错误的 Token"""
        # 缺少 Bearer 前缀
        unauth_client.headers["Authorization"] = "invalid_token"
        
        response = unauth_client.post("/user/queryByPage", json={
            "pageNum": 1,
            "pageSize": 10
        })
        
        if response.status_code in [401, 403]:
            pass
        elif response.status_code == 200:
            data = response.json()
            assert data["code"] != 200


class TestPermission:
    """权限测试"""
    
    @pytest.fixture
    def admin_client(self):
        """管理员客户端"""
        client = httpx.Client(base_url=BASE_URL, timeout=30)
        
        response = client.post("/login", json={
            "username": "admin",
            "password": "admin123"
        })
        
        data = response.json()
        if data["code"] == 200 and data.get("data"):
            token = data["data"].get("token")
            if token:
                client.headers["Authorization"] = f"Bearer {token}"
        
        yield client
        client.close()
    
    def test_admin_can_query_users(self, admin_client):
        """管理员可以查询用户"""
        response = admin_client.post("/user/queryByPage", json={
            "pageNum": 1,
            "pageSize": 10
        })
        
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200
    
    def test_admin_can_query_roles(self, admin_client):
        """管理员可以查询角色"""
        response = admin_client.post("/role/queryByPage", json={
            "pageNum": 1,
            "pageSize": 10
        })
        
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
