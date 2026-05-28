/**
 * 组件分析器
 * 分析组件源代码，提取Props、类型、导入等信息
 */

import * as fs from 'fs';
import * as path from 'path';

interface PropInfo {
  name: string;
  type: string;
  description?: string;
  defaultValue?: string;
  required?: boolean;
}

interface TypeInfo {
  name: string;
  properties: PropInfo[];
  description?: string;
}

interface ComponentAnalysis {
  name: string;
  type: 'component' | 'hook' | 'util' | 'type';
  description?: string;
  imports: string[];
  props: PropInfo[];
  types: TypeInfo[];
  examples: string[];
  dependencies: string[];
}

/**
 * 判断组件类型
 */
function detectComponentType(filePath: string, content: string): ComponentAnalysis['type'] {
  const fileName = path.basename(filePath);

  // Hook检测
  if (/^use[A-Z]/.test(fileName) || content.includes('use') && content.includes('useState')) {
    return 'hook';
  }

  // 工具函数检测
  if (content.includes('export function') && !content.includes('React')) {
    return 'util';
  }

  // 类型定义检测
  if (fileName.includes('.d.ts') || content.includes('export interface') || content.includes('export type')) {
    return 'type';
  }

  // 默认为组件
  return 'component';
}

/**
 * 提取导入语句
 */
function extractImports(content: string): string[] {
  const importRegex = /import\s+(?:(?:\{[^}]*\}|\*\s+as\s+\w+|\w+)\s+from\s+)?['"]([^'"]+)['"]/g;
  const imports: string[] = [];
  let match;

  while ((match = importRegex.exec(content)) !== null) {
    if (!imports.includes(match[1])) {
      imports.push(match[1]);
    }
  }

  return imports;
}

/**
 * 提取Props接口
 */
function extractPropsInterface(content: string): PropInfo[] {
  const props: PropInfo[] = [];

  // 查找Props接口定义
  const interfaceRegex = /(?:interface|type)\s+(\w*Props?\w*)\s*(?:extends\s+(\w+))?\s*\{([^}]+)\}/g;
  let match;

  while ((match = interfaceRegex.exec(content)) !== null) {
    const interfaceName = match[1];
    const interfaceBody = match[3];

    // 提取接口属性
    const propertyRegex = /(\w+)\s*(\?)?:\s*([^;,=\n]+)(?:\s*=\s*([^;,]+))?(?:[;,])/g;
    let propMatch;

    while ((propMatch = propertyRegex.exec(interfaceBody)) !== null) {
      props.push({
        name: propMatch[1],
        type: propMatch[3].trim(),
        required: !propMatch[2], // 有?表示可选
        defaultValue: propMatch[4]?.trim()
      });
    }
  }

  return props;
}

/**
 * 提取类型定义
 */
function extractTypes(content: string): TypeInfo[] {
  const types: TypeInfo[] = [];

  // 查找所有接口和类型定义
  const typeRegex = /(?:export\s+)?(?:interface|type)\s+(\w+)\s*(?:extends\s+(\w+))?\s*\{([^}]+)\}/g;
  let match;

  while ((match = typeRegex.exec(content)) !== null) {
    const typeName = match[1];
    const typeBody = match[3];

    // 跳过Props类型（已在props中处理）
    if (typeName.toLowerCase().includes('props')) {
      continue;
    }

    const properties: PropInfo[] = [];
    const propertyRegex = /(\w+)\s*(\?)?:\s*([^;,=\n]+)(?:\s*=\s*([^;,]+))?(?:[;,])/g;
    let propMatch;

    while ((propMatch = propertyRegex.exec(typeBody)) !== null) {
      properties.push({
        name: propMatch[1],
        type: propMatch[3].trim(),
        required: !propMatch[2]
      });
    }

    types.push({
      name: typeName,
      properties
    });
  }

  return types;
}

/**
 * 提取代码示例（从注释中）
 */
function extractExamples(content: string): string[] {
  const examples: string[] = [];

  // 查找 @example 注释
  const exampleRegex = /@example\s+([\s\S]*?)(?=@\w+|\*\/)/g;
  let match;

  while ((match = exampleRegex.exec(content)) !== null) {
    examples.push(match[1].trim());
  }

  return examples;
}

/**
 * 提取组件描述（从注释中）
 */
function extractDescription(content: string): string | undefined {
  // 查找文件顶部的描述注释
  const descRegex = /\/\*\*[\s\S]*?\* @(?:description|brief)\s+([^\n]+)[\s\S]*?\*\//;
  const match = descRegex.exec(content);
  return match?.[1]?.trim();
}

/**
 * 分析组件文件
 */
function analyzeComponent(filePath: string): ComponentAnalysis {
  const content = fs.readFileSync(filePath, 'utf-8');
  const fileName = path.basename(filePath, path.extname(filePath));

  const componentType = detectComponentType(filePath, content);
  const imports = extractImports(content);
  const props = extractPropsInterface(content);
  const types = extractTypes(content);
  const examples = extractExamples(content);
  const description = extractDescription(content);

  // 提取外部依赖（从import中过滤相对路径）
  const dependencies = imports.filter(imp => !imp.startsWith('.'));

  return {
    name: fileName,
    type: componentType,
    description,
    imports,
    props,
    types,
    examples,
    dependencies
  };
}

/**
 * 打印分析结果
 */
function printAnalysis(analysis: ComponentAnalysis): void {
  console.log(`\n📦 组件分析结果:`);
  console.log(`   名称: ${analysis.name}`);
  console.log(`   类型: ${analysis.type}`);
  if (analysis.description) {
    console.log(`   描述: ${analysis.description}`);
  }

  console.log(`\n📥 导入依赖 (${analysis.imports.length}):`);
  analysis.imports.forEach(imp => console.log(`   - ${imp}`));

  console.log(`\n📋 Props (${analysis.props.length}):`);
  analysis.props.forEach(prop => {
    console.log(`   - ${prop.name}${prop.required ? '' : '?'}: ${prop.type}`);
    if (prop.defaultValue) {
      console.log(`     默认值: ${prop.defaultValue}`);
    }
  });

  if (analysis.types.length > 0) {
    console.log(`\n📝 类型定义 (${analysis.types.length}):`);
    analysis.types.forEach(type => {
      console.log(`   - ${type.name} (${type.properties.length} 个属性)`);
    });
  }

  if (analysis.examples.length > 0) {
    console.log(`\n💡 示例代码:`);
    analysis.examples.forEach((ex, i) => {
      console.log(`   示例 ${i + 1}:`);
      console.log(`   ${ex.split('\n').join('\n   ')}`);
    });
  }
}

// CLI 接口
if (require.main === module) {
  const args = process.argv.slice(2);
  const filePath = args[0];

  if (!filePath) {
    console.error('❌ 请提供组件文件路径');
    console.log('用法: npx ts-node analyze-component.ts <component-file-path>');
    process.exit(1);
  }

  if (!fs.existsSync(filePath)) {
    console.error(`❌ 文件不存在: ${filePath}`);
    process.exit(1);
  }

  try {
    console.log(`🔍 分析组件: ${filePath}\n`);
    const analysis = analyzeComponent(filePath);
    printAnalysis(analysis);

    // 输出JSON格式
    if (args.includes('--json')) {
      console.log('\n📄 JSON 输出:');
      console.log(JSON.stringify(analysis, null, 2));
    }
  } catch (error) {
    console.error('❌ 分析失败:', error);
    process.exit(1);
  }
}

export { analyzeComponent, ComponentAnalysis, PropInfo, TypeInfo };
