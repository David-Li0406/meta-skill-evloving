#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
示例01: 基础请求

学习目标:
- 使用 httpx 发送 GET/POST 请求
- 理解请求参数和请求体
- 获取响应数据

运行方式:
    python test_basic.py
    # 或
    make 01
"""

import httpx

# 配置
BASE_URL = "http://localhost:5000"


def demo_get_request():
    """GET 请求示例"""
    print("=" * 50)
    print("1. GET 请求示例")
    print("=" * 50)
    
    # 简单 GET 请求
    response = httpx.get(f"{BASE_URL}/")
    print(f"状态码: {response.status_code}")
    
    # 带查询参数的 GET 请求
    response = httpx.get(
        f"{BASE_URL}/user/queryById",
        params={"id": 1}
    )
    print(f"带参数的 GET 请求:")
    print(f"  URL: {response.url}")
    print(f"  状态码: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"  响应: {data}")
    
    print("✓ GET 请求完成\n")


def demo_post_request():
    """POST 请求示例"""
    print("=" * 50)
    print("2. POST 请求示例")
    print("=" * 50)
    
    # POST 请求（JSON 请求体）
    response = httpx.post(
        f"{BASE_URL}/login",
        json={
            "username": "admin",
            "password": "admin123"
        }
    )
    
    print(f"POST 请求:")
    print(f"  URL: {response.url}")
    print(f"  状态码: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"  业务码: {data.get('code')}")
        print(f"  消息: {data.get('msg')}")
        
        if data.get("data") and data["data"].get("token"):
            token = data["data"]["token"]
            print(f"  Token: {token[:50]}...")
    
    print("✓ POST 请求完成\n")


def demo_response_info():
    """响应信息示例"""
    print("=" * 50)
    print("3. 响应信息详解")
    print("=" * 50)
    
    response = httpx.get(f"{BASE_URL}/")
    
    # 状态码
    print(f"状态码: {response.status_code}")
    print(f"状态短语: {response.reason_phrase}")
    
    # 响应头
    print(f"\n响应头:")
    for key, value in list(response.headers.items())[:5]:
        print(f"  {key}: {value}")
    
    # 响应时间
    print(f"\n响应时间: {response.elapsed.total_seconds():.3f}秒")
    
    # 响应内容
    print(f"\n响应内容类型: {response.headers.get('content-type')}")
    
    print("✓ 响应信息获取完成\n")


def demo_client_usage():
    """使用 Client 示例"""
    print("=" * 50)
    print("4. 使用 httpx.Client")
    print("=" * 50)
    
    # 创建客户端（推荐方式）
    with httpx.Client(base_url=BASE_URL, timeout=30) as client:
        # 登录
        response = client.post("/login", json={
            "username": "admin",
            "password": "admin123"
        })
        
        if response.status_code == 200:
            data = response.json()
            if data.get("code") == 200 and data.get("data"):
                token = data["data"].get("token")
                
                # 设置认证头
                client.headers["Authorization"] = f"Bearer {token}"
                
                # 后续请求自动携带 Token
                response = client.post("/user/queryByPage", json={
                    "pageNum": 1,
                    "pageSize": 10
                })
                
                print(f"查询用户列表:")
                print(f"  状态码: {response.status_code}")
                if response.status_code == 200:
                    result = response.json()
                    print(f"  业务码: {result.get('code')}")
                    if result.get("data") and result["data"].get("list"):
                        print(f"  用户数量: {len(result['data']['list'])}")
    
    print("✓ Client 使用完成\n")


def main():
    """主函数"""
    print("\n" + "=" * 50)
    print("API 接口测试教程 - 示例01: 基础请求")
    print("=" * 50 + "\n")
    
    try:
        demo_get_request()
        demo_post_request()
        demo_response_info()
        demo_client_usage()
        
        print("=" * 50)
        print("✓ 所有示例运行完成!")
        print("=" * 50)
        
    except httpx.ConnectError:
        print("❌ 连接失败: 请确保后端服务已启动")
        print(f"   服务地址: {BASE_URL}")
        print("   启动命令: python run.py")
    except Exception as e:
        print(f"❌ 发生错误: {e}")


if __name__ == "__main__":
    main()
