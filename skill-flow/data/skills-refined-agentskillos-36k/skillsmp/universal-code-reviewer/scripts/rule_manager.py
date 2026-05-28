#!/usr/bin/env python3
"""
规则管理器：负责项目嗅探、规则持久化、上下文准备。
"""
import os
import sys
import json
from shared import get_core_foundry_root, get_rules_dir, get_references_dir, get_skill_root

def sniff_project(project_root):
    """
    通过扫描文件内容识别技术栈
    """
    tech_stack = {
        "framework": "Unknown",
        "language": "Unknown",
        "patterns": []
    }
    
    files = os.listdir(project_root) if os.path.isdir(project_root) else []
    
    # 前端项目检测
    if "package.json" in files:
        tech_stack["language"] = "Javascript/Typescript"
        with open(os.path.join(project_root, "package.json"), "r") as f:
            content = f.read()
            if "vue" in content: tech_stack["framework"] = "Vue"
            if "react" in content: tech_stack["framework"] = "React"
            if "next" in content: tech_stack["framework"] = "Next.js"
    
    # Python 项目检测
    if "requirements.txt" in files or "pyproject.toml" in files or "setup.py" in files:
        tech_stack["language"] = "Python"
        if "django" in str(files).lower(): tech_stack["framework"] = "Django"
        if "flask" in str(files).lower(): tech_stack["framework"] = "Flask"
        if "fastapi" in str(files).lower(): tech_stack["framework"] = "FastAPI"
    
    # Java 项目检测
    if "pom.xml" in files or "build.gradle" in files:
        tech_stack["language"] = "Java"
        tech_stack["framework"] = "Spring" if "pom.xml" in files else "Gradle"
    
    return tech_stack

def save_rules(project_name, content):
    rules_dir = get_rules_dir()
    rule_file = os.path.join(rules_dir, f"{project_name}.md")
    with open(rule_file, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✅ [CHECKPOINT:RULES_SAVED] 规则已持久化: {rule_file}")

def load_reference(name):
    ref_file = os.path.join(get_references_dir(), f"{name}.md")
    if os.path.exists(ref_file):
        with open(ref_file, 'r', encoding='utf-8') as f:
            return f.read()
    return f"⚠️ Reference {name} not found at {ref_file}"

def check_ready(project_name, project_root):
    """
    一键加载 CR 所需的所有上下文，并明确输出状态。
    """
    rules_dir = get_rules_dir()
    rule_file = os.path.join(rules_dir, f"{project_name}.md")
    
    print("\n" + "="*60)
    print(f"🔥 CR CONTEXT BUNDLE: {project_name}")
    print("="*60)
    
    # ========== 阶段 1: 规则检查 ==========
    rules_ready = False
    if os.path.exists(rule_file):
        print(f"\n✅ [CHECKPOINT:RULES_FOUND] Location: {rule_file}")
        print("-"*40)
        with open(rule_file, 'r', encoding='utf-8') as f:
            print(f.read())
        rules_ready = True
    else:
        print(f"\n🔴 [CHECKPOINT:RULES_MISSING] No rules for: {project_name}")
        print("🔍 Auto-sniffing project...")
        tech_stack = sniff_project(project_root)
        print(json.dumps(tech_stack, indent=2, ensure_ascii=False))
        print("\n" + "!"*60)
        print("⚠️ MANDATORY ACTION: Generate rules NOW and run:")
        print(f"   python3 scripts/rule_manager.py save {project_name} \"<RULES_CONTENT>\"")
        print("!"*60)

    # ========== 阶段 2: 注入全局红线 ==========
    # ========== 阶段 2: 注入全局红线 ==========
    print("\n" + "="*20 + " GLOBAL CHECKLIST " + "="*20)
    print(load_reference("code-quality"))
    print("\n" + "-"*40)
    print(load_reference("checklists"))


    # ========== 阶段 2: 注入输出模板 ==========
    print("\n" + "="*20 + " FEEDBACK TEMPLATE " + "="*20)
    print(load_reference("feedback-templates"))

    # ========== 最终状态判定 ==========
    print("\n" + "="*60)
    if rules_ready:
        print("✅ [STATUS:READY] All context loaded. You may proceed with CR.")
        print("="*60)
        return 0
    else:
        print("🔴 [STATUS:BLOCKED] Rules missing. You MUST save rules before CR.")
        print("="*60)
        return 1

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: rule_manager.py <sniff|save|ready> ...")
        sys.exit(1)
        
    action = sys.argv[1]
    if action == "sniff":
        tech = sniff_project(sys.argv[2])
        print(json.dumps(tech, indent=2, ensure_ascii=False))
    elif action == "save":
        save_rules(sys.argv[2], sys.argv[3])
    elif action == "ready":
        exit_code = check_ready(sys.argv[2], sys.argv[3])
        sys.exit(exit_code)
