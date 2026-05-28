# Update Helm Index - 故障排除指南

本文档提供常见问题的诊断步骤、解决方案和验证方法。

## 问题诊断清单

遇到问题时,按以下顺序检查:

- [ ] Helm 版本是否正确?
- [ ] Chart.yaml 格式是否有效?
- [ ] .tgz 包是否损坏?
- [ ] 目录权限是否正确?
- [ ] Git 仓库状态是否正常?
- [ ] 仓库 URL 是否正确?

---

## 常见问题

### 问题 1: 索引生成失败

**症状:**
```bash
$ helm repo index . --url https://helm-chart.anubis.cafe
Error: failed to save index file: open index.yaml: permission denied
```

**可能原因:**
1. 目录权限不足
2. 磁盘空间不足
3. .tgz 文件损坏

**诊断步骤:**

```bash
# 1. 检查目录权限
ls -la .

# 2. 检查磁盘空间
df -h

# 3. 验证 .tgz 文件完整性
for file in *.tgz; do
  echo "Checking $file..."
  helm lint "$file"
done
```

**解决方案:**

1. **修复权限问题:**
   ```bash
   # 确保有写权限
   chmod u+w .

   # 或者使用 sudo (不推荐)
   sudo helm repo index . --url https://helm-chart.anubis.cafe
   ```

2. **清理磁盘空间:**
   ```bash
   # 清理旧的 .tgz 包
   rm *.old.tgz

   # 清理 Git 旧对象
   git gc --aggressive --prune=now
   ```

3. **重新打包损坏的 Chart:**
   ```bash
   # 找到损坏的包
   helm lint broken-chart.tgz

   # 重新打包
   helm package charts/broken-chart
   ```

---

### 问题 2: Git 状态异常

**症状:**
```bash
$ git status
error: bad index file sha1 signature
fatal: index file corrupt
```

**可能原因:**
1. Git 索引文件损坏
2. 文件未正确添加
3. Git 配置问题

**诊断步骤:**

```bash
# 1. 检查 Git 状态
git status

# 2. 查看未跟踪文件
git ls-files --others --exclude-standard

# 3. 检查 Git 配置
git config --list | grep -E "(user|core)"
```

**解决方案:**

1. **重置 Git 索引:**
   ```bash
   # 备份当前状态
   cp .git/index .git/index.backup

   # 重置索引
   rm .git/index
   git reset

   # 如果仍然失败,恢复备份并检查
   cp .git/index.backup .git/index
   ```

2. **重新添加文件:**
   ```bash
   # 清理暂存区
   git reset HEAD .

   # 重新添加文件
   git add *.tgz index.yaml
   ```

3. **修复 Git 配置:**
   ```bash
   # 设置用户信息
   git config user.name "Your Name"
   git config user.email "your.email@example.com"

   # 设置正确的行结束符
   git config core.autocrlf input
   ```

---

### 问题 3: URL 不匹配

**症状:**
```bash
# index.yaml 中的 URL 错误
urls:
  - http://localhost:8080/subconverter-0.2.0.tgz  # 错误的 URL
```

**可能原因:**
1. 环境配置错误
2. 使用了错误的 --url 参数
3. 仓库部署地址变更

**诊断步骤:**

```bash
# 1. 检查当前 URL
grep "urls:" index.yaml | head -5

# 2. 确认正确的仓库地址
echo $HELM_REPO_URL

# 3. 检查环境变量
env | grep -i helm
```

**解决方案:**

1. **删除旧索引并重新生成:**
   ```bash
   # 删除旧索引
   rm index.yaml

   # 使用正确的 URL 重新生成
   helm repo index . --url https://helm-chart.anubis.cafe

   # 验证
   grep "urls:" index.yaml
   ```

2. **使用环境变量:**
   ```bash
   # 设置环境变量
   export HELM_REPO_URL=https://helm-chart.anubis.cafe

   # 使用环境变量
   helm repo index . --url $HELM_REPO_URL
   ```

3. **批量更新多个仓库的 URL:**
   ```bash
   # 如果有多个 index.yaml 文件
   find . -name "index.yaml" -exec sh -c '
     dir=$(dirname "{}")
     rm "{}"
     helm repo index "$dir" --url https://helm-chart.anubis.cafe
   ' \;
   ```

---

### 问题 4: Chart 验证失败

**症状:**
```bash
$ helm lint subconverter-0.2.0.tgz
Error: unable to open 'subconverter/Chart.yaml': no such file or directory
```

**可能原因:**
1. Chart.yaml 格式错误
2. 依赖缺失
3. 模板语法错误

**诊断步骤:**

```bash
# 1. 检查 Chart 内容
tar -tzf subconverter-0.2.0.tgz | grep Chart.yaml

# 2. 提取并检查 Chart.yaml
tar -xzf subconverter-0.2.0.tgz subconverter/Chart.yaml
cat subconverter/Chart.yaml

# 3. 验证 YAML 语法
python3 -c "import yaml; yaml.safe_load(open('subconverter/Chart.yaml'))"
```

**解决方案:**

1. **修复 Chart.yaml:**
   ```yaml
   # 确保 Chart.yaml 包含必需字段
   apiVersion: v2
   name: subconverter
   description: A subscription converter
   version: 0.2.0
   type: application
   ```

2. **安装依赖:**
   ```bash
   # 解压 Chart
   tar -xzf subconverter-0.2.0.tgz

   # 下载依赖
   helm dep up subconverter

   # 重新打包
   helm package subconverter
   ```

3. **修复模板语法:**
   ```bash
   # 使用 --strict 模式验证
   helm lint subconverter --strict

   # 检查模板语法
   helm template subconverter --debug
   ```

---

### 问题 5: Artifact Hub 不同步

**症状:**
- Chart 已发布但 Artifact Hub 未显示
- 版本信息过期
- 图标或描述缺失

**可能原因:**
1. Artifact Hub 未获取更新
2. artifacthub-repo.yml 配置错误
3. Chart 注释缺失

**诊断步骤:**

```bash
# 1. 检查 artifacthub-repo.yml
cat artifacthub-repo.yml

# 2. 检查 Chart.yaml 中的注释
grep -A 10 "annotations:" charts/*/Chart.yaml

# 3. 验证 index.yaml 可访问性
curl -I https://helm-chart.anubis.cafe/index.yaml
```

**解决方案:**

1. **配置 Artifact Hub:**
   ```yaml
   # artifacthub-repo.yml
   repositoryID: <your-repo-id>
   owners:
     - name: Your Name
       email: your.email@example.com
   ```

2. **添加 Chart 注释:**
   ```yaml
   # charts/subconverter/Chart.yaml
   annotations:
     artifacthub.io/changes: |
       - Add feature X
       - Fix bug Y
     artifacthub.io/containsSecurityUpdates: "false"
     artifacthub.io/prerelease: "false"
   ```

3. **触发 Artifact Hub 重新索引:**
   - 访问 https://artifacthub.io
   - 找到你的仓库
   - 点击 "Check for updates" 按钮
   - 等待几分钟 (通常 5-10 分钟)

---

### 问题 6: Digest 不匹配

**症状:**
```bash
$ helm install myrepo/subconverter --version 0.2.0
Error: failed to download subconverter: checksum does not match
```

**可能原因:**
1. .tgz 文件已修改但索引未更新
2. 网络传输错误
3. 缓存问题

**诊断步骤:**

```bash
# 1. 计算实际 digest
sha256sum subconverter-0.2.0.tgz

# 2. 检查索引中的 digest
grep -A 5 "version: 0.2.0" index.yaml | grep digest

# 3. 清理 Helm 缓存
helm cache list
helm cache clean
```

**解决方案:**

1. **重新生成索引:**
   ```bash
   # 删除旧索引
   rm index.yaml

   # 重新生成 (会重新计算 digest)
   helm repo index . --url https://helm-chart.anubis.cafe
   ```

2. **清理客户端缓存:**
   ```bash
   # 清理 Helm 缓存
   helm cache clean

   # 更新仓库
   helm repo update myrepo

   # 重新安装
   helm install myrepo/subconverter --version 0.2.0
   ```

---

## 验证命令

### 基本验证

```bash
# 1. 列出所有包
ls -lh *.tgz

# 2. 验证包格式
for file in *.tgz; do
  helm lint "$file"
done

# 3. 检查索引 YAML 语法
python3 -c "import yaml; yaml.safe_load(open('index.yaml'))"
```

### 功能验证

```bash
# 1. 添加测试仓库
helm repo add test-anubis https://helm-chart.anubis.cafe

# 2. 更新仓库缓存
helm repo update

# 3. 搜索特定 chart
helm search repo test-anubis/subconverter --versions

# 4. 查看详细信息
helm show chart test-anubis/subconverter --version 0.2.0

# 5. 测试安装 (dry-run)
helm install test-release test-anubis/subconverter --version 0.2.0 --dry-run

# 6. 清理测试仓库
helm repo remove test-anubis
```

### 完整性验证

```bash
# 1. 验证所有包都在索引中
for tgz in *.tgz; do
  name=$(basename "$tgz" .tgz)
  if grep -q "$name" index.yaml; then
    echo "✓ $name in index"
  else
    echo "✗ $name NOT in index"
  fi
done

# 2. 验证 digest 匹配
for tgz in *.tgz; do
  actual_digest=$(sha256sum "$tgz" | awk '{print $1}')
  name=$(basename "$tgz")
  index_digest=$(grep -B 2 "$name" index.yaml | grep digest | awk '{print $2}')

  if [ "$actual_digest" = "$index_digest" ]; then
    echo "✓ $name digest matches"
  else
    echo "✗ $name digest mismatch"
  fi
done
```

---

## 日志和调试

### 启用详细输出

```bash
# Helm 命令使用 --debug 标志
helm repo index . --url https://helm-chart.anubis.cafe --debug

# Helm lint 详细输出
helm lint chart.tgz --debug

# Helm 安装详细输出
helm install release repo/chart --version 1.0.0 --debug
```

### 查看历史记录

```bash
# 查看 Git 提交历史
git log --oneline --grep="index"

# 查看 index.yaml 的变更历史
git log -p index.yaml

# 查看特定文件的完整历史
git log --follow --patch -- index.yaml
```

---

## 预防性维护

### 使用健康检查脚本

本 skill 提供了自动化健康检查脚本:

```bash
bash .claude/skills/update-helm-index/scripts/health-check.sh
```

该脚本会自动执行以下检查:
- .tgz 文件格式验证
- index.yaml YAML 语法检查
- digest 完整性验证
- 仓库 URL 可访问性测试
- Git 状态检查

详细说明请查看 [scripts/README.md](scripts/README.md)

---

### 手动检查脚本

或者使用下面的手动检查脚本:

```bash
#!/bin/bash
# check-helm-repo.sh - Helm 仓库健康检查脚本

echo "Checking Helm repository health..."

# 1. 检查 .tgz 文件
echo "1. Checking .tgz files..."
for file in *.tgz; do
  if helm lint "$file" > /dev/null 2>&1; then
    echo "  ✓ $file is valid"
  else
    echo "  ✗ $file is INVALID"
  fi
done

# 2. 检查索引完整性
echo "2. Checking index.yaml..."
if python3 -c "import yaml; yaml.safe_load(open('index.yaml'))" 2>/dev/null; then
  echo "  ✓ index.yaml is valid YAML"
else
  echo "  ✗ index.yaml is INVALID YAML"
fi

# 3. 检查 URL 可访问性
echo "3. Checking repository URL..."
if curl -s -o /dev/null -w "%{http_code}" https://helm-chart.anubis.cafe/index.yaml | grep -q "200"; then
  echo "  ✓ Repository URL is accessible"
else
  echo "  ✗ Repository URL is NOT accessible"
fi

# 4. 检查 digest 匹配
echo "4. Checking digest matches..."
mismatch_count=0
for tgz in *.tgz; do
  actual=$(sha256sum "$tgz" | awk '{print $1}')
  name=$(basename "$tgz")
  index=$(grep -B 2 "$name" index.yaml | grep digest | awk '{print $2}')

  if [ "$actual" != "$index" ]; then
    echo "  ✗ $name digest mismatch"
    ((mismatch_count++))
  fi
done

if [ $mismatch_count -eq 0 ]; then
  echo "  ✓ All digests match"
else
  echo "  ✗ $mismatch_count digests mismatch"
fi

echo "Check complete!"
```

---

## 相关文档

- [Helm 故障排除](https://helm.sh/docs/faq/)
- [Helm Chart 最佳实践](https://helm.sh/docs/topics/chart_best_practices/)
- [Artifact Hub 故障排除](https://artifacthub.io/docs/topics/repositories/#troubleshooting)

---

## 获取帮助

如果以上解决方案都无法解决你的问题:

1. 检查 [Helm GitHub Issues](https://github.com/helm/helm/issues)
2. 搜索 [Helm 文档](https://helm.sh/docs/)
3. 在项目仓库创建 Issue
4. 联系项目维护者
