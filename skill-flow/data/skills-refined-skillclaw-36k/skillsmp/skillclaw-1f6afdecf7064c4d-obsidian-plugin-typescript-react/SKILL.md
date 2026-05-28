---
name: obsidian-plugin-typescript-react-expert
description: Use this skill when developing Obsidian plugins with TypeScript and React, ensuring type safety and proper integration with the Obsidian API.
---

# Your Expertise
- TypeScript best practices for Obsidian plugins
- React functional components with hooks
- Type-safe settings and data structures
- Integrating React with Obsidian's ItemView and Modal classes
- Async/await patterns and error handling
- Obsidian API types and styling conventions

# Your Tools
- Read: Examine existing TypeScript and React code
- Write: Create new TypeScript files and React components
- Edit: Fix type errors and improve code
- Bash: Run TypeScript compiler checks
- Grep: Find component usage patterns

# Obsidian TypeScript and React Patterns

## 1. Plugin Settings
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

## 2. Type-Safe Commands
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
  // Type-safe processing
  return text.toUpperCase();
}
```

## 3. React Component File (.tsx)
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

## 4. ItemView Integration
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

## 5. Modal Integration
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