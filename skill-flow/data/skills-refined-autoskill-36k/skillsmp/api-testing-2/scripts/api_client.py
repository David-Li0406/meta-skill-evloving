#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
API 客户端封装

提供统一的 HTTP 请求封装，支持：
- JWT Token 自动管理
- 请求/响应日志
- 超时和重试配置
- 响应断言辅助

使用方法：
    python api_client.py --help

示例：
    # 作为模块导入
    from scripts.api_client import APIClient
    
    client = APIClient()
    client.login("admin", "admin123")
    response = client.get("/user/queryById", params={"id": 1})
    print(response.json())
    client.close()
"""

import argparse
import json
import sys
from typing import Any, Dict, Optional

import httpx


class APIClient:
    """API 客户端封装类"""
    
    # 默认配置
    DEFAULT_BASE_URL = "http://localhost:5000"
    DEFAULT_TIMEOUT = 30
    DEFAULT_USERNAME = "admin"
    DEFAULT_PASSWORD = "admin123"
    
    def __init__(
        self,
        base_url: str = None,
        timeout: int = None,
        auto_login: bool = False
    ):
        """
        初始化 API 客户端
        
        Args:
            base_url: API 基础地址，默认 http://localhost:5000
            timeout: 请求超时时间（秒），默认 30
            auto_login: 是否自动登录，默认 False
        """
        self.base_url = base_url or self.DEFAULT_BASE_URL
        self.timeout = timeout or self.DEFAULT_TIMEOUT
        self.token: Optional[str] = None
        self.user_info: Optional[Dict] = None
        
        # 创建 httpx 客户端
        self.client = httpx.Client(
            base_url=self.base_url,
            timeout=self.timeout,
            headers={"Content-Type": "application/json"}
        )
        
        if auto_login:
            self.login()
    
    def login(
        self,
        username: str = None,
        password: str = None
    ) -> Dict[str, Any]:
        """
        登录获取 Token
        
        Args:
            username: 用户名，默认 admin
            password: 密码，默认 admin123
            
        Returns:
            登录响应数据
        """
        response = self.client.post("/login", json={
            "username": username or self.DEFAULT_USERNAME,
            "password": password or self.DEFAULT_PASSWORD
        })
        
        data = response.json()
        
        if data.get("code") == 200 and data.get("data"):
            self.token = data["data"].get("token")
            self.user_info = data["data"].get("user_info")
            
            # 设置 Authorization 头
            if self.token:
                self.client.headers["Authorization"] = f"Bearer {self.token}"
        
        return data
    
    def logout(self) -> None:
        """退出登录，清除 Token"""
        self.token = None
        self.user_info = None
        self.client.headers.pop("Authorization", None)
    
    def get(self, path: str, **kwargs) -> httpx.Response:
        """发送 GET 请求"""
        return self.client.get(path, **kwargs)
    
    def post(self, path: str, **kwargs) -> httpx.Response:
        """发送 POST 请求"""
        return self.client.post(path, **kwargs)
    
    def put(self, path: str, **kwargs) -> httpx.Response:
        """发送 PUT 请求"""
        return self.client.put(path, **kwargs)
    
    def delete(self, path: str, **kwargs) -> httpx.Response:
        """发送 DELETE 请求"""
        return self.client.delete(path, **kwargs)
    
    def patch(self, path: str, **kwargs) -> httpx.Response:
        """发送 PATCH 请求"""
        return self.client.patch(path, **kwargs)
    
    def request(self, method: str, path: str, **kwargs) -> httpx.Response:
        """发送自定义方法请求"""
        return self.client.request(method, path, **kwargs)
    
    # ========== 断言辅助方法 ==========
    
    def assert_success(self, response: httpx.Response) -> Dict[str, Any]:
        """
        断言请求成功
        
        Args:
            response: HTTP 响应对象
            
        Returns:
            响应 JSON 数据
            
        Raises:
            AssertionError: 如果请求失败
        """
        assert response.status_code == 200, f"HTTP 状态码错误: {response.status_code}"
        
        data = response.json()
        assert data.get("code") == 200, f"业务码错误: {data.get('code')}, msg: {data.get('msg')}"
        
        return data
    
    def assert_failed(self, response: httpx.Response, expected_code: int = None) -> Dict[str, Any]:
        """
        断言请求失败
        
        Args:
            response: HTTP 响应对象
            expected_code: 期望的业务错误码
            
        Returns:
            响应 JSON 数据
        """
        data = response.json()
        assert data.get("code") != 200, f"期望失败但实际成功: {data}"
        
        if expected_code:
            assert data.get("code") == expected_code, f"错误码不匹配: 期望 {expected_code}, 实际 {data.get('code')}"
        
        return data
    
    # ========== 便捷方法 ==========
    
    def get_openapi_spec(self) -> Dict[str, Any]:
        """获取 OpenAPI 规范文档"""
        response = self.get("/openapi.json")
        return response.json()
    
    def get_api_paths(self) -> Dict[str, Any]:
        """获取所有 API 路径"""
        spec = self.get_openapi_spec()
        return spec.get("paths", {})
    
    def close(self) -> None:
        """关闭客户端连接"""
        self.client.close()
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(
        description="API 客户端工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 测试登录
  python api_client.py --test-login
  
  # 测试登录（指定账号）
  python api_client.py --test-login --username admin --password admin123
  
  # 获取 OpenAPI 文档
  python api_client.py --get-openapi
  
  # 列出所有 API 路径
  python api_client.py --list-apis
  
  # 发送 GET 请求
  python api_client.py --method GET --path /user/queryById --params '{"id": 1}'
  
  # 发送 POST 请求
  python api_client.py --method POST --path /login --body '{"username": "admin", "password": "admin123"}'
"""
    )
    
    parser.add_argument("--base-url", default="http://localhost:5000", help="API 基础地址")
    parser.add_argument("--username", default="admin", help="登录用户名")
    parser.add_argument("--password", default="admin123", help="登录密码")
    parser.add_argument("--timeout", type=int, default=30, help="请求超时时间（秒）")
    
    # 操作选项
    parser.add_argument("--test-login", action="store_true", help="测试登录")
    parser.add_argument("--get-openapi", action="store_true", help="获取 OpenAPI 文档")
    parser.add_argument("--list-apis", action="store_true", help="列出所有 API 路径")
    
    # 自定义请求
    parser.add_argument("--method", choices=["GET", "POST", "PUT", "DELETE", "PATCH"], help="请求方法")
    parser.add_argument("--path", help="请求路径")
    parser.add_argument("--params", help="查询参数（JSON 格式）")
    parser.add_argument("--body", help="请求体（JSON 格式）")
    parser.add_argument("--auth", action="store_true", help="是否需要认证")
    
    args = parser.parse_args()
    
    # 创建客户端
    client = APIClient(base_url=args.base_url, timeout=args.timeout)
    
    try:
        # 测试登录
        if args.test_login:
            print(f"正在测试登录: {args.base_url}")
            result = client.login(args.username, args.password)
            if result.get("code") == 200:
                print("✅ 登录成功")
                print(f"Token: {client.token[:50]}..." if client.token else "无 Token")
            else:
                print(f"❌ 登录失败: {result.get('msg')}")
            return
        
        # 获取 OpenAPI 文档
        if args.get_openapi:
            spec = client.get_openapi_spec()
            print(json.dumps(spec, indent=2, ensure_ascii=False))
            return
        
        # 列出所有 API
        if args.list_apis:
            paths = client.get_api_paths()
            print(f"共 {len(paths)} 个 API 路径:\n")
            for path, methods in sorted(paths.items()):
                for method in methods.keys():
                    if method.upper() in ["GET", "POST", "PUT", "DELETE", "PATCH"]:
                        print(f"  {method.upper():6} {path}")
            return
        
        # 自定义请求
        if args.method and args.path:
            # 需要认证时先登录
            if args.auth:
                client.login(args.username, args.password)
            
            # 解析参数
            params = json.loads(args.params) if args.params else None
            body = json.loads(args.body) if args.body else None
            
            # 发送请求
            response = client.request(
                args.method,
                args.path,
                params=params,
                json=body
            )
            
            print(f"状态码: {response.status_code}")
            print(f"响应:\n{json.dumps(response.json(), indent=2, ensure_ascii=False)}")
            return
        
        # 无操作时显示帮助
        parser.print_help()
        
    finally:
        client.close()


if __name__ == "__main__":
    main()
