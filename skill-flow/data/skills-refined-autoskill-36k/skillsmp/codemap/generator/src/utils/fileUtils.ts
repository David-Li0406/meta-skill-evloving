/**
 * 文件工具
 */

import { readFileSync, existsSync } from "fs";
import { join, relative, extname } from "path";

export interface FileContent {
  path: string;
  content: string;
}

/**
 * 读取文件内容
 */
export function readFiles(
  filePaths: string[],
  projectRoot: string,
): FileContent[] {
  const files: FileContent[] = [];

  for (const filePath of filePaths) {
    try {
      if (!existsSync(filePath)) {
        console.error(`File not found: ${filePath}`);
        continue;
      }

      const relativePath = relative(projectRoot, filePath);
      const content = readFileSync(filePath, "utf-8");

      files.push({
        path: relativePath,
        content,
      });
    } catch (e) {
      console.error(`Failed to read file: ${filePath}`, e);
    }
  }

  return files;
}

/**
 * 根据文件扩展名获取语言
 */
export function getFileLanguage(filePath: string): string {
  const ext = extname(filePath).toLowerCase();

  const langMap: Record<string, string> = {
    ".js": "javascript",
    ".jsx": "javascript",
    ".ts": "typescript",
    ".tsx": "typescript",
    ".py": "python",
    ".rs": "rust",
    ".go": "go",
    ".java": "java",
    ".c": "c",
    ".cpp": "cpp",
    ".h": "c",
    ".hpp": "cpp",
    ".cs": "csharp",
    ".php": "php",
    ".rb": "ruby",
    ".swift": "swift",
    ".kt": "kotlin",
    ".dart": "dart",
    ".scala": "scala",
    ".sh": "bash",
    ".yaml": "yaml",
    ".yml": "yaml",
    ".json": "json",
    ".xml": "xml",
    ".html": "html",
    ".css": "css",
    ".scss": "scss",
    ".sass": "sass",
    ".less": "less",
    ".md": "markdown",
    ".sql": "sql",
  };

  return langMap[ext] || "text";
}

/**
 * 格式化文件为 Markdown 代码块
 */
export function formatFileAsMarkdown(file: FileContent): string {
  const lang = getFileLanguage(file.path);
  return `## ${file.path}
\`\`\`${lang}
${file.content}
\`\`\``;
}

/**
 * 构建生成提示
 */
export function buildGeneratePrompt(
  query: string,
  files: FileContent[],
): string {
  const filesMarkdown = files.map(formatFileAsMarkdown).join("\n\n");

  return `根据以下代码，分析查询："${query}"

文件内容：
${filesMarkdown}

要求：
1. 识别关键组件、函数和类
2. 分析它们之间的关系和调用流程
3. 提取准确的代码行号
4. 创建追踪指南

只返回纯 JSON（无 markdown 代码块）：

{
  "schemaVersion": 1,
  "title": "${query}",
  "description": "简要描述",
  "created_at": "${new Date().toISOString()}",
  "traces": [
    {
      "id": "1",
      "title": "步骤标题",
      "description": "步骤描述",
      "locations": [
        {
          "id": "1a",
          "path": "文件路径",
          "lineNumber": 1,
          "lineContent": "代码内容",
          "title": "节点标题",
          "description": "节点描述"
        }
      ],
      "traceTextDiagram": "树状调用图",
      "traceGuide": "## Motivation\n动机\n\n## Details\n详细说明"
    }
  ]
}`;
}
