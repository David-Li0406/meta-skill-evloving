#!/usr/bin/env python3
"""
GitHub API 封装
提供 GitHub API 的基础调用功能
"""

import requests
import json
import sys
from pathlib import Path

# 添加脚本目录到路径
sys.path.insert(0, str(Path(__file__).parent))
from token_manager import load_token
from utils import print_error, print_success, print_info


class GitHubAPI:
    """GitHub API 客户端"""

    def __init__(self, token=None):
        """
        初始化 GitHub API 客户端

        Args:
            token: GitHub Personal Access Token
        """
        self.token = token or load_token()
        if not self.token:
            raise Exception("GitHub Token 未配置，请先使用 token_manager.py 设置 Token")

        self.base_url = "https://api.github.com"
        self.headers = {
            "Authorization": f"token {self.token}",
            "Accept": "application/vnd.github.v3+json"
        }

    def _request(self, method, endpoint, data=None, params=None):
        """
        发送 HTTP 请求

        Args:
            method: HTTP 方法（GET, POST, PUT, DELETE）
            endpoint: API 端点
            data: 请求体数据
            params: URL 参数

        Returns:
            dict: 响应数据
        """
        url = f"{self.base_url}{endpoint}"

        try:
            if method in ['GET', 'DELETE']:
                response = requests.request(
                    method,
                    url,
                    headers=self.headers,
                    params=params
                )
            else:
                response = requests.request(
                    method,
                    url,
                    headers=self.headers,
                    json=data,
                    params=params
                )

            # 检查响应状态
            if response.status_code in [200, 201, 204]:
                if response.status_code == 204:
                    return None
                try:
                    return response.json()
                except:
                    return {"status": "success"}
            else:
                error_msg = f"API 请求失败 ({response.status_code})"
                try:
                    error_detail = response.json()
                    error_msg += f": {error_detail.get('message', '未知错误')}"
                except:
                    pass
                raise Exception(error_msg)

        except requests.exceptions.RequestException as e:
            raise Exception(f"网络请求失败: {e}")

    def get_user(self):
        """获取当前用户信息"""
        return self._request("GET", "/user")

    def get_username(self):
        """获取当前用户名"""
        user = self.get_user()
        return user.get('login', '')

    def list_repos(self, visibility='all', sort='updated'):
        """
        列出用户的所有仓库

        Args:
            visibility: all, public, private
            sort: created, updated, pushed, full_name

        Returns:
            list: 仓库列表
        """
        params = {
            'visibility': visibility,
            'sort': sort,
            'per_page': 100
        }

        repos = []
        page = 1

        while True:
            params['page'] = page
            data = self._request("GET", "/user/repos", params=params)

            if not data:
                break

            repos.extend(data)

            if len(data) < 100:
                break

            page += 1

        return repos

    def get_repo(self, owner, repo):
        """
        获取仓库信息

        Args:
            owner: 仓库所有者
            repo: 仓库名称

        Returns:
            dict: 仓库信息
        """
        return self._request("GET", f"/repos/{owner}/{repo}")

    def create_repo(self, name, description='', private=False):
        """
        创建新仓库

        Args:
            name: 仓库名称
            description: 仓库描述
            private: 是否私有

        Returns:
            dict: 创建的仓库信息
        """
        data = {
            'name': name,
            'description': description,
            'private': private,
            'auto_init': False  # 不自动创建 README
        }

        return self._request("POST", "/user/repos", data=data)

    def delete_repo(self, owner, repo):
        """
        删除仓库

        Args:
            owner: 仓库所有者
            repo: 仓库名称
        """
        return self._request("DELETE", f"/repos/{owner}/{repo}")

    def search_repos(self, query, sort='updated', order='desc'):
        """
        搜索仓库

        Args:
            query: 搜索关键词
            sort: 排序方式
            order: 排序顺序

        Returns:
            dict: 搜索结果
        """
        params = {
            'q': query,
            'sort': sort,
            'order': order,
            'per_page': 30
        }

        return self._request("GET", "/search/repositories", params=params)


if __name__ == "__main__":
    # 测试代码
    try:
        api = GitHubAPI()
        user = api.get_user()
        print(f"✅ 登录成功！用户: {user.get('login')}")
        print(f"   姓名: {user.get('name')}")
        print(f"   仓库数: {user.get('public_repos')}")

        # 列出仓库
        repos = api.list_repos()
        print(f"\n📋 你的仓库（前5个）:")
        for repo in repos[:5]:
            print(f"   - {repo.get('full_name')} ({repo.get('visibility')})")

    except Exception as e:
        print(f"❌ 错误: {e}")
