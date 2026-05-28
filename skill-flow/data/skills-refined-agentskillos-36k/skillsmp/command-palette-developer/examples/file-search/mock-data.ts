// Generate 10,000 mock file objects for demonstration

import type { FileItem, FileType } from './types';

const FILE_EXTENSIONS: FileType[] = [
  'js', 'ts', 'tsx', 'jsx',
  'json', 'md', 'css', 'scss',
  'html', 'svg', 'png', 'jpg',
  'pdf', 'txt', 'yaml', 'yml',
  'toml', 'xml', 'sh', 'py',
  'go', 'rs', 'c', 'cpp',
  'java', 'rb', 'php',
];

const DIRECTORIES = [
  'src/components',
  'src/hooks',
  'src/utils',
  'src/features/auth',
  'src/features/user',
  'src/features/dashboard',
  'src/features/settings',
  'src/lib',
  'src/styles',
  'src/assets/images',
  'src/assets/icons',
  'tests/unit',
  'tests/integration',
  'tests/e2e',
  'docs',
  'config',
  'scripts',
  'public',
  'dist',
  'node_modules/@types',
  'node_modules/react',
  'node_modules/react-dom',
  '.github/workflows',
];

const FILE_NAMES = [
  'index', 'App', 'config', 'utils', 'helpers',
  'types', 'constants', 'hooks', 'api', 'client',
  'service', 'controller', 'model', 'view', 'presenter',
  'Button', 'Input', 'Form', 'Modal', 'Dialog',
  'Header', 'Footer', 'Sidebar', 'Nav', 'Menu',
  'Card', 'List', 'Table', 'Grid', 'Layout',
  'useAuth', 'useFetch', 'useForm', 'useDebounce', 'useTheme',
  'README', 'CHANGELOG', 'LICENSE', 'package',
];

function randomElement<T>(arr: T[]): T {
  return arr[Math.floor(Math.random() * arr.length)];
}

function randomInt(min: number, max: number): number {
  return Math.floor(Math.random() * (max - min + 1)) + min;
}

function generateFileName(index: number): string {
  const baseName = randomElement(FILE_NAMES);
  const suffix = Math.random() > 0.7 ? `-${randomInt(1, 10)}` : '';
  return `${baseName}${suffix}`;
}

function getFileSize(type: FileType): number {
  // Return size in bytes based on file type
  switch (type) {
    case 'jpg':
    case 'png':
      return randomInt(50_000, 5_000_000); // 50KB - 5MB
    case 'pdf':
      return randomInt(100_000, 10_000_000); // 100KB - 10MB
    case 'json':
    case 'md':
      return randomInt(500, 50_000); // 500B - 50KB
    case 'js':
    case 'ts':
    case 'tsx':
    case 'jsx':
      return randomInt(1_000, 100_000); // 1KB - 100KB
    default:
      return randomInt(500, 20_000); // 500B - 20KB
  }
}

function getRandomDate(): Date {
  // Random date within last year
  const now = Date.now();
  const yearAgo = now - 365 * 24 * 60 * 60 * 1000;
  const timestamp = randomInt(yearAgo, now);
  return new Date(timestamp);
}

function generateMockContent(type: FileType, name: string): string {
  switch (type) {
    case 'ts':
    case 'tsx':
      return `import React from 'react';

export interface ${name}Props {
  title: string;
  description?: string;
}

export function ${name}({ title, description }: ${name}Props) {
  return (
    <div className="container">
      <h1>{title}</h1>
      {description && <p>{description}</p>}
    </div>
  );
}`;
    case 'js':
    case 'jsx':
      return `export function ${name}(props) {
  const { title, description } = props;

  return (
    <div className="container">
      <h1>{title}</h1>
      {description && <p>{description}</p>}
    </div>
  );
}`;
    case 'json':
      return JSON.stringify({
        name: name,
        version: '1.0.0',
        description: 'Mock package',
        dependencies: {
          react: '^18.0.0',
          typescript: '^5.0.0',
        },
      }, null, 2);
    case 'md':
      return `# ${name}

This is a mock markdown file.

## Features

- Feature 1
- Feature 2
- Feature 3

## Installation

\`\`\`bash
npm install
\`\`\``;
    case 'css':
      return `.${name.toLowerCase()} {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  padding: 2rem;
}`;
    case 'py':
      return `def ${name.toLowerCase()}(x, y):
    """Calculate sum of two numbers"""
    return x + y

if __name__ == "__main__":
    result = ${name.toLowerCase()}(1, 2)
    print(f"Result: {result}")`;
    default:
      return `// ${name}\n// Mock file content`;
  }
}

export function generateMockFiles(count: number = 10_000): FileItem[] {
  const files: FileItem[] = [];

  for (let i = 0; i < count; i++) {
    const directory = randomElement(DIRECTORIES);
    const extension = randomElement(FILE_EXTENSIONS);
    const baseName = generateFileName(i);
    const name = `${baseName}.${extension}`;
    const path = `${directory}/${name}`;

    files.push({
      id: `file-${i}`,
      name,
      path,
      type: extension,
      size: getFileSize(extension),
      modified: getRandomDate(),
      content: generateMockContent(extension, baseName),
    });
  }

  return files;
}

// Pre-generate files for consistent performance
export const mockFiles: FileItem[] = generateMockFiles(10_000);

// Helper to get files by type
export function getFilesByType(type: FileType): FileItem[] {
  return mockFiles.filter(file => file.type === type);
}

// Helper to get recent files (last 7 days)
export function getRecentFiles(limit: number = 10): FileItem[] {
  const sevenDaysAgo = Date.now() - 7 * 24 * 60 * 60 * 1000;
  return mockFiles
    .filter(file => file.modified.getTime() > sevenDaysAgo)
    .sort((a, b) => b.modified.getTime() - a.modified.getTime())
    .slice(0, limit);
}
