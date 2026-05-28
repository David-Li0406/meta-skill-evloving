import os
import sys
import datetime

def input_required(prompt):
    while True:
        value = input(prompt + " ").strip()
        if value:
            return value
        print("此项不能为空，请重新输入。")

def select_options(prompt, options, multiple=True):
    print(f"\n{prompt}")
    for idx, (key, desc) in enumerate(options.items()):
        print(f"{key}. {desc}")
    
    while True:
        choice_str = input(f"请选择 ({'可多选，如 A,B' if multiple else '单选'}): ").upper().replace(" ", "").strip()
        choices = choice_str.split(",")
        
        valid_choices = []
        for c in choices:
            if c in options:
                valid_choices.append(options[c])
            else:
                print(f"无效选项: {c}")
        
        if valid_choices:
            return valid_choices if multiple else valid_choices[0]
        print("未选择任何有效选项，请重试。")

def generate_plan():
    print("=== 🚀 第一性原理学习计划深度生成器 ===")
    print("基于底层逻辑，通过多维度拆解，助你构建稳固的知识体系。\n")

    # 1. 目标定义
    subject = input_required("1. 你想学习什么主题？(例如: 量子计算 / Rust编程)")
    
    purpose_options = {
        "A": "解决具体的生产/实践问题 (Problem Solving)",
        "B": "构建完整的思维模型 (Mental Model)",
        "C": "理解底层物理/数学/逻辑定律 (First Principles)",
        "D": "职业技能迁移与竞争力提升 (Carrer Growth)",
        "E": "学术考试或专业认证 (Academic)",
        "F": "建立该领域的知识地图 (Knowledge Mapping)",
        "G": "个人兴趣与跨界连接 (Interest)"
    }
    purposes = select_options("2. 你学习这个的主要目的是？", purpose_options)
    
    goal_options = {
        "A": "语义理解：能看懂相关术语和基本逻辑",
        "B": "操作入门：能模仿并完成标准流程",
        "C": "独立实践：能脱离教程解决中等难度问题",
        "D": "深度拆解：能分析该事物的基本构成元素",
        "E": "系统综合：能将不同模块组合成新系统",
        "F": "底层创新：能基于第一性原理推导新的解决方案",
        "G": "知识传授：能用大白话向外行讲透原理 (Feynman)"
    }
    goals = select_options("3. 你希望达到什么程度？", goal_options)
    
    verify_method = input_required("4. 你将如何衡量'学会'了？(例如: 写一个自己的编译器 / 讲解并录视频)")

    # 2. 现状评估
    base_options = {
        "A": "零基础：从未接触，甚至不知道基本术语",
        "B": "碎片化：看过一些资料，但没有形成体系",
        "C": "相关背景：在类似领域有经验，可以类比",
        "D": "有基础：掌握了初级技能，但感觉有瓶颈",
        "E": "偏见期：已学过但不深刻，存在'我以为我会'的错觉"
    }
    current_base = select_options("5. 你目前的基础如何？", base_options, multiple=False)
    
    # 3. 学习风格与困难
    style_options = {
        "A": "Active Recall (主动回忆)：通过自测强制提取记忆",
        "B": "Feynman Technique (费曼技巧)：模拟教学以查漏补缺",
        "C": "Deconstruction (拆解)：先将复杂主题拆成最小原子单位",
        "D": "First Principles (推导)：从公理出发，拒绝类比",
        "E": "Project-based (项目驱动)：在解决实际问题中学习",
        "F": "Interleaving (交错练习)：混合不同题型交叉学习"
    }
    styles = select_options("6. 你偏好/想尝试的学习策略？", style_options)

    # 4. 资源与约束
    time_avail = input_required("7. 每天可投入的稳定时间？(例如: 1.5小时)")
    
    # 生成 Markdown 内容
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d")
    output = f"""# 📚 第一性原理学习计划: {subject}
> **创建日期**: {timestamp} | **核心主题**: {subject}

## 🎯 需求画像 (User Persona)
- **学习目的**: {', '.join(purposes)}
- **目标水平**: {', '.join(goals)}
- **基础评估**: {current_base}
- **每日投入**: {time_avail}
- **衡量指标**: {verify_method}

## 🧠 学习策略 (Cognitive Strategies)
{chr(10).join(['- ' + s for s in styles])}

## 🏗️ 知识拆解 (First Principles Decomposition)

### 1. 原子元素 (Atomic Elements)
> 列出该主题中最基本、不可再分的真理或概念。
- [ ] 元素 A: 
- [ ] 元素 B: 

### 2. 构建模块 (Building Blocks)
> 描述这些原子如何组合成更复杂的系统。
- [ ] 模块 1: 
- [ ] 模块 2: 

## 📅 学习路径设计

### 第一阶段: 基础假设审计 (Assumption Audit)
- 检查你对 {subject} 的所有现有理解，识别哪些是"听来的"，哪些是"推导出来的"。

### 第二阶段: 深度构建 (Deep Building)
- 按照任务优先级，利用 **50/10 深度工作块** 进行学习。
- 重点关注原子元素间的逻辑连接。

### 第三阶段: 费曼压测 (Stress Test)
- 尝试通过 **{styles[0]}** 来检验对核心概念的理解。

## 🔄 科学复习节点 (Spaced Repetition)

| 轮次 | 复习时机 | 完成情况 | 核心任务 |
|:---|:---|:---:|:---|
| R1 | 1天后 | [ ] | 主动回忆核心原子概念 |
| R2 | 3天后 | [ ] | 尝试从零推导基本结论 |
| R3 | 7天后 | [ ] | 建立该知识点与其他领域的连接 |
| R4 | 14天后 | [ ] | 完成一个小型应用项目 |
| R5 | 30天后 | [ ] | 向他人讲解，消除卡顿点 |

## 🛠️ 元认知自检 (Daily Meta-Check)
1. **本质思考**: 我现在是在"记忆"步骤，还是在"理解"原理？
2. **逻辑链条**: 这个结论是从哪个基本事实推导出来的？
3. **冗余清理**: 我的理解中是否有不必要的类比？
"""
    
    # 保存文件
    safe_subject = "".join([c for c in subject if c.isalnum() or c==' ']).rstrip()
    filename = f"plan_{safe_subject.replace(' ', '_').lower()}.md"
    
    # 确保不覆盖已有文件
    counter = 1
    base_filename = filename
    while os.path.exists(filename):
        filename = f"{base_filename[:-3]}_{counter}.md"
        counter += 1

    with open(filename, "w", encoding='utf-8') as f:
        f.write(output)
    
    print(f"\n✨ 深度学习计划已生成: {filename}")
    print("提示: 第一性原理要求你不断追问'为什么'，请在打开文件后填写具体的原子元素。")

if __name__ == "__main__":
    try:
        generate_plan()
    except KeyboardInterrupt:
        print("\n\n👋 程序已停止。")
