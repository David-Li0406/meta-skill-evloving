#!/usr/bin/env python3
"""
merge_evolution.py - 增量合并经验数据

将新的经验数据合并到 evolution.json，支持去重和增量更新。

用法:
    python merge_evolution.py <skill_dir> <json_string>
    python merge_evolution.py <skill_dir> <json_file>

输入 JSON 格式:
    {
        "preferences": ["偏好1", "偏好2"],
        "fixes": ["修复1", "修复2"],
        "contexts": ["场景1", "场景2"],
        "custom_prompts": "自定义指令"
    }
"""

import os
import sys
import json
import datetime
from pathlib import Path
from typing import Union


def load_evolution(evolution_path: Path) -> dict:
    """加载现有的 evolution.json"""
    if evolution_path.exists():
        try:
            return json.loads(evolution_path.read_text(encoding='utf-8'))
        except (json.JSONDecodeError, IOError):
            pass
    return {}


def save_evolution(evolution_path: Path, data: dict) -> bool:
    """保存 evolution.json"""
    try:
        evolution_path.write_text(
            json.dumps(data, indent=2, ensure_ascii=False),
            encoding='utf-8'
        )
        return True
    except IOError as e:
        print(f"错误: 无法写入文件: {e}", file=sys.stderr)
        return False


def merge_list_dedupe(existing: list, new_items: list) -> list:
    """合并列表并去重（保持顺序）"""
    result = list(existing)
    for item in new_items:
        # 标准化比较（去除首尾空格）
        item_normalized = item.strip() if isinstance(item, str) else item
        existing_normalized = [
            x.strip() if isinstance(x, str) else x
            for x in result
        ]
        if item_normalized not in existing_normalized:
            result.append(item)
    return result


def merge_evolution(skill_dir: str, new_data: Union[str, dict]) -> bool:
    """
    合并经验数据到 evolution.json

    Args:
        skill_dir: Skill 目录路径
        new_data: JSON 字符串或字典

    Returns:
        bool: 是否成功
    """
    skill_path = Path(skill_dir)
    evolution_path = skill_path / "evolution.json"

    # 检查 Skill 目录
    if not skill_path.exists():
        print(f"错误: Skill 目录不存在: {skill_dir}", file=sys.stderr)
        return False

    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        print(f"警告: 没有找到 SKILL.md: {skill_dir}", file=sys.stderr)

    # 解析输入数据
    if isinstance(new_data, str):
        # 检查是否是文件路径
        if os.path.isfile(new_data):
            try:
                new_data = json.loads(Path(new_data).read_text(encoding='utf-8'))
            except (json.JSONDecodeError, IOError) as e:
                print(f"错误: 无法读取 JSON 文件: {e}", file=sys.stderr)
                return False
        else:
            try:
                new_data = json.loads(new_data)
            except json.JSONDecodeError as e:
                print(f"错误: 无法解析 JSON: {e}", file=sys.stderr)
                return False

    if not isinstance(new_data, dict):
        print("错误: 输入数据必须是 JSON 对象", file=sys.stderr)
        return False

    # 加载现有数据
    current_data = load_evolution(evolution_path)

    # 记录合并前的状态
    items_before = sum(len(current_data.get(k, [])) for k in ['preferences', 'fixes', 'contexts'])

    # 更新时间戳
    current_data['last_updated'] = datetime.datetime.now().isoformat()

    # 合并列表字段（去重）
    for list_key in ['preferences', 'fixes', 'contexts']:
        if list_key in new_data:
            existing_list = current_data.get(list_key, [])
            new_items = new_data[list_key]
            if isinstance(new_items, list):
                current_data[list_key] = merge_list_dedupe(existing_list, new_items)

    # 处理 custom_prompts（覆盖）
    if 'custom_prompts' in new_data and new_data['custom_prompts']:
        current_data['custom_prompts'] = new_data['custom_prompts']

    # 更新 last_evolved_hash
    if 'last_evolved_hash' in new_data:
        current_data['last_evolved_hash'] = new_data['last_evolved_hash']

    # 保存
    if not save_evolution(evolution_path, current_data):
        return False

    # 统计
    items_after = sum(len(current_data.get(k, [])) for k in ['preferences', 'fixes', 'contexts'])
    items_added = items_after - items_before

    skill_name = skill_path.name
    print(f"✅ 已合并经验数据: {skill_name}")
    print(f"   新增 {items_added} 条记录（总计 {items_after} 条）")

    return True


def main():
    import argparse

    parser = argparse.ArgumentParser(description='增量合并经验数据到 evolution.json')
    parser.add_argument('skill_dir', help='Skill 目录路径')
    parser.add_argument('json_data', help='JSON 字符串或 JSON 文件路径')

    args = parser.parse_args()

    success = merge_evolution(args.skill_dir, args.json_data)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
