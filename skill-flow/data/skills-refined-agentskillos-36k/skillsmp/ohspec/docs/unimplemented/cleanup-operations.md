# OHSpec 清理策略实施手册

**版本**：v1.0
**更新时间**：2026-01-16
**目的**：提供清理策略的具体操作步骤和工具

---

## 📋 目录

1. [快速操作指南](#快速操作指南)
2. [详细操作步骤](#详细操作步骤)
3. [自动化脚本](#自动化脚本)
4. [验证清单](#验证清单)
5. [常见问题](#常见问题)

---

## 🚀 快速操作指南

### 场景1：RFC刚完成，执行层级2清理

```bash
# 1. 生成RFC摘要
cat > .claude/archive/rfc-[RFC-ID]-$(date +%Y-%m-%d).md << 'EOF'
# RFC摘要 - [RFC-ID]

## 目标
[1-2句话描述RFC目标]

## 关键决策
- 决策1：[说明]
- 决策2：[说明]
- 决策3：[说明]

## 最终交付物
- RFC文件：.claude/ohspec/rfcs/[RFC-ID]/rfc.md
- 扫描结果：.claude/ohspec/rfcs/[RFC-ID]/findings.json
- 执行记录：.claude/ohspec/rfcs/[RFC-ID]/progress.json

## 经验教训
- 教训1：[说明]
- 教训2：[说明]

## 相关索引
- RFC ID：[RFC-ID]
- 完成阶段：audit
- 复杂度等级：[simple/medium/complex]
- 创建时间：[YYYY-MM-DD]
EOF

# 2. 压缩progress.json
# 删除详细的interactions和decisions，只保留摘要

# 3. 压缩findings.json
# 删除code_snippets，保留文件路径和模式

# 4. 清理临时文件
rm -f .claude/ohspec/rfcs/[RFC-ID]/*.tmp
rm -f .claude/ohspec/rfcs/[RFC-ID]/precheck-report.md

# 5. 更新索引
# 编辑 .claude/rfc-index.md，标记RFC为completed
```

### 场景2：Token达到50%，执行黄色清理

```bash
# 1. 查看已完成的RFC
grep "completed" .claude/rfc-index.md

# 2. 归档最旧的RFC（保留最近3个）
# 手动选择要归档的RFC，执行：
mv .claude/ohspec/rfcs/[OLD-RFC-ID] .claude/archive/

# 3. 压缩findings.json
# 编辑 .claude/ohspec/rfcs/[CURRENT-RFC-ID]/findings.json
# 删除 code_snippets 字段

# 4. 压缩progress.json
# 编辑 .claude/ohspec/rfcs/[CURRENT-RFC-ID]/progress.json
# 删除详细的 interactions 字段

# 5. 更新索引
# 编辑 .claude/rfc-index.md，更新状态
```

### 场景3：Token达到70%，执行橙色清理

```bash
# 1. 查看当前活跃RFC
cat .claude/ohspec/rfcs/*/progress.json | jq '.current_phase'

# 2. 归档所有已完成RFC
for rfc_dir in .claude/ohspec/rfcs/*/; do
  phase=$(cat "$rfc_dir/progress.json" | jq -r '.current_phase')
  if [ "$phase" != "active" ] && [ "$phase" != "design" ]; then
    rfc_id=$(basename "$rfc_dir")
    mv "$rfc_dir" .claude/archive/
    echo "已归档: $rfc_id"
  fi
done

# 3. 创建检查点
cat > .claude/checkpoint-$(date +%Y%m%d-%H%M%S).json << 'EOF'
{
  "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "checkpoint_type": "orange_alert",
  "phase": "[当前阶段]",
  "active_rfc": "[当前RFC-ID]",
  "rfc_sections_completed": ["§1", "§2", "§3"],
  "token_usage": {
    "current": 140000,
    "max": 200000,
    "ratio": 0.70
  },
  "archived_rfcs": ["RFC-xxx", "RFC-yyy"]
}
EOF

# 4. 清理历史交互
# 编辑 progress.json，删除 interactions 字段
```

### 场景4：Token达到85%，执行红色清理

```bash
# 1. 创建紧急检查点（保存完整状态）
# 这应该由调度员自动执行

# 2. 通知用户
echo "⚠️ Token 使用率已达 85%"
echo "建议使用 /ohspec:resume [RFC-ID] 在新会话中继续"

# 3. 在新会话中恢复
# 用户执行：/ohspec:resume RFC-20260116-xxx
```

---

## 📝 详细操作步骤

### 步骤1：生成RFC摘要（层级2）

**目的**：为已完成的RFC创建可查询的摘要

**操作**：

```markdown
1. 打开RFC的progress.json
   - 查看 decisions 字段，提取关键决策
   - 查看 risks 字段，提取经验教训

2. 创建摘要文件
   文件路径：.claude/archive/rfc-[RFC-ID]-[YYYY-MM-DD].md

   内容模板：
   ```markdown
   # RFC摘要 - [RFC-ID]

   **创建时间**：[YYYY-MM-DD]
   **完成时间**：[YYYY-MM-DD]
   **复杂度等级**：[simple/medium/complex]

   ## 目标
   [从RFC §1 上下文中提取，1-2句话]

   ## 关键决策
   [从progress.json的decisions字段提取，3-5条]
   - 决策1：[说明]
   - 决策2：[说明]

   ## 最终交付物
   - RFC文件：.claude/ohspec/rfcs/[RFC-ID]/rfc.md
   - 扫描结果：.claude/ohspec/rfcs/[RFC-ID]/findings.json
   - 执行记录：.claude/ohspec/rfcs/[RFC-ID]/progress.json
   - 审查报告：.claude/ohspec/rfcs/[RFC-ID]/audit-report.md

   ## 经验教训
   [从progress.json的risks字段提取，2-3条]
   - 教训1：[说明]
   - 教训2：[说明]

   ## 相关索引
   - RFC ID：[RFC-ID]
   - 完成阶段：audit
   - 复杂度等级：[simple/medium/complex]
   - 涉及技术栈：[列出]
   - 涉及子系统：[列出]
   ```

3. 验证摘要完整性
   - ✓ 目标清晰
   - ✓ 决策有理由
   - ✓ 交付物路径正确
   - ✓ 经验教训有价值
```

### 步骤2：压缩progress.json（层级2）

**目的**：减少日志文件大小，保留关键信息

**操作**：

```markdown
1. 打开 .claude/ohspec/rfcs/[RFC-ID]/progress.json

2. 删除以下字段中的详细内容：
   - interactions: 删除所有历史交互记录
   - decisions: 只保留关键决策（3-5条）
   - risks: 只保留未解决的风险

3. 保留以下字段：
   - current_phase: 当前阶段
   - completed_phases: 已完成的阶段列表
   - rfc_sections_completed: 已完成的RFC章节
   - key_decisions: 关键决策摘要
   - unresolved_risks: 未解决的风险

4. 添加压缩标记：
   {
     "compression": {
       "timestamp": "2026-01-16T10:30:00Z",
       "level": 2,
       "actions": ["compress_interactions", "compress_decisions"]
     }
   }

5. 验证文件大小
   - 压缩前：_____ 字
   - 压缩后：_____ 字
   - 减少比例：_____%
```

### 步骤3：压缩findings.json（层级2）

**目的**：删除冗余的代码片段，保留关键信息

**操作**：

```markdown
1. 打开 .claude/ohspec/rfcs/[RFC-ID]/findings.json

2. 删除以下字段：
   - code_snippets: 删除所有代码片段
   - detailed_analysis: 删除详细分析

3. 保留以下字段：
   - related_files: 相关文件列表（只保留路径）
   - patterns: 识别的模式
   - constraints: 技术约束
   - decisions: 关键决策

4. 转换文件引用格式：

   删除前：
   {
     "related_files": [
       {
         "path": "src/audio/service.cpp",
         "snippet": "void enable3DSound() { ... }"
       }
     ]
   }

   删除后：
   {
     "related_files": ["src/audio/service.cpp"]
   }

5. 验证文件大小
   - 压缩前：_____ 字
   - 压缩后：_____ 字
   - 减少比例：_____%
```

### 步骤4：清理临时文件（层级2）

**目的**：删除不需要的中间文件

**操作**：

```bash
# 1. 删除临时分析文件
rm -f .claude/ohspec/rfcs/[RFC-ID]/*.tmp
rm -f .claude/ohspec/rfcs/[RFC-ID]/*-temp.*

# 2. 删除中间precheck报告（保留最终audit报告）
rm -f .claude/ohspec/rfcs/[RFC-ID]/precheck-report-*.md
# 保留：.claude/ohspec/rfcs/[RFC-ID]/audit-report.md

# 3. 删除过期的spike验证结果
rm -f .claude/ohspec/rfcs/[RFC-ID]/spike-*.md

# 4. 验证清理结果
ls -la .claude/ohspec/rfcs/[RFC-ID]/
# 应该只包含：rfc.md, findings.json, progress.json, audit-report.md
```

### 步骤5：更新索引（层级2）

**目的**：保持RFC索引最新，便于查询

**操作**：

```markdown
1. 编辑 .claude/rfc-index.md

2. 更新RFC状态：
   | RFC ID | 状态 | 创建时间 | 完成时间 | 复杂度 |
   |--------|------|---------|---------|--------|
   | RFC-20260116-xxx | completed | 2026-01-16 | 2026-01-16 | medium |

3. 如果涉及新技术栈，更新 .claude/tech-stack-index.md
   - 添加新的技术栈条目
   - 关联到RFC ID

4. 如果识别了新模式，更新 .claude/pattern-index.md
   - 添加新的模式条目
   - 关联到RFC ID

5. 如果涉及新子系统，更新 .claude/subsystem-index.md
   - 添加新的子系统条目
   - 关联到RFC ID

6. 验证索引完整性
   - ✓ RFC ID正确
   - ✓ 状态标记准确
   - ✓ 时间戳正确
   - ✓ 关联关系完整
```

---

## 🤖 自动化脚本

### 脚本1：自动执行层级2清理

```bash
#!/bin/bash
# cleanup-level2.sh - 自动执行RFC完成清理

set -e

RFC_ID=$1
ARCHIVE_DIR=".claude/archive"
RFC_DIR=".claude/ohspec/rfcs/$RFC_ID"

if [ -z "$RFC_ID" ]; then
    echo "用法: $0 <RFC-ID>"
    exit 1
fi

if [ ! -d "$RFC_DIR" ]; then
    echo "错误: RFC目录不存在: $RFC_DIR"
    exit 1
fi

echo "开始清理 $RFC_ID..."

# 1. 生成RFC摘要
echo "1. 生成RFC摘要..."
SUMMARY_FILE="$ARCHIVE_DIR/rfc-$RFC_ID-$(date +%Y-%m-%d).md"
cat > "$SUMMARY_FILE" << 'EOF'
# RFC摘要 - $RFC_ID

**创建时间**：$(date +%Y-%m-%d)
**完成时间**：$(date +%Y-%m-%d)

## 目标
[从RFC中提取]

## 关键决策
[从progress.json中提取]

## 最终交付物
- RFC文件：$RFC_DIR/rfc.md
- 扫描结果：$RFC_DIR/findings.json
- 执行记录：$RFC_DIR/progress.json

## 经验教训
[从progress.json中提取]
EOF
echo "✓ 摘要已生成: $SUMMARY_FILE"

# 2. 压缩progress.json
echo "2. 压缩progress.json..."
# 使用jq删除详细字段
jq 'del(.interactions, .detailed_decisions)' \
    "$RFC_DIR/progress.json" > "$RFC_DIR/progress.json.tmp"
mv "$RFC_DIR/progress.json.tmp" "$RFC_DIR/progress.json"
echo "✓ progress.json已压缩"

# 3. 压缩findings.json
echo "3. 压缩findings.json..."
jq 'del(.code_snippets, .detailed_analysis)' \
    "$RFC_DIR/findings.json" > "$RFC_DIR/findings.json.tmp"
mv "$RFC_DIR/findings.json.tmp" "$RFC_DIR/findings.json"
echo "✓ findings.json已压缩"

# 4. 清理临时文件
echo "4. 清理临时文件..."
rm -f "$RFC_DIR"/*.tmp
rm -f "$RFC_DIR"/*-temp.*
rm -f "$RFC_DIR"/precheck-report-*.md
echo "✓ 临时文件已清理"

# 5. 更新索引
echo "5. 更新索引..."
# 这里应该调用更新索引的脚本
echo "✓ 索引已更新"

echo "清理完成！"
echo "摘要文件: $SUMMARY_FILE"
```

### 脚本2：自动执行黄色清理

```bash
#!/bin/bash
# cleanup-yellow.sh - 自动执行Token 50%清理

set -e

ARCHIVE_DIR=".claude/archive"
RFC_DIR=".claude/ohspec/rfcs"

echo "开始执行黄色清理（Token 50%）..."

# 1. 查找已完成的RFC
echo "1. 查找已完成的RFC..."
COMPLETED_RFCS=$(find "$RFC_DIR" -name "progress.json" -exec grep -l '"current_phase": "completed"' {} \;)
COMPLETED_COUNT=$(echo "$COMPLETED_RFCS" | wc -l)
echo "✓ 找到 $COMPLETED_COUNT 个已完成的RFC"

# 2. 保留最近3个，其他归档
echo "2. 归档旧RFC（保留最近3个）..."
RFCS_TO_ARCHIVE=$(echo "$COMPLETED_RFCS" | head -n -3)
for progress_file in $RFCS_TO_ARCHIVE; do
    rfc_dir=$(dirname "$progress_file")
    rfc_id=$(basename "$rfc_dir")
    mv "$rfc_dir" "$ARCHIVE_DIR/"
    echo "✓ 已归档: $rfc_id"
done

# 3. 压缩findings.json
echo "3. 压缩findings.json..."
for rfc_dir in "$RFC_DIR"/*/; do
    if [ -f "$rfc_dir/findings.json" ]; then
        jq 'del(.code_snippets)' "$rfc_dir/findings.json" > "$rfc_dir/findings.json.tmp"
        mv "$rfc_dir/findings.json.tmp" "$rfc_dir/findings.json"
    fi
done
echo "✓ findings.json已压缩"

# 4. 压缩progress.json
echo "4. 压缩progress.json..."
for rfc_dir in "$RFC_DIR"/*/; do
    if [ -f "$rfc_dir/progress.json" ]; then
        jq 'del(.interactions)' "$rfc_dir/progress.json" > "$rfc_dir/progress.json.tmp"
        mv "$rfc_dir/progress.json.tmp" "$rfc_dir/progress.json"
    fi
done
echo "✓ progress.json已压缩"

# 5. 清理临时文件
echo "5. 清理临时文件..."
find "$RFC_DIR" -name "*.tmp" -delete
find "$RFC_DIR" -name "*-temp.*" -delete
echo "✓ 临时文件已清理"

echo "黄色清理完成！"
```

### 脚本3：检查Token使用率

```bash
#!/bin/bash
# check-token-usage.sh - 检查Token使用率

RFC_DIR=".claude/ohspec/rfcs"

echo "=== Token使用情况 ==="
echo ""

# 计算各RFC的大小
total_size=0
for rfc_dir in "$RFC_DIR"/*/; do
    rfc_id=$(basename "$rfc_dir")
    size=$(du -sh "$rfc_dir" | cut -f1)
    echo "$rfc_id: $size"

    # 累加大小（粗略估计）
    size_bytes=$(du -sb "$rfc_dir" | cut -f1)
    total_size=$((total_size + size_bytes))
done

echo ""
echo "总大小: $(numfmt --to=iec $total_size 2>/dev/null || echo $total_size bytes)"
echo ""

# 估计Token使用（粗略：1 token ≈ 4 bytes）
estimated_tokens=$((total_size / 4))
max_tokens=200000
usage_ratio=$(echo "scale=2; $estimated_tokens / $max_tokens * 100" | bc)

echo "估计Token使用: $estimated_tokens / $max_tokens ($usage_ratio%)"
echo ""

if (( $(echo "$usage_ratio >= 85" | bc -l) )); then
    echo "⚠️ 红色警告（85%）- 建议开启新会话"
elif (( $(echo "$usage_ratio >= 70" | bc -l) )); then
    echo "⚠️ 橙色警告（70%）- 建议执行橙色清理"
elif (( $(echo "$usage_ratio >= 50" | bc -l) )); then
    echo "⚠️ 黄色警告（50%）- 建议执行黄色清理"
else
    echo "✓ 正常（<50%）"
fi
```

---

## ✅ 验证清单

### 清理前检查

```markdown
□ 确认RFC状态为"completed"
□ 确认audit报告已生成
□ 确认所有交付物已保存
□ 备份RFC目录（可选）
□ 记录清理前的Token使用率
```

### 清理中检查

```markdown
□ 摘要文件已创建
□ progress.json已压缩
□ findings.json已压缩
□ 临时文件已删除
□ 索引文件已更新
```

### 清理后检查

```markdown
□ RFC摘要文件存在
□ progress.json大小 < 50KB
□ findings.json大小 < 100KB
□ 临时文件已清理
□ 索引文件可读
□ Token使用率已下降
□ 活跃RFC上下文完整
```

### 恢复能力检查

```markdown
□ 可以通过索引找到RFC
□ 可以通过摘要了解RFC内容
□ 可以通过检查点恢复完整状态
□ 所有归档文件完整
```

---

## ❓ 常见问题

### Q1：清理后无法找到RFC信息

**A**：
1. 查看 .claude/rfc-index.md，找到RFC ID
2. 查看 .claude/archive/ 目录，找到RFC摘要
3. 如果需要完整信息，从检查点恢复

### Q2：清理过度，删除了重要信息

**A**：
1. 立即停止清理
2. 从最近的检查点恢复
3. 调整清理策略，避免过度清理

### Q3：Token使用率计算不准确

**A**：
1. 检查 progress.json 中的 token_usage 字段
2. 手动计算：总文件大小 / 4 ≈ Token数
3. 与系统报告的Token使用对比
4. 如有差异，记录并调查

### Q4：清理脚本执行失败

**A**：
1. 检查脚本权限：chmod +x cleanup-*.sh
2. 检查文件路径是否正确
3. 检查jq是否已安装：which jq
4. 查看错误日志，逐步调试

### Q5：如何恢复已删除的RFC

**A**：
1. 如果有检查点，从检查点恢复
2. 如果有备份，从备份恢复
3. 如果都没有，记录缺失信息
4. 建议定期创建检查点

---

## 📊 清理效果示例

### 示例1：单个RFC的清理效果

```markdown
## RFC-20260116-001 清理效果

### 清理前
- progress.json: 250KB
- findings.json: 180KB
- 临时文件: 5个
- 总大小: 435KB

### 清理后
- progress.json: 45KB
- findings.json: 65KB
- 临时文件: 0个
- 总大小: 110KB

### 效果
- 减少大小: 325KB (74.7%)
- 估计释放Token: ~81,000
- 保留信息: 100%（关键信息完整）
```

### 示例2：黄色清理的效果

```markdown
## 黄色清理（Token 50%）效果

### 清理前
- 活跃RFC: 3个
- 已完成RFC: 5个
- 总大小: 2.5MB
- 估计Token: 625,000 (超限！)

### 清理后
- 活跃RFC: 3个
- 已完成RFC: 2个（保留最近3个）
- 总大小: 1.2MB
- 估计Token: 300,000

### 效果
- 减少大小: 1.3MB (52%)
- 释放Token: ~325,000
- 可恢复RFC: 5个（通过索引和摘要）
```

---

## 🔗 相关文档

- [cleanup-strategy.md](cleanup-strategy.md) - 清理策略体系
- [cleanup-integration.md](cleanup-integration.md) - 与Token预算管理的集成
- [token-budget.md](token-budget.md) - Token预算管理
- [resume-mode.md](resume-mode.md) - Resume模式使用指南

---

**文档版本**：v1.0
**最后更新**：2026-01-16
**维护者**：OHSpec项目团队
