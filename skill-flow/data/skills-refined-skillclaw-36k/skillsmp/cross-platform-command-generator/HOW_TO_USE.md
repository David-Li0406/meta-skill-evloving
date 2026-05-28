# 如何使用跨平台命令生成器技能

嘿 Claude — 我刚刚添加了 "cross-platform-command-generator" 技能。你能帮我生成在 Linux、macOS 和 Windows 上查找大文件的命令吗?

## 使用示例

### 示例 1: 基础命令生成

```
@cross-platform-command-generator

任务: 列出当前目录下所有文件的详细信息
目标平台: Linux, macOS, Windows
```

**期望输出**: 针对每个平台生成对应的 `ls` / `dir` / `Get-ChildItem` 命令

---

### 示例 2: 查找大文件

```
@cross-platform-command-generator

任务: 查找 /home/user 目录下所有大于 500MB 的文件
目标平台: 所有平台
安全级别: 标准
```

**期望输出**: 跨平台 `find` / `Get-ChildItem` 命令,附带大小过滤

---

### 示例 3: 系统监控命令

```
@cross-platform-command-generator

生成命令: 检查系统中所有监听端口和对应的进程
目标平台: Linux, Windows
需要权限: 管理员
```

**期望输出**: `netstat` / `Get-NetTCPConnection` 命令,标注需要 sudo/admin 权限

---

### 示例 4: 自动化脚本生成

```
@cross-platform-command-generator

生成自动化部署脚本:
- 脚本名称: deploy_app
- 功能:
  1. 停止应用服务
  2. 备份当前版本
  3. 部署新版本
  4. 启动服务
  5. 验证部署结果
- 目标平台: Linux, Windows
- 包含: 参数解析、错误处理、回滚机制、日志记录
- 安全要求: 需要权限检查和操作确认
```

**期望输出**: 完整的 `.sh` 和 `.ps1` 脚本文件,附带 README

---

### 示例 5: 安全审计脚本

```
@cross-platform-command-generator

生成安全检查脚本:
- 检查文件权限 (777, 666)
- 检查监听端口
- 检查运行的可疑进程
- 检查防火墙状态
- 生成安全报告
- 平台: Linux, macOS, Windows
```

**期望输出**: 安全审计脚本,包含危险操作警告

---

### 示例 6: 数据备份脚本

```
@cross-platform-command-generator

生成增量备份脚本:
- 源目录: /data 或 C:\Data
- 备份目标: 网络存储
- 压缩格式: tar.gz (Linux/macOS), zip (Windows)
- 保留最近 7 天的备份
- 发送备份完成通知
- 平台: 所有平台
```

**期望输出**: 跨平台备份脚本,附带调度配置说明

---

### 示例 7: 命令翻译

```
@cross-platform-command-generator

将这个 Linux 命令转换为 Windows 等效命令:
grep -r "ERROR" /var/log/*.log | wc -l

目标平台: Windows (PowerShell 和 CMD)
```

**期望输出**: PowerShell 和 CMD 的等效命令,附带兼容性说明

---

### 示例 8: 批量文件处理

```
@cross-platform-command-generator

生成命令: 批量重命名文件,将所有 .txt 文件改为 .bak
目录: 当前目录及子目录
目标平台: Linux, macOS, Windows
安全: 需要操作前确认
```

**期望输出**: 安全的批量重命名命令,包含危险操作警告

---

## 你需要提供的信息

### 命令生成模式
- **任务描述**: 用自然语言描述你想执行的操作
- **目标平台** (可选): 选择 Linux, macOS, Windows 或全部
- **安全级别** (可选): 是否允许需要提升权限的命令
- **特殊参数** (可选): 文件路径、大小阈值、搜索模式等

### 脚本生成模式
- **脚本用途**: 脚本的主要功能
- **目标平台**: 需要生成哪些平台的脚本
- **功能模块**: 需要包含的功能列表
- **安全要求**: 输入验证、权限检查、确认机制等
- **参数定义** (可选): 脚本接受的命令行参数

---

## 你将获得的输出

### 命令生成模式输出

**JSON 格式结构化命令**:
```json
{
  "task_description": "原始任务描述",
  "platforms": {
    "linux": {
      "command": "生成的命令",
      "requires_sudo": false,
      "safety_level": "safe"
    },
    "windows": {
      "powershell": "PowerShell 命令",
      "cmd": "CMD 命令",
      "requires_admin": false,
      "safety_level": "safe"
    }
  },
  "compatibility_notes": ["兼容性说明"],
  "security_warnings": ["安全警告"]
}
```

### 脚本生成模式输出

**完整脚本文件包**:
- `script_name.sh` - Linux/macOS Shell 脚本
- `script_name.ps1` - Windows PowerShell 脚本
- `script_name.bat` - Windows 批处理脚本
- `README.md` - 使用说明和示例
- 包含: 参数解析、错误处理、日志记录、帮助信息

---

## 最佳实践

### 1. 明确任务描述
使用具体的动词和参数描述任务,例如:
- ✅ "查找 /var/log 下所有大于 100MB 的 .log 文件"
- ❌ "找大文件"

### 2. 指定安全级别
如果命令需要管理员权限,明确说明:
- "需要 sudo/管理员权限"
- "允许破坏性操作"

### 3. 验证生成的命令
在生产环境执行前:
- 在测试环境中验证命令
- 阅读安全警告
- 理解命令的具体作用

### 4. 使用脚本模式处理复杂任务
单条命令无法满足时,使用脚本生成模式:
- 多步骤操作流程
- 需要错误处理和回滚
- 需要日志记录和报告

### 5. 关注兼容性说明
不同平台的命令可能:
- 输出格式不同
- 参数语法不同
- 功能支持程度不同

---

## 限制和注意事项

### 技术限制
- 复杂的 Shell 脚本逻辑可能需要手动调整
- 某些高级功能无法在所有平台上完全等效
- 第三方工具的可用性因平台而异

### 安全限制
- 生成的命令基于静态模式分析,无法保证 100% 安全
- 破坏性操作会被标记,但仍需人工确认
- 生产环境使用前应由专业人员审核

### 最佳使用场景
- DevOps 自动化脚本生成
- 跨平台工具开发
- 系统管理任务自动化
- 快速原型开发

### 不适用场景
- 高度定制化的企业级部署
- 需要精细权限控制的安全关键场景
- 实时性能敏感的操作

---

## 故障排除

### 问题: 生成的命令不工作

**解决方法**:
1. 检查目标平台和系统版本
2. 确认所需工具已安装
3. 检查文件路径和权限
4. 查看兼容性说明

### 问题: 缺少某些平台的命令

**解决方法**:
1. 明确指定目标平台
2. 检查命令是否有平台限制
3. 查看替代方案建议

### 问题: 安全警告太多

**解决方法**:
1. 审查命令的实际需求
2. 使用更安全的替代方法
3. 在隔离环境中测试
4. 寻求专业安全审核

---

## 扩展用法

### 与其他技能组合使用

**与代码审查技能组合**:
```
@cross-platform-command-generator 生成部署脚本
@code-reviewer 审查生成的脚本安全性
```

**与文档生成技能组合**:
```
@cross-platform-command-generator 生成运维脚本
@api-document-generator 为脚本生成使用文档
```

### 集成到 CI/CD 流程

生成的脚本可以直接集成到:
- GitHub Actions
- GitLab CI
- Jenkins
- Azure DevOps

示例工作流:
```yaml
- name: Run health check
  run: |
    chmod +x health_check.sh
    ./health_check.sh
```

---

## 获取帮助

如果遇到问题:
1. 检查本文档的故障排除部分
2. 查看示例用法获取灵感
3. 明确描述你的具体需求
4. 提供目标平台和环境信息

---

**技能版本**: 1.0.0
**最后更新**: 2025-10-30
**维护者**: Claude Code Skills Factory
