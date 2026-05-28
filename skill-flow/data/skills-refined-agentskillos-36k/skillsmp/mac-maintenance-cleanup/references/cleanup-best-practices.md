# Mac 系统清理最佳实践

本文档提供 Mac 系统清理的最佳实践、安全注意事项和维护建议。

## 清理频率建议

### 日常清理（每周）

**目标**：保持系统流畅，防止缓存堆积

**操作**：
```bash
# 快速检查系统状态
mo status

# 预览并清理缓存
mo clean --dry-run
mo clean
```

**清理内容**：
- 系统缓存
- 浏览器缓存
- 应用临时文件
- 废纸篓

**预期效果**：释放 5-15GB 空间

### 深度清理（每月）

**目标**：彻底清理系统，释放更多空间

**操作**：
```bash
# 1. 磁盘分析
mo analyze

# 2. 深度清理缓存
mo clean --dry-run --debug
mo clean

# 3. 清理安装文件
mo installer

# 4. 系统优化
mo optimize --dry-run
mo optimize
```

**清理内容**：
- 所有缓存（包括开发者工具）
- 安装文件（.dmg、.pkg）
- 旧应用卸载
- 系统优化

**预期效果**：释放 30-100GB 空间

### 开发者清理（按需）

**目标**：清理开发环境，回收项目构建产物

**操作**：
```bash
# 扫描项目构建产物
mo purge
```

**清理内容**：
- node_modules
- target、build、dist
- venv、.venv
- .gradle、.m2

**预期效果**：释放 10-50GB 空间

---

## 清理前准备

### 1. 数据备份

在执行深度清理前，建议备份重要数据：

```bash
# 使用 Time Machine 备份
# 或手动备份重要文件到外部存储
```

### 2. 关闭应用

关闭所有正在运行的应用，尤其是：

- 浏览器（Chrome、Safari、Firefox）
- 开发工具（Xcode、IDE）
- 创意软件（Photoshop、Premiere）

### 3. 检查活动进程

```bash
# 检查是否有大文件正在使用
lsof | grep -E "(node|java|python)"

# 检查下载进程
ps aux | grep -E "(wget|curl)"
```

### 4. 保存工作

- 保存所有文档
- 提交代码更改
- 导出重要数据

---

## 安全注意事项

### 1. 始终预览

**原则**：永远不要在未预览的情况下执行清理

**正确做法**：
```bash
# 先预览
mo clean --dry-run

# 检查清理内容
# 确认无误后再执行
mo clean
```

### 2. 检查清理内容

在执行清理前，检查：

- 是否包含重要文件
- 是否正在下载或安装
- 是否有应用正在使用

### 3. 保护重要路径

使用 whitelist 保护重要缓存：

```bash
mo clean --whitelist
```

**建议保护的路径**：
- 工作项目缓存
- VPN 配置
- 应用特定数据

### 4. 分步执行

对于大型清理，分步执行：

```bash
# 第一步：清理缓存
mo clean

# 等待完成，检查系统状态

# 第二步：清理安装文件
mo installer

# 第三步：系统优化
mo optimize
```

---

## 清理后验证

### 1. 检查磁盘空间

```bash
# 查看磁盘使用情况
df -h

# 使用 Mole 查看详细状态
mo status
```

### 2. 验证应用功能

测试常用应用是否正常工作：

- 浏览器启动和加载
- 开发工具编译和运行
- 创意软件打开和保存

### 3. 检查系统功能

验证系统功能正常：

- 搜索功能（Spotlight）
- 通知中心
- Launchpad
- 系统偏好设置

### 4. 监控系统性能

观察清理后的性能变化：

- 应用启动速度（可能稍慢，缓存重建中）
- 系统响应速度
- 磁盘读写速度

**注意**：清理后首次启动应用可能较慢，这是正常现象（缓存重建中）

---

## 常见问题和解决方案

### 问题 1：清理后磁盘空间未释放

**可能原因**：
- 废纸篓未清空
- 交换文件未删除
- 本地快照占用空间

**解决方案**：
```bash
# 1. 清空废纸篓
rm -rf ~/.Trash/*

# 2. 检查本地快照
tmutil listlocalsnapshots /
tmutil deletelocalsnapshots com.apple.TimeMachine.

# 3. 重启系统（清理交换文件）
sudo reboot
```

### 问题 2：应用无法启动或崩溃

**可能原因**：
- 误删了应用必需的缓存
- 应用配置损坏

**解决方案**：
```bash
# 1. 重新安装应用
brew reinstall <app-name>

# 2. 恢复应用配置
# 从 Time Machine 恢复
~/Library/Preferences/<app-plist>

# 3. 重置应用
defaults delete com.<developer>.<app>
```

### 问题 3：系统性能下降

**可能原因**：
- Spotlight 正在重建索引
- 系统正在重建缓存

**解决方案**：
```bash
# 等待系统稳定（通常 1-2 小时）

# 检查 Spotlight 索引状态
mdutil -s /

# 如果需要，强制重建索引
sudo mdutil -E /

# 检查系统负载
mo status
```

### 问题 4：浏览器书签或历史丢失

**可能原因**：
- 误删了浏览器数据

**解决方案**：
```bash
# 从 Time Machine 恢复
~/Library/Safari/
~/Library/Application Support/Google/Chrome/
~/Library/Application Support/Firefox/
```

### 问题 5：开发环境损坏

**可能原因**：
- 误删了 node_modules 或其他依赖

**解决方案**：
```bash
# 重新安装依赖
npm install
# 或
yarn install

# 重新构建项目
npm run build
```

---

## 维护建议

### 1. 定期维护计划

创建定期维护计划：

```bash
# 每周一次日常清理
# 每月一次深度清理
# 每季度一次全面维护

# 使用 cron 或 launchd 自动化
# 创建定期清理提醒
```

### 2. 监控磁盘使用

定期检查磁盘使用情况：

```bash
# 每周检查
df -h

# 分析大文件
mo analyze ~/Documents ~/Downloads

# 设置磁盘空间警报
# 当磁盘使用率 >80% 时提醒
```

### 3. 管理下载文件

定期清理下载文件夹：

```bash
# 检查下载文件
ls -lh ~/Downloads

# 删除旧安装文件
mo installer

# 清理其他下载文件
find ~/Downloads -type f -mtime +30 -delete
```

### 4. 管理媒体文件

定期管理媒体文件：

```bash
# 检查媒体文件大小
du -sh ~/Movies ~/Music ~/Pictures

# 删除重复文件（使用第三方工具）
# gem install duplicates

# 压缩旧视频
# ffmpeg -i input.mp4 -crf 28 output.mp4
```

### 5. 管理开发项目

定期清理开发项目：

```bash
# 删除旧项目
find ~/Projects -type d -mtime +180 -exec rm -rf {} \;

# 清理构建产物
mo purge

# 清理 npm 缓存
npm cache clean --force
```

---

## 性能优化建议

### 1. 系统优化

```bash
# 重建系统数据库
mo optimize

# 重建 Spotlight 索引
sudo mdutil -E /

# 修复磁盘权限
diskutil repairDisk /
```

### 2. 应用优化

- 关闭不必要的启动项
- 禁用不必要的通知
- 清理应用偏好设置

### 3. 网络优化

```bash
# 重置网络
mo optimize

# 清理 DNS 缓存
sudo dscacheutil -flushcache
sudo killall -HUP mDNSResponder

# 更换 DNS 服务器（如果需要）
# 系统偏好设置 > 网络 > 高级 > DNS
```

### 4. 显示优化

- 减少透明度和动画效果
- 关闭动态壁纸
- 调整显示器分辨率

---

## 专业建议

### 1. 备份策略

- 使用 Time Machine 定期备份
- 使用云服务备份重要文件
- 定期测试备份恢复

### 2. 清理时机

- 在系统空闲时清理
- 避免在重要任务前清理
- 选择周末或假期进行深度清理

### 3. 清理日志

记录清理操作：

```bash
# 创建清理日志
echo "$(date): 开始清理" >> ~/cleanup.log

# 记录清理结果
mo clean --dry-run >> ~/cleanup.log

# 保存清理前后对比
```

### 4. 自动化

使用自动化工具：

```bash
# 创建清理脚本
cat > ~/cleanup.sh << 'EOF'
#!/bin/bash
mo clean --dry-run
mo clean
EOF

# 设置可执行权限
chmod +x ~/cleanup.sh

# 使用 launchd 定期执行
# 创建 ~/Library/LaunchAgents/com.user.cleanup.plist
```

---

## 参考资源

- Mole 官方文档：https://github.com/tw93/mole
- Apple 官方维护指南：https://support.apple.com/zh-cn/macos
- macOS 存储管理：系统偏好设置 > 关于本机 > 存储空间

---

## 总结

遵循这些最佳实践，可以：

1. **安全清理**：避免误删重要文件
2. **优化性能**：保持系统流畅运行
3. **释放空间**：最大化磁盘使用效率
4. **预防问题**：减少系统故障和数据丢失

记住：**清理是为了优化，不是为了冒险**。始终谨慎操作，定期备份。
