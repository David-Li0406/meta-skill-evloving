/**
 * 组件文档扫描器
 * 扫描项目中的组件文件，对比文档更新时间，识别需要更新或新增文档的组件
 * 使用git提交历史获取准确的文件修改时间
 */

import * as fs from 'fs';
import * as path from 'path';
import { execSync } from 'child_process';

interface ComponentInfo {
  componentPath: string;
  docPath: string;
  componentMtime: Date;
  docMtime: Date | null;
  status: 'missing' | 'outdated' | 'current';
}

interface ScanOptions {
  rootDir: string;
  extensions?: string[];
  docFileName?: string; // 文档文件名（默认为 index.zh-CN.md）
  excludeDirs?: string[];
  excludeFiles?: string[]; // 排除的文件模式
}

/**
 * 判断文件是否应该被排除
 */
function shouldExcludeFile(fileName: string, excludePatterns: string[]): boolean {
  return excludePatterns.some(pattern => {
    // 支持简单的通配符匹配
    const regex = new RegExp(pattern.replace('*', '.*'));
    return regex.test(fileName);
  });
}

/**
 * 获取文件的git最后提交时间
 * @param filePath 文件路径
 * @returns 最后提交时间的Date对象，如果文件不在git历史中则返回null
 */
function getGitLastModifiedTime(filePath: string): Date | null {
  try {
    // 从文件所在目录开始向上查找git仓库根目录
    let currentDir = path.dirname(filePath);
    let gitRoot: string | null = null;

    // 向上查找.git目录，最多查找10层
    for (let i = 0; i < 10; i++) {
      const gitDir = path.join(currentDir, '.git');
      if (fs.existsSync(gitDir)) {
        gitRoot = currentDir;
        break;
      }

      const parentDir = path.dirname(currentDir);
      if (parentDir === currentDir) {
        // 已到达根目录
        break;
      }
      currentDir = parentDir;
    }

    if (!gitRoot) {
      // 文件不在git仓库中
      return null;
    }

    const gitDirPath = path.join(gitRoot, '.git');

    // 检查文件是否被git跟踪（使用绝对路径）
    try {
      execSync(
        `git --git-dir="${gitDirPath}" --work-tree="${gitRoot}" ls-files --error-unmatch "${filePath}"`,
        {
          encoding: 'utf-8',
          stdio: ['pipe', 'pipe', 'ignore']
        }
      );
    } catch {
      // 文件不在git跟踪中（可能是新文件）
      return null;
    }

    // 获取文件的最后提交时间戳（Unix时间戳，秒）
    const timestamp = execSync(
      `git --git-dir="${gitDirPath}" --work-tree="${gitRoot}" log -1 --format=%ct -- "${filePath}"`,
      {
        encoding: 'utf-8',
        stdio: ['pipe', 'pipe', 'ignore']
      }
    ).trim();

    if (!timestamp) {
      return null;
    }

    // 转换为Date对象（秒转毫秒）
    return new Date(parseInt(timestamp) * 1000);
  } catch (error) {
    // 获取git时间失败，返回null
    return null;
  }
}

/**
 * 扫描目录下的组件文件
 */
function scanComponents(options: ScanOptions): ComponentInfo[] {
  const {
    rootDir,
    extensions = ['.tsx', '.jsx'], // 默认只扫描组件文件，不包括 .ts/.js
    docFileName = 'index.zh-CN.md',
    excludeDirs = ['node_modules', 'dist', 'build', '.git', 'styles'],
    excludeFiles = ['index.ts', 'index.tsx', 'index.js', 'index.jsx', '*.store.ts', '*.store.js', 'use*.ts', 'use*.js']
  } = options;

  const components: ComponentInfo[] = [];

  /**
   * 扫描组件目录（一级子目录）
   */
  function scanComponentDirs(rootDir: string) {
    const entries = fs.readdirSync(rootDir, { withFileTypes: true });

    for (const entry of entries) {
      const componentDir = path.join(rootDir, entry.name);

      // 只处理一级子目录
      if (!entry.isDirectory()) {
        continue;
      }

      // 跳过排除的目录
      if (excludeDirs.includes(entry.name)) {
        continue;
      }

      // 在组件目录中查找主要的组件文件
      const files = fs.readdirSync(componentDir);
      const mainComponentFile = files.find(file => {
        // 匹配与目录名同名的 .tsx 或 .jsx 文件
        const baseName = path.basename(file, path.extname(file));
        const ext = path.extname(file);
        const isMainComponent = baseName.toLowerCase() === entry.name.toLowerCase() && extensions.includes(ext);
        const notExcluded = !shouldExcludeFile(file, excludeFiles);
        return isMainComponent && notExcluded;
      });

      if (mainComponentFile) {
        const componentPath = path.join(componentDir, mainComponentFile);
        const docPath = path.join(componentDir, docFileName);

        // 使用git获取组件文件修改时间
        const componentMtime = getGitLastModifiedTime(componentPath);

        // 如果组件文件没有git历史（新文件），使用文件系统时间作为备选
        const componentTime = componentMtime || fs.statSync(componentPath).mtime;

        // 检查文档是否存在
        let docMtime: Date | null = null;
        let status: ComponentInfo['status'] = 'missing';

        if (fs.existsSync(docPath)) {
          // 使用git获取文档修改时间
          const gitDocTime = getGitLastModifiedTime(docPath);

          // 如果文档没有git历史（新文件），使用文件系统时间作为备选
          docMtime = gitDocTime || fs.statSync(docPath).mtime;

          // 比较时间：组件比文档新则需要更新
          if (componentTime > docMtime) {
            status = 'outdated';
          } else {
            status = 'current';
          }
        }

        // 只记录需要更新或新增的组件
        if (status !== 'current') {
          components.push({
            componentPath,
            docPath,
            componentMtime: componentTime,
            docMtime,
            status
          });
        }
      }
    }
  }

  scanComponentDirs(rootDir);
  return components;
}

/**
 * 打印扫描结果
 */
function printResults(components: ComponentInfo[]) {
  const missing = components.filter(c => c.status === 'missing').length;
  const outdated = components.filter(c => c.status === 'outdated').length;

  console.log(`\n📊 扫描结果:`);
  console.log(`   - 需要新增文档: ${missing} 个组件`);
  console.log(`   - 需要更新文档: ${outdated} 个组件`);
  console.log(`   - 总计: ${components.length} 个组件`);
  console.log(`   ℹ️  使用git提交历史进行时间对比\n`);

  if (components.length > 0) {
    console.log(`📝 组件列表:`);
    components.forEach((comp, index) => {
      const statusIcon = comp.status === 'missing' ? '❌' : '⚠️';
      const statusText = comp.status === 'missing' ? '缺失' : '过时';
      const componentName = path.basename(path.dirname(comp.componentPath));
      console.log(`   ${index + 1}. ${statusIcon} ${componentName}`);
      console.log(`      组件文件: ${path.basename(comp.componentPath)}`);
      console.log(`      状态: ${statusText}`);
      console.log(`      组件git提交时间: ${comp.componentMtime.toLocaleString('zh-CN')}`);
      if (comp.docMtime) {
        console.log(`      文档git提交时间: ${comp.docMtime.toLocaleString('zh-CN')}`);
      }
      console.log('');
    });
  }
}

// CLI 接口
if (require.main === module) {
  const args = process.argv.slice(2);
  const rootDir = args[0] || process.cwd();

  console.log(`🔍 开始扫描组件...`);
  console.log(`   根目录: ${rootDir}\n`);

  try {
    const components = scanComponents({ rootDir });
    printResults(components);

    // 输出JSON格式供后续处理
    if (args.includes('--json')) {
      console.log('\n📄 JSON 输出:');
      console.log(JSON.stringify(components, null, 2));
    }
  } catch (error) {
    console.error('❌ 扫描失败:', error);
    process.exit(1);
  }
}

export { scanComponents, ComponentInfo, ScanOptions };
