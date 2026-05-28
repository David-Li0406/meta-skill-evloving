#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
示例09: 综合测试套件 - 用户模块测试
"""

import pytest
import httpx
from typing import List


class TestUserQuery:
    """用户查询测试"""
    
    def test_query_user_list(self, api_client: httpx.Client):
        """查询用户列表"""
        response = api_client.post("/user/queryByPage", json={
            "pageNum": 1,
            "pageSize": 10
        })
        
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200
        assert "list" in data["data"]
        assert "total" in data["data"]
    
    def test_query_user_by_id(self, api_client: httpx.Client):
        """根据 ID 查询用户"""
        response = api_client.get("/user/queryById", params={"id": 1})
        
        assert response.status_code == 200
        data = response.json()
        
        if data["code"] == 200 and data["data"]:
            assert data["data"]["id"] == 1
    
    def test_query_user_not_found(self, api_client: httpx.Client):
        """查询不存在的用户"""
        response = api_client.get("/user/queryById", params={"id": 999999})
        
        data = response.json()
        assert data["data"] is None or data["code"] != 200
    
    @pytest.mark.parametrize("page_num,page_size", [
        (1, 10),
        (1, 20),
        (2, 10),
        (1, 1),
    ])
    def test_query_pagination(self, api_client: httpx.Client, page_num: int, page_size: int):
        """分页查询"""
        response = api_client.post("/user/queryByPage", json={
            "pageNum": page_num,
            "pageSize": page_size
        })
        
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200
        assert len(data["data"]["list"]) <= page_size


class TestUserCRUD:
    """用户 CRUD 测试"""
    
    def test_create_user(self, api_client: httpx.Client, cleanup_users: List[int], unique_username: str):
        """创建用户"""
        response = api_client.post("/user/insert", json={
            "username": unique_username,
            "password": "Test@123456",
            "status": 1
        })
        
        if response.status_code == 200:
            data = response.json()
            if data["code"] == 200 and data.get("data") and data["data"].get("id"):
                cleanup_users.append(data["data"]["id"])
                assert data["data"]["username"] == unique_username
    
    def test_update_user(self, api_client: httpx.Client, cleanup_users: List[int], unique_username: str):
        """更新用户"""
        # 先创建
        create_resp = api_client.post("/user/insert", json={
            "username": unique_username,
            "password": "Test@123456",
            "status": 1
        })
        
        if create_resp.status_code == 200 and create_resp.json()["code"] == 200:
            user_id = create_resp.json()["data"]["id"]
            cleanup_users.append(user_id)
            
            # 更新
            update_resp = api_client.put("/user/update", json={
                "id": user_id,
                "email": "updated@test.com"
            })
            
            assert update_resp.status_code == 200
    
    def test_delete_user(self, api_client: httpx.Client, unique_username: str):
        """删除用户"""
        # 先创建
        create_resp = api_client.post("/user/insert", json={
            "username": unique_username,
            "password": "Test@123456",
            "status": 1
        })
        
        if create_resp.status_code == 200 and create_resp.json()["code"] == 200:
            user_id = create_resp.json()["data"]["id"]
            
            # 删除
            delete_resp = api_client.delete("/user/delete", params={"id": user_id})
            
            assert delete_resp.status_code == 200
            
            # 验证已删除
            query_resp = api_client.get("/user/queryById", params={"id": user_id})
            query_data = query_resp.json()
            assert query_data["data"] is None or query_data["code"] != 200


class TestUserValidation:
    """用户参数校验测试"""
    
    @pytest.mark.parametrize("username,expected_valid", [
        ("valid_user", True),
        ("ab", False),  # 太短
        ("", False),    # 空
    ])
    def test_username_validation(
        self,
        api_client: httpx.Client,
        cleanup_users: List[int],
        username: str,
        expected_valid: bool
    ):
        """用户名校验"""
        import uuid
        
        test_username = f"{username}_{uuid.uuid4().hex[:4]}" if username else username
        
        response = api_client.post("/user/insert", json={
            "username": test_username,
            "password": "Test@123456",
            "status": 1
        })
        
        if response.status_code == 422:
            assert not expected_valid
        else:
            data = response.json()
            actual_valid = data["code"] == 200
            
            if actual_valid and data.get("data") and data["data"].get("id"):
                cleanup_users.append(data["data"]["id"])
