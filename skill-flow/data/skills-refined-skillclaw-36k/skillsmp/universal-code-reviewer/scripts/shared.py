#!/usr/bin/env python3
"""
共享工具模块：提供路径定位等核心函数，确保所有脚本行为一致。
"""
import os
import subprocess

def get_core_foundry_root():
    """
    智能定位真实的 core-foundry 源码仓库根目录。
    优先级：脚本推断 > Spotlight 搜索 > 回退默认
    """
    # 1. 尝试从当前脚本物理位置推断
    current_script_dir = os.path.dirname(os.path.abspath(__file__))
    prospective_root = os.path.abspath(os.path.join(current_script_dir, "../../../.."))
    if os.path.basename(prospective_root) == "core-foundry":
        return prospective_root

    # 2. 调用 Mac Spotlight 全局秒搜 core-foundry 文件夹
    try:
        cmd = ["mdfind", "kMDItemContentType == 'public.folder' && kMDItemFSName == 'core-foundry'"]
        result = subprocess.check_output(cmd).decode().splitlines()
        for path in result:
            if os.path.exists(os.path.join(path, "scripts/sync-skills.py")):
                return path
    except:
        pass
    
    return prospective_root

def get_skill_root():
    """
    定位 universal-code-reviewer Skill 的根目录
    """
    return os.path.join(get_core_foundry_root(), "skills/coding/universal-code-reviewer")

def get_rules_dir():
    """
    获取规则存放目录
    """
    rules_dir = os.path.join(get_skill_root(), "rules")
    os.makedirs(rules_dir, exist_ok=True)
    return rules_dir

def get_references_dir():
    """
    获取参考文档目录
    """
    return os.path.join(get_skill_root(), "references")
