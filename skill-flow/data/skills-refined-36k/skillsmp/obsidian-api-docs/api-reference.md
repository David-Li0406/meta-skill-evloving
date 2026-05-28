# Obsidian API Quick Reference

This is a quick reference for commonly used Obsidian APIs. For full details, fetch the documentation URLs.

## Core Classes

### App
The main application interface.
- `app.vault` - Access to the vault
- `app.workspace` - Access to workspace
- `app.metadataCache` - File metadata
- `app.fileManager` - File operations

### Vault
File system operations.
- `vault.getMarkdownFiles()` - Get all markdown files
- `vault.read(file)` - Read file contents
- `vault.modify(file, data)` - Modify file
- `vault.create(path, data)` - Create new file
- `vault.delete(file)` - Delete file
- `vault.adapter.exists(path)` - Check if path exists

### Workspace
UI and layout management.
- `workspace.getActiveViewOfType(MarkdownView)` - Get active markdown view
- `workspace.getActiveFile()` - Get currently open file
- `workspace.on(event, callback)` - Listen to workspace events
- `workspace.getLeaf()` - Get a workspace leaf for custom views

### Editor
Text editing operations.
- `editor.getValue()` - Get full editor content
- `editor.setValue(text)` - Set full editor content
- `editor.getSelection()` - Get selected text
- `editor.replaceSelection(text)` - Replace selected text
- `editor.getCursor()` - Get cursor position
- `editor.getLine(n)` - Get specific line

### Modal
Dialog windows.
- `new Modal(app)` - Create modal
- `modal.open()` - Show modal
- `modal.close()` - Hide modal
- `modal.contentEl` - Content container element
- `modal.titleEl` - Title container element

## Plugin Lifecycle

```typescript
export default class MyPlugin extends Plugin {
  async onload() {
    // Initialize plugin
    await this.loadSettings();
    this.addCommand(...);
    this.registerView(...);
    this.addSettingTab(...);
  }

  onunload() {
    // Cleanup
  }
}
```

## Common Patterns

### Adding a Command
```typescript
this.addCommand({
  id: 'my-command',
  name: 'My Command',
  callback: () => {
    // Do something
  }
});
```

### Editor Command
```typescript
this.addCommand({
  id: 'editor-command',
  name: 'Editor Command',
  editorCallback: (editor: Editor, view: MarkdownView) => {
    const selection = editor.getSelection();
    editor.replaceSelection(selection.toUpperCase());
  }
});
```

### Settings
```typescript
interface MySettings {
  mySetting: string;
}

const DEFAULT_SETTINGS: MySettings = {
  mySetting: 'default'
}

async loadSettings() {
  this.settings = Object.assign({}, DEFAULT_SETTINGS, await this.loadData());
}

async saveSettings() {
  await this.saveData(this.settings);
}
```

### Events
```typescript
this.registerEvent(
  this.app.workspace.on('file-open', (file) => {
    console.log('File opened:', file?.path);
  })
);
```

## Useful Documentation Links

Use WebFetch with these URLs for detailed information on specific topics.
