#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
示例02: 响应验证

学习目标:
- 验证 HTTP 状态码
- 验证响应 JSON 结构
- 使用 pytest 断言

运行方式:
    pytest test_validation.py -v
    # 或
    make 02
"""

import pytest
import httpx

BASE_URL = "http://localhost:5000"


class TestResponseValidation:
    """响应验证测试"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """测试前置"""
        self.client = httpx.Client(base_url=BASE_URL, timeout=30)
        yield
        self.client.close()
    
    # ========== 状态码验证 ==========
    
    def test_status_code_200(self):
        """验证成功状态码"""
        response = self.client.get("/")
        assert response.status_code == 200, f"期望 200，实际 {response.status_code}"
    
    def test_status_code_404(self):
        """验证 404 状态码"""
        response = self.client.get("/not_exist_path")
        assert response.status_code == 404, f"期望 404，实际 {response.status_code}"
    
    # ========== JSON 结构验证 ==========
    
    def test_json_structure(self):
        """验证 JSON 响应结构"""
        response = self.client.post("/login", json={
            "username": "admin",
            "password": "admin123"
        })
        
        assert response.status_code == 200
        
        data = response.json()
        
        # 验证必须字段存在
        assert "code" in data, "响应缺少 code 字段"
        assert "msg" in data, "响应缺少 msg 字段"
        assert "data" in data, "响应缺少 data 字段"
    
    def test_business_code(self):
        """验证业务状态码"""
        response = self.client.post("/login", json={
            "username": "admin",
            "password": "admin123"
        })
        
        data = response.json()
        
        # 验证业务码
        assert data["code"] == 200, f"业务码错误: {data['code']}, msg: {data.get('msg')}"
    
    def test_data_not_null(self):
        """验证数据不为空"""
        response = self.client.post("/login", json={
            "username": "admin",
            "password": "admin123"
        })
        
        data = response.json()
        
        assert data["code"] == 200
        assert data["data"] is not None, "data 不应为空"
        assert data["data"].get("token"), "token 不应为空"
    
    # ========== 数据类型验证 ==========
    
    def test_data_types(self):
        """验证数据类型"""
        # 先登录
        login_resp = self.client.post("/login", json={
            "username": "admin",
            "password": "admin123"
        })
        token = login_resp.json()["data"]["token"]
        self.client.headers["Authorization"] = f"Bearer {token}"
        
        # 查询列表
        response = self.client.post("/user/queryByPage", json={
            "pageNum": 1,
            "pageSize": 10
        })
        
        data = response.json()
        
        if data["code"] == 200:
            # 验证类型
            assert isinstance(data["data"]["list"], list), "list 应为数组"
            assert isinstance(data["data"]["total"], int), "total 应为整数"
            assert isinstance(data["data"]["pageNum"], int), "pageNum 应为整数"
    
    # ========== 字段值验证 ==========
    
    def test_field_values(self):
        """验证字段值"""
        # 登录
        login_resp = self.client.post("/login", json={
            "username": "admin",
            "password": "admin123"
        })
        token = login_resp.json()["data"]["token"]
        self.client.headers["Authorization"] = f"Bearer {token}"
        
        # 查询指定用户
        response = self.client.get("/user/queryById", params={"id": 1})
        data = response.json()
        
        if data["code"] == 200 and data["data"]:
            user = data["data"]
            
            # 验证字段值
            assert user["id"] == 1, f"ID 不匹配: {user['id']}"
            assert "username" in user, "缺少 username 字段"
            assert user["username"], "username 不应为空"
    
    # ========== 响应时间验证 ==========
    
    def test_response_time(self):
        """验证响应时间"""
        response = self.client.get("/")
        
        elapsed = response.elapsed.total_seconds()
        assert elapsed < 2.0, f"响应时间过长: {elapsed:.2f}秒"
    
    # ========== 响应头验证 ==========
    
    def test_response_headers(self):
        """验证响应头"""
        response = self.client.get("/")
        
        # 验证 Content-Type
        content_type = response.headers.get("content-type", "")
        assert "application/json" in content_type or "text/html" in content_type


class TestErrorResponses:
    """错误响应验证"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        self.client = httpx.Client(base_url=BASE_URL, timeout=30)
        yield
        self.client.close()
    
    def test_login_wrong_password(self):
        """验证密码错误响应"""
        response = self.client.post("/login", json={
            "username": "admin",
            "password": "wrong_password"
        })
        
        data = response.json()
        
        # 密码错误应返回非 200 业务码
        assert data["code"] != 200, "密码错误应返回失败"
    
    def test_login_empty_username(self):
        """验证空用户名响应"""
        response = self.client.post("/login", json={
            "username": "",
            "password": "admin123"
        })
        
        # 应返回参数校验错误
        if response.status_code == 422:
            # FastAPI 参数校验错误
            pass
        else:
            data = response.json()
            assert data["code"] != 200, "空用户名应返回失败"
    
    def test_unauthorized_access(self):
        """验证未授权访问"""
        # 不携带 Token 访问受保护接口
        response = self.client.post("/user/queryByPage", json={
            "pageNum": 1,
            "pageSize": 10
        })
        
        # 应返回 401 或业务错误码
        if response.status_code == 401:
            pass  # HTTP 401
        else:
            data = response.json()
            # 业务层面的未授权错误
            assert data["code"] in [401, 403, 500], f"未授权应返回错误: {data['code']}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
