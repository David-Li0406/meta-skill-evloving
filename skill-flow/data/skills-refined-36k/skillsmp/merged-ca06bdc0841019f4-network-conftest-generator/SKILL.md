---
name: network-conftest-generator
description: Use this skill to generate and configure a pytest `conftest.py` for automating H3C network devices, ensuring a consistent testing environment.
---

# 网络测试环境生成器

## 目标
参考工作流程制定`Todo List`, 按照任务列表, 生成 `conftest.py` 文件，该文件是网络设备测试背景的代码文件。它负责测试背景搭建和测试背景清理，确保所有网络测试用例在统一的组网环境中执行并提供设备资源、拓扑配置和测试数据的共享机制。

## 核心资源：H3C 知识库检索指南
**重要策略：** 检索必须遵循 **“循环迭代”** 和 **“全库扫描”** 的原则。

**可用知识库（每一轮检索都必须覆盖以下所有库）：**
1. **design_ke** (用户设计经验库)
2. **background_ke** (历史背景库，conftest.py代码仓库)
3. **v9_press_example** (常见组网配置库)
4. **example_ke** (测试用例实现库)
5. **cmd_ke** (具体的命令行/配置参数库)
6. **press_config_des** (标准化配置步骤/流程)

**知识库检索脚本：**

使用以下`bash`脚本可以完成指定的知识库检索。
1. **design_ke库检索**: 
   ```bash
   python {当前skill路径}/script/data_search_h3c_example.py --description "IGMP snooping查询组" --indexname "design_ke"
   ```

2. **background_ke库检索**: 
   ```bash
   python {当前skill路径}/script/data_search_h3c_example.py --description "DPI安全测试" --indexname "background_ke"
   ```

3. **v9_press_example库检索**: 
   ```bash
   python {当前skill路径}/script/data_search_h3c_example.py --description "交换机多网段配置" --indexname "v9_press_example"
   ```

4. **example_ke库检索**: 
   ```bash
   python {当前skill路径}/script/data_search_h3c_example.py --description "DHCP中继" --indexname "example_ke"
   ```

5. **cmd_ke库检索**: 
   ```bash
   python {当前skill路径}/script/data_search_h3c_example.py --description "ip address " --indexname "cmd_ke"
   ```

6. **press_config_des库检索**: 
   ```bash
   python {当前skill路径}/script/data_search_h3c_example.py --description "时间段配置" --indexname "press_config_des"
   ```

## 工作流程

### 步骤 1：初始化检查
目标：确保工作区内存在一个可用的 `conftest.py` 基准文件。

1. **检查文件**：使用 `ls` 检查当前工作区是否存在 `conftest.py`。
2. **执行拷贝 (如果缺失)**：
   - **若文件不存在**：
     - 读取模版文件：`{当前skill路径}/templates/conftest.py`。
     - 使用 `cp` 命令将该文件拷贝到当前工作区中。
   - **若文件已存在**：
     - 直接跳到步骤 2。

### 步骤 2：深度校验与循环知识检索
目标：通过**多轮循环检索且每轮都遍历所有数据库**，动态调整检索词的循环，从宏观到微观完全理解业务背景。

1. **读取现状**
   - 读取当前工作区下 `conftest.py` 的完整内容。
   - 读取拓扑文件（通常是 .topox），获取物理设备列表，了解各个设备间链接方式。

2. **动态检索循环 (The Dynamic Loop)**：
   - **初始启动 (Seed)**：
     - 提取用户输入中的核心名词。

   - **执行循环 (Start Loop)**：
     1. **全库扫描 (Action)**：
        - 使用当前的“关键词”，**执行检索命令**，遍历所有数据库。
     
     2. **结果分析 (Observation)**：
        - 仔细阅读返回内容，寻找新术语。

     3. **决策判定 (Decision)**：
        - 判断是否掌握完成用户需求所需的每一个具体的命令行、参数取值和配置顺序。
        - **YES** -> 退出循环，进入步骤 3。
        - **NO** -> **更新关键词**。

     4. **重返第一步**：使用新关键词再次执行全库扫描。

3. **需求对比**：
   - 分析用户的具体测试需求，检查当前代码内容是否已包含用户所需的逻辑。

### 步骤 3：决策与执行
根据步骤 2 的对比结果执行：

#### 情况 A：内容不符合 (Mismatch)
1.  **制定计划 (Todo List)**：
    - 向用户简述修改计划。
2.  **重构代码与查漏补缺**：
    - 在编写具体代码行时，如果发现步骤 2 的检索仍有遗漏，**必须再次触发全库扫描**。
3.  **覆盖写入**：使用 `Edit` 将更新后的代码写入 `conftest.py`。
4.  **反馈**：回复“已通过多轮全库检索参考 H3C 知识库，深入理解业务背景后更新了 `conftest.py`。”

#### 情况 B：内容符合 (Match)
1.  **动作**：不做任何修改。
2.  **反馈**：回复“现有 `conftest.py` 已符合需求，无需修改。”

### 步骤4：校验
校验最终的`conftest.py`文件，避免出现错误。

1. **全覆盖验证**：确认在每一轮检索中，是否都没有遗漏任何一个数据库。
2. **关键词进化**：确认下一轮的检索词是否基于上一轮的学习成果进行了优化。
3. **深刻理解**：在开始写代码前，确保完全理解该特性。
4. `conftest.py`文件中不需要使用 `CheckCommand()` 或 `assert()` 等函数来验证配置结果。
5. 确保使用的设备名和端口名在拓扑中存在，注意大小写问题。
6. 不要使用 `atf_check` 和 `atf_assert`，对于 H3C 设备相关的检查只可以使用 `CheckCommand`。