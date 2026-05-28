#!/usr/bin/env python3
"""
GitHub Token 管理工具
安全存储和管理 GitHub Personal Access Token
"""

import os
import json
import base64
from pathlib import Path
import sys

# Token 存储路径
TOKEN_FILE = Path.home() / ".config" / "claude" / "skills" / "github-manager" / ".github_token"


def save_token(token):
    """
    保存 GitHub Token（使用 Base64 编码）

    Args:
        token: GitHub Personal Access Token
    """
    # 确保目录存在
    TOKEN_FILE.parent.mkdir(parents=True, exist_ok=True)

    # 简单编码（注意：这不是加密，只是基础混淆）
    encoded_token = base64.b64encode(token.encode()).decode()

    # 保存到文件
    with open(TOKEN_FILE, 'w') as f:
        f.write(encoded_token)

    # 设置文件权限（只有用户可读写）
    TOKEN_FILE.chmod(0o600)

    print(f"✅ Token 已保存到: {TOKEN_FILE}")


def load_token():
    """
    加载 GitHub Token

    Returns:
        str: Token 字符串，如果不存在则返回 None
    """
    if not TOKEN_FILE.exists():
        return None

    try:
        with open(TOKEN_FILE, 'r') as f:
            encoded_token = f.read().strip()

        # 解码
        token = base64.b64decode(encoded_token).decode()
        return token
    except Exception as e:
        print(f"❌ 加载 Token 失败: {e}")
        return None


def delete_token():
    """删除保存的 Token"""
    if TOKEN_FILE.exists():
        TOKEN_FILE.unlink()
        print("✅ Token 已删除")
    else:
        print("ℹ️  没有找到保存的 Token")


def check_token():
    """
    检查 Token 是否存在

    Returns:
        bool: Token 是否存在
    """
    return TOKEN_FILE.exists()


def main():
    """命令行接口"""
    if len(sys.argv) < 2:
        print("GitHub Token 管理工具\n")
        print("使用方法:")
        print("  python token_manager.py 设置 <token>    # 设置 Token")
        print("  python token_manager.py 查看           # 查看 Token")
        print("  python token_manager.py 删除           # 删除 Token")
        print("  python token_manager.py 检查           # 检查 Token 状态")
        print("\n获取 Token:")
        print("  1. 访问 https://github.com/settings/tokens")
        print("  2. 点击 'Generate new token' → 'Generate new token (classic)'")
        print("  3. 勾选权限：repo, user, delete_repo")
        print("  4. 生成并复制 Token")
        sys.exit(1)

    command = sys.argv[1]

    if command == "设置":
        if len(sys.argv) < 3:
            token = input("请输入 GitHub Token: ").strip()
        else:
            token = sys.argv[2]

        if token:
            save_token(token)
        else:
            print("❌ Token 不能为空")

    elif command == "查看":
        token = load_token()
        if token:
            # 只显示部分 Token
            masked = token[:8] + "..." + token[-4:]
            print(f"✅ Token: {masked}")
            print(f"   长度: {len(token)} 字符")
        else:
            print("❌ 未找到 Token，请先使用 '设置' 命令保存 Token")

    elif command == "删除":
        if confirm_action("确定要删除保存的 Token 吗？"):
            delete_token()

    elif command == "检查":
        if check_token():
            print("✅ Token 已配置")
        else:
            print("❌ Token 未配置")

    else:
        print(f"❌ 未知命令: {command}")
        sys.exit(1)


def confirm_action(message):
    """请求确认"""
    response = input(f"{message} (y/n): ").strip().lower()
    return response in ['y', 'yes']


if __name__ == "__main__":
    main()
