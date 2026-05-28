#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
示例09: 综合测试套件 - 项目模块测试
"""

import pytest
import httpx
from typing import List


class TestProjectQuery:
    """项目查询测试"""
    
    def test_query_project_list(self, api_client: httpx.Client):
        """查询项目列表"""
        response = api_client.post("/ApiProject/queryByPage", json={
            "pageNum": 1,
            "pageSize": 10
        })
        
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200
        assert "list" in data["data"]
    
    def test_query_project_by_id(self, api_client: httpx.Client, cleanup_projects: List[int], unique_project_name: str):
        """根据 ID 查询项目"""
        # 先创建
        create_resp = api_client.post("/ApiProject/insert", json={
            "project_name": unique_project_name,
            "status": 1
        })
        
        if create_resp.status_code == 200 and create_resp.json()["code"] == 200:
            project_id = create_resp.json()["data"]["id"]
            cleanup_projects.append(project_id)
            
            # 查询
            response = api_client.get("/ApiProject/queryById", params={"id": project_id})
            
            assert response.status_code == 200
            data = response.json()
            assert data["code"] == 200
            assert data["data"]["id"] == project_id


class TestProjectCRUD:
    """项目 CRUD 测试"""
    
    def test_create_project(self, api_client: httpx.Client, cleanup_projects: List[int], unique_project_name: str):
        """创建项目"""
        response = api_client.post("/ApiProject/insert", json={
            "project_name": unique_project_name,
            "project_desc": "测试项目描述",
            "status": 1
        })
        
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200
        
        if data.get("data") and data["data"].get("id"):
            cleanup_projects.append(data["data"]["id"])
            assert data["data"]["project_name"] == unique_project_name
    
    def test_update_project(self, api_client: httpx.Client, cleanup_projects: List[int], unique_project_name: str):
        """更新项目"""
        # 创建
        create_resp = api_client.post("/ApiProject/insert", json={
            "project_name": unique_project_name,
            "status": 1
        })
        
        if create_resp.status_code == 200 and create_resp.json()["code"] == 200:
            project_id = create_resp.json()["data"]["id"]
            cleanup_projects.append(project_id)
            
            # 更新
            new_desc = "更新后的描述"
            update_resp = api_client.put("/ApiProject/update", json={
                "id": project_id,
                "project_desc": new_desc
            })
            
            assert update_resp.status_code == 200
            
            # 验证
            query_resp = api_client.get("/ApiProject/queryById", params={"id": project_id})
            if query_resp.json()["code"] == 200:
                assert query_resp.json()["data"]["project_desc"] == new_desc
    
    def test_delete_project(self, api_client: httpx.Client, unique_project_name: str):
        """删除项目"""
        # 创建
        create_resp = api_client.post("/ApiProject/insert", json={
            "project_name": unique_project_name,
            "status": 1
        })
        
        if create_resp.status_code == 200 and create_resp.json()["code"] == 200:
            project_id = create_resp.json()["data"]["id"]
            
            # 删除
            delete_resp = api_client.delete("/ApiProject/delete", params={"id": project_id})
            assert delete_resp.status_code == 200
            
            # 验证
            query_resp = api_client.get("/ApiProject/queryById", params={"id": project_id})
            query_data = query_resp.json()
            assert query_data["data"] is None or query_data["code"] != 200
    
    def test_full_crud_workflow(self, api_client: httpx.Client, unique_project_name: str):
        """完整 CRUD 流程"""
        project_id = None
        
        try:
            # 1. Create
            create_resp = api_client.post("/ApiProject/insert", json={
                "project_name": unique_project_name,
                "project_desc": "初始描述",
                "status": 1
            })
            assert create_resp.json()["code"] == 200
            project_id = create_resp.json()["data"]["id"]
            
            # 2. Read
            read_resp = api_client.get("/ApiProject/queryById", params={"id": project_id})
            assert read_resp.json()["code"] == 200
            assert read_resp.json()["data"]["project_name"] == unique_project_name
            
            # 3. Update
            update_resp = api_client.put("/ApiProject/update", json={
                "id": project_id,
                "project_desc": "更新后的描述"
            })
            assert update_resp.json()["code"] == 200
            
            # 4. Delete
            delete_resp = api_client.delete("/ApiProject/delete", params={"id": project_id})
            assert delete_resp.json()["code"] == 200
            project_id = None  # 已删除
            
        finally:
            # 清理（如果删除失败）
            if project_id:
                api_client.delete("/ApiProject/delete", params={"id": project_id})
