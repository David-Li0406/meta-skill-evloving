#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
示例08: 性能基准测试

学习目标:
- 测量接口响应时间
- 设置性能基准
- 检测性能退化
- 并发请求测试

运行方式:
    pytest test_performance.py -v
    # 或
    make 08
"""

import pytest
import httpx
import time
import statistics
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict

BASE_URL = "http://localhost:5000"


class TestResponseTime:
    """响应时间测试"""
    
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
    
    def test_login_response_time(self):
        """登录接口响应时间"""
        # 预热
        self.client.post("/login", json={
            "username": "admin",
            "password": "admin123"
        })
        
        # 测量
        start = time.time()
        response = self.client.post("/login", json={
            "username": "admin",
            "password": "admin123"
        })
        elapsed = time.time() - start
        
        assert response.status_code == 200
        assert elapsed < 1.0, f"登录响应时间过长: {elapsed:.3f}秒"
        
        print(f"\n登录响应时间: {elapsed:.3f}秒")
    
    def test_query_response_time(self):
        """查询接口响应时间"""
        start = time.time()
        response = self.client.post("/user/queryByPage", json={
            "pageNum": 1,
            "pageSize": 10
        })
        elapsed = time.time() - start
        
        assert response.status_code == 200
        assert elapsed < 2.0, f"查询响应时间过长: {elapsed:.3f}秒"
        
        print(f"\n查询响应时间: {elapsed:.3f}秒")
    
    def test_average_response_time(self):
        """平均响应时间（多次请求）"""
        times = []
        iterations = 10
        
        for _ in range(iterations):
            start = time.time()
            response = self.client.post("/user/queryByPage", json={
                "pageNum": 1,
                "pageSize": 10
            })
            elapsed = time.time() - start
            
            if response.status_code == 200:
                times.append(elapsed)
        
        if times:
            avg_time = statistics.mean(times)
            min_time = min(times)
            max_time = max(times)
            
            print(f"\n响应时间统计 ({iterations} 次请求):")
            print(f"  平均: {avg_time:.3f}秒")
            print(f"  最小: {min_time:.3f}秒")
            print(f"  最大: {max_time:.3f}秒")
            
            assert avg_time < 1.0, f"平均响应时间过长: {avg_time:.3f}秒"


class TestConcurrency:
    """并发测试"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        # 登录获取 Token
        with httpx.Client(base_url=BASE_URL, timeout=30) as client:
            response = client.post("/login", json={
                "username": "admin",
                "password": "admin123"
            })
            data = response.json()
            if data["code"] == 200 and data.get("data"):
                self.token = data["data"].get("token")
            else:
                self.token = None
        
        yield
    
    def make_request(self) -> Dict:
        """发送单个请求"""
        with httpx.Client(base_url=BASE_URL, timeout=30) as client:
            if self.token:
                client.headers["Authorization"] = f"Bearer {self.token}"
            
            start = time.time()
            try:
                response = client.post("/user/queryByPage", json={
                    "pageNum": 1,
                    "pageSize": 10
                })
                elapsed = time.time() - start
                
                return {
                    "status_code": response.status_code,
                    "success": response.json().get("code") == 200 if response.status_code == 200 else False,
                    "elapsed": elapsed,
                    "error": None
                }
            except Exception as e:
                elapsed = time.time() - start
                return {
                    "status_code": 0,
                    "success": False,
                    "elapsed": elapsed,
                    "error": str(e)
                }
    
    def test_concurrent_requests(self):
        """并发请求测试"""
        concurrent_users = 10
        requests_per_user = 5
        total_requests = concurrent_users * requests_per_user
        
        results: List[Dict] = []
        
        with ThreadPoolExecutor(max_workers=concurrent_users) as executor:
            futures = [
                executor.submit(self.make_request)
                for _ in range(total_requests)
            ]
            
            for future in as_completed(futures):
                results.append(future.result())
        
        # 统计结果
        success_count = sum(1 for r in results if r["success"])
        error_count = sum(1 for r in results if r["error"])
        times = [r["elapsed"] for r in results if not r["error"]]
        
        success_rate = success_count / total_requests * 100
        avg_time = statistics.mean(times) if times else 0
        
        print(f"\n并发测试结果 ({concurrent_users} 并发, {total_requests} 请求):")
        print(f"  成功率: {success_rate:.1f}%")
        print(f"  成功: {success_count}, 失败: {total_requests - success_count}, 错误: {error_count}")
        print(f"  平均响应时间: {avg_time:.3f}秒")
        
        # 断言
        assert success_rate >= 90, f"成功率过低: {success_rate:.1f}%"
    
    def test_stress_test(self):
        """压力测试（较大并发）"""
        concurrent_users = 20
        total_requests = 50
        
        results: List[Dict] = []
        start_time = time.time()
        
        with ThreadPoolExecutor(max_workers=concurrent_users) as executor:
            futures = [
                executor.submit(self.make_request)
                for _ in range(total_requests)
            ]
            
            for future in as_completed(futures):
                results.append(future.result())
        
        total_time = time.time() - start_time
        
        # 统计
        success_count = sum(1 for r in results if r["success"])
        success_rate = success_count / total_requests * 100
        throughput = total_requests / total_time
        
        print(f"\n压力测试结果 ({concurrent_users} 并发, {total_requests} 请求):")
        print(f"  总耗时: {total_time:.2f}秒")
        print(f"  吞吐量: {throughput:.1f} 请求/秒")
        print(f"  成功率: {success_rate:.1f}%")
        
        # 断言
        assert success_rate >= 80, f"成功率过低: {success_rate:.1f}%"


class TestPerformanceBaseline:
    """性能基准测试"""
    
    # 性能基准（根据实际情况调整）
    BASELINES = {
        "login": 0.5,           # 登录接口 < 0.5秒
        "query_list": 1.0,      # 列表查询 < 1秒
        "query_by_id": 0.3,     # 单条查询 < 0.3秒
    }
    
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
    
    def measure_api(self, name: str, method: str, path: str, **kwargs) -> float:
        """测量 API 响应时间"""
        # 预热
        if method == "GET":
            self.client.get(path, **kwargs)
        else:
            self.client.post(path, **kwargs)
        
        # 测量（取 3 次平均）
        times = []
        for _ in range(3):
            start = time.time()
            if method == "GET":
                response = self.client.get(path, **kwargs)
            else:
                response = self.client.post(path, **kwargs)
            elapsed = time.time() - start
            
            if response.status_code == 200:
                times.append(elapsed)
        
        avg_time = statistics.mean(times) if times else 0
        baseline = self.BASELINES.get(name, 1.0)
        
        status = "✓" if avg_time < baseline else "✗"
        print(f"\n{status} {name}: {avg_time:.3f}秒 (基准: {baseline}秒)")
        
        return avg_time
    
    def test_login_baseline(self):
        """登录接口性能基准"""
        # 使用新客户端（不带 Token）
        with httpx.Client(base_url=BASE_URL, timeout=30) as client:
            times = []
            for _ in range(3):
                start = time.time()
                response = client.post("/login", json={
                    "username": "admin",
                    "password": "admin123"
                })
                elapsed = time.time() - start
                if response.status_code == 200:
                    times.append(elapsed)
            
            avg_time = statistics.mean(times) if times else 0
            baseline = self.BASELINES["login"]
            
            assert avg_time < baseline, f"登录接口超过基准: {avg_time:.3f}秒 > {baseline}秒"
    
    def test_query_list_baseline(self):
        """列表查询性能基准"""
        avg_time = self.measure_api(
            "query_list",
            "POST",
            "/user/queryByPage",
            json={"pageNum": 1, "pageSize": 10}
        )
        
        baseline = self.BASELINES["query_list"]
        assert avg_time < baseline, f"列表查询超过基准: {avg_time:.3f}秒 > {baseline}秒"
    
    def test_query_by_id_baseline(self):
        """单条查询性能基准"""
        avg_time = self.measure_api(
            "query_by_id",
            "GET",
            "/user/queryById",
            params={"id": 1}
        )
        
        baseline = self.BASELINES["query_by_id"]
        assert avg_time < baseline, f"单条查询超过基准: {avg_time:.3f}秒 > {baseline}秒"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
