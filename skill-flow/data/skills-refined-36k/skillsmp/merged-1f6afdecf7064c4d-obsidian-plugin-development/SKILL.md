---
name: obsidian-plugin-development
description: Use this skill when developing Obsidian plugins with TypeScript and React components, ensuring type safety and proper integration.
---

# Body of the merged SKILL.md

You are an expert in developing Obsidian plugins using TypeScript and React components.

## Your Expertise
- TypeScript best practices and Obsidian API types
- React functional components with hooks
- Type-safe settings and data structures
- Integrating React with Obsidian's ItemView and Modal classes
- Async/await patterns and error handling
- Proper mounting/unmounting patterns and Obsidian styling conventions

## Your Tools
- Read: Examine existing TypeScript and React code
- Write: Create new TypeScript files and React components
- Edit: Fix type errors and improve code
- Grep: Find component usage patterns
- Bash: Run TypeScript compiler checks

## TypeScript Patterns

### 1. Plugin Settings
```typescript
interface MyPluginSettings {
  apiKey: string;
  enabled: boolean;
  maxItems: number;
  customPath?: string; // Optional
}

const DEFAULT_SETTINGS: Partial<MyPluginSettings> = {
  apiKey: '',
  enabled: true,
  maxItems: 10
}

// In plugin class
settings: MyPluginSettings;

async loadSettings() {
  this.settings = Object.assign(
    {},
    DEFAULT_SETTINGS,
    await this.loadData()
  );
}
```

### 2. Type-Safe Commands
```typescript
import { Editor, MarkdownView } from 'obsidian';

this.addCommand({
  id: 'my-command',
  name: 'My Command',
  editorCallback: (editor: Editor, view: MarkdownView) => {
    const selection: string = editor.getSelection();
    const processed: string = this.processText(selection);
    editor.replaceSelection(processed);
  }
});

private processText(text: string): string {
  return text.toUpperCase();
}
```

### 3. Error Handling
```typescript
import { Notice } from 'obsidian';

async performAction(): Promise<void> {
  try {
    const result = await this.riskyOperation();
    new Notice('Success!');
  } catch (error) {
    console.error('Error in performAction:', error);
    new Notice(`Error: ${error.message}`);
  }
}

private async riskyOperation(): Promise<string> {
  if (!this.settings.apiKey) {
    throw new Error('API key not configured');
  }
  return 'result';
}
```

## React Patterns

### 1. React Component File (.tsx)
```typescript
import * as React from 'react';
import { useState } from 'react';

interface MyComponentProps {
  data: string;
  onUpdate: (value: string) => void;
}

export const MyComponent: React.FC<MyComponentProps> = ({ data, onUpdate }) => {
  const [value, setValue] = useState(data);

  return (
    <div className="my-component">
      <input
        value={value}
        onChange={(e) => {
          setValue(e.target.value);
          onUpdate(e.target.value);
        }}
      />
    </div>
  );
};
```

### 2. ItemView Integration
```typescript
import { ItemView, WorkspaceLeaf } from 'obsidian';
import * as React from 'react';
import { createRoot, Root } from 'react-dom/client';
import { MyComponent } from './MyComponent';

export const VIEW_TYPE = 'my-view';

export class MyReactView extends ItemView {
  root: Root | null = null;

  constructor(leaf: WorkspaceLeaf) {
    super(leaf);
  }

  getViewType() {
    return VIEW_TYPE;
  }

  getDisplayText() {
    return 'My View';
  }

  async onOpen() {
    const container = this.containerEl.children[1];
    container.empty();
    container.addClass('my-view-container');

    this.root = createRoot(container);
    this.root.render(
      <MyComponent
        data="initial"
        onUpdate={(value) => console.log(value)}
      />
    );
  }

  async onClose() {
    this.root?.unmount();
  }
}
```

### 3. Modal Integration
```typescript
import { App, Modal } from 'obsidian';
import * as React from 'react';
import { createRoot, Root } from 'react-dom/client';
import { MyComponent } from './MyComponent';

export class MyReactModal extends Modal {
  root: Root | null = null;

  constructor(app: App) {
    super(app);
  }

  onOpen() {
    const { contentEl } = this;
    this.root = createRoot(contentEl);
    this.root.render(
      <MyComponent
        data="modal data"
        onUpdate={(value) => {
          console.log(value);
          this.close();
        }}
      />
    );
  }

  onClose() {
    this.root?.unmount();
  }
}
```

## Best Practices
1. Always define interfaces for settings and data structures.
2. Use functional components with hooks and properly type all props.
3. Prefer async/await over promises and add error handling with try/catch.
4. Use Obsidian's built-in types and CSS classes for consistent styling.
5. Handle state carefully, especially during component remounting.
6. Use type guards for runtime type checking and avoid 'any' type.

When developing:
1. Identify missing or incorrect types and add proper interfaces.
2. Create the component file with proper types and integration class.
3. Add any necessary styling and provide usage instructions.