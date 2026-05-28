# Update Helm Index - 辅助脚本

本目录包含用于自动化 Helm Chart 仓库索引更新的辅助脚本。

## 📋 脚本列表

### check-env.sh
**环境检查脚本** - 验证所有前置条件

检查项目:
- ✅ 必需命令 (helm, git, grep, sha256sum)
- ✅ Helm 版本 (>= 3.0.0)
- ✅ Git 配置 (user.name, user.email)
- ✅ 目录写权限
- ✅ .tgz 文件状态
- ✅ index.yaml 语法

用法:
```bash
bash check-env.sh
```

---

### update-index.sh
**一键更新脚本** - 自动执行完整的索引更新流程

功能:
- 🔍 环境检查
- 📦 打包 Charts
- 🔄 更新 index.yaml
- ✅ 验证更新结果
- 📝 Git 提交

用法:
```bash
# 预览模式(推荐首次使用)
bash update-index.sh --dry-run

# 执行更新
bash update-index.sh

# 自动推送到远程
bash update-index.sh --auto-push

# 使用自定义 URL
bash update-index.sh --url https://example.com/charts

# 查看帮助
bash update-index.sh --help
```

选项:
- `--dry-run` - 只显示将要执行的操作,不实际执行
- `--skip-checks` - 跳过环境检查(不推荐)
- `--auto-push` - 自动推送到远程仓库(默认需要确认)
- `--url <URL>` - 指定仓库 URL
- `--help` - 显示帮助信息

---

### health-check.sh
**健康检查脚本** - 定期验证仓库完整性

检查项目:
- 📦 .tgz 文件格式验证
- 📄 index.yaml YAML 语法检查
- 🔗 仓库 URL 可访问性测试
- 🔐 digest 完整性验证
- 📊 Git 状态检查

用法:
```bash
bash health-check.sh
```

建议:
- 定期运行 (每周或每次发布前)
- 集成到 CI/CD 流程
- 在发现问题时查看详细报告

---

## 🚀 快速开始

### 首次使用

1. **检查环境**
   ```bash
   bash .claude/skills/update-helm-index/scripts/check-env.sh
   ```

2. **预览更新流程**
   ```bash
   bash .claude/skills/update-helm-index/scripts/update-index.sh --dry-run
   ```

3. **执行更新**
   ```bash
   bash .claude/skills/update-helm-index/scripts/update-index.sh
   ```

4. **验证仓库健康**
   ```bash
   bash .claude/skills/update-helm-index/scripts/health-check.sh
   ```

### 常见工作流

#### 发布新版本 Chart
```bash
# 1. 更新 Chart.yaml 版本号
vim charts/my-chart/Chart.yaml

# 2. 运行一键更新
bash .claude/skills/update-helm-index/scripts/update-index.sh

# 3. 推送到远程
git push
```

#### 定期维护检查
```bash
# 运行健康检查
bash .claude/skills/update-helm-index/scripts/health-check.sh

# 如发现问题,运行更新修复
bash .claude/skills/update-helm-index/scripts/update-index.sh
```

---

## 📚 相关文档

详细使用说明请参考:

- [SKILL.md](../SKILL.md) - 技能概览和快速开始
- [workflows.md](../workflows.md) - 详细的工作流程说明
- [troubleshooting.md](../troubleshooting.md) - 故障排除指南

---

## ⚙️ 环境变量

### HELM_REPO_URL
设置默认的 Helm 仓库 URL

```bash
export HELM_REPO_URL=https://helm-chart.anubis.cafe
bash update-index.sh
```

---

## 🔧 故障排除

### 脚本无法执行
```bash
# 确保脚本有执行权限
chmod +x *.sh
```

### 环境检查失败
查看 check-env.sh 的输出,根据提示修复问题:
- Helm 版本不足 → 升级 Helm
- Git 未配置 → 配置 user.name 和 user.email
- 缺少必需命令 → 安装相应工具

### 索引更新失败
1. 运行 `bash check-env.sh` 检查环境
2. 查看 [troubleshooting.md](../troubleshooting.md)
3. 使用 `--dry-run` 模式调试

---

## 💡 最佳实践

1. **首次使用前**
   - 运行 `check-env.sh` 验证环境
   - 使用 `--dry-run` 预览操作

2. **定期维护**
   - 每周运行 `health-check.sh`
   - 发布前验证仓库完整性

3. **安全操作**
   - 重要操作前备份
   - 使用 `--dry-run` 测试
   - 避免跳过环境检查

4. **版本控制**
   - 每次更新创建清晰的提交信息
   - 使用 `--auto-push` 前确认变更

---

## 📝 许可证

这些脚本与主项目使用相同的许可证。
