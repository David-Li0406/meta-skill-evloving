#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
示例06: 数据驱动测试 ⭐

学习目标:
- 从 JSON/YAML 文件加载测试数据
- 实现测试用例与数据分离
- 便于维护和扩展

运行方式:
    pytest test_data_driven.py -v
    # 或
    make 06
"""

import json
import os
import pytest
import httpx
from pathlib import Path

BASE_URL = "http://localhost:5000"

# ========== 测试数据定义 ==========

# 方式1：直接在代码中定义测试数据
LOGIN_TEST_DATA = [
    {
        "case_id": "TC_LOGIN_001",
        "case_name": "正常登录",
        "username": "admin",
        "password": "admin123",
        "expected_code": 200,
        "expected_success": True
    },
    {
        "case_id": "TC_LOGIN_002",
        "case_name": "密码错误",
        "username": "admin",
        "password": "wrong_password",
        "expected_code": 200,
        "expected_success": False
    },
    {
        "case_id": "TC_LOGIN_003",
        "case_name": "用户不存在",
        "username": "not_exist_user_12345",
        "password": "any_password",
        "expected_code": 200,
        "expected_success": False
    },
    {
        "case_id": "TC_LOGIN_004",
        "case_name": "用户名为空",
        "username": "",
        "password": "admin123",
        "expected_code": 422,
        "expected_success": False
    },
    {
        "case_id": "TC_LOGIN_005",
        "case_name": "密码为空",
        "username": "admin",
        "password": "",
        "expected_code": 200,
        "expected_success": False
    }
]

API_TEST_DATA = [
    {
        "case_id": "TC_API_001",
        "case_name": "查询用户列表",
        "method": "POST",
        "path": "/user/queryByPage",
        "need_auth": True,
        "body": {"pageNum": 1, "pageSize": 10},
        "expected_code": 200
    },
    {
        "case_id": "TC_API_002",
        "case_name": "查询角色列表",
        "method": "POST",
        "path": "/role/queryByPage",
        "need_auth": True,
        "body": {"pageNum": 1, "pageSize": 10},
        "expected_code": 200
    },
    {
        "case_id": "TC_API_003",
        "case_name": "未授权访问",
        "method": "POST",
        "path": "/user/queryByPage",
        "need_auth": False,
        "body": {"pageNum": 1, "pageSize": 10},
        "expected_code": 401  # 或其他未授权错误码
    }
]


# ========== 数据加载工具 ==========

def load_test_data_from_json(file_path: str) -> list:
    """从 JSON 文件加载测试数据"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def load_test_data_from_yaml(file_path: str) -> list:
    """从 YAML 文件加载测试数据"""
    try:
        import yaml
        with open(file_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except ImportError:
        pytest.skip("需要安装 pyyaml: pip install pyyaml")


def load_test_data_from_csv(file_path: str) -> list:
    """从 CSV 文件加载测试数据"""
    import csv
    data = []
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # 转换布尔值
            for key, value in row.items():
                if value.lower() == 'true':
                    row[key] = True
                elif value.lower() == 'false':
                    row[key] = False
            data.append(row)
    return data


# ========== 测试类 ==========

class TestLoginDataDriven:
    """登录接口数据驱动测试"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        self.client = httpx.Client(base_url=BASE_URL, timeout=30)
        yield
        self.client.close()
    
    @pytest.mark.parametrize("test_case", LOGIN_TEST_DATA, ids=lambda x: x["case_id"])
    def test_login(self, test_case):
        """登录测试 - 数据驱动"""
        response = self.client.post("/login", json={
            "username": test_case["username"],
            "password": test_case["password"]
        })
        
        # 验证 HTTP 状态码
        if test_case["expected_code"] == 422:
            assert response.status_code == 422, \
                f"[{test_case['case_id']}] {test_case['case_name']}: 期望 422，实际 {response.status_code}"
        else:
            assert response.status_code == 200, \
                f"[{test_case['case_id']}] {test_case['case_name']}: HTTP 状态码错误"
            
            # 验证业务结果
            data = response.json()
            actual_success = data["code"] == 200
            
            assert actual_success == test_case["expected_success"], \
                f"[{test_case['case_id']}] {test_case['case_name']}: " \
                f"期望={test_case['expected_success']}, 实际={actual_success}, msg={data.get('msg')}"


class TestAPIDataDriven:
    """API 接口数据驱动测试"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        self.client = httpx.Client(base_url=BASE_URL, timeout=30)
        self.token = None
        
        # 登录获取 Token
        response = self.client.post("/login", json={
            "username": "admin",
            "password": "admin123"
        })
        data = response.json()
        if data["code"] == 200 and data.get("data"):
            self.token = data["data"].get("token")
        
        yield
        self.client.close()
    
    @pytest.mark.parametrize("test_case", API_TEST_DATA, ids=lambda x: x["case_id"])
    def test_api(self, test_case):
        """API 测试 - 数据驱动"""
        # 设置认证
        if test_case.get("need_auth") and self.token:
            self.client.headers["Authorization"] = f"Bearer {self.token}"
        else:
            self.client.headers.pop("Authorization", None)
        
        # 发送请求
        method = test_case["method"].upper()
        path = test_case["path"]
        body = test_case.get("body")
        params = test_case.get("params")
        
        if method == "GET":
            response = self.client.get(path, params=params)
        elif method == "POST":
            response = self.client.post(path, json=body)
        elif method == "PUT":
            response = self.client.put(path, json=body)
        elif method == "DELETE":
            response = self.client.delete(path, params=params)
        else:
            response = self.client.request(method, path, json=body)
        
        # 验证结果
        expected_code = test_case["expected_code"]
        
        if expected_code in [401, 403]:
            # 未授权场景
            if response.status_code in [401, 403]:
                pass  # HTTP 层面的未授权
            else:
                data = response.json()
                assert data["code"] in [401, 403, 500], \
                    f"[{test_case['case_id']}] {test_case['case_name']}: 期望未授权错误"
        else:
            assert response.status_code == 200, \
                f"[{test_case['case_id']}] {test_case['case_name']}: HTTP 状态码错误"
            
            data = response.json()
            assert data["code"] == expected_code, \
                f"[{test_case['case_id']}] {test_case['case_name']}: " \
                f"期望业务码={expected_code}, 实际={data['code']}"


class TestFromExternalFile:
    """从外部文件加载测试数据示例"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        self.client = httpx.Client(base_url=BASE_URL, timeout=30)
        yield
        self.client.close()
    
    def test_from_json_file(self):
        """从 JSON 文件加载测试数据"""
        test_data_file = Path(__file__).parent / "test_data" / "login_cases.json"
        
        if test_data_file.exists():
            test_cases = load_test_data_from_json(str(test_data_file))
            
            for case in test_cases:
                response = self.client.post("/login", json={
                    "username": case["username"],
                    "password": case["password"]
                })
                
                if response.status_code != 422:
                    data = response.json()
                    actual_success = data["code"] == 200
                    assert actual_success == case["expected_success"], \
                        f"[{case['case_id']}] 测试失败"
        else:
            pytest.skip(f"测试数据文件不存在: {test_data_file}")


class TestDataDrivenWithSetupTeardown:
    """带前置后置的数据驱动测试"""
    
    CRUD_TEST_DATA = [
        {
            "case_id": "TC_CRUD_001",
            "case_name": "创建并查询",
            "create_data": {"project_name": "数据驱动测试项目", "status": 1},
            "expected_create": True,
            "expected_query": True
        }
    ]
    
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
        
        self.created_ids = []
        yield
        
        # 清理
        for id in self.created_ids:
            try:
                self.client.delete("/ApiProject/delete", params={"id": id})
            except Exception:
                pass
        self.client.close()
    
    @pytest.mark.parametrize("test_case", CRUD_TEST_DATA, ids=lambda x: x["case_id"])
    def test_crud_data_driven(self, test_case):
        """CRUD 数据驱动测试"""
        import uuid
        
        # 添加唯一后缀避免重复
        create_data = test_case["create_data"].copy()
        create_data["project_name"] = f"{create_data['project_name']}_{uuid.uuid4().hex[:8]}"
        
        # 创建
        response = self.client.post("/ApiProject/insert", json=create_data)
        
        if response.status_code == 422:
            assert not test_case["expected_create"], f"[{test_case['case_id']}] 创建应成功"
            return
        
        data = response.json()
        actual_create = data["code"] == 200
        assert actual_create == test_case["expected_create"], \
            f"[{test_case['case_id']}] 创建结果不匹配"
        
        if actual_create and data.get("data") and data["data"].get("id"):
            project_id = data["data"]["id"]
            self.created_ids.append(project_id)
            
            # 查询
            query_resp = self.client.get("/ApiProject/queryById", params={"id": project_id})
            query_data = query_resp.json()
            actual_query = query_data["code"] == 200 and query_data["data"] is not None
            
            assert actual_query == test_case["expected_query"], \
                f"[{test_case['case_id']}] 查询结果不匹配"


# ========== 测试数据文件示例 ==========

"""
创建 test_data/login_cases.json 文件：

[
    {
        "case_id": "TC_001",
        "case_name": "正常登录",
        "username": "admin",
        "password": "admin123",
        "expected_success": true
    },
    {
        "case_id": "TC_002",
        "case_name": "密码错误",
        "username": "admin",
        "password": "wrong",
        "expected_success": false
    }
]

创建 test_data/login_cases.yaml 文件：

- case_id: TC_001
  case_name: 正常登录
  username: admin
  password: admin123
  expected_success: true

- case_id: TC_002
  case_name: 密码错误
  username: admin
  password: wrong
  expected_success: false

创建 test_data/login_cases.csv 文件：

case_id,case_name,username,password,expected_success
TC_001,正常登录,admin,admin123,true
TC_002,密码错误,admin,wrong,false
"""


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
