#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
示例04: CRUD 测试

学习目标:
- 测试创建（Create）接口
- 测试查询（Read）接口
- 测试更新（Update）接口
- 测试删除（Delete）接口
- 测试数据清理

运行方式:
    pytest test_crud.py -v
    # 或
    make 04
"""

import pytest
import httpx
import uuid

BASE_URL = "http://localhost:5000"


class TestProjectCRUD:
    """项目管理 CRUD 测试"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """测试前置"""
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
        
        # 记录创建的数据 ID，用于清理
        self.created_ids = []
        
        yield
        
        # 清理测试数据
        for id in self.created_ids:
            try:
                self.client.delete("/ApiProject/delete", params={"id": id})
            except Exception:
                pass
        
        self.client.close()
    
    # ========== Create 测试 ==========
    
    def test_create_success(self):
        """创建成功"""
        unique_name = f"测试项目_{uuid.uuid4().hex[:8]}"
        
        response = self.client.post("/ApiProject/insert", json={
            "project_name": unique_name,
            "project_desc": "这是一个测试项目",
            "status": 1
        })
        
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200, f"创建失败: {data.get('msg')}"
        
        # 记录 ID 用于清理
        if data.get("data") and data["data"].get("id"):
            self.created_ids.append(data["data"]["id"])
            
            # 验证返回的数据
            assert data["data"]["project_name"] == unique_name
    
    def test_create_missing_required_field(self):
        """创建失败 - 缺少必填字段"""
        response = self.client.post("/ApiProject/insert", json={
            "project_desc": "缺少项目名称"
            # 缺少 project_name
        })
        
        # 应返回参数校验错误
        if response.status_code == 422:
            pass  # FastAPI 参数校验
        else:
            data = response.json()
            assert data["code"] != 200, "缺少必填字段应创建失败"
    
    def test_create_duplicate_name(self):
        """创建失败 - 名称重复（如果有唯一约束）"""
        unique_name = f"重复测试_{uuid.uuid4().hex[:8]}"
        
        # 第一次创建
        response = self.client.post("/ApiProject/insert", json={
            "project_name": unique_name,
            "status": 1
        })
        
        if response.json()["code"] == 200:
            self.created_ids.append(response.json()["data"]["id"])
            
            # 第二次创建相同名称
            response2 = self.client.post("/ApiProject/insert", json={
                "project_name": unique_name,
                "status": 1
            })
            
            # 根据业务逻辑，可能允许重复或不允许
            # 这里只是示例，实际根据业务调整
    
    # ========== Read 测试 ==========
    
    def test_query_list(self):
        """查询列表"""
        response = self.client.post("/ApiProject/queryByPage", json={
            "pageNum": 1,
            "pageSize": 10
        })
        
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200
        
        # 验证分页结构
        assert "list" in data["data"], "响应缺少 list 字段"
        assert "total" in data["data"], "响应缺少 total 字段"
        assert isinstance(data["data"]["list"], list)
    
    def test_query_by_id(self):
        """根据 ID 查询"""
        # 先创建一条数据
        unique_name = f"查询测试_{uuid.uuid4().hex[:8]}"
        create_resp = self.client.post("/ApiProject/insert", json={
            "project_name": unique_name,
            "status": 1
        })
        
        if create_resp.json()["code"] == 200:
            project_id = create_resp.json()["data"]["id"]
            self.created_ids.append(project_id)
            
            # 查询该数据
            response = self.client.get("/ApiProject/queryById", params={"id": project_id})
            
            assert response.status_code == 200
            data = response.json()
            assert data["code"] == 200
            assert data["data"]["id"] == project_id
            assert data["data"]["project_name"] == unique_name
    
    def test_query_not_found(self):
        """查询不存在的数据"""
        response = self.client.get("/ApiProject/queryById", params={"id": 999999})
        
        data = response.json()
        # 不存在的数据应返回空或错误
        assert data["data"] is None or data["code"] != 200
    
    # ========== Update 测试 ==========
    
    def test_update_success(self):
        """更新成功"""
        # 先创建
        unique_name = f"更新测试_{uuid.uuid4().hex[:8]}"
        create_resp = self.client.post("/ApiProject/insert", json={
            "project_name": unique_name,
            "status": 1
        })
        
        if create_resp.json()["code"] == 200:
            project_id = create_resp.json()["data"]["id"]
            self.created_ids.append(project_id)
            
            # 更新
            new_name = f"已更新_{uuid.uuid4().hex[:8]}"
            response = self.client.put("/ApiProject/update", json={
                "id": project_id,
                "project_name": new_name,
                "project_desc": "更新后的描述"
            })
            
            assert response.status_code == 200
            data = response.json()
            assert data["code"] == 200
            
            # 验证更新结果
            query_resp = self.client.get("/ApiProject/queryById", params={"id": project_id})
            query_data = query_resp.json()
            assert query_data["data"]["project_name"] == new_name
    
    def test_update_not_found(self):
        """更新不存在的数据"""
        response = self.client.put("/ApiProject/update", json={
            "id": 999999,
            "project_name": "不存在的项目"
        })
        
        # 应返回错误
        data = response.json()
        # 根据业务逻辑可能返回不同错误码
    
    # ========== Delete 测试 ==========
    
    def test_delete_success(self):
        """删除成功"""
        # 先创建
        unique_name = f"删除测试_{uuid.uuid4().hex[:8]}"
        create_resp = self.client.post("/ApiProject/insert", json={
            "project_name": unique_name,
            "status": 1
        })
        
        if create_resp.json()["code"] == 200:
            project_id = create_resp.json()["data"]["id"]
            # 不加入 created_ids，因为要测试删除
            
            # 删除
            response = self.client.delete("/ApiProject/delete", params={"id": project_id})
            
            assert response.status_code == 200
            data = response.json()
            assert data["code"] == 200
            
            # 验证已删除
            query_resp = self.client.get("/ApiProject/queryById", params={"id": project_id})
            query_data = query_resp.json()
            assert query_data["data"] is None or query_data["code"] != 200
    
    def test_delete_not_found(self):
        """删除不存在的数据"""
        response = self.client.delete("/ApiProject/delete", params={"id": 999999})
        
        # 根据业务逻辑，可能返回成功或失败
        # 这里只是示例


class TestCRUDWorkflow:
    """CRUD 完整流程测试"""
    
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
        
        yield
        self.client.close()
    
    def test_full_crud_workflow(self):
        """完整 CRUD 流程"""
        unique_name = f"流程测试_{uuid.uuid4().hex[:8]}"
        
        # 1. Create
        create_resp = self.client.post("/ApiProject/insert", json={
            "project_name": unique_name,
            "project_desc": "初始描述",
            "status": 1
        })
        assert create_resp.json()["code"] == 200, "创建失败"
        project_id = create_resp.json()["data"]["id"]
        
        try:
            # 2. Read
            read_resp = self.client.get("/ApiProject/queryById", params={"id": project_id})
            assert read_resp.json()["code"] == 200, "查询失败"
            assert read_resp.json()["data"]["project_name"] == unique_name
            
            # 3. Update
            new_name = f"更新后_{uuid.uuid4().hex[:8]}"
            update_resp = self.client.put("/ApiProject/update", json={
                "id": project_id,
                "project_name": new_name,
                "project_desc": "更新后的描述"
            })
            assert update_resp.json()["code"] == 200, "更新失败"
            
            # 验证更新
            verify_resp = self.client.get("/ApiProject/queryById", params={"id": project_id})
            assert verify_resp.json()["data"]["project_name"] == new_name
            
            # 4. Delete
            delete_resp = self.client.delete("/ApiProject/delete", params={"id": project_id})
            assert delete_resp.json()["code"] == 200, "删除失败"
            
            # 验证删除
            final_resp = self.client.get("/ApiProject/queryById", params={"id": project_id})
            assert final_resp.json()["data"] is None or final_resp.json()["code"] != 200
            
        except AssertionError:
            # 清理
            self.client.delete("/ApiProject/delete", params={"id": project_id})
            raise


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
