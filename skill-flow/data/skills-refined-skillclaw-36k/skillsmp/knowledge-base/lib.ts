import { readdir, stat, readFile, mkdir, writeFile, copyFile } from "fs/promises";
import { join, resolve, dirname, extname } from "path";
import { fileURLToPath } from "url";
import { exec } from "child_process";
import { promisify } from "util";

const execAsync = promisify(exec);

// 自动定位当前项目的 docs/knowledge 目录
const KNOWLEDGE_ROOT = resolve(process.cwd(), "docs/knowledge");

// 技能模板目录
const TEMPLATES_DIR = resolve(dirname(fileURLToPath(import.meta.url)), "templates");

// 标准目录结构
const REQUIRED_DIRS = [
  "concepts",   // 概念
  "guides",     // 指南
  "decisions",  // 决策
  "external"    // 外部参考
];

async function exists(path: string) {
  try {
    await stat(path);
    return true;
  } catch {
    return false;
  }
}

// 生成 ISO 日期字符串 (yyyy-mm-dd)
function getISODateString(): string {
  const now = new Date();
  const year = now.getFullYear();
  const month = String(now.getMonth() + 1).padStart(2, "0");
  const day = String(now.getDate()).padStart(2, "0");
  return `${year}-${month}-${day}`;
}

// 替换模板中的占位符
function replaceTemplatePlaceholders(content: string, date: string, name: string, category?: string): string {
  return content
    .replace(/{{date}}/g, date)
    .replace(/{{name}}/g, name)
    .replace(/{{category}}/g, category || "general");
}

// 1. Init
async function init() {
  console.log(`🧠 Initializing Knowledge Base at: ${KNOWLEDGE_ROOT}\n`);

  if (!(await exists(KNOWLEDGE_ROOT))) {
    await mkdir(KNOWLEDGE_ROOT, { recursive: true });
    console.log(`✅ Created: ${KNOWLEDGE_ROOT}`);
  }

  for (const dir of REQUIRED_DIRS) {
    const path = join(KNOWLEDGE_ROOT, dir);
    if (!(await exists(path))) {
      await mkdir(path, { recursive: true });
      console.log(`✅ Created: ${path}/`);
    }
  }

  const indexPath = join(KNOWLEDGE_ROOT, "index.md");
  if (!(await exists(indexPath))) {
    await writeFile(indexPath, "# Knowledge Base Index\n\n> Generated automatically\n");
    console.log(`✅ Created: index.md`);
  }

  console.log(`\n✨ Knowledge Base structure initialized!`);
}

// 2. Scan
async function scan() {
  console.log(`🔍 Scanning project structure for undocumented concepts...\n`);

  const projectRoot = resolve(process.cwd(), "src");
  if (!(await exists(projectRoot))) {
    console.log("❌ src/ directory not found. Run from project root.");
    process.exit(1);
  }

  const { stdout } = await execAsync(`find ${projectRoot} -name "*.ts" -type f 2>/dev/null`);
  const files = stdout.trim().split("\n").filter(Boolean);

  const concepts = new Set<string>();

  for (const file of files) {
    const fileName = extname(file).replace(".ts", "");
    const fileNameConcepts = fileName
      .split(/[-_.]/)
      .map(word => word.charAt(0).toUpperCase() + word.slice(1))
      .filter(word => word.length > 2);

    fileNameConcepts.forEach(concept => concepts.add(concept));

    const content = await readFile(file, 'utf-8');
    const classMatches = content.matchAll(/export (?:class|interface|type) (\w+)/g);
    for (const match of classMatches) {
      concepts.add(match[1]);
    }
  }

  const sortedConcepts = Array.from(concepts).sort();

  const reportPath = join(KNOWLEDGE_ROOT, "SCAN_REPORT.md");
  let reportContent = "# Undocumented Concepts\n\n";
  reportContent += `Scan Date: ${new Date().toISOString()}\n`;
  reportContent += `Total Files: ${files.length}\n`;
  reportContent += `Found Concepts: ${sortedConcepts.length}\n\n`;
  reportContent += "## Concepts\n\n";

  for (const concept of sortedConcepts) {
    const existsInDocs = await exists(join(KNOWLEDGE_ROOT, "concepts", `${concept}.md`));
    const mark = existsInDocs ? "✅" : "⬜";
    reportContent += `- [${mark}] **${concept}**\n`;
  }

  reportContent += "\n\n## Next Steps\n";
  reportContent += "Run `bun ~/.pi/agent/skills/knowledge-base/lib.ts create concept <Name>` to document these.";

  await writeFile(reportPath, reportContent);
  console.log(`✅ Scan complete. Suggestions saved to: ${reportPath}`);
  console.log(reportContent);
}

// 3. Create
async function create(type: string, name: string, category?: string) {
  if (!['concept', 'guide', 'decision', 'term'].includes(type)) {
    console.error("❌ Invalid type. Use: concept, guide, decision, or term");
    process.exit(1);
  }

  if (!name) {
    console.error("❌ Please provide a name.");
    process.exit(1);
  }

  const actualType = type === 'term' ? 'concept' : type;

  const filename = name.replace(/[^a-zA-Z0-9\-_]/g, '') + ".md";
  let subDir = actualType + "s";
  let templateName = `${actualType}-template.md`;

  let targetDir = join(KNOWLEDGE_ROOT, subDir);
  if (category) {
    const sanitizedCategory = category.replace(/[^a-zA-Z0-9\-_/]/g, '');
    targetDir = join(targetDir, sanitizedCategory);
    if (!(await exists(targetDir))) {
      await mkdir(targetDir, { recursive: true });
      console.log(`✅ Created category directory: ${sanitizedCategory}/`);
    }
  }

  if (type === 'decision') {
    const date = new Date().toISOString().slice(0, 10).replace(/-/g, "");
    const safeName = name.replace(/\s+/g, '-');
    const finalFilename = `${date}-${safeName}.md`;

    const targetPath = join(targetDir, finalFilename);
    if (await exists(targetPath)) {
      console.error(`❌ File exists: ${targetPath}`);
      process.exit(1);
    }

    let content = await readFile(join(TEMPLATES_DIR, templateName), 'utf-8');
    content = content.replace(/\[Decision Title\]/, name);
    content = replaceTemplatePlaceholders(content, getISODateString(), name, category);

    await writeFile(targetPath, content);
    console.log(`✅ Created: ${targetPath}`);
    return;
  }

  const targetPath = join(targetDir, filename);
  if (await exists(targetPath)) {
    console.error(`❌ File exists: ${targetPath}`);
    process.exit(1);
  }

  let content = await readFile(join(TEMPLATES_DIR, templateName), 'utf-8');
  content = content.replace(/\[Concept Name\]|\[Guide Title\]/, name);
  content = replaceTemplatePlaceholders(content, getISODateString(), name, category);

  await writeFile(targetPath, content);
  console.log(`✅ Created: ${targetPath}`);
}

// 4. Index
async function generateIndex() {
  console.log("🔄 Generating Knowledge Index...");

  let content = "# Knowledge Base Index\n\n";
  content += "> Generated automatically. Do not edit manually.\n\n";

  for (const dir of REQUIRED_DIRS) {
    const dirPath = join(KNOWLEDGE_ROOT, dir);
    if (!(await exists(dirPath))) continue;

    content += `## ${dir.charAt(0).toUpperCase() + dir.slice(1)}\n`;

    const docs: { path: string; title: string; relativePath: string }[] = [];
    
    async function collectDocs(currentDir: string, relativePath: string = "") {
      const entries = await readdir(currentDir);
      for (const entry of entries) {
        const fullPath = join(currentDir, entry);
        const statInfo = await stat(fullPath);
        
        if (statInfo.isDirectory()) {
          await collectDocs(fullPath, join(relativePath, entry));
        } else if (entry.endsWith('.md') && entry !== 'index.md') {
          const fileContent = await readFile(fullPath, 'utf-8');
          const titleMatch = fileContent.match(/^#\s+(.+)$/m) || fileContent.match(/^title:\s+"(.+)"$/m);
          const title = titleMatch ? titleMatch[1] : entry.replace('.md', '');
          docs.push({
            path: fullPath,
            title: title,
            relativePath: join(relativePath, entry)
          });
        }
      }
    }
    
    await collectDocs(dirPath);
    
    if (docs.length === 0) {
      content += "*No documents yet*\n\n";
      continue;
    }

    docs.forEach(doc => {
      content += `- [${doc.title}](knowledge/${doc.relativePath})\n`;
    });
    content += "\n";
  }

  await writeFile(join(KNOWLEDGE_ROOT, "index.md"), content);
  console.log("✅ Index generated!");
}

// CLI
const command = process.argv[2];

switch (command) {
  case 'init':
    init();
    break;
  case 'scan':
    scan();
    break;
  case 'create':
    const type = process.argv[3];
    const name = process.argv[4];
    const category = process.argv[5];
    create(type, name, category);
    break;
  case 'index':
    generateIndex();
    break;
  default:
    console.log(`
Knowledge Base Skill v1.0

Usage:
  bun lib.ts init                 Initialize knowledge base structure
  bun lib.ts scan                 Scan project for undocumented concepts
  bun lib.ts create <type> <name> [category]  Create a document
  bun lib.ts index                Generate index.md

Types:
  concept, guide, decision, term

Examples:
  bun lib.ts create concept "UserAuthentication" auth
  bun lib.ts create guide "ErrorHandling" backend
  bun lib.ts create decision "UsePostgres" database
`);
}
