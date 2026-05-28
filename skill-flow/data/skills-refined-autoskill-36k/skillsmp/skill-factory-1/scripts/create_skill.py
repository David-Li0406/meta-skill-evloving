#!/usr/bin/env python3
"""
create_skill.py - 从 GitHub 仓库信息创建 Skill 目录结构

根据 fetch_github_info.py 获取的仓库信息，生成标准化的 Skill 目录。

用法:
    python create_skill.py <json_file_or_string> <output_dir>

示例:
    python create_skill.py repo_info.json ./skills
    python create_skill.py '{"name":"test","url":"..."}' ./skills
"""

import sys
import os
import json
import datetime
import re
from typing import Optional


def sanitize_name(name: str) -> str:
    """将仓库名转换为合法的 Skill 名称"""
    # 转小写，替换非法字符为连字符
    safe = re.sub(r'[^a-z0-9-]', '-', name.lower())
    # 合并连续连字符
    safe = re.sub(r'-+', '-', safe)
    # 去除首尾连字符
    safe = safe.strip('-')
    # 限制长度
    return safe[:64] if safe else 'unnamed-skill'


def generate_skill_description(repo_info: dict) -> str:
    """生成 Skill 的 description 字段"""
    name = repo_info.get('name', 'Unknown')
    desc = repo_info.get('description', '')

    if desc:
        # 使用仓库描述
        base_desc = f"{desc}"
    else:
        base_desc = f"{name} 工具封装"

    # 添加触发条件
    trigger_hint = f"当用户需要使用 {name} 的功能时使用此 Skill。"

    full_desc = f"{base_desc}。{trigger_hint}"

    # 限制长度
    if len(full_desc) > 1024:
        full_desc = full_desc[:1020] + "..."

    return full_desc


def generate_skill_md(repo_info: dict, safe_name: str) -> str:
    """生成 SKILL.md 内容"""
    now = datetime.datetime.now().strftime('%Y-%m-%d')

    # 提取 README 摘要（前 800 字符）
    readme = repo_info.get('readme', '')
    readme_summary = readme[:800] + '...' if len(readme) > 800 else readme

    # 清理 README 中的徽章等
    readme_summary = re.sub(r'\[!\[.*?\]\(.*?\)\]\(.*?\)', '', readme_summary)
    readme_summary = re.sub(r'!\[.*?\]\(.*?\)', '', readme_summary)
    readme_summary = readme_summary.strip()

    content = f"""---
name: {safe_name}
description: {generate_skill_description(repo_info)}

# 生命周期管理字段
source_url: {repo_info.get('url', '')}
source_hash: {repo_info.get('latest_hash', '')}
version: 0.1.0
created_at: {now}
updated_at: {now}
evolution_enabled: true

# 可选字段
entry_point: scripts/wrapper.py
---

# {repo_info.get('name', safe_name)} Skill

> 此 Skill 由 skill-factory 自动生成，封装了 [{repo_info.get('name', '')}]({repo_info.get('url', '')}) 的功能。

## 概述

{readme_summary if readme_summary else '[TODO: 添加工具概述]'}

## 使用场景

- [TODO: 描述主要使用场景]
- [TODO: 描述触发条件]

## 核心功能

- [TODO: 列出核心功能]

## 使用方法

### 基本用法

```bash
# TODO: 添加基本用法示例
```

### 高级用法

参考 [原始仓库文档]({repo_info.get('url', '')}) 获取更多信息。

## 依赖

- [TODO: 列出依赖项]

## 实现说明

主要逻辑在 `scripts/wrapper.py` 中实现。

---

> **注意**: 此文件由 skill-factory 自动生成，请根据实际需求完善内容。
"""
    return content


def generate_wrapper_py(repo_info: dict, safe_name: str) -> str:
    """生成 wrapper.py 占位脚本"""
    name = repo_info.get('name', safe_name)

    content = f'''#!/usr/bin/env python3
"""
{name} Wrapper Script

此脚本封装了 {name} 的核心功能，供 Claude 调用。

用法:
    python wrapper.py [args...]

TODO:
    - 实现实际的调用逻辑
    - 添加参数解析
    - 添加错误处理
"""

import sys
import subprocess
from typing import List, Optional


def run_command(args: List[str]) -> tuple[int, str, str]:
    """执行命令并返回结果"""
    try:
        result = subprocess.run(
            args,
            capture_output=True,
            text=True,
            timeout=300
        )
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return -1, "", "Command timed out"
    except Exception as e:
        return -1, "", str(e)


def main(args: Optional[List[str]] = None):
    """主入口函数"""
    if args is None:
        args = sys.argv[1:]

    print(f"[{name} Wrapper]")
    print(f"This is a placeholder wrapper for {name}.")
    print(f"Arguments received: {{args}}")
    print()
    print("TODO: Implement actual invocation logic")
    print(f"Hint: Check {repo_info.get('url', 'the original repository')} for usage")

    # TODO: 实现实际逻辑
    # 示例:
    # returncode, stdout, stderr = run_command(['{name}'] + args)
    # print(stdout)
    # if stderr:
    #     print(stderr, file=sys.stderr)
    # return returncode

    return 0


if __name__ == "__main__":
    sys.exit(main())
'''
    return content


def create_skill(repo_info: dict, output_dir: str) -> str:
    """
    创建 Skill 目录结构

    Args:
        repo_info: 仓库信息字典
        output_dir: 输出目录

    Returns:
        str: 创建的 Skill 路径
    """
    # 生成安全的名称
    safe_name = sanitize_name(repo_info.get('name', 'unnamed'))
    skill_path = os.path.join(output_dir, safe_name)

    # 检查是否已存在
    if os.path.exists(skill_path):
        print(f"警告: 目录已存在: {skill_path}", file=sys.stderr)
        print("将覆盖现有文件...", file=sys.stderr)

    # 1. 创建目录结构
    os.makedirs(os.path.join(skill_path, "scripts"), exist_ok=True)
    os.makedirs(os.path.join(skill_path, "references"), exist_ok=True)
    os.makedirs(os.path.join(skill_path, "assets"), exist_ok=True)

    # 2. 创建 SKILL.md
    skill_md = generate_skill_md(repo_info, safe_name)
    with open(os.path.join(skill_path, "SKILL.md"), "w", encoding="utf-8") as f:
        f.write(skill_md)

    # 3. 创建 wrapper.py
    wrapper_py = generate_wrapper_py(repo_info, safe_name)
    with open(os.path.join(skill_path, "scripts", "wrapper.py"), "w", encoding="utf-8") as f:
        f.write(wrapper_py)

    # 4. 创建 .gitkeep 文件保持空目录
    for subdir in ["references", "assets"]:
        gitkeep_path = os.path.join(skill_path, subdir, ".gitkeep")
        if not os.path.exists(gitkeep_path):
            open(gitkeep_path, 'w').close()

    return skill_path


def main():
    if len(sys.argv) < 3:
        print("用法: python create_skill.py <json_file_or_string> <output_dir>", file=sys.stderr)
        print("示例:", file=sys.stderr)
        print("  python create_skill.py repo_info.json ./skills", file=sys.stderr)
        print('  python create_skill.py \'{"name":"test"}\' ./skills', file=sys.stderr)
        sys.exit(1)

    json_input = sys.argv[1]
    output_dir = sys.argv[2]

    # 解析 JSON（支持文件或字符串）
    if os.path.isfile(json_input):
        with open(json_input, 'r', encoding='utf-8') as f:
            repo_info = json.load(f)
    else:
        try:
            repo_info = json.loads(json_input)
        except json.JSONDecodeError as e:
            print(f"错误: 无法解析 JSON: {e}", file=sys.stderr)
            sys.exit(1)

    # 验证必需字段
    if not repo_info.get('name'):
        print("错误: JSON 中缺少 'name' 字段", file=sys.stderr)
        sys.exit(1)

    # 创建 Skill
    skill_path = create_skill(repo_info, output_dir)

    # 输出结果
    print(f"✅ Skill 创建成功: {skill_path}")
    print()
    print("下一步操作:")
    print(f"  1. 审阅并完善 {skill_path}/SKILL.md")
    print(f"  2. 实现 {skill_path}/scripts/wrapper.py 中的逻辑")
    print(f"  3. 添加必要的参考文档到 {skill_path}/references/")
    print(f"  4. 测试 Skill 功能")


if __name__ == "__main__":
    main()
