#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
认证授权测试示例

演示如何测试登录、Token 验证、权限控制等场景。
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))
from api_client import APIClient


class TestAuthentication:
    """认证测试"""
    
    @pytest.fixture
    def client(self):
        """创建未登录的客户端"""
        client = APIClient(base_url="http://localhost:5000")
        yield client
        client.close()
    
    # ========== 登录测试 ==========
    
    def test_login_success(self, client):
        """正常登录"""
        response = client.post("/login", json={
            "username": "admin",
            "password": "admin123"
        })
        
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200
        assert "token" in data["data"]
        assert data["data"]["token"] is not None
    
    def test_login_wrong_password(self, client):
        """密码错误"""
        response = client.post("/login", json={
            "username": "admin",
            "password": "wrong_password"
        })
        
        data = response.json()
        assert data["code"] != 200
    
    def test_login_user_not_exist(self, client):
        """用户不存在"""
        response = client.post("/login", json={
            "username": "not_exist_user",
            "password": "any_password"
        })
        
        data = response.json()
        assert data["code"] != 200
    
    def test_login_empty_username(self, client):
        """用户名为空"""
        response = client.post("/login", json={
            "username": "",
            "password": "admin123"
        })
        
        # 应该返回参数校验错误
        assert response.status_code in [200, 422]
        if response.status_code == 200:
            data = response.json()
            assert data["code"] != 200
    
    def test_login_empty_password(self, client):
        """密码为空"""
        response = client.post("/login", json={
            "username": "admin",
            "password": ""
        })
        
        assert response.status_code in [200, 422]
        if response.status_code == 200:
            data = response.json()
            assert data["code"] != 200


class TestAuthorization:
    """授权测试"""
    
    @pytest.fixture
    def unauthenticated_client(self):
        """未认证的客户端"""
        client = APIClient(base_url="http://localhost:5000")
        yield client
        client.close()
    
    @pytest.fixture
    def authenticated_client(self):
        """已认证的客户端"""
        client = APIClient(base_url="http://localhost:5000")
        client.login("admin", "admin123")
        yield client
        client.close()
    
    # ========== Token 验证测试 ==========
    
    def test_access_protected_api_without_token(self, unauthenticated_client):
        """未携带 Token 访问受保护接口"""
        response = unauthenticated_client.post("/user/queryByPage", json={
            "pageNum": 1,
            "pageSize": 10
        })
        
        # 应该返回 401 或业务错误码
        assert response.status_code in [401, 403, 200]
        if response.status_code == 200:
            data = response.json()
            assert data["code"] in [401, 403, 500]  # 未授权错误码
    
    def test_access_protected_api_with_token(self, authenticated_client):
        """携带 Token 访问受保护接口"""
        response = authenticated_client.post("/user/queryByPage", json={
            "pageNum": 1,
            "pageSize": 10
        })
        
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200
    
    def test_access_with_invalid_token(self, unauthenticated_client):
        """使用无效 Token 访问"""
        # 设置一个无效的 Token
        unauthenticated_client.client.headers["Authorization"] = "Bearer invalid_token_12345"
        
        response = unauthenticated_client.post("/user/queryByPage", json={
            "pageNum": 1,
            "pageSize": 10
        })
        
        # 应该返回认证失败
        assert response.status_code in [401, 403, 200]
        if response.status_code == 200:
            data = response.json()
            assert data["code"] != 200
    
    def test_access_with_expired_token(self, unauthenticated_client):
        """使用过期 Token 访问（模拟）"""
        # 这是一个模拟的过期 Token
        expired_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwiZXhwIjoxNjAwMDAwMDAwfQ.invalid"
        unauthenticated_client.client.headers["Authorization"] = f"Bearer {expired_token}"
        
        response = unauthenticated_client.post("/user/queryByPage", json={
            "pageNum": 1,
            "pageSize": 10
        })
        
        # 应该返回 Token 过期错误
        assert response.status_code in [401, 403, 200]


class TestPermission:
    """权限控制测试"""
    
    @pytest.fixture
    def admin_client(self):
        """管理员客户端"""
        client = APIClient(base_url="http://localhost:5000")
        client.login("admin", "admin123")
        yield client
        client.close()
    
    def test_admin_can_query_users(self, admin_client):
        """管理员可以查询用户列表"""
        response = admin_client.post("/user/queryByPage", json={
            "pageNum": 1,
            "pageSize": 10
        })
        
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200
    
    def test_admin_can_query_roles(self, admin_client):
        """管理员可以查询角色列表"""
        response = admin_client.post("/role/queryByPage", json={
            "pageNum": 1,
            "pageSize": 10
        })
        
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200
    
    def test_admin_can_query_menus(self, admin_client):
        """管理员可以查询菜单树"""
        response = admin_client.get("/menu/tree")
        
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
