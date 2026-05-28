#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
基础 CRUD 接口测试示例

演示如何测试标准的增删改查接口。
"""

import pytest
import sys
import os

# 添加 scripts 目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))
from api_client import APIClient


class TestApiProjectCRUD:
    """API 项目管理 CRUD 测试"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """测试前置：创建客户端并登录"""
        self.client = APIClient(base_url="http://localhost:5000")
        self.client.login()
        self.created_ids = []  # 记录创建的数据 ID，用于清理
        yield
        # 清理测试数据
        for id in self.created_ids:
            try:
                self.client.delete(f"/ApiProject/delete", params={"id": id})
            except Exception:
                pass
        self.client.close()
    
    # ========== Create 测试 ==========
    
    def test_create_project(self):
        """创建项目"""
        response = self.client.post("/ApiProject/insert", json={
            "project_name": "测试项目_001",
            "project_desc": "这是一个测试项目",
            "status": 1
        })
        
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200
        
        # 记录 ID 用于清理
        if data.get("data") and data["data"].get("id"):
            self.created_ids.append(data["data"]["id"])
    
    def test_create_project_missing_name(self):
        """创建项目 - 缺少必填字段"""
        response = self.client.post("/ApiProject/insert", json={
            "project_desc": "缺少项目名称"
        })
        
        # 应该返回参数校验错误
        assert response.status_code in [200, 422]
        if response.status_code == 200:
            data = response.json()
            assert data["code"] != 200
    
    # ========== Read 测试 ==========
    
    def test_query_project_list(self):
        """查询项目列表"""
        response = self.client.post("/ApiProject/queryByPage", json={
            "pageNum": 1,
            "pageSize": 10
        })
        
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200
        assert "list" in data["data"]
        assert "total" in data["data"]
        assert isinstance(data["data"]["list"], list)
    
    def test_query_project_by_id(self):
        """根据 ID 查询项目"""
        # 先创建一个项目
        create_resp = self.client.post("/ApiProject/insert", json={
            "project_name": "查询测试项目",
            "status": 1
        })
        create_data = create_resp.json()
        
        if create_data["code"] == 200 and create_data.get("data"):
            project_id = create_data["data"]["id"]
            self.created_ids.append(project_id)
            
            # 查询该项目
            response = self.client.get("/ApiProject/queryById", params={"id": project_id})
            
            assert response.status_code == 200
            data = response.json()
            assert data["code"] == 200
            assert data["data"]["id"] == project_id
            assert data["data"]["project_name"] == "查询测试项目"
    
    def test_query_project_not_found(self):
        """查询不存在的项目"""
        response = self.client.get("/ApiProject/queryById", params={"id": 99999})
        
        data = response.json()
        # 不存在的数据应该返回空或错误
        assert data["data"] is None or data["code"] != 200
    
    # ========== Update 测试 ==========
    
    def test_update_project(self):
        """更新项目"""
        # 先创建一个项目
        create_resp = self.client.post("/ApiProject/insert", json={
            "project_name": "待更新项目",
            "status": 1
        })
        create_data = create_resp.json()
        
        if create_data["code"] == 200 and create_data.get("data"):
            project_id = create_data["data"]["id"]
            self.created_ids.append(project_id)
            
            # 更新项目
            response = self.client.put("/ApiProject/update", json={
                "id": project_id,
                "project_name": "已更新项目",
                "project_desc": "更新后的描述"
            })
            
            assert response.status_code == 200
            data = response.json()
            assert data["code"] == 200
            
            # 验证更新结果
            query_resp = self.client.get("/ApiProject/queryById", params={"id": project_id})
            query_data = query_resp.json()
            assert query_data["data"]["project_name"] == "已更新项目"
    
    # ========== Delete 测试 ==========
    
    def test_delete_project(self):
        """删除项目"""
        # 先创建一个项目
        create_resp = self.client.post("/ApiProject/insert", json={
            "project_name": "待删除项目",
            "status": 1
        })
        create_data = create_resp.json()
        
        if create_data["code"] == 200 and create_data.get("data"):
            project_id = create_data["data"]["id"]
            
            # 删除项目
            response = self.client.delete("/ApiProject/delete", params={"id": project_id})
            
            assert response.status_code == 200
            data = response.json()
            assert data["code"] == 200
            
            # 验证已删除
            query_resp = self.client.get("/ApiProject/queryById", params={"id": project_id})
            query_data = query_resp.json()
            assert query_data["data"] is None or query_data["code"] != 200


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
