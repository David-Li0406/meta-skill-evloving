#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
示例07: 契约测试

学习目标:
- 验证 OpenAPI/Swagger 规范
- 校验响应结构符合契约
- 检测接口变更

运行方式:
    pytest test_contract.py -v
    # 或
    make 07
"""

import pytest
import httpx
from typing import Dict, Any, List

BASE_URL = "http://localhost:5000"


class TestOpenAPIContract:
    """OpenAPI 契约测试"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        self.client = httpx.Client(base_url=BASE_URL, timeout=30)
        self.openapi_spec = None
        
        # 获取 OpenAPI 规范
        try:
            response = self.client.get("/openapi.json")
            if response.status_code == 200:
                self.openapi_spec = response.json()
        except Exception:
            pass
        
        yield
        self.client.close()
    
    def test_openapi_available(self):
        """验证 OpenAPI 文档可访问"""
        response = self.client.get("/openapi.json")
        assert response.status_code == 200, "OpenAPI 文档不可访问"
        
        data = response.json()
        assert "openapi" in data, "缺少 openapi 版本字段"
        assert "paths" in data, "缺少 paths 字段"
        assert "info" in data, "缺少 info 字段"
    
    def test_openapi_version(self):
        """验证 OpenAPI 版本"""
        if not self.openapi_spec:
            pytest.skip("OpenAPI 文档不可用")
        
        version = self.openapi_spec.get("openapi", "")
        assert version.startswith("3."), f"期望 OpenAPI 3.x，实际 {version}"
    
    def test_login_endpoint_exists(self):
        """验证登录接口存在"""
        if not self.openapi_spec:
            pytest.skip("OpenAPI 文档不可用")
        
        paths = self.openapi_spec.get("paths", {})
        assert "/login" in paths, "登录接口不存在"
        assert "post" in paths["/login"], "登录接口应支持 POST 方法"
    
    def test_login_request_schema(self):
        """验证登录接口请求结构"""
        if not self.openapi_spec:
            pytest.skip("OpenAPI 文档不可用")
        
        paths = self.openapi_spec.get("paths", {})
        login_spec = paths.get("/login", {}).get("post", {})
        
        # 检查请求体定义
        request_body = login_spec.get("requestBody", {})
        assert request_body, "登录接口缺少 requestBody 定义"
    
    def test_login_response_schema(self):
        """验证登录接口响应结构"""
        if not self.openapi_spec:
            pytest.skip("OpenAPI 文档不可用")
        
        paths = self.openapi_spec.get("paths", {})
        login_spec = paths.get("/login", {}).get("post", {})
        
        # 检查响应定义
        responses = login_spec.get("responses", {})
        assert "200" in responses, "登录接口缺少 200 响应定义"
    
    def test_all_endpoints_have_responses(self):
        """验证所有接口都有响应定义"""
        if not self.openapi_spec:
            pytest.skip("OpenAPI 文档不可用")
        
        paths = self.openapi_spec.get("paths", {})
        
        for path, methods in paths.items():
            for method, spec in methods.items():
                if method.upper() in ["GET", "POST", "PUT", "DELETE", "PATCH"]:
                    responses = spec.get("responses", {})
                    assert responses, f"{method.upper()} {path} 缺少响应定义"


class TestResponseContract:
    """响应契约测试"""
    
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
    
    def test_standard_response_structure(self):
        """验证标准响应结构"""
        response = self.client.post("/user/queryByPage", json={
            "pageNum": 1,
            "pageSize": 10
        })
        
        assert response.status_code == 200
        data = response.json()
        
        # 验证标准响应字段
        assert "code" in data, "响应缺少 code 字段"
        assert "msg" in data, "响应缺少 msg 字段"
        assert "data" in data, "响应缺少 data 字段"
        
        # 验证字段类型
        assert isinstance(data["code"], int), "code 应为整数"
        assert isinstance(data["msg"], str), "msg 应为字符串"
    
    def test_pagination_response_structure(self):
        """验证分页响应结构"""
        response = self.client.post("/user/queryByPage", json={
            "pageNum": 1,
            "pageSize": 10
        })
        
        data = response.json()
        
        if data["code"] == 200:
            page_data = data["data"]
            
            # 验证分页字段
            assert "list" in page_data, "分页响应缺少 list 字段"
            assert "total" in page_data, "分页响应缺少 total 字段"
            assert "pageNum" in page_data, "分页响应缺少 pageNum 字段"
            assert "pageSize" in page_data, "分页响应缺少 pageSize 字段"
            
            # 验证字段类型
            assert isinstance(page_data["list"], list), "list 应为数组"
            assert isinstance(page_data["total"], int), "total 应为整数"
    
    def test_user_entity_structure(self):
        """验证用户实体结构"""
        response = self.client.get("/user/queryById", params={"id": 1})
        data = response.json()
        
        if data["code"] == 200 and data["data"]:
            user = data["data"]
            
            # 验证必须字段
            required_fields = ["id", "username"]
            for field in required_fields:
                assert field in user, f"用户实体缺少 {field} 字段"
            
            # 验证字段类型
            assert isinstance(user["id"], int), "id 应为整数"
            assert isinstance(user["username"], str), "username 应为字符串"


class TestSchemaValidator:
    """Schema 验证器"""
    
    @staticmethod
    def validate_schema(data: Any, schema: Dict) -> List[str]:
        """
        简单的 Schema 验证
        
        Args:
            data: 要验证的数据
            schema: Schema 定义
            
        Returns:
            错误列表
        """
        errors = []
        
        schema_type = schema.get("type")
        
        if schema_type == "object":
            if not isinstance(data, dict):
                errors.append(f"期望 object，实际 {type(data).__name__}")
                return errors
            
            # 验证必须字段
            required = schema.get("required", [])
            for field in required:
                if field not in data:
                    errors.append(f"缺少必须字段: {field}")
            
            # 验证属性
            properties = schema.get("properties", {})
            for field, field_schema in properties.items():
                if field in data:
                    field_errors = TestSchemaValidator.validate_schema(data[field], field_schema)
                    errors.extend([f"{field}.{e}" for e in field_errors])
        
        elif schema_type == "array":
            if not isinstance(data, list):
                errors.append(f"期望 array，实际 {type(data).__name__}")
                return errors
            
            items_schema = schema.get("items", {})
            for i, item in enumerate(data):
                item_errors = TestSchemaValidator.validate_schema(item, items_schema)
                errors.extend([f"[{i}].{e}" for e in item_errors])
        
        elif schema_type == "string":
            if not isinstance(data, str):
                errors.append(f"期望 string，实际 {type(data).__name__}")
        
        elif schema_type == "integer":
            if not isinstance(data, int):
                errors.append(f"期望 integer，实际 {type(data).__name__}")
        
        elif schema_type == "boolean":
            if not isinstance(data, bool):
                errors.append(f"期望 boolean，实际 {type(data).__name__}")
        
        return errors
    
    def test_login_response_schema(self):
        """使用 Schema 验证登录响应"""
        client = httpx.Client(base_url=BASE_URL, timeout=30)
        
        try:
            response = client.post("/login", json={
                "username": "admin",
                "password": "admin123"
            })
            
            # 定义期望的 Schema
            expected_schema = {
                "type": "object",
                "required": ["code", "msg", "data"],
                "properties": {
                    "code": {"type": "integer"},
                    "msg": {"type": "string"},
                    "data": {
                        "type": "object",
                        "properties": {
                            "token": {"type": "string"}
                        }
                    }
                }
            }
            
            data = response.json()
            errors = self.validate_schema(data, expected_schema)
            
            assert not errors, f"Schema 验证失败: {errors}"
            
        finally:
            client.close()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
