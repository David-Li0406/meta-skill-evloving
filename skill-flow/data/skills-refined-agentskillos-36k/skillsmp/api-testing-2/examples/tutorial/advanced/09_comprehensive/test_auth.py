#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
示例09: 综合测试套件 - 认证模块测试
"""

import pytest
import httpx


class TestLogin:
    """登录测试"""
    
    def test_login_success(self, unauthenticated_client: httpx.Client, admin_credentials: dict):
        """正常登录"""
        response = unauthenticated_client.post("/login", json=admin_credentials)
        
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200
        assert data["data"]["token"]
    
    def test_login_wrong_password(self, unauthenticated_client: httpx.Client):
        """密码错误"""
        response = unauthenticated_client.post("/login", json={
            "username": "admin",
            "password": "wrong_password"
        })
        
        data = response.json()
        assert data["code"] != 200
    
    def test_login_user_not_exist(self, unauthenticated_client: httpx.Client):
        """用户不存在"""
        response = unauthenticated_client.post("/login", json={
            "username": "not_exist_user_12345",
            "password": "any_password"
        })
        
        data = response.json()
        assert data["code"] != 200
    
    @pytest.mark.parametrize("username,password", [
        ("", "admin123"),
        ("admin", ""),
        ("", ""),
    ])
    def test_login_empty_credentials(self, unauthenticated_client: httpx.Client, username: str, password: str):
        """空凭证"""
        response = unauthenticated_client.post("/login", json={
            "username": username,
            "password": password
        })
        
        if response.status_code != 422:
            data = response.json()
            assert data["code"] != 200


class TestAuthorization:
    """授权测试"""
    
    def test_access_with_token(self, api_client: httpx.Client):
        """携带 Token 访问"""
        response = api_client.post("/user/queryByPage", json={
            "pageNum": 1,
            "pageSize": 10
        })
        
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200
    
    def test_access_without_token(self, unauthenticated_client: httpx.Client):
        """不携带 Token 访问"""
        response = unauthenticated_client.post("/user/queryByPage", json={
            "pageNum": 1,
            "pageSize": 10
        })
        
        if response.status_code in [401, 403]:
            pass
        else:
            data = response.json()
            assert data["code"] in [401, 403, 500]
    
    def test_access_with_invalid_token(self, unauthenticated_client: httpx.Client):
        """无效 Token"""
        unauthenticated_client.headers["Authorization"] = "Bearer invalid_token"
        
        response = unauthenticated_client.post("/user/queryByPage", json={
            "pageNum": 1,
            "pageSize": 10
        })
        
        if response.status_code in [401, 403]:
            pass
        else:
            data = response.json()
            assert data["code"] != 200
