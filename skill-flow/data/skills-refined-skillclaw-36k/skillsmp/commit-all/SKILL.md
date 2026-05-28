---
name: commit-all
description: 提交所有工作区改动到当前 git 分支并生成规范的提交消息。当用户输入 "commit" 时使用
allowed-tools: Read, Bash
---

## 提交步骤

### 1. 检查变更状态

并行运行以下命令获取变更信息：

```bash
git status
git diff --staged
git diff
```

### 2. 分析变更类型

根据文件变更，确定提交类型和作用域：

**提交类型 (type):**
- `feat`: 新功能（如新增 export_service.py）
- `fix`: 错误修复
- `refactor`: 代码重构（不改变功能）
- `docs`: 文档更新（如修改 CLAUDE.md）
- `test`: 测试相关（如添加 test_*.py）
- `perf`: 性能优化
- `chore`: 构建、依赖更新、配置

**作用域 (scope):**
- `agent`: Agent 工厂或工具
- `service`: 业务服务层
- `router`: FastAPI 路由
- `db`: 数据库相关
- `export`: 文档导出
- `test`: 测试
- `docker`: Docker 配置

### 3. 生成提交消息
遵循 Conventional Commits 格式，使用中文描述：

```
<type>(<scope>): <简短描述>

<详细说明>

<footer>
```

**规则：**
1. 第一行（subject）不超过 50 字符
2. 使用中文描述具体改动
3. 详细说明解释 WHAT 和 WHY，而不是 HOW
4. 使用现在时："添加" 而非 "已添加"
5. 一个提交只做一件事（单一职责）

**示例：**
```
feat(export): 添加文档导出服务

- 实现 ExportService 类支持多格式导出
- 添加 export_to_docx() 方法转换 Markdown 到 Word
- 集成 Mermaid 图表转图片功能
- 添加相应的单元测试

Closes #123
```

### 4. 暂存所有文件并提交

使用 HEREDOC 格式执行提交（确保格式正确）：
```bash
git add .
git commit -m "$(cat <<'EOF'
<type>(<scope>): <简短描述>

<详细说明>

🤖 Generated with Claude Code

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
EOF
)"
```

### 5. 确认提交成功

运行 `git status` 和 `git log -1` 确认提交已创建，并告知用户执行结果。

## 参考资料

- [Conventional Commits 规范](https://www.conventionalcommits.org/)
- Bid Agent 开发文档：CLAUDE.md
