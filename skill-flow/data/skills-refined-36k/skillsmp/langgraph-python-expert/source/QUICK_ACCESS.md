# LangGraph Source Quick Access

快速访问 LangGraph 官方源代码的关键部分。

## 🚀 快速开始

```bash
# 更新到最新版本
cd langgraph
git pull origin main

# 查看 sparse-checkout 配置
git sparse-checkout list
```

## 📂 核心文件位置

### 主要 API 类和函数

**图构建相关：**
```
langgraph/libs/langgraph/langgraph/graph/
├── state.py      - StateGraph 主要实现
├── message.py    - MessageGraph 实现
└── graph.py      - 基础图类

langgraph/libs/langgraph/langgraph/constants.py
├── START         - 起始节点常量
└── END           - 结束节点常量
```

**检查点存储：**
```
langgraph/libs/checkpoint/langgraph/checkpoint/
├── base.py       - BaseCheckpointSaver 基类
└── memory.py     - MemorySaver 内存存储

langgraph/libs/checkpoint-sqlite/langgraph/checkpoint/sqlite/
└── __init__.py   - SqliteSaver

langgraph/libs/checkpoint-postgres/langgraph/checkpoint/postgres/
└── __init__.py   - PostgresSaver
```

**预构建组件：**
```
langgraph/libs/prebuilt/langgraph/prebuilt/
├── react.py      - create_react_agent
├── tool_node.py  - ToolNode 工具执行节点
└── chat.py       - 聊天相关组件
```

### 示例代码

**基础示例：**
```
langgraph/examples/
├── create-react-agent.ipynb      - React Agent 创建
├── persistence.ipynb             - 持久化示例
├── human_in_the_loop/            - 人机交互
└── multi_agent/                  - 多代理协作
```

### 文档

```
langgraph/docs/docs/
├── index.md                      - 文档首页
├── llms.txt                      - LLM 友好索引
├── concepts/                     - 概念文档
│   ├── high_level.md
│   └── low_level.md
├── how-tos/                      - 操作指南
└── reference/                    - API 参考
```

## 🔍 代码导航技巧

### 1. 查找特定功能
```bash
# 查找 StateGraph 的实现
grep -r "class StateGraph" langgraph/libs/

# 查找检查点相关的实现
grep -r "class.*Saver" langgraph/libs/
```

### 2. 查看最新变更
```bash
cd langgraph
git log --oneline -10
```

### 3. 查找使用示例
```bash
# 在示例中查找特定 API 的使用
grep -r "StateGraph" langgraph/examples/ --include="*.py" --include="*.ipynb"
```

## 📚 重要文件说明

### 核心实现文件
1. **`libs/langgraph/langgraph/graph/state.py`** - StateGraph 主要实现
2. **`libs/langgraph/langgraph/pregel/`** - Pregel 算法实现
3. **`libs/checkpoint/langgraph/checkpoint/base.py`** - 检查点基类

### 配置文件
1. **`README.md`** - 官方说明文档
2. **`CLAUDE.md`** - Claude Code 使用指南
3. **`AGENTS.md`** - Agent 开发指南

## 📖 学习路径建议

1. **初学者：**
   - 从 `examples/create-react-agent.ipynb` 开始
   - 阅读 `docs/docs/concepts/high_level.md`

2. **中级：**
   - 研究 `examples/multi_agent/` 中的示例
   - 查看 `libs/prebuilt/` 预构建组件

3. **高级：**
   - 阅读 `libs/langgraph/langgraph/pregel/` 实现
   - 研究检查点系统 `libs/checkpoint*/`

## 📞 获取帮助

- **官方文档：** `docs/docs/` 目录
- **示例代码：** `examples/` 目录
- **LLM 索引：** `docs/docs/llms.txt`
- **GitHub Issues：** [LangGraph Issues](https://github.com/langchain-ai/langgraph/issues)

