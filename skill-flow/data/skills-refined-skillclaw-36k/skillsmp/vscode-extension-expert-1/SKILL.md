---

name: vscode-extension-expert

description: Comprehensive VSCode extension development expert that guides you through creating extensions using the official Yeoman generator tool. Provides interactive setup, configuration guidance, and development workflow support. Covers scaffolding with yo code, extension anatomy, debugging, testing, publishing, and API reference. Features primary access to complete VS Code API documentation at `@source/vscode-docs/api/` for authoritative reference. Use when starting new VSCode extensions, setting up development environment, configuring extension manifests, debugging extensions, or when mentioning VSCode extension creation, TypeScript extensions, plugin development, or editor customization. Built with official VS Code documentation, generator best practices, and complete API reference.

allowed-tools: Read, Write, Edit, Glob, Grep, Bash

---

# VSCode Extension Expert

A comprehensive guide for developing Visual Studio Code extensions using TypeScript/JavaScript. This skill is built directly from the official VSCode extension samples repository and covers everything from basic extension creation to advanced language features, custom editors, and publishing workflows.

## 🎯 Getting Started with Official Generator

The best way to create a new VS Code extension is by using the official Yeoman generator tool. This ensures you have the latest structure and allows you to configure your extension according to your preferences.

### Prerequisites

Ensure you have [Node.js](https://nodejs.org/) and [Git](https://git-scm.com/) installed.

### Creating a New Extension

**Option 1: One-time use (recommended for first-time users)**
```bash
npx --package yo --package generator-code -- yo code
```

**Option 2: Global installation (for frequent development)**
```bash
npm install --global yo generator-code
yo code
```

### Interactive Setup Process

When you run the generator, you'll be guided through these choices:

```
? What type of extension do you want to create?
❯ New Extension (TypeScript)    # Recommended for better DX
  New Extension (JavaScript)    # If you prefer plain JS
  New Color Theme
  New Language Support
  New Code Snippets
  New Keymap
  New Extension Pack
  New Language Pack (Localization)

? What's the name of your extension? MyExtension

? What's the identifier of your extension? my-extension

? What's the description of your extension? Brief description of your extension

? Initialize a git repository? Yes

? Which bundler to use?
❯ webpack    # Recommended for production
  esbuild     # Faster builds
  unbundled   # No bundling (simpler)

? Which package manager to use?
❯ npm        # Node Package Manager
  yarn        # Yarn Package Manager
  pnpm        # Performant npm
  bun         # Fast JavaScript runtime

? Do you want to open the new folder with Visual Studio Code?
❯ Open with `code`
  Open in new window
  Don't open
```

### After Creation

Once the generator completes:

1. **Open the extension folder in VS Code**
2. **Navigate to `src/extension.ts`** to see the entry point
3. **Press F5** or run **Debug: Start Debugging** to launch the Extension Development Host
4. **Test your extension** by running the Hello World command from the Command Palette (Ctrl+Shift+P)

### Development Workflow

```bash
# Navigate to your extension folder
cd my-extension

# Install dependencies (if not done by generator)
npm install

# Start development
code .

# In VS Code, press F5 to run the extension
# Make changes to src/extension.ts
# Save and reload the Extension Development Host to see changes
```

### First Development Steps

1. **Modify the Hello World command** in `src/extension.ts`
2. **Run Developer: Reload Window** in the Extension Development Host
3. **Test your changes** by running the command again
4. **Set breakpoints** to debug your extension code
5. **Check the console** for any errors or logs

## 🛠️ How to Use This Skill

This skill is designed to guide you through the VS Code extension development process. Here's how to get the most out of it:

### Starting a New Extension Project

Just say you want to create a VS Code extension, and I'll help you:

```
"I want to create a new VS Code extension"
"Help me set up a VS Code extension project"
"I need to create a TypeScript extension for VS Code"
```

I'll then:
1. Guide you through the `yo code` generator setup
2. Help you choose the right options based on your needs
3. Explain each choice and its implications
4. Help you troubleshoot any setup issues

### During Development

Once you have your extension scaffolded, I can help with:

```
"How do I add a new command to my extension?"
"My extension isn't loading, can you help me debug?"
"I want to create a webview panel"
"How do I add configuration options?"
"Help me write tests for my extension"
```

### Working with Generated Projects

I'll respect your choices from the generator:
- **Package manager**: Whether you chose npm, yarn, pnpm, or bun
- **Bundler**: Whether you chose webpack, esbuild, or unbundled
- **Language**: TypeScript or JavaScript
- **Extension type**: Commands, themes, language support, etc.

### Example Interactions

**Creating a new extension:**
```
You: I want to create a VS Code extension
Me: I'll help you create a VS Code extension using the official generator!
    Let's run: npx --package yo --package generator-code -- yo code

    When you run this, you'll see some questions. I'll help you answer them...
```

**Adding features:**
```
You: How do I add a status bar item to my extension?
Me: Great question! Let's consult the official API documentation at
    `@source/vscode-docs/api/references/vscode-api.md` for the statusBar API,
    and I'll show you how to implement it in your extension...
```

**API Reference:**
```
You: What's the correct way to create a webview?
Me: Let me check the authoritative API reference at `@source/vscode-docs/api/extension-guides/webview/`
    to get you the most accurate and up-to-date information...
```

**Debugging issues:**
```
You: My extension command isn't showing up
Me: Let's check your package.json against the manifest specification at
    `@source/vscode-docs/api/references/extension-manifest.md` and verify
    the command registration...
```

## Core Concepts

### 1. Extension Anatomy

**package.json Structure**
```json
{
  "name": "my-extension",
  "displayName": "My Extension",
  "description": "Description of my extension",
  "version": "0.0.1",
  "engines": {
    "vscode": "^1.85.0"
  },
  "categories": ["Other"],
  "activationEvents": [
    "onCommand:extension.helloWorld"
  ],
  "main": "./out/extension.js",
  "contributes": {
    "commands": [
      {
        "command": "extension.helloWorld",
        "title": "Hello World"
      }
    ]
  },
  "scripts": {
    "vscode:prepublish": "npm run compile",
    "compile": "tsc -p ./",
    "watch": "tsc -watch -p ./"
  },
  "devDependencies": {
    "@types/vscode": "^1.85.0",
    "@types/node": "16.x",
    "typescript": "^4.9.4"
  }
}
```

**Extension Entry Point (extension.ts)**
```typescript
import * as vscode from 'vscode';

// This method is called when your extension is activated
export function activate(context: vscode.ExtensionContext) {
    console.log('Extension "my-extension" is now active!');

    // Register command
    const disposable = vscode.commands.registerCommand('extension.helloWorld', () => {
        vscode.window.showInformationMessage('Hello World!');
    });

    context.subscriptions.push(disposable);
}

// This method is called when your extension is deactivated
export function deactivate() {}
```

### 2. Common Extension Patterns

**Command Registration**
```typescript
// Register multiple commands
const commands = [
    vscode.commands.registerCommand('extension.doSomething', () => {
        // Command implementation
    }),
    vscode.commands.registerCommand('extension.doSomethingElse', () => {
        // Another command
    })
];

context.subscriptions.push(...commands);
```

**Status Bar Integration**
```typescript
// Create status bar item
const statusBarItem = vscode.window.createStatusBarItem(
    vscode.StatusBarAlignment.Right,
    100
);
statusBarItem.text = '$(gear) My Extension';
statusBarItem.tooltip = 'My Extension Status';
statusBarItem.command = 'extension.toggleFeature';
statusBarItem.show();

context.subscriptions.push(statusBarItem);
```

### 3. Webview Development

**Basic Webview**
```typescript
import * as vscode from 'vscode';

export function createWebviewPanel(context: vscode.ExtensionContext) {
    const panel = vscode.window.createWebviewPanel(
        'myWebview', // viewType
        'My Webview', // title
        vscode.ViewColumn.One, // editor position
        {
            enableScripts: true,
            retainContextWhenHidden: true
        }
    );

    // Set webview HTML
    panel.webview.html = getWebviewContent(context.extensionUri);

    // Handle messages from webview
    panel.webview.onDidReceiveMessage(
        message => {
            switch (message.command) {
                case 'alert':
                    vscode.window.showInformationMessage(message.text);
                    return;
            }
        },
        undefined,
        context.subscriptions
    );

    return panel;
}

function getWebviewContent(extensionUri: vscode.Uri): string {
    return `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>My Webview</title>
</head>
<body>
    <h1>Hello from Webview!</h1>
    <button onclick="sendMessage()">Send Message</button>

    <script>
        const vscode = acquireVsCodeApi();

        function sendMessage() {
            vscode.postMessage({
                command: 'alert',
                text: 'Hello from webview!'
            });
        }
    </script>
</body>
</html>`;
}
```

**Webview View (Sidebar Panel)**
```typescript
export class SidebarWebviewProvider implements vscode.WebviewViewProvider {
    public static readonly viewType = 'my-extension.sidebar';

    private _view?: vscode.WebviewView;

    constructor(private readonly _extensionUri: vscode.Uri) {}

    public resolveWebviewView(
        webviewView: vscode.WebviewView,
        context: vscode.WebviewViewResolveContext,
        _token: vscode.CancellationToken,
    ) {
        this._view = webviewView;

        webviewView.webview.options = {
            enableScripts: true,
            localResourceRoots: [this._extensionUri]
        };

        webviewView.webview.html = this._getHtmlForWebview(webviewView.webview);

        // Handle messages
        webviewView.webview.onDidReceiveMessage(data => {
            switch (data.type) {
                case 'onInfo': {
                    vscode.window.showInformationMessage(data.value);
                    break;
                }
            }
        });
    }

    private _getHtmlForWebview(webview: vscode.Webview) {
        return `<!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Sidebar Content</title>
        </head>
        <body>
            <h1>Sidebar Content</h1>
            <button onclick="sendMessage()">Send Info</button>
            <script>
                const vscode = acquireVsCodeApi();
                function sendMessage() {
                    vscode.postMessage({
                        type: 'onInfo',
                        value: 'Hello from sidebar!'
                    });
                }
            </script>
        </body>
        </html>`;
    }
}
```

### 4. Tree View Provider

**Basic Tree View**
```typescript
export class TreeDataProvider implements vscode.TreeDataProvider<TreeItem> {
    private _onDidChangeTreeData: vscode.EventEmitter<TreeItem | undefined | null | void> = new vscode.EventEmitter<TreeItem | undefined | null | void>();
    readonly onDidChangeTreeData: vscode.Event<TreeItem | undefined | null | void> = this._onDidChangeTreeData.event;

    private treeItems: TreeItem[] = [];

    constructor() {
        this.treeItems = [
            new TreeItem('Item 1', vscode.TreeItemCollapsibleState.None),
            new TreeItem('Item 2', vscode.TreeItemCollapsibleState.None)
        ];
    }

    refresh(): void {
        this._onDidChangeTreeData.fire();
    }

    getTreeItem(element: TreeItem): vscode.TreeItem {
        return element;
    }

    getChildren(element?: TreeItem): Thenable<TreeItem[]> {
        if (!element) {
            return Promise.resolve(this.treeItems);
        }
        return Promise.resolve([]);
    }
}

class TreeItem extends vscode.TreeItem {
    constructor(
        public readonly label: string,
        public readonly collapsibleState: vscode.TreeItemCollapsibleState
    ) {
        super(label, collapsibleState);
        this.tooltip = `${this.label}-tooltip`;
        this.description = this.label;
    }
}
```

### 5. Language Features

**Code Completion Provider**
```typescript
export class CompletionItemProvider implements vscode.CompletionItemProvider {
    provideCompletionItems(
        document: vscode.TextDocument,
        position: vscode.Position,
        token: vscode.CancellationToken,
        context: vscode.CompletionContext
    ): vscode.CompletionItem[] {
        return [
            new vscode.CompletionItem('console.log', vscode.CompletionItemKind.Method),
            new vscode.CompletionItem('console.error', vscode.CompletionItemKind.Method),
            new vscode.CompletionItem('console.warn', vscode.CompletionItemKind.Method)
        ];
    }
}

// Register the provider
vscode.languages.registerCompletionItemProvider(
    'javascript',
    new CompletionItemProvider(),
    '.'
);
```

**Code Actions Provider**
```typescript
export class CodeActionProvider implements vscode.CodeActionProvider {
    provideCodeActions(
        document: vscode.TextDocument,
        range: vscode.Range,
        context: vscode.CodeActionContext,
        token: vscode.CancellationToken
    ): vscode.CodeAction[] {
        const action = new vscode.CodeAction(
            'Convert to arrow function',
            vscode.CodeActionKind.QuickFix
        );
        action.edit = new vscode.WorkspaceEdit();
        action.edit.replace(
            document.uri,
            range,
            '() => { /* converted function */ }'
        );
        return [action];
    }
}

// Register the provider
vscode.languages.registerCodeActionsProvider(
    'javascript',
    new CodeActionProvider()
);
```

**Diagnostic Provider**
```typescript
export class DiagnosticProvider {
    private diagnosticCollection: vscode.DiagnosticCollection;

    constructor() {
        this.diagnosticCollection = vscode.languages.createDiagnosticCollection('myExtension');
    }

    updateDiagnostics(document: vscode.TextDocument) {
        const diagnostics: vscode.Diagnostic[] = [];

        // Example: Check for console.log statements
        const text = document.getText();
        const regex = /console\.log\(/g;
        let match;

        while ((match = regex.exec(text)) !== null) {
            const start = document.positionAt(match.index);
            const end = document.positionAt(match.index + match[0].length);
            const range = new vscode.Range(start, end);

            const diagnostic = new vscode.Diagnostic(
                range,
                'console.log found in production code',
                vscode.DiagnosticSeverity.Warning
            );
            diagnostics.push(diagnostic);
        }

        this.diagnosticCollection.set(document.uri, diagnostics);
    }
}
```

### 6. Configuration and Settings

**Reading Configuration**
```typescript
function getConfiguration() {
    const config = vscode.workspace.getConfiguration('myExtension');
    const enabled = config.get<boolean>('enabled', true);
    const apiKey = config.get<string>('apiKey', '');
    const timeout = config.get<number>('timeout', 5000);

    return { enabled, apiKey, timeout };
}

// Listen to configuration changes
vscode.workspace.onDidChangeConfiguration(event => {
    if (event.affectsConfiguration('myExtension')) {
        // Handle configuration changes
        const newConfig = getConfiguration();
        // Update extension behavior
    }
});
```

**Configuration Schema (package.json)**
```json
{
  "contributes": {
    "configuration": {
      "title": "My Extension",
      "properties": {
        "myExtension.enabled": {
          "type": "boolean",
          "default": true,
          "description": "Enable/disable the extension"
        },
        "myExtension.apiKey": {
          "type": "string",
          "default": "",
          "description": "API key for external service",
          "scope": "application"
        },
        "myExtension.timeout": {
          "type": "number",
          "default": 5000,
          "minimum": 1000,
          "maximum": 30000,
          "description": "Timeout in milliseconds"
        }
      }
    }
  }
}
```

### 7. Testing Extensions

**Unit Tests**
```typescript
// test/extension.test.ts
import * as assert from 'assert';
import * as vscode from 'vscode';

suite('Extension Test Suite', () => {
    vscode.window.showInformationMessage('Start all tests.');

    test('Extension should be present', () => {
        assert.ok(vscode.extensions.getExtension('publisher.my-extension'));
    });

    test('Extension should activate', async () => {
        const extension = vscode.extensions.getExtension('publisher.my-extension');
        await extension?.activate();
        assert.ok(true);
    });

    test('Should register commands', async () => {
        const commands = await vscode.commands.getCommands();
        const includesCommand = commands.includes('extension.helloWorld');
        assert.ok(includesCommand);
    });
});
```

**Integration Tests**
```typescript
// test/runTest.ts
import * as path from 'path';
import { runTests } from '@vscode/test-electron';

async function main() {
    try {
        // The folder containing the Extension Manifest package.json
        const extensionDevelopmentPath = path.resolve(__dirname, '../../');

        // The path to the extension test runner script
        const extensionTestsPath = path.resolve(__dirname, './suite/index');

        // Download VS Code, unzip it and run the integration test
        await runTests({
            extensionDevelopmentPath,
            extensionTestsPath,
            launchArgs: ['--disable-extensions'] // Disable other extensions
        });
    } catch (err) {
        console.error('Failed to run tests');
        process.exit(1);
    }
}

main();
```

### 8. Publishing Extensions

**Build Scripts (package.json)**
```json
{
  "scripts": {
    "vscode:prepublish": "npm run compile",
    "compile": "tsc -p ./",
    "package": "vsce package",
    "publish": "vsce publish",
    "version": "npm run compile && vsce package"
  },
  "devDependencies": {
    "@vscode/test-electron": "^2.3.8",
    "@vscode/vsce": "^2.21.1"
  }
}
```

**Publishing Commands**
```bash
# Install vsce tool
npm install -g @vscode/vsce

# Create publisher account (one-time)
vsce create-publisher your-publisher-name

# Package extension
vsce package

# Publish to marketplace
vsce publish

# Publish specific version
vsce publish 1.0.1
```

## Advanced Topics

### 1. Multi-root Workspace Support

```typescript
// Handle multi-root workspaces
function getWorkspaceFolders() {
    const folders = vscode.workspace.workspaceFolders;
    if (!folders) {
        vscode.window.showErrorMessage('No folder opened');
        return [];
    }
    return folders;
}

// Listen to workspace folder changes
vscode.workspace.onDidChangeWorkspaceFolders(event => {
    event.added.forEach(folder => {
        console.log(`Folder added: ${folder.name}`);
    });
    event.removed.forEach(folder => {
        console.log(`Folder removed: ${folder.name}`);
    });
});
```

### 2. Terminal Integration

**Create Terminal**
```typescript
export function createTerminal() {
    const terminal = vscode.window.createTerminal({
        name: 'My Extension Terminal',
        cwd: vscode.workspace.workspaceFolders?.[0]?.uri.fsPath
    });

    terminal.sendText('echo "Hello from terminal!"');
    terminal.show();
    return terminal;
}

// Terminal process provider (for custom shells)
export class CustomTerminal implements vscode.Pseudoterminal {
    private writeEmitter = new vscode.EventEmitter<string>();
    onDidWrite: vscode.Event<string> = this.writeEmitter.event;

    private closeEmitter = new vscode.EventEmitter<number>();
    onDidClose?: vscode.Event<number> = this.closeEmitter.event;

    private open = false;

    open(): void {
        this.open = true;
        this.writeEmitter.fire('Custom terminal started\r\n');
    }

    close(): void {
        this.open = false;
        this.closeEmitter.fire(0);
    }

    handleInput(data: string): void {
        if (data === '\r' || data === '\n') {
            this.writeEmitter.fire('\r\n');
        } else {
            this.writeEmitter.fire(data);
        }
    }
}
```

### 3. File System Provider

```typescript
export class CustomFileSystemProvider implements vscode.FileSystemProvider {
    private _onDidChangeFile: vscode.EventEmitter<vscode.FileChangeEvent[]> = new vscode.EventEmitter<vscode.FileChangeEvent[]>();
    onDidChangeFile: vscode.Event<vscode.FileChangeEvent[]> = this._onDidChangeFile.event;

    watch(uri: vscode.Uri): vscode.Disposable {
        // Return a disposable that stops watching
        return new vscode.Disposable(() => {});
    }

    stat(uri: vscode.Uri): vscode.FileStat | Thenable<vscode.FileStat> {
        return {
            type: vscode.FileType.File,
            ctime: Date.now(),
            mtime: Date.now(),
            size: 1024
        };
    }

    readDirectory(uri: vscode.Uri): [string, vscode.FileType][] | Thenable<[string, vscode.FileType][]> {
        return [
            ['file1.txt', vscode.FileType.File],
            ['folder1', vscode.FileType.Directory]
        ];
    }

    readFile(uri: vscode.Uri): Uint8Array | Thenable<Uint8Array> {
        return new Uint8Array(Buffer.from('Hello from custom file system'));
    }

    writeFile(uri: vscode.Uri, content: Uint8Array, options: { create: boolean; overwrite: boolean; }): void | Thenable<void> {
        // Handle file writing
    }

    delete(uri: vscode.Uri): void | Thenable<void> {
        // Handle file deletion
    }

    rename(oldUri: vscode.Uri, newUri: vscode.Uri, options: { overwrite: boolean; }): void | Thenable<void> {
        // Handle file renaming
    }

    createDirectory(uri: vscode.Uri): void | Thenable<void> {
        // Handle directory creation
    }
}
```

## Best Practices

### 1. Performance Optimization

**Lazy Loading**
```typescript
export function activate(context: vscode.ExtensionContext) {
    // Lazy load expensive modules
    const getExpensiveModule = () => {
        return require('./expensive-module');
    };

    const disposable = vscode.commands.registerCommand('extension.expensiveCommand', () => {
        const module = getExpensiveModule();
        module.doExpensiveOperation();
    });

    context.subscriptions.push(disposable);
}
```

**Efficient Data Structures**
```typescript
// Use efficient data structures for large datasets
class EfficientDataManager {
    private cache = new Map<string, any>();
    private disposables: vscode.Disposable[] = [];

    constructor() {
        // Clean up cache when documents change
        this.disposables.push(
            vscode.workspace.onDidChangeTextDocument(event => {
                this.cache.delete(event.document.uri.toString());
            })
        );
    }

    getData(uri: vscode.Uri): any {
        const key = uri.toString();
        if (!this.cache.has(key)) {
            this.cache.set(key, this.computeData(uri));
        }
        return this.cache.get(key);
    }

    dispose() {
        this.disposables.forEach(d => d.dispose());
    }
}
```

### 2. Error Handling

**Robust Error Handling**
```typescript
export async function safeCommand() {
    try {
        const result = await vscode.window.showInputBox({
            prompt: 'Enter something',
            validateInput: value => {
                if (!value || value.trim() === '') {
                    return 'Please enter a valid value';
                }
                return null;
            }
        });

        if (result) {
            // Process input
            vscode.window.showInformationMessage(`Processing: ${result}`);
        }
    } catch (error) {
        console.error('Command failed:', error);
        vscode.window.showErrorMessage(`Command failed: ${error.message}`);
    }
}
```

### 3. User Experience

**Progress Indicators**
```typescript
export async function longRunningOperation() {
    await vscode.window.withProgress({
        location: vscode.ProgressLocation.Notification,
        title: 'Long Running Operation',
        cancellable: true
    }, async (progress, token) => {
        for (let i = 0; i < 100; i++) {
            if (token.isCancellationRequested) {
                vscode.window.showInformationMessage('Operation cancelled');
                return;
            }

            progress.report({
                increment: 1,
                message: `Processing item ${i + 1}/100`
            });

            // Simulate work
            await new Promise(resolve => setTimeout(resolve, 100));
        }
    });

    vscode.window.showInformationMessage('Operation completed!');
}
```

## 📚 Official Resources and Reference Materials

### 🎯 Primary API Documentation (Authoritative Reference)
**Complete VS Code API Documentation**: `@source/vscode-docs/api/` - **FIRST REFERENCE FOR ALL API NEEDS**

**Core API Reference**:
- **Extension API**: `@source/vscode-docs/api/references/vscode-api.md` - Complete VS Code API reference
- **Extension Manifest**: `@source/vscode-docs/api/references/extension-manifest.md` - Package.json schema and options
- **Contribution Points**: `@source/vscode-docs/api/references/contribution-points.md` - All contribution points reference
- **Activation Events**: `@source/vscode-docs/api/references/activation-events.md` - Extension activation options

**Development Guides**:
- **Getting Started**: `@source/vscode-docs/api/get-started/` - Complete beginner's guide
- **Extension Guides**: `@source/vscode-docs/api/extension-guides/` - Detailed feature implementation guides
- **Working with Extensions**: `@source/vscode-docs/api/working-with-extensions/` - Testing, debugging, publishing
- **UX Guidelines**: `@source/vscode-docs/api/ux-guidelines/` - Extension design best practices

**Extension Capabilities**:
- **Theming**: `@source/vscode-docs/api/extension-capabilities/theming.md` - Theme development
- **Extending Workbench**: `@source/vscode-docs/api/extension-capabilities/extending-workbench.md` - UI extensions
- **Language Extensions**: `@source/vscode-docs/api/language-extensions/` - Language server and syntax support

### 🎯 Primary Development Workflow (Recommended)
1. **Create with Generator**: Use `yo code` to scaffold your extension with your preferred settings
2. **Development**: Modify `src/extension.ts` and other files in your generated project
3. **API Reference**: Consult `@source/vscode-docs/api/` for authoritative API documentation
4. **Testing**: Press F5 to test in Extension Development Host
5. **Debugging**: Use VS Code's built-in debugger and console
6. **Publishing**: Use `vsce` to package and publish your extension

### 📖 Code Examples (for learning specific implementations)
When you need to see how specific features are implemented, refer to these official examples:

**Core Extension Features**:
- **Commands**: `@source/vscode-extension-samples/command-sample/` - Command registration and handling
- **Tree View**: `@source/vscode-extension-samples/tree-view-sample/` - Custom tree views
- **Language Features**: `@source/vscode-extension-samples/completions-sample/` - Code completion
- **Code Actions**: `@source/vscode-extension-samples/code-actions-sample/` - Quick fixes and refactorings
- **Status Bar**: `@source/vscode-extension-samples/statusbar-sample/` - Status bar integration

**UI Development**:
- **Web Views**: `@source/vscode-extension-samples/webview-sample/` - Custom UI panels
- **Webview Views**: `@source/vscode-extension-samples/webview-view-sample/` - Sidebar webviews
- **Custom Editors**: `@source/vscode-extension-samples/custom-editor-sample/` - Custom file editors

**Advanced Features**:
- **Language Features**: `@source/vscode-extension-samples/lsp-sample/` - Language Server Protocol
- **Terminal**: `@source/vscode-extension-samples/terminal-sample/` - Terminal integration
- **Configuration**: `@source/vscode-extension-samples/configuration-sample/` - Extension settings
- **Authentication**: `@source/vscode-extension-samples/authenticationprovider-sample/` - Auth providers

**Testing and Development**:
- **Testing**: `@source/vscode-extension-samples/helloworld-test-sample/` - Extension testing patterns
- **Multi-root Workspace**: `@source/vscode-extension-samples/basic-multi-root-sample/` - Workspace handling

### 🔗 External Documentation (Supplementary)
- **Extension API**: [VS Code Extension API Reference](https://code.visualstudio.com/api/references/vscode-api)
- **Contribution Points**: [Extension Manifest Reference](https://code.visualstudio.com/api/references/contribution-points)
- **Extension Guides**: [Complete Extension Development Guide](https://code.visualstudio.com/api/extension-guides/overview)
- **UX Guidelines**: [Extension UX Guidelines](https://code.visualstudio.com/api/ux-guidelines/overview)

> **💡 Priority Order**: Always consult `@source/vscode-docs/api/` first for API documentation, then use code samples for implementation examples. The local documentation is the most authoritative and up-to-date reference.

## Common Extension Templates

### Basic Command Extension
```typescript
import * as vscode from 'vscode';

export function activate(context: vscode.ExtensionContext) {
    const disposable = vscode.commands.registerCommand('extension.myCommand', () => {
        vscode.window.showInformationMessage('Command executed!');
    });

    context.subscriptions.push(disposable);
}
```

### Language Server Extension
```typescript
import * as vscode from 'vscode';
import { LanguageClient, LanguageClientOptions } from 'vscode-languageclient/node';

export function activate(context: vscode.ExtensionContext) {
    const serverOptions: ServerOptions = {
        command: 'path/to/server',
        args: []
    };

    const clientOptions: LanguageClientOptions = {
        documentSelector: [{ scheme: 'file', language: 'mylang' }]
    };

    const client = new LanguageClient(
        'myLanguageServer',
        'My Language Server',
        serverOptions,
        clientOptions
    );

    client.start();
}
```

## Troubleshooting

**Common Issues:**
- Extension not loading: Check `engines.vscode` version compatibility
- Commands not registering: Verify command IDs match in package.json and extension.ts
- Activation issues: Check activationEvents in package.json
- TypeScript errors: Ensure @types/vscode matches VSCode version

**Debug Techniques:**
- Use `console.log()` for debugging (appears in Developer Tools console)
- Enable debug mode: Help > Toggle Developer Tools
- Test with different VSCode versions
- Check extension host logs: View > Output > Extension Host

**Performance Debugging:**
- Profile startup time with `--inspect-extensions` flag
- Use `vscode.window.withProgress()` for long operations
- Implement proper cleanup in deactivate function
- Monitor memory usage with heap snapshots

## Quick Reference

### Essential APIs
- `vscode.commands.registerCommand()` - Register commands
- `vscode.window.createWebviewPanel()` - Create webviews
- `vscode.window.createTreeView()` - Create tree views
- `vscode.languages.registerCompletionItemProvider()` - Add completions
- `vscode.languages.registerCodeActionsProvider()` - Add code actions
- `vscode.workspace.getConfiguration()` - Read settings
- `vscode.window.createStatusBarItem()` - Status bar items
- `vscode.window.createTerminal()` - Terminal integration

### Common Contribution Points
- `contributes.commands` - Register commands
- `contributes.views` - Add view containers
- `contributes.configuration` - Add settings
- `contributes.languages` - Define new languages
- `contributes grammars` - Add syntax highlighting
- `contributes.themes` - Custom themes
- `contributes.keybindings` - Keyboard shortcuts

### Essential Commands
```bash
# Create new extension
npx --package yo --package generator-code -- yo code

# Or install globally
npm install --global yo generator-code
yo code

# Development workflow
npm run compile          # Compile TypeScript
npm run watch           # Watch for changes
npm test                # Run tests
npm run package         # Package extension
vsce publish            # Publish to marketplace
```

### Essential API Documentation Access
```bash
# Quick API reference lookup
@source/vscode-docs/api/references/vscode-api.md          # Complete API reference
@source/vscode-docs/api/references/extension-manifest.md  # Package.json schema
@source/vscode-docs/api/references/contribution-points.md # All contributions
@source/vscode-docs/api/extension-guides/                 # Implementation guides
```

### Package Manager Commands
```bash
# npm
npm install <package>
npm run <script>

# yarn
yarn add <package>
yarn <script>

# pnpm
pnpm add <package>
pnpm <script>

# bun
bun add <package>
bun <script>
```

### Common Debugging Shortcuts
- `F5` - Start debugging
- `Ctrl+Shift+P` - Open Command Palette
- `Ctrl+Shift+I` - Open Developer Tools
- `Ctrl+R` - Reload Extension Development Host
- `Ctrl+Shift+D` - Open Debug view

This skill provides comprehensive VSCode extension development capabilities, guiding you through the official generator workflow and providing expert assistance for building powerful, production-ready extensions with your preferred tools and configuration.