/**
 * TODO生成器
 * 根据组件扫描结果生成todos.md任务清单
 */

import * as fs from 'fs';
import * as path from 'path';
import { scanComponents, ComponentInfo } from './scan-components';

interface TodoItem {
  number: number;
  componentPath: string;
  docPath: string;
  status: 'missing' | 'outdated';
  completed: boolean;
}

/**
 * 生成todos.md内容
 */
function generateTodosMarkdown(components: ComponentInfo[]): string {
  const date = new Date().toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit'
  });

  const missing = components.filter(c => c.status === 'missing');
  const outdated = components.filter(c => c.status === 'outdated');

  let markdown = `# 组件文档更新任务清单

> 生成时间: ${date}
> 总计: ${components.length} 个任务（${missing.length} 个新增，${outdated.length} 个更新）
> 使用git提交历史进行时间对比

---

## 📋 统计信息

- **需要新增文档**: ${missing.length} 个组件
- **需要更新文档**: ${outdated.length} 个组件
- **总任务数**: ${components.length} 个

---

## ✅ 任务列表

`;

  // 生成任务列表
  components.forEach((comp, index) => {
    const number = index + 1;
    const isMissing = comp.status === 'missing';
    const statusIcon = isMissing ? '🆕' : '🔄';
    const statusText = isMissing ? '新增文档' : '更新文档';
    const relativePath = path.relative(process.cwd(), comp.componentPath);

    markdown += `### ${number}. ${statusIcon} ${statusText}: ${path.basename(comp.componentPath)}

\`\`\`
组件路径: ${relativePath}
文档路径: ${path.relative(process.cwd(), comp.docPath)}
状态: ${isMissing ? '文档缺失' : '文档过时'}
组件git提交时间: ${comp.componentMtime.toLocaleString('zh-CN')}
${isMissing ? '' : `文档git提交时间: ${comp.docMtime?.toLocaleString('zh-CN')}`}
\`\`\`

#### 操作步骤

1. [ ] 读取组件源码: \`${relativePath}\`
2. [ ] 分析组件结构（Props、类型、依赖等）
3. [ ] ${isMissing ? '创建新文档' : '更新现有文档'}: \`${path.relative(process.cwd(), comp.docPath)}\`
4. [ ] 验证文档格式是否符合规范
5. [ ] 检查文档完整性（API、类型、示例等）

---

`;
  });

  // 添加使用说明
  markdown += `## 📝 使用说明

1. 按照任务列表顺序处理每个组件
2. 完成一个任务后，在对应的 [ ] 中添加 x 标记为已完成
3. 所有任务完成后，删除此文件

## 📚 文档规范参考

所有组件文档必须遵循以下格式规范：

- **引用方式**: import 方式
- **功能类型**: 工具/组件
- **功能名称**: 组件/工具名称
- **功能描述**: 详细描述和适用场景
- **何时使用**: 使用场景说明
- **使用示例**: 代码示例
- **API**: 完整的API表格（属性名、类型、说明、默认值）
- **类型描述**: TypeScript类型定义表格
- **主题变量**: CSS主题变量（如有）

`;

  return markdown;
}

/**
 * 写入todos.md文件
 */
function writeTodosFile(content: string, outputPath: string = 'todos.md'): void {
  fs.writeFileSync(outputPath, content, 'utf-8');
  console.log(`✅ 已生成任务清单: ${outputPath}`);
}

// CLI 接口
if (require.main === module) {
  const args = process.argv.slice(2);
  const rootDir = args[0] || process.cwd();
  const outputPath = args[1] || path.join(rootDir, 'todos.md');

  console.log(`🔍 扫描组件中...`);

  try {
    const components = scanComponents({ rootDir });

    if (components.length === 0) {
      console.log(`✅ 所有组件文档都是最新的，无需更新！`);
      process.exit(0);
    }

    console.log(`📝 生成任务清单中...\n`);
    const content = generateTodosMarkdown(components);
    writeTodosFile(content, outputPath);

    console.log(`\n🎉 任务清单生成完成！`);
    console.log(`   - 文件位置: ${outputPath}`);
    console.log(`   - 任务数量: ${components.length}`);
    console.log(`\n💡 下一步: 打开 todos.md 查看详细任务列表\n`);

  } catch (error) {
    console.error('❌ 生成失败:', error);
    process.exit(1);
  }
}

export { generateTodosMarkdown, writeTodosFile, TodoItem };
