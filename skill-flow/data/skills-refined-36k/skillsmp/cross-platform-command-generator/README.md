# Cross-Platform Command Generator

## 概述

跨平台命令生成器是一个强大的 Claude 技能,用于生成适用于 Linux、macOS 和 Windows 的命令行和自动化脚本。该技能特别适合 DevOps 工程师、系统管理员和需要跨平台自动化的开发人员。

**版本**: 1.0.0
**作者**: Claude Code Skills Factory
**创建日期**: 2025-10-30

---

## 核心功能

### 1. 自然语言命令生成
- 将自然语言描述转换为特定平台命令
- 支持 Linux/Unix (Bash)、macOS (Bash/Zsh)、Windows (PowerShell/CMD)
- 自动识别常见任务模式 (文件操作、系统监控、网络诊断等)

### 2. 跨平台脚本生成
- 生成完整的自动化脚本文件 (.sh, .ps1, .bat)
- 包含错误处理、日志记录、参数解析
- 遵循平台最佳实践和编码规范

### 3. 安全性检查
- 危险命令检测 (rm -rf, format, del /f 等)
- 权限提升操作识别 (sudo, runas)
- 风险等级评估 (safe/warning/dangerous/critical)
- 命令注入防护

### 4. 兼容性分析
- 跨平台命令等效性检查
- 平台特性差异说明
- 替代方案推荐
- 兼容性报告生成

---

## 技术架构

### Python 模块

#### 1. `command_generator.py`
**核心命令生成引擎**

**主要类**:
- `PlatformCommandGenerator`: 命令生成主类

**主要方法**:
- `analyze_task()`: 分析任务描述,识别命令模式
- `extract_parameters()`: 从自然语言中提取参数
- `generate_commands()`: 生成平台特定命令
- `_assess_safety()`: 评估命令安全等级

**命令模式数据库**:
- 14+ 常见任务模式 (文件操作、系统信息、进程管理、网络诊断等)
- Linux/macOS/Windows 命令映射
- 参数模板和格式化

**示例**:
```python
from command_generator import cross_platform_translate

result = cross_platform_translate(
    "Find all files larger than 100MB",
    platforms=["linux", "windows"]
)
```

---

#### 2. `security_validator.py`
**安全验证模块**

**主要类**:
- `SecurityValidator`: 安全检查主类

**主要方法**:
- `check_dangerous_commands()`: 检测危险命令模式
- `assess_risk_level()`: 评估整体风险等级
- `privilege_required()`: 检查权限需求
- `validate_input_safety()`: 输入安全验证
- `generate_security_report()`: 生成安全报告

**危险模式类别**:
- `destructive_operations`: 破坏性操作 (数据丢失风险)
- `privilege_escalation`: 权限提升
- `system_modification`: 系统配置修改
- `network_security`: 网络安全设置
- `data_exfiltration`: 数据传输/导出
- `process_injection`: 进程注入/调试

**示例**:
```python
from security_validator import validate_command_security

result = validate_command_security("rm -rf /tmp/*", platform="linux")
# Returns: risk_level, warnings, requires_privilege, is_safe
```

---

#### 3. `script_builder.py`
**脚本文件生成器**

**主要类**:
- `ScriptBuilder`: 脚本构建主类

**主要方法**:
- `generate_bash_script()`: 生成 Bash 脚本
- `generate_powershell_script()`: 生成 PowerShell 脚本
- `generate_batch_script()`: 生成批处理脚本
- `create_readme()`: 生成脚本使用文档

**脚本结构特性**:
- **Bash 脚本**: Shebang, strict mode, 错误处理函数, 参数解析, 日志记录
- **PowerShell 脚本**: Synopsis/Description, strict mode, cmdlet 风格, 参数块
- **批处理脚本**: Echo off, 延迟展开, 错误处理, 日志功能

**示例**:
```python
from script_builder import ScriptBuilder

builder = ScriptBuilder(
    script_name="system_check",
    description="System health monitoring"
)

bash_script = builder.generate_bash_script(
    functions=[...],
    main_logic="check_disk_space\ncheck_memory"
)
```

---

#### 4. `compatibility_checker.py`
**兼容性检查器**

**主要类**:
- `CompatibilityChecker`: 兼容性分析主类

**主要方法**:
- `find_equivalent_commands()`: 查找等效命令
- `check_platform_compatibility()`: 检查平台特性支持
- `suggest_alternatives()`: 推荐替代方案
- `analyze_script_compatibility()`: 脚本兼容性分析

**命令等效数据库**:
- 40+ 常用命令的跨平台映射
- 文件操作: ls, cat, grep, find, cp, mv, rm, mkdir
- 系统信息: uname, whoami, hostname
- 进程管理: ps, kill
- 网络工具: ping, curl, wget, netstat
- 归档工具: tar, unzip
- 文本处理: sed, awk
- 包管理: apt-get, yum, brew

**平台特性数据库**:
- Shell 类型
- 包管理器
- 文件权限模型
- 符号链接支持
- 大小写敏感性
- 路径分隔符

**示例**:
```python
from compatibility_checker import CompatibilityChecker

checker = CompatibilityChecker()
result = checker.find_equivalent_commands(
    "ls -la",
    source_platform="linux",
    target_platforms=["windows"]
)
```

---

## 安装指南

### Claude Code (项目级别)

1. 复制技能文件夹到项目 `.claude/skills/` 目录:
```bash
cp -r cross-platform-command-generator /path/to/project/.claude/skills/
```

2. 重启 Claude Code 或重新加载项目

### Claude Code (用户级别)

1. 复制技能文件夹到用户 `.claude/skills/` 目录:

**Linux/macOS**:
```bash
cp -r cross-platform-command-generator ~/.claude/skills/
```

**Windows (PowerShell)**:
```powershell
Copy-Item -Path cross-platform-command-generator -Destination "$env:USERPROFILE\.claude\skills\" -Recurse
```

2. 重启 Claude Code

### 从 ZIP 安装

1. 解压 `cross-platform-command-generator.zip`
2. 按照上述方法复制到对应目录

---

## 快速开始

### 示例 1: 生成简单命令

**输入**:
```
@cross-platform-command-generator

任务: 列出当前目录下所有文件
目标平台: Linux, Windows
```

**输出**:
```json
{
  "platforms": {
    "linux": {
      "command": "ls -lah",
      "safety_level": "safe"
    },
    "windows": {
      "powershell": "Get-ChildItem -Force",
      "cmd": "dir /a"
    }
  }
}
```

---

### 示例 2: 生成自动化脚本

**输入**:
```
@cross-platform-command-generator

生成系统健康检查脚本:
- 检查磁盘空间
- 检查内存使用
- 检查 CPU 负载
- 平台: Linux, Windows
```

**输出**:
- `system_health_check.sh` (Linux)
- `system_health_check.ps1` (Windows)
- `README.md` (使用说明)

---

## 依赖要求

### Python 环境
- **Python 版本**: 3.7+
- **标准库**: typing, json, re, datetime (无需额外安装)

### 目标平台要求

**Linux**:
- Bash 4.0+ 或 Zsh
- 常用工具: find, grep, tar, etc.

**macOS**:
- Bash 3.2+ 或 Zsh (macOS 10.15+ 默认 Zsh)
- 可选: Homebrew (用于包管理)

**Windows**:
- PowerShell 5.1+ 或 PowerShell Core 7+
- CMD (所有 Windows 版本)
- 可选: Windows 10+ (包含 tar, curl 等 Unix 工具)

---

## 使用场景

### DevOps / 系统运维
- 基础设施即代码 (IaC) 脚本生成
- 跨云平台自动化部署
- 系统监控和健康检查
- 灾难恢复和备份自动化

### 软件开发 / 自动化
- CI/CD 流水线脚本
- 构建和测试自动化
- 环境配置脚本
- 代码质量检查

### 安全运维
- 安全审计脚本
- 漏洞扫描自动化
- 日志分析和威胁检测
- 合规性检查

### 混合云和多云环境
- 跨平台资源管理
- 统一运维工具链
- 平台迁移脚本
- 多环境配置管理

---

## 文件结构

```
cross-platform-command-generator/
├── SKILL.md                        # 技能定义文件 (YAML frontmatter)
├── README.md                       # 本文件
├── HOW_TO_USE.md                   # 详细使用指南
├── command_generator.py            # 核心命令生成引擎
├── security_validator.py           # 安全验证模块
├── script_builder.py               # 脚本文件生成器
├── compatibility_checker.py        # 兼容性检查器
├── sample_input.json               # 命令生成示例输入
├── sample_script_request.json      # 脚本生成示例输入
└── expected_output.json            # 预期输出示例
```

---

## 限制和注意事项

### 技术限制
- 某些高级功能可能无法在所有平台上完全等效实现
- 不同操作系统版本的命令语法可能存在差异
- 生成的命令可能依赖特定工具或软件的安装

### 安全限制
- 安全检查基于已知危险模式,无法识别所有潜在风险
- 某些命令的安全性取决于具体执行环境和参数
- 对第三方工具的安全性不做保证

### 使用建议
- 生产环境部署前应由专业人员审核生成的命令和脚本
- 建议先在测试环境验证生成的命令
- 定期更新技能以支持最新的操作系统和工具

---

## 版本历史

### v1.0.0 (2025-10-30)
- 初始版本发布
- 支持 14+ 常见任务模式
- 4 个核心 Python 模块
- 全面的安全检查和兼容性分析
- 支持 Bash, PowerShell, CMD 脚本生成

---

## 贡献和反馈

如有问题、建议或改进想法,欢迎反馈:
- 技能仓库: claude-code-skill-factory
- 问题跟踪: GitHub Issues

---

## 许可证

本技能由 Claude Code Skills Factory 生成和维护。

---

## 相关资源

- **Claude Skills 文档**: https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview
- **Skills Marketplace**: https://github.com/anthropics/skills
- **PowerShell 文档**: https://docs.microsoft.com/powershell/
- **Bash 参考**: https://www.gnu.org/software/bash/manual/

---

**技能就绪!** 开始使用 `@cross-platform-command-generator` 生成你的第一个跨平台命令吧!
