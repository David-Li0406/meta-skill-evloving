#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
示例09: 综合测试套件 - 共享 Fixtures

这个文件定义了测试套件中共享的 fixtures。
"""

import pytest
import httpx
import uuid
from typing import Generator, List

BASE_URL = "http://localhost:5000"


@pytest.fixture(scope="session")
def base_url() -> str:
    """API 基础地址"""
    return BASE_URL


@pytest.fixture(scope="session")
def admin_credentials() -> dict:
    """管理员凭证"""
    return {
        "username": "admin",
        "password": "admin123"
    }


@pytest.fixture(scope="session")
def session_client(base_url: str, admin_credentials: dict) -> Generator[httpx.Client, None, None]:
    """
    会话级别的 API 客户端
    整个测试会话只创建一次，所有测试共享
    """
    client = httpx.Client(base_url=base_url, timeout=30)
    
    # 登录
    response = client.post("/login", json=admin_credentials)
    data = response.json()
    
    if data["code"] == 200 and data.get("data"):
        token = data["data"].get("token")
        if token:
            client.headers["Authorization"] = f"Bearer {token}"
    
    yield client
    
    client.close()


@pytest.fixture
def api_client(base_url: str, admin_credentials: dict) -> Generator[httpx.Client, None, None]:
    """
    函数级别的 API 客户端
    每个测试函数创建新的客户端
    """
    client = httpx.Client(base_url=base_url, timeout=30)
    
    # 登录
    response = client.post("/login", json=admin_credentials)
    data = response.json()
    
    if data["code"] == 200 and data.get("data"):
        token = data["data"].get("token")
        if token:
            client.headers["Authorization"] = f"Bearer {token}"
    
    yield client
    
    client.close()


@pytest.fixture
def unauthenticated_client(base_url: str) -> Generator[httpx.Client, None, None]:
    """未认证的客户端"""
    client = httpx.Client(base_url=base_url, timeout=30)
    yield client
    client.close()


@pytest.fixture
def cleanup_users(api_client: httpx.Client) -> Generator[List[int], None, None]:
    """
    用户数据清理 fixture
    
    使用方式:
        def test_create_user(api_client, cleanup_users):
            response = api_client.post("/user/insert", json={...})
            user_id = response.json()["data"]["id"]
            cleanup_users.append(user_id)  # 测试结束后自动清理
    """
    created_ids: List[int] = []
    yield created_ids
    
    # 清理
    for user_id in created_ids:
        try:
            api_client.delete("/user/delete", params={"id": user_id})
        except Exception:
            pass


@pytest.fixture
def cleanup_projects(api_client: httpx.Client) -> Generator[List[int], None, None]:
    """项目数据清理 fixture"""
    created_ids: List[int] = []
    yield created_ids
    
    for project_id in created_ids:
        try:
            api_client.delete("/ApiProject/delete", params={"id": project_id})
        except Exception:
            pass


@pytest.fixture
def unique_username() -> str:
    """生成唯一用户名"""
    return f"test_user_{uuid.uuid4().hex[:8]}"


@pytest.fixture
def unique_project_name() -> str:
    """生成唯一项目名"""
    return f"test_project_{uuid.uuid4().hex[:8]}"


# ========== 辅助函数 ==========

def assert_success_response(response: httpx.Response, msg: str = "") -> dict:
    """
    断言成功响应
    
    Args:
        response: HTTP 响应
        msg: 错误消息前缀
        
    Returns:
        响应 JSON 数据
    """
    assert response.status_code == 200, f"{msg}HTTP 状态码错误: {response.status_code}"
    
    data = response.json()
    assert data["code"] == 200, f"{msg}业务码错误: {data['code']}, msg: {data.get('msg')}"
    
    return data


def assert_error_response(response: httpx.Response, expected_codes: List[int] = None) -> dict:
    """
    断言错误响应
    
    Args:
        response: HTTP 响应
        expected_codes: 期望的错误码列表
        
    Returns:
        响应 JSON 数据
    """
    if response.status_code in [401, 403, 404, 422]:
        return {"code": response.status_code}
    
    data = response.json()
    
    if expected_codes:
        assert data["code"] in expected_codes, f"错误码不匹配: {data['code']}"
    else:
        assert data["code"] != 200, f"期望错误但返回成功"
    
    return data
