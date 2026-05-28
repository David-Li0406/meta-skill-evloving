#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
数据驱动测试示例

演示如何从外部文件（JSON/YAML/CSV）加载测试数据，
实现测试用例与测试数据分离。
"""

import json
import os
import pytest
import sys
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))
from api_client import APIClient


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
        "username": "not_exist_user",
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
    }
]

USER_CRUD_TEST_DATA = [
    {
        "case_id": "TC_USER_CREATE_001",
        "case_name": "创建普通用户",
        "action": "create",
        "data": {
            "username": "data_driven_user_001",
            "password": "Test@123456",
            "email": "user001@test.com",
            "status": 1
        },
        "expected_success": True
    },
    {
        "case_id": "TC_USER_CREATE_002",
        "case_name": "创建用户-用户名重复",
        "action": "create",
        "data": {
            "username": "admin",  # 已存在的用户名
            "password": "Test@123456",
            "status": 1
        },
        "expected_success": False
    },
    {
        "case_id": "TC_USER_QUERY_001",
        "case_name": "查询用户列表",
        "action": "query_list",
        "data": {
            "pageNum": 1,
            "pageSize": 10
        },
        "expected_success": True
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
            data.append(row)
    return data


# ========== 测试类 ==========

class TestLoginDataDriven:
    """登录接口数据驱动测试"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        self.client = APIClient(base_url="http://localhost:5000")
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
                f"[{test_case['case_id']}] {test_case['case_name']}: HTTP 状态码不匹配"
        else:
            assert response.status_code == 200
            
            # 验证业务结果
            data = response.json()
            actual_success = data["code"] == 200
            
            assert actual_success == test_case["expected_success"], \
                f"[{test_case['case_id']}] {test_case['case_name']}: " \
                f"期望={test_case['expected_success']}, 实际={actual_success}"


class TestUserCRUDDataDriven:
    """用户 CRUD 数据驱动测试"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        self.client = APIClient(base_url="http://localhost:5000")
        self.client.login()
        self.created_ids = []
        yield
        # 清理测试数据
        for id in self.created_ids:
            try:
                self.client.delete("/user/delete", params={"id": id})
            except Exception:
                pass
        self.client.close()
    
    @pytest.mark.parametrize("test_case", USER_CRUD_TEST_DATA, ids=lambda x: x["case_id"])
    def test_user_crud(self, test_case):
        """用户 CRUD 测试 - 数据驱动"""
        action = test_case["action"]
        data = test_case["data"]
        expected_success = test_case["expected_success"]
        
        if action == "create":
            response = self.client.post("/user/insert", json=data)
        elif action == "query_list":
            response = self.client.post("/user/queryByPage", json=data)
        elif action == "query_by_id":
            response = self.client.get("/user/queryById", params=data)
        elif action == "update":
            response = self.client.put("/user/update", json=data)
        elif action == "delete":
            response = self.client.delete("/user/delete", params=data)
        else:
            pytest.fail(f"未知操作: {action}")
        
        # 验证结果
        if response.status_code == 422:
            assert not expected_success, \
                f"[{test_case['case_id']}] {test_case['case_name']}: 期望成功但参数校验失败"
        else:
            result = response.json()
            actual_success = result["code"] == 200
            
            # 记录创建的数据 ID
            if action == "create" and actual_success and result.get("data"):
                if result["data"].get("id"):
                    self.created_ids.append(result["data"]["id"])
            
            assert actual_success == expected_success, \
                f"[{test_case['case_id']}] {test_case['case_name']}: " \
                f"期望={expected_success}, 实际={actual_success}, msg={result.get('msg')}"


class TestFromExternalFile:
    """从外部文件加载测试数据示例"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        self.client = APIClient(base_url="http://localhost:5000")
        yield
        self.client.close()
    
    def test_from_json_file(self):
        """从 JSON 文件加载测试数据"""
        # 示例：创建测试数据文件
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


# ========== 测试数据文件示例 ==========

"""
# login_cases.json 示例内容：
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

# login_cases.yaml 示例内容：
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

# login_cases.csv 示例内容：
case_id,case_name,username,password,expected_success
TC_001,正常登录,admin,admin123,true
TC_002,密码错误,admin,wrong,false
"""


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
