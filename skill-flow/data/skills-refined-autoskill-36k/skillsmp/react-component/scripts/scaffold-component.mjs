#!/usr/bin/env node

import { fileURLToPath } from 'url';
import path from 'path';
import fs from 'fs';

// Get __dirname equivalent in ES Modules
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const [featureName, componentName] = process.argv.slice(2);

if (!featureName || !componentName) {
  console.error('Usage: node scaffold-component.mjs <featureName> <ComponentName>');
  console.error('Example: node scaffold-component.mjs userProfile UserProfileCard');
  process.exit(1);
}

const targetDir = path.join(process.cwd(), `src/features/${featureName}/components`);
const containerPath = path.join(targetDir, `${componentName}Container.tsx`);
const viewPath = path.join(targetDir, `${componentName}View.tsx`);
const storiesPath = path.join(targetDir, `${componentName}View.stories.tsx`);

// Ensure target directory exists
fs.mkdirSync(targetDir, { recursive: true });

const toCamelCase = (name) => name.charAt(0).toLowerCase() + name.slice(1);
const componentNameCamel = toCamelCase(componentName);
const featureNameCamel = toCamelCase(featureName);

const containerContent = `// src/features/${featureName}/components/${componentName}Container.tsx
import { ${componentName}View } from './${componentName}View';
// TODO: Replace with your actual data fetching hook
import { use${componentName}Query } from '../api/use${componentName}Query';

interface ${componentName}Data {
  // Define your data structure here
  id: string;
  name: string;
}

export function ${componentName}Container() {
  // TODO: Implement your actual data fetching logic
  const { data, error, isLoading } = use${componentName}Query();

  if (isLoading) return <${componentName}View state="loading" />; 
  if (error) return <${componentName}View state="error" message={error.message} />;
  if (!data) return <${componentName}View state="empty" />;

  return <${componentName}View state="ready" data={data} />;
}
`;

const viewContent = `// src/features/${featureName}/components/${componentName}View.tsx
import React from 'react';

interface ${componentName}Data {
  // Define your data structure here
  id: string;
  name: string;
}

export type ${componentName}ViewProps =
  | { state: 'loading' }
  | { state: 'error'; message: string }
  | { state: 'empty' }
  | { state: 'ready'; data: ${componentName}Data };

export function ${componentName}View(props: ${componentName}ViewProps) {
  switch (props.state) {
    case 'loading':
      return <div className="p-4 text-center text-gray-500">Loading ${componentNameCamel}...</div>;
    case 'error':
      return <div className="p-4 text-center text-red-500">Error: {props.message}</div>;
    case 'empty':
      return <div className="p-4 text-center text-gray-500">No ${componentNameCamel} data available.</div>;
    case 'ready':
      return (
        <div className="p-4 border rounded-lg shadow-sm">
          <h2 className="text-xl font-semibold">Hello, {props.data.name}!</h2>
          <p className="text-gray-600">ID: {props.data.id}</p>
          {/* TODO: Implement your actual UI for the ready state */}
        </div>
      );
    default:
      return null;
  }
}
`;

const storiesContent = `// src/features/${featureName}/components/${componentName}View.stories.tsx
import type { Meta, StoryObj } from '@storybook/react';
import { ${componentName}View, type ${componentName}ViewProps } from './${componentName}View';
import { HttpResponse, http, delay } from 'msw';

// Mock data for the ready state
const mock${componentName}Data = {
  id: 'abc-123',
  name: 'Jane Doe',
};

// Define a mock query hook (replace with your actual one if it exists)
const use${componentName}Query = () => {
  return { data: mock${componentName}Data, error: null, isLoading: false };
};


const meta = {
  title: 'Features/${featureNameCamel}/${componentName}View',
  component: ${componentName}View,
  tags: ['autodocs'],
  argTypes: {
    state: {
      control: 'select',
      options: ['loading', 'error', 'empty', 'ready'],
      description: 'The current state of the component',
    },
    message: {
      control: 'text',
      description: 'Error message (only for error state)',
    },
    data: {
      control: 'object',
      description: 'Data to display (only for ready state)',
    },
  },
  parameters: {
    // Add MSW handlers for API mocking if needed
    msw: {
      handlers: [
        http.get('/api/${featureNameCamel}/${componentNameCamel}', () => {
          return HttpResponse.json(mock${componentName}Data);
        }),
      ],
    },
  },
} satisfies Meta<typeof ${componentName}View>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Loading: Story = {
  args: {
    state: 'loading',
  },
  parameters: {
    msw: {
      handlers: [
        http.get('/api/${featureNameCamel}/${componentNameCamel}', async () => {
          await delay('infinite'); // Simulate loading
          return HttpResponse.json({});
        }),
      ],
    },
  },
};

export const Empty: Story = {
  args: {
    state: 'empty',
  },
  parameters: {
    msw: {
      handlers: [
        http.get('/api/${featureNameCamel}/${componentNameCamel}', () => {
          return HttpResponse.json({}); // Empty response
        }),
      ],
    },
  },
};

export const Error: Story = {
  args: {
    state: 'error',
    message: 'Failed to fetch ${componentNameCamel} data.',
  },
  parameters: {
    msw: {
      handlers: [
        http.get('/api/${featureNameCamel}/${componentNameCamel}', () => {
          return new HttpResponse(null, { status: 500 }); // Simulate error
        }),
      ],
    },
  },
};

export const Ready: Story = {
  args: {
    state: 'ready',
    data: mock${componentName}Data,
  },
};
`;

try {
  fs.writeFileSync(containerPath, containerContent);
  console.log(`Created: ${containerPath}`);
  fs.writeFileSync(viewPath, viewContent);
  console.log(`Created: ${viewPath}`);
  fs.writeFileSync(storiesPath, storiesContent);
  console.log(`Created: ${storiesPath}`);

  console.log(`\nComponent '${componentName}' for feature '${featureName}' scaffolded successfully.`);
  console.log('Remember to update `src/features/' + featureName + '/api/use' + componentName + 'Query.ts` (or equivalent) for data fetching.');
  console.log('And `src/features/' + featureName + '/types/' + featureName + '.types.ts` for actual data types.');
} catch (error) {
  console.error('Error creating component files:', error);
  process.exit(1);
}
